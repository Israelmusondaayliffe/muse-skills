---
name: loopkit
description: "Bounded, resumable Plan-Act-Verify loops with durable on-disk state: design a verifiable contract, execute bounded iterations with receipts, independently verify completion, resume after interruption, schedule recurrence, and diagnose stuck or drifting loops. Use when the user says build a loop, run this until done, make this recurring, resume the run, schedule this task, verify it is actually done, or diagnose a stuck loop. Do not use for quick one-shot questions."
---

# LoopKit

Run durable work loops: a contract on disk, bounded iterations with evidence receipts, independent verification, and generation-guarded state, so an interruption or a long pause cannot quietly move the finish line. A loop fits only when fresh feedback can change the next action. If the work finishes in one pass, do it in one pass.

Adapted from the public `loopkit` plugin (MIT). Plugin hooks and manifests do not transfer; everything here runs with native Hatch tools.

A loop is finished when `state.json` shows `completed` through a validated receipt whose every machine check and judgment criterion passed. A contract, a started run, or an iteration that "looks done" is not completion.

## Start here

1. **Loop or one pass?** One edit with one check is a one-pass task; do it and verify it, no run directory needed. Use a loop when the work needs several act-check cycles, must survive interruption, or must recur.
2. **Classify the request** and run only that phase:

| Request | Phase | First command |
|---|---|---|
| "build a loop", new contract | Design | copy `assets/contract-template.json`, then `python3 bin/validate_contract.py /abs/contract.json` |
| "run it", validated contract | Run | `python3 bin/init_run.py /abs/contract.json --workspace /abs/workspace --slug <name>` |
| "is it actually done" | Verify | re-run each `machine_checks` command yourself |
| "resume" | Resume | `python3 bin/checkpoint_run.py RUN_DIR` |
| "make it recurring" | Schedule | readiness gate below |
| "it's stuck / drifting" | Diagnose | `python3 bin/doctor_run.py RUN_DIR` |

3. **State location.** Runs live under `~/workspace/loopkit/runs/<workspace-hash>/<timestamp>-<slug>/`. Set `LOOPKIT_STATE_ROOT` to use another root (for example a scratch folder in a test).

## Design

1. Define the outcome so a stranger can verify it from artifacts and checks.
2. At least one deterministic machine check: a shell command you can run with `muse.exec` that exits 0 on success. Keep judgment criteria separate.
3. Allowed paths, forbidden paths, approval-gated external actions.
4. Iteration caps from the user. If none were given, propose small ones (for example 2 iterations, no-progress limit 1) and state them; ask only if the task is risky.
5. Success, failure, blocked, and exhausted stops.
6. Replace every `__REPLACE_ME__`. A contract that still contains one is not complete: `validate_contract.py` exits 1 naming each field, and `init_run.py` refuses it. Fill a missing value from the user's answer, never with invented text. Field notes: `references/contract-fields.md`.
7. `validate_contract.py` prints `contract valid`, then `init_run.py` creates the run with `status: ready`, `generation: 0`. Return the run directory and the authority boundary. Start executing only when the user asked for an end-to-end run.

## Run

1. Read `contract.json`, `state.json`, `checkpoint.md`; confirm they still match the request.
2. Start: `python3 bin/transition_run.py RUN_DIR running --expected-generation 0 --reason "start"` (use the current `generation` from `state.json`; each write increments it).
3. Iterate: observe fresh state, take the one highest-value in-scope action, run the checks, write a receipt (`references/receipt-schema.md`) with evidence files inside the run directory, then:
   `python3 bin/validate_receipt.py RUN_DIR /abs/receipt.json`
   `python3 bin/record_receipt.py RUN_DIR /abs/receipt.json --expected-generation N`
4. Repeat only while status is `running`, progress is measurable, and caps hold. Terminal states: `completed`, `waiting_input`, `blocked`, `exhausted`, `failed`, `cancelled`. Never relabel failed, blocked, or exhausted as success, and never widen paths or the goal mid-run.

## Verify

Read `contract.json`, not the builder's summary. Re-run each machine check exactly as recorded, when safe. Judge each criterion with fresh file, line, or command evidence. `completed` only if every required check and criterion passes; otherwise the honest nonterminal status with the precise failure and the smallest next action. A renamed, stubbed, skipped, or deleted check is not proof. Checks: `references/adversarial-checks.md`.

## Resume

Never infer state from chat memory. Read `contract.json`, `state.json`, `checkpoint.md`, and the newest receipt; confirm the run id matches across them. Refresh with `checkpoint_run.py`, inspect fresh workspace state, then route: `waiting_input` asks only for the missing decision; `blocked` checks the named prerequisite; `running` continues. Files that disagree mean diagnose, not guess (`references/resume-integrity.md`).

## Schedule

Scheduling creates a recurring job, which needs the user's explicit approval of cadence and timezone, and a cron tool that is actually listed in this session. If either is missing, deliver the tested manual command and stop.

Readiness gate: one successful manual run, a self-contained task prompt naming workspace and run directory, clean no-op behavior on quiet runs, evidence on meaningful change, and a stop condition. Then `python3 bin/write_schedule.py RUN_DIR /abs/schedule-draft.json` (`references/schedule-schema.md`), create the job, record its real id in `schedule.json`, and inspect the first scheduled receipt before calling it ready.

## Worked example (illustrative, synthetic)

Request: "Use LoopKit to add a summary section to release-notes.md. The draft contract is attached; the owner's answer for the missing stop is attached."

- `validate_contract.py` exits 1: `stops.exhausted must be a non-empty string without __REPLACE_ME__`. Report that one gap; fill it with the owner's text ("two iterations used without both checks passing"). Validation prints `contract valid`.
- `init_run.py` returns the run directory; `state.json` shows `ready`, generation 0. `transition_run.py RUN_DIR running --expected-generation 0 --reason "start"` moves it to generation 1.
- Act once: add `## Summary` with one sentence restating the three bullets. Judgment: the summary may only restate; "faster downloads" would be a new claim the notes do not make. `grep -q '^## Summary$' release-notes.md` exits 0.
- Receipt with both the machine check and the judgment criterion, evidence file under the run's `evidence/`, `status: completed`; `record_receipt.py ... --expected-generation 1`; `state.json` shows `completed`, generation 2.

A wrong version would say "contract valid" before the fix, invent the exhausted rule, edit `state.json` by hand, or create a cron job nobody asked for.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `validate_contract.py` exit 1 | Placeholder left, empty field, bad cap | Fill each named field from the user's facts | a value is unknown: ask for that one field |
| `generation mismatch: expected N, found M` | Stale generation number | Re-read `state.json`; use its `generation` | mismatch repeats: another writer; diagnose |
| `invalid receipt transition: ready -> completed` | Run never started | `transition_run.py ... running` first | valid |
| `evidence path does not exist` | Evidence written outside the run or not yet | Write the evidence file; re-validate | valid |
| Same failure two iterations in a row | No progress | Record `exhausted` or `blocked` with the failure | always at `no_progress_limit` |
| Cron tool missing or unapproved | Host capability or authority | Deliver the manual command | always; never an endless shell loop |

## Tooling

`bin/` holds pure local JSON and file helpers with atomic writes and locks. They never run machine checks and never touch the network; you run checks with `muse.exec`. `validate_contract.py`, `init_run.py`, `transition_run.py`, `validate_receipt.py`, `record_receipt.py`, `checkpoint_run.py`, `doctor_run.py`, `write_schedule.py`, backed by `loopkit_core.py`. References: `contract-fields.md`, `receipt-schema.md`, `resume-integrity.md`, `schedule-schema.md`, `failure-modes.md`, `adversarial-checks.md`, `ownership-and-state.md`, `examples.md`.

## Operating rules

1. The contract is the finish line; state files beat chat memory.
2. Every state change goes through a generation-checked script; never edit `state.json` by hand.
3. Never invent a success condition, check, cadence, path, or permission the contract lacks. Ask one focused question only when the answer changes safety or the contract.
4. The loop grants no new authority: scheduled jobs, external sends, purchases, deletions, and privacy-sensitive access stay approval-gated.
5. Hatch has no plugin hooks. Refresh the checkpoint before and after long background work.
