#!/usr/bin/env python3
"""
dossier_check.py

Deterministic gate between the researcher and planner phases of the
assumption-challenger pipeline.

Validates a research dossier on:
  1. Minimum source count (varies by effort mode)
  2. Source diversity (no single domain dominates)
  3. Recency (for fast-moving subjects, 30%+ sources from last 12 months)
  4. Dimensional coverage (at least 4 dimensions touched, or skipped dimensions
     explicitly justified)
  5. Expert disagreement is mapped (not buried)
  6. Each dimension has at least 2 findings

Exits 0 if the dossier passes. Exits 1 with a structured failure report if not.
The orchestrator should send the failure report back to the researcher.

Usage:
    python dossier_check.py <path-to-dossier.md> --effort {light,standard,deep} \\
        --pace {fast,standard,slow}

Notes on parsing:
    The script expects the dossier to follow assets/research_dossier_template.md.
    It uses regex to locate sections rather than parsing markdown formally,
    which is sufficient given the template is fixed.
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# Effort-mode-specific thresholds.
THRESHOLDS = {
    "light":    {"min_sources": 3,  "min_findings_per_dim": 1, "min_dims_covered": 3},
    "standard": {"min_sources": 8,  "min_findings_per_dim": 2, "min_dims_covered": 4},
    "deep":     {"min_sources": 15, "min_findings_per_dim": 3, "min_dims_covered": 4},
}

# Recency requirements by subject pace.
RECENCY_RULES = {
    "fast":     {"months_window": 12, "min_recent_pct": 0.30},
    "standard": {"months_window": 36, "min_recent_pct": 0.20},
    "slow":     {"months_window": 60, "min_recent_pct": 0.10},
}

# Source diversity: no single domain may exceed this fraction of total sources.
MAX_DOMAIN_SHARE = 0.50


def read_dossier(path: Path) -> str:
    if not path.exists():
        sys.exit(f"FAIL: dossier file not found at {path}")
    return path.read_text(encoding="utf-8")


def extract_sources(dossier: str) -> list[dict]:
    """
    Extract source rows from the source list table in the dossier.

    The template has a markdown table with columns:
    | ID | Source | Tier | Date Published | Date Accessed | Notes |
    """
    sources = []

    # Find the source list section.
    match = re.search(
        r"##\s*Source List(.*?)(?:\n##\s|\Z)",
        dossier,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return sources

    table_block = match.group(1)

    # Parse table rows. Skip header and separator rows.
    for line in table_block.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        # Skip header row (contains "Source") and separator (contains "---").
        if len(cells) < 4:
            continue
        if cells[0].lower() == "id" or all(re.match(r"^-+$", c) for c in cells if c):
            continue
        # Skip placeholder rows from unfilled templates.
        if "[Title]" in cells[1] or cells[1] == "":
            continue

        sources.append({
            "id": cells[0],
            "source": cells[1],
            "tier": cells[2] if len(cells) > 2 else "",
            "date_published": cells[3] if len(cells) > 3 else "",
            "date_accessed": cells[4] if len(cells) > 4 else "",
            "notes": cells[5] if len(cells) > 5 else "",
        })

    return sources


def parse_date(date_str: str) -> Optional[datetime]:
    """Try a few common date formats. Return None if unparseable."""
    date_str = date_str.strip()
    if not date_str or date_str.lower() in {"n/a", "unknown", "[date]"}:
        return None

    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y", "%B %Y", "%b %Y", "%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def extract_dimensions_covered(dossier: str) -> tuple[list[str], list[str]]:
    """Pull the 'Dimensions Covered' and 'Skipped' lists."""
    covered, skipped = [], []
    match = re.search(
        r"##\s*Dimensions Covered(.*?)(?:\n##\s|\Z)",
        dossier,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return covered, skipped

    block = match.group(1)
    # Split into "Covered" and "Skipped" sub-blocks.
    covered_match = re.search(
        r"\*\*Covered:\*\*(.*?)(?:\*\*Skipped:|\Z)",
        block,
        flags=re.DOTALL,
    )
    skipped_match = re.search(r"\*\*Skipped:\*\*(.*)", block, flags=re.DOTALL)

    if covered_match:
        for line in covered_match.group(1).splitlines():
            line = line.strip("- *").strip()
            # Filter out template placeholders and empty lines.
            if line and not line.startswith("[") and line not in {"Technical", "Market", "User / audience", "Regulatory"} or (line and not line.startswith("[")):
                # Keep real entries (allow the template defaults if present).
                if line:
                    covered.append(line)
        # Cleaner pass: keep only non-bracket entries.
        covered = [c for c in covered if c and not c.startswith("[") and c.lower() != "[add as needed]"]

    if skipped_match:
        for line in skipped_match.group(1).splitlines():
            line = line.strip("- *").strip()
            if line and not line.startswith("[") and ":" in line:
                skipped.append(line)

    return covered, skipped


def extract_findings_per_dimension(dossier: str) -> dict[str, int]:
    """Count findings under each Dimension N section."""
    counts = {}
    # Match "### Dimension N: Name" headings, then count "#### Finding" within.
    dim_pattern = re.compile(
        r"###\s*Dimension\s+\d+:\s*(.+?)\n(.*?)(?=\n###\s*Dimension\s+\d+:|\n##\s|\Z)",
        flags=re.DOTALL | re.IGNORECASE,
    )
    for m in dim_pattern.finditer(dossier):
        dim_name = m.group(1).strip()
        body = m.group(2)
        # Skip template placeholder dimensions.
        if dim_name.startswith("[") or "[Name]" in dim_name:
            continue
        finding_count = len(re.findall(r"^####\s*Finding", body, flags=re.MULTILINE))
        counts[dim_name] = finding_count
    return counts


def has_disagreement_map(dossier: str) -> bool:
    """Check that the disagreement section has at least one real entry."""
    match = re.search(
        r"##\s*Expert Disagreement Map(.*?)(?:\n##\s|\Z)",
        dossier,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return False
    body = match.group(1)
    # At least one ### Disagreement entry that isn't a placeholder.
    entries = re.findall(r"###\s*Disagreement\s*[A-Z]:\s*(.+)", body)
    real_entries = [e for e in entries if not e.strip().startswith("[")]
    return len(real_entries) >= 1


def domain_from_source(source: str) -> str:
    """
    Extract a rough domain identifier from a source entry. Used for
    diversity check.

    Strategy:
      - If the source is a URL, return the domain (host).
      - Otherwise, take the first significant word. This collapses
        sources like "Maven blog post" and "Maven case study" to "maven",
        catching the common case where one outlet dominates the dossier.
    """
    src = source.lower().strip()
    if not src:
        return "unknown"

    # URL case.
    url_match = re.search(r"https?://([^/\s,)]+)", src)
    if url_match:
        host = url_match.group(1)
        host = re.sub(r"^www\.", "", host)
        return host

    # Strip everything after first comma or open paren (often a date or note).
    src = re.split(r"[,(]", src)[0].strip()

    # Take the first significant word to identify outlet.
    stopwords = {
        "the", "a", "an", "of", "and", "or", "for", "in", "on", "at",
        "report", "analysis", "study", "page", "post", "article", "blog",
        "newsletter", "podcast", "doc", "docs", "documentation",
        "case", "white", "paper", "research", "data",
    }
    words = [w for w in re.findall(r"[a-z0-9]+", src) if w not in stopwords]
    if not words:
        return src or "unknown"
    return words[0]


def check_dossier(dossier_path: Path, effort: str, pace: str) -> dict:
    """
    Run all checks. Return a structured result dict with pass/fail flags
    and human-readable failure reasons.
    """
    dossier = read_dossier(dossier_path)
    thresh = THRESHOLDS[effort]
    recency = RECENCY_RULES[pace]

    failures = []

    # Check 1: Source count.
    sources = extract_sources(dossier)
    if len(sources) < thresh["min_sources"]:
        failures.append(
            f"Source count: found {len(sources)} sources, "
            f"need at least {thresh['min_sources']} for {effort} mode."
        )

    # Check 2: Source diversity.
    if sources:
        domains = [domain_from_source(s["source"]) for s in sources]
        domain_counts = Counter(domains)
        top_domain, top_count = domain_counts.most_common(1)[0]
        share = top_count / len(sources)
        if share > MAX_DOMAIN_SHARE:
            failures.append(
                f"Source diversity: {top_count}/{len(sources)} sources "
                f"({share:.0%}) come from '{top_domain}'. "
                f"Limit is {MAX_DOMAIN_SHARE:.0%}. Add sources from other domains."
            )

    # Check 3: Recency.
    if sources:
        cutoff = datetime.now() - timedelta(days=30 * recency["months_window"])
        parsed_dates = [parse_date(s["date_published"]) for s in sources]
        valid_dates = [d for d in parsed_dates if d is not None]
        if valid_dates:
            recent = [d for d in valid_dates if d >= cutoff]
            recent_pct = len(recent) / len(valid_dates)
            if recent_pct < recency["min_recent_pct"]:
                failures.append(
                    f"Recency: only {recent_pct:.0%} of dated sources are within "
                    f"the last {recency['months_window']} months. "
                    f"Need at least {recency['min_recent_pct']:.0%} for {pace}-paced subjects."
                )
        else:
            failures.append(
                "Recency: no source has a parseable Date Published. "
                "Add publication dates so recency can be evaluated."
            )

    # Check 4: Dimensional coverage.
    covered, skipped = extract_dimensions_covered(dossier)
    if len(covered) < thresh["min_dims_covered"]:
        failures.append(
            f"Dimensional coverage: only {len(covered)} dimensions covered, "
            f"need at least {thresh['min_dims_covered']} for {effort} mode. "
            f"Either research more dimensions or justify skipped ones explicitly."
        )

    # Check 5: Expert disagreement is mapped.
    if not has_disagreement_map(dossier):
        failures.append(
            "Expert disagreement: no real entries in the Expert Disagreement Map. "
            "If the subject genuinely has consensus, state so explicitly. Otherwise, "
            "search for the contrarian position and add at least one disagreement."
        )

    # Check 6: Findings per dimension.
    findings_by_dim = extract_findings_per_dimension(dossier)
    thin_dims = [
        (dim, count) for dim, count in findings_by_dim.items()
        if count < thresh["min_findings_per_dim"]
    ]
    if thin_dims:
        details = "; ".join(f"'{d}' has {c}" for d, c in thin_dims)
        failures.append(
            f"Findings per dimension: need at least {thresh['min_findings_per_dim']} "
            f"finding(s) per covered dimension for {effort} mode. Thin: {details}."
        )

    return {
        "passed": len(failures) == 0,
        "effort": effort,
        "pace": pace,
        "stats": {
            "source_count": len(sources),
            "dimensions_covered": len(covered),
            "dimensions_skipped": len(skipped),
            "findings_by_dimension": findings_by_dim,
            "has_disagreement_map": has_disagreement_map(dossier),
        },
        "failures": failures,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dossier", type=Path, help="Path to dossier markdown file.")
    parser.add_argument(
        "--effort", choices=["light", "standard", "deep"], default="standard",
        help="Effort mode (controls thresholds). Default: standard.",
    )
    parser.add_argument(
        "--pace", choices=["fast", "standard", "slow"], default="standard",
        help="Subject pace (controls recency rules). Default: standard.",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output result as JSON. Default: human-readable.",
    )
    args = parser.parse_args()

    result = check_dossier(args.dossier, args.effort, args.pace)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        if result["passed"]:
            print(f"PASS: dossier passes all checks for {args.effort} mode "
                  f"({args.pace}-paced subject).")
            print(f"  Sources: {result['stats']['source_count']}")
            print(f"  Dimensions covered: {result['stats']['dimensions_covered']}")
            print(f"  Disagreement mapped: {result['stats']['has_disagreement_map']}")
        else:
            print(f"FAIL: dossier does not pass {args.effort} mode checks.")
            print(f"Pace: {args.pace}-paced subject.")
            print()
            print("Failures:")
            for i, fail in enumerate(result["failures"], 1):
                print(f"  {i}. {fail}")
            print()
            print("Stats:")
            print(f"  Source count: {result['stats']['source_count']}")
            print(f"  Dimensions covered: {result['stats']['dimensions_covered']}")
            print(f"  Findings by dim: {result['stats']['findings_by_dimension']}")
            print(f"  Disagreement mapped: {result['stats']['has_disagreement_map']}")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
