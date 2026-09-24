#!/usr/bin/env python3
"""Completeness gate for a gauntlet brief (SPEC section 9.2 step 5).

Checks <run-dir>/PLAN.md and <run-dir>/run.json for the 11 required brief
fields. Every field must be present and non-empty. Additional constraints:
success_criteria must number 3 to 7, execution_shape must be S1, S2, or S3.

Prints JSON with missing[] (absent or empty fields) and invalid{} (present
but constraint-violating fields).
Exit codes: 0 gate passes, 1 any field missing or invalid, 2 usage error.
"""

import argparse
import json
import os
import re
import sys

REQUIRED_FIELDS = [
    "goal_one_line",
    "success_criteria",
    "bar_definition",
    "bar_rationale",
    "done_means",
    "domain_primary",
    "execution_shape",
    "budget_ceiling",
    "out_of_scope",
    "non_negotiables",
    "inspection_feasibility",
]

HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
# Label regexes tolerate an optional leading list marker ("- ", "* ", "1. ")
# so the plan template's bulleted brief fields parse.
BOLD_LABEL_RE = re.compile(r"^(?:[-*+]|\d+[.)])?\s*\*\*([^*]+)\*\*\s*[:.]?\s*(.*)$")
PLAIN_LABEL_RE = re.compile(r"^(?:[-*+]|\d+[.)])?\s*([A-Za-z][A-Za-z0-9 _\-]{0,60})\s*:\s*(.*)$")
LIST_ITEM_RE = re.compile(r"(?m)^\s*(?:[-*+]|\d+[.)])\s+\S")
SHAPE_RE = re.compile(r"\bS[123]\b")


def normalize(name):
    """Lowercase and collapse non-alphanumerics to single underscores."""
    return re.sub(r"[^a-z0-9]+", "_", str(name).lower()).strip("_")


def is_empty(value):
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def collect_json_fields(obj, out):
    """Recursively collect required fields found as keys in run.json."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            nk = normalize(key)
            if nk in REQUIRED_FIELDS and nk not in out and not is_empty(value):
                out[nk] = value
            collect_json_fields(value, out)
    elif isinstance(obj, list):
        for item in obj:
            collect_json_fields(item, out)


def parse_plan(text):
    """Extract required fields from PLAN.md headings and label lines."""
    fields = {}
    required = set(REQUIRED_FIELDS)
    current = None
    buf = []

    def flush():
        nonlocal current, buf
        if current is not None:
            body = "\n".join(buf).strip()
            if current not in fields and body:
                fields[current] = body
        current = None
        buf = []

    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        bold = BOLD_LABEL_RE.match(line)
        plain = PLAIN_LABEL_RE.match(line)
        if heading:
            name = normalize(heading.group(1))
            flush()
            if name in required:
                current = name
        elif bold and normalize(bold.group(1)) in required:
            flush()
            current = normalize(bold.group(1))
            if bold.group(2).strip():
                buf.append(bold.group(2).strip())
        elif plain and normalize(plain.group(1)) in required:
            flush()
            current = normalize(plain.group(1))
            if plain.group(2).strip():
                buf.append(plain.group(2).strip())
        elif current is not None:
            buf.append(line)
    flush()
    return fields


def count_criteria(value):
    if isinstance(value, list):
        return len([v for v in value if str(v).strip()])
    text = str(value)
    bullets = LIST_ITEM_RE.findall(text)
    if bullets:
        return len(bullets)
    return len([ln for ln in text.splitlines() if ln.strip()])


def main():
    parser = argparse.ArgumentParser(
        description="Block until every required brief field is present, "
        "non-empty, and within its constraints."
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Path to .gauntlet/runs/<run-id>",
    )
    args = parser.parse_args()

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        print(json.dumps({"error": "run dir not found: %s" % run_dir}))
        return 2

    found = {}
    sources = {}

    run_json_path = os.path.join(run_dir, "run.json")
    if os.path.isfile(run_json_path):
        try:
            with open(run_json_path, "r", encoding="utf-8") as fh:
                run_data = json.load(fh)
        except ValueError:
            run_data = None
        if run_data is not None:
            json_fields = {}
            collect_json_fields(run_data, json_fields)
            for key, value in json_fields.items():
                found[key] = value
                sources[key] = "run.json"

    plan_path = os.path.join(run_dir, "PLAN.md")
    if os.path.isfile(plan_path):
        with open(plan_path, "r", encoding="utf-8", errors="replace") as fh:
            plan_fields = parse_plan(fh.read())
        for key, value in plan_fields.items():
            if key not in found:
                found[key] = value
                sources[key] = "PLAN.md"

    missing = [f for f in REQUIRED_FIELDS if f not in found or is_empty(found[f])]

    invalid = {}
    if "success_criteria" not in missing:
        count = count_criteria(found["success_criteria"])
        if not 3 <= count <= 7:
            invalid["success_criteria"] = (
                "found %d criteria, need 3 to 7, each independently "
                "checkable" % count
            )
    if "execution_shape" not in missing:
        raw = str(found["execution_shape"]).strip()
        match = SHAPE_RE.search(raw)
        if not match or (len(raw) <= 3 and raw not in ("S1", "S2", "S3")):
            invalid["execution_shape"] = (
                "value %r is not one of S1, S2, S3" % raw
            )

    result = {
        "script": "brief_complete",
        "run_dir": run_dir,
        "ok": not missing and not invalid,
        "missing": missing,
        "invalid": invalid,
        "found": {k: sources[k] for k in sorted(sources) if k not in missing},
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
