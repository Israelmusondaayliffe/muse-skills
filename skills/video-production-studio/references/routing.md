# Routing — brief to production path

Pick ONE primary route before generating any asset. The route sets which
reference guides and production surfaces the build uses.

## Routes

| Route | Triggers | Guide |
|---|---|---|
| `faceless-explainer` | Topic explainer from text/notes; no product, no URL; every visual invented | references/shared-pipeline.md + ai-assets.md |
| `product-launch` | Marketing, launching, promoting, or revealing a product (even from a URL) | references/shared-pipeline.md + website-capture.md |
| `pr-story` | GitHub PR → code-change explainer (changelog, feature reveal, fix) | references/pr-explainer.md |
| `website-capture` | Tour/showcase/social clip OF a general website (not a launch) | references/website-capture.md |
| `music-visualization` | Beat-synced video from a music track | references/music-video.md |
| `slideshow` | Still-image or deck-led video; photo montages, pitch decks | references/rendering-recipes.md (`bin/assemble_slideshow.py`) |
| `motion-graphics` | Short (≤ ~30s), unnarrated, design-led: kinetic type, stat hit, logo sting, lower third, chart | references/motion-graphics.md |
| `general-video` | Mixed or custom production no specialist route owns | references/shared-pipeline.md |
| `ai-generation` | Prompt-led AI clips only (user wants generated footage, no assembly) | references/ai-assets.md |
| `captions-only` | Add burned-in captions to an existing video file | references/captioning.md |
| `overlays-only` | Lower thirds, callouts, labels on existing footage | references/graphic-overlays.md |

Supporting steps used inside routes: `captions` (captioning.md), `overlays`
(graphic-overlays.md), `voiceover` (voiceover.md), `delivery-qc`
(references/delivery-qc.md — required for every rendered delivery).

## Route selection rules

- If the user named a product being marketed → `product-launch`, even from a URL.
- If the user gave a URL and the intent is a tour/showcase → `website-capture`.
- If the user gave a GitHub PR → `pr-story`.
- If the user gave a music track → `music-visualization`.
- If the user gave text/notes and a topic → `faceless-explainer`.
- If the user gave images and wants a video → `slideshow`.
- Short, no narration, motion is the message → `motion-graphics`.
- "Add captions/subtitles to this video" → `captions-only`.
- Unclear or "make a video" with no specifics → ask ONE clarifying question,
  then route. Do not build before the route is chosen.

## Runtime selection (Hatch)

Runtimes are the production surfaces actually available here — record the
choice in the route JSON and validate with `bin/validate_route.py`:

- `ffmpeg` — assembly, slideshows, overlays, caption burn-in, audio mixing.
  Check before choosing it: `command -v ffmpeg ffprobe`. If either is
  missing, rendering is blocked; do not record `renderer_available: true`.
- `ai-generation` — only when `media.generate_image` / `media.generate_video`
  (or another generation tool) appears in the current tool list and the user
  approved its cost. Use it for
  AI-created visuals and clips.
- `browser-capture` — delegate a live-browser task for website screenshots/
  scroll capture when the user asked for a website video.
- `hybrid` — two or more of the above (the common case).
- `external` — the user supplies finished footage; the studio only assembles,
  captions, or QCs it.
- `none` — planning only (see references/planning-bundle.md).

Never claim a renderer you did not use. When the user asked only for a plan,
use runtime `none` and completion state `planning-complete`. When the user
asked for a clip, a plan is never the finished state: use `rendered-partial`
or `blocked` and list what is missing.
