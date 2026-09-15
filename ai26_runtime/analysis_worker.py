#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Incremental analysis worker: sources -> canonical pipeline -> annotations.

Local Ollama only. Stage-aware local model routing is resolved by
pipeline.Stage.call via laclaugpt.model_routing. No cloud fallback.

Failure semantics:
- if the pipeline subprocess fails, documents are marked analysis_status=error
  with the stderr tail, NOT done;
- documents are marked done only after their annotations were actually written;
- every tick appends a run record for observability.

Issue #136: source text and source-native metadata are reattached to the canonical
annotation after the CSV bridge. This keeps the temporary CSV deliberately small
without making it a lossy boundary for researcher-facing provenance.
"""
from __future__ import annotations

import csv as csvmod
import json
import os
import subprocess
import sys
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(os.environ.get(
    "LACLAUGPT_ROOT", str(Path(__file__).resolve().parents[1])
)).expanduser().resolve()
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "ai26_runtime"))

os.environ["LLM_MODE"] = "local"
os.environ.setdefault("OLLAMA_HOST", "http://127.0.0.1:11434")
os.environ.setdefault("OLLAMA_KEEP_ALIVE", "24h")
os.environ.pop("LLM_ALLOW_CLOUD_FALLBACK", None)

from mongo_writer import get_db  # noqa: E402

P = "ai26_"
BATCH = int(os.environ.get("AI26_BATCH", "10"))


def pick_unanalyzed(arena: str | None = None) -> list[dict]:
    db = get_db()
    query = {"analysis_status": {"$ne": "done"}}
    if arena:
        query["metadata.arena"] = arena
    return list(
        db[P + "sources"].find(query)
        .sort([("analysis_status", 1), ("collected_at", 1)])
        .limit(BATCH)
    )


def _json_safe(value: Any) -> Any:
    try:
        return json.loads(json.dumps(value, ensure_ascii=False, default=str))
    except (TypeError, ValueError):
        return str(value)


def _source_for_annotation(annotation_id: str, docs: list[dict]) -> dict | None:
    candidates = {annotation_id, annotation_id.split("::", 1)[-1]}
    for doc in docs:
        native_id = str(doc.get("native_id") or "")
        source_url = str(doc.get("source_url") or "")
        normalized_url = str(doc.get("normalized_source_url") or "")
        if candidates.intersection({native_id, source_url, normalized_url}):
            return doc
    return None


def _enrich_annotation(annotation, source_doc: dict | None) -> None:
    """Restore researcher-visible source material lost by the narrow CSV bridge."""
    if not source_doc:
        return
    metadata = _json_safe(source_doc.get("metadata") or {})
    transformations = dict(annotation.transformations or {})
    provenance = dict(annotation.collection_provenance or {})

    source_text = source_doc.get("raw_text") or ""
    if source_text:
        transformations.setdefault("source_text", str(source_text))

    # Preserve common upstream intermediate/modal fields if collectors supplied
    # them, without inventing a platform-specific canonical schema.
    for key in (
        "transcript",
        "whisper_transcript",
        "caption",
        "ocr_text",
        "frame_analysis",
        "discourse_analysis",
        "populism_analysis",
        "entities",
        "topics",
        "sentiment",
        "analysis_warnings",
        "analysis_errors",
    ):
        value = source_doc.get(key)
        if value not in (None, "", [], {}):
            transformations.setdefault(key, _json_safe(value))

    provenance.setdefault("source_native_metadata", metadata)
    provenance.setdefault(
        "source_record",
        _json_safe(
            {
                key: value
                for key, value in source_doc.items()
                if key not in {"_id", "raw_text"}
            }
        ),
    )

    annotation.transformations = transformations
    annotation.collection_provenance = provenance
    if not annotation.source_platform:
        annotation.source_platform = str(
            source_doc.get("platform") or source_doc.get("source_type") or ""
        )
    if not annotation.source_author:
        annotation.source_author = str(source_doc.get("author_text") or "")
    if not annotation.source_timestamp:
        annotation.source_timestamp = str(source_doc.get("published_at") or "")
    if not annotation.source_url:
        annotation.source_url = str(source_doc.get("source_url") or "")
    if not annotation.language:
        annotation.language = str((source_doc.get("metadata") or {}).get("language") or "")


def run_pipeline(docs: list[dict]) -> dict:
    """Build a narrow canonical CSV from the docs and run pipeline.py."""
    db = get_db()
    arena = (docs[0].get("metadata") or {}).get("arena", "elites")
    run_config = REPO / "run_configs" / f"arena_{arena}.yaml"
    if not run_config.exists():
        run_config = REPO / "run_configs" / "arena_ep24.yaml"
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as tmp:
        writer = csvmod.writer(tmp)
        writer.writerow([
            "document_id", "text", "url", "author", "created_at", "source_platform"
        ])
        ids = []
        for d in docs:
            did = d["native_id"]
            ids.append(did)
            writer.writerow([
                did,
                d.get("raw_text") or d.get("title") or "",
                d.get("source_url") or "",
                d.get("author_text") or "",
                d.get("published_at") or "",
                d.get("source_type") or "",
            ])
        csv_path = tmp.name
    out_jsonl = tempfile.mktemp(suffix=".jsonl")
    started = datetime.now(timezone.utc)
    run_id = f"ai26-incr-{started.strftime('%Y%m%dT%H%M%S')}"
    try:
        result = subprocess.run(
            [
                "python3", "pipeline.py", "--run-config", str(run_config),
                "--csv", csv_path, "--output", out_jsonl,
            ],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=3600,
        )
    except subprocess.TimeoutExpired as exc:
        _mark_error(db, ids, f"pipeline timeout after 3600s: {exc}")
        _record_run(db, run_id, arena, len(docs), 0, "timeout", started)
        return {"docs": len(docs), "annotated": 0, "status": "timeout"}
    except Exception as exc:
        _mark_error(db, ids, f"pipeline spawn failed: {exc}")
        _record_run(db, run_id, arena, len(docs), 0, "spawn_error", started)
        return {"docs": len(docs), "annotated": 0, "status": "spawn_error"}

    annotated_ids: list[str] = []
    stats = {"docs": len(docs), "annotated": 0, "status": "ok"}
    if result.returncode != 0:
        stats["status"] = "pipeline_error"
        tail = (result.stderr or result.stdout or "")[-1500:]
        _mark_error(db, ids, tail)
        _record_run(
            db, run_id, arena, len(docs), 0, "pipeline_error", started,
            stderr_tail=tail,
        )
    elif Path(out_jsonl).exists():
        from laclaugpt_interchange import from_jsonl

        annotations = from_jsonl(out_jsonl)
        for ann in annotations:
            _enrich_annotation(ann, _source_for_annotation(ann.document_id, docs))
            payload = ann.model_dump(mode="json")
            db2 = get_db()
            db2[P + "annotations"].update_one(
                {"document_id": ann.document_id, "run_id": ann.run_id},
                {"$set": payload},
                upsert=True,
            )
            stats["annotated"] += 1
            annotated_ids.append(ann.document_id)
        Path(out_jsonl).unlink()
        if annotated_ids:
            bare = [a.split("::", 1)[1] for a in annotated_ids if "::" in a]
            match_ids = list(dict.fromkeys(annotated_ids + bare))
            db[P + "sources"].update_many(
                {
                    "$or": [
                        {"native_id": {"$in": match_ids}},
                        {"source_url": {"$in": match_ids}},
                        {"normalized_source_url": {"$in": match_ids}},
                    ]
                },
                {
                    "$set": {
                        "analysis_status": "done",
                        "analyzed_at": datetime.now(timezone.utc).isoformat(),
                    }
                },
            )
    else:
        stats["status"] = "no_output"
        _mark_error(db, ids, "pipeline produced no output file")
        _record_run(db, run_id, arena, len(docs), 0, "no_output", started)
    if stats.get("status") == "ok":
        _record_run(
            db, run_id, arena, len(docs), stats["annotated"], "ok", started
        )
    Path(csv_path).unlink()
    return stats


def _mark_error(db, ids: list[str], reason: str) -> None:
    if not ids:
        return
    db[P + "sources"].update_many(
        {"native_id": {"$in": ids}},
        {
            "$set": {
                "analysis_status": "error",
                "analysis_error": (reason or "")[-1000:],
            }
        },
    )


def _record_run(
    db,
    run_id: str,
    arena: str,
    docs: int,
    annotated: int,
    status: str,
    started: datetime,
    stderr_tail: str = "",
) -> None:
    db[P + "runs"].insert_one({
        "run_id": run_id,
        "kind": "incremental_analysis",
        "arena": arena,
        "docs": docs,
        "annotated": annotated,
        "status": status,
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "stderr_tail": stderr_tail[-500:],
    })


def main() -> None:
    docs = pick_unanalyzed()
    if not docs:
        print("nothing to analyze")
        return
    try:
        stats = run_pipeline(docs)
        print(f"analysis: {stats}")
    except Exception:
        print("worker crashed:", traceback.format_exc()[-1500:])
        raise


if __name__ == "__main__":
    main()
