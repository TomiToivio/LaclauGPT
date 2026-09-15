# LaclauGPT modular functional parity audit

Date: 2026-09-16

Source monolith: `TomiToivio/LaclauGPT-Discourse-Analysis`

Audited modular repositories:

- `TomiToivio/LaclauGPT`
- `TomiToivio/LaclauGPT-Data-Collection`
- `TomiToivio/LaclauGPT-Data-Analysis`
- `TomiToivio/LaclauGPT-Data-Visualization`

This audit evaluates functional preservation rather than directory-level copying. A feature counts as preserved when the modular architecture has an explicit implementation or a documented replacement that retains the research capability and the public/private boundary. Private study configuration and corpus-derived resources are intentionally excluded from the public repositories.

## Executive result

The modular split has preserved most of the important architecture and has improved separation of concerns, privacy boundaries, installability and testability. Collection and Visualization already contain explicit migration maps and canonical-schema adapters. Data Analysis contains a real provider-neutral analysis runtime, codebook machinery, context retrieval, memory, multimodal evidence support, provenance and synthetic tests.

Parity is not yet complete. Two gaps remain important enough to block a claim of full functional parity:

1. the canonical analysis pipeline does not yet expose all useful legacy discourse-analysis concepts as first-class fields;
2. there is no single cross-module synthetic regression fixture proving Collection -> Analysis -> Visualization compatibility in one end-to-end test.

These are tracked in:

- `TomiToivio/LaclauGPT-Data-Analysis#11`
- `TomiToivio/LaclauGPT#9`

The remaining gaps are therefore explicit rather than silently lost.

## Parity matrix

| Legacy feature / capability | New canonical home | Status | Evidence / tests | Action |
|---|---|---|---|---|
| Browser-assisted capture | Data Collection | replaced by safer implementation | Firefox extension and capture server in Data Collection | Keep explicit user-triggered capture as public default |
| TikTok / Instagram / X normalization | Data Collection | migrated | platform adapters and collector migration map | Maintain parser regression fixtures |
| Bluesky / RSS collection | Data Collection | migrated | reusable collectors documented in migration map | None |
| Legacy Node capture backend | Data Collection | intentionally deprecated | migration map documents typed Python replacement | None |
| Raw/session-wide automatic interception | Data Collection | intentionally deprecated as public default | privacy rationale documented | Specialized adapters may exist privately if required |
| Stable source identity (`source_url`) | Collection + Analysis + Visualization | migrated | canonical contracts and module tests | Add cross-module test in #9 |
| CSV / JSON-like interchange | all modules | migrated | canonical loading/writing contracts | Cross-module fixture in #9 |
| SQLite local-first persistence | Collection / Analysis / Visualization review storage | migrated | storage modules and tests | Cross-module fixture in #9 |
| MongoDB support | module-specific optional adapters | migrated/reimplemented | documented optional remote adapters | Keep optional, never required for CI |
| Redis support | Collection/runtime integration | migrated/reimplemented | optional remote/service config | Keep optional |
| S3 / CSC Allas-compatible object storage | Collection / deployment boundary | migrated as adapter architecture | remote/object-storage configuration documented | Integration tests can remain mocked/local |
| Canonical codebook model | Data Analysis | migrated | `codebooks.py`, public/synthetic codebooks | None |
| Country/project-specific codebooks | Data Analysis API + private study resources | preserved with privacy split | public format/API plus private resources excluded | Keep project data out of public Git |
| Human-generated entity resources | Data Analysis API + private study resources | preserved with privacy split | codebook entries/memory allow entity dictionaries | Project-specific dictionaries remain private |
| Codebook-to-prompt/context wiring | Data Analysis | migrated | `analyze_record()` retrieves codebook context; `test_analysis_runtime.py` verifies codebook refs | Expand stage coverage with #11 |
| Persistent context / memory | Data Analysis | migrated | SQLite memory, retrieval/context modules and tests | None |
| Ollama/local model runtime | Data Analysis | migrated/reimplemented | provider protocol, routing and runtime docs | None |
| Cloud fallback controls | Data Analysis | improved replacement | explicit routing/provenance policy | None |
| Summary | Data Analysis | migrated | canonical analysis result and runtime test | Add general researcher rendering in #11 |
| Entities / actors | Data Analysis | migrated | canonical entities + provenance | Extend relation support in #11 |
| Formations / ideology classification | Data Analysis | migrated | formations and classification results | None |
| Signifiers | Data Analysis | migrated | `signifiers` field | Expand subtype parity in #11 |
| Nodal points | Data Analysis | migrated | first-class `nodal_points` | None |
| Floating signifiers | Data Analysis | still missing as first-class pipeline output | not present in current `AnalysisProposal` | #11 |
| Empty-signifier candidates | Data Analysis | still missing as first-class pipeline output | not present in current `AnalysisProposal` | #11 |
| Chains of equivalence | Data Analysis | still missing as first-class pipeline output | not present in current `AnalysisProposal` | #11 |
| Chains of difference | Data Analysis | still missing as first-class pipeline output | not present in current `AnalysisProposal` | #11 |
| Antagonisms / oppositional structures | Data Analysis | still missing as first-class pipeline output | not present in current `AnalysisProposal` | #11 |
| Discourses | Data Analysis | migrated | first-class `discourses` output | None |
| Sociotechnical imaginaries | Data Analysis | migrated | first-class `imaginaries` output | None |
| Topics / themes | Data Analysis | partial | backend support exists, but not first-class in the canonical LLM proposal | #11 |
| Sentiment / stance | Data Analysis | partial | can be represented through generic classifications; richer explicit semantics are not first-class | #11 |
| Frame analysis | Data Analysis multimodal/canonical layer | partial | multimodal evidence support exists, but general parity should be explicit | #11 |
| Whisper / ASR evidence | Data Analysis multimodal | migrated/reimplemented | multimodal package + tests | Keep optional and provenance-linked |
| OCR / frame-derived evidence | Data Analysis multimodal | migrated/reimplemented | multimodal package + tests | Keep optional and provenance-linked |
| Multimodal fusion | Data Analysis | migrated/reimplemented | evidence bundle/fusion code and tests | None |
| Human-readable multimodal researcher summary | Data Analysis | migrated | `researcher_summary()` and multimodal tests | Add equivalent general analyzed-record renderer in #11 |
| Structured JSON/canonical output | Data Analysis | migrated | Pydantic canonical model | None |
| Human-readable analyzed-record export | Data Analysis / Visualization | partial | Visualization supports researcher-facing views; Analysis lacks one stable general renderer | #11 |
| Temporal/grouped aggregation | Analysis / Visualization | partial | visualization transforms and analytical backends exist; canonical aggregation API remains less explicit | #11 |
| Dashboard / researcher review | Data Visualization | migrated/reimplemented | unified app, review package, canonical dashboard tests | None |
| Monitor/live corpus status | Data Visualization | migrated/reimplemented | monitor transforms and unified dashboard | None |
| Legacy EP24 dashboard compatibility | Data Visualization | preserved through bounded adapter | `legacy_ep24.py` + migration report | Keep adapter isolated from canonical core |
| Graph/signifier/actor/timeline views | Data Visualization | migrated/reimplemented | pure transforms + unified app | None |
| Researcher correction/review semantics | Data Visualization | migrated/reimplemented | typed review package/store | None |
| Laptop/local configuration | all modules | migrated/improved | env/profile examples and docs | None |
| Server mode | all modules | migrated/improved | deployment docs/config profiles | None |
| HPC / CSC-style execution | Analysis / deployment docs | preserved architecturally | runtime configuration avoids hard-coded machine paths | Add environment-specific orchestration only where reusable |
| Privacy-safe config handling | all modules | improved replacement | `.env.example`, ignored runtime data, privacy docs/guards | None |
| Module-level unit/regression tests | each module | migrated/improved | CI workflows and synthetic tests | None |
| Cross-module end-to-end parity test | umbrella repo / CI orchestration | missing | no single Collection -> Analysis -> Visualization fixture | #9 |

## 1. Codebooks and researcher guidance

Data Analysis is the correct canonical home for reusable codebook machinery. It contains a typed `Codebook` / `CodebookEntry` API, public/synthetic codebooks, persistent memory support and context retrieval.

The analysis runtime accepts codebook entries directly, retrieves a context block from the record text and appends the retrieved codebook candidates to the model prompt with the explicit rule that they are context rather than evidence. The resulting record stores codebook references. Synthetic tests verify stable IDs, aliases and propagation of codebook references through the pipeline.

This is sufficient to confirm that codebook-driven analysis is real rather than documentation-only. The remaining concern is breadth: as the analysis pipeline gains additional discourse stages, every relevant stage should receive the same canonical codebook/context service instead of inventing stage-specific codebook logic. That requirement is included in Data Analysis #11.

Country/project-specific codebooks and human-generated entity mappings should not be copied into the public repository when they contain unpublished corpus-derived information. The correct parity model is a stable public API plus private project resources that conform to it.

## 2. Analysis functionality

The modular Data Analysis package already preserves important monolith functionality:

- provider-neutral LLM analysis;
- local Ollama-oriented routing;
- structured outputs;
- provenance and model-run metadata;
- review/uncertainty boundaries;
- entity extraction;
- formation/classification outputs;
- signifiers and nodal points;
- discourse and imaginary outputs;
- NLP/topic/embedding/statistics backends;
- persistent memory/context retrieval;
- multimodal evidence fusion and human-readable multimodal summaries.

The main parity gap is not absence of an analysis engine, but an underspecified canonical discourse schema at the orchestration layer. The current proposal shape is narrower than the useful legacy Laclau/Mouffe/Palonen vocabulary. Data Analysis #11 therefore requires explicit treatment of floating/empty signifiers, equivalence/difference chains, antagonisms, topics/themes, sentiment/stance, frame analysis, relations and aggregation.

This should be implemented as backend-neutral canonical fields with evidence, provenance and human-review semantics. It should not be solved by dumping additional opaque model JSON into an untyped field.

## 3. Data model and interoperability

All three principal modules now center `source_url` as stable identity and document canonical records instead of relying on a single storage engine. The architecture supports local files/CSV-like flows and SQLite, with optional remote adapters for MongoDB and object storage/service infrastructure.

The key remaining risk is schema drift between repositories. Module-local tests can all pass while a field is silently renamed or dropped at a repository boundary. This is why umbrella issue #9 adds one versioned synthetic fixture that must survive Collection -> Analysis -> Visualization unchanged in identity and without loss of optional legacy-compatible fields.

A single canonical logical record matters more than identical internal classes in every repository. Each module may have its own implementation types, but the serialized contract and field semantics must remain compatible.

## 4. Collection functionality

The Collection repository has an explicit migration matrix. Reusable platform parsers, browser-assisted acquisition, normalized records, storage adapters and provenance concepts have new homes. The old Node backend and broad automatic interception design are intentionally deprecated rather than accidentally omitted.

The replacement is deliberately more conservative: explicit user-triggered browser capture, a localhost capture service by default, typed Python normalization and clear separation of capture from storage. That is a functional replacement with a stronger privacy posture, not a parity regression.

Media handling is intentionally reference-first. Deployments may add explicit media transfer/download adapters, but canonical metadata capture does not require downloading media. Scheduling is treated as orchestration of the same package entry points rather than a second duplicate pipeline.

## 5. Visualization functionality

Visualization has a detailed migration report and a bounded `legacy_ep24.py` compatibility layer. It preserves the important researcher workflows without preserving the monolithic dashboard architecture:

- monitor/status views;
- actor/signifier/timeline/relation transforms;
- record selection and close reading;
- transcript/OCR/multimodal display concepts;
- human-readable summaries;
- researcher review/corrections;
- legacy EP24 compatibility where necessary;
- canonical record loading as the primary path.

The repository also includes canonical dashboard and cross-backend tests. The architectural improvement is that analysis logic no longer belongs in the UI and legacy column peculiarities are isolated in an adapter.

## 6. Configuration and environments

The modular repositories consistently replace hard-coded workstation/HPC paths with configuration profiles, environment variables and ignored runtime data. Local/laptop execution is first-class, server deployments are documented, and optional remote services can be configured without becoming import-time requirements.

This preserves the useful legacy execution modes while making machine-specific CSC paths deployment configuration instead of source code. That is the correct direction for Roihu/Pouta/Allas usage as well as researchers' laptops.

## 7. Tests and regression coverage

Existing tests already cover substantial pieces independently:

- Analysis: canonical contracts, codebook/memory behavior, fake-provider runtime, multimodal behavior, config/storage/privacy boundaries.
- Visualization: canonical dashboard flow, config and cross-backend contract behavior.
- Collection: module CI plus canonical/capture/storage-oriented tests and migration contracts.

The missing test is architectural rather than local: one fixture passing through all modules. Umbrella issue #9 is the required regression tripwire for future refactors.

## Deprecated or deliberately not migrated

The following should not be reintroduced merely for historical similarity:

- credential-bearing or project-specific public configuration;
- raw research data, browser profiles, cookies or session state in Git;
- the old Node capture backend when the Python implementation covers the reusable behavior;
- silent broad browser interception as the default public acquisition method;
- monolithic dashboards that mix analysis logic, storage, secrets and UI state;
- private Finland/Poland codebooks or corpus-derived entity mappings in public repositories.

These are documented exclusions, not lost features.

## Acceptance assessment for issue #5

- [x] Important monolith functionality inventoried at capability level.
- [x] Every major useful capability has an assigned module/home.
- [x] Codebook machinery and codebook-to-analysis wiring confirmed with synthetic tests.
- [x] Canonical identity/interoperability architecture verified at module level.
- [x] Human-readable multimodal researcher output preserved; general analyzed-record rendering tracked in Data Analysis #11.
- [x] Multimodal functionality preserved as optional evidence rather than contaminating text-only records.
- [x] Missing functionality explicitly tracked in follow-up issues.
- [x] Deprecated functionality explicitly documented.
- [x] Important module-local regression tests exist.
- [ ] One cross-module regression fixture still needs implementation: umbrella #9.
- [x] Final parity matrix documented here.

Issue #5 can therefore be considered audit-complete once this document is merged, with implementation parity gaps continuing in #9 and Data Analysis #11 rather than remaining hidden inside the audit issue.