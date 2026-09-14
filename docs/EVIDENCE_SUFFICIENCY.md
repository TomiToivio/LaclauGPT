# Evidence sufficiency and abstention

LaclauGPT separates **input sufficiency** from interpretive validity.

Before a document enters discourse, ideology, or populism coding, a pipeline may
run a deterministic source-evidence check with `laclaugpt.evidence_quality`.
The check asks a deliberately narrow question: is there enough observable source
material in at least one enabled channel to justify interpretation?

This is different from several other safeguards:

- **input sufficiency**: is there enough transcript, OCR, or visual observation
  to analyse at all?
- **quotation verification**: does a model-produced evidence quote occur in the
  source material?
- **model-reported confidence**: an uncalibrated model self-report, not a
  probability of correctness;
- **substantive validity**: does a coding make theoretical and empirical sense?
- **human review**: does a researcher accept, revise, or reject the coding?

These checks should not be collapsed into one score.

## Content first, metadata second

Political identity and sampling context are useful metadata, but they are not
source evidence for substantive political content. A post from a politician,
campaign, movement, or politically selected account can still contain ordinary
personal, aesthetic, administrative, or otherwise non-political material.

The public prompts therefore apply a content-first sequence:

1. assess whether observable source evidence is sufficient;
2. produce a descriptive summary and political/non-political classification;
3. enter Laclaudian discourse coding only when the material is applicable;
4. enter Formula-of-Populism coding only when source evidence and applicability
   support it;
5. keep empty lists and explicit abstention as valid results throughout.

This prevents metadata leakage from turning account identity into inferred
political content.

## Deterministic gate

`assess_evidence()` accepts project-neutral channels:

```python
from laclaugpt.evidence_quality import assess_evidence

quality = assess_evidence(
    transcript=transcript,
    ocr_text=ocr_text,
    visual_observations=frame_summary,
    visual_status=frame_status,
)

if not quality.allow_interpretive_analysis:
    # retain the source and provenance, but abstain from interpretive coding
    ...
```

Thresholds are explicit parameters because different corpora, languages, media
formats, and OCR systems require validation. The defaults are conservative
starting points, not universal scientific cutoffs.

A visual observation counts only when it is non-empty and, if a stage status is
supplied, that status indicates success or partial success. OCR must contain a
minimum amount of content-like text rather than merely being non-empty. Speech
transcripts similarly require a minimum token count. Multiple usable channels
are reported as `multimodal`.

## Prompt-level fail-safe

The public summary, discourse, postprocess, and populism prompts reinforce the
same principle:

- insufficient evidence should produce abstention rather than invented
  structure;
- non-political content should not acquire political topics or entities merely
  from account identity;
- non-applicable discourse rows should not retain signifier, articulation,
  imaginary, or formation codings;
- placeholder labels such as `None explicitly named`, `N/A`, and `unknown` are
  not entities;
- populism coding should stop when evidence is insufficient or discourse is not
  applicable.

These validators are guardrails, not substitutes for research judgement.

## Publication boundary

The public repository contains only the generic method, synthetic regression
fixtures, and reusable code. Corpus-specific thresholds, collected media,
operational source selections, machine paths, credentials, private codebooks,
and study-specific run configuration belong in controlled research storage or a
private operational repository.
