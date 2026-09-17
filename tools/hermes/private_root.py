#!/usr/bin/env python3
"""Safety preflight for the private LaclauGPT/Hermes state root.

This tool deliberately does not create, copy, upload, or inspect research data.
It only validates that LACLAUGPT_PRIVATE_ROOT points to a plausible private
location outside the current public repository and reports basic permission
warnings on POSIX systems.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path

ENV_VAR = "LACLAUGPT_PRIVATE_ROOT"
RECOMMENDED_DIRS = ("research", "config", "credentials", "deploy", "logs", "hermes", "backups")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolved_private_root() -> Path:
    value = os.environ.get(ENV_VAR, "").strip()
    if not value:
        raise RuntimeError(f"{ENV_VAR} is not set")
    return Path(value).expanduser().resolve()


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def check_root(root: Path) -> list[str]:
    errors: list[str] = []
    public_root = repo_root().resolve()

    if is_within(root, public_root) or root == public_root:
        errors.append(f"private root is inside public repository: {public_root}")

    if not root.exists():
        errors.append(f"private root does not exist: {root}")
        return errors

    if not root.is_dir():
        errors.append(f"private root is not a directory: {root}")
        return errors

    if not os.access(root, os.R_OK | os.W_OK | os.X_OK):
        errors.append(f"private root is not fully accessible to current user: {root}")

    if os.name == "posix":
        mode = stat.S_IMODE(root.stat().st_mode)
        if mode & (stat.S_IRWXG | stat.S_IRWXO):
            errors.append(
                f"private root permissions are broader than owner-only ({oct(mode)}); "
                "consider chmod 700 if compatible with your environment"
            )

    return errors


def cmd_check() -> int:
    try:
        root = resolved_private_root()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    problems = check_root(root)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1

    print(f"OK: {ENV_VAR}={root}")
    missing = [name for name in RECOMMENDED_DIRS if not (root / name).exists()]
    if missing:
        print("INFO: optional recommended subdirectories missing: " + ", ".join(missing))
    return 0


def cmd_init() -> int:
    try:
        root = resolved_private_root()
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    public_root = repo_root().resolve()
    if is_within(root, public_root) or root == public_root:
        print(f"ERROR: refusing to initialize private state inside public repository: {public_root}", file=sys.stderr)
        return 1

    root.mkdir(parents=True, exist_ok=True)
    for name in RECOMMENDED_DIRS:
        (root / name).mkdir(exist_ok=True)

    if os.name == "posix":
        root.chmod(0o700)
        for name in RECOMMENDED_DIRS:
            (root / name).chmod(0o700)

    print(f"Initialized private root at {root}")
    return cmd_check()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "init"), help="validate or initialize the private root")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return cmd_init() if args.command == "init" else cmd_check()


if __name__ == "__main__":
    raise SystemExit(main())
