from __future__ import annotations

import csv
import tempfile
from pathlib import Path

import legacy_asr
import legacy_fetch
import legacy_screen_metadata


def _manifest(path: Path) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["document_id", "source_url"])
        writer.writerow(["synthetic-1", "https://example.invalid/media/example.mp4"])


def test_legacy_manifest_and_destination_are_generic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        manifest = Path(tmp) / "manifest.csv"
        _manifest(manifest)
        pairs = legacy_fetch.load_manifest(manifest)
        assert pairs == [("synthetic-1", "https://example.invalid/media/example.mp4")]
        dest = legacy_fetch._dest_for(Path(tmp), pairs[0][1])
        assert dest.suffix == ".mp4"


def test_legacy_asr_uses_vad_with_injected_model() -> None:
    class Info:
        language = "en"
        language_probability = 0.9
        duration = 1.0

    class Segment:
        text = "synthetic transcript"

    class Model:
        model_size_or_path = "synthetic"
        def transcribe(self, path, **kwargs):
            assert kwargs["vad_filter"] is True
            return [Segment()], Info()

    result = legacy_asr.transcribe_video("synthetic.mp4", model=Model())
    assert result["transcript"] == "synthetic transcript"
    assert result["language"] == "en"


def test_legacy_screen_metadata_is_provisional() -> None:
    meta = legacy_screen_metadata.extract_screen_metadata("Instagram\nExample User\n@example.user")
    record = legacy_screen_metadata.screen_metadata_record(meta)["screen_metadata"]
    assert record["handle"] == "example.user"
    assert record["review_status"] == "proposed"
    assert record["source"] == "ocr"
