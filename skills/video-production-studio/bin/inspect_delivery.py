#!/usr/bin/env python3
"""Inspect video metadata with ffprobe and evaluate basic requirements."""

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path


def probe_with_ffprobe(video: Path) -> dict:
    run = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_streams", "-show_format",
            "-of", "json", str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    probe = json.loads(run.stdout)
    streams = probe.get("streams", [])
    video_stream = next((item for item in streams if item.get("codec_type") == "video"), {})
    audio_streams = [item for item in streams if item.get("codec_type") == "audio"]
    try:
        duration = float(probe.get("format", {}).get("duration"))
    except (TypeError, ValueError):
        duration = None
    return {
        "provider": "ffprobe",
        "width": video_stream.get("width"),
        "height": video_stream.get("height"),
        "duration": duration,
        "audio_streams": len(audio_streams),
        "readable": bool(video_stream),
    }


def mdls_number(output: str, key: str):
    match = re.search(rf"^{re.escape(key)}\s*=\s*([0-9.]+)\s*$", output, re.MULTILINE)
    return float(match.group(1)) if match else None


def probe_with_mdls(video: Path) -> dict:
    run = subprocess.run(
        [
            "mdls",
            "-name", "kMDItemDurationSeconds",
            "-name", "kMDItemPixelWidth",
            "-name", "kMDItemPixelHeight",
            "-name", "kMDItemCodecs",
            "-name", "kMDItemAudioBitRate",
            str(video),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    width_value = mdls_number(run.stdout, "kMDItemPixelWidth")
    height_value = mdls_number(run.stdout, "kMDItemPixelHeight")
    duration = mdls_number(run.stdout, "kMDItemDurationSeconds")
    audio_bitrate = mdls_number(run.stdout, "kMDItemAudioBitRate")
    width = int(width_value) if width_value is not None else None
    height = int(height_value) if height_value is not None else None
    audio_streams = 1 if audio_bitrate and audio_bitrate > 0 else 0
    return {
        "provider": "mdls",
        "width": width,
        "height": height,
        "duration": duration,
        "audio_streams": audio_streams,
        "readable": width is not None and height is not None,
    }


def probe_media(video: Path) -> dict:
    if shutil.which("ffprobe"):
        return probe_with_ffprobe(video)
    if shutil.which("mdls"):
        return probe_with_mdls(video)
    raise OSError("neither ffprobe nor mdls is available")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--min-width", type=int)
    parser.add_argument("--min-height", type=int)
    parser.add_argument("--min-duration", type=float)
    parser.add_argument("--max-duration", type=float)
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.video.is_file():
        print(json.dumps({"valid": False, "error": "video file not found"}, indent=2))
        return 2
    try:
        probe = probe_media(args.video)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": f"media probe failed: {exc}"}, indent=2))
        return 2
    width = probe["width"]
    height = probe["height"]
    duration = probe["duration"]
    audio_streams = probe["audio_streams"]
    checks = {
        "readable": probe["readable"],
        "min_width": args.min_width is None or (isinstance(width, int) and width >= args.min_width),
        "min_height": args.min_height is None or (isinstance(height, int) and height >= args.min_height),
        "min_duration": args.min_duration is None or (duration is not None and duration >= args.min_duration),
        "max_duration": args.max_duration is None or (duration is not None and duration <= args.max_duration),
        "audio": not args.require_audio or audio_streams > 0,
    }
    result = {
        "valid": all(checks.values()),
        "file": str(args.video),
        "provider": probe["provider"],
        "bytes": args.video.stat().st_size,
        "width": width,
        "height": height,
        "duration_seconds": duration,
        "audio_streams": audio_streams,
        "checks": checks,
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
