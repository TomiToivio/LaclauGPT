# Hermes operations skill

Use this skill when Hermes performs public-repository maintenance, scheduled repository review, installation health checks, bounded repairs/restarts, or cron/agent operations for LaclauGPT.

## Authority gate

Before taking an action, classify it as:

1. **explicit user task** — directly requested by the user now; or
2. **scheduled task** — explicitly listed in a user-approved cron/systemd/Slurm/agent job; or
3. **observation only** — information needed to execute 1 or 2.

Only categories 1 and 2 authorize mutations. Observation never creates authority to write, merge, restart, deploy, change data, or broaden the task. If a scheduled job says “check”, do not silently reinterpret it as “fix”. If it says “check and fix/restart”, repairs must be bounded to the named repositories/installations and validated after the change.

## Public project map

Inspect these four public repositories as one project while respecting ownership boundaries:

- `TomiToivio/LaclauGPT` — paper/theory/contracts/reports/coordination.
- `TomiToivio/LaclauGPT-Data-Collection` — collection and normalization.
- `TomiToivio/LaclauGPT-Data-Analysis` — analysis pipeline.
- `TomiToivio/LaclauGPT-Data-Visualization` — dashboard and researcher UI.

For each repository, prefer current `AGENTS.md`, `HERMES.md`, `CLAUDE.md`, `CODEX.md`, README/docs, open issues/PRs, recent commits, and CI state over memory.

## Publication-safety gate

Before **every** public GitHub write:

- inspect the proposed diff/comment/report for research records, excerpts from private corpora, unpublished annotations and researcher notes;
- remove secrets, tokens, connection strings, private endpoints, hostnames, cookies, browser state, SSH material and `.env` values;
- remove private source/watch lists and operational collection targets;
- remove machine-specific paths or installation details that expose private infrastructure;
- use synthetic/public-safe examples instead of private records;
- cite or link public sources rather than copying private source material;
- verify that no generated logs or stack traces contain credentials or private URLs.

If uncertain whether something is public, treat it as private.

## Private state

Private operational and research material must live outside public working trees under `LACLAUGPT_PRIVATE_ROOT`.

Suggested layout:

```text
$LACLAUGPT_PRIVATE_ROOT/
  research/       # corpora, row-level records, private annotations
  config/         # project/arena/machine/execution configuration
  credentials/    # secrets and auth material
  deploy/         # host-specific systemd/cron/Slurm/SSH details
  logs/           # private operational logs
  hermes/         # schedule state, run manifests, local agent notes
  backups/        # protected backups, when appropriate
```

Run `python tools/hermes/private_root.py check` before accessing private state. Never commit, symlink, or copy this directory into a public repository.

## Scheduled public-repository check

A user-approved cron job may ask Hermes to review the four public repositories. For each repository:

1. fetch/pull only when allowed by the local installation policy;
2. inspect recent commits, open issues/PRs, unresolved review discussion and CI/test status;
3. identify concrete actionable regressions, gaps or stale documentation;
4. work on an issue only when the schedule explicitly authorizes issue work and the issue is unambiguously in scope;
5. do not create duplicate issues: search existing open/closed issues first;
6. make minimal changes in the owning repository;
7. run the repository-prescribed tests/linters;
8. report what changed, what remains broken and any validation not performed.

Do not merge PRs, close issues, or publish new issues merely because they exist. Those are mutations and require explicit task/schedule authority.

## Installation health check and bounded repair

Installation-specific knowledge belongs in a private manifest, for example:

`$LACLAUGPT_PRIVATE_ROOT/hermes/installations.yaml`

The public repo may document the schema but must not contain actual hosts, usernames, credentials, private paths or endpoints.

A private installation entry may define:

- logical installation name;
- repository path(s);
- allowed read-only health commands;
- expected services/processes;
- allowed restart command(s);
- allowed repair command(s);
- post-repair validation command(s);
- whether restart/repair is authorized for scheduled execution.

Health workflow:

1. verify the private-root safety gate;
2. inspect repository cleanliness before modifying anything;
3. run only declared health checks;
4. collect minimal diagnostic output, keeping it private;
5. if healthy, stop;
6. if unhealthy and repair is **not** authorized, report only;
7. if repair is authorized, prefer the smallest reversible fix;
8. restart only the named service/process when necessary and authorized;
9. rerun health and validation checks;
10. never discard uncommitted researcher work, rewrite history, rotate credentials, delete data, or change infrastructure topology unless explicitly instructed.

## Cron discipline

Scheduled jobs should be deterministic and auditable. Private cron configuration should record:

- task name and exact allowed actions;
- repositories/installations in scope;
- cadence/timezone;
- whether writes are allowed;
- whether issue work is allowed;
- whether restart/repair is allowed;
- output/report destination;
- timeout and lock/concurrency behavior;
- last-run status.

Use a lock so two scheduled Hermes runs cannot mutate the same installation simultaneously. Scheduled jobs must use the same canonical project configuration as human runs, never a hidden analytical configuration invented by the agent.

## Failure policy

Fail closed on unclear authority, unsafe private-root configuration, dirty working trees before destructive operations, missing canonical instructions, or ambiguous publication safety. A failed scheduled run should leave a concise private diagnostic and avoid partial public writes when possible.