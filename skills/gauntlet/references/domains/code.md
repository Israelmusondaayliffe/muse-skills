# Domain adapter: code

SPEC 4.1 row: a piece is a module, system, or function cluster. The bar is a reference implementation, a test suite, or a latency or memory target. Inspection is `run`, `test`, `measure`. Blind comparison is partial, on behavior. Integrity checks: no stubs, no dead paths, tests execute, claimed coverage real.

## What counts as a piece

A piece is a module, a system, or a function cluster: the smallest unit whose behavior can be exercised and judged without touching its neighbors. Good pieces: a parser plus its error paths, a rate limiter, one CLI subcommand, an API endpoint with its data access layer, a retry policy. Bad pieces: "the backend" (too big, split along testable behavior boundaries), "clean up naming" (not independently judgeable, fold it into a real piece), a helper that only makes sense mid-refactor (blocked until its caller exists). Each piece owns disjoint artifact paths in `pieces.json`. If a proposed split forces two pieces onto one file, re-split along module boundaries or merge them. A piece whose behavior cannot be exercised by `run`, `test`, or `measure` is not a valid code piece: split it or drop it.

## What a valid bar looks like here

Three valid bar families. Every one is backed by a file, command, or measurement that exists before round one, and is recorded in `bar/bar.md` with the exact command and threshold.

1. A reference implementation vendored under `bar/refs/`, judged by comparing outputs on a shared input set, never by reading source.
2. A test suite frozen at brief time under `bar/tests/`, with pass threshold and coverage floor stated.
3. A latency, memory, or throughput target with the benchmark command, fixed workload file, machine assumptions, and numeric threshold.

`validate_bar.py` fails a bar that is only adjectives ("fast, clean, production-grade"), that references an artifact this run will produce, or whose reference paths do not resolve. "Beats the current implementation" is valid only after the current implementation is snapshotted into `bar/refs/` before the loop starts.

## Three worked bar examples

Example 1, reference implementation. Goal: reimplement a JSON schema validator. Bar: the existing library vendored at `bar/refs/jsonschema-ref/` plus a case set `bar/refs/cases.jsonl` (312 cases). At brief time, `python3 bar/refs/run_ref.py --cases bar/refs/cases.jsonl > bar/refs/expected.jsonl` freezes expected verdicts. Piece inspection: `run` with `inspection_command: python3 tools/run_candidate.py --cases bar/refs/cases.jsonl --out rounds/validator-core/004/inspection/outputs.jsonl`. Acceptance: verdicts identical to `expected.jsonl` on all 312 cases, and `measure` shows candidate wall time under 2x the reference on the same machine.

Example 2, frozen test suite plus coverage floor. Goal: rate limiter module. Bar: 148 tests frozen at `bar/tests/` at brief time. Inspection: `test` with `inspection_command: python3 -m pytest bar/tests -q --junitxml=rounds/limiter/003/inspection/junit.xml`, threshold zero failures and zero skips added after brief. Coverage: `measure` with `inspection_command: python3 -m coverage run -m pytest bar/tests && python3 -m coverage report --include='src/ratelimit/*'`, floor 85 percent on `src/ratelimit/`.

Example 3, latency and memory target. Goal: query planner rewrite. Bar: p95 latency under 120 ms and peak RSS under 256 MB on the fixed workload `bar/refs/workload-5k.jsonl`. Inspection: `measure` with `inspection_command: python3 bar/bench/bench.py --workload bar/refs/workload-5k.jsonl --json > rounds/planner/002/inspection/bench.json`. The machine assumption is written in `bar/bar.md`; a benchmark run on a different machine class is `cannot-verify`, never a pass.

## Inspection methods, in priority order

1. `test`. Execute the frozen suite against the real artifact. Capture the full transcript and exit code into `rounds/<piece>/<n>/inspection/`.
2. `run`. Execute the artifact on the declared input set and capture actual outputs. A process that starts and exits cleanly is evidence; a description of what it would do is not.
3. `measure`. Benchmarks, coverage, memory profiles, with the exact command from `bar/bar.md` and JSON output stored as evidence.

Every method declares an `inspection_command`. `read` has no standalone role in this domain: source reading may inform the builder, but judgment inspects executed behavior. If any inspection command fails or produces nothing, the round fails and no verdict is produced.

## Blind comparison feasibility and how to set it up

Partial, and only on behavior. Blind comparison works on behavior and output, not on source. Do not ask a critic to blind-compare two implementations by reading them; ask it to compare what they produce. Setup: run candidate and reference against the identical input set, write both output files (test transcripts, run outputs, benchmark JSON) to disk, then let `blind_pair.py` copy them to neutral paths with neutral filenames and seal the map. The critic receives two behavior records, the acceptance criterion, and nothing that names an implementation. Where the bar is a numeric threshold rather than a comparator, set `"blind": false` and judge against the measured number. Never fabricate a blind comparison over source trees.

## What the integrity verifier checks in this domain

No stubs: no function returning canned values, `NotImplementedError`, or TODO bodies on any declared path. No dead paths: no code that exists only to satisfy a reviewer and is never reachable. Tests execute: re-run the recorded `inspection_command` and confirm the exit code, not the narrated summary. Claimed coverage real: re-run the coverage command; a stale or hand-written number is a fail. No weakened gates: tests deleted, skipped, or thresholds loosened after brief time fail, and `hash_plan.py` catches edited success criteria. Existence of files is not evidence of work.

## Common failure modes

- Overfitting to the case set: the builder hardcodes expected outputs. Counter: hold out a slice of cases at brief time and run it only at verification.
- Stub convergence: the piece "passes" because unimplemented branches are never exercised. Counter: integrity verifier traces declared paths to executed tests.
- Suite erosion: failing tests get skipped or deleted mid-run. Counter: freeze `bar/tests/` and diff at verification.
- Source aesthetics judged instead of behavior. Counter: critics receive behavior records only.
- Benchmark drift: numbers from a different machine or workload. Counter: workload path and machine assumption live in `bar/bar.md` and are checked.

## When this domain is the wrong adapter

Use another adapter when the artifact is judged by a reader or viewer, not an executor: documentation and explainers are `prose`, the look of a rendered UI is `visual`, skills and system prompts are `prompt-system`, sourced analysis is `research`. A web app is a mixed project: declare `code` primary and give appearance pieces a per-piece `visual` override in `pieces.json`. If nothing about the goal can be run, tested, or measured, it was never a code piece.
