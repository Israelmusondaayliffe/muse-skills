"""Event-backed node state transitions and deterministic replay."""

from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import tempfile
from typing import Optional, Sequence

from .constants import EventType, NODE_STATUS_TRANSITIONS, NodeStatus, RunStatus
from .events import EventStore, WriterAuthorityError
from .models import Event, NodeRuntimeState, RuntimeState


class IllegalTransitionError(ValueError):
    """Raised when a node status transition is outside the closed transition set."""


class RetryRejectedError(IllegalTransitionError):
    """Raised when a failed node does not satisfy the retry contract."""


def _atomic_write_state(path: Path, state: RuntimeState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        json.dumps(
            state.to_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
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


def _copy_state(state: RuntimeState) -> RuntimeState:
    return RuntimeState.from_dict(state.to_dict())


def _event_type(source: NodeStatus, target: NodeStatus) -> EventType:
    if source == NodeStatus.FAILED and target == NodeStatus.READY:
        return EventType.NODE_RETRIED
    return {
        NodeStatus.READY: EventType.NODE_READY,
        NodeStatus.RUNNING: EventType.NODE_STARTED,
        NodeStatus.SUCCEEDED: EventType.NODE_SUCCEEDED,
        NodeStatus.FAILED: EventType.NODE_FAILED,
        NodeStatus.BLOCKED: EventType.NODE_BLOCKED,
        NodeStatus.SKIPPED: EventType.SIGNAL_OBSERVED,
        NodeStatus.CANCELLED: EventType.RUN_CANCELLED,
    }[target]


def _apply_transition(state: RuntimeState, payload: dict[str, object]) -> RuntimeState:
    node_id = str(payload["nodeId"])
    source = NodeStatus(str(payload["fromStatus"]))
    target = NodeStatus(str(payload["toStatus"]))
    current = state.node_states.get(node_id)
    if current is None:
        raise IllegalTransitionError(f"unknown node {node_id!r}")
    if current.status != source or (source, target) not in NODE_STATUS_TRANSITIONS:
        raise IllegalTransitionError(
            f"illegal node transition {current.status.value} to {target.value}"
        )
    attempts = current.attempts + (1 if target == NodeStatus.RUNNING else 0)
    completed_epoch = state.epoch if target == NodeStatus.SUCCEEDED else current.completed_epoch
    last_error = payload.get("error") if target == NodeStatus.FAILED else current.last_error
    blocker = payload.get("blocker") if target == NodeStatus.BLOCKED else current.blocker
    if target in (NodeStatus.READY, NodeStatus.RUNNING, NodeStatus.SUCCEEDED):
        blocker = None
    if target in (NodeStatus.READY, NodeStatus.RUNNING, NodeStatus.SUCCEEDED):
        last_error = None
    updated_node = replace(
        current,
        status=target,
        attempts=attempts,
        last_error=None if last_error is None else str(last_error),
        blocker=None if blocker is None else str(blocker),
        completed_epoch=completed_epoch,
    )
    node_states = dict(state.node_states)
    node_states[node_id] = updated_node
    return replace(
        state,
        node_states=node_states,
        total_node_runs=state.total_node_runs + (1 if target == NodeStatus.RUNNING else 0),
    )


def _apply_run_completion(state: RuntimeState, payload: dict[str, object]) -> RuntimeState:
    source = RunStatus(str(payload["fromRunStatus"]))
    target = RunStatus(str(payload["toRunStatus"]))
    if state.status != source or source != RunStatus.RUNNING or target != RunStatus.COMPLETED:
        raise IllegalTransitionError(
            f"illegal run transition {state.status.value} to {target.value}"
        )
    return replace(state, status=target)


def replay_events(events: Sequence[Event]) -> RuntimeState:
    state: Optional[RuntimeState] = None
    for event in events:
        if event.type == EventType.RUN_STARTED and "initialState" in event.payload:
            if state is not None:
                raise IllegalTransitionError("run.started may initialize state only once")
            state = RuntimeState.from_dict(event.payload["initialState"])
            continue
        if event.type == EventType.REWRITE_APPLIED and "state" in event.payload:
            if state is None:
                raise IllegalTransitionError("rewrite.applied precedes run.started")
            rewritten = RuntimeState.from_dict(event.payload["state"])
            if rewritten.run_id != state.run_id:
                raise IllegalTransitionError("rewrite.applied state belongs to another run")
            if rewritten.graph_version <= state.graph_version:
                raise IllegalTransitionError("rewrite.applied graph version is not monotonic")
            state = rewritten
            continue
        if event.type == EventType.RUN_COMPLETED and "toRunStatus" in event.payload:
            if state is None:
                raise IllegalTransitionError("run.completed precedes run.started")
            state = _apply_run_completion(state, event.payload)
            continue
        if "fromStatus" in event.payload and "toStatus" in event.payload:
            if state is None:
                raise IllegalTransitionError("node transition precedes run.started")
            state = _apply_transition(state, event.payload)
    if state is None:
        raise IllegalTransitionError("event log does not contain run.started state")
    return state


class StateMachine:
    """The sole controller interface for persisted runtime state mutation."""

    def __init__(
        self,
        run_directory: Path,
        state: RuntimeState,
        event_store: EventStore,
    ) -> None:
        self.run_directory = Path(run_directory)
        self.path = self.run_directory / "state.json"
        self.event_store = event_store
        self._state = _copy_state(state)
        self._poisoned = False

    @classmethod
    def create(
        cls,
        run_directory: Path,
        initial_state: RuntimeState,
        event_store: EventStore,
        *,
        actor_node_id: str = "controller",
        timestamp: Optional[str] = None,
    ) -> "StateMachine":
        event_store.require_controller(actor_node_id)
        if event_store.read_all():
            raise ValueError("cannot initialize state from a non-empty event log")
        event_store.append(
            EventType.RUN_STARTED,
            {"initialState": initial_state.to_dict()},
            initial_state.graph_version,
            actor_node_id=actor_node_id,
            timestamp=timestamp,
        )
        machine = cls(run_directory, initial_state, event_store)
        _atomic_write_state(machine.path, machine._state)
        return machine

    @classmethod
    def resume(cls, run_directory: Path, event_store: EventStore) -> "StateMachine":
        state = replay_events(event_store.read_all())
        machine = cls(run_directory, state, event_store)
        _atomic_write_state(machine.path, machine._state)
        return machine

    @property
    def state(self) -> RuntimeState:
        return _copy_state(self._state)

    def transition_node(
        self,
        node_id: str,
        target: NodeStatus,
        *,
        actor_node_id: str = "controller",
        timestamp: Optional[str] = None,
        max_attempts: Optional[int] = None,
        required_inputs_exist: bool = True,
        approval_outstanding: bool = False,
        error: Optional[str] = None,
        blocker: Optional[str] = None,
    ) -> RuntimeState:
        self.event_store.require_controller(actor_node_id)
        if self._poisoned:
            raise RuntimeError("state machine requires replay after a failed state write")
        current = self._state.node_states.get(node_id)
        if current is None:
            raise IllegalTransitionError(f"unknown node {node_id!r}")
        if (current.status, target) not in NODE_STATUS_TRANSITIONS:
            raise IllegalTransitionError(
                f"illegal node transition {current.status.value} to {target.value}"
            )
        if current.status == NodeStatus.FAILED and target == NodeStatus.READY:
            if max_attempts is None or current.attempts >= max_attempts:
                raise RetryRejectedError("attempt budget exhausted")
            if not required_inputs_exist:
                raise RetryRejectedError("required inputs are unavailable")
            if approval_outstanding:
                raise RetryRejectedError("required approval is outstanding")
        payload = {
            "nodeId": node_id,
            "fromStatus": current.status.value,
            "toStatus": target.value,
        }
        if error is not None:
            payload["error"] = error
        if blocker is not None:
            payload["blocker"] = blocker
        event = self.event_store.append(
            _event_type(current.status, target),
            payload,
            self._state.graph_version,
            actor_node_id=actor_node_id,
            timestamp=timestamp,
        )
        updated = _apply_transition(self._state, event.payload)
        try:
            _atomic_write_state(self.path, updated)
        except BaseException:
            self._poisoned = True
            raise
        self._state = updated
        return self.state

    def complete_run(
        self,
        *,
        actor_node_id: str = "controller",
        timestamp: Optional[str] = None,
    ) -> RuntimeState:
        """Persist the only successful terminal run transition as an event."""
        self.event_store.require_controller(actor_node_id)
        if self._poisoned:
            raise RuntimeError("state machine requires replay after a failed state write")
        if self._state.status != RunStatus.RUNNING:
            raise IllegalTransitionError(
                f"illegal run transition {self._state.status.value} to completed"
            )
        payload = {
            "fromRunStatus": self._state.status.value,
            "toRunStatus": RunStatus.COMPLETED.value,
        }
        event = self.event_store.append(
            EventType.RUN_COMPLETED,
            payload,
            self._state.graph_version,
            actor_node_id=actor_node_id,
            timestamp=timestamp,
        )
        updated = _apply_run_completion(self._state, event.payload)
        try:
            _atomic_write_state(self.path, updated)
        except BaseException:
            self._poisoned = True
            raise
        self._state = updated
        return self.state
