#!/usr/bin/env python3
"""Find exact-name overlaps in a capability inventory.

Reads the JSON written by collect_inventory.py and reports every skill name
that appears more than once, classified as identical-mirror, drifted-copy,
cross-layer (workspace vs bundled), or unresolved. Read-only: no source
is modified. See ../references/classification.md for dispositions.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def classify(locations: list[dict]) -> str:
    fingerprints = {loc.get("skill_sha256") for loc in locations
                    if loc.get("skill_sha256")}
    layers = {loc.get("layer") for loc in locations}
    if len(locations) > 1 and len(fingerprints) == 1:
        return "identical-mirror"
    if len(fingerprints) > 1:
        return "drifted-copy"
    if len(layers) > 1:
        return "cross-layer"
    return "unresolved"


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: find_overlaps.py INVENTORY.json OUTPUT.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid inventory: {exc}", file=sys.stderr)
        return 2

    groups: dict[str, list[dict]] = defaultdict(list)
    for item in data.get("skills", []):
        name = item.get("name", "")
        if name:
            groups[name].append({
                "name": name,
                "directory": item.get("directory"),
                "layer": item.get("layer"),
                "path": item.get("path"),
                "skill_sha256": item.get("skill_sha256"),
            })

    overlaps = []
    for name, locations in sorted(groups.items()):
        if len(locations) > 1:
            overlaps.append({
                "name": name,
                "state": classify(locations),
                "locations": locations,
            })

    output = {
        "overlap_count": len(overlaps),
        "overlaps": overlaps,
        "note": ("Exact-name groups only. Different names claiming the same "
                 "user intent (trigger-collision) require manual review of "
                 "descriptions. See references/classification.md."),
    }
    Path(sys.argv[2]).write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": sys.argv[2],
                      "overlap_count": len(overlaps)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
