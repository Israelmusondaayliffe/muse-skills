# Task: Style translator (medium/style transformation)

Scope: translate an image into a requested artistic medium, material, visual style or photographic treatment while retaining its recognizable content and respecting a supplied style reference.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Inspect the content reference and any style reference. Describe their assigned roles and the features that matter: subject/world identity, shape language, palette, texture, edge treatment, depth, mood. A supplied style reference outranks a generic recipe for its assigned role.
2. Use `../recipes/style_translator/medium-methods.md` to express how the target medium shapes marks, materials, light and spatial presentation. Read `source-style-templates.md` when its detailed forms fit the task.
3. Choose faithful transformation or creative reinterpretation from the request. A medium can change completely while pose and composition stay fixed. When a new shot or reinterpretation is wanted, develop it naturally and retain the agreed anchors. Do not force ten styles, normalize stylized proportions, or impose photographic skin on a nonphotographic medium.
4. Write complete prompts in the requested form. Alternatives should explore the open treatment choices while preserving the source's character. Check that the medium is described through its visual properties, the style reference stays recognizable, and no accidental content drift was introduced.

Dedicated illustration/photo conversion is `illustration-photo.md`, but a clearly requested style transformation needs no handoff. Review actual outputs only when available; do not confuse a written preservation instruction with proof of fidelity.
