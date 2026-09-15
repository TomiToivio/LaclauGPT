"""Project-neutral helpers for researcher-readable analysis reports.

The canonical interchange keeps machine-readable structured summaries intact.
These helpers provide the deterministic rendering layer used by human-facing
exports, dashboards and reports so reviewers never have to reverse-engineer
raw JSON.
"""
from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from laclaugpt_interchange import DocumentAnnotation


_LABELS = {
    "narrative_construction": "Narrative",
    "political_classification": "Political classification",
    "political": "Political",
    "political_subcategory": "Category",
    "key_political_topics": "Key political topics",
    "political_entities": "Political entities",
    "sentiments": "Sentiments",
    "people_power_narrative": "People–power narrative",
    "social_contract": "Social contract",
    "grievances": "Grievances",
    "difficult_language": "Difficult language",
}

# Fields that are intentionally implementation-only and therefore excluded
# from the complete researcher rendering. Keep this list tiny and explicit.
_NON_RESEARCH_FACING_FIELDS: frozenset[str] = frozenset()


def humanize_summary(summary: str) -> str:
    """Render a structured JSON summary as labelled Markdown prose.

    Non-JSON summaries pass through unchanged. The machine-readable summary is
    never mutated; this is strictly a presentation helper for human review.
    """
    text = (summary or "").strip()
    if not (text.startswith("{") and text.endswith("}")):
        return text
    try:
        payload = json.loads(text)
    except (TypeError, ValueError):
        return text
    if not isinstance(payload, dict):
        return text

    lines: list[str] = []
    for key, value in payload.items():
        label = _LABELS.get(key, key.replace("_", " ").capitalize())
        if isinstance(value, Mapping):
            parts = [
                f"{sub_key}: {sub_value}"
                for sub_key, sub_value in value.items()
                if sub_value not in ("", None, [], "absent")
            ]
            if parts:
                lines.append(f"- **{label}**: " + "; ".join(parts))
        elif isinstance(value, list):
            items: list[str] = []
            for item in value:
                if isinstance(item, Mapping):
                    parts = [
                        f"{sub_key}: {sub_value}"
                        for sub_key, sub_value in item.items()
                        if sub_value not in ("", None, [], "absent")
                    ]
                    if parts:
                        items.append("(" + "; ".join(parts) + ")")
                elif item not in ("", None):
                    items.append(str(item))
            if items:
                lines.append(f"- **{label}**: " + "; ".join(items))
        elif value not in ("", None):
            lines.append(f"- **{label}**: {value}")
    return "\n".join(lines) if lines else text


def _is_populated(value: Any) -> bool:
    if value is None:
        return False
    if value == "":
        return False
    if isinstance(value, (list, tuple, set, dict)) and not value:
        return False
    return True


def _display_label(key: str) -> str:
    return _LABELS.get(key, key.replace("_", " ").capitalize())


def _render_value(value: Any, *, level: int = 0) -> list[str]:
    """Render nested JSON-compatible values deterministically as Markdown."""
    indent = "  " * level
    if isinstance(value, Mapping):
        lines: list[str] = []
        for key in sorted(value):
            item = value[key]
            if not _is_populated(item):
                continue
            label = _display_label(str(key))
            if isinstance(item, (Mapping, list, tuple)):
                lines.append(f"{indent}- **{label}**:")
                lines.extend(_render_value(item, level=level + 1))
            else:
                lines.append(f"{indent}- **{label}**: {item}")
        return lines
    if isinstance(value, (list, tuple)):
        lines = []
        for item in value:
            if not _is_populated(item):
                continue
            if isinstance(item, Mapping):
                lines.append(f"{indent}-")
                lines.extend(_render_value(item, level=level + 1))
            else:
                lines.append(f"{indent}- {item}")
        return lines
    return [f"{indent}{value}"]


def research_facing_payload(annotation: DocumentAnnotation) -> dict[str, Any]:
    """Return all populated researcher-facing fields from one annotation.

    The function is intentionally schema-driven rather than maintained as a
    hand-picked allow-list. New interchange fields therefore become visible to
    researchers automatically unless they are explicitly added to
    ``_NON_RESEARCH_FACING_FIELDS``.
    """
    payload = annotation.model_dump(mode="json")
    return {
        key: value
        for key, value in payload.items()
        if key not in _NON_RESEARCH_FACING_FIELDS and _is_populated(value)
    }


def render_human_readable_analysis(annotation: DocumentAnnotation) -> str:
    """Render every populated research-facing annotation field.

    This renderer makes no model call and performs no interpretation. It is a
    stable, reproducible inspection view suitable for CSV columns, dashboards,
    Markdown reports and review interfaces.
    """
    payload = research_facing_payload(annotation)
    preferred = [
        "document_id",
        "source_platform",
        "source_country",
        "language",
        "source_author",
        "source_timestamp",
        "source_url",
        "summary",
        "entities",
        "topics",
        "signifiers",
        "signifier_roles",
        "articulations",
        "discourses",
        "formation_candidates",
        "populism_analysis",
        "populism_elements",
        "us",
        "frontier",
        "affects",
        "sentiment_observations",
        "imaginaries",
        "evidence_quotes",
        "hegemonic_evidence",
        "counter_evidence",
        "uncertainties",
        "review_status",
        "requires_human_review",
        "relevance",
        "relevance_reason",
        "discourse_applicable",
        "discourse_applicability_reason",
        "model",
        "model_digest",
        "prompt_versions",
        "run_id",
        "analysis_stage",
        "transformations",
        "collection_provenance",
        "source_modalities",
        "parent_id",
        "sequence_index",
        "schema_version",
        "created_at",
    ]
    ordered = [key for key in preferred if key in payload]
    ordered.extend(sorted(key for key in payload if key not in ordered))

    lines = [f"# Document {annotation.document_id}", ""]
    for key in ordered:
        value = payload[key]
        label = _display_label(key)
        lines.append(f"## {label}")
        lines.append("")
        if key == "summary" and isinstance(value, str):
            lines.append(humanize_summary(value) or "(empty)")
        elif isinstance(value, (Mapping, list, tuple)):
            rendered = _render_value(value)
            lines.extend(rendered or ["(empty)"])
        else:
            lines.append(str(value))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def researcher_row(annotation: DocumentAnnotation) -> dict[str, Any]:
    """Return a lossless machine row plus deterministic human-readable view."""
    row = annotation.model_dump(mode="json")
    row["human_readable_analysis"] = render_human_readable_analysis(annotation)
    return row


def render_researcher_report(
    annotations: Sequence[DocumentAnnotation],
    *,
    synthesis: Mapping[str, Any] | None = None,
    project_label: str = "LaclauGPT",
) -> str:
    """Return a project-neutral Markdown digest for human researchers."""
    synthesis = synthesis or {}
    relevant = [a for a in annotations if a.relevance != "irrelevant"]
    irrelevant = [a for a in annotations if a.relevance == "irrelevant"]
    lines = [
        f"# {project_label} analysis report",
        "",
        f"Documents: {len(annotations)} ({len(relevant)} retained, {len(irrelevant)} marked irrelevant)",
        f"Review queue: {sum(1 for a in annotations if a.requires_human_review)} provisional annotations need human review",
        "",
        "## Corpus synthesis (descriptive only)",
        "",
        f"- documents in synthesis: {synthesis.get('documents', synthesis.get('document_count', len(annotations)))}",
        f"- signifier families: {len(synthesis.get('signifier_frequency', synthesis.get('signifier_distribution', {})))}",
        f"- floating candidates: {len(synthesis.get('floating_candidates', []))}",
        f"- empty candidates: {len(synthesis.get('empty_candidates', []))}",
        f"- nodal candidates: {len(synthesis.get('nodal_candidates', []))}",
        "",
        "> Frequency is not hegemony; candidate rows need human adjudication.",
        "",
    ]
    if synthesis.get("human_readable_synthesis"):
        lines.extend([
            "### Corpus interpretation",
            "",
            str(synthesis["human_readable_synthesis"]),
            "",
        ])
    for annotation in annotations:
        lines.append(render_human_readable_analysis(annotation).rstrip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_researcher_report(
    annotations: Sequence[DocumentAnnotation],
    path: str | Path,
    *,
    synthesis: Mapping[str, Any] | None = None,
    project_label: str = "LaclauGPT",
) -> str:
    """Write :func:`render_researcher_report` output to ``path``."""
    destination = Path(path)
    destination.write_text(
        render_researcher_report(
            annotations,
            synthesis=synthesis,
            project_label=project_label,
        ),
        encoding="utf-8",
    )
    return str(destination)
