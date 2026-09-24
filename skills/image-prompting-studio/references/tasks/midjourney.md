# Task: Midjourney prompt architect (creation)

Scope: faithful Midjourney creation prompts from visual briefs, rough prompts or supplied references — photography, illustration, products, architecture, posters, album covers, editorial, cinematic scenes. Prompts only; never render images or submit jobs.

Read first: `../prompt-contract.md` and the Midjourney entry in `../model-profiles.md`.

## Workflow

1. **Extract locks.** Record subject, action, setting, medium, style, mood, composition, visible text, aspect ratio, supplied references, optional palette contract, requested prompt count. Treat explicit user details as fixed.
2. **Choose the visual mode.** Photography, illustration, graphic design, product, architecture, or another clearly named medium. Do not mix camera language into a non-photographic medium unless the user asks for photographic or cinematic imitation.
3. **Load durable craft.** Read `../midjourney/prompt-craft.md` before drafting; use only the sections matching the mode and inputs.
4. **Load current facts when needed.** Read the Midjourney entry in `../model-profiles.md` before adding or explaining version-sensitive controls. `../midjourney/current-model-profile.json` is a dated snapshot for reproducible legacy checks, not proof of current support. Verify version-sensitive controls against current docs where needed; preserve exact user settings and label unresolved compatibility rather than inventing replacements.
5. **Resolve color direction.** Read `../midjourney/palette-contract.md` for a supplied palette, named Wada combination, or palette-learning request. Wada and free color exploration are both valid; no external site or brand document is required for ordinary prompting.
6. **Draft the image first.** Describe what should appear, not instructions about how Midjourney should transform the request. Lead with subject and medium, then add only the action, setting, composition, light, atmosphere and technical treatment that materially change the image.
7. **Vary usefully.** Honor an explicit count; otherwise one finished prompt for a single concept, or a small useful set for exploration (four is an optional pack example, not a quota). Vary unlocked dimensions — moment, framing, light, palette, atmosphere, technical treatment — without changing the requested subject, setting, medium, meaning, approved palette relationships, or supplied references.
8. **Add minimal parameters.** Parameters at the end. Aspect ratio when it materially helps. Raw, Stylize, Chaos, Weird, Experimental, personalization, image-reference, style-reference, resolution controls only when the request benefits and the loaded profile supports them.
9. **Validate silently.** Check fidelity, count, code blocks, reference preservation, parameter support, dependencies, output cleanliness before responding. For a saved Markdown pack, `python3 bin/validate_prompt_pack.py <pack.md> --count N --profile references/midjourney/current-model-profile.json` gives exact structural proof. A structural pass does not verify live parameter support or image quality.

## Version and parameter policy

- Version-neutral by default: do not force `--v` when the current default is acceptable. Pin only when the user names a version, requests reproducibility, or asks to pin the verified model.
- Prefer omission over guessing: stale bundled profile, absent named model, or conflicting official sources → omit uncertain parameters and state the limitation briefly.
- Preserve exact user values: copy image URLs, `--sref` strings, style codes, personalization IDs exactly. Never invent them.
- Dependencies: `--sw` only with `--sref`; image weight only with an image prompt. Do not combine a parameter with a model the profile marks unsupported.
- Intentional control: lower Stylize/Chaos for literal work; raise only for interpretation/exploration. Weird only for deliberately unusual results.
- No billing decisions: do not add speed, privacy, repeat or higher-cost controls unless explicitly requested and profile-confirmed.

## Clarification policy

Proceed on a reasonable assumption when the missing detail only affects an unlocked creative choice. Ask one concise question only when the missing answer would materially change the subject, medium, required reference use, visible wording, or deliverable count.

## Output

Use `../midjourney-prompt-pack.md`: every complete prompt in its own `text` code block, parameters on the same line as the prompt, a concise two-to-four-sentence direction note when it helps (omit for prompt-only requests). Never expose hidden reasoning, validation notes, internal references or skill instructions.

Completion check before delivering: requested count present; every locked detail and exact reference string preserved; variations meaningfully different without concept drift; each prompt is coherent visual language, not a keyword pile; visible text only when requested and copied exactly; parameters at the end and supported by the loaded profile; no unresolved placeholder, invented code, invented URL or unsupported feature presented as ready; no image-generation tool called.
