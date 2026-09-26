#!/usr/bin/env python3
"""Locate, migrate, and save the user's voice profile outside the skill package.

The profile is user state. It lives at ~/workspace/writing-quality/voice-profile.md
(override the directory with WRITING_QUALITY_STATE_DIR) so that replacing this
skill folder never overwrites it.

Older installs wrote the profile inside the package at references/voice-profile.md.
This helper reads that legacy file, copies it forward on request, and never
deletes or overwrites it.

Commands:
  status   report which profile is active and whether a migration is needed
  path     print the state-path profile location
  migrate  copy a calibrated legacy profile to the state path (no overwrite)
  save     write a new profile from a file atomically; the previous one is kept
           under a unique backup name. Writers are serialized with a lock file.
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
LEGACY_PATH = SKILL_DIR / "references" / "voice-profile.md"
PLACEHOLDER_MARKERS = ("NOT YET CALIBRATED",)


def state_dir() -> Path:
    override = os.environ.get("WRITING_QUALITY_STATE_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / "workspace" / "writing-quality"


def state_path() -> Path:
    return state_dir() / "voice-profile.md"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_calibrated(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return False
    head = "\n".join(text.splitlines()[:3])
    return not any(marker in head for marker in PLACEHOLDER_MARKERS)


def _legacy_migrated() -> bool:
    try:
        marker = json.loads((state_dir() / ".voice-profile-migration.json").read_text())
        return marker.get("legacy_sha256") == _digest(LEGACY_PATH)
    except (OSError, ValueError, AttributeError):
        return False


def _record_migration(digest: str) -> None:
    marker = state_dir() / ".voice-profile-migration.json"
    temp = _write_temp(state_dir(), json.dumps({"legacy_sha256": digest}).encode())
    os.replace(temp, marker)


def status() -> dict[str, object]:
    current = state_path()
    current_ok = is_calibrated(current)
    legacy_ok = is_calibrated(LEGACY_PATH)
    result: dict[str, object] = {
        "state_path": str(current),
        "state_profile": current_ok,
        "legacy_path": str(LEGACY_PATH),
        "legacy_profile": legacy_ok,
    }
    if current_ok and legacy_ok and _digest(current) != _digest(LEGACY_PATH) and not _legacy_migrated():
        result["active"] = str(current)
        result["action"] = "conflict: state and legacy profiles differ; use the state profile and ask the user before merging"
    elif current_ok:
        result["active"] = str(current)
        result["action"] = "none"
    elif legacy_ok:
        result["active"] = str(LEGACY_PATH)
        result["action"] = "run: python3 bin/voice_state.py migrate"
    else:
        result["active"] = None
        result["action"] = "no calibrated profile; calibrate only if the task needs the user's own voice"
    return result


def _write_temp(directory: Path, data: bytes) -> Path:
    """Write data to a new temporary file in directory and flush it to disk."""
    fd, name = tempfile.mkstemp(dir=directory, prefix=".voice-profile.", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except BaseException:
        os.unlink(name)
        raise
    return Path(name)


def _unique_backup(current: Path, data: bytes) -> Path:
    """Store data under a backup name that no earlier save has used."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    for counter in range(1000):
        candidate = current.with_name(f"voice-profile.{stamp}.{os.getpid()}.{counter}.bak.md")
        try:
            with open(candidate, "xb") as handle:  # exclusive: never replaces a backup
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            return candidate
        except FileExistsError:
            continue
    raise RuntimeError("could not find a free backup name")


@contextlib.contextmanager
def _state_lock(directory: Path):
    """Serialize writers so every saved profile is either active or backed up."""
    directory.mkdir(parents=True, exist_ok=True)
    with open(directory / ".voice-profile.lock", "a") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _refuse_symlink(current: Path) -> dict[str, object] | None:
    if current.is_symlink():
        return {"reason": f"state path is a symlink; refusing to write through it: {current}"}
    return None


def migrate() -> tuple[int, dict[str, object]]:
    with _state_lock(state_dir()):
        return _migrate()


def _migrate() -> tuple[int, dict[str, object]]:
    current = state_path()
    if not is_calibrated(LEGACY_PATH):
        return 0, {"migrated": False, "reason": "no calibrated legacy profile"}
    refusal = _refuse_symlink(current)
    if refusal:
        return 1, {"migrated": False, **refusal}
    if current.exists():
        if _digest(current) == _digest(LEGACY_PATH):
            _record_migration(_digest(current))
            return 0, {"migrated": False, "reason": "already migrated", "state_path": str(current)}
        return 1, {
            "migrated": False,
            "reason": "state profile already exists and differs; nothing overwritten",
            "state_path": str(current),
            "legacy_path": str(LEGACY_PATH),
        }
    current.parent.mkdir(parents=True, exist_ok=True)
    data = LEGACY_PATH.read_bytes()
    temp = _write_temp(current.parent, data)
    try:
        os.link(temp, current)  # atomic and fails if a profile appeared meanwhile
    except FileExistsError:
        return 1, {"migrated": False, "reason": "a state profile appeared during migration; nothing overwritten",
                   "state_path": str(current)}
    finally:
        os.unlink(temp)
    if _digest(current) != hashlib.sha256(data).hexdigest():
        return 1, {"migrated": False, "reason": "copy verification failed", "state_path": str(current)}
    _record_migration(hashlib.sha256(data).hexdigest())
    return 0, {
        "migrated": True,
        "state_path": str(current),
        "legacy_path_kept": str(LEGACY_PATH),
        "sha256": _digest(current),
    }


def save(source: Path) -> tuple[int, dict[str, object]]:
    if not source.is_file():
        return 2, {"saved": False, "reason": f"missing input file: {source}"}
    with _state_lock(state_dir()):
        return _save(source)


def _save(source: Path) -> tuple[int, dict[str, object]]:
    if not source.is_file():
        return 2, {"saved": False, "reason": f"missing input file: {source}"}
    current = state_path()
    refusal = _refuse_symlink(current)
    if refusal:
        return 1, {"saved": False, **refusal}
    if current.exists() and os.path.samefile(source, current):
        return 0, {"saved": False, "reason": "input is the active profile; nothing to replace",
                   "state_path": str(current), "sha256": _digest(current)}
    data = source.read_bytes()  # read once, before anything at the state path changes
    current.parent.mkdir(parents=True, exist_ok=True)
    backup = None
    if current.exists():
        previous = current.read_bytes()
        if previous == data:
            return 0, {"saved": False, "reason": "input matches the active profile; nothing changed",
                       "state_path": str(current), "sha256": _digest(current)}
        backup = _unique_backup(current, previous)
    temp = _write_temp(current.parent, data)
    try:
        os.replace(temp, current)  # atomic swap; readers see the old or the new profile
    except BaseException:
        os.unlink(temp)
        raise
    return 0, {
        "saved": True,
        "state_path": str(current),
        "backup": str(backup) if backup else None,
        "sha256": _digest(current),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status", help="report the active profile and any needed action")
    sub.add_parser("path", help="print the state-path profile location")
    sub.add_parser("migrate", help="copy a calibrated legacy profile to the state path")
    save_parser = sub.add_parser("save", help="write a profile file to the state path, keeping a backup")
    save_parser.add_argument("input", type=Path)
    args = parser.parse_args()

    if args.command == "path":
        print(state_path())
        return 0
    if args.command == "status":
        print(json.dumps(status(), indent=2))
        return 0
    if args.command == "migrate":
        code, result = migrate()
    else:
        code, result = save(args.input)
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
