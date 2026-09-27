---
name: diagnosing-bugs
description: "Use when the user says 'diagnose' or 'debug this', or reports something broken, throwing, failing, or slow. A discipline for hard bugs and performance regressions: build a tight feedback loop first, reproduce and minimise, generate ranked falsifiable hypotheses, instrument one variable at a time, write the regression test before the fix, then clean up."
---

Invocation: model or user

# Diagnosing Bugs

Skip phases only when explicitly justified. When exploring the codebase, read `CONTEXT.md` (if it exists) and check ADRs in the area you are touching.

## Redact

This skill shows commands, outputs, and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars so the credential stays in the environment, not in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal. If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Phase 1: Build a feedback loop

This is the skill. Everything else is mechanical. A **tight** pass/fail signal that goes red on *this* bug lets bisection, hypothesis-testing, and instrumentation do their work. Without one, staring at code will not save you. Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.

Ways to construct one, in roughly this order:

1. **Failing test** at whatever seam reaches the bug: unit, integration, e2e.
2. **Curl / HTTP script** against a running dev server.
3. **CLI invocation** with a fixture input, diffing stdout against a known-good snapshot.
4. **Headless browser script** (Playwright / Puppeteer) driving the UI and asserting on DOM, console, network.
5. **Replay a captured trace.** Save a real network request, payload, or event log; replay it through the code path in isolation.
6. **Throwaway harness.** Minimal subset of the system (one service, mocked deps) exercising the bug path with one function call.
7. **Property / fuzz loop.** For "sometimes wrong output", run 1000 random inputs and look for the failure mode.
8. **Bisection harness.** Bug appeared between two known states: automate "boot at state X, check, repeat" so you can `git bisect run`.
9. **Differential loop.** Same input through old vs new version (or two configs); diff outputs.
10. **HITL bash script.** Last resort: if a human must click, drive them with `bin/hitl-loop.template.sh` so the loop stays structured. Captured output feeds back to you.

### Tighten the loop

Treat the loop as a product: make it faster (cache setup, skip unrelated init, narrow scope), sharper (assert the specific symptom, not "didn't crash"), and more deterministic (pin time, seed RNG, isolate filesystem, freeze network). A 30-second flaky loop is barely better than no loop; a 2-second deterministic one is a debugging superpower.

### Non-deterministic bugs

Aim for a **higher reproduction rate**, not a clean repro. Loop the trigger 100x, parallelise, add stress, narrow timing windows, inject sleeps. A 50%-flake bug is debuggable; 1% is not. Keep raising the rate until it is debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to the reproducing environment, (b) a redacted captured artifact (HAR file, log dump, core dump, screen recording with timestamps), or (c) permission to add temporary production instrumentation. Do **not** hypothesise without a loop.

### Completion criterion

Phase 1 is done when you can name **one command** (script path, test invocation, curl), already run at least once (show the invocation and redacted output), that is:

- **Red-capable**: drives the actual bug code path and asserts the **user's exact symptom**, so it catches this specific bug and goes green once fixed.
- **Deterministic**: same verdict every run (flaky bugs: pinned, high reproduction rate).
- **Fast**: seconds, not minutes.
- **Agent-runnable**: runs unattended; a human in the loop only via `bin/hitl-loop.template.sh`.

Reading code to build a theory before this command exists means stopping: jumping straight to a hypothesis is the exact failure this skill prevents. No red-capable command, no Phase 2.

## Phase 2: Reproduce and minimise

Run the loop; watch it go red. Confirm the failure matches the **user's** description (wrong bug = wrong fix), reproduces across runs (or at a high enough rate), and the exact symptom is captured (error message, wrong output, slow timing) for later verification.

**Minimise**: shrink to the smallest scenario that still goes red. Cut inputs, callers, config, data, and steps one at a time, re-running after each cut; keep only what is load-bearing. A minimal repro shrinks the hypothesis space and becomes the regression test. Done when every remaining element is load-bearing: removing any one turns the loop green. Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

Generate **3 to 5 ranked hypotheses** before testing any. Single-hypothesis generation anchors on the first plausible idea. Each must be **falsifiable**:

> "If <X> is the cause, then <changing Y> will make the bug disappear / <changing Z> will make it worse."

No stated prediction, no hypothesis: discard or sharpen it. **Show the ranked list to the user before testing.** Their domain knowledge often re-ranks instantly or marks already-ruled-out ideas. Do not block on it; proceed with your ranking if the user is AFK.

## Phase 4: Instrument

Each probe maps to a specific Phase 3 prediction. **Change one variable at a time.** Prefer: (1) debugger / REPL inspection where supported, one breakpoint beats ten logs; (2) targeted logs at boundaries that distinguish hypotheses; never "log everything and grep". Tag every debug log with a unique prefix, e.g. `[DEBUG-a4f2]`, so cleanup is one grep; untagged logs survive, tagged logs die.

**Perf branch**: for performance regressions, logs are usually wrong. Establish a baseline (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

## Phase 5: Fix and regression test

Write the regression test **before the fix**, but only at a **correct seam**: the test must exercise the real bug pattern as it occurs at the call site. A too-shallow seam (single-caller test for a multi-caller bug) gives false confidence. **If no correct seam exists, that is itself the finding**: the architecture prevents the bug from being locked down. Flag it for the next phase.

If a correct seam exists: (1) turn the minimised repro into a failing test at that seam; (2) watch it fail; (3) apply the fix; (4) watch it pass; (5) re-run the Phase 1 loop against the original, un-minimised scenario.

## Phase 6: Cleanup

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (grep the prefix)
- [ ] Throwaway prototypes deleted (or moved to a clearly-marked debug location)
- [ ] The correct hypothesis is stated in the commit / PR message, so the next debugger learns

## Knowledge-work port

The portable core for non-code work:

- **Tight feedback loop first.** Define one cheap, repeatable check that fails on *this* problem and passes when solved (a draft test, a worked example, a checklist against the brief).
- **Falsifiable hypotheses.** State predictions as "If X is the cause, then changing Y removes the problem, or changing Z makes it worse." No prediction, no hypothesis.
- **One variable at a time.** Change one thing per pass, then re-run the loop.
- **Reproduce, then minimise.** Capture the exact symptom first; strip the scenario to its load-bearing elements before theorising.
- **Never theorise without a loop.** No pass/fail signal, no hypothesis.
- **HITL last resort.** When a human must judge, structure them with `bin/hitl-loop.template.sh` so feedback stays looped, not ad hoc.
