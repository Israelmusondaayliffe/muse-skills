#!/usr/bin/env python3
"""Compute verification consensus for one piece. No model judgment.

Reads verification/<piece>/quality-*.json and integrity-*.json under the run
directory, applies the fixed consensus table from SPEC section 9.5, writes
consensus.json into the same verification directory, and prints it on stdout.
A model must never compute consensus. This script is the only author of
consensus.json.

Consensus table, first matching row wins:
  any integrity fail                        -> failed (regardless of quality votes)
  any cannot-verify, either type            -> unverifiable
  all pass, both types                      -> verified
  majority quality pass with dissent        -> verified-with-dissent
  otherwise (majority quality fail, or tie) -> failed

Exit codes: 0 consensus computed (whatever its value), 1 validation failure,
2 usage error.
"""

import argparse
import glob
import json
import os
import sys
from datetime import datetime, timezone

RESULT_SET = {"pass", "fail", "cannot-verify"}
TYPE_SET = {"quality", "integrity"}
CONSENSUS_SET = {"verified", "verified-with-dissent", "failed", "unverifiable"}


def die(message):
    print(json.dumps({"error": message}))
    sys.exit(1)


def atomic_write_json(path, payload):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    os.replace(tmp, path)


def load_verdicts(verification_dir, verifier_type, expected_piece_id=None):
    """Load and validate every <type>-*.json verdict, sorted by filename."""
    pattern = os.path.join(verification_dir, "{0}-*.json".format(verifier_type))
    verdicts = []
    for path in sorted(glob.glob(pattern)):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            die("{0}: unreadable verifier verdict ({1})".format(path, exc))
        if not isinstance(data, dict):
            die("{0}: verifier verdict must be a JSON object".format(path))
        declared_type = data.get("verifier_type")
        if declared_type not in TYPE_SET:
            die("{0}: verifier_type {1!r} not in closed set {2}".format(
                path, declared_type, sorted(TYPE_SET)))
        if declared_type != verifier_type:
            die("{0}: verifier_type {1!r} does not match filename type {2!r}".format(
                path, declared_type, verifier_type))
        result = data.get("result")
        if result not in RESULT_SET:
            die("{0}: result {1!r} not in closed set {2}".format(
                path, result, sorted(RESULT_SET)))
        if not isinstance(data.get("plan_hash_matched"), bool):
            die("{0}: plan_hash_matched must be a boolean".format(path))
        if expected_piece_id is not None and data.get("piece_id") != expected_piece_id:
            die("{0}: piece_id {1!r} does not match the piece under consensus {2!r}".format(
                path, data.get("piece_id"), expected_piece_id))
        verdicts.append((path, data))
    return verdicts


def vote_counts(verdicts):
    counts = {"pass": 0, "fail": 0, "cannot-verify": 0}
    for _, data in verdicts:
        counts[data["result"]] += 1
    return counts


def dissent_lines(verdicts, verifier_type):
    """Non-pass reasons, preserved verbatim, in filename order."""
    lines = []
    for path, data in verdicts:
        if data["result"] == "pass":
            continue
        index = data.get("verifier_index")
        if not isinstance(index, int):
            index = os.path.basename(path)
        reason = data.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            reason = "no reason recorded"
        lines.append("{0} verifier {1}: {2}".format(
            verifier_type.capitalize(), index, reason))
    return lines


def decide(quality_results, integrity_results):
    """The section 9.5 table. First matching row wins."""
    if "fail" in integrity_results:
        return "failed"
    if "cannot-verify" in quality_results or "cannot-verify" in integrity_results:
        return "unverifiable"
    if all(r == "pass" for r in quality_results + integrity_results):
        return "verified"
    # No integrity fail, no cannot-verify, at least one quality fail remains.
    passes = quality_results.count("pass")
    fails = quality_results.count("fail")
    if passes > fails:
        return "verified-with-dissent"
    return "failed"


def main():
    parser = argparse.ArgumentParser(
        description="Compute consensus.json for one piece from verifier "
                    "verdicts on disk. Never computed by a model.")
    parser.add_argument("--run-dir", required=True,
                        help="Path to .gauntlet/runs/<run-id>")
    parser.add_argument("--piece", required=True, help="Piece id")
    args = parser.parse_args()

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        die("run directory not found: {0}".format(run_dir))
    verification_dir = os.path.join(run_dir, "verification", args.piece)
    if not os.path.isdir(verification_dir):
        die("verification directory not found: {0}".format(verification_dir))

    quality = load_verdicts(verification_dir, "quality", args.piece)
    integrity = load_verdicts(verification_dir, "integrity", args.piece)
    if not quality:
        die("no quality-*.json verdicts in {0}; both verifier types are "
            "required".format(verification_dir))
    if not integrity:
        die("no integrity-*.json verdicts in {0}; both verifier types are "
            "required".format(verification_dir))

    quality_results = [d["result"] for _, d in quality]
    integrity_results = [d["result"] for _, d in integrity]
    consensus = decide(quality_results, integrity_results)
    if consensus not in CONSENSUS_SET:
        die("internal error: consensus {0!r} not in closed set".format(consensus))

    payload = {
        "piece_id": args.piece,
        "quality_votes": vote_counts(quality),
        "integrity_votes": vote_counts(integrity),
        "consensus": consensus,
        "dissent": (dissent_lines(quality, "quality")
                    + dissent_lines(integrity, "integrity")),
        "plan_hash_matched": all(
            d["plan_hash_matched"] for _, d in quality + integrity),
        "computed_by": "scripts/consensus.py",
        "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    atomic_write_json(os.path.join(verification_dir, "consensus.json"), payload)
    print(json.dumps(payload, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
