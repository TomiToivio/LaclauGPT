# LaclauGPT research, methodology and technology roadmap

LaclauGPT is developed as a research framework in a continuous loop between **scientific writing**, **methodological development**, **technical implementation**, and **real research use**.

The current flagship programme, **AI26: Ideological contestation over AI**, is the main reference case used to guide LaclauGPT development. AI26 is not merely a demonstration dataset or a final validation exercise. It is used continuously to test whether the theory, methodology, data contracts, collection system, analysis methods, visualizations and human-researcher workflows work together in practice.

At the same time, LaclauGPT is a general research framework and is continuously used for other research projects. Features developed through AI26 should therefore remain reusable across other studies rather than becoming hard-coded AI26-specific behavior.

The roadmap is iterative rather than strictly linear. New empirical findings can require methodological or technical changes, and new methods or technologies can require revisions to the paper. The four phases describe increasing research maturity rather than rigid software releases.

## Guiding development cycle

```text
Paper / theory
     ↓
Methodology
     ↓
LaclauGPT implementation
     ↓
AI26 + other research projects
     ↓
Human interpretation and evaluation
     ↓
Revisions to theory, methods and technology
     ↺
```

Three tracks evolve together throughout all phases:

1. **Paper(s) and theory** — the scientific argument, research questions, theoretical framework, methodological justification and empirical findings.
2. **Methodology** — operationalisation of discourse theory, computational and LLM-assisted methods, validation, uncertainty, provenance and human-in-the-loop interpretation.
3. **Technology** — the real-time Collection → Analysis → Visualization pipeline, shared contracts, deployment profiles and research-facing interfaces.

## Phase 1 — Research plan and working pipeline

### Paper(s) and theory

The first version of the paper or papers specifies the research programme:

- core research questions and scope;
- basic theoretical framework;
- basic methodology;
- role of LaclauGPT as an LLM-assisted computational discourse-analysis framework;
- AI26 as the principal development and empirical reference case;
- human-in-the-loop requirements and the distinction between computational proposals and final scholarly interpretation.

The purpose of this version is to establish a coherent research plan rather than to present final empirical findings.

### Methodology

Phase 1 establishes the minimum reproducible methodological framework required to run the study:

- corpus and source design;
- canonical data and provenance model;
- theory-sensitive coding concepts;
- basic NLP and LLM-assisted discourse-analysis methods;
- uncertainty and abstention rules;
- traceability from interpretation back to evidence;
- researcher review and manual discourse-analysis workflow;
- initial validation strategy.

Methods should remain modular so that additional theories or analytical techniques can be added later without invalidating the basic pipeline.

### Technology

The technical objective is to establish an end-to-end **real-time or near-real-time AI26 pipeline**:

```text
Data Collection → Data Analysis → Data Visualization → Human Review
```

The system should be capable of continuously collecting permitted AI26 sources, transforming them into canonical records, running analysis, and making results available for visualization and researcher inspection.

Phase 1 therefore prioritizes a working research instrument over feature completeness.

### Phase 1 outcome

A first publishable research-plan/methodology paper and a functioning AI26 pipeline that can already be used to develop and test LaclauGPT against real research material.

## Phase 2 — Expanded framework and operational AI26 observatory

### Paper(s) and theory

The second version of the paper or papers may:

- add additional theories where they improve the research design;
- provide more detailed descriptions of existing theoretical concepts;
- refine research questions and conceptual distinctions;
- expand the methodological justification;
- document lessons learned from running AI26 and other research projects.

The theoretical framework should grow only when additions improve explanatory or analytical value. The roadmap does not require theoretical expansion for its own sake.

### Methodology

Phase 2 may add or refine methods such as:

- improved Laclau/Mouffe/Palonen operationalisations;
- richer contextual and temporal analysis;
- embeddings, semantic relations and retrieval/context-memory methods;
- multimodal analysis;
- network or relational methods where research questions justify them;
- additional statistical, qualitative or mixed-method validation;
- improved intercoder/human-model comparison procedures;
- study-specific extensions implemented as reusable plugins or profiles.

The methodology documentation should become sufficiently detailed that another researcher can understand what computational outputs mean, what they do not mean, and how they enter the final interpretive analysis.

### Technology

By Phase 2 the **AI26 real-time Collection → Analysis → Visualization pipeline is running operationally**.

Technical work shifts from merely making the pipeline function toward reliability and research quality:

- stable cross-module contracts;
- continuous ingestion and scheduled analysis;
- monitoring and failure recovery;
- provenance and reproducibility;
- richer dashboards and exploration interfaces;
- researcher feedback loops;
- performance profiles for laptop, institutional servers and HPC/cloud environments where relevant;
- reusable configuration for other research projects.

AI26 acts as the primary live integration test, while other projects test whether the framework remains general.

### Phase 2 outcome

A more mature theoretical and methodological publication and an operational AI26 research observatory continuously producing inspectable research material.

## Phase 3 — Preliminary empirical results

### Paper(s) and theory

The third version of the paper or papers may incorporate **preliminary AI26 results** produced through the running data-collection, analysis and visualization pipeline.

Computational results are not treated as autonomous findings. They are inputs into a human-led research process.

The paper should clearly distinguish:

- collected evidence;
- computational measurements and model outputs;
- LLM-assisted analytical proposals;
- researcher coding and interpretation;
- final claims supported by human discourse analysis.

### Methodology

Phase 3 emphasizes empirical validation and reflexive methodology:

- evaluate which automated and LLM-assisted methods are useful for discourse research;
- document failure modes, uncertainty and disagreements;
- compare computational suggestions with human interpretation;
- refine codebooks, prompts, models and operational definitions where evidence warrants it;
- preserve an auditable trail between source material, machine-assisted analysis and researcher conclusions.

The human researcher remains responsible for the final discourse analysis and scholarly claims.

### Technology

The pipeline now supports sustained empirical research rather than primarily framework development:

- longitudinal AI26 collection;
- reproducible analysis runs;
- comparison across time, arenas, actors and corpora;
- interactive inspection of evidence behind analytical outputs;
- export of research-ready tables, figures, corpora subsets and provenance information;
- versioning of methods and models so preliminary findings can be reproduced.

### Phase 3 outcome

One or more papers presenting preliminary AI26 findings together with an empirically tested account of the LaclauGPT methodology and its limitations.

## Phase 4 — Final AI26 results

### Paper(s) and theory

The fourth version of the paper or papers may contain the **final results of the AI26 project**.

Depending on the publication strategy, this may be a single final paper, a sequence of thematic papers, or a combination of methodological and substantive publications.

The final publications should integrate:

- the mature theoretical framework;
- the validated methodological framework;
- the documented role of computational and LLM assistance;
- the complete relevant AI26 evidence base;
- final human-led discourse analysis;
- limitations, negative results and unresolved ambiguities;
- implications for future research using LaclauGPT.

### Methodology

The methodology is consolidated into a stable, documented research protocol. Experimental methods that proved useful can become supported components; methods that proved unreliable should remain experimental or be removed from the recommended workflow.

The final methodological account should make explicit which conclusions depend on human interpretation, which are computational measurements, and how uncertainty was handled.

### Technology

The technical system should support reproducibility and continued reuse after AI26:

- stable archival/export workflows;
- reproducible analysis configurations;
- preservation of methodological and model provenance;
- documented deployment and maintenance procedures;
- reusable study templates for future projects;
- separation of general LaclauGPT capabilities from AI26-specific study configuration.

AI26 may conclude as a research project, but the pipeline and methodological framework continue as infrastructure for later studies.

### Phase 4 outcome

Final AI26 research publications plus a mature LaclauGPT framework that has been developed, stress-tested and documented through continuous real-world research use.

## Cross-phase principles

The following principles apply throughout all four phases:

- **AI26 guides development continuously.** It is the main live reference case, not a one-time benchmark performed after development.
- **Other research projects remain first-class users.** AI26-driven features must be designed so they can generalize to other corpora and research questions.
- **Human-in-the-loop is non-negotiable.** LLM and computational outputs are research assistance, not autonomous scholarly judgement.
- **Final discourse analysis is human.** LaclauGPT can retrieve, structure, compare, measure, suggest and visualize; the researcher remains responsible for interpretation and published claims.
- **Theory, methodology and technology co-evolve.** None of the three tracks is treated as merely an implementation detail of another.
- **Reproducibility and provenance grow with the project.** Every phase should improve the ability to trace findings back to sources, methods, model versions and researcher decisions.
- **Modularity over accumulation.** New theories, methods and technologies are added when they answer research needs, not simply because they are available.
- **Public framework, protected research material.** General methods, contracts and reusable engineering belong in the public framework where appropriate; restricted datasets, credentials, unpublished annotations and sensitive operational details remain outside the public repository.

## Relationship to the repository architecture

This meta-repository owns the roadmap, paper, theory, shared research contracts and project-level methodology.

Implementation remains distributed across the three core repositories:

- **LaclauGPT-Data-Collection** — continuous source acquisition, normalization and provenance;
- **LaclauGPT-Data-Analysis** — NLP, LLM-assisted analysis, computational methods, uncertainty and evidence-linked outputs;
- **LaclauGPT-Data-Visualization** — dashboards, temporal views, maps, graphs, corpus exploration and human review.

AI26 supplies the main end-to-end development case across all three modules, while reusable interfaces and contracts ensure that LaclauGPT remains usable for other research programmes.
