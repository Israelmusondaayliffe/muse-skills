---
name: implement
description: "Use when the user asks, as a direct command, to implement a piece of work described by a spec or set of tickets. This subagent implements the work with TDD at pre-agreed seams, runs typechecks and single test files regularly with the full test suite once at the end, then code-reviews the result and commits to the current branch."
---

Invocation: user-invoked only

## Procedure

1. **Build test-first.** Use the `tdd` subagent where possible, at pre-agreed seams.
2. **Check continuously.** Run typechecking regularly and single test files regularly; run the full test suite once at the end.
3. **Review the work.** Use the `code-review` subagent once the work is done.
4. **Commit.** Commit the work to the current branch.

## Knowledge-work port

- Execute directly from the spec or ticket list; do not re-plan work that is already planned.
- Produce the work in slices, checking each slice against the spec before moving on (test-first at agreed seams).
- Do a continuous sanity pass per slice and one full review of everything at the end.
- Run a final two-axis review (standards and spec) before calling it done, then hand back on the agreed surface.
