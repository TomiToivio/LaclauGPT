# Migration to project/paper meta-repository

This migration implements GitHub issue #1 and ends the period where `LaclauGPT` duplicated the implementation tree from `LaclauGPT-Discourse-Analysis`.

## Destination verification

Before removing duplicate implementation code, the three destination repositories were checked on their current `main` branches:

- **LaclauGPT-Data-Collection** contains a packaged collection module with platform collectors, normalization, storage adapters, privacy/publication docs, tests and CI.
- **LaclauGPT-Data-Analysis** contains the standalone analysis package with backend-neutral contracts; spaCy, SentenceTransformers, scikit-learn, BERTopic, gensim, Transformers and statsmodels backends; local CSV/SQLite/filesystem defaults; optional MongoDB/Redis/S3 adapters; tests and CI.
- **LaclauGPT-Data-Visualization** contains the standalone visualization package with data/runtime/storage layers, Streamlit-facing application code, privacy/configuration docs, tests and CI.

The dedicated repositories are therefore the implementation sources of truth. Stale duplicate code in the meta-repository is removed rather than copied back into those newer package architectures.

## Ownership inventory

### Removed from the top-level repository as implementation duplicates

Collection-owned material included `collector/`, collection/runtime pieces under `ai26_runtime/`, `minet_adapter/`, collection-specific config/run files and codebook/collection source trees.

Analysis-owned material included `laclaugpt/`, `laclaugpt_model/`, `laclaugpt_memory/`, `laclaugpt_primitives/`, `laclaugpt_interchange/`, analysis adapters, `pipeline.py`, `llm.py`, `memory.py`, prompts, run configuration, processor/seed scripts and the monolithic implementation test suite.

Visualization-owned material and dashboard/runtime documentation is no longer maintained as duplicate top-level implementation material. Visualization implementation lives in `LaclauGPT-Data-Visualization`.

The former root `pyproject.toml` was removed because this repository no longer publishes or owns a Python implementation package.

### Kept here intentionally

- `paper/`
- `THEORY.md`
- scientific and project-level documentation under `docs/`
- project history, methodology, interoperability, validation, publication/privacy and architecture material that applies across modules
- the project license and top-level contribution/agent policy

Some historical documentation remains for research provenance even when it refers to earlier implementation stages. It is not an implementation source of truth.

## Code-specific documentation cleanup

Module-specific operational docs are removed from the meta-repo when the dedicated module already carries the relevant maintained documentation. Cross-cutting methodology and scientific design docs remain because they explain the research framework rather than a single Python package.

## New structure

The three module repositories are pinned as Git submodules under `modules/`:

- `modules/data-collection`
- `modules/data-analysis`
- `modules/data-visualization`

The top-level README now documents both recursive full-system installation and standalone module installation.

## Configuration policy

All three modules should remain local-first and independently useful. CSV, SQLite and local filesystem operation are first-class; MongoDB, Redis and S3-compatible storage are optional distributed backends. Secrets, private data and machine-specific configuration remain outside public Git history.

## Follow-up rule

Future implementation changes belong in the owning module repository. This meta-repository should change a submodule pin rather than copy module source code into the root tree.
