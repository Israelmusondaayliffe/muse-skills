from typing import Any, Dict

from .schemas import validate_brief, validate_scores


SHAPES = {"artifact-generator", "workflow-automation", "crud-internal-app", "interactive-dashboard", "personal-analysis", "novel-or-unknown"}


def infer_scores(brief: Dict[str, Any]) -> Dict[str, int]:
    validate_brief(brief)
    access = str(brief["access"]).lower()
    users = int(brief["expected_users"])
    reach = 0 if users == 1 and "read" in access else 1 if "read" in access else 2
    automation = str(brief["automation_level"]).lower()
    reversible = str(brief["reversibility"]).lower()
    if any(marker in reversible for marker in ("irreversible", "cannot undo", "not reversible")):
        reversibility = 3
    elif "human" in automation and "fully reversible" in reversible:
        reversibility = 0
    elif "reversible" in reversible:
        reversibility = 2
    else:
        reversibility = 3
    exposure_text = str(brief["external_exposure"]).lower()
    exposure = 4 if "public" in exposure_text or "customer" in exposure_text else 3 if "external" in exposure_text or "investor" in exposure_text else 0 if users == 1 else 1
    sensitivity_text = str(brief["data_sensitivity"]).lower()
    if any(word in sensitivity_text for word in ("regulated", "medical", "credential", "secret", "biometric")):
        sensitivity = 4
    elif any(word in sensitivity_text for word in ("financial", "personnel", "personal", "restricted", "investor")):
        sensitivity = 3
    elif "confidential" in sensitivity_text:
        sensitivity = 2
    elif "internal" in sensitivity_text:
        sensitivity = 1
    else:
        sensitivity = 0
    return {"reach": reach, "reversibility": reversibility, "exposure": exposure, "data_sensitivity": sensitivity}


def score(scores: Dict[str, int]) -> int:
    validate_scores(scores)
    return sum(scores.values())
