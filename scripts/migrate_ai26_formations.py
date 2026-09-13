#!/usr/bin/env python3
"""Migrate analyzed AI26 JSON/JSONL records to the simple formation taxonomy.

The utility is intentionally conservative:
- it refuses paths that look like raw/source/collection data;
- it never calls an LLM merely to rename labels;
- deterministic aliases are migrated directly;
- ambiguous legacy labels are resolved only when the analyzed record contains
  supporting textual evidence; otherwise they are retained in provenance and
  flagged for human review;
- output is written to a sibling ``.ai26-simple`` file by default.  ``--in-place``
  requires an explicit opt-in and creates a backup first.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import re
import shutil
import sys
from typing import Any

# Make ``python scripts/migrate_ai26_formations.py ...`` work from a checkout.
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

# Strong evidence cues used only for labels that the migration table marks as
# context-dependent.  These cues are deliberately narrow: uncertain cases stay
# reviewable instead of being forced into a canonical bucket.
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


def _labels(record: dict[str, Any]) -> list[str]:
    """Read common historical formation representations."""
    value = record.get("formations", record.get("formation", []))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]

    # Canonical/interchange-derived exports may carry candidate objects instead
    # of a top-level formation field.
    candidates = record.get("formation_candidates") or []
    labels: list[str] = []
    for item in candidates:
        if not isinstance(item, dict):
            continue
        candidate = item.get("formation", item.get("label", ""))
        if isinstance(candidate, dict):
            candidate = candidate.get("label", "")
        if str(candidate or "").strip():
            labels.append(str(candidate).strip())
    return labels


def _record_text(record: dict[str, Any]) -> str:
    """Collect already-analyzed evidence fields without using actor identity."""
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
    """Resolve context-dependent aliases only from analyzed textual evidence."""
    key = _norm(label)
    candidates = AMBIGUOUS_CANDIDATES.get(key)
    if not candidates:
        return [], [], True
    text = _record_text(record)
    formations: list[str] = []
    for candidate in candidates:
        if any(cue in text for cue in EVIDENCE_CUES[candidate]):
            formations.append(candidate)

    tags = list(normalize_formation(label).tags)
    # If the old label itself names a modifier, retain it as a facet even when
    # the formation cannot be safely resolved.
    if key == "institutional/policy-driven ai governance" and "policy_governance" not in tags:
        tags.append("policy_governance")
    elif key == "left techno-optimism / open source advocacy" and "open_source_advocacy" not in tags:
        tags.append("open_source_advocacy")
    elif key == "ai alignment/safety research discourse" and "alignment_research" not in tags:
        tags.append("alignment_research")
    elif key == "technical ai safety / auditism" and "auditism" not in tags:
        tags.append("auditism")
    elif key == "x-risk doomerism / safety-centric accelerationism" and "safety_centric_accelerationism" not in tags:
        tags.append("safety_centric_accelerationism")

    return formations, tags, not bool(formations)


def migrate_record(record: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    if record.get("formation_migration_version") == MIGRATION_VERSION:
        return record, []

    labels = _labels(record)
    deterministic = [
        label for label in labels if _norm(label) not in AMBIGUOUS_CANDIDATES
    ]
    result = normalize_formations(deterministic)
    formations = list(result.formations)
    tags = list(result.tags)
    needs_review = result.needs_review
    unknowns = [label for label in deterministic if normalize_formation(label).unknown]

    for label in labels:
        if _norm(label) not in AMBIGUOUS_CANDIDATES:
            continue
        resolved, extra_tags, unresolved = _evidence_resolve(label, record)
        for formation in resolved:
            if formation not in formations:
                formations.append(formation)
        for tag in extra_tags:
            if tag not in tags:
                tags.append(tag)
        needs_review = needs_review or unresolved

    migrated = dict(record)
    migrated["formations"] = formations
    migrated["formation_tags"] = tags
    migrated["formation_original"] = " | ".join(labels)
    migrated["formation_migration_version"] = MIGRATION_VERSION
    migrated["formation_needs_review"] = bool(needs_review)
    return migrated, unknowns


def _read(path: Path) -> tuple[list[dict[str, Any]], str]:
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        rows = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return rows, "jsonl"
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
        path.write_text(
            json.dumps(records, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        wrapper = json.loads(original.read_text(encoding="utf-8"))
        wrapper["records"] = records
        path.write_text(
            json.dumps(wrapper, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


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
