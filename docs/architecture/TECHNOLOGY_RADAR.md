# LaclauGPT Technology Radar

This document records the architectural direction evaluated in issue #27. It is a technology radar, not an instruction to migrate every implementation immediately.

The governing rule is:

> **Advanced infrastructure should enhance LaclauGPT, never become mandatory for LaclauGPT.**

A useful end-to-end research workflow must continue to work on a laptop using local files plus SQLite/CSV/Parquet and local or remote model APIs. Distributed services and HPC are opt-in execution/storage adapters around the same conceptual data model.

## Architectural invariants

1. **Canonical record first, storage backend second.** The normative cross-module semantics remain in `docs/CANONICAL_DATA_CONTRACT.md`.
2. **One phenomenon, one record contract, many adapters.** MongoDB, SQLite, Parquet, CSV, Redis and S3/Allas do not define competing schemas.
3. **Meta-repository stays non-runtime.** Implementation belongs in Data Collection, Data Analysis and Data Visualization.
4. **Local mode remains first-class.** Redis, MongoDB, S3/Allas, GPU and SLURM are optional.
5. **Provenance is mandatory.** Analysis records should preserve source identity, pipeline/model/prompt/codebook versions, timestamps, validation state and human/LLM/classical-model origin where applicable.
6. **Research interpretation remains human-in-the-loop.** Computational output is evidence-bearing analytical material, not autonomous scholarly judgement.

## Technology radar

### Adopt / default direction

Use these as the boring, interoperable core when implementing new functionality, while preserving compatibility with existing code.

| Area | Direction | Notes |
| --- | --- | --- |
| API/schema | FastAPI + Pydantic | Typed public APIs and validated serialized contracts |
| Operational storage | MongoDB when distributed; SQLite/filesystem locally | Same canonical semantics in both modes |
| Bulk/object storage | CSC Allas / S3-compatible storage | Media, archives, snapshots, Parquet, model artifacts |
| Analytical interchange | Parquet + Apache Arrow | Shared substrate across Python, R and DuckDB |
| Dataframes/query | Polars + DuckDB for new transformation-heavy work | Keep Pandas for compatibility and notebooks |
| Classical ML | scikit-learn + scipy/statsmodels | Reproducible non-LLM baselines remain important |
| Linguistic NLP | spaCy | Deterministic linguistic features and custom pipelines |
| Transformer NLP | Hugging Face Transformers | Explicit model/version provenance |
| Embeddings/reranking | sentence-transformers | Keep generation independent from storage backend |
| Graph analytics | NetworkX, with igraph for larger graphs | Storage and analytics remain separate concerns |
| Local LLM interface | Ollama/provider adapters | Structured Pydantic/JSON-schema outputs preferred |
| Frontend | React + TypeScript + Vite for long-term dashboards | Streamlit remains valid for prototypes/legacy research UI |
| Developer tooling | uv/pyproject, pytest, ruff, type checking, pre-commit, CI | Optional dependency groups should isolate heavy features |

### Trial / benchmark before standardizing

These are strong candidates, but adoption should follow representative benchmarks or a concrete research need.

| Area | Candidates | Adoption trigger |
| --- | --- | --- |
| Topic exploration | BERTopic + UMAP/HDBSCAN | Human-validated exploratory value beyond existing methods |
| Dense/sparse retrieval | BGE / FlagEmbedding | Better retrieval/reranking on LaclauGPT evaluation questions |
| Vector database | Qdrant | MongoDB/local FAISS demonstrably insufficient |
| Workflow orchestration | Prefect | Multi-stage flows become difficult to reproduce/observe with simpler tooling |
| Background queue | Celery, Dramatiq, RQ or Arq | Benchmark operational simplicity against task requirements |
| Distributed dataframe/ML | Dask or Ray Data | Workloads exceed one machine or require heterogeneous distributed execution |
| GPU acceleration | RAPIDS cuDF/cuML/cuGraph, Polars GPU | Measurable gain on CSC GPU workloads |
| Graph database | ArangoDB | Persistent multi-hop graph queries or GraphRAG justify another service |
| Bayesian research analysis | PyMC + ArviZ | Study design benefits from posterior uncertainty/hierarchical modelling |
| R text-as-data | quanteda ecosystem | Comparative or publication workflow benefits from first-class R analysis |

### Hold / experimental only

Do not add these as core dependencies without a demonstrated use case:

- JAX
- graph-tool
- dedicated GraphRAG frameworks
- Kafka
- Spark
- Kubernetes-style deployment
- heavyweight multi-service orchestration

## Data and storage adapters

The canonical schema is the stable seam. Implementation repositories may provide adapters such as:

```text
StorageAdapter
├── LocalFilesystemAdapter
├── SQLiteAdapter
├── ParquetAdapter
├── MongoAdapter
└── S3AllasAdapter
```

Redis is coordination infrastructure rather than the research archive. Durable results must be persisted before asynchronous work is acknowledged.

A future shared schema package is acceptable only if it remains small, independently versioned and free of Collection/Analysis/Visualization business logic.

## Retrieval / RAG abstraction

Do not allow a RAG framework or vector database to define the LaclauGPT data model. Prefer a small internal contract:

```text
Retriever
├── KeywordRetriever
├── LocalVectorRetriever
├── MongoVectorRetriever
├── QdrantRetriever
├── GraphRetriever
└── HybridRetriever
```

A representative pipeline is:

```text
query
→ query analysis
→ lexical + vector retrieval
→ optional graph expansion
→ reranking
→ context builder
→ LLM
→ answer + citations/provenance
```

FAISS is suitable for local/offline research indexes. A dedicated shared vector service should be introduced only after retrieval benchmarks show a need.

## Graph architecture

Graph storage and graph analytics are separate decisions.

A practical maturity path is:

1. store canonical nodes/edges alongside documents/entities in ordinary persistent storage;
2. materialize into NetworkX for prototypes and small/medium graphs;
3. use igraph for larger CPU analyses;
4. test cuGraph on CSC GPU nodes where scale warrants it;
5. synchronize to a graph database only when persistent graph traversal adds real value.

Laclaudian concepts must not be collapsed into generic clustering/network outputs. Topic clusters, embedding neighborhoods and graph communities are descriptive computational features to compare with theory-guided discourse analysis.

## Execution backends

Keep execution mode independent from the conceptual pipeline:

```text
ExecutionBackend
├── LocalBackend
├── QueueBackend
└── SlurmBackend
```

`LocalBackend` must remain sufficient for a meaningful laptop workflow. `QueueBackend` may use Redis-backed workers for ordinary asynchronous jobs. `SlurmBackend` should submit batch/HPC work to CSC rather than pretending HPC nodes are permanent queue workers.

Apptainer is the preferred direction when packaged HPC environments are useful.

## Deployment profiles

### A. Laptop / zero infrastructure

```text
SQLite + local filesystem
CSV/Parquet
DuckDB
Pandas/Polars
local/cloud Ollama or provider API
FastAPI optional
Streamlit or local web UI
```

### B. Shared Linux research server

```text
MongoDB
Redis optional
S3/Allas
FastAPI
cron or worker queue
Ollama/provider API
React dashboard
```

### C. Distributed research deployment

```text
Researcher laptop:
  browser-assisted collectors
  manual coding/review tools
  dashboard

Linux server:
  collectors
  FastAPI
  realtime workers
  MongoDB
  Redis where useful
  dashboard

CSC Roihu:
  SLURM batch analysis
  embeddings
  multimodal inference
  reprocessing
  optional GPU acceleration

Shared:
  canonical contracts
  MongoDB when network policy permits
  Redis only where operationally useful
  CSC Allas/S3
```

## Benchmark programme

Technology choices should be based on representative LaclauGPT data rather than library popularity.

### Dataframe benchmark

Compare Pandas, Polars eager/lazy, DuckDB SQL and, where useful, cuDF, Dask and Ray Data on:

- nested JSON normalization
- exploding analysis fields
- joins across source/analysis/entity records
- grouping by ideology/platform/time
- large Parquet reads/writes
- S3/Allas IO

### NLP benchmark

Use human-validated multilingual samples, initially including Finnish, Polish and English where relevant. Compare candidate spaCy/Stanza/UD pipelines, transformer models, embeddings and topic configurations on:

- quality against human-coded samples
- speed and memory
- multilingual consistency
- reproducibility
- interpretability

### Retrieval benchmark

Build a small set of real LaclauGPT research questions and compare:

- lexical/BM25 retrieval
- local vector retrieval
- Mongo vector retrieval where available
- Qdrant if tested
- hybrid retrieval
- reranking
- optional graph expansion

### Graph benchmark

Compare NetworkX, igraph and cuGraph where justified. Add a persistent graph database only when benchmark questions require durable multi-hop traversal.

## Dependency policy

Heavy or infrastructure-specific libraries should be optional extras rather than universal requirements, conceptually for example:

```text
laclaugpt[analysis]
laclaugpt[nlp]
laclaugpt[graph]
laclaugpt[mongo]
laclaugpt[redis]
laclaugpt[gpu]
laclaugpt[hpc]
laclaugpt[dev]
```

The concrete extras belong in the implementation repositories that own the corresponding code.

## Decision record

Issue #27 is considered resolved at the architecture level by this radar plus the existing canonical contract, modular architecture and messaging specifications.

The decision is **incremental convergence**, not wholesale migration:

- keep the stable canonical contract;
- preserve laptop/local operation;
- introduce distributed/HPC capabilities through adapters;
- benchmark competing analytical technologies on real corpora;
- keep classical NLP/statistics, embeddings, graph analysis and structured LLM analysis as complementary layers;
- add persistent services only when they solve a measured problem.
