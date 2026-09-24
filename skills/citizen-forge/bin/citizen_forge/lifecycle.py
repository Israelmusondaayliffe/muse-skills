from datetime import datetime, timezone
from typing import Any, Dict, List


def signals(status: Dict[str, Any], policy: Dict[str, Any], now_epoch: float) -> List[Dict[str, str]]:
    found = []
    last_used = float(status.get("last_used_epoch", now_epoch))
    if now_epoch - last_used > int(policy["inactive_days"]) * 86400:
        found.append({"signal": "INACTIVE", "action": "ARCHIVE_RECOMMENDED"})
    if not status.get("primary_owner") or (status.get("shared") and not status.get("backup_owner")):
        found.append({"signal": "OWNERSHIP_MISSING", "action": "TRANSFER_REQUIRED"})
    if status.get("health") == "failed":
        found.append({"signal": "HEALTH_FAILED", "action": "RECOVERY_REVIEW"})
    if float(status.get("review_due_epoch", now_epoch + 1)) <= now_epoch:
        found.append({"signal": "REVIEW_DUE", "action": "LIFECYCLE_REVIEW"})
    return found
