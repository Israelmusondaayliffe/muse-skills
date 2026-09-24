# AI-generated assets

Use `media.generate_image` and `media.generate_video` for AI-created visuals.
These run through a media subagent — pass the user's request text verbatim
(one image/video per call, max four image calls per turn).

## Image assets

- Stills for slideshow beats, backgrounds, thumbnails, overlays.
- Generate at the target aspect (ask for 16:9/9:1/1:1 in the prompt text).
- Inspect every result before using it (the tool returns `local_path`).

## Video clips

- Short AI clips as beats or B-roll, then assemble with ffmpeg
  (references/rendering-recipes.md). Chain a consistent look across clips
  with `resume_from_snapshot_id`.
- Keep AI clips short and cut on motion; do not stretch one clip past its
  natural length.

## Prompt craft (distilled from the video-prompt-builder playbook)

Four modes — pick by input:

1. **BUILD** — brief/concept only → text-to-video. Write shot-by-shot
   prompts in ONE code block, shots separated by `---`. Director's notes
   tone: describe what happens, no hype adjectives ("stunning",
   "breathtaking"). Replace em-dashes with periods or commas.
2. **ANIMATE** — user supplied image(s) → image-to-video: single image +
   motion intent; two images → first/last frame; several → role-based
   (subject / style / environment / structural-guide, mark what must NOT
   render).
3. **DECONSTRUCT** — user references an existing video → break it into the
   effects format first (shots, camera, effects, energy arc), then build.
4. **REMIX** — user has an effects breakdown + a new subject → transfer the
   effects architecture to the new subject.

Shot prompt anatomy: subject + action → camera (lens, move, framing) →
environment/lighting → effects timeline → energy/pacing note → consistency
constraints (character, physics, anatomy — name what must NOT change).

Failure modes to write around: text/typography in-frame (AI mangles it —
overlay text in ffmpeg instead), hands, fast complex motion, morphing
faces across cuts. Keep prompts under ~60s of described action per clip;
for longer, plan extensions and join in ffmpeg.

## Validation

For structured multi-shot prompt documents, run:

```bash
python3 <SKILL_DIR>/bin/validate_video_prompt.py PROMPT.md --profile seedance-2.5 --mode MODE
# python3 <SKILL_DIR>/bin/validate_video_prompt.py --help  # modes: text-to-video, continuous-one-take,
#   beat-cut-music-video, omni-reference, first-last-frame, extension, visual-edit,
#   audio-edit, ultra-long, storyboard, blockout, green-screen, clip-join
```

This checks prompt structure (code blocks, timestamp ordering, reference
tags) — not whether any external service is available or how a generation
turned out. For Hatch's own `media.generate_video`, the structural habits
(single code block, `---` separators, shot anatomy) still apply; the
Seedance-specific tag syntax is optional.
