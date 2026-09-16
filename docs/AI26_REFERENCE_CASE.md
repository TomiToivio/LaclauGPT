# AI26 public reference case

AI26, **Ideological contestation over AI**, is the canonical public example study for the current LaclauGPT architecture. The study is directly tied to `paper/PAPER.md`, so it provides a realistic, inspectable path from theory to Collection, Analysis and Visualization without making the software itself AI26-specific.

## Research design

The paper compares three arenas:

1. **AI elites** — entrepreneurs, researchers, intellectuals, labs and adjacent ideological movements around frontier AI.
2. **Grassroots mobilisation** — movements and conflicts around employment, creative work, surveillance, data extraction, environmental impacts, data centres, regulation and broader opposition/support.
3. **Parliamentary and electoral politics** — party politics, parliamentary debate, election corpora, government/policy discourse and AI governance.

The public project profile enables Laclaudian analysis, Palonen's Formula of Populism, sociotechnical imaginaries, sentiment, topics, entities, context memory, temporal analysis and multimodal analysis. Network/ANT/ValueFlows extensions remain optional rather than required defaults.

## Formation vocabulary

For reproducible aggregation the current computational vocabulary contains six provisional labels:

- `accelerationism`
- `doomerism`
- `left-wing accelerationism`
- `ai safety`
- `ai critical`
- `anti-ai`

These are **sensitising categories**, not a closed ontology and not permanent properties of actors. Multi-label overlap and abstention are valid. Richer ideological nuance belongs in evidence-linked relations, tags, signifiers, demands, subjects, imaginaries and researcher interpretation.

The paper's broader vocabulary remains richer than these six labels. In particular, techno-optimism, singularitarianism, transhumanism, effective accelerationism, existential-risk discourse, Critical AI perspectives, labour/creative resistance and opposition to particular AI deployments should not be collapsed mechanically into fixed boxes.

## Current candidate signifiers and motifs

The public AI26 codebook should evolve with the research situation while preserving conceptual continuity. As of 2026-09-16, useful candidate signifiers/context cues include:

- core: `artificial intelligence`, `AGI`, `AI safety`, `AI regulation`, `risk`, `progress`, `innovation`, `economic growth`, `abundance`, `human flourishing`, `stagnation`, `deceleration`, `existential risk`
- governance/pacing: `safety`, `pacing`, `competition`, `control`, `liability`, `independent evaluation`, `standards`, `regulation`, `national security`, `China`
- political economy: `labour`, `job displacement`, `automation`, `ownership`, `market power`, `Big Tech`, `public interest AI`, `open source`, `data centres`, `energy`, `environment`
- critical/resistance: `surveillance`, `data extraction`, `copyright`, `creative work`, `discrimination`, `democracy`, `public control`, `pause`
- future imaginaries: `post-work society`, `postcapitalism`, `fully automated luxury communism`, `technological singularity`, `cyborg`, `humanity`, `extinction`

These are retrieval/analysis hints only. Frequency does not establish a nodal point; semantic ambiguity does not establish floating or empty signification; negative language does not establish antagonism; sentiment does not establish affective investment.

## Why the September 2026 update matters

Recent public debate has sharpened a relational conflict around frontier-AI pacing. Dario Amodei has argued for coordinated pacing, independent evaluation and shared safety mechanisms, while Mark Zuckerberg and Jensen Huang have publicly emphasized competitive incentives, innovation and company-level responsibility. OpenAI, Anthropic and Google DeepMind have also reportedly discussed forms of safety coordination.

For AI26 this is not a reason to create a new ideology label. It is a reason to track how `safety`, `pacing`, `competition`, `innovation`, `China`, `control`, `liability`, `independent evaluation` and `regulation` are articulated by different actors over time. Organizations must not be frozen into one formation merely because of a single intervention.

## Public/private boundary

Public repositories may contain:

- project and arena schemas;
- public conceptual codebooks;
- named public organizations/actors already part of the research design;
- public URLs/source-family examples;
- synthetic fixtures;
- example prompts and secret-free runtime profiles;
- documentation of sampling logic and methodological provenance.

Keep private or ignored:

- credentials, cookies, tokens and browser profiles;
- private MongoDB/Redis/S3 endpoints and infrastructure identifiers;
- machine-specific absolute paths and secrets;
- private/non-public source lists or researcher watch lists;
- raw collected records and copyrighted media copies;
- researcher notes, annotations and review databases not intended for publication.

The rule is therefore **public methodology, private operations/data** rather than "all study configuration must be private".

## Module mapping

- `LaclauGPT-Data-Collection`: public AI26 study/arena/source-family examples and collection metadata.
- `LaclauGPT-Data-Analysis`: public AI26 codebook, formations, theory-sensitive prompt/context examples and validation semantics.
- `LaclauGPT-Data-Visualization`: public AI26 dashboard/filter/view semantics, while consuming canonical records rather than hard-coding AI26 fields.

Agents should use AI26 as the first realistic example when documenting or testing cross-module behavior, but every public API must continue to support other studies such as EP24, Brazil26 and future projects.
