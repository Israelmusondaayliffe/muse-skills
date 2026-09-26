# Delivery QC

A playable file is the START of delivery verification, not the end. Run
technical checks and visual inspection on every rendered delivery, then
record the result.

## Technical checks

```bash
python3 <SKILL_DIR>/bin/inspect_delivery.py renders/final.mp4 \
  --width 1920 --height 1080 \
  --min-duration 28 --max-duration 32 \
  --require-audio --output renders/qc-technical.json
```

`inspect_delivery.py` uses ffprobe (with a macOS `mdls` fallback that a
Linux host will not have). Pass `--width`/`--height` for exact dimensions. It checks the file
is readable, dimensions, duration bounds, and audio presence, and exits
non-zero on failure. If ffprobe cannot read the file, report technical
verification as **blocked**, not passed.

## Visual inspection

Extract frames and look at them — `ffmpeg -ss <t> -i renders/final.mp4
-frames:v 1 check_<t>.png`. Inspect at minimum:

1. Opening frame and first three seconds.
2. A text-heavy moment — size, contrast, spelling, safe areas.
3. A transition-heavy moment — dropped frames, abrupt motion.
4. Midpoint — visual and audio continuity.
5. Final frame and call to action.
6. Caption timing against speech at start, middle, end.
7. Source media — cropping, stretching, color shifts, missing content.

Record exact timestamps for every failure. Keep platform-safe-area
assumptions explicit (assume bottom 10% may be covered on social).

## Caption and audio checks

- If no caption source exists, do not claim caption accuracy.
- Audio: narration intelligible, BGM ducked, no clipping, SFX not
  masking speech. Check the first and last 2 seconds for pops/cutoffs.

## Report

Copy `assets/qc-report-template.md` to the project's `qc-report.md` and
fill it in. Result is **pass**, **fail**, or **blocked** — and any untested
requirement is listed as untested, never assumed.

## Fix loop

Fix failures, re-render, and rerun BOTH technical and visual checks. A
re-render invalidates the previous visual pass.
