# Shared production pipeline

The standard 7-stage build used by `faceless-explainer`, `product-launch`,
`general-video`, and `pr-story`. Route-specific guides add their own capture
or analysis steps in front; the stages below stay the same.

Work in `PROJECT_DIR = ~/workspace/videos/<project-name>/` (kebab-case from
the topic, e.g. `acme-launch`; never a timestamp). Layout:

```
videos/<project>/
  route.json            # route decision (assets/route-template.json), validated
  STORYBOARD.md         # scenes/beats with timing, visuals, transitions
  SCRIPT.md             # narration script (when narrated)
  assets/               # source media, ledger in assets/index.md
  audio/                # narration.wav, bgm.mp3, sfx/, audio_meta.json
  build/                # intermediate clips, slides, frames
  renders/              # final delivery files
  qc-report.md          # delivery QC record
```

## Stage 0 — Setup and brief

Lock: objective (what the viewer should understand or do), audience, duration,
aspect ratio, platform, narration (yes/no), source assets. Ask only what is
missing — one compact question, with recommended defaults pre-filled.

## Stage 1 — Design system

Write a short `DESIGN.md`: palette (exact hex), font pairing, visual motif,
do's/don'ts. Keep it to one page. For brand videos, derive it from captured
site tokens (references/website-capture.md); otherwise pick deliberately —
no default blue/gray, no system-ui-as-brand.

## Stage 2 — Storyboard + script (user gate)

Write `STORYBOARD.md` concept-first: message → narrative arc → beats that
serve the arc → technique per beat. Then `SCRIPT.md` for narration, one line
per beat. When the user asked for a finished video and supplied what it
needs, that request authorizes the build: write the storyboard, show a
short beat summary alongside the work, and keep building. Stop for approval
only when the user asked to review the plan first, when a key fact (product
claims, names, brand copy) is missing, or before any paid generation.

Slide/beat writing rules (from the slideshow and explainer playbooks):

- Headline is a complete-sentence claim, not a label.
- One idea + one visual per beat; split crowded beats.
- Lead with the punchline — strongest point first.
- Market sizing bottom-up only: never a bare "$50B TAM" without the math.
- Text minimums at 1080p: headlines 72–96px, body ≥ 40px.

## Stage 3 — Audio

See references/voiceover.md. Narration via the podcast skill (script in,
`narration.wav` + word timings out). Music bed: user-supplied track, or a
track from `assets/sfx/` for SFX; for BGM ask the user or use a licensed
source — never rip from the web. Mix narration + BGM + SFX with ffmpeg;
duck BGM under narration (`sidechaincompress`).

## Stage 4 — Build visuals

Per the route: AI-generated clips (references/ai-assets.md), Ken Burns
slideshow (`bin/assemble_slideshow.py`), screen captures
(references/website-capture.md), or ffmpeg motion graphics
(references/motion-graphics.md). Build one beat at a time; keep each
intermediate in `build/`.

## Stage 5 — Assemble

Concat beats, add transitions (xfade for crossfades, or hard cuts on beat
grids), mix audio, burn captions if requested (references/captioning.md).
Output to `renders/<project>-v1.mp4` (h264, yuv420p, aac).

## Stage 6 — Deliver (render gate)

A request for a video is a request for the rendered file: render the MP4.
Deliver only a plan when the user asked for a plan, or when rendering is
blocked (then say what blocked it).

## Stage 7 — QC

`bin/inspect_delivery.py` for technical checks + the visual inspection in
references/delivery-qc.md. Record `qc-report.md` from
assets/qc-report-template.md. Fix failures, rerun both checks.

## Gates that never skip

- Cost approval before any paid generation or narration call.
- Technical + visual QC (Stage 7) — a rendered file is not complete until
  both pass. Report untested requirements honestly; never claim a pass you
  did not run.
