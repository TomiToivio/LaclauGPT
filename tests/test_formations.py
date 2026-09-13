from laclaugpt.formations import CANONICAL_FORMATIONS, MIGRATION_VERSION, normalize_formation
from scripts.migrate_ai26_formations import migrate_record


def test_canonical_vocabulary():
    assert CANONICAL_FORMATIONS == (
        "accelerationism", "doomerism", "left-wing accelerationism",
        "ai safety", "ai critical", "anti-ai",
    )


def test_aliases_and_normalization():
    assert list(normalize_formation(" x-RISK   DOOMERISM ").formations) == ["doomerism"]
    assert list(normalize_formation("techno-optimism").formations) == ["accelerationism"]
    assert list(normalize_formation("critical ai studies").formations) == ["ai critical"]
    assert list(normalize_formation("TESCREAL").formations) == ["accelerationism"]


def test_multilabel_and_tags():
    assert list(normalize_formation("x-risk doomerism / ai safety alignment").formations) == ["doomerism", "ai safety"]
    result = normalize_formation("critical ai / anti-big tech")
    assert list(result.formations) == ["ai critical"]
    assert list(result.tags) == ["anti_big_tech"]


def test_ambiguous_requires_review():
    assert normalize_formation("technical ai safety / auditism").needs_review


def test_migration_preserves_provenance_and_is_idempotent():
    source = {"id": "doc-1", "formation": "critical ai / anti-ai mobilization", "evidence": "x"}
    first, unknown = migrate_record(source)
    assert unknown == []
    assert first["formations"] == ["ai critical", "anti-ai"]
    assert first["formation_original"] == "critical ai / anti-ai mobilization"
    assert first["formation_migration_version"] == MIGRATION_VERSION
    assert first["evidence"] == "x"
    second, unknown2 = migrate_record(first)
    assert second == first and unknown2 == []
