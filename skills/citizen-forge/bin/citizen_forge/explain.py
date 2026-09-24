from typing import Any, Dict


PLAIN = {
    "UNAVAILABLE": "Citizen Forge cannot verify this protection in the current setup. It is not counted as passing.",
    "EXPERT_REVIEW_REQUIRED": "This application can affect sensitive information, outside users, or hard-to-reverse actions. A qualified reviewer must decide the next step.",
    "REUSE_RECOMMENDED": "A similar application already exists. Contact its owner before creating another one.",
    "RELEASE_BLOCKED": "The application is not ready. One or more required protections do not yet have passing evidence.",
    "TRANSFER_REQUIRED": "The application does not have enough active ownership. Changes and releases are restricted until ownership is restored.",
}


def explain(code: str, details: Dict[str, Any] = None) -> Dict[str, Any]:
    impact = PLAIN.get(code, "Citizen Forge recorded a technical decision.")
    return {"what_happened": impact, "impact": "No blocked operation was performed.", "safest_next_action": (details or {}).get("required_next_action", "Review the named evidence and repair recommendation."), "state_changed": False}
