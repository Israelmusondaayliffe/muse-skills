#!/usr/bin/env python3
"""Evaluate every gauntlet stop condition for a run. First to fire wins.

Order, per SPEC 11.4:
  1. User stop           presence of a file named STOP in the run directory
  2. Piece converged     2 consecutive blind wins on a looping piece
  3. All pieces converged
  4. Round cap per piece rounds_completed >= rounds_cap (default 10)
  5. No-gain rule        same largest gap twice with no win (no_gain_streak >= 2):
                         escalate to lead for re-split, stop looping the piece
  6. Wave cap            current_wave exceeds wave_cap (default 4)
  7. Wall clock          open session elapsed >= wall_clock_hours_per_session (default 6)
  8. Subagent cap        subagents_total >= subagent_cap_per_run (default 400)
  9. Cost ceiling        cost_spent >= numeric cost_ceiling, when both are numeric

Caps set `capped` or `paused`. They never set `converged` or `done` (INV-7).
Prints JSON {fired, condition, scope, action} on stdout and updates
run.json / pieces.json statuses on disk when a condition fires.

Exit codes: 0 evaluated (fired or not), 1 validation failure, 2 usage error.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_BUDGETS = {
    "rounds_cap_per_piece": 10,
    "wave_cap": 4,
    "wall_clock_hours_per_session": 6,
    "subagent_cap_per_run": 400,
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")
    os.replace(tmp, path)


def parse_ts(value):
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def as_number(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def as_int(value, default):
    number = as_number(value)
    if number is None:
        return default
    return int(number)


def fail(message):
    print(json.dumps({"fired": False, "error": message}))
    return 1


def emit(fired, condition=None, scope=None, action="continue"):
    print(json.dumps({
        "fired": fired,
        "condition": condition,
        "scope": scope,
        "action": action,
    }))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Evaluate gauntlet stop conditions in SPEC 11.4 order; first to fire wins.")
    parser.add_argument("--run-dir", required=True,
                        help="Path to .gauntlet/runs/<run-id>")
    args = parser.parse_args(argv)

    run_dir = os.path.abspath(args.run_dir)
    run_path = os.path.join(run_dir, "run.json")
    pieces_path = os.path.join(run_dir, "pieces.json")

    if not os.path.isdir(run_dir):
        return fail("run directory not found: %s" % run_dir)
    if not os.path.isfile(run_path):
        return fail("run.json not found in %s" % run_dir)
    try:
        run = load_json(run_path)
    except (ValueError, OSError) as exc:
        return fail("could not read run.json: %s" % exc)

    pieces_doc = {"pieces": []}
    if os.path.isfile(pieces_path):
        try:
            pieces_doc = load_json(pieces_path)
        except (ValueError, OSError) as exc:
            return fail("could not read pieces.json: %s" % exc)
    pieces = pieces_doc.get("pieces") or []

    budgets = dict(DEFAULT_BUDGETS)
    budgets.update(run.get("budgets") or {})
    now = datetime.now(timezone.utc)

    # 1. User stop flag.
    if os.path.exists(os.path.join(run_dir, "STOP")):
        run["status"] = "stopped"
        run["stop_reason"] = "user-stop"
        save_json(run_path, run)
        return emit(True, "user-stop", "run",
                    "stop the run; state intact and resumable")

    # 2. Piece converged: 2 consecutive blind wins.
    for piece in pieces:
        if piece.get("status") == "looping" and as_int(piece.get("consecutive_wins"), 0) >= 2:
            piece["status"] = "converged"
            save_json(pieces_path, pieces_doc)
            return emit(True, "piece-converged", piece.get("id"),
                        "mark the piece converged; stop looping it")

    # 3. All pieces converged (dropped pieces do not block convergence).
    active = [p for p in pieces if p.get("status") != "dropped"]
    if active and all(p.get("status") == "converged" for p in active):
        run["status"] = "converged"
        run["stop_reason"] = "all-pieces-converged"
        save_json(run_path, run)
        return emit(True, "all-pieces-converged", "run",
                    "run converged; route to gauntlet-verify")

    # 4. Round cap per piece. Capped, never converged or done (INV-7).
    for piece in pieces:
        if piece.get("status") != "looping":
            continue
        cap = as_int(piece.get("rounds_cap"), as_int(budgets.get("rounds_cap_per_piece"), 10))
        if as_int(piece.get("rounds_completed"), 0) >= cap:
            piece["status"] = "capped"
            save_json(pieces_path, pieces_doc)
            return emit(True, "round-cap", piece.get("id"),
                        "piece capped at the round cap; last gap preserved; capped is not done")

    # 5. No-gain rule: same largest gap twice with no win. round_record.py sets
    # no_gain_streak to the number of consecutive repeats, so a streak of 1
    # means the identical gap has now appeared in two consecutive rounds.
    for piece in pieces:
        if piece.get("status") != "looping":
            continue
        if as_int(piece.get("no_gain_streak"), 0) >= 1:
            piece["status"] = "blocked"
            save_json(pieces_path, pieces_doc)
            return emit(True, "no-gain", piece.get("id"),
                        "escalate to the lead for a re-split; stop looping this piece")

    # 6. Wave cap: fires when the run would enter a wave beyond the cap.
    wave_cap = as_int(budgets.get("wave_cap"), 4)
    current_wave = as_int(run.get("current_wave"), 1)
    if current_wave > wave_cap:
        run["status"] = "paused"
        run["stop_reason"] = "wave-cap"
        save_json(run_path, run)
        return emit(True, "wave-cap", "run",
                    "pause at the wave boundary; wave cap reached; paused is not done")

    # 7. Wall clock per session, measured from the open sessions.json entry.
    wall_limit = as_number(budgets.get("wall_clock_hours_per_session"))
    if wall_limit is None:
        wall_limit = float(DEFAULT_BUDGETS["wall_clock_hours_per_session"])
    sessions_path = os.path.join(run_dir, "sessions", "sessions.json")
    open_session = None
    if os.path.isfile(sessions_path):
        try:
            sessions = (load_json(sessions_path).get("sessions") or [])
        except (ValueError, OSError):
            sessions = []
        for session in reversed(sessions):
            if not session.get("exited"):
                open_session = session
                break
    if open_session is not None:
        entered = parse_ts(open_session.get("entered"))
        if entered is not None:
            elapsed_hours = (now - entered).total_seconds() / 3600.0
            if elapsed_hours >= wall_limit:
                run["status"] = "paused"
                run["stop_reason"] = "wall-clock"
                save_json(run_path, run)
                scope = "session-%s" % open_session.get("index", "unknown")
                return emit(True, "wall-clock", scope,
                            "pause the session; release the lane lock and write the handoff")

    # 8. Subagent cap per run.
    cost = {}
    cost_path = os.path.join(run_dir, "cost.json")
    if os.path.isfile(cost_path):
        try:
            cost = load_json(cost_path)
        except (ValueError, OSError):
            cost = {}
    subagent_cap = as_int(budgets.get("subagent_cap_per_run"), 400)
    subagents_total = as_number(cost.get("subagents_total"))
    if subagents_total is not None and subagents_total >= subagent_cap:
        run["status"] = "paused"
        run["stop_reason"] = "subagent-cap"
        save_json(run_path, run)
        return emit(True, "subagent-cap", "run",
                    "pause the run; subagent cap reached; paused is not done")

    # 9. Cost ceiling: fires only when both ceiling and spend are numeric.
    ceiling = as_number(budgets.get("cost_ceiling"))
    spent = as_number(cost.get("cost_spent"))
    if ceiling is not None and spent is not None and spent >= ceiling:
        run["status"] = "paused"
        run["stop_reason"] = "cost-ceiling"
        save_json(run_path, run)
        return emit(True, "cost-ceiling", "run",
                    "pause the run; cost ceiling reached; paused is not done")

    return emit(False)


if __name__ == "__main__":
    sys.exit(main())
