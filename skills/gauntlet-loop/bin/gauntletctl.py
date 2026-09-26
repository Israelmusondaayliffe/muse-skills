#!/usr/bin/env python3
"""Deterministic project-state operations for the Gauntlet Loop skill.

Ported from the Codex/Claude gauntlet-loop plugin to the Muse (Hatch)
workspace skill format. All operations are local: they read and write a
.gauntlet/ workspace inside a project root and never touch the network,
the user's accounts, or any host agent runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"
STATES = {
    "not_initialized",
    "intake",
    "grilling",
    "plan_proposed",
    "plan_approved",
    "gauntlet_compiled",
    "executing",
    "integrating",
    "ready_for_verification",
    "verifying",
    "verified",
    "verified_with_caveats",
    "failed_verification",
    "unable_to_verify",
    "waiting_for_user",
    "blocked",
    "paused",
    "stopped",
}
PRIMARY_TRANSITIONS = {
    "not_initialized": {"intake"},
    "intake": {"grilling", "waiting_for_user", "paused", "stopped"},
    "grilling": {"plan_proposed", "waiting_for_user", "blocked", "paused", "stopped"},
    "plan_proposed": {"plan_approved", "grilling", "waiting_for_user", "paused", "stopped"},
    "plan_approved": {"gauntlet_compiled", "grilling", "waiting_for_user", "paused", "stopped"},
    "gauntlet_compiled": {"executing", "waiting_for_user", "blocked", "paused", "stopped"},
    "executing": {"integrating", "waiting_for_user", "blocked", "paused", "stopped"},
    "integrating": {"ready_for_verification", "executing", "waiting_for_user", "blocked", "paused", "stopped"},
    "ready_for_verification": {"verifying", "executing", "paused", "stopped"},
    "verifying": {"verified", "verified_with_caveats", "failed_verification", "unable_to_verify", "stopped"},
    "failed_verification": {"executing", "waiting_for_user", "blocked", "paused", "stopped"},
    "unable_to_verify": {"executing", "waiting_for_user", "blocked", "paused", "stopped"},
    "waiting_for_user": {"grilling", "plan_proposed", "plan_approved", "gauntlet_compiled", "executing", "integrating", "ready_for_verification", "verifying", "paused", "stopped"},
    "blocked": {"executing", "integrating", "verifying", "waiting_for_user", "paused", "stopped"},
    "paused": {"grilling", "plan_proposed", "plan_approved", "gauntlet_compiled", "executing", "integrating", "ready_for_verification", "verifying", "stopped"},
    "verified": set(),
    "verified_with_caveats": set(),
    "stopped": set(),
}
PLAN_HEADINGS = [
    "## 1. Project purpose",
    "## 2. Desired outcome",
    "## 5. Primary deliverables",
    "## 7. In scope",
    "## 8. Out of scope",
    "## 16. Provisional quality bars",
    "## 17. Source and evidence requirements",
    "## 21. Approval boundaries",
    "## 22. Resource envelope",
    "## 23. Acceptance criteria",
    "## 24. Stop conditions",
]
HANDOFF_HEADINGS = [f"## {index}." for index in range(1, 26)]


class GauntletError(RuntimeError):
    """Raised for deterministic contract failures."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GauntletError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise GauntletError(f"invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def replace_markdown_section(content: str, heading: str, value: str) -> str:
    """Replace one level-two Markdown section without disturbing its neighbors."""
    pattern = re.compile(rf"(?ms)(^## {re.escape(heading)}\n\n).*?(?=^## |\Z)")
    replacement = rf"\g<1>{value.strip()}\n\n"
    if not pattern.search(content):
        raise GauntletError(f"project file missing section: {heading}")
    return pattern.sub(replacement, content, count=1)


def update_project_summary(
    root: Path,
    state: dict[str, Any],
    *,
    objective: str | None = None,
    next_action: str | None = None,
) -> None:
    """Keep the canonical project summary aligned with deterministic state."""
    path = root / "project.md"
    if not path.is_file():
        return
    if objective is None:
        try:
            goal = read_json(root / "gauntlet.yaml").get("goal")
            if goal and goal != "Pending approved plan":
                objective = goal
        except GauntletError:
            objective = None
    content = path.read_text(encoding="utf-8")
    if objective:
        content = replace_markdown_section(content, "Current objective", objective)
    content = replace_markdown_section(content, "Current status", f"`{state.get('state', 'unknown')}`")
    content = replace_markdown_section(content, "Approved plan version", str(state.get("plan_version", 0)))
    content = replace_markdown_section(content, "Current Gauntlet version", str(state.get("program_version", 0)))
    if next_action:
        content = replace_markdown_section(content, "Next recommended action", next_action)
    path.write_text(content, encoding="utf-8")


def gauntlet_dir(project_root: Path) -> Path:
    return project_root.resolve() / ".gauntlet"


def initial_program() -> dict[str, Any]:
    return {
        "version": 1,
        "status": "not_compiled",
        "plan_version": 0,
        "plan_sha256": None,
        "project_type": "unresolved",
        "goal": "Pending approved plan",
        "execution": {
            "explicitly_invoked": True,
            "effort_preference": "highest_available",
            "fresh_judges": True,
            "judge_context_policy": "fresh_no_inherited_turns",
            "builder_can_issue_final_verdict": False,
            "allow_parallel_agents": True,
            "allow_user_owned_tasks": False,
            "write_isolation": "serialized",
        },
        "continuity": {
            "canonical_project_file": ".gauntlet/project.md",
            "canonical_handoff_file": ".gauntlet/handoff.md",
            "update_after_material_event": True,
            "resume_requires_explicit_invocation": True,
        },
        "budget": {
            "max_elapsed_minutes": 30,
            "max_agent_launches": 6,
            "max_concurrency": 2,
            "max_critic_rounds_per_workstream": 2,
            "extension_requires_user_approval": True,
        },
        "global_quality_bar": {"description": "Pending approved plan", "dimensions": [], "evidence_required": []},
        "workstreams": [],
        "integration_waves": [],
        "verification_panel": [],
    }


def command_init(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve()
    if not project_root.exists() or not project_root.is_dir():
        raise GauntletError(f"project root is not a directory: {project_root}")
    root = gauntlet_dir(project_root)
    if (root / "runs").exists() or (root / "sealed").exists():
        # The artifact-comparison gauntlet skill owns .gauntlet/runs and .gauntlet/sealed.
        raise GauntletError(f"gauntlet (artifact comparison) state exists in {root}; use another project root. --force does not override this.")
    if root.exists() and any(root.iterdir()) and not args.force:
        raise GauntletError(f"refusing to overwrite existing Gauntlet workspace: {root}")

    directories = [
        "sessions",
        "threads",
        "workstreams",
        "integration",
        "verification/verifier-reports",
        "reports",
    ]
    for directory in directories:
        (root / directory).mkdir(parents=True, exist_ok=True)

    project_template = (ASSETS / "project.md").read_text(encoding="utf-8")
    (root / "project.md").write_text(project_template.replace("{{PROJECT_NAME}}", args.name), encoding="utf-8")
    for source, target in [
        ("plan.md", "plan.md"),
        ("handoff.md", "handoff.md"),
    ]:
        shutil.copyfile(ASSETS / source, root / target)

    for filename, heading in [
        ("brief.md", "# Project Brief\n"),
        ("decisions.md", "# Decisions\n"),
        ("assumptions.md", "# Assumptions\n"),
        ("risks.md", "# Risks\n"),
        ("open-questions.md", "# Open Questions\n"),
        ("progress.md", "# Progress\n"),
        ("source-register.md", "# Source Register\n"),
        ("artifact-register.md", "# Artifact Register\n"),
        ("integration/integration-plan.md", "# Integration Plan\n"),
        ("integration/contradiction-register.md", "# Contradiction Register\n"),
        ("integration/synthesis-report.md", "# Synthesis Report\n"),
        ("verification/acceptance-matrix.md", "# Acceptance Matrix\n"),
        ("verification/unresolved-findings.md", "# Unresolved Findings\n"),
    ]:
        path = root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(heading, encoding="utf-8")

    state = {
        "schema_version": 1,
        "project_name": args.name,
        "state": "intake",
        "plan_version": 0,
        "program_version": 0,
        "previous_active_state": None,
        "created_at": now(),
        "updated_at": now(),
        "history": [
            {
                "previous_state": "not_initialized",
                "new_state": "intake",
                "timestamp": now(),
                "actor": args.actor,
                "reason": "Explicit Gauntlet initialization",
                "related_artifacts": [".gauntlet/project.md", ".gauntlet/state.json"],
                "required_next_action": "Run gauntlet-plan.",
            }
        ],
    }
    write_json(root / "state.json", state)
    program = initial_program()
    write_json(root / "gauntlet.yaml", program)
    write_json(
        root / "budget-ledger.json",
        {
            "captured_at": now(),
            "limits": program["budget"],
            "usage": {
                "elapsed_minutes": 0,
                "agent_launches": 0,
                "peak_concurrency": 1,
                "target_changes": 0,
                "support_artifact_count": 0,
                "critic_rounds": {},
            },
        },
    )
    write_json(
        root / "runtime-task-records.json",
        {
            "schema_version": 1,
            "owner": "gauntlet",
            "run_id": None,
            "plan_version": 0,
            "plan_sha256": None,
            "records": [],
        },
    )
    result = command_validate(argparse.Namespace(project_root=str(project_root), strict=False))
    result.update({"initialized": True, "project_root": str(project_root), "gauntlet_root": str(root)})
    return result


def validate_program(program: dict[str, Any], compiled: bool) -> list[str]:
    errors: list[str] = []
    execution = program.get("execution", {})
    budget = program.get("budget", {})
    if execution.get("explicitly_invoked") is not True:
        errors.append("program must record explicitly_invoked=true")
    if execution.get("fresh_judges") is not True:
        errors.append("program must require fresh judges")
    if execution.get("judge_context_policy") != "fresh_no_inherited_turns":
        errors.append("program must require fresh_no_inherited_turns judges")
    if execution.get("builder_can_issue_final_verdict") is not False:
        errors.append("builder_can_issue_final_verdict must be false")
    if execution.get("write_isolation") not in {"disjoint_targets", "separate_worktrees", "serialized"}:
        errors.append("write_isolation must be disjoint_targets, separate_worktrees, or serialized")
    for key in [
        "max_elapsed_minutes",
        "max_agent_launches",
        "max_concurrency",
        "max_critic_rounds_per_workstream",
    ]:
        value = budget.get(key)
        if not isinstance(value, int) or value < 1:
            errors.append(f"budget.{key} must be a positive integer")
    if budget.get("extension_requires_user_approval") is not True:
        errors.append("budget extension must require user approval")
    if compiled:
        if program.get("status") != "compiled":
            errors.append("compiled project requires program status=compiled")
        plan_sha256 = program.get("plan_sha256")
        if not isinstance(plan_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", plan_sha256):
            errors.append("compiled project requires a lowercase plan_sha256")
        if not isinstance(program.get("workstreams"), list) or not program["workstreams"]:
            errors.append("compiled program requires at least one workstream")
        else:
            workstreams = program["workstreams"]
            ids = [item.get("id") for item in workstreams if isinstance(item, dict)]
            if len(ids) != len(workstreams) or any(not isinstance(item, str) or not item for item in ids):
                errors.append("every workstream requires a non-empty id")
            if len(ids) != len(set(ids)):
                errors.append("workstream ids must be unique")
            id_set = set(ids)
            required = {
                "id",
                "objective",
                "dependencies",
                "write_targets",
                "acceptance_criteria",
                "evidence_required",
                "builder_charter",
                "critic_charter",
                "critic",
                "max_critic_rounds",
                "stop_conditions",
            }
            dependencies: dict[str, list[str]] = {}
            write_targets: list[tuple[str, str]] = []
            for item in workstreams:
                if not isinstance(item, dict):
                    errors.append("workstream entries must be objects")
                    continue
                missing = sorted(required - set(item))
                if missing:
                    errors.append(f"workstream {item.get('id', '?')} missing fields: {missing}")
                for key in [
                    "dependencies",
                    "write_targets",
                    "acceptance_criteria",
                    "evidence_required",
                    "stop_conditions",
                ]:
                    if not isinstance(item.get(key), list) or not item.get(key):
                        if key == "dependencies" and item.get(key) == []:
                            continue
                        errors.append(f"workstream {item.get('id', '?')}.{key} must be a non-empty array")
                workstream_id = item.get("id")
                dependencies[workstream_id] = item.get("dependencies", [])
                for dependency in item.get("dependencies", []):
                    if dependency not in id_set:
                        errors.append(f"workstream {workstream_id} has unknown dependency: {dependency}")
                for target in item.get("write_targets", []):
                    if isinstance(target, str) and target:
                        write_targets.append((workstream_id, target.rstrip("/")))
                if not isinstance(item.get("max_critic_rounds"), int) or item.get("max_critic_rounds", 0) < 1:
                    errors.append(f"workstream {workstream_id}.max_critic_rounds must be positive")
                for key in ["objective", "builder_charter", "critic_charter", "critic"]:
                    if not isinstance(item.get(key), str) or not item.get(key, "").strip():
                        errors.append(f"workstream {workstream_id}.{key} must be non-empty")

            visiting: set[str] = set()
            visited: set[str] = set()

            def visit(node: str) -> None:
                if node in visiting:
                    errors.append(f"workstream dependency cycle includes: {node}")
                    return
                if node in visited:
                    return
                visiting.add(node)
                for dependency in dependencies.get(node, []):
                    if dependency in id_set:
                        visit(dependency)
                visiting.remove(node)
                visited.add(node)

            for workstream_id in ids:
                visit(workstream_id)

            if execution.get("write_isolation") == "disjoint_targets":
                for index, (owner, target) in enumerate(write_targets):
                    for other_owner, other_target in write_targets[index + 1 :]:
                        if owner != other_owner and (
                            target == other_target
                            or target.startswith(other_target + "/")
                            or other_target.startswith(target + "/")
                        ):
                            errors.append(
                                f"overlapping write targets require serialization or worktrees: "
                                f"{owner}:{target} and {other_owner}:{other_target}"
                            )
            waves = program.get("integration_waves")
            if not isinstance(waves, list) or not waves:
                errors.append("compiled program requires integration waves")
            else:
                covered = {
                    item
                    for wave in waves
                    if isinstance(wave, dict)
                    for item in wave.get("workstreams", [])
                }
                if covered != id_set:
                    errors.append("integration waves must cover every workstream exactly by identity")
        panel = program.get("verification_panel")
        if (
            not isinstance(panel, list)
            or len(panel) < 3
            or len(set(panel)) != len(panel)
            or any(not isinstance(item, str) or not item for item in panel)
        ):
            errors.append("compiled program requires at least three verification perspectives")
    return errors


def substantive_markdown(path: Path, minimum: int = 20) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    body = "\n".join(line for line in content.splitlines() if not line.lstrip().startswith("#")).strip()
    return len(body) >= minimum


def has_blocking_findings(path: Path) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8").lower()
    return "[blocking]" in content or "severity: blocking" in content or "status: blocking" in content


def has_required_unresolved(path: Path) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8").lower()
    return "[required]" in content or "severity: required" in content or "status: required" in content


def validate_budget_ledger(
    root: Path,
    program: dict[str, Any],
    ledger_data: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if ledger_data is None:
        try:
            ledger = read_json(root / "budget-ledger.json")
        except GauntletError as exc:
            return [str(exc)]
    else:
        ledger = ledger_data
    usage = ledger.get("usage", {})
    budget = program.get("budget", {})
    checks = [
        ("elapsed_minutes", "max_elapsed_minutes"),
        ("agent_launches", "max_agent_launches"),
        ("peak_concurrency", "max_concurrency"),
    ]
    for usage_key, budget_key in checks:
        value = usage.get(usage_key)
        limit = budget.get(budget_key)
        if not isinstance(value, int) or value < 0:
            errors.append(f"budget ledger {usage_key} must be a non-negative integer")
        elif isinstance(limit, int) and value > limit:
            errors.append(f"budget exhausted: {usage_key}={value} exceeds {budget_key}={limit}")
    for usage_key in ("target_changes", "support_artifact_count"):
        value = usage.get(usage_key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            errors.append(f"budget ledger {usage_key} must be a non-negative integer")
    rounds = usage.get("critic_rounds")
    if not isinstance(rounds, dict):
        errors.append("budget ledger critic_rounds must be an object")
    else:
        round_limit = budget.get("max_critic_rounds_per_workstream")
        for workstream_id, count in rounds.items():
            if not isinstance(count, int) or count < 0:
                errors.append(f"critic round count must be non-negative: {workstream_id}")
            elif isinstance(round_limit, int) and count > round_limit:
                errors.append(f"critic rounds exhausted for {workstream_id}: {count}>{round_limit}")
    return errors


def validate_compiled_gate(root: Path, state: dict[str, Any], program: dict[str, Any]) -> list[str]:
    errors = validate_program(program, compiled=True)
    plan = (root / "plan.md").read_text(encoding="utf-8") if (root / "plan.md").is_file() else ""
    decisions = (root / "decisions.md").read_text(encoding="utf-8") if (root / "decisions.md").is_file() else ""
    if "Status: approved" not in plan:
        errors.append("approved plan must contain 'Status: approved'")
    elif program.get("plan_sha256") != sha256_file(root / "plan.md"):
        errors.append("compiled program plan_sha256 must match the approved plan")
    if "Approval:" not in decisions:
        errors.append("decisions register must contain an Approval record")
    if int(state.get("plan_version", 0)) < 1:
        errors.append("compiled state requires plan_version >= 1")
    if not (root / "runtime-capabilities.json").is_file():
        errors.append("compiled state requires runtime-capabilities.json")
    if not (root / "runtime-task-records.json").is_file():
        errors.append("compiled state requires runtime-task-records.json")
    errors.extend(validate_budget_ledger(root, program))
    return errors


def evidence_reference_exists(root: Path, reference: str) -> bool:
    cleaned = reference.strip().strip("`")
    if not cleaned or "://" in cleaned:
        return False
    candidate = Path(cleaned)
    if not candidate.is_absolute():
        candidate = root.parent / candidate
    return candidate.resolve().is_file()


def compiled_criteria(program: dict[str, Any]) -> set[str]:
    return {
        str(criterion).strip()
        for workstream in program.get("workstreams", [])
        if isinstance(workstream, dict)
        for criterion in workstream.get("acceptance_criteria", [])
        if str(criterion).strip()
    }


def validate_critic_report(
    path: Path,
    expected_workstream: str,
    expected_criteria: set[str],
    root: Path,
) -> list[str]:
    errors: list[str] = []
    try:
        report = read_json(path)
    except GauntletError as exc:
        return [str(exc)]
    if report.get("workstream_id") != expected_workstream:
        errors.append(f"{path}: workstream_id must be {expected_workstream}")
    if report.get("critic_isolation") != "fresh_no_inherited_turns":
        errors.append(f"{path}: critic must be fresh with no inherited turns")
    if report.get("verdict") != "artifact_wins":
        errors.append(f"{path}: authoritative critic verdict must be artifact_wins")
    evidence = report.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{path}: critic report requires evidence")
    else:
        for reference in evidence:
            if not isinstance(reference, str) or not evidence_reference_exists(root, reference):
                errors.append(f"{path}: critic evidence does not resolve to an existing file: {reference}")
    checked = report.get("criteria_checked")
    if not isinstance(checked, list) or set(checked) != expected_criteria:
        errors.append(
            f"{path}: critic criteria coverage mismatch; "
            f"expected={sorted(expected_criteria)} actual={sorted(checked or [])}"
        )
    return errors


def validate_ready_gate(root: Path, program: dict[str, Any]) -> list[str]:
    errors = validate_budget_ledger(root, program)
    for workstream in program.get("workstreams", []):
        workstream_id = workstream.get("id")
        errors.extend(
            validate_critic_report(
                root / "workstreams" / str(workstream_id) / "critic-report.json",
                str(workstream_id),
                {str(item).strip() for item in workstream.get("acceptance_criteria", [])},
                root,
            )
        )
    for relative, label in [
        ("integration/synthesis-report.md", "integration synthesis"),
        ("artifact-register.md", "artifact register"),
        ("source-register.md", "source register"),
    ]:
        if not substantive_markdown(root / relative):
            errors.append(f"{label} is missing or placeholder-only")
    if has_blocking_findings(root / "integration/contradiction-register.md"):
        errors.append("integration contradiction register contains blocking findings")
    if has_required_unresolved(root / "verification/unresolved-findings.md"):
        errors.append("required unresolved work prevents ready_for_verification")
    return errors


def validate_acceptance_matrix(path: Path, program: dict[str, Any], root: Path) -> list[str]:
    if not path.is_file():
        return [f"missing acceptance matrix: {path}"]
    lines = path.read_text(encoding="utf-8").splitlines()
    completed = [line for line in lines if line.strip().lower().startswith("- [x]")]
    incomplete = [line for line in lines if line.strip().lower().startswith("- [ ]")]
    errors: list[str] = []
    if not completed:
        errors.append("acceptance matrix requires at least one completed criterion")
    if incomplete:
        errors.append("acceptance matrix contains incomplete criteria")
    seen_criteria: list[str] = []
    allowed_roles = set(program.get("verification_panel", []))
    for line in completed:
        parts = [part.strip() for part in line.split("|")]
        criterion = parts[0].split("]", 1)[-1].strip() if parts else ""
        seen_criteria.append(criterion)
        for marker in ["Artifact:", "Check:", "Evidence:", "Verifier:"]:
            if marker not in line:
                errors.append(f"acceptance criterion missing {marker} traceability: {line}")
        values = {
            part.split(":", 1)[0]: part.split(":", 1)[1].strip()
            for part in parts[1:]
            if ":" in part
        }
        for label in ["Artifact", "Evidence"]:
            for reference in [item.strip() for item in values.get(label, "").split(",") if item.strip()]:
                if not evidence_reference_exists(root, reference):
                    errors.append(
                        f"acceptance {label.lower()} does not resolve to an existing file: {reference}"
                    )
        verifier = values.get("Verifier")
        if verifier and verifier not in allowed_roles:
            errors.append(f"acceptance verifier is not in the compiled panel: {verifier}")
    required = compiled_criteria(program)
    actual = set(seen_criteria)
    if actual != required or len(seen_criteria) != len(actual):
        errors.append(
            f"acceptance criterion coverage mismatch; expected={sorted(required)} actual={sorted(actual)}"
        )
    return errors


def validate_verifier_report(path: Path, root: Path) -> tuple[list[str], dict[str, Any]]:
    try:
        report = read_json(path)
    except GauntletError as exc:
        return [str(exc)], {}
    errors: list[str] = []
    if not isinstance(report.get("verifier_role"), str) or not report.get("verifier_role", "").strip():
        errors.append(f"{path}: verifier_role is required")
    if report.get("verifier_isolation") != "fresh_no_inherited_turns":
        errors.append(f"{path}: verifier must be fresh with no inherited turns")
    if report.get("verdict") not in {"pass", "fail", "unable_to_verify"}:
        errors.append(f"{path}: invalid verifier verdict")
    criteria = report.get("criteria_checked")
    if not isinstance(criteria, list) or not criteria:
        errors.append(f"{path}: criteria_checked must be non-empty")
    else:
        for criterion in criteria:
            if not isinstance(criterion, dict):
                errors.append(f"{path}: criteria entries must be objects")
                continue
            if not criterion.get("criterion"):
                errors.append(f"{path}: criterion id is required")
            if criterion.get("result") not in {"pass", "fail", "unable_to_verify"}:
                errors.append(f"{path}: criterion result is invalid")
            if criterion.get("result") == "pass" and not criterion.get("evidence"):
                errors.append(f"{path}: passing criteria require evidence")
            for reference in criterion.get("evidence", []):
                if not isinstance(reference, str) or not evidence_reference_exists(root, reference):
                    errors.append(
                        f"{path}: verifier evidence does not resolve to an existing file: {reference}"
                    )
    return errors, report


def panel_snapshot(
    root: Path,
    program: dict[str, Any],
) -> tuple[list[str], str | None, list[tuple[Path, dict[str, Any]]]]:
    errors = validate_acceptance_matrix(root / "verification" / "acceptance-matrix.md", program, root)
    reports: list[tuple[Path, dict[str, Any]]] = []
    report_paths = sorted((root / "verification" / "verifier-reports").glob("*.json"))
    if len(report_paths) < 3:
        errors.append("verification requires at least three verifier reports")
    roles: set[str] = set()
    outcomes: list[str] = []
    caveats = False
    checked_criteria: set[str] = set()
    for path in report_paths:
        report_errors, report = validate_verifier_report(path, root)
        errors.extend(report_errors)
        if report:
            role = report.get("verifier_role")
            if role in roles:
                errors.append(f"duplicate verifier role: {role}")
            roles.add(role)
            outcomes.append(report.get("verdict"))
            outcomes.extend(
                item.get("result")
                for item in report.get("criteria_checked", [])
                if isinstance(item, dict)
            )
            checked_criteria.update(
                str(item.get("criterion")).strip()
                for item in report.get("criteria_checked", [])
                if isinstance(item, dict) and item.get("criterion")
            )
            caveats = caveats or bool(report.get("residual_risks"))
            reports.append((path, report))
    expected_roles = set(program.get("verification_panel", []))
    if roles != expected_roles:
        errors.append(f"verifier role mismatch; expected={sorted(expected_roles)} actual={sorted(roles)}")
    required = compiled_criteria(program)
    if checked_criteria != required:
        errors.append(
            f"verifier criterion coverage mismatch; "
            f"expected={sorted(required)} actual={sorted(checked_criteria)}"
        )
    if errors:
        return errors, None, reports
    if "fail" in outcomes:
        verdict = "failed_verification"
    elif "unable_to_verify" in outcomes:
        verdict = "unable_to_verify"
    elif caveats:
        verdict = "verified_with_caveats"
    else:
        verdict = "verified"
    return errors, verdict, reports


def validate_verifying_gate(root: Path, program: dict[str, Any]) -> list[str]:
    errors = validate_acceptance_matrix(root / "verification" / "acceptance-matrix.md", program, root)
    try:
        capabilities = read_json(root / "runtime-capabilities.json")
        if capabilities.get("fresh_no_inherited_turns_supported") is not True:
            errors.append("fresh isolated agents are unavailable; verification cannot begin")
    except GauntletError as exc:
        errors.append(str(exc))
    return errors


def validate_terminal_gate(root: Path, program: dict[str, Any], target: str) -> list[str]:
    errors, computed, _ = panel_snapshot(root, program)
    if computed and computed != target:
        errors.append(f"terminal verdict must match computed panel verdict: {computed}")
    report = root / "reports" / "evidence-report.md"
    if not substantive_markdown(report, minimum=200):
        errors.append("final evidence report is missing or incomplete")
    elif f"Verdict: `{target}`" not in report.read_text(encoding="utf-8"):
        errors.append("final evidence report verdict does not match terminal state")
    if target in {"verified", "verified_with_caveats"}:
        if has_required_unresolved(root / "verification" / "unresolved-findings.md"):
            errors.append("required unresolved work prevents a verified verdict")
        if has_blocking_findings(root / "verification" / "unresolved-findings.md"):
            errors.append("blocking verification findings prevent a verified verdict")
        if has_blocking_findings(root / "integration" / "contradiction-register.md"):
            errors.append("blocking integration contradictions prevent a verified verdict")
    return errors


def validate_continuity_consistency(root: Path, state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    project_path = root / "project.md"
    if project_path.is_file():
        project = project_path.read_text(encoding="utf-8")
        required = [
            f"`{state.get('state')}`",
            f"## Approved plan version\n\n{state.get('plan_version')}",
            f"## Current Gauntlet version\n\n{state.get('program_version')}",
        ]
        for marker in required:
            if marker not in project:
                errors.append(f"project summary is stale or inconsistent: missing {marker!r}")
    return errors


def command_validate(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve()
    root = gauntlet_dir(project_root)
    required_files = [
        "project.md",
        "brief.md",
        "plan.md",
        "gauntlet.yaml",
        "budget-ledger.json",
        "runtime-task-records.json",
        "state.json",
        "decisions.md",
        "assumptions.md",
        "risks.md",
        "open-questions.md",
        "progress.md",
        "source-register.md",
        "artifact-register.md",
        "handoff.md",
    ]
    required_directories = ["sessions", "threads", "workstreams", "integration", "verification", "reports"]
    errors = [f"missing file: .gauntlet/{name}" for name in required_files if not (root / name).is_file()]
    errors.extend(f"missing directory: .gauntlet/{name}" for name in required_directories if not (root / name).is_dir())

    state: dict[str, Any] = {}
    program: dict[str, Any] = {}
    if (root / "state.json").is_file():
        try:
            state = read_json(root / "state.json")
            for key in ["schema_version", "project_name", "state", "plan_version", "program_version", "history"]:
                if key not in state:
                    errors.append(f"state missing key: {key}")
            if state.get("state") not in STATES:
                errors.append(f"unknown state: {state.get('state')}")
            if not isinstance(state.get("history"), list):
                errors.append("state.history must be an array")
        except GauntletError as exc:
            errors.append(str(exc))

    if (root / "gauntlet.yaml").is_file():
        try:
            program = read_json(root / "gauntlet.yaml")
            compiled = state.get("state") in {
                "gauntlet_compiled",
                "executing",
                "integrating",
                "ready_for_verification",
                "verifying",
                "verified",
                "verified_with_caveats",
                "failed_verification",
                "unable_to_verify",
            }
            errors.extend(validate_program(program, compiled))
        except GauntletError as exc:
            errors.append(str(exc))

    if (root / "plan.md").is_file():
        plan = (root / "plan.md").read_text(encoding="utf-8")
        errors.extend(f"plan missing heading: {heading}" for heading in PLAN_HEADINGS if heading not in plan)

    if getattr(args, "strict", False):
        errors.extend(command_validate_handoff(argparse.Namespace(project_root=str(project_root)))["errors"])
        errors.extend(validate_continuity_consistency(root, state))
        current = state.get("state")
        compiled_states = {
            "gauntlet_compiled",
            "executing",
            "integrating",
            "ready_for_verification",
            "verifying",
            "verified",
            "verified_with_caveats",
            "failed_verification",
            "unable_to_verify",
        }
        ready_states = {
            "ready_for_verification",
            "verifying",
            "verified",
            "verified_with_caveats",
            "failed_verification",
            "unable_to_verify",
        }
        verifying_states = {
            "verifying",
            "verified",
            "verified_with_caveats",
            "failed_verification",
            "unable_to_verify",
        }
        terminal_states = {
            "verified",
            "verified_with_caveats",
            "failed_verification",
            "unable_to_verify",
        }
        if current in compiled_states:
            errors.extend(validate_compiled_gate(root, state, program))
        if current in ready_states:
            errors.extend(validate_ready_gate(root, program))
        if current in verifying_states:
            errors.extend(validate_verifying_gate(root, program))
        if current in terminal_states:
            errors.extend(validate_terminal_gate(root, program, current))

    return {
        "valid": not errors,
        "project_root": str(project_root),
        "state": state.get("state"),
        "errors": errors,
    }


def command_transition(args: argparse.Namespace) -> dict[str, Any]:
    root = gauntlet_dir(Path(args.project_root))
    state_path = root / "state.json"
    state = read_json(state_path)
    current = state.get("state")
    target = args.to
    if target not in STATES:
        raise GauntletError(f"unknown target state: {target}")
    allowed = PRIMARY_TRANSITIONS.get(current, set())
    if target not in allowed and not args.force:
        raise GauntletError(f"invalid transition: {current} -> {target}")
    program = read_json(root / "gauntlet.yaml")
    gate_errors: list[str] = []
    if target == "plan_approved":
        plan = (root / "plan.md").read_text(encoding="utf-8") if (root / "plan.md").is_file() else ""
        decisions = (root / "decisions.md").read_text(encoding="utf-8") if (root / "decisions.md").is_file() else ""
        if "Status: approved" not in plan:
            gate_errors.append("plan approval requires 'Status: approved' in .gauntlet/plan.md")
        if "Approval:" not in decisions:
            gate_errors.append("plan approval requires an Approval record in .gauntlet/decisions.md")
    if target == "gauntlet_compiled":
        gate_errors.extend(validate_compiled_gate(root, state, program))
    if target == "ready_for_verification":
        gate_errors.extend(validate_ready_gate(root, program))
    if target == "verifying":
        gate_errors.extend(validate_verifying_gate(root, program))
    if target in {"verified", "verified_with_caveats", "failed_verification", "unable_to_verify"}:
        gate_errors.extend(validate_compiled_gate(root, state, program))
        gate_errors.extend(validate_ready_gate(root, program))
        gate_errors.extend(validate_verifying_gate(root, program))
        gate_errors.extend(validate_terminal_gate(root, program, target))
    if gate_errors:
        raise GauntletError(f"transition gate failed for {target}: " + "; ".join(gate_errors))
    if target in {"waiting_for_user", "blocked", "paused"}:
        state["previous_active_state"] = current
    if target == "plan_approved":
        state["plan_version"] = max(1, int(state.get("plan_version", 0)))
    if target == "gauntlet_compiled":
        state["program_version"] = max(1, int(state.get("program_version", 0)))
    event = {
        "previous_state": current,
        "new_state": target,
        "timestamp": now(),
        "actor": args.actor,
        "reason": args.reason,
        "related_artifacts": args.artifact or [],
        "required_next_action": args.next_action,
    }
    state["state"] = target
    state["updated_at"] = now()
    state.setdefault("history", []).append(event)
    write_json(state_path, state)
    update_project_summary(root, state, next_action=args.next_action)
    return {"updated": True, "previous_state": current, "new_state": target, "event": event}


def section_text(title: str, value: str) -> str:
    return f"## {title}\n\n{value.strip() or 'None recorded.'}\n"


def command_handoff(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve()
    root = gauntlet_dir(project_root)
    state = read_json(root / "state.json")
    latest = state.get("history", [])[-1] if state.get("history") else {}
    content = "# Gauntlet Handoff\n\n"
    values = [
        ("1. Project identity", state.get("project_name", "")),
        ("2. Current objective", args.objective or "See .gauntlet/project.md."),
        ("3. Why this project matters", "See the approved project plan."),
        ("4. Approved plan and version", f"Plan version {state.get('plan_version', 0)}."),
        ("5. Current state", state.get("state", "unknown")),
        ("6. Work completed in this session", args.completed or "See the latest state history event."),
        ("7. Artifacts created or changed", "\n".join(f"- {item}" for item in (args.artifact or []))),
        ("8. Evidence produced", "\n".join(f"- {item}" for item in (args.evidence or []))),
        ("9. Decisions made", "See .gauntlet/decisions.md."),
        ("10. Decisions awaiting approval", "See .gauntlet/open-questions.md."),
        ("11. Assumptions currently in force", "See .gauntlet/assumptions.md."),
        ("12. Known failures and weaknesses", args.failures or "See workstream critic reports."),
        ("13. Critic findings still open", "See .gauntlet/verification/unresolved-findings.md."),
        ("14. Current workstreams", "See .gauntlet/gauntlet.yaml and workstream current-state files."),
        ("15. Blocked workstreams", "See .gauntlet/progress.md."),
        ("16. Source and citation status", "See .gauntlet/source-register.md."),
        ("17. Integration status", "See .gauntlet/integration/synthesis-report.md."),
        ("18. Risks and uncertainties", "See .gauntlet/risks.md and .gauntlet/open-questions.md."),
        ("19. Exact next actions", args.next_action or latest.get("required_next_action", "Review the current state.")),
        ("20. Files the next agent should read first", ".gauntlet/project.md\n\n.gauntlet/handoff.md\n\n.gauntlet/plan.md\n\n.gauntlet/gauntlet.yaml"),
        ("21. Commands or checks the next agent should run", "python3 <plugin-root>/scripts/gauntletctl.py validate --project-root ."),
        ("22. Things the next agent must not redo", args.do_not_redo or "Do not repeat work recorded as complete."),
        ("23. Things the next agent must not assume", "Do not assume missing evidence, approvals, or fresh-context verification."),
        ("24. User preferences and explicit instructions", args.user_instructions or "See the approved plan and decisions register."),
        ("25. Session provenance", f"Generated at {now()} by {args.actor}."),
    ]
    content += "\n".join(section_text(title, str(value)) for title, value in values)
    destination = root / "handoff.md"
    destination.write_text(content, encoding="utf-8")
    update_project_summary(root, state, objective=args.objective, next_action=args.next_action)
    sessions = root / "sessions"
    number = len(list(sessions.glob("session-*.md"))) + 1
    session_path = sessions / f"session-{number:03d}.md"
    session_path.write_text(content, encoding="utf-8")
    return {
        "created": True,
        "handoff": str(destination),
        "session_record": str(session_path),
        "validation": command_validate_handoff(argparse.Namespace(project_root=str(project_root))),
    }


def command_validate_handoff(args: argparse.Namespace) -> dict[str, Any]:
    path = gauntlet_dir(Path(args.project_root)) / "handoff.md"
    errors: list[str] = []
    if not path.is_file():
        errors.append(f"missing handoff: {path}")
    else:
        content = path.read_text(encoding="utf-8")
        for marker in HANDOFF_HEADINGS:
            if marker not in content:
                errors.append(f"handoff missing section marker: {marker}")
        for required in [
            "## 2. Current objective",
            "## 5. Current state",
            "## 19. Exact next actions",
            "## 20. Files the next agent should read first",
            "## 22. Things the next agent must not redo",
            "## 23. Things the next agent must not assume",
        ]:
            start = content.find(required)
            if start >= 0:
                next_heading = content.find("\n## ", start + len(required))
                body = content[start + len(required): next_heading if next_heading >= 0 else None].strip()
                if not body:
                    errors.append(f"handoff section is empty: {required}")
        try:
            state = read_json(path.parent / "state.json")
            if f"## 5. Current state\n\n{state.get('state')}" not in content:
                errors.append("handoff current state does not match state.json")
            if f"Plan version {state.get('plan_version')}" not in content:
                errors.append("handoff plan version does not match state.json")
        except GauntletError as exc:
            errors.append(str(exc))
    return {"valid": not errors, "handoff": str(path), "errors": errors}


def command_evidence(args: argparse.Namespace) -> dict[str, Any]:
    project_root = Path(args.project_root).resolve()
    root = gauntlet_dir(project_root)
    state = read_json(root / "state.json")
    program = read_json(root / "gauntlet.yaml")
    if state.get("state") != "verifying":
        raise GauntletError("evidence report can be generated only while state=verifying")
    gate_errors = validate_ready_gate(root, program)
    gate_errors.extend(validate_verifying_gate(root, program))
    panel_errors, computed_verdict, reports = panel_snapshot(root, program)
    gate_errors.extend(panel_errors)
    if gate_errors:
        raise GauntletError("evidence gate failed: " + "; ".join(gate_errors))
    verdict = args.verdict
    if verdict != computed_verdict:
        raise GauntletError(f"requested verdict {verdict} does not match computed verdict {computed_verdict}")
    template = (ASSETS / "evidence-report.md").read_text(encoding="utf-8")
    verifier_summary = "\n".join(
        f"- `{path.relative_to(root)}`: {report.get('verifier_role')} returned `{report.get('verdict')}`."
        for path, report in reports
    )
    preamble = (
        f"Verdict: `{verdict}`\n\n"
        f"Generated: {now()}\n\n"
        f"Project: {state.get('project_name')}\n\n"
        f"State: `{state.get('state')}`\n\n"
        f"Plan version: {state.get('plan_version')}\n\n"
        f"Program version: {program.get('version')}\n\n"
        "Computed from schema-checked fresh verifier reports and the completed acceptance matrix.\n\n"
        f"Verifier reports:\n\n{verifier_summary}\n\n"
        "Acceptance traceability: `.gauntlet/verification/acceptance-matrix.md`\n\n"
        "Integration evidence: `.gauntlet/integration/synthesis-report.md`\n\n"
        "Artifact register: `.gauntlet/artifact-register.md`\n\n"
        "Source register: `.gauntlet/source-register.md`\n\n"
    )
    output = root / "reports" / "evidence-report.md"
    output.write_text(template.replace("# Gauntlet Evidence Report\n", "# Gauntlet Evidence Report\n\n" + preamble, 1), encoding="utf-8")
    return {"created": True, "path": str(output), "verdict": verdict}


def command_capabilities(args: argparse.Namespace) -> dict[str, Any]:
    if args.fresh_isolation and not (args.isolation_evidence or "").strip():
        raise GauntletError("--fresh-isolation requires --isolation-evidence describing an observed check")
    data = {
        "captured_at": now(),
        "host": "Hatch",
        "assistant": "Muse",
        "host_version": args.host_version,
        "parent_model": args.model,
        "parent_reasoning": args.reasoning,
        "agent_tools": args.agent_tools,
        "thread_tools": args.thread_tools,
        "max_concurrency": args.max_concurrency,
        "fresh_no_inherited_turns_supported": True if args.fresh_isolation else "unknown",
        "isolation_evidence": args.isolation_evidence,
        "limitations": [
            "The script cannot inspect model-visible tool inventory by itself.",
            "Parent model, effort, and host mode remain user-selected.",
            "Isolation is recorded from evidence the lead supplies; a host or model name is not proof.",
        ],
    }
    destination = gauntlet_dir(Path(args.project_root)) / "runtime-capabilities.json"
    write_json(destination, data)
    return {"created": True, "path": str(destination), "capabilities": data}


def command_usage(args: argparse.Namespace) -> dict[str, Any]:
    root = gauntlet_dir(Path(args.project_root))
    ledger_path = root / "budget-ledger.json"
    ledger = read_json(ledger_path)
    usage = ledger.setdefault("usage", {})
    updates = {
        "elapsed_minutes": args.elapsed_minutes,
        "agent_launches": args.agent_launches,
        "peak_concurrency": args.peak_concurrency,
        "target_changes": args.target_changes,
        "support_artifact_count": args.support_artifacts,
    }
    for key, value in updates.items():
        if value is not None:
            if value < 0:
                raise GauntletError(f"{key} must be non-negative")
            usage[key] = value
    if args.workstream and args.critic_rounds is None:
        raise GauntletError("--workstream requires --critic-rounds")
    if args.critic_rounds is not None:
        if not args.workstream:
            raise GauntletError("--critic-rounds requires --workstream")
        if args.critic_rounds < 0:
            raise GauntletError("critic_rounds must be non-negative")
        usage.setdefault("critic_rounds", {})[args.workstream] = args.critic_rounds
    ledger["captured_at"] = now()
    program = read_json(root / "gauntlet.yaml")
    errors = validate_budget_ledger(root, program, ledger)
    if errors:
        raise GauntletError("budget ledger update rejected: " + "; ".join(errors))
    write_json(ledger_path, ledger)
    return {"updated": True, "path": str(ledger_path), "usage": usage}


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Manage deterministic Gauntlet project state.")
    sub = root.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--project-root", required=True)
    init.add_argument("--name", required=True)
    init.add_argument("--actor", default="lead-agent")
    init.add_argument("--force", action="store_true")
    init.set_defaults(handler=command_init)

    validate = sub.add_parser("validate")
    validate.add_argument("--project-root", required=True)
    validate.add_argument("--strict", action="store_true")
    validate.set_defaults(handler=command_validate)

    transition = sub.add_parser("transition")
    transition.add_argument("--project-root", required=True)
    transition.add_argument("--to", required=True)
    transition.add_argument("--actor", required=True)
    transition.add_argument("--reason", required=True)
    transition.add_argument("--artifact", action="append")
    transition.add_argument("--next-action", required=True)
    transition.add_argument("--force", action="store_true")
    transition.set_defaults(handler=command_transition)

    handoff = sub.add_parser("handoff")
    handoff.add_argument("--project-root", required=True)
    handoff.add_argument("--actor", required=True)
    handoff.add_argument("--objective")
    handoff.add_argument("--completed")
    handoff.add_argument("--failures")
    handoff.add_argument("--next-action")
    handoff.add_argument("--do-not-redo")
    handoff.add_argument("--user-instructions")
    handoff.add_argument("--artifact", action="append")
    handoff.add_argument("--evidence", action="append")
    handoff.set_defaults(handler=command_handoff)

    validate_handoff = sub.add_parser("validate-handoff")
    validate_handoff.add_argument("--project-root", required=True)
    validate_handoff.set_defaults(handler=command_validate_handoff)

    evidence = sub.add_parser("evidence")
    evidence.add_argument("--project-root", required=True)
    evidence.add_argument("--verdict", required=True)
    evidence.set_defaults(handler=command_evidence)

    capabilities = sub.add_parser("capabilities")
    capabilities.add_argument("--project-root", required=True)
    capabilities.add_argument("--host-version", default="unknown")
    capabilities.add_argument("--model", default="unknown")
    capabilities.add_argument("--reasoning", default="unknown")
    capabilities.add_argument("--agent-tools", choices=["available", "unavailable", "unknown"], default="unknown")
    capabilities.add_argument("--thread-tools", choices=["available", "unavailable", "unknown"], default="unknown")
    capabilities.add_argument("--max-concurrency", type=int, default=1)
    capabilities.add_argument("--fresh-isolation", action="store_true")
    capabilities.add_argument("--isolation-evidence", help="Observed check, e.g. a spawned child could not read a canary from the parent turn")
    capabilities.set_defaults(handler=command_capabilities)

    usage = sub.add_parser("usage")
    usage.add_argument("--project-root", required=True)
    usage.add_argument("--elapsed-minutes", type=int)
    usage.add_argument("--agent-launches", type=int)
    usage.add_argument("--peak-concurrency", type=int)
    usage.add_argument("--target-changes", type=int)
    usage.add_argument("--support-artifacts", type=int)
    usage.add_argument("--workstream")
    usage.add_argument("--critic-rounds", type=int)
    usage.set_defaults(handler=command_usage)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = args.handler(args)
    except GauntletError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 2
    print(json.dumps({"ok": bool(result.get("valid", True)), **result}, indent=2))
    return 0 if result.get("valid", True) else 1


if __name__ == "__main__":
    sys.exit(main())
