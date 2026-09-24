"""Deterministic readiness, concurrency, epoch, and deadlock decisions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional, Sequence, Tuple

from .artifacts import ArtifactRegistry
from .constants import ActivationMode, ApprovalStatus, NodeStatus, RunStatus, Temporal
from .models import Approval, Edge, Graph, Node, RuntimeState


_ELIGIBLE_STATUSES = frozenset(
    {NodeStatus.PENDING, NodeStatus.BLOCKED, NodeStatus.FAILED}
)
_TERMINAL_STATUSES = frozenset(
    {
        NodeStatus.SUCCEEDED,
        NodeStatus.SKIPPED,
        NodeStatus.CANCELLED,
    }
)


@dataclass(frozen=True)
class DeadlockReport:
    """Deterministic evidence that an incomplete run cannot schedule work."""

    blocked_node_ids: Tuple[str, ...]
    reason: str = "incomplete graph has no runnable nodes or epoch transition"


def _granted_approval_ids(approvals: Iterable[Approval]) -> frozenset[str]:
    granted = set()
    for approval in approvals:
        if approval.status == ApprovalStatus.GRANTED:
            granted.add(approval.approval_id)
            granted.add(approval.subject_id)
    return frozenset(granted)


def _node_state_condition(
    edge: Edge,
    node_id: str,
    required_status: NodeStatus,
    state: RuntimeState,
) -> bool:
    runtime = state.node_states.get(node_id)
    if runtime is None or runtime.status != required_status:
        return False
    if required_status != NodeStatus.SUCCEEDED:
        return True
    if edge.temporal == Temporal.NEXT_EPOCH:
        return state.epoch > 1 and runtime.completed_epoch == state.epoch - 1
    return runtime.completed_epoch == state.epoch


def _temporal_condition(edge: Edge, state: RuntimeState) -> bool:
    if edge.temporal == Temporal.SAME_EPOCH:
        return True
    source = state.node_states.get(edge.source)
    return (
        state.epoch > 1
        and source is not None
        and source.completed_epoch == state.epoch - 1
    )


def _edge_satisfied(
    edge: Edge,
    state: RuntimeState,
    artifact_registry: Optional[ArtifactRegistry],
    granted_approval_ids: frozenset[str],
) -> bool:
    if not _temporal_condition(edge, state):
        return False
    if edge.artifact_types and (
        artifact_registry is None
        or not artifact_registry.satisfies_activation(edge.artifact_types)
    ):
        return False
    activation = edge.activation
    conditions = []
    if activation is not None:
        conditions.extend(
            _node_state_condition(edge, item.node_id, item.status, state)
            for item in activation.node_states
        )
        conditions.extend(
            artifact_registry is not None
            and artifact_registry.satisfies_activation((artifact_type,))
            for artifact_type in activation.artifacts
        )
        conditions.extend(
            approval_id in granted_approval_ids
            for approval_id in activation.approvals
        )
    if not conditions:
        source = state.node_states.get(edge.source)
        if source is None or source.status != NodeStatus.SUCCEEDED:
            return False
        if edge.temporal == Temporal.SAME_EPOCH:
            return source.completed_epoch == state.epoch
        return source.completed_epoch == state.epoch - 1
    if activation is not None and activation.mode == ActivationMode.ANY:
        return any(conditions)
    return all(conditions)


def _node_attempt_limit(graph: Graph, node: Node) -> int:
    if node.budget is not None:
        return node.budget.max_attempts
    return graph.limits.default_max_attempts


def _node_is_ready(
    graph: Graph,
    node: Node,
    state: RuntimeState,
    artifact_registry: Optional[ArtifactRegistry],
    granted_approval_ids: frozenset[str],
) -> bool:
    if not node.enabled or state.status != RunStatus.RUNNING:
        return False
    if state.epoch < 1 or state.epoch > graph.limits.max_epochs:
        return False
    runtime = state.node_states.get(node.id)
    if runtime is None or runtime.status not in _ELIGIBLE_STATUSES:
        return False
    if runtime.attempts >= _node_attempt_limit(graph, node):
        return False
    if state.total_node_runs >= graph.limits.max_node_runs:
        return False
    required_inputs = tuple(
        item.artifact_type for item in node.inputs if item.required
    )
    if required_inputs and (
        artifact_registry is None
        or not artifact_registry.satisfies_activation(required_inputs)
    ):
        return False
    incoming = tuple(
        edge
        for edge in graph.edges
        if edge.enabled and edge.required and edge.target == node.id
    )
    return all(
        _edge_satisfied(
            edge,
            state,
            artifact_registry,
            granted_approval_ids,
        )
        for edge in incoming
    )


def _downstream_required_count(
    graph: Graph, state: RuntimeState, node_id: str
) -> int:
    return len(
        {
            edge.target
            for edge in graph.edges
            if edge.enabled
            and edge.required
            and edge.source == node_id
            and state.node_states.get(edge.target) is not None
            and state.node_states[edge.target].status not in _TERMINAL_STATUSES
        }
    )


def concurrency_limit(
    graph: Graph,
    state: RuntimeState,
    *,
    detected_available_worker_slots: Optional[int] = None,
    fixed_agent_limit: Optional[int] = None,
) -> int:
    """Clamp dispatch capacity while reserving a fixed harness slot for control."""
    running = sum(
        runtime.status == NodeStatus.RUNNING
        for runtime in state.node_states.values()
    )
    graph_slots = max(0, graph.limits.max_concurrent_workers - running)
    detected = graph_slots if detected_available_worker_slots is None else max(
        0, detected_available_worker_slots
    )
    if fixed_agent_limit is not None:
        detected = min(detected, max(0, fixed_agent_limit - 1))
    return min(graph_slots, detected)


def get_ready_nodes(
    graph: Graph,
    state: RuntimeState,
    *,
    artifact_registry: Optional[ArtifactRegistry] = None,
    approvals: Sequence[Approval] = (),
    detected_available_worker_slots: Optional[int] = None,
    fixed_agent_limit: Optional[int] = None,
) -> Tuple[Node, ...]:
    """Return the deterministically ordered nodes dispatchable in this decision."""
    granted = _granted_approval_ids(approvals)
    ready = [
        node
        for node in graph.nodes
        if _node_is_ready(graph, node, state, artifact_registry, granted)
    ]
    ready.sort(
        key=lambda node: (
            -node.priority,
            -int(node.critical),
            -_downstream_required_count(graph, state, node.id),
            node.id,
        )
    )
    limit = concurrency_limit(
        graph,
        state,
        detected_available_worker_slots=detected_available_worker_slots,
        fixed_agent_limit=fixed_agent_limit,
    )
    return tuple(ready[:limit])


def can_advance_epoch(graph: Graph, state: RuntimeState) -> bool:
    """Return whether next-epoch work exists after the current epoch completes."""
    if state.status != RunStatus.RUNNING or state.epoch >= graph.limits.max_epochs:
        return False
    if any(
        runtime.status in (NodeStatus.RUNNING, NodeStatus.READY)
        for runtime in state.node_states.values()
    ):
        return False
    for edge in graph.edges:
        if not edge.enabled or not edge.required or edge.temporal != Temporal.NEXT_EPOCH:
            continue
        source = state.node_states.get(edge.source)
        target = state.node_states.get(edge.target)
        if (
            source is not None
            and source.status == NodeStatus.SUCCEEDED
            and source.completed_epoch == state.epoch
            and target is not None
            and target.status in _ELIGIBLE_STATUSES
        ):
            return True
    return False


def detect_deadlock(
    graph: Graph,
    state: RuntimeState,
    *,
    artifact_registry: Optional[ArtifactRegistry] = None,
    approvals: Sequence[Approval] = (),
) -> Optional[DeadlockReport]:
    """Report an incomplete run with no running, ready, or next-epoch work."""
    if state.status != RunStatus.RUNNING:
        return None
    enabled = [node for node in graph.nodes if node.enabled]
    if enabled and all(
        state.node_states.get(node.id) is not None
        and state.node_states[node.id].status in _TERMINAL_STATUSES
        for node in enabled
    ):
        return None
    if any(
        runtime.status in (NodeStatus.RUNNING, NodeStatus.READY)
        for runtime in state.node_states.values()
    ):
        return None
    if get_ready_nodes(
        graph,
        state,
        artifact_registry=artifact_registry,
        approvals=approvals,
    ):
        return None
    if can_advance_epoch(graph, state):
        return None
    blocked = tuple(
        sorted(
            node.id
            for node in enabled
            if state.node_states.get(node.id) is not None
            and state.node_states[node.id].status not in _TERMINAL_STATUSES
        )
    )
    return DeadlockReport(blocked_node_ids=blocked)


__all__ = [
    "DeadlockReport",
    "can_advance_epoch",
    "concurrency_limit",
    "detect_deadlock",
    "get_ready_nodes",
]
