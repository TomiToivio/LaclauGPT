#!/usr/bin/env python3
"""Offline guard: the published pre-analysis schema must stay structurally sound.

The umbrella repository owns the *methodological contract* for the Phase 1
Multimodal Social-Semiotic Pre-Analysis stage (#61); executable models live in
TomiToivio/LaclauGPT-Data-Analysis. This script checks the published contract
itself, so the two cannot silently disagree again.

Background: ``docs/SOCIAL_SEMIOTIC_PREANALYSIS.md`` and
``schemas/social-semiotic-preanalysis.v1.schema.json`` were merged on
``phase-1`` by PR #63 *after* the Phase-1 promotion, so for a period ``main``
neither documented nor published this stage while Data-Analysis already emitted
it. The schema also declared ``additionalProperties: false`` without the
compatibility projections the canonical models actually export, so a real
validator rejected canonical output. These checks fail closed on both classes.

Uses only the standard library so it runs in the meta-repo CI job unchanged.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "social-semiotic-preanalysis.v1.schema.json"
DOC_PATH = ROOT / "docs" / "SOCIAL_SEMIOTIC_PREANALYSIS.md"
PLAN_PATH = ROOT / "docs" / "PHASE1_SOCIAL_SEMIOTIC_PREANALYSIS_PLAN.md"
PAPER_PATH = ROOT / "paper" / "PHASE_1_PAPER.md"
SUMMARY_PATH = ROOT / "sources" / "SUMMARIES.md"

SCHEMA_VERSION = "social-semiotic-preanalysis.v1"

#: Analyst classifications that must never appear as schema properties.
FORBIDDEN_PROPERTIES = (
    "empty_signifiers", "floating_signifiers", "nodal_points",
    "chains_of_equivalence", "chains_of_difference", "antagonisms", "frontiers",
    "populism", "ideology", "ideological_formation", "party_alignment",
    "political_alignment", "hegemony", "political_subjects", "political_demands",
    "sentiment",
)

#: Fields the canonical Analysis models export that the schema must accept.
#: These are descriptive compatibility projections, not downstream analysis.
REQUIRED_COMPAT_PROPERTIES = (
    "narrative", "semiotic_modes", "cross_modal_relations", "difficult_language",
    "topics", "entities", "claims", "event_candidates",
)


def _load_schema() -> dict:
    assert SCHEMA_PATH.is_file(), f"published schema missing: {SCHEMA_PATH.relative_to(ROOT)}"
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def check_documents_exist() -> list[str]:
    problems = []
    for path in (DOC_PATH, PLAN_PATH):
        if not path.is_file():
            problems.append(f"missing Phase 1 method document: {path.relative_to(ROOT)}")
    return problems


def check_paper_documents_stage() -> list[str]:
    """The Phase 1 paper must explain the stage and its boundary."""
    if not PAPER_PATH.is_file():
        return ["paper/PHASE_1_PAPER.md is missing"]
    text = PAPER_PATH.read_text(encoding="utf-8")
    lowered = text.lower()
    problems = []
    if "social-semiotic pre-analysis" not in lowered and "social semiotic" not in lowered:
        problems.append("paper does not document the social-semiotic pre-analysis stage")
    for term in ("kress", "van leeuwen", "halliday", "martinec", "barthes", "wanselin"):
        if term not in lowered:
            problems.append(f"paper does not cite {term.title()}")
    for term in ("llm structuralism", "laclau"):
        if term not in lowered:
            problems.append(f"paper does not state the boundary against {term}")
    return problems


def check_sources_summary() -> list[str]:
    if not SUMMARY_PATH.is_file():
        return ["sources/SUMMARIES.md is missing"]
    lowered = SUMMARY_PATH.read_text(encoding="utf-8").lower()
    if "wanselin" not in lowered:
        return ["sources/SUMMARIES.md lacks the Wanselin et al. source analysis"]
    return []


def check_schema_identity(schema: dict) -> list[str]:
    problems = []
    if SCHEMA_VERSION not in json.dumps(schema):
        problems.append(f"schema does not declare {SCHEMA_VERSION}")
    if schema.get("additionalProperties") is not False:
        problems.append("item-level schema must set additionalProperties:false (fail closed)")
    required = set(schema.get("required", []))
    for field in ("schema_version", "prompt_version", "summary", "modalities_present",
                  "evidence", "uncertainty"):
        if field not in required:
            problems.append(f"schema must require {field}")
    return problems


def check_boundary(schema: dict) -> list[str]:
    """No downstream classification may be a schema property."""
    problems = []
    properties = set(schema.get("properties", {}))
    defs = schema.get("$defs", {})
    for name, definition in defs.items():
        properties |= {f"{name}.{key}" for key in definition.get("properties", {})}
    for forbidden in FORBIDDEN_PROPERTIES:
        if forbidden in schema.get("properties", {}):
            problems.append(f"downstream field leaked into schema properties: {forbidden}")
    # A literal mention inside a description is documentation, not a property.
    return problems


def check_compat_projections(schema: dict) -> list[str]:
    """The schema must accept the canonical models' compatibility projections."""
    problems = []
    properties = schema.get("properties", {})
    for field in REQUIRED_COMPAT_PROPERTIES:
        if field not in properties:
            problems.append(
                f"schema omits canonical compatibility projection {field!r}; "
                "canonical output would fail validation"
            )
    if "frame_analysis" not in schema.get("$defs", {}):
        problems.append("schema lacks a frame_analysis definition for the frame-level pass")
    return problems


def check_doc_covers_contract(schema: dict) -> list[str]:
    """The method doc must describe the schema version and the hard boundary."""
    if not DOC_PATH.is_file():
        return []
    text = DOC_PATH.read_text(encoding="utf-8")
    lowered = text.lower()
    problems = []
    if SCHEMA_VERSION not in text:
        problems.append("method doc does not name the schema version")
    if "must not" not in lowered:
        problems.append("method doc does not state the hard negative boundary")
    for term in ("uncertainty", "denotation", "modality"):
        if term not in lowered:
            problems.append(f"method doc does not describe {term}")
    return problems


def main() -> int:
    problems: list[str] = []
    problems += check_documents_exist()
    problems += check_paper_documents_stage()
    problems += check_sources_summary()
    schema = _load_schema()
    problems += check_schema_identity(schema)
    problems += check_boundary(schema)
    problems += check_compat_projections(schema)
    problems += check_doc_covers_contract(schema)

    if problems:
        print("social-semiotic pre-analysis contract check FAILED:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("ok    social-semiotic pre-analysis contract (#61)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
