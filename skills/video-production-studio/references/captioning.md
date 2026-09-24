# Captioning

Burned-in (open) captions via `bin/burn_captions.py`, which renders an SRT
(or word timings) into the video with ffmpeg's `subtitles` filter.

## Transcript sources (in order of reliability)

1. The narration `SCRIPT.md` — verbatim truth when the video was voiced
   from it.
2. Word timings from the podcast skill (`audio/words.json`) → build the SRT
   with `--words` (see references/voiceover.md).
3. A user-supplied transcript.
4. Manual authoring while watching the video. Last resort — state that
   timing was done by hand.

Never claim caption accuracy when no caption source exists.

## SRT authoring rules

- ≤ 2 lines per cue, ≤ 42 characters per line.
- Minimum cue duration 1s; maximum ~7s. Split long sentences.
- Break lines on phrase boundaries, not mid-phrase.
- Drop filler (um/uh, stutters, self-corrections) unless the user wants
  verbatim.

## Burn

```bash
python3 <SKILL_DIR>/bin/burn_captions.py in.mp4 captions.srt -o renders/captioned.mp4
```

Default style: Noto Sans 28px, white with dark outline, bottom-centered,
48px margin — readable on most footage. Override with `--style` (ffmpeg
`force_style` syntax) or `--font "FontName"`.

Check the font exists first: `fc-list | grep -i "<name>"`.

## Caption design guidance

- **Rail (default):** clean lower-third verbatim subtitles. Right for
  explainers, voiceover, talking-head — anywhere the words must read.
- **Embedded peaks:** for stylized pieces, promote ≤ 1 key word per beat
  to large in-scene typography (drawtext with `enable='between(t,a,b)'`,
  sized 2–3× rail text). Scarcity is the point — embedding every word is
  the common mistake.
- Safe areas: keep captions ≥ 48px from the bottom at 1080p, inside the
  title-safe margin, and clear of platform UI chrome (assume bottom 10%
  may be covered on social).

## QC

Spot-check caption timing against speech at the start, middle, and end of
the video (see references/delivery-qc.md). Record exact timestamps for
every sync failure.
