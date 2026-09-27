---
name: implement-spec
description: "Use when the user provides a spec with tickets and wants, as a direct command, the entire spec implemented as one PR on a single branch. This subagent treats the tickets as a task graph with blocking relationships and a ready frontier: implementer subagents run in parallel, each in its own worktree on its own branch, communicating via sparse context pointers and merged by a merger subagent, finishing with code review, a ready-for-review PR, and worktree cleanup."
---

Invocation: user-invoked only

## Procedure

1. **Read the spec and tickets.** Read enough to understand the task graph: the tickets are not a list of steps, they have blocking relationships, so there is always a **frontier** of tickets ready to be grabbed.
2. **(Optional) Explore.** Use an exploration subagent for any exploration the tickets require (codebase files, external docs). It saves markdown notes in a directory outside the repo, accessible to all future subagents, so implementers focus on implementation.
3. **Create a branch and a draft PR** marked as closing the spec issue and tickets.
4. **Implement.** Use implementer subagents for each ticket, in the background, each in its own worktree on its own branch, for maximum concurrency.
5. **Merge.** Once an implementer subagent completes, a merger subagent merges its work into the PR branch.
6. **Advance the frontier.** When merges change which tickets are unblocked, kick off more implementer subagents on the new frontier.
7. **Review and fix.** Once all tickets are complete, run `code-review` on the PR branch and fix all issues in a single implementer subagent.
8. **Mark the PR ready for review.**
9. **Clean up** all implementer subagent worktrees.

Communication to and from subagents stays sparse: communicate primarily through **context pointers** (spec, tickets, research notes, previous commits), never by duplicating information already available via a pointer.

## Knowledge-work port

- Decompose a large knowledge task into tickets with blocking relationships; always work the ready frontier in parallel.
- Subagents communicate via context pointers (links to the spec, tickets, notes, prior commits), never by copying content between them.
- Merge each finished slice into the main line of the work; re-scan the frontier after every merge.
- One final review pass fixes everything at the end; clean up scratch directories before shipping.
