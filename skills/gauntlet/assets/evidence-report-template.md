# EVIDENCE.md: {{run_id}}

Every number, path, command, and hash below is read from a file in `.gauntlet/`. The reporting skill may not compute, estimate, recall, or infer any of them. A value missing from state prints `not recorded`, and every `not recorded` is itself listed in section 7.

## 1. Verdict

{{consensus_value}}

One line, the consensus value verbatim from `consensus.json`. No softening, no upgrading. If the run recorded degraded mode, the banner appears here: {{degraded_mode_banner_or_omit}}

## 2. Goal and bar

- What was asked: {{goal_one_line}}
- What it was measured against: {{bar_definition}}
- Why that bar is fair: {{bar_rationale}}
- Plan hash: {{plan_hash}}
- Plan hash matched at verification: {{plan_hash_matched}}

## 3. Per-piece table

| Piece | Rounds | Final blind result | Quality votes | Integrity votes | Consensus | Artifact path |
|---|---|---|---|---|---|---|
| {{piece_id}} | {{rounds_completed}} | {{final_blind_result}} | {{quality_votes}} | {{integrity_votes}} | {{piece_consensus}} | {{artifact_path}} |

## 4. Re-run the checks

Every inspection command with its exit code, copy-pasteable.

```
{{inspection_command}}   # exit {{exit_code}}
```

## 5. Claim audit summary

Per knowledge-work piece:

| Piece | Claims | Unsupported | Citation ratio | Unreachable sources |
|---|---|---|---|---|
| {{piece_id}} | {{claim_count}} | {{unsupported_count}} | {{citation_ratio}} | {{unreachable_sources}} |

## 6. Artifact integrity

SHA-256 of every artifact file at report time, from `hash_artifacts.py`.

| Artifact file | SHA-256 |
|---|---|
| {{artifact_path}} | {{sha256}} |

## 7. What was not verified

Mandatory, never omitted, never empty by silence. List every `cannot-verify`, every capped piece, every skipped inspection, every part of the goal that never became a piece, and every `not recorded` value printed anywhere in this report.

- {{unverified_item}}

## 8. Known remaining gaps

The last `gap.md` of every non-converged piece, verbatim.

### {{piece_id}}

{{last_gap_verbatim}}

## 9. Budget spent

- Rounds: {{rounds_total}}
- Subagents: {{subagents_total}}
- Sessions: {{sessions_total}}
- Wall clock: {{wall_clock_hours}}
- Cost ledger: {{cost_ledger}}
- Stop reason: {{stop_reason}}
