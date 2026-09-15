import csv
import json
from pathlib import Path

from laclaugpt.researcher_exports import (
    export_filtered_rows,
    export_researcher_csv,
    export_researcher_jsonl,
)
from laclaugpt_interchange import DocumentAnnotation


def annotation(document_id: str) -> DocumentAnnotation:
    return DocumentAnnotation(
        document_id=document_id,
        source_platform="x",
        transformations={
            "source_text": f"text for {document_id}",
            "transcript": f"transcript for {document_id}",
            "frame_analysis": {"frame": "security"},
        },
        collection_provenance={
            "source_native_metadata": {
                "conversation_id": f"thread-{document_id}",
                "engagement": {"likes": 7},
            },
            "llm_stages": {
                "discourse": {"actual_model": "gemma4:12b"}
            },
        },
        prompt_versions={"discourse": "v1"},
    )


def test_csv_keeps_nested_metadata_and_human_readable_analysis(tmp_path: Path) -> None:
    path = tmp_path / "rows.csv"
    export_researcher_csv([annotation("d1")], path)
    with path.open(encoding="utf-8", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert "human_readable_analysis" in row
    assert "source_native_metadata" in row
    native = json.loads(row["source_native_metadata"])
    assert native["conversation_id"] == "thread-d1"
    provenance = json.loads(row["collection_provenance"])
    assert provenance["llm_stages"]["discourse"]["actual_model"] == "gemma4:12b"
    assert "transcript for d1" in row["human_readable_analysis"]


def test_jsonl_preserves_machine_structure(tmp_path: Path) -> None:
    path = tmp_path / "rows.jsonl"
    export_researcher_jsonl([annotation("d1")], path)
    payload = json.loads(path.read_text(encoding="utf-8").strip())
    assert payload["transformations"]["frame_analysis"]["frame"] == "security"
    assert payload["source_native_metadata"]["engagement"]["likes"] == 7
    assert payload["collection_provenance"]["llm_stages"]["discourse"]["actual_model"] == "gemma4:12b"


def test_filtered_export_contains_only_selected_documents(tmp_path: Path) -> None:
    path = tmp_path / "filtered.jsonl"
    docs = [annotation("d1"), annotation("d2")]
    export_filtered_rows(docs, ["d2"], path, format="jsonl")
    payloads = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert [item["document_id"] for item in payloads] == ["d2"]
