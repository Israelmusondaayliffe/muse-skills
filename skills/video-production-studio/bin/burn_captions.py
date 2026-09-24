#!/usr/bin/env python3
"""Burn captions into a video with ffmpeg.

Usage:
    python3 burn_captions.py INPUT.mp4 captions.srt -o out.mp4
    python3 burn_captions.py INPUT.mp4 captions.srt -o out.mp4 --style STYLE --font "Noto Sans"

Build an SRT from word timings first:
    python3 burn_captions.py INPUT.mp4 --words words.json -o out.mp4
    # words.json: [{"start": 0.0, "end": 1.2, "text": "..."}, ...]

Requires ffmpeg on PATH.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

DEFAULT_STYLE = (
    "FontName=Noto Sans,FontSize=28,PrimaryColour=&HFFFFFF&,"
    "OutlineColour=&H99000000&,BorderStyle=1,Outline=2,Shadow=0,"
    "Alignment=2,MarginV=48"
)


def ffmpeg_escape(path: str) -> str:
    return path.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")


def format_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def words_to_srt(words: list[dict], max_chars: int = 84, max_gap: float = 1.5) -> str:
    """Group word timings into readable SRT cues."""
    cues, current, cur_start = [], [], None
    cur_len = 0
    for w in words:
        text = str(w.get("text", "")).strip()
        if not text:
            continue
        start, end = float(w["start"]), float(w["end"])
        if current and (start - current[-1]["end"] > max_gap or cur_len + len(text) + 1 > max_chars):
            cues.append((cur_start, current[-1]["end"], " ".join(x["text"] for x in current)))
            current, cur_start, cur_len = [], None, 0
        if cur_start is None:
            cur_start = start
        current.append({"text": text, "end": end})
        cur_len += len(text) + 1
    if current:
        cues.append((cur_start, current[-1]["end"], " ".join(x["text"] for x in current)))
    blocks = []
    for i, (s, e, t) in enumerate(cues, 1):
        blocks.append(f"{i}\n{format_ts(s)} --> {format_ts(e)}\n{t}\n")
    return "\n".join(blocks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("captions", type=Path, nargs="?")
    parser.add_argument("--words", type=Path, help="word-timing JSON to build an SRT from")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--style", default=DEFAULT_STYLE, help="subtitles force_style string")
    parser.add_argument("--font", default=None, help="override FontName in the style")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"input not found: {args.input}")
        return 2

    srt_path = args.captions
    tmp_srt = None
    if args.words:
        words = json.loads(args.words.read_text(encoding="utf-8"))
        tmp = tempfile.NamedTemporaryFile(
            suffix=".srt", delete=False, dir=str(args.output.parent)
        )
        tmp.write(words_to_srt(words).encode("utf-8"))
        tmp.close()
        tmp_srt = Path(tmp.name)
        srt_path = tmp_srt
    if srt_path is None or not srt_path.is_file():
        print("provide captions.srt or --words words.json")
        return 2

    style = args.style
    if args.font:
        style = style.replace("FontName=Noto Sans", f"FontName={args.font}")

    vf = f"subtitles={ffmpeg_escape(str(srt_path))}:force_style='{style}'"
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", str(args.input),
             "-vf", vf, "-c:a", "copy", str(args.output)],
            check=True,
        )
    finally:
        if tmp_srt is not None:
            tmp_srt.unlink(missing_ok=True)

    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
