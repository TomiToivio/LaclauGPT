"""Configuration and export helpers for corpus synthesis."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable

import yaml

from laclaugpt.synthesis import CorpusSynthesis, SynthesisConfig
from laclaugpt.synthesis_windows import CadenceConfig


def load_synthesis_config(path: str | Path) -> tuple[SynthesisConfig, CadenceConfig]:
    """Load issue-136 synthesis/cadence settings from YAML without code edits."""
    source = Path(path)
    payload = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    root = payload.get("synthesis", payload)
    if not isinstance(root, dict):
        raise ValueError("synthesis configuration must be a mapping")

    cadence_raw = root.get("cadence") or {}
    compare_raw = root.get("compare_previous") or {}
    if not isinstance(cadence_raw, dict):
        raise ValueError("synthesis.cadence must be a mapping")
    if isinstance(compare_raw, bool):
        compare_raw = {"enabled": compare_raw}
    if not isinstance(compare_raw, dict):
        raise ValueError("synthesis.compare_previous must be a mapping or boolean")

    synthesis = SynthesisConfig(
        enabled=bool(root.get("enabled", True)),
        group_by=list(root.get("group_by") or ["date"]),
        minimum_documents=int(root.get("minimum_documents", 5)),
        rolling_window_days=int(cadence_raw.get("rolling_window_days", 7)),
        compare_previous=bool(compare_raw.get("enabled", True)),
        compare_periods=int(compare_raw.get("periods", 1)),
        historical_baseline_days=compare_raw.get("historical_baseline_days", 30),
        include_intermediate_results=bool(root.get("include_intermediate_results", True)),
        include_source_metadata=bool(root.get("include_source_metadata", True)),
        cadence_daily=bool(cadence_raw.get("daily", True)),
        every_n_documents=cadence_raw.get("every_n_documents"),
        model=str(root.get("model") or ""),
        prompt_version=str(root.get("prompt_version") or ""),
        config_version=str(root.get("config_version") or "1"),
    )
    cadence = CadenceConfig(
        daily=bool(cadence_raw.get("daily", True)),
        rolling_window_days=int(cadence_raw.get("rolling_window_days", 7)),
        previous_periods=int(compare_raw.get("periods", 1)),
        historical_baseline_days=compare_raw.get("historical_baseline_days", 30),
        every_n_documents=cadence_raw.get("every_n_documents"),
    )
    return synthesis, cadence


def _rows(syntheses: Iterable[CorpusSynthesis]) -> list[dict[str, Any]]:
    return [item.model_dump(mode="json") for item in syntheses]


def export_synthesis_json(syntheses: Iterable[CorpusSynthesis], path: str | Path) -> str:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(_rows(syntheses), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return str(destination)


def export_synthesis_csv(syntheses: Iterable[CorpusSynthesis], path: str | Path) -> str:
    destination = Path(path)
    rows = _rows(syntheses)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        destination.write_text("", encoding="utf-8")
        return str(destination)
    columns = list(rows[0])
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False, sort_keys=True)
                    if isinstance(value, (dict, list))
                    else value
                    for key, value in row.items()
                }
            )
    return str(destination)


def export_synthesis_markdown(
    syntheses: Iterable[CorpusSynthesis], path: str | Path
) -> str:
    destination = Path(path)
    items = list(syntheses)
    lines = ["# Corpus synthesis", ""]
    for item in items:
        label = ", ".join(f"{key}={value}" for key, value in item.grouping.items()) or "all documents"
        lines.extend(
            [
                f"## {label}",
                "",
                f"Documents: {item.document_count}",
                f"Window: {item.time_window.get('start', '')} to {item.time_window.get('end', '')}",
                "",
                item.human_readable_synthesis,
                "",
                "### Detected changes",
                "",
                "```json",
                json.dumps(item.detected_changes.model_dump(mode="json"), ensure_ascii=False, indent=2),
                "```",
                "",
                "> Descriptive/provisional synthesis only. Frequency is not hegemony.",
                "",
            ]
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return str(destination)
