#!/usr/bin/env python3
"""Offline guard for the §4.2 sparse-cell rule (#88, decided in #89).

Issue #88 measured the AI26 frame and showed the paper's stratification promise could not be met as
written: Finnish is a 289-document total across three arenas, the elites × fi cell is 26, and every
Finnish cell comes from a single source type. #89 merged the rule that makes §4.2 executable — a
reportable subgroup needs 30 independently double-coded eligible documents, pooling must be
preregistered and justified, and arena-less records are counted separately.

Nothing checked that rule. A later edit could delete the threshold, soften "do not publish a
subgroup-specific estimate" into a suggestion, or let the paper promise cross-product strata again,
and CI would stay green. This is the drift this file exists to catch.

Offline and dependency-free, like its siblings in this directory. Run:
    python3 scripts/verify_stratification_88.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "docs" / "VALIDATION_PROTOCOL.md"
PAPER = ROOT / "paper" / "PHASE_1_PAPER.md"
RECORD = ROOT / "docs" / "AI26_STRATIFICATION_88.md"

#: The merged guardrail. Changing the number is a research decision, not a refactor.
MINIMUM_SUBGROUP = "30"

PROTOCOL_CLAUSES = (
    # The number itself, with the sentence that gives it force.
    f"Conservative minimum reportable subgroup: {MINIMUM_SUBGROUP}",
    "Below 30, do not publish a subgroup-specific chance-corrected agreement estimate",
    # The honest hedge: 30 stops a publication, it does not make 31 reliable.
    "30 is a reporting guardrail, not a power or reliability guarantee",
    # Pooling is allowed, but only as a declared act with named parts.
    "Any pooling across arenas, languages or formations must be preregistered",
)

PAPER_CLAUSES = (
    # §4.2 must preregister the threshold rather than leave it to whoever draws the sample.
    "minimum reportable cell size",
    # Arena-less records are counted, not assigned.
    "counted separately",
    # Small cells are exploratory unless the pooling is justified.
    "pooled only under a stated theoretical justification",
    # The claim that #88 showed was impossible without the rule.
    "sufficient independently double-coded cases in every reported subgroup",
)


def check(path: Path, clauses: tuple[str, ...], label: str, problems: list[str]) -> None:
    if not path.exists():
        problems.append(f"missing {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for clause in clauses:
        if clause not in text:
            problems.append(f"{label} lost its clause: {clause!r}")


def main() -> int:
    problems: list[str] = []
    check(PROTOCOL, PROTOCOL_CLAUSES, "the validation protocol", problems)
    check(PAPER, PAPER_CLAUSES, "paper §4.2", problems)

    if not RECORD.exists():
        problems.append(f"missing {RECORD.relative_to(ROOT)}")
    else:
        record = RECORD.read_text(encoding="utf-8")
        for phrase in ("289", "elites × fi", "286", "30"):
            if phrase not in record:
                problems.append(f"the #88 measurement record lost its '{phrase}' evidence")
        if "does not edit `paper/PHASE_1_PAPER.md`" not in record:
            problems.append("the record no longer states that §4.2 is the author's text")

    if problems:
        for problem in problems:
            print(f"FAIL {problem}", file=sys.stderr)
        return 1
    print(
        f"OK sparse-cell rule intact: minimum reportable subgroup {MINIMUM_SUBGROUP}, "
        "pooling declared, arena-less records counted separately"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
