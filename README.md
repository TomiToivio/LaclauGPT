# LaclauGPT

[![Meta-repo checks](https://github.com/TomiToivio/LaclauGPT/actions/workflows/ci.yml/badge.svg)](https://github.com/TomiToivio/LaclauGPT/actions/workflows/ci.yml)

**LaclauGPT** is an open social-science research framework for **LLM-assisted computational discourse analysis** of large textual and multimodal corpora. It combines computational methods with interpretive political research while keeping model outputs traceable to source evidence, uncertainty, provenance and human review.

## Start here: project map

**This repository is the LaclauGPT meta-repository and the main entry point to the project.** It contains the scientific paper, theory, project-wide architecture, canonical data contract, interoperability rules and full-system documentation. The executable pipeline is split into three focused peer repositories:

| Repository | Role |
| --- | --- |
| **[LaclauGPT](https://github.com/TomiToivio/LaclauGPT)** | **Meta-repo:** scientific paper, theory, architecture, shared contracts and complete-system documentation |
| **[LaclauGPT-Data-Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection)** | **Collect:** acquire/capture source material, normalize it, preserve raw data and provenance, and emit canonical records |
| **[LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis)** | **Analyze:** enrich canonical records with NLP, embeddings, LLM-assisted discourse analysis, statistics, uncertainty and evidence-linked analytical proposals |
| **[LaclauGPT-Data-Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization)** | **Visualize/review:** dashboards, timelines, maps, graphs, corpus exploration and human researcher review |

The normal research flow is:

```text
Data Collection  ->  Data Analysis  ->  Data Visualization
       \                 |                    /
        \________ shared canonical record ___/
                         |
              LaclauGPT meta-repo
       paper + theory + shared contracts
```

If you arrived here looking for the **paper or theory**, stay in this repository. If you want to **run or develop one pipeline stage**, use the corresponding peer repository above. If you want the **complete system**, keep the four repositories as siblings in one workspace.

The current flagship research programme is **[LaclauGPT: Ideological contestation over AI](paper/PAPER.md)**. The project's canonical theoretical and methodological contract is **[THEORY.md](THEORY.md)**.

The framework is developed around Ernesto Laclau and Chantal Mouffe's discourse theory and Emilia Palonen's work on populism, polarisation and hegemonic dynamics, with project-specific extensions such as Critical AI Studies and sociotechnical imaginaries. The AI/AGI study is the main development case, but LaclauGPT is deliberately a **general research framework rather than a single-purpose AI ideology classifier**.

> [!WARNING]
> **Human-in-the-loop academic research only.** LaclauGPT's machine-generated interpretations are preliminary analysis to be verified by a human researcher. They must not be treated as final research findings or autonomous scholarly judgement.

## This repository

This repository is the **project and scientific-paper meta-repository**. It is the front door to the project, not a fourth implementation codebase. The scientific paper, theory, project architecture, interoperability rules, canonical cross-module data contract and full-system installation instructions live here. Executable implementation code lives in three independently installable peer repositories.

## Core modules

| Module | Responsibility | Repository |
| --- | --- | --- |
| Data Collection | acquisition, capture, normalization and collection-side storage adapters | [LaclauGPT-Data-Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection) |
| Data Analysis | NLP, embeddings, topic modelling, LLM-assisted analysis, statistics and analysis contracts | [LaclauGPT-Data-Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) |
| Data Visualization | dashboards, plots, maps, graph/network views and research-facing visual exploration | [LaclauGPT-Data-Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization) |

Each module owns its Python package, tests, implementation-specific configuration and developer documentation.

## Plugin platform architecture

LaclauGPT uses a **“WordPress for computational social science”** metaphor: a small stable contract layer with optional collection, analysis, visualization and researcher-workflow plugins. This is a modularity model, not a decision to merge the three runtime modules.

The governing architecture is documented in [`docs/architecture/PLUGIN_PLATFORM_ARCHITECTURE.md`](docs/architecture/PLUGIN_PLATFORM_ARCHITECTURE.md). Collection, Analysis and Visualization remain independently deployable and communicate through versioned canonical contracts and explicit job/API boundaries.

## Canonical data contract

All three modules share one logical record contract defined in [`docs/CANONICAL_DATA_CONTRACT.md`](docs/CANONICAL_DATA_CONTRACT.md).

The governing rule is:

> **One phenomenon, one record contract, many storage adapters.**

`source_url` (or a stable URI-like equivalent when no normal URL exists) is the source identity anchor. CSV/Pandas, SQLite, MongoDB, JSONL, Parquet, Redis-backed workflows and S3/Allas references are storage or transport choices. They must not create different meanings or competing record schemas.

## Recommended workspace layout

```text
LaclauGPT-workspace/
├── LaclauGPT/
├── LaclauGPT-Data-Collection/
├── LaclauGPT-Data-Analysis/
└── LaclauGPT-Data-Visualization/
```

Clone the meta-repository first:

```bash
git clone https://github.com/TomiToivio/LaclauGPT.git
cd LaclauGPT
```

Then clone missing peer modules:

```bash
./scripts/bootstrap-modules.sh
```

Update the three module repositories with ordinary Git pulls:

```bash
./scripts/update-modules.sh
```

Create and activate a Python environment, then install all three modules in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U pip
./scripts/install-modules.sh
```

The helper scripts deliberately do not pin module commits, manage shared configuration, or switch branches. At this stage the modules are independent repositories updated with ordinary `git pull --ff-only`.

See [`docs/installation/FULL_SYSTEM.md`](docs/installation/FULL_SYSTEM.md) for the same workflow in more detail.

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

For restricted studies such as EP24 or Hungary26, follow [`docs/PUBLIC_PRIVATE_STUDY_ARCHITECTURE.md`](docs/PUBLIC_PRIVATE_STUDY_ARCHITECTURE.md): reusable engineering stays public, while study data, codebooks, researcher material, credentials, CSC identifiers/paths and unpublished outputs stay in the private runtime layer.

See [`docs/architecture/MODULAR_ARCHITECTURE.md`](docs/architecture/MODULAR_ARCHITECTURE.md), [`docs/architecture/PLUGIN_PLATFORM_ARCHITECTURE.md`](docs/architecture/PLUGIN_PLATFORM_ARCHITECTURE.md), [`docs/CANONICAL_DATA_CONTRACT.md`](docs/CANONICAL_DATA_CONTRACT.md) and [`docs/INTEROPERABILITY_SPEC.md`](docs/INTEROPERABILITY_SPEC.md).

## Scientific paper and theory

The scientific paper lives at [`paper/PAPER.md`](paper/PAPER.md). [`THEORY.md`](THEORY.md) is the canonical high-level theory and methodology source.

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
└── scripts/
    ├── bootstrap-modules.sh
    ├── update-modules.sh
    └── install-modules.sh
```

## Optional / experimental ecosystem

Research assistants, agent tooling, simulation laboratories and other experiments remain optional projects. They must not become hidden dependencies of the three core modules or of the scientific paper repository.

See [`docs/MIGRATION_TO_META_REPO.md`](docs/MIGRATION_TO_META_REPO.md) for the migration record and ownership decisions.