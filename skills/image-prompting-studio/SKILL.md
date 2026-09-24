---
name: "image_prompting_studio"
description: "Write image-generation prompts: create, edit, camera studies, storyboards, typography, infographics, series, grids, brand interpretation, and Midjourney prompt syntax. Prepares prompts only; the user generates images in their own tool."
metadata: { "includeInPrompt": true }
---

# Image Prompting Studio

## Purpose

Turn a brief (and any supplied images) into copyable, faithful image-generation prompts the user can run in their own tool — Midjourney, ChatGPT Images, Gemini/Nano Banana, Seedream, Recraft, Ideogram, Luma, or anything else. Also review supplied prompts and rendered results against a brief. This skill prepares prompts only; it never generates images or submits generation jobs.

## Workflow

1. **Read the contract.** Follow [references/prompt-contract.md](references/prompt-contract.md) for counts, formats, reference handling, and delivery. It is the governing document for every task below.
2. **Route by deliverable.** Pick one primary task guide from the table; the user's explicit task choice wins. Supporting references can help without creating a mandatory chain of skill reads.
3. **Check the model profile.** When the user names a model, consult only its entry in [references/model-profiles.md](references/model-profiles.md). With no model named, write a broadly compatible non-Midjourney prompt. Model profiles are dated (verified 2026-09-13); refresh them on the user's request, not silently.
4. **Extract locks.** Subject, action/setting, medium, mood, exact copy, aspect ratio, supplied references, requested count. Treat explicit user details as fixed. Ask only when the missing answer would materially change the result; useful alternatives can cover ordinary creative ambiguity.
5. **Choose a format.** See [references/formats.md](references/formats.md): natural-language brief, JSON envelope, or system-style operating prompt. Preserve the user's choice. Templates live in `references/templates/`.
6. **Draft and validate.** Write the prompt(s), then run the completion checklist below before delivering.

### Task routing table

| Requested work | Task guide |
|---|---|
| General scene, subject or concept | [references/tasks/create.md](references/tasks/create.md) |
| Targeted change or image-only exploration | [references/tasks/edit.md](references/tasks/edit.md) |
| Viewpoint, lens or framing alternatives | [references/tasks/camera.md](references/tasks/camera.md) |
| Coverage or frame blueprint before prompting | [references/tasks/shot-planner.md](references/tasks/shot-planner.md) |
| Combine references with roles and priority | [references/tasks/reference-composer.md](references/tasks/reference-composer.md) |
| Facts and current references are the main missing ingredient | [references/tasks/research.md](references/tasks/research.md) |
| Continuity across related images | [references/tasks/series.md](references/tasks/series.md) |
| One prompt must request multiple separate image files | [references/tasks/multi-output.md](references/tasks/multi-output.md) |
| Lettering or exact multilingual text is central | [references/tasks/typography.md](references/tasks/typography.md) |
| Factual relationships, labels, data or process | [references/tasks/infographic.md](references/tasks/infographic.md) |
| Poster, cover, spread or image/text page composition | [references/tasks/editorial.md](references/tasks/editorial.md) |
| Ordered narrative or instructional beats | [references/tasks/storyboard.md](references/tasks/storyboard.md) |
| One composite grid with multiple cells | [references/tasks/campaign-grid.md](references/tasks/campaign-grid.md) |
| Apply brand visual language to a creative image concept | [references/tasks/brand.md](references/tasks/brand.md) |
| Faithful illustration to photo or photo to illustration | [references/tasks/illustration-photo.md](references/tasks/illustration-photo.md) |
| Creative medium/style transformation | [references/tasks/style.md](references/tasks/style.md) |
| Age, season, historical change, decay or restoration | [references/tasks/time.md](references/tasks/time.md) |
| Spatial arrangement is the main design problem | [references/tasks/layout.md](references/tasks/layout.md) |
| Assess or repair supplied prompts | [references/tasks/review.md](references/tasks/review.md) |
| Midjourney creation prompt syntax | [references/tasks/midjourney.md](references/tasks/midjourney.md) |
| Midjourney editor, edits or retexture prompts | [references/tasks/midjourney-edit.md](references/tasks/midjourney-edit.md) |

### Resolving overlap

- A poster usually belongs to editorial; lettering as the subject belongs to typography; factual relationships belong to infographic; spatial arrangement as the main problem belongs to layout.
- A coherent set belongs to series; ordered storytelling belongs to storyboard. One submission yielding separate files → multi-output. One composite grid → campaign-grid.
- Faithful photo/illustration translation keeps the reference's recognizable character or world; broader medium/style reinterpretation belongs to style.
- A brand name alone does not turn an ordinary image prompt into a brand strategy task.
- Research can supply facts inside any task without becoming a compulsory second workflow.

## Output contract

- Every delivered prompt goes in its own triple-backtick code block (use `text` for Midjourney prompts).
- JSON prompts must parse as JSON after placeholders are filled. Use `bin/validate_prompt_payload.py` for a deterministic structural check of JSON prompts.
- Midjourney deliverables follow [references/midjourney-prompt-pack.md](references/midjourney-prompt-pack.md); a saved pack can be structurally checked with `bin/validate_prompt_pack.py --profile references/midjourney/current-model-profile.json`.
- For a singular request deliver one complete prompt; for open exploration choose a useful small set. No fixed quotas, mandatory diversity distributions, or word caps.
- Keep exact supplied copy, names and factual content. Never fill missing facts with plausible invented details; clearly distinguish proposed creative copy from approved copy.
- Put a direction note (two to four sentences) only when it helps explain variation axes or a consequential assumption; omit for prompt-only requests.

## Operating rules

1. **Prompts are the deliverable.** Do not generate images, submit jobs, operate queues, purchase credits, or call image-generation tools. If the user wants execution, hand over complete prompts and explain generation happens in their chosen tool.
2. **Read supplied images before describing them.** Name references by visible content and role. Do not force reposing into faithful medium conversions.
3. **Never invent** parameters, style codes, personalization IDs, image URLs, or model settings. Copy supplied reference strings exactly. Describe only supported controls per the loaded model profile.
4. **No acceptance claims.** Prompt preparation does not prove rendered or creative success. When rendered results are available, inspect the actual images and report observed drift; without them, label conclusions as prompt review only. The user selects preferred results.
5. **Save a recipe as a reusable preferred result only after the user explicitly selects it.**
6. **Ask for personal input when it matters.** If the task needs brand assets, reference images, exact copy, or a named model the user hasn't given, ask rather than inventing.
7. **Do not claim verification you didn't do.** A SEARCH phrase is not evidence of retrieval; browsing on this host is available for factual tasks — use it and supply verified facts.

## Examples

Illustration → photo (attach images the user is authorized to use):

```text
Convert these illustrations into photographic prompts, one per image. Preserve the recognizable subject, pose, composition and world; explain the material, light and texture changes needed for a photograph. Each complete prompt in its own code block. Prompts only.
```

Midjourney series:

```text
Write a coherent Midjourney still-life series for these products. Keep the same surface, lighting logic and material treatment with a suitable composition for each object. Use only supported Midjourney parameters and explain consequential choices. Each prompt in a separate code block. No image generation.
```

Everyday scenes plus an edit (attach the scene image; name a model or accept broadly compatible language):

```text
Write everyday-scene prompts: making coffee in a small kitchen, reading on a train, browsing a market stall — natural light, ordinary camera feel. Then write an edit prompt for the attached kitchen image moving the scene to a balcony while preserving the person. Prompts only.
```

## Completion checklist (run before every delivery)

- Requested or context-appropriate prompt count is present.
- Every locked detail, exact copy string, and supplied reference value is preserved.
- Variations are meaningfully different without concept drift.
- Each prompt is coherent visual language, not a disconnected keyword pile.
- Parameters (if any) are at the end, supported by the loaded profile, and never invented.
- No unresolved placeholder, invented URL/code, or unsupported feature presented as ready.
- JSON payloads parse; use the validators when a deterministic check is useful.
- No image-generation tool was called; delivery explains prompts are run separately by the user.
