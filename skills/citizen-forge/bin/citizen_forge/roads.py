import json
from pathlib import Path
from typing import Any, Dict, List

from .errors import PolicyError


ROAD_BY_SHAPE = {
    "artifact-generator": "python-artifact-generator",
    "workflow-automation": "python-workflow-automation",
    "crud-internal-app": "python-internal-crud",
    "interactive-dashboard": "python-interactive-dashboard",
    "personal-analysis": "python-artifact-generator",
}


def load_roads(roads_root: Path) -> Dict[str, Dict[str, Any]]:
    values = {}
    for road_file in roads_root.glob("*/road.json"):
        value = json.loads(road_file.read_text(encoding="utf-8"))
        if value.get("name") != road_file.parent.name or not value.get("version"):
            raise PolicyError("The paved-road registry is invalid.")
        values[value["name"]] = value
    return values


def select(shape: str, roads_root: Path) -> Dict[str, Any]:
    name = ROAD_BY_SHAPE.get(shape)
    roads = load_roads(roads_root)
    if name is None or name not in roads:
        raise PolicyError("No approved paved road exists for this application shape.")
    return roads[name]
