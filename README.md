# LaclauGPT

[![Meta-repo checks](https://github.com/TomiToivio/LaclauGPT/actions/workflows/ci.yml/badge.svg)](https://github.com/TomiToivio/LaclauGPT/actions/workflows/ci.yml)

LaclauGPT is a social-science research framework for LLM-assisted computational discourse analysis, developed around Laclau/Mouffe/Palonen-inspired analysis while keeping model outputs auditable, provenance-aware and human-reviewable.

This repository is the **project and scientific-paper meta-repository**. It is the front door to the project, not a fourth implementation codebase. The scientific paper, theory, project architecture, interoperability rules, canonical cross-module data contract and full-system installation instructions live here. Executable implementation code lives in three independently installable Git submodules.

## Core modules

| Module | Responsibility | Repository |
| --- | --- | --- |
| Data Collection | acquisition, capture, normalization and collection-side storage adapters | [LaclauGPT-Data-Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection) |
| Data Analysis | NLP, embeddings, topic modelling, LLM-assisted analysis, statistics and analysis contracts | [LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) |
| Data Visualization | dashboards, plots, maps, graph/network views and research-facing visual exploration | [LaclauGPT-Data-Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization) |

They are checked out under `modules/` as Git submodules. Each module owns its Python package, tests, implementation-specific configuration and developer documentation.

## Canonical data contract

All three modules share one logical record contract defined in [`docs/CANONICAL_DATA_CONTRACT.md`](docs/CANONICAL_DATA_CONTRACT.md).

The governing rule is:

> **One phenomenon, one record contract, many storage adapters.**

`source_url` (or a stable URI-like equivalent when no normal URL exists) is the source identity anchor. CSV/Pandas, SQLite, MongoDB, JSONL, Parquet, Redis-backed workflows and S3/Allas references are storage or transport choices. They must not create different meanings or competing record schemas.

The canonical contract reconciles:

- source/ingestion concepts from `CyborgAnthropology`;
- optional legacy EP24/multimodal fields such as transcripts, OCR and frame evidence;
- current LaclauGPT analysis fields such as provenance, entities, topics, formations, signifiers, relations, uncertainty and human review.

Text-only records remain first-class records. Multimodal fields are optional.

Implementation work is tracked in the module repositories:

- [Data Collection canonical-schema issue](https://github.com/TomiToivio/LaclauGPT-Data-Collection/issues/3)
- [Data Analysis canonical-schema issue](https://github.com/TomiToivio/LaclauGPT-Data-Analysis/issues/4)
- [Data Visualization canonical-schema issue](https://github.com/TomiToivio/LaclauGPT-Data-Visualization/issues/3)

## Install the complete system

```bash
git clone --recurse-submodules https://github.com/TomiToivio/LaclauGPT.git
cd LaclauGPT
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e modules/data-collection
pip install -e modules/data-analysis
pip install -e modules/data-visualization
```

For an existing clone:

```bash
git submodule update --init --recursive
```

See [`docs/installation/FULL_SYSTEM.md`](docs/installation/FULL_SYSTEM.md) for profiles and configuration.

## Install one module only

The modules remain standalone. Clone and install only what you need, for example:

```bash
git clone https://github.com/TomiToivio/LaclauGPT-Data-Analysis.git
cd LaclauGPT-Data-Analysis
python -m pip install -e .
```

The same pattern applies to Data Collection and Data Visualization. No module should require a checkout of this meta-repository merely to work.

## Configuration model

The project is **local-first**. A laptop workflow should work with CSV/SQLite/local files and in-memory/local caches where applicable. Distributed deployments may opt into MongoDB, Redis and S3-compatible object storage such as CSC Allas.

Secrets and machine-specific values belong in environment variables, ignored local config or a secret manager. Never commit research datasets, credentials, private endpoints, cookies, browser profiles, private study codebooks, generated outputs or local SQLite research databases to public repositories.

See [`docs/architecture/MODULAR_ARCHITECTURE.md`](docs/architecture/MODULAR_ARCHITECTURE.md), [`docs/CANONICAL_DATA_CONTRACT.md`](docs/CANONICAL_DATA_CONTRACT.md) and [`docs/INTEROPERABILITY_SPEC.md`](docs/INTEROPERABILITY_SPEC.md).

## Scientific paper and theory

The scientific paper lives under [`paper/`](paper/). [`THEORY.md`](THEORY.md) is the high-level theory source. This repository follows the current paper/theory state previously maintained in `LaclauGPT-Discourse-Analysis`, while implementation ownership has moved to the dedicated modules.

LaclauGPT is human-in-the-loop academic research software. Automated outputs are preliminary research material and must be verified by a human researcher before they are treated as substantive findings.

## Where changes belong

- Change collectors, ingestion or normalization code in **LaclauGPT-Data-Collection**.
- Change NLP/LLM/statistical analysis code in **LaclauGPT-Data-Analysis**.
- Change dashboards and visualization code in **LaclauGPT-Data-Visualization**.
- Change the paper, theory, cross-module architecture, interoperability, canonical data contract or project-level documentation here.

Do not reintroduce duplicate implementation code into this repository.

## Repository layout

```text
LaclauGPT/
├── README.md
├── THEORY.md
├── paper/
├── docs/
├── modules/
│   ├── data-collection/       # Git submodule
│   ├── data-analysis/         # Git submodule
│   └── data-visualization/    # Git submodule
└── .gitmodules
```

## Optional / experimental ecosystem

Research assistants, agent tooling, simulation laboratories and other experiments remain optional projects. They must not become hidden dependencies of the three core modules or of the scientific paper repository.

See [`docs/MIGRATION_TO_META_REPO.md`](docs/MIGRATION_TO_META_REPO.md) for the migration record and ownership decisions.
