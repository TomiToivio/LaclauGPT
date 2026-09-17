# Cross-module contract conformance skill

Use this skill when a change touches a **shared** LaclauGPT contract, or when you need to establish whether the modules still agree with each other. This is the coordinating skill: the owning module stays responsible for its implementation, but the contracts and their tripwire are owned here.

## Why this exists

LaclauGPT is four public repositories forming one pipeline:

```text
Collection -> Analysis -> Visualization
```

Each module has its own test suite, and every suite can be green while the modules **disagree with each other**. A shared-schema break does not appear as a failing unit test in any single repository — it appears as a mismatch at the boundary. That is the failure mode this skill covers.

Two consequences worth stating plainly:

- A green suite is **not** evidence of contract conformance.
- A contract change is a cross-repository change, even when it is a one-line edit in one file.

## The normative contracts

All three live in this repository and outrank module-local conventions.

| Contract | Path | Governs |
| --- | --- | --- |
| Canonical data contract | `docs/CANONICAL_DATA_CONTRACT.md` | the record shape and `source_url` as semantic identity |
| Storage backend contract | `docs/STORAGE_BACKEND_CONTRACT.md` | `auto | mongodb | csv` selection, local-first fallback, fail-closed rules |
| Cross-module parity fixture | `fixtures/cross_module/canonical_parity_v1.json` + its `README.md` | the versioned schema-drift tripwire |

Related but narrower: `docs/DATA_LIFECYCLE.md`, `docs/MESSAGING_TASK_QUEUE.md`, `schemas/*.json`.

## The invariants that actually bind the modules

Read the fixture `README.md` for the authoritative list. In practice these are the ones that break:

1. **`source_url` is the identity.** It must survive canonicalization and every storage/transport round trip unchanged. Platform ids (`document_id`, `video_id`, `new_id`) and backend keys (`_id`, SQLite primary keys, row numbers, object keys, filenames, queue ids) are aliases. A derived object may have its own id but must retain a path back to `source_url`.
2. **Legacy identifiers and optional source metadata survive** without silent loss — `source_native_ids.legacy_document_id`, `source.raw_metadata.legacy_optional_field`.
3. **Multimodal content travels as references only.** Transcripts, OCR, frames and media references may be present without requiring media downloads or external services; large binaries stay outside the record.
4. **Analysis metadata is preserved**: codebook references, model provenance, uncertainty, evidence links, epistemic type.
5. **Review stays human-controlled.** The fixture carries a `CANDIDATE_INTERPRETATION` with `PROVISIONAL` status; no stage may promote it. Frequency is not hegemony, polysemy is not empty signification, negativity is not antagonism, model confidence is not theoretical confidence.
6. **Visualization renders generically** — no project-specific adapter required.

## Procedure

### 1. Establish the current state before editing

```bash
python scripts/verify_cross_module_fixture.py
```

This is the repository's own offline guard: it checks the fixture's invariants and that JSON, JSONL, CSV and SQLite each reconstruct the same logical record. It contacts nothing.

### 2. Check each affected module against its own instance

Every module that consumes the fixture vendors a copy and exposes an offline conformance command:

```bash
# in LaclauGPT-Data-Collection, -Data-Analysis, -Data-Visualization
python tools/verify_contracts.py
```

Each instance verifies conformance **from that module's perspective** — Collection establishes identity, Analysis enriches it without losing it, Visualization must not rewrite it. Run the ones for the modules your change touches, not just the one you edited.

### 3. Verify the vendored fixture copies have not drifted

The fixture is vendored per module. A copy that silently diverges from the normative one defeats the tripwire, because each module then passes against its own private semantics.

- compare the vendored copy against `fixtures/cross_module/canonical_parity_v1.json` semantically (field-by-field), not byte-wise;
- formatting may differ; content must not;
- if a copy is stale, refresh it — never edit the module copy to make a test pass.

### 4. Change a contract only deliberately

- The fixture is a **versioned** tripwire. A breaking change requires either backward-compatible consumers or a **new fixture version**.
- Do not overwrite an older fixture in a way that makes historical expectations ambiguous.
- Do not fork the semantics into a second incompatible fixture.
- When a contract changes, update: the contract document, the fixture, the repository's own verifier if its assertions are affected, and every module's vendored copy and conformance tool — in the same change set, with the module PRs cross-referenced.

### 5. Route implementation to the owning module

Contracts are owned here; **implementations are not**. If the fix is in the storage adapter, the record model or a view transform, it belongs in the owning module's repository. This repository documents and coordinates.

## Failure triage

| Symptom | Likely cause |
| --- | --- |
| identity differs after a round trip | an adapter is re-keying on a backend id |
| a nested section vanished | an adapter flattened a structured field, or a schema change was not propagated |
| review status changed | a stage auto-promoted provisional evidence |
| module passes, sibling fails | the change was applied to one copy of a shared contract |
| everything passes but CI disagrees | a vendored fixture copy is stale, or a module pinned an older fixture version |

## Reporting

When a contract defect is found, report it in the **owning** repository with sanitized, reproducible evidence (synthetic fixtures, counts, field paths — never research rows or private configuration). Search open and closed issues first. Cite the contract section that is violated, so the rule and the evidence travel together.

## Boundaries

- Never use real research data, private corpora, credentials or machine paths to demonstrate a contract failure. The fixture exists precisely so the check can be public and offline.
- Never weaken an assertion to make a red gate green. If the fixture and the module disagree, one of them is wrong and the difference is the finding.
- This skill does not authorize merging, deploying or restarting anything. See `skills/hermes-operations/SKILL.md` for the authority gate.
