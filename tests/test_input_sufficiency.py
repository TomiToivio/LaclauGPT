"""Regression tests for project-neutral source sufficiency and abstention.

These cases are synthetic. They encode methodological invariants learned from
pilot work without publishing corpus rows, identifiers, targets, or operational
collection settings.
"""
from __future__ import annotations

from laclaugpt.evidence_quality import assess_evidence
from prompts import discourse, populism, postprocess, summary


def test_short_fragmentary_input_abstains() -> None:
    result = assess_evidence(
        transcript="brief fragment",
        ocr_text="CC UI id",
        visual_observations="",
    )
    assert result.status == "insufficient"
    assert result.mode == "none"
    assert result.allow_interpretive_analysis is False


def test_transcript_can_supply_sufficient_evidence_alone() -> None:
    result = assess_evidence(
        transcript=(
            "Citizens are discussing a proposed public policy and explaining "
            "why the institutional decision matters for their community today."
        )
    )
    assert result.status == "sufficient"
    assert result.mode == "text"
    assert result.transcript_usable is True


def test_visual_observations_require_successful_stage_when_status_is_supplied() -> None:
    failed = assess_evidence(
        visual_observations="A speaker stands beside a campaign poster.",
        visual_status="failed",
    )
    assert failed.visual_usable is False
    assert failed.status == "insufficient"

    available = assess_evidence(
        visual_observations="A speaker stands beside a campaign poster.",
        visual_status="partial",
    )
    assert available.visual_usable is True
    assert available.mode == "vision_only"


def test_summary_nonpolitical_validator_clears_political_families() -> None:
    Summary = summary.pydantic_models()
    row = Summary.model_validate({
        "narrative_construction": "A person describes an ordinary daily activity.",
        "political_classification": "non-political",
        "political": False,
        "political_subcategory": "",
        "difficult_language": [],
        "key_political_topics": [{"topic": "elections", "description": "unsupported"}],
        "political_entities": [{"entity": "Example Party", "role": "unsupported"}],
        "sentiments": [{"sentiment": "positive", "target": "Example Party", "justification": "unsupported"}],
        "people_power_narrative": {
            "status": "present",
            "collective_expression": "we",
            "opposed_expression": "them",
            "evidence_quote": "we and them",
            "explanation": "unsupported",
        },
        "social_contract": [{"element": "trust", "explanation": "unsupported"}],
        "grievances": [{"grievance": "policy", "potential_impact": "unsupported"}],
    })
    assert row.key_political_topics == []
    assert row.political_entities == []
    assert row.sentiments == []
    assert row.social_contract == []
    assert row.grievances == []
    assert row.people_power_narrative.status == "uncertain"


def test_discourse_nonapplicable_validator_clears_theoretical_codings() -> None:
    Analysis = discourse.pydantic_models()
    row = Analysis.model_validate({
        "applicable": False,
        "applicability_reason": "No substantive political discourse in source content.",
        "signifiers": [{
            "term": "freedom",
            "role": "element",
            "rationale": "unsupported",
            "evidence_quote": "freedom",
            "confidence": 0.4,
        }],
        "articulations": [],
        "imaginaries": [],
        "formation_candidates": [],
        "hegemonic_evidence": ["unsupported"],
        "uncertainties": [],
    })
    assert row.signifiers == []
    assert row.hegemonic_evidence == []


def test_postprocess_rejects_placeholder_entities_and_keeps_type_alignment() -> None:
    Extraction = postprocess.pydantic_models()
    row = Extraction.model_validate({
        "entities": ["None explicitly named", "Example Institution"],
        "entity_types": ["ORG", "ORG"],
        "new_entities": ["unknown", "Example Person"],
    })
    assert row.entities == ["Example Institution"]
    assert row.entity_types == ["ORG"]
    assert row.new_entities == ["Example Person"]


def test_all_prompts_expose_abstention_language() -> None:
    summary_text = summary.build_system_prompt("topic", "metadata").lower()
    discourse_text = discourse.build_system_prompt("topic", "metadata").lower()
    populism_text = populism.build_system_prompt("topic", "metadata").lower()
    postprocess_text = postprocess.build_system_prompt().lower()

    assert "evidence_quality_status=insufficient" in summary_text
    assert "applicability gate" in discourse_text
    assert "abstention gate" in populism_text
    assert "placeholder" in postprocess_text
