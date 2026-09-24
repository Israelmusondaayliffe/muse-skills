# Task: Camera directions (viewpoint studies)

Scope: controlled viewpoint studies or natural new shots from a reference — camera angle, framing, shot distance, turnarounds, still endpoints — preserving the intended character, object or world.

Read first: `../prompt-contract.md`. When a model is named, consult only its entry in `../model-profiles.md`.

## Choose the kind of change

- Camera-only study: retain subject state, style, environment, physical lighting; the new viewpoint changes what is visible and how the same light is seen.
- New shot in a shoot: pose, gaze, expression, action, lighting can develop naturally while keeping continuity.
- Do not force every axis to freeze or demand a secondary pose change. Follow combined instructions (e.g. new angle at night) without a needless mode question.

Inspect the reference before describing it. Record the few identity, design, world, palette and style anchors that distinguish it. Unknown back surfaces or off-frame space are plausible inference, not recovered facts.

## Write the directions

Use `../recipes/camera_directions/camera-methods.md` for distance, perspective, lighting continuity, objects/worlds, turnarounds and the still/video boundary. Read `camera-light-vocabulary.md` when optical or lighting detail changes the prompt. Read only the templates the job needs:

- `controlled-angle-templates.md`: preservation-heavy viewpoint studies, panoramic candidate
- `source-nano-camera-templates.md`: concise directions, four-view character sheet
- `angle-recipes.md`: curated twelve-shot shoot with composition, portrait, wardrobe, accessory examples

Each prompt names the reference, camera position, distance/crop, what becomes visible, and allowed changes. Requested counts win over recipe-bank counts. Preserve exact target style and aspect ratio unless the brief permits a change.

## Checks

Meaningful viewpoint differences, reference continuity, each still coherent from its camera. Distinguish separate image prompts, one composite turnaround, and an actual camera move. A still can depict an endpoint or implied-motion moment; continuous motion needs a video deliverable — explain that boundary without requiring another skill. When images are available, compare them to the reference and report observed drift; never claim preservation from wording alone.
