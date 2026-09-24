# Audit Policy Reference

Measure paired outcomes with and without retrieval using equivalent contracts, environments, budgets, and verifiers. Report helpful, neutral, harmful, and indeterminate retrievals as separate counts — never collapse indeterminate into improvement. Treat fewer than twenty preregistered pairs per claimed task family as exploratory, not conclusive.

Track per run: evidence levels achieved, draft revisions, execution attempts, verifier errors, human overrides, stale or conflicting records, local exclusions, tool errors, latency, and cost (when available). Keep critical security counts separate and require zero across the maintained regression suite.

Run `bin/run-regressions` for the deterministic regression suite against the ledger. The audit is read-only: it validates and counts, it never mutates records, policy, skills, or host configuration.
