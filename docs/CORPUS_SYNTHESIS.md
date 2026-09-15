# Corpus synthesis and researcher-visible outputs

Issue #136 adds a second analytical scale above per-document coding while keeping the canonical `DocumentAnnotation` as the evidence-bearing unit.

```text
source evidence
    -> DocumentAnnotation
    -> deterministic researcher row/rendering
    -> configurable grouped corpus synthesis
    -> unified researcher dashboard
```

## Corpus synthesis

`laclaugpt.synthesis` provides a project-neutral `SynthesisConfig` and stable `CorpusSynthesis` object.

Built-in grouping dimensions are:

- `date`
- `signifier`
- `author`
- `source_platform` (alias `source` / `platform`)
- `formation`

Dimensions compose, for example `date + formation`, `date + signifier`, `source_platform + formation`, or `author + signifier`. Additional canonical annotation fields can be named directly, and source metadata can be addressed as `metadata.<key>`.

Example:

```python
from laclaugpt.synthesis import SynthesisConfig, synthesize_annotations

config = SynthesisConfig(
    group_by=["date", "formation"],
    minimum_documents=5,
    compare_previous=True,
)

records = synthesize_annotations(
    current_annotations,
    previous_annotations=previous_annotations,
    config=config,
)
```

Each synthesis records its exact document IDs, grouping keys, time window, source/author/signifier/formation/topic/discourse distributions, articulation counts, populism and sentiment/affect summaries, review/uncertainty state, evidence-bearing document references, provenance, previous-window reference and explicit change fields.

Current change fields include emerging/declining signifiers and formations, changed articulation patterns, affect/sentiment shifts, populism movement, source emphasis movement and a continuity/drift classification. They are descriptive candidate signals for human review, not automatic theoretical claims.

A caller may provide a `narrative_synthesizer` callback when a configured local LLM should create the higher-level prose interpretation. The stable machine object is built first and remains available regardless of whether an LLM narrative is requested.

Documents explicitly marked `relevance="irrelevant"` are retained in canonical storage but excluded from corpus synthesis.

## Daily, rolling, and previous-period comparison

`laclaugpt.synthesis_windows` provides scheduler-neutral window orchestration. `daily_windows()` creates contiguous daily periods and `synthesize_rolling()` supports rolling windows such as current 7 days versus previous 7 days.

For composite groupings that include `date`, previous-period matching intentionally ignores the literal date when selecting the baseline while retaining all other grouping dimensions. Thus `date + formation=accel` on 15 September is compared with the same formation in the previous period, not with an impossible previous record whose date is also 15 September.

`CadenceConfig` includes daily operation, rolling-window length, previous-period count, historical-baseline length and optional `every_n_documents` thresholds. Scheduling remains outside the analytical core so cron, Slurm, an agent or an explicit researcher batch can invoke the same deterministic functions.

## YAML configuration without code edits

`laclaugpt.synthesis_io.load_synthesis_config()` accepts an issue-136-style YAML configuration, for example:

```yaml
synthesis:
  enabled: true
  group_by: [date, formation]
  cadence:
    daily: true
    rolling_window_days: 7
    every_n_documents: 100
  compare_previous:
    enabled: true
    periods: 1
    historical_baseline_days: 30
  minimum_documents: 5
  include_intermediate_results: true
  include_source_metadata: true
```

The loader returns both the synthesis configuration and cadence configuration. This keeps grouping/window changes out of Python code.

## Synthesis exports

`laclaugpt.synthesis_io` exports stable synthesis objects as JSON, deterministic CSV and researcher-readable Markdown. The unified dashboard additionally exposes machine-readable synthesis JSON and the complete document rows belonging to the selected synthesis group.

## Complete researcher-visible row rendering and exports

`laclaugpt.researcher_reporting.render_human_readable_analysis()` deterministically renders every populated research-facing field in a `DocumentAnnotation`. It makes no model call and performs no new interpretation.

`researcher_row()` preserves the complete machine-readable annotation and adds:

```text
human_readable_analysis
```

Because the renderer is schema-driven rather than maintained as a hand-selected field list, newly added populated annotation fields become visible automatically unless they are explicitly classified as non-research-facing. Regression tests enforce this behavior.

This means transcripts/source text, intermediate frame/discourse/populism outputs, stage model information, warnings, source-native metadata and other preserved intermediates remain visible whenever the upstream adapter stores them under canonical fields such as `transformations` or `collection_provenance`.

`laclaugpt.researcher_exports` provides complete CSV, JSONL and Parquet exports. CSV serializes nested canonical structures deterministically instead of dropping them and includes a dedicated serialized `source_native_metadata` field plus `human_readable_analysis`. `export_filtered_rows()` exports an exact researcher-selected document set.

## Unified dashboard

`laclaugpt-dashboard` launches `laclaugpt.visualization.unified_dashboard` as the supported default front door.

The unified view reuses the existing live dashboard and its canonical document inspection/review implementation, then adds:

- a complete human-readable analysis expander for each document;
- configurable corpus synthesis grouping;
- optional previous/baseline JSONL comparison with non-temporal group matching;
- explicit machine-readable change/drift display;
- downloadable corpus-synthesis JSON;
- downloadable complete researcher rows for the selected synthesis group.

The older dashboard modules remain implementation/compatibility views. New project code should target the canonical interchange + synthesis objects, not a dashboard-specific schema.

## Model routing

Corpus synthesis may use a caller-provided narrative model, but the default local routing has **not** been silently changed. Issue #136 requires a reproducible benchmark before changing `STAGE_ROUTING`.

See [`MODEL_ROUTING_BENCHMARK.md`](MODEL_ROUTING_BENCHMARK.md) for the candidate Gemma 4 / EmbeddingGemma / Qwen3 methodology, executable local-only benchmark harness and decision rule.

## Safeguards

- Frequency, graph centrality and model confidence do not establish hegemony.
- Corpus synthesis remains provisional and human-reviewable.
- Exact evidence-bearing document IDs are retained.
- Machine-readable structure is never replaced by prose.
- No private operational targets, hostnames, credentials or private datasets belong in public synthesis configuration.
