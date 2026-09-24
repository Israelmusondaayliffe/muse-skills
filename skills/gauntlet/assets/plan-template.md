# PLAN.md: {{run_id}}, wave {{wave_number}}

The wave plan. Versioned per wave at `waves/<n>/PLAN.md`; this root copy points at the current wave.

- Current wave: {{wave_number}}
- Current wave plan file: {{wave_plan_path}}

## Brief fields

All eleven fields must be present and non-empty before `brief_complete.py` passes. Success criteria live in the delimited block below and count as the `success_criteria` field.

- goal_one_line: {{goal_one_line}}
- bar_definition: {{bar_definition}} (backed by a file, command, source set, or measurement)
- bar_rationale: {{bar_rationale}}
- done_means: {{done_means}} (one of: blind win, measured threshold, user judgment)
- domain_primary: {{domain_primary}} (per-piece overrides live in `pieces.json`)
- execution_shape: {{execution_shape}} (one of: S1, S2, S3)
- budget_ceiling: {{budget_ceiling}} (rounds, wall clock, cost, or all three)
- out_of_scope: {{out_of_scope}}
- non_negotiables: {{non_negotiables}}
- inspection_feasibility: {{inspection_feasibility}} (per proposed piece, at least one method from the closed set: run, test, measure, screenshot, render, reader-proxy, claim-audit, source-reach, red-team, read; read alone never qualifies)

## Success criteria

3 to 7 criteria, each independently checkable. This block is hashed by `hash_plan.py` and copied verbatim into each piece's `acceptance`. Do not edit anything between the markers after hashing; a mismatch at verification time is an integrity failure.

<!-- success-criteria:start -->
1. {{criterion_1}}
2. {{criterion_2}}
3. {{criterion_3}}
<!-- success-criteria:end -->

## Decomposition (provisional)

`decomposition_owner: lead-agent`. The plugin proposes; the lead agent re-splits during the run.

| Piece ID | Name | Domain | Lane | Wave | Artifact paths | Inspection methods | Blind feasible | Acceptance |
|---|---|---|---|---|---|---|---|---|
| {{piece_id}} | {{piece_name}} | {{piece_domain}} | {{lane}} | {{wave}} | {{artifact_paths}} | {{methods}} | {{true_or_false}} | {{acceptance}} |

## Budgets

- rounds_cap_per_piece: {{rounds_cap_per_piece}} (default 10)
- wave_cap: {{wave_cap}} (default 4)
- wall_clock_hours_per_session: {{wall_clock_hours_per_session}} (default 6)
- subagent_cap_per_run: {{subagent_cap_per_run}} (default 400)
- cost_ceiling: {{cost_ceiling}} (user-set at brief)

## What this wave attempts

{{wave_objective}}
