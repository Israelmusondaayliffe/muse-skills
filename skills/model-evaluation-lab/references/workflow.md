# Evaluation routing workflow

Route every new or multi-stage request through this sequence:

1. No frozen plan, or the user asks what to compare: `plan` stage (build and freeze the evaluation plan).
2. Frozen plan present and cases need execution: `execute` stage (`benchmark execution`).
3. Raw case results present but no checked aggregates: `normalize` stage (normalize supplied results).
4. Comparable normalized results present: `decide` stage (selection memo).
5. Decision memo present: report decision-ready state, or route a requested re-evaluation back to `plan`.

## Classification

- `plan` — a model, prompt, agent, tool, or deployment comparison is new, or candidates/cases/metrics/budget are not yet fixed.
- `execute` — a frozen, validated plan exists and no raw results have been collected.
- `normalize` — completed raw case results were supplied and need validation and aggregation.
- `decide` — comparable normalized runs exist and a deployment, migration, rollback, or no-decision recommendation is needed.
- `full-workflow` — the user asked to take a comparison from a new question through a deployment decision.

## Routing record

Write the routing record using `../assets/router-template.json` (schema: `../assets/router-schema.json`) and validate:

```bash
python3 scripts/validate_output.py router <routing.json>
```

The validator requires one allowed stage, one current state, named prerequisites, a missing-input statement, a next action, and the `handoff_ready` gate.

## Stop rules

- Stop at planning when candidates, cases, metrics, or decision rules are not fixed.
- Stop at execution when candidate coverage or environment conditions diverge.
- Do not rank partial, incomparable, or unsafe results. The decide stage then writes a `no-decision` memo that names the run needed to resolve it (see `memo-guide.md`, Error recovery).

## Error recovery

Set `handoff_ready` to false when the requested stage lacks its prerequisite. Name the missing input and route back to the earliest stage that can create it. Do not guess that an artifact exists.

The router selects the next stage. Each stage owns its domain work and returns a validated artifact to the router.
