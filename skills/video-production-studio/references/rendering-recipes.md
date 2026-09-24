# Rendering recipes (ffmpeg)

`ffmpeg`/`ffprobe` live at `/usr/bin/ffmpeg`, `/usr/bin/ffprobe`. All recipes
assume h264 + aac delivery (`-c:v libx264 -pix_fmt yuv420p -c:a aac`).

## Slideshow assembly

Use `bin/assemble_slideshow.py` — images + per-slide duration + Ken Burns
motion + optional audio → MP4:

```bash
python3 <SKILL_DIR>/bin/assemble_slideshow.py manifest.json -o renders/deck.mp4
```

Manifest: `width`, `height`, `fps`, `slides[]` (`image`, `duration` seconds,
`motion`: `zoom-in` | `zoom-out` | `pan-left` | `pan-right` | `static`),
optional `audio` (looped to fill the video) and `audio_fade_out` seconds.

## Concatenate clips

Same codec/size → concat demuxer (fast, lossless):

```bash
printf "file 'b1.mp4'\nfile 'b2.mp4'\n" > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy joined.mp4
```

Different sizes → normalize first:

```bash
ffmpeg -y -i in.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p norm.mp4
```

## Crossfade between two clips

```bash
ffmpeg -y -i a.mp4 -i b.mp4 -filter_complex \
 "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5[v]" \
 -map "[v]" -c:v libx264 -pix_fmt yuv420p out.mp4
```

Set `offset` to (duration of A − fade duration). Transitions: `fade`,
`fadeblack`, `slideleft`, `smoothleft`, `circleopen`.

## Lower third (drawtext)

```bash
ffmpeg -y -i in.mp4 -vf \
 "drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf:text='Ada Lovelace':fontsize=64:fontcolor=white:x=120:y=h-260:enable='between(t,2,8)',\
  drawtext=fontfile=/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf:text='CEO, Acme':fontsize=40:fontcolor=white:x=122:y=h-180:enable='between(t,2,8)'" \
 -c:v libx264 -pix_fmt yuv420p -c:a copy out.mp4
```

Escape `:` `'` in text with backslashes. Keep lower thirds inside the
title-safe area (≥ 80px margins at 1080p).

## Picture-in-picture

```bash
ffmpeg -y -i main.mp4 -i inset.mp4 -filter_complex \
 "[1:v]scale=480:270[pip];[0:v][pip]overlay=W-w-60:H-h-60:enable='between(t,3,10)'[v]" \
 -map "[v]" -map 0:a -c:v libx264 -pix_fmt yuv420p -c:a copy out.mp4
```

## Audio mix with ducking (narration over BGM)

```bash
ffmpeg -y -i narration.wav -i bgm.mp3 -filter_complex \
 "[1:a]volume=0.25,sidechaincompress=threshold=0.02:ratio=8:attack=20:release=400:makeup=1[bg];[0:a][bg]amix=inputs=2:duration=first[a]" \
 -map "[a]" -c:a aac -b:a 192k mix.m4a
```

SFX one-shots: `assets/sfx/` (19 Pixabay-licensed effects — whoosh, pop,
riser, chime, glitch, click; see `assets/sfx/CREDITS.md` and
`manifest.json`). Layer with `amix` or `adelay` + `amix`.

## Extract inspection frames

```bash
ffmpeg -y -ss 12 -i render.mp4 -frames:v 1 frame_12s.png   # single frame
ffmpeg -y -i render.mp4 -vf fps=1/5 thumbs_%03d.png         # contact sheet, 1 per 5s
```

## Fit to platform aspect

- Landscape 1920×1080 (default), portrait 1080×1920 (Stories/TikTok),
  square 1080×1080 (feed). Pad, don't stretch; keep text ≥ 40px equivalent.
