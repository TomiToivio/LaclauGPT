# Cross-module RDF / knowledge-graph architecture

**Status:** normative cross-module architecture, Phase-0 safe  
**Issue:** #60  
**Scope:** LaclauGPT meta-repository plus Data Collection, Data Analysis and Data Visualization

## Decision

LaclauGPT uses **one conceptual research graph with multiple physical backends**. RDF/JSON-LD is the semantic interchange layer, not a mandatory runtime database.

The canonical research objects remain authoritative. Knowledge-graph views are deterministic projections that preserve stable identity, evidence, provenance, uncertainty and human-review state.

Phase-0 behavior MUST remain unchanged unless KG support is explicitly enabled.

## Architectural invariants

1. **Stable semantic identity is backend-neutral.** MongoDB ObjectIds, SQLite rowids and ArangoDB `_key` values are storage details, never semantic identity.
2. **Every derived claim is traceable.** Analytical relations link to source/evidence and the run/activity that produced them.
3. **Contextual Laclaudian roles are assignments, not intrinsic word classes.** A signifier can be nodal in one discourse and floating in another.
4. **RDF is optional.** Local CSV/SQLite users do not need a triple store, MongoDB or ArangoDB.
5. **One contract, many projections.** Laclau, DNA and SNA layers reuse the same actor/source/statement/concept identities.
6. **No graph-centrality shortcut to theory.** Network metrics do not by themselves establish hegemony, nodal status, antagonism or discourse formation.

## Logical layers

### 1. Collection/source layer

Core resource kinds:

- study / collection
- source platform/channel
- document, post, message, article or transcript
- media object and derivative file
- account/person/organization
- URL and external identifier
- research note
- collection activity

Preferred vocabularies: Schema.org, DCTERMS, PROV-O and Web Annotation.

Key relations include authorship, collection/source membership, reply/mention/link/media relations and derivation.

### 2. Laclau discourse-analysis layer

Core analytical objects:

- statement / analytical unit
- signifier/concept
- articulation
- equivalence/difference relation
- discourse formation
- nodal/floating/empty **role assignment**
- chain of equivalence
- antagonism/frontier
- collective subject / actor position
- theme, arena, topic and formation labels
- evidence and confidence/review metadata

Interpretive objects MUST point to the exact evidence target and `prov:Activity` that generated them.

### 3. Phase-2 DNA layer

The DNA projection reuses actor, statement, concept and source identities.

Minimum reversible mapping:

```text
Actor --MAKES_STATEMENT--> Statement --REFERS_TO--> Concept
                         \--STANCE--> {agreement|disagreement|qualified}
Statement --IN_DOCUMENT--> Document
Statement --AT_TIME--> time
```

DNA import/export adapters should preserve qualifier/value fields and source/evidence references. LaclauGPT must not invent a parallel identity model for DNA.

### 4. Phase-2 SNA layer

SNA reuses account/person/organization identities and adds typed interaction edges:

- reply
- mention
- repost/share
- hyperlink
- co-occurrence
- membership
- other project-defined interaction types

Edges carry direction, weight, temporal scope and platform/source context. Community assignments and graph metrics are derived analytical outputs with their own run provenance.

## Stable URI policy

Recommended URI form:

```text
https://w3id.org/laclaugpt/resource/{project}/{kind}/{stable-id}
```

Examples:

```text
https://w3id.org/laclaugpt/resource/ai26/document/sha256-...
https://w3id.org/laclaugpt/resource/ai26/actor/account-123
https://w3id.org/laclaugpt/resource/ai26/statement/st-456
https://w3id.org/laclaugpt/resource/ai26/run/run-20260919T120000Z
```

Rules:

- use an existing canonical ID when available;
- otherwise derive a deterministic ID from stable upstream identity;
- never expose a database row identifier as the public semantic ID;
- identity reconciliation records MUST be explicit and provenance-bearing;
- use `owl:sameAs` only for strong identity claims; prefer SKOS mapping relations for weaker alignment.

## Vocabulary policy

Reuse before inventing:

| Need | Vocabulary |
| --- | --- |
| provenance, derivation, activity, agent | PROV-O |
| generic metadata | DCTERMS |
| web/media/person/org metadata | Schema.org |
| concepts/codebooks/signifiers | SKOS |
| text/image/media evidence anchors | Web Annotation |
| lexical forms | OntoLex-Lemon where useful |
| validation | SHACL |
| time | OWL-Time when richer intervals are required |
| geospatial semantics | GeoSPARQL when required |

The `laclaugpt:` namespace is reserved for discourse-theoretical semantics and cross-module contract terms that established vocabularies cannot express faithfully.

## Canonical node/edge contract

A backend-neutral graph API exposes at least:

### Node

```json
{
  "id": "stable URI",
  "type": "document|actor|statement|concept|articulation|formation|...",
  "label": "human-readable label",
  "project_id": "ai26",
  "properties": {},
  "provenance": {}
}
```

### Edge

```json
{
  "id": "stable URI",
  "type": "AUTHORS|MENTIONS|ARTICULATES|EQUIVALENT_TO|...",
  "source": "stable URI",
  "target": "stable URI",
  "directed": true,
  "weight": 1.0,
  "properties": {},
  "evidence": [],
  "generated_by": "stable run URI"
}
```

Interpretive relations that need assertion-level metadata SHOULD be reified as assertion resources in RDF. Direct predicates may be emitted as a convenience projection.

## Physical backends

### CSV / SQLite / DuckDB

Phase-0/local reference representation:

- `nodes.csv` / `nodes` table
- `edges.csv` / `edges` table
- optional `evidence`, `runs` and `identity_map` tables
- RDF export/import as JSON-LD, Turtle and N-Quads/N-Triples

SQLite/DuckDB are not presented as native triple stores.

### MongoDB

Recommended representation:

- canonical entity documents keyed by stable semantic ID;
- typed relationship collection keyed by stable edge ID;
- evidence/provenance embedded or referenced deterministically;
- indexes on `project_id`, type, source, target, run and time;
- RDF/JSON-LD projection at export/query boundaries.

MongoDB `_id` MUST NOT become semantic identity.

### ArangoDB

Optional graph-native adapter:

- vertex collections derived from canonical node types;
- edge collections derived from typed relationships;
- semantic URI stored as an indexed field;
- Arango `_key` remains an implementation detail;
- AQL traversal maps back to the common graph response contract.

ArangoDB is optional, not the ontology.

## Query contract

A common service should support:

- get node by stable ID;
- bounded neighbors by edge type/direction;
- filter by project/time/source/actor/concept/formation;
- evidence/provenance expansion;
- path queries with explicit maximum depth;
- aggregate counts and derived projections;
- export of a bounded subgraph.

Backend adapters implement the same semantics using local SQL/filtering, MongoDB aggregation, AQL, or SPARQL-compatible projection.

## Provenance model

Use PROV-O:

- collected source: `prov:Entity`
- collection/preprocess/analysis/export: `prov:Activity`
- researcher/model/software agent: `prov:Agent`
- derivation: `prov:wasDerivedFrom`
- generation: `prov:wasGeneratedBy`
- association: `prov:wasAssociatedWith`

For model-generated claims retain, when available: model identifier/digest, prompt version, codebook/schema version, configuration hash, timestamp, confidence/uncertainty and review state.

## JSON-LD and SHACL

The versioned context is `schemas/laclaugpt-context.v1.jsonld`.

The baseline SHACL profile is `schemas/laclaugpt-rdf.shacl.ttl`.

Validation should run before explicit RDF publication or persistent graph-store writes. Optional KG failure MUST NOT fail a normal Phase-0 run unless the project explicitly sets RDF/KG output as required.

## Phase activation

| Phase | KG behavior |
| --- | --- |
| Phase-0 | stable IDs, metadata/provenance mapping, optional export/import, fixtures, validation; disabled by default |
| Phase-1 | Laclau analytical graph and evidence-linked role assignments |
| Phase-2 | DNA and SNA projections/adapters activated without redesigning identity |
| Later | richer temporal/multimodal semantics, graph-native querying, provenance-aware GraphRAG |

## Module ownership

- **LaclauGPT:** semantic contract, namespace/context, SHACL baseline, URI policy, backend compatibility and examples.
- **Data Collection:** stable source IDs, collection provenance, source metadata and collection-boundary export.
- **Data Analysis:** Laclau/DNA/SNA analytical graph production, graph validation and storage adapters.
- **Data Visualization:** backend-neutral graph API/UI, temporal filtering, provenance/evidence inspection and graph export.

Tracking issues: Collection #117, Analysis #249, Visualization #101.

## RAG contract

Graph-assisted RAG must return bounded subgraphs plus evidence paths:

```text
answer claim
  -> analytical assertion
  -> analysis run/config/model
  -> evidence annotation
  -> canonical source
```

Graph retrieval is an optional context provider and does not replace full-text/vector retrieval.

## Backend compatibility matrix

| Capability | CSV/SQLite | MongoDB | ArangoDB | RDF file/SPARQL |
| --- | --- | --- | --- | --- |
| stable IDs | yes | yes | yes | yes |
| provenance | yes | yes | yes | yes |
| local no-service mode | yes | no | no | file: yes |
| graph traversal | bounded app/SQL | aggregation/app | native AQL | SPARQL when available |
| JSON-LD/RDF export | yes | yes | yes | native |
| Phase-0 default dependency | none | optional | optional | none |

## Migration strategy

1. Add stable IDs and provenance without changing ordinary storage.
2. Materialize the same canonical objects into node/edge projections.
3. Validate synthetic fixtures and RDF exports.
4. Add backend adapters behind the shared interface.
5. Activate DNA/SNA only in Phase-2 project profiles.
6. Never require a destructive migration merely to enable semantic export.

## Acceptance fixture

`fixtures/knowledge_graph/example.jsonld`, `nodes.csv` and `edges.csv` represent the same small research object. They demonstrate collection -> analysis -> visualization identity continuity without any database service.

## Relationship to existing specifications

This document extends rather than replaces:

- `docs/CANONICAL_DATA_CONTRACT.md`
- `docs/DISCOURSE_GRAPH_SCHEMA.md`
- `docs/RDF_APPLICATION_PROFILE.md`
- `docs/CROSS_TOOL_COMPATIBILITY_CONTRACT.md`

Where an older RDF representation conflicts with the canonical graph invariant that discursive roles are contextual assignments, the contextual-assignment model is authoritative.
