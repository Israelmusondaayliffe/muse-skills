# Graphic overlays

Design rules for lower thirds, callouts, labels, frames, and picture
compositions on existing footage. Implementation is ffmpeg-native
(`drawtext`, `overlay`, `subtitles`); see references/rendering-recipes.md
for the commands.

## Layout patterns

- **Lower third**: name + title, bottom-left, inside the title-safe margin
  (≥ 80px at 1080p). One accent bar or rule; no boxes behind text unless
  contrast demands it (then a 60–70% black plate).
- **Callout**: short label + thin leader line pointing at the subject. Keep
  leader lines ≤ 2px, labels ≤ 6 words.
- **Split**: two sources side by side — use for before/after. Equal halves
  only when both deserve equal weight.
- **Stack**: vertical arrangement for portrait delivery.
- **PiP**: inset ≤ 25% of frame area, bottom-right default, 60px margins.

## Type and contrast

- Headline 64–96px, body 40–48px at 1080p. Never below 40px for anything
  the viewer must read.
- White text with a dark outline or plate passes on any footage; colored
  text must clear WCAG-ish contrast against its actual background — check
  on a real frame, not in your head.
- One font family per video, two weights max. Confirm the font file exists:
  `fc-list | grep -i "<name>"`.

## Source images as evidence

Screenshots, tweets, charts, code, documents, and anything with readable
text are **content evidence, not decoration**: preserve the source aspect
ratio (`force_original_aspect_ratio=decrease` + `pad`, never stretch).
After fitting, inspect all four edges for truncated text or logos — a
visible crop on meaningful content is a bug unless the source itself
cropped it. Decorative/background images may fill-frame (`increase` +
`crop`).

## Timing

- Overlays enter after the cut (≥ 0.3s in) and exit before it (≥ 0.3s out).
- `enable='between(t,A,B)'` windows per overlay; stagger stacked elements
  by ~0.15s.
- Never cover faces, captions, or the video's own lower-third region with
  a new overlay.

## Transcription (for overlay copy)

When overlay copy comes from speech, transcribe from the narration script
or word timings (references/voiceover.md) — do not invent quotes. Correct
names, terms, and numbers against the source before burning in.
