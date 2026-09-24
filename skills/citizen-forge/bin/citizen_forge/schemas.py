from typing import Any, Dict, Iterable

from .errors import ValidationError


BRIEF_FIELDS = (
    "name", "problem", "outcome", "current_process", "intended_users",
    "expected_users", "second_consumer", "primary_owner", "backup_owner",
    "data_sources", "access", "data_sensitivity", "external_exposure",
    "automation_level", "reversibility", "frequency", "failure_consequence",
    "overlap", "shape", "confidence",
)


def require_fields(data: Dict[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in data or data[field] in (None, "")]
    if missing:
        raise ValidationError("{} is missing: {}".format(label, ", ".join(missing)))


def validate_brief(brief: Dict[str, Any]) -> None:
    require_fields(brief, BRIEF_FIELDS, "The application brief")
    if not isinstance(brief["expected_users"], int) or brief["expected_users"] < 1:
        raise ValidationError("Expected users must be a whole number of at least one.")
    if not isinstance(brief["second_consumer"], bool):
        raise ValidationError("Second-consumer status must be yes or no.")
    if not 0 <= float(brief["confidence"]) <= 1:
        raise ValidationError("Classification confidence must be between zero and one.")


def validate_scores(scores: Dict[str, Any]) -> None:
    required = ("reach", "reversibility", "exposure", "data_sensitivity")
    require_fields(scores, required, "Risk facts")
    if any(not isinstance(scores[key], int) or not 0 <= scores[key] <= 4 for key in required):
        raise ValidationError("Each risk score must be a whole number from zero to four.")


def validate_check_result(result: Dict[str, Any]) -> None:
    require_fields(result, ("check_id", "severity", "status", "evidence", "explanation", "repair", "ai_may_repair", "human_decision_required"), "Check result")
    if result["status"] not in {"PASS", "FAIL", "BLOCKED", "NOT_APPLICABLE", "UNAVAILABLE"}:
        raise ValidationError("The check returned an unknown status.")
