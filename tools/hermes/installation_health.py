#!/usr/bin/env python3
"""Run declared private installation health checks and optional bounded recovery.

Actual installation details belong in:
  $LACLAUGPT_PRIVATE_ROOT/hermes/installations.json

This tool is check-only unless --repair is explicitly passed. Even with --repair,
it executes repair/restart commands only when the selected private installation
entry has the corresponding authorized flag set to true.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ENV_VAR = "LACLAUGPT_PRIVATE_ROOT"


def private_root() -> Path:
    raw = os.environ.get(ENV_VAR, "").strip()
    if not raw:
        raise RuntimeError(f"{ENV_VAR} is not set")
    return Path(raw).expanduser().resolve()


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / "hermes" / "installations.json"
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_installation(manifest: dict[str, Any], name: str) -> dict[str, Any]:
    for item in manifest.get("installations", []):
        if item.get("name") == name:
            return item
    raise KeyError(f"installation not found: {name}")


def run(command: str, cwd: str | None, timeout: int) -> dict[str, Any]:
    proc = subprocess.run(
        command,
        shell=True,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
        env=os.environ.copy(),
    )
    return {"command": command, "returncode": proc.returncode, "output": proc.stdout[-8000:]}


def execute_many(commands: list[str], cwd: str | None, timeout: int) -> list[dict[str, Any]]:
    return [run(command, cwd, timeout) for command in commands]


def healthy(results: list[dict[str, Any]]) -> bool:
    return bool(results) and all(result["returncode"] == 0 for result in results)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("installation", help="Logical installation name from the private manifest")
    parser.add_argument("--repair", action="store_true", help="Allow privately authorized repair/restart actions")
    parser.add_argument("--timeout", type=int, default=120, help="Per-command timeout in seconds")
    args = parser.parse_args()

    try:
        root = private_root()
        manifest = load_manifest(root)
        item = find_installation(manifest, args.installation)
    except (RuntimeError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    cwd = item.get("cwd")
    checks = list(item.get("health_checks", []))
    if not checks:
        print("ERROR: installation has no declared health_checks", file=sys.stderr)
        return 2

    report: dict[str, Any] = {
        "installation": args.installation,
        "health": execute_many(checks, cwd, args.timeout),
        "repair_attempted": False,
    }

    if healthy(report["health"]):
        report["healthy"] = True
        print(json.dumps(report, indent=2))
        return 0

    report["healthy"] = False
    if not args.repair:
        print(json.dumps(report, indent=2))
        return 1

    repair_cfg = item.get("repair", {})
    restart_cfg = item.get("restart", {})
    repair_commands = list(repair_cfg.get("commands", [])) if repair_cfg.get("authorized") is True else []
    restart_commands = list(restart_cfg.get("commands", [])) if restart_cfg.get("authorized") is True else []

    if not repair_commands and not restart_commands:
        report["repair_refused"] = "private manifest does not authorize repair or restart"
        print(json.dumps(report, indent=2))
        return 1

    report["repair_attempted"] = True
    if repair_commands:
        report["repair"] = execute_many(repair_commands, cwd, args.timeout)
    if restart_commands:
        report["restart"] = execute_many(restart_commands, cwd, args.timeout)

    validation = list(item.get("validate", checks))
    report["validation"] = execute_many(validation, cwd, args.timeout)
    report["healthy_after_repair"] = healthy(report["validation"])
    print(json.dumps(report, indent=2))
    return 0 if report["healthy_after_repair"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
