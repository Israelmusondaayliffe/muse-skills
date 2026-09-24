"""Bounded rewrite compilation, policy enforcement, and immutable version application."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable, Mapping, Optional, Sequence, Tuple

from .constants import (
    ApprovalStatus,
    ApprovalSubjectType,
    EdgeKind,
    EventType,
    ExecutionMode,
    NodeKind,
    NodeStatus,
    RiskLevel,
    RewriteOperationKind,
)
from .events import EventStore
from .models import Approval, Graph, NodeRuntimeState, RewriteOperation, RewriteProposal, RuntimeState
from .validation import parse_and_validate_rewritten_graph


class RewriteError(RuntimeError):
    """Base class for rewrite failures."""


class VersionMismatchError(RewriteError):
    """Raised when a proposal is not based on the current immutable version."""


class RewritePolicyError(RewriteError):
    """Raised when a rewrite is outside the declared policy contract."""


class ProhibitedMutationError(RewritePolicyError):
    """Raised for mutations that approval can never authorize."""


class ApprovalRequiredError(RewritePolicyError):
    """Raised when a medium or high risk proposal lacks explicit approval."""


class RewriteValidationError(RewriteError):
    """Raised when the complete rewritten graph violates an invariant."""


_RISK_ORDER = {RiskLevel.LOW: 0, RiskLevel.MEDIUM: 1, RiskLevel.HIGH: 2}
_INTERNAL_CAPABILITIES = frozenset(
    {"analysis", "artifact-read", "artifact-write", "evaluation", "file-read", "research", "state-read"}
)
_UPDATE_FIELDS = frozenset(
    {"label", "purpose", "critical", "priority", "execution", "inputs", "outputs", "successCriteria", "budget", "localLoop"}
)


def _canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")


def _graph_digest(graph: Graph) -> str:
    canonical = json.dumps(
        graph.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _atomic_replace(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _atomic_create(path: Path, content: bytes) -> None:
    """Create an immutable file using a staged same-filesystem hard link."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise RewritePolicyError(f"immutable record {path.name!r} already exists") from error
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _operation(value: RewriteOperation | Mapping[str, Any]) -> RewriteOperation:
    return value if isinstance(value, RewriteOperation) else RewriteOperation.from_dict(value)


def _node(graph: Graph, node_id: str) -> Any:
    for item in graph.nodes:
        if item.id == node_id:
            return item
    raise RewritePolicyError(f"unknown node {node_id!r}")


def _edge(graph: Graph, edge_id: str) -> Any:
    for item in graph.edges:
        if item.id == edge_id:
            return item
    raise RewritePolicyError(f"unknown edge {edge_id!r}")


def _external_node_data(value: Mapping[str, Any]) -> bool:
    execution = value.get("execution")
    if isinstance(execution, dict) and execution.get("mode") == ExecutionMode.TOOL.value:
        return True
    capabilities = value.get("capabilities", [])
    return isinstance(capabilities, list) and any(item not in _INTERNAL_CAPABILITIES for item in capabilities)


def _validate_policy(graph: Graph, operation: RewriteOperation) -> None:
    params = operation.params
    kind = operation.kind
    if kind == RewriteOperationKind.ADD_NODE:
        value = params.get("node")
        if not isinstance(value, dict):
            raise RewritePolicyError("add_node requires a node object")
        if any(item.id == value.get("id") for item in graph.nodes):
            raise RewritePolicyError(f"duplicate node {value.get('id')!r}")
        if value.get("kind") in {NodeKind.AUTHORITY.value, NodeKind.CONTROLLER.value}:
            raise ProhibitedMutationError("adding an authority or controller changes static authority boundaries")
    elif kind == RewriteOperationKind.UPDATE_NODE:
        node_id = params.get("nodeId")
        if not isinstance(node_id, str):
            raise RewritePolicyError("update_node requires nodeId")
        target = _node(graph, node_id)
        changes = params.get("changes")
        if not isinstance(changes, dict) or not changes:
            raise RewritePolicyError("update_node requires non-empty changes")
        prohibited = set(changes) - _UPDATE_FIELDS
        if prohibited:
            names = ", ".join(sorted(prohibited))
            raise ProhibitedMutationError(f"update_node cannot change protected fields: {names}")
        if target.kind in (NodeKind.AUTHORITY, NodeKind.CONTROLLER):
            raise ProhibitedMutationError(f"node {node_id!r} is part of the static authority boundary")
        if target.critical and changes.get("critical") is False:
            raise ProhibitedMutationError(
                f"node {node_id!r} cannot be downgraded to evade critical protection"
            )
        if "execution" in changes:
            execution = changes["execution"]
            if not isinstance(execution, dict):
                raise RewritePolicyError("execution update must be an object")
            old_capability = target.execution.to_dict()
            merged = {**old_capability, **execution}
            if merged.get("mode") == ExecutionMode.TOOL.value and target.execution.mode != ExecutionMode.TOOL:
                raise ProhibitedMutationError("update_node cannot expand a node into external tool permissions")
    elif kind == RewriteOperationKind.DISABLE_NODE:
        node_id = params.get("nodeId")
        if not isinstance(node_id, str):
            raise RewritePolicyError("disable_node requires nodeId")
        target = _node(graph, node_id)
        if target.kind in (NodeKind.AUTHORITY, NodeKind.CONTROLLER):
            raise ProhibitedMutationError(f"node {node_id!r} cannot be disabled")
    elif kind == RewriteOperationKind.ADD_EDGE:
        value = params.get("edge")
        if not isinstance(value, dict):
            raise RewritePolicyError("add_edge requires an edge object")
        if any(item.id == value.get("id") for item in graph.edges):
            raise RewritePolicyError(f"duplicate edge {value.get('id')!r}")
    elif kind == RewriteOperationKind.DISABLE_EDGE:
        edge_id = params.get("edgeId")
        if not isinstance(edge_id, str):
            raise RewritePolicyError("disable_edge requires edgeId")
        target = _edge(graph, edge_id)
        if target.required and target.kind in (EdgeKind.GOAL, EdgeKind.APPROVE):
            raise ProhibitedMutationError(f"edge {edge_id!r} is a protected authority or approval boundary")
    elif kind == RewriteOperationKind.SET_PRIORITY:
        node_id = params.get("nodeId")
        priority = params.get("priority")
        if not isinstance(node_id, str):
            raise RewritePolicyError("set_priority requires nodeId")
        _node(graph, node_id)
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise RewritePolicyError("set_priority requires an integer priority")
    else:
        raise RewritePolicyError(f"unsupported primitive operation {kind.value!r}")


def _operation_risk(
    graph: Graph,
    operation: RewriteOperation,
    state: Optional[RuntimeState] = None,
) -> RiskLevel:
    _validate_policy(graph, operation)
    params = operation.params
    if operation.kind == RewriteOperationKind.SET_PRIORITY:
        return RiskLevel.LOW
    if operation.kind == RewriteOperationKind.DISABLE_NODE:
        target = _node(graph, str(params["nodeId"]))
        if target.critical:
            return RiskLevel.HIGH
        runtime = state.node_states.get(target.id) if state is not None else None
        if runtime is not None and (
            runtime.attempts != 0
            or runtime.status not in (NodeStatus.PENDING, NodeStatus.READY, NodeStatus.BLOCKED)
        ):
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
    if operation.kind == RewriteOperationKind.ADD_NODE:
        value = params["node"]
        if _external_node_data(value):
            return RiskLevel.HIGH
        if value.get("kind") == NodeKind.EVALUATOR.value or "diagnostic" in str(value.get("purpose", "")).lower():
            return RiskLevel.LOW
        return RiskLevel.MEDIUM
    if operation.kind == RewriteOperationKind.UPDATE_NODE:
        changes = params["changes"]
        if set(changes) <= {"priority"}:
            return RiskLevel.LOW
        return RiskLevel.MEDIUM
    if operation.kind == RewriteOperationKind.DISABLE_EDGE:
        target = _edge(graph, str(params["edgeId"]))
        if target.required and target.kind == EdgeKind.VERIFY:
            return RiskLevel.HIGH
        return RiskLevel.MEDIUM if target.required else RiskLevel.LOW
    if operation.kind == RewriteOperationKind.ADD_EDGE:
        value = params["edge"]
        if value.get("temporal") == "next_epoch" or value.get("required") is False:
            return RiskLevel.LOW
        return RiskLevel.MEDIUM
    return RiskLevel.MEDIUM


def classify_risk(
    graph: Graph,
    operations: Iterable[RewriteOperation | Mapping[str, Any]],
    *,
    state: Optional[RuntimeState] = None,
) -> RiskLevel:
    """Return the highest policy risk across validated primitive operations."""
    risks = [_operation_risk(graph, _operation(item), state) for item in operations]
    return max(risks, key=_RISK_ORDER.__getitem__) if risks else RiskLevel.LOW


def apply_operations(
    graph: Graph,
    operations: Iterable[RewriteOperation | Mapping[str, Any]],
) -> Graph:
    """Apply primitives to an owned graph copy without bypassing policy checks."""
    data = deepcopy(graph.to_dict())
    current = graph
    for raw_operation in operations:
        operation = _operation(raw_operation)
        _validate_policy(current, operation)
        params = operation.params
        if operation.kind == RewriteOperationKind.ADD_NODE:
            data["nodes"].append(deepcopy(params["node"]))
        elif operation.kind == RewriteOperationKind.UPDATE_NODE:
            target = next(item for item in data["nodes"] if item["id"] == params["nodeId"])
            for key, value in params["changes"].items():
                if key == "execution" and isinstance(value, dict):
                    target[key] = {**target[key], **deepcopy(value)}
                else:
                    target[key] = deepcopy(value)
        elif operation.kind == RewriteOperationKind.DISABLE_NODE:
            next(item for item in data["nodes"] if item["id"] == params["nodeId"])["enabled"] = False
        elif operation.kind == RewriteOperationKind.ADD_EDGE:
            data["edges"].append(deepcopy(params["edge"]))
        elif operation.kind == RewriteOperationKind.DISABLE_EDGE:
            next(item for item in data["edges"] if item["id"] == params["edgeId"])["enabled"] = False
        elif operation.kind == RewriteOperationKind.SET_PRIORITY:
            next(item for item in data["nodes"] if item["id"] == params["nodeId"])["priority"] = params["priority"]
        current = Graph.from_dict(data)
    return Graph.from_dict(data)


def compile_pattern(pattern: str, params: Mapping[str, Any]) -> Tuple[RewriteOperation, ...]:
    """Compile a named restructuring pattern into the six primitive operations."""
    raw: list[dict[str, Any]] = []
    if pattern == "split_node":
        raw.append({"kind": "disable_node", "params": {"nodeId": params["nodeId"]}})
        raw.extend({"kind": "add_node", "params": {"node": item}} for item in params.get("nodes", []))
        raw.extend({"kind": "add_edge", "params": {"edge": item}} for item in params.get("edges", []))
    elif pattern == "merge_nodes":
        raw.extend({"kind": "disable_node", "params": {"nodeId": item}} for item in params.get("nodeIds", []))
        raw.append({"kind": "add_node", "params": {"node": params["node"]}})
        raw.extend({"kind": "add_edge", "params": {"edge": item}} for item in params.get("edges", []))
    elif pattern == "replace_node":
        raw.append({"kind": "disable_node", "params": {"nodeId": params["nodeId"]}})
        raw.append({"kind": "add_node", "params": {"node": params["node"]}})
        raw.extend({"kind": "add_edge", "params": {"edge": item}} for item in params.get("edges", []))
    elif pattern == "add_reviewer":
        raw = [
            {"kind": "add_node", "params": {"node": params["node"]}},
            {"kind": "add_edge", "params": {"edge": params["edge"]}},
        ]
    elif pattern == "reroute_edge":
        raw = [
            {"kind": "disable_edge", "params": {"edgeId": params["edgeId"]}},
            {"kind": "add_edge", "params": {"edge": params["edge"]}},
        ]
    elif pattern == "collapse_fanout":
        raw.extend({"kind": "disable_edge", "params": {"edgeId": item}} for item in params.get("edgeIds", []))
        raw.extend({"kind": "disable_node", "params": {"nodeId": item}} for item in params.get("nodeIds", []))
    elif pattern == "serialize_branch":
        raw = [{"kind": "add_edge", "params": {"edge": params["edge"]}}]
    elif pattern == "create_arbitration_node":
        raw = [{"kind": "add_node", "params": {"node": params["node"]}}]
        raw.extend({"kind": "add_edge", "params": {"edge": item}} for item in params.get("edges", []))
    elif pattern == "promote_successful_pattern":
        raw = [{"kind": "set_priority", "params": {"nodeId": params["nodeId"], "priority": params["priority"]}}]
    else:
        raise RewritePolicyError(f"unknown rewrite pattern {pattern!r}")
    if not raw:
        raise RewritePolicyError(f"rewrite pattern {pattern!r} compiled to no operations")
    return tuple(RewriteOperation.from_dict(item) for item in raw)


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RewriteError(f"cannot read trusted runtime file {path.name!r}: {error}") from error


class RewriteEngine:
    """Controller-owned proposal and application interface for one run."""

    def __init__(self, run_directory: Path, run_id: str) -> None:
        self.run_directory = Path(run_directory)
        self.run_id = run_id
        self.event_store = EventStore(self.run_directory, run_id)

    @classmethod
    def initialize(
        cls,
        run_directory: Path,
        graph: Graph,
        state: RuntimeState,
        *,
        timestamp: Optional[str] = None,
    ) -> "RewriteEngine":
        path = Path(run_directory)
        if state.graph_version != 1:
            raise VersionMismatchError("initial runtime state must use graph version 1")
        path.mkdir(parents=True, exist_ok=True)
        for child in ("rewrites/proposals", "rewrites/applied", "graph-versions"):
            (path / child).mkdir(parents=True, exist_ok=True)
        graph_bytes = _canonical_bytes(graph.to_dict())
        _atomic_create(path / "graph-versions" / "v0001.json", graph_bytes)
        _atomic_replace(path / "graph.json", graph_bytes)
        _atomic_replace(path / "state.json", _canonical_bytes(state.to_dict()))
        digest = _graph_digest(graph)
        _atomic_replace(path / "graph-versions" / "hashes.json", _canonical_bytes({"1": digest}))
        engine = cls(path, state.run_id)
        engine.event_store.append(EventType.GRAPH_CREATED, {"graphId": graph.graph_id}, 1, timestamp=timestamp)
        engine.event_store.append(EventType.GRAPH_VALIDATED, {"graphVersion": 1}, 1, timestamp=timestamp)
        engine.event_store.append(EventType.RUN_STARTED, {"initialState": state.to_dict()}, 1, timestamp=timestamp)
        return engine

    def _state(self) -> RuntimeState:
        state = RuntimeState.from_dict(_read_json(self.run_directory / "state.json"))
        if state.run_id != self.run_id:
            raise RewriteError("state run identifier does not match the rewrite engine")
        return state

    def _graph(self, version: Optional[int] = None) -> Graph:
        path = self.run_directory / "graph.json" if version is None else self.run_directory / "graph-versions" / f"v{version:04d}.json"
        return Graph.from_dict(_read_json(path))

    def propose(self, proposal: RewriteProposal, *, timestamp: Optional[str] = None) -> Path:
        state = self._state()
        if proposal.run_id != self.run_id:
            raise RewritePolicyError(f"proposal run id {proposal.run_id!r} does not match {self.run_id!r}")
        if proposal.base_graph_version != state.graph_version:
            raise VersionMismatchError(
                f"base graph version {proposal.base_graph_version} does not match current version {state.graph_version}"
            )
        rollback = self.run_directory / "graph-versions" / f"v{proposal.rollback_version:04d}.json"
        if not rollback.is_file():
            raise VersionMismatchError(f"rollback graph version {proposal.rollback_version} does not exist")
        graph = self._graph()
        classified = classify_risk(graph, proposal.operations, state=state)
        if _RISK_ORDER[proposal.risk_level] < _RISK_ORDER[classified]:
            raise RewritePolicyError(
                f"declared risk {proposal.risk_level.value} understates classified risk {classified.value}"
            )
        if classified in (RiskLevel.MEDIUM, RiskLevel.HIGH) and not proposal.approval_required:
            raise RewritePolicyError(f"{classified.value} risk rewrite must declare approvalRequired")
        destination = self.run_directory / "rewrites" / "proposals" / f"{proposal.proposal_id}.json"
        _atomic_create(destination, _canonical_bytes(proposal.to_dict()))
        self.event_store.append(
            EventType.REWRITE_PROPOSED,
            {"proposalId": proposal.proposal_id, "riskLevel": proposal.risk_level.value},
            state.graph_version,
            timestamp=timestamp,
        )
        return destination

    def _load_proposal(self, proposal_id: str) -> RewriteProposal:
        return RewriteProposal.from_dict(
            _read_json(self.run_directory / "rewrites" / "proposals" / f"{proposal_id}.json")
        )

    def apply(
        self,
        proposal_id: str,
        *,
        approvals: Sequence[Approval] = (),
        timestamp: Optional[str] = None,
    ) -> RuntimeState:
        proposal = self._load_proposal(proposal_id)
        state = self._state()
        if proposal.base_graph_version != state.graph_version:
            raise VersionMismatchError(
                f"base graph version {proposal.base_graph_version} does not match current version {state.graph_version}"
            )
        current = self._graph()
        classified = classify_risk(current, proposal.operations, state=state)
        if _RISK_ORDER[proposal.risk_level] < _RISK_ORDER[classified]:
            raise RewritePolicyError(
                f"declared risk {proposal.risk_level.value} understates classified risk {classified.value}"
            )
        approval_required = proposal.approval_required or classified in (RiskLevel.MEDIUM, RiskLevel.HIGH)
        if approval_required and not any(
            item.run_id == self.run_id
            and item.subject_type == ApprovalSubjectType.REWRITE
            and item.subject_id == proposal.proposal_id
            and item.status == ApprovalStatus.GRANTED
            for item in approvals
        ):
            raise ApprovalRequiredError(
                f"rewrite {proposal.proposal_id!r} requires a matching granted approval"
            )
        if classified == RiskLevel.LOW and state.auto_rewrites_applied >= current.limits.max_auto_rewrites:
            raise RewritePolicyError("automatic rewrite budget is exhausted")
        rewritten = apply_operations(current, proposal.operations)
        original = self._graph(1)
        result = parse_and_validate_rewritten_graph(rewritten.to_dict(), original_graph=original)
        if result.violations:
            raise RewriteValidationError("\n".join(str(item) for item in result.violations))
        assert result.graph is not None
        new_version = state.graph_version + 1
        if new_version > current.limits.max_graph_versions:
            raise RewritePolicyError("graph version budget is exhausted")
        version_path = self.run_directory / "graph-versions" / f"v{new_version:04d}.json"
        graph_bytes = _canonical_bytes(result.graph.to_dict())
        _atomic_create(version_path, graph_bytes)
        hashes_path = self.run_directory / "graph-versions" / "hashes.json"
        hashes = _read_json(hashes_path)
        hashes[str(new_version)] = _graph_digest(result.graph)
        updated_nodes = dict(state.node_states)
        for node in result.graph.nodes:
            updated_nodes.setdefault(node.id, NodeRuntimeState(node.id, NodeStatus.PENDING))
        updated_state = replace(
            state,
            graph_version=new_version,
            node_states=updated_nodes,
            auto_rewrites_applied=state.auto_rewrites_applied + (1 if classified == RiskLevel.LOW else 0),
        )
        applied_record = {
            **proposal.to_dict(),
            "classifiedRiskLevel": classified.value,
            "appliedGraphVersion": new_version,
            "rollbackVersion": proposal.rollback_version,
        }
        applied_path = self.run_directory / "rewrites" / "applied" / f"{proposal.proposal_id}.json"
        _atomic_create(applied_path, _canonical_bytes(applied_record))
        _atomic_replace(hashes_path, _canonical_bytes(hashes))
        _atomic_replace(self.run_directory / "graph.json", graph_bytes)
        _atomic_replace(self.run_directory / "state.json", _canonical_bytes(updated_state.to_dict()))
        self.event_store.append(
            EventType.REWRITE_APPLIED,
            {
                "proposalId": proposal.proposal_id,
                "baseGraphVersion": proposal.base_graph_version,
                "graphVersion": new_version,
                "rollbackVersion": proposal.rollback_version,
                "state": updated_state.to_dict(),
            },
            new_version,
            timestamp=timestamp,
        )
        return RuntimeState.from_dict(updated_state.to_dict())


__all__ = [
    "ApprovalRequiredError",
    "ProhibitedMutationError",
    "RewriteEngine",
    "RewriteError",
    "RewritePolicyError",
    "RewriteValidationError",
    "VersionMismatchError",
    "apply_operations",
    "classify_risk",
    "compile_pattern",
]
