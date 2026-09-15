#!/usr/bin/env python3
"""Reproducible local Ollama routing benchmark for issue #136.

Input is JSONL with one safely publishable/private-local benchmark case per line:

{
  "id": "case-001",
  "task": "discourse",
  "language": "fi",
  "source_text": "...",
  "prompt": "Return JSON ...",
  "required_keys": ["signifiers", "evidence"],
  "expected_terms": ["AI"],
  "evidence_fields": ["evidence", "evidence_quotes"]
}

The harness never uploads benchmark text. It talks only to the configured local
Ollama host, records generic aggregate/per-case metrics, and can be run on any
machine without committing hardware inventory or corpus content to the repo.
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import time
from pathlib import Path
from typing import Any, Iterable

import ollama

DEFAULT_MODELS = [
    "gemma4:e2b",
    "gemma4:e4b",
    "gemma4:12b",
    "gemma4:26b",
    "gemma4:31b",
    "qwen3:30b",
]


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            cases.append(json.loads(line))
    return cases


def _walk_values(value: Any, keys: set[str]) -> Iterable[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in keys:
                if isinstance(item, str):
                    yield item
                elif isinstance(item, list):
                    for part in item:
                        if isinstance(part, str):
                            yield part
                        elif isinstance(part, dict):
                            yield from _walk_values(part, keys)
            yield from _walk_values(item, keys)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_values(item, keys)


def _term_recall(payload: Any, expected_terms: list[str]) -> float | None:
    if not expected_terms:
        return None
    haystack = json.dumps(payload, ensure_ascii=False).casefold()
    hits = sum(term.casefold() in haystack for term in expected_terms)
    return hits / len(expected_terms)


def _evidence_fidelity(
    payload: Any, source_text: str, evidence_fields: list[str]
) -> tuple[float | None, int]:
    evidence = [
        item.strip()
        for item in _walk_values(payload, set(evidence_fields))
        if item.strip()
    ]
    if not evidence:
        return None, 0
    source = source_text.casefold()
    matched = sum(item.casefold() in source for item in evidence)
    hallucinated = len(evidence) - matched
    return matched / len(evidence), hallucinated


def _vram_snapshot() -> dict[str, Any]:
    try:
        proc = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=name,memory.used,memory.total",
                "--format=csv,noheader,nounits",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return {}
    rows = []
    for line in proc.stdout.splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) == 3:
            rows.append(
                {"gpu": parts[0], "memory_used_mb": parts[1], "memory_total_mb": parts[2]}
            )
    return {"gpus": rows} if rows else {}


def run_case(client: ollama.Client, model: str, case: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    error = ""
    payload: Any = None
    raw = ""
    try:
        response = client.chat(
            model=model,
            messages=[{"role": "user", "content": str(case["prompt"])}],
            format="json",
            options={"temperature": 0},
        )
        raw = response.message.content or ""
        payload = json.loads(raw)
    except Exception as exc:  # benchmark must record, not hide, model failures
        error = f"{type(exc).__name__}: {exc}"
    seconds = time.perf_counter() - started

    required = list(case.get("required_keys") or [])
    valid = isinstance(payload, dict) and all(key in payload for key in required)
    fidelity, hallucinated = _evidence_fidelity(
        payload,
        str(case.get("source_text") or ""),
        list(case.get("evidence_fields") or ["evidence", "evidence_quote", "evidence_quotes"]),
    ) if payload is not None else (None, 0)

    return {
        "case_id": case.get("id", ""),
        "task": case.get("task", ""),
        "language": case.get("language", ""),
        "model": model,
        "seconds": seconds,
        "structured_valid": bool(valid),
        "expected_term_recall": _term_recall(payload, list(case.get("expected_terms") or []))
        if payload is not None else None,
        "evidence_fidelity": fidelity,
        "hallucinated_evidence_items": hallucinated,
        "error": error,
        "response_chars": len(raw),
    }


def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    models = sorted({row["model"] for row in rows})
    for model in models:
        subset = [row for row in rows if row["model"] == model]
        recalls = [row["expected_term_recall"] for row in subset if row["expected_term_recall"] is not None]
        fidelity = [row["evidence_fidelity"] for row in subset if row["evidence_fidelity"] is not None]
        seconds = [row["seconds"] for row in subset]
        output.append(
            {
                "model": model,
                "cases": len(subset),
                "structured_valid_rate": sum(row["structured_valid"] for row in subset) / len(subset),
                "mean_expected_term_recall": statistics.fmean(recalls) if recalls else None,
                "mean_evidence_fidelity": statistics.fmean(fidelity) if fidelity else None,
                "hallucinated_evidence_items": sum(row["hallucinated_evidence_items"] for row in subset),
                "mean_seconds": statistics.fmean(seconds) if seconds else None,
                "documents_per_minute": (60.0 / statistics.fmean(seconds)) if seconds and statistics.fmean(seconds) else None,
                "failures": sum(bool(row["error"]) for row in subset),
            }
        )
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", type=Path)
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--host", default=os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434"))
    args = parser.parse_args()

    cases = load_cases(args.cases)
    if not cases:
        raise SystemExit("benchmark case file is empty")
    client = ollama.Client(host=args.host)
    rows = [run_case(client, model, case) for model in args.models for case in cases]
    result = {
        "method_version": "1",
        "models": args.models,
        "case_count": len(cases),
        "vram_snapshot_after_run": _vram_snapshot(),
        "summary": summarize(rows),
        "rows": rows,
        "notes": [
            "Benchmark text is never sent to a cloud service by this harness.",
            "Evidence fidelity is exact-substring fidelity and should be supplemented by human review.",
            "Formation/discourse/populism quality requires human/codebook scoring in the benchmark case set.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
