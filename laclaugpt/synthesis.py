"""Configurable corpus-level synthesis over canonical document annotations.

This module deliberately keeps corpus claims evidence-first and provisional.
It aggregates already-analysed ``DocumentAnnotation`` objects, records the exact
included document set and provenance, and exposes explicit machine-readable
change fields.  It does not treat frequency as hegemony.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from itertools import product
from typing import Any, Callable, Iterable, Mapping, Sequence
from uuid import uuid4

from pydantic import BaseModel, Field

from laclaugpt_interchange import DocumentAnnotation


class SynthesisConfig(BaseModel):
    """Project-neutral corpus synthesis settings.

    ``group_by`` is composable. Built-in dimensions are ``date``, ``signifier``,
    ``author``, ``source_platform``/``source`` and ``formation``. Arbitrary
    source metadata can be addressed as ``metadata.<key>``.
    """

    enabled: bool = True
    group_by: list[str] = Field(default_factory=lambda: ["date"])
    minimum_documents: int = 5
    rolling_window_days: int | None = 7
    compare_previous: bool = True
    compare_periods: int = 1
    historical_baseline_days: int | None = 30
    include_intermediate_results: bool = True
    include_source_metadata: bool = True
    cadence_daily: bool = True
    every_n_documents: int | None = None
    model: str = ""
    prompt_version: str = ""
    config_version: str = "1"


class DetectedChanges(BaseModel):
    emerging_signifiers: list[str] = Field(default_factory=list)
    declining_signifiers: list[str] = Field(default_factory=list)
    emerging_formations: list[str] = Field(default_factory=list)
    declining_formations: list[str] = Field(default_factory=list)
    changed_articulations: list[str] = Field(default_factory=list)
    affect_or_sentiment_shift: list[str] = Field(default_factory=list)
    populism_shift: str = ""
    source_or_author_shift: list[str] = Field(default_factory=list)
    continuity_or_drift: str = "no baseline"


class CorpusSynthesis(BaseModel):
    synthesis_id: str
    grouping: dict[str, str]
    time_window: dict[str, str]
    document_ids: list[str]
    document_count: int
    source_distribution: dict[str, int] = Field(default_factory=dict)
    author_distribution: dict[str, int] = Field(default_factory=dict)
    signifier_distribution: dict[str, int] = Field(default_factory=dict)
    formation_distribution: dict[str, int] = Field(default_factory=dict)
    topic_distribution: dict[str, int] = Field(default_factory=dict)
    frame_or_discourse_distribution: dict[str, int] = Field(default_factory=dict)
    articulation_summary: dict[str, int] = Field(default_factory=dict)
    populism_summary: dict[str, Any] = Field(default_factory=dict)
    sentiment_affect_summary: dict[str, int] = Field(default_factory=dict)
    uncertainty_review: dict[str, Any] = Field(default_factory=dict)
    evidence_document_ids: list[str] = Field(default_factory=list)
    previous_window_reference: dict[str, Any] | None = None
    detected_changes: DetectedChanges = Field(default_factory=DetectedChanges)
    human_readable_synthesis: str = ""
    provenance: dict[str, Any] = Field(default_factory=dict)


NarrativeSynthesizer = Callable[[Mapping[str, Any]], str]


def _timestamp(annotation: DocumentAnnotation) -> str:
    return (annotation.source_timestamp or annotation.created_at or "").strip()


def _date(annotation: DocumentAnnotation) -> str:
    stamp = _timestamp(annotation)
    return stamp[:10] if len(stamp) >= 10 else "unknown"


def _metadata_lookup(annotation: DocumentAnnotation, key: str) -> list[str]:
    current: Any = {
        "collection_provenance": annotation.collection_provenance,
        "transformations": annotation.transformations,
        **(annotation.collection_provenance or {}),
        **(annotation.transformations or {}),
    }
    for part in key.split("."):
        if isinstance(current, Mapping):
            current = current.get(part)
        else:
            current = None
        if current is None:
            return ["unknown"]
    if isinstance(current, (list, tuple, set)):
        values = [str(item) for item in current if str(item).strip()]
        return values or ["unknown"]
    return [str(current)] if str(current or "").strip() else ["unknown"]


def dimension_values(annotation: DocumentAnnotation, dimension: str) -> list[str]:
    """Return one or more grouping values for a configured dimension."""
    name = dimension.strip().lower()
    if name in {"date", "day"}:
        return [_date(annotation)]
    if name == "signifier":
        return sorted({item.label for item in annotation.signifiers if item.label}) or ["none"]
    if name == "author":
        return [annotation.source_author or "unknown"]
    if name in {"source", "source_platform", "platform"}:
        return [annotation.source_platform or "unknown"]
    if name in {"formation", "formation_candidate"}:
        return sorted({item.formation.label for item in annotation.formation_candidates if item.formation.label}) or ["none"]
    if name.startswith("metadata."):
        return _metadata_lookup(annotation, dimension.split(".", 1)[1])
    value = getattr(annotation, dimension, None)
    if isinstance(value, str):
        return [value or "unknown"]
    if isinstance(value, (list, tuple, set)):
        values = [str(item) for item in value if str(item).strip()]
        return values or ["none"]
    return [str(value)] if value is not None else ["unknown"]


def group_annotations(
    annotations: Sequence[DocumentAnnotation], group_by: Sequence[str]
) -> dict[tuple[tuple[str, str], ...], list[DocumentAnnotation]]:
    """Group annotations across one or more dimensions.

    Multi-valued dimensions (for example signifiers or formation candidates)
    intentionally place a document in each relevant group.
    """
    dimensions = [item for item in group_by if item]
    if not dimensions:
        return {tuple(): list(annotations)}
    groups: dict[tuple[tuple[str, str], ...], list[DocumentAnnotation]] = {}
    for annotation in annotations:
        value_sets = [dimension_values(annotation, dim) for dim in dimensions]
        for values in product(*value_sets):
            key = tuple(zip(dimensions, values))
            groups.setdefault(key, []).append(annotation)
    return groups


def _count_refs(items: Iterable[Any], attr: str = "label") -> Counter[str]:
    counter: Counter[str] = Counter()
    for item in items:
        value = getattr(item, attr, "")
        if value:
            counter[str(value)] += 1
    return counter


def _aggregate(annotations: Sequence[DocumentAnnotation]) -> dict[str, Any]:
    source = Counter(a.source_platform or "unknown" for a in annotations)
    author = Counter(a.source_author or "unknown" for a in annotations)
    signifiers: Counter[str] = Counter()
    formations: Counter[str] = Counter()
    topics: Counter[str] = Counter()
    discourses: Counter[str] = Counter()
    articulations: Counter[str] = Counter()
    sentiment_affect: Counter[str] = Counter()
    populist = Counter()
    evidence_docs: list[str] = []

    for ann in annotations:
        signifiers.update(ref.label for ref in ann.signifiers if ref.label)
        formations.update(
            item.formation.label
            for item in ann.formation_candidates
            if item.formation.label
        )
        topics.update(ref.label for ref in ann.topics if ref.label)
        discourses.update(item.label for item in ann.discourses if item.label)
        for item in ann.articulations:
            targets = ", ".join(ref.label for ref in item.related_to if ref.label)
            label = f"{item.signifier.label} -> {targets}" if targets else item.signifier.label
            if label:
                articulations[label] += 1
        for item in ann.affects:
            if item.affect:
                sentiment_affect[f"affect:{item.affect}"] += 1
        for item in ann.sentiment_observations:
            if item.polarity:
                sentiment_affect[f"sentiment:{item.polarity}"] += 1
        populist[str(ann.populist)] += 1
        if ann.evidence_quotes or ann.hegemonic_evidence or any(
            getattr(item, "evidence", "")
            for item in ann.articulations + ann.signifier_roles + ann.formation_candidates
        ):
            evidence_docs.append(ann.document_id)

    return {
        "source_distribution": dict(source),
        "author_distribution": dict(author),
        "signifier_distribution": dict(signifiers),
        "formation_distribution": dict(formations),
        "topic_distribution": dict(topics),
        "frame_or_discourse_distribution": dict(discourses),
        "articulation_summary": dict(articulations),
        "populism_summary": {
            "populist": populist.get("True", 0),
            "non_populist": populist.get("False", 0),
            "unreviewed_or_abstained": populist.get("None", 0),
        },
        "sentiment_affect_summary": dict(sentiment_affect),
        "uncertainty_review": {
            "documents_requiring_review": sum(a.requires_human_review for a in annotations),
            "documents_with_uncertainties": sum(bool(a.uncertainties) for a in annotations),
            "review_status_distribution": dict(Counter(a.review_status for a in annotations)),
        },
        "evidence_document_ids": evidence_docs,
    }


def _changed_keys(current: Mapping[str, int], previous: Mapping[str, int]) -> tuple[list[str], list[str]]:
    emerging = sorted(key for key, value in current.items() if value > 0 and previous.get(key, 0) == 0)
    declining = sorted(key for key, value in previous.items() if value > 0 and current.get(key, 0) == 0)
    return emerging, declining


def _changes(current: Mapping[str, Any], previous: Mapping[str, Any] | None) -> DetectedChanges:
    if not previous:
        return DetectedChanges()
    emerging_s, declining_s = _changed_keys(
        current["signifier_distribution"], previous["signifier_distribution"]
    )
    emerging_f, declining_f = _changed_keys(
        current["formation_distribution"], previous["formation_distribution"]
    )
    emerging_a, declining_a = _changed_keys(
        current["articulation_summary"], previous["articulation_summary"]
    )
    emerging_affect, declining_affect = _changed_keys(
        current["sentiment_affect_summary"], previous["sentiment_affect_summary"]
    )
    emerging_source, declining_source = _changed_keys(
        current["source_distribution"], previous["source_distribution"]
    )
    cur_pop = current["populism_summary"]
    prev_pop = previous["populism_summary"]
    populism_shift = (
        f"populist documents {prev_pop.get('populist', 0)} -> {cur_pop.get('populist', 0)}; "
        f"non-populist {prev_pop.get('non_populist', 0)} -> {cur_pop.get('non_populist', 0)}"
    )
    total_named_change = sum(map(len, (
        emerging_s, declining_s, emerging_f, declining_f,
        emerging_a, declining_a, emerging_affect, declining_affect,
        emerging_source, declining_source,
    )))
    return DetectedChanges(
        emerging_signifiers=emerging_s,
        declining_signifiers=declining_s,
        emerging_formations=emerging_f,
        declining_formations=declining_f,
        changed_articulations=[*(f"emerging: {x}" for x in emerging_a), *(f"declining: {x}" for x in declining_a)],
        affect_or_sentiment_shift=[*(f"emerging: {x}" for x in emerging_affect), *(f"declining: {x}" for x in declining_affect)],
        populism_shift=populism_shift,
        source_or_author_shift=[*(f"emerging source: {x}" for x in emerging_source), *(f"declining source: {x}" for x in declining_source)],
        continuity_or_drift="meaningful drift" if total_named_change else "continuity",
    )


def _window(annotations: Sequence[DocumentAnnotation]) -> dict[str, str]:
    stamps = sorted(stamp for stamp in (_timestamp(a) for a in annotations) if stamp)
    return {"start": stamps[0] if stamps else "", "end": stamps[-1] if stamps else ""}


def _default_human_summary(grouping: Mapping[str, str], aggregated: Mapping[str, Any], changes: DetectedChanges) -> str:
    group_text = ", ".join(f"{key}={value}" for key, value in grouping.items()) or "all documents"
    top_signifiers = sorted(
        aggregated["signifier_distribution"].items(), key=lambda item: (-item[1], item[0])
    )[:8]
    top_formations = sorted(
        aggregated["formation_distribution"].items(), key=lambda item: (-item[1], item[0])
    )[:5]
    return (
        f"Provisional corpus synthesis for {group_text}. "
        f"Top signifiers: {', '.join(f'{k} ({v})' for k, v in top_signifiers) or 'none'}. "
        f"Formation candidates: {', '.join(f'{k} ({v})' for k, v in top_formations) or 'none'}. "
        f"Temporal assessment: {changes.continuity_or_drift}. "
        "Counts are descriptive evidence, not proof of hegemony or theoretical importance."
    )


def synthesize_group(
    annotations: Sequence[DocumentAnnotation],
    *,
    grouping: Mapping[str, str] | None = None,
    previous_annotations: Sequence[DocumentAnnotation] | None = None,
    config: SynthesisConfig | None = None,
    narrative_synthesizer: NarrativeSynthesizer | None = None,
) -> CorpusSynthesis:
    """Create one stable synthesis object for a document group."""
    config = config or SynthesisConfig()
    current = _aggregate(annotations)
    previous = _aggregate(previous_annotations or []) if previous_annotations else None
    detected = _changes(current, previous)
    grouping = dict(grouping or {})
    base = {
        "grouping": grouping,
        "time_window": _window(annotations),
        "document_ids": [a.document_id for a in annotations],
        "document_count": len(annotations),
        **current,
        "previous_window_reference": (
            {
                "time_window": _window(previous_annotations or []),
                "document_ids": [a.document_id for a in (previous_annotations or [])],
                "document_count": len(previous_annotations or []),
            }
            if previous_annotations
            else None
        ),
        "detected_changes": detected,
    }
    human = (
        narrative_synthesizer(base)
        if narrative_synthesizer is not None
        else _default_human_summary(grouping, current, detected)
    )
    return CorpusSynthesis(
        synthesis_id=f"syn-{uuid4().hex}",
        human_readable_synthesis=human,
        provenance={
            "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "model": config.model,
            "prompt_version": config.prompt_version,
            "config_version": config.config_version,
            "group_by": config.group_by,
            "minimum_documents": config.minimum_documents,
            "human_in_the_loop": True,
            "frequency_is_not_hegemony": True,
        },
        **base,
    )


def synthesize_annotations(
    annotations: Sequence[DocumentAnnotation],
    *,
    config: SynthesisConfig | None = None,
    previous_annotations: Sequence[DocumentAnnotation] | None = None,
    narrative_synthesizer: NarrativeSynthesizer | None = None,
) -> list[CorpusSynthesis]:
    """Batch synthesis entry point with configurable composable groupings."""
    config = config or SynthesisConfig()
    if not config.enabled:
        return []
    previous_groups = group_annotations(previous_annotations or [], config.group_by)
    output: list[CorpusSynthesis] = []
    for key, group in group_annotations(annotations, config.group_by).items():
        relevant = [a for a in group if a.relevance != "irrelevant"]
        if len(relevant) < config.minimum_documents:
            continue
        grouping = dict(key)
        previous = [
            a for a in previous_groups.get(key, []) if a.relevance != "irrelevant"
        ]
        output.append(
            synthesize_group(
                relevant,
                grouping=grouping,
                previous_annotations=previous if config.compare_previous else None,
                config=config,
                narrative_synthesizer=narrative_synthesizer,
            )
        )
    return output
