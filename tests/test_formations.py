from pathlib import Path

import pandas as pd

from laclaugpt.formations import CANONICAL_FORMATIONS, MIGRATION_VERSION, normalize_formation
from laclaugpt.visualization.live_dashboard import _formation_actor_counts
from scripts.migrate_ai26_formations import _is_allowed, migrate_record


DETERMINISTIC = {
    "accelerationism": ["accelerationism"],
    "x-risk doomerism": ["doomerism"],
    "left techno-optimism": ["left-wing accelerationism"],
    "techno-optimism": ["accelerationism"],
    "effective accelerationism": ["accelerationism"],
    "techno-optimism / accelerationism": ["accelerationism"],
    "institutional techno-optimism": ["accelerationism"],
    "corporate techno-optimism": ["accelerationism"],
    "institutional ai safety/governance": ["ai safety"],
    "left techno-optimism / accelerationist adjacent": ["left-wing accelerationism"],
    "institutional safetyism": ["ai safety"],
    "critical ai studies": ["ai critical"],
    "technical alignmentism": ["ai safety"],
    "institutional technocratic governance": ["ai safety"],
    "techno-institutionalism": ["ai safety"],
    "tescreal": ["accelerationism"],
    "accelerationist critique of institutional capture": ["accelerationism"],
    "corporate techno-utilitarianism": ["accelerationism"],
    "x-risk doomerism / ai safety alignment": ["doomerism", "ai safety"],
    "ai safety / x-risk discourse": ["ai safety", "doomerism"],
    "left techno-optimism / institutional accelerationism": [
        "left-wing accelerationism", "accelerationism"
    ],
    "critical ai / anti-ai mobilization": ["ai critical", "anti-ai"],
    "critical ai / anti-ai mobilisation": ["ai critical", "anti-ai"],
    "left-wing techno-optimism / corporate techno-optimism": [
        "left-wing accelerationism", "accelerationism"
    ],
    "anti-ai backlash": ["anti-ai"],
}


def test_canonical_vocabulary():
    assert CANONICAL_FORMATIONS == (
        "accelerationism",
        "doomerism",
        "left-wing accelerationism",
        "ai safety",
        "ai critical",
        "anti-ai",
    )


def test_every_deterministic_mapping():
    for label, expected in DETERMINISTIC.items():
        assert list(normalize_formation(label).formations) == expected


def test_case_whitespace_normalization_and_canonical_idempotence():
    assert list(normalize_formation(" x-RISK   DOOMERISM ").formations) == ["doomerism"]
    for label in CANONICAL_FORMATIONS:
        assert list(normalize_formation(f"  {label.upper()}  ").formations) == [label]


def test_modifier_becomes_secondary_tag():
    result = normalize_formation("critical ai / anti-big tech")
    assert list(result.formations) == ["ai critical"]
    assert list(result.tags) == ["anti_big_tech"]
    result = normalize_formation("critical ai / anti-hype")
    assert list(result.formations) == ["ai critical"]
    assert list(result.tags) == ["anti_hype"]


def test_ambiguous_label_uses_record_evidence_when_clear():
    source = {
        "formation": "technical ai safety / auditism",
        "evidence": "Independent model evaluation and safety audits are required before release.",
    }
    migrated, unknown = migrate_record(source)
    assert unknown == []
    assert migrated["formations"] == ["ai safety"]
    assert migrated["formation_tags"] == ["auditism"]
    assert migrated["formation_needs_review"] is False


def test_ambiguous_label_remains_reviewable_without_evidence():
    source = {"formation": "technical ai safety / auditism", "evidence": ""}
    migrated, unknown = migrate_record(source)
    assert unknown == []
    assert migrated["formations"] == []
    assert migrated["formation_tags"] == ["auditism"]
    assert migrated["formation_needs_review"] is True


def test_unknown_label_is_preserved_as_provenance_and_flagged():
    source = {"formation": "novel local formation", "evidence": "some evidence"}
    migrated, unknown = migrate_record(source)
    assert unknown == ["novel local formation"]
    assert migrated["formations"] == []
    assert migrated["formation_original"] == "novel local formation"
    assert migrated["formation_needs_review"] is True


def test_migration_reads_nested_candidate_shape():
    source = {
        "formation_candidates": [
            {"formation": "x-risk doomerism", "evidence": "extinction risk"},
            {"formation": {"label": "institutional safetyism"}},
        ]
    }
    migrated, unknown = migrate_record(source)
    assert unknown == []
    assert migrated["formations"] == ["doomerism", "ai safety"]


def test_migration_preserves_provenance_and_is_idempotent():
    source = {
        "id": "doc-1",
        "formation": "critical ai / anti-ai mobilization",
        "evidence": "x",
        "timestamp": "2026-01-01T00:00:00Z",
    }
    first, unknown = migrate_record(source)
    assert unknown == []
    assert first["formations"] == ["ai critical", "anti-ai"]
    assert first["formation_original"] == "critical ai / anti-ai mobilization"
    assert first["formation_migration_version"] == MIGRATION_VERSION
    assert first["evidence"] == "x"
    assert first["timestamp"] == source["timestamp"]
    second, unknown2 = migrate_record(first)
    assert second == first and unknown2 == []


def test_raw_and_source_paths_are_refused():
    assert _is_allowed(Path("data/analyzed/ai26.jsonl"))
    assert _is_allowed(Path("exports/ai26-analysis.json"))
    assert not _is_allowed(Path("data/raw/ai26.jsonl"))
    assert not _is_allowed(Path("sources/analyzed-copy.jsonl"))
    assert not _is_allowed(Path("collector/output.jsonl"))


def test_dashboard_counts_multilabel_records_in_both_formations():
    frame = pd.DataFrame(
        [
            {
                "document_id": "d1",
                "source_author": "actor-a",
                "formations": ["doomerism", "ai safety"],
            },
            {
                "document_id": "d2",
                "source_author": "actor-b",
                "formations": ["ai safety"],
            },
        ]
    )
    counts = _formation_actor_counts(frame).set_index("formation")
    assert counts.loc["doomerism", "documents"] == 1
    assert counts.loc["ai safety", "documents"] == 2
