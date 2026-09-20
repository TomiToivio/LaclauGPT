<!-- PHASE-BRANCH-POLICY:v1 -->

## Mandatory phase-branch policy

LaclauGPT is developed on persistent phase branches: `phase-0`, `phase-1`, `phase-2`, `phase-3`, and `phase-4`.

**Current active/stable phase: Phase 1.** Therefore `main` must represent the current Phase-1 state and must stay synchronized with `phase-1`. The `phase-0` branch remains the preserved Phase 0 baseline and must not be repurposed or advanced.

Before making any issue-driven change, an agent MUST determine the issue's intended phase from explicit issue text, title, labels, milestone, linked plan, or repository documentation. Then:

1. Work from the matching persistent phase branch, e.g. a Phase-1 issue starts from `phase-1`, not `main` and not `phase-0`.
2. Prefer a short-lived issue branch created from that phase branch, such as `issue-123-description`, and target the pull request back to the same `phase-N` branch.
3. Never merge later-phase work into `main` while an earlier phase is current. Phase-2 through Phase-4 may advance independently without destabilizing the current Phase 1 line. `phase-0` remains the preserved Phase 0 baseline.
4. Phase-0 maintenance fixes target `phase-0` only and do not move `main` backward. Current development and fixes target `phase-1`; after validation, keep `main` synchronized with `phase-1`.
5. When the project officially advances phases, synchronize `main` to the newly active phase branch only after explicit human approval.
6. If an issue has no phase information, treat it as belonging to the current phase unless the task or surrounding roadmap clearly says otherwise. Currently that means `phase-1`.
7. Do not silently move work between phases. If implementation reveals that an issue belongs to another phase, update/document the issue or report the mismatch before merging.
8. Preserve `TOMI-LOCKED`, privacy, public/private, runtime-data, scientific-method, and module-boundary rules on every phase branch.

See `docs/PHASE_BRANCHING.md` for the repository-wide workflow.

# AGENTS.md

## Broad agent role

Agents in this repository may act as **research coordinators, academic research assistants, literature-review agents, theory/methodology assistants, project architects, data stewards, interoperability auditors and documentation maintainers**. They should understand the scientific project well enough to connect paper/theory, public codebooks, module architecture, deployment assumptions and research documentation without collapsing implementation boundaries.

This is the umbrella/meta repository. Implementation remains in the owning modules. Agents should route changes to the correct repository rather than solving every task here.

Before guessing project semantics, read current canonical material. For AI26 use this order:

1. `paper/PHASE_1_PAPER.md`
2. `docs/AI26_REFERENCE_CASE.md`
3. `docs/CANONICAL_DATA_CONTRACT.md` and architecture/runtime docs
4. current public module codebooks/configuration in the owning repository
5. situation reports and `sources/` literature workspace
6. legacy repositories only as archaeology when current public-safe material is genuinely missing

Canonical current files outrank model memory. Never reconstruct authoritative project/codebook/deployment settings from recollection when a source of truth exists.

## Scope

This repository is the LaclauGPT project / paper meta-repository. Keep it focused on scientific and project-level material, project architecture, interoperability, literature/source curation, and git submodule coordination.

Implementation belongs in the owning modules:

- collection/acquisition/normalization -> `TomiToivio/LaclauGPT-Data-Collection`
- NLP/LLM/statistics/discourse analysis -> `TomiToivio/LaclauGPT-Data-Analysis`
- dashboards/plots/maps/network visualization -> `TomiToivio/LaclauGPT-Data-Visualization`
- simulation/agent-society experiments -> `TomiToivio/LaclauGPT-Social-Simulation-Laboratory`

Storage is deployment infrastructure rather than a module boundary: MongoDB, Redis and S3-compatible object storage may run wherever a deployment requires them, behind each owning module's storage abstraction and the project-wide contract in `docs/STORAGE_BACKEND_CONTRACT.md`. There is no separate storage repository.

## Research-assistant capabilities

Agents may:

- review and improve theory/method documentation;
- maintain the paper/reference-study alignment across modules;
- search and summarize relevant literature while distinguishing source claims from LaclauGPT interpretation;
- audit cross-module contracts, schemas, privacy boundaries and deployment consistency;
- prepare issues/roadmaps for the owning implementation repository;
- inspect current events or public research context when a study design/configuration update requires it;
- identify contradictions between codebooks, paper, runtime documentation and module behavior;
- preserve a human-in-the-loop, evidence-linked research workflow.

Agents must not present provisional computational outputs as validated political/discourse-theoretical conclusions.

## AI26 public reference case

AI26 (`Ideological contestation over AI`) is the canonical public reference study for the current LaclauGPT architecture because the modular system is being developed primarily alongside the public paper in `paper/PHASE_1_PAPER.md`. Agents should use AI26 when they need a realistic cross-module example, while keeping implementations study-agnostic.

Public repositories MAY contain publication-safe AI26 methodology: project/arena definitions, conceptual codebooks, sensitising formation labels, analytic hints, public source-family examples, synthetic fixtures, example prompts and secret-free runtime profiles. This material should track the paper and documented situation reports.

The six current computational formation labels are reproducibility anchors, not a closed ontology: `accelerationism`, `doomerism`, `left-wing accelerationism`, `ai safety`, `ai critical`, and `anti-ai`. Analysis must begin from evidence-linked claims, demands, signifiers, relations, subjects, affects and imaginaries; documents and actors may overlap formations or remain unclassified.

Current situation-specific terms such as `safety`, `pacing`, `competition`, `innovation`, `China`, `control`, `liability`, `independent evaluation`, `regulation`, `labour`, `surveillance`, `data centres`, and `ownership` are candidate signifiers/context cues, not automatic ideological labels.

Never publish credentials, cookies, browser profiles, private API/backend endpoints, machine-specific secrets, private source/watch lists, row-level research data, researcher notes or unpublished annotations. Public AI26 examples should be reproducible without exposing operational research infrastructure. See `docs/AI26_REFERENCE_CASE.md`.

## Source-reading workspace

Use `sources/` as the publication-safe literature workspace. Researchers may place local PDFs under `sources/pdfs/`; that directory and all PDFs under `sources/` are Git-ignored.

When asked to process source PDFs:

1. inspect the local PDFs in `sources/pdfs/`;
2. identify bibliographic metadata only from verifiable information in the document or a reliable external source;
3. add/update the compact index in `sources/SOURCES.md`;
4. add/update concise analytical summaries in `sources/SUMMARIES.md`;
5. distinguish source claims from LaclauGPT interpretation;
6. explain relevance to `paper/PHASE_1_PAPER.md` where material;
7. prefer updating an existing entry over creating duplicates;
8. do not commit PDFs, extracted full text, private annotations, or long copyrighted passages.

Whenever an agent encounters a paper, book, chapter, preprint, or substantial methodological source that is plausibly related to LaclauGPT during literature searches, repository work, issue preparation, or research discussion, also check and update `sources/READING_SUGGESTIONS.md`. This reading-suggestions file is cumulative and is not limited to locally downloaded PDFs. Add concise verified bibliographic metadata plus a short statement of LaclauGPT relevance; update existing entries rather than duplicating them. Inclusion is a reading recommendation, not endorsement and not automatic incorporation into the paper.

See `sources/README.md` for the expected workflow and templates.

## Submodules

Canonical paths are `modules/data-collection`, `modules/data-analysis`, and `modules/data-visualization` plus any explicitly documented newer modules. Update gitlinks deliberately; do not copy module source trees into this repository.

## Mandatory runtime data contract

Read `docs/RUNTIME_DATA.md`. Every module uses its repository-local `data/` directory as the private runtime root, and the entire `data/` tree stays outside Git.

Runtime logs, databases, local settings, CSV/JSONL files, private/operational study codebooks, source/target lists, downloads, media, transcripts, frames, exports, caches, temporary files, Ollama material, Whisper model caches and other generated artifacts belong under `data/`.

Do not use `.gitkeep` or tracked README files inside `data/`. Public templates, schemas, public-safe AI26 methodology and synthetic test fixtures live outside `data/`.

### Same-machine pipeline

When modules run as sibling repositories on one machine:

1. Analysis may read canonical data directly from `LaclauGPT-Data-Collection/data/` through runtime configuration.
2. Visualization may read canonical analysis results directly from `LaclauGPT-Data-Analysis/data/` through runtime configuration.
3. Private data must not be copied into Git merely to connect modules.

### Distributed pipeline

Use MongoDB for records, Redis for coordination/cache/state, and S3-compatible object storage such as CSC Allas for files and large artifacts. CSV/JSONL export/import is the explicit manual fallback.

Storage topology must not change canonical record semantics.

## Canonical data contract

`docs/CANONICAL_DATA_CONTRACT.md` is the source of truth for semantics across Collection -> Analysis -> Visualization and future modules.

- Preserve stable source identity across modules and storage backends.
- Treat CSV/Pandas, SQLite, MongoDB, JSONL, Parquet, Redis and S3/Allas as representations/adapters, not alternative schemas.
- Preserve provenance and human-review state.
- Keep multimodal fields optional.
- Add migrations for persisted schema changes.
- Keep legacy compatibility at adapter boundaries rather than making legacy columns canonical.

## Privacy

Never commit runtime research datasets, operational/private settings, researcher review databases, real transcripts/OCR/frames, private target lists or machine-specific deployment state. Public-safe AI26 methodology and source-family examples are allowed when they contain no credentials, private endpoints, non-public lists or row-level research data.

## Validation

Top-level CI validates meta-repository integrity. Full unit/integration, runtime-path and storage round-trip tests belong to the implementation repositories. Agents should report cross-module inconsistencies explicitly and create implementation issues in the owning module rather than hiding them in umbrella documentation.

## TOMI-LOCKED

Anything marked `TOMI-LOCKED` is a human-controlled invariant.

Agents MUST NOT modify, refactor, rename, migrate, remove, reinterpret, or change the semantics of a TOMI-LOCKED element.

This includes indirect changes whose effect would alter a locked interface, data format, workflow, behavior, assumption, prompt, schema, configuration, or documented contract.

When an agent encounters `TOMI-LOCKED`:

1. Preserve the marked element exactly unless Tomi's current instruction explicitly authorizes changing that specific locked element.
2. Do not bypass the lock through dependent code, schemas, serializers, migrations, tests, prompts, documentation, interfaces, configuration, or compatibility layers.
3. Do not remove the `TOMI-LOCKED` marker during cleanup, refactoring, migration, modernization, or documentation work.
4. Broad instructions such as "refactor", "modernize", "fix everything", "make CI green", "update the pipeline", or similar do NOT override a lock.
5. If a requested task conflicts with a locked element, preserve the lock, complete any non-conflicting work that is safe to do, and clearly report the conflict.
6. If Tomi explicitly authorizes a change to a specific locked element, that element may be changed, but the `TOMI-LOCKED` marker remains unless Tomi explicitly asks to remove the lock itself.

Only explicit authorization from Tomi for the specific locked element overrides the lock.

Marker examples:

```python
# TOMI-LOCKED
# Do not modify without explicit approval from Tomi.
```

```markdown
<!-- TOMI-LOCKED -->
```

```yaml
# TOMI-LOCKED
```

The marker is intentionally grep-friendly:

```bash
grep -R "TOMI-LOCKED" .
```

