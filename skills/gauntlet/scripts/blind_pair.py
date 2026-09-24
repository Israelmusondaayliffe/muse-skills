#!/usr/bin/env python3
"""Set up a blind comparison pair for one round. SPEC sections 5.1 and 11.2.

Seeds an RNG with a recorded seed, randomly assigns A and B labels to our
artifact and the reference, copies both to neutral paths under
rounds/<piece>/<nnn>/blind/, strips obvious metadata lines from text files,
and writes the label map to the sealed directory outside runs/:
<run-dir>/../../sealed/<run-id>/<piece>/<nnn>/map.json.

Stdout carries the neutral paths only. The mapping, the seed, and the source
paths never appear on stdout. Critic subagents receive paths inside runs/
only, so the sealed map is structurally out of their reach.

Exit codes: 0 success, 1 validation failure, 2 usage error.
"""

import argparse
import json
import os
import random
import re
import sys

METADATA_KEY = re.compile(
    r"^\s*(author|by|date|created|updated|modified|source|origin|file|"
    r"filename|path|title|version|draft|generated(-by)?|model|agent|"
    r"session|run|run[-_]id|piece|round)\s*[:=]",
    re.IGNORECASE)


def die(message):
    print(json.dumps({"error": message}))
    sys.exit(1)


def atomic_write_bytes(path, payload):
    tmp = path + ".tmp"
    with open(tmp, "wb") as handle:
        handle.write(payload)
    os.replace(tmp, path)


def strip_metadata(raw):
    """Strip obvious provenance from text content. Binary passes through.

    Removes a leading YAML frontmatter block, then leading blank lines,
    leading metadata-key lines (author, date, source, path, and similar),
    and leading single-line HTML comments. Body content is untouched.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                lines = lines[i + 1:]
                break
    while lines:
        stripped = lines[0].strip()
        is_comment = stripped.startswith("<!--") and stripped.endswith("-->")
        if stripped == "" or is_comment or METADATA_KEY.match(stripped):
            lines.pop(0)
            continue
        break
    cleaned = "\n".join(lines)
    if cleaned and not cleaned.endswith("\n"):
        cleaned += "\n"
    return cleaned.encode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Blind-pair our artifact and the reference under neutral "
                    "labels. Prints neutral paths only, never the mapping.")
    parser.add_argument("--run-dir", required=True,
                        help="Path to .gauntlet/runs/<run-id>")
    parser.add_argument("--piece", required=True, help="Piece id")
    parser.add_argument("--round", required=True, type=int,
                        help="Round number, 1-based")
    parser.add_argument("--ours", required=True,
                        help="Path to our artifact or its inspection output")
    parser.add_argument("--reference", required=True,
                        help="Path to the reference artifact or its "
                             "inspection output")
    parser.add_argument("--seed", type=int, default=None,
                        help="RNG seed. Recorded in the sealed map either "
                             "way. Pass one for deterministic assignment")
    args = parser.parse_args()

    if args.round < 1:
        parser.error("--round must be 1 or greater")

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        die("run directory not found: {0}".format(run_dir))
    ours = os.path.abspath(args.ours)
    reference = os.path.abspath(args.reference)
    if not os.path.isfile(ours):
        die("ours artifact not found: {0}".format(ours))
    if not os.path.isfile(reference):
        die("reference artifact not found: {0}".format(reference))

    run_id = os.path.basename(os.path.normpath(run_dir))
    round_label = "{0:03d}".format(args.round)

    seed = args.seed
    if seed is None:
        seed = int.from_bytes(os.urandom(8), "big")
    rng = random.Random(seed)
    ours_label = "A" if rng.random() < 0.5 else "B"

    source_for = {
        "A": ours if ours_label == "A" else reference,
        "B": reference if ours_label == "A" else ours,
    }

    blind_dir = os.path.join(run_dir, "rounds", args.piece, round_label, "blind")
    os.makedirs(blind_dir, exist_ok=True)

    neutral_paths = {}
    for label in ("A", "B"):
        source = source_for[label]
        ext = os.path.splitext(source)[1]
        neutral = os.path.join(blind_dir, "item-{0}{1}".format(label.lower(), ext))
        with open(source, "rb") as handle:
            raw = handle.read()
        atomic_write_bytes(neutral, strip_metadata(raw))
        neutral_paths[label] = neutral

    if os.path.basename(os.path.dirname(os.path.abspath(run_dir))) != "runs":
        die("--run-dir must be a .gauntlet/runs/<run-id> directory; got {0!r}. "
            "Refusing so the sealed map cannot land inside runs/.".format(run_dir))
    sealed_dir = os.path.normpath(os.path.join(
        run_dir, "..", "..", "sealed", run_id, args.piece, round_label))
    os.makedirs(sealed_dir, exist_ok=True)
    map_payload = {
        "seed": seed,
        "a": source_for["A"],
        "b": source_for["B"],
        "ours_label": ours_label,
    }
    map_bytes = (json.dumps(map_payload, indent=2) + "\n").encode("utf-8")
    atomic_write_bytes(os.path.join(sealed_dir, "map.json"), map_bytes)

    # Neutral paths only. Never the mapping.
    print(json.dumps({
        "item_a": neutral_paths["A"],
        "item_b": neutral_paths["B"],
    }, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
