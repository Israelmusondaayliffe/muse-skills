import json
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator

from .errors import StorageError


def confined(root: Path, candidate: Path) -> Path:
    real_root = root.resolve()
    resolved = candidate.resolve(strict=False)
    if resolved != real_root and real_root not in resolved.parents:
        raise StorageError("That path is outside the selected project. No files were changed.")
    current = resolved
    while current != real_root and current != current.parent:
        if current.is_symlink():
            raise StorageError("A symbolic link would leave the selected project. No files were changed.")
        current = current.parent
    return resolved


def read_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError("Citizen Forge could not safely read {}: {}".format(path.name, exc))
    if not isinstance(value, dict):
        raise StorageError("{} must contain a JSON object.".format(path.name))
    return value


def snapshot(path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / (path.name + ".{}.bak".format(time.time_ns()))
    if path.exists():
        shutil.copy2(str(path), str(target))
    else:
        target.write_text("ABSENT\n", encoding="utf-8")
    return target


def atomic_write_json(path: Path, value: Dict[str, Any], backup_dir: Path = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if backup_dir is not None:
        snapshot(path, backup_dir)
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, str(path))
    except Exception as exc:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise StorageError("Citizen Forge could not finish the safe write: {}".format(exc))


@contextmanager
def project_lock(citizen_dir: Path, stale_after: int = 300) -> Iterator[None]:
    lock = citizen_dir / ".write.lock"
    citizen_dir.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        age = time.time() - lock.stat().st_mtime
        if age <= stale_after:
            raise StorageError("Another Citizen Forge change is active. Wait for it to finish, then retry.")
        raise StorageError("A stale write lock was detected. Review recovery evidence before removing it.")
    try:
        os.write(descriptor, str(os.getpid()).encode("ascii"))
        os.close(descriptor)
        yield
    finally:
        try:
            lock.unlink()
        except FileNotFoundError:
            pass
