# Loop failure modes

## False completion

Symptoms: completed state without a valid receipt, missing check ids, stale evidence, relaxed tests, or self-review. Repair the verification gate and return the run to an honest nonterminal state only with explicit approval for the state change.

## Context loss

Symptoms: the next action conflicts with the contract after a long pause or session change. Refresh the checkpoint from durable files with `bin/checkpoint_run.py RUN_DIR` and re-read `contract.json`, `state.json`, and the newest receipt. Hatch has no compaction hooks; refresh checkpoints manually before and after long background work.

## Repetition

Symptoms: equivalent actions recur with no new evidence. Check receipt persistence, no-progress counting, action granularity, and whether the next action reads the latest workspace state.

## Authority drift

Symptoms: the loop touches new paths, services, or external actions. Stop and restore the contract boundary. Permissions never expand because a loop repeats.

## Scheduler drift

Symptoms: wrong cadence, silent failures, or repeated no-op noise. Keep decisions in the cron job's task prompt, record the cron job id and timezone in the schedule record, and observe a real scheduled execution before declaring readiness.
