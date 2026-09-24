#!/usr/bin/env python3
"""Initialize a gauntlet run directory (SPEC sections 7 and 8.2).

Creates .gauntlet/runs/<YYYYMMDD-HHMM-slug>/ under --root with the full
state skeleton: bar/refs/, waves/, rounds/, claims/, verification/,
sessions/, empty CONTEXT.md and PLAN.md, schema-correct empty pieces.json,
lanes.json, cost.json, and sessions/sessions.json, plus run.json seeded per
SPEC 8.2 with status "briefed" and default budgets. Also creates the sealed
directory at .gauntlet/sealed/<run-id>/, outside runs/ (SPEC 11.2).

Prints a machine-readable JSON result on stdout:

    {"run_dir": "<absolute path>", "sealed_dir": "<absolute path>",
     "run": { ...run.json contents... }}

Exit codes: 0 on success, 1 when the run directory already exists,
2 on usage errors (bad slug, bad domain, bad shape, bad --created).
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

DOMAINS = [
    "code",
    "visual",
    "prose",
    "research",
    "deck",
    "strategy",
    "prompt-system",
    "brand",
]
SHAPES = ["S1", "S2", "S3"]

# SPEC 11.4 defaults. All user-overridable at brief time, by editing run.json.
DEFAULT_BUDGETS = {
    "rounds_cap_per_piece": 10,
    "wave_cap": 4,
    "wall_clock_hours_per_session": 6,
    "subagent_cap_per_run": 400,
    "cost_ceiling": "user-set",
}

SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]*")


def parse_created(raw):
    """Parse an ISO timestamp, tolerating a trailing Z. Returns UTC."""
    text = raw.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Create a gauntlet run directory skeleton (SPEC 7, 8.2)."
    )
    parser.add_argument(
        "--root",
        required=True,
        help="Project directory that contains (or will contain) .gauntlet/.",
    )
    parser.add_argument(
        "--slug",
        required=True,
        help="Run slug: lowercase letters, digits, hyphens.",
    )
    parser.add_argument("--goal", required=True, help="One-line goal.")
    parser.add_argument(
        "--domain", required=True, choices=DOMAINS, help="Primary domain."
    )
    parser.add_argument(
        "--shape", required=True, choices=SHAPES, help="Execution shape."
    )
    parser.add_argument(
        "--created",
        default=None,
        help="ISO timestamp for the run id and created field. Default: now (UTC).",
    )
    args = parser.parse_args(argv)

    if not SLUG_RE.fullmatch(args.slug):
        parser.error(
            "--slug must be lowercase letters, digits, and hyphens, "
            "starting with a letter or digit"
        )
    if args.created:
        try:
            created = parse_created(args.created)
        except ValueError as exc:
            parser.error("--created is not a valid ISO timestamp: %s" % exc)
    else:
        created = datetime.now(timezone.utc)

    run_id = created.strftime("%Y%m%d-%H%M") + "-" + args.slug
    root = Path(args.root).resolve()
    run_dir = root / ".gauntlet" / "runs" / run_id
    sealed_dir = root / ".gauntlet" / "sealed" / run_id

    if run_dir.exists():
        print("Run directory already exists: %s" % run_dir, file=sys.stderr)
        print(json.dumps({"error": "run-dir-exists", "run_dir": str(run_dir)}))
        return 1

    # Directory skeleton, SPEC section 7.
    for rel in ("bar/refs", "waves", "rounds", "claims", "verification", "sessions"):
        (run_dir / rel).mkdir(parents=True)
    sealed_dir.mkdir(parents=True, exist_ok=True)

    # run.json per SPEC 8.2. precheck is recorded by the front door;
    # project_root anchors artifact path resolution for hash_artifacts.py.
    run = {
        "run_id": run_id,
        "goal_one_line": args.goal,
        "domain_primary": args.domain,
        "execution_shape": args.shape,
        "status": "briefed",
        "created": created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "plan_hash": None,
        "precheck": None,
        "context_isolation": "clean",
        "budgets": dict(DEFAULT_BUDGETS),
        "current_wave": 1,
        "stop_reason": None,
        "project_root": str(root),
    }
    write_json(run_dir / "run.json", run)

    # CONTEXT.md is append-only and PLAN.md is the wave plan; gauntlet-brief
    # writes their content. Created empty so the skeleton is complete.
    (run_dir / "CONTEXT.md").write_text("", encoding="utf-8")
    (run_dir / "PLAN.md").write_text("", encoding="utf-8")

    write_json(
        run_dir / "pieces.json",
        {
            "run_id": run_id,
            "plan_hash": None,
            "decomposition_owner": "lead-agent",
            "pieces": [],
        },
    )
    write_json(run_dir / "lanes.json", {"shape": args.shape, "lanes": []})
    write_json(
        run_dir / "cost.json",
        {
            "rounds_total": 0,
            "subagents_total": 0,
            "sessions_total": 0,
            "wall_clock_hours": 0,
            "cost_spent": 0,
            "tokens": "unknown",
            "notes": "",
        },
    )
    write_json(run_dir / "sessions" / "sessions.json", {"sessions": []})

    print(
        json.dumps(
            {"run_dir": str(run_dir), "sealed_dir": str(sealed_dir), "run": run},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
