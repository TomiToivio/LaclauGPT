"""Time-window orchestration for corpus synthesis.

The lower-level :mod:`laclaugpt.synthesis` module groups a supplied current set.
This module defines rolling/custom windows and, importantly, matches baseline
records on non-temporal dimensions so ``date + formation`` can compare today's
formation with the same formation yesterday rather than looking for the same
literal date in both periods.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Iterable, Sequence

from pydantic import BaseModel, Field

from laclaugpt.synthesis import (
    CorpusSynthesis,
    NarrativeSynthesizer,
    SynthesisConfig,
    dimension_values,
    group_annotations,
    synthesize_group,
)
from laclaugpt_interchange import DocumentAnnotation


class SynthesisWindow(BaseModel):
    start: datetime
    end: datetime
    label: str = ""


class CadenceConfig(BaseModel):
    """Scheduler-neutral cadence/window definition.

    A cron, batch runner or researcher can call the same deterministic functions.
    ``every_n_documents`` is exposed for count-triggered orchestration; callers
    decide when to invoke the batch based on their ingestion counter.
    """

    daily: bool = True
    rolling_window_days: int = Field(default=7, ge=1)
    previous_periods: int = Field(default=1, ge=0)
    historical_baseline_days: int | None = Field(default=30, ge=1)
    every_n_documents: int | None = Field(default=None, ge=1)


def _parse_timestamp(annotation: DocumentAnnotation) -> datetime | None:
    raw = (annotation.source_timestamp or annotation.created_at or "").strip()
    if not raw:
        return None
    normalized = raw.replace("Z", "+00:00")
    try:
        stamp = datetime.fromisoformat(normalized)
    except ValueError:
        try:
            stamp = datetime.fromisoformat(raw[:10])
        except ValueError:
            return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc)


def select_window(
    annotations: Iterable[DocumentAnnotation], window: SynthesisWindow
) -> list[DocumentAnnotation]:
    start = window.start.astimezone(timezone.utc)
    end = window.end.astimezone(timezone.utc)
    selected: list[DocumentAnnotation] = []
    for annotation in annotations:
        stamp = _parse_timestamp(annotation)
        if stamp is not None and start <= stamp < end:
            selected.append(annotation)
    return selected


def rolling_windows(
    *, end: datetime, window_days: int, periods: int
) -> list[SynthesisWindow]:
    """Return current window first, then contiguous previous windows."""
    end = end.astimezone(timezone.utc)
    width = timedelta(days=window_days)
    return [
        SynthesisWindow(
            start=end - width * (index + 1),
            end=end - width * index,
            label="current" if index == 0 else f"previous-{index}",
        )
        for index in range(periods + 1)
    ]


def daily_windows(*, day: datetime, periods: int = 1) -> list[SynthesisWindow]:
    day = day.astimezone(timezone.utc)
    end = day.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return rolling_windows(end=end, window_days=1, periods=periods)


def _matches_non_temporal_group(
    annotation: DocumentAnnotation,
    grouping: dict[str, str],
) -> bool:
    for dimension, expected in grouping.items():
        if dimension.casefold() in {"date", "day"}:
            continue
        if expected not in dimension_values(annotation, dimension):
            return False
    return True


def synthesize_window_comparison(
    current_annotations: Sequence[DocumentAnnotation],
    previous_annotations: Sequence[DocumentAnnotation],
    *,
    config: SynthesisConfig | None = None,
    narrative_synthesizer: NarrativeSynthesizer | None = None,
) -> list[CorpusSynthesis]:
    """Synthesize current groups against matching prior non-date group state."""
    config = config or SynthesisConfig()
    output: list[CorpusSynthesis] = []
    for key, group in group_annotations(current_annotations, config.group_by).items():
        retained = [item for item in group if item.relevance != "irrelevant"]
        if len(retained) < config.minimum_documents:
            continue
        grouping = dict(key)
        baseline = [
            item
            for item in previous_annotations
            if item.relevance != "irrelevant"
            and _matches_non_temporal_group(item, grouping)
        ]
        output.append(
            synthesize_group(
                retained,
                grouping=grouping,
                previous_annotations=baseline if config.compare_previous else None,
                config=config,
                narrative_synthesizer=narrative_synthesizer,
            )
        )
    return output


def synthesize_rolling(
    annotations: Sequence[DocumentAnnotation],
    *,
    end: datetime,
    synthesis_config: SynthesisConfig | None = None,
    cadence: CadenceConfig | None = None,
    narrative_synthesizer: NarrativeSynthesizer | None = None,
) -> list[CorpusSynthesis]:
    """Explicit batch invocation for a rolling current vs previous window."""
    synthesis_config = synthesis_config or SynthesisConfig()
    cadence = cadence or CadenceConfig()
    windows = rolling_windows(
        end=end,
        window_days=cadence.rolling_window_days,
        periods=max(1, cadence.previous_periods),
    )
    current = select_window(annotations, windows[0])
    previous: list[DocumentAnnotation] = []
    for window in windows[1:]:
        previous.extend(select_window(annotations, window))
    return synthesize_window_comparison(
        current,
        previous,
        config=synthesis_config,
        narrative_synthesizer=narrative_synthesizer,
    )
