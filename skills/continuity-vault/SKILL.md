---
name: continuity-vault
description: "Keep work usable and trustworthy across sessions: route continuity operations (task handoffs, durable extraction, knowledge promotion, knowledge graphs, recall routing, staleness audits, evidence digests, session compounding). Use when work from a task, delegated slice, project, or research must survive compaction or a fresh session, or when prior knowledge may be stale or conflicting. Treats workspace files as authority and memory as recall only; never silently rewrites, deletes, or promotes source material."
---

# Continuity Vault

Move work across sessions and agents without losing provenance. The finished result is one route's record, built from actual files, validated, and saved where the task allows: a handoff a stranger can resume from, a promotion decision, an audit verdict, a digest with every claim cited. This skill keeps no state of its own.

## Start here

1. **Name four things** before anything else: the **source** (files, project, session), its **authority layer** (below), the **future use**, and the **write boundary** (where you may save). If the source cannot be named, stop and say so.
2. **Pick one route** from what you can observe. Procedures and record formats: [references/routes.md](references/routes.md).

| What you see | Route | Record |
|---|---|---|
| Someone must continue this work in a fresh session or as a delegated slice | `handoff` | [assets/task-handoff-template.md](assets/task-handoff-template.md) + `assets/handoff-schema.json` |
| Notes of a finished meeting, interview, workshop, or working session that should yield outputs | `compound` | [assets/session-compounder-template.md](assets/session-compounder-template.md), `bin/validate_session_compounder.py` |
| Knowledge must outlive a model change or an ending access window | `extract` | [references/extraction-moves.md](references/extraction-moves.md) |
| An extracted item needs a durable home | `promote` | `assets/promotion-schema.json` |
| Relationships across many files matter more than notes | `graph` | [references/graphify.md](references/graphify.md) |
| Prior context may exist, location unknown | `search` | native recall, then `bin/local_fallback.py search` |
| Two sources disagree, or a claim may be stale | `audit` | `assets/audit-schema.json`, result `clear`, `needs-review`, or `blocked` |
| A closed set of sources needs a short cited summary | `digest` | `bin/local_fallback.py digest` |

Ownership: this skill owns durable handoffs and session compounding into workspace records; do not route that work back to `signal-to-system`. Generic decision interviews ("grill me", "pressure-test this decision") belong to `strategy-room`.

3. **Read the sources** the route needs. Use recall only to find them, then recheck load-bearing facts in the files.
4. **Write and validate the record** against the schema named in the table, for example `python3 bin/validate_output.py assets/handoff-schema.json <record.json>` (`promote` uses `promotion-schema.json`, `audit` uses `audit-schema.json`). Save only inside the write boundary.

## Authority hierarchy (Muse on Hatch)

1. Standing instruction chain: `SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md` (read-only).
2. Goal contracts: `~/workspace/goals/<slug>/GOAL.md` and their write boundaries.
3. Project and workspace source files (the work itself).
4. Derived artifacts (reports, digests, prior handoffs): evidence, not authority.
5. Recall only: `muse.memory_search` / `muse.memory_get`, daily notes in `~/memory/`, connected device integrations. They find context; they never settle a load-bearing conflict.

**When memory is unavailable** (no recall tool, or it returns nothing): work from the files the user supplied or named. For `search`, run `bin/local_fallback.py search --root <dir> --authority "<authority statement from this task>" --query "<literal>"` on roots the user authorized in this task only; the helper refuses `/`, the home folder or its parents, symlinks, and missing roots. It returns `no-evidence` only after a finished search and `search-incomplete` when a bound stopped it. Never widen the search.

## Handoff method (the most common route)

A good handoff lets a stranger with no chat history take the next step. It:

- separates **completed**, **in progress**, **not started**, and **blocked**, each from the files or log, not from memory;
- records decisions that constrain the next person, with who decided and the source;
- lists proof in an evidence table and says what each proof does and does not establish. A claim that something works, with no run behind it, goes in as unverified;
- names actions that still need the user's or someone else's approval;
- ends with one first action, a verification command, a stop condition, and a recovery step.

Cold-read check before delivering: from the handoff alone, can a stranger name the source, the state, the next action, the stop condition, and how to verify? If not, fix the gap.

## Worked example (illustrative)

A session log on a link-checker script says: "Ran `python3 -m unittest tests/test_internal.py`: Ran 3 tests, OK", "external check started, no timeout yet", "Jordan decides 5s or 10s", and "the external tests should pass on CI". The TODO file lists 2 external tests as planned.

Judgment: the 3 internal tests go in Evidence as passed, with the command. "Should pass on CI" goes in Evidence as unverified with no run behind it, not in Completed. The timeout is Blocked, owned by Jordan; the handoff must not pick a value. First action: finish the HEAD-then-GET fallback without a timeout, or get Jordan's decision.

The routing record, validated from this skill folder:

```bash
SCRATCH=$(mktemp -d)
cat > "$SCRATCH/handoff-routing.json" <<'EOF'
{"source": "session-log.md, project/README.md, project/TODO.md",
 "authority_layer": "project source files",
 "route": "handoff",
 "rationale": "work stops today; a new person continues tomorrow without this chat",
 "next_skill": "none",
 "verification": "python3 -m unittest tests/test_internal.py",
 "destructive_action_authorized": false}
EOF
python3 bin/validate_output.py assets/handoff-schema.json "$SCRATCH/handoff-routing.json"
```

It prints `"valid": true`. A wrong version would list the external tests as passing, choose the 10s timeout, or add owners and dates the log does not contain.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| Validator reports a missing or empty field | Record incomplete | Fill it from the sources; mark real gaps as gaps | the value exists nowhere in the sources |
| Two instruction layers conflict | Stale or competing rule | Switch to `audit`; preserve both sources | always before resolving; the owner decides |
| Provenance for an item is missing | Source lost or never recorded | Destination `none` until recovered | the user wants it promoted anyway |
| A `compound` output uses an item with `unknown` permission | Consent not recorded | Mark the gap; create the other selected outputs | the blocked output is the one the user needs |
| Recall returns nothing | Memory unavailable or empty | Supplied files, then the bounded fallback on authorized roots | no root is authorized |
| `local_fallback.py` refuses a root | Broad root, symlink, or missing folder | Ask for the exact project folder | always; never pick a wider root |

## Completion

- **Complete:** the route's record is validated, saved inside the write boundary, and passes the cold-read check where it applies.
- **Complete with gaps:** the record is valid and the gaps (missing owner, unverified claim, unresolved permission) are named in it.
- **Blocked:** the source cannot be named, the authority is missing, or the conflict needs an owner; say what would clear it.

For `compound`, if the request already names the outputs, treat those as selected; otherwise recommend a ranked set and let the user choose before creating.

## Continuity guardrails

Hatch has no session-start or pre-compact hooks, so run these as procedures:

- **Session start:** before resuming, check `muse.memory_search`, goal status, and the instruction chain.
- **Compaction guard:** in a long session, write a `handoff` to a workspace file (for example `~/workspace/goals/<slug>/hidden_files/`) so a fresh context can resume cold.
- **Graph upkeep and staleness:** a git `post-commit` hook or a user-approved `cron` job runs `graphify --update` or a bounded `audit`.

## Operating rules

1. One route per run; state it and why.
2. Never move, overwrite, delete, or promote material without the task's existing write authority. A handoff records authority; it grants none.
3. A destination outside the approved boundary is recommended, not written.
4. Editing `SOUL.md`, `AGENTS.md`, `IDENTITY.md`, `USER.md`, or `MEMORY.md` needs an explicit user request, a backup, and evidence the rule belongs at that layer. Memory files are read-only here.
5. Never invent identifiers, consent, owners, dates, or quotes. Do not request or store credentials; read connected sources only through their own skills.

## Tooling

- `bin/local_fallback.py`: bounded read-only `search` and `digest` with authority checks and source hashes.
- `bin/validate_output.py`: validates `handoff`, `promote`, and `audit` records against `assets/*-schema.json`.
- `bin/validate_session_compounder.py`: validates a `compound` record's provenance, permission, selection, and gaps.
- `assets/learnings-note-template.md`: format for a durable learnings note.
