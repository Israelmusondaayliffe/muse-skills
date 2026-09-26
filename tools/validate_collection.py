#!/usr/bin/env python3
"""Check discovery metadata, relative Markdown file links, and backtick package paths.

This is a structural check, not evidence of skill quality or host discovery.
Requires Python 3.10+. No dependencies or writes.
"""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote


# Backtick paths that name a file in the user's own project, not a shipped package file.
# Keyed by document; add an entry only after confirming the file is illustrative.
ILLUSTRATIVE_PATHS = {
    "skills/video-production-studio/references/music-video.md": {"assets/bgm.mp3"},  # user-supplied track
}

PACKAGE_PREFIXES = ("references/", "scripts/", "bin/", "assets/", "templates/", "examples/", "schemas/", "../", "./")


def backtick_paths(text):
    """Yield inline-code tokens that name a package file, e.g. `scripts/x.py --help`.

    Only tokens starting with a package folder are checked, so output names such as
    `route.json` are not mistaken for links. Placeholders and globs are skipped.
    """
    for token in re.findall(r"`([^`\n]+)`", text):
        words = token.split()
        if not words:
            continue
        path = words[1] if words[0] in {"python", "python3", "bash", "sh"} and len(words) > 1 else words[0]
        path = path.rstrip(".,;:)")
        if (path.startswith(PACKAGE_PREFIXES) and not any(c in path for c in "<>{}*$|")
                and re.search(r"(\.[A-Za-z0-9]{1,5}|/)$", path)):
            yield path


def check(root):
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    for entry in skills:
        text = entry.read_text()
        front = text.split("---", 2)
        if len(front) != 3 or front[0].strip():
            errors.append(f"{entry.relative_to(root)}: missing frontmatter")
            continue
        name = re.search(r"^name:\s*[\"']?([a-z0-9-]+)[\"']?\s*$", front[1], re.M)
        if not name or name.group(1) != entry.parent.name:
            errors.append(f"{entry.relative_to(root)}: name must match folder in lowercase-hyphen form")
        if not re.search(r"^description:\s*\S", front[1], re.M):
            errors.append(f"{entry.relative_to(root)}: missing description")
    for doc in sorted((root / "skills").rglob("*.md")):
        # Code blocks may contain illustrative Markdown rather than actual links.
        text = re.sub(r"(?ms)^```.*?^```[^\n]*", "", doc.read_text())
        for link in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", text):
            link = unquote(link.strip("<>").split("#", 1)[0])
            if not link or ":" in link or link.startswith(("/", "~")) or any(c in link for c in "<>{}*"):
                continue
            if not (doc.parent / link).exists():
                errors.append(f"{doc.relative_to(root)}: missing link {link}")
        if doc.name.startswith(("NOTICE", "LICENSE")):
            continue  # provenance notes name upstream paths, not package files
        skill = root / "skills" / doc.relative_to(root / "skills").parts[0]
        allowed = ILLUSTRATIVE_PATHS.get(doc.relative_to(root).as_posix(), set())
        for path in backtick_paths(text):
            if path in allowed:
                continue
            if not ((doc.parent / path).exists() or (skill / path).exists()):
                errors.append(f"{doc.relative_to(root)}: missing backtick path {path}")
    return {"skills": len(skills), "errors": errors, "scope": "metadata, Markdown file links, and backtick package paths only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, indent=2))
    return bool(result["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
