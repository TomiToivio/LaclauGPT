# Full-system installation

## Clone everything

```bash
git clone --recurse-submodules https://github.com/TomiToivio/LaclauGPT.git
cd LaclauGPT
```

For an existing checkout:

```bash
git submodule update --init --recursive
```

## One shared Python environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e modules/data-collection
pip install -e modules/data-analysis
pip install -e modules/data-visualization
```

Install optional extras from the individual module README files only when needed. Heavy NLP/topic-model dependencies and distributed storage clients are intentionally optional.

## Local-first profile

Start locally before adding infrastructure. Prefer:

- CSV or SQLite for tabular/record data
- local directories for artifacts/media/exports
- in-memory/local cache where applicable
- synthetic or explicitly authorized research inputs

Each module documents its own environment variable names and safe example configuration.

## Distributed profile

For server/HPC/distributed operation, modules may use:

- MongoDB for shared records/documents
- Redis for cache/coordination
- S3-compatible object storage, including CSC Allas, for artifacts and media

Credentials and private endpoints must be supplied outside Git through environment variables, deployment tooling or a secret manager.

## Standalone installation

You do not need this meta-repository when using only one module. Clone the desired module and install it independently with its documented `pyproject.toml` extras.

## Updating pinned modules

```bash
git submodule update --remote modules/data-collection
git submodule update --remote modules/data-analysis
git submodule update --remote modules/data-visualization
```

Review and commit the changed gitlinks deliberately. A meta-repo commit should make clear which module revisions it pins.
