# Benchmark execution and normalization guide

Execute the frozen plan on the authorized backend, or normalize completed case results. Preserve raw evidence, record conditions, and stop when plan comparability breaks.

## Preconditions

Validate that the evaluation plan is frozen and `plan_ready` is true. No execution or normalization proceeds without it.

## Backend routing

- **Local harness:** use when the model endpoint and dataset can be invoked reproducibly on this VM. Keep the runner script with the run artifacts; record the plan hash, model and prompt identifiers, environment, dataset version, tool state, repetitions, and cost-accounting method with the run.
- **Subagent execution:** hand a spawned subagent the frozen case pack (cases, candidate configs, raw-result contract, safety stops). It returns raw JSON only; it does not see other candidates' results and does not alter the plan.
- **External authorized runner:** export the frozen plan and require the stable raw-result contract on return.

## Normalize supplied results

Normalization needs no execution backend:

```bash
python3 scripts/normalize_results.py raw.json normalized.json
python3 scripts/validate_output.py run normalized.json
```

## Raw-result contract

Each case record must include a unique `id`, candidate configuration (`candidate`), pass state (`passed`), numeric `score`, latency in milliseconds (`latency_ms`), and marginal request cost (`cost_usd`). Record failures explicitly — do not encode a failed execution as a score of zero unless the frozen metric defines that treatment.

Raw input object also carries `run_id`, `plan_hash`, `environment`, `metric_name`, and optionally `cases`, `execution_errors`, `expected_case_count`.

## Execution discipline

- Execute every frozen case. Do not add cases after results are visible.
- Save raw case-level results before aggregation, then normalize and validate.
- Mark the run `partial` when an execution fails or coverage differs. Preserve successful raw records, list the failed case identifiers, and require an equivalent rerun before comparison.
- Stop immediately when the plan's safety rule fires.

## No execution backend

Do not block planning, schema validation, or normalization of supplied raw results when no execution backend exists. If a requested run has no authorized local runner, subagent path, or external runner, write an execution-blocked handoff from `../assets/blocked-template.json` (schema: `../assets/blocked-schema.json`) and validate it:

```bash
python3 scripts/validate_output.py blocked <handoff.json>
```

The handoff must contain the frozen plan hash, backend requirement, case count, safety stops, and missing credential names or tools **without their values**. Include an exact rerun command or name the owner who can execute the plan. Mark execution, measured results, model selection, and the winner as incomplete. Do not create raw run records or infer scores, latency, cost, safety results, model selection, or a winner. The validator additionally rejects any artifact that embeds secret-looking values or measured-result fields.

## Handoff gate

The normalized run is comparable only when candidate coverage, plan hash, dataset, environment, and stopping-rule treatment match. A partial run can be preserved but cannot support model selection.
