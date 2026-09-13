# -*- coding: utf-8 -*-
"""Generic legacy ASR compatibility helpers."""
from __future__ import annotations

import json
import time
from pathlib import Path

import legacy_fetch

DEFAULT_MODEL = "large-v3"
DEFAULT_DEVICE = "auto"
DEFAULT_COMPUTE = "auto"
TRANSCRIPT_VERSION = "legacy-asr-1.0"


def transcribe_video(video_path: str | Path, *, model_size: str = DEFAULT_MODEL,
                     device: str = DEFAULT_DEVICE, compute_type: str = DEFAULT_COMPUTE,
                     language: str | None = None, model=None):
    if model is None:
        from faster_whisper import WhisperModel
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
    segments, info = model.transcribe(str(video_path), vad_filter=True, language=language)
    parts = [(seg.text or "").strip() for seg in segments]
    return {
        "transcript": " ".join(x for x in parts if x),
        "language": info.language,
        "language_probability": round(float(info.language_probability), 4),
        "duration": round(float(info.duration), 2),
    }


def transcribe_manifest(manifest_path: str | Path, videos_dir: str | Path,
                        out_path: str | Path, *, model_size: str = DEFAULT_MODEL,
                        device: str = DEFAULT_DEVICE, compute_type: str = DEFAULT_COMPUTE,
                        model=None) -> int:
    pairs = legacy_fetch.load_manifest(manifest_path)
    videos_dir = Path(videos_dir)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line).get("document_id", ""))
    written = 0
    with open(out_path, "a", encoding="utf-8") as out:
        for doc_id, url in pairs:
            if doc_id in done:
                continue
            video = legacy_fetch._dest_for(videos_dir, url)
            if not video.exists():
                raise FileNotFoundError(f"video for {doc_id} not fetched")
            result = transcribe_video(video, model_size=model_size, device=device,
                                      compute_type=compute_type, model=model)
            record = {
                "document_id": doc_id,
                "source_url": url,
                "transcript_version": TRANSCRIPT_VERSION,
                "model": model_size if model is None else getattr(model, "model_size_or_path", model_size),
                "vad_filter": True,
                "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
                **result,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1
    return written


def write_slurm_script(path: str | Path, dataset: str, *, time_limit: str = "04:00:00") -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"""#!/bin/bash
#SBATCH --job-name=legacy_asr_{dataset}
#SBATCH --time={time_limit}
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --gpus=1
set -euo pipefail
: "${{LACLAUGPT_REPO_ROOT:?set LACLAUGPT_REPO_ROOT}}"
: "${{LACLAUGPT_DATA_DIR:?set LACLAUGPT_DATA_DIR}}"
REPO_ROOT=$LACLAUGPT_REPO_ROOT
DATA_ROOT=$LACLAUGPT_DATA_DIR
cd "$REPO_ROOT"
export LACLAUGPT_MEMORY_DIR=$DATA_ROOT/memory
""", encoding="utf-8")
    return path
