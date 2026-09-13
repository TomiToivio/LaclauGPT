#!/usr/bin/env python3
"""Migrate analyzed AI26 JSON/JSONL records to the simple formation taxonomy.

The utility is conservative: it refuses raw/source/collection paths, never uses
an LLM merely to rename labels, preserves historical classifications, and flags
ambiguous cases for human review. By default it writes a sibling
``.ai26-simple`` output; ``--in-place`` is explicit and creates a backup.
"""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter
from pathlib import Path
import re
import shutil
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from laclaugpt.formations import (  # noqa: E402
    MIGRATION_VERSION,
    normalize_formation,
    normalize_formations,
)

ANALYZED_HINTS = ("analy", "derived", "output", "export", "result")
RAW_HINTS = ("/raw/", "/source/", "/sources/", "/collect", "collector/")

EVIDENCE_CUES: dict[str, tuple[str, ...]] = {
    "accelerationism": (
        "accelerat", "build faster", "abundance", "innovation", "progress",
        "techno-optim", "singular", "growth", "pro-development",
    ),
    "doomerism": (
        "x-risk", "existential risk", "extinction", "human extinction",
        "everyone dies", "doom", "catastrophic ai",
    ),
    "left-wing accelerationism": (
        "post-work", "postcapital", "fully automated", "left techno",
        "socialist automation", "automation for all",
    ),
    "ai safety": (
        "ai safety", "alignment", "audit", "evaluation", "frontier safety",
        "risk management", "governance", "guardrail", "model eval",
    ),
    "ai critical": (
        "critical ai", "ai hype", "anti-hype", "big tech", "extraction",
        "surveillance", "data colonial", "labor exploitation", "labour exploitation",
    ),
    "anti-ai": (
        "anti-ai", "ban ai", "stop ai", "reject ai", "no ai", "ludd",
        "abolish ai", "against ai",
    ),
}

AMBIGUOUS_CANDIDATES: dict[str, tuple[str, ...]] = {
    "institutional/policy-driven ai governance": ("ai safety", "accelerationism"),
    "left techno-optimism / open source advocacy": ("left-wing accelerationism",),
    "ai alignment/safety research discourse": ("ai safety",),
    "technical ai safety / auditism": ("ai safety",),
    "x-risk doomerism / safety-centric accelerationism": (
        "doomerism", "ai safety", "accelerationism"
    ),
}


def _norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


def _is_allowed(path: Path) -> bool:
    text = "/" + str(path).replace("\\", "/").casefold().lstrip("/")
    return any(x in text for x in ANALYZED_HINTS) and not any(x in text for x in RAW_HINTS)


def _candidate_label(item: dict[str, Any]) -> str:
    candidate = item.get("formation", item.get("label", ""))
    if isinstance(candidate, dict):
        candidate = candidate.get("label", "")
    return str(candidate or "").strip()


def _labels(record: dict[str, Any]) -> list[str]:
    """Read common historical formation representations."""
    value = record.get("formations", record.get("formation", []))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and value:
        return [str(v) for v in value if str(v).strip()]

    labels: list[str] = []
    for item in record.get("formation_candidates") or []:
        if isinstance(item, dict):
            label = _candidate_label(item)
            if label:
                labels.append(label)
    return labels


def _record_text(record: dict[str, Any]) -> str:
    """Collect already-analyzed evidence without using actor identity."""
    values: list[str] = []
    preferred = (
        "evidence", "evidence_quote", "summary", "analysis", "rationale",
        "supporting_features", "counter_evidence", "text",
    )
    for key in preferred:
        value = record.get(key)
        if isinstance(value, str):
            values.append(value)
        elif isinstance(value, list):
            values.extend(str(v) for v in value if isinstance(v, (str, int, float)))
    for item in record.get("formation_candidates") or []:
        if not isinstance(item, dict):
            continue
        for key in preferred:
            value = item.get(key)
            if isinstance(value, str):
                values.append(value)
            elif isinstance(value, list):
                values.extend(str(v) for v in value if isinstance(v, (str, int, float)))
    return _norm(" ".join(values))


def _evidence_resolve(label: str, record: dict[str, Any]) -> tuple[list[str], list[str], bool]:
    key = _norm(label)
    candidates = AMBIGUOUS_CANDIDATES.get(key)
    if not candidates:
        return [], [], True
    text = _record_text(record)
    formations = [
        candidate for candidate in candidates
        if any(cue in text for cue in EVIDENCE_CUES[candidate])
    ]
    tags = list(normalize_formation(label).tags)
    return formations, tags, not bool(formations)


def _canonical_for_label(label: str, record: dict[str, Any]) -> tuple[list[str], list[str], bool, bool]:
    """Return formations, tags, needs_review, unknown for one original label."""
    if _norm(label) in AMBIGUOUS_CANDIDATES:
        formations, tags, unresolved = _evidence_resolve(label, record)
        return formations, tags, unresolved, False
    result = normalize_formation(label)
    return list(result.formations), list(result.tags), result.needs_review, result.unknown


def _rewrite_candidate_objects(record: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    """Make nested AI26 export candidates canonical while preserving originals.

    The live dashboard adapter reads ``formation_candidates``. Merely adding a
    top-level ``formations`` list would therefore leave old dashboard labels in
    place. We keep an untouched ``formation_candidates_original`` snapshot and
    rewrite the dashboard-facing candidate list to one object per canonical
    formation. Unresolved candidates are omitted from that list and remain in
    the original snapshot plus the record-level review flag.
    """
    original = record.get("formation_candidates")
    if not isinstance(original, list):
        return [], False

    rewritten: list[dict[str, Any]] = []
    unresolved = False
    seen: set[tuple[str, str, str]] = set()
    for item in original:
        if not isinstance(item, dict):
            continue
        label = _candidate_label(item)
        if not label:
            continue
        formations, tags, needs_review, _unknown = _canonical_for_label(label, record)
        unresolved = unresolved or needs_review
        for formation in formations:
            candidate = copy.deepcopy(item)
            candidate["formation"] = formation
            candidate.pop("label", None)
            candidate["formation_original"] = label
            if tags:
                candidate["formation_tags"] = list(tags)
            candidate["formation_migration_version"] = MIGRATION_VERSION
            evidence = str(candidate.get("evidence") or candidate.get("evidence_quote") or "")
            key = (formation, evidence, label)
            if key not in seen:
                seen.add(key)
                rewritten.append(candidate)
    return rewritten, unresolved


def migrate_record(record: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if record.get("formation_migration_version") == MIGRATION_VERSION:
        return record, []

    labels = _labels(record)
    formations: list[str] = []
    tags: list[str] = []
    needs_review = False
    unknowns: list[str] = []

    for label in labels:
        resolved, extra_tags, unresolved, unknown = _canonical_for_label(label, record)
        for formation in resolved:
            if formation not in formations:
                formations.append(formation)
        for tag in extra_tags:
            if tag not in tags:
                tags.append(tag)
        needs_review = needs_review or unresolved
        if unknown:
            unknowns.append(label)

    migrated = dict(record)
    migrated["formations"] = formations
    migrated["formation_tags"] = tags
    migrated["formation_original"] = " | ".join(labels)
    migrated["formation_migration_version"] = MIGRATION_VERSION

    if isinstance(record.get("formation_candidates"), list):
        migrated["formation_candidates_original"] = copy.deepcopy(record["formation_candidates"])
        rewritten, nested_unresolved = _rewrite_candidate_objects(record)
        migrated["formation_candidates"] = rewritten
        needs_review = needs_review or nested_unresolved

    migrated["formation_needs_review"] = bool(needs_review)
    return migrated, unknowns


def _read(path: Path) -> tuple[list[dict[str, Any]], str]:
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ], "jsonl"
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data, "json"
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"], "wrapped"
    raise ValueError(f"unsupported JSON shape: {path}")


def _write(path: Path, records: list[dict[str, Any]], mode: str, original: Path) -> None:
    if mode == "jsonl":
        path.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n",
            encoding="utf-8",
        )
    elif mode == "json":
        path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        wrapper = json.loads(original.read_text(encoding="utf-8"))
        wrapper["records"] = records
        path.write_text(json.dumps(wrapper, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Migrate analyzed AI26 formation labels to ai26-simple-v1"
    )
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--in-place", action="store_true")
    args = ap.parse_args()

    for path in args.paths:
        if not _is_allowed(path):
            raise SystemExit(f"refusing non-analyzed/raw-looking path: {path}")
        records, mode = _read(path)
        before = Counter(label for r in records for label in _labels(r))
        migrated: list[dict[str, Any]] = []
        unknowns: list[str] = []
        for record in records:
            out, unknown = migrate_record(record)
            migrated.append(out)
            unknowns.extend(unknown)
        after = Counter(f for r in migrated for f in r.get("formations", []))
        multi = sum(len(r.get("formations", [])) > 1 for r in migrated)
        review = sum(bool(r.get("formation_needs_review")) for r in migrated)

        print(f"{path}: records={len(records)} multi_label={multi} needs_review={review}")
        print("before:", dict(before))
        print("after:", dict(after))
        if unknowns:
            print("unknown labels:", sorted(set(unknowns)))
        if args.dry_run:
            continue

        if args.in_place:
            backup = path.with_suffix(path.suffix + ".bak")
            if not backup.exists():
                shutil.copy2(path, backup)
            target = path
        else:
            target = path.with_name(path.stem + ".ai26-simple" + path.suffix)
        _write(target, migrated, mode, path)
        print("wrote:", target)


if __name__ == "__main__":
    main()
