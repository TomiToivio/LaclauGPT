---
layout: default
title: LaclauGPT
description: Open research framework for LLM-assisted computational discourse analysis.
---

# LaclauGPT

**LLM-assisted computational discourse analysis for social and political research.**

LaclauGPT is an open social-science research framework for studying large textual and multimodal corpora with computational methods and LLM assistance. It keeps interpretation traceable to source evidence, uncertainty, provenance, and human researcher review.

## Research status

> **Draft research plan.** The current Phase 1 paper is a working research-plan manuscript. It has not been formally published or peer reviewed, and its arguments, methods, scope, and wording may change as the research develops.

## About and authorship

LaclauGPT has been under development by [Tomi Toivio](https://github.com/TomiToivio) since **2023**.

Contact: [tomi.toivio@helsinki.fi](mailto:tomi.toivio@helsinki.fi) · [GitHub profile](https://github.com/TomiToivio)

The project was originally created for the **EP24 research project** in connection with the [Helsinki Hub on Emotions, Populism and Polarisation (HEPP)](https://www.helsinki.fi/en/researchgroups/emotions-populism-and-polarisation) and the [Helsinki Institute for Social Sciences and Humanities (HSSH)](https://www.helsinki.fi/en/helsinki-institute-social-sciences-and-humanities). The current version is guided primarily by the **AI26 research project**, while also supporting other research projects and methodological development.

## Project background and funding

LaclauGPT grew out of research-software work at the **[Helsinki Hub on Emotions, Populism and Polarisation (HEPP)](https://www.helsinki.fi/en/researchgroups/emotions-populism-and-polarisation), University of Helsinki**, and the **2024 European Parliament election (EP24)** research programme. The original pipeline collected and analysed multimodal TikTok and Instagram material across multiple European countries. The current modular framework generalises that work into reusable collection, analysis and visualization components.

The software has been developed in connection with **CO3**, **ENDURE** and **PLEDGE**, supported by the European Union and the Research Council of Finland / Academy of Finland. Click a project logo to visit its official project page.

<p class="project-logos" align="center">
  <a href="https://www.co3socialcontract.eu/" title="CO3"><img src="https://www.helsinki.fi/assets/drupal/styles/16_10_fallback/s3/media-image/co3_rgb%20%281%29.jpg.jpeg?itok=2G8xjx4J" height="100" alt="CO3 project logo"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.endure-project.org/" title="ENDURE"><img src="https://www.endure-project.org/favicon.ico" height="76" alt="ENDURE project logo"></a>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.pledgeproject.eu/" title="PLEDGE"><img src="https://cdn.myportfolio.com/80780752-1793-414b-936a-f0cd10a2ac7d/57c00d24-bb6a-4af2-a001-c65a765651f9_rw_1920.png?h=41199a43847532a5a8800551fe811ed5" height="100" alt="PLEDGE project logo"></a>
</p>

**[CO3](https://www.co3socialcontract.eu/)** studies resilient social contracts and is funded by Horizon Europe under grant agreement **101132631**. **[ENDURE](https://www.endure-project.org/)** studied inequalities, community resilience and post-pandemic governance through the Trans-Atlantic Platform Recovery, Renewal and Resilience programme, with Finnish participation supported by the Academy of Finland / Research Council of Finland. **[PLEDGE](https://www.pledgeproject.eu/)** studies the emotional dynamics of political grievances and democratic governance and is funded by Horizon Europe under grant agreement **101132560**.

## Active project

The current LaclauGPT architecture consists of **four active repositories**:

| Repository | Role |
| --- | --- |
| [LaclauGPT](https://github.com/TomiToivio/LaclauGPT) | **Project hub:** scientific paper, theory, architecture, shared contracts, roadmap, and complete-system documentation |
| [LaclauGPT Data Collection](https://github.com/TomiToivio/LaclauGPT-Data-Collection) | **Collect:** acquisition, capture, normalization, provenance, scheduling, and storage adapters |
| [LaclauGPT Data Analysis](https://github.com/TomiToivio/LaclauGPT-Data-Analysis) | **Analyze:** NLP, embeddings, LLM-assisted discourse analysis, statistics, uncertainty, and evidence-linked analytical proposals |
| [LaclauGPT Data Visualization](https://github.com/TomiToivio/LaclauGPT-Data-Visualization) | **Visualize and review:** dashboards, timelines, maps, graphs, corpus exploration, and human researcher review |

The research pipeline is:

```text
Data Collection → Data Analysis → Data Visualization
                       ↑
                 LaclauGPT hub
          theory · paper · contracts
```

## Research

The current flagship research programme is **LaclauGPT: Ideological contestation over AI**. The framework is grounded in discourse theory associated with Ernesto Laclau and Chantal Mouffe and is designed for human-in-the-loop computational social-science research.

- [Scientific paper]({{ '/paper/PHASE_1_PAPER.html' | relative_url }})
- [Theory and methodology]({{ '/THEORY.html' | relative_url }})
- [Roadmap](ROADMAP.md)
- [Canonical data contract](CANONICAL_DATA_CONTRACT.md)
- [Plugin platform architecture](architecture/PLUGIN_PLATFORM_ARCHITECTURE.md)

## Historical research archive

Two earlier repositories are preserved as **historical research artifacts**. They document the lineage of LaclauGPT but are **not part of the current software architecture**.

| Repository | Historical role |
| --- | --- |
| [LaclauGPT Multimodal Analysis](https://github.com/TomiToivio/LaclauGPT-Multimodal-Analysis) | Legacy EP2024 multimodal analysis pipeline and research documentation |
| [LaclauGPT TikTok Scraper](https://github.com/TomiToivio/LaclauGPT-TikTok-Scraper) | Legacy EP2024 TikTok collection tooling and research documentation |

For current development, start with the four repositories in **Active project** above.

## Research-use boundary

> **Human-in-the-loop academic research only.** Machine-generated interpretations are preliminary analytical proposals. Source evidence and interpretations must be verified by a human researcher before they are reported or cited as research conclusions.

## Source code

All active public development is organized under the [LaclauGPT GitHub project](https://github.com/TomiToivio/LaclauGPT).
