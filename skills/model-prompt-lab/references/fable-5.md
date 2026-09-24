# Claude Fable 5 — Model Profile, Migration Playbook, Long-Run Design

Claude Fable 5 (`claude-fable-5`, generally available; Mythos 5 is the same
underlying model, approved organizations only). The governing idea: **subtraction
and trust**. Fable 5's instruction following is strong enough that one brief
instruction steers a whole behavior class; legacy scaffolding written for 4.x now
degrades output rather than protecting it. Every prompt decision here defaults to
shorter prompts, subtraction over addition, intent over procedure. When in doubt,
remove the instruction and test.

## Effort

The primary intelligence/latency/cost lever. `high` default for most tasks;
`xhigh` for capability-sensitive work; `medium`/`low` for routine or
latency-sensitive work. Lower tiers on Fable 5 often beat prior models' `xhigh`.
Reduce effort if a task completes correctly but takes too long. Only these four
tiers are named — do not assume others exist without confirming current docs.

## API facts (verify at delivery time)

- **Adaptive thinking only.** No extended thinking budgets; any `budget_tokens`
  config is a migration artifact — remove it.
- **Summarized-only thinking output.** The API returns summarized `thinking`
  blocks. If an application needs reasoning visibility, read those structured
  blocks; never prompt the model to echo reasoning in its response text.
- **`refusal` stop reason** on safety-classifier hits. Configure fallback to
  Claude Opus 4.8 (`claude-opus-4-8`).
- Steer with intent, not procedure: "I'm working on X for Y, they need Z"
  connects the task to relevant context instead of guessing.

## Safety classifiers (Fable 5 specific)

Three domains can return `stop_reason: "refusal"`:

1. **Offensive cybersecurity** (exploits, malware, attack tooling). Benign
   security work can also trip it.
2. **Biology and life sciences** (lab methods, molecular mechanisms). Beneficial
   work can also trip it.
3. **Reasoning extraction.** Prompts that tell the model to echo, transcribe, or
   explain its internal reasoning in response text ("show your thinking",
   reflection blocks from older skills). This is the most common self-inflicted
   refusal.

Mitigations: fallback to `claude-opus-4-8`; audit prompts and skills for
reasoning-echo instructions; use structured `thinking` blocks; use a send_to_user
tool for progress surfacing. Fable 5 is explicitly not intended for offensive
cyber or bio/life-sciences work.

## Migration: Opus 4.6/4.7/4.8 → Fable 5

The philosophy is inverted from prior migrations: **subtract first**. Default
action for legacy scaffolding is remove-and-retest, not port-and-keep.

1. **Infrastructure first.** Client timeouts (turns run many minutes at
   high/xhigh), streaming, progress UI, async run checking (scheduled jobs, not
   blocking requests), Opus 4.8 fallback, hide token countdowns from the model.
2. **Hard removals.** `budget_tokens`; reasoning-echo instructions; remaining-token
   countdowns surfaced to the model; prefilled assistant turns.
3. **Deprune candidates** (remove, re-test, restore only on measured regression):
   enumerated behavior lists; anti-laziness language ("be thorough", "don't stop
   early"); forced interim summaries; aggressive subagent-authorization language;
   code-review recall workarounds; vision compensation rituals; tool-triggering
   pressure; "CRITICAL: You MUST" emphasis.
4. **Additions:** only the Fable-5-specific guards the workload needs (see
   snippets below, picked by symptom).
5. **Effort re-evaluation:** usually downward.
6. **Test.** Restore removed items only where regression is measured.

## Symptom → snippet (use as-is or lightly adapted, never stacked by default)

**Overplans on ambiguous tasks at high effort — act when ready:**
```text
When you have enough information to act, act. Do not re-derive facts already established in the conversation, re-litigate a decision the user has already made, or narrate options you will not pursue in user-facing messages. If you are weighing a choice, give a recommendation, not an exhaustive survey. This does not apply to thinking blocks.
```

**Unrequested tidying at higher effort — scope restraint:**
```text
Don't add features, refactor, or introduce abstractions beyond what the task requires. A bug fix doesn't need surrounding cleanup and a one-shot operation usually doesn't need a helper. Don't design for hypothetical future requirements: do the simplest thing that works well. Avoid premature abstraction and half-finished implementations. Don't add error handling, fallbacks, or validation for scenarios that cannot happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).
```

**Human-facing output — brevity and readability:**
```text
Lead with the outcome. Your first sentence after finishing should answer "what happened" or "what did you find": the thing the user would ask for if they said "just give me the TLDR." Supporting detail comes after. Being readable and being concise are different things, and readability matters more. Keep output short by being selective about what you include — drop details that don't change what the reader would do next — not by compressing writing into fragments, abbreviations, arrow chains, or jargon.
```

**Long-running interactive work — checkpoint discipline:**
```text
Pause for the user only when the work genuinely requires them: a destructive or irreversible action, a real scope change, or input that only they can provide. If you hit one of these, ask and end the turn, rather than ending on a promise.
```

**Every autonomous run — evidence-grounded progress (non-optional):**
```text
Before reporting progress, audit each claim against a tool result from this session. Only report work you can point to evidence for; if something is not yet verified, say so explicitly. Report outcomes faithfully: if tests fail, say so with the output; if a step was skipped, say that; when something is done and verified, state it plainly without hedging.
```

**Unattended pipelines only — autonomous system reminder (anti early-stop):**
```text
You are operating autonomously. The user is not watching in real time and cannot answer questions mid-task. For reversible actions that follow from the original request, proceed without asking. Before ending your turn, check your last paragraph. If it is a plan, an analysis, a question, a list of next steps, or a promise about work you have not done, do that work now with tool calls. End your turn only when the task is complete or you are blocked on input only the user can provide.
```

**Users describing problems — assessment vs action:**
```text
When the user is describing a problem, asking a question, or thinking out loud rather than requesting a change, the deliverable is your assessment. Report your findings and stop. Don't apply a fix until they ask for one.
```

**Multi-workstream — delegation:** "Delegate independent subtasks to subagents and
keep working while they run. Intervene if a subagent goes off track or is missing
relevant context." Prefer async communication; prefer long-lived subagents.

**Memory system (recurring/long-horizon agents):**
```text
Store one lesson per file with a one-line summary at the top. Record corrections and confirmed approaches alike, including why they mattered. Don't save what the repo or chat history already records; update an existing note rather than creating a duplicate; delete notes that turn out to be wrong.
```

**Intent framing (user-side pattern):** "I'm working on [the larger task] for
[who it's for]. They need [what the output enables]. With that in mind: [request]."

## Long-run harness design (five pillars)

For multi-hour or multi-day autonomous runs, the prompt should address all five:

1. **Truthful progress** — the evidence-grounded snippet, in every long-run prompt.
2. **Verification cadence** — fresh-context verifier subagents (they get the spec
   and the artifact, not the builder's narrative) beat self-critique. Tie
   intervals to milestones; keep the spec durable and addressable (a file).
3. **Turn-ending discipline** — checkpoint snippet for interactive work;
   autonomous-reminder snippet for unattended pipelines. Rare early-stop recovery:
   a bare "continue" or "go ahead and do it end to end" resumes a stalled run —
   build that nudge into pipeline retry logic.
4. **Memory across runs** — writable Markdown directory, one lesson per file,
   hygiene rules in the prompt (don't duplicate the repo, update rather than
   duplicate, delete wrong notes).
5. **Infrastructure** — timeouts, streaming, progress UI, async checking via
   scheduled jobs, Opus 4.8 fallback.

## Known behavioral deltas vs Opus 4.8

- Overplanning on ambiguous tasks at high effort → act-when-ready snippet.
- Tidying/refactoring beyond the ask → scope restraint.
- Fabricated status on long runs → evidence-grounded progress nearly eliminates it.
- Occasional unrequested actions (drafts emails, makes git branches) →
  assessment-vs-action boundary.
- Rare early stopping deep in long sessions → checkpoints + autonomous reminder.
- Context anxiety on token-countdown display → hide countdowns; reassure only if
  they must show.
- Dispatches parallel subagents readily → authorize delegation explicitly, keep
  them long-lived.
- Excellent verification at higher effort → interval-based verifier subagents.
- Working shorthand leaking into final summaries → readability addendum for
  agentic conversations.
- Much higher vision accuracy on dense technical images → provide bash/crop
  affordances instead of transcription rituals.
