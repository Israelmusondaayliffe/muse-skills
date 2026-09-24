import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .models import State
from .schemas import BRIEF_FIELDS, validate_brief
from .storage import atomic_write_json, project_lock


QUESTION_ORDER = [
    ("problem", "What problem should this solve?", "This keeps the build focused on a real need."),
    ("outcome", "What should be easier or possible when it works?", "This defines what success means."),
    ("current_process", "How do you handle this today?", "This shows what the app must replace or support."),
    ("intended_users", "Who will use or depend on it?", "People relying on the result change the safety requirements."),
    ("expected_users", "About how many people will use it?", "Shared software needs stronger protection."),
    ("second_consumer", "Will anyone besides you open, run, depend on, or directly use this?", "A second consumer moves the app into the managed lifecycle."),
    ("primary_owner", "Who is responsible for this app?", "Someone must be able to answer questions and act when it fails."),
    ("backup_owner", "Who can take over if the primary owner is unavailable?", "Shared apps cannot rely on one person forever."),
    ("data_sources", "What information will the app read?", "Data source and sensitivity determine the safe route."),
    ("access", "Will it only read information, or will it also change information?", "Writes can affect other people and may need approval."),
    ("data_sensitivity", "Is the information public, internal, confidential, financial, personal, regulated, or secret?", "More sensitive information needs stricter handling."),
    ("external_exposure", "Can anyone outside your organization use or see it?", "External use does not qualify for automatic citizen release."),
    ("automation_level", "Does a person start each action, or can it act on its own?", "Autonomous actions can create a larger impact."),
    ("reversibility", "If it makes a mistake, can the result be fully undone?", "Safe failure requires a practical recovery path."),
    ("frequency", "How often will it be used?", "Frequent use can increase the impact of a mistake."),
    ("failure_consequence", "What happens if it is wrong or unavailable?", "Consequential failures need professional review."),
    ("overlap", "What existing tools might already do this?", "Reusing an owned application is safer than creating a duplicate."),
    ("shape", "Which description fits best: document generator, workflow automation, internal data app, dashboard, personal analysis, or unknown?", "The approved architecture depends on the application shape."),
    ("confidence", "How confident is the proposed shape, from zero to one?", "Uncertain classifications cannot approve themselves."),
]


def missing_questions(partial: Dict[str, Any]) -> List[Dict[str, str]]:
    return [{"field": field, "question": question, "why": why} for field, question, why in QUESTION_ORDER if field not in partial or partial[field] in (None, "")]


def normalize_brief(value: Dict[str, Any]) -> Dict[str, Any]:
    brief = dict(value)
    brief["expected_users"] = int(brief["expected_users"])
    brief["second_consumer"] = bool(brief["second_consumer"]) or brief["expected_users"] > 1 or len(str(brief["intended_users"]).split(",")) > 1
    aliases = {
        "document generator": "artifact-generator",
        "artifact generator": "artifact-generator",
        "workflow automation": "workflow-automation",
        "internal data app": "crud-internal-app",
        "dashboard": "interactive-dashboard",
        "personal analysis": "personal-analysis",
        "unknown": "novel-or-unknown",
    }
    brief["shape"] = aliases.get(str(brief["shape"]).lower(), brief["shape"])
    brief["confidence"] = float(brief["confidence"])
    validate_brief(brief)
    return brief


def brief_markdown(brief: Dict[str, Any]) -> str:
    lines = ["# Application brief", "", "Confirmed facts:"]
    labels = {field: field.replace("_", " ").capitalize() for field in BRIEF_FIELDS}
    for field in BRIEF_FIELDS:
        lines.append("- {}: {}".format(labels[field], brief[field]))
    lines.extend(["", "Safety note: the application will be reclassified if its users, data, exposure, write access, automation, or recovery changes.", ""])
    return "\n".join(lines)


def initialize_project(project_root: Path, value: Dict[str, Any], confirmed: bool = False) -> Dict[str, Any]:
    brief = normalize_brief(value)
    citizen = project_root / ".citizen"
    with project_lock(citizen):
        for name in ("releases", "changes", "exceptions", "evidence", "generated-docs", "backups", "audit"):
            (citizen / name).mkdir(parents=True, exist_ok=True)
        atomic_write_json(citizen / "brief.json", brief, citizen / "backups")
        (citizen / "brief.md").write_text(brief_markdown(brief), encoding="utf-8")
        ownership = {"primary_owner": brief["primary_owner"], "backup_owner": brief["backup_owner"], "valid": bool(brief["primary_owner"]) and (not brief["second_consumer"] or bool(brief["backup_owner"]))}
        atomic_write_json(citizen / "ownership.json", ownership, citizen / "backups")
        app_id = hashlib.sha256((brief["name"] + "|" + brief["primary_owner"]).encode("utf-8")).hexdigest()[:16]
        app = {"app_id": app_id, "name": brief["name"], "created_at": datetime.now(timezone.utc).isoformat(), "brief_fingerprint": hashlib.sha256(json.dumps(brief, sort_keys=True).encode("utf-8")).hexdigest()}
        atomic_write_json(citizen / "app.json", app, citizen / "backups")
        atomic_write_json(citizen / "state.json", {"state": State.IDEA_DRAFT.value, "brief_confirmed": bool(confirmed), "updated_at": datetime.now(timezone.utc).isoformat()}, citizen / "backups")
    return app
