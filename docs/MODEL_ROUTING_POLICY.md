# Shared Gemma4 model-routing policy

This document defines the project-level model-selection contract for Ollama-backed LaclauGPT components. It coordinates Data Analysis, optional RAG/research-QA helpers, visualization-side LLM features and agents without forcing every module to duplicate its own defaults.

## Principles

1. Prefer explicit configuration over auto-detection.
2. Prefer local Ollama over cloud inference.
3. Never silently fall back to cloud.
4. Select the smallest sensible Gemma4 model for the task and available resources.
5. Keep embedding-model selection separate from generative-model selection.
6. Do not download models automatically at import/startup time.
7. Record the effective model decision in provenance.
8. Offline CI must not require Ollama or model downloads.

## Supported Gemma4 tiers

| Tier | Model | Intended use |
|---|---|---|
| edge | `gemma4:e2b` | very low-resource laptop/server, helper tasks |
| light | `gemma4:e4b` | ordinary laptop, lightweight RAG/Q&A |
| balanced | `gemma4:12b` | workstation/capable laptop, routine analysis |
| large | `gemma4:26b` | GPU server / CSC Roihu, heavier analysis |
| dense-large | `gemma4:31b` | high-VRAM local GPU workloads |
| cloud | `gemma4:31b-cloud` | explicit cloud opt-in only |

These are routing policy names, not installation guarantees. A module must fail clearly when an explicitly selected required model is unavailable. It must not auto-pull a different or cloud model behind the user's back.

## Machine-profile defaults

Profiles provide convenient initial tiers but do not override explicit user configuration.

| Machine profile | Default |
|---|---|
| `laptop-low-resource` | `gemma4:e2b` |
| `laptop` | `gemma4:e4b`, promote to `gemma4:12b` when declared/detected resources permit |
| `workstation` | `gemma4:12b` |
| `linux-server-low-resource` | `gemma4:e2b` or `gemma4:e4b` |
| `linux-server-gpu` | `gemma4:26b` |
| `roihu-slurm-gpu` | `gemma4:26b`, with `gemma4:31b` available when resources permit |
| `ollama-cloud` | `gemma4:31b-cloud`, only when cloud is explicitly enabled |

Do not route by hostname alone. A machine-profile name is a declared execution role; capability information may refine it.

## Selection precedence

Use the following precedence order:

1. Explicit per-task model override.
2. Explicit global generative-model override.
3. Declared machine profile plus declared capabilities.
4. Safe local capability detection.
5. Lightweight local fallback (`gemma4:e2b`).

Cloud is excluded from automatic fallback. `gemma4:31b-cloud` may be selected only when both cloud use is explicitly enabled and the model/profile is explicitly requested.

## Capability inputs

A common router may consider:

- GPU present: yes/no
- available VRAM
- system RAM
- local vs remote Ollama endpoint
- explicit machine profile
- task class
- cloud permission
- user/project override

Capability detection should be advisory and conservative. Modules should not fail merely because optional GPU probes are unavailable.

## Task classes

The common vocabulary is:

- `analysis`
- `multimodal_analysis`
- `rag_helper`
- `rag_synthesis`
- `research_qa`
- `agent`

Task-specific routing may intentionally select a smaller model than the machine maximum. For example, a `rag_helper` query-rewrite step on a GPU server does not need to consume the same model used for heavy discourse analysis.

Suggested defaults when no explicit per-task override exists:

- `analysis`: machine-profile default
- `multimodal_analysis`: machine-profile default, subject to model capability
- `rag_helper`: at most the profile's normal tier; prefer E2B/E4B on low-resource systems
- `rag_synthesis`: machine-profile default
- `research_qa`: machine-profile default
- `agent`: machine-profile default unless the agent's job is explicitly lightweight

## Configuration contract

Modules should accept a shared logical configuration even when their concrete config loaders differ. Recommended environment names:

```text
LACLAUGPT_MACHINE_PROFILE
LACLAUGPT_MODEL
LACLAUGPT_MODEL_ANALYSIS
LACLAUGPT_MODEL_MULTIMODAL_ANALYSIS
LACLAUGPT_MODEL_RAG_HELPER
LACLAUGPT_MODEL_RAG_SYNTHESIS
LACLAUGPT_MODEL_RESEARCH_QA
LACLAUGPT_MODEL_AGENT
LACLAUGPT_ALLOW_CLOUD=false
LACLAUGPT_OLLAMA_URL
LACLAUGPT_EMBEDDING_MODEL
```

`LACLAUGPT_EMBEDDING_MODEL` is intentionally separate. A generative Gemma4 tag must never be assumed to be the embedding model.

Example YAML:

```yaml
machine:
  profile: workstation

ollama:
  base_url: ${LACLAUGPT_OLLAMA_URL:-http://127.0.0.1:11434}
  allow_cloud: false

models:
  default: gemma4:12b
  analysis: null
  multimodal_analysis: null
  rag_helper: gemma4:e4b
  rag_synthesis: null
  research_qa: null
  agent: null
  embedding: ${LACLAUGPT_EMBEDDING_MODEL:-}
```

The repository/module may map existing variable names to this contract for backwards compatibility, but public documentation should converge on one vocabulary.

## Router contract

The project-level behavior can be represented by a small backend-independent interface:

```python
selected = model_router.select(
    task="analysis",
    machine_profile="roihu-slurm-gpu",
    capabilities={
        "gpu": True,
        "vram_gb": 48,
        "system_ram_gb": 128,
        "ollama_backend": "local",
    },
    explicit_model=None,
    allow_cloud=False,
)
```

A selection result should include more than the model string:

```python
{
    "model": "gemma4:26b",
    "task": "analysis",
    "machine_profile": "roihu-slurm-gpu",
    "backend": "ollama",
    "backend_location": "local",
    "routing_reason": "profile_default_with_gpu_capability",
    "capability_tier": "large",
    "cloud_allowed": False,
}
```

## Provenance requirements

For every LLM-backed analytical or researcher-facing result, record where practical:

- effective model tag
- provider/backend (`ollama` or explicit cloud backend)
- endpoint class: local / remote / cloud
- machine/execution profile
- task class
- routing reason
- capability tier
- generation options that materially affect reproducibility
- prompt/schema/codebook versions where applicable

Do not store credentials or authenticated endpoint URLs in provenance.

## RAG integration

RAG and research-QA features must use this same router. Do not maintain a second model-default table for RAG.

Examples:

- low-resource laptop `rag_helper` -> `gemma4:e2b` or `gemma4:e4b`
- workstation `rag_synthesis` -> `gemma4:12b`
- GPU server / Roihu `rag_synthesis` -> `gemma4:26b` or `gemma4:31b`
- cloud research Q&A -> `gemma4:31b-cloud` only with explicit cloud opt-in

Embedding selection remains independent.

## Module responsibilities

### Data Collection

Collection normally has no LLM dependency. Any bounded helper that does use an LLM must consume this policy rather than hard-coding a model.

### Data Analysis

Data Analysis is the primary implementation/consumer of routing. Existing deployment-profile work should expose a reusable router/result shape that other modules can mirror or import later.

### Data Visualization

RAG synthesis, researcher Q&A and future LLM-backed UI helpers must consume the effective shared routing config. Standard dashboards must continue to work without Ollama.

### Agents

Agents must respect the same local/cloud policy and task/model provenance. An agent must never silently select a cloud model.

## CI and testing

Normal CI must remain offline.

Tests should cover routing as pure configuration logic using synthetic capability dictionaries. They must not:

- require an Ollama daemon;
- download Gemma4 models;
- require a GPU;
- contact cloud inference APIs.

Recommended contract tests:

1. explicit model override wins;
2. low-resource profile selects E2B/E4B;
3. workstation selects 12B;
4. GPU server/Roihu selects 26B by default;
5. 31B can be selected when declared resources/profile permit;
6. cloud model is rejected unless cloud opt-in is true;
7. no automatic cloud fallback occurs;
8. embedding-model configuration is independent;
9. routing decision emits provenance fields.

## Cross-module compatibility rule

A module may add task-specific heuristics, but it must not redefine the supported model tiers or cloud policy incompatibly. If model names change in the future, update this document first and coordinate module implementations from the same contract.
