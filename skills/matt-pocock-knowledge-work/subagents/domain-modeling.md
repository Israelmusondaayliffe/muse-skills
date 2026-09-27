---
name: domain-modeling
description: "Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, recording or editing an ADR, challenging vague language with precise canonical terms, or stress-testing domain relationships with concrete scenarios."
---

Invocation: model or user

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the active discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely reading `CONTEXT.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed. If neither `CONTEXT-MAP.md` nor a root `CONTEXT.md` exists, create a root `CONTEXT.md` lazily at the first resolved term; when multiple contexts exist, infer which one the topic relates to, and ask if unclear.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up: capture them as they happen. `CONTEXT.md` should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

Glossary entry format:

```md
**Term**:
A one or two sentence description of what the term IS, not what it does.
_Avoid_: synonyms, rejected alternatives
```

Rules: be opinionated (pick the best word, list the rest under `_Avoid_`). Keep definitions tight: one or two sentences max. Only include terms specific to this project's context, not general programming concepts. Group terms under subheadings when natural clusters emerge.

For multi-context repos, `CONTEXT-MAP.md` lists each context with a link, plus a Relationships section describing how contexts connect (e.g. Ordering emits `OrderPlaced` events; Fulfillment consumes them to start picking).

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR.

ADR template (in `docs/adr/`, numbered `0001-slug.md`, `0002-slug.md`, ...; scan for the highest number and increment):

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording that a decision was made and why, not in filling out sections.

Optional sections, only when they add genuine value: **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`), **Considered Options** (only when rejected alternatives are worth remembering), **Consequences** (only when non-obvious downstream effects need calling out).

What qualifies: architectural shape, integration patterns between contexts, technology choices that carry lock-in, boundary and scope decisions (the explicit no-s are as valuable as the yes-s), deliberate deviations from the obvious path, constraints not visible in the code, and rejected alternatives when the rejection is non-obvious.

See `references/domain-modeling-context-format.md` and `references/domain-modeling-adr-format.md` for the exact context and ADR formats.