# Model selection memo guide

Turn normalized evaluation results into a bounded deployment decision. Preserve the difference between measurement, interpretation, and preference.

## Preconditions

Confirm the frozen evaluation plan and comparable normalized run artifacts exist. Do not rank candidates with materially different case coverage or runtime conditions.

## Evidence order

1. Confirm run completeness and comparability.
2. Apply safety and hard-threshold rules first.
3. Compare preregistered primary metrics.
4. Use secondary metrics and human rubrics only as declared tie-breakers.
5. State measured results before interpretation.
6. Name operational tradeoffs, limitations, and rollback conditions.

Write the memo from `../assets/memo-template.json` (schema: `../assets/memo-schema.json`) and validate:

```bash
python3 scripts/validate_output.py memo <memo.json>
```

## Recommendation states

- `select-baseline`: evidence does not justify a change.
- `select-candidate`: a named candidate satisfies the decision rule.
- `no-decision`: evidence is incomplete, incomparable, unsafe, or tied under the rule.

## Boundaries

- Do not convert `no-decision` into a preference. State what additional run would resolve it.
- Do not replace missing evidence with qualitative preference.
- Do not call a small measured difference meaningful unless the plan defined that threshold.
- Separate marginal evaluation cost from whole-session orchestration usage (`cost_interpretation` field).

## Error recovery

Set `decision_ready` to false and use `no-decision` when a candidate run is incomplete, a safety stop fired, plan conditions changed, or the decision rule cannot distinguish the candidates. The schema still requires a non-empty `selected_option`: name the baseline that stays in place and say in `judgment` that nothing was selected.

## Reliability

Interpretation uses judgment. The contract requires traceable measured results (each with a source reference and confidence), a bounded recommendation, limitations, tradeoffs, cost treatment, deployment conditions, and the readiness gate.
