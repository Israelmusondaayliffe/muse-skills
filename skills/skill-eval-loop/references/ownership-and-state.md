# Ownership and state

Skill Eval Loop owns, per target: the suite, run evidence (cases, rubric, diff, trace), the pinned baseline, regression decisions, and staged candidate copies. It does not own the target skill itself and never edits it outside the staged repair flow.

Neighboring owners it can coordinate with:

- **skill-creator** (`skill_creator`): skill authoring patterns; advises on trigger descriptions and SKILL.md fixes during repair.
- **capability-operator**: inventory, overlap analysis, and discoverability across `~/workspace/skills/`.
- **loopkit** + **cron**: recurring eval schedules and sustained loop operations — only after a successful manual end-to-end run.

The local evaluator is complete without any of them. It validates suites and supplied evidence, fingerprints source and candidate, enforces limits and approval gates, compares local baseline pass rates, and writes the terminal receipt. There is no external analyzer on this host; missing enhanced analysis is recorded as `evaluator_status: unavailable` with no invented score or grade.

State lives under `~/workspace/skills/skill-eval-loop/state/`, or `$SKILL_EVAL_LOOP_STATE` when set. Each target gets `targets/<readable-name>-<path-hash>/` containing `state.json`, `suite.json`, `baseline.json`, `runs/<run-id>/` (cases, rubric, diff, receipt, trace), `staging/`, and `backups/`.

Promotion is never part of evaluation. A candidate must be staged, evaluated against the full suite, pinned to a passing run, explicitly approved, and checked against the original source fingerprint before promotion replaces the source. A state-root backup of the source is made first.
