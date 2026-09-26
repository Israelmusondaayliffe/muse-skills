"""Ported tests for the Hatch workspace skill adaptation of practice-compiler.

Layout: tests/<this file> resolves the skill root as parents[1], matching the
skill directory structure (SKILL.md, scripts/, tests/, fixtures live at
tests/fixtures/).
"""

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "practice_compiler.py"
SPEC = importlib.util.spec_from_file_location("practice_compiler", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class PracticeCompilerTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = Path(__file__).resolve().parent / "fixtures" / "sessions"

    def _tmpdir(self):
        """Temp dir under home so session files are not auto-classified synthetic
        (the scanner treats fixture/test/tmp path parts as synthetic sources)."""
        return tempfile.TemporaryDirectory(dir=str(Path.home()))

    def test_redacts_secrets_and_email(self):
        value = MODULE.redact(
            "owner@example.com token=sk-test-secret "
            "OPENAI_API_KEY=supersecret123 ghp_abcdefghijklmnopqrstuvwxyz123456"
        )
        self.assertNotIn("owner@example.com", value)
        self.assertNotIn("sk-test-secret", value)
        self.assertNotIn("supersecret123", value)
        self.assertNotIn("ghp_", value)

    def test_extracts_actual_command_not_plain_mention(self):
        signals, errors = MODULE.extract_signals(self.fixtures / "session-a.jsonl")
        self.assertFalse(errors)
        kinds = [item["kind"] for item in signals]
        self.assertIn("executed-command", kinds)
        self.assertIn("command-failure", kinds)

    def test_repeated_command_becomes_proposal(self):
        signals = []
        for name in ("session-a.jsonl", "session-b.jsonl"):
            found, _ = MODULE.extract_signals(self.fixtures / name)
            signals.extend(found)
        proposals = MODULE.build_proposals(signals, 2)
        self.assertTrue(any(item["signal_class"] == "repeated-task" for item in proposals))
        self.assertTrue(all(isinstance(item["evidence"][0], dict) for item in proposals))
        self.assertTrue(all("citation" in item["evidence"][0] for item in proposals))

    def test_direct_user_extraction_ignores_injected_nested_user_text(self):
        event = {
            "type": "session_meta",
            "payload": {
                "base_instructions": {
                    "role": "user",
                    "content": "No, change every file.",
                }
            },
        }
        self.assertEqual([], MODULE.direct_user_text(event))
        wrapper = {
            "type": "response_item",
            "payload": {"role": "user", "content": "<recommended_plugins>injected</recommended_plugins>"},
        }
        self.assertEqual([], MODULE.direct_user_text(wrapper))

    def test_later_user_message_is_follow_up(self):
        self.assertEqual(
            "follow-up-instruction",
            MODULE.classify_user_signal("Publish the verified result.", 1),
        )

    def test_semantic_variants_group_across_sessions(self):
        base = {"source_class": "user"}
        signals = [
            MODULE.signal(
                "recurring-feedback", Path("/tmp/a.jsonl"), 3,
                "Keep changes surgical and do not redesign approved parts.",
                MODULE.semantic_key("Keep changes surgical and do not redesign approved parts."),
                {**base, "session_id": "a"},
            ),
            MODULE.signal(
                "recurring-feedback", Path("/tmp/b.jsonl"), 8,
                "Do not redesign the approved parts. Keep the change surgical.",
                MODULE.semantic_key("Do not redesign the approved parts. Keep the change surgical."),
                {**base, "session_id": "b"},
            ),
        ]
        proposals = MODULE.build_proposals(signals, 2)
        self.assertEqual(1, len(proposals))
        self.assertEqual("recurring-feedback", proposals[0]["signal_class"])

    def test_fixture_source_is_classified_synthetic(self):
        metadata, errors = MODULE.session_metadata(self.fixtures / "session-a.jsonl")
        self.assertFalse(errors)
        self.assertEqual("synthetic", metadata["source_class"])

    def test_claude_sidechain_is_never_default_user_source(self):
        from argparse import Namespace
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name, extra in [("child.jsonl", {"isSidechain": True}), ("subagents/agent-x.jsonl", {})]:
                path = root / name
                path.parent.mkdir(exist_ok=True)
                path.write_text(json.dumps({"type": "user", "timestamp": "2026-09-08T12:00:00Z", "message": {"role": "user", "content": "Always use my private configuration"}, **extra}) + "\n")
                meta, errors = MODULE.session_metadata(path, "claude")
                self.assertFalse(errors)
                self.assertEqual(meta["source_class"], "subagent")
            args = Namespace(sessions_root=[str(root)], adapter="claude", since="2026-09-08", until="2026-09-08", timezone="UTC", source_class=["user"], limit=20)
            selected, counts, errors = MODULE.select_files(args)
            self.assertEqual(selected, [])
            self.assertEqual(counts["subagent"], 2)
            self.assertFalse(errors)

    def test_scan_cursor_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = type("Args", (), {
                "sessions_root": [str(self.fixtures)], "limit": 20,
                "min_occurrences": 2, "scan_id": "first", "state_root": str(root),
                "source_class": ["synthetic"], "since": None, "until": None, "stdout": False,
                "timezone": "UTC",
            })()
            first = MODULE.cmd_scan(args)
            args.scan_id = "second"
            second = MODULE.cmd_scan(args)
            self.assertEqual(3, first["files_processed"])
            self.assertEqual(0, second["files_processed"])
            self.assertEqual(3, second["files_skipped"])

    def test_rejected_proposal_stays_rejected_on_rescan(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = type("Args", (), {
                "sessions_root": [str(self.fixtures)], "limit": 20,
                "min_occurrences": 2, "scan_id": "first", "state_root": str(root),
                "source_class": ["synthetic"], "since": None, "until": None, "stdout": False,
                "timezone": "UTC",
            })()
            MODULE.cmd_scan(args)
            proposal = MODULE.read_proposals(root)[0]
            decision_args = type("Args", (), {
                "proposal_id": proposal["proposal_id"], "decision": "reject",
                "note": "one-off", "state_root": str(root)
            })()
            MODULE.cmd_decide(decision_args)
            cursor = MODULE.load_json(root / "cursor.json")
            cursor["processed"] = {}
            MODULE.atomic_json(root / "cursor.json", cursor)
            args.scan_id = "second"
            MODULE.cmd_scan(args)
            refreshed = MODULE.load_json(root / "proposals" / f"{proposal['proposal_id']}.json")
            self.assertEqual(refreshed["status"], "rejected")
            self.assertFalse((root / "handoffs" / f"{proposal['proposal_id']}.json").exists())

    def test_stdout_mode_is_read_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "state"
            args = type("Args", (), {
                "sessions_root": [str(self.fixtures)], "limit": 20,
                "min_occurrences": 2, "scan_id": "preview", "state_root": str(root),
                "source_class": ["synthetic"], "since": "2020-01-01", "until": "2030-01-01",
                "stdout": True, "timezone": "UTC",
            })()
            result = MODULE.cmd_scan(args)
            self.assertEqual("stdout", result["mode"])
            self.assertIn("proposal_records", result)
            self.assertFalse(root.exists())

    def test_date_only_boundary_uses_requested_timezone(self):
        boundary = MODULE.parse_boundary("2026-07-27", end=True, timezone_name="America/New_York")
        self.assertEqual("2026-07-28T03:59:59.999999+00:00", boundary.isoformat())

    def test_persistent_scans_accumulate_repetition(self):
        with self._tmpdir() as temp:
            root = Path(temp)
            first_root = root / "first"
            second_root = root / "second"
            first_root.mkdir()
            second_root.mkdir()
            (first_root / "one.jsonl").write_text(
                '{"type":"response_item","payload":{"role":"user","content":"Keep approved changes surgical."}}\n'
            )
            (second_root / "two.jsonl").write_text(
                '{"type":"response_item","payload":{"role":"user","content":"Keep the approved change surgical."}}\n'
            )
            args = type("Args", (), {
                "sessions_root": [str(first_root)], "limit": 20,
                "min_occurrences": 2, "scan_id": "first", "state_root": str(root / "state"),
                "source_class": ["user"], "since": None, "until": None, "stdout": False,
                "timezone": "UTC",
            })()
            MODULE.cmd_scan(args)
            self.assertEqual([], MODULE.read_proposals(root / "state"))
            args.sessions_root = [str(second_root)]
            args.scan_id = "second"
            MODULE.cmd_scan(args)
            proposals = MODULE.read_proposals(root / "state")
            self.assertEqual(1, len(proposals))
            self.assertEqual(2, proposals[0]["occurrences"])

    def test_cross_scan_semantic_variant_keeps_proposal_id(self):
        with self._tmpdir() as temp:
            root = Path(temp)
            first_root = root / "first"
            second_root = root / "second"
            first_root.mkdir()
            second_root.mkdir()
            first_text = "Keep approved changes surgical and preserve structure."
            second_text = "Keep approved changes surgical and preserve layout."
            self.assertGreater(
                MODULE.jaccard(MODULE.semantic_tokens(first_text), MODULE.semantic_tokens(second_text)),
                0.5,
            )
            for index in range(2):
                (first_root / f"first-{index}.jsonl").write_text(
                    json.dumps({"type": "response_item", "payload": {"role": "user", "content": first_text}}) + "\n"
                )
                (second_root / f"second-{index}.jsonl").write_text(
                    json.dumps({"type": "response_item", "payload": {"role": "user", "content": second_text}}) + "\n"
                )
            args = type("Args", (), {
                "sessions_root": [str(first_root)], "limit": 20,
                "min_occurrences": 2, "scan_id": "first", "state_root": str(root / "state"),
                "source_class": ["user"], "since": None, "until": None, "stdout": False,
                "timezone": "UTC",
            })()
            MODULE.cmd_scan(args)
            first_id = MODULE.read_proposals(root / "state")[0]["proposal_id"]
            args.sessions_root = [str(second_root)]
            args.scan_id = "second"
            MODULE.cmd_scan(args)
            proposals = MODULE.read_proposals(root / "state")
            registry = MODULE.load_json(root / "state" / "proposal-registry.json")
            self.assertEqual([first_id], [item["proposal_id"] for item in proposals])
            self.assertEqual([first_id], list(registry["proposals"]))

    def test_host_adapters_require_explicit_source_roots(self):
        missing = type("Args", (), {"sessions_root": None, "adapter": "codex"})()
        with self.assertRaises(MODULE.CompilerError):
            MODULE.session_roots(missing)
        codex = type("Args", (), {"sessions_root": ["/tmp/selected-codex"], "adapter": "codex"})()
        claude = type("Args", (), {"sessions_root": ["/tmp/selected-claude"], "adapter": "claude"})()
        muse = type("Args", (), {"sessions_root": ["/tmp/selected-muse-exports"], "adapter": "muse"})()
        self.assertEqual("selected-codex", MODULE.session_roots(codex)[0].name)
        self.assertEqual("selected-claude", MODULE.session_roots(claude)[0].name)
        self.assertEqual("selected-muse-exports", MODULE.session_roots(muse)[0].name)

    def test_learning_signal_classes_cover_cost_tools_repairs_and_methods(self):
        self.assertEqual("cost-decision", MODULE.classify_user_signal("Stop wasting tokens on low-value tests.", 1))
        self.assertEqual("missed-tool", MODULE.classify_user_signal("Why haven't you used computer use?", 1))
        self.assertEqual("repeated-repair", MODULE.classify_user_signal("Fix the render again.", 1))
        self.assertEqual("user-method", MODULE.classify_user_signal("I would use the image as a style anchor.", 1))

    def test_design_exports_are_bounded_deduplicated_and_proposal_only(self):
        payload = {
            "schema_version": "1.0",
            "records": [
                {"source_type": "design-neutral-export", "fingerprint": "a" * 64,
                 "project_id": "project-" + "1" * 20, "signal_class": "cost-decision",
                 "summary": "Stop low value reruns", "impact": "cost", "method": None,
                 "created_at": "2026-09-01T10:00:00Z"},
                {"source_type": "design-neutral-export", "fingerprint": "b" * 64,
                 "project_id": "project-" + "2" * 20, "signal_class": "cost-decision",
                 "summary": "Stop low value reruns", "impact": "cost", "method": None,
                 "created_at": "2026-09-01T11:00:00Z"},
            ],
        }
        since = MODULE.parse_boundary("2026-09-01")
        until = MODULE.parse_boundary("2026-09-01", end=True)
        signals = MODULE.design_export_signals(payload, since, until)
        proposals = MODULE.build_proposals(signals, 2)
        self.assertEqual(1, len(proposals))
        self.assertEqual("staged", proposals[0]["status"])
        self.assertTrue(all(item["source_class"] == "design-export" for item in proposals[0]["evidence"]))
        payload["records"][0]["exact_quote"] = "raw quote"
        with self.assertRaises(MODULE.CompilerError):
            MODULE.design_export_signals(payload, since, until)

    # ---- Hatch adaptation tests ----

    def test_muse_adapter_reads_session_meta_and_marks_user_source(self):
        # Copy the fixture out of the fixtures/ tree so it is not auto-classified synthetic.
        with self._tmpdir() as temp:
            path = Path(temp) / "muse-session-1.jsonl"
            path.write_text((self.fixtures / "session-muse.jsonl").read_text(encoding="utf-8"))
            metadata, errors = MODULE.session_metadata(path, "muse")
            self.assertFalse(errors)
            self.assertEqual("muse-session-1", metadata["session_id"])
            self.assertEqual("user", metadata["source_class"])
            signals, errors = MODULE.extract_signals(path, "muse")
            self.assertFalse(errors)
            kinds = {item["kind"] for item in signals}
            self.assertIn("recurring-feedback", kinds)
            self.assertIn("executed-command", kinds)
            self.assertIn("command-failure", kinds)

    def test_muse_adapter_respects_subagent_thread_source(self):
        with self._tmpdir() as temp:
            path = Path(temp) / "child.jsonl"
            path.write_text(
                json.dumps({"type": "session_meta", "payload": {"id": "child", "thread_source": "subagent", "timestamp": "2026-09-20T10:00:00Z"}}) + "\n"
                + json.dumps({"type": "user_message", "payload": {"content": "Check the logs."}, "timestamp": "2026-09-20T10:01:00Z"}) + "\n"
            )
            metadata, errors = MODULE.session_metadata(path, "muse")
            self.assertFalse(errors)
            self.assertEqual("subagent", metadata["source_class"])

    def test_default_state_root_lives_outside_skill_package(self):
        with self._isolated_home() as home:
            default = MODULE.root_path(None)
            self.assertEqual((home / "workspace" / "practice-compiler" / "state").resolve(), default)
            self.assertNotIn(MODULE.SKILL_DIR, default.parents)
            with tempfile.TemporaryDirectory() as temp:
                os.environ["PRACTICE_COMPILER_STATE"] = temp
                self.assertEqual(Path(temp).resolve(), MODULE.root_path(None))

    # ---- state relocation: legacy in-package state is kept, migrated, or reported ----

    def _isolated_home(self, legacy=None):
        """Point HOME (and optionally the legacy root) at a temp dir; restore afterwards."""
        test = self

        class Home:
            def __enter__(self):
                self.temp = tempfile.TemporaryDirectory()
                self.saved = {key: os.environ.get(key) for key in ("HOME", "PRACTICE_COMPILER_STATE", "PRACTICE_COMPILER_LEGACY_STATE")}
                os.environ["HOME"] = self.temp.name
                os.environ.pop("PRACTICE_COMPILER_STATE", None)
                if legacy is None:
                    os.environ.pop("PRACTICE_COMPILER_LEGACY_STATE", None)
                else:
                    os.environ["PRACTICE_COMPILER_LEGACY_STATE"] = str(Path(self.temp.name) / legacy)
                return Path(self.temp.name).resolve()

            def __exit__(self, *exc):
                for key, value in self.saved.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value
                self.temp.cleanup()

        return Home()

    @staticmethod
    def _write_records(root, proposal_id, status="staged"):
        MODULE.atomic_json(root / "proposals" / f"{proposal_id}.json", {"proposal_id": proposal_id, "status": status})
        MODULE.atomic_json(root / "cursor.json", {"schema_version": 2, "processed": {}})

    def test_legacy_state_is_read_but_never_forked_before_migration(self):
        with self._isolated_home(legacy="old-package/hidden_files/state") as home:
            legacy = home / "old-package" / "hidden_files" / "state"
            self._write_records(legacy, "pc-legacy")
            status = MODULE.state_status()
            self.assertEqual("migrate", status["action"])
            self.assertEqual(legacy, MODULE.root_path(None))
            with self.assertRaises(MODULE.CompilerError):
                MODULE.root_path(None, write=True)
            self.assertFalse((home / "workspace" / "practice-compiler" / "state").exists())

    def test_migrate_copies_forward_and_keeps_legacy(self):
        with self._isolated_home(legacy="old/state") as home:
            legacy = home / "old" / "state"
            self._write_records(legacy, "pc-legacy")
            before = MODULE.tree_digest(legacy)
            result = MODULE.migrate_state()
            target = home / "workspace" / "practice-compiler" / "state"
            self.assertTrue(result["migrated"])
            self.assertEqual(before, MODULE.tree_digest(target))
            self.assertEqual(before, MODULE.tree_digest(legacy))
            self.assertTrue((legacy / "proposals" / "pc-legacy.json").exists())
            self.assertEqual(target, MODULE.root_path(None, write=True))
            # New writes after migration are not mistaken for a conflict.
            self._write_records(target, "pc-new")
            self.assertEqual("none", MODULE.state_status()["action"])

    def test_conflict_is_reported_and_nothing_is_overwritten(self):
        with self._isolated_home(legacy="old/state") as home:
            legacy = home / "old" / "state"
            target = home / "workspace" / "practice-compiler" / "state"
            self._write_records(legacy, "pc-legacy")
            self._write_records(target, "pc-current", status="approved")
            legacy_before = MODULE.tree_digest(legacy)
            target_before = MODULE.tree_digest(target)
            status = MODULE.state_status()
            self.assertEqual("conflict", status["action"])
            self.assertEqual(target, MODULE.root_path(None))
            with self.assertRaises(MODULE.CompilerError):
                MODULE.root_path(None, write=True)
            with self.assertRaises(MODULE.CompilerError):
                MODULE.migrate_state()
            self.assertEqual(legacy_before, MODULE.tree_digest(legacy))
            self.assertEqual(target_before, MODULE.tree_digest(target))
            # An explicit root is the user's resolution and is honored.
            self.assertEqual(legacy, MODULE.root_path(str(legacy), write=True))

    def test_identical_state_and_legacy_is_not_a_conflict(self):
        with self._isolated_home(legacy="old/state") as home:
            legacy = home / "old" / "state"
            target = home / "workspace" / "practice-compiler" / "state"
            self._write_records(legacy, "pc-same")
            for path in MODULE.state_files(legacy):
                destination = target / path.relative_to(legacy)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(path.read_bytes())
            self.assertEqual("none", MODULE.state_status()["action"])

    def test_default_legacy_location_under_workspace_skills_is_detected(self):
        with self._isolated_home() as home:
            legacy = home / "workspace" / "skills" / "practice-compiler" / "hidden_files" / "state"
            self._write_records(legacy, "pc-installed")
            status = MODULE.state_status()
            self.assertEqual("migrate", status["action"])
            self.assertIn(str(legacy), [item["path"] for item in status["legacy_roots"]])

    def test_preferred_handoff_owner_maps_to_hatch_workspace_skills(self):
        self.assertEqual("capability-operator", MODULE.preferred_handoff_owner("skill"))
        self.assertEqual("skill-creator", MODULE.preferred_handoff_owner("new-skill"))
        self.assertEqual("harness-engineering", MODULE.preferred_handoff_owner("agents-md"))
        self.assertEqual("harness-engineering", MODULE.preferred_handoff_owner("hook"))
        self.assertEqual("harness-engineering", MODULE.preferred_handoff_owner("tool-cli"))
        self.assertEqual("continuity-vault", MODULE.preferred_handoff_owner("durable-knowledge"))
        self.assertIsNone(MODULE.preferred_handoff_owner("discard"))

    def test_approved_proposal_handoff_disclaims_destination_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # A "fixtures" path part keeps the copies classified synthetic on every
            # platform; the window matches test_stdout_mode_is_read_only.
            (root / "fixtures").mkdir()
            for name in ("session-a.jsonl", "session-b.jsonl"):
                (root / "fixtures" / name).write_text((self.fixtures / name).read_text(encoding="utf-8"))
            scan_args = type("Args", (), {
                "sessions_root": [str(root / "fixtures")], "limit": 20,
                "min_occurrences": 2, "scan_id": "s1", "state_root": str(root / "state"),
                "source_class": ["synthetic"], "since": "2020-01-01", "until": "2030-01-01", "stdout": False,
                "timezone": "UTC",
            })()
            MODULE.cmd_scan(scan_args)
            proposal = MODULE.read_proposals(root / "state")[0]
            decide_args = type("Args", (), {
                "proposal_id": proposal["proposal_id"], "decision": "approve",
                "note": "approved for handoff", "state_root": str(root / "state"),
                "available_owner": ["capability-operator"],
            })()
            result = MODULE.cmd_decide(decide_args)
            self.assertEqual("capability-operator", result["selected_owner"])
            handoff = MODULE.load_json(Path(result["handoff"]))
            self.assertIn("does not authorize", handoff["authority_boundary"])
            self.assertEqual("approved", MODULE.load_json(root / "state" / "proposals" / f"{proposal['proposal_id']}.json")["status"])


if __name__ == "__main__":
    unittest.main()
