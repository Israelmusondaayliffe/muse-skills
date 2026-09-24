import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .models import CheckResult, CheckStatus


CONTROL_IDS = [
    "CF-A01", "CF-A02", "CF-A03", "CF-A04", "CF-A05", "CF-A06", "CF-A07", "CF-A08",
    "CF-B09", "CF-B10", "CF-B11", "CF-B12", "CF-B13", "CF-B14", "CF-B15", "CF-B16", "CF-B17", "CF-B18", "CF-B19", "CF-B20", "CF-B21", "CF-B22",
    "CF-C23", "CF-C24", "CF-C25", "CF-C26", "CF-C27", "CF-C28", "CF-C29", "CF-C30", "CF-C31", "CF-C32", "CF-C33",
    "CF-D34", "CF-D35",
]

TEXT_SUFFIXES = {".py", ".html", ".js", ".ts", ".json", ".toml", ".yaml", ".yml", ".md", ".txt", ".sql"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^$\{][^'\"]{7,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]


def result(check_id: str, status: CheckStatus, explanation: str, evidence: Iterable[str] = (), repair: str = "Follow the approved paved road and rerun this check.", severity: str = "high", ai: bool = True, human: bool = False) -> CheckResult:
    return CheckResult(check_id, severity, status, list(evidence), explanation, repair, ai, human)


def _source_files(root: Path) -> List[Path]:
    ignored = {".git", ".citizen", "__pycache__", ".venv", "venv"}
    root = root.resolve()
    files = []
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES or ignored.intersection(path.parts):
            continue
        try:
            path.resolve().relative_to(root)
        except ValueError:
            continue
        files.append(path)
    return files


def _escaped_links(root: Path) -> List[str]:
    root = root.resolve()
    escaped = []
    for path in root.rglob("*"):
        if not path.is_symlink():
            continue
        try:
            path.resolve().relative_to(root)
        except (OSError, ValueError):
            escaped.append(str(path.relative_to(root)))
    return escaped


def _verified_evidence(path: Path, check_id: str) -> bool:
    if path.is_symlink() or not path.is_file():
        return False
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        datetime.fromisoformat(str(value["generated_at"]).replace("Z", "+00:00"))
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        return False
    return value.get("check_id") == check_id and value.get("status") == "PASS" and isinstance(value.get("producer"), str) and bool(value["producer"].strip())


def run_static(project_root: Path, policy: Dict[str, Any], brief: Dict[str, Any]) -> List[CheckResult]:
    project_root = project_root.resolve()
    files = _source_files(project_root)
    escaped_links = _escaped_links(project_root)
    texts = {}
    for path in files:
        try:
            texts[path] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
    joined = "\n".join(texts.values())
    oversized = [str(path.relative_to(project_root)) for path, text in texts.items() if len(text.splitlines()) > policy["max_source_lines"] or len(text.encode("utf-8")) > policy["max_source_bytes"]]
    inline = [str(path.relative_to(project_root)) for path, text in texts.items() if path.suffix.lower() in {".html", ".py", ".js"} and re.search(r"(?s)(?:const|var|let|DATA|data)\s*[=:].{1025,}", text)]
    minified = [str(path.relative_to(project_root)) for path, text in texts.items() if any(len(line) > 1000 for line in text.splitlines())]
    secret_hits = [str(path.relative_to(project_root)) for path, text in texts.items() if any(pattern.search(text) for pattern in SECRET_PATTERNS)]
    self_mod = [str(path.relative_to(project_root)) for path, text in texts.items() if re.search(r"(?i)(?:__file__|\.html).{0,120}(?:write|open|replace)|(?:write|open|replace).{0,120}(?:__file__|\.html)", text)]
    startup_rewrite = [str(path.relative_to(project_root)) for path, text in texts.items() if re.search(r"(?is)(startup|onload|DOMContentLoaded).{0,300}(write|replace|save)", text)]
    unsafe_eval = [str(path.relative_to(project_root)) for path, text in texts.items() if re.search(r"(?i)\b(eval|exec|pickle\.loads|yaml\.load|shell\s*=\s*True)\s*\(", text)]
    values = {
        "CF-A01": result("CF-A01", CheckStatus.FAIL if escaped_links else CheckStatus.PASS, "Project-root confinement was {}.".format("violated by symlinks" if escaped_links else "verified"), escaped_links or [str(project_root)]),
        "CF-A02": result("CF-A02", CheckStatus.FAIL if escaped_links else CheckStatus.PASS, "The scan rejected paths that could reach unrelated local content." if not escaped_links else "Links to unrelated local content were found.", escaped_links or ["Static scan scope"]),
        "CF-A03": result("CF-A03", CheckStatus.FAIL if secret_hits else CheckStatus.PASS, "Plaintext secret patterns were {}.".format("found" if secret_hits else "not found"), secret_hits or ["No matches"], ai=False, human=bool(secret_hits)),
        "CF-A04": result("CF-A04", CheckStatus.PASS if not secret_hits else CheckStatus.FAIL, "Secret values must use environment variables or verified secret references.", secret_hits or ["No plaintext values"]),
        "CF-A05": result("CF-A05", CheckStatus.UNAVAILABLE, "Network-destination enforcement is not connected in this local environment.", ["No network-policy adapter"], ai=False, human=True),
        "CF-A06": result("CF-A06", CheckStatus.PASS if (project_root / "requirements.lock").exists() else CheckStatus.FAIL, "Dependency lock evidence {}.".format("exists" if (project_root / "requirements.lock").exists() else "is missing"), ["requirements.lock"] if (project_root / "requirements.lock").exists() else []),
        "CF-A07": result("CF-A07", CheckStatus.UNAVAILABLE, "Production-write confirmation has no verified production adapter.", ["Local-only posture"], ai=False, human=True),
        "CF-A08": result("CF-A08", CheckStatus.PASS, "The routine build path contains no elevated provisioning adapter.", ["Environment posture"]),
        "CF-B09": result("CF-B09", CheckStatus.FAIL if oversized else CheckStatus.PASS, "Source size budgets were {}.".format("exceeded" if oversized else "met"), oversized or ["Within budgets"]),
        "CF-B10": result("CF-B10", CheckStatus.FAIL if inline else CheckStatus.PASS, "Large inline data was {}.".format("found" if inline else "not found"), inline or ["No large inline data"]),
        "CF-B11": result("CF-B11", CheckStatus.FAIL if minified else CheckStatus.PASS, "Minified or generated content was {} in normal source.".format("found" if minified else "not found"), minified or ["No long source lines"]),
        "CF-B12": result("CF-B12", CheckStatus.FAIL if self_mod else CheckStatus.PASS, "Self-modifying source behavior was {}.".format("found" if self_mod else "not found"), self_mod or ["No self-modification"]),
        "CF-B13": result("CF-B13", CheckStatus.FAIL if startup_rewrite else CheckStatus.PASS, "Startup data rewriting was {}.".format("found" if startup_rewrite else "not found"), startup_rewrite or ["No startup rewriting"]),
        "CF-B14": result("CF-B14", CheckStatus.FAIL if inline or self_mod else CheckStatus.PASS, "Persistent data is separated from application source." if not inline and not self_mod else "Persistent data is coupled to source.", inline + self_mod),
        "CF-B15": result("CF-B15", CheckStatus.UNAVAILABLE, "Atomic-write behavior requires a verified behavioral test; source keywords are not proof.", [], ai=False, human=True),
        "CF-B16": result("CF-B16", CheckStatus.UNAVAILABLE, "Concurrency behavior requires a verified behavioral test; source keywords are not proof.", [], ai=False, human=True),
        "CF-B17": result("CF-B17", CheckStatus.UNAVAILABLE, "External-input validation requires verified negative tests; source keywords are not proof.", [], ai=False, human=True),
        "CF-B18": result("CF-B18", CheckStatus.NOT_APPLICABLE if not brief["second_consumer"] else CheckStatus.UNAVAILABLE, "Authentication is not required for a sole-user prototype." if not brief["second_consumer"] else "Shared production authentication is unavailable without a verified identity adapter.", ["Brief"], ai=False, human=brief["second_consumer"]),
        "CF-B19": result("CF-B19", CheckStatus.NOT_APPLICABLE if "write" not in str(brief["access"]).lower() else CheckStatus.FAIL, "Write authorization was evaluated.", ["Brief"]),
        "CF-B20": result("CF-B20", CheckStatus.UNAVAILABLE, "Audit behavior requires a verified behavioral test; source keywords are not proof.", [], ai=False, human=True),
        "CF-B21": result("CF-B21", CheckStatus.FAIL if unsafe_eval else CheckStatus.PASS, "Unsafe evaluation, deserialization, or shell interpolation was {}.".format("found" if unsafe_eval else "not found"), unsafe_eval or ["No unsafe primitives"]),
        "CF-B22": result("CF-B22", CheckStatus.NOT_APPLICABLE if not any(path.suffix == ".sql" for path in files) else CheckStatus.FAIL, "Schema migration evidence was evaluated.", ["Source scan"]),
    }
    return [values[key] for key in CONTROL_IDS[:22]]


def run_release_evidence(project_root: Path, policy: Dict[str, Any], brief: Dict[str, Any]) -> List[CheckResult]:
    citizen = project_root / ".citizen"
    evidence = citizen / "evidence"
    def ev(check_id: str, filename: str, explanation: str, unavailable: bool = False) -> CheckResult:
        path = evidence / filename
        if _verified_evidence(path, check_id):
            return result(check_id, CheckStatus.PASS, explanation, [str(path)])
        if path.exists():
            return result(check_id, CheckStatus.FAIL, explanation + " Evidence exists but is invalid or unverified.", [str(path)], ai=False, human=True)
        status = CheckStatus.UNAVAILABLE if unavailable else CheckStatus.FAIL
        return result(check_id, status, explanation + " Evidence is missing.", [], ai=not unavailable, human=unavailable)
    values = [
        ev("CF-C23", "tests-pass.json", "Required tests passed."),
        ev("CF-C24", "quality-pass.json", "Supported lint and type checks passed."),
        ev("CF-C25", "secret-scan-pass.json", "Secret scan passed."),
        ev("CF-C26", "dependency-vulnerability-pass.json", "Dependency vulnerability policy passed.", True),
        ev("CF-C27", "dependency-lock-pass.json", "Dependency lock policy passed."),
        ev("CF-C28", "license-pass.json", "License policy passed."),
        ev("CF-C29", "reproducible-build-pass.json", "The build is reproducible."),
        ev("CF-C30", "diff-classification.json", "The change was classified."),
        ev("CF-C31", "human-gate.json", "Consequential-change approval exists.", True),
        ev("CF-C32", "restore-test.json", "Backup and restore evidence exists.", True),
        ev("CF-C33", "documentation-current.json", "Documentation, ownership, status, and catalog records are current."),
        ev("CF-D34", "runtime-posture.json", "Health, errors, usage, owner, and recovery metadata exists.", True),
        ev("CF-D35", "lifecycle-review.json", "Lifecycle signals were evaluated.", True),
    ]
    return values


def run_all(project_root: Path, policy: Dict[str, Any], brief: Dict[str, Any]) -> List[CheckResult]:
    return run_static(project_root, policy, brief) + run_release_evidence(project_root, policy, brief)
