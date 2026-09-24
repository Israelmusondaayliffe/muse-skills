#!/usr/bin/env python3
"""Freeze and verify the plan hash. SPEC sections 5.4, 9.2, and 9.5.

Hashes the success-criteria block of PLAN.md and, when present, bar/rubric.md
with SHA-256.

--record writes plan_hash (and rubric_hash when a rubric exists) into
run.json and pieces.json.

--check recomputes both hashes, compares them to the recorded values, and
reports match or mismatch per file. Any mismatch exits 1. A rubric or
success-criteria block edited mid-run is an integrity failure, not a
refinement.

Exit codes: 0 success (record done, or check all-match), 1 validation
failure or mismatch, 2 usage error.
"""

import argparse
import hashlib
import json
import os
import re
import sys

CRITERIA_HEADING = re.compile(r"^(#{1,6})\s*success\s+criteria\b", re.IGNORECASE)
ANY_HEADING = re.compile(r"^(#{1,6})\s")


def die(message):
    print(json.dumps({"error": message}))
    sys.exit(1)


def atomic_write_json(path, payload):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    os.replace(tmp, path)


def sha256_label(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def criteria_block(plan_text):
    """Extract the success-criteria block: its heading through the line
    before the next heading of the same or higher level. None if absent."""
    lines = plan_text.splitlines()
    start = None
    level = None
    for i, line in enumerate(lines):
        match = CRITERIA_HEADING.match(line.strip())
        if match:
            start = i
            level = len(match.group(1))
            break
    if start is None:
        return None
    block = [lines[start]]
    for line in lines[start + 1:]:
        heading = ANY_HEADING.match(line)
        if heading and len(heading.group(1)) <= level:
            break
        block.append(line)
    return "\n".join(l.rstrip() for l in block).strip()


def current_hashes(run_dir):
    """Recompute (plan_hash, rubric_hash) from the files on disk.
    Values are None when the file or block is absent."""
    plan_hash = None
    plan_path = os.path.join(run_dir, "PLAN.md")
    if os.path.isfile(plan_path):
        with open(plan_path, "r", encoding="utf-8") as handle:
            block = criteria_block(handle.read())
        if block:
            plan_hash = sha256_label(block.encode("utf-8"))
    rubric_hash = None
    rubric_path = os.path.join(run_dir, "bar", "rubric.md")
    if os.path.isfile(rubric_path):
        with open(rubric_path, "rb") as handle:
            rubric_hash = sha256_label(handle.read())
    return plan_hash, rubric_hash


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        die("{0}: unreadable JSON ({1})".format(path, exc))
    if not isinstance(data, dict):
        die("{0}: expected a JSON object".format(path))
    return data


def record(run_dir):
    plan_hash, rubric_hash = current_hashes(run_dir)
    if plan_hash is None:
        die("PLAN.md is missing or has no success-criteria block; "
            "nothing to record")
    written = []
    for name in ("run.json", "pieces.json"):
        path = os.path.join(run_dir, name)
        if not os.path.isfile(path):
            die("{0} not found; initialize the run before recording "
                "the plan hash".format(path))
        data = load_json(path)
        data["plan_hash"] = plan_hash
        if rubric_hash is not None:
            data["rubric_hash"] = rubric_hash
        atomic_write_json(path, data)
        written.append(name)
    print(json.dumps({
        "mode": "record",
        "plan_hash": plan_hash,
        "rubric_hash": rubric_hash,
        "written": written,
    }, indent=2))
    sys.exit(0)


def check(run_dir):
    plan_hash, rubric_hash = current_hashes(run_dir)
    run_data = load_json(os.path.join(run_dir, "run.json"))
    pieces_data = load_json(os.path.join(run_dir, "pieces.json"))
    recorded_plan = run_data.get("plan_hash")
    recorded_rubric = run_data.get("rubric_hash")

    results = {}

    if recorded_plan is None:
        results["PLAN.md"] = "not-recorded"
    elif plan_hash is None:
        results["PLAN.md"] = "mismatch"
    elif plan_hash != recorded_plan:
        results["PLAN.md"] = "mismatch"
    elif pieces_data.get("plan_hash") != recorded_plan:
        # run.json and pieces.json must carry the same frozen hash.
        results["PLAN.md"] = "mismatch"
    else:
        results["PLAN.md"] = "match"

    if recorded_rubric is None and rubric_hash is None:
        results["bar/rubric.md"] = "absent"
    elif recorded_rubric is None:
        # Rubric present without a frozen hash fails bar validation too.
        results["bar/rubric.md"] = "not-recorded"
    elif rubric_hash is None:
        # Recorded but the file moved or vanished.
        results["bar/rubric.md"] = "mismatch"
    elif rubric_hash != recorded_rubric:
        results["bar/rubric.md"] = "mismatch"
    else:
        results["bar/rubric.md"] = "match"

    ok = all(status in ("match", "absent") for status in results.values())
    print(json.dumps({
        "mode": "check",
        "results": results,
        "recorded_plan_hash": recorded_plan,
        "current_plan_hash": plan_hash,
        "recorded_rubric_hash": recorded_rubric,
        "current_rubric_hash": rubric_hash,
        "ok": ok,
    }, indent=2))
    sys.exit(0 if ok else 1)


def main():
    parser = argparse.ArgumentParser(
        description="Record or verify the SHA-256 hash of the PLAN.md "
                    "success-criteria block and bar/rubric.md.")
    parser.add_argument("--run-dir", required=True,
                        help="Path to .gauntlet/runs/<run-id>")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", action="store_true",
                      help="Compute hashes and write plan_hash into "
                           "run.json and pieces.json")
    mode.add_argument("--check", action="store_true",
                      help="Recompute hashes and compare to recorded "
                           "values, exit 1 on any mismatch")
    args = parser.parse_args()

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        die("run directory not found: {0}".format(run_dir))

    if args.record:
        record(run_dir)
    else:
        check(run_dir)


if __name__ == "__main__":
    main()
