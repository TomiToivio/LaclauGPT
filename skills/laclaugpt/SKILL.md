# LaclauGPT umbrella agent skill

Use this skill when an agent operates the LaclauGPT umbrella/meta repository. The agent may act as a research coordinator, academic research assistant, literature-review agent, theory/methodology assistant, project architect, data steward, interoperability auditor and documentation maintainer.

## First-read order

For AI26/project-level work, inspect:

1. `paper/PAPER.md`
2. `docs/AI26_REFERENCE_CASE.md`
3. `docs/CANONICAL_DATA_CONTRACT.md` and architecture/runtime docs
4. the owning module's current public codebooks/configuration
5. `sources/` and situation reports where relevant
6. legacy repositories only as archaeology for missing public-safe material

Current canonical files outrank model memory.

## Scope

This repository coordinates theory/paper, public research documentation, project-wide contracts, literature/source curation and submodule architecture. Implementation belongs in Data Collection, Data Analysis, Data Visualization, Data Storage or Social Simulation Laboratory according to responsibility.

## Research capabilities

Agents may review theory/methodology, maintain literature indexes/summaries, compare current public research and project assumptions, audit module interoperability/privacy, prepare implementation issues, and identify contradictions between paper, codebooks, schemas and runtime docs.

Always distinguish external source claims from LaclauGPT interpretation and from model-generated/computational outputs. Preserve uncertainty and human review.

## AI26

AI26 is the canonical realistic public reference case. Public methodology/codebooks/source-family examples are allowed; private operations/data remain private. Formation labels and candidate signifiers are sensitising/reproducibility aids, not automatic actor identities or conclusions.

## Cross-module routing

- acquisition/normalization -> Data Collection
- NLP/LLM/statistics/discourse analysis -> Data Analysis
- dashboards/maps/plots/review UI -> Data Visualization
- persistence/object/database infrastructure -> Data Storage
- simulations/agent-society experiments -> Social Simulation Laboratory

Do not duplicate sibling implementations in the umbrella repository.

## Literature workflow

Use `sources/` for publication-safe bibliographic indexing, analytical summaries and reading suggestions. Do not commit PDFs/full extracted text. Verify bibliographic details and keep source claims distinct from project interpretation.

## Privacy and quality

Never publish credentials, private endpoints, source/watch lists, row-level research data, annotations or machine-specific operational state. Preserve the canonical data contract across modules. Report inconsistencies explicitly and route implementation fixes to the owning module.