# Hermes operations skill

Use this skill when Hermes performs public-repository maintenance, scheduled repository review, installation health checks, bounded repairs/restarts, or cron/agent operations for LaclauGPT.

## Authority gate

Before taking an action, classify it as:

1. **explicit user task** — directly requested by the user now; or
2. **scheduled task** — explicitly listed in a user-approved cron/systemd/Slurm/agent job; or
3. **observation only** — information needed to execute 1 or 2.

Only categories 1 and 2 authorize mutations. Observation never creates authority to write, merge, restart, deploy, change data, or broaden the task. If a scheduled job says “check”, do not silently reinterpret it as “fix”. If it says “check and fix/restart”, repairs must be bounded to the named repositories/installations and validated after the change.

## Project map

Inspect these four repositories as one project while respecting ownership boundaries:

- `TomiToivio/LaclauGPT` — public paper/theory/contracts/reports/coordination.
- `TomiToivio/LaclauGPT-Data-Collection` — public collection and normalization.
- `TomiToivio/LaclauGPT-Data-Analysis` — public analysis pipeline.
- `TomiToivio/LaclauGPT-Data-Visualization` — public dashboard and researcher UI.

Storage is deployment infrastructure rather than a separate module. MongoDB, Redis, Allas/S3 and filesystem/runtime storage belong to deployments and to the modules that use them; shared storage contracts remain in the umbrella repository.

For each repository, prefer current `AGENTS.md`, `HERMES.md`, `CLAUDE.md`, `CODEX.md`, README/docs, open issues/PRs, recent commits, and CI state over memory.

For live AI26 verification, additionally load `skills/hermes-ai26-operations/SKILL.md`.

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

`LACLAUGPT_PRIVATE_ROOT` must point to an authorized private runtime/configuration root outside public working trees. Reuse an existing verified host root where one exists rather than creating a detached duplicate.

The private root may contain non-public research configuration, source/watch lists, researcher overlays/codebooks, notes, machine-specific non-secret deployment configuration, private dashboard/RAG presets, operational manifests, private health reports and suitable private artifacts according to the installation's storage policy.

Raw credentials still do **not** belong in ordinary Git history. Passwords, tokens, SSH keys, cookies, authenticated service URIs, Redis secrets, Allas/OpenStack credentials and similar material must remain in ignored/protected runtime env/secret files or another approved secrets mechanism.

A conceptual layout is:

```text
$LACLAUGPT_PRIVATE_ROOT/
  projects/ai26/collection/
  projects/ai26/analysis/
  projects/ai26/visualization/
  projects/ai26/shared/
  operations/laskin/
  operations/hermes/
  reports/private/
  runtime/          # normally ignored
  secrets/          # ignored/protected
```

Run `python tools/hermes/private_root.py check` before accessing private state. Never symlink or copy private material into a public repository.

## Scheduled repository check

A user-approved cron job may ask Hermes to review the project repositories. For each repository:

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

Installation-specific knowledge belongs in a private manifest under the authorized private root, for example:

`$LACLAUGPT_PRIVATE_ROOT/operations/hermes/installations.yaml`

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

For AI26, process existence alone is insufficient. Use `skills/hermes-ai26-operations/SKILL.md` to require recent Collection -> storage infrastructure -> Analysis -> Visualization evidence and dashboard freshness before reporting `HEALTHY`.

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

Use a lock so two scheduled Hermes runs cannot mutate the same installation simultaneously. Scheduled jobs must use the same canonical project configuration as human runs, never a hidden analytical configuration invented by the agent. A scheduled health check is one bounded iteration, not a forever-running autonomous instruction.

## Failure policy

Fail closed on unclear authority, unsafe private-root configuration, dirty working trees before destructive operations, missing canonical instructions, or ambiguous publication safety. A failed scheduled run should leave a concise private diagnostic and avoid partial public writes when possible.