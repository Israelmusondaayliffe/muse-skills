---
name: loop-observatory
description: "Read-only cross-loop telemetry: ingest terminal LoopKit runs and registered run roots, normalize outcome evidence, compare loop performance across time or versions, audit judge calibration for false passes and false failures, and hand off unresolved runs for repair. Use when asked to ingest terminal runs, compare acceptance or exhaustion across loops, calculate cost per accepted result, audit judges, or find repeated limit exhaustion. Do not use to design, run, schedule, or repair a loop."
---

# Loop Observatory

Read-only measurement layer for bounded agent loops. It ingests terminal LoopKit runs and explicitly registered run roots, normalizes them into comparable evidence records, and produces portfolio metrics and judge-calibration audits as JSON plus Markdown.

Adapted from the public `loop-observatory` plugin (MIT) by Israelmusondaayliffe. Codex/Claude plugin manifests, slash commands, and hook formats do not transfer; everything here runs with native Hatch tools.

## Router

Classify the request and run only the matching phase. Load the named reference only when needed.

- **Ingest** new terminal runs: `references/ownership-and-sources.md`, `references/normalized-schema.md`, then Ingest below.
- **Report** portfolio metrics: ingest once first, then Report below.
- **Audit** judge calibration: ingest once first, then Audit below.
- A request to design, run, schedule, or repair a loop is out of scope: route it to the loopkit or agent-ops skill and say so.

## Tooling

`bin/loop_observatory.py` — ported CLI (reviewed: pure stdlib JSON/file I/O with atomic writes; read-only against sources, no network, no subprocess, no credential access).

- State lives in `$LOOP_OBSERVATORY_HOME` (default `~/workspace/loop-observatory/`).
- LoopKit runs are discovered under `$LOOPKIT_STATE_ROOT` (default `~/workspace/loopkit/`), matching the loopkit skill.
- External run roots must be registered explicitly before ingestion.

## Ingest

1. Register external run roots once: `python3 bin/loop_observatory.py register-root /absolute/path/to/root` (the LoopKit root needs no registration).
2. Run: `python3 bin/loop_observatory.py ingest [--loopkit-root /absolute/path]`
3. When read-only behavior must be proven, confirm the source fingerprint before and after: the CLI hashes each source tree around the read and fails if it changes mid-read.
4. Return the counts the CLI reports — ingested, unchanged, duplicate, incomplete, corrupt — plus the error list for corrupt sources. Treat corrupt and incomplete sources as evidence failures, never as terminal successes.

## Report

1. `python3 bin/loop_observatory.py report` writes a timestamped JSON + Markdown report under `<state>/reports/` and prints the summary.
2. Acceptance rate is calculated only from runs with known human labels. Cost per accepted result is calculated only when every accepted run has known cost evidence. Missing evidence stays unknown — never inferred (field definitions in `references/normalized-schema.md`).
3. Scheduled use: `python3 bin/loop_observatory.py report --scheduled` returns a clean no-op when no new terminal runs were ingested since the last report. Recurrence is a cron job created with user approval — Hatch has no plugin hooks; `--scheduled` exists to give it no-op behavior.

## Audit

1. `python3 bin/loop_observatory.py audit` compares machine verdicts against later human labels.
2. A false pass requires a positive machine verdict plus a negative human label; a false failure requires the reverse. Unlabeled runs stay outside disagreement rates. Escalation reasons that repeat across runs are reported as clusters.
3. Repairs are out of scope here. For a flagged RECORD_ID, run `python3 bin/loop_observatory.py repair-handoff RECORD_ID` and return the complete handoff unresolved. Do not claim a repair occurred.

## Repair handoff

The handoff is local and read-only. It records the source run, normalized evidence, the disagreement type, the owner class, the requested outcome, and the missing proof — then stays unresolved. A repair is complete only when the owning capability (loopkit skill or agent-ops) produces a repair receipt and a new terminal run with a different source hash is ingested.

## Output Contract

- Ingest returns: per-class counts (ingested / unchanged / duplicate / incomplete / corrupt) plus any error list.
- Report returns: paths to the JSON and Markdown report files plus the headline metrics.
- Audit returns: false-pass and false-failure record IDs, disagreement rate, exhausted run IDs, escalation clusters.
- Missing evidence is reported as unknown, never filled in.

## Operating Rules

1. Source runs are read-only: never edit, repair, or relabel them; never infer missing labels, costs, or durations.
2. Do not design, execute, schedule, or directly repair any loop here — route those to the loopkit skill or agent-ops.
3. Keep observatory state under `$LOOP_OBSERVATORY_HOME`; leave source directories untouched (fingerprints prove this).
4. Scheduled reporting is a cron job with user approval; never an endless shell loop and never a claim that Hatch runs plugin hooks.
5. Ask the user before ingesting run roots they have not named or registered.
