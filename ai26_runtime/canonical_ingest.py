#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Canonical-corpus -> source-store ingestion sync.

Bridges canonical normalized collection records into the shared incremental
analysis source collection. Operational targets stay outside this public module.

Issue #136: ingestion must be lossless for researcher-facing source metadata.
Alongside the stable cross-platform fields used by the worker, the complete
source-native metadata, canonical source metadata and ingestion provenance are
preserved under namespaced keys. Nothing analytical is inferred here.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO = Path(os.environ.get(
    "LACLAUGPT_ROOT", str(Path(__file__).resolve().parents[1])
)).expanduser().resolve()
sys.path.insert(0, str(REPO / "ai26_runtime"))
sys.path.insert(0, str(REPO))
os.environ.setdefault("AI26_DATA_ROOT", os.path.expanduser("~/laclaugpt-ai26-data"))

from mongo_writer import get_db, P  # noqa: E402

CANONICAL = REPO / "collection-data" / "normalized"
DATA_ROOT = Path(os.environ["AI26_DATA_ROOT"])
STATE = DATA_ROOT / "canonical_ingest_state.json"
INGEST_BATCH = int(os.environ.get("AI26_INGEST_BATCH", "500"))

FILES: dict[str, str] = {
    "rss.jsonl": "rss",
    "social.jsonl": "social",
    "web.jsonl": "web",
    "minet.jsonl": "minet",
    "manual.jsonl": "manual",
}


def _json_safe(value: Any) -> Any:
    """Round-trip arbitrary source metadata into JSON-compatible values."""
    try:
        return json.loads(json.dumps(value, ensure_ascii=False, default=str))
    except (TypeError, ValueError):
        return str(value)


def _doc(record: dict, source_type: str) -> dict | None:
    src = record.get("source") or {}
    text = src.get("raw_text") or ""
    native = src.get("native_id") or src.get("source_id")
    if not text or not native:
        return None
    meta = src.get("metadata") or {}
    ing = record.get("ingestion") or {}

    # Keep a useful stable subset for ordinary queries, plus namespaced lossless
    # metadata for researcher inspection and future platform-specific adapters.
    stable_metadata = {
        "arena": meta.get("arena") or "",
        "channel": meta.get("channel") or "canonical_sync",
        "study": meta.get("study") or "",
        "collector": meta.get("collector") or src.get("platform") or source_type,
        "feed_name": meta.get("feed_name") or "",
        "source_family": meta.get("source_source_family")
        or meta.get("source_family") or "",
        "sampling_stratum": meta.get("sampling_stratum") or "",
        "sampling_rationale": meta.get("source_sampling_rationale")
        or meta.get("sampling_rationale") or "",
        "source_priority": meta.get("source_priority") or "",
        "language": src.get("language") or "",
        "dedup_id": meta.get("dedup_id") or "",
    }
    stable_metadata["source_native"] = _json_safe(meta)
    stable_metadata["canonical_source"] = _json_safe(
        {key: value for key, value in src.items() if key != "raw_text"}
    )
    stable_metadata["ingestion"] = _json_safe(ing)

    return {
        "source_type": source_type,
        "platform": src.get("platform") or source_type,
        "native_id": str(native),
        "title": (src.get("title") or "")[:300],
        "author_text": src.get("author_text") or "",
        "published_at": src.get("published_at") or "",
        "collected_at": (
            src.get("collected_at") or datetime.now(timezone.utc).isoformat()
        ),
        "source_url": src.get("source_url") or "",
        "normalized_source_url": src.get("normalized_source_url")
        or src.get("source_url") or "",
        "raw_text": text,
        "analysis_status": "pending",
        "metadata": stable_metadata,
    }


def main() -> int:
    db = get_db()
    seen: dict = {}
    if STATE.exists():
        try:
            seen = json.loads(STATE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            seen = {}
    saved = 0
    per_file: dict[str, int] = {}
    for fname, source_type in sorted(FILES.items()):
        path = CANONICAL / fname
        if not path.exists():
            continue
        count = 0
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                dedup = ((record.get("source") or {}).get("metadata") or {}).get(
                    "dedup_id"
                ) or ((record.get("source") or {}).get("source_id") or "")
                key = f"{fname}:{dedup}"
                if seen.get(key):
                    continue
                doc = _doc(record, source_type)
                if not doc:
                    continue
                db[P + "sources"].update_one(
                    {"source_type": source_type, "native_id": doc["native_id"]},
                    {"$setOnInsert": doc},
                    upsert=True,
                )
                seen[key] = 1
                count += 1
                if count >= INGEST_BATCH:
                    break
        if count:
            per_file[fname] = count
            saved += count
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(seen), encoding="utf-8")
    print(f"canonical sync: saved={saved} per_file={per_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
