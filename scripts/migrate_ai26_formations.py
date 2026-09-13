#!/usr/bin/env python3
"""Migrate analyzed AI26 JSON/JSONL records to the simple formation taxonomy.

Never targets raw/source collection files.  Defaults to writing a sibling
``.ai26-simple`` output; use ``--in-place`` explicitly to replace analyzed data.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import shutil

from laclaugpt.formations import MIGRATION_VERSION, normalize_formation, normalize_formations

ANALYZED_HINTS = ("analy", "derived", "output", "export")
RAW_HINTS = ("raw", "source", "collect")


def _is_allowed(path: Path) -> bool:
    text = str(path).casefold()
    return any(x in text for x in ANALYZED_HINTS) and not any(x in text for x in RAW_HINTS)


def _labels(record: dict) -> list[str]:
    value = record.get("formations", record.get("formation", []))
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    return []


def migrate_record(record: dict) -> tuple[dict, list[str]]:
    if record.get("formation_migration_version") == MIGRATION_VERSION:
        return record, []
    labels = _labels(record)
    result = normalize_formations(labels)
    migrated = dict(record)
    migrated.update(result.as_dict())
    unknown = [label for label in labels if normalize_formation(label).unknown]
    return migrated, unknown


def _read(path: Path):
    if path.suffix.lower() in {".jsonl", ".ndjson"}:
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()], "jsonl"
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data, "json"
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"], "wrapped"
    raise ValueError(f"unsupported JSON shape: {path}")


def _write(path: Path, records: list[dict], mode: str, original: Path) -> None:
    if mode == "jsonl":
        path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    elif mode == "json":
        path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        wrapper = json.loads(original.read_text(encoding="utf-8")); wrapper["records"] = records
        path.write_text(json.dumps(wrapper, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--in-place", action="store_true")
    args = ap.parse_args()
    for path in args.paths:
        if not _is_allowed(path):
            raise SystemExit(f"refusing non-analyzed/raw-looking path: {path}")
        records, mode = _read(path)
        before = Counter(label for r in records for label in _labels(r))
        migrated, unknowns = [], []
        for record in records:
            out, unknown = migrate_record(record); migrated.append(out); unknowns.extend(unknown)
        after = Counter(f for r in migrated for f in r.get("formations", []))
        multi = sum(len(r.get("formations", [])) > 1 for r in migrated)
        review = sum(bool(r.get("formation_needs_review")) for r in migrated)
        print(f"{path}: records={len(records)} multi_label={multi} needs_review={review}")
        print("before:", dict(before)); print("after:", dict(after))
        if unknowns: print("unknown labels:", sorted(set(unknowns)))
        if args.dry_run: continue
        if args.in_place:
            backup = path.with_suffix(path.suffix + ".bak")
            if not backup.exists(): shutil.copy2(path, backup)
            target = path
        else:
            target = path.with_name(path.stem + ".ai26-simple" + path.suffix)
        _write(target, migrated, mode, path)
        print("wrote:", target)


if __name__ == "__main__":
    main()
