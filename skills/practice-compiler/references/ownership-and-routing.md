# Ownership and routing

Practice Compiler owns read-only trace scanning, redacted signal records, deduplicated proposal staging, and human decisions about those proposals.

It does not own the destination change. These are preferred owners, not runtime requirements:

| Proposal destination | Preferred owner |
| --- | --- |
| Existing skill update | capability-operator |
| New skill candidate | skill-creator |
| AGENTS.md, hook, cron, config, tool, or CLI change | harness-engineering |
| Durable knowledge | continuity-vault |
| Content idea | The user's content backlog, then the chosen writing workflow |
| Discard | No handoff |

Select a preferred owner only when the caller confirms it is available (pass `--available-owner <skill>` at decide time). Otherwise write the generic handoff with an unassigned owner. The handoff still includes the proposal ID, redacted evidence references, occurrence count, decision note, requested outcome, destination class, authority boundary, and proof required before the receiving change.
