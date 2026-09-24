---
name: "video-production-studio"
description: "Coordinate brief-to-video production: route the request, plan, build, and QC the delivery. Use when the user wants a video made — explainers, product launches, PR explainers, website tours, music videos, slideshows, motion graphics, AI-generated clips, captions or overlays on existing footage — or asks for a video production plan. Routes to one production path, renders with ffmpeg and AI media tools, and verifies every delivery."
---

# Video Production Studio

## Purpose

Take a video request from brief to verified delivery on Hatch. The studio
routes each brief to one primary production path, runs a gated build
pipeline, and quality-checks the render before handoff.

## Workflow

1. **Clarify the brief.** Extract objective, audience, duration, aspect
   ratio, platform, narration (yes/no), and source assets. Ask one compact
   question covering only what is missing, with recommended defaults
   pre-filled. Never invent brand, product, or personal details — ask.
2. **Route.** Pick ONE route from `references/routing.md`. Record it in
   `route.json` (copy `assets/route-template.json`) and validate:
   `python3 bin/validate_route.py route.json`. Choose the runtime from
   actually-available surfaces: `ffmpeg` (always), `ai-generation`
   (`media.generate_image`/`media.generate_video`), `browser-capture`
   (delegate a live-browser task), `hybrid`, `external` (user footage),
   or `none` (planning only).
3. **Plan or build.** For plan-only requests (or when production is
   impossible here), write the six-file planning bundle per
   `references/planning-bundle.md` and stop at `planning-complete`.
   Otherwise run the route's pipeline — most routes follow
   `references/shared-pipeline.md` (brief → design → storyboard/script →
   audio → build → assemble → QC).
4. **Keep the gates.** Storyboard approval before building; technical +
   visual QC after rendering (`references/delivery-qc.md`). Verification
   gates never skip — autonomous mode only skips preference questions.
5. **Deliver.** Render MP4 only on explicit request. Hand off the file plus
   the QC report; include an honest "what I did NOT verify" section when
   anything was skipped.

## Output Contract

- A rendered delivery ends in `videos/<project>/renders/` with
  `qc-report.md` filled from `assets/qc-report-template.md`, technical
  checks from `bin/inspect_delivery.py`, and visual inspection recorded.
- Completion state is `rendered-delivery-complete` ONLY when a renderer
  produced the file and both QC passes ran. Otherwise `planning-complete`
  with rendering/visual-QC marked incomplete.
- Route JSON validates clean with `bin/validate_route.py`.

## Operating Rules

- **Build exactly what was asked.** A title card is a title card — propose
  additions, don't add them silently.
- **One route, one runtime decision, before asset generation.** Do not
  start building while the path is unclear.
- **No renderer fiction.** Never reference HyperFrames, Remotion, Codex,
  Claude Code, or their CLIs/hooks — they do not exist here. Production
  surfaces are: terminal + ffmpeg, `media.generate_image`/`generate_video`,
  delegated live-browser tasks, the podcast skill (voiceover), subagents
  (parallel frame/clip work), cron/hooks (scheduled renders, QC checks).
- **Media handling.** SFX: the bundled `assets/sfx/` library (Pixabay
  Content License, credits in `assets/sfx/CREDITS.md`). BGM: user-supplied
  or licensed — never rip from the web. AI visuals: inspect every
  generation before use.
- **Captions need a source.** Script, word timings, or transcript — without
  one, do not claim caption accuracy.
- **Slide/text minimums.** 72–96px headlines, ≥ 40px body at 1080p;
  title-safe margins ≥ 80px.
- **Async work.** Long renders run in the background; frame/clip builds
  fan out to subagents. The route record and QC report are the durable
  handoff — write them to the project dir, not the chat.

## Resources

- `bin/` — `validate_route.py` (route validation), `inspect_delivery.py`
  (ffprobe technical QC), `validate_video_prompt.py` (AI prompt structure
  checks), `assemble_slideshow.py` (images + Ken Burns + audio → MP4),
  `burn_captions.py` (SRT/word-timings → burned-in captions).
- `references/` — `routing.md`, `shared-pipeline.md`, `rendering-recipes.md`,
  `voiceover.md`, `captioning.md`, `ai-assets.md`, `website-capture.md`,
  `pr-explainer.md`, `music-video.md`, `motion-graphics.md`,
  `graphic-overlays.md`, `delivery-qc.md`, `planning-bundle.md`.
- `assets/` — `route-template.json`, `qc-report-template.md`, `sfx/`
  (19 licensed sound effects + manifest + credits).
