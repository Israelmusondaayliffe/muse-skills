"""Backtick path detection in tools/validate_collection.py."""
import unittest

from test_acceptance_guards import module

v = module("tools/validate_collection.py", "validate_collection")


class BacktickPaths(unittest.TestCase):
    def test_only_package_paths_are_checked(self):
        text = ("Run `python3 scripts/check.py --json`, read `references/routing.md`. "
                "Write `route.json` and `qc-report.md`; see `references/<name>.md` and `assets/*.png`.")
        self.assertEqual(list(v.backtick_paths(text)), ["scripts/check.py", "references/routing.md"])

    def test_illustrative_exception_is_scoped_to_its_document(self):
        errors = v.check(v.Path(__file__).resolve().parents[1])["errors"]
        self.assertFalse([e for e in errors if "music-video.md" in e and "assets/bgm.mp3" in e])
        self.assertEqual(set(v.ILLUSTRATIVE_PATHS), {"skills/video-production-studio/references/music-video.md"})


if __name__ == "__main__":
    unittest.main()
