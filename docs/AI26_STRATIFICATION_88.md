# #88 — what the AI26 frame can actually support in §4.2

Measured 2026-11-11 against `ai26__records` (ready, `handoff.published_at` inside the declared
window `2026-09-01 .. 2026-12-31`), read-only, from Laskin.

The corpus has grown since the issue was written — 4,737 in-window ready records now, 3,135 of them
analysed — but the shape the issue describes is unchanged.

## Arena × language

| arena | en | fi | unknown | other | total |
|---|---|---|---|---|---|
| elites | 2,367 | **26** | 54 | 32 | 2,479 |
| grassroots | 988 | **152** | 6 | 13 | 1,159 |
| parliamentary | 473 | **107** | 205 | 27 | 812 |
| arena-blank | 276 | 4 | 5 | 1 | 286 |
| **total** | **4,104** | **289** | 270 | 73 | 4,736 |

Finnish is 289 documents across three arenas. Analysis coverage of the Finnish cells is *not* the
problem — elites 25/26 (96 %), grassroots 149/152 (98 %), parliamentary 98/107 (92 %). The cells
are small because the material is small.

The 286 arena-blank records are the same records the issue names: `external-link-fetcher` children
whose actor→arena mapping never resolved (#336). They cannot enter an arena-stratified sample in
any configuration.

## Cell grid, arena × language × platform

The binding constraint is not the arena row — it is the cell. Finnish documents come from two
routes only:

```
grassroots     rss      152
parliamentary  rss       82
parliamentary  bluesky   25
elites         rss       26
blank          x          4
```

There is no Finnish cell with a second source type. A "source type" stratum therefore cannot be
populated inside Finnish at all, in any arena.

## What each option in the issue would cost

| option | measured consequence |
|---|---|
| **1. minimum per-cell size, small cells pooled** | at n ≥ 20: elites×fi (26) survives as a bare cell; parliamentary×fi (107) and grassroots×fi (152) survive; everything with a second source type disappears. Pooled reporting is the only honest treatment for elites×fi. |
| **2. Finnish demoted to a robustness check** | en cells are ample (elites 2,367, grassroots 988, parliamentary 473). Agreement statistics on English only, Finnish as a qualitative cross-language illustration, requires no new data. |
| **3. extend the window or add Finnish elite sources** | the elites×fi cell is 26 documents in ~70 days from `rss` alone. Widening it is a source-selection decision (which Finnish elite outlets count), not a corpus accident — and the Eduskunta routes are closed (#88 comments, measured 2026-11-09). |
| **4. restrict the agreement claim to en × elites** | 2,367 documents, all analysed at 61.5 %. The narrowest defensible claim, and the only one that can be made today with room to spare. |

## The rule now recorded

`docs/VALIDATION_PROTOCOL.md` declares a **minimum cell size of 20 documents** and a pooling rule:
cells below it are never reported as independently estimated; they are pooled or reported as a
qualitative illustration. The threshold lives in the validation manifest, so it is a decision with
a number attached rather than an implicit judgement.

This is option 1 as the protocol default, because it changes how cells are *reported* rather than
what the study *claims*. Options 2 and 4 remain open and are cheaper to adopt — they narrow the
claim instead of qualifying it — and switching to either is a manifest change plus an edit to
§4.2 in the author's own words.

## What this document does not do

It does not edit `paper/PHASE_1_PAPER.md`. §4.2 is the author's text, and which claim the paper
makes is the author's decision — the issue says so explicitly. What is now in place is the
measurement and the rule; the sentence in §4.2 still has to be written by Tomi.
