"""Runtime integration for configurable analysis context profiles.

This module deliberately wraps the historical root ``pipeline.py`` instead of
changing its default behaviour.  A profile is active only when a canonical run
explicitly selects ``dataset.pipeline.context_profile`` (or a benchmark passes a
profile directly).  Legacy/direct pipeline callers therefore keep byte-for-byte
context behaviour unless they opt in.
"""
from __future__ import annotations

import hashlib
import json
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable

from laclaugpt.context_profiles import ContextProfile, load_profile

logger = logging.getLogger("laclaugpt.context")

_EMPTY_CONTEXT_MARKERS = (
    "(no established codebook entries match this chunk yet)",
    "(context memory disabled for this analysis profile)",
    "(context memory disabled by selected context profile)",
)


def _state_payload(path: str | Path, max_chars: int) -> tuple[str, dict[str, Any]]:
    """Load previous daily/batch state with an explicit trust boundary."""
    source = Path(path)
    raw = source.read_text(encoding="utf-8")
    trust = "model_proposed"
    review_status = ""
    text = raw.strip()
    if source.suffix.casefold() == ".json":
        payload = json.loads(raw)
        if isinstance(payload, dict):
            review_status = str(payload.get("review_status") or "").casefold()
            if review_status in {"human_reviewed", "accepted", "source_fact"}:
                trust = review_status
        text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    warning = (
        "HUMAN-REVIEWED SITUATIONAL STATE. Source documents remain primary evidence."
        if trust != "model_proposed"
        else "UNTRUSTED PRIOR STATE. Orientation only: never treat prior model output as evidence or ground truth."
    )
    clipped = text[:max_chars] if max_chars > 0 else ""
    block = f"{warning}\n{clipped}" if clipped else ""
    return block, {
        # Keep operational/private directory layouts out of exported provenance.
        # The content hash identifies the exact state artifact reproducibly.
        "source": source.name,
        "sha256": digest,
        "trust": trust,
        "review_status": review_status,
        "chars": len(clipped),
    }


def _is_missing_codebook(block: str) -> bool:
    stripped = (block or "").strip()
    return not stripped or any(stripped.startswith(marker) for marker in _EMPTY_CONTEXT_MARKERS)


def build_context_block(stage: Any, text: str, kinds: Iterable[str],
                        profile: ContextProfile) -> tuple[str, dict[str, Any]]:
    """Build one bounded prompt context and provenance record."""
    kinds = tuple(kinds)
    if not profile.context_memory or not stage.run.enabled("context_memory"):
        memory_block = "(context memory disabled by selected context profile)"
    else:
        memory_block = stage.memory.context_prompt_block(
            text,
            top_k_per_kind=profile.glossary_top_k,
            kinds=kinds,
        )

    missing_codebook = _is_missing_codebook(memory_block)
    required = stage.stage_name in profile.codebook_required_stages and profile.inject_codebook
    if required and missing_codebook:
        message = (
            f"required codebook context is missing for stage {stage.stage_name!r} "
            f"under profile {profile.name!r}"
        )
        if profile.fail_on_missing_codebook:
            raise RuntimeError(message)
        logger.warning(message)

    blocks = [memory_block] if profile.inject_codebook else []
    state_provenance: dict[str, Any] | None = None
    previous_state = getattr(stage.run, "previous_batch_summary", "")
    if profile.inject_previous_batch_summary and previous_state:
        state_block, state_provenance = _state_payload(
            previous_state,
            max(0, profile.max_context_chars // 2),
        )
        if state_block:
            blocks.append("PREVIOUS BATCH / DAILY SITUATIONAL STATE:\n" + state_block)

    corpus_stats = getattr(stage.run, "corpus_stats_path", "")
    corpus_stats_provenance: dict[str, Any] | None = None
    if profile.inject_corpus_stats and corpus_stats:
        stats_block, corpus_stats_provenance = _state_payload(
            corpus_stats,
            max(0, profile.max_context_chars // 3),
        )
        if stats_block:
            blocks.append("DESCRIPTIVE CORPUS STATE:\n" + stats_block)

    combined = "\n\n".join(block for block in blocks if block).strip()
    if len(combined) > profile.max_context_chars:
        combined = combined[:profile.max_context_chars]
    digest = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    provenance = {
        "profile": profile.name,
        "stage": stage.stage_name,
        "kinds": list(kinds),
        "glossary_top_k": profile.glossary_top_k,
        "chars": len(combined),
        "sha256": digest,
        "codebook_required": required,
        "codebook_missing": bool(required and missing_codebook),
        "previous_batch_summary": state_provenance,
        "corpus_stats": corpus_stats_provenance,
        "vector_rag": profile.vector_rag,
    }
    return combined or "(no context selected for this stage)", provenance


@contextmanager
def _patched_stage_context(pipeline_module: Any, profile: ContextProfile):
    """Temporarily apply profile-aware context to root pipeline Stage objects."""
    Stage = pipeline_module.Stage
    original_memory_context = Stage.memory_context
    original_provenance = Stage.provenance

    def memory_context(self, text: str, kinds=None):
        selected = tuple(kinds) if kinds is not None else tuple(pipeline_module.KINDS)
        block, provenance = build_context_block(self, text, selected, profile)
        self._context_provenance = provenance
        return block

    def provenance(self):
        payload = original_provenance(self)
        context = getattr(self, "_context_provenance", None)
        if profile.context_provenance and context is not None:
            payload["context"] = context
        return payload

    Stage.memory_context = memory_context
    Stage.provenance = provenance
    try:
        yield
    finally:
        Stage.memory_context = original_memory_context
        Stage.provenance = original_provenance


def run_pipeline_with_context_profile(run_config: Any, csv_path: str,
                                      dry_run: bool = False,
                                      output_path: str | None = None):
    """Run the canonical root pipeline with an explicit context profile.

    If ``run_config.context_profile`` is empty, delegation is direct and current
    production behaviour is unchanged.  This is the feature-flag boundary for
    issue #140.
    """
    import pipeline as root_pipeline

    profile_name = str(getattr(run_config, "context_profile", "") or "").strip()
    if not profile_name:
        return root_pipeline.run_pipeline(run_config, csv_path, dry_run, output_path)

    profile = load_profile(profile_name)
    with _patched_stage_context(root_pipeline, profile):
        return root_pipeline.run_pipeline(run_config, csv_path, dry_run, output_path)
