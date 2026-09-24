#!/usr/bin/env python3
"""Surface precheck for the gauntlet plugin (SPEC section 2).

Detects the four capabilities a gauntlet run depends on:

- filesystem read and write (tempfile probe)
- command execution (subprocess echo probe)
- network fetch (socket connect to a well-known host, only with --expect-network)
- clean-context subagent spawning (--surface hatch or --surface claude-code
  means true; --surface chat means false; otherwise heuristic: CLAUDECODE /
  CLAUDE_CODE_* env means true, else "unknown", which maps to degraded)

Prints a machine-readable JSON result on stdout:

    {"result": "full" | "degraded" | "unsupported",
     "subagents": true | false | "unknown",
     "filesystem": bool,
     "command_execution": bool,
     "network": bool | null,
     "remediation": str | null}

"unsupported" fires when there is no filesystem, or when there are no
subagents and no command execution. A remediation line is printed to stderr
for degraded and unsupported results.

Exit codes: 0 for full or degraded, 1 for unsupported, 2 for usage errors.
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import tempfile

WELL_KNOWN_HOSTS = [("1.1.1.1", 443), ("8.8.8.8", 53)]
PROBE_TOKEN = "gauntlet-precheck"


def probe_filesystem():
    """Write and read back a temp file. True only if both succeed."""
    try:
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".gauntlet-precheck", delete=True
        ) as fh:
            fh.write(PROBE_TOKEN)
            fh.flush()
            fh.seek(0)
            return fh.read() == PROBE_TOKEN
    except Exception:
        return False


def probe_command_execution():
    """Run an echo subprocess. Falls back to a Python -c probe."""
    try:
        proc = subprocess.run(
            ["echo", PROBE_TOKEN], capture_output=True, text=True, timeout=10
        )
        if proc.returncode == 0 and PROBE_TOKEN in proc.stdout:
            return True
    except Exception:
        pass
    try:
        proc = subprocess.run(
            [sys.executable, "-c", "print('%s')" % PROBE_TOKEN],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return proc.returncode == 0 and PROBE_TOKEN in proc.stdout
    except Exception:
        return False


def probe_network(timeout=3.0):
    """Socket connect to a well-known host with a short timeout."""
    for host, port in WELL_KNOWN_HOSTS:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            continue
    return False


def detect_subagents(surface):
    """Heuristic for clean-context subagent support.

    Returns True, False, or "unknown". "unknown" maps to degraded because
    isolation the surface cannot confirm must never be claimed (SPEC 11.1).
    """
    if surface == "hatch":
        return True
    if surface == "claude-code":
        return True
    if surface == "chat":
        return False
    if os.environ.get("CLAUDECODE"):
        return True
    if any(key.startswith("CLAUDE_CODE") for key in os.environ):
        return True
    return "unknown"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Detect whether this surface can run a gauntlet "
        "(SPEC section 2). Prints JSON on stdout."
    )
    parser.add_argument(
        "--surface",
        choices=["auto", "hatch", "claude-code", "cowork", "chat"],
        default="auto",
        help="Surface hint. auto uses the environment heuristic (default).",
    )
    parser.add_argument(
        "--expect-network",
        action="store_true",
        help="Probe network reach. Only pass this when the domain needs "
        "source-reach; otherwise network stays null and never blocks full.",
    )
    args = parser.parse_args(argv)

    filesystem = probe_filesystem()
    command_execution = probe_command_execution()
    network = probe_network() if args.expect_network else None
    subagents = detect_subagents(args.surface)

    missing = []
    if not filesystem:
        missing.append("filesystem read and write")
    if not command_execution:
        missing.append("command execution")
    if subagents is False:
        missing.append("clean-context subagent spawning")
    elif subagents == "unknown":
        missing.append("clean-context subagent spawning (unconfirmed on this surface)")
    if args.expect_network and not network:
        missing.append("network fetch (this domain needs source-reach)")

    if not filesystem or (subagents is False and not command_execution):
        result = "unsupported"
    elif (
        subagents is True
        and filesystem
        and command_execution
        and (network is None or network)
    ):
        result = "full"
    else:
        result = "degraded"

    remediation = None
    if result == "degraded":
        remediation = (
            "Degraded surface, missing: "
            + "; ".join(missing)
            + ". Name the missing capability and its cost to the user before "
            "proceeding, record it in run.json (context_isolation or "
            "execution set to degraded), and carry the degradation banner in "
            "every handoff and evidence report from this run."
        )
    elif result == "unsupported":
        remediation = (
            "Unsupported surface, missing: "
            + "; ".join(missing)
            + ". Refuse to initialize a run; the method needs an agentic "
            "harness. Offer brief-only mode: run gauntlet-brief and "
            "gauntlet-prompt, produce CONTEXT.md, PLAN.md, bar/, and "
            "prompt.md, and hand the user a portable prompt to run elsewhere. "
            "Never simulate a loop."
        )

    payload = {
        "result": result,
        "subagents": subagents,
        "filesystem": filesystem,
        "command_execution": command_execution,
        "network": network,
        "remediation": remediation,
    }
    print(json.dumps(payload, indent=2))
    if remediation:
        print(remediation, file=sys.stderr)
    return 1 if result == "unsupported" else 0


if __name__ == "__main__":
    sys.exit(main())
