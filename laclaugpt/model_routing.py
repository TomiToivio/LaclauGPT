# -*- coding: utf-8 -*-
"""Task-difficulty model routing for local Gemma 4 variants.

The checked-in routing remains conservative until issue #136's reproducible
benchmark is completed. Operators may override a stage with environment variable
``LACLAUGPT_MODEL_<STAGE>`` without editing public code; the actual selected tag
is returned for provenance. Embeddings use a separate configurable model because
retrieval/similarity should not be routed through a chat model.

Routing by pipeline stage (STAGE_ROUTING, canonical defaults below):
    summary      -> e4b   (gemma4:e4b)
    discourse    -> 12b   (batiai/gemma4-12b:q6)
    postprocess  -> e2b   (gemma4:e2b)
    populism     -> 12b   (batiai/gemma4-12b:q6)
    entities     -> e2b   (gemma4:e2b)
    sentiment    -> e2b   (gemma4:e2b)
    topics       -> 12b   (batiai/gemma4-12b:q6)
    temporal     -> 12b   (batiai/gemma4-12b:q6)

Corpus synthesis is intentionally not added to the default table yet. The
benchmark hypothesis is gemma4:26b for synthesis/temporal comparison, but issue
#136 explicitly requires measurement before changing default routing.
"""
from __future__ import annotations

import json
import os
import subprocess
from functools import lru_cache

MODELS = {
    "e2b": "gemma4:e2b",
    "e4b": "gemma4:e4b",
    "12b": "batiai/gemma4-12b:q6",
    "26b": "gemma4:26b",
    "31b": "gemma4:31b",
}

EMBEDDING_MODEL = os.environ.get("LACLAUGPT_EMBEDDING_MODEL", "embeddinggemma")

# Ascending capability order for fallback walks. 31b is benchmark/reference
# capacity, not a current default pipeline route.
CAPABILITY_ORDER = ["e2b", "e4b", "12b", "26b", "31b"]

# Public routing policy only. Host-specific capacity measurements and residency
# decisions belong in private/runtime deployment notes, not in this module.
STAGE_ROUTING = {
    "summary": "e4b",
    "discourse": "12b",
    "postprocess": "e2b",
    "populism": "12b",
    "entities": "e2b",
    "sentiment": "e2b",
    "topics": "12b",
    "temporal": "12b",
}

# Texts longer than this escalate cheap e2b/e4b stages to the currently available
# high-capability tier. This preserves the historical behavior without changing
# theory-sensitive stage defaults.
LONG_TEXT_CHARS = 8000

# Standard public loopback default. Production endpoints must be supplied via
# the environment/private deployment configuration.
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")


@lru_cache(maxsize=1)
def _loaded_models() -> set[str]:
    """Names of models present in the local Ollama instance."""
    try:
        raw = subprocess.run(
            ["curl", "-s", f"{OLLAMA_HOST}/api/tags"],
            capture_output=True, text=True, timeout=10).stdout
        return {m["name"] for m in json.loads(raw).get("models", [])}
    except Exception:
        return set()


@lru_cache(maxsize=1)
def _free_vram_gb() -> float:
    """Free VRAM across GPUs, best-effort via nvidia-smi."""
    try:
        raw = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10).stdout
        per_gpu = [int(x) for x in raw.strip().splitlines() if x.strip()]
        return max(per_gpu, default=0) / 1024.0
    except Exception:
        return 0.0


def _stage_override(stage: str) -> str:
    key = "LACLAUGPT_MODEL_" + stage.upper().replace("-", "_")
    return os.environ.get(key, "").strip()


def pick_model(stage: str, text_len: int = 0) -> str:
    """Resolve the local model for one pipeline stage.

    An explicit ``LACLAUGPT_MODEL_<STAGE>`` tag wins and is returned unchanged so
    stage-level model choice can be configured externally and recorded in
    provenance. Without an override: stage routing -> long-text escalation ->
    availability/VRAM fallback. Raises if no configured local model is available.
    """
    override = _stage_override(stage)
    if override:
        return override

    tier = STAGE_ROUTING.get(stage, "26b")
    if text_len > LONG_TEXT_CHARS and tier in ("e2b", "e4b"):
        tier = "26b"
    loaded = _loaded_models()
    free = _free_vram_gb()
    start = CAPABILITY_ORDER.index(tier)
    need_gb = {"e2b": 6, "e4b": 8, "12b": 13, "26b": 17, "31b": 20}
    for name in reversed(CAPABILITY_ORDER[:start + 1]):
        tag = MODELS[name]
        if tag not in loaded:
            continue
        if free == 0 or free >= need_gb[name] * 0.9:
            return tag
    for name in CAPABILITY_ORDER:
        if MODELS[name] in loaded:
            return MODELS[name]
    raise RuntimeError("no configured local model available on this Ollama host")


def pick_embedding_model() -> str:
    """Return the configured embedding-specific Ollama model tag."""
    return EMBEDDING_MODEL


def routing_table() -> dict:
    """Resolved routing for logging/provenance."""
    return {stage: pick_model(stage) for stage in STAGE_ROUTING}
