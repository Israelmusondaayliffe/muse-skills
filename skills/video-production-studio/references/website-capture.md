# Website capture → video

Route `website-capture`: a tour, showcase, or social clip OF a general site
(not a product launch — that is `product-launch` + this guide's capture
mechanics).

## Step 0 — Capture (browser delegation)

This skill cannot drive the live browser itself. Delegate a browser task:
"Capture <URL>: full-page screenshot at 1920×1080 and 1080×1920, plus
screenshots of <key sections>; record brand tokens (primary colors as hex,
font families, logo files). Save everything under the project
`capture/` directory."

Gates: the site summary is written strategy-first (what the product does,
who it's for, brand voice) before the asset/color/font inventory; capture
files exist on disk.

If the site blocks capture, note `capture/BLOCKED.md` and continue with
the no-capture path (brand tokens hand-written from the brief).

## Step 1 — Brand identity

Write `DESIGN.md` from captured tokens: exact palette, typography, component
style, do's/don'ts. Fast path for billboard-style social ads: a 50-line
colors + fonts + do's/don'ts summary.

## Step 2 — Brief

Lock video type, duration, format, and — critically — the ONE message and
narrative arc. Duration drivers: social ad 10–15s (platform limit), product
demo 30–60s (script length), feature announcement 15–30s, brand reel 20–45s
(music track), launch teaser 10–20s. Beat count follows the storyboard,
never a table.

## Step 3 — Storyboard + script (user gate)

Concept-first: message → arc → beats → technique per beat → brand accents
pass last. Write `STORYBOARD.md` + `SCRIPT.md`; present the beat-by-beat
summary and iterate until the user approves.

## Step 4 — Voiceover and timing

references/voiceover.md. Narration optional; if none, set manual beat
timings from the storyboard. Map real audio durations back onto beats.

## Step 5 — Build

Assemble from captures: Ken Burns moves over screenshots
(`bin/assemble_slideshow.py`), callout overlays
(references/graphic-overlays.md), AI B-roll for transitions
(references/ai-assets.md). Read every beat's build output top-to-bottom
against `DESIGN.md` and `STORYBOARD.md` before rendering.

## Step 6 — Validate and deliver

`bin/inspect_delivery.py` + references/delivery-qc.md. Render MP4 only on
explicit request. At handoff, include an honest "What I did NOT verify"
section when anything was skipped — verification gates are never skipped
in autonomous mode, only user-preference questions are.

## Formats

Landscape 1920×1080 default; portrait 1080×1920 (Stories/TikTok); square
1080×1080 (feed).
