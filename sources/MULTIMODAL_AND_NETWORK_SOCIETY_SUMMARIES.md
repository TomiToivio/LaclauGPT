# Multimodality and Network Society source summaries

These summaries were added to support the multimodal pre-analysis layer of LaclauGPT and the planned AI26 analysis pipeline. They separate source-derived claims from LaclauGPT-specific implementation notes.

## John A. Bateman, Janina Wildfeuer & Tuomo Hiippala — *Multimodality: A Hands-On Guide* (2026)

**Bibliographic note:** De Gruyter Brill. ISBN 978-3-11-141051-7; PDF ISBN 978-3-11-141165-1. The volume is a sequel to Bateman, Wildfeuer & Hiippala (2017), *Multimodality: Foundations, Research and Analysis*.

**Core argument / research question:** The book develops a practical, empirically oriented framework for multimodal research. Its central concern is how researchers can move from heterogeneous communicative material to systematic analysis without treating multimodality as a loose checklist of visual features. The framework connects semiotic modes, genre, medium, materiality, canvases/slices, annotation, corpus construction and pattern analysis.

**Methodological architecture:** The book's "multimodal navigator" organises research into selection/identification, analysis, and evaluation/reporting. It develops core constructs of semiotic mode, genre, medium and materiality, then shows how communicative material can be segmented into canvases/slices and annotated at several levels. The empirical workflow is explicitly iterative rather than a one-shot classification exercise. Annotation is treated as a bridge between qualitative interpretation and larger-scale corpus analysis.

**Key concepts:**

- **Semiotic mode:** meaning-making resources should be identified from the communicative material and their organisation, not assumed solely from everyday labels such as "image" or "text".
- **Medium / genre / materiality:** meaning is constrained by the material and medial organisation through which semiotic modes are realised.
- **Canvas and slicing:** complex multimodal artefacts can contain regions, layers and temporally unfolding sub-canvases. This is especially important for social-media interfaces, overlays, screenshots, picture-in-picture and other nested media.
- **Annotation:** both feature-based and instance-based annotation are useful. Repeated objects, visual regions and temporally bounded events can be tracked without collapsing them into high-level interpretations.
- **Corpus analysis / pattern harvesting:** once grounded annotations exist, regularities can be examined quantitatively while retaining an interpretable link back to the original semiotic material.

**TikTok / short-video relevance:** The TikTok case study develops a multilevel annotation scheme beginning with the video canvas and supported semiotic modes before zooming into shots and other expressive forms. Relevant attributes include shot framing, angle, movement and dynamicity, but also TikTok-specific categories such as provenance, contextualisation, usage, adjustment and composition. Split screens and picture-in-picture are treated as normal resources rather than exceptional filmic devices. The authors argue that this semiotically grounded annotation can provide a more open and intersubjectively inspectable base for later critical or ideological interpretation.

**LLM / automation implications:** The book explicitly recognises that detailed multimodal annotation is time-consuming and that full automation across all modes remains limited. At the same time, a general annotation framework creates a stable target for semi-automated techniques. For LaclauGPT this supports using an LLM as an annotator or assistant only within a transparent schema, keeping uncertainty and source evidence visible and preserving human review.

**Concepts useful for LaclauGPT:**

1. Use a **descriptive semiotic layer before discourse-theoretical interpretation**.
2. Treat a social-media item as a materially organised multimodal ensemble rather than as transcript plus decorative image.
3. Record canvas/layout, shots, overlays, embedded media, provenance/usage, visual composition, visible text and temporal sequencing before interpreting ideology.
4. Preserve the difference between direct observation, OCR/ASR/model-derived context and later interpretation.
5. Make the multimodal output reusable by later Laclau/Mouffe/Palonen, DNA, Critical AI Studies and other analytical plugins.

**Relevance to AI26:** Very high. AI26 contains screenshots of model interfaces, corporate demos, memes, charts, data-centre imagery, robots, protests, AI-generated material, news clips and mixed platform artefacts. A canvas/mode/provenance-first method is better suited to this heterogeneity than an election-specific visual checklist.

**Limitations / cautions:** The framework is intentionally general and can become detailed if every annotation tier is implemented literally. LaclauGPT should therefore use a compact subset for routine automated pre-analysis and reserve fine-grained annotation for research questions that need it. The framework provides semiotic grounding; it does not itself supply a theory of ideology, hegemony or political discourse.

**Implementation decision:** Use Bateman/Wildfeuer/Hiippala-style problem-oriented multimodality as the default qualitative multimodal pre-analysis. The LLM prompt should focus on material/canvas organisation, scene and activity, composition, text/symbols/interface, provenance/usage, cross-modal contribution and uncertainty. It should not classify ideology at frame level.

---

## Manuel Castells — *The Rise of the Network Society* (2nd ed., with new preface, 2010; originally 1996/2000)

**Bibliographic note:** Wiley-Blackwell. Volume I of *The Information Age: Economy, Society, and Culture*. ISBN 978-1-4051-9686-4.

**Core argument / research question:** Castells analyses the emergence of a social structure organised increasingly through networks enabled by information and communication technologies. The book examines technological change, informational/global economic organisation, network enterprises, transformations of work, electronic communication, the "culture of real virtuality," the space of flows and changing temporal organisation.

**Network society:** Castells argues that networks increasingly organise key dimensions of social practice. Digital networking technologies greatly expand networks' capacity for reconfiguration and operation across scale. Networks include some actors, places and territories while excluding or marginalising others, so network connectivity is also a question of inequality and power.

**Flows:** The network society is organised through flows of information, capital, technology, organisational interaction, images, sounds and symbols. For Castells, flows are not merely messages moving between already fixed social units; they are part of the material organisation of dominant economic, political and symbolic processes.

**Space of flows / space of places:** Castells distinguishes locally contiguous social life from a "space of flows" that supports simultaneous interaction among physically separated actors and sites. Nodes and hubs acquire different functions and weight within networks. This is useful for analysing digital political communication because online media can connect locally embodied events, organisations and audiences into translocal communicative processes.

**Communication and power:** Electronic communication networks transform culture and political communication. Media and computer-mediated communication become central arenas in which political processes are organised and represented. The framework therefore draws attention to the relation between actors, communication infrastructures, institutions, network positions and flows, while cautioning against reducing politics to media effects alone.

**Concepts useful for LaclauGPT:**

- actors, organisations and institutions;
- networks and explicit relations;
- nodes, hubs, channels and sites;
- flows of information, images, technology, money, authority or people;
- mediated/translocal communication versus local embodied settings;
- inclusion/exclusion and access to networks;
- power as partly related to the organisation and control of networks and flows.

**Why Castells fits the "light sociology" stage:** These concepts can orient a descriptive sociological reading without requiring the model to decide ideology, habitus, functional differentiation, class position or hegemonic articulation in advance. A lightweight Castells pass can ask who is connected to whom, through what media or institutions, what appears to flow, and how local places connect to mediated/translocal spaces. Those observations can then be handed to stronger theories later.

**Relevance to AI26:** High. AI discourse is produced through highly networked relations among firms, labs, researchers, investors, governments, media, online communities, social movements and platform publics. AI26 material also routinely mixes local places such as data centres, parliaments, conferences or protests with global platform communication. Castells therefore provides a useful contextual vocabulary before specialised discourse analysis.

**Limitations / cautions:** *The Rise of the Network Society* is a macro-sociological interpretation, not an SNA coding manual and not a complete formal theory of society. The light pre-analysis must not invent ties, centrality, brokerage or network power from a single document. Some of Castells's empirical examples are historically tied to the information-economy conditions of the 1990s and 2000s; concepts should be used heuristically rather than as timeless claims.

**Implementation decision:** Use Castells only in the item-level summary stage, after semiotic description. Extract evidence-backed actors/organisations/institutions, explicit or strongly implied relations, flows, nodes/channels, local/translocal spatial organisation and observable power/access relations. Keep this separate from formal SNA/DNA and from the later Laclau/Mouffe/Palonen discourse stage.

---

## Combined pipeline implication

For LaclauGPT the two sources support a layered sequence:

`raw multimodal evidence -> semiotic/material analysis -> multimodal synthesis -> light Castells contextualisation -> dedicated discourse/theory stages`

This ordering intentionally delays Laclau/Mouffe/Palonen, DNA and Critical AI Studies until the source has first been described in a theory-light, reusable form. The multimodal layer should therefore be detailed enough to preserve composition, provenance and cross-modal meaning, but light enough to remain general across AI26, EP24 and future studies.
