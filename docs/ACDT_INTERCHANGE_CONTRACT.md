# AC/DT cross-repository interchange contract

Version: `acdt-result/1.0`

This document specifies the compatibility boundary used by Collection, Analysis and Visualization for AC/DT-era and current LaclauGPT studies. It is additive to the canonical record contract. Existing canonical records remain the source/evidence container; this contract standardizes method-result semantics.

## 1. Identity

Every source record must retain a stable `source_url` or URI-like source identity. Source-native IDs such as post/document/actor/conversation identifiers are retained as native IDs or source metadata. An analysis result references its inputs through `input_record_ids`; it must not replace source identity with an analysis-generated database primary key.

## 2. Required method-result fields

| Field | Meaning |
| --- | --- |
| `schema_version` | `acdt-result/1.0` |
| `method_id` | Stable ID from `schemas/acdt_method_registry.v1.yaml` |
| `method_version` | Version of the research-method contract |
| `interpretation_mode` | `exploratory_instrumentalist`, `measurement`, or `theoretical_interpretive` |
| `study_id` | Study/project identifier, or `null` if genuinely unavailable |
| `corpus_id` | Corpus/subcorpus identifier, or `null` |
| `input_record_ids` | Stable source-record identities contributing to the result |
| `parameters` | Method parameters sufficient to understand/reproduce the run where possible |
| `provenance` | Producer, software version, git commit/run/worker identifiers and time where available |
| `validation` | Validation status, human-review status and validation method/notes |
| `output` | Method-specific payload |

Optional but strongly preferred fields include preprocessing details, model/lexicon identity, language/translation/adaptation metadata, output artefact references, and explicit evidence references.

## 3. Missing legacy metadata

Backwards compatibility must never fabricate metadata. When an older result lacks a field:

- use JSON `null` when the field exists conceptually but the value is unknown;
- use `not_available` only in display/adaptation layers where a visible sentinel is needed;
- keep the original legacy object under a namespaced `legacy` field when possible;
- do not infer model versions, lexicons, languages, thresholds, actor identities or ideological labels from surrounding data.

## 4. Interpretation-mode semantics

### `exploratory_instrumentalist`

The output is a pattern/navigation/sampling device. Examples: topic models used as a magnifying glass, word frequencies, hashtag co-occurrence, temporal peaks, close-reading samples. These results cannot on their own establish frame, discourse, articulation, ideology, antagonism or hegemony.

### `measurement`

The output is treated as a measurement. Examples: SNA metrics, sentiment/emotion, Wordscores/Wordfish, DNA projections. The result must expose method-specific diagnostics/validation status. A measurement still does not automatically become a Laclaudian theoretical code.

### `theoretical_interpretive`

The output contains theory-bearing interpretations. It must be linked to primary evidence, preserve uncertainty/counterevidence where applicable, and expose human-review status. Corpus-level claims such as hegemony, ideological formation or stable floating/empty signification require corpus-level evidence and human review.

## 5. Language and translation

A multilingual/translated analysis should preserve, where available:

- source language;
- analysis language;
- whether translated text was used;
- translation method/model/tool;
- lexicon or model language;
- language adaptation method;
- validation of adapted lexicons/models.

Translation is a transformation in provenance, not a silent replacement of the source text.

## 6. Evidence drill-down

Aggregate outputs should preserve enough references for the dashboard to trace a claim or pattern back toward primary records. Recommended `evidence_refs` fields are:

```json
{
  "record_id": "stable source id",
  "source_url": "optional source URL",
  "artifact_id": "optional aggregate/artifact id",
  "selector": {
    "quote": "optional short evidence excerpt",
    "start_offset": 0,
    "end_offset": 20,
    "timestamp_seconds": 12.5,
    "frame_ref": "frame-12"
  }
}
```

Privacy, platform terms and licensing may prevent distribution of source content; in that case preserve identifiers/provenance appropriate to the study rather than copying restricted material into public fixtures.

## 7. Semantic non-equivalences

No adapter or visualization may silently promote:

- frequency to hegemony;
- co-occurrence/similarity to articulation;
- network community/cluster to ideological formation;
- negative sentiment to antagonistic frontier;
- sentiment/emotion/intensity to affective investment;
- topic membership to frame/discourse/ideology;
- visual/embedding proximity to political equivalence;
- a latent Wordscores/Wordfish coordinate to an ideological label without declared substantive validation.

## 8. Round-trip rule

Compatibility tests should exercise:

`legacy import -> canonical normalization -> analysis/load -> acdt-result envelope -> export -> re-import -> visualization product`

The round trip is successful when source identity, legacy-specific fields needed for reproducibility, method identity/version, interpretation mode, validation/review state and evidence/provenance references survive without semantic upgrading or invented values.