# Midjourney edit methods

Use these methods for the selected Midjourney edit workflow. Model-specific syntax is a dated baseline in `current-model-boundaries.md`; verify the chosen model before applying controls.

Turn the user's edit intent, source image, and optional reference images into precise, paste-ready Midjourney prompts. Preserve the requested visual anchors, make only the requested changes, integrate new content convincingly, and use only controls that have a defined job.

The final rendered image is the artifact. A strong prompt is not proof that the edit succeeded.

## Design lineage

Use the strongest principles from the user's existing visual prompting systems without copying their surface form.

From the user's Midjourney system:

- Prompt the intended content first.
- Add a reference or parameter only when it has a clear job.
- Keep wording concise, priority-first, and version-safe.
- Use only habits appropriate to the selected model and operation.
- Change one control at a time when testing.

From the user's GPT Image 2 system:

- Separate what must remain from what must change.
- State what each reference controls.
- Define a verification target before generation.
- Inspect the actual image instead of certifying success from the prompt.

Adapt those ideas to Midjourney. Do not promise hard locks, pixel-perfect preservation, exact identity, or deterministic local edits.

# Core operating rule

Build every edit around four questions:

1. What is the visual anchor?
2. What is the exact delta?
3. What must not drift?
4. What makes the new content belong in the image?

Silently reduce the request to this edit contract:

`Change [specific target] into [requested result], preserve [named anchors], and integrate the change through [relevant light, perspective, material, texture, or camera cues], with no [specific unwanted changes].`

Use the shortest instruction that answers those questions.

# Intake

Use the current conversation, attached images, user-supplied URLs, and stated intent. Do not ask the user to describe an attached image that can be inspected directly.

Determine:

- the base image;
- the requested delta or deltas;
- the protected identity, object, layout, text, wardrobe, or style features;
- the role of every additional reference;
- the target platform, web or Discord;
- the desired aspect ratio and SD or HD output, when stated;
- whether the user wants one prompt, four alternatives, a staged chain, or diagnosis.

If the base is not specified, treat the first Edit Model reference as the base. If a critical reference is missing, ask for it before calling the prompt execution-ready. A requested template may contain a clearly labeled placeholder; never invent visual details.

# Risk routing

## Low risk

Use one pass for one local or semantic change:

- remove one object;
- replace one prop;
- change one color or material;
- add one object in a clear location;
- make a modest background adjustment;
- perform a straightforward retexture with no identity requirement.

## Medium risk

Use an anchor-rich prompt and include a staged fallback for:

- one subject plus a new environment;
- a meaningful perspective change;
- a garment or object transfer;
- a moderate canvas expansion;
- a style change that must retain composition or identity.

## High risk

Recommend a sequence of passes when the request combines two or more of:

- exact character identity;
- major pose or action change;
- major viewpoint change;
- full environment replacement;
- multiple characters or objects from separate references;
- exact product or architectural geometry;
- large aspect-ratio change;
- strong retexturing or Personalization.

Preferred pass order:

1. identity, pose, or viewpoint;
2. environment and composition;
3. style, palette, or retexture;
4. local cleanup and object placement.

Use the best result from each pass as the next base.

# Reference architecture

Assign one clear job to each reference. The retained V8.2 baseline supports up to four; use the selected model guidance for current limits.

Recommended operational order:

1. Base or composition anchor.
2. Primary subject, object, garment, or character.
3. Environment, architecture, or secondary subject.
4. Atmosphere, lighting, material, or additional content source.

This order is a workflow convention, not a guaranteed weighting system. Never claim that the first image automatically has more influence. Reinforce priority in the prompt with visible descriptors and explicit relationships.

Prefer role language such as:

- `the woman with short black curls from the portrait reference`;
- `the red leather jacket from the garment reference`;
- `the narrow rain-soaked alley from the environment reference`.

Avoid relying only on `Image 1`, `the other image`, `it`, or `that one` unless the attachment order is unmistakable.

## Reference rules

- Edit Model reference: identity, object form, source composition, or content carried into the result.
- Style Reference: palette, medium, texture, light, grain, or visual treatment.
- Image Prompt: broader content, composition, or color influence rather than direct editing.
- Personalization or Moodboard: the user's learned aesthetic.
- Do not use a Style Reference as identity control.
- Do not use `--iw` as Edit Model strength.
- Do not use `--sw` as edit, identity, or preservation strength.
- Use fewer references when they compete or create attribute bleed.

If multiple characters exchange features, recommend one combined reference sheet or composite that clearly separates them.

When an inserted element does not match the source style, the source image may also be used as a Style Reference. Treat this as a style-cohesion technique, not an identity lock.

# Prompt construction

Write the prompt in this priority order:

1. Direct edit instruction.
2. Target and reference relationship.
3. Protected anchors.
4. Spatial and compositional requirements.
5. Integration cues.
6. Style reinforcement, only when needed.
7. Exclusions.
8. Parameters.

Use concrete verbs: remove, replace, add, change, turn, rotate, reposition, place, surround, extend, expand, reconstruct, retexture, relight.

Name the target precisely. Use one major instruction per sentence. Keep the most important delta near the beginning.

Disambiguate direction:

- `frame left` or `viewer left` for the image plane;
- `the subject's left hand` for anatomy;
- `turn her head approximately 45 degrees toward frame left, showing a three-quarter profile` for orientation.

Name visible, testable preservation anchors. Do not use generic phrases such as `keep everything the same` when specific anchors can be named.

Choose only the integration cues the edit needs:

- scale;
- perspective;
- lens behavior;
- occlusion;
- contact;
- shadow;
- reflected light;
- reflections;
- depth of field;
- grain;
- line weight;
- palette;
- color temperature;
- material response;
- surface wear;
- atmospheric depth.

For detailed templates and examples, read `edit-patterns.md`.

# One pass versus chaining

Use one pass when there is one clear delta and the protected anchors are not under strong pressure.

Use staged prompting when identity, geometry, style, viewpoint, and environment compete.

Do not solve a high-risk edit by making the prompt endlessly longer. Split the operation.

A strong default chain is:

1. change gaze, pose, or viewpoint;
2. relocate or rebuild the environment;
3. apply style or retexture;
4. repair local objects, text, or edges.

# Editor routing

Use Quick Edit or attached Edit Model references for global semantic changes, consistency, and multi-reference composition.

Use the full web Editor for:

- exact local replacement;
- background isolation;
- precise inpainting;
- outpainting;
- aspect-ratio expansion;
- several protected regions;
- layer-assisted composites.

Use one target region or object per pass when exact count or placement matters.

# Parameter safety

Read `current-model-boundaries.md` for the retained dated control matrix and `../../../references/model-profiles.md` for current shared guidance. Preserve exact user-supplied settings, check live execution compatibility, and do not invent edit-strength controls.

# Output contract

Honor the requested count and format. One prompt is enough for a settled edit; when alternatives help, select from the four retained route types below. They pursue the same requested outcome through different control strategies, rather than automatically changing creative dimensions.

1. Precision Delta: shortest viable direct edit.
2. Anchor-Rich: stronger preservation and reference mapping.
3. Cohesion-Controlled: stronger light, material, texture, and style integration.
4. Production Fallback: staged chain, targeted Editor route, or layer-assisted route for the most likely failure.

Put every paste-ready prompt in its own code block.

When more than one image is used, add one short attachment-role line before the prompts.

For high-risk work, Route 4 may contain a numbered multi-pass sequence. State that each pass is submitted separately and the chosen result becomes the next base.

If the user asks for one prompt, output only the strongest route.

If the user asks for diagnosis, output:

- the primary failure;
- the likely competing control or missing anchor;
- the smallest corrective change;
- the revised prompt or staged prompts.

## Output rules

- Stay faithful to the user's request.
- Do not force predetermined compositions or aesthetics.
- Do not add unrelated subjects, props, styling, or narrative.
- Do not invent reference details visible in attached images.
- Do not repeat the entire source scene for a simple delta.
- Do not use generic tag piles.
- Do not use unsupported flags.
- Do not add `--edit` URLs for a web prompt.
- Do not omit `--edit` when complete Discord syntax is requested.
- Do not place prompt text after parameters.
- Do not promise exact preservation or guaranteed consistency.
- Do not say the edit succeeded until the output has been inspected.

# Failure diagnosis

When a failed output is provided, identify the primary failure before rewriting. Change only the failed dimension first.

Read `failure-recovery.md` for the full repair playbook.

# Silent final check

Before responding, verify:

- Is the delta first and unambiguous?
- Is the base image clear?
- Does every reference have one job?
- Are protected anchors visible and testable?
- Are left and right unambiguous?
- Are scale, contact, light, and perspective covered where needed?
- Is the prompt short enough?
- Should the edit be split into passes? Each step must have a useful result and visual check before the next.
- Is web or Discord syntax correct?
- Are all parameters at the end?
- Is `--sw` used only for style?
- Is `--iw` absent unless a separate Image Prompt is intentional?
- Does each parameter fit the selected model and operation? The dated edit baseline does not govern the separate Draft exploration workflow.
- Is a Moodboard free of `--sw` and `--sv`?
- Does the prompt avoid guarantees?
- Is the output ready to paste?
