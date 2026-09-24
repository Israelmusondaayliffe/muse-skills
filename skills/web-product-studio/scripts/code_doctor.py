#!/usr/bin/env python3
"""
Code Doctor - Deterministic code validation for the code-production-agent skill.

Modes:
  full     - Run all checks (syntax, errors, complexity, security, style)
  syntax   - Syntax validation only
  errors   - Common error pattern scan
  complexity - Function length and nesting depth analysis
  security - Basic security issue scan
  style    - Naming and formatting checks
  structure - Folder structure analysis against a plan

Usage:
  python code_doctor.py --mode full <file_or_directory>
  python code_doctor.py --mode syntax <file_path>
  python code_doctor.py --mode structure <directory> --plan <plan_file>
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


# --- Language Detection ---

LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".sql": "sql",
    ".sh": "bash",
    ".bash": "bash",
}


def detect_language(filepath):
    ext = Path(filepath).suffix.lower()
    return LANG_MAP.get(ext, "unknown")


# --- Syntax Check ---

def check_syntax_python(content, filepath):
    issues = []
    try:
        compile(content, filepath, "exec")
    except SyntaxError as e:
        issues.append({
            "severity": "critical",
            "type": "syntax",
            "file": filepath,
            "line": e.lineno,
            "message": f"Syntax error: {e.msg}",
            "plain_english": "There's a typo or structural mistake in the code that prevents it from running."
        })
    return issues


def check_syntax_json(content, filepath):
    issues = []
    try:
        json.loads(content)
    except json.JSONDecodeError as e:
        issues.append({
            "severity": "critical",
            "type": "syntax",
            "file": filepath,
            "line": e.lineno,
            "message": f"Invalid JSON: {e.msg}",
            "plain_english": "The data file has a formatting mistake (maybe a missing comma or bracket)."
        })
    return issues


def check_syntax_js(content, filepath):
    """Basic JS/TS syntax heuristics (not a full parser)."""
    issues = []
    lines = content.split("\n")

    # Check bracket/paren/brace balance
    counts = {"(": 0, ")": 0, "[": 0, "]": 0, "{": 0, "}": 0}
    for char in content:
        if char in counts:
            counts[char] += 1

    if counts["("] != counts[")"]:
        issues.append({
            "severity": "critical",
            "type": "syntax",
            "file": filepath,
            "line": None,
            "message": f"Unbalanced parentheses: {counts['(']} open, {counts[')']} close",
            "plain_english": "There's a missing or extra parenthesis somewhere in the code."
        })
    if counts["["] != counts["]"]:
        issues.append({
            "severity": "critical",
            "type": "syntax",
            "file": filepath,
            "line": None,
            "message": f"Unbalanced brackets: {counts['[']} open, {counts[']']} close",
            "plain_english": "There's a missing or extra square bracket somewhere in the code."
        })
    if counts["{"] != counts["}"]:
        issues.append({
            "severity": "critical",
            "type": "syntax",
            "file": filepath,
            "line": None,
            "message": f"Unbalanced braces: {counts['{']} open, {counts['}']} close",
            "plain_english": "There's a missing or extra curly brace somewhere in the code."
        })

    return issues


def check_syntax(content, filepath, lang):
    if lang == "python":
        return check_syntax_python(content, filepath)
    elif lang == "json":
        return check_syntax_json(content, filepath)
    elif lang in ("javascript", "typescript"):
        return check_syntax_js(content, filepath)
    return []


# --- Common Error Pattern Scan ---

def scan_errors(content, filepath, lang):
    issues = []
    lines = content.split("\n")

    # Universal patterns
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Console/print debugging left in
        if lang in ("javascript", "typescript"):
            if re.search(r'\bconsole\.(log|debug|info)\b', stripped):
                if not re.search(r'//.*console', stripped):  # Not in comment
                    issues.append({
                        "severity": "note",
                        "type": "error_pattern",
                        "file": filepath,
                        "line": i,
                        "message": "console.log left in code",
                        "plain_english": "Debug logging found. Remove before shipping unless intentional."
                    })

        if lang == "python":
            if re.search(r'^\s*print\(', stripped) and "# debug" not in stripped.lower():
                issues.append({
                    "severity": "note",
                    "type": "error_pattern",
                    "file": filepath,
                    "line": i,
                    "message": "print() statement found",
                    "plain_english": "Debug print found. Consider using logging instead."
                })

        # TODO/FIXME/HACK comments
        if re.search(r'\b(TODO|FIXME|HACK|XXX)\b', stripped):
            issues.append({
                "severity": "warning",
                "type": "error_pattern",
                "file": filepath,
                "line": i,
                "message": f"Unresolved marker: {stripped[:80]}",
                "plain_english": "There's an unfinished task marked in the code."
            })

    # Language-specific patterns
    if lang in ("javascript", "typescript"):
        issues.extend(_scan_js_errors(content, filepath, lines))
    elif lang == "python":
        issues.extend(_scan_python_errors(content, filepath, lines))

    return issues


def _scan_js_errors(content, filepath, lines):
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # var usage
        if re.match(r'\bvar\s+', stripped):
            issues.append({
                "severity": "warning",
                "type": "error_pattern",
                "file": filepath,
                "line": i,
                "message": "'var' used instead of 'let' or 'const'",
                "plain_english": "Old-style variable declaration. Use 'const' or 'let' instead."
            })

        # == instead of ===
        if re.search(r'[^!=]==[^=]', stripped) and "===" not in stripped:
            issues.append({
                "severity": "warning",
                "type": "error_pattern",
                "file": filepath,
                "line": i,
                "message": "Loose equality '==' used instead of strict '==='",
                "plain_english": "Using loose comparison which can cause unexpected type conversion bugs."
            })

        # eval usage
        if re.search(r'\beval\s*\(', stripped):
            issues.append({
                "severity": "critical",
                "type": "security",
                "file": filepath,
                "line": i,
                "message": "eval() used - security risk",
                "plain_english": "eval() executes arbitrary code and is a major security vulnerability."
            })

    return issues


def _scan_python_errors(content, filepath, lines):
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Mutable default argument
        if re.search(r'def\s+\w+\s*\([^)]*=\s*(\[\]|\{\}|\bset\(\))', stripped):
            issues.append({
                "severity": "warning",
                "type": "error_pattern",
                "file": filepath,
                "line": i,
                "message": "Mutable default argument (list, dict, or set as default)",
                "plain_english": "Using a list or dictionary as a default value causes a shared-state bug."
            })

        # Bare except
        if re.match(r'\s*except\s*:', stripped):
            issues.append({
                "severity": "warning",
                "type": "error_pattern",
                "file": filepath,
                "line": i,
                "message": "Bare except: catches all exceptions including KeyboardInterrupt",
                "plain_english": "This catches ALL errors, even ones that shouldn't be caught. Specify the error type."
            })

        # eval usage
        if re.search(r'\beval\s*\(', stripped):
            issues.append({
                "severity": "critical",
                "type": "security",
                "file": filepath,
                "line": i,
                "message": "eval() used - security risk",
                "plain_english": "eval() executes arbitrary code and is a major security vulnerability."
            })

    return issues


# --- Complexity Analysis ---

def analyze_complexity(content, filepath, lang):
    issues = []
    lines = content.split("\n")

    if lang == "python":
        issues.extend(_complexity_python(lines, filepath))
    elif lang in ("javascript", "typescript"):
        issues.extend(_complexity_js(lines, filepath))

    return issues


def _complexity_python(lines, filepath):
    issues = []
    func_name = None
    func_start = 0
    func_lines = 0
    max_indent = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Detect function definition
        match = re.match(r'^(\s*)def\s+(\w+)', line)
        if match:
            # Report previous function
            if func_name and func_lines > 30:
                issues.append({
                    "severity": "warning",
                    "type": "complexity",
                    "file": filepath,
                    "line": func_start,
                    "message": f"Function '{func_name}' is {func_lines} lines (recommend max 30)",
                    "plain_english": f"The function '{func_name}' is very long. Breaking it into smaller pieces would make it easier to understand and maintain."
                })
            if func_name and max_indent > 4:
                issues.append({
                    "severity": "warning",
                    "type": "complexity",
                    "file": filepath,
                    "line": func_start,
                    "message": f"Function '{func_name}' has nesting depth {max_indent} (recommend max 3)",
                    "plain_english": f"The function '{func_name}' has too many nested levels. Consider using early returns or extracting helper functions."
                })

            func_name = match.group(2)
            func_start = i
            func_lines = 0
            max_indent = 0
        elif func_name:
            func_lines += 1
            indent = len(line) - len(line.lstrip())
            indent_level = indent // 4
            max_indent = max(max_indent, indent_level)

    # Report last function
    if func_name and func_lines > 30:
        issues.append({
            "severity": "warning",
            "type": "complexity",
            "file": filepath,
            "line": func_start,
            "message": f"Function '{func_name}' is {func_lines} lines (recommend max 30)",
            "plain_english": f"The function '{func_name}' is very long."
        })

    return issues


def _complexity_js(lines, filepath):
    issues = []
    func_pattern = re.compile(
        r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:function|\([^)]*\)\s*=>|\w+\s*=>))'
    )
    func_name = None
    func_start = 0
    func_lines = 0
    brace_depth = 0
    max_depth = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("//"):
            continue

        match = func_pattern.search(line)
        if match and brace_depth == 0:
            if func_name and func_lines > 30:
                issues.append({
                    "severity": "warning",
                    "type": "complexity",
                    "file": filepath,
                    "line": func_start,
                    "message": f"Function '{func_name}' is {func_lines} lines (recommend max 30)",
                    "plain_english": f"The function '{func_name}' is very long."
                })

            func_name = match.group(1) or match.group(2)
            func_start = i
            func_lines = 0
            max_depth = 0

        if func_name:
            func_lines += 1
            brace_depth += line.count("{") - line.count("}")
            max_depth = max(max_depth, brace_depth)

    if func_name and func_lines > 30:
        issues.append({
            "severity": "warning",
            "type": "complexity",
            "file": filepath,
            "line": func_start,
            "message": f"Function '{func_name}' is {func_lines} lines (recommend max 30)",
            "plain_english": f"The function '{func_name}' is very long."
        })

    return issues


# --- Security Scan ---

def scan_security(content, filepath, lang):
    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Hardcoded secrets patterns
        secret_patterns = [
            (r'(?:password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', "Hardcoded password"),
            (r'(?:api_key|apikey|api-key)\s*=\s*["\'][^"\']+["\']', "Hardcoded API key"),
            (r'(?:secret|token)\s*=\s*["\'][A-Za-z0-9+/=]{16,}["\']', "Hardcoded secret/token"),
            (r'(?:aws_access_key|aws_secret)\s*=\s*["\'][^"\']+["\']', "Hardcoded AWS credential"),
        ]

        for pattern, desc in secret_patterns:
            if re.search(pattern, stripped, re.IGNORECASE):
                # Skip if it's clearly a placeholder
                if any(p in stripped.lower() for p in ["your_", "placeholder", "example", "xxx", "changeme", "process.env", "os.environ"]):
                    continue
                issues.append({
                    "severity": "critical",
                    "type": "security",
                    "file": filepath,
                    "line": i,
                    "message": desc,
                    "plain_english": f"A {desc.lower()} was found in the code. This should be in an environment variable, not in the code."
                })

        # SQL injection patterns
        if lang in ("python", "javascript", "typescript"):
            if re.search(r'(?:execute|query)\s*\(\s*f?["\'].*\{|\+\s*\w+.*(?:SELECT|INSERT|UPDATE|DELETE)', stripped, re.IGNORECASE):
                if not re.search(r'\?\s*,|\%s|:\w+|\$\d+', stripped):
                    issues.append({
                        "severity": "critical",
                        "type": "security",
                        "file": filepath,
                        "line": i,
                        "message": "Possible SQL injection: string concatenation in query",
                        "plain_english": "User input might be directly inserted into a database query. This is a serious security risk. Use parameterized queries instead."
                    })

        # innerHTML usage
        if re.search(r'\.innerHTML\s*=', stripped):
            issues.append({
                "severity": "warning",
                "type": "security",
                "file": filepath,
                "line": i,
                "message": "innerHTML assignment - potential XSS vulnerability",
                "plain_english": "Directly setting HTML content can allow malicious code injection. Use textContent or sanitize the input."
            })

    return issues


# --- Style Check ---

def check_style(content, filepath, lang):
    issues = []
    lines = content.split("\n")

    # File-level checks
    if len(lines) > 500:
        issues.append({
            "severity": "note",
            "type": "style",
            "file": filepath,
            "line": None,
            "message": f"File is {len(lines)} lines. Consider splitting into smaller modules.",
            "plain_english": "This file is very long. Splitting it into smaller, focused files would improve readability."
        })

    for i, line in enumerate(lines, 1):
        # Very long lines
        if len(line) > 120:
            issues.append({
                "severity": "note",
                "type": "style",
                "file": filepath,
                "line": i,
                "message": f"Line is {len(line)} characters (recommend max 120)",
                "plain_english": "This line is very long and hard to read."
            })

    # Single-letter variable names (excluding common conventions: i, j, k, x, y, e)
    allowed_short = {"i", "j", "k", "x", "y", "e", "f", "n", "_"}
    if lang == "python":
        for i, line in enumerate(lines, 1):
            for match in re.finditer(r'\b([a-z])\s*=\s*', line):
                if match.group(1) not in allowed_short:
                    issues.append({
                        "severity": "note",
                        "type": "style",
                        "file": filepath,
                        "line": i,
                        "message": f"Single-letter variable name '{match.group(1)}'",
                        "plain_english": "Using a single letter as a variable name makes the code harder to understand."
                    })

    return issues


# --- Structure Analysis ---

def analyze_structure(directory, plan_file=None):
    """Analyze directory structure. Optionally compare against a plan file."""
    issues = []
    structure = []

    for root, dirs, files in os.walk(directory):
        # Skip hidden dirs and node_modules
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        level = root.replace(directory, "").count(os.sep)
        indent = "  " * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        for f in sorted(files):
            if not f.startswith("."):
                structure.append(f"{indent}  {f}")

    # Check for common missing files
    all_files = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            all_files.append(os.path.join(root, f))

    file_names = [os.path.basename(f) for f in all_files]

    # Check for empty directories
    for root, dirs, files in os.walk(directory):
        if not dirs and not files:
            issues.append({
                "severity": "note",
                "type": "structure",
                "file": root,
                "line": None,
                "message": "Empty directory",
                "plain_english": "This folder is empty. It might be a leftover from setup."
            })

    return {
        "structure": "\n".join(structure),
        "file_count": len(all_files),
        "issues": issues
    }


# --- Main Runner ---

def run_checks(filepath, mode="full"):
    """Run specified checks on a file or directory."""
    results = {
        "file": filepath,
        "mode": mode,
        "issues": [],
        "summary": {}
    }

    if os.path.isdir(filepath):
        # Run on all supported files in directory
        for root, dirs, files in os.walk(filepath):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
            for f in files:
                fpath = os.path.join(root, f)
                lang = detect_language(fpath)
                if lang == "unknown":
                    continue
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                    file_issues = _check_file(content, fpath, lang, mode)
                    results["issues"].extend(file_issues)
                except Exception as e:
                    results["issues"].append({
                        "severity": "warning",
                        "type": "read_error",
                        "file": fpath,
                        "line": None,
                        "message": f"Could not read file: {e}",
                        "plain_english": "This file couldn't be opened for checking."
                    })
    else:
        lang = detect_language(filepath)
        if lang == "unknown":
            results["issues"].append({
                "severity": "note",
                "type": "unsupported",
                "file": filepath,
                "line": None,
                "message": f"Unsupported file type: {Path(filepath).suffix}",
                "plain_english": "This file type isn't supported for automated checking."
            })
        else:
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                results["issues"] = _check_file(content, filepath, lang, mode)
            except Exception as e:
                results["issues"].append({
                    "severity": "critical",
                    "type": "read_error",
                    "file": filepath,
                    "line": None,
                    "message": f"Could not read file: {e}",
                    "plain_english": "This file couldn't be opened for checking."
                })

    # Summarize
    by_severity = {"critical": 0, "warning": 0, "note": 0}
    by_type = {}
    for issue in results["issues"]:
        sev = issue.get("severity", "note")
        by_severity[sev] = by_severity.get(sev, 0) + 1
        typ = issue.get("type", "unknown")
        by_type[typ] = by_type.get(typ, 0) + 1

    results["summary"] = {
        "total_issues": len(results["issues"]),
        "by_severity": by_severity,
        "by_type": by_type,
        "passed": by_severity["critical"] == 0
    }

    return results


def _check_file(content, filepath, lang, mode):
    issues = []
    checks = {
        "syntax": lambda: check_syntax(content, filepath, lang),
        "errors": lambda: scan_errors(content, filepath, lang),
        "complexity": lambda: analyze_complexity(content, filepath, lang),
        "security": lambda: scan_security(content, filepath, lang),
        "style": lambda: check_style(content, filepath, lang),
    }

    if mode == "full":
        for check_fn in checks.values():
            issues.extend(check_fn())
    elif mode in checks:
        issues.extend(checks[mode]())

    return issues


def format_report(results):
    """Format results as a readable report."""
    lines = []
    lines.append("=" * 60)
    lines.append("CODE DOCTOR REPORT")
    lines.append("=" * 60)
    lines.append(f"Target: {results['file']}")
    lines.append(f"Mode: {results['mode']}")
    lines.append("")

    summary = results["summary"]
    lines.append(f"Total issues: {summary['total_issues']}")
    lines.append(f"  Critical: {summary['by_severity'].get('critical', 0)}")
    lines.append(f"  Warnings: {summary['by_severity'].get('warning', 0)}")
    lines.append(f"  Notes:    {summary['by_severity'].get('note', 0)}")
    lines.append(f"  Status:   {'PASSED' if summary['passed'] else 'FAILED (critical issues found)'}")
    lines.append("")

    if results["issues"]:
        lines.append("-" * 60)

        # Group by severity
        for sev in ["critical", "warning", "note"]:
            sev_issues = [i for i in results["issues"] if i["severity"] == sev]
            if sev_issues:
                lines.append(f"\n[{sev.upper()}]")
                for issue in sev_issues:
                    loc = f"{issue['file']}"
                    if issue.get("line"):
                        loc += f":{issue['line']}"
                    lines.append(f"  {loc}")
                    lines.append(f"    {issue['message']}")
                    lines.append(f"    -> {issue['plain_english']}")
                    lines.append("")
    else:
        lines.append("No issues found. Code looks clean.")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Code Doctor - Deterministic code validation")
    parser.add_argument("target", help="File or directory to check")
    parser.add_argument("--mode", choices=["full", "syntax", "errors", "complexity", "security", "style", "structure"],
                        default="full", help="Check mode (default: full)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--plan", help="Plan file for structure comparison (used with --mode structure)")

    args = parser.parse_args()

    if args.mode == "structure":
        result = analyze_structure(args.target, args.plan)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("DIRECTORY STRUCTURE:")
            print(result["structure"])
            print(f"\nFiles: {result['file_count']}")
            if result["issues"]:
                print("\nIssues:")
                for issue in result["issues"]:
                    print(f"  [{issue['severity']}] {issue['file']}: {issue['message']}")
        sys.exit(0)

    results = run_checks(args.target, args.mode)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_report(results))

    sys.exit(0 if results["summary"]["passed"] else 1)


if __name__ == "__main__":
    main()
