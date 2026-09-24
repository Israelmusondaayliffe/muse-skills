---
name: "gauntlet"
description: "Run the gauntlet: a heavyweight builder-vs-blind-critic loop for mega projects that justify real cost. Use only when the user explicitly says gauntlet, run the gauntlet, gauntlet loop, gauntlet mode, beat this bar, blind critic loop, resume the gauntlet, or gauntlet handoff. Turns a goal into a script-validated brief with an external bar, loops builders against blind critics until the work wins or stops, verifies with independent agents, and reports with re-runnable evidence. Never load for ordinary tasks, quick edits, or 'make this really good'."
metadata: { "includeInPrompt": true }
---

# Gauntlet

Explicit-only mega-project loop: split a goal into the smallest independently judgeable pieces, give each piece a builder and a blind critic with fresh context, judge against an external bar, name one gap per round, loop until the work wins or the run stops, verify with agents that never saw the build, and report with receipts.

Adapted from the Community Agent Plugins `gauntlet` plugin (method source: Matt Shumer, "How to Run a Gauntlet Loop"). Manifest/agent formats from the plugin do not transfer; what transfers is the method, the state layout, and the 17 validation scripts in `scripts/`.

## Operating rules

1. **Explicit only.** If the user says "make this really good" or "push it to the limit" without naming the gauntlet, do not proceed and do not initialize state. Point out the gauntlet exists and must be invoked by name. No confirmation, no run.
2. **The seven invariants win every conflict:**
   - The bar is external and inspectable (INV-1). Never a self-authored mid-run rubric, never prose adjectives.
   - The builder never grades itself (INV-2). Critics and verifiers run in fresh context with no builder history; enforced by spawning discipline and validated by `round_record.py`.
   - Judgment inspects the real thing (INV-3): rendered pixels, running processes, actual test output, full text read end to end. Never a description.
   - Quality and integrity are judged separately, by different verifiers (INV-4).
   - Nothing is done without re-runnable evidence (INV-5). Absence of evidence is reported as absence, never a pass.
   - Continuity is written from state by script, not narrated (INV-6).
   - Caps pause, they do not certify (INV-7). A capped piece is `capped`, never `done`.
3. **Scripts decide.** Where a step names a script, its output is binding; do not override it by hand. Never hand-edit a verdict, consensus, or report value into passing.
4. **Never simulate the loop.** No faked rounds, no imagined critics, no "as a critic I would say" stand-ins. If the surface cannot run it, say so and offer brief-only mode.
5. **The router never reports completion.** Completion claims come only from the evidence stage reading verified consensus from disk. The router never skips verification to reach the report.

## Tooling

All scripts live in `scripts/` and run with `python3 scripts/<name>.py --run-dir <run-dir>`. They are pure stdlib, covered by the upstream test suite (172 tests, all passing at port time), and safe: they only read and write files under the run directory, plus reachability probes in `claim_audit.py` (`--skip-network` available) and `precheck.py`.

| Script | Job |
|---|---|
| `precheck.py` | Surface capability check. Run with `--surface hatch`; returns `full` / `degraded` / `unsupported` as JSON |
| `init_run.py` | Create `.gauntlet/runs/<YYYYMMDD-HHMM-slug>/` and the sealed directory |
| `validate_bar.py` | Gate the bar (external, inspectable, resolvable refs) |
| `brief_complete.py` | Gate the 11 brief fields |
| `validate_pieces.py` | Enforce the inspection closed set and lane ownership |
| `hash_plan.py` | Freeze (`--record`) and re-check (`--check`) success criteria and rubric hashes |
| `lint_prompt.py` | Lint `prompt.md` (under 600 words, 9 required clauses, no architecture prescription) |
| `lock.py` | Lane lock acquire / heartbeat / release / status |
| `blind_pair.py` | Neutral A/B copies plus a sealed label map outside `runs/` |
| `round_record.py` | Validate and atomically record a critic verdict (enforces INV-2) |
| `check_stops.py` | Evaluate every stop condition; first to fire wins |
| `claim_audit.py` | Audit the claim ledger for a piece |
| `consensus.py` | Compute verification consensus — the only author of `consensus.json` |
| `hash_artifacts.py` | SHA-256 every artifact file at report time |
| `build_report.py` | Assemble `EVIDENCE.md` and `EVIDENCE.json` entirely from state |
| `render_workbench.py` | Regenerate `workbench.html` from state after every round |
| `write_handoff.py` | Generate the script-written session handoff (`--run-dir`, `--session N`, optional `--exit-reason`, `--rounds`, `--subagents`) |

Subagent role briefs for spawned children live in `agents/`: `builder.md`, `critic.md`, `reader-proxy.md`, `quality-verifier.md`, `integrity-verifier.md`, `smoother.md`. Paste the brief into the child's spawn message; the child's entire context is that brief plus the file paths it may read. See `references/hatch-mechanics.md` for how fresh-context spawning works on Hatch.

## Workflow

### Stage 0 — Precheck (router first)

Read run state from disk before routing: run directory under `.gauntlet/runs/` in the project root (match run ID slug and `goal_one_line`; never create a second run for a goal that has one). Then run `precheck.py --surface hatch` and record the result in `run.json`.

- `full`: proceed.
- `degraded`: name the missing capability and its cost, get the user's go-ahead, record `"context_isolation": "degraded"` or `"execution": "degraded"` in `run.json`; every handoff and report carries the banner.
- `unsupported`: refuse the loop. Offer brief-only mode (stages 1–2), produce `CONTEXT.md`, `PLAN.md`, `bar/`, `prompt.md`, and hand the user a portable prompt.

### Routing (first match wins)

| Signal | Route |
|---|---|
| No run directory for this goal | Precheck, then brief |
| Precheck `unsupported` | Brief-only mode, then stop |
| Brief exists, no `prompt.md` | Prompt stage |
| `prompt.md` exists, status not `running` | Run stage |
| "resume", new session, or stale `run.lock` | Handoff read mode, then run stage |
| Session ending, or "hand this off" | Handoff write mode |
| Status `stopped` or `converged`, no consensus | Verify stage |
| Consensus `verified` or `verified-with-dissent` | Evidence stage |
| Consensus `failed` or `unverifiable` | Run stage with verifier gaps as new work |
| "Is it actually done" | Verify stage, never the report first |

Full routing detail, run discovery, and degraded/unsupported behavior: `references/routing.md`.

### Stage 1 — Brief

Turn the goal into a decision-complete, script-validated run definition. Explore before asking (conversation, repo, files — never ask for what is discoverable). Interview in one-question turns (tappable options for closed answers) until decision-complete; the ordinary ask-sparingly budget does not apply here.

1. Pick exactly one domain adapter from `references/domains/`: `code`, `visual`, `prose`, `research`, `deck`, `strategy`, `prompt-system`, `brand`. Mixed projects declare a primary plus per-piece overrides. The adapter defines what a piece is, what the bar looks like, how the artifact is inspected, whether blinding is feasible, and what integrity checks.
2. Set the bar in `bar/bar.md` (what, why fair, how inspected) with real refs in `bar/refs/`. Gate with `validate_bar.py`. A failed bar blocks the stage — fix the bar or interview for a better one. Bar-setting guidance: `references/choosing-a-bar.md`.
3. Gate completeness with `brief_complete.py` (11 fields: goal_one_line, 3–7 independently checkable success_criteria, bar_definition, bar_rationale, done_means from `blind win | measured threshold | user judgment`, domain_primary, execution_shape S1|S2|S3, budget_ceiling, out_of_scope, non_negotiables, inspection_feasibility).
4. Size it: S1 (≤10 pieces, one session, one lane), S2 (sequential multi-session, default), S3 (parallel lanes, disjoint artifact paths, lane locks).
5. Propose provisional pieces (id, domain, lane, wave, artifact paths, inspection methods, bar refs, blind feasibility, acceptance, verifier counts). Success criteria are copied verbatim from `PLAN.md` into each piece's `acceptance`.
6. `init_run.py` → write `CONTEXT.md` and `PLAN.md` (templates in `assets/`) → `hash_plan.py --record` → `validate_pieces.py`. Set status `briefed`. `CONTEXT.md` is append-only (corrections appended with date and reason); `PLAN.md` is versioned per wave.

### Stage 2 — Prompt

Fill `assets/prompt-template.md` from `run.json`, `PLAN.md`, `bar/bar.md`. Keep it under 400 words (warn above 400, fail above 600); no architecture, no fixed round counts. Check anti-patterns: `references/prompt-antipatterns.md`. Lint with `lint_prompt.py` — a failed lint blocks the stage. Write `prompt.md`, set status `prompted`, surface the prompt to the user in one fenced code block.

### Stage 3 — Run (the loop)

Preconditions: run directory, `prompt.md`, validated bar. You are the lead: orchestrate, builders build, critics judge, scripts decide.

Per round, per eligible piece (status `looping`, under caps, in this wave, your lane):

1. **Builder**, fresh context via `subagent.spawn` with `agents/builder.md` plus goal, bar refs, piece definition, artifact path, last `gap.md`. Not given: critic reasoning, other pieces, own prior rationale. It edits the real artifact; you snapshot to `rounds/<piece>/<n>/artifact/`.
2. **Inspect.** Run every declared inspection method; for `inspection_command`s record `{"command", "exit_code", "ran_at"}` rows in `rounds/<piece>/<n>/inspection/results.json`. Knowledge-work pieces get the reader-proxy child (`agents/reader-proxy.md`, mechanism in `references/reader-proxy.md`) and `claim_audit.py`. If inspection fails or produces nothing, the round FAILS — send it back as the gap, spawn no critic. Never judge a broken artifact.
3. **Blind pair** with `blind_pair.py` (skip where `blind_feasible` is false; judge against the frozen rubric instead).
4. **Critic**, fresh context via `subagent.spawn` with `agents/critic.md` plus goal, bar description, neutral A/B inspection outputs, acceptance criterion. Not given: which is ours, builder history, prior verdicts, the sealed map.
5. **Record** with `round_record.py`. You assert `critic_saw_builder_context: false`, `critic_context_source: "files-only"`; a rejected verdict is a failed round. You unseal the map and write `winner_is_ours` after validation.
6. **Win/loss.** Ours lost: write `gap.md`, reset `consecutive_wins`, loop. Ours won: increment; two consecutive wins converge the piece (`converged`).
7. **Every round:** `render_workbench.py`, `check_stops.py`, lock heartbeat, write all state to disk (a session that dies must lose at most one round).

**Wave boundary:** when every piece in the wave is `converged`, `capped`, or `blocked`, stop all lanes, merge, and spawn the smoother (`agents/smoother.md`, fresh context, whole artifact, no piece history) to reconcile. Record as a `smooth` round; write `waves/<n>/merge.md`. Protocol: `references/parallelism-and-locks.md`.

**Stops:** `check_stops.py` evaluates user stop, convergence (2 blind wins), round cap (default 10/piece), no-gain rule (same gap twice → re-split), wave cap (default 4), wall clock (default 6h/session), subagent cap (default 400), cost ceiling. First to fire wins; caps pause, never certify.

### Stage 4 — Verify

Runs only on `stopped` or `converged` runs with no consensus. Convergence is a critic outcome, not a verdict.

1. Plan hash first: `hash_plan.py --check`. A mismatch → `cannot-verify` regardless of the artifact.
2. Spawn N quality verifiers (`agents/quality-verifier.md`) and N integrity verifiers (`agents/integrity-verifier.md`) per piece, fresh context each, given only: goal from `CONTEXT.md`, criteria from `PLAN.md`, the bar, the piece's acceptance, the artifact, inspection output. Nothing else.
3. Write verdicts to `verification/<piece>/quality-*.json`, `integrity-*.json`; compute consensus with `consensus.py` only.
4. `verified` / `verified-with-dissent` → evidence stage. `failed` / `unverifiable` → back to the run stage with verifier reasons as new work. Spawning discipline: `references/verification-independence.md`.

### Stage 5 — Evidence

Only after a `verified` or `verified-with-dissent` consensus. Run `hash_artifacts.py`, then `build_report.py`. Every number, path, command, and hash is read from state — the skill computes nothing; missing values print `not recorded` and are listed in section 7. Nine fixed sections: verdict (verbatim), goal and bar, per-piece table, re-run the checks, claim audit summary, artifact integrity, what was not verified, known remaining gaps, budget spent. Template: `assets/evidence-report-template.md`.

### Stage 6 — Handoff

Continuity from state, not narration. Write mode: `write_handoff.py --run-dir <run-dir> --session <n> --exit-reason "<reason>"` → `sessions/<n>/HANDOFF.md` (twelve fixed sections; template in `assets/handoff-template.md`), then the departing agent may append exactly one `## Judgment notes (unverified)` section and nothing more; release the lane lock; write the `sessions.json` exit record. Read mode: read `CONTEXT.md`, newest `HANDOFF.md`, `run.json`, `PLAN.md`, `pieces.json`, `lanes.json`, in that order; check `run.lock` staleness (heartbeat older than 2 hours or holder exited); claim the lane; restate the contract in one line; route to the run stage. Never resume from the handoff alone — state files win any disagreement. Protocol: `references/multi-session.md`.

## Output contract

Run state lives in `.gauntlet/runs/<run-id>/` under the target project root; sealed blind maps in `.gauntlet/sealed/<run-id>/`. Schemas for `run.json`, `pieces.json`, `lanes.json`, verdicts, consensus, claim ledger, cost, and sessions: `references/schemas.md`. User-visible outputs: `workbench.html` (live progress, regenerated by script), `EVIDENCE.md` / `EVIDENCE.json` (after verification only), `HANDOFF.md` (session boundaries).
