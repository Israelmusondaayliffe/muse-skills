---
name: grill-with-docs
description: "Use when the user wants a relentless interview to sharpen a plan or design and create docs (ADRs and glossary) as the interview progresses, with trigger phrases like grill me or grill this with docs. It invokes grilling plus domain-modeling. Start here whenever working in a working directory: it is stateful, retaining what it learns in CONTEXT.md and ADRs."
---

Invocation: user-invoked only

Invoke the `grilling` skill and the `domain-modeling` skill together.

`grilling` runs the relentless interview; `domain-modeling` is the active discipline that sharpens the project's domain language as the interview runs: challenge a fuzzy term, resolve an overloaded word, record a hard-to-reverse decision as an ADR, keeping `CONTEXT.md` a clean glossary.

This is the stateful way into grilling: it retains what it learns in `CONTEXT.md` and ADRs, which makes it the better of the two grilling wrappers whenever a repo is there to leave a paper trail in. Not working in a working directory? Use `/grill-me` instead.
