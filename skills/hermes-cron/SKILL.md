# Hermes cron and scheduled-operations skill

Use this skill only for a user-approved scheduled Hermes run. It defines how cron/systemd/Slurm/agent schedules translate into authority and safe execution.

## Principle

A schedule is a narrow standing instruction, not general autonomy. Perform only the named tasks, against the named repositories/installations, with the named mutation permissions.

## Required private schedule fields

Keep real schedules and host details outside public repositories, preferably under `$LACLAUGPT_PRIVATE_ROOT/hermes/`. Each scheduled task should record:

- `name`;
- `cadence` and timezone;
- `task` / exact allowed actions;
- repositories/installations in scope;
- `allow_public_writes`;
- `allow_issue_work`;
- `allow_restart`;
- `allow_repair`;
- output/report destination;
- timeout;
- lock name/path to prevent overlapping mutation runs.

Do not infer a permission that is absent or false.

## Standard jobs

### Repository watch

Read the four public repositories, recent commits, open issues/PRs, CI and review state. If `allow_issue_work` is false, stop at diagnosis/reporting. If true, work only on concrete in-scope issues and use the owning repository's agent instructions/tests.

### Installation watch

Run `python tools/hermes/private_root.py check`, then use `tools/hermes/installation_health.py <name>` for check-only operation. Use `--repair` only when both the schedule and private installation manifest authorize repair/restart. Validate after any mutation.

### Daily report

Follow `skills/laclaugpt-daily-report/SKILL.md`. The schedule authorizes updating the day's public report and explicitly allowed public source-summary files, nothing broader.

## Concurrency and failure

Use an OS-level lock or scheduler mechanism so the same scheduled mutating job cannot overlap itself. On timeout, unclear authority, dirty working tree before a destructive operation, unsafe private-root state, or failed validation, stop and leave diagnostics private. Do not compensate for a failed command with increasingly broad repairs.

## Cron environment

Cron often has a minimal environment. Explicitly set required `PATH`, project virtualenv/tool paths, `LACLAUGPT_PRIVATE_ROOT`, and other non-secret selectors through protected private configuration. Never publish a real crontab containing usernames, host paths, tokens, private endpoints or environment secrets.

## Public reporting

Scheduled diagnostics are private by default. Publish only sanitized, research-safe conclusions explicitly required by the job, such as the daily report or a user-authorized GitHub issue/comment.