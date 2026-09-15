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
         \---- versioned data -----/
               contracts/provenance
```

## Ownership

**Data Collection** owns acquisition, scraping/import, normalization, capture provenance, media acquisition and collection-side storage adapters.

**Data Analysis** owns NLP, embeddings, topic discovery, classical statistical baselines, LLM-assisted analysis, multimodal interpretation and analysis-specific contracts/provenance.

**Data Visualization** owns dashboards, plots, maps, graph/network views, interactive exploration and presentation/export logic.

**LaclauGPT** owns the scientific paper, theory, cross-module architecture, interoperability rules, installation guidance and project-level publication/privacy policy.

## Interoperability principles

1. Modules must remain independently installable.
2. Module boundaries should use documented/versioned records rather than imports from another module's internal implementation.
3. Provenance identifiers and source/representation identifiers should survive transformations across module boundaries.
4. Descriptive computational results must remain distinguishable from theory-guided interpretive claims and human review state.
5. Local CSV/SQLite/filesystem operation is first-class. MongoDB, Redis and S3-compatible object storage are optional distributed backends.
6. Public repositories contain no real research data or secrets.

## Dependency policy

The meta-repository may pin module revisions through Git submodules but does not own their Python packages. The modules should not require this meta-repository at runtime.

Optional research assistants, simulations and experiments may consume module outputs, but they are not core dependencies.
