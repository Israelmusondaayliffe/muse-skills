#!/usr/bin/env python3
"""Assemble EVIDENCE.md and EVIDENCE.json for a gauntlet run (SPEC 9.6).

Nine sections, in this exact order:
1. Verdict, 2. Goal and bar, 3. Per-piece table, 4. Re-run the checks,
5. Claim audit summary, 6. Artifact integrity, 7. What was not verified,
8. Known remaining gaps, 9. Budget spent.

Every value is read from state files under the run directory: run.json,
pieces.json, verification/*/consensus.json, claims/*/audit.json,
artifact-hashes.json, cost.json, rounds/*/*/gap.md, and bar/bar.md. This
script never estimates. It computes only the deterministic run-level rollup
of per-piece consensus values (any failed -> failed; any missing or
unverifiable -> unverifiable; any dissent -> verified-with-dissent;
otherwise verified). Any missing value prints "not recorded" and is itself
listed in section 7 "What was not verified".

Refuses (exit 1) when no consensus.json exists for any piece, because
verification has not run and the router must go to gauntlet-verify first.
It does build for failed or unverifiable consensus, verdict verbatim, no
softening, no upgrading. When run.json context_isolation is anything other
than "clean", section 1 carries a degraded-mode banner.

Exit codes: 0 on success, 1 on refusal or missing run.json/invalid state,
2 on usage errors.
"""

import argparse
import json
import sys
from pathlib import Path

KNOWLEDGE_DOMAINS = {"prose", "research", "strategy", "deck", "prompt-system"}
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


def fmt_votes(votes):
    if not isinstance(votes, dict):
        return None
    return "pass %s, fail %s, cannot-verify %s" % (
        votes.get("pass", 0),
        votes.get("fail", 0),
        votes.get("cannot-verify", 0),
    )


def last_gap_text(run_dir, piece_id):
    """Return the newest rounds/<piece>/<round>/gap.md text, or None."""
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


def overall_verdict(values):
    """Deterministic rollup of per-piece consensus values. None = missing."""
    if any(v == "failed" for v in values):
        return "failed"
    if any(v is None or v == "unverifiable" for v in values):
        return "unverifiable"
    if any(v == "verified-with-dissent" for v in values):
        return "verified-with-dissent"
    if values and all(v == "verified" for v in values):
        return "verified"
    return "unverifiable"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Assemble EVIDENCE.md and EVIDENCE.json from state files."
    )
    parser.add_argument(
        "--run-dir", required=True, help="Path to .gauntlet/runs/<run-id>."
    )
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).resolve()
    run = load_json(run_dir / "run.json")
    if run is None:
        print("Missing required state file: %s" % (run_dir / "run.json"), file=sys.stderr)
        return 1

    pieces_doc = load_json(run_dir / "pieces.json") or {}
    pieces = pieces_doc.get("pieces") or []

    consensus = {}
    verification_dir = run_dir / "verification"
    if verification_dir.is_dir():
        for piece_dir in sorted(verification_dir.iterdir()):
            if not piece_dir.is_dir():
                continue
            doc = load_json(piece_dir / "consensus.json")
            if doc is not None:
                consensus[piece_dir.name] = doc

    if not consensus:
        print(
            json.dumps(
                {
                    "result": "refused",
                    "reason": "verification-not-run",
                    "detail": "No consensus.json exists for any piece. "
                    "Run gauntlet-verify before building the report.",
                }
            )
        )
        print(
            "Refusing to build the report: verification has not run "
            "(no verification/*/consensus.json found). Run gauntlet-verify first.",
            file=sys.stderr,
        )
        return 1

    not_recorded = []

    def nr(section, what):
        not_recorded.append("section %s: %s" % (section, what))
        return NOT_RECORDED

    piece_ids = [p.get("id") for p in pieces if p.get("id")] or sorted(consensus)
    verdict = overall_verdict([
        (consensus.get(pid) or {}).get("consensus") if pid in consensus else None
        for pid in piece_ids
    ])

    # Section 1: Verdict, with the degraded banner when isolation was not clean.
    isolation = run.get("context_isolation")
    if isolation is None and "context_isolation" not in run:
        isolation = nr("1 (Verdict)", "run.json: context_isolation")
    banner = None
    if isolation != "clean":
        banner = (
            "DEGRADED MODE: run.json records context_isolation = \"%s\". "
            "Judge and verifier isolation on this run was weaker than a clean "
            "context window. Read every verdict in that light." % isolation
        )
    sec1_lines = [str(verdict)]
    if banner:
        sec1_lines += ["", banner]

    # Section 2: Goal and bar.
    goal = run.get("goal_one_line") or nr("2 (Goal and bar)", "run.json: goal_one_line")
    bar_file = run_dir / "bar" / "bar.md"
    if bar_file.is_file():
        bar_lines = [l.strip() for l in bar_file.read_text(encoding="utf-8").splitlines() if l.strip()]
        bar_line = bar_lines[0] if bar_lines else nr("2 (Goal and bar)", "bar/bar.md is empty")
    else:
        bar_line = nr("2 (Goal and bar)", "bar/bar.md")
    plan_hash = run.get("plan_hash") or nr("2 (Goal and bar)", "run.json: plan_hash")
    known_matches = [
        c.get("plan_hash_matched")
        for c in consensus.values()
        if c.get("plan_hash_matched") is not None
    ]
    if not known_matches:
        hash_matched = nr("2 (Goal and bar)", "plan_hash_matched from consensus.json")
    elif all(known_matches):
        hash_matched = "matched for every piece with a consensus"
    else:
        hash_matched = "MISMATCH reported by at least one consensus (integrity failure)"
    sec2_lines = [
        "- Goal: %s" % goal,
        "- Bar: %s" % bar_line,
        "- Bar detail and rationale: %s" % (
            str(bar_file) if bar_file.is_file() else NOT_RECORDED
        ),
        "- Plan hash: %s" % plan_hash,
        "- Plan hash matched at verification: %s" % hash_matched,
    ]

    # Section 3: Per-piece table.
    sec3_rows = []
    piece_json = []
    for piece in pieces:
        pid = piece.get("id") or NOT_RECORDED
        rounds = piece.get("rounds_completed")
        if rounds is None:
            rounds = nr("3 (Per-piece table)", "rounds_completed for piece %s" % pid)
        status = piece.get("status")
        wins = piece.get("consecutive_wins")
        if status is None:
            blind = nr("3 (Per-piece table)", "status for piece %s" % pid)
        elif status == "converged":
            blind = "won (%s consecutive blind wins)" % (
                wins if wins is not None else NOT_RECORDED
            )
        else:
            blind = "%s, consecutive wins %s" % (
                status, wins if wins is not None else NOT_RECORDED
            )
        cdoc = consensus.get(pid)
        if cdoc is None:
            quality = nr("3 (Per-piece table)", "quality votes for piece %s (no consensus.json)" % pid)
            integrity = NOT_RECORDED
            cons_value = NOT_RECORDED
        else:
            quality = fmt_votes(cdoc.get("quality_votes")) or nr(
                "3 (Per-piece table)", "quality_votes for piece %s" % pid
            )
            integrity = fmt_votes(cdoc.get("integrity_votes")) or nr(
                "3 (Per-piece table)", "integrity_votes for piece %s" % pid
            )
            cons_value = cdoc.get("consensus") or nr(
                "3 (Per-piece table)", "consensus value for piece %s" % pid
            )
        paths = ", ".join(piece.get("artifact_paths") or []) or nr(
            "3 (Per-piece table)", "artifact_paths for piece %s" % pid
        )
        sec3_rows.append(
            "| %s | %s | %s | %s | %s | %s | %s |"
            % (pid, rounds, blind, quality, integrity, cons_value, paths)
        )
        piece_json.append(
            {
                "piece_id": pid,
                "rounds": rounds,
                "final_blind_result": blind,
                "quality_votes": quality,
                "integrity_votes": integrity,
                "consensus": cons_value,
                "artifact_paths": paths,
            }
        )
    if not sec3_rows:
        nr("3 (Per-piece table)", "pieces.json has no pieces")

    # Section 4: Re-run the checks. Exit codes are read from the newest
    # rounds/<piece>/<nnn>/inspection/results.json entry whose command matches;
    # gauntlet-run records {"command", "exit_code", "ran_at"} rows there at
    # inspection time. Anything unrecorded prints "not recorded".
    def recorded_exit_code(pid, command):
        rounds_dir = run_dir / "rounds" / str(pid)
        if not rounds_dir.is_dir():
            return None
        for round_dir in sorted(rounds_dir.iterdir(), reverse=True):
            results_path = round_dir / "inspection" / "results.json"
            if not results_path.is_file():
                continue
            try:
                rows = json.loads(results_path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                continue
            if isinstance(rows, dict):
                rows = rows.get("results", [])
            for row in rows if isinstance(rows, list) else []:
                if isinstance(row, dict) and row.get("command") == command \
                        and isinstance(row.get("exit_code"), int):
                    return row["exit_code"]
        return None

    checks = []
    for piece in pieces:
        pid = piece.get("id") or NOT_RECORDED
        for inspection in piece.get("inspection") or []:
            method = inspection.get("method", NOT_RECORDED)
            command = inspection.get("inspection_command")
            if command:
                exit_code = recorded_exit_code(pid, command)
                if exit_code is None:
                    exit_code = nr(
                        "4 (Re-run the checks)",
                        "exit code for piece %s command: %s" % (pid, command),
                    )
                checks.append(
                    {"piece_id": pid, "method": method, "command": command,
                     "exit_code": exit_code}
                )
            else:
                checks.append(
                    {"piece_id": pid, "method": method, "command": None,
                     "exit_code": None,
                     "note": "no command; evidence under rounds/%s/<round>/inspection/" % pid}
                )
    sec4_lines = []
    for check in checks:
        if check["command"]:
            sec4_lines.append(
                "- piece %s (%s): `%s` (recorded exit code: %s)"
                % (check["piece_id"], check["method"], check["command"], check["exit_code"])
            )
        else:
            sec4_lines.append(
                "- piece %s (%s): %s" % (check["piece_id"], check["method"], check["note"])
            )
    if not sec4_lines:
        sec4_lines.append("- %s" % nr("4 (Re-run the checks)", "no inspection entries in pieces.json"))

    # Section 5: Claim audit summary, per knowledge-work piece.
    claim_rows = []
    claim_json = []
    for piece in pieces:
        pid = piece.get("id") or NOT_RECORDED
        domain = piece.get("domain") or run.get("domain_primary")
        audit = load_json(run_dir / "claims" / pid / "audit.json")
        if audit is None and domain not in KNOWLEDGE_DOMAINS:
            continue
        if audit is None:
            nr("5 (Claim audit summary)", "claims/%s/audit.json" % pid)
            row = {
                "piece_id": pid,
                "claims": NOT_RECORDED,
                "unsupported": NOT_RECORDED,
                "citation_ratio": NOT_RECORDED,
                "unreachable_sources": NOT_RECORDED,
            }
        else:
            def pick(*keys, _audit=audit, _pid=pid):
                for key in keys:
                    if key in _audit:
                        return _audit[key]
                return nr(
                    "5 (Claim audit summary)",
                    "claims/%s/audit.json: %s" % (_pid, keys[0]),
                )
            unreachable = pick("unreachable_sources", "unreachable_count")
            if isinstance(unreachable, list):
                unreachable = len(unreachable)
            row = {
                "piece_id": pid,
                "claims": pick("total_claims", "claims_total", "claim_count"),
                "unsupported": pick("unsupported_count", "unsupported"),
                "citation_ratio": pick("claim_to_citation_ratio", "citation_ratio"),
                "unreachable_sources": unreachable,
            }
        claim_json.append(row)
        claim_rows.append(
            "| %s | %s | %s | %s | %s |"
            % (
                row["piece_id"], row["claims"], row["unsupported"],
                row["citation_ratio"], row["unreachable_sources"],
            )
        )

    # Section 6: Artifact integrity.
    hashes = load_json(run_dir / "artifact-hashes.json")
    sec6_lines = []
    if hashes is None:
        sec6_lines.append(
            "- %s" % nr(
                "6 (Artifact integrity)",
                "artifact-hashes.json (run hash_artifacts.py before the report)",
            )
        )
    else:
        for entry in hashes.get("artifacts") or []:
            if entry.get("missing"):
                sec6_lines.append(
                    "- %s: MISSING at hash time (%s)"
                    % (entry.get("path"), entry.get("resolved_path"))
                )
            else:
                sec6_lines.append(
                    "- %s: sha256 %s" % (entry.get("path"), entry.get("sha256"))
                )
        snapshots = hashes.get("round_snapshots") or []
        sec6_lines.append(
            "- Round snapshots hashed: %d (see artifact-hashes.json)" % len(snapshots)
        )

    # Section 8: Known remaining gaps (built before 7 so its misses land in 7).
    sec8_lines = []
    gaps_json = {}
    for piece in pieces:
        pid = piece.get("id") or NOT_RECORDED
        if piece.get("status") == "converged":
            continue
        gap = last_gap_text(run_dir, pid)
        if gap is None:
            gap = nr("8 (Known remaining gaps)", "last gap.md for piece %s" % pid)
        gaps_json[pid] = gap
        sec8_lines += ["### %s" % pid, "", gap, ""]
    if not sec8_lines:
        sec8_lines.append("All pieces converged. No remaining gaps recorded.")

    # Section 9: Budget spent.
    cost = load_json(run_dir / "cost.json")

    def cost_value(key):
        if cost is None or key not in cost:
            return nr("9 (Budget spent)", "cost.json: %s" % key)
        return cost[key]

    budget = {
        "rounds_total": cost_value("rounds_total"),
        "subagents_total": cost_value("subagents_total"),
        "sessions_total": cost_value("sessions_total"),
        "wall_clock_hours": cost_value("wall_clock_hours"),
        "tokens": cost_value("tokens"),
        "target_changes_total": cost_value("target_changes_total"),
        "support_artifacts_total": cost_value("support_artifacts_total"),
        "notes": (cost or {}).get("notes", ""),
        "stop_reason": run["stop_reason"] if "stop_reason" in run else nr(
            "9 (Budget spent)", "run.json: stop_reason"
        ),
    }
    if budget["stop_reason"] is None:
        budget["stop_reason"] = "none"
    sec9_lines = [
        "- Rounds: %s" % budget["rounds_total"],
        "- Subagents: %s" % budget["subagents_total"],
        "- Sessions: %s" % budget["sessions_total"],
        "- Wall clock hours: %s" % budget["wall_clock_hours"],
        "- Cost ledger (tokens): %s" % budget["tokens"],
        "- Target changes: %s" % budget["target_changes_total"],
        "- Support artifacts: %s" % budget["support_artifacts_total"],
        "- Ledger notes: %s" % (budget["notes"] or "none"),
        "- Stop reason: %s" % budget["stop_reason"],
    ]

    # Section 7: What was not verified. Mandatory, never omitted.
    sec7_items = []
    for pid in piece_ids:
        cdoc = consensus.get(pid)
        if cdoc is None:
            sec7_items.append(
                "Piece %s: no consensus.json, verification not recorded for this piece." % pid
            )
            continue
        q_cv = (cdoc.get("quality_votes") or {}).get("cannot-verify", 0)
        i_cv = (cdoc.get("integrity_votes") or {}).get("cannot-verify", 0)
        if q_cv or i_cv:
            sec7_items.append(
                "Piece %s: %s quality and %s integrity cannot-verify votes. Dissent: %s"
                % (pid, q_cv, i_cv, "; ".join(cdoc.get("dissent") or []) or NOT_RECORDED)
            )
    for piece in pieces:
        pid = piece.get("id") or NOT_RECORDED
        status = piece.get("status")
        if status in ("capped", "blocked", "dropped"):
            sec7_items.append(
                "Piece %s: status %s. Caps pause, they do not certify (INV-7)."
                % (pid, status)
            )
        if not (run_dir / "rounds" / pid).is_dir():
            sec7_items.append(
                "Piece %s: no rounds recorded; inspection may never have run." % pid
            )
    sec7_lines = ["- %s" % item for item in sec7_items]
    if not_recorded:
        sec7_lines.append("- Values not recorded in state:")
        sec7_lines += ["  - %s" % item for item in not_recorded]
    if not sec7_lines:
        sec7_lines.append(
            "- Nothing outstanding. Every piece has a consensus and every value was recorded."
        )

    run_id = run.get("run_id", NOT_RECORDED)
    md = []
    md.append("# EVIDENCE: %s" % run_id)
    md.append("")
    md.append("## 1. Verdict")
    md.append("")
    md += sec1_lines
    md.append("")
    md.append("## 2. Goal and bar")
    md.append("")
    md += sec2_lines
    md.append("")
    md.append("## 3. Per-piece table")
    md.append("")
    md.append("| Piece | Rounds | Final blind result | Quality votes | Integrity votes | Consensus | Artifact path |")
    md.append("|---|---|---|---|---|---|---|")
    md += sec3_rows if sec3_rows else ["| %s | | | | | | |" % NOT_RECORDED]
    md.append("")
    md.append("## 4. Re-run the checks")
    md.append("")
    md += sec4_lines
    md.append("")
    md.append("## 5. Claim audit summary")
    md.append("")
    if claim_rows:
        md.append("| Piece | Claims | Unsupported | Citation ratio | Unreachable sources |")
        md.append("|---|---|---|---|---|")
        md += claim_rows
    else:
        md.append("No knowledge-work pieces in this run, and no claim audits recorded.")
    md.append("")
    md.append("## 6. Artifact integrity")
    md.append("")
    md += sec6_lines
    md.append("")
    md.append("## 7. What was not verified")
    md.append("")
    md += sec7_lines
    md.append("")
    md.append("## 8. Known remaining gaps")
    md.append("")
    md += sec8_lines
    md.append("")
    md.append("## 9. Budget spent")
    md.append("")
    md += sec9_lines
    md.append("")

    evidence_md = run_dir / "EVIDENCE.md"
    evidence_md.write_text("\n".join(md), encoding="utf-8")

    evidence = {
        "run_id": run_id,
        "verdict": verdict,
        "context_isolation": isolation,
        "degraded": isolation != "clean",
        "sections": {
            "1_verdict": {"verdict": verdict, "banner": banner},
            "2_goal_and_bar": {
                "goal": goal,
                "bar": bar_line,
                "plan_hash": plan_hash,
                "plan_hash_matched": hash_matched,
            },
            "3_pieces": piece_json,
            "4_checks": checks,
            "5_claim_audit": claim_json,
            "6_artifact_hashes": hashes if hashes is not None else NOT_RECORDED,
            "7_not_verified": sec7_items + not_recorded,
            "8_remaining_gaps": gaps_json,
            "9_budget": budget,
        },
    }
    evidence_json = run_dir / "EVIDENCE.json"
    evidence_json.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "result": "built",
                "verdict": verdict,
                "evidence_md": str(evidence_md),
                "evidence_json": str(evidence_json),
                "not_recorded": not_recorded,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
