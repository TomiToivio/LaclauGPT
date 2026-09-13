# Research-data publication audit

This audit covers the public default branch and its publication boundary. It is a repository-level screening, not institutional legal or data-protection review and not a forensic scan of every historical Git object.

## Executive assessment

The public repository should expose reusable research machinery rather than institutional research material.

### PUBLIC

- source code, generic collectors and adapters;
- methods, schemas and conceptual codebooks;
- generic configuration templates;
- synthetic fixtures and example URLs;
- non-identifying provenance and workflow documentation;
- aggregate outputs only after disclosure/licensing review.

### RESTRICTED

- raw or derived human research data;
- subject/account mappings and document-level annotations;
- project-specific empirical codebooks;
- named-person analytical mappings;
- operational storage paths, manifests and reprocessing jobs;
- machine-local or study-specific deployment configuration;
- credentials, tokens, private network information and research-data dumps.

## Legacy institutional research

Project-specific integrations from earlier institutional studies are not published as active research configurations on the current default branch. Reusable mechanics have been generalized under `legacy` compatibility modules and templates. Public legacy surfaces contain no project-specific countries, actor mappings, seed codebooks, storage layouts, manifests, scheduler allocations, or research-subject records.

Any retained institutional legacy material belongs in controlled storage or another explicitly authorized access-controlled location and remains subject to the originating project's governance, ethics, data-protection, licensing, and publication rules.

## Existing safeguards

- runtime research data is not a Git publication surface;
- downloaded source content, media, transcripts, database files and runtime outputs are excluded;
- live source selection and operational collection configuration remain private;
- public machine/runtime profiles are templates rather than deployment records;
- publication-safety tests scan for common credentials, private paths, production storage indicators and operational source registries;
- public examples should use synthetic identities and URLs.

## Git-history note

This sanitization applies to the current public branch. Git history is not rewritten automatically. If institutional review determines that historical objects contain material requiring removal, treat that as a separate remediation task with explicit human approval.

## Licensing

Do not apply a data licence to third-party social-media material merely because it was publicly accessible. Software, documentation, original schemas, synthetic fixtures and project-owned metadata must be licensed according to their own rights status. Privacy, data-protection, copyright/database rights and platform terms remain separate constraints.

## Open-science target state

**Open methods, open code, open semantics, open documentation, open provenance, synthetic examples and safe aggregates; controlled project-specific research material and human-level data.**
