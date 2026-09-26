"""Focused regression tests for previously false acceptance claims."""
import importlib.util
import json
from pathlib import Path
import unittest
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(relative, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class AcceptanceGuards(unittest.TestCase):
    def test_unreadable_protected_inputs_are_input_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            before, after = Path(folder) / "before.md", Path(folder) / "after.md"
            before.write_bytes(bytes([255]))
            after.write_text("valid text")
            command = [sys.executable, str(ROOT / "skills/writing-quality/bin/protected_scope_validator.py"), str(before), str(after)]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("error", json.loads(result.stdout))
            before.write_text("valid text")
            missing = Path(folder) / "missing.md"
            result = subprocess.run(command[:-1] + [str(missing)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)

    def test_valid_partial_route_reports_its_gap(self):
        with tempfile.TemporaryDirectory() as folder:
            data = json.loads((ROOT / "skills/video-production-studio/assets/route-template.json").read_text())
            data.update(route="motion-graphics", runtime="ffmpeg", renderer_available=True,
                requested_deliverable="clip", completion_state="rendered-partial",
                rendering_status="complete", visual_qc_status="complete", missing_requirements=["music missing"],
                duration_seconds=4, width=640, height=360, skills=["video-delivery-qc"],
                objective="Synthetic clip", rationale="Check honest partial delivery")
            target = Path(folder) / "route.json"
            target.write_text(json.dumps(data))
            result = subprocess.run([sys.executable, str(ROOT / "skills/video-production-studio/bin/validate_route.py"), str(target)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(json.loads(result.stdout)["completion_state"], "rendered-partial")
            self.assertEqual(json.loads(result.stdout)["missing_requirements"], ["music missing"])

    def test_heuristic_score_never_certifies_prose(self):
        result = subprocess.run([sys.executable,
            str(ROOT / "skills/founder-revenue-engine/scripts/quality_validator.py"),
            "We tested 12 drafts. It costs $3. We don't know the cause yet."],
            capture_output=True, text=True)
        self.assertIn("ADVISORY PATTERN SCORE", result.stdout)
        self.assertIn("does not verify facts", result.stdout)
        self.assertNotIn("Ship it", result.stdout)
        self.assertNotIn("No changes needed", result.stdout)

    def test_budget_blocks_unapproved_unknown_and_excess_usage(self):
        with tempfile.TemporaryDirectory() as directory:
            created = subprocess.check_output([
                sys.executable, str(ROOT / "skills/gauntlet/scripts/init_run.py"),
                "--root", directory, "--slug", "fixture", "--goal", "Fixture",
                "--domain", "code", "--shape", "S1"], text=True)
            run = Path(json.loads(created)["run_dir"])

            def check(*args):
                return json.loads(subprocess.check_output([
                    sys.executable, str(ROOT / "skills/gauntlet/scripts/check_stops.py"),
                    "--run-dir", str(run), *args], text=True))

            self.assertEqual(check()["condition"], "budget-unverified")
            document = json.loads((run / "run.json").read_text())
            document["budgets"].update(approved=True, approval_ref="synthetic test only")
            (run / "run.json").write_text(json.dumps(document))
            self.assertFalse(check()["fired"])
            self.assertEqual(check("--next-launches", "7")["condition"], "proposed-budget-exceeded")
            self.assertEqual(check("--next-cost", "0.01")["condition"], "proposed-budget-exceeded")
            cost = json.loads((run / "cost.json").read_text())
            for value in ("unknown", "nan", -1):
                cost["cost_spent"] = value
                (run / "cost.json").write_text(json.dumps(cost))
                self.assertEqual(check()["condition"], "budget-unverified")

    def test_surface_labels_do_not_prove_isolation(self):
        precheck = module("skills/gauntlet/scripts/precheck.py", "precheck")
        with patch.dict("os.environ", {"CLAUDECODE": "1"}):
            for surface in ("auto", "hatch", "claude-code", "cowork"):
                self.assertEqual(precheck.detect_subagents(surface), "unknown")
        self.assertFalse(precheck.detect_subagents("chat"))

    def test_template_cannot_initialize_as_completed_contract(self):
        core = module("skills/loopkit/bin/loopkit_core.py", "loopkit_core")
        template = (ROOT / "skills/loopkit/assets/contract-template.json").read_text()
        self.assertTrue(core.validate_contract(json.loads(template)))
        filled = json.loads(template.replace("__REPLACE_ME__", "concrete fixture"))
        self.assertEqual(core.validate_contract(filled), [])
        filled["goal"]["outcome"] = "Deliver __REPLACE_ME__"
        self.assertTrue(core.validate_contract(filled))


if __name__ == "__main__":
    unittest.main()
