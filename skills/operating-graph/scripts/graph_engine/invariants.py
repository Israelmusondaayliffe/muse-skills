"""Deterministic validation for the 22 Operating Graph invariants."""

from __future__ import annotations

import ast
from collections import defaultdict, deque
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
from typing import Any, Dict, Iterable, Mapping, Optional, Set, Tuple

from .constants import EdgeKind, ExecutionMode, NodeKind, Temporal
from .models import Artifact, Edge, Graph, RewriteProposal, RuntimeState


_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_INTERNAL_CAPABILITIES = frozenset(
    {
        "analysis",
        "artifact-read",
        "artifact-write",
        "evaluation",
        "file-read",
        "research",
        "state-read",
    }
)
_FREE_FORM_CONDITION_KEYS = frozenset({"code", "condition", "expression", "script"})
_SHELL_OPERATORS = frozenset({"&", "&&", "<", ">", "|", "||"})
_ALLOWED_STOP_LABELS = frozenset(
    {
        "approved",
        "complete",
        "completed",
        "done",
        "passed",
        "ready",
        "succeeded",
        "success",
        "verified",
    }
)
_PROSE_CHARACTERS = re.compile(r"^[A-Z][A-Za-z0-9\s`'(),.;:?!_-]*$")
_PROSE_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
_PROSE_GRAMMAR_MARKERS = frozenset(
    {
        "a",
        "all",
        "an",
        "and",
        "are",
        "as",
        "at",
        "exists",
        "for",
        "from",
        "has",
        "have",
        "in",
        "is",
        "of",
        "on",
        "or",
        "sure",
        "the",
        "to",
        "when",
        "with",
    }
)


@dataclass(frozen=True)
class InvariantViolation:
    """One invariant failure with a stable code and sort key."""

    invariant: int
    message: str
    location: str = ""

    @property
    def code(self) -> str:
        return f"OGI-{self.invariant:02d}"

    def __str__(self) -> str:
        location = f" at {self.location}" if self.location else ""
        return f"{self.code}{location}: {self.message}"


def _violation(invariant: int, message: str, location: str = "") -> InvariantViolation:
    return InvariantViolation(invariant=invariant, message=message, location=location)


def _ordered(violations: Iterable[InvariantViolation]) -> Tuple[InvariantViolation, ...]:
    unique = {(item.invariant, item.location, item.message): item for item in violations}
    return tuple(unique[key] for key in sorted(unique))


def _enabled_nodes(graph: Graph) -> Dict[str, Any]:
    return {node.id: node for node in graph.nodes if node.enabled}


def _enabled_edges(graph: Graph) -> Tuple[Edge, ...]:
    enabled = _enabled_nodes(graph)
    return tuple(
        edge for edge in graph.edges
        if edge.enabled and edge.source in enabled and edge.target in enabled
    )


def _adjacency(edges: Iterable[Edge]) -> Dict[str, Set[str]]:
    result: Dict[str, Set[str]] = defaultdict(set)
    for edge in edges:
        result[edge.source].add(edge.target)
    return result


def _reachable(start: str, edges: Iterable[Edge]) -> Set[str]:
    adjacency = _adjacency(edges)
    seen: Set[str] = {start}
    pending = deque([start])
    while pending:
        source = pending.popleft()
        for target in sorted(adjacency.get(source, ())):
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen


def _cyclic_components(node_ids: Iterable[str], edges: Iterable[Edge]) -> Tuple[Tuple[str, ...], ...]:
    """Return deterministic strongly connected components that contain a cycle."""
    adjacency = _adjacency(edges)
    index = 0
    indexes: Dict[str, int] = {}
    lowlinks: Dict[str, int] = {}
    stack: list[str] = []
    on_stack: Set[str] = set()
    components: list[Tuple[str, ...]] = []

    def visit(node_id: str) -> None:
        nonlocal index
        indexes[node_id] = index
        lowlinks[node_id] = index
        index += 1
        stack.append(node_id)
        on_stack.add(node_id)
        for target in sorted(adjacency.get(node_id, ())):
            if target not in indexes:
                visit(target)
                lowlinks[node_id] = min(lowlinks[node_id], lowlinks[target])
            elif target in on_stack:
                lowlinks[node_id] = min(lowlinks[node_id], indexes[target])
        if lowlinks[node_id] != indexes[node_id]:
            return
        component: list[str] = []
        while stack:
            member = stack.pop()
            on_stack.remove(member)
            component.append(member)
            if member == node_id:
                break
        ordered = tuple(sorted(component))
        if len(ordered) > 1 or (ordered and ordered[0] in adjacency.get(ordered[0], set())):
            components.append(ordered)

    for node_id in sorted(set(node_ids)):
        if node_id not in indexes:
            visit(node_id)
    return tuple(sorted(components))


def _producers(graph: Graph, artifact_type: str) -> Tuple[Any, ...]:
    return tuple(
        node for node in graph.nodes
        if node.enabled
        and any(output.required and output.artifact_type == artifact_type for output in node.outputs)
    )


def _has_evaluator_path(graph: Graph, producer_id: str, artifact_type: str) -> bool:
    enabled_nodes = _enabled_nodes(graph)
    enabled_edges = _enabled_edges(graph)
    producing_flow_edges = tuple(
        edge for edge in enabled_edges if edge.kind not in (EdgeKind.VERIFY, EdgeKind.APPROVE)
    )
    producing_flow = _reachable(producer_id, producing_flow_edges)
    return any(
        edge.kind == EdgeKind.VERIFY
        and edge.source in producing_flow
        and edge.target != producer_id
        and edge.target in enabled_nodes
        and enabled_nodes[edge.target].kind == NodeKind.EVALUATOR
        and bool(edge.artifact_types)
        and artifact_type in edge.artifact_types
        for edge in enabled_edges
    )


def _permission_boundary(graph: Graph) -> Tuple[Tuple[str, Tuple[str, ...]], ...]:
    return tuple(
        sorted((node.id, tuple(sorted(node.capabilities))) for node in graph.nodes)
    )


def _permissions_within_boundary(graph: Graph, original_graph: Graph) -> bool:
    """Preserve existing grants and prevent new nodes from expanding their union."""
    original = {node.id: tuple(sorted(node.capabilities)) for node in original_graph.nodes}
    allowed = {capability for node in original_graph.nodes for capability in node.capabilities}
    for node in graph.nodes:
        capabilities = tuple(sorted(node.capabilities))
        if node.id in original and capabilities != original[node.id]:
            return False
        if node.id not in original and not set(capabilities) <= allowed:
            return False
    return True


def _required_approval_boundary(graph: Graph) -> Tuple[Tuple[Any, ...], ...]:
    approvals = []
    for edge in graph.edges:
        activation_approvals = tuple(sorted(edge.activation.approvals if edge.activation else ()))
        if edge.required and (edge.kind == EdgeKind.APPROVE or activation_approvals):
            approvals.append((edge.id, edge.source, edge.target, edge.kind.value, activation_approvals))
    return tuple(sorted(approvals))


def _authority_definition(graph: Graph) -> Tuple[Dict[str, Any], ...]:
    return tuple(node.to_dict() for node in graph.nodes if node.kind == NodeKind.AUTHORITY)


def _is_external_node(graph: Graph, node: Any) -> bool:
    if node.execution.mode == ExecutionMode.TOOL:
        return True
    if any(capability not in _INTERNAL_CAPABILITIES for capability in node.capabilities):
        return True
    return any(
        edge.enabled
        and node.id in (edge.source, edge.target)
        and edge.kind == EdgeKind.PUBLISH
        for edge in graph.edges
    )


def _edge_subjects(edge: Edge) -> Set[str]:
    subjects = set(edge.artifact_types)
    if edge.activation:
        subjects.update(edge.activation.artifacts)
        subjects.update(edge.activation.approvals)
    return subjects


def _is_excluded_feedback(edge: Edge, nodes: Mapping[str, Any]) -> bool:
    if edge.temporal != Temporal.NEXT_EPOCH:
        return False
    source = nodes.get(edge.source)
    return (
        edge.kind in (EdgeKind.LEARN, EdgeKind.MEASURE)
        or (source is not None and source.kind == NodeKind.SIGNAL)
    )


def _target_originates_subject(
    verification_edge: Edge,
    edges: Iterable[Edge],
    nodes: Mapping[str, Any],
) -> bool:
    if verification_edge.source == verification_edge.target:
        return True
    subjects = _edge_subjects(verification_edge)
    if not subjects:
        return False
    ancestry_edges = tuple(
        edge
        for edge in edges
        if edge.id != verification_edge.id
        and edge.kind not in (EdgeKind.VERIFY, EdgeKind.APPROVE)
        and not _is_excluded_feedback(edge, nodes)
        and bool(_edge_subjects(edge) & subjects)
    )
    return verification_edge.source in _reachable(
        verification_edge.target,
        ancestry_edges,
    )


def _stop_condition_is_executable(condition: str) -> bool:
    condition = condition.strip()
    if condition in _ALLOWED_STOP_LABELS:
        return False
    if _has_shell_operator_syntax(condition):
        return True
    try:
        tree = ast.parse(condition, mode="exec")
    except SyntaxError:
        tree = None
    if tree is not None and tree.body:
        plain_label = (
            len(tree.body) == 1
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, (ast.Constant, ast.Name))
        )
        if not plain_label:
            return True
    return not _is_clear_human_prose(condition)


def _has_shell_operator_syntax(condition: str) -> bool:
    if "$(" in condition or "=>" in condition:
        return True
    try:
        lexer = shlex.shlex(condition, posix=True, punctuation_chars=";&|<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        tokens = list(lexer)
    except ValueError:
        return False
    return any(token in _SHELL_OPERATORS for token in tokens)


def _is_clear_human_prose(condition: str) -> bool:
    if not condition or not _PROSE_CHARACTERS.fullmatch(condition):
        return False
    clauses = [clause.strip() for clause in condition.split(";")]
    for clause in clauses:
        words = _PROSE_WORD.findall(clause)
        if len(words) < 2:
            return False
        lowered_words = {word.lower() for word in words}
        has_sentence_punctuation = clause.endswith((".", "?", "!"))
        has_grammar_marker = bool(lowered_words & _PROSE_GRAMMAR_MARKERS)
        if not has_grammar_marker and not (
            len(words) >= 4 and has_sentence_punctuation
        ):
            return False
    return True


def validate_raw_condition_fields(value: Any) -> Tuple[InvariantViolation, ...]:
    """Reject arbitrary condition or expression fields before model parsing drops them."""
    violations: list[InvariantViolation] = []

    def visit(item: Any, location: str) -> None:
        if isinstance(item, dict):
            for key, child in item.items():
                child_location = f"{location}.{key}" if location else str(key)
                normalized_key = key.lower() if isinstance(key, str) else ""
                is_free_form_condition = (
                    normalized_key in _FREE_FORM_CONDITION_KEYS
                    or normalized_key in {"if", "predicate", "when"}
                    or (
                        normalized_key.endswith("condition")
                        and normalized_key != "stopcondition"
                    )
                )
                if is_free_form_condition:
                    violations.append(
                        _violation(
                            19,
                            "free-form condition fields are not allowed; use structured activation fields",
                            child_location,
                        )
                    )
                visit(child, child_location)
        elif isinstance(item, list):
            for index, child in enumerate(item):
                visit(child, f"{location}[{index}]")

    visit(value, "graph")
    return _ordered(violations)


def _validate_graph_invariants(
    graph: Graph,
    *,
    original_graph: Optional[Graph] = None,
) -> Tuple[InvariantViolation, ...]:
    """Return all structurally decidable invariant failures in stable order."""
    violations: list[InvariantViolation] = []

    node_ids = [node.id for node in graph.nodes]
    edge_ids = [edge.id for edge in graph.edges]
    for label, identifiers in (("node", node_ids), ("edge", edge_ids)):
        for identifier in sorted(set(identifiers)):
            if identifiers.count(identifier) > 1:
                violations.append(_violation(1, f"{label} ID {identifier!r} is not unique", f"{label}s.{identifier}"))

    identifiers = [("graphId", graph.graph_id)]
    identifiers.extend((f"nodes.{node.id}.id", node.id) for node in graph.nodes)
    identifiers.extend((f"edges.{edge.id}.id", edge.id) for edge in graph.edges)
    identifiers.extend((f"goal.deliverables.{item.id}.id", item.id) for item in graph.goal.deliverables)
    for location, identifier in identifiers:
        if not _ID_PATTERN.fullmatch(identifier):
            violations.append(_violation(2, f"ID {identifier!r} must use lowercase letters, digits, and hyphens", location))

    node_id_set = set(node_ids)
    for edge in graph.edges:
        if edge.source not in node_id_set:
            violations.append(_violation(3, f"edge source {edge.source!r} does not exist", f"edges.{edge.id}.source"))
        if edge.target not in node_id_set:
            violations.append(_violation(3, f"edge target {edge.target!r} does not exist", f"edges.{edge.id}.target"))
        if edge.activation:
            for requirement in edge.activation.node_states:
                if requirement.node_id not in node_id_set:
                    violations.append(_violation(3, f"activation node {requirement.node_id!r} does not exist", f"edges.{edge.id}.activation.nodeStates"))

    authorities = [node for node in graph.nodes if node.enabled and node.kind == NodeKind.AUTHORITY]
    controllers = [node for node in graph.nodes if node.enabled and node.kind == NodeKind.CONTROLLER]
    if len(authorities) != 1:
        violations.append(_violation(4, f"expected exactly one enabled authority node, found {len(authorities)}", "nodes"))
    if len(controllers) != 1:
        violations.append(_violation(5, f"expected exactly one enabled controller node, found {len(controllers)}", "nodes"))
    if len(authorities) != 1 or graph.goal.authority_node_id != authorities[0].id:
        violations.append(_violation(6, "goal authorityNodeId must identify the enabled authority node", "goal.authorityNodeId"))

    if original_graph is not None:
        immutable_checks = (
            (graph.goal.to_dict() == original_graph.goal.to_dict(), "goal boundary changed", "goal"),
            (_authority_definition(graph) == _authority_definition(original_graph), "authority definition changed", "nodes"),
            (_permissions_within_boundary(graph, original_graph), "permission boundary changed", "nodes.capabilities"),
            (graph.limits.to_dict() == original_graph.limits.to_dict(), "hard limits changed", "limits"),
            (
                graph.rewrite_policy is not None
                and original_graph.rewrite_policy is not None
                and graph.rewrite_policy.to_dict() == original_graph.rewrite_policy.to_dict(),
                "rewrite policy boundary changed",
                "rewritePolicy",
            ),
            (_required_approval_boundary(graph) == _required_approval_boundary(original_graph), "required approval boundary changed", "edges"),
        )
        for valid, message, location in immutable_checks:
            if not valid:
                violations.append(_violation(7, message, location))

    enabled_nodes = _enabled_nodes(graph)
    enabled_edges = _enabled_edges(graph)
    if len(authorities) == 1:
        reachable = _reachable(authorities[0].id, enabled_edges)
        for node_id in sorted(set(enabled_nodes) - reachable):
            violations.append(_violation(8, f"enabled node {node_id!r} is not reachable from authority", f"nodes.{node_id}"))

    for deliverable in graph.goal.deliverables:
        producers = _producers(graph, deliverable.artifact_type)
        if not producers:
            violations.append(_violation(9, f"deliverable artifact type {deliverable.artifact_type!r} has no enabled producer", f"goal.deliverables.{deliverable.id}"))
        if not any(_has_evaluator_path(graph, producer.id, deliverable.artifact_type) for producer in producers):
            violations.append(_violation(10, f"deliverable {deliverable.id!r} has no independent evaluator path", f"goal.deliverables.{deliverable.id}"))

    for edge in enabled_edges:
        if (
            edge.kind in (EdgeKind.VERIFY, EdgeKind.APPROVE)
            and _target_originates_subject(edge, enabled_edges, enabled_nodes)
        ):
            violations.append(
                _violation(
                    11,
                    f"node {edge.target!r} evaluates or approves a subject from its own producing flow",
                    f"edges.{edge.id}",
                )
            )

    enabled_authority_ids = {node.id for node in authorities}
    for node in graph.nodes:
        if not node.enabled or not _is_external_node(graph, node):
            continue
        approved = any(
            edge.enabled
            and edge.required
            and edge.kind == EdgeKind.APPROVE
            and edge.source in enabled_authority_ids
            and edge.target == node.id
            for edge in graph.edges
        )
        if not approved:
            violations.append(_violation(12, f"external side-effect node {node.id!r} lacks a required authority approval predecessor", f"nodes.{node.id}"))

    same_epoch_edges = tuple(edge for edge in enabled_edges if edge.temporal == Temporal.SAME_EPOCH)
    same_epoch_cycles = _cyclic_components(enabled_nodes, same_epoch_edges)
    for component in same_epoch_cycles:
        description = ", ".join(component)
        violations.append(_violation(13, f"enabled same-epoch dependencies contain a cycle: {description}", "edges"))
        violations.append(_violation(14, f"enabled cycle lacks a next_epoch edge: {description}", "edges"))

    if any(edge.temporal == Temporal.NEXT_EPOCH for edge in enabled_edges) and graph.limits.max_epochs <= 0:
        violations.append(_violation(15, "graphs using next_epoch edges require a finite positive maxEpochs", "limits.maxEpochs"))

    limits = (
        ("maxConcurrentWorkers", graph.limits.max_concurrent_workers),
        ("maxNodeRuns", graph.limits.max_node_runs),
        ("maxGraphVersions", graph.limits.max_graph_versions),
        ("maxEpochs", graph.limits.max_epochs),
        ("maxAutoRewrites", graph.limits.max_auto_rewrites),
        ("defaultMaxAttempts", graph.limits.default_max_attempts),
    )
    for name, value in limits:
        if value <= 0:
            violations.append(_violation(16, f"runtime limit {name} must be a positive integer", f"limits.{name}"))
    for node in graph.nodes:
        node_limits = (
            ("budget.maxAttempts", node.budget.max_attempts if node.budget else None),
            ("budget.workUnits", node.budget.work_units if node.budget else None),
            ("localLoop.maxIterations", node.local_loop.max_iterations if node.local_loop else None),
        )
        for name, value in node_limits:
            if value is not None and value <= 0:
                violations.append(_violation(16, f"runtime limit {name} must be a positive integer", f"nodes.{node.id}.{name}"))

    required_artifact_types: Set[str] = set()
    for node in graph.nodes:
        if node.enabled:
            required_artifact_types.update(item.artifact_type for item in node.inputs if item.required)
    for edge in enabled_edges:
        if edge.required:
            required_artifact_types.update(edge.artifact_types)
            if edge.activation:
                required_artifact_types.update(edge.activation.artifacts)
    for artifact_type in sorted(required_artifact_types):
        if not _producers(graph, artifact_type):
            violations.append(_violation(17, f"required artifact type {artifact_type!r} has no enabled producer", f"artifacts.{artifact_type}"))
    for edge in enabled_edges:
        if not edge.required:
            continue
        source = enabled_nodes[edge.source]
        source_outputs = {
            output.artifact_type for output in source.outputs if output.required
        }
        edge_requirements = set(edge.artifact_types)
        if edge.activation:
            edge_requirements.update(edge.activation.artifacts)
        for artifact_type in sorted(edge_requirements - source_outputs):
            violations.append(
                _violation(
                    17,
                    f"required edge artifact type {artifact_type!r} is not a required output of source {source.id!r}",
                    f"edges.{edge.id}.artifactTypes",
                )
            )

    nodes_by_id = {node.id: node for node in graph.nodes}
    for edge in graph.edges:
        if not edge.enabled:
            continue
        source = nodes_by_id.get(edge.source)
        if source is not None and not source.enabled:
            violations.append(_violation(18, f"disabled node {source.id!r} cannot satisfy an enabled dependency", f"edges.{edge.id}.source"))
        if edge.activation:
            for requirement in edge.activation.node_states:
                dependency = nodes_by_id.get(requirement.node_id)
                if dependency is not None and not dependency.enabled:
                    violations.append(_violation(18, f"disabled node {dependency.id!r} cannot satisfy activation", f"edges.{edge.id}.activation.nodeStates"))

    for node in graph.nodes:
        if node.local_loop and _stop_condition_is_executable(node.local_loop.stop_condition):
            violations.append(
                _violation(
                    19,
                    "local loop stop condition contains executable expression syntax",
                    f"nodes.{node.id}.localLoop.stopCondition",
                )
            )

    return _ordered(violations)


def validate_graph_invariants(graph: Graph) -> Tuple[InvariantViolation, ...]:
    """Return all graph-only invariant failures for an initial graph."""
    return _validate_graph_invariants(graph)


def validate_rewritten_graph_invariants(
    graph: Graph,
    *,
    original_graph: Graph,
) -> Tuple[InvariantViolation, ...]:
    """Return graph failures with mandatory original authority-boundary checks."""
    return _validate_graph_invariants(graph, original_graph=original_graph)


def validate_runtime_dependencies(
    graph: Graph,
    state: RuntimeState,
    *,
    satisfactions: Iterable[Tuple[str, str]],
) -> Tuple[InvariantViolation, ...]:
    """Validate runtime evidence needed for invariant 18."""
    disabled_ids = {node.id for node in graph.nodes if not node.enabled}
    violations = []
    for consumer_id, provider_id in satisfactions:
        if provider_id in disabled_ids:
            violations.append(
                _violation(
                    18,
                    f"consumer {consumer_id!r} used disabled dependency provider {provider_id!r}",
                    f"state.nodeStates.{consumer_id}.dependencies",
                )
            )
    return _ordered(violations)


def validate_runtime_limits(
    graph: Graph,
    state: RuntimeState,
    *,
    current_concurrency: int,
    graph_version_count: int,
) -> Tuple[InvariantViolation, ...]:
    """Validate runtime counters that graph structure alone cannot prove."""
    violations = []
    if state.epoch > graph.limits.max_epochs:
        violations.append(_violation(15, f"runtime epoch {state.epoch} exceeds maxEpochs {graph.limits.max_epochs}", "state.epoch"))
    if state.total_node_runs > graph.limits.max_node_runs:
        violations.append(_violation(16, f"runtime node runs {state.total_node_runs} exceed maxNodeRuns {graph.limits.max_node_runs}", "state.totalNodeRuns"))
    if state.auto_rewrites_applied > graph.limits.max_auto_rewrites:
        violations.append(_violation(16, f"automatic rewrites {state.auto_rewrites_applied} exceed maxAutoRewrites {graph.limits.max_auto_rewrites}", "state.autoRewritesApplied"))
    if current_concurrency > graph.limits.max_concurrent_workers:
        violations.append(_violation(16, f"current concurrency {current_concurrency} exceeds maxConcurrentWorkers {graph.limits.max_concurrent_workers}", "runtime.currentConcurrency"))
    if graph_version_count > graph.limits.max_graph_versions:
        violations.append(_violation(16, f"graph version count {graph_version_count} exceeds maxGraphVersions {graph.limits.max_graph_versions}", "runtime.graphVersionCount"))
    nodes_by_id = {node.id: node for node in graph.nodes}
    for node_id, runtime in state.node_states.items():
        node = nodes_by_id.get(node_id)
        max_attempts = node.budget.max_attempts if node and node.budget else graph.limits.default_max_attempts
        if runtime.attempts > max_attempts:
            violations.append(_violation(16, f"node attempts {runtime.attempts} exceed maxAttempts {max_attempts}", f"state.nodeStates.{node_id}.attempts"))
    return _ordered(violations)


def validate_artifact_path(artifact: Artifact, run_directory: Path) -> Tuple[InvariantViolation, ...]:
    """Validate path containment for invariant 20 without touching the artifact."""
    relative = PurePosixPath(artifact.path)
    violations = []
    malformed = not artifact.path or any(ord(character) < 32 or ord(character) == 127 for character in artifact.path)
    if malformed:
        violations.append(_violation(20, f"artifact path {artifact.path!r} is malformed", f"artifacts.{artifact.artifact_id}.path"))
    if relative.is_absolute() or ".." in relative.parts:
        violations.append(_violation(20, f"artifact path {artifact.path!r} escapes the run directory", f"artifacts.{artifact.artifact_id}.path"))
    elif not malformed:
        root = run_directory.resolve()
        try:
            resolved = (root / Path(*relative.parts)).resolve()
            resolved.relative_to(root)
        except (OSError, RuntimeError, ValueError):
            violations.append(_violation(20, f"artifact path {artifact.path!r} escapes the run directory", f"artifacts.{artifact.artifact_id}.path"))
    expected_prefix = ("artifacts", artifact.node_id)
    if len(relative.parts) < 3 or relative.parts[:2] != expected_prefix:
        violations.append(_violation(20, f"artifact path {artifact.path!r} is outside its producer directory", f"artifacts.{artifact.artifact_id}.path"))
    return _ordered(violations)


def validate_applied_rewrite(
    proposal: RewriteProposal,
    *,
    available_versions: Iterable[int],
) -> Tuple[InvariantViolation, ...]:
    """Validate the trusted version context for an applied rewrite."""
    available = set(available_versions)
    violations = []
    if proposal.base_graph_version not in available:
        violations.append(_violation(21, f"base graph version {proposal.base_graph_version} does not exist", "rewrite.baseGraphVersion"))
    if proposal.rollback_version not in available:
        violations.append(_violation(21, f"rollback graph version {proposal.rollback_version} does not exist", "rewrite.rollbackVersion"))
    return _ordered(violations)


def _version_digest(value: Any) -> str:
    payload = value.to_dict() if isinstance(value, Graph) else value
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def validate_graph_versions(
    versions: Mapping[int, Any],
    *,
    immutable_hashes: Optional[Mapping[int, str]] = None,
) -> Tuple[InvariantViolation, ...]:
    """Validate sequential numbering and trusted immutable digests."""
    violations = []
    actual = sorted(versions)
    expected = list(range(1, actual[-1] + 1)) if actual else [1]
    if actual != expected:
        violations.append(_violation(22, f"graph versions must be sequential from 1; found {actual}", "graph-versions"))
    trusted = immutable_hashes or {}
    for version in actual:
        if version not in trusted:
            violations.append(_violation(22, f"graph version {version} has no trusted immutable digest", f"graph-versions.v{version:04d}"))
        elif _version_digest(versions[version]) != trusted[version]:
            violations.append(_violation(22, f"graph version {version} differs from its immutable digest", f"graph-versions.v{version:04d}"))
    return _ordered(violations)


__all__ = [
    "InvariantViolation",
    "validate_applied_rewrite",
    "validate_artifact_path",
    "validate_graph_invariants",
    "validate_graph_versions",
    "validate_raw_condition_fields",
    "validate_rewritten_graph_invariants",
    "validate_runtime_dependencies",
    "validate_runtime_limits",
]
