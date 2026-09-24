from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List


class State(str, Enum):
    IDEA_DRAFT = "IDEA_DRAFT"
    PROTOTYPE_ONLY = "PROTOTYPE_ONLY"
    REGISTERED = "REGISTERED"
    TRIAGE_PENDING = "TRIAGE_PENDING"
    APPROVED = "APPROVED"
    REUSE_RECOMMENDED = "REUSE_RECOMMENDED"
    EXPERT_REVIEW_REQUIRED = "EXPERT_REVIEW_REQUIRED"
    PROVISIONING_PLANNED = "PROVISIONING_PLANNED"
    PROVISIONED = "PROVISIONED"
    BUILDING = "BUILDING"
    RELEASE_CANDIDATE = "RELEASE_CANDIDATE"
    RELEASE_BLOCKED = "RELEASE_BLOCKED"
    RUNNING = "RUNNING"
    CHANGE_PENDING = "CHANGE_PENDING"
    ARCHIVE_RECOMMENDED = "ARCHIVE_RECOMMENDED"
    ARCHIVED = "ARCHIVED"
    TRANSFER_REQUIRED = "TRANSFER_REQUIRED"
    RETIRED = "RETIRED"


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    severity: str
    status: CheckStatus
    evidence: List[str]
    explanation: str
    repair: str
    ai_may_repair: bool
    human_decision_required: bool

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["status"] = self.status.value
        return value


@dataclass(frozen=True)
class AdapterReport:
    name: str
    available: bool
    authenticated: bool
    actions: List[str]
    permissions: List[str]
    dry_run: bool
    verification: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
