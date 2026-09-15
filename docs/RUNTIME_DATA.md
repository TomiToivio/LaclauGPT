# Project-wide runtime data contract

All LaclauGPT modules use a repository-local `data/` directory as the single local runtime boundary. The entire tree is excluded from Git.

Recommended private layout for each implementation module:

```text
data/
  logs/
  database/
  config/
  files/
  csv/
  jsonl/
  codebooks/
  sources/
  downloads/
  media/
  models/
    ollama/
    whisper/
  cache/
  tmp/
  exports/
  artifacts/
  runs/
  browser/
  transcripts/
  frames/
```

Git does not track empty directories, so modules create these directories at runtime rather than committing `.gitkeep` files under `data/`.

## Local single-machine topology

When the repositories are siblings on one machine, the preferred local flow is:

```text
LaclauGPT-Data-Collection/data/
        ↓ direct configured filesystem access
LaclauGPT-Data-Analysis/data/
        ↓ direct configured filesystem access
LaclauGPT-Data-Visualization/data/
```

Analysis may read canonical Collection records/files directly from Collection's private `data/` tree. Visualization may read canonical Analysis results directly from Analysis's private `data/` tree. These paths are runtime configuration, never committed machine-specific constants.

## Distributed topology

For distributed execution, the preferred transport is:

- MongoDB for canonical records and queryable metadata
- Redis for coordination, queue/cache/state where needed
- S3-compatible object storage, including CSC Allas, for files, media and large artifacts

The backend must not change canonical record semantics.

## Manual transfer fallback

CSV and JSONL remain supported interoperability formats. A researcher can explicitly export from one module's `data/exports/` or `data/csv/` and import into the next module's private `data/` tree.

## What always belongs under data/

Runtime logs, SQLite databases, real local configuration, real source/target lists, study codebooks, CSV/JSONL corpora, downloaded files, media, transcripts, sampled frames, researcher exports, caches, temporary state, local Ollama material, Whisper model caches and other generated/model artifacts belong under `data/`.

Public templates, schemas, documentation and synthetic tests belong outside `data/` and must not depend on private runtime material.
