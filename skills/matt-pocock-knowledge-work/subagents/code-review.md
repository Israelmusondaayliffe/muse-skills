---
name: code-review
description: "Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to 'review since X'. This subagent runs a two-axis review of the diff between HEAD and a fixed point (commit, branch, tag, or merge-base): Standards (does the work follow the repo's documented coding standards?) and Spec (does the work match what the originating issue or spec asked for?). Both axes run as parallel sub-agents so they do not pollute each other's context, then findings are aggregated side by side, never merged or reranked across axes."
---

Invocation: model or user

## Procedure

The issue tracker should have been provided to you. If `docs/agents/issue-tracker.md` is missing, tell the user to run the `setup-matt-pocock-skills` brief.

1. **Pin the fixed point.** Whatever the user supplied (commit SHA, branch, tag, `main`, `HEAD~5`); ask if they did not specify one. Capture `git diff <fixed-point>...HEAD` (three-dot, against the merge-base) and `git log <fixed-point>..HEAD --oneline`. Confirm the ref resolves and the diff is non-empty. Fail here, not inside two parallel sub-agents.
2. **Identify the spec source**, in this order: issue references in commit messages (via the issue-tracker workflow); a path the user passed; a spec file under `docs/`, `specs/`, or `.scratch/` matching the branch or feature. If nothing is found, ask the user. If no spec exists, the Spec sub-agent reports "no spec available".
3. **Identify the standards sources.** Repo docs like `CODING_STANDARDS.md` or `CONTRIBUTING.md`, plus the Fowler smell baseline from _Refactoring_ ch.3: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest. Two rules: a documented repo standard always overrides the baseline, and each smell is a judgement call, never a hard violation. Skip anything tooling already enforces.
4. **Spawn both sub-agents in parallel.**
   - **Standards** brief: given the diff, commit list, standards sources, and the full smell baseline, report (a) every place the diff violates a documented standard (cite the standard: file plus rule) and (b) any baseline smell spotted (name it, quote the hunk). Distinguish hard violations from judgement calls. Under 400 words.
   - **Spec** brief: given the diff, commit list, and spec contents, report (a) requirements missing or partial, (b) behavior not asked for (scope creep), (c) requirements that look implemented but wrong. Quote the spec line for each finding. Under 400 words.
5. **Aggregate.** Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do not merge or rerank findings across axes: code can follow every standard and still implement the wrong thing, or do exactly what the issue asked while breaking conventions. End with a one-line summary: total findings per axis, and the worst issue within each axis.

## Knowledge-work port

- Review a finished draft along two axes run independently: Standards (does it match the brief's style rules, the repo's conventions, and any agreed patterns?) and Spec (does it cover every requirement the original brief or source asked for, with nothing invented?).
- Keep the axes separate: polished prose answering the wrong brief is a Standards pass and a Spec fail, and the two findings must not cancel each other.
- Each pass gets the source brief plus the draft; aggregate the two reports without reranking.
