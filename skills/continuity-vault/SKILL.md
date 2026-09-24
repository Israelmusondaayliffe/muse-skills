---
name: continuity-vault
description: "Keep work usable and trustworthy across sessions: route continuity operations (task handoffs, durable extraction, knowledge promotion, knowledge graphs, recall routing, staleness audits, evidence digests, session compounding). Use when work from a task, delegated slice, project, or research must survive compaction or a fresh session — or when prior knowledge may be stale or conflicting. Treats workspace files as authority and memory as recall only; never silently rewrites, deletes, or promotes source material."
---

# Continuity Vault

## Purpose

Move information across sessions and agents without losing provenance, and decide
explicitly where extracted knowledge should live. This skill is a **router plus
procedures**: pick one route, run it with recorded evidence, and validate the record.

## Authority hierarchy (Muse on Hatch)

1. Standing instruction chain: `SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md` (read-only).
2. Goal contracts: `~/workspace/goals/<slug>/GOAL.md` and their stated write boundaries.
3. Project and workspace source files (the work itself).
4. Derived artifacts (reports, digests, prior handoffs) — evidence, not authority.
5. Recall surfaces only: `muse.memory_search` / `muse.memory_get`, daily notes in
   `~/memory/`, and connected device integrations. They can *find* context; they
   cannot settle a load-bearing conflict.

Memory and recall tools never promote, overwrite, delete, or resolve conflicts on
their own. A handoff records authority; it grants none.

## Routes

Pick exactly one primary route per run. Detail for each route lives in
[references/routes.md](references/routes.md).

| Route | Use when | Core procedure |
|---|---|---|
| `handoff` | A fresh task or delegated slice must continue without conversation history | Build from actual files using [assets/task-handoff-template.md](assets/task-handoff-template.md) |
| `extract` | Knowledge must survive a model change or access window ending | Irreversibility test first, then one of five moves in [references/extraction-moves.md](references/extraction-moves.md) |
| `promote` | Extracted knowledge needs a governed durable destination | Destination table + decision record; never silently rewrites sources |
| `graph` | Relationships across sources matter more than linear notes | [references/graphify.md](references/graphify.md) pipeline (`graphifyy` pip package) |
| `search` | Prior context may exist but its location is unknown | Native recall (`muse.memory_search`, memory files) first; bounded local fallback only when needed |
| `audit` | Claims, instructions, or references may be stale or conflicting | Read-only audit, `clear` / `needs-review` / `blocked` |
| `digest` | A bounded set of sources needs a concise continuity summary | Direct evidence digest from a closed source set, every claim cited |
| `compound` | A completed meeting, interview, workshop, or working session should produce durable outputs | Faithful extraction → recommend → user selects → create only selected, permission-safe outputs |

## Workflow

1. Name the **source** (file, project, session), the **authority layer** (from the
   hierarchy above), the intended **future use**, and the **allowed write boundary**.
2. Select one route from the table. Read the route's section in `references/routes.md`.
3. Use recall surfaces only to find likely context; recheck load-bearing facts
   against authoritative files.
4. Produce the route's record (JSON and/or template). Validate it:
   `bin/validate_output.py assets/<route>-schema.json <artifact.json>`
   (`bin/validate_session_compounder.py` for the `compound` route).
5. Return a bounded result. Do not move, overwrite, delete, or promote material
   without the task's existing write authority.

## Continuity guardrails

The source plugin used host hooks (session-start, pre-compact) that don't exist on
Hatch. Run these as procedures instead:

- **Session start.** Before picking up resumed work: review relevant memories
  (`muse.memory_search`), check goal status, and read the instruction chain files.
- **Compaction guard.** If a session is long or about to compact, write a `handoff`
  record to a workspace file (e.g. `~/workspace/goals/<slug>/hidden_files/`) so a
  fresh context can resume cold. A cold-read handoff should identify source, state,
  next action, stop condition, and verification with no prior chat.
- **Graph maintenance.** Use a git `post-commit` hook or a `cron` job to run
  `graphify --update`; see [references/graphify.md](references/graphify.md).
- **Staleness cadence.** For living knowledge, set a `cron` audit on a bounded
  source set (monthly or per-milestone) rather than relying on memory.

## Bounded local fallback (recall without native recall tools)

Only when native recall (`muse.memory_search`, memory files) cannot serve the
`search` or `digest` route:

- `search`: ask for (or reuse) only the exact workspace roots the user authorized
  **in the current task**, then run `bin/local_fallback.py search --root <dir>
  --authority "<task authority statement>" --query "<literal>"`. Filesystem access
  is not search authority; sibling projects and `~` are refused.
- `digest`: close the source set to exact files inside authorized roots, then run
  `bin/local_fallback.py digest --source <file> --audience "<who>" ...`. The
  helper records source hashes and exact excerpts.

The fallback is read-only. `no-evidence` only after a completed search finds
nothing; `search-incomplete` when a bound stops the search. Never widen the search.

## Tooling

- `bin/local_fallback.py` — bounded local recall / evidence digest, with authority
  checks (refuses filesystem root, home directory, symlinks, missing roots).
- `bin/validate_output.py` — validates a route's JSON record against an asset schema.
- `bin/validate_session_compounder.py` — validates a `compound` record's provenance,
  permission, selection, and gap invariants.
- `assets/task-handoff-template.md`, `assets/session-compounder-template.md`,
  `assets/learnings-note-template.md` — human-facing record formats.
- `assets/*-schema.json` — field contracts for `handoff`, `promote`, `audit` records.

## Operating Rules

1. One route per run; state the route and why in the output.
2. Name the source before doing anything else. If the source cannot be named, stop.
3. If two instruction layers conflict, route to `audit` and preserve both sources.
4. If provenance is missing, choose destination `none` until the source is recovered.
5. If a destination is outside the approved boundary, recommend it without writing.
6. Editing `SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `USER.md`, or `MEMORY.md` is not a
   normal promotion destination: it needs an explicit user request, a backup of the
   current file, and evidence the rule belongs at that layer. Memory files are
   read-only through this skill; record findings in the final report instead.
7. Never invent identifiers, consent, owners, dates, or quotes. Mark gaps explicitly.
8. Do not request or store credentials. Read connected sources (Gmail, Calendar,
   Drive, etc.) only through their own skills.
