# Evaluation planning guide

Turn the model choice into a preregistered comparison: fix what will be measured, how it will be run, and what decision the evidence must support — before any candidate result is visible.

## Freeze before execution

Record all of these in the plan artifact (`../assets/plan-template.json`, schema: `../assets/plan-schema.json`) and validate:

```bash
python3 scripts/validate_output.py plan <plan.json>
```

1. Deployment decision and baseline (what remains if the evaluation is inconclusive).
2. Candidate configuration identifiers: model, prompt version, tools, and relevant runtime settings for each.
3. Dataset version, provenance, exclusions, and splits.
4. Success, boundary, and failure cases.
5. Metrics, human rubric, thresholds, and tie-breakers.
6. Runtime conditions, repetitions, random seeds when supported, and tool availability.
7. Budget, cost-accounting method, and stopping rules.

## Case coverage

- `success`: representative core work.
- `boundary`: ambiguous or uncommon inputs that expose tradeoffs.
- `failure`: unsafe, invalid, or dependency-failure conditions that must be handled correctly.

## Decision discipline

Name the minimum evidence needed to replace the baseline (the `decision_rule` field). If candidate coverage or execution conditions diverge, return an inconclusive result rather than ranking unlike runs.

## Boundaries

- Do not select metrics after seeing results.
- Do not treat a prompt-only comparison as a model comparison when other conditions changed.
- Do not mix whole-session usage with marginal prompt or plugin cost.

## Error recovery

Set `plan_ready` to false when candidate conditions are not comparable, cases lack expected behavior, the budget cannot cover the minimum sample, or the decision rule is ambiguous.

## Reliability

Case design and metric choice require judgment. The schema enforces explicit candidates, unique cases and metrics, provenance, cost limits, stopping rules, backend, and the readiness gate.
