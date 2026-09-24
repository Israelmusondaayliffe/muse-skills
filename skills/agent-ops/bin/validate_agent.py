#!/usr/bin/env python3
"""Deterministic validator for agent-builder outputs.

Kinds:
  agent     Autonomous agent design: stop conditions, ground truth,
            success criteria, pause points.
  workflow  Workflow design: control element present (gate, classifier
            fallback, aggregation, orchestrator verification, or
            evaluator criteria) plus stop/cap.
  subagent  Claude Code subagent file: frontmatter shape, kebab-case
            name, description, ground truth, stop conditions.
All kinds: no em-dashes or en-dashes.

Usage:
  python validate_agent.py <file> --kind agent|workflow|subagent
  cat design.md | python validate_agent.py - --kind agent

Exit 0 when all required checks pass, 1 otherwise.
"""

import argparse
import re
import sys

CHECKS = {
    "stops": {
        "label": "Stop conditions (numeric cap and failure stop)",
        "patterns": [
            r"\bmaximum (of )?\d+\b", r"\bmax(imum)? \d+ (iterations|attempts|steps|rounds|runs)\b",
            r"\bstop after \d+\b", r"\bafter \d+ (attempts|retries|tries|rounds)\b",
            r"\b\$\d+", r"\b\d+ dollars?\b", r"\bbudget\b.{0,30}\d",
        ],
        "hint": "Add numeric stop conditions: 'Maximum 15 iterations' and 'if X fails after 3 attempts, stop and report.'",
    },
    "ground_truth": {
        "label": "Ground truth verification (not self-report)",
        "patterns": [
            r"\brun (the )?(tests?|build|lint|pytest|npm (test|run build))\b",
            r"\bground truth\b", r"\btool results?\b", r"\bcode execution\b",
            r"\btest output\b", r"\bverify (with|against|by running)\b",
            r"\bnot (from|on) (your own|its own|self)[- ]report\b",
            r"\bnever trust (the )?(worker'?s? )?self[- ]report\b",
            r"\bverifier agent\b", r"\bseparate (grader|evaluator|fast model)\b",
        ],
        "hint": "Name the environmental check: 'verify by running <command> and assess from its output, never self-report.'",
    },
    "success": {
        "label": "Success criteria",
        "patterns": [
            r"\bstop (and report )?when\b", r"\bdone means\b", r"\bsuccess criteria\b",
            r"\bcomplete[d]? (and|with|when)\b", r"\ball .{0,40}(pass|complete)\b",
            r"\bhand back\b.{0,60}\bwhen\b", r"\baccepted (means|when)\b",
        ],
        "hint": "Add a checkable success condition: 'Stop when [end state] is complete and verified.'",
    },
    "pause": {
        "label": "Human pause points",
        "patterns": [
            r"\bpause point\b", r"\bcheckpoint\b", r"\bsign[- ]?off\b",
            r"\bwait for (me|the user|approval)\b", r"\bapproval gate\b",
            r"\bstop and (wait|confirm|ask)\b", r"\breturn(ing)? to the (human|user) (only )?for\b",
            r"\bhand back to the main agent\b", r"\bescalate\b",
        ],
        "hint": "Place a human checkpoint before any step where a wrong call poisons downstream work.",
    },
    "control": {
        "label": "Workflow control element (gate/fallback/aggregation/verification/criteria)",
        "patterns": [
            r"\bgate\b", r"\bfallback\b", r"\baggregat(e|ion|or)\b", r"\bvot(e|ing)\b",
            r"\bevaluat(or|ion) criteria\b", r"\bclassif(y|ier|ication)\b",
            r"\borchestrator (runs|verifies|checks)\b", r"\bcheck between (steps|phases)\b",
            r"\btests? per phase\b", r"\bvalidate[sd]? (it )?against\b",
        ],
        "hint": "Add the pattern's defining control: gates between chain steps, a classifier fallback, an aggregation rule, orchestrator-run verification, or explicit evaluator criteria.",
    },
    "frontmatter": {
        "label": "Subagent frontmatter (name + description)",
        "patterns": [],  # handled structurally
        "hint": "Subagent files need YAML frontmatter with kebab-case 'name:' and a delegation-first 'description:'.",
    },
    "iteration_policy": {
        "label": "Iteration policy (how to choose the next attempt)",
        "patterns": [
            r"\biteration policy\b", r"\bbetween (iterations|attempts)\b",
            r"\b(next|each) (action|attempt|iteration).{0,50}\b(choose|chosen|decide|pick)\b",
            r"\bif .{0,60}\b(cluster|appears?|persists?|fails?)\b.{0,60}\b(expand|tighten|switch|rerun|try)\b",
        ],
        "hint": "State how the agent picks its next action between attempts, retries without a policy repeat the same guess.",
    },
}

KIND_REQUIRED = {
    "agent": ["stops", "ground_truth", "success", "pause"],
    "workflow": ["control", "stops", "success"],
    "subagent": ["frontmatter", "ground_truth", "stops", "success"],
}

KIND_OPTIONAL = {
    "agent": ["iteration_policy"],
    "workflow": [],
    "subagent": [],
}


def check_frontmatter(text):
    m = re.match(r"\s*---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return False, "no frontmatter block"
    fm = m.group(1)
    name = re.search(r"^name:\s*(\S+)", fm, re.MULTILINE)
    desc = re.search(r"^description:\s*\S+", fm, re.MULTILINE)
    if not name:
        return False, "missing name field"
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name.group(1)):
        return False, f"name '{name.group(1)}' is not kebab-case"
    if not desc:
        return False, "missing description field"
    return True, "ok"


def check(text, key):
    lowered = text.lower()
    return any(re.search(p, lowered, re.MULTILINE) for p in CHECKS[key]["patterns"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="Design file, or - for stdin")
    ap.add_argument("--kind", choices=["agent", "workflow", "subagent"], required=True)
    args = ap.parse_args()

    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    failures = []
    print(f"Validating ({args.kind} kind)\n" + "-" * 52)

    for key in KIND_REQUIRED[args.kind]:
        if key == "frontmatter":
            ok, detail = check_frontmatter(text)
            print(f"[{'PASS' if ok else 'FAIL'}] {CHECKS[key]['label']}" + ("" if ok else f" ({detail})"))
        else:
            ok = check(text, key)
            print(f"[{'PASS' if ok else 'FAIL'}] {CHECKS[key]['label']}")
        if not ok:
            print(f"       fix: {CHECKS[key]['hint']}")
            failures.append(key)

    for key in KIND_OPTIONAL[args.kind]:
        ok = check(text, key)
        print(f"[{'PASS' if ok else 'WARN'}] {CHECKS[key]['label']} (advisory)")
        if not ok:
            print(f"       consider: {CHECKS[key]['hint']}")

    if "—" in text or "–" in text:
        print("[FAIL] Em-dash / en-dash found. Replace with a period or comma.")
        failures.append("dashes")
    else:
        print("[PASS] No em-dashes")

    print("-" * 52)
    if failures:
        print(f"RESULT: FAIL ({len(failures)} required check(s) missing)")
        sys.exit(1)
    print("RESULT: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
