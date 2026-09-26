"""Regression tests for the execution guards added in the remaining-repairs wave."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_acceptance_guards import module, ROOT

GAUNTLET = ROOT / "skills/gauntlet/scripts"
LOOP = ROOT / "skills/gauntlet-loop/bin/gauntletctl.py"


def run(*args, stdin=None):
    return subprocess.run([sys.executable, *map(str, args)], input=stdin,
                          capture_output=True, text=True)


def init_artifact_run(root):
    done = run(GAUNTLET / "init_run.py", "--root", root, "--slug", "fixture", "--goal", "Fixture",
               "--domain", "code", "--shape", "S1")
    return done, (json.loads(done.stdout).get("run_dir") if done.returncode == 0 else None)


class ExecutionGuards(unittest.TestCase):
    def test_gauntlet_editions_never_share_a_root(self):
        with tempfile.TemporaryDirectory() as d:
            loop_root = Path(d, "loop"); loop_root.mkdir()
            self.assertEqual(run(LOOP, "init", "--project-root", loop_root, "--name", "x").returncode, 0)
            refused, _ = init_artifact_run(loop_root)
            self.assertNotEqual(refused.returncode, 0)
            self.assertIn("gauntlet-loop-state-present", refused.stdout)
            self.assertFalse((loop_root / ".gauntlet/runs").exists())

            artifact_root = Path(d, "artifact"); artifact_root.mkdir()
            created, _ = init_artifact_run(artifact_root)
            self.assertEqual(created.returncode, 0)
            for extra in ((), ("--force",)):
                refused = run(LOOP, "init", "--project-root", artifact_root, "--name", "x", *extra)
                self.assertNotEqual(refused.returncode, 0)
                self.assertFalse((artifact_root / ".gauntlet/state.json").exists())

    def test_open_session_without_timestamp_pauses_the_run(self):
        with tempfile.TemporaryDirectory() as d:
            _, run_dir = init_artifact_run(Path(d))
            run_dir = Path(run_dir)
            document = json.loads((run_dir / "run.json").read_text())
            document["budgets"].update(approved=True, approval_ref="synthetic test only")
            (run_dir / "run.json").write_text(json.dumps(document))
            sessions = run_dir / "sessions/sessions.json"
            sessions.parent.mkdir(exist_ok=True)
            sessions.write_text(json.dumps({"sessions": [{"entered": "not a time"}]}))
            result = json.loads(run(GAUNTLET / "check_stops.py", "--run-dir", run_dir).stdout)
            self.assertEqual(result["condition"], "budget-unverified")
            self.assertEqual(json.loads((run_dir / "run.json").read_text())["status"], "paused")

    def test_fresh_isolation_needs_observed_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(LOOP, "init", "--project-root", d, "--name", "x").returncode, 0)
            claimed = run(LOOP, "capabilities", "--project-root", d, "--fresh-isolation")
            self.assertNotEqual(claimed.returncode, 0)
            self.assertIn("isolation-evidence", claimed.stdout)
            recorded = run(LOOP, "capabilities", "--project-root", d)
            self.assertEqual(recorded.returncode, 0)
            capabilities = json.loads(Path(d, ".gauntlet/runtime-capabilities.json").read_text())
            self.assertEqual(capabilities["isolation_evidence"], None)

    def test_failing_regression_case_is_a_failed_check(self):
        cli = ROOT / "skills/proofloop/bin/run-regressions"
        payload = {"cases": [{"case_id": "a", "actual": 1, "expected": 1},
                             {"case_id": "b", "actual": 1, "expected": 2}]}
        self.assertEqual(run(cli, "--input", "-", stdin=json.dumps(payload)).returncode, 2)
        payload["cases"].pop()
        self.assertEqual(run(cli, "--input", "-", stdin=json.dumps(payload)).returncode, 0)

    def test_harness_plan_rejects_placeholders_and_non_string_content(self):
        h = module("skills/harness-engineering/scripts/harnessctl.py", "harnessctl_guards")
        template = json.loads((ROOT / "skills/harness-engineering/assets/harness-plan.template.json").read_text())
        with self.assertRaises(h.HarnessError):
            h.validate_operations(template)
        with tempfile.TemporaryDirectory() as d:
            root = str(Path(d).resolve())
            plan = dict(template, run_id="fixture", allowed_roots=[root], approval_groups=["files"],
                        support_artifacts=[])
            plan["outcome"] = dict(primary_metric="files", before_state="old", target_state="new",
                                   unresolved_before=1, unresolved_target=0, expected_primary_outputs=1)
            plan["resource_budget"] = dict(max_task_launches=0, max_support_artifacts=1, max_verification_passes=1,
                                           max_low_yield_waves=1, high_cost_approved=False, cost_warning=None)
            plan["operations"] = [dict(id="one", action="create", target=f"{root}/new.txt",
                                       approval_group="files", content="text")]
            h.validate_operations(plan)
            plan["operations"][0]["content"] = 5
            with self.assertRaises(h.HarnessError):
                h.validate_operations(plan)


if __name__ == "__main__":
    unittest.main()
