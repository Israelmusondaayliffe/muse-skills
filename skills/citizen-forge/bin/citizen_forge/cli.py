import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

from .audit import verify_chain
from .catalog import register
from .change_classifier import classify
from .checks import run_all
from .errors import CitizenForgeError
from .explain import explain
from .intake import initialize_project, missing_questions
from .policy import decide, load_policy
from .provision import plan as provisioning_plan, provision
from .release import decide_release
from .risk import infer_scores
from .roads import select
from .storage import atomic_write_json, read_json


PLUGIN_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = PLUGIN_ROOT / "policies" / "default-policy.json"
ROADS_ROOT = PLUGIN_ROOT / "assets" / "roads"


def emit(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def command_idea(args: argparse.Namespace) -> None:
    value = json.loads(Path(args.brief).read_text(encoding="utf-8"))
    missing = missing_questions(value)
    if missing:
        emit({"status": "QUESTION_REQUIRED", "next_question": missing[0]})
        return
    emit(initialize_project(Path(args.project).resolve(), value, confirmed=args.confirmed))


def command_triage(args: argparse.Namespace) -> None:
    root = Path(args.project).resolve()
    brief = read_json(root / ".citizen" / "brief.json")
    scores = infer_scores(brief)
    decision = decide(brief, scores, load_policy(DEFAULT_POLICY))
    atomic_write_json(root / ".citizen" / "triage.json", {"scores": scores}, root / ".citizen" / "backups")
    atomic_write_json(root / ".citizen" / "decision.json", decision, root / ".citizen" / "backups")
    emit(decision)


def command_register(args: argparse.Namespace) -> None:
    emit(register(Path(args.project).resolve(), Path(args.catalog).resolve() if args.catalog else None))


def command_provision(args: argparse.Namespace) -> None:
    root = Path(args.project).resolve()
    brief = read_json(root / ".citizen" / "brief.json")
    road = select(brief["shape"], ROADS_ROOT)
    value = provisioning_plan(root, road, {})
    road_root = ROADS_ROOT / road["name"]
    emit(provision(root, road_root, value))


def command_check(args: argparse.Namespace) -> None:
    root = Path(args.project).resolve()
    brief = read_json(root / ".citizen" / "brief.json")
    checks = run_all(root, load_policy(DEFAULT_POLICY), brief)
    emit([item.to_dict() for item in checks])


def command_release(args: argparse.Namespace) -> None:
    root = Path(args.project).resolve()
    brief = read_json(root / ".citizen" / "brief.json")
    checks = run_all(root, load_policy(DEFAULT_POLICY), brief)
    change = classify(args.change)
    emit(decide_release(checks, change))


def command_explain(args: argparse.Namespace) -> None:
    emit(explain(args.code))


def command_verify_audit(args: argparse.Namespace) -> None:
    emit({"valid": verify_chain(Path(args.project).resolve() / ".citizen" / "audit" / "events.jsonl")})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="citizen-forge", description="Deterministic governance for beginner-owned internal applications.")
    sub = parser.add_subparsers(dest="command", required=True)
    idea = sub.add_parser("idea")
    idea.add_argument("--project", required=True)
    idea.add_argument("--brief", required=True)
    idea.add_argument("--confirmed", action="store_true")
    idea.set_defaults(func=command_idea)
    registration = sub.add_parser("register")
    registration.add_argument("--project", required=True)
    registration.add_argument("--catalog")
    registration.set_defaults(func=command_register)
    triage = sub.add_parser("triage")
    triage.add_argument("--project", required=True)
    triage.set_defaults(func=command_triage)
    provisioning = sub.add_parser("provision")
    provisioning.add_argument("--project", required=True)
    provisioning.set_defaults(func=command_provision)
    checks = sub.add_parser("check")
    checks.add_argument("--project", required=True)
    checks.set_defaults(func=command_check)
    release = sub.add_parser("release")
    release.add_argument("--project", required=True)
    release.add_argument("--change", default="initial release")
    release.set_defaults(func=command_release)
    explanation = sub.add_parser("explain")
    explanation.add_argument("code")
    explanation.set_defaults(func=command_explain)
    audit = sub.add_parser("verify-audit")
    audit.add_argument("--project", required=True)
    audit.set_defaults(func=command_verify_audit)
    return parser


def main(argv=None) -> int:
    try:
        args = build_parser().parse_args(argv)
        args.func(args)
        return 0
    except (CitizenForgeError, ValueError, OSError, json.JSONDecodeError) as exc:
        emit({"status": "BLOCKED", "what_happened": str(exc), "safest_next_action": "Fix the named input or evidence, then retry."})
        return 2
