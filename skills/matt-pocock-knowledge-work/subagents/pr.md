---
name: pr
description: "Use when writing a PR body."
---

Invocation: model or user

## Procedure

Use this template for writing the PR body:

```markdown
## Summary

<diagram, diff-sketch, or tree>

## Evidence

- **Before:** <screenshot/output/failing test run>
  **After:** <screenshot/output/passing test run>

## Merge Danger

**Door:** <one-way or two-way>

<optional: description>

**Blast Radius:** <one-word description>

<optional: potential ramifications of merge>
```

### Sections

Skip all preambles and keep prose brief. Use the user's domain language from `CONTEXT.md`.

### Summary

Pick the smallest visual that makes the key point clear. Use one, or several, but don't overwhelm:

- **Pseudocode** for logic or an algorithm.
- **Call tree** for runtime control flow.
- **Component tree** (with file paths) for UI structure, including state and module boundaries that matter.
- **Shallow file tree** (with one-line responsibility comments) for file responsibility or a broad refactor.
- **Mermaid** (sequence or flow) for component interaction, control flow, or data flow.
- **Diff** when the point is what changes and the surrounding shape already exists: match the diff shape to the topic (component change, file-layout change, call-tree change, state change).
- **Whole block** when most of it is new, when omitted context would hide ownership or order, or when the user needs a copyable target shape.

Keep only the calls, files, props, states, and boundaries needed to answer the user's current question or the options to resolve the current discussion point. Place each visual next to the short text it supports.

### Evidence

Concrete evidence that the change works. Show a before and after.

- Screenshots are S-tier: use them when the environment supports it and the change is visual.
- Execution-based evidence is A-tier: test results, console output. Show the exact test that now fails and passes, using pseudocode.

### Merge Danger

Describe whether it is a **one-way** or **two-way** door. You can walk back through two-way doors, but not one-way doors. A PR cheap to roll back is lower risk. Destructive actions or hard-to-reverse decisions are one-way doors.

**Blast radius** is the potential impact or scope of the changes. Consider all possibilities: layout shift, breakages for consumers, mobile responsiveness, etc.

## Knowledge-work port

- Use the same three headings for any proposal that changes shared work: Summary, Evidence, Danger.
- Summary is one visual: a diagram, diff, or outline sketch, not a wall of prose.
- Evidence is before/after: the draft before, the improved draft after, side by side.
- Danger is a one-way/two-way door: can the decision be walked back? Name the blast radius of getting it wrong.
- Skip preambles; domain language only.
