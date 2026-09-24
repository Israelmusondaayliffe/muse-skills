#!/usr/bin/env python3
"""Validate a Guide Production Studio contract without judging prose quality."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA = "guide-production-studio/guide-contract/v1"
ROOT_FIELDS = {
    "schema_version", "id", "title", "audience", "reader_job", "outcome",
    "format", "visual_requirement", "sources", "concepts", "evidence",
    "examples", "visuals", "architecture", "boundaries", "publication",
    "acceptance", "limits",
}
GATES = [
    "purpose", "context", "vocabulary", "action", "evidence",
    "provenance_privacy", "examples_reuse", "troubleshooting",
    "structure_visuals", "voice_value",
]
SOURCE_CLASSES = {
    "public-attributable", "public-reference", "private-transform-only",
    "user-owned", "forbidden",
}
EVIDENCE_STATES = {"verified", "user-supplied", "observed", "unrun", "unknown"}
MODES = {"single-page", "layered-page", "parent-with-children"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any, label: str, errors: list[str], *, required: bool = False) -> list[str]:
    if not isinstance(value, list) or any(not nonempty(item) for item in value):
        errors.append(f"{label} must be a list of non-empty strings")
        return []
    if required and not value:
        errors.append(f"{label} must not be empty")
    if len(value) != len(set(value)):
        errors.append(f"{label} must not contain duplicates")
    return value


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["contract root must be an object"]
    if set(data) != ROOT_FIELDS:
        errors.append(
            f"contract fields mismatch: missing={sorted(ROOT_FIELDS - set(data))} "
            f"extra={sorted(set(data) - ROOT_FIELDS)}"
        )
    if data.get("schema_version") != SCHEMA:
        errors.append(f"schema_version must be {SCHEMA}")
    for field in ("id", "title", "reader_job", "outcome"):
        if not nonempty(data.get(field)) or "replace-with" in str(data.get(field, "")):
            errors.append(f"{field} must be resolved")

    audience = data.get("audience")
    if not isinstance(audience, dict) or set(audience) != {"primary", "starting_point", "expert_value"}:
        errors.append("audience must contain primary, starting_point, and expert_value")
    else:
        for field, value in audience.items():
            if not nonempty(value):
                errors.append(f"audience.{field} must be a non-empty string")

    if data.get("format") not in MODES:
        errors.append(f"format must be one of {sorted(MODES)}")
    if data.get("visual_requirement") not in {"required", "not-required", "reference-only", "awaiting-evidence"}:
        errors.append("visual_requirement is invalid")

    sources = data.get("sources")
    source_ids: set[str] = set()
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
        sources = []
    for index, source in enumerate(sources):
        required = {
            "id", "title", "location", "classification", "authority",
            "permitted_public_use", "required_attribution", "current_verification",
        }
        if not isinstance(source, dict) or set(source) != required:
            errors.append(f"sources[{index}] has invalid fields")
            continue
        if not nonempty(source.get("id")) or source["id"] in source_ids:
            errors.append(f"sources[{index}].id must be unique and non-empty")
        else:
            source_ids.add(source["id"])
        for field in ("title", "location", "authority", "current_verification"):
            if not nonempty(source.get(field)):
                errors.append(f"sources[{index}].{field} must be non-empty")
        if source.get("classification") not in SOURCE_CLASSES:
            errors.append(f"sources[{index}].classification is invalid")
        for field in ("permitted_public_use", "required_attribution"):
            if not isinstance(source.get(field), bool):
                errors.append(f"sources[{index}].{field} must be boolean")

    concepts = data.get("concepts")
    if not isinstance(concepts, list) or not concepts:
        errors.append("concepts must contain at least one explained term")
    else:
        for index, concept in enumerate(concepts):
            if not isinstance(concept, dict) or set(concept) != {"term", "plain_definition", "source_ids"}:
                errors.append(f"concepts[{index}] has invalid fields")
                continue
            if not nonempty(concept.get("term")) or not nonempty(concept.get("plain_definition")):
                errors.append(f"concepts[{index}] must define a term in plain language")
            refs = string_list(concept.get("source_ids"), f"concepts[{index}].source_ids", errors, required=True)
            if any(ref not in source_ids for ref in refs):
                errors.append(f"concepts[{index}] references an unknown source")

    evidence = data.get("evidence")
    evidence_ids: set[str] = set()
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
        evidence = []
    for index, item in enumerate(evidence):
        required = {"id", "claim_or_method", "source_ids", "status", "public_use"}
        if not isinstance(item, dict) or set(item) != required:
            errors.append(f"evidence[{index}] has invalid fields")
            continue
        if not nonempty(item.get("id")) or item["id"] in evidence_ids:
            errors.append(f"evidence[{index}].id must be unique and non-empty")
        else:
            evidence_ids.add(item["id"])
        if not nonempty(item.get("claim_or_method")):
            errors.append(f"evidence[{index}].claim_or_method must be non-empty")
        refs = string_list(item.get("source_ids"), f"evidence[{index}].source_ids", errors, required=True)
        if any(ref not in source_ids for ref in refs):
            errors.append(f"evidence[{index}] references an unknown source")
        if item.get("status") not in EVIDENCE_STATES:
            errors.append(f"evidence[{index}].status is invalid")
        if not isinstance(item.get("public_use"), bool):
            errors.append(f"evidence[{index}].public_use must be boolean")

    examples = data.get("examples")
    if not isinstance(examples, list) or not examples:
        errors.append("examples must contain at least one real or clearly bounded example")
        examples = []
    for index, item in enumerate(examples):
        required = {"id", "evidence_ids", "kind", "run_status", "public_use"}
        if not isinstance(item, dict) or set(item) != required:
            errors.append(f"examples[{index}] has invalid fields")
            continue
        if not nonempty(item.get("id")):
            errors.append(f"examples[{index}].id must be non-empty")
        refs = string_list(item.get("evidence_ids"), f"examples[{index}].evidence_ids", errors, required=True)
        if any(ref not in evidence_ids for ref in refs):
            errors.append(f"examples[{index}] references unknown evidence")
        if item.get("kind") not in {"real", "planning-only"}:
            errors.append(f"examples[{index}].kind is invalid")
        if item.get("run_status") not in EVIDENCE_STATES:
            errors.append(f"examples[{index}].run_status is invalid")
        if not isinstance(item.get("public_use"), bool):
            errors.append(f"examples[{index}].public_use must be boolean")

    visuals = data.get("visuals")
    if not isinstance(visuals, list):
        errors.append("visuals must be a list")
        visuals = []
    if data.get("visual_requirement") == "required" and not visuals:
        errors.append("visual evidence is required but visuals is empty")
    for index, item in enumerate(visuals):
        required = {"id", "kind", "source_ids", "inspection_job", "public_use"}
        if not isinstance(item, dict) or set(item) != required:
            errors.append(f"visuals[{index}] has invalid fields")
            continue
        if not nonempty(item.get("id")) or not nonempty(item.get("inspection_job")):
            errors.append(f"visuals[{index}] must have id and inspection_job")
        refs = string_list(item.get("source_ids"), f"visuals[{index}].source_ids", errors, required=True)
        if any(ref not in source_ids for ref in refs):
            errors.append(f"visuals[{index}] references an unknown source")
        visual_kinds = {
            "comparison", "crop", "frame-sequence", "contact-sheet",
            "diagram", "screenshot", "clip",
        }
        if item.get("kind") not in visual_kinds:
            errors.append(f"visuals[{index}].kind is invalid")
        if not isinstance(item.get("public_use"), bool):
            errors.append(f"visuals[{index}].public_use must be boolean")

    architecture = data.get("architecture")
    if not isinstance(architecture, dict) or set(architecture) != {"mode", "pages", "components"}:
        errors.append("architecture must contain mode, pages, and components")
    else:
        if architecture.get("mode") != data.get("format"):
            errors.append("architecture.mode must match format")
        pages = architecture.get("pages")
        if not isinstance(pages, list) or not pages:
            errors.append("architecture.pages must be a non-empty list")
        else:
            for index, page in enumerate(pages):
                if not isinstance(page, dict) or set(page) != {"id", "title", "reader_job"}:
                    errors.append(f"architecture.pages[{index}] has invalid fields")
                elif not all(nonempty(page.get(field)) for field in ("id", "title", "reader_job")):
                    errors.append(f"architecture.pages[{index}] fields must be non-empty")
        components = architecture.get("components")
        if not isinstance(components, list) or not components:
            errors.append("architecture.components must be a non-empty list")
        else:
            for index, component in enumerate(components):
                required = {
                    "id", "kind", "reader_problem", "action_enabled",
                    "source_ids", "why_it_belongs", "required",
                }
                if not isinstance(component, dict) or set(component) != required:
                    errors.append(f"architecture.components[{index}] has invalid fields")
                    continue
                for field in ("id", "kind", "reader_problem", "action_enabled", "why_it_belongs"):
                    if not nonempty(component.get(field)):
                        errors.append(f"architecture.components[{index}].{field} must be non-empty")
                refs = string_list(
                    component.get("source_ids"),
                    f"architecture.components[{index}].source_ids",
                    errors,
                    required=True,
                )
                if any(ref not in source_ids for ref in refs):
                    errors.append(f"architecture.components[{index}] references an unknown source")
                if not isinstance(component.get("required"), bool):
                    errors.append(f"architecture.components[{index}].required must be boolean")

    boundaries = data.get("boundaries")
    boundary_fields = {
        "public_allowed", "private_excluded", "unsupported_forbidden",
    }
    if not isinstance(boundaries, dict) or set(boundaries) != boundary_fields:
        errors.append("boundaries has invalid fields")
    else:
        for field in boundaries:
            string_list(boundaries[field], f"boundaries.{field}", errors, required=True)

    publication = data.get("publication")
    if not isinstance(publication, dict) or set(publication) != {"authorized", "destination"}:
        errors.append("publication has invalid fields")
    elif publication.get("authorized") is not False or publication.get("destination") is not None:
        errors.append("guide production contract must not authorize publication")

    acceptance = data.get("acceptance")
    required_acceptance = {"human_owner", "required_gates", "cold_reader_required_before_scale", "bulk_scale_allowed"}
    if not isinstance(acceptance, dict) or set(acceptance) != required_acceptance:
        errors.append("acceptance has invalid fields")
    else:
        if not nonempty(acceptance.get("human_owner")):
            errors.append("acceptance.human_owner must be non-empty")
        if acceptance.get("required_gates") != GATES:
            errors.append("acceptance.required_gates must contain the ten ordered gates")
        if acceptance.get("cold_reader_required_before_scale") is not True:
            errors.append("cold reader must be required before scale")
        if acceptance.get("bulk_scale_allowed") is not False:
            errors.append("bulk scale must remain blocked in the guide contract")

    limits = data.get("limits")
    if not isinstance(limits, dict) or set(limits) != {"max_internal_support_artifacts", "max_repair_waves"}:
        errors.append("limits has invalid fields")
    else:
        if limits.get("max_internal_support_artifacts") != 2:
            errors.append("max_internal_support_artifacts must be 2")
        if limits.get("max_repair_waves") != 1:
            errors.append("max_repair_waves must be 1")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.contract.read_text(encoding="utf-8"))
        errors = validate(data)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
