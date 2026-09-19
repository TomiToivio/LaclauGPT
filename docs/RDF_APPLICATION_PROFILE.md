# LaclauGPT RDF / Linked Data application profile

**Status:** normative interoperability specification  
**Scope:** optional semantic interchange layer  
**Issues:** #37, #60

## 1. Purpose

LaclauGPT MAY expose canonical research records and analysis results as RDF/Linked Data. RDF is an **optional adapter**, not a replacement for the canonical record, MongoDB, Parquet, CSV, NetworkX, DNA/DATS interchange, or other operational formats.

The design rule is deliberately conservative:

> Reuse mature RDF vocabularies for generic semantics and define `laclaugpt:` terms only for discourse-theoretical semantics that cannot be represented faithfully by an established vocabulary.

The canonical LaclauGPT object remains the source of truth. RDF materialization consumes canonical objects and MUST preserve the IDs, evidence links, provenance and review state needed to interpret the resulting graph.

## 2. Project-level feature switch

RDF is selected by the **project profile** because projects own analytical modules and project-wide defaults. It MUST be disabled unless explicitly enabled.

Recommended project configuration:

```yaml
analysis:
  rdf:
    enabled: false
    required: false
    formats: [json-ld, turtle, nquads]
    store:
      backend: file
    validation:
      shacl: true
    graphrag:
      enabled: false
```

Semantics:

- `analysis.rdf.enabled: false` means no automatic RDF materialization, triple-store writes, RDF graph visualization or RDF GraphRAG retrieval.
- `analysis.rdf.enabled: true` enables the RDF postprocess/export capability for that project.
- `analysis.rdf.required: false` means RDF failures are isolated from the ordinary canonical pipeline and reported as adapter failures.
- `analysis.rdf.required: true` MAY fail the run when RDF materialization/validation fails. This is intended only for projects whose protocol explicitly requires RDF output.
- `analysis.rdf.graphrag.enabled` MUST NOT be effective unless `analysis.rdf.enabled` is true.
- machine/execution profiles MAY provide endpoint/path/capability details but MUST NOT silently enable RDF for a project.
- per-run overrides MAY narrow export scope or format, but MUST NOT bypass a project-level `enabled: false` policy unless the canonical configuration contract explicitly permits that override.

A project that omits the entire `analysis.rdf` section MUST behave as though `enabled: false` and `required: false` were configured.

## 3. Vocabulary reuse matrix

| LaclauGPT semantic object | Preferred RDF vocabulary | Notes |
| --- | --- | --- |
| source/generated object | PROV-O `prov:Entity` | use derivation/generation relations rather than custom provenance predicates |
| analysis/preprocess/export run | PROV-O `prov:Activity` | model, researcher or agent is associated as a `prov:Agent` |
| generic metadata | DCTERMS | title, creator, language, dates, identifier, source, relation, format, rights |
| dataset/export/distribution | DCAT | use for corpus/export descriptions where dataset semantics are useful |
| generic Person/Organization/Place/Event/CreativeWork | Schema.org | do not reproduce generic entity classes in `laclaugpt:` |
| evidence annotation/target | Web Annotation (`oa:`) | text spans, image regions, media fragments and annotation bodies |
| fine-grained text offsets / NLP anchoring | NIF where useful | optional profile; Web Annotation remains valid without NIF |
| concept/codebook | SKOS | concept schemes, labels, broader/narrower/related and mappings |
| lexical realization | OntoLex-Lemon | distinguish lexical entry/form from discourse concept and occurrence |
| argument claims/support/attack | AIF/AIF-RDF where applicable | argumentation is not treated as a substitute for discourse theory |
| temporal interval | OWL-Time | only when richer temporal semantics are required |
| geospatial semantics | GeoSPARQL | only when graph-native geospatial semantics are required |
| external identity/alignment | OWL/SKOS mappings | prefer `owl:sameAs`, `skos:exactMatch` or `skos:closeMatch` according to evidence strength |

The application profile MUST NOT mint LaclauGPT terms for generic people, organizations, documents, timestamps, datasets, places, provenance activities, lexical entries, or annotations merely to make names look uniform.

## 4. Minimal LaclauGPT vocabulary

The first profile defines only theory-specific classes and relations needed by LaclauGPT. Implementations MAY use a narrower subset.

### Classes

- `laclaugpt:Articulation`
- `laclaugpt:DiscourseFormation`
- `laclaugpt:Signifier`
- `laclaugpt:EmptySignifier`
- `laclaugpt:FloatingSignifier`
- `laclaugpt:NodalPoint`
- `laclaugpt:ChainOfEquivalence`
- `laclaugpt:Antagonism`
- `laclaugpt:DiscursiveFrontier`

Nodal-point, floating-signifier and empty-signifier status are contextual analytical roles. They MUST be represented through `DiscursiveRoleAssignment` rather than by permanently retyping a signifier. A role assignment links the signifier/concept to a role plus discourse/context, evidence, provenance, confidence and review state. This keeps the RDF layer aligned with the canonical discourse graph.

### Relations

- `laclaugpt:articulates`
- `laclaugpt:participatesInFormation`
- `laclaugpt:hasDiscursiveRole`\n- `laclaugpt:role`\n- `laclaugpt:concept`
- `laclaugpt:hasEquivalentMoment`
- `laclaugpt:constructsAntagonism`
- `laclaugpt:constructsFrontier`
- `laclaugpt:hasEvidence`
- `laclaugpt:reviewState`
- `laclaugpt:confidence`

Generic provenance relations remain PROV-O relations. Generic labels remain SKOS/RDFS labels. Generic source links remain DCTERMS/PROV/Web Annotation links.

## 5. Concept, lexical form and occurrence are distinct

Implementations MUST preserve this distinction:

```text
SKOS/discourse concept
        ^
        |
OntoLex lexical entry/form
        ^
        |
Web Annotation or NIF occurrence in source evidence
```

A signifier such as a project concept for “freedom” is not identical to the English lexical form `freedom`, the Finnish lexical form `vapaus`, or one occurrence of either string in a document.

Multilingual projects SHOULD represent stable concepts with SKOS, language-tagged labels and optional OntoLex lexical entries. Source-level mentions SHOULD be evidence annotations anchored to the original content.

## 6. Canonical-to-RDF mapping

| Canonical object/path | RDF representation |
| --- | --- |
| `CanonicalRecord.source_url` | stable subject URI or `dcterms:identifier`; retain literal source locator even when an internal URI is minted |
| `source.*` | DCTERMS + Schema.org + PROV-O |
| `content.*` | `schema:CreativeWork` properties and/or Web Annotation targets; large media remain external references |
| `evidence[]` | `oa:Annotation` / target-selector structures; NIF MAY be added for character-offset NLP workflows |
| `analysis.entities[]` | Schema.org classes or external entity URIs where justified |
| `analysis.entity_mentions[]` | Web Annotation/NIF occurrence linked to the entity |
| `analysis.topics[]` / codebooks | SKOS concepts/concept schemes |
| lexical signifier forms | OntoLex-Lemon |
| `analysis.formations[]` | `laclaugpt:DiscourseFormation` |
| `analysis.signifiers[]` | `laclaugpt:Signifier` and specializations when theoretically supported |
| `analysis.nodal_points[]` | `laclaugpt:NodalPoint` |
| `analysis.relations[]` | explicit `laclaugpt:Articulation` resources by default; direct predicates MAY be emitted as a derived convenience view |
| `provenance[]` | PROV-O entities/activities/agents/derivations |
| `review.*` | review-state literal/controlled URI plus PROV attribution to reviewer where publishable |
| corpus/export | DCAT Dataset/Distribution + DCTERMS + PROV-O |

### Stable URI rule

Implementations MUST use deterministic URI generation. Recommended form:

```text
{base}/{project}/{kind}/{percent-encoded-stable-id}
```

Examples:

```text
https://data.example/laclaugpt/ai26/source/sha256-...
https://data.example/laclaugpt/ai26/articulation/a-123
https://data.example/laclaugpt/ai26/evidence/e-456
```

The project namespace prevents accidental graph collision. Canonical source IDs MUST remain recoverable even when the source locator cannot itself be used safely as the RDF subject.

## 7. Assertion-level provenance

The default portable representation for analytical edges is an explicit `laclaugpt:Articulation` node. This allows evidence, confidence, provenance and review metadata to be attached without requiring RDF-star support.

Example:

```turtle
:articulation-1 a laclaugpt:Articulation ;
    laclaugpt:articulates :freedom, :regulation ;
    laclaugpt:hasEvidence :evidence-1 ;
    laclaugpt:confidence 0.87 ;
    laclaugpt:reviewState "PROVISIONAL" ;
    prov:wasGeneratedBy :analysis-run-1 .
```

RDF-star MAY be offered as an additional serialization/query optimization when a selected backend supports the required semantics. It MUST NOT be the only representation needed for interchange. Named graphs MAY be used to isolate project/run/export boundaries and SHOULD use deterministic graph URIs.

## 8. Evidence and provenance requirements

Every interpretive RDF object SHOULD preserve:

1. the canonical source or upstream entity;
2. one or more evidence references when evidence exists;
3. the activity that generated the assertion;
4. the producing human/model/agent where publishable;
5. model/prompt/codebook/version identifiers when available;
6. confidence/uncertainty when produced by the canonical analysis;
7. review state.

The RDF layer MUST preserve the canonical distinction among raw observation, deterministic transformation, statistical inference, LLM inference, human annotation and human validation. PROV specialization or activity metadata SHOULD encode this rather than flattening every result into an undifferentiated triple.

## 9. SHACL validation

`schemas/laclaugpt-rdf.shacl.ttl` defines a small operational validation profile. Implementations MAY add stricter local shapes but MUST NOT weaken required evidence/provenance rules silently.

SHACL validation is recommended before persistent store writes and explicit exports. Validation failure behavior follows `analysis.rdf.required`:

- `false`: report adapter/validation error, preserve ordinary pipeline result;
- `true`: fail the RDF-required run according to the normal run-journal/error contract.

OWL reasoning is optional and MUST NOT be required for baseline export/import.

## 10. Materialization pipeline

```text
canonical record(s)
      |
      v
RDF materializer
      |
      +--> JSON-LD
      +--> Turtle
      +--> N-Quads/N-Triples
      +--> optional RDF/XML/TriG
      +--> optional RDF store
```

Requirements:

- consume canonical schema objects, never raw prompt text as an interchange contract;
- deterministic and idempotent URI generation where practical;
- preserve evidence and provenance;
- support record, batch and corpus scopes;
- support incremental materialization;
- keep project/run boundaries explicit;
- isolate failures when RDF is optional;
- never require a running triple store merely to serialize RDF.

JSON-LD is the preferred programmatic interchange format. Turtle is the preferred human-inspection fixture format. N-Quads is preferred when named-graph boundaries must survive bulk interchange.

## 11. Optional RDF stores

All stores sit behind an `RDFStore` adapter. A project can enable serialization without enabling a server store.

Recommended backend classes:

```text
RDFStore
├── FileRDFStore
├── RDFLibStore
├── OxigraphStore
├── SPARQLStore
└── vendor-specific optional adapters
```

Expected capabilities are capability-discovered rather than assumed: query, update, named graphs, bulk load/export, authentication/TLS and health checks.

Operational MongoDB/Parquet storage remains valid and may continue to be primary. The RDF store is a semantic projection unless a project explicitly declares otherwise.

## 12. Export contract

Required formats when RDF is enabled:

- JSON-LD
- Turtle
- N-Quads or N-Triples

Optional formats:

- RDF/XML
- TriG

Export scopes MAY include project/corpus, selected documents, authors, formations, signifiers, entities, time ranges, analysis runs, named graphs or a SPARQL `CONSTRUCT` result.

An export SHOULD include DCAT/DCTERMS dataset metadata and PROV-O generation provenance sufficient to identify the project, canonical schema version, RDF profile version and export activity.

## 13. RDF GraphRAG

RDF GraphRAG is independently optional and gated by both:

```yaml
analysis:
  rdf:
    enabled: true
    graphrag:
      enabled: true
```

GraphRAG MUST retrieve bounded, provenance-preserving subgraphs rather than inject arbitrary graph dumps into prompts. Retrieval SHOULD support project/time/source/author/formation/signifier/entity/review-state filters and SHOULD return evidence references alongside analytical relations.

RDF GraphRAG is an additional context provider. It does not supersede Mongo/vector/full-text retrieval or the canonical context-memory policy.

## 14. Dashboard contract

When the project has RDF enabled, Visualization MAY expose an RDF/knowledge-graph plugin. The frontend MUST consume a vendor-neutral node/edge/query API or SPARQL adapter, not database-specific graph internals.

The plugin SHOULD support bounded neighbor expansion, class/predicate filters, provenance/evidence inspection, review/confidence filters, named-graph/project filters, prefix-aware labels, multilingual labels, and graph/table switching.

The UI MUST NOT attempt to render an unbounded corpus graph. Query-driven subgraphs are mandatory for large datasets.

If RDF is disabled for the project, RDF-specific dashboard controls SHOULD be hidden or visibly unavailable rather than issuing failing queries.

## 15. Round-trip policy

RDF export/import SHOULD round-trip the semantics needed by LaclauGPT even when byte-for-byte equality is impossible. At minimum preserve:

- canonical source identity;
- project namespace;
- evidence links;
- provenance activity/run identity;
- discourse-theoretical object type;
- relation endpoints;
- confidence/uncertainty when present;
- review state;
- external mappings and language tags.

Any deliberately lossy mapping MUST be documented by the adapter and surfaced in export metadata or logs.

## 16. Privacy and publication boundaries

RDF does not make private data public by default. Project/arena data-boundary policy still applies.

- never publish private source lists, researcher notes, private codebooks, credentials or restricted content merely because they can be serialized as RDF;
- external entity linking is optional and MUST respect study ethics and privacy policy;
- persistent store endpoints and credentials belong to machine/private runtime configuration, never public project YAML;
- exports MUST apply the same de-identification/publication rules as JSON/CSV/Parquet exports.

## 17. Implementation ownership

The meta-repository owns this application profile, minimal vocabulary, SHACL baseline and canonical mappings.

- **Data Analysis** owns canonical-result -> RDF materialization, validation, store adapters, RDF export and RDF GraphRAG provider.
- **Data Visualization** owns optional RDF graph/query visualization and dashboard export controls.
- **Data Collection** does not need to generate RDF at ingestion time; it MUST preserve stable canonical source IDs and metadata so later RDF materialization is lossless.

Implementations SHOULD add synthetic offline tests. CI MUST NOT require a live SPARQL server.

## 18. Conformance checklist

An RDF implementation conforms to this profile when:

- RDF is disabled by default and project-gated;
- ordinary non-RDF projects run without RDF dependencies;
- canonical records remain authoritative;
- standard vocabularies are reused for generic semantics;
- custom vocabulary remains small and theory-specific;
- materialization is deterministic enough for repeatable tests;
- evidence/provenance/review semantics survive export;
- SHACL can validate synthetic fixtures offline;
- at least JSON-LD, Turtle and N-Quads/N-Triples can be exported;
- GraphRAG/store/dashboard components remain optional;
- privacy/data-boundary rules are preserved.
