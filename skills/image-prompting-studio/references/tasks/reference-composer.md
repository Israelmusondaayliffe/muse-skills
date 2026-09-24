# Task: Reference composer (multi-reference fusion)

Scope: compose subjects, objects, environments, style or layout from multiple image references with clear roles and priority.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Read every supplied reference. Identify what each contributes: identity, object geometry, wardrobe, environment, composition, pose, material, lighting or style.
2. Build a short reference map with an explicit priority for conflicts. Do not transfer a style reference's face or a wardrobe reference's identity unless requested.
3. Build one coherent scene: resolve scale, perspective, eye lines, body/object contacts, occlusion, lighting so the result feels constructed in one space. State who holds what and where each subject sits. Multiple references do not require blending every feature. For a subject placed in a location, preserve recognition anchors while adapting illumination and contact to the setting.
4. JSON separates roles and integration constraints; NL suits a simple blend; a shared system-style prompt suits several compositions under one reference map. Do not impose a four-reference limit or claim an unsupported high-fidelity headcount.

## Recipes

Use `../recipes/reference_composer/gpt-compose.md`, `uni-fuse.md`, `fusion-methods.md`. A separate prompt must remain understandable when copied with its intended attachments. Check for cross-reference leakage in the written prompt and, if rendered outputs exist, inspect actual integration.
