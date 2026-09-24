#!/usr/bin/env python3
"""Deterministic, non-mutating AI Film Studio helper.

Subcommands:
  route PACKET.json
      Validate a film-advisor packet and return a routing decision or a stop.
      Never performs an external action.
  grill DECISIONS.json
      Build the local wayfinding decision record from a decisions object.
  shot SHOT_RECORD.json MODEL_ID [--profile-version V]
      Build a complete model-neutral PromptPacket from a ShotRecord.
      Emits no model-specific syntax; compiled_prompt stays empty.

All output is JSON on stdout. This script reads files, writes nothing, and
never starts a generation, upload, purchase, or publication.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROUTES = {
    "concept": "wayfinding",
    "brief": "film-brief",
    "architecture": "production-architect",
    "assets": "asset-bible",
    "performance": "performance-bible",
    "geography": "geography-lock",
    "shots": "shot-direction",
    "adapter": "prompt-packet",
    "iteration": "iteration-supervisor",
    "finish": "post-delivery",
}

PLANNING_ACTIONS = {"plan", "draft", "validate"}
EXTERNAL_ACTIONS = {
    "paid_generation",
    "account_signin",
    "upload",
    "purchase",
    "destructive_replacement",
    "publication",
    "material_scope_expansion",
}
ALL_ACTIONS = PLANNING_ACTIONS | EXTERNAL_ACTIONS

REQUIRED_EVIDENCE = {
    "paid_generation": ("target_surface", "cost_preview", "approval_id"),
    "account_signin": ("account_or_surface", "approval_id"),
    "upload": ("destination", "files", "approval_id"),
    "purchase": ("vendor", "cost_preview", "approval_id"),
    "destructive_replacement": ("target", "recovery_plan", "approval_id"),
    "publication": ("destination", "visibility", "approval_id"),
    "material_scope_expansion": ("scope_delta", "cost_preview", "approval_id"),
}

FILM_GRILL_FIELDS = (
    "intent",
    "audience",
    "story",
    "runtime",
    "visual_language",
    "sound_language",
    "resources",
    "budget",
    "schedule",
    "rights",
    "target_models",
    "distribution",
    "risk",
    "approval_policy",
    "smallest_test_scene",
)

SHOT_PACKET_FIELDS = (
    "id",
    "scene_id",
    "purpose",
    "duration_seconds",
    "status",
    "target_model",
    "active_references",
    "geography",
    "first_frame",
    "action_beats",
    "performance",
    "camera",
    "lens",
    "light",
    "physics",
    "dialogue",
    "sound",
    "constraints",
)


def _stopped(packet_id: str, reason: str, **details: Any) -> Dict[str, Any]:
    return {
        "protocol": "film-advisor/v1",
        "packet_id": packet_id,
        "status": "stopped",
        "reason": reason,
        "details": details,
    }


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


# ---------------------------------------------------------------- route ---

def _validate_packet(packet: Any) -> Optional[str]:
    if not isinstance(packet, dict):
        return "packet_must_be_object"
    required = {
        "schema_version",
        "packet_id",
        "activation",
        "route",
        "project_root",
        "production_contract",
        "requested_actions",
    }
    if set(packet) != required:
        return "packet_keys_invalid"
    if packet.get("schema_version") != "ai-film-studio/film-advisor-packet/v1":
        return "invalid_schema_version"
    if not isinstance(packet.get("packet_id"), str) or not re.fullmatch(
        r"film_packet_[a-z0-9_]+", packet["packet_id"]
    ):
        return "invalid_packet_id"
    activation = packet.get("activation")
    if (
        not isinstance(activation, dict)
        or set(activation) != {"mode", "invocation"}
        or activation.get("mode") != "explicit"
        or activation.get("invocation") != "film-advisor"
    ):
        return "activation_not_explicit"
    if packet.get("route") not in ROUTES:
        return "unknown_route"
    if not _nonempty(packet.get("project_root")):
        return "invalid_project_root"
    contract = packet.get("production_contract")
    if (
        not isinstance(contract, dict)
        or set(contract) != {"status", "film_brief_id", "film_brief_sha256"}
    ):
        return "invalid_production_contract"
    if contract.get("status") not in {"draft", "approved"}:
        return "invalid_production_contract"
    if packet["route"] not in {"concept", "brief"} and (
        contract.get("status") != "approved"
        or not re.fullmatch(r"[a-f0-9]{64}", str(contract.get("film_brief_sha256", "")))
    ):
        return "production_contract_not_approved"
    actions = packet.get("requested_actions")
    if not isinstance(actions, list):
        return "invalid_requested_actions"
    for action in actions:
        if (
            not isinstance(action, dict)
            or set(action) != {"type", "target", "approval"}
            or action.get("type") not in ALL_ACTIONS
            or not _nonempty(action.get("target"))
        ):
            return "invalid_action"
        approval = action.get("approval")
        if (
            not isinstance(approval, dict)
            or set(approval) != {"status", "id", "action_type", "target", "evidence"}
            or approval.get("status") not in {"not_granted", "approved"}
            or not isinstance(approval.get("evidence"), dict)
        ):
            return "invalid_approval"
    return None


def _approval_error(action: Dict[str, Any]) -> Optional[str]:
    action_type, target, approval = action["type"], action["target"], action["approval"]
    if approval.get("status") != "approved" or not _nonempty(approval.get("id")):
        return "approval_not_granted"
    if approval.get("action_type") != action_type or approval.get("target") != target:
        return "approval_scope_mismatch"
    evidence = approval["evidence"]
    for field in REQUIRED_EVIDENCE[action_type]:
        value = evidence.get(field)
        if isinstance(value, list):
            if not value:
                return f"missing_{field}"
        elif not _nonempty(value):
            return f"missing_{field}"
    return None


def evaluate_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    """Return a route or a stop. Never performs an external action."""
    packet_id = (
        str(packet.get("packet_id", "unknown"))
        if isinstance(packet, dict)
        else "unknown"
    )
    error = _validate_packet(packet)
    if error:
        return _stopped(packet_id, error)
    for action in packet["requested_actions"]:
        if action["type"] in EXTERNAL_ACTIONS:
            approval_error = _approval_error(action)
            if approval_error:
                return _stopped(
                    packet_id,
                    "external_action_requires_approval",
                    action_type=action["type"],
                    target=action["target"],
                    approval_error=approval_error,
                    required_evidence=list(REQUIRED_EVIDENCE[action["type"]]),
                )
    return {
        "protocol": "film-advisor/v1",
        "packet_id": packet_id,
        "status": "accepted",
        "route": packet["route"],
        "station": ROUTES[packet["route"]],
        "authority": ["route", "request_record", "validate", "stop_on_gate"],
        "prohibited": sorted(EXTERNAL_ACTIONS),
    }


# ---------------------------------------------------------------- grill ---

def build_local_grill_state(decisions: Dict[str, Any]) -> Dict[str, Any]:
    """Build the local film decision record from a decisions object.

    Each FILM_GRILL_FIELDS entry should be {"decision": str,
    "alternatives": [...], "reason": str, "source": str, "next_proof": str}.
    "_assumptions" (dict) carries labelled assumptions.
    """
    if not isinstance(decisions, dict):
        return _stopped("film_grill", "decisions_must_be_object")
    decided: Dict[str, Any] = {}
    alternatives: Dict[str, Any] = {}
    decision_reasons: Dict[str, Any] = {}
    source_evidence: Dict[str, Any] = {}
    next_proof: Dict[str, Any] = {}
    open_fields: List[str] = []
    for field in FILM_GRILL_FIELDS:
        entry = decisions.get(field)
        if not isinstance(entry, dict) or not _nonempty(entry.get("decision")):
            open_fields.append(field)
            continue
        decided[field] = entry["decision"].strip()
        alternatives[field] = entry.get("alternatives", [])
        decision_reasons[field] = entry.get("reason", "")
        source_evidence[field] = entry.get("source", "user decision")
        next_proof[field] = entry.get("next_proof", "")
    assumptions = decisions.get("_assumptions", {})
    if not isinstance(assumptions, dict):
        assumptions = {}
    return {
        "protocol": "film-wayfinder/local-grill/v1",
        "status": "ready" if not open_fields else "needs_input",
        "decided": decided,
        "assumed": assumptions,
        "open": open_fields,
        "alternatives": alternatives,
        "decision_reasons": decision_reasons,
        "source_evidence": source_evidence,
        "next_proof": next_proof,
        "next_question": open_fields[0] if open_fields else None,
    }


# ----------------------------------------------------------------- shot ---

def build_model_neutral_shot_packet(
    shot_record: Dict[str, Any],
    model_id: str,
    profile_version: str = "unverified",
) -> Dict[str, Any]:
    """Build a complete normalized PromptPacket. No model-specific syntax."""
    if not isinstance(shot_record, dict):
        return _stopped("prompt_packet", "shot_record_must_be_object")
    missing = [field for field in SHOT_PACKET_FIELDS if field not in shot_record]
    if missing:
        return _stopped("prompt_packet", "shot_record_incomplete",
                        missing_fields=missing)
    shot_id = str(shot_record.get("id", ""))
    if not re.fullmatch(r"shot_[a-z0-9_]+", shot_id):
        return _stopped("prompt_packet", "invalid_shot_id")
    if not _nonempty(model_id):
        return _stopped("prompt_packet", "model_id_required")
    canonical = json.dumps(shot_record, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    shot_sha256 = hashlib.sha256(canonical).hexdigest()
    packet = {
        "schema_version": "ai-film-studio/PromptPacket/v1",
        "id": f"prompt_{shot_id.removeprefix('shot_')}",
        "shot_record_id": shot_id,
        "shot_record_sha256": shot_sha256,
        "model_profile_id": model_id,
        "model_profile_version": profile_version,
        "status": "local",
        "format_owner": "ai-film-studio:model-neutral",
        "normalized_shot_record": {
            field: shot_record[field] for field in SHOT_PACKET_FIELDS
        },
        "compiled_prompt": "",
        "validator_result": {
            "status": "unrun",
            "validator": "ai-film-studio:local-record-validator",
            "evidence": [],
        },
        "source_references": [
            {"path": f"records/{shot_id}.json", "sha256": shot_sha256}
        ],
        "prompt_sha256": "",
        "external_action_policy": "approval-required",
    }
    return {
        "protocol": "film-prompt/model-neutral/v1",
        "status": "complete_model_neutral",
        "prompt_packet": packet,
        "surface_note": (
            "Model-specific syntax is not emitted here. Verify the selected "
            "surface, version, controls, cost, and approval before any live use."
        ),
    }


# ------------------------------------------------------------------ cli ---

def _load_json(path: str) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"film_advisor: unable to read {path}: {error}", file=sys.stderr)
        raise SystemExit(2)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(prog="film_advisor.py")
    sub = parser.add_subparsers(dest="command", required=True)

    p_route = sub.add_parser("route", help="evaluate a film-advisor packet")
    p_route.add_argument("packet")

    p_grill = sub.add_parser("grill", help="build the local grill decision record")
    p_grill.add_argument("decisions")

    p_shot = sub.add_parser("shot", help="build a model-neutral prompt packet")
    p_shot.add_argument("shot_record")
    p_shot.add_argument("model_id")
    p_shot.add_argument("--profile-version", default="unverified")

    args = parser.parse_args(argv)
    if args.command == "route":
        result = evaluate_packet(_load_json(args.packet))
    elif args.command == "grill":
        result = build_local_grill_state(_load_json(args.decisions))
    else:
        result = build_model_neutral_shot_packet(
            _load_json(args.shot_record), args.model_id,
            profile_version=args.profile_version,
        )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
