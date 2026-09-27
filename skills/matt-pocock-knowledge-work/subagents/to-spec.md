---
name: to-spec
description: "Use when turning the current conversation into a spec and publishing it to the project issue tracker: no interview, just synthesis of what has already been discussed."
---

Invocation: user-invoked only

Takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; synthesize what is already known.

The issue tracker and triage label vocabulary should have been provided. If not, tell the user to run `/setup-matt-pocock-skills`.

## Procedure

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch the seams at which the feature will be tested. Prefer existing seams to new ones, and propose new seams at the highest point possible. Fewer seams is better; the ideal number is one.

   **Checkpoint:** check with the user that these seams match their expectations before writing the spec.

3. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent` triage label; no further triage is needed.

## Spec template

```markdown
## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories, each in the format:

1. As an <actor>, I want a <feature>, so that <benefit>

This list should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

Decisions that were made, which can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets; they go stale quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo.

## Testing Decisions

Testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.
```

See `assets/spec-template.md` for the full spec template.