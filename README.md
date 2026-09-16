# LaclauGPT

[![Meta-repo checks](https://github.com/TomiToivio/LaclauGPT/actions/workflows/ci.yml/badge.svg)](https://github.com/TomiToivio/LaclauGPT/actions/workflows/ci.yml)

**LaclauGPT** is an open social-science research framework for **LLM-assisted computational discourse analysis** of large textual and multimodal corpora. It combines computational methods with interpretive political research while keeping model outputs traceable to source evidence, uncertainty, provenance and human review.

## Start here: project map

**This repository is the LaclauGPT meta-repository and the main entry point to the project.** It contains the scientific paper, theory, project-wide architecture, canonical data contract, interoperability rules and full-system documentation. The executable pipeline is split into three focused repositories, included here under `modules/` as Git submodules:

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

If you arrived here looking for the **paper or theory**, stay in this repository. If you want to **run or develop one pipeline stage**, follow the corresponding module above. If you want the **complete system**, clone this repository with its submodules.

The current flagship research programme is **[LaclauGPT: Ideological contestation over AI](paper/PAPER.md)**. The project's canonical theoretical and methodological contract is **[THEORY.md](THEORY.md)**.

The framework is developed around Ernesto Laclau and Chantal Mouffe's discourse theory and Emilia Palonen's work on populism, polarisation and hegemonic dynamics, with project-specific extensions such as Critical AI Studies and sociotechnical imaginaries. The AI/AGI study is the main development case, but LaclauGPT is deliberately a **general research framework rather than a single-purpose AI ideology classifier**. The same architecture can support election research, populism, grievance politics, social-media research and other comparative discourse-analysis projects.

In short:

- **Current research focus:** ideological contestation over AI and the methodology developed in the scientific paper.
- **General software goal:** reusable LLM-assisted computational discourse analysis rather than a hard-wired political classifier.
- **Theoretical core:** Laclau and Mouffe, with Palonen's Formula of Populism and project-specific theoretical extensions.
- **Methodological principle:** models propose interpretations; evidence, uncertainty, provenance and human review remain visible.
- **Research-use boundary:** LaclauGPT is intended for **academic research purposes only**. It is not an autonomous decision-maker, and its outputs must not substitute for accountable human scholarly judgement.
- **Data principle:** open code and methods, while restricted research corpora, credentials and identifiable row-level research data remain outside public repositories.

> [!WARNING]
> **Human-in-the-loop academic research only.** LaclauGPT's machine-generated summaries, classifications, discourse-theoretical codes, populism analyses, signifier roles, ideological formations, affects and other interpretations are **preliminary analysis to be verified by a human researcher**. They must not be treated as final research findings, ground truth or autonomous scholarly judgement. Human verification of source evidence and interpretation is required before results are used, reported, published or cited as research conclusions. LaclauGPT is designed for academic research, not autonomous operational, administrative, intelligence, moderation, profiling or policy decisions about people or groups.

## Research philosophy: human-in-the-loop as an assemblage

LaclauGPT uses a deliberately assemblage-based working philosophy of AI:

> **AI = HUMAN + LLM + LANGUAGE + INTERNET**

This is a methodological and philosophical framing, not a settled empirical claim about machine consciousness.

- **HUMAN — interpretation and accountable agency.** The researcher chooses questions, defines concepts and codebooks, evaluates evidence, resolves ambiguity, rejects model output and remains responsible for conclusions.
- **LLM — learned model plus agentic machinery.** Models may contribute structured proposals, retrieval, comparison, tool use and iterative analysis, but their outputs remain fallible and provisional.
- **LANGUAGE — communication protocol and cognitive medium.** Language couples the researcher, model, sources and theoretical concepts. LaclauGPT also takes seriously the working hypothesis that linguistic structure helps constitute the concepts, distinctions and inferential relations through which intelligent behaviour becomes possible.
- **INTERNET — infrastructure and epistemic environment.** Networks, servers, software, model repositories, databases, APIs and research corpora form part of the practical research system. Retrieved information remains evidence to evaluate, not automatically trusted truth.

Accordingly, **human-in-the-loop is not merely a final approval button attached to an otherwise autonomous pipeline**. The human researcher is constitutive of the research process throughout. LaclauGPT aims to extend researchers' capacity to inspect large corpora, generate provisional interpretations and compare discursive patterns while preserving source evidence, uncertainty, provenance and scholarly responsibility.

## Theoretical and methodological orientation

LaclauGPT treats political meaning as **relational, contested and only partially fixed**. Its purpose is not merely to detect topics, sentiment or frequently occurring words, but to investigate how meanings, identities, demands, signifiers and political frontiers are articulated in relation to one another.

The framework can propose evidence for concepts such as articulations, nodal points, floating and empty signifiers, equivalential and differential relations, collective subjects, antagonistic frontiers, affective investments, ideological formations, myths, imaginaries and hegemonic dynamics. These are **theoretical roles supported by evidence**, not labels that should be inferred mechanically from keywords or frequency.

Key methodological cautions include:

- frequency is not hegemony;
- semantic similarity is not equivalence;
- negative sentiment is not antagonism;
- polysemy or vagueness is not empty signification;
- mentioning "the people" is not automatically populism;
- document-level evidence does not by itself establish a corpus-level ideological formation.

The LLM therefore acts as a structured analytical assistant. It may propose interpretations, but researchers must be able to inspect the source passage, reject or revise a coding, compare alternative readings, mark uncertainty and validate corpus-level claims. **Abstention and empty outputs are legitimate results when evidence is insufficient.**

For the full conceptual contract, see **[THEORY.md](THEORY.md)**. For the current research application, see **[paper/PAPER.md](paper/PAPER.md)**.

## This repository

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

The scientific paper lives at [`paper/PAPER.md`](paper/PAPER.md). [`THEORY.md`](THEORY.md) is the canonical high-level theory and methodology source. This repository follows the current paper/theory state previously maintained in `LaclauGPT-Discourse-Analysis`, while implementation ownership has moved to the dedicated modules.

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
