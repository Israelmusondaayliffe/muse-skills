#!/usr/bin/env python3
"""Validate a Model Evaluation Lab artifact against its bundled schema.

Usage: validate_output.py <router|plan|run|blocked|memo> ARTIFACT.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

STAGES = {
    "router": "router-schema.json",
    "plan": "plan-schema.json",
    "run": "run-schema.json",
    "blocked": "blocked-schema.json",
    "memo": "memo-schema.json",
}

PLAN_HASH = re.compile(r"^sha256:[0-9a-f]{64}$")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:[a-z0-9]+[_-])*(?:api[_-]?key|token|secret|password|credential)\b"
    r"\s*[:=]\s*\S+"
)
SECRET_TOKEN = re.compile(
    r"\b(?:sk-[A-Za-z0-9_-]{8,}|hf_[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_-]{8,})\b"
)
FORBIDDEN_RESULT_FIELDS = {
    "results",
    "aggregates",
    "scores",
    "latency_ms",
    "cost_usd",
    "safety_results",
    "selected_option",
}


def load_json(path: Path, label: str) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is invalid: {exc}") from exc


def _presence_errors(schema: dict, data: dict) -> list[str]:
    return [
        f"missing required field: {field}"
        for field in schema.get("required", [])
        if field not in data
    ]


def _scalar_errors(schema: dict, data: dict) -> list[str]:
    errors = []
    for field in schema.get("nonempty_strings", []):
        if not isinstance(data.get(field), str) or not data[field].strip():
            errors.append(f"{field} must be a non-empty string")
    for field in schema.get("list_fields", []):
        if not isinstance(data.get(field), list) or not data[field]:
            errors.append(f"{field} must be a non-empty list")
    for field in schema.get("boolean_fields", []):
        if not isinstance(data.get(field), bool):
            errors.append(f"{field} must be boolean")
    for field, allowed in schema.get("enums", {}).items():
        if data.get(field) not in allowed:
            errors.append(f"{field} must be one of {allowed}")
    return errors


def _identifier_errors(schema: dict, data: dict) -> list[str]:
    errors = []
    for field in schema.get("id_lists", []):
        seen: set[str] = set()
        for index, item in enumerate(data.get(field, [])):
            if not isinstance(item, dict):
                errors.append(f"{field}[{index}] must be an object")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip() or item_id in seen:
                errors.append(f"{field}[{index}].id must be non-empty and unique")
            else:
                seen.add(item_id)
    return errors


def _item_errors(schema: dict, data: dict) -> list[str]:
    errors = []
    for field, required_fields in schema.get("item_required", {}).items():
        for index, item in enumerate(data.get(field, [])):
            if not isinstance(item, dict):
                continue
            for required_field in required_fields:
                if item.get(required_field) in (None, "", []):
                    errors.append(f"{field}[{index}].{required_field} is required")
    for dotted_field, allowed in schema.get("item_enums", {}).items():
        list_field, item_field = dotted_field.split(".", 1)
        for index, item in enumerate(data.get(list_field, [])):
            if isinstance(item, dict) and item.get(item_field) not in allowed:
                errors.append(
                    f"{list_field}[{index}].{item_field} must be one of {allowed}"
                )
    return errors


def _blocked_extra_errors(data: dict) -> list[str]:
    errors = []
    plan_hash = data.get("plan_hash")
    if not isinstance(plan_hash, str) or not PLAN_HASH.fullmatch(plan_hash):
        errors.append(
            "plan_hash must use sha256 followed by 64 lowercase hexadecimal characters"
        )
    case_count = data.get("case_count")
    if isinstance(case_count, bool) or not isinstance(case_count, int) or case_count <= 0:
        errors.append("case_count must be a positive integer")
    for field in (
        "execution_complete",
        "measured_results_complete",
        "model_selection_complete",
    ):
        if data.get(field) is not False:
            errors.append(f"{field} must be false for an execution-blocked handoff")
    if data.get("winner") is not None:
        errors.append("winner must be null for an execution-blocked handoff")
    rerun_command = data.get("rerun_command")
    named_owner = data.get("named_owner")
    if not any(
        isinstance(value, str) and value.strip()
        for value in (rerun_command, named_owner)
    ):
        errors.append("provide a non-empty rerun_command or named_owner")
    missing = data.get("missing_credentials_or_tools", [])
    if isinstance(missing, list):
        if not missing:
            errors.append("missing_credentials_or_tools must not be empty")
        for index, item in enumerate(missing):
            if not isinstance(item, str) or not item.strip():
                errors.append(
                    f"missing_credentials_or_tools[{index}] must be a non-empty string"
                )
            elif SECRET_ASSIGNMENT.search(item) or SECRET_TOKEN.search(item):
                errors.append(
                    f"missing_credentials_or_tools[{index}] exposes a secret value"
                )
    safety_stops = data.get("safety_stops", [])
    if isinstance(safety_stops, list):
        if not safety_stops:
            errors.append("safety_stops must not be empty")
        for index, item in enumerate(safety_stops):
            if not isinstance(item, str) or not item.strip():
                errors.append(f"safety_stops[{index}] must be a non-empty string")
    present_forbidden = sorted(FORBIDDEN_RESULT_FIELDS.intersection(data))
    if present_forbidden:
        errors.append(
            "execution-blocked handoff must omit measured result fields: "
            f"{present_forbidden}"
        )
    return errors


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in STAGES:
        print(
            f"usage: validate_output.py <{'|'.join(STAGES)}> ARTIFACT.json",
            file=sys.stderr,
        )
        return 2
    stage = sys.argv[1]
    here = Path(__file__).resolve().parent
    schema_path = here.parent / "assets" / STAGES[stage]
    artifact_path = Path(sys.argv[2])
    try:
        schema = load_json(schema_path, "schema")
        data = load_json(artifact_path, "artifact")
    except ValueError as exc:
        print(
            json.dumps(
                {"valid": False, "stage": stage, "errors": [str(exc)]}, indent=2
            )
        )
        return 1
    if not isinstance(schema, dict):
        print(
            json.dumps(
                {"valid": False, "stage": stage, "errors": ["schema must be a JSON object"]},
                indent=2,
            )
        )
        return 1
    errors: list[str] = []
    if not isinstance(data, dict):
        errors.append("artifact must be a JSON object")
    else:
        errors.extend(_presence_errors(schema, data))
        errors.extend(_scalar_errors(schema, data))
        errors.extend(_identifier_errors(schema, data))
        errors.extend(_item_errors(schema, data))
        if stage == "blocked":
            errors.extend(_blocked_extra_errors(data))
    result = {
        "valid": not errors,
        "stage": stage,
        "skill": schema.get("skill"),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
