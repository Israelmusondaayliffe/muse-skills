# Prompt anti-patterns

A catalog of the ways gauntlet prompts fail, each with a before and after pair. The shared rule behind all of them: the prompt states the contract (goal, bar, loop, evidence) and leaves the how to the lead agent. `lint_prompt.py` catches most of these mechanically; this file explains why they are failures so you stop producing them, not just stop shipping them.

## 1. Architecture prescription

Dictating a stack, framework, or system design the user never asked for. The lead agent's builders will discover better structures than a prompt written before any round has run, and a prescribed architecture becomes a constraint the critic cannot judge against the bar.

**Before**

```
Build the dashboard as a React SPA with a Redux store, a Node/Express API layer,
and a PostgreSQL backend. Use a components/ directory with one folder per widget.
```

**After**

```
Build the dashboard. The bar is the reference screenshots at bar/refs/ and the load
test at bar/loadtest.sh. Beat both. You own every technical choice the user did not
constrain.
```

## 2. Fixed round counts

Telling the loop how many rounds to run. Convergence is decided by two consecutive blind wins and stops are decided by `check_stops.py` against the caps in `run.json`. A number in the prompt either under-runs a hard piece or wastes rounds on an easy one, and it hands the model a schedule to perform against instead of a bar to beat.

**Before**

```
Run five rounds of improvement on each section, then move to the next.
```

**After**

```
Loop each piece until it beats the bar or the user stops the run. Caps pause work;
they never certify it.
```

## 3. Rubric in the prompt

Inlining scoring criteria into the prompt body. The bar lives in `bar/`, frozen and hashed at brief time. A rubric restated in the prompt is a second, unhashed copy that drifts from the frozen one, and it invites the critic to grade against prose in its context instead of inspecting the real thing.

**Before**

```
Judge each draft on clarity (1-5), structure (1-5), and originality (1-5).
A section passes at 12 or above.
```

**After**

```
The bar: the frozen rubric at bar/rubric.md, hash recorded in run.json. Critics score
against that file. You may not restate, edit, or soften it.
```

## 4. Verbosity

Padding the prompt with context the run directory already holds: background narrative, restated brief answers, motivational framing, defensive caveats. Every extra sentence dilutes the nine clauses that matter, and the linter fails the prompt past 600 words regardless of how good the padding sounds.

**Before**

```
This project matters a great deal to the team, and it has a long history: it began as
a workshop exercise in 2024, evolved through three internal drafts... [300 words of
backstory] ...so please keep all of this in mind as you carefully and thoughtfully
approach each piece.
```

**After**

```
Full project context is at <run-dir>/CONTEXT.md. Read it first.
```

## 5. Missing reader-proxy and claim-ledger clauses on knowledge work

Prose, research, strategy, deck, and prompt-system pieces do not compile or render, so a prompt that omits the reader-proxy and claim-ledger requirements leaves the loop with `read` as its only inspection, which is never sufficient. The linter fails knowledge-work prompts that omit these clauses.

**Before**

```
For each section, have the critic read the draft and compare it to the reference.
```

**After**

```
Inspect every knowledge-work piece with a fresh reader-proxy agent against its frozen
question set, and maintain a claim ledger validated by claim_audit.py. Unanswered
questions and unsupported claims are gaps.
```

## 6. Prescribing file layouts

Naming the directories, modules, or file structure of the work product. The state layout under `.gauntlet/` is fixed by the plugin and does not belong in the prompt; the artifact's own layout belongs to the builders. A prescribed layout is architecture prescription wearing a filesystem.

**Before**

```
Organize the output as chapters/01-intro.md through chapters/08-close.md, with a
shared glossary.md and an appendix/ directory for source excerpts.
```

**After**

```
Write state to <run-dir> after every round. The artifact's own structure is yours to
choose and re-choose as the pieces converge.
```

## 7. Replacing the model's decomposition judgment

Handing the lead agent a fixed piece list and forbidding re-splits. The brief's decomposition is marked provisional on purpose (`"decomposition_owner": "lead-agent"`): the lead re-splits as rounds reveal which pieces are really independent and which gaps keep pointing at a seam. A frozen decomposition in the prompt turns the no-gain rule's escalation path into a dead end.

**Before**

```
The work consists of exactly these six pieces, listed below. Do not add, merge, or
split pieces: [list].
```

**After**

```
Split the goal into the smallest independently judgeable pieces. A first-pass
decomposition is in <run-dir>/pieces.json, marked provisional. You own it and may
re-split as you learn.
```
