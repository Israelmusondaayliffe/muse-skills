---
name: model-evaluation-lab
description: "Run reproducible model evaluations: freeze an evaluation plan (decision, baseline, candidates, cases, metrics, budget, stopping rules), execute or normalize benchmark runs, and write a model-selection memo that separates measurement from judgment. Use when comparing models, prompts, agents, tool behavior, or deployment configurations, or when a deployment decision needs an evidence-backed recommendation."
---

# Model Evaluation Lab

## Purpose

Replace model-choice impressions with a fixed plan, reproducible run records, normalized results, and a deployment decision with explicit limitations. The skill runs as four stages with a routing front door. Muse itself performs the routing — there are no platform hooks here; the checklists below are run as procedures.

## Stages

Pick the entry stage from artifact state (see `references/workflow.md` for the full routing procedure):

| Stage | What it does | Reference | Artifact |
|---|---|---|---|
| `router` | Front door: inventory request and artifacts, select the next stage or stop on a missing prerequisite | `references/workflow.md` | routing record |
| `plan` | Freeze the decision, baseline, candidates, cases, metrics, budget, backend, and stopping rules before results are visible | `references/plan-guide.md` | evaluation plan |
| `execute` / `normalize` | Run the frozen plan on an authorized backend, or normalize supplied raw results into the stable comparison schema | `references/run-guide.md` | normalized run |
| `decide` | Test evidence against the preregistered decision rule; produce a memo that separates measurement from judgment | `references/memo-guide.md` | selection memo |

For a full evaluation, return to the router after each validated stage and choose the next stage from fresh artifact state.

## Workflow

1. **Inventory.** Record what exists: the decision question, baseline, candidates, frozen plan, plan hash, raw results, normalized results, prior memo. If the user has not stated the decision, the baseline, or what changes between candidates, ask — never invent them.
2. **Route.** Classify the request as `plan`, `execute`, `normalize`, `decide`, or `full-workflow` per `references/workflow.md`. Write the routing record to JSON (template: `assets/router-template.json`) and validate it before acting on it.
3. **Plan (never skipped).** With the user, freeze every field in `references/plan-guide.md`, write the plan JSON (template: `assets/plan-template.json`), validate it, and compute the plan hash:
   ```bash
   python3 -c "import hashlib;print('sha256:'+hashlib.sha256(open('plan.json','rb').read()).hexdigest())"
   ```
   Never select metrics after seeing results. Never compare candidates whose conditions changed mid-run as if they were identical.
4. **Execute or normalize.** If completed raw case results were supplied, normalize them:
   ```bash
   python3 scripts/normalize_results.py raw.json normalized.json
   ```
   Otherwise run the frozen plan on an authorized backend (see Execution Backends). Save raw case-level records before aggregation, then normalize and validate. Never add cases after results are visible.
5. **Decide.** Confirm run completeness and comparability, apply the frozen decision rule in evidence order (`references/memo-guide.md`), write the memo JSON (template: `assets/memo-template.json`), and validate it. Route human-facing prose through the `writing-quality` skill if the memo will be shared.
6. **Deliver.** Summarize the outcome in plain language plus the validated artifacts. Decision memos meant for others are delivered as a readable document; the JSON artifacts are the machine-checked evidence trail.

Validate every stage artifact with:
```bash
python3 scripts/validate_output.py <router|plan|run|blocked|memo> <artifact.json>
```

## Execution Backends

Choose exactly one per evaluation and record it in the frozen plan:

- **Local harness.** A script on this VM calls the model endpoint(s) and records raw case results in the raw-result contract. Use when the endpoint is reachable reproducibly from here. API credentials come only from an already-connected credential the user approved for this evaluation; never paste secrets into files or logs.
- **Subagent execution.** Spawn a subagent with the frozen case pack (cases, candidate configs, raw-result contract, safety stops) and have it execute cases and return raw JSON. Same contract applies; the subagent must not see candidate results from other runs or alter the plan.
- **External authorized runner.** Export the frozen plan and require the stable raw-result contract on return. Use when credentials or production infrastructure must stay outside this VM.
- **No backend.** Planning, schema validation, and normalization of supplied raw results stay available. A requested run with no authorized backend gets an execution-blocked handoff instead of fabricated results (template: `assets/blocked-template.json`; validator: `scripts/validate_output.py blocked <handoff.json>`).

## Pre-Stage Checklists

(Run as procedures, not as platform hooks.)

**Before planning:**
- [ ] The deployment decision is stated in one sentence, with the baseline that remains if the evaluation is inconclusive.
- [ ] Candidate configurations are named precisely (model, prompt version, tools, runtime settings) and are comparable.
- [ ] The user has confirmed the minimum evidence that would justify replacing the baseline.

**Before executing:**
- [ ] The plan is frozen and validated, `plan_ready` is true, and the plan hash is recorded.
- [ ] Exactly one execution backend is authorized and named in the plan.
- [ ] The frozen safety stops are understood (stop on any safety event; stop when candidate coverage or environment conditions diverge).

**Before writing the decision memo:**
- [ ] Normalized results are complete and comparable (same plan hash, case coverage, environment).
- [ ] No partial, incomparable, or unsafe results are being ranked.
- [ ] If evidence cannot distinguish the candidates, the recommendation is `no-decision` with the additional run that would resolve it.

## Companion Skills on Hatch

All optional. Missing companions do not block any stage.

- **model-prompt-lab:** prompt-focused case design, prompt construction, migration test cases.
- **data-storytelling-studio:** decision-facing charts and executive readouts from normalized results.
- **knowledge-work-superpowers:** evidence planning, staged execution, review, and delivery of the final decision artifact.
- **writing-quality:** final prose validation for a shared memo.
- A remote dataset/job/run-tracking companion (Hugging Face-style) is **not** available in this workspace. Backend options are the local harness, subagent execution, or an external authorized runner the user names.

## Output Contract

- Each stage produces a JSON artifact matching its schema (`assets/*-schema.json`; templates in `assets/*-template.json`). Validation is required, not optional.
- Raw results always use the raw-result contract in `references/run-guide.md`; normalized runs use `assets/run-schema.json`.
- Working artifacts (plans, raw results, normalized runs, routing records, handoffs) live in `~/workspace/evals/<run-id>/` and are treated as evidence, not deliverables.
- A memo the user wants to share is written as a readable document to `~/workspace/your_files/` (or a goal's `files/` directory when the work serves a goal), backed by the validated `memo` artifact.

## Operating Rules

1. Ask the user for the input the stage needs (decision, candidates, budget, backend authorization). Never invent user-specific details, results, or costs.
2. Freeze the plan before any candidate result is visible. No post-hoc metrics, no added cases, no plan edits to favor a candidate.
3. Do not execute a benchmark without a frozen plan. Do not write a selection memo from partial or incomparable normalized results.
4. Never invent executions, scores, latency, cost, safety outcomes, a selection, or a winner. When execution is blocked, say so and produce the handoff.
5. Separate measured results from judgment. Report marginal candidate request cost separately from whole-session orchestration usage.
6. Do not rank candidates with materially different case coverage or runtime conditions. Call small differences meaningless unless the plan defined that threshold.
7. If a routing prerequisite is missing, set `handoff_ready` to false, name the missing input, and route back to the earliest stage that can create it. Do not guess that an artifact exists.
