# Ownership and state (Hatch adaptation)

## Ownership

LoopKit owns loop and goal contracts, bounded execution, receipts, resume, scheduling records, and runtime diagnosis. It does not own agent definitions, idea-to-result workflows that need no feedback loop, or learning protocols.

## State lookup

Resolve the state root in this order:

1. `LOOPKIT_STATE_ROOT` for an isolated or test run.
2. Otherwise `~/workspace/loopkit/` — durable across chat sessions, subagents, and cron runs. (The original plugin's `~/.claude/loopkit` / `~/.codex/loopkit` host roots do not apply on Hatch.)

Each workspace uses a 12-character SHA-256 hash of its resolved path. Every run directory contains `contract.json`, `state.json`, append-only `events.jsonl`, compact `checkpoint.md`, an `evidence/` directory, and optional `schedule.json` / `BLOCKED.md`.

Run layout:

```text
~/workspace/loopkit/runs/<workspace-hash>/<YYYYMMDDTHHMMSSZ>-<slug>/
  contract.json
  state.json
  events.jsonl
  checkpoint.md
  evidence/
  BLOCKED.md        optional
  schedule.json     optional
```

## Authority

LoopKit records authority but does not create it. Cron jobs, external messages, destructive actions, privacy-sensitive access, purchases, and production changes remain separately approval-gated under the active task's rules.
