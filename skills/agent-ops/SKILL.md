---
name: agent-ops
description: Design, build, and audit reusable agent systems on Hatch. Covers pattern selection (single call, workflows, or autonomous agents), subagent brief design with ground truth and stop conditions, multi-subagent orchestration, and read-only audits of existing agent setups. Use when the user asks to build a reusable agent or delegation pattern, design a recurring automated workflow, review an agent setup for safety, or wants an honest assessment of whether a task even needs an agent.
---

# Agent Ops

Turn "I want an agent that does X" into a working agent system on Hatch, or tell the user when a plain prompt is the right answer. Built on Anthropic's Building Effective Agents: the most successful implementations use simple, composable patterns, not complex frameworks.

## Workflow

### 1. Route the request

Classify before building:

- **agent-design**: the user wants a reusable agent, a subagent brief pattern, a recurring automated workflow, or delegation architecture.
- **audit**: the user wants an existing agent setup, cron job, or workflow reviewed for safety and reliability. Read-only unless a repair is separately requested.

If the request is a one-off task rather than a reusable system, do not activate this skill. Just do the task.

### 2. For agent-design: climb the simplicity ladder

Start at rung 1 and justify every step up. The trade is always explicit: agentic systems buy task performance with latency and cost.

- **Rung 1, single optimized call**: would one well-crafted prompt with retrieved context solve this? Usually yes. If yes, say so and stop.
- **Rung 2, workflow**: does the task decompose into predictable, predefined paths? Pick the matching pattern from references/patterns.md.
- **Rung 3, autonomous agent**: only for open-ended problems with unpredictable step counts, checkable success, a feedback loop, and meaningful human oversight.

Say plainly when the user asks for an agent they do not need. Never deliver a rung-3 design when rung 1 or 2 solves the task.

### 3. Build by mode

**ARCHITECT** (default entry): pattern selection. Load references/patterns.md. Output a filled assets/agent-spec-template.md naming the chosen pattern, the rejected simpler rung with a concrete reason, the trade accepted, ground truth, stops, pause points, and scope. Hand off to WORKFLOW or AGENT.

**WORKFLOW** (pattern already chosen): load references/patterns.md. Emit pattern artifacts translated to Hatch terms:

- chaining: ordered step prompts plus the programmatic gate between steps (what is checked, what happens on failure). Phase-gated plans with a check command at each gate.
- routing: classifier prompt with category definitions and an explicit fallback, plus one specialized prompt per category. State what happens on misclassification.
- parallelization: independent passes as multiple subagent.spawn calls in one turn, or sectioning prompts with an aggregation rule. Never two writers on the same files; boundaries live in the spec.
- orchestrator-workers: orchestrator brief (decomposition rules, synthesis duties, its own verification step), worker brief template (spec in, scoped output, own stop rules), plus a reviewer brief when warranted. The orchestrator never trusts worker self-reports; it runs named verification commands.
- evaluator-optimizer: generator prompt, evaluator prompt with explicit criteria, loop rule (max rounds, what "accepted" means), and the fresh-context rule: the evaluator never grades the generator's own work (spawn a separate subagent).

**AGENT** (true autonomous agent): load references/autonomous-agents.md. If custom tools are involved, load references/aci-design.md. Write the subagent brief with all five loop mechanics: task acquisition, ground truth every step (named commands, never self-report), pause points (before any step where a wrong call poisons downstream work), stop conditions (max iterations or budget, failure stop with report, blocked stop naming what would clear the block), and an iteration policy (how it picks its next action between attempts). Run `python3 bin/validate_agent.py <brief-file> --kind agent` and fix failures before delivering.

**ACI** (tool interface design): load references/aci-design.md. Write each tool definition to the checklist (example usage, edge cases, format requirements, boundaries from neighboring tools) and poka-yoke repeated mistakes by redesigning arguments so the error class becomes structurally impossible.

**REVIEW** (existing setup): load references/patterns.md and references/autonomous-agents.md. Map the setup to its pattern, then check simplicity, transparency, ACI quality, ground truth, stops, pause points, gates, and scope. Report severity-ordered findings mapped to evidence in their artifacts, then corrected artifacts, then one reusable prevention rule.

### 4. Output contract

Every build delivers:

1. One line naming the mode, chosen pattern, and why this rung and not the simpler one.
2. The filled design spec or the brief artifacts, each in its own labeled code block with its destination (e.g. `subagent.spawn` brief, cron instruction block, skill file path).
3. A sandbox-test note: how to test before trusting it, because errors compound in agentic systems.

### 5. For audit: assess read-only

Collect the instructions, schedule, tools, state model, and verification contract. Check every control in references/audit-controls.md. Record findings with assets/audit-template.json, run `python3 bin/validate_audit.py <file>`, and report blockers first with evidence and a concrete remedy. Do not implement fixes during an audit-only request. Mark a control unknown when evidence is absent; never infer a pass.

## Operating Rules

1. The subagent brief is the artifact. Children do not inherit the transcript: a brief must be fully self-contained (task, scope, ground truth commands, stops, what to hand back).
2. Reaching a budget or iteration cap is not completing the objective. Say so in every design and every report.
3. Fresh-context review is the honest check. A builder grading its own work is not verification.
4. Do not duplicate injected context (MEMORY.md, AGENTS.md, SOUL.md, standing files) inside briefs or cron instructions; that material loads every turn and duplication compounds cost.
5. Minimal worker set. Spawning a subagent for work you can complete directly is waste.
6. Scripts are validators only; the model does the design judgment.
7. This skill does not cover request routing between existing workspace skills; that belongs to capability-operator.
