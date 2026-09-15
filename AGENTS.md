# AGENTS.md

## Scope

This repository is the LaclauGPT **project / paper meta-repository**. Keep it focused on scientific and project-level material.

### Belongs here

- `paper/` and paper-related references/material
- `THEORY.md`
- project architecture and interoperability documentation
- the project-wide canonical data-contract specification and versioning policy
- project-level privacy/reproducibility guidance
- installation/orchestration instructions for the full three-module system
- Git submodule pins for the three core modules

### Does not belong here

Do not add substantive implementation code, implementation tests, runtime configs, prompts, collectors, analysis workers, dashboards, storage adapters or module-specific developer docs to this repository.

Use the owning repository instead:

- collection/acquisition/normalization -> `TomiToivio/LaclauGPT-Data-Collection`
- NLP/LLM/statistics/discourse-analysis implementation -> `TomiToivio/LaclauGPT-Data-Analysis`
- dashboards/plots/maps/network visualization -> `TomiToivio/LaclauGPT-Data-Visualization`

## Submodules

The canonical submodule paths are:

- `modules/data-collection`
- `modules/data-analysis`
- `modules/data-visualization`

When a module changes independently, update the corresponding gitlink deliberately. Do not copy its source tree back into this repository.

## Canonical data contract

`docs/CANONICAL_DATA_CONTRACT.md` is the project-level source of truth for data semantics across Collection -> Analysis -> Visualization.

Agents working anywhere in the LaclauGPT project MUST follow these rules:

1. Use the canonical schema rather than inventing module-specific persistent record types.
2. Preserve `source_url` (or its canonical URI-like equivalent) as the stable source identity across modules and storage backends.
3. Treat CSV/Pandas, SQLite, MongoDB, JSONL, Parquet, Redis and S3/Allas as representations/adapters, not alternative schemas.
4. Keep backend IDs (`_id`, SQLite PKs, row numbers), legacy IDs (`document_id`, `video_id`, `new_id`) and derived-object IDs as aliases or local identifiers rather than replacements for source identity.
5. Add an explicit schema-version migration whenever persisted field meaning/cardinality/naming changes.
6. Add or update synthetic contract/round-trip tests in every affected implementation repository.
7. Keep legacy compatibility at adapter boundaries. Do not let numbered legacy columns or old dashboard schemas become the canonical model.
8. Preserve provenance and human-review state through serialization and storage changes.
9. Keep multimodal fields optional. Text-only records must never need fake transcript/OCR/frame values.
10. Audit older LaclauGPT/CyborgAnthropology repositories for useful code before rewriting it, while classifying private material as `PRIVATE_DO_NOT_COPY`.

The meta-repository defines the contract. Concrete Pydantic models, serializers, storage adapters and implementation tests belong in the owning module repositories.

## Privacy

Never commit research datasets, credentials, API tokens, cookies, browser profiles, SSH keys, private endpoints, project-private codebooks, local `.env` files, generated outputs, researcher notes/review databases, real transcripts/OCR/frames, target/account/source lists, or machine-specific deployment settings.

Public examples and schema fixtures must be synthetic and contain placeholders only.

## Interoperability

Prefer stable/versioned serialized interchange records and provenance across Collection -> Analysis -> Visualization. Avoid coupling modules through private/internal Python imports.

Local-first operation should remain possible without MongoDB, Redis or S3. Distributed backends are optional deployment choices and MUST NOT alter record semantics.

## Validation

Top-level CI should validate meta-repository integrity only: submodule presence/pins, documentation structure and lightweight installation metadata. Full unit/integration and storage round-trip suites belong to the module repositories.
