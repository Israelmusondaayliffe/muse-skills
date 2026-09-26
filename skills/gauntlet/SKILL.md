---
name: "gauntlet"
description: "Run the artifact gauntlet: a builder-vs-blind-critic loop that makes an artifact beat an external, inspectable bar, then verifies with agents that never saw the build. Use only when the user explicitly asks for the gauntlet by name for artifact work: run the gauntlet on this artifact, gauntlet run, gauntlet mode, beat this bar, blind critic loop, resume the gauntlet, gauntlet handoff. A bare 'run the gauntlet' with no existing state gets one question choosing between this skill and gauntlet-loop (governed multi-workstream projects). Never load for ordinary tasks, quick edits, or 'make this really good'."
metadata: { "includeInPrompt": true }
---

# Gauntlet

Make an artifact beat an external bar. Split the goal into the smallest independently judgeable pieces; each piece gets a builder and a blind critic with fresh context, judged against the bar, one gap per round, until it wins or a stop fires. Agents that never saw the build verify; scripts write the report from state.

Adapted from the Community Agent Plugins `gauntlet` plugin (method source: Matt Shumer, "How to Run a Gauntlet Loop"). What transfers is the method, the state layout, and the 17 scripts in `scripts/`.

A gauntlet run is finished only when a verified consensus exists and `build_report.py` wrote `EVIDENCE.md` from state. A brief, a converged piece, a capped piece, or a paused run is progress, not done.

## Start here

1. **Is this the gauntlet, and which one?** Follow `references/routing.md`. Existing `<root>/.gauntlet/runs/*/run.json` means this skill; `<root>/.gauntlet/state.json` means gauntlet-loop. With no state, a bar to beat or a blind comparison means this skill; workstreams or a governed plan mean gauntlet-loop. A bare "run the gauntlet" gets one choice question and nothing is initialized. "Make this really good" without the name is not a gauntlet request.
2. **Read state before acting.** Find an existing run under `.gauntlet/runs/` (match slug and `goal_one_line`). Never create a second run for a goal that has one. State files win over conversation memory.
3. **Precheck.** `python3 scripts/precheck.py --surface hatch`. It reports `subagents: "unknown"` on every host except chat, because a host name is not proof of clean context. So on Muse expect `degraded`: tell the user once that critic isolation is unconfirmed, record `"context_isolation": "degraded"` in `run.json`, and carry the banner into every handoff and report. `unsupported` means brief-only mode.
4. **Budget gate (a real resource gate).** `init_run.py` writes a small envelope: 2 rounds per piece, 1 wave, 0.5 hours per session, 6 launches, cost ceiling 0 (no metered spend), `approved: false`. State it in plain numbers with anything the brief needs beyond it, ask once, and record the answer in `run.json` budgets (`approved: true`, `approval_ref` pointing at the decision recorded in `CONTEXT.md`). Until then `check_stops.py` pauses the run as `budget-unverified`. If the user already stated an envelope in this request, record it; do not ask again.

| State on disk | Next stage | First command |
|---|---|---|
| No run for this goal | Brief | `python3 scripts/init_run.py --root <project> --slug <slug> --goal "<one line>" --domain <domain> --shape S1` |
| Precheck `unsupported` | Brief-only mode, then stop | Produce `CONTEXT.md`, `PLAN.md`, `bar/`, `prompt.md`; hand over the prompt |
| Brief exists, no `prompt.md` | Prompt | `python3 scripts/lint_prompt.py <run>/prompt.md --domain <domain>` |
| Budgets not approved | Budget gate (step 4) | `python3 scripts/check_stops.py --run-dir <run>` |
| `prompt.md` exists, status not `running` | Run | `python3 scripts/check_stops.py --run-dir <run> --next-launches 2` |
| "resume", new session, stale `run.lock` | Handoff read, then run | read `CONTEXT.md`, newest `HANDOFF.md`, `run.json` |
| `stopped` or `converged`, no consensus | Verify | `python3 scripts/hash_plan.py --run-dir <run> --check` |
| Consensus `verified` or `verified-with-dissent` | Evidence | `python3 scripts/hash_artifacts.py --run-dir <run>` |
| Consensus `failed` or `unverifiable` | Run, with verifier gaps as work | `check_stops.py` against the remaining envelope |

Full routing, degraded, and unsupported behavior: `references/routing.md`.

## The seven invariants (they win every conflict)

1. The bar is external and inspectable (INV-1): files, commands, or measurements, never adjectives or a mid-run rubric.
2. The builder never grades itself (INV-2). Critics and verifiers get file-only briefs; `round_record.py` rejects a verdict that is not recorded as `files-only`.
3. Judgment inspects the real thing (INV-3): rendered pixels, test output, the full text.
4. Quality and integrity are judged separately (INV-4).
5. Nothing is done without re-runnable evidence (INV-5). Missing evidence is reported as missing.
6. Continuity is written from state by script (INV-6).
7. Caps pause, they do not certify (INV-7). A capped piece is `capped`, never `done`.

Scripts decide where a step names one. Never hand-edit a verdict, consensus, or report value. Never simulate the loop: no narrated rounds, no imagined critics.

## Stages

**1. Brief.** Explore before asking. Interview one question at a time only for what changes the run: bar, success criteria, budget, scope. Pick one adapter from `references/domains/` (`code`, `visual`, `prose`, `research`, `deck`, `strategy`, `prompt-system`, `brand`). Write `bar/bar.md` with real refs in `bar/refs/` and gate it with `validate_bar.py` (`references/choosing-a-bar.md`). Gate the 11 fields with `brief_complete.py`. Size: S1 (up to 10 pieces, one session), S2 (sequential sessions), S3 (parallel lanes with locks). Then `init_run.py`, `CONTEXT.md` and `PLAN.md` from `assets/`, `hash_plan.py --record`, `validate_pieces.py`.

**2. Prompt.** Fill `assets/prompt-template.md`, keep it under 400 words, lint with `lint_prompt.py` (a failed lint blocks), check `references/prompt-antipatterns.md`, show the prompt in one fenced block.

**3. Run.** Per round, per eligible piece:
1. `check_stops.py --run-dir <run> --next-launches N --next-cost C` with the launches and verified maximum metered cost you are about to spend. A fired stop means do not dispatch.
2. Builder in fresh context (`agents/builder.md`, goal, bar refs, piece, artifact path, last `gap.md`). Record the launch in `cost.json` (`subagents_total`, `cost_spent`) as it happens.
3. Inspect with every declared method; record `inspection_command` rows. Nothing produced means the round fails; no critic for a broken artifact.
4. `blind_pair.py`, then the critic in fresh context (`agents/critic.md`, neutral A/B outputs only). Record with `round_record.py`.
5. Lost: write `gap.md`, loop. Won: two consecutive wins converge the piece.
6. `render_workbench.py`, `check_stops.py`, lock heartbeat, state to disk.

Wave boundary: merge, run the smoother (`agents/smoother.md`), `references/parallelism-and-locks.md`. Stops in order: user `STOP` file, budget unverified or proposed usage over the envelope, convergence, round cap (piece cap clamped to the run cap), no-gain, wave cap, wall clock (from the open session's `entered` timestamp), launch cap, cost ceiling. These are cooperative gates over records you keep; they cannot see an unrecorded launch or cap account-wide spend, so record every launch.

**4. Verify.** Only on `stopped` or `converged` runs without consensus. `hash_plan.py --check` first (mismatch means `cannot-verify`). Spawn quality and integrity verifiers with file-only briefs (`agents/quality-verifier.md`, `agents/integrity-verifier.md`), within the approved launch cap. `consensus.py` is the only author of `consensus.json`. Spawning discipline: `references/verification-independence.md`.

**5. Evidence.** Only after `verified` or `verified-with-dissent`: `hash_artifacts.py`, then `build_report.py`. Every number comes from state; missing values print `not recorded`.

**6. Handoff.** `write_handoff.py --run-dir <run> --session <n> --exit-reason "<reason>"`, one optional `## Judgment notes (unverified)` section, release the lock. Read mode reads state in the order in `references/multi-session.md` and writes a `sessions.json` entry with an ISO `entered` timestamp.

## Worked example (illustrative, synthetic)

Request: "Run the gauntlet on the Tidewater tagline; beat these three reference taglines." No run exists.

- Routing: a bar to beat, so this skill. No choice question needed.
- Precheck: `degraded`, `subagents: "unknown"`. Tell the user critic isolation is unconfirmed on this host; record `context_isolation: degraded`.
- Init: `python3 scripts/init_run.py --root ~/workspace/tidewater --slug tidewater-tagline --goal "Tidewater tagline that beats the bar" --domain prose --shape S1`.
- Budget: `check_stops.py --run-dir <run> --next-launches 2` returns `budget-unverified`. Say: "This run can use 2 critic rounds for 1 piece, 6 launches total, 30 minutes, no metered spend. One round is a builder plus a critic. Approve that envelope?" After "yes", set `approved: true`, `approval_ref: "CONTEXT.md 2026-09-25 user approved envelope"`, status `running`.
- Judgment: one piece, not three. A tagline is one judgeable unit, and splitting it would spend launches on fragments no critic can compare against a whole reference.
- Round 1 loses (gap: "does not name kayakers"). Round 2 wins. The round cap of 2 fires before a second consecutive win, so the piece is `capped`. Report "capped after 2 rounds, 1 win, last gap preserved", and offer one more round only with a new approval. Not done.

A wrong version would launch critics before approval, record `context_isolation: clean` because the host is Hatch, or call the capped piece finished.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop when |
|---|---|---|---|
| `check_stops` fires `budget-unverified` | No recorded approval, non-numeric cap or cost, bad `cost.json`, or open session without `entered` | Fix the record from the user's actual answer or reconcile `cost.json` | never self-approve; ask once |
| `proposed-budget-exceeded` | The next dispatch would pass the launch cap or cost ceiling | Dispatch fewer launches, or ask for a new envelope | the user declines; report paused |
| `validate_bar.py` fails | Bar is adjectives, or refs do not resolve | Replace with files or measurements; re-gate | no inspectable bar exists; brief-only |
| `lint_prompt.py` fails | Over 600 words, missing clause, architecture prescribed | Cut and re-lint | lint passes |
| Inspection produced nothing | Broken artifact or wrong command | Round fails; send the failure back as the gap | same failure twice triggers no-gain |
| `init_run.py` exits with `gauntlet-loop-state-present` | This root holds gauntlet-loop state | Use another root; never mix editions | always |
| Consensus `failed` | Verifiers found gaps | Gaps become run work within the remaining envelope | envelope exhausted: report paused |

## Completion

- **Verified**: consensus `verified` or `verified-with-dissent`, `EVIDENCE.md` built from state, degradation banner present if isolation was not clean.
- **Paused**: a cap or budget stop fired. Report the stop reason, what converged, what is capped, and what one more round would need.
- **Brief-only**: surface unsupported; deliver the brief files and the prompt.
- **Blocked**: say what is missing (bar, inspection method, approval) and the smallest next action.

Never report completion from the router, and never skip verification to reach the report.

## Resources

- `scripts/`: `precheck.py`, `init_run.py`, `validate_bar.py`, `brief_complete.py`, `validate_pieces.py`, `hash_plan.py`, `lint_prompt.py`, `lock.py`, `blind_pair.py`, `round_record.py`, `check_stops.py`, `claim_audit.py` (`--skip-network` available), `consensus.py`, `hash_artifacts.py`, `build_report.py`, `render_workbench.py`, `write_handoff.py`. Run as `python3 scripts/<name>.py --run-dir <run>`; they read and write only the run directory, plus optional reachability probes.
- `agents/`: role briefs for builder, critic, reader-proxy, quality-verifier, integrity-verifier, smoother. Paste the brief into the child's spawn message with only the file paths it may read (`references/hatch-mechanics.md`).
- `references/`: `routing.md`, `schemas.md`, `choosing-a-bar.md`, `domains/`, `prompt-antipatterns.md`, `reader-proxy.md`, `verification-independence.md`, `parallelism-and-locks.md`, `multi-session.md`, `hatch-mechanics.md`.
- State: `<project>/.gauntlet/runs/<run-id>/` and `<project>/.gauntlet/sealed/<run-id>/`. Outputs: `workbench.html`, `EVIDENCE.md` and `EVIDENCE.json` after verification, `HANDOFF.md` at session boundaries.
