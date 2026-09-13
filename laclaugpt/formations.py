"""Canonical AI26 ideological-formation normalization.

The paper deliberately treats formations as provisional sensitising concepts,
not a closed ontology.  This module therefore defines only the small public
computational vocabulary used for aggregation and comparison.  Richer research
terms remain valid in source material, theory, provenance, and secondary tags.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

MIGRATION_VERSION = "ai26-simple-v1"

CANONICAL_FORMATIONS = (
    "accelerationism",
    "doomerism",
    "left-wing accelerationism",
    "ai safety",
    "ai critical",
    "anti-ai",
)

TECHNICAL_STATES = {"other", "uncertain", "unclassified", ""}


def _norm(value: str) -> str:
    """Normalize spacing/case without erasing meaningful punctuation."""
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


ALIASES: dict[str, tuple[str, ...]] = {
    "accelerationism": ("accelerationism",),
    "x-risk doomerism": ("doomerism",),
    "left techno-optimism": ("left-wing accelerationism",),
    "techno-optimism": ("accelerationism",),
    "effective accelerationism": ("accelerationism",),
    "techno-optimism / accelerationism": ("accelerationism",),
    "institutional techno-optimism": ("accelerationism",),
    "corporate techno-optimism": ("accelerationism",),
    "institutional ai safety/governance": ("ai safety",),
    "left techno-optimism / accelerationist adjacent": ("left-wing accelerationism",),
    "institutional safetyism": ("ai safety",),
    "ai_safetyism": ("ai safety",),
    "critical ai studies": ("ai critical",),
    "technical alignmentism": ("ai safety",),
    "institutional technocratic governance": ("ai safety",),
    "techno-institutionalism": ("ai safety",),
    "tescreal": ("accelerationism",),
    "accelerationist critique of institutional capture": ("accelerationism",),
    "corporate techno-utilitarianism": ("accelerationism",),
    "x-risk doomerism / ai safety alignment": ("doomerism", "ai safety"),
    "ai safety / x-risk discourse": ("ai safety", "doomerism"),
    "left techno-optimism / institutional accelerationism": (
        "left-wing accelerationism", "accelerationism"
    ),
    "critical ai / anti-ai mobilization": ("ai critical", "anti-ai"),
    "critical ai / anti-ai mobilisation": ("ai critical", "anti-ai"),
    "left-wing techno-optimism / corporate techno-optimism": (
        "left-wing accelerationism", "accelerationism"
    ),
    # Historical public-repo labels.
    "anti-ai backlash": ("anti-ai",),
    "doomerism": ("doomerism",),
    "left-wing accelerationism": ("left-wing accelerationism",),
    "ai safety": ("ai safety",),
    "ai critical": ("ai critical",),
    "anti-ai": ("anti-ai",),
}

# These labels carry a usable formation signal plus a modifier that belongs in
# a secondary facet rather than in the formation ontology.
TAGGED_ALIASES: dict[str, tuple[tuple[str, ...], tuple[str, ...]]] = {
    "critical ai / anti-big tech": (("ai critical",), ("anti_big_tech",)),
    "critical ai / anti-hype": (("ai critical",), ("anti_hype",)),
}

# These require record-level evidence before they can be safely collapsed.
AMBIGUOUS_ALIASES: dict[str, tuple[str, ...]] = {
    "institutional/policy-driven ai governance": ("policy_governance",),
    "left techno-optimism / open source advocacy": ("open_source_advocacy",),
    "ai alignment/safety research discourse": ("alignment_research",),
    "technical ai safety / auditism": ("auditism",),
    "x-risk doomerism / safety-centric accelerationism": ("safety_centric_accelerationism",),
}


@dataclass(frozen=True)
class FormationNormalization:
    formations: tuple[str, ...]
    tags: tuple[str, ...]
    original: str
    needs_review: bool = False
    unknown: bool = False

    def as_dict(self) -> dict:
        return {
            "formations": list(self.formations),
            "formation_tags": list(self.tags),
            "formation_original": self.original,
            "formation_migration_version": MIGRATION_VERSION,
            "formation_needs_review": self.needs_review,
        }


def normalize_formation(label: str) -> FormationNormalization:
    """Normalize one historical/model-produced formation label.

    Ambiguous labels are deliberately not guessed from actor identity or label
    wording alone.  They retain provenance and are flagged for human review.
    """
    original = str(label or "").strip()
    key = _norm(original)
    if key in TECHNICAL_STATES:
        return FormationNormalization((), (), original)
    if key in TAGGED_ALIASES:
        formations, tags = TAGGED_ALIASES[key]
        return FormationNormalization(formations, tags, original)
    if key in AMBIGUOUS_ALIASES:
        return FormationNormalization((), AMBIGUOUS_ALIASES[key], original, needs_review=True)
    if key in ALIASES:
        return FormationNormalization(ALIASES[key], (), original)
    return FormationNormalization((), (), original, needs_review=True, unknown=True)


def normalize_formations(labels: Iterable[str]) -> FormationNormalization:
    """Normalize several labels while preserving order and provenance."""
    originals: list[str] = []
    formations: list[str] = []
    tags: list[str] = []
    needs_review = False
    unknown = False
    for label in labels:
        result = normalize_formation(label)
        if result.original:
            originals.append(result.original)
        for formation in result.formations:
            if formation not in formations:
                formations.append(formation)
        for tag in result.tags:
            if tag not in tags:
                tags.append(tag)
        needs_review = needs_review or result.needs_review
        unknown = unknown or result.unknown
    return FormationNormalization(
        tuple(formations), tuple(tags), " | ".join(originals), needs_review, unknown
    )
