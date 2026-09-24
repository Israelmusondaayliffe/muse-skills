#!/usr/bin/env python3
"""Validate Session Compounder provenance, selection, and permission invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path


SOURCE_SECTIONS = ("decisions", "follow_ups", "durable_knowledge")
PERMISSIONS = {"allowed", "restricted", "unknown", "prohibited"}
PERMISSION_CHECKS = {"allowed", "blocked", "unresolved"}
EXTERNAL_ACTIONS = {"none", "publish", "message", "share", "upload", "connected-write"}


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("artifact must be a JSON object")
    return value


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_fields(errors: list[str], value: object, prefix: str, fields: tuple[str, ...]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return
    for field in fields:
        if field not in value or value[field] in (None, "", []):
            errors.append(f"{prefix}.{field} is required")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_output.py ARTIFACT.json", file=sys.stderr)
        return 2
    try:
        data = load(Path(sys.argv[1]))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2

    errors: list[str] = []
    source_record = data.get("source_record")
    require_fields(
        errors,
        source_record,
        "source_record",
        ("session", "date", "purpose", "source_locations", "source_completeness", "recorded_audience", "privacy_or_attribution_limits"),
    )
    source_locations: set[str] = set()
    if isinstance(source_record, dict):
        locations = source_record.get("source_locations")
        if isinstance(locations, list) and all(nonempty(item) for item in locations):
            source_locations = set(locations)
        else:
            errors.append("source_record.source_locations must be a non-empty string list")
        if source_record.get("source_completeness") not in {"complete", "partial", "unknown"}:
            errors.append("source_record.source_completeness must be complete, partial, or unknown")
        audiences = source_record.get("recorded_audience")
        if not isinstance(audiences, list) or not audiences or not all(nonempty(item) for item in audiences):
            errors.append("source_record.recorded_audience must be a non-empty string list")

    source_items: dict[str, dict] = {}
    unknown_permission_ids: set[str] = set()
    for section in SOURCE_SECTIONS:
        items = data.get(section)
        if not isinstance(items, list):
            errors.append(f"{section} must be a list")
            continue
        for index, item in enumerate(items):
            prefix = f"{section}[{index}]"
            required = ("id", "evidence", "source_location", "reuse_permission", "attribution_rule", "deidentification_required")
            require_fields(errors, item, prefix, required)
            if not isinstance(item, dict):
                continue
            item_id = item.get("id")
            if not nonempty(item_id) or item_id in source_items:
                errors.append(f"{prefix}.id must be non-empty and unique")
                continue
            source_items[item_id] = item
            if item.get("source_location") not in source_locations:
                errors.append(f"{prefix}.source_location must name a source_record location")
            permission = item.get("reuse_permission")
            if permission not in PERMISSIONS:
                errors.append(f"{prefix}.reuse_permission must be one of {sorted(PERMISSIONS)}")
            audiences = item.get("allowed_audience")
            if not isinstance(audiences, list) or not all(nonempty(audience) for audience in audiences):
                errors.append(f"{prefix}.allowed_audience must be a string list")
                audiences = []
            if permission in {"allowed", "restricted"} and not audiences:
                errors.append(f"{prefix}.allowed_audience is required when reuse is {permission}")
            if permission in {"unknown", "prohibited"}:
                unknown_permission_ids.add(item_id)
                if audiences:
                    errors.append(f"{prefix}.allowed_audience must be empty when reuse is {permission}")
            if not isinstance(item.get("deidentification_required"), bool):
                errors.append(f"{prefix}.deidentification_required must be boolean")
            if section == "follow_ups":
                if item.get("owner_status") not in {"recorded", "unresolved"}:
                    errors.append(f"{prefix}.owner_status must be recorded or unresolved")
                if item.get("owner_status") == "recorded" and not nonempty(item.get("owner")):
                    errors.append(f"{prefix}.owner is required when owner_status is recorded")
                if item.get("owner_status") == "unresolved" and item.get("owner") not in (None, ""):
                    errors.append(f"{prefix}.owner must be empty when owner_status is unresolved")
                if item.get("timing_status") not in {"recorded", "unresolved"}:
                    errors.append(f"{prefix}.timing_status must be recorded or unresolved")
                if item.get("timing_status") == "recorded" and not nonempty(item.get("timing")):
                    errors.append(f"{prefix}.timing is required when timing_status is recorded")
                if item.get("timing_status") == "unresolved" and item.get("timing") not in (None, ""):
                    errors.append(f"{prefix}.timing must be empty when timing_status is unresolved")

    gaps = data.get("unresolved_gaps")
    gap_item_ids: set[str] = set()
    blocked_candidate_ids: set[str] = set()
    if not isinstance(gaps, list):
        errors.append("unresolved_gaps must be a list")
        gaps = []
    for index, gap in enumerate(gaps):
        prefix = f"unresolved_gaps[{index}]"
        require_fields(errors, gap, prefix, ("id", "affected_source_item_ids", "blocked_candidate_output_ids", "resolution_needed"))
        if isinstance(gap, dict):
            gap_item_ids.update(gap.get("affected_source_item_ids", []))
            blocked_candidate_ids.update(gap.get("blocked_candidate_output_ids", []))
    for item_id in sorted(unknown_permission_ids - gap_item_ids):
        errors.append(f"source item {item_id} has unresolved permission without a marked gap")

    recommendations: dict[str, dict] = {}
    recommended_outputs = data.get("recommended_outputs")
    if not isinstance(recommended_outputs, list) or not recommended_outputs:
        errors.append("recommended_outputs must be a non-empty list")
        recommended_outputs = []
    for index, item in enumerate(recommended_outputs):
        prefix = f"recommended_outputs[{index}]"
        require_fields(errors, item, prefix, ("id", "output_type", "value", "evidence_strength", "effort", "sensitivity", "source_item_ids", "intended_audience", "user_selected", "permission_check"))
        if not isinstance(item, dict):
            continue
        item_id = item.get("id")
        if not nonempty(item_id) or item_id in recommendations:
            errors.append(f"{prefix}.id must be non-empty and unique")
            continue
        recommendations[item_id] = item
        evidence_ids = item.get("source_item_ids")
        if not isinstance(evidence_ids, list) or not evidence_ids:
            errors.append(f"{prefix}.source_item_ids must be a non-empty list")
            evidence_ids = []
        missing = set(evidence_ids) - set(source_items)
        if missing:
            errors.append(f"{prefix}.source_item_ids are unknown: {sorted(missing)}")
        if not isinstance(item.get("user_selected"), bool):
            errors.append(f"{prefix}.user_selected must be boolean")
        if item.get("permission_check") not in PERMISSION_CHECKS:
            errors.append(f"{prefix}.permission_check must be one of {sorted(PERMISSION_CHECKS)}")
        blocked_by_source = bool(set(evidence_ids) & unknown_permission_ids)
        if blocked_by_source and item.get("permission_check") == "allowed":
            errors.append(f"{prefix} cannot be allowed while a source permission is unknown or prohibited")
        if blocked_by_source and item_id not in blocked_candidate_ids:
            errors.append(f"{prefix} is permission-blocked but is not named in an unresolved gap")

    derivative_outputs = data.get("derivative_outputs")
    if not isinstance(derivative_outputs, list):
        errors.append("derivative_outputs must be a list")
        derivative_outputs = []
    for index, item in enumerate(derivative_outputs):
        prefix = f"derivative_outputs[{index}]"
        require_fields(errors, item, prefix, ("id", "recommendation_id", "source_item_ids", "intended_audience", "audience_within_recorded_permission", "permission_check", "location", "newly_proposed_material", "attribution_applied", "deidentification_applied", "external_action", "external_action_authorized"))
        if not isinstance(item, dict):
            continue
        recommendation = recommendations.get(item.get("recommendation_id"))
        if recommendation is None:
            errors.append(f"{prefix}.recommendation_id must name a recommended output")
            continue
        if recommendation.get("user_selected") is not True:
            errors.append(f"{prefix} cannot exist until the user selects its recommendation")
        if recommendation.get("permission_check") != "allowed" or item.get("permission_check") != "allowed":
            errors.append(f"{prefix} requires an allowed permission check")
        evidence_ids = item.get("source_item_ids")
        if not isinstance(evidence_ids, list) or not evidence_ids:
            errors.append(f"{prefix}.source_item_ids must be a non-empty list")
            evidence_ids = []
        if set(evidence_ids) != set(recommendation.get("source_item_ids", [])):
            errors.append(f"{prefix}.source_item_ids must match the selected recommendation")
        intended_audience = item.get("intended_audience")
        if item.get("audience_within_recorded_permission") is not True:
            errors.append(f"{prefix}.audience_within_recorded_permission must be true")
        for source_id in evidence_ids:
            source_item = source_items.get(source_id)
            if source_item is None:
                errors.append(f"{prefix}.source_item_ids includes unknown id: {source_id}")
                continue
            if source_item.get("reuse_permission") not in {"allowed", "restricted"}:
                errors.append(f"{prefix} uses source item {source_id} without reusable permission")
            if intended_audience not in source_item.get("allowed_audience", []):
                errors.append(f"{prefix}.intended_audience exceeds permission for {source_id}")
            if source_item.get("deidentification_required") and item.get("deidentification_applied") is not True:
                errors.append(f"{prefix} must apply required de-identification for {source_id}")
        if item.get("external_action") not in EXTERNAL_ACTIONS:
            errors.append(f"{prefix}.external_action must be one of {sorted(EXTERNAL_ACTIONS)}")
        if item.get("external_action") != "none" and item.get("external_action_authorized") is not True:
            errors.append(f"{prefix} cannot perform an external action without explicit authority")
        if not isinstance(item.get("external_action_authorized"), bool):
            errors.append(f"{prefix}.external_action_authorized must be boolean")

    handoffs = data.get("handoffs", {})
    if not isinstance(handoffs, dict):
        errors.append("handoffs must be an object when supplied")
    else:
        for name, handoff in handoffs.items():
            if not isinstance(handoff, dict) or not str(handoff.get("owner", "")).strip():
                errors.append(f"handoffs.{name} must name the selected owner")

    result = {"valid": not errors, "skill": "session-compounder", "errors": errors}
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
