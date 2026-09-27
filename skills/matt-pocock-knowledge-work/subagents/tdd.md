---
name: tdd
description: "Use when the user wants to build features or fix bugs test-first, mentions 'red-green-refactor', or wants integration tests. This subagent runs the red-green loop: failing test first, then only enough code to pass it, one vertical slice at a time. It tests only at pre-agreed seams (public interfaces, never internals), reads CONTEXT.md and relevant ADRs so test names match the project's domain language, and rejects the anti-patterns: implementation-coupled tests, tautological assertions, and horizontal slicing (all tests before any implementation). Refactoring stays out of the loop and belongs to code-review."
---

Invocation: model or user

## Procedure

1. **Read the context.** Before anything, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you are touching.
2. **Agree the seams.** A seam is the public boundary you test at. Write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. Testing effort lands on the critical paths and complex logic, not every edge case.
3. **Red.** Write the failing test first. The test verifies behavior through public interfaces, not implementation details, and reads like a specification ("user can checkout with valid cart").
4. **Green.** Write only enough code to pass. No anticipation of future tests, no speculative features.
5. **Repeat one slice at a time.** One seam, one test, one minimal implementation per cycle. Each test is a **tracer bullet** that responds to what the last cycle taught you. Never slice horizontally (all tests first, then implementation): bulk tests verify imagined behavior.
6. **Source expected values independently.** A known-good literal, a worked example, the spec. Never recompute the expected value the way the code does, or the test passes by construction and can never disagree with the code.
7. **Keep refactoring out.** Refactoring belongs to the review stage (the `code-review` subagent), not the red-green cycle.

## Knowledge-work port

- State the checkable claim before producing the artifact (the "failing test": what must be true for this piece to pass).
- Then produce only enough content to satisfy that claim, nothing speculative.
- Work one claim at a time in vertical slices, each slice responding to what the last one taught you.
- Judge every slice against the source material, never against your own draft (this avoids tautological checks).
- Revision and polish are a separate pass at the end, not part of the loop.

See `references/tdd-tests.md` and `references/tdd-mocking.md` for test and mocking detail.