# AGENTS.md

## Scope

This repository is the LaclauGPT project / paper meta-repository. Keep it focused on scientific and project-level material, project architecture, interoperability, and git submodule coordination.

Implementation belongs in the owning modules:

- collection/acquisition/normalization -> `TomiToivio/LaclauGPT-Data-Collection`
- NLP/LLM/statistics/discourse analysis -> `TomiToivio/LaclauGPT-Data-Analysis`
- dashboards/plots/maps/network visualization -> `TomiToivio/LaclauGPT-Data-Visualization`

## Submodules

Canonical paths are `modules/data-collection`, `modules/data-analysis`, and `modules/data-visualization`. Update gitlinks deliberately; do not copy module source trees into this repository.

## Mandatory runtime data contract

Read `docs/RUNTIME_DATA.md`. Every module uses its repository-local `data/` directory as the private runtime root, and the entire `data/` tree stays outside Git.

Runtime logs, databases, local settings, CSV/JSONL files, study codebooks, source/target lists, downloads, media, transcripts, frames, exports, caches, temporary files, Ollama material, Whisper model caches and other generated artifacts belong under `data/`.

Do not use `.gitkeep` or tracked README files inside `data/`. Public templates, schemas, docs and synthetic test fixtures live outside `data/`.

### Same-machine pipeline

When modules run as sibling repositories on one machine:

1. Analysis may read canonical data directly from `LaclauGPT-Data-Collection/data/` through runtime configuration.
2. Visualization may read canonical analysis results directly from `LaclauGPT-Data-Analysis/data/` through runtime configuration.
3. Private data must not be copied into Git merely to connect modules.

### Distributed pipeline

Use MongoDB for records, Redis for coordination/cache/state, and S3-compatible object storage such as CSC Allas for files and large artifacts. CSV/JSONL export/import is the explicit manual fallback.

Storage topology must not change canonical record semantics.

## Canonical data contract

`docs/CANONICAL_DATA_CONTRACT.md` is the source of truth for semantics across Collection -> Analysis -> Visualization.

- Preserve stable source identity across modules and storage backends.
- Treat CSV/Pandas, SQLite, MongoDB, JSONL, Parquet, Redis and S3/Allas as representations/adapters, not alternative schemas.
- Preserve provenance and human-review state.
- Keep multimodal fields optional.
- Add migrations for persisted schema changes.
- Keep legacy compatibility at adapter boundaries rather than making legacy columns canonical.

## Privacy

Never commit runtime research datasets, operational settings, researcher review databases, real transcripts/OCR/frames, target lists or machine-specific deployment state. Public examples and schema fixtures must be synthetic.

## Validation

Top-level CI validates meta-repository integrity. Full unit/integration, runtime-path and storage round-trip tests belong to the implementation repositories.
