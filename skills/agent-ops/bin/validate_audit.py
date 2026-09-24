#!/usr/bin/env python3
"""Validate an agent-system audit ledger."""

import json
import sys
from pathlib import Path

SEVERITIES = {"blocker", "high", "medium", "low"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_audit.py AUDIT.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    if not isinstance(data.get("system"), str) or not data["system"].strip():
        errors.append("system must be a non-empty string")
    findings = data.get("findings")
    if not isinstance(findings, list):
        errors.append("findings must be a list")
        findings = []
    seen = set()
    for index, item in enumerate(findings):
        if not isinstance(item, dict):
            errors.append(f"findings[{index}] must be an object")
            continue
        finding_id = item.get("id")
        if not isinstance(finding_id, str) or not finding_id or finding_id in seen:
            errors.append(f"findings[{index}].id must be non-empty and unique")
        seen.add(finding_id)
        if item.get("severity") not in SEVERITIES:
            errors.append(f"findings[{index}].severity is invalid")
        for field in ("control", "evidence", "remedy"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"findings[{index}].{field} must be non-empty")
    print(json.dumps({"valid": not errors, "finding_count": len(findings), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
