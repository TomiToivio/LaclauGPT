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

This repository coordinates theory/paper, public research documentation, project-wide contracts, literature/source curation and submodule architecture. Implementation belongs in Data Collection, Data Analysis, Data Visualization or Social Simulation Laboratory according to responsibility.

## Research capabilities

Agents may review theory/methodology, maintain literature indexes/summaries, compare current public research and project assumptions, audit module interoperability/privacy, prepare implementation issues, and identify contradictions between paper, codebooks, schemas and runtime docs.

Always distinguish external source claims from LaclauGPT interpretation and from model-generated/computational outputs. Preserve uncertainty and human review.

## AI26

AI26 is the canonical realistic public reference case. Public methodology/codebooks/source-family examples are allowed; private operations/data remain private. Formation labels and candidate signifiers are sensitising/reproducibility aids, not automatic actor identities or conclusions.

## Cross-module routing

- acquisition/normalization -> Data Collection
- NLP/LLM/statistics/discourse analysis -> Data Analysis
- dashboards/maps/plots/review UI -> Data Visualization
- simulations/agent-society experiments -> Social Simulation Laboratory

Storage (MongoDB, Redis, S3-compatible object storage) is deployment infrastructure owned by the module that uses it, not a separate repository. Do not duplicate sibling implementations in the umbrella repository.

For the current public four-repository operational surface, Hermes must know and inspect `TomiToivio/LaclauGPT`, `TomiToivio/LaclauGPT-Data-Collection`, `TomiToivio/LaclauGPT-Data-Analysis`, and `TomiToivio/LaclauGPT-Data-Visualization` while still routing implementation to the owning repository.

## Hermes operations and schedules

When Hermes is asked to perform repository operations, installation health checks, scheduled maintenance, or the daily public report, also load the specialized skills:

- `skills/hermes-operations/SKILL.md`
- `skills/hermes-cron/SKILL.md`
- `skills/laclaugpt-daily-report/SKILL.md`

Hermes may mutate state only when explicitly instructed by the user or when the exact mutation is authorized by a user-approved schedule. A scheduled check is not blanket autonomy.

Private research/operational material must live outside public working trees under `LACLAUGPT_PRIVATE_ROOT`. Run `python tools/hermes/private_root.py check` before tasks that require private state. Never publish private research data, row-level records, researcher notes, operational source/watch lists, credentials, private endpoints, host-specific deployment details, `.env` values, or confidential installation state.

## Literature workflow

Use `sources/` for publication-safe bibliographic indexing, analytical summaries and reading suggestions. Do not commit PDFs/full extracted text. Verify bibliographic details and keep source claims distinct from project interpretation.

## Privacy and quality

Never publish credentials, private endpoints, source/watch lists, row-level research data, annotations or machine-specific operational state. Preserve the canonical data contract across modules. Report inconsistencies explicitly and route implementation fixes to the owning module.

When a change touches a shared contract, or when you need to establish whether the modules still agree with each other, load `skills/cross-module-contracts/SKILL.md`. A green per-module test suite is not evidence of cross-module conformance: run the repository verifier (`python scripts/verify_cross_module_fixture.py`) and each affected module's `python tools/verify_contracts.py`.