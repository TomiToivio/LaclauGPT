# 2026 study operations: modular deployment map

This document maps the active 2026 research workloads onto the public LaclauGPT modules. It describes architecture and public contracts only. Real target lists, collected data, researcher annotations, codebooks, credentials, hostnames, CSC project identifiers, filesystem paths, service units and schedules remain private or machine-local.

## Module ownership

| Responsibility | Canonical public repository |
|---|---|
| acquisition, browser capture, normalization, collection state | `LaclauGPT-Data-Collection` |
| LLM/NLP/multimodal analysis and batch/realtime orchestration | `LaclauGPT-Data-Analysis` |
| monitoring, researcher review and exploration | `LaclauGPT-Data-Visualization` |
| theory, shared contracts and deployment topology | `LaclauGPT` |

The modules exchange canonical records keyed by stable `source_url`. A study may change machine topology without changing its research schema.

## AI26: real-time full stack on a Linux research server

```text
Firefox / feed / platform collectors
       ↓
LaclauGPT-Data-Collection
       ↓ canonical source records
LaclauGPT-Data-Analysis incremental worker + local Ollama
       ↓ canonical analyzed records
LaclauGPT-Data-Visualization Monitor / Review / Explore
```

Public preparation:

- Collection contains the canonical Firefox extension/backend and a synthetic `ai26.example.yaml` study profile.
- Browser capture remains loopback-only; a researcher workstation may reach a server backend through authenticated tunnelling rather than a public ingestion port.
- Analysis contains an append-only `source_url`-keyed incremental JSONL worker and a supervisor-friendly loop script with cloud fallback disabled.
- Visualization can point directly at the AI26 study-specific Analysis output directory and run loopback-only behind an SSH tunnel or separately configured authenticated reverse proxy.

Private completion still required: the real AI26 sampling frame, storage paths, model selection if different from public defaults, process supervision, backup/rotation policy and network access configuration.

## EP24: Finland + Poland reprocessing on CSC Roihu, visualization on CSC Pouta

```text
private EP24 inputs/codebooks/media
       ↓
Roihu: LaclauGPT-Data-Analysis EP24 compatibility batch harness
       ↓ canonical + researcher-facing analysis output
private transfer/shared storage
       ↓
Pouta: LaclauGPT-Data-Visualization Researcher Review / Explore
```

Public preparation:

- Data Analysis includes the reusable Roihu GH200/Ollama runtime harness and fail-closed external boundaries for the restricted Finland/Poland manifests, historical row-level data, human codebooks and compatibility driver.
- Visualization uses the common canonical dashboard. Historical EP24 flat exports remain isolated behind the legacy adapter; new reprocessing output should prefer canonical nested records.
- The Pouta dashboard launcher defaults to loopback and requires explicit opt-in before any non-loopback bind.

Private completion still required: actual CSC allocation, Roihu/Pouta paths, restricted EP24 material, data transfer/shared-storage wiring, Pouta security groups/authentication/TLS and researcher access policy.

## Hungary26: reprocessing on CSC Roihu

```text
private Hungary26 corpus + study codebook/config
       ↓
LaclauGPT-Data-Analysis generic Roihu study-reprocessing harness
       ↓
canonical analyzed records + provenance
```

Public preparation:

- The generic Roihu batch harness is study-neutral and accepts `STUDY_ID=hungary26` plus an externally staged executable driver.
- It initializes the Roihu GPU software environment, performs an ARM64 virtualenv/NumPy preflight, starts job-local Ollama, forbids silent cloud fallback, and runs the private study driver.
- Hungary26 analysis semantics currently enable Laclau/Palonen analysis, sentiment, topics, entities, context memory, temporal and multimodal processing; concrete study resources remain private.

Private completion still required: the Hungary26 dataset, codebook, project-specific driver/configuration, CSC allocation/path values and validation against a researcher-reviewed sample before a full run.

## Brazil26: collection with the shared Firefox tool

```text
researcher Firefox profile
       ↓ private loopback/tunnel
LaclauGPT-Data-Collection capture backend
       ↓
private Brazil26 canonical collection store
```

Public preparation:

- Collection contains a synthetic `brazil26.example.yaml` election-study template with fictional candidates/parties.
- AI26 and Brazil26 share one collector implementation but must use independent private study YAMLs, data roots, SQLite/raw state, capture ports/tunnels and Firefox profiles.
- The Firefox backend stays loopback-only by design. Real candidate/party/account sampling frames must never be committed.

Private completion still required: the researcher-approved Brazil26 sampling frame, runtime data root, browser profile, process supervision, media/storage policy and live collection schedule.

## Cross-study invariants

1. `source_url` is the canonical identity across Collection, Analysis and Visualization.
2. Study-specific runtime data and review state are isolated even when code is shared.
3. Sampling-group metadata is provenance, not an automatic ideological or political label.
4. Collection never performs discourse-theoretical interpretation.
5. Visualization never performs analysis; it displays and reviews existing outputs.
6. Slurm jobs never launch browser collectors or dashboards.
7. Public repositories contain synthetic fixtures/examples only.
8. Local inference must not silently fall back to cloud inference.
9. Researcher review remains required before machine-generated interpretations are treated as findings.

## Desired convergence

EP24 currently retains a compatibility wrapper because of historical multimodal/export machinery. Hungary26 is prepared against the generic study-reprocessing boundary. The architectural goal is to migrate reusable EP24 ASR/OCR/keyframe/config/export/quality components into `LaclauGPT-Data-Analysis` until EP24, Hungary26 and future studies can use the same generic batch interface with only private data/codebooks/configuration varying by project.
