import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .models import AdapterReport
from .storage import atomic_write_json, confined, project_lock, read_json


ADAPTERS = ("git", "ci", "identity", "secret-manager", "database", "cloud-runtime", "infrastructure-as-code", "approval", "application-catalog", "observability", "usage-analytics", "backup")


def adapter_reports(configured: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    reports = []
    for name in ADAPTERS:
        value = configured.get(name, {})
        reports.append(AdapterReport(name, bool(value.get("available")), bool(value.get("authenticated")), list(value.get("actions", [])), list(value.get("permissions", [])), bool(value.get("dry_run")), str(value.get("verification", "No verified adapter is configured."))).to_dict())
    return reports


def plan(project_root: Path, road: Dict[str, Any], configured: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    reports = adapter_reports(configured)
    production_ready = all(item["available"] and item["authenticated"] for item in reports if item["name"] in road.get("production_adapters", []))
    return {
        "road": road["name"],
        "road_version": road["version"],
        "creates": road["scaffold_files"],
        "requires_credentials": road.get("production_adapters", []),
        "human_authorization": ["production writes", "production provisioning"],
        "unavailable": [item["name"] for item in reports if not item["available"]],
        "local_only": not production_ready,
        "adapters": reports,
    }


def provision(project_root: Path, road_root: Path, plan_value: Dict[str, Any]) -> Dict[str, Any]:
    citizen = project_root / ".citizen"
    with project_lock(citizen):
        for relative in plan_value["creates"]:
            source = confined(road_root, road_root / relative)
            target = confined(project_root, project_root / relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_file() and not target.exists():
                shutil.copy2(str(source), str(target))
        atomic_write_json(citizen / "provisioning-plan.json", plan_value, citizen / "backups")
        result = {"created": [path for path in plan_value["creates"] if (project_root / path).exists()], "local_only": plan_value["local_only"], "production_provisioned": False, "evidence": ["Files verified inside the selected project root."]}
        atomic_write_json(citizen / "provisioning-result.json", result, citizen / "backups")
        atomic_write_json(citizen / "environment-posture.json", {"local_only": plan_value["local_only"], "adapters": plan_value["adapters"]}, citizen / "backups")
    return result
