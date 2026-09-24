import re
from typing import Any, Dict, Iterable, List


def _tokens(value: str) -> set:
    return {token for token in re.findall(r"[a-z0-9]+", value.lower()) if len(token) > 2}


def similarity(left: Dict[str, Any], right: Dict[str, Any]) -> float:
    a = _tokens(" ".join(str(left.get(key, "")) for key in ("name", "problem", "outcome", "data_sources")))
    b = _tokens(" ".join(str(right.get(key, "")) for key in ("name", "problem", "outcome", "data_sources")))
    return len(a & b) / len(a | b) if a | b else 0.0


def candidates(brief: Dict[str, Any], entries: Iterable[Dict[str, Any]], threshold: float = 0.45) -> List[Dict[str, Any]]:
    found = []
    for entry in entries:
        score = similarity(brief, entry)
        if score >= threshold:
            found.append({"app_id": entry.get("app_id"), "name": entry.get("name"), "owner": entry.get("primary_owner"), "similarity": round(score, 3)})
    return sorted(found, key=lambda item: item["similarity"], reverse=True)
