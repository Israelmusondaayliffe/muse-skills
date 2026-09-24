#!/usr/bin/env python3
"""Validate a single visual direction selection for a web product.

Adapted from the web-product-studio bundle: the original enforced a fixed
list of host-specific design skills. In this environment visual direction is
a free-form named choice, so the validator enforces the invariant that
matters: exactly one selected direction or none, with evidence and rationale.
"""

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_selection.py SELECTION.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    errors = []
    selected = data.get("selected")
    if selected is not None and (not isinstance(selected, str) or not selected.strip()):
        errors.append("selected must be a non-empty string or null")
    if not isinstance(data.get("evidence"), list) or not data["evidence"]:
        errors.append("evidence must be a non-empty list")
    if not isinstance(data.get("rationale"), str) or not data["rationale"].strip():
        errors.append("rationale must be non-empty")
    if not isinstance(data.get("rejected"), list):
        errors.append("rejected must be a list")
    # Guard against conflicting simultaneous directions: evidence/rationale
    # mentioning a second full design system alongside a selection is suspect.
    if selected and isinstance(data.get("rationale"), str):
        lower = data["rationale"].lower()
        if "two directions" in lower or "both systems" in lower:
            errors.append("rationale suggests more than one visual direction; select exactly one")
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
