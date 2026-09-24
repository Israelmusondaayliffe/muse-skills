#!/usr/bin/env python3
"""Validate generic or Seedance 2.5 video prompt deliverables."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


MODES = (
    "auto",
    "text-to-video",
    "continuous-one-take",
    "beat-cut-music-video",
    "omni-reference",
    "first-last-frame",
    "extension",
    "visual-edit",
    "audio-edit",
    "ultra-long",
    "storyboard",
    "blockout",
    "green-screen",
    "clip-join",
)


def code_blocks(text: str) -> list[str]:
    return re.findall(r"```[\w-]*\n(.*?)\n```", text, flags=re.S)


def infer_mode(text: str) -> str:
    lowered = text.lower()
    checks = (
        ("continuous-one-take", ("continuous unbroken take", "single continuous", "one-take")),
        ("beat-cut-music-video", ("hard cuts", "no soft crossfades", "music video")),
        ("first-last-frame", ("start from @image", "end exactly at @image", "first and last frame")),
        ("extension", ("extend @video", "generate only the new segment", "existing frames")),
        ("audio-edit", ("change only", "background music", "audio edit")),
        ("visual-edit", ("edit @video", "target:", "unchanged")),
        ("ultra-long", ("ultra-long", "ultra long", "full video: 180")),
        ("storyboard", ("storyboard", "each panel is one full shot")),
        ("blockout", ("clayrender", "clay render", "blockout", "white model")),
        ("green-screen", ("green screen", "chroma green")),
        ("clip-join", ("connect @video", "connective tissue")),
        ("omni-reference", ("omni reference", "@audio", "@video", "@image")),
    )
    for mode, needles in checks:
        if any(needle in lowered for needle in needles):
            return mode
    return "text-to-video"


def parse_timestamp(value: str) -> float:
    if ":" in value:
        minutes, seconds = value.split(":", maxsplit=1)
        return (int(minutes) * 60) + float(seconds)
    return float(value)


def timeline_intervals(prompt: str) -> list[tuple[float, float]]:
    timestamp = r"\d{1,3}(?::\d{2}(?:\.\d{1,3})?|\.\d{1,3})?"
    pattern = re.compile(
        rf"\[\s*({timestamp})\s*[-–]\s*({timestamp})(?:\s*\|[^\]]*)?\s*\]",
        re.I,
    )
    return [(parse_timestamp(start), parse_timestamp(end)) for start, end in pattern.findall(prompt)]


def declared_duration(prompt: str) -> float | None:
    patterns = (
        r"(?:full video|duration)\s*:\s*(?:exactly\s*)?(\d{1,3}(?:\.\d+)?)\s*(?:seconds?|s)\b",
        r"\b(?:create|generate|make|produce)\b.{0,40}\b(\d{1,3}(?:\.\d+)?)[ -]second\b",
    )
    for pattern in patterns:
        match = re.search(pattern, prompt, flags=re.I)
        if match:
            return float(match.group(1))
    return None


def check_timeline(prompt: str, errors: list[str]) -> None:
    intervals = timeline_intervals(prompt)
    duration = declared_duration(prompt)
    if duration is None:
        errors.append("Seedance timed mode must declare duration")
        return
    if not intervals:
        errors.append("Seedance timed mode has no bracketed timeline")
        return
    if abs(intervals[0][0]) > 0.001:
        errors.append("timeline must begin at 0")
    if abs(intervals[-1][1] - duration) > 0.001:
        errors.append(f"timeline must end at declared duration {duration:g}")
    for previous, current in zip(intervals, intervals[1:]):
        if abs(previous[1] - current[0]) > 0.001:
            errors.append("timeline has a gap or overlap")
            break
    if any(start >= end for start, end in intervals):
        errors.append("timeline contains a non-positive interval")
    end_states = len(re.findall(r"\bend state\s*:", prompt, flags=re.I))
    if end_states < len(intervals):
        errors.append("every timed beat must name an end state")


def check_references(prompt: str, errors: list[str]) -> None:
    tags = {
        match.group(0).replace(" ", "").lower()
        for match in re.finditer(r"@(image|video|audio|clayrender)\s*\d+", prompt, flags=re.I)
    }
    for tag in sorted(tags):
        lines = [line for line in prompt.splitlines() if tag in line.replace(" ", "").lower()]
        has_positive = any(re.search(r"\b(defines?|controls?|is only|supplies?)\b", line, re.I) for line in lines)
        has_negative = any(re.search(r"\b(do not|must not|ignore|not use|only)\b", line, re.I) for line in lines)
        if not has_positive or not has_negative:
            errors.append(f"{tag} needs positive and negative scope")


def validate_generic(text: str) -> list[str]:
    errors: list[str] = []
    if not code_blocks(text):
        errors.append("no video prompt code blocks found")
    if "\u2014" in text:
        errors.append("contains em dash")
    if re.search(r"\b(stunning|breathtaking|game-changing)\b", text, flags=re.I):
        errors.append("contains hype language")
    return errors


def validate_seedance(text: str, selected_mode: str) -> tuple[list[str], str]:
    errors = validate_generic(text)
    blocks = code_blocks(text)
    mode = infer_mode(text) if selected_mode == "auto" else selected_mode
    if len(blocks) != 1:
        errors.append("Seedance deliverable must contain exactly one prompt code block")
        return errors, mode
    prompt = blocks[0]
    if re.search(r"\bSeedance\s+2\.0\b", text, flags=re.I):
        errors.append("contains stale Seedance 2.0 guidance")
    if re.search(r"\bSora(?:\s+\d+(?:\.\d+)?)?\b", prompt, flags=re.I):
        errors.append("Seedance prompt contains Sora model direction")

    timed_modes = {
        "text-to-video",
        "continuous-one-take",
        "beat-cut-music-video",
        "omni-reference",
        "ultra-long",
        "storyboard",
    }
    if mode in timed_modes:
        check_timeline(prompt, errors)

    if "@" in prompt:
        check_references(prompt, errors)

    if mode == "continuous-one-take":
        if not re.search(r"\b(continuous|uninterrupted|unbroken)\b", prompt, flags=re.I):
            errors.append("one-take prompt needs continuous movement")
        if not re.search(r"\b(no cuts?|without cuts?|one uninterrupted)\b", prompt, flags=re.I):
            errors.append("one-take prompt must prohibit cuts")
        if not re.search(
            r"\b(follows?|arcs?|glides?|drifts?|tracks?|move(?:s|ment)? through|handoff)\b",
            prompt,
            flags=re.I,
        ):
            errors.append("one-take prompt needs an explicit spatial handoff")
        if re.search(r"(?<!no )hard cut(?:s)?\s+(?:to|at|on)", prompt, flags=re.I):
            errors.append("one-take prompt contains a positive hard-cut instruction")

    if mode == "beat-cut-music-video":
        if "hard cut" not in prompt.lower():
            errors.append("beat-cut prompt must direct hard cuts")
        if not re.search(r"\b(on|exactly on|lands? on)\b.{0,30}\bbeat\b", prompt, flags=re.I):
            errors.append("beat-cut prompt must bind cuts or action to beats")
        if "no soft crossfades" not in prompt.lower():
            errors.append("beat-cut prompt must reject soft crossfades")

    if mode == "extension":
        for pattern, label in (
            (r"\b(new segment|new footage)\b", "new segment only"),
            (r"\b(preserve|unchanged|existing frames|prior frames)\b", "prior-frame preservation"),
            (r"\b(continuity|no hard cuts|nothing appears)\b", "continuity clause"),
        ):
            if not re.search(pattern, prompt, flags=re.I):
                errors.append(f"extension prompt missing {label}")

    if mode in {"visual-edit", "audio-edit"}:
        for pattern, label in (
            (r"\b(target|change only|edit)\b", "target"),
            (r"\b(change|replace|remove|adjust)\b", "change"),
            (r"\b(seconds?|timing|during|from)\b", "timing"),
            (r"\b(keep|preserve|unchanged|except)\b", "unchanged elements"),
        ):
            if not re.search(pattern, prompt, flags=re.I):
                errors.append(f"edit prompt missing {label}")

    if mode == "first-last-frame":
        if not re.search(r"\b(start|opening)\b", prompt, flags=re.I):
            errors.append("first-last prompt missing opening state")
        if not re.search(r"\b(end|closing)\b", prompt, flags=re.I):
            errors.append("first-last prompt missing closing state")
        if "midpoint" not in prompt.lower():
            errors.append("first-last prompt missing midpoint")

    if not re.search(r"\b(audio|sound|ambience|music|dialogue|foley)\b", prompt, flags=re.I):
        errors.append("Seedance prompt needs explicit audio direction")
    if not re.search(r"\b(forbidden|no |do not|must not)\b", prompt, flags=re.I):
        errors.append("Seedance prompt needs explicit forbidden elements")
    return errors, mode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Prompt deliverable to validate")
    parser.add_argument("--profile", choices=("generic", "seedance-2.5"), default="generic")
    parser.add_argument("--mode", choices=MODES, default="auto")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = pathlib.Path(args.file).expanduser()
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"FAIL {path}: {exc}", file=sys.stderr)
        return 2

    if args.profile == "seedance-2.5":
        errors, mode = validate_seedance(text, args.mode)
    else:
        errors = validate_generic(text)
        mode = "generic"

    if errors:
        print(f"FAIL {path} [{args.profile}/{mode}]: " + "; ".join(errors))
        return 1
    print(f"PASS {path} [{args.profile}/{mode}]: {len(code_blocks(text))} prompt block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
