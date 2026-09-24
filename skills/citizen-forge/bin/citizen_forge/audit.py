import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .errors import StorageError


GENESIS = "0" * 64


def _canonical(value: Dict[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def read_events(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    events = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise StorageError("Audit history is damaged at line {}: {}".format(number, exc))
    return events


def verify_chain(path: Path) -> bool:
    previous = GENESIS
    for event in read_events(path):
        claimed = event.get("event_hash")
        body = dict(event)
        body.pop("event_hash", None)
        if body.get("previous_hash") != previous or hashlib.sha256(_canonical(body)).hexdigest() != claimed:
            raise StorageError("Audit history verification failed. Changes and releases are blocked.")
        previous = claimed
    return True


def append_event(path: Path, event_type: str, actor: str, reason: str, details: Dict[str, Any]) -> Dict[str, Any]:
    verify_chain(path)
    events = read_events(path)
    previous = events[-1]["event_hash"] if events else GENESIS
    body = {
        "actor": actor,
        "details": details,
        "event_type": event_type,
        "previous_hash": previous,
        "reason": reason,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    body["event_hash"] = hashlib.sha256(_canonical(body)).hexdigest()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(body, sort_keys=True) + "\n")
        handle.flush()
        import os
        os.fsync(handle.fileno())
    return body
