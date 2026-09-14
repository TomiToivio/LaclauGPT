"""Deterministic input-sufficiency checks before interpretive analysis.

This module deliberately separates *source sufficiency* from model confidence,
quotation verification, and substantive theoretical validity.  It provides a
small project-neutral gate that callers can use before expensive or highly
interpretive stages such as discourse, ideology, or populism coding.

The gate never decides whether a claim is true or political.  It only asks
whether at least one configured evidence channel contains enough observable
material to justify interpretive analysis.  Abstention is an expected result.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Iterable, Literal

EvidenceMode = Literal[
    "text",
    "ocr_only",
    "vision_only",
    "multimodal",
    "none",
]
EvidenceStatus = Literal["sufficient", "insufficient"]

_WORD_RE = re.compile(r"\b[^\W\d_]{2,}\b", re.UNICODE)
_DEFAULT_OCR_NOISE = frozenset(
    {
        "cc",
        "id",
        "ui",
        "www",
        "http",
        "https",
    }
)


@dataclass(frozen=True)
class EvidenceQuality:
    """Result of a deterministic source-sufficiency assessment."""

    status: EvidenceStatus
    mode: EvidenceMode
    reason: str
    transcript_usable: bool
    ocr_usable: bool
    visual_usable: bool
    allow_interpretive_analysis: bool

    def as_dict(self) -> dict:
        return asdict(self)


def _words(text: str) -> list[str]:
    return _WORD_RE.findall(str(text or ""))


def _ocr_signal(
    text: str,
    *,
    noise_tokens: Iterable[str] = _DEFAULT_OCR_NOISE,
) -> tuple[int, int, float]:
    """Return ``(word_count, content_words, content_ratio)`` for OCR text.

    The heuristic is intentionally simple and deterministic.  Project-specific
    pipelines may provide a different noise vocabulary or stricter thresholds,
    but callers should not silently convert fragmentary OCR into substantive
    evidence merely because a string is non-empty.
    """

    words = _words(text)
    noise = {str(token).strip().casefold() for token in noise_tokens}
    content = [word for word in words if word.casefold() not in noise]
    ratio = len(content) / len(words) if words else 0.0
    return len(words), len(content), ratio


def assess_evidence(
    *,
    transcript: str = "",
    ocr_text: str = "",
    visual_observations: str = "",
    visual_status: str = "",
    min_transcript_words: int = 12,
    min_ocr_content_words: int = 12,
    min_ocr_content_ratio: float = 0.5,
    noise_tokens: Iterable[str] = _DEFAULT_OCR_NOISE,
) -> EvidenceQuality:
    """Assess whether observable source material supports interpretation.

    Parameters are intentionally exposed rather than hard-coded to a single
    study.  ``visual_status`` is optional; when supplied it must indicate a
    successful or partially successful visual stage before visual observations
    count as usable.
    """

    transcript_words = _words(transcript)
    transcript_usable = len(transcript_words) >= min_transcript_words

    ocr_words, ocr_content_words, ocr_ratio = _ocr_signal(
        ocr_text,
        noise_tokens=noise_tokens,
    )
    ocr_usable = bool(str(ocr_text or "").strip()) and (
        ocr_content_words >= min_ocr_content_words
        and ocr_ratio >= min_ocr_content_ratio
    )

    visual_text = str(visual_observations or "").strip()
    status = str(visual_status or "").strip().casefold()
    visual_status_ok = not status or status in {
        "ok",
        "partial",
        "available",
        "succeeded",
        "success",
    }
    visual_usable = bool(visual_text) and visual_status_ok

    usable_channels = sum((transcript_usable, ocr_usable, visual_usable))
    if usable_channels >= 2:
        mode: EvidenceMode = "multimodal"
    elif transcript_usable:
        mode = "text"
    elif ocr_usable:
        mode = "ocr_only"
    elif visual_usable:
        mode = "vision_only"
    else:
        mode = "none"

    allow = mode != "none"
    if allow:
        reason = f"usable source evidence via {mode} channel(s)"
        quality_status: EvidenceStatus = "sufficient"
    else:
        reason = (
            "insufficient observable source evidence: "
            f"transcript_words={len(transcript_words)}, "
            f"ocr_words={ocr_words}, "
            f"ocr_content_words={ocr_content_words}, "
            f"ocr_content_ratio={ocr_ratio:.2f}, "
            f"visual_status={status or 'unspecified'}"
        )
        quality_status = "insufficient"

    return EvidenceQuality(
        status=quality_status,
        mode=mode,
        reason=reason,
        transcript_usable=transcript_usable,
        ocr_usable=ocr_usable,
        visual_usable=visual_usable,
        allow_interpretive_analysis=allow,
    )
