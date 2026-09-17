# Cross-module canonical parity fixture

`canonical_parity_v1.json` is the versioned, privacy-safe contract fixture for the Collection → Analysis → Visualization handoff.

It contains no real research data, no credentials, no private source lists, and no network-dependent references. All URLs use `example.invalid` or `fixture://` identifiers.

## Invariants

Every module that consumes this fixture must preserve these invariants:

1. `source_url` remains exactly `https://example.invalid/laclaugpt/synthetic/record-001` after canonicalization and every storage/transport round trip.
2. `source_native_ids.legacy_document_id` and `source.raw_metadata.legacy_optional_field` survive without silent loss.
3. Optional multimodal-shaped content (`transcripts`, `ocr`, `frames`, `media_references`) may be present without requiring media downloads or external services.
4. Analysis preserves codebook references, model provenance, uncertainty, evidence links, epistemic type, and review state.
5. Visualization must be able to render the canonical record generically, without a project-specific adapter.
6. Review semantics remain human-controlled: the fixture contains a `CANDIDATE_INTERPRETATION` with `PROVISIONAL` review status and must not be silently promoted.

## Module responsibilities

### Data Collection

Load or construct the fixture through the canonical Collection record model and verify that normalization plus supported JSON/JSONL/CSV/SQLite adapters preserve the invariant fields. Synthetic multimodal references should remain references only.

### Data Analysis

Load the canonical record, run a fake/provider-neutral analysis path or equivalent deterministic fixture path, and preserve identity plus existing provenance/review fields. Tests must not invoke a cloud model or require Ollama.

### Data Visualization

Load the analyzed canonical record through the generic canonical adapter and verify monitor, researcher-review, explore/view-model transforms and a human-readable detail rendering. No EP24/AI26/project-specific adapter should be required.

## Backend parity

JSON is the reference wire representation. JSONL, CSV and SQLite are transport/storage adapters and must reconstruct the same logical record before module semantics are applied.

MongoDB/S3/Redis are not required in CI for this fixture. Their adapters should preserve the same logical contract:

- MongoDB stores/querys the canonical durable record and review state.
- S3/Allas stores referenced large/raw artefacts rather than changing record semantics.
- Redis carries references, coordination and transient state, never the sole durable canonical record.

## Updating the fixture

This file is a schema-drift tripwire. Breaking changes require either backward-compatible consumers or a new fixture version. Do not overwrite an older fixture in a way that makes historical contract expectations ambiguous.
