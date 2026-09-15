from datetime import datetime, timezone

from laclaugpt.synthesis import SynthesisConfig
from laclaugpt.synthesis_windows import (
    CadenceConfig,
    daily_windows,
    synthesize_rolling,
    synthesize_window_comparison,
)
from laclaugpt_interchange import DocumentAnnotation, FormationAssessment, MemoryRef


def doc(document_id: str, date: str, signifier: str, formation: str) -> DocumentAnnotation:
    return DocumentAnnotation(
        document_id=document_id,
        source_timestamp=f"{date}T12:00:00Z",
        source_platform="x",
        signifiers=[MemoryRef(obj_id=f"S-{signifier}", label=signifier, kind="signifier")],
        formation_candidates=[
            FormationAssessment(
                formation=MemoryRef(
                    obj_id=f"F-{formation}", label=formation, kind="formation"
                ),
                evidence="evidence",
                evidence_verified=True,
            )
        ],
        relevance="relevant",
    )


def test_daily_windows_are_contiguous() -> None:
    windows = daily_windows(day=datetime(2026, 9, 15, tzinfo=timezone.utc), periods=1)
    assert windows[0].start.isoformat().startswith("2026-09-15")
    assert windows[1].start.isoformat().startswith("2026-09-14")
    assert windows[1].end == windows[0].start


def test_date_plus_formation_compares_same_formation_across_dates() -> None:
    current = [doc("new", "2026-09-15", "abundance", "accel")]
    previous = [doc("old", "2026-09-14", "safety", "accel")]
    syntheses = synthesize_window_comparison(
        current,
        previous,
        config=SynthesisConfig(
            group_by=["date", "formation"],
            minimum_documents=1,
            compare_previous=True,
        ),
    )
    assert len(syntheses) == 1
    result = syntheses[0]
    assert result.grouping == {"date": "2026-09-15", "formation": "accel"}
    assert result.previous_window_reference is not None
    assert result.previous_window_reference["document_ids"] == ["old"]
    assert "abundance" in result.detected_changes.emerging_signifiers
    assert "safety" in result.detected_changes.declining_signifiers


def test_rolling_batch_current_vs_previous_period() -> None:
    docs = [
        doc("new", "2026-09-15", "abundance", "accel"),
        doc("old", "2026-09-14", "safety", "accel"),
    ]
    result = synthesize_rolling(
        docs,
        end=datetime(2026, 9, 16, tzinfo=timezone.utc),
        synthesis_config=SynthesisConfig(
            group_by=["formation"], minimum_documents=1, compare_previous=True
        ),
        cadence=CadenceConfig(rolling_window_days=1, previous_periods=1),
    )
    assert len(result) == 1
    assert result[0].previous_window_reference["document_ids"] == ["old"]
    assert result[0].detected_changes.continuity_or_drift == "meaningful drift"
