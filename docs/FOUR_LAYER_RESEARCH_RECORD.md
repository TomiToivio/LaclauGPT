# Four-layer LaclauGPT research record

**Contract version:** `1.1.0`  
**Scope:** LaclauGPT, Data Collection, Data Analysis and Data Visualization

This document extends the canonical data contract with an explicit preservation rule for research data. A later pipeline stage MUST enrich the record, not erase earlier evidence or researcher-facing fields.

## The four required layers

Every persisted research record has four logical layers in addition to identity, provenance and review state.

### 1. Raw capture

`raw_capture` preserves what Collection actually received from an RSS feed, API, browser/web scraper, file source or other collector.

For API/browser/RSS-style collection, preserve the exact source item or response payload when practical. For large responses, binary files or source formats that should not be embedded, preserve an immutable `raw_capture.ref` to local/S3/CSC Allas storage. Prefer both an item payload and a full-response reference when available.

Never reconstruct a normalized row and call it original raw data. Legacy imports that lack the original source payload must say so in `raw_capture.metadata`.

### 2. Intermediate processing

`intermediate` is a lossless history of source-derived processing stages. It includes, where applicable:

- Whisper/ASR results and language detection;
- translations;
- OCR observations;
- extracted/sample frame references;
- per-frame or multimodal descriptions;
- preprocessing results;
- stage-specific structured outputs and model proposals.

Later stages MUST NOT delete earlier intermediate results. Re-runs should retain sufficient provenance/history to explain which output was used.

### 3. Canonical current analysis

`analysis` contains the current structured LaclauGPT result: entities, topics, classifications, formations, signifiers, nodal points, discourses, imaginaries, relations, us/them/frontier, affects, sentiments, Formula of Populism, uncertainty, abstentions, codebook/memory references and model runs.

New analysis fields are additive. They do not replace raw or intermediate data.

### 4. Human-readable researcher view

`human_readable` contains a deterministic researcher-facing summary and Markdown report. The report should cover source identity, raw-capture availability, source text, ASR/Whisper, OCR, frame/multimodal analysis, the analysis summary and the complete structured analysis. This is generated from the canonical record rather than maintained as a competing schema.

## Legacy dataframe/dashboard compatibility

The nested `1.1.0` record is authoritative, but CSV/Pandas/dashboard views MUST continue exposing useful historical EP24-style fields. At minimum, when applicable, projections include:

- `whisper_transcript`, `whisper_language`, `whisper_translated`;
- `ocr_1` ... `ocr_6`;
- `frame_1` ... `frame_6`;
- `summary_analysis`;
- entities, topics and sentiment aliases;
- Formula of Populism aliases;
- source/country/author/video/date/storage aliases;
- historical topic-model/classifier fields when imported;
- review/researcher values when available;
- `raw_ref`, `raw_payload_json`;
- `human_readable_summary`, `human_readable_markdown`.

Imported legacy values MUST be retained when no newer canonical equivalent exists. Canonical derived values may supersede an alias when a new stage produces a real replacement.

## Storage rules

### MongoDB

Store the complete canonical `1.1.0` document, including raw/intermediate/analysis/human-readable sections. Project-prefixed collections remain defined by the distributed-storage contract. Mongo `_id` never replaces `source_url`.

### SQLite

Store complete canonical JSON keyed by `source_url`. Review state may use separate tables, but research-record fields must not be truncated into a dashboard-only row.

### JSON / JSONL

Serialize the complete nested record.

### CSV / Pandas

CSV is a researcher/interchange projection. It contains deterministic JSON columns for the nested sections **and** wide legacy-compatible columns. Reading the CSV must reconstruct the canonical record before analysis or visualization.

### S3 / CSC Allas

Large raw captures, media, frames and other artifacts may live in S3-compatible object storage. Canonical records contain durable references, checksums and provenance. One bucket can contain multiple projects under project prefixes.

### Redis

Redis is a control/coordination plane for settings, codebooks, queues, locks, cache and references. Do not use Redis as the sole durable store for raw research data, intermediate evidence or final research records.

## Module responsibilities

- **Data Collection** preserves the full received source material and normalized source metadata/content. It initializes empty intermediate/analysis sections and a collection-stage human-readable summary.
- **Data Analysis** preserves Collection fields unchanged, appends intermediate stage outputs, writes structured analysis and regenerates the legacy projection and human-readable report.
- **Data Visualization** reconstructs the canonical record before producing a DataFrame. Researcher Review and Research Data views always expose raw/intermediate/new-analysis information and populated legacy aliases.
- **LaclauGPT meta-repository** owns this normative contract and schema evolution.

## Projects

AI26, EP24, Brazil26 and Hungary26 use the same record contract. Project-specific codebooks, source lists, data and credentials remain private runtime material.

## Privacy

Public repositories contain schema, adapters, synthetic tests and generic examples only. Do not commit real research rows, source watchlists, codebooks, browser/session material, credentials, CSC project IDs, private endpoints or private object-store paths.
