#!/usr/bin/env python3
"""Offline regression guard for the shared cross-module canonical fixture."""

from __future__ import annotations

import csv
import io
import json
import sqlite3
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "cross_module" / "canonical_parity_v1.json"
EXPECTED_URL = "https://example.invalid/laclaugpt/synthetic/record-001"


def assert_contract(record: dict) -> None:
    assert record["fixture_version"] == "1.0.0"
    assert record["source_url"] == EXPECTED_URL
    assert record["source_native_ids"]["legacy_document_id"] == "legacy-001"
    assert record["source"]["raw_metadata"]["legacy_optional_field"] == "must-survive-roundtrip"
    content = record["content"]
    for field in ("transcripts", "ocr", "frames", "media_references"):
        assert field in content and content[field], field
    analysis = record["analysis"]
    assert analysis["codebook_refs"][0]["id"] == "synthetic-codebook"
    assert analysis["model_runs"][0]["provider"] == "fake"
    assert analysis["uncertainty"][0]["target_id"] == "obj_candidate_001"
    obj = analysis["analysis_objects"][0]
    assert obj["epistemic_type"] == "CANDIDATE_INTERPRETATION"
    assert obj["review_status"] == "PROVISIONAL"
    assert record["review"]["status"] == "PROVISIONAL"
    assert any(p["stage"] == "collection" for p in record["provenance"])
    assert any(p["stage"] == "analysis" for p in record["provenance"])


def json_roundtrip(record: dict) -> dict:
    return json.loads(json.dumps(record, sort_keys=True))


def jsonl_roundtrip(record: dict) -> dict:
    payload = json.dumps(record, sort_keys=True) + "\n"
    return json.loads(payload.splitlines()[0])


def csv_roundtrip(record: dict) -> dict:
    # CSV is an adapter, not an alternative schema. Nested sections are encoded as JSON.
    row = {key: (json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else value) for key, value in record.items()}
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(row))
    writer.writeheader()
    writer.writerow(row)
    buf.seek(0)
    parsed = next(csv.DictReader(buf))
    out = {}
    for key, original in record.items():
        value = parsed[key]
        out[key] = json.loads(value) if isinstance(original, (dict, list)) else value
    return out


def sqlite_roundtrip(record: dict) -> dict:
    con = sqlite3.connect(":memory:")
    try:
        con.execute("CREATE TABLE records (source_url TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        con.execute(
            "INSERT INTO records(source_url, payload) VALUES (?, ?)",
            (record["source_url"], json.dumps(record, sort_keys=True)),
        )
        payload = con.execute("SELECT payload FROM records WHERE source_url = ?", (record["source_url"],)).fetchone()[0]
        return json.loads(payload)
    finally:
        con.close()


def main() -> None:
    record = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert_contract(record)
    for name, adapter in (
        ("JSON", json_roundtrip),
        ("JSONL", jsonl_roundtrip),
        ("CSV", csv_roundtrip),
        ("SQLite", sqlite_roundtrip),
    ):
        roundtripped = adapter(record)
        assert_contract(roundtripped)
        assert roundtripped == record, f"{name} round trip changed canonical semantics"
    print("Cross-module canonical parity fixture passed JSON/JSONL/CSV/SQLite regression checks.")


if __name__ == "__main__":
    main()
