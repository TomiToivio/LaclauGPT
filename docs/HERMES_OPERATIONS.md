# Hermes operations, private state, and scheduled maintenance

This document defines the public contract for running Hermes against the LaclauGPT project. It intentionally contains no real hostnames, usernames, credentials, private paths, source lists, or infrastructure endpoints.

## Public project surface

Hermes treats these as the four public LaclauGPT repositories:

| Repository | Public responsibility |
| --- | --- |
| `TomiToivio/LaclauGPT` | paper, theory, cross-module contracts, public reports, literature workspace, project/agent documentation |
| `TomiToivio/LaclauGPT-Data-Collection` | collection/acquisition, normalization, collection runtime |
| `TomiToivio/LaclauGPT-Data-Analysis` | multimodal/NLP/LLM/statistical/discourse analysis |
| `TomiToivio/LaclauGPT-Data-Visualization` | dashboards, plots/maps/graphs and researcher-facing UI/control plane |

The main repository coordinates the project but is not a dumping ground for sibling implementation.

## Private root

Set a private root outside every public clone:

```bash
export LACLAUGPT_PRIVATE_ROOT="$HOME/.local/share/laclaugpt-private"
mkdir -p "$LACLAUGPT_PRIVATE_ROOT"/{research,config,credentials,deploy,logs,hermes,backups}
chmod 700 "$LACLAUGPT_PRIVATE_ROOT"
python tools/hermes/private_root.py check
```

On servers/HPC, use an access-controlled project/service directory appropriate to that system instead of assuming the workstation path above.

Private root contents may include research corpora, row-level data, unpublished annotations, source/watch lists, `.env` files, database/service configuration, credentials, machine/execution profiles, host-specific cron/systemd/Slurm files, installation manifests, operational logs and private agent run state.

Do not symlink the private root into a public clone. Do not paste its content into issues, PRs, logs, public reports or prompts that will be persisted publicly.

## Installation manifest

A private manifest may be kept at:

```text
$LACLAUGPT_PRIVATE_ROOT/hermes/installations.yaml
```

Example **shape only**:

```yaml
installations:
  - name: logical-name
    repositories:
      main: /private/path/to/LaclauGPT
      collection: /private/path/to/LaclauGPT-Data-Collection
      analysis: /private/path/to/LaclauGPT-Data-Analysis
      visualization: /private/path/to/LaclauGPT-Data-Visualization
    health_checks:
      - "command chosen by researcher"
    restart:
      authorized: false
      commands: []
    repair:
      authorized: false
      commands: []
    validate:
      - "post-repair validation command"
```

Never commit a real manifest. Hermes must not infer host commands or restart authority from this public example.

## Authorization model

Hermes may mutate state only because:

1. the user explicitly requested the action; or
2. the user previously approved a schedule whose private configuration explicitly includes that action.

A scheduled task has narrow authority. For example:

- “check repositories” permits inspection, not automatic fixes;
- “check and work on open issues” permits bounded issue work, but not unrelated deployments;
- “check installation and restart the dashboard if unhealthy” permits the named restart after diagnosis, but not deleting data or upgrading unrelated services;
- “write the daily public report” permits report/source-summary updates, not editing the paper or merging PRs.

## Suggested scheduled jobs

These are task definitions, not real cron lines. Keep actual scheduling details and installation paths private.

### Public repository health and issue review

Cadence: daily or as explicitly configured.

Actions:

1. inspect the four public repositories;
2. review recent commits, CI, open issues/PRs and unresolved reviews;
3. detect regressions and documentation drift;
4. when explicitly authorized, work on concrete in-scope issues in the owning repository;
5. validate changes with repository-prescribed tests;
6. keep all research/private operational data out of GitHub.

### Installation health and repair

Cadence: user-selected.

Actions:

1. run `private_root.py check`;
2. load the private installation manifest;
3. run declared health checks;
4. if unhealthy, collect a private diagnostic;
5. only if the manifest/schedule authorizes it, perform the smallest declared repair/restart;
6. rerun validation;
7. never destroy uncommitted work or research data.

### Daily LaclauGPT public report

Cadence: daily.

Actions:

1. review all four public repositories and the previous report;
2. read the current paper/theory/reference material;
3. summarize newly added public sources;
4. search fresh AI26-relevant news and scientific literature;
5. describe current AI26 discourse/trend signals with dates and sources;
6. note theory/implementation drift and high-signal next actions;
7. update `docs/reports/YYYY-MM-DD.md`;
8. update publication-safe source indexes/summaries when warranted.

Use `skills/laclaugpt-daily-report/SKILL.md` for the report contract.

## Public-write checklist

Before any GitHub write, Hermes should be able to answer **yes** to all of these:

- Is this write explicitly authorized by the current task or schedule?
- Is this the correct owning repository?
- Is every included datum already public or intentionally publication-safe?
- Are secrets, private endpoints, host details and machine paths absent?
- Are private research data, source/watch lists, annotations and researcher notes absent?
- Are logs/tracebacks sanitized?
- Is the change minimal and reproducible?
- Were appropriate tests/checks run, or are missing validations stated?

If any answer is no or uncertain, do not publish the write.

## Recovery philosophy

For operational failures, preserve evidence before repair, prefer reversible changes, validate after repair, and leave the system no worse than it was. Never use `git reset --hard`, destructive database operations, credential rotation, mass deletion, or infrastructure changes as an autonomous “fix” unless the user explicitly asked for that exact class of action.
