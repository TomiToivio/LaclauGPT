# LaclauGPT storage backend contract

**Status:** project-wide normative contract  
**Scope:** Collection, Analysis, Visualization, and simulation/research-agent consumers

LaclauGPT uses one logical canonical data model across storage adapters. MongoDB is the preferred shared remote document store and may also provide lightweight graph traversal and native vector search where the connected deployment supports those capabilities. Local CSV/filesystem operation remains a first-class zero-infrastructure mode.

## Backend selection

Implementations SHOULD expose equivalent semantics to:

```text
LACLAUGPT_STORAGE_BACKEND=auto|mongodb|csv
```

The exact internal configuration API may differ by module, but the observable behavior MUST be the same:

- `auto`: use MongoDB only when a MongoDB endpoint has been explicitly configured and passes the module's connectivity/capability check; otherwise use CSV/local storage.
- `mongodb`: require MongoDB and fail clearly before processing data if it is unavailable.
- `csv`: never attempt a MongoDB connection and operate on local files only.

`auto` MUST NOT discover or invent remote endpoints. Merely installing a MongoDB client library is not sufficient to select remote storage.

Shared environment names SHOULD be:

```text
LACLAUGPT_STORAGE_BACKEND
LACLAUGPT_MONGODB_URI
LACLAUGPT_MONGODB_DATABASE
LACLAUGPT_DATA_DIR
```

For backwards compatibility a module MAY accept historical aliases such as `MONGODB_URI`, but its public documentation should prefer the project-wide names above.

## Canonical-data rule

Storage engines are adapters, not alternative schemas. Every supported adapter MUST preserve the semantics defined by `docs/CANONICAL_DATA_CONTRACT.md`, especially:

- canonical `source_url` / URI-like identity;
- source-native and legacy IDs as aliases rather than competing identities;
- raw/source metadata and content;
- source units and multimodal references when present;
- analysis objects, evidence links and explicit relationships;
- codebook/model/vector metadata;
- uncertainty and abstentions;
- provenance and processing versions;
- record-level and object-level human review;
- dataset/study/privacy classification and researcher-readable summaries where present.

Analysis enrichments MUST NOT overwrite immutable/raw collection fields.

## Local CSV/filesystem mode

CSV/local mode is the minimum common denominator and MUST remain usable without MongoDB, Redis, S3/Allas, a graph database, a vector database, or cloud infrastructure.

Nested values such as relationships, evidence, embeddings, provenance and review objects SHOULD be represented deterministically as JSON in CSV cells or in documented local sidecars/tables. An adapter MUST be able to reconstruct the canonical nested record before module semantics are applied.

Embeddings are optional. If present, local round-trips MUST preserve the vector plus its model/version/dimensionality metadata. If absent, vector features degrade cleanly rather than blocking normal operation.

## MongoDB document role

MongoDB is the preferred shared remote store when explicitly configured. Implementations SHOULD store canonical records in a representation that reconstructs the same canonical object as local mode.

MongoDB is responsible for durable shared records and queryable enrichments. It is not a replacement for Redis task coordination or S3/Allas binary object storage when those optional facilities are in use.

Remote deployment examples MUST use authentication and TLS where the deployment supports it and MUST NOT recommend unauthenticated public exposure.

## Lightweight graph contract

The canonical evidence/relationship model is storage-neutral. MongoDB MAY provide lightweight graph traversal over explicit references or edge-like records, including bounded `$graphLookup`/aggregation queries.

Typical portable relations include:

```text
Record -> Actor
Record -> Organization
Record -> Event
Record -> Location
Record -> Signifier
Record -> Frame
Record -> Imaginary
Record -> Topic
Record -> RelatedRecord
Actor -> Organization
Actor -> Signifier
Signifier -> Signifier
Frame -> Signifier
```

Every relationship MUST retain provenance/evidence and a distinguishable origin such as observed, extracted, inferred, human-validated, or simulated where applicable.

Graph queries MUST be bounded by explicit hop/node/result limits and SHOULD allow dataset/date/arena/platform filters. MongoDB is the persistence/traversal layer; NetworkX or other specialized libraries remain appropriate for centrality, community detection, shortest paths and other graph algorithms.

A dedicated graph database is therefore optional and MUST NOT be required by baseline Collection, Analysis or Visualization workflows.

## Vector and retrieval contract

Embeddings MUST carry reproducibility metadata, including at minimum model/version and dimensionality when known. Native MongoDB vector search is optional and capability-aware.

A MongoDB deployment without native vector search MUST still support ordinary canonical storage and graph/reference workflows.

Data Analysis owns embedding generation and hybrid retrieval by default. Retrieval interfaces SHOULD be backend-independent and MAY combine:

- vector similarity;
- graph neighbourhood/path evidence;
- metadata filters;
- temporal relevance;
- reviewed prior analysis/context.

Returned context SHOULD retain stable source/object IDs, retrieval method, scores where available, graph evidence where applicable, and embedding/index versions so prompt/context construction is auditable.

Visualization MAY expose these capabilities, but UI components MUST consume a repository/query abstraction rather than issuing MongoDB-specific queries directly.

## Simulation boundary

Simulation consumers MUST reuse the same canonical entity/relationship identifiers where practical while keeping empirical and simulated state explicitly separate.

Simulation records/relations MUST retain provenance such as `origin=simulated`, a simulation run ID, and source lineage when derived from empirical records. Simulated material MUST NOT be silently written back as observed evidence.

NetworkX, Mesa and simulation engines remain responsible for in-memory simulation/graph dynamics. MongoDB may persist state and provide bounded graph/vector context when configured; CSV/JSON/local files remain a valid fallback.

## Cross-module compatibility

The current implementation ownership is:

- `LaclauGPT-Data-Collection`: canonical collection persistence, `auto|mongodb|csv` selection, graph/vector metadata preservation.
- `LaclauGPT-Data-Analysis`: canonical enrichment, embeddings, graph/vector/hybrid retrieval, NetworkX export.
- `LaclauGPT-Data-Visualization`: backend-independent reads, bounded graph views and optional vector/context views.
- `LaclauGPT`: this normative cross-module contract and canonical schema.
- Social Simulation Laboratory: consumer of the same contract; empirical/simulated separation remains mandatory.

Storage is deployment infrastructure, not a module: MongoDB, Redis and S3-compatible object storage run wherever a deployment needs them. Shared contracts belong here; reusable implementation helpers stay in their owning modules.

## Security and privacy

Public repositories, tests and examples MUST NOT contain credentials, private MongoDB hosts, private source lists, research datasets, private codebooks, cookies, tokens or unpublished researcher material.

Configuration values belong in environment variables, ignored local files, a secret manager, or an authorized private runtime repository. Synthetic/public fixtures are the only acceptable public CI data.

Privacy/dataset classification and provenance MUST survive conversions between local files, MongoDB, graph views and vector indexes.

## Regression requirements

Module CI SHOULD verify, with synthetic fixtures where practical:

1. CSV/local operation works without MongoDB installed or running.
2. `auto` falls back locally when an explicitly configured MongoDB endpoint is unreachable.
3. `mongodb` mode fails clearly when the endpoint is unavailable.
4. `csv` mode never attempts a MongoDB connection.
5. Canonical identity and graph/reference fields survive local and MongoDB round-trips.
6. Optional embeddings plus model/version metadata survive round-trips.
7. MongoDB vector capability can be absent without breaking ordinary operation.
8. Graph traversal is bounded and exportable to NetworkX/specialized tooling.
9. Collection -> Analysis -> Visualization preserves the same logical canonical record in both shared-remote and local workflows.
10. No module bypasses its canonical storage/repository abstraction with an incompatible schema.

The versioned synthetic cross-module fixture under `fixtures/cross_module/` is the preferred architecture tripwire for schema parity once all modules adopt it.
