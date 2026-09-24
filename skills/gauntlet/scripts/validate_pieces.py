#!/usr/bin/env python3
"""Validate pieces.json and lanes.json for a gauntlet run (SPEC 8.1, 8.3, 8.4, 6).

Enforced rules:
- Every piece declares at least one inspection method from the closed set:
  run, test, measure, screenshot, render, reader-proxy, claim-audit,
  source-reach, red-team, read.
- Every method except read and reader-proxy declares an inspection_command.
- read alone is never sufficient. On knowledge-work domains (prose,
  research, strategy, deck, prompt-system) read must pair with reader-proxy
  or claim-audit.
- Unknown methods and unknown piece statuses are rejected.
- Any S3 configuration where two lanes share an owned path, or two pieces
  in different lanes share an artifact path, is refused.

Prints machine-readable JSON findings on stdout.
Exit codes: 0 valid, 1 validation failure, 2 usage error.
"""

import argparse
import json
import os
import sys

METHODS = {
    "run", "test", "measure", "screenshot", "render", "reader-proxy",
    "claim-audit", "source-reach", "red-team", "read",
}
NO_COMMAND_METHODS = {"read", "reader-proxy"}
KNOWLEDGE_DOMAINS = {"prose", "research", "strategy", "deck", "prompt-system"}
PIECE_STATUSES = {
    "pending", "looping", "converged", "capped", "blocked", "dropped",
}


def norm_path(p):
    """Strip fragment, leading ./ and trailing / for overlap comparison."""
    p = str(p).split("#", 1)[0].strip()
    while p.startswith("./"):
        p = p[2:]
    return p.rstrip("/")


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Enforce the inspection closed set, reject unjudgeable "
        "pieces and overlapping lane paths."
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

    findings = []
    pieces_data = load_json(os.path.join(run_dir, "pieces.json"))
    lanes_data = load_json(os.path.join(run_dir, "lanes.json"))
    run_data = load_json(os.path.join(run_dir, "run.json")) or {}

    shape = None
    if isinstance(lanes_data, dict) and lanes_data.get("shape"):
        shape = str(lanes_data["shape"]).strip()
    elif run_data.get("execution_shape"):
        shape = str(run_data["execution_shape"]).strip()

    domain_primary = str(run_data.get("domain_primary", "")).strip()

    pieces = []
    if not isinstance(pieces_data, dict):
        findings.append({
            "check": "pieces-missing",
            "detail": "pieces.json is missing or not valid JSON.",
        })
    else:
        pieces = [p for p in (pieces_data.get("pieces") or [])
                  if isinstance(p, dict)]
        if not pieces:
            findings.append({
                "check": "no-pieces",
                "detail": "pieces.json declares no pieces.",
            })

    for piece in pieces:
        pid = str(piece.get("id", "<no-id>"))
        domain = str(piece.get("domain", "") or domain_primary).strip()

        status = piece.get("status")
        if status is not None and status not in PIECE_STATUSES:
            findings.append({
                "check": "unknown-status",
                "piece": pid,
                "detail": "status %r is not in the closed set %s."
                % (status, sorted(PIECE_STATUSES)),
            })

        inspections = piece.get("inspection") or []
        if not isinstance(inspections, list):
            inspections = [inspections]
        methods = set()
        for entry in inspections:
            if isinstance(entry, str):
                entry = {"method": entry}
            if not isinstance(entry, dict):
                findings.append({
                    "check": "unknown-method",
                    "piece": pid,
                    "detail": "inspection entry %r is not an object." % (entry,),
                })
                continue
            method = str(entry.get("method", "")).strip()
            if method not in METHODS:
                findings.append({
                    "check": "unknown-method",
                    "piece": pid,
                    "detail": "method %r is not in the closed set %s."
                    % (method, sorted(METHODS)),
                })
                continue
            methods.add(method)
            if method not in NO_COMMAND_METHODS:
                command = str(entry.get("inspection_command", "") or "").strip()
                if not command:
                    findings.append({
                        "check": "missing-inspection-command",
                        "piece": pid,
                        "detail": "method %r declares no inspection_command. "
                        "Every method except read and reader-proxy needs "
                        "one." % method,
                    })

        if not methods:
            findings.append({
                "check": "no-inspection",
                "piece": pid,
                "detail": "piece declares no valid inspection method. A "
                "piece that cannot be inspected is not a valid piece. "
                "Split it or drop it.",
            })
        elif methods == {"read"}:
            findings.append({
                "check": "read-alone",
                "piece": pid,
                "detail": "read is the only inspection method. read alone "
                "is never sufficient.",
            })

        if (
            "read" in methods
            and domain in KNOWLEDGE_DOMAINS
            and not ({"reader-proxy", "claim-audit"} & methods)
        ):
            findings.append({
                "check": "knowledge-read-unpaired",
                "piece": pid,
                "detail": "domain %r is knowledge work: read must pair "
                "with reader-proxy or claim-audit." % domain,
            })

    # S3 overlap checks: lanes own disjoint artifact paths.
    if shape == "S3":
        lanes = []
        if isinstance(lanes_data, dict):
            lanes = [ln for ln in (lanes_data.get("lanes") or [])
                     if isinstance(ln, dict)]
        if not lanes:
            findings.append({
                "check": "lanes-missing",
                "detail": "shape is S3 but lanes.json declares no lanes.",
            })

        owned = {}
        for lane in lanes:
            lane_id = str(lane.get("id", "<no-id>"))
            for path in lane.get("owned_paths") or []:
                key = norm_path(path)
                if not key:
                    continue
                if key in owned and owned[key] != lane_id:
                    findings.append({
                        "check": "lane-path-overlap",
                        "lanes": sorted([owned[key], lane_id]),
                        "detail": "lanes %r and %r both own path %r. S3 "
                        "lanes must own disjoint artifact paths."
                        % (owned[key], lane_id, path),
                    })
                else:
                    owned[key] = lane_id

        artifact_lanes = {}
        for piece in pieces:
            pid = str(piece.get("id", "<no-id>"))
            lane_id = str(piece.get("lane", "")).strip()
            for path in piece.get("artifact_paths") or []:
                key = norm_path(path)
                if not key:
                    continue
                prior = artifact_lanes.get(key)
                if prior and prior[0] != lane_id:
                    findings.append({
                        "check": "cross-lane-artifact-overlap",
                        "pieces": sorted([prior[1], pid]),
                        "detail": "pieces %r (lane %r) and %r (lane %r) "
                        "share artifact path %r across lanes under S3."
                        % (prior[1], prior[0], pid, lane_id, path),
                    })
                else:
                    artifact_lanes[key] = (lane_id, pid)

    result = {
        "script": "validate_pieces",
        "run_dir": run_dir,
        "shape": shape,
        "ok": not findings,
        "pieces_checked": len(pieces),
        "findings": findings,
    }
    print(json.dumps(result, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
