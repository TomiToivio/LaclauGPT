# Canonical LaclauGPT Data Contract

**Version:** 1.1.0-draft  
**Status:** Project-wide normative specification  
**Owner:** `TomiToivio/LaclauGPT` meta-repository

This document defines the logical record contract shared by LaclauGPT Data Collection, Data Analysis and Data Visualization. Storage engines and tabular formats are adapters around this contract. They are not alternative schemas.

## 1. Core rule

> **One phenomenon, one record contract, many storage adapters.**

A logical record MUST preserve the same meaning when represented through Pydantic/Python, JSON/JSONL, Pandas/CSV, SQLite, MongoDB, Parquet, Redis-backed workflows or S3/Allas metadata references.

The implementation repositories are responsible for adapters and tests:

- Collection: https://github.com/TomiToivio/LaclauGPT-Data-Collection/issues/3
- Analysis: https://github.com/TomiToivio/LaclauGPT-Data-Analysis/issues/4
- Visualization: https://github.com/TomiToivio/LaclauGPT-Data-Visualization/issues/3

The top-level repository owns this specification, schema evolution rules and cross-module semantics. It MUST NOT become a fourth implementation package.

## 2. Identity

### 2.1 Canonical source identity

`source_url` is the preferred canonical identity when a stable source URL exists.

When there is no ordinary web URL, use a stable URI-like identifier with equivalent semantics, for example:

```text
at://did:plc:.../app.bsky.feed.post/...
youtube:video:dQw4w9WgXcQ
telegram:channel:message:12345
file+sha256:...
```

The field is still exposed as `source_url` in the canonical record because it is the human-visible source locator/identifier contract. Implementations MAY additionally expose `source_uri` as an alias, but MUST NOT create two competing identities.

### 2.2 Rules

- `source_url` MUST be stable and deterministic for the source object.
- It MUST survive Collection -> Analysis -> Visualization unchanged after canonicalization.
- Backends SHOULD enforce uniqueness on the canonicalized value when practical.
- Platform-native IDs, historical `document_id`, `video_id`, `new_id`, database primary keys and row numbers are aliases or implementation identifiers, not semantic replacements for `source_url`.
- Derived objects such as source units, observations, measurements, entity mentions, relations, interpretations, embeddings and review events MAY have their own stable IDs, but MUST retain a path back to `source_url`.
- If a deterministic fallback must be generated, the unhashed human-readable locator SHOULD still be retained when available.

### 2.3 Canonicalization

Canonicalization MUST be deterministic and separately testable. At minimum:

- lowercase URL scheme and host;
- remove fragments where they do not identify distinct source objects;
- remove known tracking parameters such as `utm_*` and `fbclid` when safe;
- normalize equivalent trailing-slash forms where safe;
- preserve source-native object IDs;
- never collapse URLs that identify materially different source objects.

Platform-specific canonicalizers belong in Collection, not in this meta-repository.

## 3. Canonical record shape

The canonical record is a structured object with a small required core and optional nested sections.

```text
CanonicalRecord
├── schema_version
├── source_url
├── source_native_ids
├── source
├── content
├── source_units
├── alignments
├── evidence
├── analysis
├── provenance
└── review
```

### 3.1 Required core

| Field | Type | Meaning |
| --- | --- | --- |
| `schema_version` | string | Contract version used to serialize the record. |
| `source_url` | string | Canonical source URL or URI-like identifier. |
| `source_native_ids` | object | Optional platform/legacy IDs such as tweet ID, video ID, old `document_id`. |
| `source` | object | Source/platform/collection metadata. |
| `content` | object | Source content and optional multimodal content references. |
| `provenance` | array | Collection, preprocessing and analysis provenance events. |

`source_units`, `alignments`, `evidence`, `analysis` and `review` MAY be empty when not applicable.

## 4. Source section

The source section generalizes useful ingestion concepts while removing scraper-specific naming.

Recommended fields:

```yaml
source:
  platform: ""
  source_type: ""
  author: ""
  author_fullname: ""
  created_at: null
  collected_at: null
  collector: ""
  collection_method: ""
  language: ""
  country: ""
  parent_source_url: null
  raw_metadata: {}
  raw_ref: null
```

## 5. Content section

The content section stores source-derived representations, not interpretive theory claims.

Recommended shape:

```yaml
content:
  text: ""
  title: null
  language: null
  translated_text: null
  transcripts: []
  ocr: []
  frames: []
  media_references: []
  file_references: []
```

Large binary media MUST remain outside the record. Store references, checksums and metadata only.

## 6. Addressable source units

A `source_unit` is an inspectable portion of a source below whole-record level. It provides the common addressing layer for text spans, transcript segments, audio/video ranges, OCR regions, image regions and structured webpage sections.

Recommended shape:

```yaml
source_units:
  - unit_id: unit_transcript_001
    source_url: https://example.org/item/1
    unit_type: transcript_span
    parent_unit_id: null
    text: "..."
    text_start: null
    text_end: null
    token_start: null
    token_end: null
    start_seconds: 12.2
    end_seconds: 18.9
    frame_timestamp_seconds: null
    bbox: null
    media_ref: s3://bucket/key
    anchor: null
    provenance_id: prov_123
```

Supported addressing fields are optional and modality-dependent. Implementations MUST NOT invent coordinates, offsets or timestamps that are not known.

`unit_type` SHOULD use a documented vocabulary such as:

```text
record_text
text_span
transcript_span
audio_range
video_range
frame
image_region
ocr_region
web_section
metadata_observation
```

Rules:

- every `source_unit` MUST retain `source_url`;
- `unit_id` MUST be stable within the serialized record and SHOULD remain stable across review/reprocessing where the addressed source region has not changed;
- child units MAY reference `parent_unit_id`;
- exact source anchors SHOULD be preferred over copied text when possible;
- Collection MAY create source units only from source structure or deterministic preprocessing, never interpretive claims.

## 7. Multimodal alignment

`alignments` explicitly connect source units that refer to the same source moment, passage or region across modalities.

Example:

```yaml
alignments:
  - alignment_id: align_001
    relation: same_moment
    unit_ids:
      - unit_transcript_001
      - unit_frame_003
      - unit_ocr_007
    confidence: 1.0
    method: deterministic_timestamp
    provenance_id: prov_140
```

Recommended alignment relations include:

```text
same_moment
overlaps
contains
same_region
same_passage
corresponds_to
```

Alignment is descriptive infrastructure. It MUST NOT imply that the aligned units support the same interpretation.

## 8. Evidence graph

The canonical evidence model is a storage-neutral graph/DAG. It consists of reusable analytical objects plus explicit typed links between them.

### 8.1 Analytical object

```yaml
analysis_objects:
  - object_id: obj_001
    object_type: observation
    epistemic_type: SOURCE_OBSERVATION
    label: "speaker mentions automation"
    value: null
    source_url: https://example.org/item/1
    source_unit_ids: [unit_transcript_001]
    provenance_id: prov_200
    review_status: PROVISIONAL
    supersedes: null
    metadata: {}
```

`analysis.analysis_objects` MAY contain generic qualitative objects and discourse-theoretical objects. Recommended `object_type` values include:

```text
observation
measurement
entity
actor
relation
event
narrative_episode
proposition
candidate_interpretation
confirmed_interpretation
research_claim
formation
signifier
nodal_point
frontier
imaginary
frame
topic
```

Object type describes what the object is. `epistemic_type` describes its epistemic role. They MUST NOT be conflated.

### 8.2 Evidence links

```yaml
evidence:
  - evidence_id: edge_001
    relation: derived_from
    from_id: obj_measurement_001
    to_id: unit_transcript_001
    source_url: https://example.org/item/1
    provenance_id: prov_201
    review_status: PROVISIONAL
    metadata: {}
```

Recommended relations include:

```text
derived_from
supports
contradicts
refines
same_as
part_of
precedes
follows
mentions
involves_actor
evidence_for
```

Rules:

- evidence links MUST reference stable object/unit IDs;
- interpretive objects SHOULD be transitively traceable to one or more source units when source evidence exists;
- cross-source similarity MUST NOT be represented as `same_as` automatically;
- inference/model edges MUST retain provenance and review status;
- graph databases are optional. JSON, CSV, SQLite and MongoDB adapters MUST preserve the same logical links.

## 9. Explicit epistemic stages

LaclauGPT distinguishes epistemic type from workflow review status.

Canonical epistemic types:

```text
SOURCE_OBSERVATION
MEASUREMENT
CANDIDATE_INTERPRETATION
CONFIRMED_INTERPRETATION
RESEARCH_CLAIM
```

Semantics:

- `SOURCE_OBSERVATION`: source-bound descriptive statement, such as visible text, a spoken proposition, actor mention or directly observed event metadata.
- `MEASUREMENT`: deterministic/statistical/computational derived feature, such as sentiment score, embedding similarity, frequency or detected object.
- `CANDIDATE_INTERPRETATION`: model- or researcher-proposed interpretation not yet confirmed for scholarly use.
- `CONFIRMED_INTERPRETATION`: interpretation explicitly reviewed and accepted by an authorized researcher under a known version/provenance trail.
- `RESEARCH_CLAIM`: scholarly argument/claim that may depend on multiple confirmed interpretations, measurements and source observations.

A pipeline MUST NOT promote an object from one epistemic type to another merely because processing completed successfully.

### 9.1 Review status is orthogonal

Workflow/review states remain:

```text
PROVISIONAL
ACCEPTED
REJECTED
REVISED
CANONICAL
SUPERSEDED
```

Examples:

- a `SOURCE_OBSERVATION` may be `REJECTED` if OCR was wrong;
- a `MEASUREMENT` may be `ACCEPTED` without becoming an interpretation;
- a `CANDIDATE_INTERPRETATION` may be `ACCEPTED`, then represented as a separately versioned `CONFIRMED_INTERPRETATION`;
- a `RESEARCH_CLAIM` may be `PROVISIONAL` while a draft paper is under revision.

Review status describes workflow state. Epistemic type describes the role of the object in knowledge production.

## 10. Analysis section

Suggested conceptual shape:

```yaml
analysis:
  status: collection-only
  started_at: null
  completed_at: null
  summary: null
  analysis_objects: []
  entities: []
  entity_mentions: []
  topics: []
  topic_assignments: []
  classifications: []
  embeddings: []
  formations: []
  signifiers: []
  nodal_points: []
  discourses: []
  imaginaries: []
  relations: []
  events: []
  actors: []
  narrative_episodes: []
  us: []
  them: []
  frontier: []
  affects: []
  sentiments: []
  formula_of_populism: null
  uncertainty: []
  abstentions: []
  codebook_refs: []
  memory_refs: []
  model_runs: []
```

Existing specialized arrays MAY remain for ergonomic compatibility, but canonical implementations SHOULD expose stable object IDs and epistemic metadata for items that participate in the evidence graph.

Descriptive NLP outputs and theoretical discourse claims MUST remain distinguishable. Analysis stages MUST permit abstention.

## 11. Reusable confirmed objects and versioning

Researcher-confirmed observations and interpretations MAY become explicit inputs to later analyses.

Requirements:

- reviewed analytical objects MUST have stable `object_id` values;
- reuse MUST occur through explicit object references, never hidden prompt/context injection;
- later provenance MUST record input object IDs and versions;
- revisions MUST create a new version/object state and preserve supersession history;
- historical provenance MUST NOT be mutated;
- `supersedes`, `superseded_by` or equivalent explicit version links SHOULD be used;
- cross-run reuse MUST record reviewer, review timestamp and originating run/codebook/model version where applicable.

A confirmed object is reusable evidence, not immutable truth. Later analyses MAY contradict or supersede it while preserving the original record.

## 12. Object-level human review

Human review applies to individual analytical objects and evidence links, not only the whole canonical record.

Recommended review event:

```yaml
review_events:
  - review_id: review_001
    target_id: obj_001
    target_kind: analysis_object
    action: confirm
    reviewer: researcher_id
    reviewed_at: "2026-09-17T16:00:00Z"
    previous_status: PROVISIONAL
    new_status: ACCEPTED
    note: null
    provenance_id: prov_review_001
```

Supported actions SHOULD include:

```text
confirm
reject
revise
annotate
split
merge
flag_unsupported
attach_evidence
remove_evidence
supersede
```

Visualization SHOULD expose these actions without requiring direct database editing. Public repositories MUST use only synthetic review examples.

## 13. Cross-source qualitative comparison

Analysis objects MAY reference related objects from other canonical records.

Rules:

- every cross-source object relation MUST retain both source lineages;
- similarity, co-reference and identity MUST be separate relation types;
- automatic similarity MUST NOT silently merge actors/events/interpretations;
- human-confirmed identity merges SHOULD be auditable and reversible;
- competing interpretations of the same source unit MAY coexist.

## 14. Provenance

Provenance is append-only logical history for transformations, model runs, reuse and review.

Recommended fields:

```yaml
provenance:
  - provenance_id: prov_...
    stage: collection|preprocess|analysis|review|export
    method: ""
    module: ""
    module_version: ""
    git_commit: ""
    model: null
    model_version: null
    created_at: "2026-09-15T00:00:00Z"
    run_id: ""
    input_refs: []
    transformations: []
    metadata: {}
```

`input_refs` SHOULD include source-unit/object/version references when an analysis depends on previously derived or confirmed objects.

Provenance MUST survive backend round trips.

## 15. Record-level review section

Record-level review remains available for broad workflow state and corrections:

```yaml
review:
  status: null
  reviewer: null
  reviewed_at: null
  note: null
  corrections: {}
  flags: []
  rerun_requests: []
  review_events: []
```

Object-level review takes precedence for claims about individual analytical objects. Real researcher notes, private annotations and study-specific review data MUST NOT be committed to public repositories.

## 16. Storage-neutral serialization rules

### JSON / JSONL / NDJSON

Canonical nested representation. JSON is the reference wire format.

### Pandas / CSV

CSV is a flattened representation of the same model.

Rules:

- use stable column names derived from canonical paths;
- encode list/object values deterministically as JSON strings, not Python repr;
- preserve `schema_version` and `source_url` in every row;
- preserve source-unit, analytical-object, evidence-link and review IDs;
- document whether one logical record expands into multiple rows/tables;
- an adapter MUST reconstruct the canonical object before Analysis/Visualization semantics are applied.

For normalized tabular exports, implementations MAY use separate logical tables such as `records`, `source_units`, `analysis_objects`, `evidence_links`, `alignments` and `review_events`, linked by stable IDs.

### SQLite

SQLite MAY normalize nested structures into multiple tables, but the public repository/storage API MUST reconstruct the same canonical record and evidence graph. `source_url` SHOULD have a uniqueness constraint or equivalent dedup rule.

### MongoDB

MongoDB MAY store the canonical nested object directly. `_id` is an implementation key and MUST NOT replace `source_url` or canonical object/unit IDs.

### Parquet

Parquet MAY preserve nested structures directly or use documented deterministic encodings. Round-trip semantics remain mandatory.

### Redis and S3/Allas

Redis is cache/coordination infrastructure, not a new schema. S3/Allas stores artifacts referenced by canonical records. Neither changes record semantics.

## 17. Null and missing-value policy

- Missing optional scalar: `null` in JSON, `None` in Python.
- Missing optional list: empty list unless absence itself has distinct meaning and is documented.
- Missing optional object: `null` or empty object according to the field contract.
- Never invent empty multimodal values merely to satisfy a flat table.
- Pandas `NaN` is an adapter artifact and MUST be normalized at the boundary.

## 18. Time policy

- Use ISO 8601 timestamps.
- Prefer timezone-aware UTC (`Z`) for persisted timestamps.
- Preserve original source timezone/offset in metadata when analytically relevant.
- Distinguish source-created time, collection time, analysis time and review time.

## 19. Schema versioning

`schema_version` follows semantic-version-like rules for the data contract.

- PATCH: clarification or additive metadata that cannot break readers.
- MINOR: additive optional fields or new enum values that older readers can safely ignore.
- MAJOR: renamed/removed fields, changed meaning, changed cardinality or incompatible identity rules.

Version 1.1.0 adds optional source units, multimodal alignments, first-class analytical objects/evidence links, explicit epistemic types and object-level review while retaining compatibility with 1.0 records that omit these fields.

Every persisted schema change MUST include:

1. version bump;
2. migration note;
3. backward/forward compatibility decision;
4. synthetic fixtures;
5. round-trip tests in affected module repositories.

Implementations MUST NOT silently reinterpret an old schema version as a new one.

## 20. Legacy compatibility

Legacy schemas are boundary concerns. Adapters MAY preserve unmapped legacy values under a namespaced compatibility object such as `legacy`, but canonical code MUST NOT depend on legacy field names.

Existing 1.0 records migrate to 1.1 by treating missing `source_units`, `alignments`, `analysis.analysis_objects`, object-level `review_events` and structured evidence links as empty. Existing flat evidence IDs MAY be retained under compatibility metadata until rewritten by module adapters.

## 21. Module responsibilities

### Collection

- canonicalize source identity;
- populate `source`, source-side `content`, collection provenance and media references;
- emit addressable source units where the source/deterministic preprocessing permits;
- preserve raw temporal/spatial/source anchors;
- never emit interpretive analytical objects or research claims;
- never emit a Collection-only persistent schema.

### Analysis

- preserve source identity and source fields;
- create observations, measurements and candidate interpretations with explicit epistemic types;
- preserve graph lineage for every derived object;
- permit abstention when evidence is insufficient;
- reuse confirmed objects only through explicit references;
- enrich `evidence`, `analysis` and analysis provenance;
- never mint a replacement source identity because a representation/model run has its own ID.

### Visualization

- reconstruct canonical records before creating DataFrames/view models;
- treat Pandas columns as a view, not the source of truth;
- navigate from analytical object to exact supporting source unit where available;
- expose object-level epistemic type, review status, evidence links and competing/revised interpretations;
- support side-by-side aligned multimodal evidence where practical;
- attach review actions to canonical source/object/evidence identities.

## 22. Privacy

The schema may describe fields that are sensitive. Public repositories MUST contain only synthetic examples.

Never commit real:

- research records/corpora;
- transcripts, OCR, frames or media;
- researcher notes or review databases;
- private codebooks;
- target/account/source lists;
- database dumps;
- generated row-level exports;
- `.env`, tokens, credentials or secrets;
- private endpoints;
- machine-specific/CSC settings.

## 23. Contract tests

Each implementation repository MUST test a synthetic canonical record across every supported storage adapter.

At minimum verify:

```text
canonical object
  -> JSON
  -> CSV/Pandas
  -> SQLite
  -> Mongo-like document
  -> canonical object
```

where supported, without semantic loss beyond explicitly documented flat-format representation.

Tests MUST cover:

- source identity;
- addressable text-only source units;
- multimodal source units and alignments;
- analytical objects across all five epistemic types;
- evidence links and transitive traceability from interpretation to source unit;
- object-level review independent of record-level review;
- confirmed-object reuse and supersession/version lineage;
- nested/list values, timestamps and provenance;
- legacy migration and missing modalities.

Live MongoDB/Ollama/Redis/S3 MUST NOT be required for normal CI.

## 24. Source lineage and archaeology

Before adding new schema logic, audit useful code and conventions in legacy/current LaclauGPT repositories where authorized. Classify reusable material as `ADOPT`, `ADAPT`, `ALREADY_IMPLEMENTED`, `LEGACY_COMPATIBILITY_ONLY`, `OBSOLETE`, or `PRIVATE_DO_NOT_COPY`.

The goal is behavioral continuity without resurrecting the old monolith.
