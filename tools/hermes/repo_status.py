#!/usr/bin/env python3
"""Read-only local status check for the four public LaclauGPT repositories.

The script never pulls, commits, edits, restarts, or contacts private services.
It is suitable as a cron preflight and emits JSON for Hermes or a human wrapper.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REPOS = {
    "main": "LaclauGPT",
    "collection": "LaclauGPT-Data-Collection",
    "analysis": "LaclauGPT-Data-Analysis",
    "visualization": "LaclauGPT-Data-Visualization",
}


def run_git(repo: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=30,
    )
    return proc.returncode, proc.stdout.strip()


def inspect(repo: Path) -> dict[str, object]:
    if not repo.exists():
        return {"exists": False, "path": str(repo)}
    code, top = run_git(repo, "rev-parse", "--show-toplevel")
    if code != 0:
        return {"exists": True, "git": False, "path": str(repo), "error": top}

    _, branch = run_git(repo, "branch", "--show-current")
    _, head = run_git(repo, "rev-parse", "HEAD")
    _, status = run_git(repo, "status", "--porcelain=v1")
    _, remote = run_git(repo, "remote", "get-url", "origin")
    return {
        "exists": True,
        "git": True,
        "path": str(Path(top)),
        "branch": branch,
        "head": head,
        "dirty": bool(status),
        "status_lines": status.splitlines()[:50] if status else [],
        "origin": remote,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace",
        type=Path,
        default=Path.cwd().parent,
        help="Directory containing the four sibling repository clones (default: parent of cwd)",
    )
    args = parser.parse_args()

    workspace = args.workspace.expanduser().resolve()
    payload = {
        "workspace": str(workspace),
        "repositories": {key: inspect(workspace / name) for key, name in REPOS.items()},
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
