# Task: Midjourney edit architect (edits)

Scope: write or repair Midjourney image-edit prompts — replacement, removal, additions, restyling, viewpoint changes, reference composition, inpainting, outpainting — plus diagnosis of a supplied Midjourney result. Prompts only; the user renders them separately in Midjourney.

Read first: `../prompt-contract.md` and the Midjourney entry in `../model-profiles.md`.

## Workflow

1. Inspect the supplied image and references. Identify the visual anchor, requested change, protected features, and the light, perspective or material cues needed to integrate the result. Ask only when a missing reference or material ambiguity prevents a faithful result.
2. Read `../midjourney/edit-methods.md` for reference-role, risk and Editor guidance. Preserve requested identity and world properties with artistic judgment. A viewpoint change can reveal new surfaces; a naturally developed shot can alter pose and light when the context calls for it.
3. Load `../midjourney/edit-patterns.md` for the relevant recipe, adapting parameters only against the selected current model. Load `../midjourney/failure-recovery.md` when an output or stated failure needs diagnosis.
4. Choose one pass or a useful staged sequence. Honor explicit count and format. Use the retained precision, anchor-rich, cohesion and fallback approaches when alternatives help; do not require four responses for every edit.
5. State attachment roles where needed. Default to web prompt format when the surface is unstated. Consult `../midjourney/current-model-boundaries.md` for web/Discord differences, then check current model guidance before asserting supported controls. Parameters go after the visual instructions.
6. Deliver each complete prompt in its own code block. For a sequence, say which result becomes the next base and what must be inspected before continuing. For diagnosis: observed failure, likely cause, smallest correction, revised prompt.

Finish when the change, references, preserved features and format are clear and no invented detail or unsupported control is presented as certain. A prompt does not prove the edit succeeded. Inspect actual output when provided; the user selects accepted results and reusable recipes.

Source attribution for the imported Midjourney edit material is recorded in `../LICENSE-NOTICES.md`.
