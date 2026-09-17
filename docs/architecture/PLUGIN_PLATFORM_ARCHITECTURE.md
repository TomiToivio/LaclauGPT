# Plugin Platform Architecture

**Status:** Project-wide architecture specification  
**Owner:** `TomiToivio/LaclauGPT` meta-repository  
**Related issue:** #28

LaclauGPT uses a "WordPress for computational social science" metaphor to describe modularity. The metaphor means a small stable contract layer plus optional plugins and workflows. It does **not** mean merging Collection, Analysis and Visualization into one repository, process, runtime or machine.

The governing rule is:

> **Keep the three-module architecture; standardize the contracts and make each module internally extensible.**

## 1. Runtime boundaries

```text
DATA COLLECTION
independent deployment
server / cron / services / browser-assisted laptop
        |
        v
canonical records + durable storage references
        |
        v
DATA ANALYSIS
independent deployment
laptop / workstation / GPU server / CSC / remote model service
        |
        v
standard analytical products
        |
        v
DATA VISUALIZATION / RESEARCH UI
independent deployment
local laptop / shared web server
```

Modules communicate through versioned serialized contracts and explicit job/API interfaces. They MUST NOT depend on a shared process, a shared filesystem, or imports from another module's private implementation.

## 2. Plugin families

LaclauGPT defines four primary plugin families and one cross-cutting adapter family.

### Collection plugins

Purpose: acquire source material and emit canonical records.

Examples: RSS/Atom, Bluesky, Mastodon, browser-assisted X, TikTok, Instagram, YouTube, Telegram, scholarly APIs, generic HTML/API and file import.

Collection plugins MAY run through CLI, cron, systemd timers, browser-assisted sessions, long-running workers or optional queues.

Collection plugins MUST NOT perform substantive social-science interpretation. Source-native transcripts/captions and deterministic extraction are allowed; interpretive claims belong in Analysis.

### Analysis plugins

Purpose: transform analysis-ready records into evidence-linked analytical results.

Analysis has three stable phases:

```text
PREPROCESS -> PROCESS PLUGINS -> POSTPROCESS
```

Preprocess normalizes heterogeneous media into analysis-ready representations while preserving provenance. Process is an ordered plugin chain initially, with dependency-aware DAG execution as a future extension. Postprocess emits stable downstream products.

Examples of process plugins include claims, framing, sentiment, topic modelling, Laclau/Mouffe, Discourse Network Analysis, SNA, Bourdieu/field analysis, Luhmann-oriented coding, events, geospatial methods, political economy and researcher-defined methods.

Laclau analysis is a first-party plugin/workflow, not the architecture itself.

### Visualization plugins

Purpose: render standard logical products rather than depend on one fixed dataframe or theory-specific output.

Supported product classes include tabular data, canonical records, knowledge graphs, social/discourse networks, geodata, timelines/events, vector/RAG indexes, reports/summaries and media/artifact references.

Examples: table explorer, maps, timelines, social/discourse networks, knowledge graphs, field-space plots, statistical views and evidence/RAG explorers.

### UI / research plugins

Purpose: provide researcher-facing workflows around the same versioned contracts.

Examples: global search, semantic search, record browser, annotation/validation, merge/split concepts and entities, soft deletion, collection/analysis settings, run controls, job monitoring, codebook/model selection, reprocessing, provenance inspection, RAG chat, research agent, notes and writing workspace.

Mutating actions MUST be permission-aware and auditable. Agent actions MUST be read-only by default and MUST preserve a visible distinction between human and agent actions.

### Storage / backend adapters

Storage is infrastructure, not a fourth runtime module.

Adapters MAY target JSON/JSONL, CSV/Parquet, SQLite, MongoDB, Redis coordination, S3/Allas, vector stores or graph stores. Backend details MUST NOT leak into plugin semantics. All adapters reconstruct or reference the same logical contracts.

## 3. Plugin manifest contract

Every plugin SHOULD expose a machine-readable manifest with the following minimum semantics:

```yaml
id: laclaugpt.analysis.claims
family: analysis
name: Claims
version: 1.0.0
api_version: 1
scope: record          # record | batch | corpus | graph | ui
requires:
  - normalized.text
produces:
  - analysis.claims
config_schema: schemas/plugins/claims.schema.json
optional_dependencies: []
entrypoint: package.module:Plugin
provenance:
  records_plugin_version: true
```

Required conceptual fields:

- stable plugin ID;
- plugin family;
- semantic version;
- platform plugin API version;
- execution scope;
- declared inputs (`requires`);
- declared outputs (`produces`);
- configuration schema;
- executable entrypoint or equivalent registry key;
- optional plugin dependencies;
- provenance behavior.

A plugin MUST fail explicitly when required inputs are unavailable. Plugins MUST NOT silently invent missing fields or reinterpret backend-specific columns as canonical semantics.

## 4. Discovery and packaging

The preferred Python discovery mechanism is package entry points backed by an explicit registry. First-party plugins MAY live in their existing repositories while exposing the same interface as third-party plugins.

Conceptual entry-point groups:

```text
laclaugpt.collection
laclaugpt.analysis
laclaugpt.visualization
laclaugpt.ui
laclaugpt.storage
```

A local plugin directory MAY be supported for development and project-local extensions. Package proliferation is not a goal: stable interfaces come before splitting plugins into many repositories or distributions.

## 5. Workflow configuration

Project configuration decides which plugins are enabled and how they compose.

A minimal analysis workflow can be represented as:

```yaml
analysis:
  preprocess:
    - multimodal_to_text
  process:
    - claims
    - framing
    - laclau
  postprocess:
    - canonical_results
    - dataframe
```

The initial execution model is an ordered linear chain. A future DAG executor MAY use `requires` and `produces` to parallelize independent plugins while retaining deterministic provenance.

Zero analysis plugins is valid. This allows Collection -> canonical normalization -> Visualization/review workflows without forced theoretical interpretation.

## 6. Shared contract vocabulary

The meta-repository owns cross-module terminology and schema evolution. The canonical data contract remains normative for source records and evidence-linked analysis.

Shared logical concepts include:

```text
CanonicalRecord / CollectedRecord
MediaAsset / artifact reference
SourceUnit / EvidenceReference
NormalizedRecord
AnalysisResult
Entity / Relation
Event / Location
Embedding
GraphNode / GraphEdge
CollectionRun / AnalysisRun / PluginRun
HumanAnnotation
CodebookVersion
Privacy / Access metadata
```

Each object MUST retain a stable path back to canonical source identity where applicable.

The contract MUST keep distinct:

- raw observed source data;
- deterministic preprocessing;
- statistical/ML inference;
- LLM inference;
- human annotation;
- human-validated inference.

## 7. Standard analytical products

Postprocess exposes standard logical products so Visualization/UI plugins do not depend on theory-specific implementation details.

```text
tabular
canonical_records
knowledge_graph
social_network
discourse_network
geodata
timeline_events
vector_rag
reports
media_references
```

Product serializers SHOULD include schema/version identifiers, producing plugin/run provenance, project/study identity and access/privacy metadata.

## 8. Deployment profiles

The same contracts apply at every scale.

### Local-first

```text
collect/import -> local files or SQLite -> local analysis -> local dashboard
```

No MongoDB, Redis, object storage, RAG or agents are required.

### Shared server

```text
scheduled collectors -> durable DB/object storage -> analysis workers -> shared UI/RAG
```

Redis MAY be used for coordination but never becomes the canonical research datastore.

### Distributed / HPC

```text
Researcher laptop
  browser collection + UI

Linux server
  scheduled collectors + shared services

GPU workstation / CSC
  heavy preprocessing + analysis + reprocessing

Shared adapters
  canonical DB + optional Redis + object storage
```

Independent deployment is a design requirement, not a temporary workaround.

## 9. RAG and research-agent boundary

RAG retrieval MUST apply project/privacy filters before evidence reaches the model. Answers SHOULD return traceable evidence/provenance links.

A research agent MAY inspect the corpus, identify missing evidence, request collection, launch analysis, inspect results, generate visualizations and write research notes only when the corresponding actions are explicitly authorized.

Agent operations MUST be:

- read-only by default;
- scoped to project permissions;
- auditable;
- provenance-preserving;
- explicit about human vs agent actions;
- cautious around destructive or configuration-changing operations.

## 10. Privacy and provenance invariants

Every module and plugin MUST preserve the privacy boundary defined by the project.

Public repositories use public-safe or synthetic fixtures only. Credentials, private collection targets, unpublished study data, private codebooks/configuration and protected media stay outside public repositories.

Privacy/access metadata MUST propagate Collection -> Analysis -> Visualization and MUST also constrain RAG and agent retrieval/actions.

Every derived value, edge, event, chart point or answer SHOULD be traceable to source/evidence where feasible. Provenance records SHOULD include plugin version, run identity, model/provider/version, prompt/schema version, codebook version/hash, timestamps and validation state where relevant.

## 11. Default LaclauGPT distribution

The historical LaclauGPT workflow remains reproducible as a default distribution:

```text
Collection plugins
  -> canonical records
  -> multimodal/text preprocess
  -> Laclau/populism analysis plugin(s)
  -> standard postprocess
  -> table/network/report products
  -> researcher UI
```

Other project distributions can enable entirely different plugin stacks without containing a Laclau plugin.

## 12. Module ownership

The meta-repository owns:

- this architecture specification;
- shared terminology and logical contracts;
- plugin interface conventions;
- cross-module schema/version rules;
- deployment profiles;
- privacy/provenance invariants;
- interoperability tests/fixtures and example full-system workflows.

Implementation belongs in peer repositories:

- Collection plugin framework: `TomiToivio/LaclauGPT-Data-Collection` issue #46;
- Analysis plugin framework: `TomiToivio/LaclauGPT-Data-Analysis` issue #35;
- Visualization/UI plugin framework: `TomiToivio/LaclauGPT-Data-Visualization` issue #22.

This repository MUST NOT absorb source-specific collectors, analysis implementations, dashboard runtime code or backend-specific business logic.

## 13. Compatibility and evolution

Plugin and product contracts require explicit versioning. Breaking semantic changes require migration notes and cross-module compatibility fixtures/tests.

The meta-repository SHOULD maintain synthetic reference workflows that exercise at least:

1. lightweight CSV import -> simple analysis -> table/chart;
2. multimodal/social source -> Laclau workflow -> network/report;
3. multi-method workflow -> standard products -> research UI;
4. local/no-Redis execution and distributed/queued execution against equivalent logical records.

The architecture should evolve by strengthening contracts first. A future decision to collapse runtimes, introduce a shared implementation package or replace the linear plugin pipe with a DAG requires separate evidence and a deliberate architecture decision.
