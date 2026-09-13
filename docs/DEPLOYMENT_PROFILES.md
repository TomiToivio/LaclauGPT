# Deployment profiles

LaclauGPT is one codebase deployed in several runtime topologies. Research semantics stay in the project/arena layers; infrastructure and orchestration change by machine/execution profile.

Canonical chain:

`project -> arena/dataset -> machine -> execution -> effective run config -> run`

The deployment profiles below are deliberately modular. Collection, analysis, LLM access, Context Memory, visualization and Slurm execution are not assumed to live on the same host.

> The profiles committed here are **public templates**, not production deployment records. Concrete model names, providers, endpoints, hostnames, ports, storage paths, credentials, schedules and allocation-specific settings belong in private or machine-local configuration.

## Supported profiles

| Environment | Machine profile | Execution profile | Collector | Analysis | LLM | Dashboard | Slurm |
|---|---|---|---:|---:|---|---:|---:|
| Laptop collector | `laptop-collector` | `collector-only` | yes | no | none | no | no |
| Laptop local analysis | `laptop-ollama` | `local-analysis` | no by default | yes | runtime-selected local model | no by default | no |
| Laptop cloud analysis | `laptop-cloud` | `cloud-analysis` | no by default | yes | runtime-selected cloud model | no by default | no |
| Linux dashboard | `linux-dashboard` | `dashboard-only` | no | no | none | yes | no |
| Linux GPU realtime | `linux-gpu-realtime` | `realtime-fullstack` | yes | yes | runtime-selected local model | yes | no |
| Slurm/HPC analysis | `roihu` | `slurm` | no | yes | runtime-selected local model | no | yes |

Model/provider values in public profiles are placeholders. Operational selections must be supplied outside the public repository without changing the project or arena definition.

## 1. Laptop: browser collector only

Use a laptop for researcher-driven browser collection without installing or starting an analysis model or dashboard.

```bash
laclaugpt profiles
# collector is launched through collector/ using the laptop-collector infrastructure profile
```

The collector writes to configured research storage. Collection can later be consumed by analysis on another machine through the canonical source/interchange conventions.

## 2. Laptop: local or cloud-assisted analysis

For a low-resource local run:

```bash
laclaugpt analyze my_corpus.csv \
  --project ai26 --arena elites \
  --machine laptop-ollama --execution local-analysis
```

The local model is supplied through runtime or machine-local configuration.

For cloud-assisted analysis:

```bash
laclaugpt analyze my_corpus.csv \
  --project ai26 --arena elites \
  --machine laptop-cloud --execution cloud-analysis
```

Cloud provider/model selection, credentials and endpoints must come from runtime/environment configuration and must not be committed.

## 3. Linux web server: dashboard only

Use `linux-dashboard` + `dashboard-only` when the host only serves visualization and researcher review.

```bash
laclaugpt dashboard data/annotations.jsonl --project ai26 --arena elites
```

This profile must not require an LLM or collector dependencies. Production HTTP binding, TLS, authentication and reverse proxy configuration stay outside research semantics and outside the public repository.

## 4. Linux GPU server: realtime full stack

Use `linux-gpu-realtime` + `realtime-fullstack` as the public template for a persistent installation where collector, analysis and dashboard are colocated.

The profile enables:

- collection;
- local analysis using a runtime-selected model;
- incremental processing;
- dashboard visualization;
- persistent Context Memory.

Even on one host these remain separate services. They should communicate through canonical files, APIs, databases or queues rather than hidden in-process coupling. Process supervision is intentionally external so systemd, containers or another supervisor can restart components independently.

Any concrete hostname, IP address, database account, filesystem path, model deployment, service schedule, backup policy or other deployment-specific setting must remain in machine-local/private configuration outside the public repository.

## 5. Slurm/HPC: analysis only

Use `roihu` + `slurm` as the public Slurm/HPC template for GPU batch analysis.

```bash
laclaugpt run \
  --project ai26 --arena elites \
  --machine roihu --execution slurm \
  --dataset my_corpus.csv
```

The Slurm execution profile owns scheduler behavior, checkpoint/retry behavior and batch mode. The machine profile owns service/backend/runtime capabilities. It disables collector and dashboard services and expects the actual local model selection to be supplied outside the public repository.

No persistent web service should be started from a Slurm job.

## Service boundaries

The following invariants apply across all deployments:

1. Collector-only must work without analysis, LLM or dashboard dependencies.
2. Analysis-only must work without collection or visualization.
3. Dashboard-only must consume existing canonical outputs without loading an LLM.
4. Slurm execution must never launch a browser collector or dashboard.
5. Full-stack deployment may colocate all modules, but they remain independently restartable services.
6. Canonical interchange/output must remain portable between environments.
7. Project and arena profiles must not be duplicated merely because hardware or execution topology changes.

## Configuration ownership

Machine profiles own public capability/topology templates such as:

- storage/backend classes;
- service availability;
- LLM transport mode;
- GPU/runtime characteristics.

Private or machine-local overlays own concrete values such as:

- actual model/provider selections;
- hostnames, ports and service endpoints;
- credentials and database accounts;
- storage paths and allocation identifiers;
- schedules, supervision and backup details.

Execution profiles own:

- manual/service/batch/realtime mode;
- scheduler type;
- recurrence;
- retry/resume/checkpoint behavior;
- generic Slurm resource policy.

Project and arena profiles continue to own theory, analytical modules, dataset semantics and research-specific model hints.

## Validation

`tests/test_deployment_profiles.py` composes every required profile offline and checks that:

- required services are enabled/disabled correctly;
- dashboard-only and collector-only have no accidental LLM dependency;
- local/cloud profiles preserve the intended routing mode without publishing production model selections;
- GPU realtime enables all three major services;
- the Slurm profile is analysis-only;
- changing machine/execution topology does not change project/arena research semantics.

The tests do not launch real models, browsers, dashboards or Slurm jobs.

## Design principle

**One LaclauGPT, many environments.**

The runtime topology is replaceable infrastructure. The discourse-analysis semantics are not.
