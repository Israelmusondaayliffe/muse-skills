from datetime import datetime, timezone
from typing import Any, Dict, Iterable

from .models import CheckResult, CheckStatus
from .checks import CONTROL_IDS


def decide_release(checks: Iterable[CheckResult], change: Dict[str, Any]) -> Dict[str, Any]:
    values = list(checks)
    counts = {check_id: 0 for check_id in CONTROL_IDS}
    for item in values:
        if item.check_id in counts:
            counts[item.check_id] += 1
    blocking = [item.check_id for item in values if item.status in {CheckStatus.FAIL, CheckStatus.BLOCKED, CheckStatus.UNAVAILABLE}]
    blocking.extend("MISSING_{}".format(check_id) for check_id, count in counts.items() if count == 0)
    blocking.extend("DUPLICATE_{}".format(check_id) for check_id, count in counts.items() if count > 1)
    unexpected = [item.check_id for item in values if item.check_id not in counts]
    blocking.extend("UNEXPECTED_{}".format(check_id) for check_id in unexpected)
    if change.get("classification") == "CONSEQUENTIAL":
        blocking.append("CONSEQUENTIAL_CHANGE_APPROVAL")
    status = "RELEASE_BLOCKED" if blocking else "RUNNING"
    return {
        "decision": status,
        "blocking_checks": sorted(set(blocking)),
        "human_approval_recorded": False,
        "change_classification": change.get("classification"),
        "decided_at": datetime.now(timezone.utc).isoformat(),
        "explanation": "Release is blocked until every required control has verified evidence." if blocking else "Every required control has fresh passing evidence.",
    }
