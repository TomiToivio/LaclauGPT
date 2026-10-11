#!/usr/bin/env python3
"""Offline guard: a daily report may not cite an undeclared port.

Issue #74. The reports of 2026-10-04, -06, -07, -08 and -09 all asserted a
*second* visualization dashboard on `:8551` answering HTTP 200, and the standing
maintenance specification repeated the same claim -- while the only command
anyone actually ran measured `:8501`. `:8551` was never a product endpoint. The
claim was propagated from one report to the next and never measured.

The failure mode is not a wrong number. It is a number that *was never checked*
being cited as a measurement, and then becoming the thing the next report
repeats. Prose has no contract, so CI could not see it.

Fix: the ports are declared once, in `schemas/laskin-service-ports.json`, and
this guard fails when a report cites a port that is not declared there.

Two declarations, two rules:

* `ports` - a real service. A report may cite it freely.
* `retracted` - a port known NOT to be a service (a phantom that was repeated).
  A report may name it *in order to retract it*, which is why the record keeps
  working; but not beside a health signal. That is exactly the defect: `:8551`
  sat next to `HTTP 200`. `AFFIRMATIVE` below is the narrow set of tokens that
  turn a mention into a claim.

Scope: `docs/reports/*.md`, the artifact class that restates health as
measurement. Four-digit tokens preceded by `arXiv` are excluded -- an arXiv
identifier (`arXiv:2609.11109`) looks exactly like a port, which is why a naive
whole-text scan of this repo is unusable.

Offline and dependency-free, like its siblings `verify_cross_module_fixture.py`
and `verify_two_machine_policy.py`.

Run: python3 scripts/verify_reported_ports.py
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "schemas" / "laskin-service-ports.json"
REPORTS = ROOT / "docs" / "reports"

# A colon followed by 4-5 digits: the shape of a TCP port in prose.
PORT = re.compile(r":(\d{4,5})\b")

# How far back to look for the `arXiv` marker that disqualifies a match.
ARXIV_LOOKBACK = 6

# Tokens that turn a bare mention of a port into a health claim. Deliberately
# narrow: these are the words the observed defect used ("`:8551` HTTP 200",
# "second dashboard ... healthy"). A retracted port may appear on a line without
# any of them, because then the line is retracting or discussing, not claiming.
AFFIRMATIVE = re.compile(r"http|healthy|active|\blisten\b", re.IGNORECASE)


def load_inventory() -> tuple[set[str], dict[str, dict], set[str]]:
    """Return (all known ports, service-port metadata, retracted ports)."""
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    services = data["ports"]
    retracted = data.get("retracted", {})
    if not isinstance(services, dict) or not services:
        raise SystemExit(f"{INVENTORY} declares no service ports")
    if not isinstance(retracted, dict):
        raise SystemExit(f"{INVENTORY}: `retracted` must be an object")
    for group, label in ((services, "ports"), (retracted, "retracted")):
        for port in group:
            if not re.fullmatch(r"\d{4,5}", port):
                raise SystemExit(f"{INVENTORY}: {label} key {port!r} is not a port number")
    for port, meta in services.items():
        if not isinstance(meta, dict) or "service" not in meta:
            raise SystemExit(f"{INVENTORY}: port {port} must name a service")
    for port, meta in retracted.items():
        if not isinstance(meta, dict) or "note" not in meta:
            raise SystemExit(f"{INVENTORY}: retracted port {port} must carry a note")
    overlap = set(services) & set(retracted)
    if overlap:
        raise SystemExit(f"{INVENTORY}: {sorted(overlap)} cannot be both a service and retracted")
    return set(services) | set(retracted), services, set(retracted)


def cited_ports(text: str) -> Iterator[str]:
    """Yield every port-like token that is not part of an arXiv identifier."""
    for match in PORT.finditer(text):
        prefix = text[max(0, match.start() - ARXIV_LOOKBACK):match.start()].lower()
        if prefix.endswith("arxiv"):
            continue
        yield match.group(1)


def undeclared_citations(text: str, known: set[str]) -> list[tuple[int, str]]:
    """(line number, port) for every cited port that is not declared at all."""
    found: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for port in sorted({p for p in cited_ports(line) if p not in known}):
            found.append((lineno, port))
    return found


def retracted_claims(text: str, retracted: set[str]) -> list[tuple[int, str]]:
    """(line number, port) where a retracted port sits beside a health signal."""
    found: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not AFFIRMATIVE.search(line):
            continue
        for port in sorted({p for p in cited_ports(line) if p in retracted}):
            found.append((lineno, port))
    return found


def self_checks(known: set[str], retracted: set[str]) -> list[str]:
    """Assert the matcher and both rules still behave on fixed fixtures.

    Without these, a mutated matcher could make the guard report success while
    checking nothing.
    """
    problems: list[str] = []
    if list(cited_ports("see arXiv:2609.11109 for details")):
        problems.append("the arXiv exclusion is broken: an arXiv id was read as a port")
    if not list(cited_ports("dashboard :8501")):
        problems.append("the port matcher is broken: a plain ':8501' was not read as a port")
    if not undeclared_citations("a mystery port :9999\n", known):
        problems.append("an undeclared port was not flagged")
    if undeclared_citations("a declared port :8501\n", known):
        problems.append("a declared port was flagged as undeclared")
    phantom = sorted(retracted)[0] if retracted else None
    if phantom is not None:
        if not retracted_claims(f"dashboard :{phantom} HTTP 200\n", retracted):
            problems.append("a retracted port was not flagged beside a health signal")
        if retracted_claims(f"retracted: :{phantom} was never a service\n", retracted):
            problems.append("retracting a port was wrongly flagged as a claim")
    return problems


def main() -> int:
    known, services, retracted = load_inventory()

    problems: list[str] = []

    # 1. Every port a report cites must be declared, as a service or a retraction.
    #    This is the check that fails on an entirely new phantom.
    report_files = sorted(REPORTS.glob("*.md"))
    if not report_files:
        problems.append(f"no reports found under {REPORTS}")
    for report in report_files:
        rel = report.relative_to(ROOT)
        text = report.read_text(encoding="utf-8")
        for lineno, port in undeclared_citations(text, known):
            problems.append(
                f"{rel}:{lineno} cites port :{port}, which is neither a declared "
                f"service nor a declared retraction in {INVENTORY.relative_to(ROOT)}"
            )
        for lineno, port in retracted_claims(text, retracted):
            problems.append(
                f"{rel}:{lineno} presents retracted port :{port} beside a health "
                f"signal; a retracted port may only be named while retracting it"
            )

    # 2. Exactly one visualization port. The original defect was a *second*
    #    dashboard asserted alongside the real one; a declaration that grows a
    #    second visualization port should force a human to look.
    visualization = [p for p, meta in services.items() if meta.get("kind") == "visualization"]
    if len(visualization) != 1:
        problems.append(
            f"exactly one visualization port must be declared, found {sorted(visualization)}"
        )

    # 3. The guard's own matcher and both rules still work.
    problems.extend(self_checks(known, retracted))

    if problems:
        print("Reported-port guard FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1

    print(
        f"Reported-port guard passed: {len(report_files)} reports cite only the "
        f"{len(services)} declared service port(s) {sorted(services)} plus "
        f"{len(retracted)} retracted port(s) {sorted(retracted)}, with exactly one "
        f"visualization port {visualization}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
