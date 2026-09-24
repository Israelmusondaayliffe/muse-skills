# Autonomous Agents

## What an agent actually is

Typically just an LLM using tools based on environmental feedback in a loop. Not a framework, not a graph, a loop with ground truth.

## The mechanics, all five required

1. Task acquisition. Starts from a command or an interactive discussion with the user. Once the task is clear, the agent plans and operates independently, returning to the human only for information or judgment.
2. Ground truth every step. At every step the agent must gain ground truth from the environment (tool results, code execution) to assess progress. Never let it run on self-report alone.
3. Pause points. Human feedback at checkpoints or blockers.
4. Stopping conditions. Max iterations, budget, and a blocked stop condition (stop and report when no defensible path remains, and what would clear the block). Always included, this maintains control. Reaching budget is not completing the objective.
5. Iteration policy. How the agent decides what to try next after each attempt. Without one, retries repeat the same guess.

## When to use agents

Open-ended problems where the number of steps cannot be predicted and a path cannot be hardcoded, with enough trust in the model's decisions. Cost is higher and errors compound: test extensively sandboxed, add guardrails.

Agents add the most value on tasks that require both conversation and action, have clear success criteria, enable feedback loops, and integrate meaningful human oversight.

## Proven domains, and why they work

- Coding agents resolving real GitHub issues from the PR description alone: verifiable through automated tests, objective quality measures, structured problem space.
- Customer support: conversation plus tools, clear resolution criteria.

The common thread is checkability. When output cannot be checked, the agent's confidence is worthless.

## The three core principles

1. Maintain simplicity in the agent's design.
2. Prioritize transparency: explicitly show the agent's planning steps.
3. Carefully craft the agent-computer interface: thorough tool documentation and testing.

## Guardrail defaults for every emitted agent

- Named ground-truth commands (tests, build, lint, a diff review), not "verify your work."
- Failure stop with a report of what went wrong, plus a numeric cap.
- A pause point before any step where a wrong call poisons downstream work.
- Sandbox first: run with restricted permissions and watch the first full cycle before trusting it.
- Fresh-context review: the checker must not inherit the builder's context, a builder grading its own work is not a check.
