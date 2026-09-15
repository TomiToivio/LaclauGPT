import csv
import json
from pathlib import Path

from laclaugpt.synthesis import DetectedChanges, CorpusSynthesis
from laclaugpt.synthesis_io import (
    export_synthesis_csv,
    export_synthesis_json,
    export_synthesis_markdown,
    load_synthesis_config,
)


def synthesis() -> CorpusSynthesis:
    return CorpusSynthesis(
        synthesis_id="syn-1",
        grouping={"date": "2026-09-15", "formation": "accel"},
        time_window={"start": "2026-09-15T00:00:00Z", "end": "2026-09-16T00:00:00Z"},
        document_ids=["d1"],
        document_count=1,
        signifier_distribution={"AI": 1},
        detected_changes=DetectedChanges(emerging_signifiers=["AI"], continuity_or_drift="meaningful drift"),
        human_readable_synthesis="Provisional synthesis.",
    )


def test_yaml_configuration_without_code_edits(tmp_path: Path) -> None:
    path = tmp_path / "synthesis.yaml"
    path.write_text(
        """
synthesis:
  enabled: true
  group_by: [date, formation]
  cadence:
    daily: true
    rolling_window_days: 7
    every_n_documents: 100
  compare_previous:
    enabled: true
    periods: 2
    historical_baseline_days: 30
  minimum_documents: 3
  include_intermediate_results: true
  include_source_metadata: true
""".strip(),
        encoding="utf-8",
    )
    config, cadence = load_synthesis_config(path)
    assert config.group_by == ["date", "formation"]
    assert config.minimum_documents == 3
    assert config.compare_periods == 2
    assert cadence.daily is True
    assert cadence.rolling_window_days == 7
    assert cadence.every_n_documents == 100


def test_synthesis_multi_format_exports(tmp_path: Path) -> None:
    item = synthesis()
    json_path = Path(export_synthesis_json([item], tmp_path / "synthesis.json"))
    csv_path = Path(export_synthesis_csv([item], tmp_path / "synthesis.csv"))
    md_path = Path(export_synthesis_markdown([item], tmp_path / "synthesis.md"))

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload[0]["synthesis_id"] == "syn-1"
    with csv_path.open(encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))
    assert json.loads(row["grouping"])["formation"] == "accel"
    markdown = md_path.read_text(encoding="utf-8")
    assert "Provisional synthesis." in markdown
    assert "Frequency is not hegemony" in markdown
