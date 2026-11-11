#!/usr/bin/env python3
"""Offline guard for the §4.2 stratification rule (#88).

Issue #88 measured the AI26 frame and showed that the paper's stratification promise cannot be met
as written: Finnish is a 289-document total across three arenas and every Finnish cell comes from a
single source type. The fix that landed is a declared minimum cell size with a pooling rule, so a
small cell is a stated limitation instead of a silently unstable agreement statistic.

Nothing checked that rule. A future edit could delete the threshold, drop the pooling sentence, or
quietly reintroduce "records with no arena" as a stratum, and CI would stay green — which is exactly
the failure mode this file exists to catch.

Offline and dependency-free, like its siblings in this directory. Run:
    python3 scripts/verify_stratification_88.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "VALIDATION_PROTOCOL.md"
RECORD = ROOT / "docs" / "AI26_STRATIFICATION_88.md"

#: The declared minimum, spelled out rather than inferred. Changing the number is a decision and
#: should require changing this guard too.
MINIMUM_CELL_SIZE = 20


def fail(problems: list[str], message: str) -> None:
    problems.append(message)


def main() -> int:
    problems: list[str] = []
    for path in (PROTOCOL, RECORD):
        if not path.exists():
            fail(problems, f"missing {path.relative_to(ROOT)}")
    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1

    protocol = PROTOCOL.read_text(encoding="utf-8")
    record = RECORD.read_text(encoding="utf-8")

    # 1. The rule exists and is a section of the sampling design, not a stray sentence.
    if "Minimum cell size and pooling (#88)" not in protocol:
        fail(problems, "the protocol lost its minimum-cell-size section (#88)")

    # 2. The threshold is declared, with the number the study actually uses.
    if not re.search(r"\*\*20 documents\*\*|minimum cell size is \*\*20\*\*", protocol):
        fail(problems, f"the protocol no longer declares a minimum cell size of {MINIMUM_CELL_SIZE}")

    # 3. Below the threshold there is no independent estimate — the pooling rule itself.
    for phrase in ("MUST NOT be reported as an independently estimated", "pooled", "qualitative illustration"):
        if phrase not in protocol:
            fail(problems, f"the pooling rule lost its '{phrase}' clause")

    # 4. Arena-blank records are not a stratum. This is the 286 that #88 is partly about.
    if "records with no arena" not in protocol.lower():
        fail(problems, "the protocol no longer excludes arena-blank records from the stratified draw")
    if "286" not in protocol:
        fail(problems, "the protocol no longer names the arena-blank count it excludes")

    # 5. The manifest records the decision, so a draw can be reproduced.
    if "minimum cell size used for the stratified draw" not in protocol:
        fail(problems, "the sampling manifest no longer records the minimum cell size")

    # 6. The measurement that justifies the rule is still available and still says what it found.
    for phrase in ("289", "Finnish", "second source type"):
        if phrase not in record:
            fail(problems, f"the #88 measurement record lost its '{phrase}' evidence")

    # 7. The paper's §4.2 remains the author's text: the record must say the agent did not write it.
    if "does not edit `paper/PHASE_1_PAPER.md`" not in record:
        fail(problems, "the record no longer states that §4.2 is the author's text to write")

    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    print(f"OK stratification rule intact: minimum cell size {MINIMUM_CELL_SIZE}, pooling declared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
