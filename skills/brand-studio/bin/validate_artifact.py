#!/usr/bin/env python3
"""Validate a brand-studio JSON artifact against its bundled schema.

Usage:
    python3 validate_artifact.py ARTIFACT.json --schema SCHEMA.json

Exit code 0 when valid, 1 when invalid, 2 on I/O or parse failure.
Structure-only check: it never establishes approval, taste, or visual proof.
"""

import argparse
import json
import sys
from pathlib import Path


def load_json(path: Path, label: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} is invalid: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--schema", type=Path, required=True)
    args = parser.parse_args()
    try:
        schema = load_json(args.schema, "schema")
        data = load_json(args.artifact, "artifact")
    except ValueError as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, indent=2))
        return 2
    errors = []
    if not isinstance(data, dict):
        errors.append("artifact must be a JSON object")
        data = {}
    for field in schema.get("required", []):
        if field not in data:
            errors.append(f"missing required field: {field}")
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
    for field, expected in schema.get("const_values", {}).items():
        if data.get(field) != expected:
            errors.append(f"{field} must equal {expected!r}")
    for field in schema.get("id_lists", []):
        values = data.get(field, [])
        if not isinstance(values, list):
            continue
        seen = set()
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                errors.append(f"{field}[{index}] must be an object")
                continue
            item_id = item.get("id")
            if not isinstance(item_id, str) or not item_id.strip() or item_id in seen:
                errors.append(f"{field}[{index}].id must be non-empty and unique")
            seen.add(item_id)
    for field, required_fields in schema.get("item_required", {}).items():
        values = data.get(field, [])
        if not isinstance(values, list):
            continue
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                continue
            for required_field in required_fields:
                value = item.get(required_field)
                if value is None or value == "" or value == []:
                    errors.append(f"{field}[{index}].{required_field} is required")
    for dotted_field, allowed in schema.get("item_enums", {}).items():
        list_field, item_field = dotted_field.split(".", 1)
        values = data.get(list_field, [])
        if not isinstance(values, list):
            continue
        for index, item in enumerate(values):
            if isinstance(item, dict) and item.get(item_field) not in allowed:
                errors.append(f"{list_field}[{index}].{item_field} must be one of {allowed}")
    if schema.get("phase") == "review" and data.get("result") == "pass":
        if any(not isinstance(c, dict) or c.get("status") != "passed" for c in data.get("checks", [])):
            errors.append("pass requires every mandatory check to be passed")
        if data.get("findings"):
            errors.append("pass requires no unresolved findings")
    if schema.get("phase") == "review" and data.get("acceptance") == "accepted":
        if not isinstance(data.get("user_acceptance_evidence"), str) or not data["user_acceptance_evidence"].strip():
            errors.append("accepted requires explicit user_acceptance_evidence")
    result = {
        "valid": not errors,
        "skill": schema.get("skill"),
        "phase": schema.get("phase"),
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
