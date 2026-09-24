#!/usr/bin/env python3
"""Validate a coordinator artifact against a compact bundled schema."""

from __future__ import annotations

import json
from pathlib import Path


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


def validate(schema_path: Path, artifact_path: Path) -> dict[str, object]:
    schema = load_json(schema_path, "schema")
    data = load_json(artifact_path, "artifact")
    if not isinstance(schema, dict):
        raise ValueError("schema must be a JSON object")
    if not isinstance(data, dict):
        return {
            "valid": False,
            "skill": schema.get("skill"),
            "errors": ["artifact must be a JSON object"],
        }
    errors = []
    errors.extend(_presence_errors(schema, data))
    errors.extend(_scalar_errors(schema, data))
    errors.extend(_identifier_errors(schema, data))
    errors.extend(_item_errors(schema, data))
    return {"valid": not errors, "skill": schema.get("skill"), "errors": errors}
