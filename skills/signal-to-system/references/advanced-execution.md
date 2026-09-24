# Advanced Execution

Single-agent execution is the default. Parallel work is an optional mode, not
a quality signal.

## Eligible workflows

Only these workflows define an optional multi-agent path:

- signal-scout for independent source lanes
- research-to-decision-map for evidence analysis and adversarial review
- capability-matcher-and-brief-builder for independent candidate research
- workshop-workbench for a fresh package review

## How parallel work runs here

Muse spawns bounded subagents itself; each subagent is given one concrete
deliverable (a search lane, a candidate research brief, an independent
review). Subagents report back and are shut down; the primary run integrates
everything.

## Escalation test

Use subagents only when all of these are true:

1. The work has independent lanes or benefits from a genuinely independent
   review.
2. Each worker has a concrete, bounded deliverable.
3. The expected gain justifies the additional time and tokens.
4. The lanes can genuinely proceed without sharing intermediate state.

Set a finite cap before launching. Use two to four workers, avoid nested
delegation, and reserve the primary context to integrate the result. Do not
launch workers merely to repeat the same search or generate more options.

If multi-agent work is unavailable in the current run, perform the same lanes
sequentially. The completion contract and artifact must remain equivalent.

## Integration

The primary run owns the final result. It must reconcile contradictions,
remove duplication, show unresolved disagreements, and return one artifact.
Worker output is evidence, not an automatic conclusion.
