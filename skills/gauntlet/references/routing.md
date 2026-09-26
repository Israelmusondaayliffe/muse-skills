# Gauntlet routing reference

The router reads durable state from disk and dispatches to exactly one stage. First match wins. The router never does stage work and never reports completion.

## Which edition owns the request

Two skills carry the gauntlet name. They differ by purpose and by state, and they never share a run.

| | `gauntlet` (this skill) | `gauntlet-loop` |
|---|---|---|
| Purpose | Beat an external, inspectable bar on an artifact. Builders improve pieces; blind critics compare ours against the bar reference; verifiers who never saw the build decide. | Govern a large multi-workstream project. Grill the plan, get it approved as a constitution, compile workstreams, run them with fresh critics, integrate, and have an independent panel issue the verdict. |
| Unit of work | A piece with a bar reference and a blind A/B comparison | A workstream with a charter, write targets, and acceptance criteria |
| State | `<root>/.gauntlet/runs/<run-id>/` (`run.json`, `pieces.json`, `cost.json`) and `<root>/.gauntlet/sealed/<run-id>/` | `<root>/.gauntlet/state.json`, `plan.md`, `gauntlet.yaml`, `budget-ledger.json` |
| Scripts | the `scripts/` folder of this skill | `gauntletctl.py` in the gauntlet-loop skill |
| Typical request | "run the gauntlet on this landing page against these three references", "blind critic loop", "beat this bar" | "run the gauntlet loop on the migration project", "governed gauntlet", "gauntlet workstreams" |

Decide ownership in this order:

1. Existing state decides a resume. `<root>/.gauntlet/runs/*/run.json` belongs to this skill; `<root>/.gauntlet/state.json` belongs to gauntlet-loop. Resume only the owning edition.
2. An explicit edition decides a new run: a bar to beat or a blind comparison means this skill; "gauntlet loop", workstreams, or a plan to govern means gauntlet-loop.
3. A request that names only "gauntlet" or "run the gauntlet" with no state and no edition signal gets one choice question, then waits: "Do you want (a) the artifact gauntlet: blind critics compare your work against an external bar, or (b) the gauntlet loop: a governed multi-workstream project with an approved plan and a verification panel?" Initialize nothing before the answer.
4. Both editions' state in one root is a conflict. Report both paths and ask which to continue. Never convert, merge, or copy state between them. The scripts refuse to initialize one edition over the other's state; pick another root instead of forcing it.

## Neighboring owners

- A general "grill me" or decision interview outside a gauntlet run belongs to `strategy-room`. `matt-partok-bundled-plugin-for-knowledge-work` runs only when the user selects it by name. Inside a gauntlet brief, this skill's own interview applies.
- When another router (for example capability-operator or signal-to-system) hands a request here, that hand-off is final. If the request does not fit either gauntlet edition, say so and name the likely owner once; do not route it back and forth.
- "Make this really good" without the gauntlet name is not a gauntlet request.

## Locating an existing run directory

1. Search `.gauntlet/runs/` under the current project root (the working directory, or the repository root if inside one).
2. Run IDs follow `YYYYMMDD-HHMM-<slug>`. Match the slug and `goal_one_line` in each candidate's `run.json` against the stated goal.
3. One clear match: use it. Several plausible matches: list run ID, goal, and status, and ask which one. Zero matches: a new run; route to precheck, then brief.

Never guess between candidates, and never create a second run for a goal that has one unless the user asks for a fresh run. Once selected, read `run.json`, then `pieces.json`, then check `prompt.md`, `run.lock`, and `verification/*/consensus.json`.

## The routing table

| Signal | Route | Why |
|---|---|---|
| No run directory for this goal | Precheck, then brief | An `unsupported` surface must not initialize state; `degraded` must be disclosed first. |
| Precheck `unsupported` | Brief-only mode, then stop | Produce `CONTEXT.md`, `PLAN.md`, `bar/`, and `prompt.md`; hand over the prompt. Never simulate a loop. |
| Brief exists, no `prompt.md` | Prompt stage | `lint_prompt.py` must pass before anything runs. |
| Budgets not approved (`budgets.approved` false or no `approval_ref`) | State the envelope, ask once, record the answer | `check_stops.py` pauses the run as `budget-unverified` until the approval is recorded. |
| `prompt.md` exists, status not `running` | Run stage | Reads state from disk and begins or continues rounds. |
| "resume", new session, or stale `run.lock` | Handoff read mode, then run stage | Reconstruct from disk, never from conversation memory. |
| Session ending, or "hand this off" | Handoff write mode | `write_handoff.py`, a `sessions.json` exit record, lock release. |
| Status `stopped`, `converged`, or `paused` with pieces `capped`, no consensus | Verify stage, or report the pause | Convergence is a critic outcome, not a verdict. A cap is not done. |
| Consensus `verified` or `verified-with-dissent` | Evidence stage | Only now may a report exist. |
| Consensus `failed` or `unverifiable` | Run stage with the gaps as new work, within the remaining approved envelope | Never forward to the report. |
| "is it actually done" | Verify stage, never the report first | A doneness question is a verification request. |

## Degraded behavior

`precheck.py` reports `subagents: "unknown"` on every host label except `chat` (false). A host or model name is not proof of clean context, so on Muse the expected precheck result is `degraded`.

- Name the missing proof and its cost to the user, and get their go-ahead once.
- Record `"context_isolation": "degraded"` (or `"execution": "degraded"`) in `run.json`. Set `clean` only when the lead has recorded host evidence of isolation, such as a spawned child failing to read a canary string that exists only in the parent turn.
- Each judge runs as a separate invocation seeded only from files. Every handoff and evidence report carries the degradation banner; it is not removable.
- On cross-surface resume, the new surface runs its own precheck. A weaker result continues in degraded mode with the banner, or waits.

## Unsupported behavior

`precheck.py` returned `unsupported` (no filesystem, or no subagents and no command execution). A plain chat surface is the canonical case.

- Refuse to initialize a run and say why: independent judgment needs fresh-context critics, and resumability needs durable files.
- Offer brief-only mode and hand the user one fenced prompt to run on an agentic host.
- Never simulate a loop. No narrated rounds, no imagined critics.
