# AI26 Phase 2 execution architecture — Laskin and NooPunk

> **Status:** project-level architecture documentation. Issue **#70** (Laskin) and
> **#71** (NooPunk) define the two machine roles. This document describes them as
> **one AI26 system**; it does not redefine module behaviour.
>
> **Phase:** AI26 Phase 2 only. It is not a description of Phase 1, and it does not
> apply to EP24, Brazil26 or Hungary26.
>
> **Privacy:** this file names machine **roles**, never machine addresses, ports,
> credentials, paths or account lists. Concrete values are deployment state and
> live outside the public repositories. See
> [PUBLIC_PRIVATE_STUDY_ARCHITECTURE.md](PUBLIC_PRIVATE_STUDY_ARCHITECTURE.md)
> and [RUNTIME_DATA.md](RUNTIME_DATA.md).

## Purpose

The question this document answers is not *"where is the code?"* but *"which
machine does what, and how do the two stay one system rather than two corpora?"*

AI26 Phase 2 runs on two machines. They are not two pipelines and not two
studies. They are two nodes that write into **one `ai26` namespace** with one
schema, one provenance model, and one deduplication rule — differing only in
which stages they run continuously and which on demand.

## Roles

| Machine | Non-browser collection | Browser collection | Analysis | Visualization | Execution |
| --- | --- | --- | --- | --- | --- |
| **Laskin** | **continuous** | never | **continuous** | **continuous** | cron + service |
| **NooPunk** | supported | **continuous** | on demand | on demand | service |

**Laskin is the primary always-on AI26 Phase 2 execution node.** It runs
Collection, Analysis and Visualization continuously.

**NooPunk supplies continuous browser collection** and can optionally run
Analysis and Visualization on demand for testing. It is *not* the primary
continuous analysis machine.

```text
                    AI26 sources
                         |
          +--------------+--------------+
          |                             |
   [Laskin] non-browser           [NooPunk] interactive
   collectors (continuous)        Firefox / browser capture
          |                        (continuous, localhost capture,
          |                         mirrored to shared storage)
          +--------------+--------------+
                         |
                         v
        shared AI26 infrastructure (one namespace)
        MongoDB  ·  Redis  ·  CSC Allas / S3
                         |
          +--------------+--------------+
          |                             |
   [Laskin] Analysis              [NooPunk] Analysis
   continuous, local Ollama       on demand (local or cloud)
   default model: gemma4:12b
          |                             |
          +--------------+--------------+
                         |
                         v
   [Laskin] Visualization (continuous)  ·  [NooPunk] Visualization (on demand)
```

Two properties of this diagram matter more than the boxes:

1. **The browser role is deliberately not symmetric.** Browser capture requires an
   interactive session, so it stays on the workstation and is never a Laskin duty.
   Feed polling, by contrast, must not depend on anyone being logged in, so it is
   Laskin's. Neither machine is a replica of the other.
2. **NooPunk's optional Analysis is not a second pipeline.** It consumes the same
   queue and writes the same collections under the same idempotency rule. Running
   it changes *who* processed an item, never *what the corpus is*.

## Phase 2 specifics

- **Scope.** This architecture is AI26 Phase 2 specific. The three pipeline
  modules are AI26 modules; project-specific execution paths for other studies do
  not live here.
- **Model.** Laskin's continuous analysis defaults to a **local Ollama** model,
  `gemma4:12b`, served on the Laskin host. Model selection is configuration, not
  code, so a future model can be substituted without rewriting the pipeline.
- **Machine identity.** A machine is **execution provenance, never study
  identity.** No machine creates its own database, bucket, project ID, run ID or
  codebook. That rule is what keeps the two nodes one system, and it is already
  enforced by the module runbooks
  ([Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection/blob/main/docs/AI26_TWO_MACHINE_COLLECTION.md),
  [Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis/blob/main/docs/AI26_LASKIN_ANALYSIS.md),
  [Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization/blob/main/docs/AI26_LASKIN_DASHBOARD.md)).

## The cross-machine contract

Both nodes behave as two nodes of one system only if every item below holds. Each
row names the public contract that owns it.

### Shared identity

| Item | Rule | Contract |
| --- | --- | --- |
| Project ID | one value, `ai26`, on both machines | `docs/DISTRIBUTED_PROJECT_STORAGE.md` |
| Run ID | one value, supplied per run via `LACLAUGPT_RUN_ID` | `schemas/distributed-run.schema.json` |
| Namespace | one `ai26` namespace; no machine-specific DB/bucket/tree | `docs/DISTRIBUTED_PROJECT_STORAGE.md` |
| Machine role | `machine_role` + `execution`, recorded but never part of study identity | `schemas/distributed-run.schema.json` |

### Storage planes

The three planes have deliberately different authority, and the distinction is
load-bearing:

| Plane | Role | Is it authoritative? |
| --- | --- | --- |
| **MongoDB** | durable canonical records, analysis results, failures, run metadata | **yes** — the queryable record of truth |
| **Redis** | transient coordination: queue, leases, locks, cache, heartbeat | **no** — never the corpus or durable result store |
| **CSC Allas / S3** | raw captures, media, transcripts, frames, large artifacts | **yes, for objects** — referenced by checksum, not copied |

Project-prefixed collections follow `<project>__<kind>`, for example
`ai26__records`, `ai26__analysis_results` and `ai26__analysis_failures`. Objects
live under project prefixes in the shared bucket. Redis stream and consumer-group
names are contracted, not invented per machine, and default to a shared prefix
(`stream_prefix`, `consumer_group_prefix`) with a `dead-letter` stream for final
failures — see `schemas/messaging-task.schema.json` and
[docs/MESSAGING_TASK_QUEUE.md](MESSAGING_TASK_QUEUE.md).

### Deduplication — the rule that prevents two corpora

The single most important cross-machine invariant is that **identity, not
machine, decides whether work is duplicated.**

Collection emits a `handoff` envelope whose `handoff_key` incorporates the source
revision. That key becomes the Analysis **idempotency key**:

```text
collection:   handoff.handoff_key   = H
analysis:     idempotency_key       = H
durable result unique index         = (project_id, run_id, idempotency_key)
```

Two consequences follow directly:

- **A result is written once.** A duplicate delivery, a crash-and-reclaim, or the
  second machine re-processing the same item cannot produce a second durable
  result; the unique index refuses it.
- **Analysis consumes only ready handoffs**, at the same frozen `run_id`, above
  the configured publication floor — so a node cannot silently widen the corpus by
  analysing whatever it happens to find.

### Job ownership and concurrent analysis

Both machines may run an analysis worker, so ownership must be explicit:

- Work is claimed through the Redis queue with **leases**. A worker that dies
  mid-task leaves the message pending; **lease expiry lets another worker
  reclaim it** rather than stranding the item.
- Queue acknowledgement happens **only after** the durable write. A worker killed
  between the two therefore leaves a reclaimable task, never a half-written
  result.
- The durable unique index is the final guard: even duplicated delivery around a
  crash boundary yields **one** result. Duplicate concurrent analysis of the same
  item is thus *harmless by construction* rather than prevented by a lock — which
  is the safer design, because it does not depend on both nodes agreeing on a
  lock protocol.
- Laskin's worker is **bounded**: it claims at most a configured number of tasks
  and exits, and is driven by a schedule rather than running as an immortal
  scheduler.

### Provenance

Machine identity is attached to every durable result as *execution* provenance —
which host, which worker, which model, which software revision, which codebook and
config — and remains separable from scientific source identity. The Analysis
manifest freezes the run: model, schema version, public git revision, codebook
and config fingerprints.

### Failure and reconnect behaviour

- A handled failure is requeued as a **new reference-only task** with
  `attempt + 1`; the old message is acknowledged. This avoids a reclaimed message
  retaining `attempt = 1` forever.
- After the configured attempts are exhausted, the task is **dead-lettered** and
  the final failure is written to durable history, so a poison task cannot block
  the head of the queue.
- Storage connectivity is expected to be remote, so the worker's failure
  behaviour is fail-closed: an unavailable MongoDB, Redis or object store is an
  error, not a silent local fallback that would fork the corpus onto one machine.

### Dashboard compatibility

The dashboard is a read surface over the same MongoDB, selecting AI26 explicitly
(`LACLAUGPT_VIS_PROJECT_ID=ai26`) and the canonical browser data contract. It does
not fork analysis logic and performs no discourse inference; it presents upstream
evidence and analysis for human review. Because both machines read one store, the
dashboard shows the same corpus regardless of which node collected or analysed a
given record.

## Orchestration

Each stage remains an independently restartable service, and process supervision
is external — the module runbooks own the concrete mechanism (scheduled wrappers
for bounded collection and analysis cycles, a service for the dashboard). Nothing
in this document prescribes a new supervisor, and no working deployment mechanism
should be replaced merely to standardise style.

## Verifying the two-machine system

A valid check answers whether **one record** moves through
Collection → storage → Analysis → Visualization with its identity intact. The
public, secret-free procedure is in the module runbooks; the bounded verification
contract is `skills/hermes-ai26-operations/SKILL.md`.

At minimum, a trace should show for a single item:

1. a canonical record in `<project>__records` with `handoff.status = ready`;
2. the same `handoff_key` used as the analysis `idempotency_key`;
3. exactly one durable result in `<project>__analysis_results`, with model,
   schema and worker provenance attached;
4. the item visible on the dashboard, having arrived from the same store.

Existence of processes is **not** evidence. A healthy system shows a *recent*
record traversing all four points; missing observability is reported as unknown
or degraded rather than filled in.

## Boundaries

- No credentials, connection strings, hostnames, ports or account lists in public
  repositories. Public templates such as `.env.example` only.
- Machine-specific configuration belongs in the private root.
- Reachability grants no authority between the nodes; the two machines coordinate
  through the shared contract, not through administrative control of each other.
- This architecture is AI26 Phase 2. It is not a description of any other study
  and does not introduce project-specific execution paths into the modules.

## Related documents

- [Roadmap](ROADMAP.md) — the four-phase development path
- [Deployment profiles](DEPLOYMENT_PROFILES.md) — machine/execution profiles
- [Distributed project storage](DISTRIBUTED_PROJECT_STORAGE.md) — the namespace contract
- [Messaging and task queue](MESSAGING_TASK_QUEUE.md) — the optional Redis plane
- [AI26 reference case](AI26_REFERENCE_CASE.md) — what AI26 is
- Module runbooks: [Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection/blob/main/docs/AI26_TWO_MACHINE_COLLECTION.md),
  [Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis/blob/main/docs/AI26_LASKIN_ANALYSIS.md),
  [Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization/blob/main/docs/AI26_LASKIN_DASHBOARD.md)
