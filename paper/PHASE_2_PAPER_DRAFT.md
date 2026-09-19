# LaclauGPT Phase 2: Advanced theoretical and methodological framework

> **STATUS: PRELIMINARY CONTENT PLAN / WORKING DRAFT / NOT PUBLISHED**
>
> This document is an unpublished planning outline for a possible Phase 2 paper. It is **not a completed manuscript, not peer reviewed, and not a published research output**. Section order, terminology, theoretical synthesis, methods, and references are provisional.
>
> **Phase progression:** [Phase 1](PHASE_1_PAPER.md) · [Phase 2](PHASE_2_PAPER_DRAFT.md) · [Phase 3](PHASE_3_PAPER_DRAFT.md) · [Phase 4](PHASE_4_PAPER_DRAFT.md)
>
> **Relationship to Phase 1:** Phase 2 continues from Phase 1 rather than rewriting it. Phase 1 remains the primary statement of the existing LaclauGPT discourse-theoretical framework, AI26 research context, LLM-assisted workflow, research arenas, and initial validation principles. Phase 2 expands the architecture toward Discourse Network Analysis (DNA), Social Network Analysis (SNA), artificial communication, digital society, and interoperability with established Python/R social-data-science tools.
>
> **Empirical status:** Phase 2 does **not** require research results. AI26 may be used for motivating examples and future research questions, but illustrative examples must not be presented as findings.

## Working title

**LaclauGPT Phase 2: From Discourse to Discourse Networks and AI-Era Social Networks**

Alternative subtitle:

**A layered framework for political meaning, discourse coalitions, communication networks, and computational interoperability**

## Central purpose

Phase 2 should develop LaclauGPT from an LLM-assisted discourse-analysis method into a layered computational social-science framework connecting:

1. **Laclau Discourse Analysis:** how political meanings, identities, demands, frontiers, signifiers, and hegemonic projects are articulated;
2. **Discourse Network Analysis:** which actors articulate, support, reject, or contest which concepts/claims, and how discourse coalitions change over time;
3. **Social and Communication Network Analysis:** how actors, organizations, institutions, platforms, communication events, and AI-mediated relations are structurally connected.

The layers should be **interoperable but not theoretically collapsed into one another**.

A compact organizing sequence:

**meaning → statements/claims → discourse coalitions → communication networks → social systems**

The key methodological distinction is that a semantic relation, an actor–concept stance relation, and a social interaction tie are not the same kind of edge.

## Proposed contribution

Phase 2 should argue that poststructuralist discourse analysis, DNA, and SNA can be connected through a provenance-preserving relational data model while retaining the conceptual differences among:

- **articulation** in Laclau and Mouffe;
- **agreement/disagreement around claims or concepts** in DNA;
- **social or communication relations** in SNA.

The paper should present LaclauGPT as an **interoperable analytical framework**, not as a replacement for DNA, conventional SNA, qualitative interpretation, or classical NLP.

---

# Proposed paper outline

## 1. Introduction: from computational discourse analysis to layered relational analysis

Open where Phase 1 ends rather than restating it.

Phase 1 established the existing Laclaudian vocabulary and AI26 research design. Phase 2 asks what becomes possible when discourse-theoretical analysis is linked to established network approaches.

Introduce five methodological problems:

- interpretive discourse analysis is theoretically rich but difficult to scale;
- DNA formalizes actor–concept relations and discourse coalitions but necessarily simplifies discourse;
- conventional SNA formalizes social relations and network structure but often has a thinner theory of political meaning;
- LLMs expand extraction and interpretation capacity but introduce new problems of validation, provenance, opacity, bias, and reproducibility;
- AI26 adds a special complication: AI is both an **object of political discourse** and increasingly part of the **communication infrastructure** through which discourse is produced and circulated.

Main research-design question:

> How can LaclauGPT connect discourse interpretation, discourse networks, and social/communication networks without treating them as interchangeable representations?

### Do not duplicate Phase 1

Avoid repeating at length:

- the general explanation of Laclau/Mouffe;
- the basic AI26 ideological-formation taxonomy;
- the full sociotechnical-imaginaries literature review;
- the existing description of LLM Structuralism.

Refer to Phase 1 and move directly to the expanded framework.

---

## 2. A layered ontology of discourse and networks

This should be the main conceptual architecture of Phase 2.

### 2.1 Layer A: articulation / semantic graph

Possible nodes:

- signifiers;
- demands;
- subjects/identities;
- concepts;
- affective objects;
- sociotechnical imaginaries.

Possible typed edges:

- articulates;
- equates;
- differentiates;
- opposes;
- represents;
- excludes;
- constructs frontier with.

**Theoretical home:** Laclau, Mouffe, Palonen, AC/DT.

### 2.2 Layer B: discourse network

Primary structure:

**actor → statement/claim → concept → stance → time**

Possible derived graphs:

- actor–concept bipartite network;
- actor congruence network;
- actor conflict network;
- concept congruence network;
- discourse-coalition network;
- temporal discourse network.

**Theoretical/methodological home:** Philip Leifeld and Discourse Network Analysis.

### 2.3 Layer C: social and communication network

Possible nodes:

- persons;
- accounts;
- organizations;
- institutions;
- publications/media;
- platforms;
- bots;
- algorithmic systems;
- LLM/AI systems where analytically justified.

Possible typed edges:

- replies to;
- mentions;
- cites;
- follows;
- collaborates with;
- belongs to;
- funds;
- publishes;
- hyperlinks to;
- shares/reposts;
- co-participates with;
- communicates with;
- generates/assists/amplifies communication.

**Theoretical home:** SNA, relational sociology, network society, systems theory, artificial communication.

### 2.4 Layer D: social-system/context layer

Represent functionally differentiated communicative contexts such as:

- politics;
- economy;
- science;
- law;
- media;
- education;
- civil society/activism;
- technology development.

Treat these as **social-system contexts or subdomains**, not necessarily independent top-level graphs.

### Core rule

> Translation between analytical layers is allowed; reduction of one layer to another is not.

Examples:

- a LaclauGPT signifier is not automatically a DNA concept;
- a DNA agreement edge is not automatically a Laclaudian equivalence relation;
- a reply/follow tie is not automatically ideological agreement;
- community detection is not automatically the discovery of a political formation;
- semantic similarity is not automatically articulation.

---

## 3. Layer One: Laclau Discourse Analysis

### 3.1 Role in Phase 2

Do not reproduce Phase 1's theoretical exposition. Define what the existing layer contributes to the larger architecture:

**Layer One analyzes political meaning.**

Potential evidence-linked output objects:

- actor/speaker;
- document/passage/statement;
- signifier;
- demand;
- subject position;
- candidate nodal point;
- candidate floating/empty-signifier function;
- equivalence/difference relation;
- antagonistic frontier;
- articulation;
- affective relation;
- sociotechnical imaginary;
- uncertainty/confidence;
- human-review state.

### 3.2 From interpretation to typed relational data

Phase 2 should clarify that graph representation is a representation of an analytical observation, not an ontological claim that discourse “is” a graph.

Prefer representations such as:

**Actor A → articulates → relation(Signifier X, Signifier Y)**

with source passage and provenance, rather than storing an unexplained Signifier X ↔ Signifier Y edge.

### 3.3 Interface to DNA

Specify an explicit translation layer.

Only reviewed LaclauGPT observations that can reasonably be expressed as actor/claim/concept/stance statements should be exported to DNA.

The translation should be inspectable and reversible.

---

## 4. Layer Two: Discourse Network Analysis

### 4.1 DNA as the middle analytical layer

DNA is the natural bridge because it joins qualitative content analysis with formal network analysis.

Organizing distinction:

- **Laclau layer:** How is political meaning articulated?
- **DNA layer:** Who supports, rejects, or contests which claims/concepts?
- **SNA layer:** Through what social and communication structures are those positions produced and circulated?

### 4.2 DNA observation model

Minimum statement schema:

- document;
- passage;
- actor;
- organization/affiliation where relevant;
- concept or claim;
- agreement/disagreement or categorical stance;
- timestamp;
- source;
- coder/model;
- uncertainty;
- validation state.

### 4.3 Core analytical outputs

Plan sections on:

- actor–concept bipartite networks;
- congruence networks;
- conflict networks;
- discourse coalitions;
- polarization;
- brokerage;
- coalition switching;
- temporal windows;
- ideological scaling where justified.

### 4.4 Interoperability with Discourse Network Analyzer

Make compatibility with the Leifeld Lab **Discourse Network Analyzer (DNA)** and **rDNA** an explicit requirement.

Target:

**LaclauGPT → DNA**
- documents;
- actors;
- statements;
- concepts;
- stances;
- dates;
- variables/metadata.

**DNA/rDNA → LaclauGPT**
- manually coded statements;
- actor–concept matrices;
- network projections;
- coalition assignments;
- temporal windows;
- coder-reviewed benchmark data.

Aim for **round-trip interoperability**, not merely one-way export.

### 4.5 Manual, classical NLP, and LLM-assisted DNA

Compare three extraction strategies:

1. manually coded DNA;
2. classical NLP / supervised machine learning;
3. LLM-assisted extraction.

The preferred architecture should be hybrid and validation-oriented.

Possible tasks:

- NER/entity linking;
- actor normalization;
- claim/concept classification;
- stance detection;
- temporal normalization;
- evidence-span extraction.

Recent automated-DNA work should be used to discuss validation, aggregation, and whether lower-level extraction errors propagate into higher-level discourse-network structures.

---

## 5. Layer Three: Social and Communication Network Analysis for the AI era

This is the largest theoretical expansion beyond Phase 1.

The goal is **not** to replace classical SNA with a grand theory. The goal is to give network construction and interpretation a richer contemporary sociological basis.

### 5.1 Harrison White: relational identity, networks, stories, and social formations

Use White as the main relational-sociology bridge between SNA and discourse.

Key concepts:

- identities as relational achievements;
- control as search for footing;
- networks and stories;
- netdoms;
- switching;
- structural equivalence;
- embedding/decoupling;
- styles;
- institutions;
- rhetorics;
- regimes.

Phase 2 question:

> How can actor identity be modeled as context-dependent and relational rather than as a permanent attribute attached to a node?

Potential implications:

- actor identities can differ by arena/topic/time;
- network communities should not automatically be treated as fixed collective identities;
- stories/discourse should remain connected to ties;
- multiplex networks may represent switching among network domains.

### 5.2 Elena Esposito: artificial communication

Use Esposito as the main AI-era extension of the communication-network layer.

Key concepts:

- algorithms as communication partners;
- artificial communication;
- communication without human-style understanding;
- personalization;
- algorithmic memory;
- prediction;
- feedback;
- opacity.

Central distinction:

> Computational participation in communication does not imply human-equivalent agency.

Potential communicator roles:

- human;
- organization;
- institution;
- bot;
- recommender/ranking system;
- LLM;
- AI-assisted human;
- hybrid organizational/AI workflow.

AI26 relevance:

AI is both:

1. an object/signifier in political discourse; and
2. part of the machinery through which discourse may be generated, ranked, summarized, recommended, amplified, or answered.

### 5.3 Armin Nassehi: patterns and the digital society

Use Nassehi as the macro-level theory of digital observation and pattern formation.

Key concepts:

- reference problem of digitalization;
- pattern recognition;
- digital traces;
- data as observation;
- self-reference;
- cybernetic feedback;
- social complexity;
- functional differentiation;
- coding and programming.

Central methodological implication:

> Network patterns are constructed observations of digital traces, not transparent maps of society itself.

Use Nassehi to theorize:

- why platform traces are analytically powerful;
- why patterns can be socially stable without being causal explanations;
- how digital observations feed into further observations and decisions;
- why politics, economy, science, law, media, and other systems can be treated as differentiated communicative contexts.

### 5.4 Selective Luhmannian foundation

Use Luhmann selectively behind Esposito and Nassehi rather than importing the entire theory of autopoiesis.

Potential concepts:

- communication as the elementary operation of social systems;
- recursive communication;
- functional differentiation;
- system/environment distinction;
- observation and second-order observation;
- operational closure.

Avoid turning Luhmannian systems directly into graph communities or network clusters.

### 5.5 Castells as inherited network-society background

Castells remains important for:

- networks and flows;
- communication power;
- programming/switching networks;
- networked counter-power;
- information infrastructures.

However, Phase 2 should not be built around another full reconstruction of Castells. White, Esposito, and Nassehi provide the main new theoretical reading spine.

### 5.6 Working synthesis

A concise division of labor:

- **White:** relational identities, ties, stories, social formations;
- **Nassehi:** digital patterns, observation, complexity, differentiated society;
- **Esposito:** algorithmic/artificial communication;
- **Luhmann:** recursive communication and functional differentiation;
- **Castells:** inherited macro vocabulary of networks, flows, and communication power.

This should remain a **theoretical constellation**, not be presented as one unified grand theory.

---

## 6. Interoperability among the three analytical layers

### 6.1 Shared provenance-preserving data model

Proposed sequence:

**Corpus → Document → Passage → Statement → Actor/Communicator → Concept/Signifier/Claim → Relation/Stance/Interaction → Time → Analytical annotation → Human validation**

Every derived relation should retain:

- source document;
- evidence span;
- timestamp;
- source platform;
- actor-resolution information;
- analytical layer;
- tool/model/version;
- prompt/codebook/configuration;
- confidence/uncertainty;
- human-review state.

### 6.2 Typed edges

Avoid a universal `related_to` edge.

Example edge families:

**Discourse**
- articulates;
- equates;
- differentiates;
- opposes;
- represents.

**DNA**
- supports;
- rejects;
- endorses;
- contests.

**SNA/communication**
- replies_to;
- mentions;
- follows;
- cites;
- shares;
- collaborates_with;
- member_of;
- funds;
- publishes;
- generated_by;
- assisted_by;
- recommended_by.

### 6.3 Multilayer / multiplex representation

Possible layers:

- semantic/articulation graph;
- actor–concept discourse network;
- account/person interaction network;
- organization/institution network;
- platform/infrastructure network.

Possible future research questions:

- Do interaction communities correspond to discourse coalitions?
- Do network brokers introduce or translate articulations across arenas?
- Does discourse polarization precede or follow interaction segregation?
- How do articulations move between elite, parliamentary/policy, and grassroots arenas?
- How does AI-mediated communication change network centrality, visibility, or discourse circulation?

These belong to later empirical phases, not Phase 2 results.

---

## 7. Classical NLP and open-source interoperability

Phase 2 should explicitly reject an LLM-only methodology.

LLMs are one component of a larger social-data-science toolchain.

### 7.1 Python

Candidate integrations:

- **pandas / NumPy:** tabular interchange and preprocessing;
- **spaCy:** sentence segmentation, tokenization, NER, rule-based matching, dependency information;
- **scikit-learn:** transparent baselines, supervised classification, clustering, dimensionality reduction, calibration/evaluation;
- **NetworkX:** inspectable graph construction and network analysis;
- **python-igraph:** faster graph operations and cross-language interoperability;
- **SciPy / statsmodels:** statistical analysis where appropriate;
- **sentence-transformers:** optional embeddings, with caution against treating similarity as discourse-theoretical relation.

### 7.2 R

Candidate integrations:

- **rDNA:** canonical DNA interface;
- **igraph:** network analysis;
- **quanteda:** corpus management, tokens, document-feature matrices, dictionaries, co-occurrence, similarity;
- **tidytext:** tidy text-analysis workflows;
- **statnet / sna / ergm:** statistical network models;
- **btergm:** temporal ERGM workflows where theoretically justified;
- **stm:** optional structural topic modeling as exploratory comparison, not as a substitute for discourse theory.

### 7.3 Standard interchange formats

Target support:

- CSV/TSV;
- JSON/JSONL;
- GraphML;
- GEXF;
- node/edge tables;
- sparse matrices;
- DNA-compatible statement tables;
- Python DataFrames;
- R data frames.

Design goal:

**LaclauGPT ↔ DNA/rDNA ↔ Python ↔ R**

without forcing researchers into one language or one software ecosystem.

---

## 8. Critical AI Studies as methodological reflexivity

Do not repeat the Phase 1 Critical AI literature review. Phase 2 should use Critical AI Studies reflexively to examine the research apparatus itself.

Questions:

- Which political and linguistic categories are easier for current models to recognize?
- Which languages, dialects, regions, and political contexts receive poorer representation?
- How do proprietary APIs and model changes affect reproducibility?
- How do training data and platform data-access regimes structure what can be observed?
- How do computing infrastructure, labor, energy, and ownership enter the research process?
- What normative assumptions are embedded in categories such as safety, toxicity, misinformation, ideology, extremism, and risk?
- Does automated actor/ideology classification reproduce researcher categories rather than discover political structure?
- Does visibility bias make highly connected actors appear more politically important than marginalized actors?
- What changes when AI is simultaneously research object, communication participant, and analytical instrument?

Critical AI sources should inform methodological caution without being treated as automatically correct empirical classifications of other actors.

---

## 9. Operational data structures

Define explicit schemas for:

### Actors/communicators
- person;
- account;
- organization;
- institution;
- platform;
- bot;
- AI system;
- hybrid/AI-assisted communicator.

### Communication events
- sender/source;
- recipient/audience where available;
- platform;
- timestamp;
- document/message;
- reply/mention/share/citation relation;
- human/AI provenance.

### Discourse objects
- signifier;
- concept;
- claim;
- stance;
- demand;
- identity;
- antagonism;
- articulation;
- sociotechnical imaginary.

### Network objects
- node;
- edge;
- edge type;
- weight;
- direction;
- time interval;
- analytical layer;
- projection method.

---

## 10. Analytical methods

### 10.1 Laclau layer
- structured LLM-assisted interpretation;
- evidence-linked articulation extraction;
- signifier/demand/frontier coding;
- human validation;
- aggregation by actor/time/arena.

### 10.2 DNA layer
- actor–concept matrices;
- actor–claim matrices;
- stance coding;
- congruence/conflict projections;
- discourse coalitions;
- temporal DNA.

### 10.3 SNA layer
- degree/strength;
- centrality where theoretically justified;
- brokerage;
- assortativity/homophily;
- community detection;
- k-core / cohesion;
- diffusion/flow;
- multilayer/multiplex analysis;
- temporal network analysis.

Do not equate a metric with a sociological concept automatically.

### 10.4 Cross-layer analysis

Potential comparisons:

- semantic/articulation communities vs DNA coalitions;
- DNA coalitions vs social-interaction communities;
- actor brokerage vs articulation change;
- temporal discourse change vs network restructuring.

---

## 11. Validation strategy

Extend Phase 1 validation to the network layers.

### Extraction validity
- actor/entity resolution;
- statement boundaries;
- concept/claim detection;
- stance detection;
- timestamps;
- interaction edges.

### Discourse-theoretical validity
- articulation;
- equivalence/difference;
- frontier;
- signifier function;
- evidence adequacy.

### Network validity
- node identity;
- edge semantics;
- duplicate handling;
- missing-data effects;
- time-window sensitivity;
- projection sensitivity.

### Cross-layer validity

Test whether apparent relationships among discourse, DNA, and SNA structures survive changes in:

- extraction model;
- prompt/codebook;
- time window;
- entity-resolution rules;
- platform;
- graph projection;
- community-detection algorithm.

### Benchmark comparisons
- human coder ↔ human coder;
- human coder ↔ LLM;
- human coder ↔ classical NLP;
- classical NLP ↔ LLM;
- LaclauGPT ↔ manually coded DNA.

---

## 12. Reproducibility and provenance

Every network edge and discourse relation should be traceable back to source evidence.

Ideal audit path:

**visualization → graph edge → derived statement → analytical annotation → original passage/document**

Store:

- collector/version;
- preprocessing version;
- model/provider/version;
- prompt;
- codebook;
- software version;
- parameters;
- date of analysis;
- uncertainty;
- human review/correction.

This is a core scientific requirement, not merely implementation metadata.

---

## 13. AI26 as application domain, not results section

AI26 can motivate methodological examples concerning:

- accelerationist/techno-optimist discourse;
- x-risk/doomer discourse;
- Critical AI;
- anti-AI/Luddite discourse;
- mainstream governance;
- left techno-optimism and adjacent formations.

Possible examples should demonstrate:

- how the same actor can occupy different discourse positions over time;
- how different networks may contain overlapping but non-identical coalitions;
- how AI-mediated communication could be represented;
- how elite, parliamentary/policy, and grassroots arenas can be compared.

Do not report Phase 2 empirical findings.

---

## 14. Limitations

Plan an explicit discussion of:

- conceptual overload;
- incompatible theoretical vocabularies;
- risk of reducing discourse theory to graph structure;
- risk of treating network clusters as political identities;
- actor-resolution errors;
- platform/API selection bias;
- missing relational data;
- multilingual measurement problems;
- unstable LLM behavior;
- proprietary model dependence;
- edge-construction choices;
- temporal-window effects;
- projection artifacts;
- overinterpretation of centrality/community metrics;
- ethical problems around public/private data and actor labeling.

---

## 15. Transition to Phase 3

Phase 2 should end with methodological readiness criteria rather than findings.

Candidate criteria:

- stable common data model;
- evidence-linked relations;
- DNA import/export tested;
- Python/R interchange tested;
- baseline classical NLP comparisons implemented;
- actor resolution evaluated;
- network-construction rules documented;
- human-coded benchmark available;
- LLM extraction error analysis completed;
- clearly defined optional components.

Phase 3 can then choose a deliberately limited subset of the framework for empirical testing.

---

# Suggested sources

## A. Read first for the SNA/communication layer

### 1. Harrison C. White — *Identity and Control: How Social Formations Emerge*, 2nd ed. (2008)

Primary use:
- relational identity;
- networks and stories;
- netdoms and switching;
- structural equivalence;
- emergent social formations.

Why first: gives the SNA layer a theory of identity and meaning that is richer than graph topology and creates the strongest bridge toward discourse analysis.

### 2. Elena Esposito — *Artificial Communication: How Algorithms Produce Social Intelligence* (2022)

Primary use:
- algorithms as communication partners;
- artificial communication;
- personalization;
- prediction;
- Luhmannian communication in the AI context.

Why first: directly addresses the AI26-era problem of non-human computational participation in communication.

### 3. Armin Nassehi — *Patterns: Theory of the Digital Society* (English ed. 2024)

Primary use:
- digital pattern recognition;
- datafication and observation;
- social complexity;
- functional differentiation;
- cybernetic feedback.

Why first: supplies the macro-level theory of why digital traces and computational patterns are socially possible and analytically consequential.

These three form the proposed new theoretical spine of the Phase 2 SNA layer:

**White → relational identity and social formations**  
**Nassehi → digital patterns and social-system complexity**  
**Esposito → artificial communication and algorithmic participation**

## B. Laclau / discourse theory inherited from Phase 1

Use selectively and cite Phase 1 rather than repeating the whole framework.

- Laclau, Ernesto & Chantal Mouffe. *Hegemony and Socialist Strategy*.
- Laclau, Ernesto. *Emancipation(s)*.
- Laclau, Ernesto. *On Populist Reason*.
- Palonen, Emilia. Work on populism, hegemony, discourse theory, and AC/DT.
- Koljonen, Juha; Kleber Carrilho; Emilia Palonen. AC/DT work relevant to computational/structured discourse analysis.

## C. Discourse Network Analysis core

- Leifeld, Philip (2013). “Reconceptualizing Major Policy Change in the Advocacy Coalition Framework: A Discourse Network Analysis of German Pension Politics.”
- Leifeld, Philip (2017). “Discourse Network Analysis: Policy Debates as Dynamic Networks.” In *The Oxford Handbook of Political Networks*.
- Leifeld, Philip (2020). “Policy Debates and Discourse Network Analysis: A Research Agenda.”
- Leifeld & Mastroianni. Recent methodological overview of DNA.
- Angst, Müller & Walker. Recent work on automated extraction of discourse networks from large media corpora.
- **Discourse Network Analyzer (DNA)** software.
- **rDNA**.

## D. SNA and relational sociology

- White, Harrison C. (2008). *Identity and Control*.
- Wasserman, Stanley & Katherine Faust. *Social Network Analysis: Methods and Applications*.
- Newman, Mark. *Networks*.
- Borgatti, Everett & Johnson. *Analyzing Social Networks*.
- Granovetter on weak ties and embeddedness.
- Burt on structural holes/brokerage.
- Padgett and Ansell on robust action and relational structure where relevant.

## E. Systems, digital society, and artificial communication

- Esposito, Elena (2022). *Artificial Communication*.
- Nassehi, Armin (2024 English ed.). *Patterns*.
- Luhmann, Niklas. *Social Systems*.
- Luhmann, Niklas. *The Society of Society*.
- Baecker, Dirk. Work on computer/digital society and next society.
- Castells, Manuel. *The Rise of the Network Society* and *Communication Power* as inherited background rather than the main new reading burden.

## F. Critical AI Studies and political economy

Use primarily for methodological reflexivity and AI26 context.

- Crawford, Kate. *Atlas of AI*.
- Benjamin, Ruha. *Race After Technology*.
- Noble, Safiya Umoja. *Algorithms of Oppression*.
- D'Ignazio, Catherine & Lauren Klein. *Data Feminism*.
- Couldry, Nick & Ulises A. Mejias. *The Costs of Connection*.
- Birhane, Abeba. Work on relational/decolonial AI and algorithmic colonization.
- Mohamed, Shakir; Marie-Therese Png; William Isaac. “Decolonial AI.”
- Lindgren, Simon (ed.). *Handbook of Critical Studies of Artificial Intelligence*.
- van Dijck, Poell & de Waal. *The Platform Society*.
- McQuillan, Dan. *Resisting AI*.

## G. Classical computational text analysis

- Grimmer, Roberts & Stewart. *Text as Data*.
- Benoit et al. (2018). “quanteda: An R Package for the Quantitative Analysis of Textual Data.”
- Pedregosa et al. (2011). “Scikit-learn: Machine Learning in Python.”
- Silge & Robinson. *Text Mining with R*.
- spaCy documentation/software papers where used.

Phase 2 should treat classical models as reproducible baselines and complementary tools rather than obsolete precursors to LLMs.

## H. Open-source network software and statistical models

- Hagberg, Schult & Swart (2008). NetworkX.
- Csárdi & Nepusz (2006). igraph.
- statnet / sna literature.
- ERGM literature.
- Leifeld et al. on `btergm` if temporal ERGMs are actually used.
- multilayer-network methodology if the cross-layer design becomes operational.

Only sources actually used in the final manuscript should remain in the final bibliography.

---

# Suggested conceptual figure

A future figure can depict:

**AI26 / other corpus**

↓  

**Classical NLP + LLM extraction + human coding/review**

↓

**Layer 1: Laclau Discourse Analysis**  
signifiers · demands · subjects · articulations · frontiers

↕ evidence-preserving translation

**Layer 2: Discourse Network Analysis**  
actors × claims/concepts × stance × time  
DNA / rDNA interoperability

↕ multiplex / cross-layer analysis

**Layer 3: Social & Communication Network Analysis**  
actors · organizations · interactions · institutions · platforms · algorithmic systems

↓

**Temporal / comparative / social-system analysis**

Across all layers:

**Critical AI reflexivity · provenance · uncertainty · human validation**

The arrows represent transformations among analytical representations, not theoretical reduction.

---

# Working methodological thesis

> **LaclauGPT Phase 2 should not turn discourse theory into network analysis. It should make interpretive discourse analysis interoperable with discourse-network and social-network methods while preserving the distinct theoretical meaning of each analytical layer.**
