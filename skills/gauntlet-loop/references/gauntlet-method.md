# Gauntlet Method

## Purpose

Use the Gauntlet only after explicit invocation for work whose value justifies a governed plan, bounded parallelism, repeated independent judgment, durable state, and whole-project verification.

## Invariants

1. The approved plan is the project constitution.
2. Every important artifact has an inspectable quality bar.
3. Builders do not issue authoritative verdicts on their own work.
4. Authoritative judges receive fresh context and inspect the real artifact.
5. Missing evidence produces failure or inability to evaluate, never a pass.
6. Parallel writes use disjoint targets or separate worktrees.
7. One integration owner controls shared decisions and shared files.
8. State is updated after material events, not only at session boundaries.
9. Resource ceilings are finite and extensions require user approval.
10. The user retains final authority.
11. Progress means integrated target-state change, not support artifacts.
12. Required unresolved work prevents project completion.
13. Low-risk workstreams may share one fresh integrated critic.

## Stage gates

```text
explicit invocation
  -> intake and grilling
  -> proposed plan
  -> user approval
  -> compiled program
  -> bounded execution
  -> integration
  -> ready_for_verification
  -> independent verification
  -> verified, verified_with_caveats, failed_verification, or unable_to_verify
```

## Authority

Gauntlet is the top-level workflow inside the authorized task. It does not override system or developer instructions, `AGENTS.md`, explicit user choices, source-owning capabilities, sandbox or approval policy, or live tool limits.
