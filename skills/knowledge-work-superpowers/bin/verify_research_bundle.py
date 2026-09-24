#!/usr/bin/env python3
"""Validate the structure and traceability of a file-based research bundle.

Bundled with the `knowledge-work-superpowers` workspace skill:
`~/workspace/skills/knowledge-work-superpowers/bin/verify_research_bundle.py`.
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|FILL IN|PLACEHOLDER)\b", re.IGNORECASE)
SOURCE_HEADERS = [
    "Source ID",
    "Title",
    "URL or Location",
    "Source Type",
    "Published or Updated",
    "Accessed",
    "Relevance",
    "Notes",
]
CLAIM_HEADERS = ["Claim ID", "Claim", "Status", "Source IDs", "Confidence", "Notes"]
SOURCE_TYPES = {"primary", "secondary", "discovery"}
CLAIM_STATUSES = {"supported", "inferred", "disputed", "unresolved"}
CONFIDENCE_LEVELS = {"high", "medium", "low"}


@dataclass(frozen=True)
class Finding:
    path: Path
    message: str


def normalize_cell(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).casefold()


def parse_markdown_table(path: Path, expected_headers: list[str]) -> tuple[list[dict[str, str]], list[Finding]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    expected = [normalize_cell(header) for header in expected_headers]
    header_index = None

    for index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        cells = [normalize_cell(cell) for cell in line.strip().strip("|").split("|")]
        if cells == expected:
            header_index = index
            break

    if header_index is None:
        return [], [Finding(path, f"missing table header: {' | '.join(expected_headers)}")]

    rows: list[dict[str, str]] = []
    for line in lines[header_index + 2 :]:
        if not line.lstrip().startswith("|"):
            break
        raw_cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(raw_cells) != len(expected_headers):
            return rows, [Finding(path, f"table row has {len(raw_cells)} cells, expected {len(expected_headers)}")]
        rows.append(dict(zip(expected_headers, raw_cells)))

    if not rows:
        return [], [Finding(path, "table contains no data rows")]
    return rows, []


def check_required_files(bundle: Path, profile: str) -> tuple[dict[str, Path], list[Finding]]:
    names = ["work-brief.md", "research-plan.md", "source-ledger.md", "claim-ledger.md"]
    if profile == "deliverable":
        names.extend(["deliverable.md", "review.md", "delivery-note.md"])

    files: dict[str, Path] = {}
    findings: list[Finding] = []
    for name in names:
        path = bundle / name
        files[name] = path
        if not path.is_file():
            findings.append(Finding(path, "required file is missing"))
            continue
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            findings.append(Finding(path, "required file is empty"))
        if PLACEHOLDER_RE.search(content):
            findings.append(Finding(path, "unresolved placeholder text found"))
    return files, findings


def validate_sources(path: Path) -> tuple[set[str], list[Finding]]:
    rows, findings = parse_markdown_table(path, SOURCE_HEADERS)
    source_ids: set[str] = set()
    for row_number, row in enumerate(rows, start=1):
        source_id = row["Source ID"].strip()
        source_type = row["Source Type"].strip().casefold()
        if not re.fullmatch(r"S\d+", source_id):
            findings.append(Finding(path, f"row {row_number}: invalid source ID '{source_id}'"))
        elif source_id in source_ids:
            findings.append(Finding(path, f"row {row_number}: duplicate source ID '{source_id}'"))
        else:
            source_ids.add(source_id)
        if source_type not in SOURCE_TYPES:
            findings.append(Finding(path, f"row {row_number}: invalid source type '{row['Source Type']}'"))
        if not row["Title"].strip():
            findings.append(Finding(path, f"row {row_number}: title is empty"))
        if not row["URL or Location"].strip():
            findings.append(Finding(path, f"row {row_number}: URL or location is empty"))
    return source_ids, findings


def validate_claims(path: Path, source_ids: set[str]) -> list[Finding]:
    rows, findings = parse_markdown_table(path, CLAIM_HEADERS)
    claim_ids: set[str] = set()

    for row_number, row in enumerate(rows, start=1):
        claim_id = row["Claim ID"].strip()
        status = row["Status"].strip().casefold()
        confidence = row["Confidence"].strip().casefold()
        linked_sources = {
            value.strip()
            for value in re.split(r"[,;]", row["Source IDs"])
            if value.strip() and value.strip().casefold() not in {"none", "n/a"}
        }

        if not re.fullmatch(r"C\d+", claim_id):
            findings.append(Finding(path, f"row {row_number}: invalid claim ID '{claim_id}'"))
        elif claim_id in claim_ids:
            findings.append(Finding(path, f"row {row_number}: duplicate claim ID '{claim_id}'"))
        else:
            claim_ids.add(claim_id)
        if not row["Claim"].strip():
            findings.append(Finding(path, f"row {row_number}: claim is empty"))
        if status not in CLAIM_STATUSES:
            findings.append(Finding(path, f"row {row_number}: invalid claim status '{row['Status']}'"))
        if confidence not in CONFIDENCE_LEVELS:
            findings.append(Finding(path, f"row {row_number}: invalid confidence '{row['Confidence']}'"))
        if status in {"supported", "inferred", "disputed"} and not linked_sources:
            findings.append(Finding(path, f"row {row_number}: status '{status}' requires at least one source ID"))
        for source_id in sorted(linked_sources):
            if source_id not in source_ids:
                findings.append(Finding(path, f"row {row_number}: unknown source ID '{source_id}'"))
    return findings


def validate_bundle(bundle: Path, profile: str) -> list[Finding]:
    if not bundle.is_dir():
        return [Finding(bundle, "bundle directory does not exist")]

    files, findings = check_required_files(bundle, profile)
    source_path = files["source-ledger.md"]
    claim_path = files["claim-ledger.md"]
    if source_path.is_file():
        source_ids, source_findings = validate_sources(source_path)
        findings.extend(source_findings)
    else:
        source_ids = set()
    if claim_path.is_file():
        findings.extend(validate_claims(claim_path, source_ids))
    return findings


def write_valid_fixture(bundle: Path) -> None:
    bundle.mkdir(parents=True, exist_ok=True)
    (bundle / "work-brief.md").write_text("# Work Brief\n\nOutcome: decide.\n", encoding="utf-8")
    (bundle / "research-plan.md").write_text("# Research Plan\n\nCheck the primary source.\n", encoding="utf-8")
    (bundle / "source-ledger.md").write_text(
        "# Source Ledger\n\n"
        "| Source ID | Title | URL or Location | Source Type | Published or Updated | Accessed | Relevance | Notes |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| S1 | Official record | https://example.com/record | primary | "
        "2026-07-01 | 2026-07-09 | Main claim | Current record |\n",
        encoding="utf-8",
    )
    (bundle / "claim-ledger.md").write_text(
        "# Claim Ledger\n\n"
        "| Claim ID | Claim | Status | Source IDs | Confidence | Notes |\n"
        "|---|---|---|---|---|---|\n"
        "| C1 | The official record contains the decision. | supported | S1 | high | Direct support |\n",
        encoding="utf-8",
    )


def run_self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="knowledge-work-superpowers-") as temp_dir:
        root = Path(temp_dir)
        valid = root / "valid"
        write_valid_fixture(valid)
        if validate_bundle(valid, "research"):
            print("SELF-TEST FAIL: valid fixture was rejected")
            return 1

        placeholder = root / "placeholder"
        write_valid_fixture(placeholder)
        (placeholder / "work-brief.md").write_text("# Work Brief\n\nTODO\n", encoding="utf-8")
        if not validate_bundle(placeholder, "research"):
            print("SELF-TEST FAIL: placeholder fixture was accepted")
            return 1

        unsupported = root / "unsupported"
        write_valid_fixture(unsupported)
        claim_path = unsupported / "claim-ledger.md"
        changed = claim_path.read_text(encoding="utf-8").replace("S1 | high", "S99 | high")
        claim_path.write_text(changed, encoding="utf-8")
        if not validate_bundle(unsupported, "research"):
            print("SELF-TEST FAIL: unknown source fixture was accepted")
            return 1

    print("SELF-TEST PASS: valid and invalid fixtures behaved as expected")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", nargs="?", type=Path, help="Directory containing the research bundle")
    parser.add_argument("--profile", choices=("research", "deliverable"), default="research")
    parser.add_argument("--self-test", action="store_true", help="Run built-in valid and invalid fixtures")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.self_test:
        return run_self_test()
    if args.bundle is None:
        print("ERROR: provide a bundle directory or use --self-test", file=sys.stderr)
        return 2

    findings = validate_bundle(args.bundle.expanduser().resolve(), args.profile)
    if findings:
        print(f"FAIL: {len(findings)} finding(s)")
        for finding in findings:
            print(f"- {finding.path}: {finding.message}")
        return 1

    print(f"PASS: research bundle satisfies the {args.profile} profile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
