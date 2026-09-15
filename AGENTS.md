# AGENTS.md

## Scope

This repository is the LaclauGPT **project / paper meta-repository**. Keep it focused on scientific and project-level material.

### Belongs here

- `paper/` and paper-related references/material
- `THEORY.md`
- project architecture and interoperability documentation
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

## Privacy

Never commit research datasets, credentials, API tokens, cookies, browser profiles, SSH keys, private endpoints, project-private codebooks, local `.env` files, generated outputs, or machine-specific deployment settings.

Public examples must be synthetic and contain placeholders only.

## Interoperability

Prefer stable/versioned serialized interchange records and provenance across Collection -> Analysis -> Visualization. Avoid coupling modules through private/internal Python imports.

Local-first operation should remain possible without MongoDB, Redis or S3. Distributed backends are optional deployment choices.

## Validation

Top-level CI should validate meta-repository integrity only: submodule presence/pins, documentation structure and lightweight installation metadata. Full unit/integration suites belong to the module repositories.
