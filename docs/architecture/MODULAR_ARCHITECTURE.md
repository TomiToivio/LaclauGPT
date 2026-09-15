# Modular Architecture

LaclauGPT is split into one scientific/project meta-repository and three core implementation repositories.

```text
                 LaclauGPT
          project / paper / docs
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
 Data Collection  Data Analysis  Data Visualization
   standalone       standalone       standalone
        \             |             /
         \---- canonical record ----/
              contract/provenance
```

## Ownership

**Data Collection** owns acquisition, scraping/import, source-identity canonicalization, normalization, capture provenance, media acquisition and collection-side storage adapters.

**Data Analysis** owns NLP, embeddings, topic discovery, classical statistical baselines, LLM-assisted analysis, multimodal interpretation, codebook/context-memory integration and analysis provenance.

**Data Visualization** owns dashboards, plots, maps, graph/network views, interactive exploration, researcher review UI and presentation/export logic.

**LaclauGPT** owns the scientific paper, theory, cross-module architecture, canonical data-contract specification/versioning policy, interoperability rules, installation guidance and project-level publication/privacy policy.

The top-level repository is not a runtime dependency and must not become a fourth implementation package.

## Canonical data contract

[`../CANONICAL_DATA_CONTRACT.md`](../CANONICAL_DATA_CONTRACT.md) is the normative cross-module data specification.

The central rule is:

> **One phenomenon, one record contract, many storage adapters.**

`source_url` (or a stable URI-like equivalent when a normal URL does not exist) is the canonical source-identity anchor. Platform-native IDs and backend primary keys are aliases/local identifiers.

The module flow is:

```text
Collection
  canonicalizes source_url
  + source/content/provenance
        |
        v
CanonicalRecord vN
        |
        v
Analysis
  preserves source identity
  + evidence/analysis/provenance
        |
        v
CanonicalRecord vN
        |
        v
Visualization
  reconstructs canonical record
  -> DataFrame/view models/review UI
```

Storage choices do not change the schema:

```text
                 CanonicalRecord
               /    |    |    \
             CSV  SQLite Mongo JSONL
              |      |     |     |
              +------+-...-+-----+
                     |
             same logical record
```

Pandas is a view/transport representation, not the schema authority. MongoDB `_id`, SQLite PKs and row numbers never replace canonical source identity. Redis is coordination/cache infrastructure. S3/Allas stores referenced artifacts, not a competing record model.

## Interoperability principles

1. Modules must remain independently installable.
2. Module boundaries use documented/versioned serialized records rather than imports from another module's private implementation.
3. `source_url` / canonical source URI survives Collection -> Analysis -> Visualization.
4. Provenance, evidence references and human-review state survive transformations and storage round trips.
5. Legacy IDs (`document_id`, `video_id`, `new_id`, platform IDs) are aliases/source-native identifiers, not competing top-level identities.
6. Multimodal fields are optional. Text-only records are valid without transcript/OCR/frame placeholders.
7. Descriptive computational results remain distinguishable from theory-guided interpretive claims and human review state.
8. Local CSV/SQLite/filesystem operation is first-class. MongoDB, Redis and S3-compatible object storage are optional distributed backends.
9. Storage adapters reconstruct the same canonical object before module-specific semantics are applied.
10. Public repositories contain no real research data, private configuration or secrets.

## Schema evolution

The canonical record carries `schema_version`.

Any persisted semantic change requires:

- an explicit version change;
- a migration note;
- synthetic compatibility fixtures;
- round-trip/contract tests in affected implementation repositories;
- updated public documentation.

Legacy mappings stay at module boundaries rather than leaking historical field names into new core APIs.

The project-level migration inventory is [`../CANONICAL_DATA_MIGRATION_INVENTORY.md`](../CANONICAL_DATA_MIGRATION_INVENTORY.md).

## Dependency policy

The meta-repository may pin module revisions through Git submodules but does not own their Python packages. The modules should not require this meta-repository at runtime.

If a shared implementation-level schema package is introduced later, it must remain small, independently versioned and free of Collection/Analysis/Visualization business logic. Until then, modules interoperate through the documented serialized contract.

Optional research assistants, simulations and experiments may consume module outputs, but they are not core dependencies.
