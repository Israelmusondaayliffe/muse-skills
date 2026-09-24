# ACI Design: Prompt Engineering Your Tools

Tool definitions deserve as much prompt engineering as the prompts themselves. Invest as much effort in the agent-computer interface as products invest in human-computer interfaces. While building their SWE-bench agent, Anthropic's team spent more time optimizing tools than the overall prompt.

## Format choice

There are usually several ways to specify the same action (diff vs full-file rewrite, markdown vs JSON output), and some formats are much harder for a model to write. Rules of thumb:

- Give the model enough tokens to think before it writes itself into a corner.
- Keep formats close to what the model has seen naturally on the internet.
- Avoid formatting overhead: no keeping accurate line counts, no string-escaping thousands of characters of code inside JSON.

## The tool design checklist

- Model's-shoes test: put yourself in the model's position. Is usage obvious from the description and parameters, or would you have to think carefully? A good definition includes example usage, edge cases, input format requirements, and clear boundaries from neighboring tools.
- Docstring standard: write parameter names and descriptions like a great docstring for a junior developer. Critical when many tools are similar.
- Empirical testing: run many example inputs, watch what mistakes the model actually makes, iterate. Tool design is not finished at the definition, it is finished when the mistakes stop.

## Poka-yoke

Change arguments so mistakes become structurally harder, not just warned against. The canonical example: the model kept fumbling relative filepaths after changing directories. Requiring absolute paths eliminated the error class entirely.

The general move: find the repeated mistake, then redesign the argument so the mistake cannot be expressed. Structural fixes beat instruction fixes, instructions drift, structure holds.

## Boundary discipline

When two tools overlap, either merge them or write the boundary explicitly into both descriptions ("use X for reading, use Y only when writing"). Ambiguous neighbors are the top cause of tool misuse in multi-tool agents.
