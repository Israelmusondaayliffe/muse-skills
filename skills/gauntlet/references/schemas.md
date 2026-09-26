# Gauntlet state layout and schemas

Runs live in `.gauntlet/runs/<YYYYMMDD-HHMM-slug>/` under the target project root.
Blind label maps are sealed outside the run directory at
`.gauntlet/sealed/<run-id>/<piece>/<round>/map.json`. No skill invents a shape;
these are the shapes (condensed from the method spec).

## Inspection methods, closed set

```
run  test  measure  screenshot  render  reader-proxy  claim-audit  source-reach  red-team  read
```

Enforced by `validate_pieces.py`: every piece declares at least one method; every
method except `read` and `reader-proxy` declares an `inspection_command`; `read`
alone is never sufficient, and on knowledge-work pieces it must pair with
`reader-proxy` or `claim-audit`; a piece inspectable by no method is not a valid
piece.

## run.json

```json
{
  "run_id": "20260923-1400-akira-editorial",
  "goal_one_line": "Ship AKIRA issue 04 at a clarity level that beats the reference set.",
  "domain_primary": "prose",
  "execution_shape": "S2",
  "status": "briefed",
  "created": "2026-09-23T14:00:00Z",
  "plan_hash": "sha256:...",
  "precheck": {"result": "degraded", "subagents": "unknown", "filesystem": true, "command_execution": true, "network": null},
  "context_isolation": "degraded",
  "budgets": {"rounds_cap_per_piece": 2, "wave_cap": 1, "wall_clock_hours_per_session": 0.5, "subagent_cap_per_run": 6, "cost_ceiling": 0, "approved": true, "approval_ref": "CONTEXT.md 2026-09-23 user approved 6 launches, 0 metered spend"},
  "current_wave": 1,
  "stop_reason": null
}
```

`init_run.py` writes the defaults shown above with `"approved": false`,
`"approval_ref": null`, and `"context_isolation": "unknown"`. The lead sets
`approved` and `approval_ref` only after the user accepts the stated envelope;
`approval_ref` points at the recorded decision. `check_stops.py` pauses the run as
`budget-unverified` while approval is missing, any cap is not a finite positive
number, `cost_ceiling` is not a finite nonnegative number, or `cost.json` usage is
unknown, negative, or non-numeric. `cost_ceiling: 0` allows no metered spend. A
piece's `rounds_cap` is clamped to `rounds_cap_per_piece`. These are cooperative
gates over records the lead keeps; they do not intercept tools or cap account-wide
spend. `context_isolation` is `clean` only when the lead has recorded host evidence
of isolation; a surface or model name is not evidence.

`status` closed set: `briefed`, `prompted`, `running`, `paused`, `stopped`,
`converged`, `verifying`, `verified`, `failed`, `unverifiable`, `reported`.

## pieces.json

```json
{
  "run_id": "20260923-1400-akira-editorial",
  "plan_hash": "sha256:...",
  "decomposition_owner": "lead-agent",
  "pieces": [{
    "id": "opening-section",
    "name": "Opening section of the editorial",
    "domain": "prose",
    "lane": "a",
    "wave": 1,
    "artifact_paths": ["drafts/akira-issue-04.md#opening"],
    "inspection": [
      {"method": "reader-proxy", "questions": ["What is this piece arguing?", "Why would a reader continue past line three?"]},
      {"method": "claim-audit", "inspection_command": "python3 ~/workspace/skills/gauntlet/scripts/claim_audit.py --run-dir <run-dir> --piece opening-section"}
    ],
    "bar_refs": ["bar/refs/reference-openings.md"],
    "blind_feasible": true,
    "acceptance": "Blind critic picks ours over the reference in 2 consecutive rounds, and reader-proxy answers both questions without guessing.",
    "verifiers": {"quality": 3, "integrity": 3},
    "status": "looping",
    "rounds_completed": 1,
    "rounds_cap": 2,
    "consecutive_wins": 0,
    "last_gap": "Second paragraph restates the first at lower density.",
    "no_gain_streak": 1
  }]
}
```

Piece `status` closed set: `pending`, `looping`, `converged`, `capped`, `blocked`,
`dropped`. Inspection commands stored in `pieces.json` must carry resolved absolute
paths, never placeholders — they are re-run as evidence outside the skill context.

## lanes.json

`{"shape": "S2", "lanes": [{"id": "a", "owned_pieces": [...], "owned_paths": [...], "lock_holder": "session-3", "heartbeat": "...", "status": "active"}]}`

## Round records (`rounds/<piece>/<nnn>/`)

Each round directory holds `artifact/` (snapshot), `inspection/` (outputs plus
`results.json` rows of `{"command", "exit_code", "ran_at"}` for every inspection
command executed), `blind/` (neutral A/B copies), `verdict.json`, and `gap.md`.

`verdict.json` (full schema enforced by `round_record.py`; the critic supplies only
`winner`, `confidence` (string), `reasoning`, `largest_gap`, `gap_is_actionable` —
the lead fills the rest): `{"piece_id", "round", "blind", "seed", "winner":
"A"|"B", "winner_is_ours", "confidence": str, "reasoning", "largest_gap",
"gap_is_actionable", "inspection_evidence": [paths], "rubric_hash" (or null),
"critic_saw_builder_context": false, "critic_context_source": "files-only"}`.
The lead writes `winner_is_ours` after unsealing; the critic never writes it.
`round_record.py` rejects any verdict where `critic_saw_builder_context` is true,
`critic_context_source` is not `files-only`, or `largest_gap` is empty.

## Verification (`verification/<piece>/`)

Verdict files `quality-1.json`..`quality-N.json`, `integrity-1.json`..`integrity-N.json`,
each: `{"piece_id", "verifier_type", "verifier_index", "result": "pass"|"fail"|"cannot-verify",
"criterion_applied", "evidence_inspected", "reason", "plan_hash_matched"}`.
`consensus.py` writes `consensus.json` applying, first match wins: any integrity
fail → `failed`; any `cannot-verify` → `unverifiable`; all pass → `verified`;
majority quality pass with dissent → `verified-with-dissent`; otherwise `failed`.

## Claim ledger (`claims/<piece>/ledger.json`)

Rows: `{"claim", "source", "support_type": "primary"|"secondary"|"user-supplied"|"own-analysis"|"unsupported",
"quote", "location"}`. `claim_audit.py` writes `audit.json`. Any `unsupported`
row is an integrity failure, not a style note.

## Other state

- `CONTEXT.md`: append-only and permanent. What the project is, the bar, dated
  decision log. Corrections are appended with a date and reason, never edited in place.
- `PLAN.md`: the wave plan — success criteria (copied verbatim into each piece's
  `acceptance`), shape, decomposition, budgets. `gauntlet-verify` reads criteria
  from `PLAN.md`, never from later state. Frozen by `hash_plan.py`.
- `bar/bar.md`: the bar definition, rationale, inspection method, rubric hash if
  any. `bar/refs/`: real reference artifacts. Passed by `validate_bar.py`.
- `cost.json`: `rounds_total`, `subagents_total`, `sessions_total`,
  `wall_clock_hours`, `tokens`, `target_changes_total`, `support_artifacts_total`.
- `sessions/sessions.json`: session entries with exit records.
- `workbench.html`: generated by `render_workbench.py` after every round, never
  hand-authored.
