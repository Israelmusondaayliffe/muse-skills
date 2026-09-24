import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("loop_observatory", ROOT.parent / "bin" / "loop_observatory.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class LoopObservatoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = os.environ.get("LOOP_OBSERVATORY_HOME")
        os.environ["LOOP_OBSERVATORY_HOME"] = self.temp.name

    def tearDown(self):
        if self.previous is None:
            os.environ.pop("LOOP_OBSERVATORY_HOME", None)
        else:
            os.environ["LOOP_OBSERVATORY_HOME"] = self.previous
        self.temp.cleanup()

    def test_loopkit_ingestion_is_idempotent_and_read_only(self):
        source = Path(self.temp.name) / "fixture-loopkit"
        shutil.copytree(ROOT / "fixtures" / "loopkit-run", source)
        before = MODULE.tree_hash(source)
        first = MODULE.ingest(source)
        second = MODULE.ingest(source)
        self.assertEqual(first["counts"]["ingested"], 1)
        self.assertEqual(second["counts"]["unchanged"], 1)
        self.assertEqual(before, MODULE.tree_hash(source))
        self.assertEqual(MODULE.records()[0]["run_id"], "lk-001")

    def test_registered_graph_and_false_failure(self):
        source = Path(self.temp.name) / "graph"
        shutil.copytree(ROOT / "fixtures" / "graph-run", source)
        MODULE.register_root(source)
        result = MODULE.ingest(Path(self.temp.name) / "missing-loopkit")
        self.assertEqual(result["counts"]["ingested"], 1)
        audit = MODULE.audit()
        self.assertEqual(len(audit["false_failures"]), 1)

    def test_missing_cost_and_acceptance_remain_unknown(self):
        source = Path(self.temp.name) / "unknown"
        source.mkdir()
        (source / "contract.json").write_text('{"id":"unknown"}', encoding="utf-8")
        (source / "state.json").write_text('{"run_id":"unknown","status":"completed"}', encoding="utf-8")
        MODULE.ingest(source)
        portfolio = MODULE.report()
        self.assertIsNone(portfolio["metrics"]["human_acceptance_rate"])
        self.assertIsNone(portfolio["metrics"]["cost_per_accepted_result"])

    def test_corrupt_source_is_reported(self):
        source = Path(self.temp.name) / "corrupt"
        source.mkdir()
        (source / "contract.json").write_text('{"id":"bad"}', encoding="utf-8")
        (source / "state.json").write_text('{broken', encoding="utf-8")
        result = MODULE.ingest(source)
        self.assertEqual(result["counts"]["corrupt"], 1)

    def test_incomplete_source_is_not_ingested(self):
        source = Path(self.temp.name) / "incomplete"
        source.mkdir()
        (source / "contract.json").write_text('{"id":"pending"}', encoding="utf-8")
        (source / "state.json").write_text('{"run_id":"pending","status":"running"}', encoding="utf-8")
        result = MODULE.ingest(source)
        self.assertEqual(result["counts"]["incomplete"], 1)
        self.assertEqual(MODULE.records(), [])

    def test_duplicate_run_is_stored_once(self):
        source = Path(self.temp.name) / "duplicates"
        shutil.copytree(ROOT / "fixtures" / "loopkit-run", source / "one")
        shutil.copytree(ROOT / "fixtures" / "loopkit-run", source / "two")
        result = MODULE.ingest(source)
        self.assertEqual(result["counts"]["ingested"], 1)
        self.assertEqual(result["counts"]["duplicate"], 1)
        self.assertEqual(len(MODULE.records()), 1)

    def test_partial_cost_evidence_keeps_portfolio_cost_unknown(self):
        base = Path(self.temp.name) / "costs"
        for name, cost in (("known", ',"cost":1.0'), ("unknown", "")):
            run = base / name
            run.mkdir(parents=True)
            (run / "contract.json").write_text(json.dumps({"id": name}), encoding="utf-8")
            (run / "state.json").write_text(
                '{"run_id":"' + name + '","status":"completed","human_acceptance":true' + cost + '}',
                encoding="utf-8",
            )
        MODULE.ingest(base)
        self.assertIsNone(MODULE.report()["metrics"]["cost_per_accepted_result"])

    def test_scheduled_report_no_op(self):
        self.assertEqual(MODULE.report(scheduled=True)["status"], "no-op")

    def test_companion_absent_handoff_is_complete_and_read_only(self):
        source = Path(self.temp.name) / "handoff-source"
        shutil.copytree(ROOT / "fixtures" / "graph-run", source)
        MODULE.register_root(source)
        before = MODULE.tree_hash(source)
        MODULE.ingest(Path(self.temp.name) / "missing-loopkit")
        record = MODULE.records()[0]
        handoff = MODULE.repair_handoff(record["record_id"])
        self.assertEqual(before, MODULE.tree_hash(source))
        self.assertEqual(handoff["handoff_status"], "unresolved")
        self.assertIs(handoff["repair_performed"], False)
        self.assertEqual(handoff["owner_class"], "operating-graph")
        self.assertEqual(handoff["disagreement"], "false-failure")
        self.assertEqual(handoff["preferred_destinations"], ["agent-ops workspace skill"])
        for field in (
            "source_run",
            "normalized_evidence",
            "disagreement",
            "owner_class",
            "requested_outcome",
            "unresolved_proof",
        ):
            self.assertIn(field, handoff)

    def test_unknown_handoff_record_fails_without_guessing(self):
        with self.assertRaisesRegex(ValueError, "unknown normalized record"):
            MODULE.repair_handoff("missing-record")


if __name__ == "__main__":
    unittest.main()
