#!/usr/bin/env python3
"""Audit the claim ledger for one piece (SPEC 5.3, 8.8).

Reads <run-dir>/claims/<piece>/ledger.json (a JSON array of rows, or an
object with a "rows" or "claims" array). Validates the support_type closed
set (primary, secondary, user-supplied, own-analysis, unsupported) and
computes: total claims, unsupported count, claim-to-citation ratio, per-row
source reachability (file existence for paths, HTTP HEAD/GET for URLs
unless --skip-network), duplicate-source concentration, and
quote-presence-in-source for readable text file sources.

Writes <run-dir>/claims/<piece>/audit.json and prints the same JSON.
Any unsupported row is an integrity failure, not a style note.
Exit codes: 0 clean, 1 unsupported or invalid rows (or missing ledger),
2 usage error.
"""

import argparse
import datetime
import json
import os
import sys

SUPPORT_TYPES = {
    "primary", "secondary", "user-supplied", "own-analysis", "unsupported",
}


def is_url(s):
    return str(s).startswith(("http://", "https://"))


def strip_fragment(path):
    return str(path).split("#", 1)[0].strip()


def normalize_text(s):
    return " ".join(str(s).split()).casefold()


def check_url(url):
    """HEAD first, GET fallback. Returns reachable or unreachable."""
    import urllib.error
    import urllib.request
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(
                url, method=method,
                headers={"User-Agent": "gauntlet-claim-audit/0.1"},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                if 200 <= resp.status < 400:
                    return "reachable"
        except urllib.error.HTTPError:
            if method == "GET":
                return "unreachable"
        except Exception:
            if method == "GET":
                return "unreachable"
    return "unreachable"


def main():
    parser = argparse.ArgumentParser(
        description="Ledger validation, source reachability, citation "
        "ratio, quote presence."
    )
    parser.add_argument(
        "--run-dir", required=True,
        help="Path to .gauntlet/runs/<run-id>",
    )
    parser.add_argument(
        "--piece", required=True,
        help="Piece id whose claims/<piece>/ledger.json is audited",
    )
    parser.add_argument(
        "--skip-network", action="store_true",
        help="Do not fetch URLs; mark them unchecked-network-skipped",
    )
    args = parser.parse_args()

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        print(json.dumps({"error": "run dir not found: %s" % run_dir}))
        return 2

    piece_dir = os.path.join(run_dir, "claims", args.piece)
    ledger_path = os.path.join(piece_dir, "ledger.json")

    findings = []
    rows = []
    if not os.path.isfile(ledger_path):
        findings.append({
            "check": "ledger-missing",
            "detail": "no ledger at claims/%s/ledger.json." % args.piece,
        })
    else:
        try:
            with open(ledger_path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except ValueError:
            data = None
            findings.append({
                "check": "ledger-invalid",
                "detail": "claims/%s/ledger.json is not valid JSON."
                % args.piece,
            })
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict):
            rows = data.get("rows") or data.get("claims") or []

    total = len(rows)
    unsupported_count = 0
    cited_count = 0
    source_counts = {}
    row_reports = []
    fatal = bool(findings)

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            findings.append({
                "check": "row-invalid",
                "row": index,
                "detail": "ledger row %d is not an object." % index,
            })
            fatal = True
            continue

        support_type = str(row.get("support_type", "")).strip()
        support_valid = support_type in SUPPORT_TYPES
        if not support_valid:
            findings.append({
                "check": "invalid-support-type",
                "row": index,
                "detail": "support_type %r is not in the closed set %s."
                % (support_type, sorted(SUPPORT_TYPES)),
            })
            fatal = True
        if support_type == "unsupported":
            unsupported_count += 1
            fatal = True
            findings.append({
                "check": "unsupported-claim",
                "row": index,
                "detail": "unsupported claim: %r at %s."
                % (str(row.get("claim_text", ""))[:120],
                   row.get("location", "<no location>")),
            })

        source = str(row.get("source", "") or "").strip()
        cited = bool(source) and support_valid and support_type != "unsupported"
        if cited:
            cited_count += 1
        if source:
            key = strip_fragment(source)
            source_counts[key] = source_counts.get(key, 0) + 1

        # Reachability.
        quote_present = "not-checked"
        if not source:
            reachability = "none"
        elif is_url(source):
            if args.skip_network:
                reachability = "unchecked-network-skipped"
            else:
                reachability = check_url(source)
        else:
            rel = strip_fragment(source)
            candidate = rel if os.path.isabs(rel) \
                else os.path.join(run_dir, rel)
            reachability = "reachable" if os.path.exists(candidate) \
                else "unreachable"
            # Quote presence, readable text file sources only.
            quote = str(row.get("supporting_quote", "") or "").strip()
            if reachability == "reachable" and quote \
                    and os.path.isfile(candidate):
                try:
                    with open(candidate, "r", encoding="utf-8") as fh:
                        body = fh.read()
                    quote_present = normalize_text(quote) in \
                        normalize_text(body)
                except (OSError, UnicodeDecodeError):
                    quote_present = "not-checked"

        if reachability == "unreachable":
            findings.append({
                "check": "source-unreachable",
                "row": index,
                "detail": "source %r does not resolve." % source,
            })
        if quote_present is False:
            findings.append({
                "check": "quote-missing-from-source",
                "row": index,
                "detail": "supporting_quote not found in source %r."
                % source,
            })

        row_reports.append({
            "row": index,
            "location": row.get("location", ""),
            "support_type": support_type,
            "support_type_valid": support_valid,
            "source": source,
            "reachability": reachability,
            "quote_present": quote_present,
        })

    top_source = None
    top_share = 0.0
    if source_counts:
        top_source = max(source_counts, key=source_counts.get)
        top_share = round(source_counts[top_source] / total, 4) if total else 0.0

    audit = {
        "script": "claim_audit",
        "piece": args.piece,
        "computed_at": datetime.datetime.now(datetime.timezone.utc)
        .isoformat(timespec="seconds"),
        "network_checked": not args.skip_network,
        "total_claims": total,
        "unsupported_count": unsupported_count,
        "claim_to_citation_ratio": round(cited_count / total, 4)
        if total else 0.0,
        "duplicate_source_concentration": {
            "distinct_sources": len(source_counts),
            "top_source": top_source,
            "top_source_share": top_share,
        },
        "rows": row_reports,
        "findings": findings,
        "ok": not fatal,
    }

    if os.path.isdir(run_dir):
        os.makedirs(piece_dir, exist_ok=True)
        audit_path = os.path.join(piece_dir, "audit.json")
        with open(audit_path, "w", encoding="utf-8") as fh:
            json.dump(audit, fh, indent=2)
            fh.write("\n")
        audit["audit_path"] = audit_path

    print(json.dumps(audit, indent=2))
    return 0 if audit["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
