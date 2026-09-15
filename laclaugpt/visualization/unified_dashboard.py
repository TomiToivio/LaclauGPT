"""Unified researcher dashboard front door for issue #136.

The existing live dashboard remains the visualization engine. This module adds
researcher-first layers without introducing another schema or project-specific
fork:

- all current live/AI26 overview, ideology, signifier, network, frontier, actor,
  timeline and review views;
- the canonical EP-style document inspection/review view already reused by the
  live dashboard;
- deterministic complete-row rendering in every document view;
- configurable corpus synthesis over the same canonical annotations;
- optional previous-window JSONL for explicit change/drift comparison;
- machine-readable synthesis download.
"""
from __future__ import annotations

import json

from laclaugpt.researcher_reporting import render_human_readable_analysis
from laclaugpt.synthesis import SynthesisConfig, synthesize_annotations
from laclaugpt.visualization import live_dashboard
from laclaugpt.visualization.data import load_annotations
from laclaugpt.visualization.runtime import require_dashboard_runtime


_ORIGINAL_DOCUMENT_VIEW = live_dashboard._document_view


def _unified_document_view(st, annotation, review_store, **kwargs) -> None:
    """Delegate to canonical inspection then add complete deterministic rendering."""
    _ORIGINAL_DOCUMENT_VIEW(st, annotation, review_store, **kwargs)
    if kwargs.get("blind_initial"):
        return
    with st.expander("Complete human-readable analysis", expanded=False):
        st.caption(
            "Deterministic rendering of every populated research-facing field. "
            "This view adds no model interpretation and does not modify canonical data."
        )
        st.markdown(render_human_readable_analysis(annotation))


def _render_synthesis_panel(st, args) -> None:
    if not args.data:
        st.caption(
            "Corpus synthesis is available when the dashboard is launched with a "
            "canonical JSONL/NDJSON path."
        )
        return

    st.header("Corpus-level discourse synthesis")
    st.caption(
        "Corpus claims remain provisional and human-reviewable. Frequency is not "
        "hegemony, and irrelevant-marked documents are excluded from synthesis."
    )
    dimensions = st.multiselect(
        "Synthesis grouping",
        ["date", "signifier", "author", "source_platform", "formation"],
        default=["date"],
        key="unified-synthesis-grouping",
    )
    minimum_documents = int(
        st.number_input(
            "Minimum documents per synthesis group",
            min_value=1,
            value=5,
            step=1,
            key="unified-synthesis-minimum",
        )
    )
    previous_path = st.text_input(
        "Optional previous/baseline canonical JSONL",
        "",
        key="unified-synthesis-previous",
    ).strip()

    try:
        annotations = load_annotations(
            args.data,
            project=args.project.strip(),
            arena=args.arena.strip(),
        )
        previous = (
            load_annotations(
                previous_path,
                project=args.project.strip(),
                arena=args.arena.strip(),
            )
            if previous_path
            else []
        )
        syntheses = synthesize_annotations(
            annotations,
            previous_annotations=previous,
            config=SynthesisConfig(
                group_by=dimensions,
                minimum_documents=minimum_documents,
                compare_previous=bool(previous),
            ),
        )
    except (OSError, ValueError) as exc:
        st.error(f"Could not create corpus synthesis: {exc}")
        return

    if not syntheses:
        st.info("No synthesis group meets the current minimum-document threshold.")
        return

    rows = [item.model_dump(mode="json") for item in syntheses]
    labels = [
        ", ".join(f"{key}={value}" for key, value in item.grouping.items())
        or "all documents"
        for item in syntheses
    ]
    selected_label = st.selectbox(
        "Synthesis group",
        labels,
        key="unified-synthesis-selected",
    )
    selected = syntheses[labels.index(selected_label)]

    cols = st.columns(4)
    cols[0].metric("Documents", selected.document_count)
    cols[1].metric("Signifiers", len(selected.signifier_distribution))
    cols[2].metric("Formations", len(selected.formation_distribution))
    cols[3].metric("Evidence-bearing docs", len(selected.evidence_document_ids))

    st.markdown(selected.human_readable_synthesis)
    if selected.previous_window_reference:
        st.subheader("Detected change / drift")
        st.json(selected.detected_changes.model_dump(mode="json"))

    with st.expander("Machine-readable synthesis object"):
        st.json(selected.model_dump(mode="json"))

    st.download_button(
        "Download all synthesis groups as JSON",
        json.dumps(rows, ensure_ascii=False, indent=2).encode("utf-8"),
        file_name="laclaugpt-corpus-synthesis.json",
        mime="application/json",
        key="unified-synthesis-download",
    )


def main() -> None:
    # Parse once, then hand the exact namespace to the live dashboard. This keeps
    # its existing filters/review/live-refresh behavior and makes this module a
    # thin consolidation layer rather than a parallel application.
    args = live_dashboard._arguments()
    original_arguments = live_dashboard._arguments
    original_document_view = live_dashboard._document_view
    live_dashboard._arguments = lambda: args
    live_dashboard._document_view = _unified_document_view
    try:
        live_dashboard.main()
    finally:
        live_dashboard._arguments = original_arguments
        live_dashboard._document_view = original_document_view

    st, _px, _go, _nx = require_dashboard_runtime()
    _render_synthesis_panel(st, args)


if __name__ == "__main__":
    main()
