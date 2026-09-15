# Context & memory architecture (issue #140)

This note defines **what context each analysis stage receives, what persists
across documents and runs, and which profiles are supported**. The implementation
is split deliberately:

- `laclaugpt/context_profiles.py` defines policy only;
- `laclaugpt/context_runtime.py` applies an explicitly selected policy to real
  pipeline prompt context and records context provenance;
- `scripts/benchmark_context.py` compares profiles on the same reviewed sample.

No profile is inferred from the machine name. Existing production behaviour is
unchanged unless a canonical run explicitly selects a context profile.

## 1. Stage map and context requirements

| Stage | Context already passed | Codebook / memory role |
|---|---|---|
| summary | transcript/OCR/frame text, source metadata, topic background | glossary helps keep actors/topics/entities stable; descriptive stage |
| discourse | source, summary, metadata, analytic hints | signifier/formation/actor codebook context is theory-facing and must be auditable |
| postprocess | source + summary | topic/entity/target glossary supports canonical IDs |
| populism | source + summary + discourse coding | signifier/target codebook context supports Formula-of-Populism coding |
| corpus synthesis | canonical annotations and grouped statistics | consumes outputs rather than silently becoming new source evidence |

Previous-stage outputs are passed explicitly as structured values. Opaque chat
history is therefore not the default memory mechanism.

## 2. Six-layer memory model

1. **Static research context** — theory, ontology, codebooks and prompt
   instructions, versioned in the repository.
2. **Corpus context** — descriptive actor/formation/frame statistics. Optional
   prompt context only when a profile asks for it.
3. **Run context** — project, arena, model, analysis switches and effective
   configuration fingerprint.
4. **Short-term analytical memory** — persistent Context Memory glossary
   (`laclaugpt_memory`) with stable IDs, aliases, review state and optional
   embeddings.
5. **Long-term retrieval memory** — prior reviewed entities/relations and
   corrections. Model proposals remain provisional and rejected merges stay
   rejected.
6. **Temporal situational state** — an optional previous daily/batch report or
   structured state file, explicitly labelled as trusted or untrusted prior
   context and never treated as source evidence.

## 3. Approaches evaluated

| Approach | Decision | Rationale |
|---|---|---|
| Plain message/history | keep only explicit stage outputs | cheap, transparent, reproducible |
| Structured rolling state | opt-in | useful for daily/batch continuity; anchoring must be benchmarked |
| Previous-stage outputs | keep | already canonical and typed |
| Previous daily/batch report | opt-in | useful situational context; always provenance-labelled |
| Claude-Code-style project memory | keep as versioned repo instructions/codebooks | deterministic and reviewable |
| LangChain memory | do not adopt by default | extra dependency without demonstrated quality gain |
| LlamaIndex | do not adopt by default | same; add only if benchmarked retrieval wins |
| Vector RAG | benchmark-gated flag, off by default | existing Context Memory already supports local embedding-assisted retrieval |
| Graph RAG / hybrid RAG | benchmark before adopting | canonical discourse graph already exists; a second graph memory risks drift |
| Entity-centric memory | keep | stable-ID glossary is already entity-centric |
| Temporal memory | keep at synthesis/state layer | avoids turning previous model output into source truth |
| Episodic corrections | keep | rejected merges/review decisions are first-class memory |
| Hierarchical memory | partial | project/corpus/run/document layers are explicit; deeper retrieval remains experimental |
| Cached context bundles | keep via fingerprints/provenance | supports reproducible reruns |

The design intentionally prefers simple deterministic mechanisms until a
human-reviewed benchmark shows that a heavier framework improves analysis.

## 4. Codebook audit and fail-loudly behaviour

The root pipeline already calls Context Memory in all four LLM stages. Issue
#140 adds explicit profile-aware validation and provenance.

| Stage | Typical codebook kinds | Required in normal profiles? | Validation behaviour |
|---|---|---:|---|
| summary | actor/topic/entity | advisory | missing block is recorded |
| discourse | signifier/formation/actor | yes | `validation` fails closed |
| postprocess | topic/entity/target | advisory | missing block is recorded |
| populism | signifier/target | yes | `validation` fails closed |

For routine profiles, a missing required block emits a warning and records
`codebook_missing: true` in stage context provenance. In the `validation`
profile, missing required codebook context raises immediately. This gives
production a non-breaking warning path and audit runs a hard gate.

Each stage provenance may include:

```json
{
  "context": {
    "profile": "high_accuracy",
    "stage": "discourse",
    "kinds": ["entity", "topic", "signifier"],
    "glossary_top_k": 8,
    "chars": 7421,
    "sha256": "...",
    "codebook_required": true,
    "codebook_missing": false,
    "previous_batch_summary": {
      "sha256": "...",
      "trust": "model_proposed"
    }
  }
}
```

The hash is part of reproducibility: context changes change the prompt and the
existing stage-cache fingerprint already includes the rendered prompt text.

## 5. Profiles and environments

| Profile | Glossary top-k | Previous state | Corpus stats | Context cap | Missing required codebook | Recommended use |
|---|---:|---:|---:|---:|---|---|
| `fast_local` | 3 | no | no | 2k chars | warn | laptop debugging and tiny pilots |
| `balanced` | 5 | no | no | 6k chars | warn | routine production, local or Roihu |
| `high_accuracy` | 8 | yes if supplied | yes if supplied | 12k chars | warn | CSC Roihu research/validation passes |
| `validation` | 5 | yes if supplied | yes if supplied | 6k chars | **fail** | reproducibility and context-ablation audits |

Models remain controlled by the existing model/runtime configuration. A context
profile does **not** silently switch Gemma tiers or cloud/local routing.

Canonical selection is explicit under the dataset pipeline settings:

```yaml
dataset:
  pipeline:
    context_profile: high_accuracy
    previous_batch_summary: /approved/private/path/previous-day.json
    corpus_stats_path: /approved/private/path/corpus-state.json
```

The public repo should contain only generic examples. Operational paths and
research data remain private.

## 6. Previous daily report / situational state

State-aware profiles can read JSON or Markdown. JSON is preferred because it can
carry `review_status` and structured fields such as major actors, emerging
frames, important signifiers, unresolved ambiguities, codebook changes and human
corrections.

Rules:

- `review_status: human_reviewed|accepted|source_fact` is labelled reviewed, but
  the source documents still remain primary evidence;
- any other state is injected with an **UNTRUSTED PRIOR STATE** warning;
- the exact file hash and injected character count are stored in provenance;
- the state is bounded by the profile context budget;
- a stateless run remains possible by omitting the state path.

This lets the benchmark compare the same profile with and without previous-day
state and measure both continuity gains and anchoring effects.

## 7. Benchmark harness

The public repository contains methodology and code; the human-reviewed sample
may remain in the private research environment.

Dry matrix validation:

```bash
python3 scripts/benchmark_context.py \
  --sample /private/gold.csv --project ai26 --arena grassroots \
  --machine laptop-ollama --profiles fast_local,balanced,high_accuracy
```

Full Roihu comparison:

```bash
python3 scripts/benchmark_context.py \
  --sample /private/gold.csv --project ai26 --arena grassroots \
  --machine roihu --profiles balanced,high_accuracy,validation --full \
  --previous-state /private/previous-day.json \
  --out /private/context-benchmark.json
```

When matching human columns exist (`gold_populist` / `human_populist`,
`gold_entities` / `human_entities`, `gold_frames` / `human_frames`), the harness
reports agreement and precision/recall. It always reports evidence fidelity,
unsupported-evidence rate, canonical-ID rate, context size, missing-codebook
count, wall time, throughput and process memory delta. It does not invent a
quality score for dimensions absent from the gold sample.

A useful experimental sequence is:

1. `fast_local` vs `balanced` for speed/context-cost baseline;
2. `balanced` vs `high_accuracy` for retrieval-depth/context benefit;
3. `high_accuracy` with and without `--previous-state` for the daily-report
   situational-memory experiment;
4. `validation` to prove that required codebooks are actually present.

## 8. Memory hygiene

- Model-generated memory never silently becomes ground truth.
- Previous-state text is explicitly trust-labelled.
- Human rejection of merges remains binding.
- Stable IDs preserve exact wording/alias history.
- Context is bounded and hashed.
- Codebook gaps are visible in provenance and fail closed in audit mode.
- Heavy vector/graph frameworks remain off until human-reviewed benchmarking
  demonstrates a gain.

## 9. Recommended defaults and migration

- **Local / Laskin:** start with `balanced`; use `fast_local` for debugging.
- **CSC Roihu:** use `balanced` for throughput and `high_accuracy` for expensive
  research passes; use `validation` before trusting a new codebook/run setup.
- **Previous daily state:** keep opt-in until the same-sample benchmark shows a
  continuity benefit without unacceptable anchoring.

Migration is additive. If `dataset.pipeline.context_profile` is absent, the
canonical wrapper delegates directly to the existing pipeline and does not
alter prompt context, model routing, evidence gates, stages, or relevance
handling.
