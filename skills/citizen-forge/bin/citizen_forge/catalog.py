import json
from pathlib import Path
from typing import Any, Dict, List

from .duplicates import candidates
from .storage import atomic_write_json, read_json


def load_catalog(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"entries": [], "scope": "project-only"}
    value = read_json(path)
    if not isinstance(value.get("entries"), list):
        value["entries"] = []
    return value


def register(project_root: Path, catalog_path: Path = None) -> Dict[str, Any]:
    citizen = project_root / ".citizen"
    app = read_json(citizen / "app.json")
    brief = read_json(citizen / "brief.json")
    target = catalog_path or citizen / "catalog.json"
    catalog = load_catalog(target)
    overlap = candidates(brief, catalog["entries"])
    if not any(entry.get("app_id") == app["app_id"] for entry in catalog["entries"]):
        catalog["entries"].append({**app, "problem": brief["problem"], "outcome": brief["outcome"], "data_sources": brief["data_sources"], "primary_owner": brief["primary_owner"], "consumer_status": "shared" if brief["second_consumer"] else "personal"})
        atomic_write_json(target, catalog, citizen / "backups")
    return {"catalog_path": str(target), "scope": catalog.get("scope", "workspace"), "duplicate_candidates": overlap}
