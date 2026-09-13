# AI26 canonical formation vocabulary

AI26 uses a deliberately small computational vocabulary for ideological formation aggregation:

- `accelerationism`
- `doomerism`
- `left-wing accelerationism`
- `ai safety`
- `ai critical`
- `anti-ai`

These labels are **provisional sensitising concepts**, consistent with `paper/PAPER.md`. They are not a closed ontology of political thought and must not be inferred from actor identity alone.

Research vocabulary remains richer than the aggregation vocabulary. Terms such as techno-optimism, singularitarianism, TESCREAL, alignment, auditism, anti-hype, anti-Big-Tech, open-source advocacy, and policy governance may remain in evidence, source text, theoretical discussion, tags, and provenance without becoming additional top-level formations.

## Multi-label records

A document may receive zero, one, or several canonical formations when the evidence genuinely supports overlap. Compound strings are not canonical formation labels. For example:

```json
{
  "formations": ["doomerism", "ai safety"],
  "formation_tags": [],
  "formation_original": "x-risk doomerism / ai safety alignment",
  "formation_migration_version": "ai26-simple-v1",
  "formation_needs_review": false
}
```

Modifiers belong in `formation_tags` rather than expanding the formation taxonomy. Examples include `anti_big_tech`, `anti_hype`, `auditism`, `open_source_advocacy`, and `policy_governance`.

Unknown or context-dependent historical labels are preserved in `formation_original` and flagged with `formation_needs_review` when the analyzed evidence is insufficient for a safe mapping.

## Migration

Use:

```bash
python scripts/migrate_ai26_formations.py --dry-run data/analyzed/ai26.jsonl
```

The migration utility is idempotent, reports before/after counts, unknown labels, multi-label records, and review-required records. It refuses paths that look like raw/source/collection data. By default it writes a sibling `.ai26-simple` output. `--in-place` is opt-in and creates a backup first.

The migration is deterministic for simple aliases. Context-dependent historical labels are resolved only from existing analyzed evidence; no LLM call is required merely to rename categories.

## Spiralism boundary

AI Spiralism / synthetic spirituality is not part of the canonical AI26 ideological formation vocabulary. If retained in the repository, it remains an exploratory source family with separate analytical boundaries.
