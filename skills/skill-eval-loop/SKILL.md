---
name: skill-eval-loop
description: "Run an evidence-backed eval loop on a workspace skill: build trigger suites (ten positive, ten near-miss negatives), functional checks, and rubrics; execute runs against supplied case and rubric evidence with regression comparison to a pinned baseline; stage bounded candidate repairs and promote only with explicit approval. Use when a skill needs regression testing, a pinned baseline, candidate comparison, or a staged repair with approval-gated promotion. Never invents results. Evidence is supplied and validated, not synthesized."
---

# Skill Eval Loop

Give a workspace skill a pinned baseline, a regression verdict, or a tested repair. The finished result is a receipt the script wrote (`receipt.json` is the status source), plus what it means: passed and pinned, regressed with the failing case ids, or blocked on named missing evidence. Deterministic work (fingerprints, receipts, diffs) is the script's; judgment (case results, rubric evidence, repairs) comes from you or a subagent and is validated, never invented. There is no external analyzer: receipts record `evaluator_status: unavailable` and no score.

## Start here

Run commands from this skill folder. State lives at `~/workspace/skill-eval-loop/state/` (override with `--state-root` or `SKILL_EVAL_LOOP_STATE`).

1. **Read the target** skill's `SKILL.md`, scripts, and references. Never edit the target outside the repair flow.
2. **Pick the phase from what already exists:**

| What exists | Phase | First command |
|---|---|---|
| No suite for the target | Suite | `python3 scripts/skill_eval_loop.py init <target-dir>` |
| Valid suite, results in hand (from your own run or supplied files) | Run | `run <target-dir> --case-results <cases.json> --rubric-results <rubric.json>` |
| Valid suite, no results yet | Run, after executing the cases | Execute each case, record `{id, passed, evidence}`, then `run` |
| Receipt `needs_repair` or `needs_review` | Repair | read `receipt.json` `errors` and `diff.json`, then `stage <target-dir>` |

3. `init` prints the target's state folder and `suite.json`. The suite's `target` is already set there; add cases to that file, then `validate-suite <that suite.json>`.

## Suite

- At least ten `should_trigger: true` cases and ten near-miss `should_trigger: false` cases in realistic language (typos, adjacent intents). They test the trigger description, not the content.
- Functional cases whose pass condition is observable from files or command output. Never a bare "file exists".
- Rubric criteria only with named ground truth: an external source, the original brief, or a fixed checklist.
- Stable, unique ids across all three groups. Field rules: `references/suite-schema.md`. Never let the skill author define success after seeing the output.

## Run

1. Obtain real results. If you execute cases yourself or through a subagent, `evidence` is the actual observation (output excerpt, file content). Missing results stay missing; they block a pass. Supplied result files are used as given, never edited.
2. `run <target-dir> --case-results ... --rubric-results ... [--candidate <staged-path>] [--token-usage N]`.
3. Read `receipt.json`, `diff.json`, `cases.json`, and `rubric.json` in the printed run folder, not the console summary.
4. Pin only a `passed` receipt: `pin-baseline <target-dir> <run-id>`.

## Repair

1. Stage the current target: `stage <target-dir>`. Record the staged path and the source fingerprint. Candidate edits happen only in the staged copy.
2. Make the smallest change tied to the failing case ids. For authoring patterns, `skill-creator` advises.
3. Rerun the full suite with `--candidate <staged-path>`. Stop if the failure signature repeats, a limit is exhausted, or another case regresses.
4. Pin the passing candidate run, then ask the user for approval. Promote only with all four: `promote <target-dir> <staged-path> <run-id> --approval APPROVED --expected-source-fingerprint <fp>`. Promotion backs up the target first and refuses stale fingerprints or an unpinned run.

## Worked example (illustrative)

A `csv-tidy` skill has a pinned baseline of 21 of 21 cases. A later run of the unchanged skill, with supplied results, fails `t-neg-07`: "Deduplicate rows in contacts.csv" triggered the skill. The receipt shows `status: needs_repair`, `stop_reason: checks_failed`, `case_pass_rate_delta` about -0.048, `no_regression: false`.

Judgment: the description says "clean ... CSV" broadly, so a dedupe request matches. The repair is to narrow the description in a staged copy (headers and whitespace only; name deduplication as out of scope), not to delete or soften the near-miss case. Report the regression, the failing id, and the proposed staged fix, then wait for approval before `promote`.

A wrong version would fill in a missing result, pin the failing run, edit the suite so it passes, or call the rerun a pass because 20 of 21 is high.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| `suite validation failed` | Too few cases, empty target, duplicate ids, rubric without ground truth | Fix the suite file; rerun `validate-suite` | ground truth for a rubric criterion does not exist |
| `suite target does not match the initialized target` | Suite points at another copy | Set `target` to the initialized path | never |
| `source fingerprint changed after initialization` | Target edited after `init` | Report it; re-`init` only if the user accepts a new baseline | always; a silent re-init hides the change |
| Receipt `needs_review`, `missing_or_invalid_evidence` | Missing, unknown, or duplicate result ids | Name the missing ids; get the real results | the results cannot be produced |
| Receipt `exhausted` | Iteration, time, or token limit, or repeated failure signature | Report the limit; never widen it silently | always |
| `state needs attention` | Legacy state in the package's old `state/` folder, or two roots differ | `state status`; for `migrate`, run `state migrate`; for `conflict`, report both paths | conflict; the user picks one root with `--state-root` |

After migrating, re-run a staged candidate before promoting it: receipts written before migration name legacy staged paths.

## Completion

- **Baseline pinned:** a `passed` receipt and `baseline.json` naming its run id.
- **Regression found:** a receipt with failing case ids and the baseline delta, plus a proposed staged fix. Not a pass.
- **Blocked:** the receipt's `errors` or limit, and exactly which evidence would clear it.
- **Promoted:** only after explicit approval; report the backup path and new fingerprint.

## Operating rules

1. Muse runs these phases as procedures. There are no platform hooks or slash commands here.
2. Never synthesize case or rubric results.
3. Never edit a target except through stage, fix the staged copy, run the candidate, pin, approval, promote.
4. Do not evaluate reserved siblings (harness-engineering, agent-ops, capability-operator, loopkit, gauntlet, writing-quality) without the user's explicit request.
5. When evidence contradicts the description, report the mismatch instead of softening the suite.
6. Recurring evals belong to LoopKit (`loopkit` builds the contract, `cron` owns the schedule) after one manual end-to-end success. This skill never schedules itself.

## Resources

- `scripts/skill_eval_loop.py` (standard library only): `init`, `validate-suite`, `run`, `pin-baseline`, `stage`, `promote`, `state status`, `state migrate`.
- `references/suite-schema.md` (suite and result file fields), `references/ownership-and-state.md` (what this skill owns, state layout), `assets/suite-template.json`, `evals/trigger-evals.json` (this skill's own trigger cases).
