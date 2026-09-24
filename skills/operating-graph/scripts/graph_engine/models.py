"""Strict, serializable dataclasses for the Operating Graph contracts."""

from __future__ import annotations

from dataclasses import dataclass, field, fields, is_dataclass
from datetime import datetime
from enum import Enum
import hashlib
import json
import math
from pathlib import PurePosixPath
import re
from typing import Any, Dict, List, Optional, Type, TypeVar

from .constants import (
    ActivationMode,
    ApprovalStatus,
    ApprovalSubjectType,
    Confidence,
    EdgeKind,
    EventType,
    ExecutionMode,
    NodeKind,
    NodeStatus,
    RiskLevel,
    RunStatus,
    RewriteOperationKind,
    Temporal,
    VerificationStatus,
)


EnumT = TypeVar("EnumT", bound=Enum)
_UTC_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


def _camel_case(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(part.capitalize() for part in tail)


def _json_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {
            _camel_case(item.name): _json_value(getattr(value, item.name))
            for item in fields(value)
        }
    if isinstance(value, list):
        return [_json_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    return value


def _object(value: Any, location: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{location}: expected object")
    return value


def _json_data(value: Any, location: str) -> Any:
    """Return an owned JSON-model copy after recursively validating it."""
    if value is None or isinstance(value, (bool, str)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{location}: expected finite number")
        return value
    if isinstance(value, list):
        return [_json_data(item, f"{location}[{index}]") for index, item in enumerate(value)]
    if isinstance(value, dict):
        if any(not isinstance(key, str) for key in value):
            raise ValueError(f"{location}: expected string keys")
        return {key: _json_data(item, f"{location}.{key}") for key, item in value.items()}
    raise ValueError(f"{location}: expected JSON value")


def _json_object(value: Any, location: str) -> Dict[str, Any]:
    return _json_data(_object(value, location), location)


def _required(data: Dict[str, Any], key: str, model: str) -> Any:
    if key not in data:
        raise ValueError(f"{model}.{key}: missing required field")
    return data[key]


def _string(value: Any, location: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{location}: expected string")
    return value


def _optional_string(value: Any, location: str) -> Optional[str]:
    if value is None:
        return None
    return _string(value, location)


def _integer(value: Any, location: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{location}: expected integer")
    return value


def _boolean(value: Any, location: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{location}: expected boolean")
    return value


def _list(value: Any, location: str) -> List[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{location}: expected array")
    return value


def _strings(value: Any, location: str) -> List[str]:
    return [_string(item, f"{location}[{index}]") for index, item in enumerate(_list(value, location))]


def _enum(enum_type: Type[EnumT], value: Any, location: str) -> EnumT:
    text = _string(value, location)
    try:
        return enum_type(text)
    except ValueError:
        raise ValueError(f"{location}: invalid {enum_type.__name__} value {text!r}") from None


def _timestamp(value: Any, location: str) -> str:
    text = _string(value, location)
    if not _UTC_TIMESTAMP.fullmatch(text):
        raise ValueError(f"{location}: expected canonical UTC timestamp")
    try:
        datetime.fromisoformat(f"{text[:-1]}+00:00")
    except ValueError:
        raise ValueError(f"{location}: expected canonical UTC timestamp") from None
    return text


class Serializable:
    def to_dict(self) -> Dict[str, Any]:
        return _json_value(self)


@dataclass(frozen=True)
class Deliverable(Serializable):
    id: str
    artifact_type: str
    description: str

    @classmethod
    def from_dict(cls, value: Any) -> "Deliverable":
        data = _object(value, "Deliverable")
        return cls(
            id=_string(_required(data, "id", "Deliverable"), "Deliverable.id"),
            artifact_type=_string(_required(data, "artifactType", "Deliverable"), "Deliverable.artifactType"),
            description=_string(_required(data, "description", "Deliverable"), "Deliverable.description"),
        )


@dataclass(frozen=True)
class Goal(Serializable):
    statement: str
    deliverables: List[Deliverable] = field(default_factory=list)
    completion_criteria: List[str] = field(default_factory=list)
    authority_node_id: str = ""

    @classmethod
    def from_dict(cls, value: Any) -> "Goal":
        data = _object(value, "Goal")
        return cls(
            statement=_string(_required(data, "statement", "Goal"), "Goal.statement"),
            deliverables=[Deliverable.from_dict(item) for item in _list(_required(data, "deliverables", "Goal"), "Goal.deliverables")],
            completion_criteria=_strings(_required(data, "completionCriteria", "Goal"), "Goal.completionCriteria"),
            authority_node_id=_string(_required(data, "authorityNodeId", "Goal"), "Goal.authorityNodeId"),
        )


@dataclass(frozen=True)
class ArtifactRequirement(Serializable):
    artifact_type: str
    required: bool

    @classmethod
    def from_dict(cls, value: Any) -> "ArtifactRequirement":
        data = _object(value, "ArtifactRequirement")
        return cls(
            artifact_type=_string(_required(data, "artifactType", "ArtifactRequirement"), "ArtifactRequirement.artifactType"),
            required=_boolean(_required(data, "required", "ArtifactRequirement"), "ArtifactRequirement.required"),
        )


@dataclass(frozen=True)
class Execution(Serializable):
    mode: ExecutionMode
    skill: Optional[str]
    model_hint: Optional[str]

    @classmethod
    def from_dict(cls, value: Any) -> "Execution":
        data = _object(value, "Execution")
        return cls(
            mode=_enum(ExecutionMode, _required(data, "mode", "Execution"), "Execution.mode"),
            skill=_optional_string(_required(data, "skill", "Execution"), "Execution.skill"),
            model_hint=_optional_string(_required(data, "modelHint", "Execution"), "Execution.modelHint"),
        )


@dataclass(frozen=True)
class Budget(Serializable):
    max_attempts: int
    work_units: int

    @classmethod
    def from_dict(cls, value: Any) -> "Budget":
        data = _object(value, "Budget")
        return cls(
            max_attempts=_integer(_required(data, "maxAttempts", "Budget"), "Budget.maxAttempts"),
            work_units=_integer(_required(data, "workUnits", "Budget"), "Budget.workUnits"),
        )


@dataclass(frozen=True)
class LocalLoop(Serializable):
    enabled: bool
    max_iterations: int
    sequence: List[str] = field(default_factory=list)
    stop_condition: str = ""

    @classmethod
    def from_dict(cls, value: Any) -> "LocalLoop":
        data = _object(value, "LocalLoop")
        return cls(
            enabled=_boolean(_required(data, "enabled", "LocalLoop"), "LocalLoop.enabled"),
            max_iterations=_integer(_required(data, "maxIterations", "LocalLoop"), "LocalLoop.maxIterations"),
            sequence=_strings(_required(data, "sequence", "LocalLoop"), "LocalLoop.sequence"),
            stop_condition=_string(_required(data, "stopCondition", "LocalLoop"), "LocalLoop.stopCondition"),
        )


@dataclass(frozen=True)
class Node(Serializable):
    id: str
    kind: NodeKind
    label: str
    purpose: str
    enabled: bool
    critical: bool
    priority: int
    execution: Execution
    capabilities: List[str] = field(default_factory=list)
    inputs: List[ArtifactRequirement] = field(default_factory=list)
    outputs: List[ArtifactRequirement] = field(default_factory=list)
    success_criteria: List[str] = field(default_factory=list)
    budget: Optional[Budget] = None
    local_loop: Optional[LocalLoop] = None

    @classmethod
    def from_dict(cls, value: Any) -> "Node":
        data = _object(value, "Node")
        return cls(
            id=_string(_required(data, "id", "Node"), "Node.id"),
            kind=_enum(NodeKind, _required(data, "kind", "Node"), "Node.kind"),
            label=_string(_required(data, "label", "Node"), "Node.label"),
            purpose=_string(_required(data, "purpose", "Node"), "Node.purpose"),
            enabled=_boolean(_required(data, "enabled", "Node"), "Node.enabled"),
            critical=_boolean(_required(data, "critical", "Node"), "Node.critical"),
            priority=_integer(_required(data, "priority", "Node"), "Node.priority"),
            execution=Execution.from_dict(_object(_required(data, "execution", "Node"), "Node.execution")),
            capabilities=_strings(_required(data, "capabilities", "Node"), "Node.capabilities"),
            inputs=[ArtifactRequirement.from_dict(item) for item in _list(_required(data, "inputs", "Node"), "Node.inputs")],
            outputs=[ArtifactRequirement.from_dict(item) for item in _list(_required(data, "outputs", "Node"), "Node.outputs")],
            success_criteria=_strings(_required(data, "successCriteria", "Node"), "Node.successCriteria"),
            budget=Budget.from_dict(_required(data, "budget", "Node")),
            local_loop=LocalLoop.from_dict(_required(data, "localLoop", "Node")),
        )


@dataclass(frozen=True)
class NodeStateRequirement(Serializable):
    node_id: str
    status: NodeStatus

    @classmethod
    def from_dict(cls, value: Any) -> "NodeStateRequirement":
        data = _object(value, "NodeStateRequirement")
        return cls(
            node_id=_string(_required(data, "nodeId", "NodeStateRequirement"), "NodeStateRequirement.nodeId"),
            status=_enum(NodeStatus, _required(data, "status", "NodeStateRequirement"), "NodeStateRequirement.status"),
        )


@dataclass(frozen=True)
class Activation(Serializable):
    mode: ActivationMode
    node_states: List[NodeStateRequirement] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    approvals: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Any) -> "Activation":
        data = _object(value, "Activation")
        return cls(
            mode=_enum(ActivationMode, _required(data, "mode", "Activation"), "Activation.mode"),
            node_states=[NodeStateRequirement.from_dict(item) for item in _list(_required(data, "nodeStates", "Activation"), "Activation.nodeStates")],
            artifacts=_strings(_required(data, "artifacts", "Activation"), "Activation.artifacts"),
            approvals=_strings(_required(data, "approvals", "Activation"), "Activation.approvals"),
        )


@dataclass(frozen=True)
class Edge(Serializable):
    id: str
    source: str
    target: str
    kind: EdgeKind
    enabled: bool
    required: bool
    temporal: Temporal
    artifact_types: List[str] = field(default_factory=list)
    activation: Optional[Activation] = None

    @classmethod
    def from_dict(cls, value: Any) -> "Edge":
        data = _object(value, "Edge")
        return cls(
            id=_string(_required(data, "id", "Edge"), "Edge.id"),
            source=_string(_required(data, "source", "Edge"), "Edge.source"),
            target=_string(_required(data, "target", "Edge"), "Edge.target"),
            kind=_enum(EdgeKind, _required(data, "kind", "Edge"), "Edge.kind"),
            enabled=_boolean(_required(data, "enabled", "Edge"), "Edge.enabled"),
            required=_boolean(_required(data, "required", "Edge"), "Edge.required"),
            temporal=_enum(Temporal, _required(data, "temporal", "Edge"), "Edge.temporal"),
            artifact_types=_strings(_required(data, "artifactTypes", "Edge"), "Edge.artifactTypes"),
            activation=Activation.from_dict(_required(data, "activation", "Edge")),
        )


@dataclass(frozen=True)
class Limits(Serializable):
    max_concurrent_workers: int
    max_node_runs: int
    max_graph_versions: int
    max_epochs: int
    max_auto_rewrites: int
    default_max_attempts: int

    @classmethod
    def from_dict(cls, value: Any) -> "Limits":
        data = _object(value, "Limits")
        return cls(
            max_concurrent_workers=_integer(_required(data, "maxConcurrentWorkers", "Limits"), "Limits.maxConcurrentWorkers"),
            max_node_runs=_integer(_required(data, "maxNodeRuns", "Limits"), "Limits.maxNodeRuns"),
            max_graph_versions=_integer(_required(data, "maxGraphVersions", "Limits"), "Limits.maxGraphVersions"),
            max_epochs=_integer(_required(data, "maxEpochs", "Limits"), "Limits.maxEpochs"),
            max_auto_rewrites=_integer(_required(data, "maxAutoRewrites", "Limits"), "Limits.maxAutoRewrites"),
            default_max_attempts=_integer(_required(data, "defaultMaxAttempts", "Limits"), "Limits.defaultMaxAttempts"),
        )


@dataclass(frozen=True)
class RewritePolicy(Serializable):
    automatic_risk_levels: List[RiskLevel] = field(default_factory=list)
    approval_risk_levels: List[RiskLevel] = field(default_factory=list)
    prohibited_mutations: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Any) -> "RewritePolicy":
        data = _object(value, "RewritePolicy")
        return cls(
            automatic_risk_levels=[_enum(RiskLevel, item, f"RewritePolicy.automaticRiskLevels[{index}]") for index, item in enumerate(_list(_required(data, "automaticRiskLevels", "RewritePolicy"), "RewritePolicy.automaticRiskLevels"))],
            approval_risk_levels=[_enum(RiskLevel, item, f"RewritePolicy.approvalRiskLevels[{index}]") for index, item in enumerate(_list(_required(data, "approvalRiskLevels", "RewritePolicy"), "RewritePolicy.approvalRiskLevels"))],
            prohibited_mutations=_strings(_required(data, "prohibitedMutations", "RewritePolicy"), "RewritePolicy.prohibitedMutations"),
        )


@dataclass(frozen=True)
class Graph(Serializable):
    schema_version: str
    graph_id: str
    name: str
    goal: Goal
    limits: Limits
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    rewrite_policy: Optional[RewritePolicy] = None
    metadata: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: Any) -> "Graph":
        data = _object(value, "Graph")
        metadata = _object(_required(data, "metadata", "Graph"), "Graph.metadata")
        created_by = _string(_required(metadata, "createdBy", "Graph.metadata"), "Graph.metadata.createdBy")
        created_at = _timestamp(_required(metadata, "createdAt", "Graph.metadata"), "Graph.metadata.createdAt")
        return cls(
            schema_version=_string(_required(data, "schemaVersion", "Graph"), "Graph.schemaVersion"),
            graph_id=_string(_required(data, "graphId", "Graph"), "Graph.graphId"),
            name=_string(_required(data, "name", "Graph"), "Graph.name"),
            goal=Goal.from_dict(_required(data, "goal", "Graph")),
            limits=Limits.from_dict(_required(data, "limits", "Graph")),
            nodes=[Node.from_dict(item) for item in _list(_required(data, "nodes", "Graph"), "Graph.nodes")],
            edges=[Edge.from_dict(item) for item in _list(_required(data, "edges", "Graph"), "Graph.edges")],
            rewrite_policy=RewritePolicy.from_dict(_required(data, "rewritePolicy", "Graph")),
            metadata={
                **{_string(key, "Graph.metadata key"): _string(item, f"Graph.metadata.{key}") for key, item in metadata.items()},
                "createdBy": created_by,
                "createdAt": created_at,
            },
        )


@dataclass(frozen=True)
class NodeRuntimeState(Serializable):
    node_id: str
    status: NodeStatus
    attempts: int = 0
    last_error: Optional[str] = None
    blocker: Optional[str] = None
    completed_epoch: Optional[int] = None
    output_artifact_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Any) -> "NodeRuntimeState":
        data = _object(value, "NodeRuntimeState")
        completed_epoch = data.get("completedEpoch")
        return cls(
            node_id=_string(_required(data, "nodeId", "NodeRuntimeState"), "NodeRuntimeState.nodeId"),
            status=_enum(NodeStatus, _required(data, "status", "NodeRuntimeState"), "NodeRuntimeState.status"),
            attempts=_integer(data.get("attempts", 0), "NodeRuntimeState.attempts"),
            last_error=_optional_string(data.get("lastError"), "NodeRuntimeState.lastError"),
            blocker=_optional_string(data.get("blocker"), "NodeRuntimeState.blocker"),
            completed_epoch=None if completed_epoch is None else _integer(completed_epoch, "NodeRuntimeState.completedEpoch"),
            output_artifact_ids=_strings(data.get("outputArtifactIds", []), "NodeRuntimeState.outputArtifactIds"),
        )


@dataclass(frozen=True)
class RuntimeState(Serializable):
    run_id: str
    graph_id: str
    graph_version: int
    epoch: int
    status: RunStatus
    node_states: Dict[str, NodeRuntimeState] = field(default_factory=dict)
    total_node_runs: int = 0
    auto_rewrites_applied: int = 0
    budget_thresholds_emitted: List[int] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Any) -> "RuntimeState":
        data = _object(value, "RuntimeState")
        node_states = _object(_required(data, "nodeStates", "RuntimeState"), "RuntimeState.nodeStates")
        return cls(
            run_id=_string(_required(data, "runId", "RuntimeState"), "RuntimeState.runId"),
            graph_id=_string(_required(data, "graphId", "RuntimeState"), "RuntimeState.graphId"),
            graph_version=_integer(_required(data, "graphVersion", "RuntimeState"), "RuntimeState.graphVersion"),
            epoch=_integer(_required(data, "epoch", "RuntimeState"), "RuntimeState.epoch"),
            status=_enum(RunStatus, _required(data, "status", "RuntimeState"), "RuntimeState.status"),
            node_states={_string(key, "RuntimeState.nodeStates key"): NodeRuntimeState.from_dict(item) for key, item in node_states.items()},
            total_node_runs=_integer(data.get("totalNodeRuns", 0), "RuntimeState.totalNodeRuns"),
            auto_rewrites_applied=_integer(data.get("autoRewritesApplied", 0), "RuntimeState.autoRewritesApplied"),
            budget_thresholds_emitted=[_integer(item, f"RuntimeState.budgetThresholdsEmitted[{index}]") for index, item in enumerate(_list(data.get("budgetThresholdsEmitted", []), "RuntimeState.budgetThresholdsEmitted"))],
        )


@dataclass(frozen=True)
class Event(Serializable):
    event_id: str
    sequence: int
    timestamp: str
    run_id: str
    graph_version: int
    actor_node_id: str
    type: EventType
    payload: Dict[str, Any]
    previous_hash: Optional[str]
    event_hash: str
    _canonical_without_hash: str = field(init=False, repr=False, compare=False)
    _canonical_with_hash: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        payload = _json_object(self.payload, "Event.payload")
        object.__setattr__(self, "payload", payload)
        data = {
            "eventId": self.event_id,
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "runId": self.run_id,
            "graphVersion": self.graph_version,
            "actorNodeId": self.actor_node_id,
            "type": self.type.value,
            "payload": payload,
            "previousHash": self.previous_hash,
        }
        canonical_without_hash = json.dumps(
            data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        )
        object.__setattr__(self, "_canonical_without_hash", canonical_without_hash)
        data["eventHash"] = self.event_hash
        object.__setattr__(
            self,
            "_canonical_with_hash",
            json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False),
        )

    @classmethod
    def from_dict(cls, value: Any) -> "Event":
        data = _object(value, "Event")
        return cls(
            event_id=_string(_required(data, "eventId", "Event"), "Event.eventId"),
            sequence=_integer(_required(data, "sequence", "Event"), "Event.sequence"),
            timestamp=_timestamp(_required(data, "timestamp", "Event"), "Event.timestamp"),
            run_id=_string(_required(data, "runId", "Event"), "Event.runId"),
            graph_version=_integer(_required(data, "graphVersion", "Event"), "Event.graphVersion"),
            actor_node_id=_string(_required(data, "actorNodeId", "Event"), "Event.actorNodeId"),
            type=_enum(EventType, _required(data, "type", "Event"), "Event.type"),
            payload=_json_object(_required(data, "payload", "Event"), "Event.payload"),
            previous_hash=_optional_string(_required(data, "previousHash", "Event"), "Event.previousHash"),
            event_hash=_string(_required(data, "eventHash", "Event"), "Event.eventHash"),
        )

    def canonical_json(self, include_event_hash: bool = False) -> str:
        return self._canonical_with_hash if include_event_hash else self._canonical_without_hash

    def to_dict(self) -> Dict[str, Any]:
        return json.loads(self._canonical_with_hash)

    def calculated_hash(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Evidence(Serializable):
    source: str
    claim: str
    confidence: Confidence

    @classmethod
    def from_dict(cls, value: Any) -> "Evidence":
        data = _object(value, "Evidence")
        return cls(
            source=_string(_required(data, "source", "Evidence"), "Evidence.source"),
            claim=_string(_required(data, "claim", "Evidence"), "Evidence.claim"),
            confidence=_enum(Confidence, _required(data, "confidence", "Evidence"), "Evidence.confidence"),
        )


@dataclass(frozen=True)
class Artifact(Serializable):
    artifact_id: str
    run_id: str
    node_id: str
    graph_version: int
    type: str
    path: str
    media_type: str
    sha256: str
    created_at: str
    supersedes: Optional[str]
    evidence: List[Evidence] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Any) -> "Artifact":
        data = _object(value, "Artifact")
        artifact_id = _string(_required(data, "artifactId", "Artifact"), "Artifact.artifactId")
        run_id = _string(_required(data, "runId", "Artifact"), "Artifact.runId")
        node_id = _string(_required(data, "nodeId", "Artifact"), "Artifact.nodeId")
        graph_version = _integer(_required(data, "graphVersion", "Artifact"), "Artifact.graphVersion")
        artifact_type = _string(_required(data, "type", "Artifact"), "Artifact.type")
        path = _string(_required(data, "path", "Artifact"), "Artifact.path")
        if not path or PurePosixPath(path).is_absolute():
            raise ValueError("Artifact.path: expected relative path")
        return cls(
            artifact_id=artifact_id,
            run_id=run_id,
            node_id=node_id,
            graph_version=graph_version,
            type=artifact_type,
            path=path,
            media_type=_string(_required(data, "mediaType", "Artifact"), "Artifact.mediaType"),
            sha256=_string(_required(data, "sha256", "Artifact"), "Artifact.sha256"),
            created_at=_timestamp(_required(data, "createdAt", "Artifact"), "Artifact.createdAt"),
            supersedes=_optional_string(_required(data, "supersedes", "Artifact"), "Artifact.supersedes"),
            evidence=[Evidence.from_dict(item) for item in _list(_required(data, "evidence", "Artifact"), "Artifact.evidence")],
        )


@dataclass(frozen=True)
class Approval(Serializable):
    approval_id: str
    run_id: str
    subject_type: ApprovalSubjectType
    subject_id: str
    requested_by: str
    required_from: str
    status: ApprovalStatus
    requested_at: str
    resolved_at: Optional[str] = None
    resolved_by: Optional[str] = None
    reason: Optional[str] = None

    @classmethod
    def from_dict(cls, value: Any) -> "Approval":
        data = _object(value, "Approval")
        approval_id = _string(_required(data, "approvalId", "Approval"), "Approval.approvalId")
        run_id = _string(_required(data, "runId", "Approval"), "Approval.runId")
        subject_type = _enum(ApprovalSubjectType, _required(data, "subjectType", "Approval"), "Approval.subjectType")
        subject_id = _string(_required(data, "subjectId", "Approval"), "Approval.subjectId")
        requested_by = _string(_required(data, "requestedBy", "Approval"), "Approval.requestedBy")
        required_from = _string(_required(data, "requiredFrom", "Approval"), "Approval.requiredFrom")
        status = _enum(ApprovalStatus, _required(data, "status", "Approval"), "Approval.status")
        requested_at = _timestamp(_required(data, "requestedAt", "Approval"), "Approval.requestedAt")
        resolved_at = data.get("resolvedAt")
        return cls(
            approval_id=approval_id,
            run_id=run_id,
            subject_type=subject_type,
            subject_id=subject_id,
            requested_by=requested_by,
            required_from=required_from,
            status=status,
            requested_at=requested_at,
            resolved_at=None if resolved_at is None else _timestamp(resolved_at, "Approval.resolvedAt"),
            resolved_by=_optional_string(data.get("resolvedBy"), "Approval.resolvedBy"),
            reason=_optional_string(data.get("reason"), "Approval.reason"),
        )


@dataclass(frozen=True)
class RewriteOperation(Serializable):
    kind: RewriteOperationKind
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: Any) -> "RewriteOperation":
        data = _object(value, "RewriteOperation")
        return cls(
            kind=_enum(RewriteOperationKind, _required(data, "kind", "RewriteOperation"), "RewriteOperation.kind"),
            params=_json_object(_required(data, "params", "RewriteOperation"), "RewriteOperation.params"),
        )


@dataclass(frozen=True)
class RewriteProposal(Serializable):
    proposal_id: str
    run_id: str
    base_graph_version: int
    trigger: str
    evidence_event_ids: List[str] = field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    reason: str = ""
    predicted_effect: str = ""
    operations: List[RewriteOperation] = field(default_factory=list)
    approval_required: bool = False
    rollback_version: int = 0

    @classmethod
    def from_dict(cls, value: Any) -> "RewriteProposal":
        data = _object(value, "RewriteProposal")
        return cls(
            proposal_id=_string(_required(data, "proposalId", "RewriteProposal"), "RewriteProposal.proposalId"),
            run_id=_string(_required(data, "runId", "RewriteProposal"), "RewriteProposal.runId"),
            base_graph_version=_integer(_required(data, "baseGraphVersion", "RewriteProposal"), "RewriteProposal.baseGraphVersion"),
            trigger=_string(_required(data, "trigger", "RewriteProposal"), "RewriteProposal.trigger"),
            evidence_event_ids=_strings(_required(data, "evidenceEventIds", "RewriteProposal"), "RewriteProposal.evidenceEventIds"),
            risk_level=_enum(RiskLevel, _required(data, "riskLevel", "RewriteProposal"), "RewriteProposal.riskLevel"),
            reason=_string(_required(data, "reason", "RewriteProposal"), "RewriteProposal.reason"),
            predicted_effect=_string(_required(data, "predictedEffect", "RewriteProposal"), "RewriteProposal.predictedEffect"),
            operations=[RewriteOperation.from_dict(item) for item in _list(_required(data, "operations", "RewriteProposal"), "RewriteProposal.operations")],
            approval_required=_boolean(_required(data, "approvalRequired", "RewriteProposal"), "RewriteProposal.approvalRequired"),
            rollback_version=_integer(_required(data, "rollbackVersion", "RewriteProposal"), "RewriteProposal.rollbackVersion"),
        )


@dataclass(frozen=True)
class VerificationResult(Serializable):
    status: VerificationStatus
    checked_at: str
    criteria: List[Dict[str, Any]] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    evidence_artifact_ids: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, value: Any) -> "VerificationResult":
        data = _object(value, "VerificationResult")
        status = _enum(VerificationStatus, _required(data, "status", "VerificationResult"), "VerificationResult.status")
        checked_at = _timestamp(_required(data, "checkedAt", "VerificationResult"), "VerificationResult.checkedAt")
        criteria = _list(_required(data, "criteria", "VerificationResult"), "VerificationResult.criteria")
        return cls(
            status=status,
            checked_at=checked_at,
            criteria=[_json_object(item, f"VerificationResult.criteria[{index}]") for index, item in enumerate(criteria)],
            issues=_strings(_required(data, "issues", "VerificationResult"), "VerificationResult.issues"),
            evidence_artifact_ids=_strings(_required(data, "evidenceArtifactIds", "VerificationResult"), "VerificationResult.evidenceArtifactIds"),
        )
