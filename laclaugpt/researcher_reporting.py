"""Project-neutral helpers for researcher-readable analysis reports.

The canonical interchange keeps machine-readable structured summaries intact.
These helpers provide a separate Markdown rendering layer so human reviewers do
not need to inspect raw JSON to understand document-level outputs.
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
        f"- documents in synthesis: {synthesis.get('documents', len(annotations))}",
        f"- signifier families: {len(synthesis.get('signifier_frequency', {}))}",
        f"- floating candidates: {len(synthesis.get('floating_candidates', []))}",
        f"- empty candidates: {len(synthesis.get('empty_candidates', []))}",
        f"- nodal candidates: {len(synthesis.get('nodal_candidates', []))}",
        "",
        "> Frequency is not hegemony; candidate rows need human adjudication.",
        "",
    ]
    for ann in annotations:
        lines.extend([
            f"## {ann.document_id}",
            "",
            f"- relevance: **{ann.relevance or 'not judged'}**" + (f" — {ann.relevance_reason}" if ann.relevance_reason else ""),
            f"- review: {ann.review_status}" + (" (needs human review)" if ann.requires_human_review else ""),
            f"- populist: {ann.populist}",
            f"- language: {ann.language or '?'} | platform: {ann.source_platform or '?'}",
            "",
            "### Summary",
            "",
            humanize_summary(ann.summary) or "(no summary)",
            "",
        ])
        if ann.populism_analysis:
            lines.extend(["### Populism analysis", "", ann.populism_analysis, ""])
        if ann.evidence_quotes:
            lines.extend(["### Evidence quotes", ""])
            lines.extend(f'- "{quote}"' for quote in ann.evidence_quotes[:5])
            lines.append("")
        if ann.uncertainties:
            lines.extend(["### Uncertainties", ""])
            lines.extend(f"- {item}" for item in ann.uncertainties[:5])
            lines.append("")
    return "\n".join(lines)


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
