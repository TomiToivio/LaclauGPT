---
layout: default
title: Project
description: The current four-repository LaclauGPT architecture.
permalink: /project/
---

# Project

LaclauGPT has been under development by [Tomi Toivio](https://github.com/TomiToivio) since **2023**. Contact: [tomi.toivio@helsinki.fi](mailto:tomi.toivio@helsinki.fi).

It was originally created for the **EP24 research project** in connection with [HEPP](https://www.helsinki.fi/en/researchgroups/emotions-populism-and-polarisation) and [HSSH](https://www.helsinki.fi/en/helsinki-institute-social-sciences-and-humanities). The current version is guided primarily by the **AI26 research project** and is also used to support other research projects.

LaclauGPT is organized as **four active repositories**. The main repository is the project and scientific-paper hub; the three peer repositories implement the executable research pipeline.

| Repository | Status | Responsibility |
| --- | --- | --- |
| [LaclauGPT](https://github.com/TomiToivio/LaclauGPT) | Active | Project hub, scientific paper, theory, architecture, shared contracts, roadmap, and complete-system documentation |
| [LaclauGPT Data Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection) | Active | Acquisition, capture, normalization, provenance, scheduling, and storage adapters |
| [LaclauGPT Data Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) | Active | NLP, embeddings, LLM-assisted discourse analysis, statistics, uncertainty, and evidence-linked analytical proposals |
| [LaclauGPT Data Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization) | Active | Dashboards, timelines, maps, graphs, corpus exploration, and human researcher review |

## Architecture

```text
Data Collection → Data Analysis → Data Visualization
                       ↑
                 LaclauGPT hub
          theory · paper · contracts
```

The meta-repository is the canonical front door. It defines the scientific and interoperability contracts shared by the implementation repositories.

## Start points

- [Scientific paper](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md)
- [Theory and methodology](https://github.com/TomiToivio/LaclauGPT/blob/main/THEORY.md)
- [Roadmap](https://github.com/TomiToivio/LaclauGPT/blob/main/docs/ROADMAP.md)
- [Canonical data contract](https://github.com/TomiToivio/LaclauGPT/blob/main/docs/CANONICAL_DATA_CONTRACT.md)
- [Plugin platform architecture](https://github.com/TomiToivio/LaclauGPT/blob/main/docs/architecture/PLUGIN_PLATFORM_ARCHITECTURE.md)
