import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/writing-quality/bin/voice_state.py"
spec = importlib.util.spec_from_file_location("voice_state", SCRIPT)
voice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(voice)

class VoiceMigrationTest(unittest.TestCase):
    def test_save_after_migration_and_legacy_change(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            legacy = root / "legacy.md"
            legacy.write_text("Calibrated original voice")
            source = root / "new.md"
            source.write_text("Calibrated updated voice")
            with patch.object(voice, "LEGACY_PATH", legacy), patch.dict(os.environ, {"WRITING_QUALITY_STATE_DIR": str(root / "state")}):
                self.assertEqual(voice.migrate()[0], 0)
                self.assertEqual(voice.save(source)[0], 0)
                self.assertEqual(voice.status()["action"], "none")
                self.assertEqual(legacy.read_text(), "Calibrated original voice")
                legacy.write_text("Separately changed legacy voice")
                self.assertTrue(voice.status()["action"].startswith("conflict:"))
                self.assertEqual(voice.migrate()[0], 1)
                self.assertEqual(voice.state_path().read_text(), source.read_text())

    def test_unrelated_existing_profile_is_conflict(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            legacy = root / "legacy.md"
            legacy.write_text("Legacy profile")
            with patch.object(voice, "LEGACY_PATH", legacy), patch.dict(os.environ, {"WRITING_QUALITY_STATE_DIR": str(root / "state")}):
                voice.state_dir().mkdir()
                voice.state_path().write_text("Existing independent state profile")
                self.assertTrue(voice.status()["action"].startswith("conflict:"))
                self.assertEqual(voice.migrate()[0], 1)
