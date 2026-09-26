---
name: loop-observatory
description: "Read-only cross-loop telemetry: ingest terminal LoopKit runs and registered run roots, normalize outcome evidence, compare loop performance across time or versions, audit judge calibration for false passes and false failures, and hand off unresolved runs for repair. Use when asked to ingest terminal runs, compare acceptance or exhaustion across loops, calculate cost per accepted result, audit judges, or find repeated limit exhaustion. Do not use to design, run, schedule, or repair a loop."
---

# Loop Observatory

Measure bounded agent loops without touching them. The finished result is the CLI's own records (ingest counts, a JSON and Markdown portfolio report, an audit, repair handoffs) plus a plain reading of what the numbers do and do not show. Missing evidence stays unknown.

Adapted from the public `loop-observatory` plugin (MIT). Everything runs with native Hatch tools; there are no plugin hooks or slash commands.

## Start here

Run commands from this skill folder with `bin/loop_observatory.py` (standard library; reads sources, writes only its own state; no network or subprocess).

1. **Locate the runs.** LoopKit runs are found under `$LOOPKIT_STATE_ROOT` (default `~/workspace/loopkit/`) or `--loopkit-root <dir>`: any folder with `state.json` beside `contract.json`. Other engines' run roots (folders with `state.json` beside `graph.json`) must be registered first with `register-root <absolute-dir>`. Ingest only roots the user named or already registered.
2. **Observatory state** lives in `$LOOP_OBSERVATORY_HOME` (default `~/workspace/loop-observatory/`). Point it at a scratch folder for trial runs.
3. **Pick the phase:**

| The request | Phase | Command |
|---|---|---|
| New runs finished; "pull them in" | Ingest | `ingest [--loopkit-root <dir>]` |
| Acceptance, exhaustion, cost per accepted result, comparison across loops | Report (ingest first) | `report` |
| "Is the judge right?", false passes or failures | Audit (ingest first) | `audit` |
| A flagged record needs fixing | Repair handoff | `repair-handoff <record-id>` |
| Design, run, schedule, or repair a loop | Out of scope | route to `loopkit` or `agent-ops` and say so |

## What the numbers mean

Field definitions: `references/normalized-schema.md`; report shape: `assets/report-template.json`.

- **Ingest counts.** `ingested` are new terminal runs. `unchanged` were seen before with the same content. `incomplete` are still running or lack a terminal status. `corrupt` could not be read; the error list names them. `incomplete` and `corrupt` are evidence gaps, never successes. `discovered: 0` means no evidence, not a healthy portfolio.
- **Human acceptance rate** uses only runs with a human label. Unlabeled runs are excluded, and the report says how many had labels (`human_acceptance_known`).
- **Cost per accepted result** is reported only when every accepted run has known cost. One accepted run without cost makes it `null`.
- **Audit.** A false pass is a passing machine verdict with a negative human label; a false failure is the reverse. Unlabeled runs stay outside the disagreement rate. Repeated escalation reasons appear as clusters.
- **Scheduled use.** `report --scheduled` returns `no-op` when nothing new was ingested. A recurring report is a cron job the user approves; never an endless shell loop.

## Worked example (illustrative, runnable from this skill folder)

```bash
export LOOP_OBSERVATORY_HOME=$(mktemp -d)
python3 bin/loop_observatory.py register-root "$PWD/tests/fixtures/graph-run"
python3 bin/loop_observatory.py ingest --loopkit-root "$PWD/tests/fixtures/loopkit-run"
python3 bin/loop_observatory.py report
python3 bin/loop_observatory.py audit
```

Ingest reports 2 discovered, 2 ingested. The report shows `human_acceptance_rate` 1.0 over 2 labeled runs, `exhausted_runs` 1, and `cost_per_accepted_result` null. The audit lists one false failure (a record id starting `operating-graph-og-001-`) and a disagreement rate of 0.5.

Reading it: both runs were accepted by a human, but the graph run hit its iteration limit and its judge said fail, so the judge is too strict for that loop. Cost per accepted result is unknown because that accepted run has no cost evidence, not because it was free. Next step: `repair-handoff <that record id>` and hand it, unresolved, to the loop's owner.

A wrong version would report an average cost of 0.42 per accepted result, call the exhausted run a failure of the work, or say the judge was fixed.

## Repair handoff

`repair-handoff <record-id>` prints a handoff with the source run, normalized evidence, disagreement type, owner class, requested outcome, and missing proof, with `handoff_status: unresolved` and `repair_performed: false`. Save it where the user asked. A repair is complete only when the owning capability (the `loopkit` skill or `agent-ops`) produces a repair receipt and a new terminal run with a different source hash is ingested.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| `discovered: 0` | Wrong root, or runs lack `state.json` plus `contract.json`/`graph.json` | List the folder; fix `--loopkit-root` or register the right root once | the user has not named a root |
| `corrupt` with a JSON error | Bad source file | Report the path and error; do not edit the source | never; sources are read-only |
| `source changed during read` | A loop is still writing | Rerun ingest once after it finishes | it keeps changing |
| Metric is `null` | Missing labels or cost evidence | Report it as unknown and say which runs lack what | never infer the value |
| `repair-handoff` fails on an id | Id not in `runs/` | Take the id from `audit` or `$LOOP_OBSERVATORY_HOME/runs/` | never guess an id |

## Completion

- Ingest: per-class counts and the error list.
- Report: JSON and Markdown report paths plus the headline metrics, with unknowns named.
- Audit: false-pass and false-failure record ids, disagreement rate, exhausted run ids, escalation clusters.
- Handoff: the saved unresolved handoff. Never claim a repair occurred.

## Operating rules

1. Source runs are read-only: never edit, repair, relabel, or infer labels, costs, or durations. The CLI hashes each source around the read and fails if it changes.
2. Do not design, execute, schedule, or repair loops here.
3. Keep observatory state under `$LOOP_OBSERVATORY_HOME`.
4. Ask before ingesting run roots the user has not named or registered.
