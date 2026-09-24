#!/usr/bin/env python3
"""Lane lock management for a gauntlet run.

All lane locks live in one file, <run-dir>/run.lock, as a JSON object keyed
by lane id. Each record holds {lane, holder, acquired, heartbeat}.

Subcommands:
  acquire    Take the lane lock. Fails (exit 1) when a live lock exists for
             the lane under a different holder. A lock is stale, and may be
             reclaimed, when its heartbeat is older than 2 hours or when its
             holder is marked exited in sessions/sessions.json.
  heartbeat  Refresh the heartbeat timestamp on a lock this holder owns.
  release    Remove the lane's lock. Idempotent when no lock exists.
  status     Report all locks, or one lane's lock, with computed liveness.

Exit codes: 0 success, 1 validation failure (refused acquire, wrong holder),
2 usage error.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

STALE_SECONDS = 2 * 3600


def now_utc():
    return datetime.now(timezone.utc)


def iso(moment):
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ts(value):
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def load_locks(lock_path):
    if not os.path.isfile(lock_path):
        return {}
    try:
        with open(lock_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (ValueError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def save_locks(lock_path, locks):
    tmp = lock_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(locks, handle, indent=2)
        handle.write("\n")
    os.replace(tmp, lock_path)


def holder_exited(run_dir, holder):
    """True when sessions.json marks the holder's session as exited."""
    if not holder:
        return False
    sessions_path = os.path.join(run_dir, "sessions", "sessions.json")
    if not os.path.isfile(sessions_path):
        return False
    try:
        with open(sessions_path, "r", encoding="utf-8") as handle:
            sessions = json.load(handle).get("sessions") or []
    except (ValueError, OSError):
        return False
    for session in sessions:
        candidates = set()
        if session.get("holder") is not None:
            candidates.add(str(session["holder"]))
        if session.get("index") is not None:
            candidates.add("session-%s" % session["index"])
            candidates.add(str(session["index"]))
        if str(holder) in candidates and session.get("exited"):
            return True
    return False


def lock_liveness(record, run_dir, now):
    """Return (live, reason). A lock with no parseable heartbeat is stale."""
    heartbeat = parse_ts(record.get("heartbeat")) or parse_ts(record.get("acquired"))
    if heartbeat is None:
        return False, "no parseable heartbeat"
    if (now - heartbeat).total_seconds() >= STALE_SECONDS:
        return False, "heartbeat older than 2 hours"
    if holder_exited(run_dir, record.get("holder")):
        return False, "holder marked exited in sessions.json"
    return True, "heartbeat fresh and holder not exited"


def cmd_acquire(run_dir, lock_path, lane, holder):
    now = now_utc()
    locks = load_locks(lock_path)
    existing = locks.get(lane)
    reclaimed = False
    if existing is not None:
        live, reason = lock_liveness(existing, run_dir, now)
        if live and existing.get("holder") != holder:
            print(json.dumps({
                "ok": False,
                "lane": lane,
                "holder": existing.get("holder"),
                "heartbeat": existing.get("heartbeat"),
                "reason": "live lock held by %s (%s)" % (existing.get("holder"), reason),
            }))
            return 1
        reclaimed = existing.get("holder") != holder
    record = {
        "lane": lane,
        "holder": holder,
        "acquired": iso(now),
        "heartbeat": iso(now),
    }
    locks[lane] = record
    save_locks(lock_path, locks)
    result = dict(record)
    result["ok"] = True
    result["reclaimed"] = reclaimed
    print(json.dumps(result))
    return 0


def cmd_heartbeat(lock_path, lane, holder):
    locks = load_locks(lock_path)
    record = locks.get(lane)
    if record is None:
        print(json.dumps({"ok": False, "lane": lane,
                          "reason": "no lock exists for this lane"}))
        return 1
    if record.get("holder") != holder:
        print(json.dumps({"ok": False, "lane": lane,
                          "reason": "lock held by %s, not %s" % (record.get("holder"), holder)}))
        return 1
    record["heartbeat"] = iso(now_utc())
    save_locks(lock_path, locks)
    result = dict(record)
    result["ok"] = True
    print(json.dumps(result))
    return 0


def cmd_release(lock_path, lane, holder):
    locks = load_locks(lock_path)
    record = locks.get(lane)
    if record is None:
        print(json.dumps({"ok": True, "lane": lane, "released": False,
                          "reason": "no lock existed for this lane"}))
        return 0
    if holder is not None and record.get("holder") != holder:
        print(json.dumps({"ok": False, "lane": lane, "released": False,
                          "reason": "lock held by %s, not %s" % (record.get("holder"), holder)}))
        return 1
    del locks[lane]
    save_locks(lock_path, locks)
    print(json.dumps({"ok": True, "lane": lane, "released": True}))
    return 0


def cmd_status(run_dir, lock_path, lane):
    now = now_utc()
    locks = load_locks(lock_path)
    report = {}
    for lane_id, record in locks.items():
        live, reason = lock_liveness(record, run_dir, now)
        entry = dict(record)
        entry["live"] = live
        entry["stale"] = not live
        entry["liveness_reason"] = reason
        report[lane_id] = entry
    if lane is not None:
        entry = report.get(lane)
        if entry is None:
            print(json.dumps({"ok": True, "lane": lane, "locked": False}))
        else:
            entry["ok"] = True
            entry["locked"] = True
            print(json.dumps(entry))
        return 0
    print(json.dumps({"ok": True, "locks": report}))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Acquire, heartbeat, release, or inspect gauntlet lane locks in run.lock.")
    parser.add_argument("--run-dir", required=True,
                        help="Path to .gauntlet/runs/<run-id>")
    parser.add_argument("command", choices=["acquire", "heartbeat", "release", "status"],
                        help="Lock operation to perform")
    parser.add_argument("--lane", help="Lane id (required for acquire, heartbeat, release)")
    parser.add_argument("--holder",
                        help="Holder id, for example session-3 (required for acquire, heartbeat)")
    args = parser.parse_args(argv)

    if args.command in ("acquire", "heartbeat", "release") and not args.lane:
        parser.error("--lane is required for %s" % args.command)
    if args.command in ("acquire", "heartbeat") and not args.holder:
        parser.error("--holder is required for %s" % args.command)

    run_dir = os.path.abspath(args.run_dir)
    if not os.path.isdir(run_dir):
        print(json.dumps({"ok": False, "reason": "run directory not found: %s" % run_dir}))
        return 1
    lock_path = os.path.join(run_dir, "run.lock")

    if args.command == "acquire":
        return cmd_acquire(run_dir, lock_path, args.lane, args.holder)
    if args.command == "heartbeat":
        return cmd_heartbeat(lock_path, args.lane, args.holder)
    if args.command == "release":
        return cmd_release(lock_path, args.lane, args.holder)
    return cmd_status(run_dir, lock_path, args.lane)


if __name__ == "__main__":
    sys.exit(main())
