"""Synthetic-tree tests for tools/muse_install.py. Never touches a real installation."""
import json
from pathlib import Path
import stat
import tempfile
import unittest

from test_acceptance_guards import module, ROOT

mi = module("tools/muse_install.py", "muse_install")
SKILLS = [f"s{i:02d}" for i in range(30)]


def write(path, text, mode=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    if mode:
        path.chmod(mode)


class MuseInstall(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name).resolve()
        self.policy = {"skills": SKILLS, "protected": ["s00/references/voice-profile.md", "s01/state/*"]}
        self.old, self.new, self.inst = (self.root / n for n in ("old", "new", "installed"))
        for s in SKILLS:
            for tree in (self.old, self.new):
                write(tree / s / "SKILL.md", f"---\nname: {s}\n---\n{s} v1\n")
        write(self.old / "s00/references/voice-profile.md", "NOT YET CALIBRATED")
        write(self.new / "s00/references/voice-profile.md", "NOT YET CALIBRATED v2")
        write(self.old / "s02/retired.md", "gone in v2")
        write(self.new / "s03/SKILL.md", "---\nname: s03\n---\ns03 v2\n")
        write(self.new / "s04/bin/tool.py", "print('new')\n", 0o755)
        # Installed = old release + calibrated private voice + legacy state + a local skill.
        for path in self.old.rglob("*"):
            if path.is_file():
                write(self.inst / path.relative_to(self.old), path.read_text())
        write(self.inst / "s00/references/voice-profile.md", "calibrated private voice")
        write(self.inst / "s01/state/ledger.json", "{\"private\": true}")
        write(self.inst / "flora/SKILL.md", "local skill")
        self.baseline = mi.tree_manifest(self.old, self.policy)
        self.reviewed = mi.tree_manifest(self.new, self.policy)

    def tearDown(self):
        self._tmp.cleanup()

    def plan(self, **kw):
        return mi.plan(self.new, self.inst, self.baseline, self.policy, self.reviewed, **kw)

    def test_plan_apply_rollback_preserves_private_and_local(self):
        profile = self.inst / "s00/references/voice-profile.md"
        profile.chmod(0)  # proves plan and apply never open the private profile
        write(self.inst / "s04/__pycache__/tool.cpython-312.pyc", "host bytecode")
        record = self.plan()
        self.assertEqual(record["status"], "ready")
        self.assertEqual([r["path"] for r in record["update"]], ["s03/SKILL.md"])
        self.assertEqual([r["path"] for r in record["create"]], ["s04/bin/tool.py"])
        self.assertEqual(record["protected"], ["s00/references/voice-profile.md"])
        self.assertEqual(record["retired_left_in_place"], ["s02/retired.md"])
        with self.assertRaises(mi.InstallError):
            mi.apply(record, self.root / "backup", "")
        receipt = mi.apply(record, self.root / "backup", "synthetic test approval")
        self.assertEqual((self.inst / "s03/SKILL.md").read_text(), "---\nname: s03\n---\ns03 v2\n")
        self.assertTrue((self.inst / "s04/bin/tool.py").stat().st_mode & stat.S_IXUSR)
        profile.chmod(0o600)
        self.assertEqual(profile.read_text(), "calibrated private voice")
        self.assertEqual((self.inst / "s04/__pycache__/tool.cpython-312.pyc").read_text(), "host bytecode")
        self.assertEqual((self.inst / "s01/state/ledger.json").read_text(), "{\"private\": true}")
        self.assertEqual((self.inst / "flora/SKILL.md").read_text(), "local skill")
        self.assertTrue((self.inst / "s02/retired.md").exists())
        self.assertEqual(self.plan()["status"], "noop")
        mi.h.rollback(Path(receipt["manifest"]))
        self.assertEqual((self.inst / "s03/SKILL.md").read_text(), "---\nname: s03\n---\ns03 v1\n")
        self.assertFalse((self.inst / "s04/bin/tool.py").exists())
        with self.assertRaises(FileExistsError):  # a backup directory is never reused
            mi.apply(self.plan(), self.root / "backup", "again")

    def test_rollback_refuses_to_clobber_newer_user_work(self):
        receipt = mi.apply(self.plan(), self.root / "backup", "synthetic test approval")
        write(self.inst / "s03/SKILL.md", "user edited after install")
        with self.assertRaises(mi.h.HarnessError):
            mi.h.rollback(Path(receipt["manifest"]))
        self.assertEqual((self.inst / "s03/SKILL.md").read_text(), "user edited after install")
        self.assertTrue((self.inst / "s04/bin/tool.py").exists())  # nothing partially restored

    def test_local_changes_block_the_whole_plan(self):
        write(self.inst / "s03/SKILL.md", "local edit")
        (self.inst / "s05/SKILL.md").unlink()
        write(self.new / "s05/SKILL.md", "---\nname: s05\n---\ns05 v2\n")
        write(self.inst / "s04/bin/tool.py", "user file at new path")
        self.reviewed = mi.tree_manifest(self.new, self.policy)
        record = self.plan()
        self.assertEqual(record["status"], "blocked")
        reasons = {r["path"]: r["reason"] for r in record["blocked"]}
        self.assertEqual(reasons, {
            "s03/SKILL.md": "installed file modified locally",
            "s04/bin/tool.py": "unknown installed file at a new release path",
            "s05/SKILL.md": "baseline file deleted locally"})
        with self.assertRaises(mi.InstallError):
            mi.apply(record, self.root / "backup", "synthetic test approval")
        self.assertEqual((self.inst / "s03/SKILL.md").read_text(), "local edit")
        self.assertFalse((self.root / "backup").exists())
        excluded = self.plan(exclude={"s03/SKILL.md", "s04/bin/tool.py", "s05/SKILL.md"})
        self.assertEqual(excluded["status"], "noop")

    def test_staging_drift_and_symlinks_are_refused(self):
        write(self.new / "s06/SKILL.md", "changed after review")
        with self.assertRaises(mi.InstallError):
            self.plan()
        self.reviewed = mi.tree_manifest(self.new, self.policy)
        (self.inst / "s03/SKILL.md").unlink()
        (self.inst / "s03/SKILL.md").symlink_to(self.root / "elsewhere")
        self.assertEqual(self.plan()["blocked"][0]["reason"], "symbolic link on installed path")

    def test_apply_requires_reviewed_payloads_and_blocks_late_drift(self):
        unreviewed = mi.plan(self.new, self.inst, self.baseline, self.policy)
        with self.assertRaises(mi.InstallError):
            mi.apply(unreviewed, self.root / "backup", "synthetic approval")
        record = self.plan()
        write(self.new / "s03/SKILL.md", "changed after plan")
        with self.assertRaises(mi.h.HarnessError):
            mi.apply(record, self.root / "backup", "synthetic approval")
        self.assertFalse((self.root / "backup").exists())
        self.assertIn("v1", (self.inst / "s03/SKILL.md").read_text())
        self.assertFalse((self.inst / "s04/bin/tool.py").exists())

    def test_pilot_wave_changes_only_selected_skill(self):
        record = self.plan(only=["s03"])
        self.assertEqual(record["selected_skills"], ["s03"])
        self.assertEqual(record["create"], [])
        mi.apply(record, self.root / "pilot-backup", "synthetic pilot approval")
        self.assertFalse((self.inst / "s04/bin/tool.py").exists())
        self.assertEqual(self.plan()["create"][0]["path"], "s04/bin/tool.py")
        with self.assertRaises(mi.InstallError):
            self.plan(only=["flora"])

    def test_staged_package_root_symlink_is_not_followed(self):
        tree = self.root / "linked-tree"
        tree.mkdir()
        (tree / "s00").symlink_to(self.old / "s00", target_is_directory=True)
        with self.assertRaises(mi.InstallError):
            mi.tree_manifest(tree, self.policy)

    def test_policy_rejects_traversal_names(self):
        path = self.root / "policy.json"
        bad = dict(self.policy, skills=["../outside", *SKILLS[1:]])
        path.write_text(json.dumps(bad))
        with self.assertRaises(mi.InstallError):
            mi.load_policy(path)

    def test_real_policy_and_git_baseline(self):
        policy = mi.load_policy()
        self.assertEqual(policy["skills"], sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")))
        baseline = mi.git_manifest(ROOT, "HEAD", policy)
        self.assertEqual(sum(k.endswith("/SKILL.md") and k.count("/") == 1 for k in baseline), 30)


if __name__ == "__main__":
    unittest.main()
