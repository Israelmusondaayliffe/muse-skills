---
name: skill-eval-loop
description: "Run an evidence-backed eval loop on a workspace skill: build trigger suites (ten positive, ten near-miss negatives), functional checks, and rubrics; execute runs against supplied case and rubric evidence with regression comparison to a pinned baseline; stage bounded candidate repairs and promote only with explicit approval. Use when a skill needs regression testing, a pinned baseline, candidate comparison, or a staged repair with approval-gated promotion. Never invents results — evidence is supplied and validated, not synthesized."
---

# Skill Eval Loop

## Purpose

Persistent local baselines and bounded repair cycles for workspace skills. Deterministic state (fingerprints, receipts, diffs) lives under this skill's `state/` directory; judgment (case results, rubric evidence, repairs) comes from you or a subagent and is validated, never invented. There is no external analyzer here: evaluation is always local, and the script records `evaluator_status: unavailable` rather than inventing a score.

## Router

Route the request to exactly one phase. Keep evaluation, judgment, and source promotion separate so a candidate cannot approve its own change.

| Phase | When | Procedure |
|---|---|---|
| `suite` | New trigger corpus, trigger cases, functional checks, or rubric needed | Build per Phase 1 below |
| `run` | Regression check, candidate comparison, baseline pinning, or receipt inspection | Run per Phase 2 below |
| `repair` | A failed or needs-review receipt needs the smallest tested fix | Stage per Phase 3 below |

End-to-end request: Phase 1 → Phase 2 (manual run + independent rubric) → pin a passing baseline → Phase 3 only if needed. After each validated phase, return to this router before the next one.

## Phase 1 — Suite builder

1. Read the target skill's `SKILL.md`, scripts, assets, and references. Do not edit the target.
2. Copy `assets/suite-template.json` into the target state directory made by `init` (below), and set its `target` to the absolute target path.
3. Add at least ten realistic `should_trigger: true` cases and ten near-miss `should_trigger: false` cases: realistic language, typos, adjacent intents. These judge the skill's trigger description, not its content.
4. Add functional cases whose pass condition is observable from files or commands.
5. Add rubric criteria only when each names an external source, the original brief, or a fixed checklist as ground truth.
6. Keep case IDs stable across versions; IDs must be unique across trigger, functional, and rubric groups.
7. Validate before any run:
   ```bash
   python3 scripts/skill_eval_loop.py init ~/workspace/skills/<target-skill>
   python3 scripts/skill_eval_loop.py validate-suite <target-state-dir>/suite.json
   ```

Never write assertions that merely check a file exists. Never let the skill author define success after seeing candidate output.

## Phase 2 — Regression run

1. Obtain real case results and independent rubric results. If you execute the cases yourself (or via a subagent), record each as `{id, passed, evidence}` where `evidence` is the actual observation (command output excerpt, file content, observed behavior). Missing results stay missing and block a pass.
2. Run without editing the target:
   ```bash
   python3 scripts/skill_eval_loop.py run ~/workspace/skills/<target-skill> \
     --case-results /path/to/cases.json --rubric-results /path/to/rubric.json [--token-usage N]
   ```
   For a staged candidate: add `--candidate <staged-path>`.
3. Inspect the run directory's `receipt.json` (status source), `diff.json` (baseline comparison), `cases.json`, and `rubric.json` — not just console output.
4. Pin only a `passed` receipt:
   ```bash
   python3 scripts/skill_eval_loop.py pin-baseline ~/workspace/skills/<target-skill> RUN_ID
   ```

Stop on: missing ground truth, repeated failure signature, exhausted limits (`max_iterations`, `max_minutes`, `max_tokens`), stale source fingerprint, or cancelled approval. Never widen limits silently. Report exactly which evidence is missing.

## Phase 3 — Repair cycle

1. Require a failed (`needs_repair`) or `needs_review` receipt with specific evidence. Read the receipt's `errors` and diff before staging.
2. Stage the current target — this is the only place candidate edits begin:
   ```bash
   python3 scripts/skill_eval_loop.py stage ~/workspace/skills/<target-skill>
   ```
   Record the staged path and the source fingerprint.
3. Make the smallest change connected to the failure, in the staged copy only. For skill-authoring questions, the `skill-creator` skill owns the authoring patterns.
4. Re-run the full suite against the staged candidate (`run --candidate <staged-path>`). Stop if the failure signature repeats, limits are exhausted, or another case regresses.
5. After the candidate receipt passes, pin it, then ask the user for explicit approval.
6. Promote only with the exact staged path, the passing run ID, the approval token, and the expected source fingerprint:
   ```bash
   python3 scripts/skill_eval_loop.py promote ~/workspace/skills/<target-skill> <staged-path> RUN_ID \
     --approval APPROVED --expected-source-fingerprint FP
   ```
   Promotion backs up the current target first, refuses stale fingerprints, and refuses unless the exact passing run is pinned as baseline.

## Scheduling

Manual end-to-end success first. Recurring evals are owned by LoopKit: `loopkit` builds the bounded contract, and `cron` owns the schedule. This skill never schedules itself.

## Tooling

Script: `scripts/skill_eval_loop.py` (standard library only). State root: `~/workspace/skills/skill-eval-loop/state/` (override with `SKILL_EVAL_LOOP_STATE`). Subcommands: `init`, `validate-suite`, `run`, `pin-baseline`, `stage`, `promote`.

## Operating Rules

1. The model executing the phases is Muse (this runtime). There are no platform hooks or slash commands — the gates above are procedures you run, not automated triggers.
2. Never synthesize case or rubric results. Supplied evidence must come from a real run you or a subagent performed, or from files the user handed you.
3. Never edit a target except through `stage` → fix staged copy → `run --candidate` → pin → explicit approval → `promote`.
4. Do not evaluate this skill's own reserved siblings (harness-engineering, agent-ops, capability-operator, loopkit, gauntlet, writing-quality) as targets without the user's explicit request.
5. When evidence contradicts the description (e.g., trigger cases fire on near-misses), report the mismatch exactly instead of softening the suite.
