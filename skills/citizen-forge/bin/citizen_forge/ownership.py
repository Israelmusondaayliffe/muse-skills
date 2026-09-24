from datetime import datetime, timezone
from typing import Any, Dict, Optional


def evaluate(record: Dict[str, Any], shared: bool) -> Dict[str, Any]:
    primary = str(record.get("primary_owner", "")).strip()
    backup = str(record.get("backup_owner", "")).strip()
    valid = bool(primary) and (not shared or bool(backup))
    return {"valid": valid, "required_state": None if valid else "TRANSFER_REQUIRED", "explanation": "Ownership is valid." if valid else "A valid primary and backup owner are required before shared changes or releases."}


def transfer(record: Dict[str, Any], new_primary: str, new_backup: str, approved_by: str) -> Dict[str, Any]:
    if not new_primary.strip() or not new_backup.strip() or not approved_by.strip():
        raise ValueError("Ownership transfer needs a primary owner, backup owner, and approver.")
    return {"primary_owner": new_primary.strip(), "backup_owner": new_backup.strip(), "approved_by": approved_by.strip(), "transferred_at": datetime.now(timezone.utc).isoformat(), "valid": True}
