"""Structural parsing and invariant validation entry points."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import re
from typing import Any, Dict, Optional, Tuple, Union

from .constants import (
    ActivationMode,
    EdgeKind,
    ExecutionMode,
    NodeKind,
    NodeStatus,
    RiskLevel,
    SCHEMA_VERSION,
    Temporal,
)
from .invariants import (
    InvariantViolation,
    validate_graph_invariants,
    validate_raw_condition_fields,
    validate_rewritten_graph_invariants,
)
from .models import Graph


@dataclass(frozen=True)
class StructuralViolation:
    code: str
    message: str
    location: str = "graph"

    def __str__(self) -> str:
        return f"{self.code} at {self.location}: {self.message}"


Violation = Union[StructuralViolation, InvariantViolation]


@dataclass(frozen=True)
class ValidationResult:
    graph: Optional[Graph]
    violations: Tuple[Violation, ...]

    @property
    def valid(self) -> bool:
        return not self.violations


class GraphValidationError(ValueError):
    def __init__(self, violations: Tuple[Violation, ...]) -> None:
        self.violations = violations
        super().__init__("\n".join(str(item) for item in violations))


def _object_schema(model: str, fields: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
    return ("object", model, fields)


def _array_schema(item: Any) -> Tuple[str, Any]:
    return ("array", item)


def _nullable_schema(item: Any) -> Tuple[str, Any]:
    return ("nullable", item)


def _enum_schema(enum_type: Any) -> Tuple[str, Any]:
    return ("enum", enum_type)


_TIMESTAMP_SCHEMA = ("timestamp",)
_UTC_TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")


_ARTIFACT_REQUIREMENT_SCHEMA = _object_schema(
    "ArtifactRequirement",
    {"artifactType": str, "required": bool},
)
_DELIVERABLE_SCHEMA = _object_schema(
    "Deliverable",
    {"id": str, "artifactType": str, "description": str},
)
_GOAL_SCHEMA = _object_schema(
    "Goal",
    {
        "statement": str,
        "deliverables": _array_schema(_DELIVERABLE_SCHEMA),
        "completionCriteria": _array_schema(str),
        "authorityNodeId": str,
    },
)
_EXECUTION_SCHEMA = _object_schema(
    "Execution",
    {
        "mode": _enum_schema(ExecutionMode),
        "skill": _nullable_schema(str),
        "modelHint": _nullable_schema(str),
    },
)
_BUDGET_SCHEMA = _object_schema(
    "Budget",
    {"maxAttempts": int, "workUnits": int},
)
_LOCAL_LOOP_SCHEMA = _object_schema(
    "LocalLoop",
    {
        "enabled": bool,
        "maxIterations": int,
        "sequence": _array_schema(str),
        "stopCondition": str,
    },
)
_NODE_SCHEMA = _object_schema(
    "Node",
    {
        "id": str,
        "kind": _enum_schema(NodeKind),
        "label": str,
        "purpose": str,
        "enabled": bool,
        "critical": bool,
        "priority": int,
        "execution": _EXECUTION_SCHEMA,
        "capabilities": _array_schema(str),
        "inputs": _array_schema(_ARTIFACT_REQUIREMENT_SCHEMA),
        "outputs": _array_schema(_ARTIFACT_REQUIREMENT_SCHEMA),
        "successCriteria": _array_schema(str),
        "budget": _BUDGET_SCHEMA,
        "localLoop": _LOCAL_LOOP_SCHEMA,
    },
)
_NODE_STATE_REQUIREMENT_SCHEMA = _object_schema(
    "NodeStateRequirement",
    {"nodeId": str, "status": _enum_schema(NodeStatus)},
)
_ACTIVATION_SCHEMA = _object_schema(
    "Activation",
    {
        "mode": _enum_schema(ActivationMode),
        "nodeStates": _array_schema(_NODE_STATE_REQUIREMENT_SCHEMA),
        "artifacts": _array_schema(str),
        "approvals": _array_schema(str),
    },
)
_EDGE_SCHEMA = _object_schema(
    "Edge",
    {
        "id": str,
        "source": str,
        "target": str,
        "kind": _enum_schema(EdgeKind),
        "enabled": bool,
        "required": bool,
        "temporal": _enum_schema(Temporal),
        "artifactTypes": _array_schema(str),
        "activation": _ACTIVATION_SCHEMA,
    },
)
_LIMITS_SCHEMA = _object_schema(
    "Limits",
    {
        "maxConcurrentWorkers": int,
        "maxNodeRuns": int,
        "maxGraphVersions": int,
        "maxEpochs": int,
        "maxAutoRewrites": int,
        "defaultMaxAttempts": int,
    },
)
_REWRITE_POLICY_SCHEMA = _object_schema(
    "RewritePolicy",
    {
        "automaticRiskLevels": _array_schema(_enum_schema(RiskLevel)),
        "approvalRiskLevels": _array_schema(_enum_schema(RiskLevel)),
        "prohibitedMutations": _array_schema(str),
    },
)
_METADATA_SCHEMA = _object_schema(
    "Graph.metadata",
    {"createdBy": str, "createdAt": _TIMESTAMP_SCHEMA},
)
_GRAPH_SCHEMA = _object_schema(
    "Graph",
    {
        "schemaVersion": str,
        "graphId": str,
        "name": str,
        "goal": _GOAL_SCHEMA,
        "limits": _LIMITS_SCHEMA,
        "nodes": _array_schema(_NODE_SCHEMA),
        "edges": _array_schema(_EDGE_SCHEMA),
        "rewritePolicy": _REWRITE_POLICY_SCHEMA,
        "metadata": _METADATA_SCHEMA,
    },
)


def _expected_name(expected: Any) -> str:
    return {str: "string", bool: "boolean", int: "integer"}.get(expected, "value")


def _matches_primitive(value: Any, expected: Any) -> bool:
    if expected is int:
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, expected)


def _collect_schema_violations(
    value: Any,
    schema: Any,
    *,
    display: str,
    location: str,
    violations: list[StructuralViolation],
) -> None:
    if isinstance(schema, tuple) and schema[0] == "nullable":
        if value is not None:
            _collect_schema_violations(
                value,
                schema[1],
                display=display,
                location=location,
                violations=violations,
            )
        return
    if isinstance(schema, tuple) and schema[0] == "enum":
        enum_type = schema[1]
        if not isinstance(value, str):
            violations.append(
                StructuralViolation("STRUCTURE", f"{display}: expected string", location)
            )
        else:
            try:
                enum_type(value)
            except ValueError:
                violations.append(
                    StructuralViolation(
                        "STRUCTURE",
                        f"{display}: invalid {enum_type.__name__} value {value!r}",
                        location,
                    )
                )
        return
    if isinstance(schema, tuple) and schema[0] == "timestamp":
        valid = isinstance(value, str) and bool(_UTC_TIMESTAMP.fullmatch(value))
        if valid:
            try:
                datetime.fromisoformat(f"{value[:-1]}+00:00")
            except ValueError:
                valid = False
        if not valid:
            violations.append(
                StructuralViolation(
                    "STRUCTURE",
                    f"{display}: expected canonical UTC timestamp",
                    location,
                )
            )
        return
    if isinstance(schema, tuple) and schema[0] == "array":
        if not isinstance(value, list):
            violations.append(
                StructuralViolation("STRUCTURE", f"{display}: expected array", location)
            )
            return
        for index, item in enumerate(value):
            _collect_schema_violations(
                item,
                schema[1],
                display=f"{display}[{index}]",
                location=f"{location}[{index}]",
                violations=violations,
            )
        return
    if isinstance(schema, tuple) and schema[0] == "object":
        _, model, fields = schema
        if not isinstance(value, dict):
            violations.append(
                StructuralViolation("STRUCTURE", f"{display}: expected object", location)
            )
            return
        for key, child_schema in fields.items():
            child_display = f"{model}.{key}"
            child_location = f"{location}.{key}" if location else key
            if key not in value:
                violations.append(
                    StructuralViolation(
                        "STRUCTURE",
                        f"{child_display}: missing required field",
                        child_location,
                    )
                )
                continue
            _collect_schema_violations(
                value[key],
                child_schema,
                display=child_display,
                location=child_location,
                violations=violations,
            )
        return
    if not _matches_primitive(value, schema):
        violations.append(
            StructuralViolation(
                "STRUCTURE",
                f"{display}: expected {_expected_name(schema)}",
                location,
            )
        )


def _ordered_violations(violations: Tuple[Violation, ...]) -> Tuple[Violation, ...]:
    def key(item: Violation) -> Tuple[int, str, str]:
        order = -1 if isinstance(item, StructuralViolation) else item.invariant
        return (order, item.location, item.message)

    unique = {(item.code, item.location, item.message): item for item in violations}
    return tuple(sorted(unique.values(), key=key))


def validate_structure(value: Any) -> Tuple[StructuralViolation, ...]:
    """Collect independently detectable shape failures before strict parsing."""
    violations: list[StructuralViolation] = []
    _collect_schema_violations(
        value,
        _GRAPH_SCHEMA,
        display="Graph",
        location="graph",
        violations=violations,
    )
    if isinstance(value, dict) and isinstance(value.get("schemaVersion"), str):
        schema_version = value["schemaVersion"]
        if schema_version != SCHEMA_VERSION:
            violations.append(
                StructuralViolation(
                    code="STRUCTURE",
                    message=f"Graph.schemaVersion: unsupported schemaVersion {schema_version!r}",
                    location="graph.schemaVersion",
                )
            )
    if not violations:
        try:
            Graph.from_dict(value)
        except ValueError as error:
            violations.append(StructuralViolation(code="STRUCTURE", message=str(error)))
    return tuple(
        sorted(
            {(item.location, item.message): item for item in violations}.values(),
            key=lambda item: (item.location, item.message),
        )
    )


def parse_and_validate_graph(value: Any) -> ValidationResult:
    """Parse a graph and return structural, raw-field, and graph violations."""
    structural = validate_structure(value)
    raw_conditions = validate_raw_condition_fields(value)
    try:
        graph = Graph.from_dict(value)
    except ValueError:
        combined: Tuple[Violation, ...] = (*structural, *raw_conditions)
        return ValidationResult(
            graph=None,
            violations=_ordered_violations(combined),
        )
    combined: Tuple[Violation, ...] = (
        *structural,
        *raw_conditions,
        *validate_graph_invariants(graph),
    )
    return ValidationResult(graph=graph, violations=_ordered_violations(combined))


def parse_and_validate_rewritten_graph(
    value: Any,
    *,
    original_graph: Graph,
) -> ValidationResult:
    """Validate a rewritten graph with mandatory original-boundary context."""
    result = parse_and_validate_graph(value)
    if result.graph is None:
        return result
    combined: Tuple[Violation, ...] = (
        *result.violations,
        *validate_rewritten_graph_invariants(result.graph, original_graph=original_graph),
    )
    return ValidationResult(result.graph, _ordered_violations(combined))


def validate_graph(graph: Graph) -> Tuple[InvariantViolation, ...]:
    """Validate an initial, already parsed graph."""
    return validate_graph_invariants(graph)


def validate_rewritten_graph(
    graph: Graph,
    *,
    original_graph: Graph,
) -> Tuple[InvariantViolation, ...]:
    """Validate a rewritten graph with mandatory original-boundary context."""
    return validate_rewritten_graph_invariants(graph, original_graph=original_graph)


def require_valid_graph(value: Any) -> Graph:
    """Return a valid initial graph or raise one error containing all violations."""
    result = parse_and_validate_graph(value)
    if result.violations:
        raise GraphValidationError(result.violations)
    assert result.graph is not None
    return result.graph


__all__ = [
    "GraphValidationError",
    "StructuralViolation",
    "ValidationResult",
    "parse_and_validate_graph",
    "parse_and_validate_rewritten_graph",
    "require_valid_graph",
    "validate_graph",
    "validate_rewritten_graph",
    "validate_structure",
]
