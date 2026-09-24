---
name: loopkit
description: "Bounded, resumable Plan-Act-Verify loops with durable on-disk state: design a verifiable contract, execute bounded iterations with receipts, independently verify completion, resume after interruption, schedule recurrence, and diagnose stuck or drifting loops. Use when the user says build a loop, run this until done, make this recurring, resume the run, schedule this task, verify it is actually done, or diagnose a stuck loop. Do not use for quick one-shot questions."
---

# LoopKit

Run durable work loops: contract on disk, bounded iterations with evidence receipts, independent verification, and generation-guarded state so interruption or a long pause cannot silently change the finish line. A loop is appropriate only when fresh feedback can change the next action. If the work finishes in one pass, use a one-shot workflow instead.

Adapted from the public `loopkit` plugin (MIT) by Israelmusondaayliffe. Codex/Claude hooks and manifests do not transfer; everything here runs with native Hatch tools.

## Router

1. Classify the request and run only the matching phase. Load the named reference only when needed.
2. End-to-end order: design → run → verify, then schedule only if recurrence is requested.

- **Design** a new loop or goal contract: `references/contract-fields.md`, then workflow below.
- **Run** a ready contract: workflow below.
- **Verify** a run or artifact: `references/receipt-schema.md`, `references/adversarial-checks.md`.
- **Resume** interrupted work: `references/resume-integrity.md`.
- **Schedule** a tested run: `references/schedule-schema.md`, via cron tools (never an endless shell loop).
- **Diagnose** repetition, drift, weak verification, or unsafe authority: `references/failure-modes.md`.

## Design

1. Define the outcome so a stranger can verify it from artifacts and checks.
2. Require at least one deterministic machine check (a shell command I can run with `muse.exec`). Keep judgment criteria separate.
3. Record allowed paths, forbidden paths, and approval-gated external actions.
4. Use user-supplied iteration limits; when none exist, ask — the schema requires explicit positive caps.
5. Define success, failure, blocked, and exhausted stops.
6. Copy `assets/contract-template.json` into the task's working path and replace every `__REPLACE_ME__`.
7. Validate: `python3 bin/validate_contract.py /absolute/path/to/contract.json`
8. Initialize state only after validation:
   `python3 bin/init_run.py /absolute/path/to/contract.json --workspace /absolute/workspace/path [--slug name]`
9. Return the run directory and summarize the authority boundary. Do not start execution unless an end-to-end run was requested.

## Run

1. Read `contract.json`, `state.json`, and `checkpoint.md` from the run directory; confirm the contract still matches the request and authority.
2. Transition with a generation check:
   `python3 bin/transition_run.py RUN_DIR running --expected-generation N --reason "..."`
3. Iterate: observe fresh state → choose the highest-value in-scope action → act once → run the relevant checks → write a receipt (`references/receipt-schema.md`) → validate and record atomically:
   `python3 bin/validate_receipt.py RUN_DIR /absolute/receipt.json`
   `python3 bin/record_receipt.py RUN_DIR /absolute/receipt.json --expected-generation N`
4. Re-read `state.json`; repeat only if status is `running`, progress is measurable, and caps hold.
5. Stops: `completed`, `waiting_input`, `blocked`, `exhausted`, `failed`, `cancelled`. Never convert a failed/blocked/exhausted run into success; never widen paths, permissions, or the goal during execution.

## Verify

Read `contract.json` without trusting the builder's summary. Re-run each machine check exactly as recorded (when safe and authorized). Judge every criterion with fresh file, line, screenshot, or command evidence — never old output. Record a receipt: `completed` only if every required check and criterion passes; otherwise the honest nonterminal status with precise failures and the smallest next action. Do not relax the contract, swallow errors, or accept a renamed, stubbed, skipped, or deleted check as proof. Keep verification separate from repair: the actor does not approve its own narrative.

## Resume

Never infer state from chat memory. Read `contract.json`, `state.json`, `checkpoint.md`, and the newest receipt; confirm the run id matches across files and the status is nonterminal. Refresh the checkpoint (`python3 bin/checkpoint_run.py RUN_DIR`), inspect fresh workspace state, then route: `waiting_input` → ask only for the missing decision; `blocked` → check the named prerequisite; `scheduled` → confirm scheduled vs manual invocation; `running` → continue the run loop. If files disagree, stop and diagnose instead of repairing by guessing.

## Schedule

Readiness gate: one successful manual run, a self-contained cron task prompt naming the workspace and run directory, user-approved cadence and timezone, clean no-op behavior, evidence returned on meaningful change, and a stop/pause condition.

1. Write the schedule record: `python3 bin/write_schedule.py RUN_DIR /absolute/schedule-draft.json` (schema in `references/schedule-schema.md`).
2. Create the cron job with `cron.add`; record the real `cron_job_id` in the run's `schedule.json`.
3. Observe the first scheduled execution and inspect its receipt; confirm no-op, evidence, permission, and stop behavior before declaring readiness.

## Diagnose

`python3 bin/doctor_run.py RUN_DIR` classifies findings into contract, execution, verification, state, or scheduler layers. Rank by severity, propose the smallest repair that preserves the intended outcome, then re-run the failing validation and one bounded cycle. See `references/failure-modes.md`. Do not change the goal, authority, or limits without user approval.

## Tooling

`bin/` holds the ported state helpers (reviewed: pure local JSON/file I/O, atomic writes, locks — no network, no subprocess, they never execute machine checks; I run those myself with `muse.exec`):

`validate_contract.py` · `init_run.py` · `transition_run.py` · `validate_receipt.py` · `record_receipt.py` · `checkpoint_run.py` · `doctor_run.py` · `write_schedule.py`, all backed by `loopkit_core.py`. Run them from any directory; `LOOPKIT_STATE_ROOT` overrides the default `~/workspace/loopkit/`.

## Operating Rules

1. The contract is the finish line; state files are authoritative over chat memory.
2. Every state change goes through a generation-checked transition — never edit `state.json` by hand.
3. Never invent a success condition, check command, cadence, path, or permission the contract lacks. Ask one focused question only when the missing answer changes safety or the contract; otherwise record the unknown and take the smallest reversible step.
4. The loop grants no new authority: cron jobs, external sends, purchases, deletions, and privacy-sensitive access stay approval-gated.
5. Hatch has no plugin hooks. Refresh checkpoints manually before and after long background work instead of relying on PreCompact/SessionStart.
6. When resuming as a subagent, spawn in a fresh context with the run directory path and instruct it to read the contract, state, and checkpoint first.
