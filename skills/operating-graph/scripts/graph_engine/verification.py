"""Original-goal terminal verification for Operating Graph runs."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterable, Optional, Sequence, Tuple

from .artifacts import ArtifactError, ArtifactRegistry
from .constants import (
    ApprovalStatus,
    EdgeKind,
    EventType,
    NodeKind,
    NodeStatus,
    RiskLevel,
    RunStatus,
    VerificationStatus,
)
from .events import EventChainError, EventStore
from .dispatch import thread_history_issues
from .invariants import validate_graph_versions
from .models import Approval, Artifact, Graph, RuntimeState, VerificationResult
from .state import StateMachine
from .validation import parse_and_validate_rewritten_graph


class VerificationError(RuntimeError):
    """Base class for terminal verification failures."""


class VerificationCorruptionError(VerificationError):
    """Raised when trusted runtime records cannot be safely inspected."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise VerificationCorruptionError(f"corrupt runtime file {path.name!r}: {error}") from error


def _atomic_replace(path: Path, value: Any) -> None:
    content = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
        + "\n"
    ).encode("utf-8")
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


def _read_approvals(path: Path, run_id: str) -> Tuple[Approval, ...]:
    if not path.exists():
        return ()
    approvals = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            approval = Approval.from_dict(json.loads(line))
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            raise VerificationCorruptionError(
                f"corrupt approval record on line {line_number}: {error}"
            ) from error
        if approval.run_id != run_id:
            raise VerificationCorruptionError(
                f"approval {approval.approval_id!r} belongs to another run"
            )
        approvals.append(approval)
    return tuple(approvals)


def _reachable_sources(graph: Graph, producer_id: str) -> frozenset[str]:
    adjacency: dict[str, set[str]] = {}
    for edge in graph.edges:
        if edge.enabled and edge.kind not in (EdgeKind.VERIFY, EdgeKind.APPROVE):
            adjacency.setdefault(edge.source, set()).add(edge.target)
    reached = {producer_id}
    pending = [producer_id]
    while pending:
        source = pending.pop()
        for target in sorted(adjacency.get(source, ())):
            if target not in reached:
                reached.add(target)
                pending.append(target)
    return frozenset(reached)


def _has_completed_independent_evaluation(
    graph: Graph,
    state: RuntimeState,
    artifact: Artifact,
) -> bool:
    nodes = {node.id: node for node in graph.nodes if node.enabled}
    producing_flow = _reachable_sources(graph, artifact.node_id)
    return any(
        edge.enabled
        and edge.kind == EdgeKind.VERIFY
        and edge.source in producing_flow
        and edge.target != artifact.node_id
        and artifact.type in edge.artifact_types
        and edge.target in nodes
        and nodes[edge.target].kind == NodeKind.EVALUATOR
        and state.node_states.get(edge.target) is not None
        and state.node_states[edge.target].status == NodeStatus.SUCCEEDED
        for edge in graph.edges
    )


def _required_approval_issues(
    graph: Graph,
    run_directory: Path,
    approvals: Sequence[Approval],
) -> list[str]:
    granted_ids = {
        value
        for approval in approvals
        if approval.status == ApprovalStatus.GRANTED
        for value in (approval.approval_id, approval.subject_id)
    }
    issues = []
    declared = {
        approval_id
        for edge in graph.edges
        if edge.enabled and edge.required and edge.activation is not None
        for approval_id in edge.activation.approvals
    }
    for approval_id in sorted(declared):
        if approval_id not in granted_ids:
            issues.append(f"required approval {approval_id!r} is not granted")
    for edge in graph.edges:
        if edge.enabled and edge.required and edge.kind == EdgeKind.APPROVE:
            if edge.id not in granted_ids and edge.target not in granted_ids:
                issues.append(
                    f"required approval edge {edge.id!r} for node {edge.target!r} is not granted"
                )
    applied_directory = run_directory / "rewrites" / "applied"
    for path in sorted(applied_directory.glob("*.json")) if applied_directory.exists() else ():
        record = _read_json(path)
        proposal_id = record.get("proposalId")
        classified = record.get("classifiedRiskLevel", record.get("riskLevel"))
        required = record.get("approvalRequired") is True or classified in {
            RiskLevel.MEDIUM.value,
            RiskLevel.HIGH.value,
        }
        if required and proposal_id not in granted_ids:
            issues.append(f"applied rewrite {proposal_id!r} has no granted approval record")
    return issues


class Verifier:
    """Verify completion against version one, not the mutable current topology."""

    def __init__(self, run_directory: Path) -> None:
        self.run_directory = Path(run_directory)

    def _trusted_context(self) -> tuple[RuntimeState, Graph, Graph, EventStore, ArtifactRegistry, Tuple[Approval, ...]]:
        state = RuntimeState.from_dict(_read_json(self.run_directory / "state.json"))
        store = EventStore(self.run_directory, state.run_id)
        try:
            store.read_all()
        except EventChainError as error:
            raise VerificationCorruptionError(f"event chain is corrupt: {error}") from error
        original = Graph.from_dict(_read_json(self.run_directory / "graph-versions" / "v0001.json"))
        current = Graph.from_dict(_read_json(self.run_directory / "graph.json"))
        version_files = sorted((self.run_directory / "graph-versions").glob("v*.json"))
        versions: dict[int, Graph] = {}
        for path in version_files:
            try:
                version = int(path.stem[1:])
            except ValueError as error:
                raise VerificationCorruptionError(f"invalid graph version filename {path.name!r}") from error
            versions[version] = Graph.from_dict(_read_json(path))
        hashes_data = _read_json(self.run_directory / "graph-versions" / "hashes.json")
        trusted = {int(key): str(value) for key, value in hashes_data.items()}
        version_violations = validate_graph_versions(versions, immutable_hashes=trusted)
        if version_violations:
            raise VerificationCorruptionError("\n".join(str(item) for item in version_violations))
        if state.graph_version not in versions or versions[state.graph_version].to_dict() != current.to_dict():
            raise VerificationCorruptionError("current graph does not match the state graph version")
        registry = ArtifactRegistry(self.run_directory, state.run_id, store)
        approvals = _read_approvals(self.run_directory / "approvals.jsonl", state.run_id)
        return state, original, current, store, registry, approvals

    def verify(self, *, timestamp: Optional[str] = None) -> VerificationResult:
        state, original, current, store, registry, approvals = self._trusted_context()
        checked_at = timestamp or _utc_now()
        store.append(
            EventType.VERIFICATION_STARTED,
            {"originalGraphVersion": 1, "currentGraphVersion": state.graph_version},
            state.graph_version,
            timestamp=timestamp,
        )
        mandatory: list[str] = []
        limitations: list[str] = []
        evidence_ids: list[str] = []

        rewrite_validation = parse_and_validate_rewritten_graph(
            current.to_dict(), original_graph=original
        )
        mandatory.extend(str(item) for item in rewrite_validation.violations)
        mandatory.extend(thread_history_issues(self.run_directory, current, state))

        try:
            artifacts = registry.read_all()
        except ArtifactError as error:
            artifacts = ()
            mandatory.append(f"artifact registry integrity failed: {error}")
        for deliverable in original.goal.deliverables:
            candidates = [item for item in artifacts if item.type == deliverable.artifact_type]
            valid: list[Artifact] = []
            integrity_errors: list[str] = []
            for artifact in candidates:
                try:
                    valid.append(registry.verify(artifact.artifact_id))
                except ArtifactError as error:
                    integrity_errors.append(str(error))
            if not valid:
                if integrity_errors:
                    mandatory.extend(
                        f"deliverable {deliverable.id!r} integrity failed: {error}"
                        for error in integrity_errors
                    )
                else:
                    mandatory.append(
                        f"deliverable {deliverable.id!r} is missing active artifact type {deliverable.artifact_type!r}"
                    )
                continue
            for artifact in valid:
                evidence_ids.append(artifact.artifact_id)
                if not artifact.evidence:
                    mandatory.append(
                        f"deliverable artifact {artifact.artifact_id!r} has no evidence provenance"
                    )
                if not _has_completed_independent_evaluation(current, state, artifact):
                    mandatory.append(
                        f"deliverable artifact {artifact.artifact_id!r} lacks a completed independent evaluator"
                    )

        mandatory.extend(_required_approval_issues(current, self.run_directory, approvals))
        for node in current.nodes:
            if not node.enabled:
                if node.critical:
                    mandatory.append(f"critical node {node.id!r} is disabled")
                continue
            runtime = state.node_states.get(node.id)
            if runtime is None:
                if node.critical:
                    mandatory.append(f"critical node {node.id!r} has no runtime state")
                continue
            if node.critical and runtime.status != NodeStatus.SUCCEEDED:
                mandatory.append(
                    f"critical node {node.id!r} remains {runtime.status.value}"
                )
            elif not node.critical and runtime.status in (NodeStatus.FAILED, NodeStatus.BLOCKED):
                limitations.append(
                    f"non-critical node {node.id!r} remains {runtime.status.value}"
                )

        mandatory = sorted(set(mandatory))
        limitations = sorted(set(limitations))
        if mandatory:
            status = VerificationStatus.FAIL
            issues = mandatory + limitations
        elif limitations:
            status = VerificationStatus.CONDITIONAL_PASS
            issues = limitations
        else:
            status = VerificationStatus.PASS
            issues = []
        criteria = [
            {
                "criterion": criterion,
                "satisfied": not mandatory,
                "basis": "original immutable goal and registered runtime evidence",
            }
            for criterion in original.goal.completion_criteria
        ]
        result = VerificationResult(
            status=status,
            checked_at=checked_at,
            criteria=criteria,
            issues=issues,
            evidence_artifact_ids=sorted(set(evidence_ids)),
        )
        _atomic_replace(self.run_directory / "verification.json", result.to_dict())
        final_event = (
            EventType.VERIFICATION_FAILED
            if status == VerificationStatus.FAIL
            else EventType.VERIFICATION_PASSED
        )
        store.append(
            final_event,
            {"status": status.value, "issues": issues},
            state.graph_version,
            timestamp=timestamp,
        )
        if status in (VerificationStatus.PASS, VerificationStatus.CONDITIONAL_PASS):
            if state.status == RunStatus.RUNNING:
                StateMachine(self.run_directory, state, store).complete_run(timestamp=timestamp)
        return VerificationResult.from_dict(result.to_dict())


__all__ = ["VerificationCorruptionError", "VerificationError", "Verifier"]
