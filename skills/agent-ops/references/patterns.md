# Agent Design Patterns

From Anthropic's Building Effective Agents (Dec 2024). The finding after working with dozens of teams: the most successful implementations use simple, composable patterns, not complex frameworks.

## Workflows vs Agents, the one distinction that matters

- Workflows: LLMs and tools orchestrated through predefined code paths. Predictable, consistent, for well-defined tasks.
- Agents: the LLM dynamically directs its own process and tool usage, maintaining control over how it accomplishes the task. For flexibility and model-driven decisions at scale.

Default rule: find the simplest solution possible and only add complexity when it demonstrably improves outcomes. Often that means no agentic system at all, a single optimized LLM call with retrieval and in-context examples is usually enough. Agentic systems trade latency and cost for task performance, decide consciously when that trade makes sense.

## The building block: the augmented LLM

Every pattern is built from one unit: an LLM enhanced with retrieval, tools, and memory. The model generates its own search queries, selects tools, and decides what to retain. Two implementation priorities: tailor the augmentations to the specific use case, and give them an easy, well-documented interface.

## The five workflow patterns

### 1. Prompt chaining

Decompose a task into a fixed sequence of steps, each LLM call processes the previous output. Add programmatic gates between steps to check the process is on track.

Use when: the task decomposes cleanly into fixed subtasks. The trade: latency for accuracy, each call is easier.

Examples: write marketing copy, then translate it. Write an outline, validate it against criteria, then write the document from it.

### 2. Routing

Classify an input, direct it to a specialized downstream prompt or process. Separation of concerns: optimizing for one input type stops hurting the others.

Use when: distinct categories are handled better separately and classification is reliable.

Examples: customer queries split into general, refund, technical paths. Easy questions to a small cheap model, hard ones to a capable model.

### 3. Parallelization

Run LLM calls simultaneously, aggregate programmatically. Two variants: sectioning (independent subtasks in parallel) and voting (same task run multiple times for diverse outputs). LLMs do better when each consideration gets its own focused call.

Examples: one call handles the query while a second screens it (guardrails). Several different prompts review code for vulnerabilities and vote.

### 4. Orchestrator-workers

A central LLM dynamically breaks down the task, delegates to worker LLMs, synthesizes results. Different from parallelization because subtasks are not predefined, the orchestrator decides them per input.

Use when: complex tasks where the needed subtasks cannot be predicted.

Examples: coding changes across an unpredictable number of files. Multi-source search and analysis.

### 5. Evaluator-optimizer

One LLM generates, another evaluates and gives feedback, in a loop.

Use when: clear evaluation criteria exist and iteration measurably helps. Two signs of good fit: a human articulating feedback would demonstrably improve the output, and an LLM can produce that feedback itself.

Examples: literary translation with critic passes. Multi-round search where the evaluator decides if more searching is warranted.

## Composition

Patterns compose: a router can front a chain, orchestrator workers can each be evaluator-optimizer pairs, a parallel section can vote on a chain's gate. Prefer the smallest composition that fits the task.
