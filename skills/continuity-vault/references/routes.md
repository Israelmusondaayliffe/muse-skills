# Continuity Vault — route procedures

One route per run. Each section gives the evidence required, the steps, and the
record format. Validate records with the `bin/` scripts before returning them.

## handoff — durable task handoff

Use when a fresh task or delegated slice must continue without conversation
history (also the compaction-guard record).

1. Read the actual source files and current evidence. Do not reconstruct state
   from memory alone.
2. State the objective and the exact boundary of already-authorized work.
3. Separate completed, in-progress, blocked, and not-started work.
4. Record decisions that constrain the next task, with reasons and source paths.
5. Link the latest proof; state what it does and does not establish.
6. Name user-owned or external actions still unapproved.
7. Give one first action that can be taken from the handoff itself.
8. Cold-read check: a fresh context should identify source, state, next action,
   stop condition, and verification without the prior chat.

Fill [assets/task-handoff-template.md](../assets/task-handoff-template.md). A
complete handoff grants no new authority.

## extract — survive a model or access change

Gate first, then one move. Full moves live in
[references/extraction-moves.md](extraction-moves.md).

**Irreversibility test:** can a cheaper model redo this tomorrow? If yes, decline
and redirect. If no (a standard, an executed roadmap, a distilled vault, a
firing skill), proceed. Priority when time is short: RECORDER, then GOALS, then
WORKSPACE, AUDIT, VAULT. "Run the full playbook" means moves in that order after
confirming scope once with the user.

## promote — governed destination decision

Promote only knowledge with a clear future use, named source, and suitable owner.

| Destination | Suitable content | Constraint |
|---|---|---|
| `durable-file` | Reusable procedure, decision record, evidence package | Version it; preserve source links |
| `project-reference` | Stable context specific to one workstream | Follow the project contract and write boundary |
| `graph` | Source-backed entities and relationships | Nodes and edges keep provenance |
| `memory-candidate` | Helpful recall cue for future retrieval | Must be reverified before load-bearing use |
| `none` | Duplicate, transient, unsupported, or sensitive material | Preserve the source; record why no promotion |

Steps: name source, reusable claim/procedure, future task it supports → determine
current authority and stability → choose destination from the table → record owner,
review trigger, provenance link, rationale, approval state. If writing is already
authorized, create a new version without silently replacing the source; otherwise
return the decision only.

Errors: missing provenance → `none`; duplicates an authoritative file → link to it
instead; unclear sensitivity or ownership → approval required, stop before writing.

## graph — relationship mapping

Turn a folder of files into a queryable knowledge graph. See
[references/graphify.md](graphify.md) for the pipeline (detect → AST + semantic
extraction → build/cluster → query). Required evidence: named nodes and
source-backed relationships. Honesty rules: never invent an edge (use AMBIGUOUS),
always show token cost, never hide cohesion scores, warn before visualizing more
than 5,000 nodes.

## search — recall routing

1. Try native recall first: `muse.memory_search` / `muse.memory_get`, daily notes,
   goal files. Native recall is authoritative enough to *find*; recheck
   load-bearing facts against authoritative files.
2. Only when native recall cannot serve: bounded local fallback via
   `bin/local_fallback.py search` with exact task-authorized roots (see SKILL.md).
3. Record query, roots, authority checks, matches. Return `no-evidence` only when
   a bounded search completes with no match; `search-incomplete` when a bound stops it.

## audit — staleness and conflict

1. Define the bounded source set, audit date, current decision, and facts that
   would be costly to get wrong.
2. Rank sources by the authority hierarchy in SKILL.md.
3. Check dates, superseding files, live platform state, unresolved placeholders,
   and instruction conflicts.
4. Per finding record: id, kind (`stale-claim`, `instruction-conflict`,
   `authority-gap`, `missing-owner`, `broken-reference`), severity (`low`,
   `medium`, `high`), source, evidence, recommended action.
5. Result: `clear` only when no actionable finding remains; `needs-review` for
   resolvable findings; `blocked` when a required authority source is absent or
   two controlling sources conflict without an owner decision.
6. Read-only: never resolves a conflict by silently editing or deleting a source.

## digest — evidence digest

1. Close the source set to exact files (inside authorized roots). For Gmail,
   Calendar, Drive, etc., read through their own skills and use local exported
   copies only when the task permits.
2. Build the digest only from that evidence. Cite the source path for every
   claim; distinguish evidence from gaps; return `no-evidence` when the set has
   no usable text.
3. Use `bin/local_fallback.py digest` for the hash/excerpt record when no writing
   companion (e.g. the `writing-quality` skill) is in play. The direct digest does
   not promote or mutate sources.

## compound — session compounding

For completed meeting, interview, workshop, or working-session notes:

1. **Inspect.** Name session, date, purpose, participants/roles, source location,
   completeness, recorded audience, privacy/attribution limits. Extract four
   categories without upgrading status: decisions actually made; follow-ups
   actually stated (owner/timing only when the source names them); durable
   knowledge; derivative outputs (separate — newly created material). Link every
   item to source evidence; exact quotes only when wording is present. Never
   infer consent, a decision, an owner, a date, or permission.
2. **Permission invariant.** An output is creatable only when every contributing
   item has recorded permission allowing the exact intended audience. `unknown`
   or `prohibited` blocks; `restricted` allows only the explicitly recorded
   audience with all restrictions preserved. Unresolved permission → marked gap,
   not creation. De-identification is not permission.
3. **Recommend, select, create.** Rank candidates by value, evidence strength,
   audience fit, effort, sensitivity. State why each is or isn't worth creating,
   then ask the user to select. Create only selected, permission-passing outputs;
   preserve source links; label newly proposed material.
4. Use [assets/session-compounder-template.md](../assets/session-compounder-template.md)
   as the selection and provenance record. Validate structured records with
   `bin/validate_session_compounder.py`.

Boundaries: no publish, message, share, upload, or connected write without
explicit authority for that action. A recommendation or handoff grants no
authority to create another output.
