---
name: writing-for-agents
description: "Use when writing or editing any document an agent consumes: a skill, AGENTS.md, CLAUDE.md, or a document reached by a pointer. Covers context pointers, the two loads, the information hierarchy, completion criteria, splitting, leading words, and pruning, plus skill mechanics (frontmatter, invocation choice, router skills). The packaging differs; the writing does not."
---

Invocation: model or user

## Context pointers

A **context pointer** is a reference held in the agent's context that names some out-of-context material and encodes the condition for reaching it. A skill's description is one; a line in `AGENTS.md` naming a doc is the same object. The pointer's wording, not its target, decides when the agent reaches the material, and how reliably. A must-have target behind a weakly worded pointer is a variance bug: sharpen the wording first, and inline the material only if sharpening fails.

A pointer does two jobs: state what the material is, and list the **branches** (distinct cases the document handles, so different runs take different paths) that should trigger reaching it. Every word of an always-loaded pointer costs on every turn, so it earns even harder pruning than the body:

- Front-load the leading word: the pointer does its triggering work there.
- One trigger per branch. Synonyms that rename a single branch are one branch written twice; collapse them and keep only genuinely distinct branches.
- Cut identity the body already carries.

## The two loads

Every document and pointer you add spends one of two budgets:

- **Context load**: cost of always-loaded material on the agent's window (an `AGENTS.md` line, a skill description, anything in context every turn), spending tokens and attention whether or not it fires.
- **Cognitive load**: cost on the human, who is the index that must remember which documents exist and when to reach for each. Not a cost to minimize: it is the price of human agency. Spend it where human judgement matters, remove it where it does not.

Material reached only through a pointer escapes context load at the price of the pointer's own line; material with no pointer at all rides entirely on cognitive load.

## Information hierarchy

A document is built from **steps** (the ordered actions the agent performs) and **reference** (definitions, rules, facts consulted on demand). The core decision is where each piece sits on the information hierarchy, ranked by how immediately the agent needs the material:

1. **In-file step**: what the agent does, in order. The primary tier.
2. **In-file reference**: consulted on demand. Often a flat peer set (every rule of a review on one rung), which is a fine arrangement, not a smell.
3. **Disclosed reference**: pushed into a separate file behind a context pointer, loaded only when the pointer fires.

Push too little down and the top bloats; push too much and you hide material the agent actually needs. That tension is the whole decision.

- **Progressive disclosure** is the move down the ladder so the top stays legible. Not primarily token optimization: it protects the hierarchy. Branching is the cleanest test: inline what every branch needs, disclose what only some branches reach. When a document has steps, misplaced in-file reference buries them and turns attention into a coin flip.
- **Co-location**: where the ladder decides how far down a piece sits, co-location decides what sits beside it. Keep a concept's definition, rules, and caveats under one heading rather than scattered. The document should read like documentation written for the agent.
- **Sprawl** is the failure mode: a document simply too long, even when every line is live and unique. The cure is the ladder: disclose reference behind pointers, split by branch or sequence.

## Steps and completion criteria

Every step ends on a **completion criterion**: the condition that tells the agent the work is done. Two properties make it a lever:

- **Clarity**: can the agent tell done from not-done? A vague bound invites **premature completion**: ending before the work is genuinely done. Defend in order: sharpen the bound first (local and cheap); only if it is irreducibly fuzzy and you observe the rush, hide the later steps by splitting across a real context boundary (a hand-off or a subagent dispatch; an inline call leaves the later steps in context and clears nothing).
- **Demand**: how much it requires. "Every modified model accounted for" forces legwork where "produce a change list" does not. Demand is not step-bound: "every rule applied" binds a body of flat reference just as "every step done" binds a sequence, which is how an all-reference document still carries an exhaustiveness bar.

The strongest criteria are both checkable and exhaustive.

## When to split

Splitting spends one of the two loads, so split only when the cut earns it:

- **By sequence**: split where the post-completion steps tempt the agent to rush the one in front. Keeping them out of view drives more legwork on the current task. Beware the reverse: merging exposes each step's later steps and invites premature completion.
- **By invocation** (skill-specific): split off a model-invoked skill when a distinct leading word should trigger it on its own, or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Leading words

A **leading word** is a compact concept already living in the model's pretraining that the agent thinks with while running the document (lesson, fog of war, tracer bullets). Repeated as a token, never as a sentence, it accumulates a distributed definition and anchors a whole region of behaviour in the fewest tokens, by recruiting priors the model already holds. Prefer an existing word: a made-up word recruits no priors, so you pay in definition tokens what a pretrained word gives free.

It anchors twice. In the body, execution: the agent reaches for the same behaviour every time the word appears. In a pointer, invocation: when the same word lives in your prompts, docs, and codebase, the agent links that shared language to the material and reaches it more reliably.

Hunt for refactors: a triad spelled out at three sites, a pointer spending a sentence to gesture at one idea. Example: "fast, deterministic, low-overhead" becomes tight (a tight loop). You win twice: fewer tokens, and a sharper hook for the agent's thinking.

**Negation** is the failure mode beside this lever: steering by prohibition drags the forbidden behaviour into context and makes it more available, not less. Prompt the **positive** ("write one-line comments") so the banned one is never spoken. A prohibition earns its place only as a hard guardrail you cannot phrase positively; even then, pair it with the positive target so attention lands on what to do.

## Pruning

- One meaning, one **single source of truth**. **Duplication** (the same meaning in two places) costs maintenance and tokens, and inflates a meaning's prominence on the ladder past its real rank. (The accidental inverse of a leading word, which repeats a token on purpose, never the meaning.)
- The **environment** is a source of truth too (package.json scripts, config files, directory layout, `--help` output), and a document restating it is a **cache**: a copy of a lookup, earning its load only when the lookup is expensive. Cache the unwritten convention, the reason behind a choice, the gotcha no config confesses. Leave the one-file, one-command lookups to the environment, where they cannot go stale.
- Check every line for **relevance**: does it still bear on what the document does? A line loses relevance by never bearing on the task or by going stale as the world it describes changes. Without a pruning discipline the default fate is **sediment**: stale layers that settle because adding feels safe and removing feels risky, until you must core down through them to find what is still live.
- Hunt **no-ops** sentence by sentence: an instruction the model already obeys by default pays load to say nothing. The test (does it change behaviour versus the default?) is model-relative, not reader-relative. When a sentence fails, delete the whole sentence rather than trim words from it. The test also grades leading words: a word too weak to beat the default (be thorough) is a no-op; the fix is a stronger word (relentless), not a different technique.

## Skill mechanics

- **Model-invoked**: keeps a description, so the agent can fire it autonomously and other skills can reach it. Model-invocation always includes user reach; a description only ever adds agent discovery. The description is the skill's top-level context pointer with permanent context load in exchange for discoverability. Mechanics: omit `disable-model-invocation`, and write a model-facing description carrying the trigger branches (the pointer-writing rules above apply in full). Content that is all reference can live in one model-invoked skill as shared reference: another skill can invoke it, so reference needed by several skills lives in one place.
- **User-invoked**: strips the description from the agent's reach. Only the human typing its name can invoke it, and no other skill can. Zero context load, but it spends cognitive load: you are the index that must remember it exists. Mechanics: set `disable-model-invocation: true`; the description becomes human-facing (a one-line summary, trigger lists stripped). Pick model-invocation only when the agent must reach the skill on its own, or another skill must.
- Shared reference that two user-invoked skills both need can live in neither: push it to a plain file outside the skill system, external reference any skill can point at.
- **Router skill**: when user-invoked skills multiply past what you can remember, one user-invoked skill names the others and when to reach for each, so the human has one skill to remember instead of many. It can only hint, never fire them: with no descriptions, nothing but the human can reach them.
