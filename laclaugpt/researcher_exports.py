"""Lossless researcher-facing export helpers.

These helpers share the same schema-driven row renderer as the dashboard/report
layer. Nested machine-readable fields are kept intact in JSONL/Parquet; CSV
serializes nested values deterministically instead of dropping them.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable, Sequence

from laclaugpt.researcher_reporting import researcher_row
from laclaugpt_interchange import DocumentAnnotation


HUMAN_READABLE_FIELD = "human_readable_analysis"
SOURCE_NATIVE_FIELD = "source_native_metadata"


def _native_metadata(annotation: DocumentAnnotation) -> dict[str, Any]:
    provenance = annotation.collection_provenance or {}
    value = (
        provenance.get("source_native_metadata")
        or provenance.get("source_native")
        or provenance.get("native_metadata")
        or {}
    )
    return value if isinstance(value, dict) else {"value": value}


def researcher_export_row(annotation: DocumentAnnotation) -> dict[str, Any]:
    """Return the complete canonical row plus explicit lossless convenience fields."""
    row = researcher_row(annotation)
    row[SOURCE_NATIVE_FIELD] = _native_metadata(annotation)
    return row


def _csv_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    if value is None:
        return ""
    return value


def _columns(rows: Sequence[dict[str, Any]]) -> list[str]:
    """Stable union of all row keys, preserving canonical first-row order."""
    if not rows:
        return []
    columns = list(rows[0])
    seen = set(columns)
    for row in rows[1:]:
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)
    return columns


def export_researcher_csv(
    annotations: Iterable[DocumentAnnotation], path: str | Path
) -> str:
    """Write one complete deterministic researcher row per annotation."""
    destination = Path(path)
    rows = [researcher_export_row(annotation) for annotation in annotations]
    destination.parent.mkdir(parents=True, exist_ok=True)
    columns = _columns(rows)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _csv_value(row.get(key)) for key in columns})
    return str(destination)


def export_researcher_jsonl(
    annotations: Iterable[DocumentAnnotation], path: str | Path
) -> str:
    """Write complete researcher rows as newline-delimited JSON."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for annotation in annotations:
            handle.write(
                json.dumps(
                    researcher_export_row(annotation),
                    ensure_ascii=False,
                    sort_keys=True,
                    default=str,
                )
                + "\n"
            )
    return str(destination)


def export_researcher_parquet(
    annotations: Iterable[DocumentAnnotation], path: str | Path
) -> str:
    """Write complete rows to Parquet while retaining nested values as JSON strings.

    Parquet engines vary in nested-Python-object support. Serializing nested values
    to JSON gives a stable cross-engine contract while preserving them losslessly.
    """
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - packaging guard
        raise RuntimeError("pandas is required for Parquet export") from exc

    destination = Path(path)
    rows = [researcher_export_row(annotation) for annotation in annotations]
    encoded = [
        {key: _csv_value(value) for key, value in row.items()}
        for row in rows
    ]
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        pd.DataFrame(encoded).to_parquet(destination, index=False)
    except ImportError as exc:
        raise RuntimeError(
            "Parquet export requires an installed pandas Parquet engine such as pyarrow"
        ) from exc
    return str(destination)


def export_filtered_rows(
    annotations: Iterable[DocumentAnnotation],
    document_ids: Iterable[str],
    path: str | Path,
    *,
    format: str = "csv",
) -> str:
    """Export exactly the currently selected/filtered document set."""
    wanted = set(document_ids)
    selected = [annotation for annotation in annotations if annotation.document_id in wanted]
    fmt = format.casefold().lstrip(".")
    if fmt == "csv":
        return export_researcher_csv(selected, path)
    if fmt in {"jsonl", "ndjson"}:
        return export_researcher_jsonl(selected, path)
    if fmt in {"parquet", "pq"}:
        return export_researcher_parquet(selected, path)
    raise ValueError(f"unsupported researcher export format: {format}")
