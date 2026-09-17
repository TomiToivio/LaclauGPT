# Hermes operations, private state, and scheduled maintenance

This document defines the public contract for running Hermes against the LaclauGPT project. It intentionally contains no real hostnames, usernames, credentials, private paths, source lists, or infrastructure endpoints.

## Project surface

Hermes treats these as the four coordinated LaclauGPT repositories:

| Repository | Responsibility |
| --- | --- |
| `TomiToivio/LaclauGPT` | public paper, theory, cross-module contracts, public reports, literature workspace, project/agent documentation |
| `TomiToivio/LaclauGPT-Data-Collection` | public collection/acquisition, normalization, collection runtime |
| `TomiToivio/LaclauGPT-Data-Analysis` | public multimodal/NLP/LLM/statistical/discourse analysis |
| `TomiToivio/LaclauGPT-Data-Visualization` | public dashboards, plots/maps/graphs and researcher-facing UI/control plane |

Storage is deployment infrastructure rather than a separate module. MongoDB, Redis, Allas/S3 and filesystem/runtime storage belong to the deployments and modules that use them; shared storage contracts belong in this umbrella repository.

The main repository coordinates the project but is not a dumping ground for sibling implementation.

## Canonical private root

`LACLAUGPT_PRIVATE_ROOT` should point to an established private runtime/configuration root outside public working trees.

Do not create a second unrelated private tree when the host already has an authorized private root. First inspect the installation and reuse its current verified path.

A conceptual layout is:

```text
$LACLAUGPT_PRIVATE_ROOT/
  projects/
    ai26/
      collection/
      analysis/
      visualization/
      shared/
  operations/
    laskin/
    hermes/
  reports/
    private/
  runtime/          # normally ignored
  secrets/          # ignored/protected
```

The private root may hold non-public AI26 configuration, source/watch lists, researcher overlays/codebooks, notes, machine-specific non-secret deployment configuration, private dashboard/RAG presets, operational manifests, private health/status reports and suitable private artifacts under the installation's storage policy.

### Raw secrets still stay out of Git

A private repository or directory is not a secrets manager. Passwords, tokens, SSH keys, cookies, authenticated MongoDB URIs, Redis secrets, Allas/OpenStack credentials and similar values must remain in ignored/protected runtime env/secret files or another approved secrets mechanism. Tracked private configuration should refer to those secret sources without embedding them.

Do not symlink private material into a public clone. Do not paste its content into public issues, PRs, logs, reports or prompts that will be persisted publicly.

Run:

```bash
python tools/hermes/private_root.py check
```

before private-state operations. The checker must confirm that the root is not inside a public working tree and represents an authorized private location.

## Installation manifest

A private manifest should live under the private root, for example:

```text
$LACLAUGPT_PRIVATE_ROOT/operations/hermes/installations.yaml
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

Never commit a real host/path/credential manifest to a public repository. Hermes must not infer host commands or restart authority from this public example.

## Authorization model

Hermes may mutate state only because:

1. the user explicitly requested the action; or
2. the user previously approved a schedule whose private configuration explicitly includes that action.

A scheduled task has narrow authority. For example:

- “check repositories” permits inspection, not automatic fixes;
- “check and work on open issues” permits bounded issue work, but not unrelated deployments;
- “check installation and restart the dashboard if unhealthy” permits the named restart after diagnosis, but not deleting data or upgrading unrelated services;
- “write the daily public report” permits report/source-summary updates, not editing the paper or merging PRs.

## AI26 Laskin end-to-end health check

Use `skills/hermes-ai26-operations/SKILL.md` for the complete live verification contract.

A valid health check must inspect current repository/runtime state and answer whether the real AI26 pipeline is moving fresh data through:

```text
Collection -> storage infrastructure -> Analysis -> Visualization
```

The check should cover, with publication-safe evidence:

- Laskin host/runtime state and repository commits;
- scheduled collection activity and canonical `project_id=ai26`;
- MongoDB, Redis and Allas/S3 connectivity and namespace consistency;
- Analysis scheduling, queue/run freshness and configured Ollama/model reachability;
- Visualization/dashboard service and current backend freshness;
- optional RAG/DNA/RDF/GraphProjection behavior where enabled;
- one recent real production record traced across as many timestamps/provenance points as the current contracts expose.

Do not mark the system `HEALTHY` just because processes exist. `HEALTHY` requires evidence of recent end-to-end AI26 data flow plus a functioning, current dashboard. Missing observability should be reported as `UNKNOWN` or `DEGRADED` as appropriate rather than filled with invented timestamps.

Private detailed reports belong under the private root, for example `reports/private/`. A publication-safe summary may be written publicly only when the task explicitly authorizes it.

## Suggested scheduled jobs

These are task definitions, not real cron lines. Keep actual scheduling details and installation paths private.

### AI26 Laskin pipeline health

Cadence: user-selected.

Actions for one bounded iteration:

1. validate the canonical private root;
2. inspect all four repository checkouts and current revisions;
3. run the authorized read-only health checks for Collection, storage infrastructure, Analysis and Visualization;
4. trace recent real AI26 activity end-to-end where possible;
5. classify overall state as `HEALTHY`, `DEGRADED`, `BROKEN` or `UNKNOWN`;
6. write the detailed private report;
7. search existing issues before commenting/creating any defect report;
8. perform restart/repair only when the schedule explicitly authorizes it;
9. rerun validation after an authorized repair;
10. stop after the single iteration.

### Public repository health and issue review

Cadence: daily or as explicitly configured.

Actions:

1. inspect the project repositories;
2. review recent commits, CI, open issues/PRs and unresolved reviews;
3. detect regressions and documentation drift;
4. when explicitly authorized, work on concrete in-scope issues in the owning repository;
5. validate changes with repository-prescribed tests;
6. keep all research/private operational data out of public GitHub repositories.

### Daily LaclauGPT public report

Cadence: daily.

Actions:

1. review the public repositories and the previous report;
2. read the current paper/theory/reference material;
3. summarize newly added public sources;
4. search fresh AI26-relevant news and scientific literature;
5. describe current AI26 discourse/trend signals with dates and sources;
6. note theory/implementation drift and high-signal next actions;
7. update `docs/reports/YYYY-MM-DD.md`;
8. update publication-safe source indexes/summaries when warranted.

Use `skills/laclaugpt-daily-report/SKILL.md` for the report contract.

## Public-write checklist

Before any public GitHub write, Hermes should be able to answer **yes** to all of these:

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

For operational failures, preserve evidence before repair, prefer reversible changes, validate after repair, and leave the system no worse than it was. Never use `git reset --hard`, destructive database operations, credential rotation, mass deletion, or infrastructure changes as an autonomous fix unless the user explicitly asked for that exact class of action.
