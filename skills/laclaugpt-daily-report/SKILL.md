# LaclauGPT daily public report skill

Use this skill for the user-approved daily public LaclauGPT research and development report. The report is written to `docs/reports/YYYY-MM-DD.md` in the main public repository.

## Inputs to inspect each run

Review the current public state of:

1. `TomiToivio/LaclauGPT`
2. `TomiToivio/LaclauGPT-Data-Collection`
3. `TomiToivio/LaclauGPT-Data-Analysis`
4. `TomiToivio/LaclauGPT-Data-Visualization`

For all four, inspect relevant recent commits, open issues/PRs, CI/test status, unresolved review discussion and important documentation changes. Search before creating duplicate work.

Also read the current `paper/PAPER.md`, `THEORY.md`, AI26 reference material, the previous daily report when available, and new entries in `sources/`.

## Research/news scan

Search current public sources for:

- important AI/AGI/LLM developments relevant to AI26;
- policy, labour, protest, civil-society, industry/lab and online-discourse developments that may affect AI26 signifiers/formations;
- new peer-reviewed papers and credible preprints relevant to AI26 theory, discourse analysis, Critical AI Studies, AI governance, accelerationism, x-risk/doomerism, labour, political economy and sociotechnical imaginaries;
- methodological developments relevant to LLM-assisted qualitative/discourse analysis, multimodal analysis, NLP/social data science and evidence-linked human-in-the-loop research.

Prefer primary scientific sources, official documents and high-quality journalism. Record publication/event dates. Distinguish source facts from interpretation. Do not predict electoral outcomes, endorse political actors, or turn external ideological labels into automatic classifications.

When a substantial new scientific source is genuinely relevant, update publication-safe literature files according to `sources/README.md`: normally `sources/SOURCES.md`, `sources/SUMMARIES.md`, and/or `sources/READING_SUGGESTIONS.md`. Summaries must be concise, source-grounded, and copyright-safe.

## Paper review

Comment on meaningful changes, tensions, omissions or implications in `paper/PAPER.md`; do not rewrite the paper unless separately authorized. Check whether repo implementation/documentation is drifting from the paper's theoretical and methodological claims.

Pay special attention to category errors the project already guards against, including treating graph centrality as a nodal point, sentiment as antagonism, embedding similarity as ideological identity, model confidence as substantive validity, or codebook/context material as source evidence.

## Required report structure

Use a compact but substantial structure such as:

- title/date and publication-safety statement;
- high-signal developments across the four public repos;
- theory and paper alignment;
- AI26 research/news and discourse-trend watch;
- new scientific literature/methods;
- tooling/interoperability watch when material;
- concrete next actions supported by evidence;
- signal-versus-noise summary.

The report should identify changes since the previous report when possible rather than merely repeating static project descriptions.

## Public-safety rules

The report is public. Never include row-level research data, private source/watch lists, private configuration, credentials, endpoints, private machine/host information, private installation state, researcher notes, unpublished annotations, or content copied from private corpora.

If a repository problem can only be explained with private operational detail, publish only the sanitized public symptom and keep the diagnostic in the private Hermes log under `LACLAUGPT_PRIVATE_ROOT`.

## Authorization boundary

A daily-report schedule authorizes the read/search/summarize operations required to create or update that day's report and any explicitly included publication-safe source-summary updates. It does **not** by itself authorize fixing arbitrary issues, restarting services, merging PRs, changing deployments, editing the paper, or modifying sibling repositories. Those actions require their own explicit user instruction or scheduled authorization.

If the schedule separately authorizes “check and work on issues”, use `skills/hermes-operations/SKILL.md` and keep that action scope distinct from the report itself.