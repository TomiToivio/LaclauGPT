# AC/DT methodology contract

Status: **normative compatibility companion to `THEORY.md`**.

This document preserves the Anarcho-Computational Discourse-Theoretical (AC/DT) research style used in the Helsinki University work that precedes the current four-repository LaclauGPT architecture. It does not weaken `THEORY.md`. Where this document and `THEORY.md` touch the same theoretical concept, the evidence-first safeguards in `THEORY.md` are normative.

## 1. Methodological stance

AC/DT combines computational exploration with interpretive discourse-theoretical research. Computational methods are used to make large corpora navigable, expose patterns, identify temporal concentrations, locate candidate relations, and select material for close reading. They do not become discourse-theoretical findings automatically.

The design therefore supports three explicit interpretation modes:

- `exploratory_instrumentalist`: computational output is an instrument for navigation, sampling and interpretation of primary material;
- `measurement`: the output is treated as a measurement and must carry method-appropriate validation and diagnostics;
- `theoretical_interpretive`: a researcher- or model-assisted theoretical coding linked to primary evidence and subject to human review.

Every reusable analytical result must declare one of these modes.

## 2. Topic instrumentalism and topic realism

Following the distinction used by Koljonen via Pääkkönen and Ylikoski, topic modelling may be used in two importantly different ways.

### Instrumentalist use

A topic model is a magnifying glass or navigation device. Topics are statistical word-pattern structures used to guide close reading, event selection or corpus exploration. In this mode:

- a topic is not asserted to be a discourse, frame, ideology or social entity;
- model quality is judged mainly by usefulness, robustness and transparent parameters;
- interpretive claims are validated against primary texts and researcher argument rather than by treating the topic model itself as ground truth.

### Realist/measurement use

A model output is used as evidence for a substantive construct. In this mode the intended construct, validation target and diagnostics must be declared. Robustness checks, external benchmarks, annotated samples or other method-specific validation are required.

The same algorithm can therefore be used under different epistemic contracts. LaclauGPT must preserve that distinction in result metadata.

## 3. AC/DT experimentalism

The `anarcho-` prefix denotes controlled methodological experimentalism, not absence of rigor. A workflow may combine topic models, frequency analysis, network maps, temporal peak detection, close reading, qualitative coding, multimodal interpretation or other methods iteratively when the research question warrants it.

Experimental freedom is constrained by reproducibility:

- method and schema versions are explicit;
- parameters and preprocessing are recorded;
- source records and evidence references survive transformations;
- model/lexicon/prompt versions are recorded when applicable;
- missing legacy metadata is represented as `null` or `not_available`, never invented;
- human review state is preserved.

## 4. Hashtag publics, landscapes, ecosystems and co-articulation

Hashtags and keywords can function as observable digital traces that connect actors, events and meanings. AC/DT-compatible analysis may therefore construct:

- **hashtag publics**: publics observable through participation around hashtags or related traces;
- **hashtag landscapes**: temporally and relationally changing distributions of hashtags, topics and actors;
- **hashtag ecosystems**: co-occurrence structures connecting multiple hashtags and interpretive frames;
- **co-articulation**: an operational observation that two signs/hashtags repeatedly occur in linked communicative contexts.

`co-articulation` in a computational network is a **candidate relation**. It is not automatically Laclaudian articulation, equivalence, an antagonistic frontier, a nodal relation or hegemony. Those stronger interpretations require evidence from discourse and human-validatable analysis.

## 5. Temporal peak analysis

Peak analysis locates high-intensity moments in a time series so researchers can inspect what happened around them. A peak result must include:

- the counted unit and grouping key;
- temporal bin size/timezone;
- threshold rule and numeric threshold;
- optional smoothing/baseline parameters;
- source record references for every selected bin/peak;
- the sampling rule used for close reading.

Legacy absolute-count thresholds remain supported. Modern alternatives such as z-score, quantile or rolling-baseline thresholds may be added, but their results must not be silently mixed.

## 6. Close reading is a first-class method

Close-reading samples may be selected by peak, event, topic, actor, outlier, network position, stratified random sampling or validation sampling. The selection procedure must be recorded so the path from aggregate pattern to primary evidence is reproducible.

Computational outputs are allowed to suggest where to read. They do not replace reading when the research claim depends on meaning, rhetoric, articulation, antagonism or hegemony.

## 7. Emotion and sentiment

Sentiment, discrete emotion and emotion intensity are supported as auxiliary computational measurements when their language adaptation and validation are documented. They must remain separate from Laclaudian **affective investment**.

- sentiment != affective investment
- emotion label != political identification
- emotion intensity != strength of hegemony
- negative sentiment != antagonistic frontier

## 8. Scaling and legacy political-text methods

Wordscores and Wordfish remain optional backwards-compatible methods for studies that used them. They must declare the intended scaling dimension, reference/training texts where applicable, preprocessing, diagnostics and validation strategy. A latent scale must not be relabelled as ideology without substantive validation.

## 9. Platform mediation and programmable politics

Digital discourse is produced through platforms, software and algorithmic infrastructures that affect collection, visibility, ordering and interaction. LaclauGPT may preserve and analyse platform affordance/mediation metadata, including collection endpoint, ranking context, interaction type and software-generated transformations.

This context layer must remain analytically distinct from discourse-theoretical relations. Platform amplification is not hegemony; recommender adjacency is not articulation; a network edge created by a platform action is not necessarily political equivalence.

## 10. Semantic guardrails inherited from `THEORY.md`

The following are non-negotiable across old and new workflows:

- frequency != hegemony
- co-occurrence/similarity != articulation
- network community != ideological formation
- negative sentiment != antagonistic frontier
- sentiment/emotion != affective investment
- topic != frame/discourse/ideology by default
- document-level theoretical interpretations remain provisional
- corpus-level theoretical claims remain human-reviewable and evidence-linked

## 11. Primary methodological lineage

The compatibility layer is grounded in the following sources already summarized in `sources/SUMMARIES.md`:

- Koljonen, J. & Palonen, E. (2021). *Performing COVID-19 Control in Finland: Interpretative Topic Modelling and Discourse Theoretical Reading of the Government Communication and Hashtag Landscape*.
- Koljonen, J. (2023). *Text as Data and Finnish Politics*.
- Herkman, J. & Palonen, E. (eds.) (2024). *Populism, Twitter and the European Public Sphere*.
- Koljonen, J., Carrilho, K. & Palonen, E. (2025/2026). *The Struggle over Masks on Twitter: an AC/DT Approach to Finnish Pandemic Governance*.
- Palonen, E. (2025). *The Birth and Death of Liberal Democracy in Hungary*.
- Lindgren, S. (2019). *Hacking Social Science for the Age of Datafication*.
- Lindgren, S. (2020). *Data Theory*.
- Lindqvist, L. & Lindgren, S. (2023). *Mapping an Emerging Hashtag Ecosystem*.
- Liminga, A. & Lindgren, S. (2024). *Mapping the Discursive Landscape of Data Activism*.
- Lindgren, S. & Kaun, A. (2025). *Programmable Politics in the Aftermaths of the Pandemic*.

See `schemas/acdt_method_registry.v1.yaml` for stable machine-readable method identifiers and `schemas/acdt_result.v1.schema.json` for the shared result envelope.