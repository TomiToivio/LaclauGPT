# Full-system installation

## Recommended workspace

Keep the meta-repository and the three implementation modules as sibling Git repositories:

```text
LaclauGPT-workspace/
├── LaclauGPT/
├── LaclauGPT-Data-Collection/
├── LaclauGPT-Data-Analysis/
└── LaclauGPT-Data-Visualization/
```

## Clone the meta-repository

```bash
git clone https://github.com/TomiToivio/LaclauGPT.git
cd LaclauGPT
```

## Clone the three peer modules

The meta-repository provides a small helper that clones only modules that are missing:

```bash
./scripts/bootstrap-modules.sh
```

You can also clone each repository manually beside `LaclauGPT`.

## Update modules

Use ordinary fast-forward Git pulls:

```bash
./scripts/update-modules.sh
```

The helper runs `git pull --ff-only` in each peer repository. It stops if a repository is missing or Git cannot update it safely. It does not switch branches, discard local changes, pin revisions or manage release versions.

## One shared Python environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -U pip
./scripts/install-modules.sh
```

The install helper performs editable installs of the three sibling repositories into the active Python environment.

Install optional extras from the individual module README files only when needed. Heavy NLP/topic-model dependencies and distributed storage clients are intentionally optional.

## Local-first profile

Start locally before adding infrastructure. Prefer CSV or SQLite for tabular/record data, local directories for artifacts/media/exports, in-memory/local cache where applicable, and synthetic or explicitly authorized research inputs.

Each module documents its own environment variable names and safe example configuration.

## Distributed profile

For server/HPC/distributed operation, modules may use MongoDB for shared records/documents, Redis for cache/coordination, and S3-compatible object storage including CSC Allas for artifacts and media.

Credentials and private endpoints must be supplied outside Git through environment variables, deployment tooling or a secret manager.

## Standalone installation

You do not need this meta-repository when using only one module. Clone the desired module and install it independently with its documented `pyproject.toml` extras.

## Scope of the workspace helpers

The current helper scripts intentionally stay small. They do not provide commit lockfiles, coordinated release versions, shared configuration, Docker orchestration, branch switching or deployment management. Those concerns can be added later if the project stabilizes enough to justify them.
