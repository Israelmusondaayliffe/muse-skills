"""State location tests: user state lives outside the skill package, and legacy
in-package state is migrated forward explicitly, never forked, overwritten, or deleted."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill_eval_loop.py"
SPEC = importlib.util.spec_from_file_location("skill_eval_loop", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)

ENV_KEYS = ("HOME", "SKILL_EVAL_LOOP_STATE", "SKILL_EVAL_LOOP_LEGACY_STATE")


class StateLocationTests(unittest.TestCase):
    def setUp(self):
        self.saved = {key: os.environ.get(key) for key in ENV_KEYS}
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name).resolve()
        os.environ["HOME"] = str(self.home)
        os.environ.pop("SKILL_EVAL_LOOP_STATE", None)
        os.environ["SKILL_EVAL_LOOP_LEGACY_STATE"] = str(self.home / "old-package" / "state")
        self.legacy = self.home / "old-package" / "state"
        self.current = self.home / "workspace" / "skill-eval-loop" / "state"
        self.target = self.home / "workspace" / "skills" / "sample-skill"
        self.target.mkdir(parents=True)
        (self.target / "SKILL.md").write_text("---\nname: sample-skill\ndescription: sample\n---\n")

    def tearDown(self):
        for key, value in self.saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        self.temp.cleanup()

    def _init(self, root=None):
        args = type("Args", (), {"target": str(self.target), "state_root": root})()
        return MODULE.cmd_init(args)

    def test_default_root_is_outside_the_package(self):
        root = MODULE.state_root(None)
        self.assertEqual(self.current, root)
        self.assertNotIn(MODULE.SKILL_DIR, root.parents)
        os.environ["SKILL_EVAL_LOOP_STATE"] = str(self.home / "override")
        self.assertEqual(self.home / "override", MODULE.state_root(None))

    def test_unmigrated_legacy_state_blocks_writes_to_new_root(self):
        self._init(str(self.legacy))
        self.assertEqual("migrate", MODULE.state_status()["action"])
        with self.assertRaises(MODULE.LoopError):
            self._init()
        self.assertFalse(self.current.exists())

    def test_migrate_keeps_legacy_and_new_writes_are_not_a_conflict(self):
        self._init(str(self.legacy))
        before = MODULE.tree_digest(self.legacy)
        result = MODULE.migrate_state()
        self.assertTrue(result["migrated"])
        self.assertEqual(before, MODULE.tree_digest(self.current))
        self.assertEqual(before, MODULE.tree_digest(self.legacy))
        self.assertFalse(self._init()["initialized"])  # sees the migrated target state
        MODULE.atomic_json(self.current / "extra.json", {"new": True})
        self.assertEqual("none", MODULE.state_status()["action"])

    def test_conflict_refuses_and_overwrites_nothing(self):
        self._init(str(self.legacy))
        MODULE.atomic_json(self.current / "other.json", {"different": True})
        legacy_before = MODULE.tree_digest(self.legacy)
        current_before = MODULE.tree_digest(self.current)
        self.assertEqual("conflict", MODULE.state_status()["action"])
        with self.assertRaises(MODULE.LoopError):
            MODULE.state_root(None)
        with self.assertRaises(MODULE.LoopError):
            MODULE.migrate_state()
        self.assertEqual(legacy_before, MODULE.tree_digest(self.legacy))
        self.assertEqual(current_before, MODULE.tree_digest(self.current))
        self.assertEqual(self.legacy, MODULE.state_root(str(self.legacy)))

    def test_installed_legacy_location_is_detected(self):
        os.environ.pop("SKILL_EVAL_LOOP_LEGACY_STATE", None)
        installed = self.home / "workspace" / "skills" / "skill-eval-loop" / "state"
        self._init(str(installed))
        status = MODULE.state_status()
        self.assertEqual("migrate", status["action"])
        self.assertIn(str(installed), [item["path"] for item in status["legacy_roots"]])


if __name__ == "__main__":
    unittest.main()
