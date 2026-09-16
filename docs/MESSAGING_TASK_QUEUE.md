# Optional messaging and task queue

LaclauGPT supports two execution styles without changing the canonical research-record semantics:

1. **Direct mode** for local, synchronous or simple deployments.
2. **Redis mode** for distributed messaging, task dispatch and worker coordination when multiple processes or machines need to cooperate.

Redis is optional. It is never the durable source of truth for research records, analysis results or large artifacts.

The machine-readable public contract is `schemas/messaging-task.schema.json`.

## Backend selection

A deployment selects messaging and task execution independently. In shorthand configuration notation, the supported combinations are:

```text
messaging_backend = none
task_queue_backend = direct

messaging_backend = redis
task_queue_backend = redis
```

The first pair is the default. The second pair is opt-in for distributed deployments. Mixed combinations are also valid when only messaging or only task dispatch needs Redis.

The equivalent default JSON is:

```json
{
  "schema_version": "1.0",
  "messaging_backend": "none",
  "task_queue_backend": "direct"
}
```

This is the default conceptual mode for a laptop or single-process workflow. No Redis service is needed.

A distributed deployment may opt in:

```json
{
  "schema_version": "1.0",
  "messaging_backend": "redis",
  "task_queue_backend": "redis",
  "redis": {
    "url_env": "LACLAUGPT_REDIS_URL",
    "stream_prefix": "laclaugpt",
    "consumer_group_prefix": "workers",
    "claim_idle_ms": 300000,
    "heartbeat_ttl_seconds": 60,
    "max_attempts": 5,
    "dead_letter_suffix": "dead-letter"
  }
}
```

Only the **name of the environment variable** belongs in public configuration. The Redis URL itself is private runtime configuration.

A mixed mode is valid. For example, a process may publish Redis status/events while still running tasks directly, or it may use Redis task dispatch without requiring every visualization process to consume the queue.

## When to use Redis

Prefer direct mode when:

- one process owns the pipeline step;
- local CSV/SQLite/filesystem data is sufficient;
- task handoff can happen synchronously;
- operational simplicity matters more than horizontal concurrency.

Prefer Redis when:

- collection and analysis run on different machines;
- several workers must safely share a queue;
- Slurm/server workers need asynchronous task dispatch;
- retries and abandoned-task recovery are required;
- dashboards need transient worker heartbeat/status information;
- producers and consumers should be independently restartable.

Do not add Redis merely because it is available. A queue is useful infrastructure, not part of the scientific method.

## Durable state boundary

The queue message is a pointer-rich coordination envelope, not a second research database.

- **MongoDB / SQLite / another durable record store** owns canonical records, durable job state and analysis/review results.
- **S3 / CSC Allas / filesystem** owns large artifacts and immutable/raw objects.
- **Redis** owns transient stream messages, consumer-group delivery state, leases, heartbeats, locks and caches.

A worker must commit durable output before acknowledging a Redis task. If a worker crashes after the durable write but before acknowledgement, retry must be safe through an idempotency key and durable uniqueness checks.

## Common task envelope

The schema definition `$defs.task_envelope` provides the cross-module message contract. A task carries small identifiers and durable references such as:

```json
{
  "schema_version": "1.0",
  "message_id": "msg-01",
  "task_id": "task-01",
  "project_id": "ai26",
  "run_id": "run-2026-09-16-test",
  "task_type": "analysis.document",
  "source_url": "https://example.invalid/synthetic/1",
  "record_id": null,
  "arena": "elites",
  "idempotency_key": "ai26:analysis.document:synthetic-1:v1",
  "attempt": 1,
  "created_at": "2026-09-16T00:00:00Z",
  "not_before": null,
  "schema_revision": "research-record-1.0",
  "config_revision": "sha256:synthetic-config",
  "codebook_revision": "sha256:synthetic-codebook",
  "producer": "collection-worker-example",
  "refs": [
    {
      "kind": "mongodb",
      "uri": "mongodb-ref://ai26/records/synthetic-1",
      "sha256": null
    }
  ],
  "metadata": {}
}
```

Public examples must remain synthetic. Real source lists, private codebooks, credentials and unpublished research configuration stay outside Git.

Large text, media, transcripts, frames, corpora and analysis payloads should be written durably and referenced from `refs`; they should not be copied into Redis Streams.

## Redis Streams convention

Redis Streams plus consumer groups are the preferred first implementation. A heavier queue framework should be introduced only when concrete requirements justify it.

Suggested project-scoped names follow the existing distributed storage namespace:

```text
laclaugpt:<project_id>:stream:collected
laclaugpt:<project_id>:stream:analysis-requested
laclaugpt:<project_id>:stream:analyzed
laclaugpt:<project_id>:stream:review-events
laclaugpt:<project_id>:stream:dead-letter
laclaugpt:<project_id>:worker:<role>:<worker_id>
```

The exact stream-to-task mapping belongs to the owning module, but every message must preserve `project_id` and `run_id` and should preserve canonical `source_url` when a source record is involved.

## Claim, acknowledge and retry semantics

A Redis task worker should implement the following ordering:

1. Consume/claim a task through a consumer group.
2. Validate project/run/schema/config compatibility.
3. Check the durable idempotency/result state.
4. If already complete, acknowledge without recomputing.
5. Mark or record durable in-progress state where the owning module requires it.
6. Execute the task.
7. Persist canonical result/job state and artifact references durably.
8. Only after the durable commit succeeds, acknowledge the Redis message.

If processing fails:

- leave the message pending or schedule an explicit retry;
- increment/record attempt state durably;
- allow another worker to reclaim work after `claim_idle_ms`;
- after `max_attempts`, emit a small dead-letter event and record the durable failure state.

Redis pending-entry state alone must not be the only history of failures or retries.

## Idempotency

Every task must have a stable `idempotency_key` derived from the logical operation, record identity and relevant analysis/config version. Durable storage must enforce the corresponding uniqueness rule.

Examples:

```text
<project>:collect:<source_url_hash>:<collector_version>
<project>:analyse:<source_url_hash>:<analysis_version>:<codebook_revision>
<project>:render:<run_id>:<view_revision>
```

The exact key format is module-owned, but equivalent work must resolve to the same key across workers.

## Worker heartbeat/status

`$defs.worker_heartbeat` defines the shared status envelope. Heartbeats are transient and may expire. They are useful for dashboards and operators but are not audit history.

Typical states are:

```text
starting -> idle -> busy -> idle -> draining -> stopped
                         \-> error
```

If durable worker/run audit history is required, persist a summary in the durable run store rather than relying on expired Redis heartbeat keys.

## Security and privacy

- Redis URLs and credentials come from private runtime environment/configuration only.
- Do not put credentials, cookies, tokens, full private configs or researcher notes in task metadata.
- Treat queue inspection as potentially sensitive operational access.
- Logs should identify project/run/task/worker IDs without dumping private payloads.
- Public fixtures use synthetic URLs, identifiers and hashes.

## Module responsibilities

The umbrella repository defines the contract only.

- **Data Collection** owns producing collection events/tasks and idempotent collection-side Redis adapters.
- **Data Analysis** owns analysis task consumption, claim/retry/reclaim logic and durable result-before-ack semantics.
- **Data Visualization** may consume transient status/events but should primarily read durable records/results; dashboards must not depend on Redis to reconstruct research state.

All modules must retain a direct/no-Redis path.

## AI26 distributed test

Issue #15 may use Redis mode for the laptop + CSC Roihu + Linux server test. That integration should select Redis explicitly and should not make the Redis dependency global for other LaclauGPT projects.

The same messaging contract is project-neutral and should work for AI26, EP24 and future studies without embedding study-specific vocabulary into the queue layer.
