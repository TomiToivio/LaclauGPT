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

## Public demo artifacts

The public reference case is intentionally concrete enough to run as a demo while keeping private operations and research data out of Git.

### Data Collection

`TomiToivio/LaclauGPT-Data-Collection` provides:

- `configs/studies/ai26.example.yaml` — public study settings, arenas, discovery vocabulary, source budgets and bounded demo targets;
- `configs/studies/ai26.collection-codebook.yaml` — collection-only sampling codebook;
- `configs/studies/ai26.sources.example.toml` — executable RSS/Atom backbone plus public web, X, Bluesky, Mastodon, YouTube and scholarly target examples.

RSS/web/scholarly material is deliberately prioritized over social volume. Social accounts are bounded examples for discursive coverage, not ideological classifications.

### Data Analysis

`TomiToivio/LaclauGPT-Data-Analysis` provides:

- `codebooks/public/seed_ai_formations.md` — human-readable methodology and vocabulary;
- `codebooks/public/ai26_v2.yaml` — machine-readable codebook for context-memory seeding;
- `docs/AI26_REFERENCE_CASE.md` — analysis profile and collection-to-analysis contract.

The machine-readable codebook contains provisional formation anchors, candidate signifiers and cross-cutting topics. It contains no private corpus-derived labels or annotations.

## Candidate signifiers and cross-cutting dimensions

Useful candidate signifiers/context cues include:

- core: `artificial intelligence`, `AGI`, `frontier AI`, `superintelligence`, `AI safety`, `risk`, `progress`, `innovation`, `economic growth`, `abundance`, `human flourishing`, `existential risk`
- governance/pacing: `pacing`, `slowdown`, `pause`, `independent evaluation`, `liability`, `standards`, `regulation`, `democratic control`
- political economy: `labour`, `automation`, `ownership`, `corporate concentration`, `public interest AI`, `open source`, `open weights`
- critical/resistance: `surveillance`, `data extraction`, `copyright`, `creator rights`, `discrimination`, `data centres`, `environment`
- geopolitical/infrastructure: `AI race`, `China`, `sovereignty`, `national security`, `compute`, `chips`, `energy`, `water`
- future imaginaries: `post-work society`, `postcapitalism`, `technological singularity`, `humanity`, `extinction`, `emancipatory automation`

These are retrieval/analysis hints only. Frequency does not establish a nodal point; semantic ambiguity does not establish floating or empty signification; negative language does not establish antagonism; sentiment does not establish affective investment.

Cross-cutting dimensions are used to avoid forcing every record into one of six formation buckets:

- political economy
- governance
- capability risk
- techno-optimism
- rights and harms
- infrastructure
- geopolitics

## Public/private boundary

Public repositories may contain:

- project and arena schemas;
- public conceptual and machine-readable codebooks;
- named public organizations/actors used as transparent demo sources;
- public URLs/source-family examples;
- synthetic fixtures;
- example prompts and secret-free runtime profiles;
- documentation of sampling logic and methodological provenance.

Keep private or ignored:

- credentials, cookies, tokens and browser profiles;
- private MongoDB/Redis/S3 endpoints and infrastructure identifiers;
- machine-specific absolute paths and secrets;
- unpublished researcher notes and annotations;
- raw collected records and copyrighted media copies;
- any operational source-selection detail that should not be published.

The rule is therefore **public methodology and demo configuration, private operations/data**.

## Module mapping

- `LaclauGPT-Data-Collection`: public AI26 study settings, collection codebook, source manifests and collection metadata.
- `LaclauGPT-Data-Analysis`: public AI26 codebooks, formations, theory-sensitive prompt/context examples and validation semantics.
- `LaclauGPT-Data-Visualization`: public AI26 dashboard/filter/view semantics, while consuming canonical records rather than hard-coding AI26 fields.

Agents should use AI26 as the first realistic example when documenting or testing cross-module behavior, but every public API must continue to support other studies such as EP24, Brazil26 and future projects.
