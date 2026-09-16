# Sources workspace

This directory is the publication-safe source-reading workspace for LaclauGPT.

## Workflow

1. Drop local PDF files into `sources/pdfs/`.
2. PDF files are intentionally ignored by Git and must remain local unless a source is explicitly licensed and intended for redistribution.
3. Ask an agent to inspect the PDFs and update the tracked Markdown files in this directory.
4. Keep `SOURCES.md` as the compact bibliographic/source index for sources actually imported/processed as local PDFs.
5. Keep `SUMMARIES.md` as the human-readable source summary file.
6. Keep `READING_SUGGESTIONS.md` as the cumulative related-work / reading queue for relevant literature discovered during searches, repository work, issue preparation, or research discussions, even when no local PDF has been added yet.

Recommended agent behavior for each new PDF:

- identify title, authors, year, venue/publisher, DOI/URL when available, and filename;
- add or update one entry in `SOURCES.md`;
- add a concise analytical summary in `SUMMARIES.md`;
- distinguish the source's claims from LaclauGPT's interpretation;
- explain relevance to the current paper in `paper/PAPER.md` when material;
- note useful concepts, methods, datasets, findings, limitations, and quotations only when necessary;
- avoid copying long copyrighted passages;
- do not infer bibliographic details that cannot be verified from the PDF;
- never commit the PDFs themselves, extracted full text, private annotations, or research data.

Recommended agent behavior whenever new LaclauGPT-related literature is discovered, even without a local PDF:

- check `READING_SUGGESTIONS.md` first to avoid duplicates;
- add or update a concise verified bibliographic entry when the source is plausibly relevant to LaclauGPT theory, methodology, empirical AI/AGI discourse, or validation/triangulation methods;
- state briefly why it may matter for LaclauGPT rather than merely collecting titles;
- prefer DOI/publisher/arXiv links and verified metadata;
- move or cross-reference the item into `SOURCES.md` / `SUMMARIES.md` if the source is later imported and actually processed;
- treat inclusion as a reading suggestion, not endorsement or automatic incorporation into the paper.

## Suggested structure

```text
sources/
├── README.md
├── READING_SUGGESTIONS.md
├── SOURCES.md
├── SUMMARIES.md
└── pdfs/              # local only, Git-ignored
```

The Markdown files are meant to become a cumulative reading map for the project rather than a dump of generated notes. Prefer concise, source-grounded entries and update existing entries instead of duplicating them.
