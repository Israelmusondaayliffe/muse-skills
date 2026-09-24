#!/usr/bin/env python3
"""Validate browser-verifiable acceptance flows."""

import json
import sys
from pathlib import Path

STATUSES = {"untested", "passed", "failed", "blocked"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_flows.py FLOWS.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    flows = data.get("flows")
    if not isinstance(flows, list) or not flows:
        errors.append("flows must be a non-empty list")
        flows = []
    seen = set()
    for index, flow in enumerate(flows):
        if not isinstance(flow, dict):
            errors.append(f"flows[{index}] must be an object")
            continue
        flow_id = flow.get("id")
        if not isinstance(flow_id, str) or not flow_id or flow_id in seen:
            errors.append(f"flows[{index}].id must be non-empty and unique")
        seen.add(flow_id)
        if not isinstance(flow.get("name"), str) or not flow["name"].strip():
            errors.append(f"flows[{index}].name must be non-empty")
        if flow.get("status") not in STATUSES:
            errors.append(f"flows[{index}].status is invalid")
        steps = flow.get("steps")
        if not isinstance(steps, list) or not steps:
            errors.append(f"flows[{index}].steps must be non-empty")
            continue
        for step_index, step in enumerate(steps):
            for field in ("action", "expected", "evidence"):
                if not isinstance(step.get(field), str) or not step[field].strip():
                    errors.append(f"flows[{index}].steps[{step_index}].{field} must be non-empty")
    print(json.dumps({"valid": not errors, "flow_count": len(flows), "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
