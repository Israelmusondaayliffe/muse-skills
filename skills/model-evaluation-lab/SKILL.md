---
name: model-evaluation-lab
description: "Run reproducible model evaluations: freeze an evaluation plan (decision, baseline, candidates, cases, metrics, budget, stopping rules), execute or normalize benchmark runs, and write a model-selection memo that separates measurement from judgment. Use when comparing models, prompts, agents, tool behavior, or deployment configurations, or when a deployment decision needs an evidence-backed recommendation."
---

# Model Evaluation Lab

Replace model-choice impressions with a frozen plan, reproducible run records, normalized results, and a decision memo that separates measurement from judgment. The work is finished when the requested stage's artifact validates and its conclusion follows from the evidence, including "no decision" when the evidence cannot separate the candidates.

## Start here

1. **Inventory the artifacts.** Record what exists: decision question, baseline, candidates, frozen plan, plan hash, raw results, normalized results, prior memo. Open each file; do not assume an artifact exists.
2. **Check the plan hash** whenever a plan and results are both present. Recompute it from the plan file and compare it with the `plan_hash` in the results. On a mismatch, stop and report it; results from a different plan cannot be judged against this one.
3. **Route by artifact state** (table below). Write the routing record from `assets/router-template.json` and validate it when running more than one stage.
4. **Produce and validate the stage artifact** with `scripts/validate_output.py`.
5. **Deliver** the plain-language outcome plus the validated artifacts.

A frozen plan plus supplied raw results authorizes normalize and decide. Do not re-plan, re-interview, or rerun cases in that case. Ask only for inputs no file holds: the decision, the baseline, what changes between candidates, or backend authorization.

| Artifact state | Stage | Reference |
|---|---|---|
| No frozen plan, or the user asks what to compare | `plan`: freeze decision, baseline, candidates, cases, metrics, budget, backend, stopping rules | `references/plan-guide.md` |
| Frozen plan, no raw results, backend authorized | `execute` | `references/run-guide.md` |
| Frozen plan, no backend available | `blocked` handoff | `references/run-guide.md` |
| Raw case results, no normalized run | `normalize` | `references/run-guide.md` |
| Normalized run(s) | `decide`: memo | `references/memo-guide.md` |
| Memo present | Report decision-ready state, or route a requested re-evaluation to `plan` | `references/workflow.md` |

## Commands

With `SKILL=~/workspace/skills/model-evaluation-lab` (or this skill's actual folder). This self-check runs from any directory and writes nothing:

```bash
python3 "$SKILL/scripts/validate_output.py" plan "$SKILL/assets/plan-template.json"
```

For your own files:

- Plan hash: `python3 -c "import hashlib,sys;print('sha256:'+hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" plan.json`
- Normalize: `python3 "$SKILL/scripts/normalize_results.py" raw.json normalized.json` (on bad input it prints the errors as JSON to stderr and exits 2)
- Validate any stage: `python3 "$SKILL/scripts/validate_output.py" <router|plan|run|blocked|memo> ARTIFACT.json`

Write new artifacts under `~/workspace/evals/<run-id>/` or the folder the user named. Do not overwrite supplied plan or raw files.

## Worked example (illustrative, synthetic)

Request: "Here is our frozen plan and the raw results for two summarization prompts. Pick the winner."

- Inventory: plan, raw results. The recomputed plan hash matches.
- Normalize: each candidate's raw file normalizes and validates with every case present. But the two `environment` fields show that the candidate prompt ran on dataset version 3 while the baseline ran on version 2. The validator cannot see this; you have to read the records. The candidate's higher mean score is therefore not a comparison.
- Judgment: the frozen rule compares candidates on identical cases. Different dataset versions break comparability, whatever the scores say. A tempting shortcut is to compare only the overlapping cases. That is a post-hoc metric change, so it is not allowed.
- Memo: `recommendation: "no-decision"`, `decision_ready: false`. `selected_option` names the baseline that stays in place, because the schema requires a non-empty string, and the judgment says so. `limitations` names the rerun that resolves it: the baseline on dataset v3 with the same environment.

A wrong version would select the higher-scoring prompt, drop the mismatched cases after seeing results, invent the missing baseline scores, or edit the plan to fit the data.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| Recomputed plan hash differs from the results' `plan_hash` | Plan edited after the run, or results from another plan | Report both hashes; ask which plan governed | immediately; do not decide on mismatched evidence |
| Normalizer exits 2 | A case is missing a required field or has a negative or non-numeric value | Read the JSON error; fix only formatting (never values) and rerun | the fix would change a measured value; report the bad record |
| `execution_status: "partial"` | Execution errors or unequal case coverage | Keep the successful records; write a `no-decision` memo naming the rerun | always, for selection; never fill missing cases |
| No authorized backend for a requested run | No endpoint, credential, or runner | Write the blocked handoff from `assets/blocked-template.json` and validate it | at the handoff; never fabricate results |
| A safety stop fired | Frozen safety rule triggered | Stop the run; record the event; memo is `no-decision` or `select-baseline` per the rule | immediately |
| The decision, baseline, or candidate difference is unstated | Missing user input | Ask for that one item; plan nothing else yet | the user answers |

## Completion

- **Decided:** a validated memo whose recommendation follows the frozen decision rule, with measured results cited to the normalized run and judgment stated separately.
- **No decision:** a validated memo with `no-decision`, `decision_ready: false`, the reason, and the exact additional run that would resolve it. This is a valid finished result.
- **Blocked:** a validated blocked handoff (plan hash, backend requirement, case count, safety stops, missing tools by name only) and every stage that could run without the backend.

## Execution backends

Choose exactly one per evaluation and record it in the frozen plan:

- **Local harness.** A script on this VM calls the endpoint(s) and records raw case results in the raw-result contract. Credentials come only from an already-connected credential the user approved for this evaluation; never write secrets into files or logs.
- **Subagent execution.** A subagent receives the frozen case pack (cases, candidate configs, raw-result contract, safety stops) and returns raw JSON. It must not see other candidates' results or alter the plan.
- **External authorized runner.** Export the frozen plan and require the raw-result contract on return.
- **No backend.** Planning, validation, and normalization of supplied results stay available. A requested run gets the blocked handoff instead of fabricated results.

## Pre-stage checks

- **Before planning:** the decision is one sentence with the baseline that remains if the result is inconclusive; candidates are named precisely (model, prompt version, tools, runtime settings); the user confirmed the minimum evidence that would justify replacing the baseline.
- **Before executing:** the plan is frozen and validated, `plan_ready` is true, the hash is recorded, exactly one backend is authorized, and the safety stops are known.
- **Before the memo:** results share plan hash, case coverage, and environment. If they do not, the memo is `no-decision`.

## Companion skills

All optional; missing companions do not block any stage. `model-prompt-lab` for prompt-focused case design; `data-storytelling-studio` for decision-facing charts from normalized results; `knowledge-work-superpowers` for evidence planning and delivery of the final artifact; `writing-quality` for a shared memo's prose. No remote dataset or job-tracking companion is available; backends are the three above.

## Output contract

- Each stage produces a JSON artifact matching its schema (`assets/*-schema.json`; templates in `assets/*-template.json`). Validation is required.
- Raw results use the raw-result contract in `references/run-guide.md`; normalized runs use `assets/run-schema.json`.
- Working artifacts are evidence, not deliverables. A memo the user wants to share is also written as a readable document (to `~/workspace/your_files/` or a named folder), backed by the validated memo JSON.

## Operating rules

1. Never invent executions, scores, latency, cost, safety outcomes, a selection, or a winner.
2. Freeze the plan before any candidate result is visible. No post-hoc metrics, added cases, or plan edits to favor a candidate.
3. Do not rank candidates with different case coverage or runtime conditions. Call small differences meaningless unless the plan defined a threshold.
4. Separate measured results from judgment. Report marginal candidate request cost separately from whole-session orchestration usage.
5. If a prerequisite is missing, set `handoff_ready` to false, name the missing input, and route back to the earliest stage that can create it.
