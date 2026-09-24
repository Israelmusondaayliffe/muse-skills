#!/usr/bin/env python3
"""Validate the bar for a gauntlet run (SPEC INV-1, section 9.2 step 4).

Reads <run-dir>/bar/bar.md and the bar_refs declared in <run-dir>/pieces.json.

Fails (exit 1) when any of these hold:
- no file, command, source set, or measurement backs the bar
- the bar definition is only adjectives (heuristic: no path, no command,
  no URL, no number in the text)
- the bar references an artifact this run will produce (a bar_ref inside
  an artifact_paths entry)
- bar/rubric.md exists without a recorded hash in run.json or bar/bar.md
- any bar_refs path, or bar/refs path named in bar.md, does not resolve

Prints machine-readable JSON findings on stdout.
Exit codes: 0 bar valid, 1 validation failure, 2 usage error.
"""

import argparse
import json
import os
import re
import sys

URL_RE = re.compile(r"https?://\S+")
NUMBER_RE = re.compile(r"\d")
PATH_RE = re.compile(r"(?<![\w/])(?:[\w.~-]+/)+[\w.~-]+")
EXT_RE = re.compile(
    r"\b[\w-]+\.(?:md|txt|json|py|sh|html|css|js|pdf|csv|png|jpg|jpeg|"
    r"yaml|yml|toml)\b"
)
COMMAND_RE = re.compile(
    r"(?m)(?:^\s*\$\s+\S+|\b(?:python3?|pytest|npm|npx|node|bash|sh|make|"
    r"cargo|go)\s+[\w./-])"
)
HASH_RE = re.compile(r"(?:sha256:\s*[0-9a-fA-F]{8,}|\b[0-9a-f]{64}\b)")
BAR_REFS_TOKEN_RE = re.compile(r"bar/refs/[\w./-]*")


def norm_path(p):
    """Strip fragment, leading ./ and trailing / for comparison."""
    p = str(p).split("#", 1)[0].strip()
    while p.startswith("./"):
        p = p[2:]
    return p.rstrip("/")


def is_url(s):
    return str(s).startswith(("http://", "https://"))


def has_rubric_hash_key(obj):
    """Recursively search a JSON structure for a non-empty rubric hash."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            kl = str(key).lower()
            if "rubric" in kl and "hash" in kl:
                if isinstance(value, str) and value.strip():
                    return True
            if has_rubric_hash_key(value):
                return True
    elif isinstance(obj, list):
        return any(has_rubric_hash_key(item) for item in obj)
    return False


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Fail soft, self-referential, unresolvable, or "
        "unhashed-rubric bars."
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Path to .gauntlet/runs/<run-id>",
    )
    args = parser.parse_args()

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        print(json.dumps({"error": "run dir not found: %s" % run_dir}))
        return 2

    findings = []
    bar_md_path = os.path.join(run_dir, "bar", "bar.md")
    refs_dir = os.path.join(run_dir, "bar", "refs")
    rubric_path = os.path.join(run_dir, "bar", "rubric.md")

    bar_text = ""
    if os.path.isfile(bar_md_path):
        with open(bar_md_path, "r", encoding="utf-8", errors="replace") as fh:
            bar_text = fh.read()
    else:
        findings.append({
            "check": "bar-missing",
            "detail": "bar/bar.md does not exist. There is no bar.",
        })

    # Gather bar_refs and artifact_paths from pieces.json.
    pieces_data = load_json(os.path.join(run_dir, "pieces.json"))
    bar_refs = []
    artifact_paths = []
    if isinstance(pieces_data, dict):
        for piece in pieces_data.get("pieces", []) or []:
            if not isinstance(piece, dict):
                continue
            for ref in piece.get("bar_refs", []) or []:
                if str(ref).strip():
                    bar_refs.append(str(ref).strip())
            for ap in piece.get("artifact_paths", []) or []:
                if str(ap).strip():
                    artifact_paths.append(str(ap).strip())

    refs_dir_files = []
    if os.path.isdir(refs_dir):
        for root, _dirs, files in os.walk(refs_dir):
            for name in files:
                refs_dir_files.append(os.path.join(root, name))

    if bar_text:
        has_url = bool(URL_RE.search(bar_text))
        has_number = bool(NUMBER_RE.search(bar_text))
        has_path = bool(PATH_RE.search(bar_text)) or bool(EXT_RE.search(bar_text))
        has_command = bool(COMMAND_RE.search(bar_text))

        # Adjective-only heuristic: no path, no command, no URL, no number.
        if not (has_url or has_number or has_path or has_command):
            findings.append({
                "check": "bar-adjective-only",
                "detail": "bar/bar.md contains no path, no command, no URL, "
                "and no number. Prose adjectives are not a bar (INV-1).",
            })

        # Backing: a real file, command, source set, or measurement.
        backed = bool(bar_refs) or bool(refs_dir_files) or has_url \
            or has_command or has_number
        if not backed:
            findings.append({
                "check": "bar-unbacked",
                "detail": "No file, command, source set, or measurement "
                "backs the bar: no bar_refs in pieces.json, no files in "
                "bar/refs/, and bar.md names no URL, command, or "
                "measurement.",
            })

    # Self-reference: a bar_ref inside an artifact_paths entry.
    norm_artifacts = [norm_path(ap) for ap in artifact_paths]
    for ref in bar_refs:
        nr = norm_path(ref)
        if not nr:
            continue
        for original, na in zip(artifact_paths, norm_artifacts):
            if nr == na or na.startswith(nr + "/") or nr.startswith(na + "/"):
                findings.append({
                    "check": "bar-self-referential",
                    "detail": "bar_ref %r points at artifact path %r, an "
                    "artifact this run will produce. The bar must be "
                    "external (INV-1)." % (ref, original),
                })
                break

    # Rubric present without a recorded hash.
    if os.path.isfile(rubric_path):
        run_data = load_json(os.path.join(run_dir, "run.json"))
        recorded = has_rubric_hash_key(run_data) if run_data else False
        if not recorded and bar_text:
            recorded = bool(HASH_RE.search(bar_text))
        if not recorded:
            findings.append({
                "check": "rubric-unhashed",
                "detail": "bar/rubric.md exists but no rubric hash is "
                "recorded in run.json or bar/bar.md. Run hash_plan.py to "
                "freeze it.",
            })

    # Resolution: every bar_refs path, and every bar/refs path named in
    # bar.md, must resolve. URLs are not fetched here (no network).
    to_resolve = []
    for ref in bar_refs:
        to_resolve.append(("pieces.json bar_refs", ref))
    for token in BAR_REFS_TOKEN_RE.findall(bar_text):
        cleaned = token.rstrip(".,;:)]}\"'")
        if cleaned:
            to_resolve.append(("bar/bar.md", cleaned))

    seen = set()
    for origin, ref in to_resolve:
        key = norm_path(ref)
        if not key or key in seen:
            continue
        seen.add(key)
        if is_url(ref):
            continue
        candidate = key if os.path.isabs(key) else os.path.join(run_dir, key)
        if not os.path.exists(candidate):
            findings.append({
                "check": "ref-unresolvable",
                "detail": "Reference %r (from %s) does not resolve to a "
                "file or directory under the run dir." % (ref, origin),
            })

    result = {
        "script": "validate_bar",
        "run_dir": run_dir,
        "ok": not findings,
        "findings": findings,
        "counts": {
            "bar_refs": len(bar_refs),
            "artifact_paths": len(artifact_paths),
            "bar_refs_dir_files": len(refs_dir_files),
        },
    }
    print(json.dumps(result, indent=2))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
