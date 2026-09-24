from typing import Any, Dict, Iterable, List


CONSEQUENTIAL = {
    "destructive migration": ("delete data", "drop table", "destructive migration"),
    "infrastructure": ("new infrastructure", "cloud resource"),
    "authentication": ("authentication", "login", "sso"),
    "authorization": ("authorization", "permission", "role"),
    "external data": ("new data source", "external data"),
    "dependency": ("new dependency", "add package"),
    "network": ("new network", "outbound destination", "api endpoint"),
    "secret handling": ("secret", "credential", "api key"),
    "policy": ("policy", "paved road", "constraint", "guardrail"),
    "exposure": ("public", "customer", "external user"),
    "sensitivity": ("financial", "personal data", "regulated", "restricted"),
    "autonomy": ("autonomous", "scheduled action", "without confirmation"),
    "irreversibility": ("irreversible", "cannot undo"),
    "ownership": ("remove owner", "no backup owner"),
    "recovery": ("disable backup", "disable audit"),
}


def classify(description: str, changed_paths: Iterable[str] = ()) -> Dict[str, Any]:
    text = (description + " " + " ".join(changed_paths)).lower()
    reasons = [name for name, patterns in CONSEQUENTIAL.items() if any(pattern in text for pattern in patterns)]
    return {"classification": "CONSEQUENTIAL" if reasons else "ROUTINE", "reasons": reasons, "human_gate_required": bool(reasons), "retriage_required": any(reason in reasons for reason in ("external data", "exposure", "sensitivity", "autonomy", "authentication", "authorization"))}
