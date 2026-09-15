# CyborgAnthropology legacy-code recycling audit

Date: 2026-09-16

This is a second-pass addendum to `docs/FUNCTIONAL_PARITY_AUDIT.md` and issue #5.

The first parity audit concentrated too heavily on `TomiToivio/LaclauGPT-Discourse-Analysis`. That was insufficient because `TomiToivio/CyborgAnthropology` contains an older but substantial collection/ingestion stack whose reusable behavior should also be considered when modularizing LaclauGPT.

The rule for this pass is **recycle behavior, not monolithic coupling**. Useful acquisition, normalization, metadata, ingestion and orchestration ideas should move into the appropriate modular package. Hard-coded project policy, credentials, operational endpoints, machine paths, private targets and old storage coupling must not.

## High-value collection code found

| Legacy path | Capability | New home | Status | Action |
|---|---|---|---|---|
| `data_collection/mastodon_collector.py` | Mastodon instance clients, hashtag/public timelines, toot identity, author/account metadata, media refs, engagement metrics | LaclauGPT-Data-Collection | MISSING / REIMPLEMENT_CLEANLY | Data Collection #11 |
| `data_collection/telegram_collector.py` | Telethon channel acquisition, stable message/channel IDs and URLs, media hooks, text/raw text | LaclauGPT-Data-Collection | MISSING / REIMPLEMENT_CLEANLY | Data Collection #11 |
| `data_collection/youtube_collector.py` | yt-dlp metadata/channel discovery, transcript API, optional Whisper fallback/audio | LaclauGPT-Data-Collection + Analysis boundary for ASR | PARTIAL / MISSING | Data Collection #11 |
| `data_collection/arxiv_collector.py` | arXiv search/category acquisition, authors/categories/dates, optional PDFs | LaclauGPT-Data-Collection | MISSING | Data Collection #11 |
| `data_collection/x_collector.py` | X account acquisition via Apify, raw response retention, author/language/media/engagement metadata | LaclauGPT-Data-Collection | PARTIAL | Reconcile with current X parser/browser path in #11 |
| `data_collection/rss_collector.py` | RSS acquisition | LaclauGPT-Data-Collection | ALREADY COVERED | Compare edge cases only |
| `data_collection/bluesky_collector.py` | Bluesky acquisition | LaclauGPT-Data-Collection | ALREADY COVERED | Compare metadata parity only |

## Reusable ingestion/document machinery

| Legacy path | Capability | New home | Status | Action |
|---|---|---|---|---|
| `data_collection/base_collector.py` | normalized item creation, dedup/source identity, language detection, HTTP/file helpers, file/API output | Data Collection core/adapters | PARTIAL / REIMPLEMENT_CLEANLY | Extract generic behavior into typed adapters; do not copy old class wholesale |
| `data_collection/pdf_collector.py` | PyMuPDF/PyPDF2/pdfplumber extraction, metadata, abstract/keyword heuristics, chunking | Data Collection document adapter, optional Analysis chunking boundary | MISSING | Data Collection #11 |
| `data_collection/directory_ingestion.py` | incoming/processed/error spool, offline batch validation, file fallback | Data Collection local/HPC ingestion | MISSING / USEFUL | Data Collection #11 |
| `data_collection/ingestion.py` | ingestion API/object-storage ideas | Collection/storage boundary | PARTIAL | Reconcile with current storage adapters; preserve Allas/S3 portability |
| `data_collection/data_injection_agent.py` | validation/routing/relevance-filter/research-note concepts | mostly project policy / Research Assistant | MIXED | Keep generic validation/routing; do not make AGI keyword heuristics generic Collection behavior |
| `data_collection/agi_scraper_agent.py` | search discovery, HTTP + Playwright fallback, RSS, URL-memory/dedup, autonomous orchestration | Collection + optional Research Assistant | MIXED / REIMPLEMENT_CLEANLY | Reuse orchestration concepts only |

## Mastodon findings

`mastodon_collector.py` is a real reusable collector, not historical scaffolding. It contains:

- a `Mastodon.py` client per instance;
- optional authenticated or public access;
- hashtag timeline collection;
- public timeline collection;
- canonical source/toot URL construction;
- duplicate checks;
- HTML-to-text normalization;
- account display name, username and profile URL;
- media attachment URL extraction;
- favourites, boosts/reblogs and reply counts;
- instance-level configuration.

The modular implementation should preserve these source semantics while emitting the current canonical record model with stable `source_url`, typed source metadata and provenance. It should not depend directly on legacy MongoDB helpers.

## Telegram findings

The old Telethon collector contains useful acquisition behavior:

- channel-scoped collection;
- message and channel IDs;
- stable source URLs;
- raw and normalized text;
- media acquisition hooks;
- session/API credential handling concepts;
- language/translation hooks.

The new implementation should keep Telethon session files, phone numbers, API IDs/hashes and target-channel lists outside Git. Translation belongs behind an optional enrichment boundary rather than being inseparable from acquisition.

## YouTube findings

The old YouTube collector has more functionality than the current generic platform parser path:

- recent-video discovery from channels through yt-dlp;
- video metadata acquisition;
- transcript retrieval through `youtube-transcript-api`;
- optional audio download;
- Whisper fallback when transcripts are unavailable.

Collection should own discovery/metadata/transcript acquisition. ASR execution can remain an optional acquisition/enrichment adapter with provenance, while interpretive analysis stays in Data Analysis.

## arXiv and PDF/document findings

The arXiv collector provides query/category search, bibliographic metadata and optional PDF acquisition. The PDF collector adds multiple text-extraction backends, document metadata extraction, abstract/keyword heuristics and overlapping text chunks.

These are valuable for papers, reports and books and should not disappear merely because the initial modular split emphasized social-platform collection.

The clean architecture is:

```text
arXiv / URL / local PDF
        -> document acquisition
        -> canonical source identity + bibliographic metadata
        -> optional object-storage reference
        -> text extraction / representation
        -> downstream Analysis
```

Document extraction must not be coupled directly to a specific MongoDB or vector database.

## X/Apify findings

The old X collector uses Apify for account acquisition and preserves raw responses, language, translation, author, tweet ID, media and engagement-oriented metadata. The new Collection repository already has X normalization/browser support, so the correct action is not blind duplication.

Instead, Apify should be considered one optional acquisition adapter feeding the same canonical X normalizer. Provider-specific actor IDs, tokens and storage logic must stay outside the canonical parser.

## Offline/HPC ingestion finding

`directory_ingestion.py` implements a useful spool pattern:

```text
incoming/*.json -> validate -> persist -> processed/
                              \-> error/
```

This is particularly useful for laptops, cron jobs and CSC/HPC batch jobs where direct service connectivity may be unavailable or undesirable. The modular system should either implement this pattern or explicitly document a better equivalent.

## Security and privacy finding

At least one historical autonomous-agent file contains hard-coded operational connection information. None of those values should be copied into the modular public repositories or examples.

Legacy repositories should therefore be treated as archaeological source code. During migration:

- secrets and endpoints become environment/config inputs;
- target lists remain private operational data;
- real corpora/raw captures are never copied;
- project ideology keyword lists belong to study configuration/codebooks, not generic collection defaults;
- old MongoDB/S3 coupling is replaced by current storage interfaces.

## Updated parity assessment

The collection side of the modular architecture cannot yet be called fully parity-complete. The following important source families are still unrepresented as first-class modular collectors or documented replacements:

- Mastodon;
- Telegram;
- YouTube metadata/transcript acquisition;
- arXiv;
- general PDF/document ingestion;
- offline directory-spool ingestion;
- optional X/Apify acquisition parity.

These are tracked in `TomiToivio/LaclauGPT-Data-Collection#11`.

Until that issue is implemented or each capability is explicitly deprecated with a reason, umbrella issue #5 should remain open.
