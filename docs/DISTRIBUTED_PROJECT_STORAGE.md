# Distributed project storage contract

LaclauGPT modules share one versioned namespace contract so multiple research projects can use the same Redis cluster, MongoDB deployment and S3-compatible bucket without colliding.

The canonical machine-readable contract is `schemas/distributed-project.schema.json`. Every submodule carries the same schema and derives names from `project_id`.

Examples of project IDs: `ai26`, `ep24`, `brazil26`, `hungary26`.

## Division of responsibility

Redis is the control plane. It distributes small versioned JSON control documents, codebooks, collection/analysis/visualization settings, run configuration, queues/streams, worker status and references to durable data. Redis is not the authoritative store for research corpora or large binary objects.

MongoDB is the queryable record plane. Canonical source records, analysis annotations, review state, run metadata and artifact metadata can share one database while remaining isolated in project-prefixed collections.

S3-compatible object storage such as CSC Allas is the object plane. Raw captures, media, transcripts, frames, exports, model-produced artifacts and large manifests can share one bucket under project-specific prefixes.

Secrets never belong in Redis documents, MongoDB records committed as examples, or object metadata. Credentials and secret-bearing endpoints remain environment/private deployment configuration.

## Namespace derivation

For project `ai26` the base Redis namespace is:

```text
laclaugpt:ai26
```

Control documents are immutable revisions plus a `current` pointer:

```text
laclaugpt:ai26:manifest:<revision>
laclaugpt:ai26:manifest:current
laclaugpt:ai26:settings:collection:<revision>
laclaugpt:ai26:settings:collection:current
laclaugpt:ai26:settings:analysis:<revision>
laclaugpt:ai26:settings:analysis:current
laclaugpt:ai26:settings:visualization:<revision>
laclaugpt:ai26:settings:visualization:current
laclaugpt:ai26:codebook:<name>:<revision>
laclaugpt:ai26:codebook:<name>:current
```

A control document uses the envelope in the JSON Schema: `schema_version`, `project_id`, `document_type`, `name`, `revision`, `updated_at`, `sha256`, `payload`, and optional durable-data `refs`.

Streams and coordination keys use the same project namespace:

```text
laclaugpt:ai26:stream:collected
laclaugpt:ai26:stream:analysis-requested
laclaugpt:ai26:stream:analyzed
laclaugpt:ai26:stream:review-events
laclaugpt:ai26:worker:collection:<worker_id>
laclaugpt:ai26:worker:analysis:<worker_id>
laclaugpt:ai26:worker:visualization:<worker_id>
laclaugpt:ai26:lock:<resource>
```

Messages should carry stable `source_url`, `project_id`, `run_id`, schema version and a MongoDB/S3 reference where applicable. A queue message should not duplicate large media or full corpora.

## MongoDB layout

The default database is `laclaugpt`. Projects get prefixed collections:

```text
ai26__records
ai26__annotations
ai26__reviews
ai26__runs
ai26__artifacts

ep24__records
ep24__annotations
...
```

The same pattern applies to `brazil26` and `hungary26`.

`source_url` remains the canonical record identity. Recommended indexes are:

- `records`: unique `source_url`; indexes on source platform/time and collection run;
- `annotations`: unique `(source_url, analysis_version)` where versioned analyses are retained;
- `reviews`: `source_url`, reviewer/review status;
- `runs`: unique `run_id`, plus start/completion/status;
- `artifacts`: `source_url`, `artifact_kind`, and durable object URI.

All persisted documents should also carry `project_id` even though the collection name already isolates the project. This catches routing mistakes and makes exports self-describing.

## S3 / CSC Allas layout

A single bucket can hold all projects:

```text
s3://<bucket>/projects/ai26/raw/
s3://<bucket>/projects/ai26/canonical/
s3://<bucket>/projects/ai26/media/
s3://<bucket>/projects/ai26/transcripts/
s3://<bucket>/projects/ai26/frames/
s3://<bucket>/projects/ai26/analysis/
s3://<bucket>/projects/ai26/codebooks/
s3://<bucket>/projects/ai26/manifests/
s3://<bucket>/projects/ai26/exports/
s3://<bucket>/projects/ai26/runs/

s3://<bucket>/projects/ep24/...
s3://<bucket>/projects/brazil26/...
s3://<bucket>/projects/hungary26/...
```

Object keys should be deterministic where practical and retain stable source identity through metadata or a source-URL hash. Enable bucket versioning when available. Never rely on object listing order as workflow state; Redis/MongoDB own workflow state and metadata.

## Redis startup flow

A distributed worker should:

1. receive or load `project_id`;
2. load the project manifest `current` pointer and immutable revision;
3. load its module settings and required codebook pointers;
4. validate `project_id`, schema version and SHA-256 hashes;
5. resolve MongoDB collections and S3 prefixes from the shared namespace helper;
6. join only that project's Redis consumer groups/streams;
7. reject records/messages whose `project_id` does not match the worker project.

This allows an AI26 worker on Laskin, an EP24/Hungary26 Slurm worker on Roihu, and a visualization worker on Pouta to use the same infrastructure safely while loading project-specific configuration dynamically.

## Portability

The contract does not require CSC. Any Redis, MongoDB and S3-compatible provider can implement the same layout. Local-first operation remains valid: the same project identity and canonical records can be represented by SQLite/filesystem/JSONL and later promoted to the distributed backends without changing `source_url` or project semantics.
