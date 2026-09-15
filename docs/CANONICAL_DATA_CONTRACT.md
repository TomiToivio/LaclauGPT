# Canonical LaclauGPT Data Contract

**Version:** 1.0.0-draft  
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
- Derived objects such as entity mentions, representations, relations, embeddings and review events MAY have their own IDs, but MUST retain a path back to `source_url`.
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

`evidence`, `analysis` and `review` MAY be empty when not applicable.

## 4. Source section

The source section generalizes the useful ingestion concepts from `CyborgAnthropology/src/models.py` while removing scraper-specific naming.

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

Mapping from the CyborgAnthropology model:

| CyborgAnthropology | Canonical LaclauGPT |
| --- | --- |
| `scraper_url` | `source_url` |
| `scraper_text` | `content.text` |
| `scraper_type` | `source.source_type` |
| `scraper_date` | `source.created_at` |
| `scraper_file` | `content.file_references[]` or `source.raw_ref` |
| `scraper_json` | `source.raw_metadata` or an external `raw_ref` |
| `source_type` | `source.collection_method` |
| `collector_id` | `source.collector` |
| `scraped_at` | `source.collected_at` |
| `local_file` | `content.media_references[].local_ref` |
| `allas_file` | `content.media_references[].object_ref` |
| `research_note` | `review.note`, never a public fixture with real content |

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

### 5.1 Optional multimodal content

Legacy EP24/TikTok fields are OPTIONAL. Text-only records remain valid without any of them.

Prefer structured collections:

```yaml
transcripts:
  - id: transcript_1
    text: "..."
    language: fi
    translated_text: null
    start_seconds: 0.0
    end_seconds: 8.2
    provider: whisper
    provenance_id: prov_123

ocr:
  - id: ocr_1
    text: "..."
    frame_ref: frame_3
    timestamp_seconds: 12.5
    bbox: [0.1, 0.2, 0.8, 0.4]
    provenance_id: prov_124

frames:
  - id: frame_3
    timestamp_seconds: 12.5
    media_ref: s3://bucket/key#t=12.5
    description: null
    provenance_id: prov_125
```

Legacy flat fields such as `ocr_1`, `ocr_2`, `frame_1`, `frame_2`, `whisper_transcript` and `whisper_translated` are adapter concerns. They MUST NOT become the canonical internal shape.

Large binary media MUST remain outside the record. Store references, checksums and metadata only.

## 6. Evidence section

`evidence` links derived analysis back to inspectable source material.

Typical evidence objects include:

- source text span;
- transcript segment;
- OCR observation;
- sampled frame;
- source metadata observation.

Every interpretive claim SHOULD cite one or more evidence IDs when evidence is available.

## 7. Analysis section

The analysis section combines current LaclauGPT descriptive and discourse-theoretical outputs while preserving their distinction.

Suggested conceptual shape:

```yaml
analysis:
  status: collection-only
  started_at: null
  completed_at: null
  summary: null
  representations: []
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

### 7.1 Descriptive vs interpretive

Descriptive NLP outputs and theoretical discourse claims MUST remain distinguishable.

Examples:

- entity mention: descriptive;
- topic assignment: descriptive/provisional depending on method;
- formation membership: interpretive/model-proposed until reviewed;
- floating/empty/nodal role: theoretical claim requiring evidence and review;
- antagonism: not equivalent to generic negativity;
- hegemony: corpus-level claim, never inferred from frequency or centrality alone.

### 7.2 Review state and uncertainty

Machine-produced interpretive objects SHOULD default to a provisional state and support explicit review states such as:

```text
PROVISIONAL
ACCEPTED
REJECTED
REVISED
CANONICAL
SUPERSEDED
```

Analysis stages MUST permit abstention.

## 8. Provenance

Provenance is append-only logical history for transformations and analysis runs.

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

Provenance MUST survive backend round trips.

## 9. Review section

Human review is attached to the canonical source identity and may contain corrections or workflow requests.

Recommended fields:

```yaml
review:
  status: null
  reviewer: null
  reviewed_at: null
  note: null
  corrections: {}
  flags: []
  rerun_requests: []
```

Real researcher notes, private annotations and study-specific review data MUST NOT be committed to public repositories.

## 10. Storage-neutral serialization rules

### 10.1 JSON / JSONL / NDJSON

Canonical nested representation. JSON is the reference wire format.

### 10.2 Pandas / CSV

CSV is a flattened representation of the same model.

Rules:

- use stable column names derived from canonical paths;
- encode list/object values deterministically as JSON strings, not Python repr;
- preserve `schema_version` and `source_url` in every row;
- document whether one logical record may expand into multiple rows;
- an adapter MUST reconstruct the canonical object before Analysis/Visualization semantics are applied.

### 10.3 SQLite

SQLite MAY normalize nested structures into multiple tables, but the public repository/storage API MUST reconstruct the same canonical record.

`source_url` SHOULD have a uniqueness constraint or equivalent dedup rule.

### 10.4 MongoDB

MongoDB MAY store the canonical nested object directly. `_id` is an implementation key and MUST NOT replace `source_url`.

### 10.5 Parquet

Parquet MAY preserve nested structures directly or use documented deterministic encodings. Round-trip semantics remain mandatory.

### 10.6 Redis and S3/Allas

Redis is cache/coordination infrastructure, not a new schema. S3/Allas stores artifacts referenced by canonical records. Neither changes record semantics.

## 11. Null and missing-value policy

- Missing optional scalar: `null` in JSON, `None` in Python.
- Missing optional list: empty list unless absence itself has distinct meaning and is documented.
- Missing optional object: `null` or empty object according to the field contract.
- Never invent empty multimodal values merely to satisfy a flat table.
- Pandas `NaN` is an adapter artifact and MUST be normalized at the boundary.

## 12. Time policy

- Use ISO 8601 timestamps.
- Prefer timezone-aware UTC (`Z`) for persisted timestamps.
- Preserve original source timezone/offset in metadata when analytically relevant.
- Distinguish source-created time, collection time, analysis time and review time.

## 13. Schema versioning

`schema_version` follows semantic-version-like rules for the data contract.

- PATCH: clarification or additive metadata that cannot break readers.
- MINOR: additive optional fields or new enum values that older readers can safely ignore.
- MAJOR: renamed/removed fields, changed meaning, changed cardinality or incompatible identity rules.

Every persisted schema change MUST include:

1. version bump;
2. migration note;
3. backward/forward compatibility decision;
4. synthetic fixtures;
5. round-trip tests in affected module repositories.

Implementations MUST NOT silently reinterpret an old schema version as a new one.

## 14. Legacy compatibility

Legacy schemas are boundary concerns.

Examples:

| Legacy field | Canonical destination |
| --- | --- |
| `document_id` | `source_native_ids.document_id` |
| `video_id`, `new_id`, `old_id` | `source_native_ids.*` |
| `author_username` | `source.author` |
| `recording_datetime` | `source.created_at` |
| `whisper_transcript` | `content.transcripts[].text` |
| `whisper_language` | `content.transcripts[].language` |
| `whisper_translated` | `content.transcripts[].translated_text` |
| `ocr_1...n` | `content.ocr[]` |
| `frame_1...n` | `content.frames[]` / evidence references |
| `summary_analysis` | `analysis.summary` |
| `entities`, `new_entity` | `analysis.entities[]` |
| `topics`, `new_theme` | `analysis.topics[]` |
| `positive/neutral/negative` | `analysis.sentiments[]` with provenance |
| populism/formula fields | `analysis.formula_of_populism` and relations/evidence |

Adapters MAY preserve unmapped legacy values under a namespaced compatibility object such as `legacy`, but canonical code MUST NOT depend on legacy field names.

## 15. Module responsibilities

### Collection

- canonicalize source identity;
- populate `source`, source-side `content`, collection provenance and media references;
- never emit a Collection-only persistent schema.

### Analysis

- preserve source identity and source fields;
- enrich `evidence`, `analysis` and analysis provenance;
- never mint a replacement identity because a representation/model run has its own ID.

### Visualization

- reconstruct canonical records before creating DataFrames/view models;
- treat Pandas columns as a view, not the source of truth;
- attach review actions to canonical source identity.

## 16. Privacy

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

## 17. Contract tests

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

Tests MUST cover source identity, nested/list values, optional multimodal fields, timestamps, provenance, analysis fields, review status, legacy migration and missing modalities.

Live MongoDB/Ollama/Redis/S3 MUST NOT be required for normal CI.

## 18. Source lineage and archaeology

Before adding new schema logic, audit useful code and conventions in:

- `TomiToivio/CyborgAnthropology`
- `TomiToivio/LaclauGPT-Discourse-Analysis`
- `TomiToivio/LaclauGPT-Multimodal-Analysis`
- `TomiToivio/LaclauGPT-TikTok-Scraper`
- `TomiToivio/LaclauGPT-Discourse-Analysis-Private` where authorized, with strict `PRIVATE_DO_NOT_COPY` handling
- EP2024/postprocess repositories
- current Collection, Analysis and Visualization repositories

Classify reusable material as `ADOPT`, `ADAPT`, `ALREADY_IMPLEMENTED`, `LEGACY_COMPATIBILITY_ONLY`, `OBSOLETE`, or `PRIVATE_DO_NOT_COPY`.

The goal is behavioral continuity without resurrecting the old monolith.