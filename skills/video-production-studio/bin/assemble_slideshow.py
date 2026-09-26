#!/usr/bin/env python3
"""Assemble a slideshow video from still images with optional Ken Burns motion and audio.

Usage:
    python3 assemble_slideshow.py manifest.json -o out.mp4

manifest.json:
    {
      "width": 1920, "height": 1080, "fps": 30,
      "slides": [
        {"image": "slide1.png", "duration": 4.0, "motion": "zoom-in"},
      ],
      "audio": "bgm.mp3",
      "audio_fade_out": 2.0
    }

motion is one of: static, zoom-in, zoom-out, pan-left, pan-right.
Requires ffmpeg and ffprobe on PATH. Exits 3 when either is missing or an
ffmpeg step fails, so the caller can report rendering as blocked.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def build_filter(motion: str, width: int, height: int, frames: int, fps: int) -> str:
    # d=1: one output frame per input frame; `on` counts frames so the zoom
    # progresses across the slide's own frames (input is -loop 1 at fps).
    scale_up = f"scale={width * 2}:{height * 2}:force_original_aspect_ratio=increase"
    crop_fill = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
    n = max(frames - 1, 1)
    if motion == "zoom-in":
        return (
            f"{scale_up},zoompan=z='1+0.25*on/{n}':d=1"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps}"
        )
    if motion == "zoom-out":
        return (
            f"{scale_up},zoompan=z='1.25-0.25*on/{n}':d=1"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps}"
        )
    if motion == "pan-left":
        return (
            f"{scale_up},zoompan=z=1.15:d=1"
            f":x='(iw-iw/zoom)*on/{n}':y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps}"
        )
    if motion == "pan-right":
        return (
            f"{scale_up},zoompan=z=1.15:d=1"
            f":x='(iw-iw/zoom)*(1-on/{n})':y='ih/2-(ih/zoom/2)':s={width}x{height}:fps={fps}"
        )
    return crop_fill


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    missing = [tool for tool in ("ffmpeg", "ffprobe") if shutil.which(tool) is None]
    if missing:
        print(f"blocked: {', '.join(missing)} not found on PATH", file=sys.stderr, flush=True)
        return 3
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    try:
        return assemble(manifest, args)
    except subprocess.CalledProcessError as exc:
        print(f"blocked: ffmpeg step failed (exit {exc.returncode}): {' '.join(map(str, exc.cmd[:6]))} ...",
              file=sys.stderr, flush=True)
        return 3


def assemble(manifest: dict, args: argparse.Namespace) -> int:
    width = int(manifest.get("width", 1920))
    height = int(manifest.get("height", 1080))
    fps = int(manifest.get("fps", 30))
    base = args.manifest.parent
    slides = manifest.get("slides", [])
    if not slides:
        print("manifest has no slides", flush=True)
        return 2

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        segments = []
        for i, slide in enumerate(slides):
            image = base / slide["image"]
            if not image.is_file():
                print(f"slide {i}: image not found: {image}", flush=True)
                return 2
            duration = float(slide.get("duration", 4.0))
            motion = slide.get("motion", "zoom-in")
            frames = max(int(round(duration * fps)), 1)
            vf = build_filter(motion, width, height, frames, fps)
            segment = tmp / f"seg{i:03d}.mp4"
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error",
                 "-loop", "1", "-framerate", str(fps), "-t", str(duration),
                 "-i", str(image),
                 "-vf", f"{vf},format=yuv420p",
                 "-frames:v", str(frames),
                 "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                 str(segment)],
                check=True,
            )
            segments.append(segment)

        concat_list = tmp / "concat.txt"
        concat_list.write_text(
            "".join(f"file '{s}'\n" for s in segments), encoding="utf-8"
        )
        silent = tmp / "silent.mp4"
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
             "-i", str(concat_list), "-c", "copy", str(silent)],
            check=True,
        )

        audio = manifest.get("audio")
        fade_out = float(manifest.get("audio_fade_out", 0) or 0)
        if audio:
            audio_path = base / audio
            if not audio_path.is_file():
                print(f"audio not found: {audio_path}", flush=True)
                return 2
            af = f"afade=t=out:st=0:d={fade_out}" if fade_out > 0 else "anull"
            # Fade applies from the end: compute via areverse trick is overkill;
            # use afade with start time = duration - fade_out via aduration probe.
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(silent)],
                check=True, capture_output=True, text=True,
            )
            total = float(probe.stdout.strip())
            af = f"afade=t=out:st={max(total - fade_out, 0):.2f}:d={fade_out}" if fade_out > 0 else "anull"
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", str(silent),
                 "-stream_loop", "-1", "-i", str(audio_path),
                 "-map", "0:v", "-map", "1:a", "-af", af,
                 "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                 "-shortest", str(args.output)],
                check=True,
            )
        else:
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", str(silent),
                 "-c", "copy", str(args.output)],
                check=True,
            )

    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
