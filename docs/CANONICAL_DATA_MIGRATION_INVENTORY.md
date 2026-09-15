# Canonical Data Model Migration Inventory

**Status:** Living project-level inventory  
**Parent:** https://github.com/TomiToivio/LaclauGPT/issues/3

This inventory records where useful schema and interoperability behavior currently lives and how it should be treated during migration to the canonical data contract in `CANONICAL_DATA_CONTRACT.md`.

The classifications are:

- `ADOPT` — semantics are directly useful and should become part of the canonical contract.
- `ADAPT` — useful behavior exists but naming/architecture must change.
- `ALREADY_IMPLEMENTED` — the modular destination already contains an equivalent implementation; converge rather than duplicate.
- `LEGACY_COMPATIBILITY_ONLY` — preserve import/export behavior at an adapter boundary, not in the canonical core.
- `OBSOLETE` — historical behavior should not be carried forward.
- `PRIVATE_DO_NOT_COPY` — useful as an architectural reference only; never copy data, secrets or project-private configuration into a public repository.

## 1. CyborgAnthropology

Repository: `TomiToivio/CyborgAnthropology`

### `src/models.py`

Classification: **ADAPT**

Useful concepts:

- URL as the natural source key;
- extracted source text;
- source/content type;
- source-created timestamp;
- raw structured metadata;
- local file/media reference;
- S3/Allas reference;
- collection method;
- collector identity;
- collection timestamp;
- optional researcher note.

Migration decision:

- `scraper_url` -> canonical `source_url`;
- `scraper_text` -> `content.text`;
- scraper-specific names become acquisition-neutral source/content names;
- researcher notes move to the review layer and remain private in real datasets;
- local/S3 fields become media/file references rather than parallel storage schemas.

Do not copy scraper-specific assumptions into Analysis or Visualization.

## 2. LaclauGPT-Discourse-Analysis

Repository: `TomiToivio/LaclauGPT-Discourse-Analysis`

Classification: **ADOPT + ADAPT**

Useful areas to audit during module implementation:

- `laclaugpt/` canonical/semi-canonical models and analysis results;
- `laclaugpt_interchange/` versioned JSONL/Pydantic interchange;
- `laclaugpt/memory/` and `laclaugpt_memory/` stable IDs, aliases, provenance and context memory;
- `laclaugpt/visualization/` canonical dashboard data assumptions;
- `collector/` source identity, capture and normalization behavior;
- current provenance/review/uncertainty structures;
- current discourse concepts: formations, signifiers, nodal points, imaginaries, equivalence/difference/antagonism, affects and frontiers.

Migration decision:

- preserve semantics, provenance and human-review orientation;
- converge old IDs onto `source_url` plus `source_native_ids`;
- avoid copying the old monolithic package layout;
- current interchange ideas should inform canonical JSON/JSONL serialization;
- theoretical claims remain distinguishable from descriptive NLP output.

## 3. LaclauGPT-Multimodal-Analysis

Repository: `TomiToivio/LaclauGPT-Multimodal-Analysis`

Classification: **ADAPT + LEGACY_COMPATIBILITY_ONLY**

Useful behavior:

- preprocessing and media metadata;
- Whisper/ASR transcript and language;
- translation;
- OCR;
- frame sampling and multimodal/frame analysis;
- per-video summary analysis;
- entities, topics/themes and sentiment;
- populism/discourse analysis fields;
- post-processing/export conventions.

Migration decision:

- model these as optional structured multimodal content/evidence/analysis fields;
- convert numbered `ocr_1...n` / `frame_1...n` columns into lists of typed observations;
- retain legacy CSV mappings in adapters;
- do not require multimodal fields for text-only records;
- preserve evidence timestamps/provenance when available.

Implementation work is tracked in `LaclauGPT-Data-Analysis` issue #3.

## 4. LaclauGPT-TikTok-Scraper

Repository: `TomiToivio/LaclauGPT-TikTok-Scraper`

Classification: **ADAPT + LEGACY_COMPATIBILITY_ONLY**

Useful behavior:

- Firefox capture semantics;
- platform/source URL extraction;
- platform-native IDs;
- browser-to-local-backend payload structure;
- media/source metadata capture.

Migration decision:

- retain source identity/provenance knowledge;
- migrate useful behavior through Data Collection issue #2;
- do not make browser-extension payloads the canonical cross-module schema;
- do not preserve obsolete Node/backend architecture solely for compatibility.

## 5. LaclauGPT-Discourse-Analysis-Private

Repository: `TomiToivio/LaclauGPT-Discourse-Analysis-Private`

Classification: **PRIVATE_DO_NOT_COPY** by default

May be inspected, when authorized, for:

- newer pipeline/schema behavior;
- AI26 dashboard field usage;
- deployment lessons;
- private pilot compatibility requirements.

Rules:

- never copy research records, transcripts, media, target lists, codebooks, credentials, endpoints, machine paths or private configuration to public repos;
- only abstract reusable architecture/semantics may be reimplemented publicly;
- synthetic public fixtures must be created independently.

## 6. EP2024 / ep2024_postprocess

Classification: **ADAPT + LEGACY_COMPATIBILITY_ONLY**

Useful behavior:

- old researcher-facing field names;
- per-video review workflow;
- human corrections and rerun requests;
- tabular/dashboard compatibility requirements.

Migration decision:

- retain compatibility mapping at Visualization/Analysis boundaries;
- never make legacy dashboard columns the canonical schema;
- researcher notes/review databases remain private runtime data.

## 7. Current Data Collection module

Repository: `TomiToivio/LaclauGPT-Data-Collection`

Classification: **ALREADY_IMPLEMENTED + ADAPT**

Current useful baseline:

- `NormalizedRecord`;
- `source_url`;
- collection provenance;
- media references;
- platform/author/timestamp/text fields;
- storage-neutral architecture and privacy guards.

Migration decision:

- evolve `NormalizedRecord` into/onto the shared canonical contract;
- make `source_url` the explicit identity anchor;
- move `document_id` to alias/native-ID semantics where possible;
- ensure every storage adapter round-trips the same canonical object.

Implementation issue: https://github.com/TomiToivio/LaclauGPT-Data-Collection/issues/3

## 8. Current Data Analysis module

Repository: `TomiToivio/LaclauGPT-Data-Analysis`

Classification: **ALREADY_IMPLEMENTED + ADAPT**

Current useful baseline:

- provenance model;
- representations;
- entity mentions/NLP documents;
- embeddings;
- topics/topic assignments;
- classification results;
- storage-neutral analysis interfaces.

Migration decision:

- retain useful typed analytical objects;
- link every derived object back to canonical source identity;
- treat analysis as enrichment of a source record, not as a replacement record schema;
- absorb Ollama/memory/codebook/multimodal migration work from issues #2 and #3 into the same contract.

Implementation issue: https://github.com/TomiToivio/LaclauGPT-Data-Analysis/issues/4

## 9. Current Data Visualization module

Repository: `TomiToivio/LaclauGPT-Data-Visualization`

Classification: **ALREADY_IMPLEMENTED + ADAPT**

Current useful baseline:

- CSV/JSONL/SQLite/Pandas loading;
- normalization of entities/topics/signifiers/formations and related list fields;
- filters and researcher-facing transformations.

Migration decision:

- canonical record must be reconstructed before view-model/DataFrame transformation;
- Pandas is a presentation/exploration representation, not a persistent source of truth;
- legacy EP24 fields are handled by a bounded compatibility adapter;
- review state links to canonical source identity.

Implementation issue: https://github.com/TomiToivio/LaclauGPT-Data-Visualization/issues/3

## 10. Cross-module migration order

Recommended dependency order:

1. Freeze the project-level canonical contract and identity rules here.
2. Collection implements canonical source/core record + storage adapters.
3. Analysis imports/accepts the canonical serialized contract and enriches it.
4. Visualization reconstructs the canonical contract before producing view models.
5. Add shared synthetic fixtures or equivalent schema-versioned fixture payloads to each module.
6. Run cross-module contract tests.
7. Only then retire duplicate legacy field paths.

The modules should not wait for every historical field to be perfect before converging on identity and versioning. `schema_version` + `source_url` + deterministic serialization are the minimum interoperability spine.

## 11. Explicit non-goals

- Do not reintroduce a top-level Python implementation package.
- Do not make MongoDB, SQLite, Pandas or CSV the schema authority.
- Do not flatten every historical field into one giant table.
- Do not require multimodal fields on text-only records.
- Do not copy private research material into synthetic fixtures.
- Do not use graph centrality/frequency as an automatic substitute for discourse-theoretical interpretation.
