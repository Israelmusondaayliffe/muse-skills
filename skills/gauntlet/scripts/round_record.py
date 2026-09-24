#!/usr/bin/env python3
"""Record one round's verdict. Enforcement layer behind INV-2.

Validates a critic verdict against the SPEC section 8.5 schema, including
the closed sets, and REJECTS with exit 1 any verdict where
critic_saw_builder_context is true, critic_context_source is anything other
than "files-only", or largest_gap is empty. Those assertions are made by the
spawning code, not self-reported by the critic, and this script is where
they are enforced rather than trusted.

On accept it atomically writes verdict.json into rounds/<piece>/<nnn>/ and
updates the piece's rounds_completed, consecutive_wins, last_gap, and
no_gain_streak in pieces.json. Two consecutive wins set the piece status to
converged.

Exit codes: 0 accepted and recorded, 1 rejected or validation failure,
2 usage error.
"""

import argparse
import json
import os
import sys

WINNER_SET = {"A", "B"}
CONFIDENCE_SET = {"low", "medium", "high"}
CONTEXT_SOURCE_REQUIRED = "files-only"

# field name -> (accepted types, allow None)
SCHEMA = {
    "piece_id": (str, False),
    "round": (int, False),
    "blind": (bool, False),
    "seed": (int, True),
    "winner": (str, False),
    "winner_is_ours": (bool, False),
    "confidence": (str, False),
    "reasoning": (str, False),
    "largest_gap": (str, False),
    "gap_is_actionable": (bool, False),
    "inspection_evidence": (list, False),
    "rubric_hash": (str, True),
    "critic_saw_builder_context": (bool, False),
    "critic_context_source": (str, False),
}


def reject(errors):
    print(json.dumps({"accepted": False, "errors": errors}, indent=2))
    sys.exit(1)


def atomic_write_json(path, payload):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
        handle.write("\n")
    os.replace(tmp, path)


def type_ok(value, expected, allow_none):
    if value is None:
        return allow_none
    if expected is int and isinstance(value, bool):
        return False
    if expected is bool:
        return isinstance(value, bool)
    return isinstance(value, expected)


def validate(verdict, piece, round_number):
    errors = []
    if not isinstance(verdict, dict):
        return ["verdict must be a JSON object"]

    for field, (expected, allow_none) in SCHEMA.items():
        if field not in verdict:
            errors.append("missing field: {0}".format(field))
            continue
        if not type_ok(verdict[field], expected, allow_none):
            errors.append("field {0} has the wrong type".format(field))
    for field in verdict:
        if field not in SCHEMA:
            errors.append("unknown field: {0}".format(field))
    if errors:
        return errors

    if verdict["piece_id"] != piece:
        errors.append("piece_id {0!r} does not match --piece {1!r}".format(
            verdict["piece_id"], piece))
    if verdict["round"] != round_number:
        errors.append("round {0} does not match --round {1}".format(
            verdict["round"], round_number))
    if verdict["winner"] not in WINNER_SET:
        errors.append("winner {0!r} not in closed set {1}".format(
            verdict["winner"], sorted(WINNER_SET)))
    if verdict["confidence"] not in CONFIDENCE_SET:
        errors.append("confidence {0!r} not in closed set {1}".format(
            verdict["confidence"], sorted(CONFIDENCE_SET)))
    evidence = verdict["inspection_evidence"]
    if not evidence or not all(
            isinstance(e, str) and e.strip() for e in evidence):
        errors.append("inspection_evidence must be a non-empty list of "
                      "non-empty paths; a verdict without inspection "
                      "evidence violates INV-5")

    # INV-2 enforcement. These three rejections are the point of this script.
    if verdict["critic_saw_builder_context"] is True:
        errors.append("REJECTED: critic_saw_builder_context is true; the "
                      "builder never grades itself and the critic must run "
                      "in fresh context (INV-2)")
    if verdict["critic_context_source"] != CONTEXT_SOURCE_REQUIRED:
        errors.append("REJECTED: critic_context_source is {0!r}; only "
                      "{1!r} is valid (INV-2)".format(
                          verdict["critic_context_source"],
                          CONTEXT_SOURCE_REQUIRED))
    if not verdict["largest_gap"].strip():
        errors.append("REJECTED: largest_gap is empty; every verdict names "
                      "exactly one actionable gap")
    return errors


def update_piece(piece_entry, verdict, round_number):
    """Apply the round outcome to the piece record. Returns the entry."""
    rounds_completed = piece_entry.get("rounds_completed")
    if not isinstance(rounds_completed, int) or isinstance(rounds_completed, bool):
        rounds_completed = 0
    piece_entry["rounds_completed"] = max(rounds_completed, round_number)

    wins = piece_entry.get("consecutive_wins")
    if not isinstance(wins, int) or isinstance(wins, bool):
        wins = 0
    streak = piece_entry.get("no_gain_streak")
    if not isinstance(streak, int) or isinstance(streak, bool):
        streak = 0

    if verdict["winner_is_ours"]:
        piece_entry["consecutive_wins"] = wins + 1
        piece_entry["no_gain_streak"] = 0
    else:
        previous_gap = piece_entry.get("last_gap")
        same_gap = (isinstance(previous_gap, str)
                    and previous_gap.strip() == verdict["largest_gap"].strip())
        piece_entry["consecutive_wins"] = 0
        piece_entry["no_gain_streak"] = streak + 1 if same_gap else 0
        piece_entry["last_gap"] = verdict["largest_gap"]

    if piece_entry["consecutive_wins"] >= 2:
        piece_entry["status"] = "converged"
    return piece_entry


def main():
    parser = argparse.ArgumentParser(
        description="Validate a critic verdict, reject fresh-context "
                    "violations, and atomically record the round.")
    parser.add_argument("--run-dir", required=True,
                        help="Path to .gauntlet/runs/<run-id>")
    parser.add_argument("--piece", required=True, help="Piece id")
    parser.add_argument("--round", required=True, type=int,
                        help="Round number, 1-based")
    parser.add_argument("--verdict", required=True,
                        help="Path to the verdict.json to validate and record")
    args = parser.parse_args()

    if args.round < 1:
        parser.error("--round must be 1 or greater")

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        reject(["run directory not found: {0}".format(run_dir)])

    try:
        with open(args.verdict, "r", encoding="utf-8") as handle:
            verdict = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        reject(["unreadable verdict {0}: {1}".format(args.verdict, exc)])

    errors = validate(verdict, args.piece, args.round)
    if errors:
        reject(errors)

    pieces_path = os.path.join(run_dir, "pieces.json")
    try:
        with open(pieces_path, "r", encoding="utf-8") as handle:
            pieces_data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        reject(["unreadable pieces.json: {0}".format(exc)])
    entries = pieces_data.get("pieces")
    if not isinstance(entries, list):
        reject(["pieces.json has no pieces list"])
    piece_entry = None
    for entry in entries:
        if isinstance(entry, dict) and entry.get("id") == args.piece:
            piece_entry = entry
            break
    if piece_entry is None:
        reject(["piece {0!r} not found in pieces.json".format(args.piece)])

    round_dir = os.path.join(
        run_dir, "rounds", args.piece, "{0:03d}".format(args.round))
    os.makedirs(round_dir, exist_ok=True)
    verdict_path = os.path.join(round_dir, "verdict.json")
    atomic_write_json(verdict_path, verdict)

    update_piece(piece_entry, verdict, args.round)
    atomic_write_json(pieces_path, pieces_data)

    print(json.dumps({
        "accepted": True,
        "piece_id": args.piece,
        "round": args.round,
        "verdict_path": verdict_path,
        "rounds_completed": piece_entry["rounds_completed"],
        "consecutive_wins": piece_entry["consecutive_wins"],
        "no_gain_streak": piece_entry["no_gain_streak"],
        "last_gap": piece_entry.get("last_gap"),
        "status": piece_entry.get("status"),
    }, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
