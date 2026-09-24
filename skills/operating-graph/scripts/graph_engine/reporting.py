"""Deterministic text, JSON, and Mermaid reporting."""

from __future__ import annotations

import json
import re

from .models import Graph, RuntimeState, VerificationResult


def render_json(result: VerificationResult) -> str:
    """Render canonical machine-readable verification output."""
    return json.dumps(
        result.to_dict(),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def render_text(result: VerificationResult) -> str:
    """Render a compact human-readable terminal verification report."""
    lines = [f"Verification: {result.status.value}", f"Checked: {result.checked_at}"]
    if result.criteria:
        lines.append("Criteria:")
        for item in result.criteria:
            marker = "pass" if item.get("satisfied") else "fail"
            lines.append(f"- [{marker}] {item.get('criterion', 'unnamed criterion')}")
    if result.evidence_artifact_ids:
        lines.append("Evidence artifacts: " + ", ".join(result.evidence_artifact_ids))
    if result.issues:
        lines.append("Issues:")
        lines.extend(f"- {issue}" for issue in result.issues)
    return "\n".join(lines) + "\n"


def _mermaid_id(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9_]", "_", value)
    if normalized and normalized[0].isdigit():
        normalized = f"n_{normalized}"
    return normalized or "node"


def _label(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', "\\\"")


def render_mermaid(graph: Graph, state: RuntimeState, result: VerificationResult) -> str:
    """Render topology plus runtime statuses as a Mermaid flowchart."""
    lines = ["flowchart TD"]
    ids = {node.id: _mermaid_id(node.id) for node in graph.nodes}
    for node in sorted(graph.nodes, key=lambda item: item.id):
        status = state.node_states.get(node.id)
        status_text = status.status.value if status is not None else "missing"
        lines.append(f'    {ids[node.id]}["{_label(node.label)}\\n{status_text}"]')
    for edge in sorted(graph.edges, key=lambda item: item.id):
        if edge.enabled and edge.source in ids and edge.target in ids:
            lines.append(f"    {ids[edge.source]} --> {ids[edge.target]}")
    statuses = sorted({item.status.value for item in state.node_states.values()})
    palette = {
        "succeeded": "fill:#dcfce7,stroke:#166534",
        "failed": "fill:#fee2e2,stroke:#991b1b",
        "blocked": "fill:#fef3c7,stroke:#92400e",
        "running": "fill:#dbeafe,stroke:#1d4ed8",
    }
    for status in statuses:
        lines.append(f"    classDef {status} {palette.get(status, 'fill:#f3f4f6,stroke:#4b5563')}")
    for node in sorted(graph.nodes, key=lambda item: item.id):
        runtime = state.node_states.get(node.id)
        if runtime is not None:
            lines.append(f"    class {ids[node.id]} {runtime.status.value}")
    lines.append(f"    %% verification: {result.status.value}")
    return "\n".join(lines) + "\n"


__all__ = ["render_json", "render_mermaid", "render_text"]
