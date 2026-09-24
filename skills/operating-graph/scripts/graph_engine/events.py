"""Atomic, controller-owned hash-chained event storage."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Dict, Optional, Tuple

from .constants import EventType
from .models import Event


class EventChainError(RuntimeError):
    """Raised when an event log cannot be trusted."""


class WriterAuthorityError(PermissionError):
    """Raised when a non-controller attempts a runtime write."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _atomic_replace(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


class EventStore:
    """Persist one run's events under a mandatory controller writer identity."""

    def __init__(
        self,
        run_directory: Path,
        run_id: str,
        *,
        controller_node_id: str = "controller",
    ) -> None:
        self.run_directory = Path(run_directory)
        self.run_id = run_id
        self.controller_node_id = controller_node_id
        self.path = self.run_directory / "events.jsonl"

    def require_controller(self, actor_node_id: str) -> None:
        if actor_node_id != self.controller_node_id:
            raise WriterAuthorityError("controller is the sole event writer")

    def read_all(self) -> Tuple[Event, ...]:
        if not self.path.exists():
            return ()
        events = []
        previous_hash: Optional[str] = None
        for expected_sequence, raw_line in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                event = Event.from_dict(json.loads(raw_line))
            except (ValueError, TypeError, json.JSONDecodeError) as error:
                raise EventChainError(
                    f"invalid event record at sequence {expected_sequence}: {error}"
                ) from error
            if event.sequence != expected_sequence:
                raise EventChainError(
                    f"expected sequence {expected_sequence}, found {event.sequence}"
                )
            expected_id = f"evt-{expected_sequence:06d}"
            if event.event_id != expected_id:
                raise EventChainError(
                    f"expected event id {expected_id}, found {event.event_id}"
                )
            if event.run_id != self.run_id:
                raise EventChainError(
                    f"event run id mismatch at sequence {expected_sequence}"
                )
            if event.previous_hash != previous_hash:
                raise EventChainError(
                    f"previous hash mismatch at sequence {expected_sequence}"
                )
            if event.event_hash != event.calculated_hash():
                raise EventChainError(
                    f"event hash mismatch at sequence {expected_sequence}"
                )
            events.append(event)
            previous_hash = event.event_hash
        return tuple(events)

    def append(
        self,
        event_type: EventType,
        payload: Dict[str, Any],
        graph_version: int,
        *,
        actor_node_id: str = "controller",
        timestamp: Optional[str] = None,
    ) -> Event:
        self.require_controller(actor_node_id)
        events = self.read_all()
        sequence = len(events) + 1
        unsigned = Event(
            event_id=f"evt-{sequence:06d}",
            sequence=sequence,
            timestamp=timestamp or _utc_now(),
            run_id=self.run_id,
            graph_version=graph_version,
            actor_node_id=actor_node_id,
            type=event_type,
            payload=payload,
            previous_hash=events[-1].event_hash if events else None,
            event_hash="",
        )
        event = Event(
            event_id=unsigned.event_id,
            sequence=unsigned.sequence,
            timestamp=unsigned.timestamp,
            run_id=unsigned.run_id,
            graph_version=unsigned.graph_version,
            actor_node_id=unsigned.actor_node_id,
            type=unsigned.type,
            payload=unsigned.payload,
            previous_hash=unsigned.previous_hash,
            event_hash=unsigned.calculated_hash(),
        )
        existing = self.path.read_bytes() if self.path.exists() else b""
        line = event.canonical_json(include_event_hash=True).encode("utf-8") + b"\n"
        _atomic_replace(self.path, existing + line)
        return event
