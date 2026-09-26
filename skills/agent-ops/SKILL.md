---
name: agent-ops
description: Design, build, and audit reusable agent systems on Hatch. Covers pattern selection (single call, workflows, or autonomous agents), subagent brief design with ground truth and stop conditions, multi-subagent orchestration, and read-only audits of existing agent setups. Use when the user asks to build a reusable agent or delegation pattern, design a recurring automated workflow, review an agent setup for safety, or wants an honest assessment of whether a task even needs an agent.
---

# Agent Ops

Turn "I want an agent that does X" into a working agent system on Hatch, or tell the user a plain prompt is enough. Built on Anthropic's Building Effective Agents: simple, composable patterns beat frameworks. The finished result is a validated artifact: a design spec or brief that passes `bin/validate_agent.py`, or an audit ledger that passes `bin/validate_audit.py`, with findings tied to evidence.

## Start here

1. **Classify the request:**

| The request | Mode | Deliverable |
|---|---|---|
| A reusable agent, delegation pattern, or recurring workflow | Design | Spec from `assets/agent-spec-template.md`, then briefs |
| "Review / audit this agent, cron job, or workflow" | Audit (read-only) | Ledger from `assets/audit-template.json` |
| Both ("audit it, then give me a fixed version") | Audit, then Design | Ledger first, corrected brief as a separate file |
| A one-off task | None | Do the task directly; do not use this skill |

2. **Read what exists:** the instructions, schedule, tools, state, and how completion is checked. For an audit, quote the setup's own words as evidence.
3. **Check delegation:** is `subagent.spawn` in the current tool list? If not, the design stays the same and the parent runs each brief sequentially in its own thread with the same stops, verification command, and approval pause. Say so in the deliverable.

## Design: climb the simplicity ladder

Start at rung 1 and justify every step up. Agentic systems trade latency and cost for task performance; name the trade.

- **Rung 1, single call:** one well-crafted prompt with retrieved context. Usually enough. If so, say so and stop.
- **Rung 2, workflow:** predictable, predefined paths. Pick the pattern from `references/patterns.md`: chaining (steps plus a checked gate between them), routing (classifier with a fallback), parallelization (independent passes, never two writers on one file), orchestrator-workers (orchestrator runs named verification, never trusts worker self-reports), evaluator-optimizer (a separate evaluator with explicit criteria and a round cap).
- **Rung 3, autonomous agent:** open-ended work with unpredictable step counts, checkable success, a feedback loop, and human oversight. Load `references/autonomous-agents.md` (and `references/aci-design.md` for custom tools).

Split deterministic work from judgment. A link check, a schema check, or a diff is a script step; deciding a fix is the judgment step, and it gets the approval pause.

Write each worker brief from [assets/subagent-template.md](assets/subagent-template.md): self-contained task, scope, ground-truth command, stop conditions with a numeric cap, pause points, and exactly what to hand back. Children do not inherit the transcript. Then run `python3 bin/validate_agent.py <brief> --kind agent|workflow|subagent` and fix every FAIL before delivering.

Output: one line naming the mode, pattern, and why not the simpler rung; each artifact in its own labeled code block with its destination (a `subagent.spawn` brief, a cron instruction block, a skill file path); a sandbox-test note saying how to trial it before trusting it.

## Audit: read-only

1. Check every control in `references/audit-controls.md`: outcome, evidence, authority, stops, state, tool contracts, recovery, cost, observability, verification.
2. **Blockers:** missing stop conditions, unbounded external authority (edits, messages, posts, spending without a bound or approval), and completion that cannot be verified independently of the agent's claim.
3. A control with no evidence in the material is **unknown**; write that in the finding. Never infer a pass.
4. If observed runtime behavior differs from the written instructions, report both and trust the observed evidence.
5. Record findings (id, control, severity `blocker|high|medium|low`, evidence, remedy) and run `python3 bin/validate_audit.py <ledger.json>`. Report blockers first. Do not implement fixes unless the user also asked for a corrected version.

## Worked example (illustrative)

A nightly cron agent is told: "Check every link in ~/workspace/docs and fix any broken ones by editing the Markdown files directly... Keep going until everything works... post 'All links fixed' in the team channel."

Audit judgment: "Keep going until everything works" has no cap, a stops blocker. Direct edits to every doc plus a channel post with no approval is unbounded authority, a blocker. "All links fixed" comes from the agent's own claim, a verification blocker. No state between nights is a medium finding. Cost is unknown.

Corrected design: rung 2 chaining, not an autonomous agent. Step 1 is a script that lists broken links (deterministic). Step 2 proposes fixes as a list and waits for approval before any edit or post. A brief for step 2 that passes the validator, runnable from this skill folder:

```bash
SCRATCH=$(mktemp -d)
cat > "$SCRATCH/brief.md" <<'EOF'
You are a docs link fixer. Task: turn the broken-link report into a proposed fix list.
Ground truth: run python3 check_links.py docs/ and assess from its output, never self-report.
Stop conditions: stop and report when every broken link has a proposed fix or a reason it has none. Maximum 3 attempts to locate a moved page. If the checker fails after 3 attempts, stop and report the error.
Pause point: wait for the user to approve the fix list before editing any file or posting anything.
EOF
python3 bin/validate_agent.py "$SCRATCH/brief.md" --kind agent
```

It prints `RESULT: PASS` with an advisory WARN for iteration policy; add one sentence on how the next attempt is chosen to clear it.

A wrong version would deliver a rung-3 agent, keep "use your best judgment" as the authority rule, or claim the brief validated without running the validator.

## When something goes wrong

| Symptom | Likely cause | Next move | Stop and ask when |
|---|---|---|---|
| `validate_agent.py` FAIL on stops | No numeric cap or failure stop | Add "Maximum N ..." and "after N attempts, stop and report" | never |
| FAIL on ground truth | Completion is self-reported | Name the command whose output decides done | no checkable command exists; say the task is not agent-ready |
| FAIL on em-dashes | Pasted prose | Replace with commas or periods | never |
| `validate_audit.py` invalid | Missing id, severity, evidence, or remedy | Fill from the setup's text | never |
| No evidence for a control | Material does not cover it | Mark it unknown in the finding | the user needs a verdict on it; ask for the missing material |
| `subagent.spawn` unavailable | Host or session limit | Run the brief sequentially in the parent with the same stops | never; the design does not change |

## Completion

- **Design complete:** spec and briefs delivered, each validator run shown passing, delegation fallback stated, sandbox-test note included.
- **Audit complete:** ledger validates, blockers first, unknown controls named, no changes made to the audited setup.
- **Not agent-ready:** say which control (usually ground truth or stops) cannot be defined yet and what would make it definable.

## Operating rules

1. The brief is the artifact. It must stand alone: task, scope, ground-truth commands, stops, hand-back.
2. Reaching a budget or iteration cap is not completing the objective. Say so in every design and report.
3. A builder grading its own work is not verification; reviewers get fresh context.
4. Do not copy standing context (MEMORY.md, AGENTS.md, SOUL.md) into briefs or cron instructions; it already loads every turn.
5. Minimal worker set. Do not spawn a subagent for work you can finish directly.
6. Scripts validate structure; the design judgment is yours.
7. Routing requests between existing workspace skills belongs to capability-operator.

## Resources

- `references/patterns.md`, `references/autonomous-agents.md`, `references/aci-design.md` (tool definitions and poka-yoke), `references/audit-controls.md`.
- `assets/agent-spec-template.md`, `assets/subagent-template.md`, `assets/audit-template.json`.
- `bin/validate_agent.py`, `bin/validate_audit.py`.
