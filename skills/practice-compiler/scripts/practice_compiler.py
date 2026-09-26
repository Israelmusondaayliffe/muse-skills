#!/usr/bin/env python3
"""Mine work-session JSONL into classified, redacted practice proposals.

Adapters: `muse` (Muse/Hatch transcript exports in the normalized JSONL event
schema, see references/transcript-export.md), `codex` (Codex session JSONL),
`claude` (Claude Code project JSONL). Persistent records live outside the
replaceable skill package at ~/workspace/practice-compiler/state; override with
--state-root or the PRACTICE_COMPILER_STATE environment variable. Earlier
versions wrote to the package's hidden_files/state; `state status` reports that
legacy tree and `state migrate` copies it forward without deleting it.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class CompilerError(RuntimeError):
    pass


CORRECTION_RE = re.compile(
    r"\b(no[, ]|actually\b|wrong\b|do not|don't|instead\b|only\b|avoid\b|"
    r"must\b|make sure\b|keep\b|stop\b|never\b|should\b)",
    re.I,
)
FOLLOW_UP_RE = re.compile(
    r"^\s*(also\b|and\b|then\b|next\b|after\b|before\b|once\b|now\b|"
    r"make sure\b|verify\b|update\b|do this\b|finally\b)",
    re.I,
)
COST_RE = re.compile(r"\b(cost|expensive|usage|token|budget|wast(?:e|ed|ing)\s+(?:time|work|effort|tokens?)|low[- ]value\s+tests?)\b", re.I)
MISSED_TOOL_RE = re.compile(r"\b(why (?:did you|haven't you|have you not) used|should have used|use (?:computer use|browser|chrome|image generation|figma|the tools))\b", re.I)
REPAIR_RE = re.compile(r"\b(fix|repair|broken|did not render|didn't render|wrong again|redo)\b", re.I)
USER_METHOD_RE = re.compile(r"\b(i would|this is how i|my method|the way i work|replicate (?:this|my) workflow)\b", re.I)
SYNTHETIC_PROMPT_RE = re.compile(
    r"(?i)(bounded .*verification task|from automatically injected prior-task memory only|"
    r"reply with exactly .*nothing else|reply only with done|fresh codex task verification|"
    r"do not use tools and do not read (?:any )?files)",
)
INJECTED_USER_PREFIXES = (
    "<recommended_plugins>",
    "# AGENTS.md instructions",
    "<environment_context>",
    "<app-context>",
    "<in-app-browser-context",
    "<skill>",
    "<codex_internal_context",
    "# Applications mentioned by the user:",
)
CONTENT_RE = re.compile(r"\b(article|tweet|tutorial|diagram|prompt|product idea|example|content)\b", re.I)
CONFIG_RE = re.compile(r"\b(config|setting|permission|environment variable|default|\.env)\b", re.I)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
SESSION_ID_RE = re.compile(r"\b[0-9a-f]{8}-[0-9a-f-]{20,}\b", re.I)
PATH_RE = re.compile(r"(?:/[A-Za-z0-9._ -]+){2,}")
URL_RE = re.compile(r"https?://\S+")
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{6,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"(?i)\b(bearer)\s+[A-Za-z0-9._~+/-]{8,}"),
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"(?i)\b[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|PASSWORD)\s*=\s*[^\s,;]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
]
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "before", "but", "by", "can",
    "do", "for", "from", "i", "in", "is", "it", "my", "of", "on", "or", "our",
    "please", "should", "so", "that", "the", "then", "this", "to", "use", "we",
    "with", "you", "your",
}
ALLOWED_SOURCE_CLASSES = {"user", "automation", "subagent", "synthetic"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def scan_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


SKILL_DIR = Path(__file__).resolve().parent.parent
STATE_ENV = "PRACTICE_COMPILER_STATE"
LEGACY_ENV = "PRACTICE_COMPILER_LEGACY_STATE"
MIGRATION_MARKER = "migrated-from.json"
IGNORED_STATE_FILES = {MIGRATION_MARKER, ".state.lock"}


def default_state_root() -> Path:
    """User state lives outside the replaceable skill package."""
    return (Path.home() / "workspace" / "practice-compiler" / "state").resolve()


def legacy_state_roots() -> list[Path]:
    """In-package state roots written by earlier versions. Read only; never deleted."""
    override = os.environ.get(LEGACY_ENV)
    if override:
        return [Path(override).expanduser().resolve()]
    candidates = [
        SKILL_DIR / "hidden_files" / "state",
        Path.home() / "workspace" / "skills" / "practice-compiler" / "hidden_files" / "state",
    ]
    unique: list[Path] = []
    for item in candidates:
        resolved = item.resolve()
        if resolved not in unique:
            unique.append(resolved)
    return unique


def state_files(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(
        path for path in root.rglob("*")
        if path.is_file() and path.relative_to(root).parts[0] not in IGNORED_STATE_FILES
    )


def tree_digest(root: Path) -> str | None:
    """Content hash of a state tree, or None when it holds no records."""
    files = state_files(root)
    if not files:
        return None
    digest = hashlib.sha256()
    for path in files:
        digest.update(str(path.relative_to(root)).encode("utf-8") + b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def state_status() -> dict[str, Any]:
    """Report the active default state root, legacy roots, and any needed action."""
    current = default_state_root()
    current_digest = tree_digest(current)
    marker = load_json(current / MIGRATION_MARKER, {}) if (current / MIGRATION_MARKER).is_file() else {}
    legacy = []
    for root in legacy_state_roots():
        digest = tree_digest(root)
        if digest is None:
            continue
        migrated = digest == current_digest or (
            marker.get("legacy_path") == str(root) and marker.get("legacy_digest") == digest
        )
        legacy.append({"path": str(root), "digest": digest, "migrated": migrated})
    pending = [item for item in legacy if not item["migrated"]]
    result: dict[str, Any] = {
        "state_root": str(current),
        "state_has_records": current_digest is not None,
        "legacy_roots": legacy,
    }
    if current_digest is not None and pending:
        result["active"] = str(current)
        result["action"] = "conflict"
        result["detail"] = (
            "state and legacy records differ; reads use the state root, persistent writes are refused "
            "until the user picks one root with --state-root. Nothing was merged, overwritten, or deleted."
        )
    elif current_digest is not None:
        result["active"] = str(current)
        result["action"] = "none"
    elif len(pending) == 1:
        result["active"] = pending[0]["path"]
        result["action"] = "migrate"
        result["detail"] = "run: python3 scripts/practice_compiler.py state migrate"
    elif pending:
        result["active"] = None
        result["action"] = "conflict"
        result["detail"] = "several legacy roots hold different records; run state migrate --from <path> for the one to keep"
    else:
        result["active"] = str(current)
        result["action"] = "none"
    return result


def root_path(explicit: str | None, write: bool = False) -> Path:
    """Resolve the state root: --state-root, then PRACTICE_COMPILER_STATE, then the default.

    With the default root, legacy in-package state is honored: reads use it until it is
    migrated, and persistent writes refuse to fork or overwrite it.
    """
    if explicit:
        return Path(explicit).expanduser().resolve()
    state_home = os.environ.get(STATE_ENV)
    if state_home:
        return Path(state_home).expanduser().resolve()
    status = state_status()
    if status["action"] == "none":
        return default_state_root()
    if write:
        raise CompilerError(
            f"state needs attention before writing ({status['action']}): "
            f"{status.get('detail', '')} Legacy roots: {[item['path'] for item in status['legacy_roots']]}"
        )
    return Path(status["active"]) if status["active"] else default_state_root()


def cmd_state(args: argparse.Namespace) -> dict[str, Any]:
    if args.state_command == "status":
        return state_status()
    return migrate_state(getattr(args, "source", None))


def migrate_state(source: str | None = None) -> dict[str, Any]:
    """Copy one legacy state tree to the default root. Never deletes or overwrites."""
    target = default_state_root()
    if source:
        legacy = Path(source).expanduser().resolve()
    else:
        pending = [item for item in state_status()["legacy_roots"] if not item["migrated"]]
        if not pending:
            return {"migrated": False, "reason": "no unmigrated legacy state", "state_root": str(target)}
        if len(pending) > 1:
            raise CompilerError("several legacy roots differ; pass --from <path> to choose one")
        legacy = Path(pending[0]["path"])
    legacy_digest = tree_digest(legacy)
    if legacy_digest is None:
        return {"migrated": False, "reason": f"no legacy records at {legacy}", "state_root": str(target)}
    if target.is_symlink():
        raise CompilerError(f"state root is a symlink; refusing to write through it: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target.parent / ".state.lock", "a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        current_digest = tree_digest(target)
        if current_digest is not None and current_digest != legacy_digest:
            raise CompilerError(
                f"state root already holds different records; nothing overwritten: {target} (legacy kept at {legacy})"
            )
        if current_digest is None:
            staging = Path(tempfile.mkdtemp(prefix=".state.migrating.", dir=target.parent))
            for path in state_files(legacy):
                destination = staging / path.relative_to(legacy)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
            if tree_digest(staging) != legacy_digest:
                raise CompilerError(f"copy verification failed; staged copy left at {staging}")
            try:
                os.rename(staging, target)  # fails if a non-empty state root appeared meanwhile
            except OSError as error:
                raise CompilerError(f"state root changed during migration; staged copy left at {staging}: {error}") from error
        atomic_json(target / MIGRATION_MARKER, {
            "legacy_path": str(legacy), "legacy_digest": legacy_digest, "migrated_at": now(),
        })
    return {
        "migrated": current_digest is None,
        "reason": "copied" if current_digest is None else "already identical; marker recorded",
        "state_root": str(target),
        "legacy_path_kept": str(legacy),
        "sha256": legacy_digest,
    }


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temporary = handle.name
    os.replace(temporary, path)


def append_jsonl(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists() and default is not None:
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CompilerError(f"cannot read valid JSON from {path}: {error}") from error


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def redact(text: str) -> str:
    result = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    for pattern in SECRET_PATTERNS:
        result = pattern.sub("[REDACTED_SECRET]", result)
    return result[:600]


def walk(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def text_values(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            if key in {"content", "text", "message", "output", "input_text"}:
                yield from text_values(child)
            elif isinstance(child, (dict, list)):
                yield from text_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from text_values(child)


def parse_arguments(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}


def normalized_command(command: str) -> str:
    value = re.sub(r"\s+", " ", command.strip())
    value = SESSION_ID_RE.sub("<session>", value)
    value = PATH_RE.sub("<path>", value)
    return value[:300]


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def parse_boundary(value: str | None, *, end: bool = False, timezone_name: str = "UTC") -> datetime | None:
    if not value:
        return None
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            day = date.fromisoformat(value)
            try:
                local_zone = ZoneInfo(timezone_name)
            except ZoneInfoNotFoundError as error:
                raise CompilerError(f"unknown timezone: {timezone_name}") from error
            return datetime.combine(day, time.max if end else time.min, tzinfo=local_zone).astimezone(timezone.utc)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.replace(tzinfo=parsed.tzinfo or timezone.utc).astimezone(timezone.utc)
    except ValueError as error:
        raise CompilerError(f"invalid date or timestamp: {value}") from error


def direct_user_text(event: dict[str, Any]) -> list[str]:
    """Return only top-level user-authored content, never recursively injected context."""
    kind = str(event.get("type", "")).lower()
    payload = event.get("payload")
    candidates: list[Any] = []
    if kind in {"user_message", "user"}:
        candidates.append(payload if payload is not None else event)
    elif kind == "response_item" and isinstance(payload, dict):
        if str(payload.get("role", "")).lower() == "user" or str(payload.get("type", "")).lower() in {
            "user_message", "user"
        }:
            candidates.append(payload.get("content") or payload.get("text") or payload.get("message"))
    result: list[str] = []
    for value in candidates:
        for text in text_values(value):
            cleaned = text.strip()
            if not cleaned or cleaned.startswith(INJECTED_USER_PREFIXES):
                continue
            result.append(cleaned)
    return result


def session_metadata(path: Path, adapter: str = "codex") -> tuple[dict[str, Any], list[str]]:
    metadata = {
        "session_id": path.stem,
        "thread_source": "unknown",
        "source_class": "synthetic" if any(part in {"fixture", "fixtures", "test", "tests", "tmp"} for part in path.parts) else "user",
        "timestamp": None,
    }
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as error:
        return metadata, [f"{path}: {error}"]
    if adapter == "claude" and "subagents" in path.parts:
        metadata["source_class"] = "subagent"
        metadata["thread_source"] = "subagent"
    saw_session_meta = False
    for number, raw in enumerate(lines if adapter == "claude" else lines[:80], start=1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as error:
            errors.append(f"{path}:{number}: {error}")
            continue
        if adapter == "claude" and (event.get("isSidechain") is True or event.get("agentId")):
            metadata["source_class"] = "subagent"
            metadata["thread_source"] = "subagent"
        timestamp = parse_timestamp(event.get("timestamp"))
        if timestamp and metadata["timestamp"] is None:
            metadata["timestamp"] = timestamp
        if adapter in {"codex", "muse"} and event.get("type") == "session_meta" and isinstance(event.get("payload"), dict):
            payload = event["payload"]
            metadata["session_id"] = str(payload.get("id") or payload.get("session_id") or metadata["session_id"])
            metadata["thread_source"] = str(payload.get("thread_source") or "unknown").lower()
            meta_timestamp = parse_timestamp(payload.get("timestamp"))
            if meta_timestamp:
                metadata["timestamp"] = meta_timestamp
            source = metadata["thread_source"]
            if source in {"automation", "scheduled", "cron"}:
                metadata["source_class"] = "automation"
            elif source in {"subagent", "agent", "delegate"}:
                metadata["source_class"] = "subagent"
            elif source in {"synthetic", "eval", "test", "verification"}:
                metadata["source_class"] = "synthetic"
            elif metadata["source_class"] != "synthetic":
                metadata["source_class"] = "user"
            saw_session_meta = True
        if metadata["source_class"] == "user":
            authored = direct_user_text(event)
            if authored and SYNTHETIC_PROMPT_RE.search(authored[0]):
                metadata["source_class"] = "synthetic"
                break
        if saw_session_meta and metadata["source_class"] in {"automation", "subagent"}:
            break
    if metadata["timestamp"] is None:
        metadata["timestamp"] = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return metadata, errors


def semantic_tokens(text: str) -> set[str]:
    normalized = redact(text).lower()
    normalized = URL_RE.sub(" url ", normalized)
    normalized = SESSION_ID_RE.sub(" session ", normalized)
    normalized = PATH_RE.sub(" path ", normalized)
    normalized = re.sub(r"\b\d+\b", " number ", normalized)
    words = re.findall(r"[a-z][a-z0-9-]{1,}", normalized)
    return {word[:-1] if word.endswith("s") and len(word) > 4 else word for word in words if word not in STOPWORDS}


def semantic_key(text: str) -> str:
    tokens = sorted(semantic_tokens(text))
    return " ".join(tokens[:18]) or re.sub(r"\s+", " ", redact(text).lower())[:180]


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def signal(
    kind: str,
    source: Path,
    line: int,
    evidence: str,
    key: str,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    details = metadata or {}
    fingerprint = hashlib.sha256(f"{kind}\0{key}".encode()).hexdigest()[:20]
    return {
        "schema_version": 2,
        "signal_id": fingerprint,
        "kind": kind,
        "fingerprint": fingerprint,
        "semantic_key": key,
        "source": str(source),
        "session_id": details.get("session_id", source.stem),
        "line": line,
        "evidence": redact(evidence),
        "citation": f"{details.get('session_id', source.stem)}:{line}",
        "metadata": details,
    }


def classify_user_signal(text: str, prior_user_messages: int) -> str:
    if COST_RE.search(text):
        return "cost-decision"
    if MISSED_TOOL_RE.search(text):
        return "missed-tool"
    if USER_METHOD_RE.search(text):
        return "user-method"
    if REPAIR_RE.search(text) and prior_user_messages:
        return "repeated-repair"
    if CORRECTION_RE.search(text):
        return "recurring-feedback"
    if prior_user_messages:
        return "follow-up-instruction"
    return "repeated-task"


def extract_signals(path: Path, adapter: str = "codex") -> tuple[list[dict[str, Any]], list[str]]:
    signals: list[dict[str, Any]] = []
    metadata, errors = session_metadata(path, adapter)
    evidence_metadata = {
        **metadata,
        "timestamp": metadata["timestamp"].isoformat() if isinstance(metadata.get("timestamp"), datetime) else metadata.get("timestamp"),
    }
    commands: list[tuple[int, str, str]] = []
    outputs: list[tuple[int, str]] = []
    prior_user_messages = 0
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as error:
        return [], errors + [f"{path}: {error}"]
    for number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as error:
            errors.append(f"{path}:{number}: {error}")
            continue
        for text in direct_user_text(event):
            kind = classify_user_signal(text, prior_user_messages)
            details = {**evidence_metadata, "content_clue": bool(CONTENT_RE.search(text)), "config_clue": bool(CONFIG_RE.search(text))}
            signals.append(signal(kind, path, number, text, semantic_key(text), details))
            prior_user_messages += 1
        for obj in walk(event):
            call_kind = str(obj.get("type", "")).lower()
            name = obj.get("name") or obj.get("tool_name")
            if call_kind in {"function_call", "tool_call", "custom_tool_call"} and isinstance(name, str):
                arguments = parse_arguments(obj.get("arguments") or obj.get("input") or obj.get("args"))
                command = arguments.get("cmd") or arguments.get("command")
                if isinstance(command, str) and command.strip():
                    commands.append((number, name, normalized_command(command)))
            if call_kind in {"function_call_output", "tool_result", "tool_output"}:
                outputs.extend((number, text) for text in text_values(obj))
            exit_code = obj.get("exit_code")
            if isinstance(exit_code, int) and exit_code != 0:
                outputs.append((number, json.dumps(obj, sort_keys=True)))
    for number, name, command in commands:
        signals.append(signal("executed-command", path, number, command, command, {**evidence_metadata, "tool": name, "command": command}))
    for number, output in outputs:
        if re.search(r"(?i)(exit[_ ]?code\s*[:=]?\s*[1-9]|error|failed|unknown flag|command not found)", output):
            key = re.sub(r"\d+", "N", redact(output).lower())[:180]
            signals.append(signal("command-failure", path, number, output, key, evidence_metadata))
    return signals, errors


def cluster_signals(signals: list[dict[str, Any]], threshold: float = 0.5) -> list[list[dict[str, Any]]]:
    clusters: list[list[dict[str, Any]]] = []
    for item in signals:
        tokens = semantic_tokens(item["semantic_key"])
        destination: list[dict[str, Any]] | None = None
        for candidate in clusters:
            if candidate[0]["kind"] != item["kind"]:
                continue
            representative = semantic_tokens(candidate[0]["semantic_key"])
            if jaccard(tokens, representative) >= threshold:
                destination = candidate
                break
        if destination is None:
            clusters.append([item])
        else:
            destination.append(item)
    return clusters


def proposal_destination(kind: str, items: list[dict[str, Any]]) -> str:
    if any(item["metadata"].get("content_clue") for item in items):
        return "content"
    if any(item["metadata"].get("config_clue") for item in items):
        return "agents-md"
    if kind == "command-failure":
        return "tool-cli"
    return "skill"


def build_proposals(signals: list[dict[str, Any]], min_occurrences: int) -> list[dict[str, Any]]:
    candidates = [item for item in signals if item["kind"] != "executed-command"]
    command_sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in signals:
        if item["kind"] == "executed-command":
            command_sessions[item["metadata"].get("command", "")].append(item)
    for command, items in command_sessions.items():
        unique = {item["session_id"] for item in items}
        if len(unique) >= min_occurrences:
            for item in items:
                candidates.append({**item, "kind": "repeated-task", "semantic_key": f"command {command}"})
    proposals: list[dict[str, Any]] = []
    for items in cluster_signals(candidates):
        if any(item["metadata"].get("source_class") != "design-export" for item in items):
            items = [item for item in items if item["metadata"].get("source_class") != "design-export"]
        sessions = {item["session_id"] for item in items}
        if len(sessions) < min_occurrences:
            continue
        kind = items[0]["kind"]
        key = items[0]["semantic_key"]
        fingerprint = hashlib.sha256(f"{kind}\0{key}".encode()).hexdigest()[:20]
        destination = proposal_destination(kind, items)
        evidence = [
            {
                "session_id": item["session_id"],
                "source": item["source"],
                "line": item["line"],
                "citation": item["citation"],
                "snippet": item["evidence"],
                "source_class": item["metadata"].get("source_class"),
            }
            for item in items[:8]
        ]
        proposals.append({
            "schema_version": 2,
            "proposal_id": f"pc-{fingerprint}",
            "fingerprint": fingerprint,
            "signal_class": kind,
            "kind": kind,
            "destination": destination,
            "summary": f"Review repeated {kind.replace('-', ' ')} evidence for a possible {destination} improvement.",
            "occurrences": len(sessions),
            "confidence": "high" if len(sessions) >= 3 else "medium",
            "evidence": evidence,
            "status": "staged",
            "created_at": now(),
        })
    return sorted(proposals, key=lambda item: (-item["occurrences"], item["proposal_id"]))


DESIGN_EXPORT_KINDS = {
    "feedback": "recurring-feedback",
    "friction": "recurring-feedback",
    "repair": "repeated-repair",
    "missed-tool": "missed-tool",
    "cost-decision": "cost-decision",
    "user-method": "user-method",
}


def design_export_signals(payload: Any, since: datetime, until: datetime) -> list[dict[str, Any]]:
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        raise CompilerError("Design export must be a schema_version 1.0 object")
    records = payload.get("records")
    if not isinstance(records, list):
        raise CompilerError("Design export records must be a list")
    signals: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("source_type") != "design-neutral-export":
            raise CompilerError(f"Design export record {index} has an invalid source type")
        forbidden = {"exact_quote", "path", "source_path", "event_path"}.intersection(record)
        if forbidden:
            raise CompilerError(f"Design export record {index} contains forbidden raw fields: {', '.join(sorted(forbidden))}")
        export_fingerprint = record.get("fingerprint")
        if not isinstance(export_fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", export_fingerprint):
            raise CompilerError(f"Design export record {index} has an invalid fingerprint")
        if export_fingerprint in seen:
            continue
        seen.add(export_fingerprint)
        created = parse_timestamp(record.get("created_at"))
        if created is None:
            raise CompilerError(f"Design export record {index} has an invalid created_at")
        if not since <= created <= until:
            continue
        project_id = record.get("project_id")
        if not isinstance(project_id, str) or not re.fullmatch(r"project-[0-9a-f]{20}", project_id):
            raise CompilerError(f"Design export record {index} has an invalid opaque project_id")
        source_kind = record.get("signal_class")
        if source_kind not in DESIGN_EXPORT_KINDS:
            raise CompilerError(f"Design export record {index} has an invalid signal class")
        summary = record.get("summary")
        if not isinstance(summary, str) or not summary.strip():
            raise CompilerError(f"Design export record {index} requires a summary")
        evidence = " ".join(str(value) for value in (summary, record.get("impact"), record.get("method")) if value)
        kind = DESIGN_EXPORT_KINDS[source_kind]
        signals.append(signal(
            kind,
            Path("design-neutral-export"),
            index + 1,
            evidence,
            semantic_key(evidence),
            {
                "session_id": project_id,
                "source_class": "design-export",
                "timestamp": created.isoformat(),
                "design_export_fingerprint": export_fingerprint,
            },
        ))
    return signals


def cmd_ingest_design(args: argparse.Namespace) -> dict[str, Any]:
    timezone_name = getattr(args, "timezone", None) or os.environ.get("TZ") or "UTC"
    since = parse_boundary(args.since, timezone_name=timezone_name)
    until = parse_boundary(args.until, end=True, timezone_name=timezone_name)
    if since is None or until is None:
        raise CompilerError("Design export intake requires --since and --until")
    if since > until:
        raise CompilerError("--since must be earlier than or equal to --until")
    payload = load_json(Path(args.input).expanduser().resolve())
    incoming = design_export_signals(payload, since, until)
    root = root_path(args.state_root, write=not args.stdout)
    if args.stdout:
        return {"mode": "stdout", "signals": len(incoming), "proposal_records": build_proposals(incoming, args.min_occurrences)}
    registry_path = root / "signal-registry.json"
    registry = load_json(registry_path, {"schema_version": 2, "signals": []})
    merged: dict[tuple[str, str, int, str], dict[str, Any]] = {}
    for item in list(registry.get("signals", [])) + incoming:
        key = (item["kind"], item["session_id"], item["line"], item["fingerprint"])
        merged[key] = item
    all_signals = list(merged.values())
    proposals = build_proposals(all_signals, args.min_occurrences)
    atomic_json(registry_path, {"schema_version": 2, "updated_at": now(), "signal_count": len(all_signals), "signals": all_signals})
    proposal_registry = merge_registry(root, proposals)
    for proposal in proposals:
        path = root / "proposals" / f"{proposal['proposal_id']}.json"
        if path.exists():
            existing = load_json(path)
            proposal["status"] = existing.get("status", proposal["status"])
        atomic_json(path, proposal)
    return {"mode": "persistent", "signals": len(incoming), "proposals": len(proposals), "registry_entries": len(proposal_registry["proposals"])}


def session_roots(args: argparse.Namespace) -> list[Path]:
    values = getattr(args, "sessions_root", None)
    if not values:
        raise CompilerError("scan requires at least one explicit --sessions-root")
    return [Path(item).expanduser().resolve() for item in values]


def select_files(args: argparse.Namespace) -> tuple[list[tuple[Path, dict[str, Any]]], dict[str, int], list[str]]:
    timezone_name = getattr(args, "timezone", None) or os.environ.get("TZ") or "UTC"
    since = parse_boundary(getattr(args, "since", None), timezone_name=timezone_name)
    until = parse_boundary(getattr(args, "until", None), end=True, timezone_name=timezone_name)
    if since and until and since > until:
        raise CompilerError("--since must be earlier than or equal to --until")
    classes = set(getattr(args, "source_class", None) or ["user"])
    unknown = classes - ALLOWED_SOURCE_CLASSES
    if unknown:
        raise CompilerError(f"unknown source class: {', '.join(sorted(unknown))}")
    discovered: list[tuple[Path, dict[str, Any]]] = []
    counts: Counter[str] = Counter()
    errors: list[str] = []
    for source_root in session_roots(args):
        if not source_root.exists():
            continue
        for path in source_root.rglob("*.jsonl"):
            metadata, found_errors = session_metadata(path, getattr(args, "adapter", "codex"))
            errors.extend(found_errors)
            timestamp = metadata["timestamp"]
            if since and timestamp < since:
                continue
            if until and timestamp > until:
                continue
            counts[metadata["source_class"]] += 1
            if metadata["source_class"] not in classes:
                continue
            discovered.append((path, metadata))
    discovered.sort(key=lambda item: item[1]["timestamp"], reverse=True)
    limit = getattr(args, "limit", 20)
    return discovered[:limit], dict(sorted(counts.items())), errors


def merge_registry(root: Path, proposals: list[dict[str, Any]]) -> dict[str, Any]:
    registry_path = root / "proposal-registry.json"
    registry = load_json(registry_path, {"schema_version": 2, "proposals": {}})
    entries = registry.setdefault("proposals", {})
    for proposal in proposals:
        proposal_id = proposal["proposal_id"]
        entry = entries.get(proposal_id, {})
        entries[proposal_id] = {
            "fingerprint": proposal["fingerprint"],
            "signal_class": proposal["signal_class"],
            "first_seen": entry.get("first_seen", proposal["created_at"]),
            "last_seen": proposal["created_at"],
            "status": entry.get("status", proposal["status"]),
            "occurrences": max(entry.get("occurrences", 0), proposal["occurrences"]),
        }
    registry["updated_at"] = now()
    atomic_json(registry_path, registry)
    return registry


def cmd_scan(args: argparse.Namespace) -> dict[str, Any]:
    selected_files, classification_counts, selection_errors = select_files(args)
    stdout_only = bool(getattr(args, "stdout", False))
    root = root_path(getattr(args, "state_root", None), write=not stdout_only)
    cursor_path = root / "cursor.json"
    cursor = {"schema_version": 2, "processed": {}} if stdout_only else load_json(cursor_path, {"schema_version": 2, "processed": {}})
    processed = cursor.setdefault("processed", {})
    selected: list[tuple[Path, str]] = []
    skipped = 0
    for path, _metadata in selected_files:
        digest = file_hash(path)
        if not stdout_only and processed.get(str(path)) == digest:
            skipped += 1
        else:
            selected.append((path, digest))
    sid = getattr(args, "scan_id", None) or scan_id()
    signals: list[dict[str, Any]] = []
    errors = list(selection_errors)
    for path, digest in selected:
        found, found_errors = extract_signals(path, getattr(args, "adapter", "codex"))
        signals.extend(found)
        errors.extend(found_errors)
        if not stdout_only:
            processed[str(path)] = digest
    analysis_signals = signals
    signal_registry: dict[str, Any] | None = None
    if not stdout_only:
        signal_registry_path = root / "signal-registry.json"
        signal_registry = load_json(signal_registry_path, {"schema_version": 2, "signals": []})
        merged: dict[tuple[str, str, int, str], dict[str, Any]] = {}
        for item in list(signal_registry.get("signals", [])) + signals:
            key = (item["kind"], item["session_id"], item["line"], item["fingerprint"])
            merged[key] = item
        analysis_signals = list(merged.values())
        signal_registry = {
            "schema_version": 2,
            "updated_at": now(),
            "signal_count": len(analysis_signals),
            "signals": analysis_signals,
        }
    proposals = build_proposals(analysis_signals, getattr(args, "min_occurrences", 2))
    errors = list(dict.fromkeys(errors))
    summary = {
        "schema_version": 2,
        "scan_id": sid,
        "mode": "stdout" if stdout_only else "persistent",
        "files_considered": len(selected_files),
        "files_processed": len(selected),
        "files_skipped": skipped,
        "signals": len(signals),
        "signal_counts": dict(sorted(Counter(item["kind"] for item in signals).items())),
        "proposals": len(proposals),
        "source_class_counts": classification_counts,
        "selected_source_classes": sorted(set(getattr(args, "source_class", None) or ["user"])),
        "date_window": {
            "since": getattr(args, "since", None),
            "until": getattr(args, "until", None),
            "timezone": getattr(args, "timezone", None) or os.environ.get("TZ") or "UTC",
        },
        "errors": errors,
        "source_roots": [str(item) for item in session_roots(args)],
        "created_at": now(),
    }
    if stdout_only:
        return {**summary, "proposal_records": proposals, "signal_records": signals}
    scan_directory = root / "scans" / sid
    if scan_directory.exists():
        raise CompilerError(f"scan already exists: {sid}")
    for item in signals:
        append_jsonl(scan_directory / "signals.jsonl", item)
    if signal_registry is not None:
        atomic_json(root / "signal-registry.json", signal_registry)
    registry = merge_registry(root, proposals)
    for proposal in proposals:
        proposal_path = root / "proposals" / f"{proposal['proposal_id']}.json"
        if proposal_path.exists():
            existing = load_json(proposal_path)
            status = existing.get("status", "staged")
            citations = {item.get("citation") for item in existing.get("evidence", []) if isinstance(item, dict)}
            proposal["evidence"] = existing.get("evidence", []) + [
                item for item in proposal["evidence"] if item.get("citation") not in citations
            ]
            proposal["evidence"] = proposal["evidence"][:12]
            proposal["status"] = status
            proposal["occurrences"] = max(existing.get("occurrences", 0), proposal["occurrences"])
        atomic_json(proposal_path, proposal)
    atomic_json(scan_directory / "summary.json", summary)
    cursor.update({"schema_version": 2, "updated_at": now(), "last_scan_id": sid})
    atomic_json(cursor_path, cursor)
    summary["registry_entries"] = len(registry["proposals"])
    return summary


def read_proposals(root: Path) -> list[dict[str, Any]]:
    directory = root / "proposals"
    if not directory.exists():
        return []
    return [load_json(path) for path in sorted(directory.glob("*.json"))]


def cmd_report(args: argparse.Namespace) -> dict[str, Any]:
    root = root_path(args.state_root)
    proposals = read_proposals(root)
    counts = Counter(item.get("status", "unknown") for item in proposals)
    result = {"state_root": str(root), "proposal_count": len(proposals), "status_counts": dict(counts), "proposals": proposals}
    if not args.state_root and not os.environ.get(STATE_ENV):
        status = state_status()
        if status["action"] != "none":
            result["state_notice"] = {"action": status["action"], "detail": status.get("detail")}
    return result


def preferred_handoff_owner(destination: str) -> str | None:
    """Preferred Hatch workspace-skill owner for a proposal destination.

    Preferred, not required: select only when the caller confirms the owner is
    available; otherwise the handoff stays generic with an unassigned owner.
    """
    return {
        "skill": "capability-operator",
        "new-skill": "skill-creator",
        "agents-md": "harness-engineering",
        "hook": "harness-engineering",
        "tool-cli": "harness-engineering",
        "config": "harness-engineering",
        "durable-knowledge": "continuity-vault",
        "content": "user-content-backlog",
        "discard": None,
    }.get(destination)


def cmd_decide(args: argparse.Namespace) -> dict[str, Any]:
    root = root_path(args.state_root, write=True)
    proposal_path = root / "proposals" / f"{args.proposal_id}.json"
    proposal = load_json(proposal_path)
    decision = {
        "schema_version": 2,
        "proposal_id": args.proposal_id,
        "decision": args.decision,
        "note": args.note or "",
        "decided_at": now(),
    }
    append_jsonl(root / "decisions.jsonl", decision)
    proposal["status"] = {"approve": "approved", "reject": "rejected", "defer": "staged"}[args.decision]
    proposal["last_decision"] = decision
    atomic_json(proposal_path, proposal)
    registry_path = root / "proposal-registry.json"
    registry = load_json(registry_path, {"schema_version": 2, "proposals": {}})
    if args.proposal_id in registry.get("proposals", {}):
        registry["proposals"][args.proposal_id]["status"] = proposal["status"]
        registry["updated_at"] = now()
        atomic_json(registry_path, registry)
    handoff_path = None
    preferred_owner = None
    selected_owner = None
    routing_mode = None
    if args.decision == "approve":
        destination = proposal.get("destination", "")
        preferred_owner = preferred_handoff_owner(destination)
        available_owners = set(getattr(args, "available_owner", None) or [])
        selected_owner = preferred_owner if preferred_owner in available_owners else None
        routing_mode = "preferred" if selected_owner else "generic"
        if destination != "discard":
            evidence_references = [
                {
                    "session_id": item.get("session_id"),
                    "source": item.get("source"),
                    "line": item.get("line"),
                    "citation": item.get("citation"),
                    "source_class": item.get("source_class"),
                    "snippet": item.get("snippet"),
                }
                for item in proposal.get("evidence", [])
                if isinstance(item, dict)
            ]
            handoff = {
                "schema_version": 2,
                "proposal_id": args.proposal_id,
                "routing_mode": routing_mode,
                "preferred_owner": preferred_owner,
                "selected_owner": selected_owner,
                "requested_outcome": proposal.get("summary"),
                "destination_class": destination,
                "evidence_references": evidence_references,
                "occurrence_count": proposal.get("occurrences"),
                "decision_note": args.note or "",
                "authority_boundary": (
                    "This approval authorizes the handoff record only. It does not authorize "
                    "source edits, publication, external messages, hooks, configuration changes, "
                    "or promotion."
                ),
                "required_next_proof": (
                    "The receiving owner must inspect the current destination, prove the proposed "
                    "scope and tests, and obtain any approval required before mutation."
                ),
                "created_at": now(),
            }
            handoff_path = root / "handoffs" / f"{args.proposal_id}.json"
            atomic_json(handoff_path, handoff)
    return {
        "proposal_id": args.proposal_id,
        "status": proposal["status"],
        "routing_mode": routing_mode,
        "preferred_owner": preferred_owner,
        "selected_owner": selected_owner,
        "handoff": str(handoff_path) if handoff_path else None,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    scan = sub.add_parser("scan")
    scan.add_argument("--sessions-root", action="append", required=True)
    scan.add_argument("--adapter", choices=["muse", "codex", "claude"], required=True)
    scan.add_argument("--limit", type=int, default=20)
    scan.add_argument("--min-occurrences", type=int, default=2)
    scan.add_argument("--since", help="inclusive ISO date or timestamp")
    scan.add_argument("--until", help="inclusive ISO date or timestamp")
    scan.add_argument("--timezone", default=os.environ.get("TZ") or "UTC", help="IANA timezone for date-only boundaries")
    scan.add_argument("--source-class", action="append", choices=sorted(ALLOWED_SOURCE_CLASSES))
    scan.add_argument("--stdout", action="store_true", help="emit records without writing state or cursor files")
    scan.add_argument("--scan-id")
    scan.add_argument("--state-root")
    scan.set_defaults(func=cmd_scan)
    design = sub.add_parser("ingest-design-export")
    design.add_argument("--input", required=True)
    design.add_argument("--since", required=True)
    design.add_argument("--until", required=True)
    design.add_argument("--timezone", default=os.environ.get("TZ") or "UTC")
    design.add_argument("--min-occurrences", type=int, default=2)
    design.add_argument("--state-root")
    design.add_argument("--stdout", action="store_true")
    design.set_defaults(func=cmd_ingest_design)
    report = sub.add_parser("report")
    report.add_argument("--state-root")
    report.set_defaults(func=cmd_report)
    decide = sub.add_parser("decide")
    decide.add_argument("proposal_id")
    decide.add_argument("decision", choices=["approve", "reject", "defer"])
    decide.add_argument("--note")
    decide.add_argument("--available-owner", action="append", help="confirmed available preferred owner")
    decide.add_argument("--state-root")
    decide.set_defaults(func=cmd_decide)
    state = sub.add_parser("state", help="report or migrate legacy in-package state")
    state_sub = state.add_subparsers(dest="state_command", required=True)
    state_sub.add_parser("status", help="show the active state root and any legacy records")
    migrate = state_sub.add_parser("migrate", help="copy legacy state to the default root; never deletes or overwrites")
    migrate.add_argument("--from", dest="source", help="legacy state root to migrate when several exist")
    state.set_defaults(func=cmd_state)
    return result


def main() -> int:
    args = parser().parse_args()
    if args.command == "scan" and (not args.since or not args.until):
        print(json.dumps({"ok": False, "error": "scan requires an exact --since and --until window"}), file=sys.stderr)
        return 1
    if getattr(args, "limit", 1) <= 0 or getattr(args, "min_occurrences", 1) <= 0:
        print(json.dumps({"ok": False, "error": "limit and min-occurrences must be positive"}), file=sys.stderr)
        return 1
    try:
        payload = args.func(args)
    except CompilerError as error:
        print(json.dumps({"ok": False, "error": str(error)}), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, **payload}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
