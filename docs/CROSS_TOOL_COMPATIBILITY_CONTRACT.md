# Cross-tool compatibility contract

**Version:** 1.0.0-draft  
**Status:** Project-wide normative extension  
**Owner:** `TomiToivio/LaclauGPT` meta-repository  
**Related:** `docs/CANONICAL_DATA_CONTRACT.md`, `docs/INTEROPERABILITY_SPEC.md`, issue #35

This document defines the project-wide contract for interoperability with DATS, DNA/rDNA, Python, R and JavaScript ecosystems. It does not replace the canonical data contract. External formats are projections and adapters around canonical LaclauGPT research objects.

## 1. Architectural rule

```text
external collectors / DATS / DNA / Python / R / JavaScript
        <->
LaclauGPT canonical research objects + provenance
        <->
Collection / Analysis / Visualization
        <->
external analysis + visualization tools
```

The canonical LaclauGPT model is authoritative inside LaclauGPT. An import adapter MUST preserve source identity, provenance, evidence, uncertainty and review state. An export adapter MUST never silently promote machine output into verified human coding.

## 2. Canonical cross-tool research objects

All objects below use stable IDs scoped by `schema_version` and retain links to the canonical source identity.

| Object | Required semantic role |
| --- | --- |
| `Document` / `CanonicalRecord` | source identity, content, source metadata, provenance |
| `EvidenceSpan` | inspectable text/transcript/OCR/frame evidence with offsets or stable media references |
| `Code` | codebook concept with stable ID, label, hierarchy and provenance |
| `Annotation` | application of a `Code` or analytical label to evidence, including coder/model and review state |
| `ResearchNote` | researcher memo or digital-ethnography note, private by default |
| `DiscourseStatement` | actor + concept/claim/demand + stance/qualifier + source/evidence + time + coder/model + confidence + review status |
| `Relation` | typed relation such as articulation, equivalence, difference or antagonism, grounded in evidence |
| `GraphProjection` | graph semantics, node/edge meaning, projection method, weighting, temporal scope and provenance |
| `AnalyticalResult` | namespaced result produced by a method/tool/model |
| `HumanReview` | reviewer decision, correction, timestamp and target object |
| `EmbeddingReference` | embedding model/version plus stable reference to vector storage or serialized vector |
| `TemporalSeries` | time-binned analytical values with binning rule, unit and provenance |

### 2.1 Minimum shared metadata

Every derived cross-tool object SHOULD carry:

```yaml
id: stable-id
schema_version: 1.0.0-draft
source_url: stable source URL/URI
provenance_id: provenance-event-id
created_at: ISO-8601 timestamp
producer:
  type: human|model|tool
  id: researcher-or-model/tool-id
review_status: PROVISIONAL|ACCEPTED|REJECTED|REVISED|CANONICAL|SUPERSEDED
confidence: null|0..1
```

Machine-produced interpretive objects default to `PROVISIONAL`. Human review is explicit and separately recorded.

## 3. DATS compatibility

DATS is treated as a qualitative/discourse-analysis workbench, not as a replacement schema.

| DATS concept | LaclauGPT mapping |
| --- | --- |
| document | `Document` / `CanonicalRecord` |
| code | `Code` |
| annotation | `EvidenceSpan` + `Annotation` |
| hierarchy/taxonomy | codebook hierarchy |
| AI classification | namespaced `AnalyticalResult` + `Annotation` |
| human correction | `HumanReview` |
| memo/logbook | `ResearchNote` |
| concept over time | `TemporalSeries` |
| whiteboard relation | typed `GraphProjection` or `ResearchNote` relation |

### 3.1 DATS adapter requirements

Adapters MUST preserve document/project identity, code hierarchy, annotation spans, coder/model identity, reviewed-vs-machine distinction, multilingual text and provenance. Multimodal evidence SHOULD be represented through stable references when DATS cannot carry the original media object directly.

Preferred transport profiles are structured JSON/JSONL or ZIP bundles when available, with CSV as a documented flat fallback. Flat formats MUST document any lossy projection and retain stable IDs needed to reconstruct nested canonical objects.

### 3.2 Optional LLM loop

```text
human concept/codebook
 -> retrieval/classification
 -> provisional AI annotation
 -> researcher review/correction
 -> improved examples/model/context
 -> temporal tracking
```

DATS annotations and reviewed codes MAY be used as LaclauGPT context or examples. LaclauGPT outputs exported to DATS MUST be marked as provisional AI annotations unless a human reviewer has explicitly accepted them.

## 4. DNA / rDNA compatibility

`DiscourseStatement` is the principal bridge to DNA/rDNA.

Recommended shape:

```yaml
id: stmt-001
actor_id: actor-001
concept_id: concept-001
qualifier: agreement|disagreement|support|oppose|other
source_url: https://example.org/item
source_document_id: doc-001
evidence_span_id: ev-001
timestamp: 2026-09-17T00:00:00Z
attributes: {}
producer:
  type: human|model|tool
  id: coder-or-model-id
confidence: null
review_status: PROVISIONAL
provenance_id: prov-001
```

Import/export profiles SHOULD support DNA statement data, actor-concept affiliation networks, congruence networks, conflict networks, longitudinal networks, GraphML, node/edge CSV, and rDNA analytical results.

Theoretical interpretations remain separate from DNA-native facts. In particular:

```text
DiscourseStatement
 -> DNA actor/concept network
 -> network measures / coalitions / conflict
 -> optional LaclauGPT interpretation
 -> articulation / equivalence / frontier / formation proposal
```

The reverse path is also supported: DNA-coded statements and rDNA/network results may be imported as evidence-linked analytical inputs for optional LLM-assisted interpretation and visualization.

## 5. Preferred interchange formats

| Format | Policy |
| --- | --- |
| JSON / JSONL | authoritative nested interchange |
| CSV | simple/manual interoperability; flattening must be documented |
| Parquet / Arrow | preferred typed tabular interchange between Python and R |
| GraphML | minimum graph interoperability target |
| GEXF | optional Gephi-oriented graph export |
| node/edge CSV | universal graph fallback |
| JSON-LD / W3C Web Annotation | compatibility target for evidence spans and annotations |
| Vega-Lite JSON | preferred portable chart specification where applicable |

Opaque runtime state such as Python pickle, RDS or application-internal databases MUST NOT be the only exchange mechanism.

## 6. Runtime placement policy

**Python** is the primary application/runtime language. Python code belongs in the relevant module's normal package structure.

**R** integrations belong in reproducible standalone scripts under `scripts/r/` or an equivalent documented scripts directory. Initial compatibility targets are `quanteda`, `stm`, `rDNA`, `igraph`, `tidyverse`/`data.table`, `arrow` and `ggplot2`.

**JavaScript** belongs only where a browser or UI runtime benefits from it: browser capture/backend integration or Visualization frontend code. Do not add Node dependencies to Python analysis code merely to invoke a visualization library.

## 7. Theory vs method compatibility

External methods are measurement, representation or exploration layers. They do not replace Laclau/Mouffe/Palonen discourse theory.

| External observation | Must NOT be silently equated with |
| --- | --- |
| DNA actor-concept agreement | Laclauian equivalence |
| high network degree | nodal status |
| community detection | ideological formation |
| semantic similarity | equivalence |
| negative sentiment | antagonism |
| topic prevalence | hegemony |
| polysemy | empty/floating signification |
| DATS code/category | theoretical truth |
| LLM classification | verified scholarly finding |

Every theoretical promotion from a descriptive/computational result to a Laclauian claim requires inspectable evidence, explicit inference and human review.

## 8. Methodological compatibility matrix

| Method | Research use | Software/ecosystem | LaclauGPT object/plugin boundary | Evidence needed | Main limitation |
| --- | --- | --- | --- | --- | --- |
| qualitative annotation/codebooks | theory-guided coding | DATS, QDA tools | `Code`, `Annotation`, `EvidenceSpan` | source span + coder | code categories are researcher constructs |
| COTA-style concept tracking | concept change over time | DATS/COTA | `TemporalSeries`, `Annotation` | reviewed concept examples | semantic drift may be model-induced |
| discourse network analysis | actor-concept coalitions/conflict | DNA/rDNA | `DiscourseStatement`, `GraphProjection` | coded statements + dates | network relation is not Laclauian relation by default |
| SNA/community detection | structural clustering/brokerage | NetworkX, igraph, Leiden | `GraphProjection`, `AnalyticalResult` | explicit graph semantics | communities are not automatically formations |
| semantic embeddings | similarity/retrieval | sentence-transformers, HF, R bridges | `EmbeddingReference` | model/version + source | similarity is not equivalence |
| topic modelling | latent thematic structure | gensim/sklearn/quanteda | `AnalyticalResult` | corpus + preprocessing | topics are not discourses/hegemony |
| structural topic modelling | covariate-aware topics | R `stm` | `AnalyticalResult`, `TemporalSeries` | document covariates | model assumptions/instability |
| contextualized topic models | embedding-conditioned topics | CTM | `AnalyticalResult` | embedding/model metadata | topic coherence is not theoretical validity |
| BERTopic | exploratory clustered topics | BERTopic | `AnalyticalResult` | embeddings + parameters | sensitive to embedding/clustering choices |
| NER/entity resolution | actor/entity identification | spaCy/HF/custom | entity objects/mentions | source span | identity resolution errors propagate |
| classification | code/formation proposal | sklearn/HF/LLM | `Annotation`, `AnalyticalResult` | labels + validation set | labels can reify priors |
| framing analysis | frame candidates | custom/LLM/DATS | `Annotation`, relations | evidence spans | frame ontology is theory-dependent |
| temporal analysis | change, bursts, phases | pandas/R/time-series libs | `TemporalSeries` | timestamps/binning rule | collection volume can mimic change |
| multimodal analysis | image/audio/video evidence | OCR/ASR/VLM tools | `EvidenceSpan`, references | media provenance | cross-modal inference needs review |
| MCA/GDA/correspondence | relational social space | R/Python | `AnalyticalResult` | coded categorical data | axes require substantive interpretation |
| descriptive/inferential statistics | prevalence/association | scipy/statsmodels/R | `AnalyticalResult` | documented sample/design | statistical association is not discourse-theory causation |
| LLM-assisted close reading | structured interpretive proposals | LLM/RAG | provisional analysis objects | quoted evidence + prompt/model provenance | requires human validation |

## 9. Round-trip invariants

Synthetic adapters in module repositories MUST test, at minimum:

1. stable IDs survive import -> canonical -> export -> re-import;
2. source text and evidence offsets survive when the target format supports them;
3. provenance and producer identity survive;
4. machine-vs-human status survives;
5. code hierarchy survives DATS round trips;
6. actor/concept/qualifier/time survive DNA round trips;
7. lossy fields are explicitly reported, never silently dropped;
8. multilingual Unicode survives unchanged;
9. an imported external analytical result remains namespaced and is not promoted to a Laclauian fact;
10. public CI uses synthetic fixtures only.

Reference fixtures live under `docs/fixtures/interoperability/`.

## 10. Cross-repository implementation ownership

- Collection: https://github.com/TomiToivio/LaclauGPT-Data-Collection/issues/65
- Analysis: https://github.com/TomiToivio/LaclauGPT-Data-Analysis/issues/57
- Visualization: https://github.com/TomiToivio/LaclauGPT-Data-Visualization/issues/30

The module repositories implement adapters, parsers, exporters, tests and UI. This meta-repository owns the shared theory/method/data semantics and versioned compatibility contract.

## 11. Non-goals

This contract does not reimplement DATS, DNA, Gephi, 4CAT or mature statistical libraries; does not make external software outputs theoretical ground truth; does not merge the three runtime modules; and does not permit private study data to be copied into the public repository.
