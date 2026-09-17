# Shared Gemma4 model-routing contract

This document defines the project-wide model-routing policy for Ollama-backed LaclauGPT components. The meta-repository owns the contract; executable routing logic belongs in the implementation repositories.

## Principles

1. Prefer the strongest sensible **local** Gemma4 model for the declared/detected machine capabilities.
2. Explicit user/project configuration wins over automatic detection.
3. Cloud inference is opt-in only. LaclauGPT must never silently fall back from local Ollama to a cloud model.
4. Model selection is task-aware. A helper task may deliberately use a smaller model than the machine maximum.
5. Embedding models are configured independently from generative Gemma4 models.
6. Normal CI and imports must remain offline and must not trigger model downloads or require a running Ollama service.
7. Every LLM-backed result should record the effective routing decision in provenance where practical.

## Supported model tiers

| Tier | Default model | Typical use |
| --- | --- | --- |
| edge-minimum | `gemma4:e2b` | constrained laptop/CPU host, lightweight helper tasks |
| edge | `gemma4:e4b` | small laptop/server with modest local capacity |
| balanced | `gemma4:12b` | workstation/capable laptop, routine analysis |
| large | `gemma4:26b` | GPU server, CSC Roihu, heavier analysis and RAG synthesis |
| dense-high | `gemma4:31b` | larger-GPU workstation/server |
| cloud-high | `gemma4:31b-cloud` | explicit cloud-enabled execution only |

`gemma3:270m` is not a project-level default for RAG or helper tasks. RAG follows the same Gemma4 routing policy as other LLM-backed components.

## Machine-profile defaults

Profiles are convenience policies, not hostname checks.

```text
laptop-low-resource       -> gemma4:e2b
laptop                    -> gemma4:e4b or gemma4:12b according to configured/detected capacity
workstation               -> gemma4:12b
linux-server-low-resource -> gemma4:e2b or gemma4:e4b
linux-server-gpu          -> gemma4:26b
roihu-slurm-gpu           -> gemma4:26b, with 12b/31b selectable according to resources
ollama-cloud              -> gemma4:31b-cloud, explicit opt-in only
```

A profile may define a preferred tier, but routing should still validate relevant capabilities when possible.

## Capability inputs

A shared router should be able to consider:

- explicit model override;
- declared machine profile;
- GPU availability;
- usable VRAM;
- system RAM;
- local versus remote Ollama endpoint;
- whether cloud execution is explicitly allowed;
- task class;
- project/run-specific policy.

Recommended precedence:

```text
explicit model override
  -> explicit project/machine profile
  -> safe capability-aware selection
  -> lightweight local fallback
```

Automatic detection must be advisory rather than magical. If hardware information is unavailable, choose a conservative local tier instead of guessing a large model.

## Task classes

Implementations should use a small shared vocabulary such as:

- `analysis`
- `multimodal_analysis`
- `rag_helper`
- `rag_synthesis`
- `research_qa`
- `agent`

A task policy may choose a smaller model than the machine maximum. For example, `rag_helper` may use E2B/E4B on a workstation while full `analysis` uses 12B.

Conceptual interface:

```python
model = model_router.select(
    task="analysis",
    machine_profile="roihu-slurm-gpu",
    capabilities=capabilities,
    allow_cloud=False,
    explicit_model=None,
)
```

The exact implementation API may differ by module, but behavior should remain compatible with this contract.

## RAG policy

RAG and researcher Q&A use this same router for generative inference.

Examples:

```text
low-resource laptop RAG helper -> gemma4:e2b / gemma4:e4b
workstation RAG synthesis      -> gemma4:12b
GPU server / Roihu synthesis   -> gemma4:26b or gemma4:31b
explicit cloud research Q&A    -> gemma4:31b-cloud
```

Embeddings remain separately configurable, for example through a distinct setting such as `LACLAUGPT_EMBEDDING_MODEL`. The router must not reuse the generative model name as an implicit embedding model.

## Local, remote and cloud semantics

The Ollama endpoint and the model tier are separate concerns.

- A local endpoint may host any supported local Gemma4 tier that fits the machine.
- A remote Ollama endpoint may still be considered private/local infrastructure from the project's perspective, but provenance must record that the endpoint was remote.
- `gemma4:31b-cloud` requires an explicit cloud-enabled profile or `allow_cloud=true` equivalent.
- Failure to reach a configured local/remote Ollama endpoint must not trigger a cloud fallback unless the user/project explicitly configured such behavior.

## Provenance

Where practical, each LLM-backed result or run should record:

```text
effective_model
effective_backend / ollama_endpoint_class
execution_location = local | remote | cloud
machine_profile
task_class
routing_tier
routing_reason
cloud_allowed
generation_options
router_version / policy_version
```

Do not store credentials or authenticated endpoint URLs in provenance.

## Configuration contract

Modules may expose different configuration surfaces, but they should map to the same concepts. Recommended shared names include:

```text
LACLAUGPT_OLLAMA_URL
LACLAUGPT_OLLAMA_MODEL
LACLAUGPT_MACHINE_PROFILE
LACLAUGPT_ALLOW_CLOUD
LACLAUGPT_EMBEDDING_MODEL
```

An explicit `LACLAUGPT_OLLAMA_MODEL` or equivalent should override automatic model selection.

## Module responsibilities

### Data Collection

Collection normally has no LLM dependency. Any bounded collection-side LLM helper should consume the shared routing policy rather than hard-code model names.

### Data Analysis

Data Analysis is the primary implementation/consumer of capability-aware routing and should expose reusable routing behavior to other project components where practical.

### Data Visualization

Research Q&A, RAG synthesis and optional LLM-backed dashboard functions should use the shared routing policy and must not silently select a cloud model.

### Agents / research assistants

Agents use the same effective model-routing configuration and record routing provenance for model-backed actions where practical.

## Offline CI and model availability

Tests must not require Ollama, GPUs or model downloads. Routing logic should be testable through synthetic capability descriptors and mocked endpoint state.

Recommended tests include:

- explicit model override wins;
- low-resource profile selects E2B/E4B;
- workstation selects 12B when capacity is sufficient;
- GPU server/Roihu defaults to 26B;
- 31B is selectable for sufficiently large declared capacity;
- cloud model is rejected unless cloud is explicitly enabled;
- failed local endpoint does not silently switch to cloud;
- embedding model remains independent;
- provenance includes model/profile/task/reason;
- importing router code performs no network calls or model downloads.

## Design rule

**One LaclauGPT model router, many machine profiles. Use the strongest sensible local Gemma4 model for the available resources, while keeping cloud inference explicit and auditable.**
