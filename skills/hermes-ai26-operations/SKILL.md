# Hermes AI26 operations skill

Use this skill for an explicitly authorized, bounded verification of the AI26 LaclauGPT production pipeline on Laskin.

This skill coordinates the project. Module implementation remains in the owning repositories.

## Scope

Treat the current production path as:

```text
Collection -> storage infrastructure -> Analysis -> Visualization
```

Storage (MongoDB, Redis, S3-compatible object storage) is deployment infrastructure behind each stage, not a separate pipeline stage or repository.

Inspect these public repositories and their current default branches before relying on memory:

1. `TomiToivio/LaclauGPT`
2. `TomiToivio/LaclauGPT-Data-Collection`
3. `TomiToivio/LaclauGPT-Data-Analysis`
4. `TomiToivio/LaclauGPT-Data-Visualization`

The task is observational by default. Restart, repair, issue creation, code changes or deployment changes require explicit current-task authority or a user-approved scheduled task that names those actions.

## Private state and storage infrastructure

Storage is deployment infrastructure, not a separate LaclauGPT module. MongoDB, Redis, Allas/S3 and filesystem/runtime storage belong to the deployments and modules that use them. Shared storage contracts live in the umbrella repository.

On an installation, `LACLAUGPT_PRIVATE_ROOT` should point at an established local private runtime/configuration root outside public working trees. Reuse an existing verified root if present.

Suggested private layout:

```text
projects/ai26/collection/
projects/ai26/analysis/
projects/ai26/visualization/
projects/ai26/shared/
operations/laskin/
operations/hermes/
reports/private/
runtime/          # normally ignored
secrets/          # ignored/protected
```

Raw credentials remain outside ordinary Git history. Do not commit passwords, tokens, SSH keys, cookies, authenticated MongoDB URIs, Redis secrets, Allas/OpenStack credentials or equivalent secrets. Tracked private configuration should reference protected environment/secret files.

Before any public write, strip private source/watch lists, raw research records, private host paths, endpoints, credentials and operational details.

## Required verification order

### 1. Host and checkouts

Collect publication-safe evidence for:

- hostname/role;
- checkout paths, branches and commits for all four repositories;
- available disk space for project/runtime storage;
- Python environment/dependency viability;
- relevant cron, systemd or user-service state;
- current time and last known successful pipeline activity.

Do not publish private paths or host details in public reports.

### 2. Collection

Verify current AI26 collection behavior in `LaclauGPT-Data-Collection`:

- `project_id=ai26` and correct server/Laskin execution profile;
- intended non-browser collectors are scheduled and have recent successful runs;
- browser-only collectors are not incorrectly expected to run on Laskin;
- failures/retries/backoff are observable;
- new records enter the canonical distributed store;
- provenance, source identity and timestamps are preserved;
- media/artifact references remain usable where applicable;
- no local-only shadow dataset silently replaces canonical storage.

Use counts and freshness, never private watch-list identities, in publication-safe output.

### 3. Storage infrastructure

Verify the deployed storage infrastructure with bounded diagnostics:

- MongoDB connectivity and expected AI26 collections;
- Redis connectivity and project-scoped state/queues/channels where implemented;
- Allas/S3 connectivity and representative object/reference access;
- consistent canonical `ai26` namespace;
- stable record identity and provenance contract;
- no conflicting per-module database/project namespace;
- sane runtime/retention paths;
- no private state leaking to public repositories or logs.

### 4. Analysis

Verify `LaclauGPT-Data-Analysis`:

- AI26 configuration loads from the canonical private overlay;
- scheduled analysis executes;
- new records are read/claimed and processed;
- configured Ollama/model endpoint is reachable;
- enabled stages run as currently documented;
- Laclaudian analysis completes;
- optional multimodal, DNA-compatible or Critical AI Studies stages work when enabled;
- periodic summaries/reports run when configured;
- outputs return to canonical distributed storage;
- provenance includes available prompt/model/codebook/schema/run revisions;
- failures, retries and stale queues are visible;
- no silent fallback to demo/local datasets occurs.

Do not invent formation assignments for diagnostics.

### 5. Visualization

Verify `LaclauGPT-Data-Visualization`:

- AI26 dashboard service is installed and running;
- it reads the canonical `ai26` backend;
- recent analysis results appear;
- Redis-backed status/config/task/message integrations work where implemented;
- Monitor, Explore, Networks, Records, Reports and Diagnostics views work where present;
- RAG and Hermes integrations work when enabled;
- optional DNA/RDF/GraphProjection views degrade gracefully when data is absent;
- diagnostics redact secrets;
- exposure matches the intended private/public network policy.

### 6. End-to-end canary

Prefer one recent real production record over synthetic insertion. Trace the strongest available evidence across all stages:

```text
collected_at
stored_at
analysis_started_at
analysis_completed_at
visualization-visible-at or latest dashboard refresh
```

If one or more timestamps do not exist in current contracts, report that limitation and create/comment an owning-repository issue only when authorized. Never fabricate timestamp precision.

A process existing is not evidence of health. HEALTHY requires evidence of recent end-to-end AI26 data flow and a functioning dashboard.

## Status classification

Use exactly one overall state:

- `HEALTHY`: recent end-to-end record flow is evidenced and dashboard freshness is current.
- `DEGRADED`: pipeline works partially but one or more components are stale, impaired or unverifiable.
- `BROKEN`: a required pipeline stage is demonstrably failing or data flow is stopped.
- `UNKNOWN`: available evidence is insufficient to determine current live state.

For each component report state, latest successful activity, freshness/lag when measurable, evidence, warnings/errors, and whether Hermes repaired anything or only observed it.

## Report shape

Produce a private detailed report under the authorized private root and, only when explicitly authorized, a publication-safe public summary.

Use this shape:

```text
Overall: HEALTHY | DEGRADED | BROKEN | UNKNOWN

Laskin host
Collection
Storage infrastructure
Analysis
Visualization/dashboard
End-to-end freshness
Scheduled jobs/services
MongoDB
Redis
Allas/S3
Ollama/model
RAG
Outstanding errors/warnings
Repairs performed
Issues created/commented
Recommended next action
```

Clearly separate observed facts, inferred diagnosis and recommendations.

## Issue and repair policy

When a concrete defect is found:

1. search open and closed issues in the owning repository;
2. comment on an existing issue when it already covers the defect;
3. create a new issue only when no suitable issue exists and issue creation is authorized;
4. include only sanitized reproducible evidence;
5. keep implementation in the owning repository.

Repairs must be the smallest reversible change permitted by the current authorization. Never discard uncommitted researcher work, rewrite history, delete research data, rotate credentials or alter infrastructure topology unless explicitly requested.

## Scheduled execution

A scheduled Hermes health check must represent one bounded iteration, not an instruction to run forever. The private schedule should record cadence, scope, timeout/locking, report destination, and whether issue work, restart or repair are allowed.

Before scheduled execution, load this skill plus the repo-specific agent instructions in each owning repository.