# Distributed project storage contract

LaclauGPT modules share one versioned namespace contract so multiple research projects can use shared MongoDB, optional Redis coordination/messaging and S3-compatible storage without colliding.

The canonical machine-readable storage namespace contract is `schemas/distributed-project.schema.json`. The optional messaging/task contract is `schemas/messaging-task.schema.json` and is documented in `docs/MESSAGING_TASK_QUEUE.md`.

Examples of project IDs: `ai26`, `ep24`, `brazil26`, `hungary26`.

## Division of responsibility

MongoDB is the queryable record plane. Canonical source records, analysis annotations, review state, run metadata and artifact metadata can share one database while remaining isolated in project-prefixed collections.

S3-compatible object storage such as CSC Allas is the object plane. Raw captures, media, transcripts, frames, exports, model-produced artifacts and large manifests can share one bucket under project-specific prefixes.

Redis is an **optional control/messaging plane**. When enabled it can distribute small versioned JSON control documents, task/event messages, codebook/settings references, worker status, leases, locks and cache state. Redis is not required for direct/synchronous execution and is never the authoritative store for research corpora, durable job/result state or large binary objects.

Secrets never belong in Redis documents, MongoDB records committed as examples, or object metadata. Credentials and secret-bearing endpoints remain environment/private deployment configuration.

## Optional Redis mode

A simple local deployment may use:

```text
messaging_backend = none
task_queue_backend = direct
```

and operate with filesystem/SQLite/CSV or another configured durable backend without a Redis service.

A distributed deployment may opt into:

```text
messaging_backend = redis
task_queue_backend = redis
```

and then use Redis Streams/consumer groups, leases and heartbeats according to `docs/MESSAGING_TASK_QUEUE.md`.

The presence of Redis namespace settings in the distributed storage schema does not make Redis a global runtime dependency. Module implementations must retain a no-Redis execution path.

## Namespace derivation

When Redis mode is enabled, for project `ai26` the base Redis namespace is:

```text
laclaugpt:ai26
```

Control documents may use immutable revisions plus a `current` pointer:

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

A control document uses the envelope in the distributed project JSON Schema: `schema_version`, `project_id`, `document_type`, `name`, `revision`, `updated_at`, `sha256`, `payload`, and optional durable-data `refs`.

Streams and coordination keys use the same project namespace:

```text
laclaugpt:ai26:stream:collected
laclaugpt:ai26:stream:analysis-requested
laclaugpt:ai26:stream:analyzed
laclaugpt:ai26:stream:review-events
laclaugpt:ai26:stream:dead-letter
laclaugpt:ai26:worker:collection:<worker_id>
laclaugpt:ai26:worker:analysis:<worker_id>
laclaugpt:ai26:worker:visualization:<worker_id>
laclaugpt:ai26:lock:<resource>
```

Messages should carry stable identifiers such as `source_url`, `project_id`, `run_id`, schema/config revisions and MongoDB/S3 references where applicable. A queue message should not duplicate large media, transcripts or full corpora.

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

Object keys should be deterministic where practical and retain stable source identity through metadata or a source-URL hash. Enable bucket versioning when available. Never rely on object listing order as workflow state; durable database state owns workflow history and Redis, when enabled, owns only transient delivery/coordination state.

## Redis startup flow

When Redis mode is enabled, a distributed worker should:

1. receive or load `project_id` and `run_id`;
2. load/validate the project/run manifest and immutable revisions from durable/private configuration or approved control documents;
3. validate `project_id`, schema version and hashes before accepting work;
4. resolve MongoDB collections and S3 prefixes from the shared namespace contract;
5. join only that project's Redis consumer groups/streams;
6. reject messages whose `project_id` or `run_id` does not match the worker;
7. check durable idempotency/result state before performing work;
8. persist durable results before acknowledging queue delivery.

A worker using direct mode skips the Redis-specific steps while preserving exactly the same canonical record and provenance semantics.

This allows an AI26 worker on a laptop, Roihu or Linux server to use Redis where distributed coordination is helpful, while a local EP24 or exploratory workflow can remain direct and Redis-free.

## Portability

The contract does not require CSC or Redis. Any MongoDB-compatible/durable record provider and S3-compatible object provider can implement the distributed data layout, and Redis can be enabled independently as a messaging/control adapter.

Local-first operation remains valid: the same project identity and canonical records can be represented by SQLite/filesystem/JSONL and later promoted to distributed backends without changing `source_url` or project semantics.
