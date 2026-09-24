# Task: Infographic (factual diagrams)

Scope: prompts for factual diagrams, maps, charts, process explanations and information graphics with explicit labels and relationships.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Start with the information, not a decorative style. Identify the audience's question and the relationship that answers it: sequence, comparison, hierarchy, geography, causality, proportion or anatomy. Choose a visual form that represents that relationship faithfully.
2. Create an exact inventory: title, labels, values, units, connections, legend, source line. State required relationships and positions, not only noun names. Distinguish a process arrow from correlation or causation. Preserve data across stylistic alternatives.
3. If information is missing, use supplied placeholders or research it (see `research.md`); do not invent credible-looking figures.
4. Specify composition, reading order, visual hierarchy, density, color meanings and medium. Labels must stay associated with the correct object or series. A map needs a defined region and source; scientific structure needs a verified reference.
5. JSON for a dense label inventory; NL when a simpler visual explanation reads better.

## Recipes

Use `../recipes/infographic/gpt-infographic.md` for diagrams, charts, maps, anatomy, educational posters, flowcharts. Check the prompt against its data source. Rendered accuracy is a separate check: inspect labels, numbers and spatial relationships when an output is available.
