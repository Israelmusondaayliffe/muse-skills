#!/usr/bin/env python3
"""Collect a read-only inventory of local skills on Hatch.

Scans skill roots for */SKILL.md, records exact paths, SHA-256 fingerprints,
and frontmatter name/description. Read-only: it never modifies skills.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def parse_frontmatter(skill_file: Path, errors: list[str]) -> dict | None:
    try:
        text = skill_file.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{skill_file}: {exc}")
        return None
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"{skill_file}: missing frontmatter block")
        return None
    front = {}
    for line in match.group(1).splitlines():
        m = re.match(r"^(name|description):\s*(.*)$", line)
        if m:
            value = m.group(2).strip().strip('"').strip("'")
            front[m.group(1)] = value
    if not front.get("name"):
        errors.append(f"{skill_file}: frontmatter missing 'name'")
    if not front.get("description"):
        errors.append(f"{skill_file}: frontmatter missing 'description'")
    return front


def skill_records(root: Path, layer: str, errors: list[str]) -> list[dict]:
    records = []
    if not root.exists():
        return records
    for skill_file in sorted(root.glob("*/SKILL.md")):
        front = parse_frontmatter(skill_file, errors) or {}
        records.append({
            "name": front.get("name") or skill_file.parent.name,
            "directory": skill_file.parent.name,
            "layer": layer,
            "path": str(skill_file.parent),
            "skill_sha256": hashlib.sha256(skill_file.read_bytes()).hexdigest(),
            "description": front.get("description"),
            "frontmatter_ok": bool(front.get("name") and front.get("description")),
        })
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-root", type=Path,
                        default=Path.home() / "workspace" / "skills",
                        help="writable workspace skill root")
    parser.add_argument("--include-bundled", action="store_true",
                        help="also list bundled skills under /opt/hatch/skills (read-only)")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    errors: list[str] = []
    records = skill_records(args.skills_root, "workspace", errors)
    if args.include_bundled:
        records += skill_records(Path("/opt/hatch/skills"), "bundled", errors)

    data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "roots": {
            "workspace_skills": str(args.skills_root),
            "bundled_skills": "/opt/hatch/skills" if args.include_bundled else None,
        },
        "skills": records,
        "skill_count": len(records),
        "errors": errors,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "skill_count": len(records),
                      "errors": len(errors)}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
