# TDD: Tests and Mocking

## What a good test is

Tests verify **behavior through public interfaces**, not implementation
details. Code can change entirely; tests shouldn't. A good test reads like a
specification — "user can checkout with valid cart" tells you exactly what
capability exists — and survives refactors because it doesn't care about
internal structure.

- **Name tests in the project's domain language** (read `CONTEXT.md` if it
  exists) so the suite reads as a statement of capabilities.
- **Test only at pre-agreed seams.** Before writing any test, write down the
  seams under test and confirm them with the user: "What's the public
  interface, and which seams should we test?" No test is written at an
  unconfirmed seam.

## The loop

- **Red before green.** Write the failing test first, then only enough code to
  pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per
  cycle — vertical tracer bullets, each responding to what the last cycle
  taught you.
- **Refactor only while green.** After the smallest implementation passes,
  improve names or structure without changing behavior, rerun the focused
  test, then begin the next slice. Leave broad design changes for code review
  or a separate approved ticket.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private
  methods, or verifies through a side channel (querying the database instead
  of using the interface). The tell: the test breaks when you refactor but
  behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the
  code does (`expect(add(a, b)).toBe(a + b)`, a hand-derived snapshot, a
  constant asserted equal to itself) — it passes by construction and can never
  disagree with the code. Expected values must come from an independent source
  of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation.
  Bulk tests verify *imagined* behavior — you test the shape of things rather
  than user-facing behavior, tests go insensitive to real changes, and you
  commit to test structure before understanding the implementation.

## Mocking

- Mock at **seams**, not internals: mock the injected port/adapter (see
  `deep-module-design.md`), never the module's private collaborators.
- Prefer **fakes over mocks** where cheap: an in-memory adapter that
  genuinely behaves like the real one beats a mock that only parrots the
  expectations you wrote for it.
- Mock only what you don't own and can't run locally (true externals:
  Stripe, Twilio). Everything in-process or local-substitutable should run
  real in tests.
- A mock that duplicates the implementation's logic is a second
  implementation to maintain — a tautology in disguise. Keep mocks
  behaviorally simple: canned responses and recorded calls, nothing more.
