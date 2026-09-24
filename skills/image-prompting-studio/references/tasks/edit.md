# Task: Edit (targeted change prompts)

Scope: edit prompts for targeted changes or exploration of uploaded images, with explicit reference preservation.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Workflow

1. Inspect the uploaded image (read it first, never describe from memory) and identify the requested change.
2. Write a change/keep relationship specific enough to prevent collateral redesign. Describe the reference by visible identifying content and, when useful, the attachment label. Simple edit: a concise NL instruction. Several changes, preserved features and integration requirements: JSON.
3. An edit must integrate with the scene: perspective, occlusion, contact shadows, reflections, light direction, material scale, texture response. A replacement object occupies the old object's role; background changes may need coherent reflected light.
4. Preserve the requested framing and ratio; change them only when the user requests expansion or reframing. Do not automatically re-pose the subject or force a cinematic re-shoot.
5. Image-only upload with no direction: offer a small useful range of complete edit prompts based on what is actually visible (lighting, material, background, narrative context, design application). If the user only asked what the image is, answer that instead. Do not make every exploratory variant a different person or world.

## Recipes

Read only what the brief needs from `../recipes/prompt_edit/`: `gpt-edit.md` (targeted edits), `nano-edit.md` (upload exploration), `architect-edit.md` (architect structures), `uni-modify.md` (Uni modifications). Use `../libraries/texture-library.md` for surface changes. Faithful illustration/photo conversion belongs to `illustration-photo.md`, but a clearly specified edit needs no handoff.
