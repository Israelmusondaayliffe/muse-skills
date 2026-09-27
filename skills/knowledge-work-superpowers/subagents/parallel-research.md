---
name: parallel-research
description: Use when two or more independent research strands need running concurrently and subagents are permitted; sequential execution would be too slow. This brief dispatches focused research agents with shared standards, an independence test, and a review and integration procedure so parallel work matches single-agent evidence quality.
---

Purpose: shorten independent research work without creating duplicated searches, inconsistent evidence standards, or conflicting edits.

## Permission gate

Use only when subagents are available, user/developer/platform instructions permit delegation, at least two research strands are independent, and agents will not edit the same files or shared state concurrently. If any condition fails, execute sequentially.

## Independence test

Strands are independent when each can be understood and completed from its own brief and sources, and one strand's result does not determine how another must research. Good split: current market size / competitor offerings / relevant regulation. Poor split: find sources, then interpret those same sources, then draft from those same interpretations. That is sequential.

## Procedure

1. **Define shared standards** before dispatching. Every agent receives: overall decision, its exact research question, scope and exclusions, source hierarchy, freshness requirement, required source and claim ledger fields, citation rules, output location or report contract, stop conditions.
2. **Create focused strands.** One problem domain per agent; remove overlap explicitly; state what the agent must return and must not do.
3. **Dispatch concurrently.** Only strands that can run without shared writes; use separate artifact paths or return reports to the coordinator.
4. **Review each return.** Was the question answered? Check source quality and freshness; confirm claims link to sources; note contradictions, missing evidence, uncertainty; reject outputs that rely on search snippets or unsupported summaries.
5. **Integrate.** The coordinator owns synthesis: merge source and claim ledgers, resolve duplicate source IDs, compare definitions and date ranges, surface cross-strand conflicts. Do not ask a synthesis agent to hide contradictions for a clean narrative.
6. **Verify the combined result.** Run the same evidence and brief checks as single-agent work. Parallel execution changes speed, not the quality standard.

## Agent brief shape

Research question / Why it matters / Scope / Excluded / Source hierarchy / Freshness rule / Required artifacts / Verification / Stop conditions / Return format.
