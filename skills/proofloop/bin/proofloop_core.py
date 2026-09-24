"""Deterministic, standard-library protocol helpers for ProofLoop v1."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any


MAX_BUDGETS = {
    "inner_drafts_max": 3,
    "execution_attempts_max": 2,
    "verifier_executions_max": 2,
    "tool_calls": 20,
    "wall_time_minutes": 30,
    "memory_writes": 2,
}
EVIDENCE_LEVELS = {"E0", "E1", "E2", "E3", "E4"}
TASK_FAMILIES = {"code", "research", "structured_artifact", "creative_preference", "other"}
ELIGIBILITY_CLASSES = {"objective", "human_verifiable", "suggestion_only", "learning_ineligible"}
PRIVACY_CLASSES = {"public", "internal", "confidential", "restricted"}
STORAGE_PROFILES = {"none", "ephemeral", "workspace_ledger", "durable_adapter"}
V1_RECORD_TYPES = {"observation", "experience", "candidate_lesson", "approved_advisory", "user_preference"}
RESERVED_RECORD_TYPES = {"policy", "revocation", "promoted_lesson"}
HIGH_STAKES_FAMILIES = {
    "medical", "legal", "financial", "employment", "identity", "security_policy", "permission"
}
SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\bAuthorization\s*:\s*Bearer\s+[A-Za-z0-9._~+/-]{8,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"),
)


def _canonical_value(value: Any) -> Any:
    if isinstance(value, float):
        raise ValueError("floats are outside the ProofLoop v1 canonical I-JSON subset")
    if value is None or isinstance(value, (str, int, bool)):
        return value
    if isinstance(value, list):
        return [_canonical_value(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("canonical object keys must be strings")
        return {key: _canonical_value(value[key]) for key in sorted(value)}
    raise ValueError(f"unsupported canonical value type: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Return the deterministic v1 canonical I-JSON subset representation."""
    return json.dumps(
        _canonical_value(value),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def generate_id(payload: dict[str, Any]) -> dict[str, Any]:
    namespace = payload.get("namespace", "record")
    content = payload.get("content", payload)
    digest = canonical_digest(content)
    return {"id": f"{namespace}-{digest[:24]}", "digest": digest, "algorithm": "sha256"}


def validate_contract(contract: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(contract, dict):
        return {"valid": False, "errors": ["contract must be an object"]}

    required = (
        "contract_version", "task_id", "goal", "task_family", "eligibility_class",
        "success_criteria", "advisory_retrieval", "aggregation_rule", "verifiers",
        "budgets", "blocked_stop", "privacy_class", "storage_profile",
    )
    for field in required:
        if field not in contract:
            errors.append(f"missing required field: {field}")

    if contract.get("contract_version") != "1.0":
        errors.append("contract_version must be 1.0")
    if not isinstance(contract.get("task_id"), str) or not contract.get("task_id"):
        errors.append("task_id must be a non-empty string")
    if not isinstance(contract.get("goal"), str) or not contract.get("goal"):
        errors.append("goal must be a non-empty string")
    if contract.get("task_family") not in TASK_FAMILIES:
        errors.append("task_family is not supported by the v1 protocol")
    if contract.get("eligibility_class") not in ELIGIBILITY_CLASSES:
        errors.append("eligibility_class is invalid")
    if contract.get("privacy_class") not in PRIVACY_CLASSES:
        errors.append("privacy_class is invalid")
    if contract.get("storage_profile") not in STORAGE_PROFILES:
        errors.append("storage_profile is invalid")
    if contract.get("aggregation_rule") != "all_required":
        errors.append("aggregation_rule must be all_required in v1")

    criteria = contract.get("success_criteria")
    if not isinstance(criteria, list) or not criteria:
        errors.append("success_criteria must contain at least one criterion")
        criteria = []
    criterion_ids: set[str] = set()
    objective_criteria: set[str] = set()
    for criterion in criteria:
        if not isinstance(criterion, dict):
            errors.append("each success criterion must be an object")
            continue
        criterion_id = criterion.get("criterion_id")
        if not isinstance(criterion_id, str) or not criterion_id:
            errors.append("criterion_id must be a non-empty string")
        elif criterion_id in criterion_ids:
            errors.append(f"duplicate criterion_id: {criterion_id}")
        else:
            criterion_ids.add(criterion_id)
        if not criterion.get("statement"):
            errors.append(f"criterion {criterion_id or '?'} requires a statement")
        level = criterion.get("evidence_minimum")
        if level not in EVIDENCE_LEVELS:
            errors.append(f"criterion {criterion_id or '?'} has invalid evidence_minimum")
        if level in {"E3", "E4"} and isinstance(criterion_id, str):
            objective_criteria.add(criterion_id)

    budgets = contract.get("budgets")
    if not isinstance(budgets, dict):
        errors.append("budgets must be an object")
    else:
        for name, maximum in MAX_BUDGETS.items():
            value = budgets.get(name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0 or value > maximum:
                errors.append(f"{name} must be an integer from 0 through {maximum}")

    covered: set[str] = set()
    verifiers = contract.get("verifiers")
    if not isinstance(verifiers, list):
        errors.append("verifiers must be an array")
        verifiers = []
    for verifier in verifiers:
        if not isinstance(verifier, dict):
            errors.append("each verifier must be an object")
            continue
        required_verifier = (
            "verifier_id", "verifier_version", "verifier_digest", "adapter_id",
            "criterion_ids", "configuration_digest", "test_or_data_digests", "boundary",
        )
        missing = [field for field in required_verifier if field not in verifier]
        if missing:
            errors.append(f"verifier missing fields: {', '.join(missing)}")
        if verifier.get("boundary") not in {"host_read_only", "contract_pinned"}:
            errors.append("verifier boundary must be host_read_only or contract_pinned")
        for digest_name in ("verifier_digest", "configuration_digest"):
            digest = verifier.get(digest_name)
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"verifier {digest_name} must be a lowercase SHA-256 digest")
        assigned = verifier.get("criterion_ids", [])
        if isinstance(assigned, list):
            covered.update(item for item in assigned if isinstance(item, str))
        else:
            errors.append("verifier criterion_ids must be an array")
    if objective_criteria - covered:
        errors.append("objective verifier coverage is missing for: " + ", ".join(sorted(objective_criteria - covered)))

    retrieval = contract.get("advisory_retrieval")
    if not isinstance(retrieval, dict) or not isinstance(retrieval.get("enabled"), bool):
        errors.append("advisory_retrieval.enabled must be boolean")
    elif retrieval["enabled"]:
        selections = retrieval.get("selections")
        if not isinstance(selections, list) or not selections:
            errors.append("enabled advisory retrieval requires selections")
        else:
            for selection in selections:
                if not isinstance(selection, dict) or set(("record_id", "content_digest", "operation", "decision_source_turn")) - set(selection):
                    errors.append("each retrieval selection must bind record_id, content_digest, operation, and decision_source_turn")
                elif selection.get("operation") != "retrieve":
                    errors.append("retrieval selection operation must be retrieve")

    if contract.get("eligibility_class") == "learning_ineligible" and contract.get("storage_profile") != "none":
        errors.append("learning_ineligible requires storage_profile none")

    return {"valid": not errors, "errors": errors, "contract_digest": canonical_digest(contract)}


def validate_record(record: Any) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return {"valid": False, "errors": ["record must be an object"]}
    required = (
        "schema_version", "record_id", "record_type", "status", "created_at", "task_id",
        "privacy_class", "scope", "content", "provenance",
    )
    for field in required:
        if field not in record:
            errors.append(f"missing required field: {field}")
    record_type = record.get("record_type")
    if record_type in RESERVED_RECORD_TYPES:
        errors.append(f"record_type {record_type} is reserved and disabled in v1")
    elif record_type not in V1_RECORD_TYPES:
        errors.append("record_type is invalid")
    if record.get("privacy_class") not in PRIVACY_CLASSES:
        errors.append("privacy_class is invalid")
    if not isinstance(record.get("scope"), dict):
        errors.append("scope must be an object")
    if not isinstance(record.get("provenance"), list):
        errors.append("provenance must be an array")
    if record_type == "candidate_lesson" and record.get("status") != "candidate":
        errors.append("candidate_lesson must have candidate status")
    return {"valid": not errors, "errors": errors, "record_digest": canonical_digest(record)}


def _redact_string(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def redact_record(value: Any) -> Any:
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, list):
        return [redact_record(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_record(item) for key, item in value.items()}
    return value


def detect_conflicts(records: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for record in records:
        content = record.get("content", {})
        scope = record.get("scope", {})
        if not isinstance(content, dict) or "key" not in content or "value" not in content:
            continue
        group_key = (canonical_json(scope), str(content["key"]))
        groups.setdefault(group_key, []).append(record)
    conflicts = []
    for (scope_json, key), group in sorted(groups.items()):
        values = {canonical_json(item.get("content", {}).get("value")) for item in group}
        if len(group) > 1 and len(values) > 1:
            conflicts.append({
                "record_ids": sorted(str(item.get("record_id")) for item in group),
                "key": key,
                "scope": json.loads(scope_json),
            })
    return {"conflicts": conflicts, "count": len(conflicts)}


def evaluate_policy(request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("requested_action")
    family = request.get("task_family")
    storage = request.get("requested_storage_profile", request.get("storage_profile", "none"))
    reasons: list[str] = []
    allowed = True

    if family in HIGH_STAKES_FAMILIES:
        storage = "none"
        if action in {"record_experience", "record_observation", "record_lesson", "record_preference", "record_audit"}:
            allowed = False
            reasons.append("high-stakes tasks create no persistent ProofLoop record")
    if action == "external_connector_write":
        allowed = False
        reasons.append("ProofLoop v1 performs zero external connector writes")
    if action in {"automatic_promotion", "audit_write"}:
        allowed = False
        reasons.append(f"{action} is prohibited in ProofLoop v1")
    if action == "accept_evidence" and request.get("verifier_mutated_after_contract"):
        allowed = False
        reasons.append("verifier mutation invalidates evidence")
    if action == "execute_capped":
        if not request.get("best_effort_authorized") or not request.get("pre_execution_gate_passed"):
            allowed = False
            reasons.append("capped execution requires explicit best-effort authorization and a passing deterministic gate")
    if action == "retrieve":
        decision = request.get("decision")
        binding = {
            "task_id": request.get("task_id"),
            "record_id": request.get("record_id"),
            "content_digest": request.get("content_digest"),
            "operation": "retrieve",
        }
        if not isinstance(decision, dict) or not decision.get("affirmative") or not decision.get("current_turn"):
            allowed = False
            reasons.append("retrieval requires an affirmative current-turn human decision")
        elif any(decision.get(key) != value for key, value in binding.items()):
            allowed = False
            reasons.append("retrieval decision binding mismatch")
        if request.get("displayed_content_digest") != request.get("content_digest"):
            allowed = False
            reasons.append("displayed content digest mismatch")
        task_scope = request.get("task_scope")
        record_scope = request.get("record_scope")
        if isinstance(task_scope, dict) and isinstance(record_scope, dict):
            for key in ("tenant", "user", "workspace", "project", "domain"):
                record_value = record_scope.get(key)
                task_value = task_scope.get(key)
                if record_value is not None and record_value != task_value:
                    allowed = False
                    reasons.append(f"scope mismatch: {key}")
                    break
    if storage == "workspace_ledger":
        capabilities = request.get("ledger_capabilities", {})
        required = ("lock", "generation_cas", "journal", "atomic_replace")
        if not isinstance(capabilities, dict) or not all(capabilities.get(name) is True for name in required):
            storage = "ephemeral"
            reasons.append("workspace ledger downgraded because atomic store guarantees are incomplete")
    return {
        "allowed": allowed,
        "storage_profile": storage,
        "reasons": reasons,
        "request": deepcopy(request),
    }


def run_regressions(payload: dict[str, Any]) -> dict[str, Any]:
    cases = payload.get("cases", [])
    results = []
    for case in cases:
        passed = case.get("actual") == case.get("expected")
        results.append({"case_id": case.get("case_id"), "passed": passed})
    passed_count = sum(1 for result in results if result["passed"])
    return {
        "passed": passed_count,
        "failed": len(results) - passed_count,
        "results": results,
        "completed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


def transfer_records(payload: dict[str, Any]) -> dict[str, Any]:
    mode = payload.get("mode")
    if mode == "export":
        records = payload.get("records", [])
        bundle = {"format": "proofloop-neutral-v1", "records": deepcopy(records)}
        return {"bundle": bundle, "bundle_digest": canonical_digest(bundle)}
    if mode == "import":
        bundle = payload.get("bundle", {})
        if bundle.get("format") != "proofloop-neutral-v1" or not isinstance(bundle.get("records"), list):
            return {"valid": False, "errors": ["invalid neutral bundle"]}
        return {"valid": True, "records": deepcopy(bundle["records"]), "bundle_digest": canonical_digest(bundle)}
    return {"valid": False, "errors": ["mode must be export or import"]}
