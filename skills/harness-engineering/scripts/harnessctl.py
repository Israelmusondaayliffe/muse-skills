#!/usr/bin/env python3
"""Local create/update operations. No network, shell execution, or host configuration probes.

Adapted from the public MIT Harness Engineering helper. Approval flags record an
approval already given by the user; they do not grant authority. Single writer only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any, Iterable


SCHEMA_VERSION = 1
PROFILE_REQUIRED = {"schema_version", "user", "scope", "decisions"}
PLAN_REQUIRED = {
    "schema_version",
    "run_id",
    "allowed_roots",
    "approval_groups",
    "outcome",
    "resource_budget",
    "support_artifacts",
    "operations",
}
SECRET_KEY = re.compile(r"(?i)(token|secret|password|cookie|credential|authorization|api[_-]?key)")
PLACEHOLDERS = ("replace-me", "__REPLACE_ME__")


def is_placeholder(value: Any) -> bool:
    return isinstance(value, str) and any(mark.lower() in value.lower() for mark in PLACEHOLDERS)


class HarnessError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot read valid JSON from {path}: {exc}") from exc


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    atomic_write(path, data.encode("utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def check_target(target: Path, allowed_roots: Iterable[Path]) -> Path:
    if not target.is_absolute():
        raise HarnessError(f"target must be absolute: {target}")
    for ancestor in (target, *target.parents):
        if ancestor.is_symlink():
            raise HarnessError(f"symbolic-link path is not allowed: {ancestor}")
    resolved = target.resolve(strict=False)
    root_pairs = [(root.expanduser(), root.expanduser().resolve(strict=False)) for root in allowed_roots]
    matches = [(original, normalized) for original, normalized in root_pairs if is_within(resolved, normalized)]
    if not matches:
        raise HarnessError(f"target is outside approved roots: {target}")
    original_root, _ = max(matches, key=lambda pair: len(pair[1].parts))
    try:
        relative = target.relative_to(original_root)
    except ValueError:
        relative = resolved.relative_to(original_root.resolve(strict=False))
        original_root = original_root.resolve(strict=False)
    current = original_root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise HarnessError(f"symbolic-link target is not allowed: {current}")
    return resolved


def validate_profile(data: Any) -> None:
    if not isinstance(data, dict) or not PROFILE_REQUIRED.issubset(data):
        missing = sorted(PROFILE_REQUIRED - set(data if isinstance(data, dict) else {}))
        raise HarnessError(f"profile missing required fields: {', '.join(missing)}")
    if data["schema_version"] != SCHEMA_VERSION:
        raise HarnessError("unsupported profile schema_version")
    if not isinstance(data["user"], dict) or not isinstance(data["scope"], dict):
        raise HarnessError("profile user and scope must be objects")
    if not isinstance(data["decisions"], list):
        raise HarnessError("profile decisions must be an array")


def validate_operations(data: Any) -> None:
    if not isinstance(data, dict) or not PLAN_REQUIRED.issubset(data):
        missing = sorted(PLAN_REQUIRED - set(data if isinstance(data, dict) else {}))
        raise HarnessError(f"operations plan missing required fields: {', '.join(missing)}")
    if data["schema_version"] != SCHEMA_VERSION:
        raise HarnessError("unsupported operations schema_version")
    if not data["run_id"] or not isinstance(data["run_id"], str) or is_placeholder(data["run_id"]):
        raise HarnessError("run_id must be a non-empty string without template placeholders")
    if not isinstance(data["allowed_roots"], list) or not data["allowed_roots"]:
        raise HarnessError("allowed_roots must be a non-empty array")
    groups = data["approval_groups"]
    if not isinstance(groups, list) or len(groups) != len(set(groups)):
        raise HarnessError("approval_groups must be a unique array")
    outcome = data["outcome"]
    outcome_fields = {
        "primary_metric",
        "before_state",
        "target_state",
        "unresolved_before",
        "unresolved_target",
        "expected_primary_outputs",
    }
    if not isinstance(outcome, dict) or set(outcome) != outcome_fields:
        raise HarnessError("outcome must contain the exact work-first fields")
    for field in ("primary_metric", "before_state", "target_state"):
        if not isinstance(outcome[field], str) or not outcome[field].strip() or is_placeholder(outcome[field]):
            raise HarnessError(f"outcome.{field} must be a non-empty string without template placeholders")
    for field in ("unresolved_before", "unresolved_target"):
        if not isinstance(outcome[field], int) or isinstance(outcome[field], bool) or outcome[field] < 0:
            raise HarnessError(f"outcome.{field} must be a non-negative integer")
    if outcome["unresolved_target"] > outcome["unresolved_before"]:
        raise HarnessError("outcome.unresolved_target cannot exceed unresolved_before")
    if not isinstance(outcome["expected_primary_outputs"], int) or isinstance(outcome["expected_primary_outputs"], bool) or outcome["expected_primary_outputs"] < 1:
        raise HarnessError("outcome.expected_primary_outputs must be a positive integer")
    budget = data["resource_budget"]
    budget_fields = {
        "max_task_launches",
        "max_support_artifacts",
        "max_verification_passes",
        "max_low_yield_waves",
        "high_cost_approved",
        "cost_warning",
    }
    if not isinstance(budget, dict) or set(budget) != budget_fields:
        raise HarnessError("resource_budget must contain the exact work-first fields")
    launches = budget["max_task_launches"]
    if not isinstance(launches, int) or isinstance(launches, bool) or not 0 <= launches <= 24:
        raise HarnessError("resource_budget.max_task_launches must be from 0 to 24")
    support_limit = budget["max_support_artifacts"]
    if not isinstance(support_limit, int) or isinstance(support_limit, bool) or not 0 <= support_limit <= 12:
        raise HarnessError("resource_budget.max_support_artifacts must be from 0 to 12")
    if budget["max_verification_passes"] != 1 or budget["max_low_yield_waves"] != 1:
        raise HarnessError("resource_budget permits one final verification pass and one low-yield wave")
    if launches > 6:
        if budget["high_cost_approved"] is not True:
            raise HarnessError("a launch cap above 6 requires high_cost_approved=true")
        if not isinstance(budget["cost_warning"], str) or not budget["cost_warning"].strip():
            raise HarnessError("a launch cap above 6 requires a cost warning")
    elif budget["high_cost_approved"] is not False or budget["cost_warning"] is not None:
        raise HarnessError("ordinary launch caps use high_cost_approved=false and cost_warning=null")
    support_artifacts = data["support_artifacts"]
    if not isinstance(support_artifacts, list) or any(not isinstance(item, str) or not item.strip() for item in support_artifacts):
        raise HarnessError("support_artifacts must be a list of non-empty paths")
    if len(support_artifacts) != len(set(support_artifacts)):
        raise HarnessError("support_artifacts must not contain duplicates")
    if len(support_artifacts) > support_limit:
        raise HarnessError("support_artifacts exceeds resource_budget.max_support_artifacts")
    ids: set[str] = set()
    for operation in data["operations"]:
        if not isinstance(operation, dict):
            raise HarnessError("each operation must be an object")
        required = {"id", "action", "target", "approval_group"}
        if not required.issubset(operation):
            raise HarnessError(f"operation missing fields: {operation}")
        if operation["id"] in ids:
            raise HarnessError(f"duplicate operation id: {operation['id']}")
        ids.add(operation["id"])
        if operation["action"] not in {"create", "update"}:
            raise HarnessError(f"unsupported action: {operation['action']}")
        if operation["approval_group"] not in groups:
            raise HarnessError(f"unknown approval group: {operation['approval_group']}")
        if ("content" in operation) == ("source" in operation):
            raise HarnessError(f"operation {operation['id']} needs exactly one of content or source")
        if "content" in operation and not isinstance(operation["content"], str):
            raise HarnessError(f"operation {operation['id']} content must be a string")
        if "source" in operation and (not isinstance(operation["source"], str) or not operation["source"].strip()):
            raise HarnessError(f"operation {operation['id']} source must be a non-empty path string")
        if not isinstance(operation["target"], str) or not isinstance(operation["id"], str):
            raise HarnessError(f"operation id and target must be strings: {operation['id']}")
        target = Path(operation["target"]).expanduser()
        check_target(target, [Path(root) for root in data["allowed_roots"]])
        if operation["action"] == "update" and not operation.get("expected_sha256"):
            raise HarnessError(f"update {operation['id']} requires expected_sha256")


def operation_bytes(operation: dict[str, Any]) -> bytes:
    if "content" in operation:
        payload = operation["content"].encode("utf-8")
    else:
        source = Path(operation["source"]).expanduser()
        if not source.is_file() or source.is_symlink():
            raise HarnessError(f"operation source is not a regular file: {source}")
        payload = source.read_bytes()
    expected = operation.get("expected_payload_sha256")
    if expected is not None and sha256_bytes(payload) != expected:
        raise HarnessError(f"payload changed since review: {operation['id']}")
    return payload


def backup_name(target: Path) -> str:
    tag = hashlib.sha256(str(target).encode("utf-8")).hexdigest()[:12]
    return f"{tag}-{target.name}"


def prepare(plan, approved):
    validate_operations(plan)
    if not approved or approved - set(plan['approval_groups']):
        raise HarnessError('name at least one known approved group')
    entries, targets = [], set()
    for op in plan['operations']:
        if op['approval_group'] not in approved:
            continue
        target = check_target(Path(op['target']).expanduser(), [Path(r) for r in plan['allowed_roots']])
        if target in targets:
            raise HarnessError(f'duplicate target: {target}')
        targets.add(target)
        before = sha256_file(target) if target.is_file() else None
        if op['action'] == 'create' and target.exists():
            raise HarnessError(f'create target exists: {target}')
        if op['action'] == 'update' and (before is None or before != op['expected_sha256']):
            raise HarnessError(f'hash drift: {target}')
        payload = operation_bytes(op)
        entries.append(dict(id=op['id'], target=str(target), before=before,
                            after=sha256_bytes(payload), payload=payload))
    if not entries:
        raise HarnessError('no operations selected')
    return entries


def apply(plan, approved, backup_dir):
    entries = prepare(plan, approved)  # inspect every target before any mutation
    backup_dir = backup_dir.expanduser().absolute()
    for entry in entries:
        target = Path(entry['target'])
        if is_within(backup_dir, target) or is_within(target, backup_dir):
            raise HarnessError('backup directory overlaps a target')
    backup_dir.mkdir(parents=True, exist_ok=False)  # never reuse a backup
    manifest = dict(schema_version=1, run_id=plan['run_id'],
                    allowed_roots=plan['allowed_roots'], entries=[])
    for index, entry in enumerate(entries):
        saved = {k:v for k,v in entry.items() if k != 'payload'}
        target = Path(entry['target'])
        saved['mode'] = target.stat().st_mode & 0o777 if target.exists() else 0o600
        if entry['before'] is not None:
            backup = backup_dir / f'{index}.bak'
            shutil.copy2(target, backup)
            if sha256_file(backup) != entry['before']:
                raise HarnessError(f'backup hash mismatch: {target}')
            saved['backup'] = str(backup)
        saved['status'] = 'pending'
        manifest['entries'].append(saved)
    journal = backup_dir / 'manifest.json'
    write_json(journal, manifest)  # recovery record exists before first write
    for entry, saved in zip(entries, manifest['entries']):
        target = check_target(Path(entry['target']), [Path(r) for r in plan['allowed_roots']])
        current = sha256_file(target) if target.is_file() else None
        if current != entry['before']:
            raise HarnessError(f'hash drift during apply; recover using {journal}: {target}')
        atomic_write(target, entry['payload'])
        os.chmod(target, saved['mode'])
        if sha256_file(target) != entry['after']:
            raise HarnessError(f'write verification failed; recover using {journal}')
        saved['status'] = 'applied'
        write_json(journal, manifest)
    return dict(status='applied', manifest=str(journal), files=len(entries))


def rollback(path):
    manifest = load_json(path)
    if not isinstance(manifest, dict) or manifest.get('schema_version') != 1 or not manifest.get('entries'):
        raise HarnessError('invalid manifest')
    roots = [Path(r) for r in manifest['allowed_roots']]
    pending = []
    for entry in reversed(manifest['entries']):
        target = check_target(Path(entry['target']), roots)
        current = sha256_file(target) if target.is_file() else None
        if current == entry['before']:
            continue  # unchanged or already restored, including crash recovery
        if current != entry['after']:
            raise HarnessError(f'rollback conflict; new user work preserved: {target}')
        if entry['before'] is not None:
            backup = Path(entry['backup'])
            if not backup.is_file() or backup.is_symlink() or sha256_file(backup) != entry['before']:
                raise HarnessError(f'backup invalid: {backup}')
        pending.append((entry, target))
    for entry, target in pending:
        if sha256_file(target) != entry['after']:
            raise HarnessError(f'rollback drift: {target}')
        if entry['before'] is None:
            target.unlink()  # only this helper's unchanged created file
        else:
            atomic_write(target, Path(entry['backup']).read_bytes())
            os.chmod(target, entry['mode'])
            if sha256_file(target) != entry['before']:
                raise HarnessError(f'restore verification failed; manifest kept for retry: {target}')
        entry['status'] = 'restored'
        write_json(path, manifest)
    return dict(status='restored', files=len(pending), manifest=str(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for command in ('dry-run', 'apply'):
        child = commands.add_parser(command)
        child.add_argument('--plan', type=Path, required=True)
        child.add_argument('--approved-group', action='append', required=True)
        if command == 'apply':
            child.add_argument('--backup-dir', type=Path, required=True)
    child = commands.add_parser('rollback')
    child.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'rollback':
            result = rollback(args.manifest)
        else:
            plan = load_json(args.plan)
            approved = set(args.approved_group)
            if args.command == 'apply':
                result = apply(plan, approved, args.backup_dir)
            else:
                result = dict(status='dry-run', changes=[
                    {k:v for k,v in entry.items() if k != 'payload'}
                    for entry in prepare(plan, approved)])
        print(json.dumps(result, indent=2))
        return 0
    except (HarnessError, OSError, KeyError, TypeError, ValueError, AttributeError) as exc:
        print(json.dumps(dict(status='blocked', reason=str(exc))))
        return 2


if __name__ == '__main__':
    sys.exit(main())
