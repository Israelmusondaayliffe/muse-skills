#!/usr/bin/env python3
"""Lint a gauntlet prompt per SPEC 9.3. The output prompt must be short.

Fails the prompt when it:
  - exceeds 600 words (warns above 400)
  - prescribes architecture, file layout, module lists, or a tech stack the
    user did not specify (lines carrying a user-specified marker are exempt)
  - fixes a round count, for example "exactly 8 rounds" or "run 10 rounds"
  - omits any of the 9 required clauses (detected by keyword sets)
  - omits the effort and subagent instruction
  - for knowledge-work domains (prose, research, strategy, deck,
    prompt-system), omits the reader-proxy or claim-ledger requirements

Prints JSON {result, word_count, failures, warnings} on stdout.
Exit codes: 0 pass (warnings allowed), 1 fail, 2 usage error.
"""

import argparse
import json
import re
import sys

DOMAINS = ["code", "visual", "prose", "research", "deck", "strategy",
           "prompt-system", "brand"]
KNOWLEDGE_DOMAINS = {"prose", "research", "strategy", "deck", "prompt-system"}

WORD_FAIL = 600
WORD_WARN = 400

PATH_RE = re.compile(r"[\w.~-]+/[\w.-][\w./~-]*")

# Each clause holds keyword groups. The clause is present only when every
# group has at least one keyword found in the prompt.
CLAUSES = [
    ("the goal", [["goal"]]),
    ("split into the smallest independently judgeable pieces",
     [["split", "decompose", "break", "divide"], ["piece"]]),
    ("builder plus separate critic with fresh context",
     [["builder"], ["critic"],
      ["fresh context", "clean context", "separate context", "fresh-context",
       "clean-context", "no shared context", "never sees the builder",
       "no builder context"]]),
    ("blind comparison where possible", [["blind"]]),
    ("loop until it wins or the user stops",
     [["loop", "iterate", "repeat", "keep going"], ["until"]]),
    ("maintain the live progress page",
     [["workbench", "progress page", "live progress", "progress board"]]),
    ("write state to the named run directory",
     [["run directory", "run dir", ".gauntlet"]]),
]

FRAMEWORK_RE = re.compile(
    r"\b(use|using|with|in|on|build|built|implement|implemented|write|written)"
    r"\b[^.\n]{0,60}?\b(react|vue|angular|svelte|next\.js|nuxt|django|flask|"
    r"fastapi|express|rails|laravel|spring boot|tailwind|bootstrap|"
    r"postgres(?:ql)?|mysql|mongodb|redis|kubernetes|docker|graphql)\b",
    re.IGNORECASE)

FILE_NAME_RE = re.compile(
    r"\b[\w][\w./-]*\.(py|js|ts|tsx|jsx|go|rs|java|rb|php|c|cpp|h|css|scss|"
    r"html|json|yaml|yml|toml|sql|sh|swift|kt)\b", re.IGNORECASE)

LIST_ITEM_RE = re.compile(r"^\s*([-*+]|\d+[.)])\s+")

CAP_CONTEXT_RE = re.compile(
    r"\b(up to|at most|cap|caps|capped|maximum|max|no more than|within|"
    r"fewer than|less than|limit|budget)\b")


def has_keyword(text_lower, keyword):
    """Match a keyword; single words match with a simple plural tolerance."""
    if " " in keyword or "-" in keyword or "." in keyword:
        return keyword in text_lower
    return re.search(r"\b" + re.escape(keyword) + r"(s|es)?\b", text_lower) is not None


def clause_present(text_lower, groups):
    return all(any(has_keyword(text_lower, kw) for kw in group) for group in groups)


def architecture_failures(text, lines):
    failures = []
    lower = text.lower()

    # Directory trees: box-drawing characters or explicit layout language.
    if any(marker in text for marker in ("├", "└", "─", "│")):
        failures.append("prescribes architecture: directory tree detected")
    elif re.search(r"\b(file layout|directory (structure|tree|layout)|"
                   r"folder structure|module (layout|structure))\b", lower):
        failures.append("prescribes architecture: file or directory layout language")

    # Lists of named modules or files to create. Bar reference lines are exempt.
    listed = 0
    for line in lines:
        stripped = line.strip()
        if not LIST_ITEM_RE.match(stripped):
            continue
        if re.search(r"\bbar\b", stripped.lower()):
            continue
        if FILE_NAME_RE.search(stripped):
            listed += 1
    if listed >= 3 or re.search(r"\bcreate (the following|these) (files|modules)\b", lower):
        failures.append("prescribes architecture: a list of named files or modules to create")

    # Tech stack prescriptions without a user-specified marker.
    for line in lines:
        low = line.lower()
        if "user-specified" in low or "user specified" in low:
            continue
        if FRAMEWORK_RE.search(line):
            failures.append("prescribes a tech stack not marked user-specified: %s"
                            % line.strip()[:80])
            break

    return failures


def round_count_failures(text_lower):
    failures = []
    for match in re.finditer(r"\b\d+\s+rounds?\b", text_lower):
        window = text_lower[max(0, match.start() - 40):match.end() + 25]
        if CAP_CONTEXT_RE.search(window):
            continue
        failures.append("fixes a round count: '%s'" % match.group(0))
        break
    if not failures and re.search(
            r"\bexactly\s+(\d+|one|two|three|four|five|six|seven|eight|nine|"
            r"ten|eleven|twelve)\s+rounds?\b", text_lower):
        failures.append("fixes a round count with 'exactly N rounds'")
    return failures


def lint(text, domain):
    lines = text.splitlines()
    lower = text.lower()
    failures = []
    warnings = []

    word_count = len(text.split())
    if word_count > WORD_FAIL:
        failures.append("prompt is %d words; the limit is %d" % (word_count, WORD_FAIL))
    elif word_count > WORD_WARN:
        warnings.append("prompt is %d words; aim for under %d" % (word_count, WORD_WARN))

    failures.extend(architecture_failures(text, lines))
    failures.extend(round_count_failures(lower))

    # Required clauses.
    for name, groups in CLAUSES:
        if not clause_present(lower, groups):
            failures.append("missing required clause: %s" % name)

    # The bar, with real paths: a path must sit near a bar mention, so an
    # unrelated path elsewhere in the prompt cannot satisfy this clause.
    bar_mentions = list(re.finditer(r"\bbar\b", lower))
    if not bar_mentions:
        failures.append("missing required clause: the bar, with real paths")
    elif not any(PATH_RE.search(lower[max(0, m.start() - 100):m.start() + 250])
                 for m in bar_mentions):
        failures.append("missing required clause: the bar, with real paths "
                        "(no real path near the bar)")

    # Effort and subagent instruction (required clause 9, called out separately).
    if not (has_keyword(lower, "subagent") or "sub-agent" in lower):
        failures.append("missing the effort and subagent instruction (no subagent mention)")
    elif not (has_keyword(lower, "effort") or "xhigh" in lower or "ultracode" in lower):
        failures.append("missing the effort and subagent instruction (no effort setting)")

    # Knowledge-work requirements.
    if domain in KNOWLEDGE_DOMAINS:
        if not ("reader-proxy" in lower or "reader proxy" in lower):
            failures.append("knowledge-work domain '%s': missing the reader-proxy requirement"
                            % domain)
        if not any(kw in lower for kw in ("claim ledger", "claim-ledger", "claim_ledger",
                                          "claim audit", "claim-audit", "claim_audit")):
            failures.append("knowledge-work domain '%s': missing the claim-ledger requirement"
                            % domain)

    return {
        "result": "fail" if failures else "pass",
        "word_count": word_count,
        "failures": failures,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Lint a gauntlet prompt.md per SPEC 9.3: length, required "
                    "clauses, no-prescription enforcement.")
    parser.add_argument("prompt", help="Path to prompt.md")
    parser.add_argument("--domain", choices=DOMAINS,
                        help="Primary domain; knowledge-work domains add "
                             "reader-proxy and claim-ledger checks")
    args = parser.parse_args(argv)

    try:
        with open(args.prompt, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        parser.error("cannot read prompt file: %s" % exc)

    report = lint(text, args.domain)
    print(json.dumps(report))
    return 0 if report["result"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
