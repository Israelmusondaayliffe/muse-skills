# GPT-5.6 — Model Profile and Lean Prompting

Current default route for GPT production prompt work. Read this before building,
migrating, or diagnosing any 5.6 prompt.

## The one idea

GPT-5.6 infers the user's underlying goal and intended level of work from context,
and lean system prompts measurably outperform heavy ones (in OpenAI's internal
coding-agent sample, leaner configs improved scores ~10-15% while cutting tokens
41-66% — directional figures; validate on your own workload). Your job is not to
describe the path; it is to supply what cannot be inferred: domain context, hard
constraints, approval boundaries, success criteria, and which ambiguities should
trigger a question.

## Model strings

| Variant | String | Best for |
|---|---|---|
| Flagship | `gpt-5.6-sol` | Frontier capability |
| Balanced | `gpt-5.6-terra` | Strong performance, lower price |
| Efficient | `gpt-5.6-luna` | High-volume workloads |
| Alias | `gpt-5.6` | Routes to `gpt-5.6-sol` |

Pro mode is `reasoning.mode: "pro"` on any 5.6 model — never invent a pro slug.

## Reasoning effort

`none`, `low`, `medium`, `high`, `xhigh`, `max`. Start from task shape, then test
one level lower:

| Shape | Start |
|---|---|
| Field extraction, triage, short transforms | `none` (keep as latency baseline) |
| Latency-sensitive production | `low` |
| General new work | `medium` (balanced default in both standard and pro modes) |
| Complex analysis, multi-step coding | `high` (only when measured quality gain) |
| Long agentic, reasoning-heavy | `xhigh` |
| Hardest quality-first | `max` (compare against `xhigh`) |

Migration rule: keep the current 5.4/5.5 setting as baseline, then compare the same
setting and one level lower. Do not silently drop a tier.

## The subtraction method

1. Start with a prompt and tool set that already works.
2. Remove one group of instructions, examples, or tools at a time.
3. Re-run the same evals after each removal. Batching removals destroys attribution.
4. Keep the removal if quality holds; restore it if quality drops.

Removable groups: a repeated instruction (keep one statement); an example that no
longer encodes a product requirement or corrects a measured gap; a tool the task
does not need; verbose tool descriptions; a protective block compensating for an
older model's weakness.

Always keep: invariants (safety rules, schema fields, forbidden actions), stated
once; domain context the model cannot infer; hard constraints; approval
boundaries; success criteria.

## Rules that bite

- **Repetition is a behavior bug.** Repeating "ask first / do not mutate / wait for
  approval" causes approval noise for safe, expected actions. Repeating brevity
  nudges stacks with 5.6's already-concise default and produces too-brief answers.
  State each instruction once, in the right section.
- **Describe outcomes, constraints, boundaries — not steps.** Long procedural
  lists narrow 5.6's search space and produce mechanical answers.
- **Ambiguity triggers.** Name which unknowns are worth stopping for: "If the
  target environment is ambiguous, ask before deploying."
- **Stopping conditions.** Every agentic prompt needs an explicit stop rule, e.g.
  "Use the minimum evidence sufficient to answer correctly, cite it precisely,
  then stop."
- **Tool surface stays lean.** Expose only tools the task needs; document each
  tool's expected return fields, types, and error behavior. This matters doubly
  with Programmatic Tool Calling, because the model writes code against those
  return shapes before seeing results.
- **Execution-mode routing** (direct calls / PTC / pro mode / multi-agent) must be
  task-specific. Generic "be efficient" language does not produce the right route.
- **Retrieval budgets** still prevent over- and under-searching.
- **Creative drafting:** keep an explicit guardrail separating source-backed
  facts from creative wording.
- **Short answers:** 5.6 is more concise by default than 5.5. When brevity is
  required, use `text.verbosity` and specify what a short answer must still
  include — required facts, decisions, caveats, next steps — trimming
  introductions and repetition first.

## Suggested prompt structure

Markdown headers, each section short, detail only where it changes behavior:

```text
Role: [1-2 sentences: function, context, job]

# Goal
[user-visible outcome]

# Success criteria
[what must be true before the final answer]

# Constraints
[policy, safety, business, evidence, side-effect limits]

# Autonomy
[one compact approval-boundary policy]

# Output
[sections, length, tone; for short answers, what must still be included]

# Stop rules
[when to retry, fallback, abstain, ask, or stop]
```

`# Personality` and `# Collaboration style` join only for customer-facing or
conversational surfaces. If a section adds nothing, remove it.

## XML blocks: gate them

Use XML blocks only when they earn their place:
- Evals show a specific recurring failure mode the block addresses.
- A high-stakes invariant must be guaranteed (`action_safety`, `citation_rules`).
- A structured output contract is required for downstream parsing.
- A task-specific `<tool_orchestration>` block is needed to route PTC.

Bad reasons: "it worked in our 5.5 prompt", "more feels safer", "just in case".

## API essentials

Use the Responses API for reasoning, tool-calling, and multi-turn workflows. It
carries reasoning pass-through, the phase parameter, native compaction, persisted
reasoning (`reasoning.context`: `auto` / `all_turns` / `current_turn`), Programmatic
Tool Calling, and multi-agent beta.

Caching: implicit still works; explicit mode added; writes are billed 1.25x
uncached input. Track `cached_tokens` and `cache_write_tokens`.

## Safeguards

5.6 runs real-time cyber and biology misuse classifiers on outputs. Expect
occasional blocks and mid-stream pauses on legitimate dual-use work. Prompt
duties: send a stable, privacy-preserving `safety_identifier` for end-user apps;
state the legitimate purpose explicitly in dual-use domains; treat mid-stream
pauses as expected behavior; never attempt to evade classifiers — reframe
legitimate intent instead.

## Small-model note (gpt-5.6-luna)

Put critical rules first; specify execution order when tool use or side effects
matter; use structural scaffolding; separate "do the action" from "report the
action"; define ambiguity behavior explicitly. State-once still applies; smaller
models are literal.
