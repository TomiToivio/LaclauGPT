# AC/DT theory and methods backwards-compatibility report

## Purpose

This report audits the current LaclauGPT theory/methodology surface against the Helsinki AC/DT research lineage and closely related work by Simon Lindgren. Its purpose is **backwards compatibility**, not expansion for expansion's sake: older AC/DT-compatible studies and datasets should remain intelligible, reproducible, importable, analysable and visualisable even as LaclauGPT develops newer LLM-assisted methods.

The audit is based on the current `THEORY.md`, the source summaries in `sources/SUMMARIES.md`, the uploaded AC/DT-team publications, and publicly available work by Juha Koljonen, Kleber Carrilho, Emilia Palonen and Simon Lindgren.

## Executive summary

LaclauGPT already has a strong **theoretical core** for post-structural discourse theory: articulation, equivalence/difference, nodal points, floating and empty signifiers, antagonistic frontiers, collective subjects, hegemony, affective investment, populism as political logic, Palonen's Formula of Populism, polarisation as bipolar hegemony, populist dynamics, myths/imaginaries and rhetoric-performative discourse analysis. The most important compatibility gaps are therefore not another layer of Laclaudian vocabulary.

The main missing or under-specified layer is the **AC/DT research practice around that theory**: experimental and bottom-up computational exploration; topic modelling used instrumentally to guide interpretation; temporal peak analysis; hashtag landscapes/ecosystems; mixed computational and close-reading workflows; actor/theme/network analysis; validated multilingual sentiment/emotion analysis; legacy Wordscores/Wordfish scaling; multimodal rhetoric-performative analysis; and explicit platform/algorithmic mediation. Simon Lindgren's work adds a particularly useful methodological bridge between discourse theory, network analysis, computational text analysis and interpretive close reading.

The compatibility target should therefore be: **keep theoretical inference strict while restoring a broad, modular exploratory-method layer beneath it**.

## 1. What the current core already covers well

`THEORY.md` should remain authoritative for the following concepts and safeguards:

- Laclau and Mouffe: articulation, discourse, element/moment, nodal point, floating signifier, empty signifier, equivalence, difference, antagonism and hegemony.
- Laclau: demand formation, collective subjects, naming/representation and populism as a political logic rather than a fixed ideology.
- Palonen: Formula of Populism, affective-antagonistic construction of `Us` and `Frontier`, polarisation as a potentially hegemonic bipolar dynamic, fringe/mainstream/competing populist dynamics, myths/imaginaries and rhetoric-performative analysis.
- Evidence discipline: frequency is not hegemony; negativity is not antagonism; sentiment is not affective investment; co-occurrence or semantic similarity is not articulation; document-level interpretations remain provisional; corpus-level claims require validation and human review.

These safeguards are important precisely because several legacy AC/DT methods produce **signals** that are theoretically suggestive but insufficient on their own.

## 2. Social-science theories and concepts missing or under-specified

### 2.1 Compatibility-critical additions

#### AC/DT as a methodological epistemology

The current theory contract names the substantive discourse-theoretical concepts but does not yet fully specify the **Anarcho-Computational Discourse-Theoretical (AC/DT)** research stance itself. AC/DT should be documented as an experimental, iterative and interpretivist workflow in which computational techniques expose patterns and direct attention, while close reading and theory-sensitive interpretation establish social-scientific claims.

Compatibility requirement:

- add `ACDT_EXPERIMENTALISM` / `ACDT_INTERPRETIVISM` as methodology metadata, not document-level political codes;
- distinguish exploratory computation from evidential theoretical inference;
- permit multiple methods and iterative recoding without implying that any one model discovers a discourse automatically.

#### Topic instrumentalism versus topic realism

Koljonen's methodological work explicitly distinguishes topic models used as representations of substantive constructs from topic models used as **instruments for navigation and close reading**. AC/DT primarily needs the latter mode.

Compatibility requirement:

- every topic-model run should record an interpretation mode such as `instrumentalist`, `realist/measurement`, or `unspecified`;
- instrumentalist topics must never be automatically promoted to `frame`, `discourse`, `ideology`, `formation`, `nodal_point` or `hegemonic_project`;
- validation expectations should depend on the stated use of the model.

#### Hashtag publics, hashtag landscapes and hashtag ecosystems

AC/DT and Lindgren-adjacent work treats hashtags as both platform affordances and possible sites of articulation, not merely keywords. The missing conceptual layer includes:

- hashtag publics;
- hashtag landscapes/ecosystems;
- co-articulation across hashtags;
- temporal reuse and recontextualisation of hashtags;
- the distinction between platform-level co-occurrence and theoretically validated articulation.

This is particularly relevant for legacy Twitter/X studies and future cross-platform work.

#### Interpretive mixed-methods / thick description

AC/DT's methodological identity depends on combining large-scale computational exploration with contextual interpretation and close reading. This should be explicit in the theory/method contract rather than left as an implementation detail.

Required concepts include:

- computational pattern as a research lead;
- purposive/peak/event sampling for close reading;
- contextual knowledge as part of interpretation;
- explicit linkage from aggregate pattern back to primary evidence;
- researcher disagreement and revision as valid parts of the workflow.

#### Platform mediation and programmable politics

The current core is strong on discourse but comparatively thin on how platform architectures, APIs, ranking systems, automation, bots and AI participate in political communication. Lindgren's later work on **programmable politics** makes this a useful compatibility layer.

This should remain analytically separate from Laclaudian articulation: platform affordances and algorithmic selection can condition visibility and connectivity without themselves proving a political equivalence or antagonistic frontier.

### 2.2 Important complementary theories for specific modules

These need not all become core `THEORY.md` concepts, but the framework should know how to carry their outputs without semantic loss.

- **Collective action and connective action:** useful for digital movements, hashtag mobilisation and the movement from personalised action frames to collective/structural frames.
- **Framing theory:** diagnostic, prognostic and motivational framing; frame bridging, extension and transformation. Source summaries already cover this literature, but it is not yet a first-class compatibility surface.
- **Public sphere / Europeanisation / political communication:** needed for EP-election legacy studies and comparative political communication.
- **Party competition and party-position theory:** needed to interpret legacy manifesto scaling and campaign communication.
- **Emotion theory:** sentiment, discrete emotions and emotion intensity are useful auxiliary constructs, but must remain distinct from Laclaudian affective investment.
- **Knowledge legitimacy, misinformation and counter-discourse:** relevant to pandemic and AI expertise contests, especially where official knowledge and counter-knowledge are articulated against one another.
- **Data activism / data justice:** useful for analysing civil-society struggles around datafication and AI.
- **Multimodal rhetoric and performativity:** needed when video, imagery, editing, sound, gesture and visual symbolism help constitute an `Us`, a frontier or an affective political identity.

## 3. Social data science methods missing or under-specified

### 3.1 High-priority AC/DT compatibility methods

#### Interpretive topic modelling

Support an explicitly exploratory topic-model workflow, initially including LDA for legacy reproduction and allowing newer topic models as optional alternatives.

Minimum output contract:

- model/method/version and parameters;
- preprocessing and language metadata;
- document-topic and topic-term weights;
- topic labels as researcher/model interpretations with provenance;
- representative source records;
- interpretation mode (`instrumentalist` by default for AC/DT);
- run-to-run stability or sensitivity information when available.

#### Temporal peak analysis

The AC/DT mask study uses peaks in topic-related daily activity to identify moments for interpretive reading. LaclauGPT should support a generalised form rather than one hard-coded threshold.

Minimum output contract:

- metric and aggregation window;
- threshold/detection rule and parameters;
- topic/theme/signifier/hashtag involved;
- start, apex and end times;
- contributing source records;
- human notes/labels;
- optional event/context annotation.

A legacy-compatible `threshold_count` detector can coexist with change-point, anomaly or burst-detection methods.

#### Close-reading sampler

Computational outputs should be able to create transparent reading samples by:

- peak/event;
- topic/theme;
- central or bridging actor;
- high/low confidence;
- outlier/contradiction;
- random validation sample.

Every sample must keep stable IDs back to the original records.

#### Thematic and vocabulary analysis

Retain straightforward word-frequency and thematic-analysis outputs because older AC/DT/EP2019 workflows used them deliberately alongside more complex methods. Add keyness, collocations/concordances and multilingual normalisation as optional corpus-assisted extensions.

#### Social network and hashtag co-occurrence analysis

Legacy compatibility requires actor/account and hashtag networks in addition to newer discourse-network structures.

Support at minimum:

- actor interaction networks;
- hashtag co-occurrence networks;
- mention/reply/repost networks where platform data permit;
- weighted edges;
- modularity/community assignments;
- degree/betweenness and other declared metrics;
- temporal slices;
- links back to the records that generated edges.

Network clusters and co-occurrence edges must remain **descriptive computational structures**, not automatic ideological formations or Laclaudian equivalences.

#### Sentiment, emotion and emotion-intensity analysis

Koljonen et al.'s Finnish manifesto work is part of the methodological lineage and should remain reproducible.

Compatibility requirements:

- polarity and discrete-emotion analysis;
- intensity scores where supported;
- lexicon/model name and version;
- language and translation/adaptation provenance;
- validation/re-annotation metadata;
- aggregation by document/actor/time/group;
- strict separation from `affective_investment` in the Laclaudian schema.

#### Wordscores and Wordfish

These are not recommended as default methods for AI26, but they are required for methodological and historical compatibility with Koljonen's party-position work.

Implement as optional legacy/measurement plugins with:

- reference texts/reference scores for Wordscores;
- declared scaling dimension;
- document-length diagnostics;
- uncertainty and validation against external estimates where available;
- warnings that Wordfish dimensions require substantive interpretation and that legacy Finnish results showed weak performance in some settings.

### 3.2 Multimodal and cross-platform compatibility

Rhetoric-performative work on campaign videos means a text-only compatibility layer is incomplete. The analysis schema should be able to retain and combine:

- transcript/speech;
- on-screen text;
- images/shots/scenes;
- audio/music/tone where ethically and technically appropriate;
- speaker/actor and temporal segments;
- visual symbols and rhetorical devices;
- multimodal evidence spans or timecodes.

The data-collection module should preserve media provenance even when the analysis module initially implements only transcript-first processing.

### 3.3 Lindgren-derived methodological extensions

The following methods are particularly compatible with AC/DT because they combine computational mapping and interpretive reading:

- temporal hashtag co-occurrence as discursive-articulation candidates;
- SNA + discourse analysis of hashtag ecosystems;
- mixed computational mapping + close reading of actor profiles;
- diffusion/amplification analysis;
- broker identification;
- platform-affordance analysis;
- explicit treatment of network thresholds and community labels as interpretive choices.

## 4. Cross-repository backwards-compatibility contract

### 4.1 `TomiToivio/LaclauGPT`

The core repository should own the **theory and method semantics**:

- document AC/DT experimentalism/interpretivism;
- add a method registry with stable IDs and citations;
- document topic instrumentalism/realism;
- add hashtag-landscape/ecosystem and platform-mediation concepts as optional analytical layers;
- preserve the current strict Laclaudian inference rules;
- maintain a source/reading list for every theory and method;
- define shared interchange schemas and versioning used by the submodules.

Suggested stable method IDs:

`topic_model_lda`, `topic_model_generic`, `peak_analysis`, `close_reading_sampler`, `thematic_analysis`, `word_frequency`, `corpus_keyness`, `hashtag_cooccurrence`, `social_network_analysis`, `sentiment_analysis`, `emotion_analysis`, `emotion_intensity`, `wordscores`, `wordfish`, `multimodal_rhetoric_performative`, `discourse_network_analysis`.

### 4.2 `TomiToivio/LaclauGPT-Data-Collection`

Collection should preserve enough source structure for old and new methods to coexist:

- stable source/record/actor IDs;
- timestamps with original timezone when available;
- hashtags, mentions, links and interaction/repost/reply identifiers;
- collection query, keyword/hashtag and API/tool provenance;
- language and translation metadata;
- raw text plus media references;
- account/actor metadata without forcing permanent ideological labels;
- platform-specific metadata in an extensible namespace;
- event/collection-window metadata for campaign or crisis studies.

Legacy imports should not discard fields merely because current AI26 analysis does not use them.

### 4.3 `TomiToivio/LaclauGPT-Data-Analysis`

Analysis should implement a **plugin-style method registry** whose outputs share provenance and evidence conventions but do not pretend to be semantically identical.

Each result should state:

- `method_id` and `method_version`;
- `schema_version`;
- input record IDs and corpus/study version;
- parameters/model/lexicon;
- language/preprocessing information;
- generated artefacts and evidence links;
- whether the output is exploratory, measurement-oriented or theoretical/interpretive;
- human validation/review status.

No compatibility adapter should silently convert computational signals into Laclaudian theoretical claims.

### 4.4 `TomiToivio/LaclauGPT-Data-Visualization`

The dashboard should be able to render both contemporary LaclauGPT outputs and legacy AC/DT artefacts:

- topic prevalence and representative documents;
- topic/signifier/hashtag timelines and peaks;
- hashtag ecosystems and actor networks;
- thematic/keyword tables and concordance drill-down;
- sentiment/emotion/intensity trends with clear labeling;
- party-position scaling plots when legacy data contain them;
- close-reading/evidence panels;
- multimodal evidence/timecodes when present;
- method/version/provenance badges;
- graceful fallback when an old dataset lacks newer fields.

Visual proximity, centrality or cluster colour must not be labelled as discourse, ideology, equivalence, antagonism or hegemony unless the underlying analysis explicitly contains a validated interpretation of that type.

## 5. Data interchange and migration rules

1. **Additive before destructive.** Prefer adding fields and adapters over renaming/removing legacy fields.
2. **Version every public schema.** Results and collection records should expose `schema_version`; method outputs should also expose `method_version`.
3. **Separate signal from interpretation.** A topic, cluster, peak, centrality score or sentiment is a signal; a discourse-theoretical coding is a separate human-reviewable interpretation.
4. **Keep provenance to primary evidence.** Every aggregate result must be drillable back to contributing record IDs when licensing/privacy allows.
5. **Keep language provenance.** Translation, lexicon adaptation, tokenisation and preprocessing must be recorded for multilingual research.
6. **Allow absence.** Old studies need not be retrofitted with fields that cannot be reconstructed faithfully; adapters should return explicit `null`/`not_available` rather than invent values.
7. **Preserve methodological plurality.** New LLM methods complement rather than erase topic models, lexicons, scaling, network analysis and close reading.
8. **No actor-essentialism.** Actor metadata can record role, institution or researcher hypotheses, but ideological formation remains statement/corpus/time dependent.

## 6. Validation and testing matrix

Create small public fixtures representing each method family:

- a Finnish manifesto fixture for Wordscores/Wordfish and sentiment/emotion;
- a hashtag/tweet fixture for topic + peak + close reading;
- a hashtag co-occurrence fixture for network/ecosystem analysis;
- an EP-election actor/tweet fixture for thematic + topic + SNA outputs;
- a multimodal fixture with transcript and timecoded visual annotations;
- a modern LaclauGPT fixture containing articulation/frontier/signifier outputs.

For every fixture test:

- import old/legacy-shaped data;
- normalise to the current interchange representation without data loss;
- run or load the applicable method output;
- export it again;
- re-import it;
- render it in the visualization layer;
- retain stable provenance/evidence references;
- prove that no adapter elevates a computational signal into an unsupported theoretical claim.

## 7. Priorities

### P0: semantic compatibility

- AC/DT methodology contract and citations in the core repo.
- Shared method/result registry and schema versions.
- Topic instrumentalism flag.
- Legacy import/export fixtures.
- Provenance from aggregates back to primary data.

### P1: analytical compatibility

- LDA/topic adapter.
- temporal peak analysis.
- close-reading sampler.
- thematic/word-frequency/corpus-assisted views.
- hashtag and actor SNA.
- validated sentiment/emotion/intensity module.

### P2: specialised compatibility

- Wordscores/Wordfish.
- multimodal rhetoric-performative analysis.
- programmable-politics/platform-affordance metadata.
- advanced temporal diffusion/broker analysis.

## 8. Definition of backwards compatibility

The four-repository LaclauGPT system is AC/DT-backwards-compatible when a researcher can take a legacy-style AC/DT dataset or result, preserve its original methodological meaning, import it into the contemporary data model, inspect and reanalyse it with the applicable legacy or modern method, export it without semantic data loss, and render it in the dashboard, while the system continues to enforce the current evidence-first distinction between **computational patterns** and **discourse-theoretical interpretations**.
