# Local Ollama routing benchmark

Issue #136 requires model-routing changes to be measured rather than guessed. The current routing therefore remains unchanged until a representative benchmark is run and reviewed.

## Candidate set

Use official Ollama tags where possible:

- `gemma4:e2b`
- `gemma4:e4b`
- `gemma4:12b`
- `gemma4:26b`
- `gemma4:31b`
- `embeddinggemma` / `embeddinggemma:300m` for embedding, retrieval and semantic-similarity tasks
- at least one non-Gemma baseline such as `qwen3:30b` where local capacity permits

`gemma4:26b` must be tested specifically for corpus synthesis and temporal comparison. Ollama describes it as a Mixture-of-Experts model with about 4B active parameters, making it a plausible high-quality synthesis tier without assuming dense-26B token cost.

Do not publish machine hostnames, private deployment paths, exact hardware inventory, credentials or private corpus contents in this repository.

## Representative task set

The public benchmark manifest should contain synthetic or safely publishable examples spanning:

1. cheap extraction / normalization;
2. entity and topic extraction;
3. evidence-bearing signifier and articulation coding;
4. frame/discourse coding;
5. Palonen populism coding with abstention cases;
6. mixed-language examples;
7. long-document evidence fidelity;
8. formation-candidate consistency;
9. corpus synthesis;
10. current-window vs previous-window change detection.

Where a human-coded reference exists, keep private texts private and publish only aggregate benchmark results that do not reconstruct the underlying records.

## Metrics

Record at least:

- structured-output validity rate;
- agreement with human/codebook expectations where a gold/reference sample exists;
- evidence fidelity and hallucinated-evidence rate;
- formation/signifier consistency;
- frame/discourse/populism quality;
- corpus-synthesis quality;
- latency and documents per minute;
- peak VRAM/RAM where available;
- failure and retry rate.

The benchmark must report results by task type and language. A single overall score is not sufficient for routing decisions.

## Routing decision rule

Prefer the smallest/fastest model whose quality is statistically or practically indistinguishable from the next larger candidate for that stage. Keep difficult theory-sensitive stages on a larger tier when smaller models show evidence loss, abstention failures or unstable formation/signifier decisions.

Do not change `STAGE_ROUTING` merely because a candidate is newer. A routing change should cite the benchmark artifact and preserve the old policy in version control.

## Proposed hypothesis to test

This is a benchmark hypothesis, not the current default policy:

| Task | First candidate to test |
| --- | --- |
| simple extraction / normalization | `gemma4:e2b` or `gemma4:e4b` |
| document-level discourse / frame / populism | `gemma4:12b` |
| corpus synthesis / temporal comparison / difficult long text | `gemma4:26b` |
| high-accuracy validation reference | `gemma4:31b` |
| embeddings / similarity / retrieval | `embeddinggemma` |

The existing custom `batiai/gemma4-12b:q6` should remain eligible until an official-tag benchmark demonstrates equal or better accuracy/latency for the relevant stages.
