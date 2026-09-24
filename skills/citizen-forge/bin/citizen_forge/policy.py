import json
from pathlib import Path
from typing import Any, Dict, Optional

from .errors import PolicyError
from .risk import SHAPES, score
from .schemas import validate_brief, validate_scores


ROUTE_PROTOTYPE = "PROTOTYPE_ONLY"
ROUTE_APPROVED = "APPROVED_PAVED_ROAD"
ROUTE_REUSE = "REUSE_RECOMMENDED"
ROUTE_REVIEW = "EXPERT_REVIEW_REQUIRED"


def load_policy(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError("The policy cannot be verified, so approval is blocked: {}".format(exc))
    if value.get("version") is None or value.get("max_auto_score") is None:
        raise PolicyError("The policy is incomplete, so approval is blocked.")
    return value


def decide(brief: Dict[str, Any], scores: Dict[str, int], policy: Dict[str, Any], duplicate: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    validate_brief(brief)
    validate_scores(scores)
    facts = {"scores": scores, "total": score(scores), "second_consumer": brief["second_consumer"], "expected_users": brief["expected_users"], "shape": brief["shape"]}
    if duplicate and duplicate.get("confirmed"):
        route, rule, action = ROUTE_REUSE, "confirmed_duplicate", "Contact the existing owner before creating another application."
    elif brief["shape"] not in SHAPES or brief["shape"] == "novel-or-unknown":
        route, rule, action = ROUTE_REVIEW, "unknown_shape", "Ask a qualified engineer to choose an architecture."
    elif float(brief["confidence"]) < float(policy["minimum_confidence"]):
        route, rule, action = ROUTE_REVIEW, "low_confidence", "A qualified reviewer must confirm the classification."
    elif max(scores.values()) >= 4:
        route, rule, action = ROUTE_REVIEW, "critical_dimension", "Professional engineering review is required."
    elif max(scores.values()) >= 3:
        route, rule, action = ROUTE_REVIEW, "elevated_dimension", "A qualified human reviewer must decide the next step."
    elif any(token in str(brief["external_exposure"]).lower() for token in ("public", "customer", "external", "investor")):
        route, rule, action = ROUTE_REVIEW, "external_use", "Professional engineering review is required."
    elif not brief["second_consumer"] and brief["expected_users"] == 1 and scores["reach"] <= 1:
        route, rule, action = ROUTE_PROTOTYPE, "sole_consumer", "Continue locally with prototype protections."
    elif score(scores) <= int(policy["max_auto_score"]):
        route, rule, action = ROUTE_APPROVED, "within_threshold", "Select the matching approved paved road."
    else:
        route, rule, action = ROUTE_REVIEW, "total_above_threshold", "A qualified reviewer must decide the next step."
    return {"facts": facts, "ai_recommendation": brief["shape"], "deterministic_rule": rule, "confidence": brief["confidence"], "policy_version": policy["version"], "final_route": route, "required_next_action": action}
