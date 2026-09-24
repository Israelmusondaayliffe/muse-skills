#!/usr/bin/env python3
"""Validate a route brief artifact against assets/route-schema.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skill_output import validate


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_route.py ARTIFACT.json", file=sys.stderr)
        return 2
    try:
        result = validate(Path(__file__).resolve().parent.parent / "assets/route-schema.json", Path(sys.argv[1]))
    except ValueError as exc:
        result = {"valid": False, "skill": "analysis-to-story-router", "errors": [str(exc)]}
    print(json.dumps(result, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
