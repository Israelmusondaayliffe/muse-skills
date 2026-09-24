# Task: Multi-output (one prompt, many images)

Scope: one prompt requesting multiple separate image outputs — including eight-image sets and coordinated pages with shared visual DNA.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Deliver one complete prompt for the requested set unless the user explicitly asks for alternative batch prompts. This covers both repeated subject variants and distinct deliverables when the central requirement is one submission producing separate images.
2. Preserve the distinction: one prompt vs one composite/contact sheet vs several separate submissions.
3. Build a shared visual DNA block: subject/world, recognition anchors, palette roles, material/treatment, graphic language, constraints that belong across the set. Then enumerate every output with its own purpose, content, exact text, layout, ratio and distinguishing direction. Allow deliberate per-image exceptions instead of forcing identical composition.
4. For an eight-image request: explicitly request eight separate image outputs, one per specification, with no grid, collage or contact sheet. Preserve the user's system-style prompt method (`<visual_dna>`, `<images>`, `<verify>` or the requested JSON/NL equivalent). On an ordinary chat surface this is an operating prompt, not a real elevated system role.

## Recipes

Use `../recipes/multi_output/gpt-multi-output.md` (event packages, product systems, editorial pages, world/character bibles) and `page-inventories.md` for starting contents — options, not a seven-page quota.

Write prompts without submitting generation requests. If reviewing user-supplied results, count the actual separate images and report any shortfall. Never label a grid as eight files or crop it to manufacture the claim. Prompt preparation does not prove an output count.
