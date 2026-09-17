# Public code, private studies

This document defines the project-wide boundary between reusable public LaclauGPT engineering and restricted study material. It closes the architecture/documentation part of issue #23 and is the governing convention for EP24, Hungary26 and future restricted projects.

## Rule

> **Public code, private studies.**

Reusable implementation belongs in the public module that owns the capability. Study data, researcher material, private operational values and unpublished outputs stay outside public Git history.

## Public repository layout

Each public module should follow this shape where applicable:

```text
config/examples/*.yaml          # placeholders and synthetic examples only
src/...                         # generic reusable implementation
tests/fixtures/                 # synthetic/minimal public fixtures only
docs/...                        # public-safe operator and architecture docs
```

A private study repository or controlled runtime may provide:

```text
config/studies/<study>/*.yaml
codebooks/
secrets/.env
runtime/data/
runtime/output/
```

Public code may reference private configuration through CLI arguments or environment variables such as `LACLAUGPT_PRIVATE_CONFIG`, `LACLAUGPT_DATA_DIR` and study-specific runtime paths. Public imports, tests and CI must never require those private files.

## What may be public

- generic dashboards and researcher-facing components
- canonical-data and legacy-boundary adapters
- generic local/MongoDB/Redis/S3-compatible storage adapters
- generic CSC Roihu/SLURM orchestration
- chunking, resume, retry and validation logic
- model/Ollama routing
- canonical and researcher export generation
- generic summary generation
- schema and configuration examples containing placeholders only
- synthetic fixtures and tests
- documentation that explains how a private study plugs into a public module

## What must remain private

- row-level research data or media
- researcher notes, workbooks and annotations
- country/study-specific codebooks derived from private research material
- private prompt/context material
- source/watch lists when restricted
- credentials, cookies, tokens and secrets
- private URLs/endpoints
- CSC usernames, project identifiers and absolute user/project paths
- sensitive Allas bucket/container identifiers
- unpublished outputs and private run manifests

If a historical file mixes generic implementation with restricted values, refactor it rather than copying it verbatim.

## Module ownership

### LaclauGPT-Data-Analysis

Owns reusable processing and execution infrastructure, including restricted-project reprocessing, Roihu/SLURM profiles, storage and path abstractions, model routing, resume/retry, validation, legacy-field preservation and researcher-readable exports.

Current maintained public implementations include the EP24 reprocessing harness, generic restricted-project Roihu workflow and Hungary26 Roihu documentation. Study-specific values remain in the private study layer.

### LaclauGPT-Data-Visualization

Owns reusable dashboards, canonical/legacy view adapters, researcher record inspection, filtering/search/export and synthetic fixtures. Legacy EP24-derived specialized dashboards are handled through explicit boundary adapters instead of leaking historical schemas into core models.

### LaclauGPT

Owns this cross-module publication/privacy convention and the architecture contract. It does not duplicate Analysis or Visualization implementation code.

## Restricted study runtime pattern

A public profile may be as small as:

```yaml
study:
  id: ${LACLAUGPT_STUDY_ID}
  private_config: ${LACLAUGPT_PRIVATE_CONFIG}

execution:
  machine: roihu
  scheduler: slurm

storage:
  backend: local_or_s3
```

The actual study values live in a private repository, ignored local configuration, deployment secret store or controlled runtime filesystem.

## Migration inventory for EP24 / Hungary26

The following inventory records the relevant implementations found while resolving issue #23. Paths in private repositories are listed for audit/provenance only and must not be copied wholesale into public repositories.

| source repo | path | branch/commit | capability | target module | classification | reason / status |
| --- | --- | --- | --- | --- | --- | --- |
| `TomiToivio/ep2024_postprocess` | `dashboard/dashboard-laptop.py` | historical default branch | researcher EP24 dashboard | Data Visualization | rewrite | legacy UI/inspection ideas are reusable, but historical implementation contains study-specific assumptions and contact/runtime details |
| `TomiToivio/ep2024_postprocess` | `dashboard/dashboard-populism.py` | historical default branch | EP24 dashboard variant | Data Visualization | rewrite | preserve useful UX patterns only through canonical/legacy boundary adapters |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | `laclaugpt/visualization/ep24_dashboard.py` | private main snapshot audited 2026-09-17 | EP24 compatibility dashboard | Data Visualization | rewrite/reference | compatibility behavior is useful; private study bindings remain restricted |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | `KEEP_PRIVATE/ep24/dashboard.py` | private main snapshot audited 2026-09-17 | canonical re-analysis dashboard | Data Visualization | private/reference | private runtime and EP24 bindings; public Visualization should consume canonical contracts instead |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | `KEEP_PRIVATE/ep24/dashboard_researcher.py` | private main snapshot audited 2026-09-17 | researcher inspection/review dashboard | Data Visualization | rewrite | useful inspection/review workflow, but country mappings, runtime paths and review storage are study-specific |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | `KEEP_PRIVATE/ep24/dashboard_reanalysis.py` | private main snapshot audited 2026-09-17 | earlier re-analysis dashboard | Data Visualization | archive/reference | retained only as historical fallback; do not revive as a second public schema |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | `KEEP_PRIVATE/ep24/pledge_dashboard/` | private main snapshot audited 2026-09-17 | specialized pledge dashboard | Data Visualization | rewrite/archive | superseded publicly by legacy specialized dashboard adapters and synthetic fixtures |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | `scripts/ep24/run_reanalysis_dashboard.sh` | private main snapshot audited 2026-09-17 | dashboard launcher | Data Visualization | private/reference | launcher binds private repo/data paths; public module should expose generic entry points |
| `TomiToivio/LaclauGPT-Data-Visualization` | `docs/LEGACY_SPECIALIZED_DASHBOARDS.md` and associated `scripts/legacy/`, `web/legacy/`, tests | current `main` | generalized legacy EP24-derived dashboards | Data Visualization | public | maintained public-safe replacement using deterministic adapters, provenance and synthetic fixtures |
| `TomiToivio/LaclauGPT-Data-Visualization` | `docs/UNIFIED_DASHBOARD.md` and current application/runtime layers | current `main` | unified researcher dashboard | Data Visualization | public | canonical visualization architecture; preferred destination for reusable EP24 inspection features |
| `TomiToivio/LaclauGPT-Data-Analysis` | `src/laclaugpt_data_analysis/ep24_reprocessing.py` | current `main` | EP24 reprocessing logic | Data Analysis | public | maintained privacy-safe reusable implementation with private grounding supplied at runtime |
| `TomiToivio/LaclauGPT-Data-Analysis` | `scripts/ep24/ep24_roihu_reprocess.sbatch` | current `main` | CSC Roihu EP24 batch harness | Data Analysis | public | contains no project IDs/private paths/data and requires runtime-supplied restricted values |
| `TomiToivio/LaclauGPT-Data-Analysis` | `scripts/ep24/run_country_reprocess.sh` | current `main` | country/study reprocessing wrapper | Data Analysis | public | private codebook/runtime paths are supplied externally |
| `TomiToivio/LaclauGPT-Data-Analysis` | `docs/ep24-reprocessing.md`, `docs/EP24_ISSUE99_ROIHU.md` | current `main` | EP24 Roihu operator docs | Data Analysis | public | documents explicit restricted-data boundary |
| `TomiToivio/LaclauGPT-Data-Analysis` | `src/laclaugpt_data_analysis/reprocessing.py`, `scripts/roihu/`, `config/examples/roihu_reprocessing.example.yaml` | current `main` | generic restricted-project reprocessing | Data Analysis | public | reusable engine/templates for EP24, Hungary26 and later studies |
| `TomiToivio/LaclauGPT-Data-Analysis` | `docs/RESTRICTED_ROIHU_REPROCESSING.md` | current `main` | public/private Roihu deployment contract | Data Analysis | public | generic execution contract with private project binding outside Git |
| `TomiToivio/LaclauGPT-Data-Analysis` | `docs/HUNGARY26_ROIHU.md` | current `main` | Hungary26 Roihu migration notes/operator guidance | Data Analysis | public | records reusable processing design while keeping Hungary26 grounding private |
| `TomiToivio/LaclauGPT-Data-Analysis` | `docs/study-deployments.md` | current `main` | EP24/Hungary26 deployment examples | Data Analysis | public | uses placeholders/environment variables rather than embedded restricted identifiers |
| `TomiToivio/LaclauGPT-Discourse-Analysis-Private` | EP24 Finland/Poland codebooks and researcher material under private study paths | private main | study grounding | private study layer | private | derived from researcher material and must not be promoted into public repos |
| private Hungary26 research/runtime material | study-specific paths in private repositories / controlled runtime | private | Hungary26 grounding/data/config | private study layer | private | codebooks, prompts, source lists, paths, identifiers, data and unpublished outputs remain restricted |

## Security checklist before publication

Before moving any historical/private implementation into a public module:

1. inspect for credentials, cookies, tokens and private endpoints;
2. remove CSC usernames, project identifiers and absolute machine/project paths;
3. remove row-level data, media and private data samples;
4. remove private codebook/prompt/context content;
5. replace operational identifiers with placeholders or environment variables;
6. replace real fixtures with synthetic fixtures;
7. keep legacy field compatibility at the boundary, not in core models;
8. inspect the complete diff before merge;
9. confirm public tests/CI run without access to private repos or data.

## Acceptance-state note

As of 2026-09-17, the reusable EP24 and Hungary26 execution/dashboard architecture has already been substantially migrated into the dedicated Analysis and Visualization repositories. Issue #23 therefore should not trigger a second wholesale copy from the private repositories. The remaining project-level responsibility is to keep the inventory and the public/private contract explicit, and to migrate only specific missing capabilities discovered by future audits.
