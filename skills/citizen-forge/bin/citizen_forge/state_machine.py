from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Set

from .audit import append_event, verify_chain
from .errors import TransitionError
from .models import State
from .storage import atomic_write_json, project_lock, read_json


ALLOWED: Dict[State, Set[State]] = {
    State.IDEA_DRAFT: {State.PROTOTYPE_ONLY, State.REGISTERED, State.EXPERT_REVIEW_REQUIRED},
    State.PROTOTYPE_ONLY: {State.REGISTERED, State.CHANGE_PENDING, State.RETIRED},
    State.REGISTERED: {State.TRIAGE_PENDING, State.TRANSFER_REQUIRED},
    State.TRIAGE_PENDING: {State.APPROVED, State.REUSE_RECOMMENDED, State.EXPERT_REVIEW_REQUIRED},
    State.APPROVED: {State.PROVISIONING_PLANNED, State.CHANGE_PENDING, State.TRANSFER_REQUIRED},
    State.PROVISIONING_PLANNED: {State.PROVISIONED, State.RELEASE_BLOCKED},
    State.PROVISIONED: {State.BUILDING, State.RELEASE_BLOCKED},
    State.BUILDING: {State.RELEASE_CANDIDATE, State.RELEASE_BLOCKED, State.CHANGE_PENDING},
    State.RELEASE_CANDIDATE: {State.RUNNING, State.RELEASE_BLOCKED},
    State.RELEASE_BLOCKED: {State.BUILDING, State.CHANGE_PENDING, State.TRANSFER_REQUIRED},
    State.RUNNING: {State.CHANGE_PENDING, State.ARCHIVE_RECOMMENDED, State.TRANSFER_REQUIRED},
    State.CHANGE_PENDING: {State.TRIAGE_PENDING, State.BUILDING, State.RELEASE_BLOCKED},
    State.ARCHIVE_RECOMMENDED: {State.RUNNING, State.ARCHIVED},
    State.ARCHIVED: {State.RUNNING, State.RETIRED},
    State.TRANSFER_REQUIRED: {State.RUNNING, State.RELEASE_BLOCKED, State.RETIRED},
    State.REUSE_RECOMMENDED: {State.RETIRED},
    State.EXPERT_REVIEW_REQUIRED: {State.RETIRED},
    State.RETIRED: set(),
}


def transition(project_root: Path, target: State, evidence: Dict[str, Any], policy_result: str, actor: str, reason: str) -> Dict[str, Any]:
    citizen = project_root / ".citizen"
    state_path = citizen / "state.json"
    audit_path = citizen / "audit" / "events.jsonl"
    with project_lock(citizen):
        verify_chain(audit_path)
        current_doc = read_json(state_path)
        current = State(current_doc["state"])
        if target == current:
            return current_doc
        if target not in ALLOWED[current]:
            raise TransitionError("{} cannot move to {}. The current evidence does not permit that step.".format(current.value, target.value))
        if not evidence:
            raise TransitionError("This state change needs evidence. Nothing was changed.")
        if not policy_result:
            raise TransitionError("This state change needs a policy result. Nothing was changed.")
        value = {
            "actor": actor,
            "evidence": evidence,
            "policy_result": policy_result,
            "previous_state": current.value,
            "reason": reason,
            "state": target.value,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        append_event(audit_path, "state_transition", actor, reason, {"from": current.value, "to": target.value, "policy_result": policy_result})
        atomic_write_json(state_path, value, citizen / "backups")
        return value
