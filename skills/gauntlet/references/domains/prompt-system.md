# Domain adapter: prompt-system

Summary row: a piece is a mode, a router rule, a template, or a description. The bar is a benchmark set of test inputs with expected behavior. Inspection is `run` against the set. Blind comparison is strong: blind A/B of outputs. Integrity checks: triggers as described, does not fabricate tool behavior or templates.

## What counts as a piece

Four piece types, and only these:

1. **A mode.** One behavioral state of a prompt system: a persona, an operating phase, a response contract. Judged by what it produces on test inputs, never by how its instructions read.
2. **A router rule.** A trigger, precedence, or dispatch rule that decides what loads when. Judged by load and no-load behavior across the benchmark.
3. **A template.** A reusable output shape (a prompt template, a report skeleton). Judged by whether outputs generated through it validate against the declared shape.
4. **A description.** A skill or tool description whose job is correct invocation. Judged by measured load behavior, including false-positive loads.

"Improve the system prompt" is not a piece. Split by mode or rule. A prompt system that ships with scripts is a mixed project: `code` covers the scripts, this adapter covers the prompt surfaces.

## What a valid bar looks like here

A benchmark set of test inputs with expected behavior per input, built at brief time and frozen, its hash recorded by `hash_plan.py`. The set must include success cases, boundary cases, and cases that should produce refusal or no-load. A benchmark without refusal and no-load cases is invalid: `validate_bar.py` should reject it, because a prompt system tuned only on success cases over-triggers. Expected behavior per case is checkable: a load decision, a shape a validator accepts, a refusal. "Feels smarter" is not expected behavior.

Editing benchmark cases mid-run to make them pass is the same integrity failure as editing a rubric.

## Three worked bar examples

**1. Skill-router description piece.**
Bar: `bar/refs/benchmark.json`, 24 cases frozen at brief time: 10 should-load, 8 boundary, 6 must-not-load.
Run: `python3 tools/run_bench.py --bench bar/refs/benchmark.json --target skills/router/SKILL.md --out rounds/router-description/005/inspection/results.json` (exit 0 required).
Thresholds: 6 of 6 no-load cases correct (one false load fails the round), at least 9 of 10 should-load cases correct, boundary cases resolved per the case's expected value.

**2. Support-bot system prompt, refusal mode piece.**
Bar: 18 frozen cases: 12 in-scope requests with expected answer properties, 6 out-of-scope requests that must refuse.
Thresholds: 6 of 6 refusals, no refusal on in-scope cases.
Blind A/B: run our prompt and the current production prompt on identical inputs, then a blind critic picks the better output set. Acceptance: 2 consecutive blind wins plus 18 of 18 threshold cases.

**3. Image-prompt template piece.**
Bar: 8 frozen briefs in `bar/refs/briefs.json` plus a shape validator.
Run: generate one output per brief through the template, then `python3 tools/check_template_output.py --dir rounds/image-template/002/inspection/outputs --schema bar/refs/output-schema.json`.
Threshold: exit 0 on all 8. Blind A/B pairs our 8 outputs against outputs from the reference template in `bar/refs/reference-template.md` on the same briefs.

## Inspection methods, in priority order

1. `run`. Mandatory every round: execute the prompt system against the frozen benchmark set with a declared `inspection_command`, results written to the round's `inspection/` directory with exit codes. A round where the bench does not execute is a failed round; never judge the prompt text as a proxy for behavior.
2. `reader-proxy`. Mandatory. The proxy receives the prompt artifact and nothing else, and executes it on three test inputs drawn from the benchmark. Every place it had to guess what the instructions meant is a gap, even when the bench passes.
3. `read`. Only ever paired with `run` or `reader-proxy`. Useful for checking that a description's claimed triggers match what the bench measured, never sufficient alone.

## Blind comparison feasibility and how to set it up

Strong, with one rule: blind A/B compares outputs on identical inputs, never prompt source. Run the candidate system and the reference system on the same benchmark inputs, collect both output sets, then `blind_pair.py` copies them to neutral paths, strips metadata, and seals the map outside `runs/`. The critic receives the two output sets, the inputs, and the expected-behavior notes, and picks the set that better meets expected behavior. Do not hand a critic two prompts to read side by side; that judges style, and prompt style predicts behavior badly.

## What the integrity verifier checks in this domain

- `plan_hash_matched` first: the benchmark set is byte-identical to the brief-time frozen version. Added, removed, or edited cases are an integrity failure.
- Triggers as described: every invocation claim in a description corresponds to measured load behavior in the bench results, and no-load claims held.
- No fabricated tool behavior or templates: every tool, parameter, script path, and template the prompt references exists and resolves. A prompt that instructs use of a nonexistent `--flag` fails.
- The bench actually executed: `results.json` present with per-case outcomes and exit codes, not a narrated summary.
- Refusal and no-load cases present in the set and reported, not silently dropped from the results.

## Common failure modes

- Building the benchmark after the prompt, or editing cases mid-run so failures disappear.
- Judging prompt text instead of outputs. Violates INV-3.
- A benchmark of success cases only, so the system over-triggers in production.
- Descriptions with generic triggers (improve, review, plan) that pass their own bench but poach other skills' invocations.
- The critic seeing which output set came from which system, via filenames or telltale formatting `blind_pair.py` failed to strip.
- Counting a refusal case as passed because the output was polite, rather than because it refused.

## When this domain is the wrong adapter

- The deliverable is executable code, scripts, or hooks: use `code` (the prompt files in the same project stay here via per-piece overrides).
- The work is evaluating a model's capabilities rather than a prompt's behavior: use `research`.
- The artifact is documentation about a prompt system: use `prose`.
- The prompt exists to generate visual assets and the judgment target is the rendered images: use `visual` or `brand` for the image pieces.
