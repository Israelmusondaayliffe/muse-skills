#!/usr/bin/env python3
"""Run bounded local recall or build a source-bound evidence digest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


DEFAULT_MAX_FILES = 5000
DEFAULT_MAX_MATCHES = 50
DEFAULT_MAX_EXCERPTS = 5
MAX_FILE_BYTES = 1_000_000
MAX_LINE_CHARS = 500
EXCLUDED_DIRECTORIES = {
    ".git",
    ".hg",
    ".pytest_cache",
    ".svn",
    ".venv",
    "__pycache__",
    "node_modules",
    "venv",
}


class FallbackError(RuntimeError):
    """A bounded fallback request is invalid or outside authority."""


def is_within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def shorten_line(line: str) -> tuple[str, bool]:
    stripped = line.strip()
    if len(stripped) <= MAX_LINE_CHARS:
        return stripped, False
    return stripped[:MAX_LINE_CHARS], True


def normalize_roots(values: list[str], authority: str) -> tuple[list[Path], list[dict[str, object]]]:
    if not authority.strip():
        raise FallbackError("an authority statement from the current task is required")
    if not values:
        raise FallbackError("at least one exact user-authorized workspace root is required")
    broad_roots = {Path("/").resolve(), Path.home().resolve()}
    roots: list[Path] = []
    checks: list[dict[str, object]] = []
    for value in values:
        supplied = Path(value).expanduser()
        if not supplied.is_absolute():
            raise FallbackError(f"authorized root must be absolute: {value}")
        if supplied.is_symlink():
            raise FallbackError(f"authorized root cannot be a symlink: {supplied}")
        try:
            resolved = supplied.resolve(strict=True)
        except OSError as exc:
            raise FallbackError(f"authorized root is unavailable: {supplied}: {exc}") from exc
        if not resolved.is_dir():
            raise FallbackError(f"authorized root is not a directory: {resolved}")
        if resolved in broad_roots or is_within(Path.home().resolve(), resolved):
            raise FallbackError(f"refusing broad root: {resolved}")
        if resolved in roots:
            continue
        roots.append(resolved)
        checks.append(
            {
                "root": str(resolved),
                "supplied_explicitly": True,
                "exists": True,
                "is_directory": True,
                "is_symlink": False,
                "broad_root": False,
                "authority_statement": authority.strip(),
            }
        )
    return roots, checks


def iter_bounded_files(roots: list[Path]):
    for root in roots:
        for directory, names, files in os.walk(root, followlinks=False):
            names[:] = sorted(
                name
                for name in names
                if name not in EXCLUDED_DIRECTORIES and not (Path(directory) / name).is_symlink()
            )
            for name in sorted(files):
                path = Path(directory) / name
                if path.is_symlink() or not path.is_file():
                    continue
                yield path


def read_text_file(path: Path) -> tuple[str | None, str | None]:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None, "too-large"
        return path.read_text(encoding="utf-8"), None
    except UnicodeDecodeError:
        return None, "non-utf8"
    except OSError:
        return None, "unreadable"


def search(args: argparse.Namespace) -> dict[str, object]:
    query = args.query.strip()
    if not query:
        raise FallbackError("query must be non-empty")
    roots, checks = normalize_roots(args.root, args.authority)
    matches: list[dict[str, object]] = []
    files_considered = 0
    file_limit_reached = False
    skipped = {"too-large": 0, "non-utf8": 0, "unreadable": 0}
    query_folded = query.casefold()
    for path in iter_bounded_files(roots):
        if files_considered >= args.max_files:
            file_limit_reached = True
            break
        files_considered += 1
        text, reason = read_text_file(path)
        if reason:
            skipped[reason] += 1
            continue
        assert text is not None
        for line_number, line in enumerate(text.splitlines(), 1):
            if query_folded not in line.casefold():
                continue
            excerpt, excerpt_truncated = shorten_line(line)
            matches.append(
                {
                    "path": str(path),
                    "line": line_number,
                    "text": excerpt,
                    "text_truncated": excerpt_truncated,
                }
            )
            if len(matches) >= args.max_matches:
                break
        if len(matches) >= args.max_matches:
            break
    match_limit_reached = len(matches) >= args.max_matches
    skipped_content = any(skipped.values())
    search_complete = not (file_limit_reached or match_limit_reached or skipped_content)
    if not search_complete:
        evidence_status = "search-incomplete"
    elif matches:
        evidence_status = "matches-found"
    else:
        evidence_status = "no-evidence"
    return {
        "schema_version": 1,
        "mode": "search",
        "query": query,
        "roots_searched": [str(root) for root in roots],
        "authority_checks": checks,
        "matches": matches,
        "evidence_status": evidence_status,
        "limits": {
            "max_files": args.max_files,
            "max_matches": args.max_matches,
            "max_file_bytes": MAX_FILE_BYTES,
        },
        "files_considered": files_considered,
        "skipped_files": skipped,
        "file_limit_reached": file_limit_reached,
        "match_limit_reached": match_limit_reached,
        "search_complete": search_complete,
        "write_performed": False,
        "destructive_action_authorized": False,
    }


def digest(args: argparse.Namespace) -> dict[str, object]:
    audience = args.audience.strip()
    if not audience:
        raise FallbackError("audience must be non-empty")
    roots, checks = normalize_roots(args.root, args.authority)
    if not args.source:
        raise FallbackError("at least one source file is required")
    entries: list[dict[str, object]] = []
    source_checks: list[dict[str, object]] = []
    seen: set[Path] = set()
    for value in args.source:
        supplied = Path(value).expanduser()
        if not supplied.is_absolute():
            raise FallbackError(f"source must be absolute: {value}")
        if supplied.is_symlink():
            raise FallbackError(f"source cannot be a symlink: {supplied}")
        try:
            path = supplied.resolve(strict=True)
        except OSError as exc:
            raise FallbackError(f"source is unavailable: {supplied}: {exc}") from exc
        owner = next((root for root in roots if is_within(path, root)), None)
        if owner is None:
            raise FallbackError(f"source is outside authorized roots: {path}")
        if not path.is_file():
            raise FallbackError(f"source is not a file: {path}")
        if path in seen:
            continue
        seen.add(path)
        text, reason = read_text_file(path)
        if reason:
            raise FallbackError(f"source is not usable text within bounds: {path}: {reason}")
        assert text is not None
        excerpts = []
        for line_number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            excerpt, excerpt_truncated = shorten_line(line)
            excerpts.append(
                {
                    "line": line_number,
                    "text": excerpt,
                    "text_truncated": excerpt_truncated,
                }
            )
            if len(excerpts) >= args.max_excerpts:
                break
        entries.append(
            {
                "path": str(path),
                "authorized_root": str(owner),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "size": path.stat().st_size,
                "excerpts": excerpts,
            }
        )
        source_checks.append(
            {
                "source": str(path),
                "inside_authorized_root": True,
                "is_symlink": False,
                "is_file": True,
            }
        )
    has_evidence = any(entry["excerpts"] for entry in entries)
    return {
        "schema_version": 1,
        "mode": "digest",
        "audience": audience,
        "roots_searched": [str(root) for root in roots],
        "authority_checks": checks,
        "source_scope_checks": source_checks,
        "digest_entries": entries,
        "evidence_status": "evidence-found" if has_evidence else "no-evidence",
        "limits": {
            "max_excerpts_per_source": args.max_excerpts,
            "max_file_bytes": MAX_FILE_BYTES,
        },
        "writing_companion_used": False,
        "write_performed": False,
        "destructive_action_authorized": False,
    }


def bounded_int(value: str, label: str, maximum: int) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"{label} must be an integer") from exc
    if not 1 <= parsed <= maximum:
        raise argparse.ArgumentTypeError(f"{label} must be from 1 to {maximum}")
    return parsed


def add_authority_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", action="append", required=True, help="Exact user-authorized workspace root")
    parser.add_argument("--authority", required=True, help="Authority statement from the current task")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search authorized local roots for a literal query")
    add_authority_arguments(search_parser)
    search_parser.add_argument("--query", required=True)
    search_parser.add_argument(
        "--max-files",
        type=lambda value: bounded_int(value, "max-files", 20_000),
        default=DEFAULT_MAX_FILES,
    )
    search_parser.add_argument(
        "--max-matches",
        type=lambda value: bounded_int(value, "max-matches", 200),
        default=DEFAULT_MAX_MATCHES,
    )
    search_parser.set_defaults(handler=search)

    digest_parser = subparsers.add_parser("digest", help="Create a direct digest from exact local evidence")
    add_authority_arguments(digest_parser)
    digest_parser.add_argument("--source", action="append", required=True, help="Exact source file inside an authorized root")
    digest_parser.add_argument("--audience", required=True)
    digest_parser.add_argument(
        "--max-excerpts",
        type=lambda value: bounded_int(value, "max-excerpts", 20),
        default=DEFAULT_MAX_EXCERPTS,
    )
    digest_parser.set_defaults(handler=digest)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = args.handler(args)
    except FallbackError as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
