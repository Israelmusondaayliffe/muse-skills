#!/usr/bin/env python3
"""Generate sessions/<n>/HANDOFF.md from state (SPEC 9.7, INV-6).

Twelve sections, in this exact order:
1. Run identity and location, 2. How to read state, 3. Wave and lane status,
4. Converged and verified pieces, 5. In flight, 6. Capped or blocked,
7. Decisions already made, 8. Do-not-redo list, 9. First three actions,
10. How to verify this document, 11. Surface notes,
12. Budget spent and remaining.

Every generated statement comes from state files: run.json, pieces.json,
lanes.json, sessions/sessions.json, cost.json, verification/*/consensus.json,
bar/bar.md, CONTEXT.md, and rounds/*/*/gap.md. The script appends nothing
beyond the twelve sections. The departing agent may later append, by hand,
exactly one section titled "## Judgment notes (unverified)" and nothing more.
Output is plain portable markdown with absolute paths and no tool-specific
syntax; section 10 carries the verification commands.

Also updates the sessions.json exit record for the given session index:
sets "exited" and "handoff", plus any of --exit-reason, --rounds,
--subagents that were passed.

Exit codes: 0 on success, 1 when run.json is missing or state is invalid,
2 on usage errors.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

NOT_RECORDED = "not recorded"


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        print("Invalid JSON in %s: %s" % (path, exc), file=sys.stderr)
        raise SystemExit(1)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def last_gap_text(run_dir, piece_id):
    piece_dir = run_dir / "rounds" / piece_id
    if not piece_dir.is_dir():
        return None
    newest = None
    for round_dir in sorted(piece_dir.iterdir()):
        gap = round_dir / "gap.md"
        if gap.is_file():
            newest = gap
    if newest is None:
        return None
    return newest.read_text(encoding="utf-8").strip()


def piece_gap(run_dir, piece):
    """Last gap for a piece: pieces.json last_gap first, then gap.md on disk."""
    gap = piece.get("last_gap")
    if gap:
        return gap
    gap = last_gap_text(run_dir, piece.get("id") or "")
    return gap if gap else NOT_RECORDED


def remaining(cap, spent):
    if isinstance(cap, (int, float)) and isinstance(spent, (int, float)):
        return cap - spent
    return NOT_RECORDED


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate sessions/<n>/HANDOFF.md from state and update "
        "the sessions.json exit record."
    )
    parser.add_argument(
        "--run-dir", required=True, help="Path to .gauntlet/runs/<run-id>."
    )
    parser.add_argument(
        "--session", required=True, type=int, help="Session index for the handoff."
    )
    parser.add_argument("--exit-reason", default=None, help="Exit reason to record.")
    parser.add_argument(
        "--rounds", default=None, type=int, help="Rounds completed this session."
    )
    parser.add_argument(
        "--subagents", default=None, type=int, help="Subagents spawned this session."
    )
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).resolve()
    run = load_json(run_dir / "run.json")
    if run is None:
        print("Missing required state file: %s" % (run_dir / "run.json"), file=sys.stderr)
        return 1

    pieces_doc = load_json(run_dir / "pieces.json") or {}
    pieces = pieces_doc.get("pieces") or []
    lanes_doc = load_json(run_dir / "lanes.json") or {}
    lanes = lanes_doc.get("lanes") or []
    cost = load_json(run_dir / "cost.json") or {}
    budgets = run.get("budgets") or {}

    consensus = {}
    verification_dir = run_dir / "verification"
    if verification_dir.is_dir():
        for piece_dir in sorted(verification_dir.iterdir()):
            if piece_dir.is_dir():
                doc = load_json(piece_dir / "consensus.json")
                if doc is not None:
                    consensus[piece_dir.name] = doc

    # Update the sessions.json exit record before generating, so the handoff
    # reflects the record it describes.
    sessions_path = run_dir / "sessions" / "sessions.json"
    sessions_doc = load_json(sessions_path) or {"sessions": []}
    sessions = sessions_doc.setdefault("sessions", [])
    entry = next((s for s in sessions if s.get("index") == args.session), None)
    if entry is None:
        entry = {
            "index": args.session,
            "surface": None,
            "model": None,
            "effort": None,
            "lane": None,
            "entered": None,
        }
        sessions.append(entry)
    entry["exited"] = now_iso()
    if args.exit_reason is not None:
        entry["exit_reason"] = args.exit_reason
    if args.rounds is not None:
        entry["rounds_completed"] = args.rounds
    if args.subagents is not None:
        entry["subagents_spawned"] = args.subagents
    entry["handoff"] = "sessions/%d/HANDOFF.md" % args.session
    sessions_path.parent.mkdir(parents=True, exist_ok=True)
    sessions_path.write_text(
        json.dumps(sessions_doc, indent=2) + "\n", encoding="utf-8"
    )

    def val(value):
        return value if value not in (None, "") else NOT_RECORDED

    run_id = val(run.get("run_id"))
    goal = val(run.get("goal_one_line"))
    bar_file = run_dir / "bar" / "bar.md"
    bar_line = NOT_RECORDED
    if bar_file.is_file():
        bar_lines = [
            l.strip()
            for l in bar_file.read_text(encoding="utf-8").splitlines()
            if l.strip()
        ]
        if bar_lines:
            bar_line = bar_lines[0]

    md = []
    md.append("# HANDOFF: %s, session %d" % (run_id, args.session))
    md.append("")

    # 1
    md.append("## 1. Run identity and location")
    md.append("")
    md.append("- Run ID: %s" % run_id)
    md.append("- Goal: %s" % goal)
    md.append("- Bar: %s" % bar_line)
    md.append("- Run directory: %s" % run_dir)
    md.append("")

    # 2
    md.append("## 2. How to read state")
    md.append("")
    md.append("Read in this order. State on disk is the truth; this document is a reading aid.")
    md.append("")
    md.append("1. %s (canonical, append-only; always first)" % (run_dir / "CONTEXT.md"))
    md.append("2. This handoff")
    md.append("3. %s (status, shape, budgets, precheck)" % (run_dir / "run.json"))
    md.append("4. %s (current wave plan)" % (run_dir / "PLAN.md"))
    md.append("5. %s (piece status and gaps)" % (run_dir / "pieces.json"))
    md.append("6. %s (lane ownership and locks)" % (run_dir / "lanes.json"))
    md.append("7. %s (session history)" % (run_dir / "sessions" / "sessions.json"))
    md.append("")
    md.append(
        "Before claiming a lane, check %s for a stale holder: a heartbeat older "
        "than two hours or a holder session marked exited." % (run_dir / "run.lock")
    )
    md.append("")

    # 3
    md.append("## 3. Wave and lane status")
    md.append("")
    md.append(
        "Current wave: %s (wave cap %s)"
        % (val(run.get("current_wave")), val(budgets.get("wave_cap")))
    )
    md.append("")
    if lanes:
        md.append("| Lane | Status | Owned pieces | Owned paths | Lock holder | Heartbeat |")
        md.append("|---|---|---|---|---|---|")
        for lane in lanes:
            md.append(
                "| %s | %s | %s | %s | %s | %s |"
                % (
                    val(lane.get("id")),
                    val(lane.get("status")),
                    ", ".join(lane.get("owned_pieces") or []) or NOT_RECORDED,
                    ", ".join(lane.get("owned_paths") or []) or NOT_RECORDED,
                    val(lane.get("lock_holder")),
                    val(lane.get("heartbeat")),
                )
            )
    else:
        md.append("No lanes recorded in lanes.json.")
    md.append("")

    # 4
    md.append("## 4. Converged and verified pieces")
    md.append("")
    done_rows = []
    for piece in pieces:
        pid = piece.get("id") or NOT_RECORDED
        cdoc = consensus.get(pid)
        if piece.get("status") == "converged" or cdoc is not None:
            done_rows.append(
                "| %s | %s | %s |"
                % (
                    pid,
                    val(piece.get("status")),
                    cdoc.get("consensus") if cdoc else "not yet verified",
                )
            )
    if done_rows:
        md.append("| Piece | Loop status | Consensus |")
        md.append("|---|---|---|")
        md += done_rows
    else:
        md.append("None yet.")
    md.append("")

    # 5
    md.append("## 5. In flight")
    md.append("")
    in_flight = [p for p in pieces if p.get("status") in ("pending", "looping")]
    if in_flight:
        by_lane = {}
        for piece in in_flight:
            by_lane.setdefault(piece.get("lane") or NOT_RECORDED, []).append(piece)
        for lane_id in sorted(by_lane, key=str):
            md.append("### Lane %s" % lane_id)
            md.append("")
            for piece in by_lane[lane_id]:
                md.append(
                    "- %s (status %s, rounds %s of cap %s)"
                    % (
                        piece.get("id") or NOT_RECORDED,
                        val(piece.get("status")),
                        val(piece.get("rounds_completed")),
                        val(piece.get("rounds_cap")),
                    )
                )
                md.append("  Last gap, verbatim: %s" % piece_gap(run_dir, piece))
            md.append("")
    else:
        md.append("No pieces in flight.")
        md.append("")

    # 6
    md.append("## 6. Capped or blocked")
    md.append("")
    stuck = [p for p in pieces if p.get("status") in ("capped", "blocked", "dropped")]
    if stuck:
        for piece in stuck:
            md.append(
                "- %s: status %s. Why: %s. Caps pause, they do not certify (a capped piece is never done)."
                % (
                    piece.get("id") or NOT_RECORDED,
                    piece.get("status"),
                    piece_gap(run_dir, piece),
                )
            )
    else:
        md.append("None.")
    md.append("")

    # 7
    md.append("## 7. Decisions already made")
    md.append("")
    md.append(
        "Decisions live in %s, which is append-only. Do not reopen anything "
        "recorded there; corrections are appended with a date and a reason."
        % (run_dir / "CONTEXT.md")
    )
    md.append("")
    decisions = []
    context_file = run_dir / "CONTEXT.md"
    if context_file.is_file():
        for number, line in enumerate(
            context_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            stripped = line.strip().lstrip("-*#").strip()
            if stripped.lower().startswith("decision"):
                decisions.append((number, stripped))
    if decisions:
        for number, text in decisions:
            md.append('- "%s" (recorded at %s, line %d)' % (text, context_file, number))
    else:
        md.append(
            "- No structured decision lines found. Read %s in full; anything "
            "recorded there stands." % context_file
        )
    md.append("")

    # 8
    md.append("## 8. Do-not-redo list")
    md.append("")
    converged_ids = [p.get("id") for p in pieces if p.get("status") == "converged"]
    md.append(
        "- Do not rebuild converged pieces: %s."
        % (", ".join(converged_ids) if converged_ids else "none yet")
    )
    md.append(
        "- Do not re-run recorded rounds; snapshots and inspection evidence live under %s."
        % (run_dir / "rounds")
    )
    md.append(
        "- Do not re-run verification for pieces that already have a consensus.json "
        "under %s, unless their artifacts changed." % (run_dir / "verification")
    )
    md.append("- Do not rewrite CONTEXT.md history; it is append-only.")
    md.append("")

    # 9
    md.append("## 9. First three actions")
    md.append("")
    if in_flight:
        third = (
            "Resume the round loop on the in-flight pieces: %s."
            % ", ".join(p.get("id") or NOT_RECORDED for p in in_flight)
        )
    elif pieces and all(p.get("id") in consensus for p in pieces if p.get("id")):
        third = "Consensus exists for every piece; build or refresh the evidence report."
    elif pieces:
        third = (
            "No pieces are in flight and verification is incomplete; run "
            "independent verification on the stopped pieces."
        )
    else:
        third = (
            "pieces.json has no pieces; read %s and decompose the goal into "
            "independently judgeable pieces." % (run_dir / "PLAN.md")
        )
    md.append("1. Read %s end to end, then the state files in section 2 order." % context_file)
    md.append(
        "2. Check %s for a stale holder, then claim a lane: update lanes.json "
        "and add your entry to %s."
        % (run_dir / "run.lock", run_dir / "sessions" / "sessions.json")
    )
    md.append("3. %s" % third)
    md.append("")

    # 10
    md.append("## 10. How to verify this document")
    md.append("")
    md.append(
        "Every generated statement above comes from state files. Verify any of "
        "them with these commands:"
    )
    md.append("")
    md.append("    python3 -m json.tool \"%s\"" % (run_dir / "run.json"))
    md.append("    python3 -m json.tool \"%s\"" % (run_dir / "pieces.json"))
    md.append("    python3 -m json.tool \"%s\"" % (run_dir / "lanes.json"))
    md.append("    python3 -m json.tool \"%s\"" % (run_dir / "sessions" / "sessions.json"))
    md.append("    ls \"%s\"" % (run_dir / "rounds"))
    md.append("    ls \"%s\"" % (run_dir / "verification"))
    md.append("")
    md.append(
        "Any gap quoted above is verbatim from pieces.json last_gap or from the "
        "newest gap.md under %s/<piece>/<round>/." % (run_dir / "rounds")
    )
    md.append("")

    # 11
    md.append("## 11. Surface notes")
    md.append("")
    md.append("- Platform: %s" % val(entry.get("surface")))
    md.append("- Model: %s" % val(entry.get("model")))
    md.append("- Effort: %s" % val(entry.get("effort")))
    md.append("- Lane held: %s" % val(entry.get("lane")))
    precheck = run.get("precheck")
    md.append(
        "- Precheck recorded in run.json: %s"
        % (json.dumps(precheck) if precheck else NOT_RECORDED)
    )
    md.append("- Context isolation this run: %s" % val(run.get("context_isolation")))
    if run.get("context_isolation") not in (None, "clean"):
        md.append(
            "- DEGRADED MODE: context isolation on this run was weaker than a "
            "clean context window. Every report from this run must carry this banner."
        )
    md.append(
        "- The next agent may lack: this session's conversation history (by "
        "design; state is the truth), the same subagent isolation (run "
        "precheck.py on entry and record the result), and the same connectors "
        "or tools. If the new surface prechecks weaker, continue degraded with "
        "the banner or wait; never silently proceed at lower isolation."
    )
    md.append("")

    # 12
    md.append("## 12. Budget spent and remaining")
    md.append("")
    rounds_spent = [p.get("rounds_completed") for p in pieces
                    if isinstance(p.get("rounds_completed"), (int, float))]
    max_rounds = max(rounds_spent) if rounds_spent else 0
    rounds_cap = budgets.get("rounds_cap_per_piece")
    wave_cap = budgets.get("wave_cap")
    current_wave = run.get("current_wave")
    subagent_cap = budgets.get("subagent_cap_per_run")
    subagents_total = cost.get("subagents_total")
    md.append("| Budget | Cap | Spent | Remaining |")
    md.append("|---|---|---|---|")
    md.append(
        "| Rounds per piece | %s | max recorded: %s | %s |"
        % (val(rounds_cap), max_rounds, remaining(rounds_cap, max_rounds))
    )
    md.append(
        "| Waves | %s | current wave: %s | %s |"
        % (val(wave_cap), val(current_wave), remaining(wave_cap, current_wave))
    )
    md.append(
        "| Subagents per run | %s | %s | %s |"
        % (
            val(subagent_cap),
            val(subagents_total),
            remaining(subagent_cap, subagents_total),
        )
    )
    md.append(
        "| Wall clock hours per session | %s | total across sessions: %s | see cap per session |"
        % (val(budgets.get("wall_clock_hours_per_session")), val(cost.get("wall_clock_hours")))
    )
    md.append(
        "| Cost ceiling | %s | tokens: %s | %s |"
        % (
            val(budgets.get("cost_ceiling")),
            val(cost.get("tokens")),
            "not computable" if cost.get("tokens") in (None, "unknown") else "see ledger",
        )
    )
    md.append("")
    md.append("- Rounds recorded in cost ledger: %s" % val(cost.get("rounds_total")))
    md.append("- Sessions recorded: %s" % val(cost.get("sessions_total")))
    md.append("- Stop reason: %s" % (run.get("stop_reason") or "none"))
    md.append("")

    handoff_dir = run_dir / "sessions" / str(args.session)
    handoff_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = handoff_dir / "HANDOFF.md"
    handoff_path.write_text("\n".join(md), encoding="utf-8")

    print(
        json.dumps(
            {
                "result": "written",
                "handoff": str(handoff_path),
                "session": args.session,
                "sessions_json_updated": True,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
