---
name: model-prompt-lab
description: Design, build, migrate, and diagnose production LLM system prompts for GPT-5.x, Claude Fable 5 / Mythos 5, and GPT-6 Astra; design reproducible prompt benchmarks; apply a frontier working-process contract (solve, build, review, learn). Use for production prompt engineering, model migration audits, prompt troubleshooting, evaluation design, and hard messy problems needing disciplined process.
---

# Model Prompt Lab

A router for production prompt work. Four prompt operations plus one working-process mode:

| Operation | Trigger | Reference |
|---|---|---|
| **Build** | "write a system prompt", "prompt for X", GPT Builder instructions, Responses API config | `references/build-prompt.md` |
| **Migrate** | "migrate prompt from A to B", "update for 5.6", port between ChatGPT/API surfaces | `references/migrate.md` |
| **Diagnose** | prompt misbehaves: too brief, approval noise, scope drift, early stopping, refusal, format drift | `references/diagnose.md` |
| **Benchmark** | compare prompts, decide if a change is production-ready, eval design | `references/benchmark.md` |
| **Fable mode** | explicit "fable mode" / "work like the big model" / "run the review", or a hard messy problem | `references/fable-mode.md` |

Model profiles (load before any build/migrate/diagnose):

| Model | Reference | Notes |
|---|---|---|
| GPT-5.6 (`gpt-5.6-sol` / `-terra` / `-luna`) | `references/gpt-5-6.md` | Current GPT default route |
| GPT-5.4 | `references/gpt-5-4.md` | Legacy and migration route |
| Claude Fable 5 / Mythos 5 (`claude-fable-5`) | `references/fable-5.md` | Current Claude route |
| Claude Fable 5.1 | `references/fable-5-1.md` | Overlay on the Fable 5 profile |
| GPT-6 Astra | `references/gpt-6-astra.md` | Evidence-boundary rules (no invented facts) |

## Start here

1. Name the deliverable: a copyable prompt, a migration ledger plus rewrite, a diagnosis with a fix, or a benchmark specification. A request to "fix" or "migrate" with the rewrite authorized ends in the rewritten prompt, not only an audit.
2. Pick one operation from the table and the target model's profile, and read that profile before editing. If the target model is not in the profile table, say so and work from its owner's docs; do not borrow another model's parameters.
3. Read the whole supplied prompt and config. List the output contract (fields, format, length limits) and the invariants first; these survive every edit.

## 1. Source verification (before any build or migration)

Model behavior, slugs, parameters, pricing, and availability change. Do not state
unstable model behavior as current without a live check.

1. If the task depends on a model string, API parameter, effort enum, pricing, or
   availability, check the owning documentation now (OpenAI platform docs for GPT,
   Anthropic docs for Claude) with web search / page-text fetch.
2. If the owning docs cannot be reached, state exactly what could not be verified
   and deliver against the reference file, flagged as such.
3. Benchmark design and migration audits never claim a model run occurred; they
   produce plans and ledgers, not results.

## 2. Extract the brief (all operations)

Before doing the work, record: the user job, target model, prompt surface
(ChatGPT, GPT Builder, Responses API, Chat Completions API, custom agent harness),
available tools, output contract, latency/cost constraints, and the source prompt
(if one was supplied). If a required item is missing and you cannot infer it
reliably, ask the user — never invent their business details, names, samples, or
credentials.

## 3. Run the operation

- **Build:** read the model profile, follow `references/build-prompt.md`, save the
  prompt in your working folder `$OUT`, and from this skill's directory run
  `python3 scripts/validate_prompt.py "$OUT/prompt.md"` (GPT-5.6 checks; the
  repetition and XML checks are also useful on other prompts). Report its output
  as run. A `PASS` with warnings still needs each warning addressed or explained.
- **Migrate:** audit first with `references/migrate.md` (read-only unless the
  user authorizes a rewrite). Migration preserves the user job but never preserves
  unsupported parameters.
- **Diagnose:** work through `references/diagnose.md` — check for instruction
  duplication *before* adding anything.
- **Benchmark:** follow `references/benchmark.md`. Produce a validated
  specification. Do not fill result fields from expectation.

## Worked example (illustrative)

Request: "Our GPT-5.6 billing assistant gives answers so short that customers write back. Fix the prompt." The prompt says "Be concise." under Constraints, "Keep answers short. Answer in as few words as possible." beside it, and "Be brief." under Output.

- Operation: Diagnose, profile `references/gpt-5-6.md`.
- Duplication check first: four brevity nudges stacked on a model that is already concise by default. `validate_prompt.py` flags "Broad brevity instruction found without a must-include contract".
- Category: TOO_BRIEF. The root cause is stacked instructions, not a missing one, so the fix removes before it adds. Keep one line: "Keep answers short, but always include the amount, the date it applies, and the next step the customer takes." Optionally set `text.verbosity` instead of prose nudges.
- Test scenario: "Why was I charged $49 on 3 September?" should now return the charge reason, the date and the action, without a follow-up question.

A wrong version would add a fifth instruction ("be thorough"), rewrite the whole prompt, or claim the fix improves satisfaction scores without a run.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| Owner docs cannot be reached | Network or access | Deliver against the profile and mark each dependent fact unverified | never state an unverified slug, price or parameter as current |
| Target model not in the profiles | New or third-party model | Use its official docs; keep the prompt model-neutral where unsure | docs are unavailable and a parameter is load-bearing; name it as open |
| A source parameter has no equivalent on the target | Unsupported parameter | Drop it and log it in the ledger | never copy it across |
| `validate_prompt.py` warns about a missing GPT-5.6 model string on a non-GPT prompt | GPT-specific check | Note that the check does not apply | never; the other checks still count |
| User asks whether the new prompt is better | No comparable runs exist | Deliver a benchmark specification with empty result fields | always; never report a result that was not run |

## Completion

- **Delivered:** the requested prompt, ledger, diagnosis or benchmark specification is complete, any validator output is shown as run, and unverified facts are marked.
- **Partial:** the rewrite is done but a load-bearing fact (model string, effort enum, tool behavior) could not be verified. Say so first and list the open items.
- A migration is not "tested" until the same eval ran on both versions; say which evals remain.

## 4. Output contract

- If the prompt itself is the deliverable, return it in its own code block,
  copy-pasteable for its surface, with only material assumptions and verification
  limits outside it.
- Use the section templates in `references/build-prompt.md` for the surrounding
  delivery (model config, structure applied, validation results).
- Do not copy private histories, benchmark receipts, voice guides, or account
  configuration into the prompt.

## Operating rules

1. Subtraction first. Newer models degrade under older-model scaffolding; remove
   and re-test rather than port-and-keep.
2. State each instruction once. Repetition is a behavior bug, not emphasis.
3. Absolute words (ALWAYS, NEVER, must) are for invariants: safety rules,
   required output fields, forbidden actions. Judgment calls get decision rules:
   a condition and the response.
4. Benchmarks and migrations produce plans and ledgers — never claim a run
   happened before it has.
5. Fable mode is process, not knowledge: the five laws and the mode procedures
   load on explicit invocation, or on hard messy problems where a quality bar is
   otherwise improvised.
6. Missing companions do not block workflows; note what you used in their place.
7. Do not reference Codex/Claude Code/Claude Cowork commands, slash commands,
   hooks (PreCompact, SessionStart), or plugin manifests. All procedures here run
   on this host: shell, filesystem, web, browser delegation, cron, subagents.
