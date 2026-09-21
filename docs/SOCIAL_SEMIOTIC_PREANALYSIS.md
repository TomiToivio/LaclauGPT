# Multimodal Social-Semiotic Pre-Analysis

**Status:** Phase 1 method and data-contract specification. This is descriptive preprocessing, not Laclau discourse analysis, ideology classification, political framing analysis, or sentiment classification.

## Pipeline boundary

raw text/image/video/audio/metadata → Multimodal Social-Semiotic Pre-Analysis → LLM Structuralism / relational representation → Laclau discourse analysis.

The first pass describes what semiotic resources are present and how they are organised. Later stages decide whether observed signs acquire Laclaudian or political status.

## Methodological basis

The core is social semiotics and Systemic Functional Linguistics (SFL). Halliday's textual, ideational, and interpersonal metafunctions provide an organising grammar. Kress and van Leeuwen extend functional analysis to visual representation and composition. Martinec and Salway provide a system for image-text relations.

Wanselin, Danielsson and Wikman (2022) combine these strands into a practical framework for static multimodal science texts. Their analytical table distinguishes textual organisation/resources and relative size/scale; ideational transitivity, narrative/conceptual visual function and image-writing relations; and interpersonal positioning, speech roles, formality and explicit/implicit values.

For LaclauGPT, the interpersonal layer is deliberately constrained. Observable address, offer/demand form, formality, gaze, typography, or explicit evaluative wording may be described. Political positioning, motive, ideological alignment, hegemony, populism, or discourse-theoretical status are downstream interpretations.

## Born-digital adaptation

Wanselin et al. analyse two static educational texts and explicitly delimit their use of multimodal text from animation. LaclauGPT therefore treats application to born-digital social media as an adaptation requiring validation.

The Phase 1 extension adds temporal sequence and duration; cuts and montage; speech/prosody when available; sound, music and silence; gesture; subtitles, OCR and ASR; screenshots, memes and reaction layouts; and platform/interface resources such as usernames, repost markers, watermarks and embedded-media boundaries.

## Hard negative boundary

The stage MUST NOT emit analyst classifications for empty/floating signifiers, nodal points, chains of equivalence/difference, antagonisms/frontiers, populism, ideology or ideological formations, party/political alignment, hegemony, political subjects/demands, or sentiment. Those words may occur literally in source evidence; they must not become analyst classifications here.

## Data contract

Every item records schema_version social-semiotic-preanalysis.v1 and an explicit prompt version.

1. Evidence pointers retain modality, source field, exact text when available, frame/timestamp coordinates, confidence and uncertainty.
2. Denotation records what is observably written, spoken, visible, audible, gestured, arranged, edited, or exposed by the interface before connotation.
3. Semiotic resources cover linguistic, visual, auditory, gestural, spatial, typographic, symbolic/graphic, temporal/editing, interface/platform and metadata modes, plus observed affordance.
4. Ideational observations use participants, processes and circumstances descriptively. Visual vectors/arrows can realise narrative or conceptual structures without assuming that visual and linguistic grammar are identical.
5. Composition covers layout, salience, foreground/background, centre/periphery, size/scale, vectors, reading/viewing order, temporal sequence, repetition, emphasis, transitions, sound emphasis, typography and interface placement.
6. Salient signs retain exact source forms and salience basis. Allowed relations are observable contrast/opposition, pairing, repetition, co-occurrence, sequence, labels, part-whole relations and spatial proximity.
7. Intermodal relations normalise the Wanselin/Martinec-Salway family into redundancy/repetition, extension/complementarity, elaboration/anchoring, contrast/conflict and ambiguity. Conflicting modes remain conflicting.
8. Cautious connotation is separate from denotation and carries basis, alternatives, evidence and confidence.
9. Uncertainty is first-class: OCR, ASR, translation, visual, audio, speaker, temporal, missing modality, source context, model, or other. Missing evidence is represented rather than silently filled in.

## Input coverage

The same conceptual schema is intended for text-only posts/articles, still images, screenshots/memes, OCR-derived text, audio-derived transcripts, short video, transcript plus sampled frames, caption plus media, repost/quoted-post structures, and mixed web/social-media objects. Text-only remains valid; multimodality is never manufactured to satisfy the schema.

## Provenance and versioning

Prompt resources are scientific-method resources. Analysis records prompt ID, version, resource hash, rendered-prompt hash, model/provider metadata, project/config revisions and context provenance. Behaviourally meaningful prompt changes require a new version.

Initial implementation: schema social-semiotic-preanalysis.v1; multimodal.system:v2; multimodal.frame_analysis:v2; multimodal.summary_analysis:v2. Historical v1 resources stay loadable for reproducibility.

## Acceptance tests

Synthetic tests cover text-only source forms, cross-modal conflict, uncertain OCR, schema rejection of extra political fields, structural leakage guards, and literal political vocabulary preserved only as evidence. The canonical test suite additionally exercises video plus sampled-frame integration and prompt provenance.

## Ownership and Phase 0 safety

The umbrella repository owns this methodological contract. Executable models, prompts, validation and canonical-pipeline integration live in TomiToivio/LaclauGPT-Data-Analysis. Legacy Puhti scripts remain historical/reference implementations and are not the canonical dependency. Phase 0 behavior remains unchanged; under the current repository policy, Phase 1 code and documentation live on `main` and the historical `phase-1` branch is synchronized with it.

## References

- Halliday, M. A. K. (1978). Language as Social Semiotic. Edward Arnold.
- Halliday, M. A. K., & Matthiessen, C. (2014). Halliday's Introduction to Functional Grammar (4th ed.). Routledge.
- Kress, G. (2010). Multimodality: A Social Semiotic Approach to Contemporary Communication. Routledge.
- Kress, G., & van Leeuwen, T. (2006). Reading Images: The Grammar of Visual Design (2nd ed.). Routledge.
- Martinec, R., & Salway, A. (2005). A system for image-text relations in new (and old) media. Visual Communication, 4(3), 337-371.
- Tang, K.-S., Won, M., & Treagust, D. (2019). Analytical framework for student-generated drawings. International Journal of Science Education, 41(16), 2296-2322.
- Wanselin, H., Danielsson, K., & Wikman, S. (2022). Analysing Multimodal Texts in Science: A Social Semiotic Perspective. Research in Science Education, 52, 891-907. DOI 10.1007/s11165-021-10027-5.
