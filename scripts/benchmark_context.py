#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Benchmark context strategies on the same human-reviewed sample (issue #140).

The public repository supplies the harness; human-reviewed research samples may
remain private. Full mode runs the *same* canonical analysis configuration with
only the context profile changed, then reports safe aggregate quality/resource
metrics. Dry mode validates the experiment matrix without invoking an LLM.

Example:
  python3 scripts/benchmark_context.py \
      --sample /private/gold_sample.csv --project ai26 --arena grassroots \
      --machine roihu --profiles balanced,high_accuracy,validation --full \
      --previous-state /private/reports/previous-day.json \
      --out /private/context_benchmark.json
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

try:  # Unix-only; benchmark remains usable on Windows without RSS telemetry.
    import resource
except ImportError:  # pragma: no cover - exercised on Windows
    resource = None

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def _labels(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, float) and value != value:  # NaN
        return set()
    text = str(value).strip()
    if not text:
        return set()
    for sep in ("|", ";"):
        if sep in text:
            return {part.strip().casefold() for part in text.split(sep) if part.strip()}
    return {text.casefold()}


def _bool(value: Any) -> bool | None:
    text = str(value or "").strip().casefold()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def _safe_div(num: int | float, den: int | float) -> float | None:
    return round(float(num) / float(den), 4) if den else None


def _max_rss() -> int | None:
    if resource is None:
        return None
    return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


def _score(sample_csv: Path, annotations: list[Any]) -> dict[str, Any]:
    import pandas as pd
    from pipeline import document_key

    frame = pd.read_csv(sample_csv)
    gold = {document_key(row): row.to_dict() for _, row in frame.iterrows()}

    evidence_total = evidence_verified = 0
    refs_total = refs_with_id = 0
    populism_total = populism_agree = 0
    entity_tp = entity_fp = entity_fn = 0
    frame_tp = frame_fp = frame_fn = 0
    context_chars = 0
    context_calls = 0
    missing_required_codebooks = 0

    evidence_fields = (
        "signifier_roles", "articulations", "imaginaries",
        "formation_candidates", "populism_elements", "hegemonic_evidence",
    )
    ref_fields = ("entities", "topics", "signifiers", "us", "frontier")

    for ann in annotations:
        row = gold.get(ann.document_id, {})
        for field in evidence_fields:
            for item in getattr(ann, field, []) or []:
                if hasattr(item, "evidence_verified"):
                    evidence_total += 1
                    evidence_verified += int(bool(item.evidence_verified))
        for field in ref_fields:
            for item in getattr(ann, field, []) or []:
                refs_total += 1
                refs_with_id += int(bool(getattr(item, "obj_id", "")))

        gold_pop = _bool(row.get("gold_populist", row.get("human_populist")))
        if gold_pop is not None and ann.populist is not None:
            populism_total += 1
            populism_agree += int(bool(ann.populist) == gold_pop)

        gold_entities = _labels(row.get("gold_entities", row.get("human_entities")))
        if gold_entities:
            predicted = {str(item.label).casefold() for item in ann.entities}
            entity_tp += len(predicted & gold_entities)
            entity_fp += len(predicted - gold_entities)
            entity_fn += len(gold_entities - predicted)

        gold_frames = _labels(row.get("gold_frames", row.get("human_frames")))
        if gold_frames:
            predicted_frames = {
                str(item.formation.label).casefold()
                for item in ann.formation_candidates
                if getattr(item, "formation", None)
            }
            frame_tp += len(predicted_frames & gold_frames)
            frame_fp += len(predicted_frames - gold_frames)
            frame_fn += len(gold_frames - predicted_frames)

        stages = (ann.collection_provenance or {}).get("llm_stages", {})
        for stage in stages.values():
            context = (stage or {}).get("context") or {}
            if context:
                context_calls += 1
                context_chars += int(context.get("chars") or 0)
                missing_required_codebooks += int(bool(context.get("codebook_missing")))

    return {
        "documents": len(annotations),
        "populism_agreement": _safe_div(populism_agree, populism_total),
        "populism_gold_n": populism_total,
        "entity_precision": _safe_div(entity_tp, entity_tp + entity_fp),
        "entity_recall": _safe_div(entity_tp, entity_tp + entity_fn),
        "frame_precision": _safe_div(frame_tp, frame_tp + frame_fp),
        "frame_recall": _safe_div(frame_tp, frame_tp + frame_fn),
        "evidence_fidelity": _safe_div(evidence_verified, evidence_total),
        "unsupported_evidence_rate": (
            _safe_div(evidence_total - evidence_verified, evidence_total)
        ),
        "canonical_id_rate": _safe_div(refs_with_id, refs_total),
        "context_calls": context_calls,
        "context_chars_total": context_chars,
        "context_chars_mean": _safe_div(context_chars, context_calls),
        "missing_required_codebooks": missing_required_codebooks,
    }


def _prepare_run(args, profile_name: str, work_dir: Path):
    from laclaugpt.config import compose_config
    from laclaugpt.context_profiles import apply_profile, load_profile
    from run_config import run_config_from_effective

    dataset_override: dict[str, Any] = {
        "input": str(args.sample),
        "output": str(work_dir / "annotations.jsonl"),
        "storage": {"work_dir": str(work_dir)},
        "pipeline": {"context_profile": profile_name},
    }
    if args.model:
        dataset_override["model"] = {"text": args.model}
    effective = compose_config(
        args.project,
        args.machine,
        args.execution,
        {"dataset": dataset_override},
        arena=args.arena,
    )
    run = run_config_from_effective(
        effective,
        run_id=f"context-benchmark-{profile_name}",
        repository_root=REPO,
    )
    apply_profile(run, load_profile(profile_name))
    if args.previous_state:
        run.previous_batch_summary = str(args.previous_state)
    if args.corpus_stats:
        run.corpus_stats_path = str(args.corpus_stats)
    return run


def run_one(args, profile_name: str) -> dict[str, Any]:
    from laclaugpt.context_profiles import load_profile
    from laclaugpt.context_runtime import run_pipeline_with_context_profile

    profile = load_profile(profile_name)
    if not args.full:
        return {
            "profile": profile_name,
            "status": "configured",
            "profile_config": profile.to_dict(),
            "note": "dry matrix only; use --full for quality/resource metrics",
        }

    before = _max_rss()
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix=f"laclaugpt-context-{profile_name}-") as tmp:
        work_dir = Path(tmp)
        run = _prepare_run(args, profile_name, work_dir)
        annotations = run_pipeline_with_context_profile(
            run,
            csv_path=str(args.sample),
            dry_run=False,
            output_path=str(work_dir / "annotations.jsonl"),
        )
        metrics = _score(args.sample, annotations)
    wall = time.perf_counter() - started
    after = _max_rss()
    rss_delta = None if before is None or after is None else max(0, after - before)
    return {
        "profile": profile_name,
        "status": "ok",
        "wall_seconds": round(wall, 3),
        "throughput_docs_per_second": _safe_div(metrics["documents"], wall),
        "max_rss_delta": rss_delta,
        "profile_config": profile.to_dict(),
        "metrics": metrics,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sample", type=Path, required=True,
                    help="human-reviewed sample CSV (may live outside this repo)")
    ap.add_argument("--project", default="ai26")
    ap.add_argument("--arena", required=True,
                    help="canonical arena belonging to --project")
    ap.add_argument("--machine", default="laptop-ollama")
    ap.add_argument("--execution", default="cli")
    ap.add_argument("--profiles", "--runs", dest="profiles",
                    default="balanced,fast_local")
    ap.add_argument("--model", default=None,
                    help="optional model override; keep identical across profiles")
    ap.add_argument("--previous-state", type=Path,
                    help="previous daily/batch JSON or Markdown for state-aware profiles")
    ap.add_argument("--corpus-stats", type=Path,
                    help="optional descriptive corpus-state file")
    ap.add_argument("--full", action="store_true",
                    help="execute LLM analysis; otherwise validate experiment matrix")
    ap.add_argument("--out", type=Path, default=Path("benchmark_results.json"))
    args = ap.parse_args()

    results = {
        "sample": str(args.sample),
        "project": args.project,
        "arena": args.arena,
        "machine": args.machine,
        "full": args.full,
        "previous_state": str(args.previous_state or ""),
        "runs": [],
    }
    for name in [s.strip() for s in args.profiles.split(",") if s.strip()]:
        try:
            entry = run_one(args, name)
        except Exception as exc:  # record one failed arm without hiding others
            entry = {
                "profile": name,
                "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
            }
        results["runs"].append(entry)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(f"results -> {args.out}")
    return 0 if all(r["status"] != "error" for r in results["runs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
