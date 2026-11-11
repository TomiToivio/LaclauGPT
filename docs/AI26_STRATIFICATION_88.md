# #88 — the AI26 frame, measured, as the evidence behind the §4.2 rule

The rule itself was decided and merged in #89 (`docs/VALIDATION_PROTOCOL.md` §3, `paper/PHASE_1_PAPER.md`
§4.2): a **minimum reportable subgroup of 30 independently double-coded eligible documents**, below
which no subgroup-specific chance-corrected agreement estimate is published, with pooling allowed
only when preregistered and theoretically justified. This file records the measurement that makes
the rule necessary, so the numbers are not re-derived from memory each time the question comes back.

Measured 2026-11-11 against `ai26__records` (ready, `handoff.published_at` inside the declared
window `2026-09-01 .. 2026-12-31`), read-only, from Laskin.

## Arena × language

| arena | en | fi | unknown | other | total |
|---|---|---|---|---|---|
| elites | 2,367 | **26** | 54 | 32 | 2,479 |
| grassroots | 988 | **152** | 6 | 13 | 1,159 |
| parliamentary | 473 | **107** | 205 | 27 | 812 |
| arena-blank | 276 | 4 | 5 | 1 | 286 |
| **total** | **4,104** | **289** | 270 | 73 | 4,736 |

Finnish is 289 documents across three arenas. Analysis coverage of those cells is *not* the
problem — elites 25/26 (96 %), grassroots 149/152 (98 %), parliamentary 98/107 (92 %). The cells
are small because the material is small.

Against the 30-case guardrail: grassroots (152) and parliamentary (107) clear it in principle but
still need adequate category prevalence; **elites × fi (26) does not clear it at all**, so no
chance-corrected agreement estimate may be published for that cell.

The 286 arena-blank records are the `external-link-fetcher` children whose actor→arena mapping
never resolved (#336). Under §4.2 they are counted separately and cannot enter an arena-stratified
sample in any configuration.

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

No Finnish cell has a second source type, so a "source type" stratum cannot be populated inside
Finnish at all, in any arena. §4.2 now distinguishes allocation strata from descriptive coverage
dimensions precisely so this is stated rather than papered over.

## Why the rule is 30 and not a smaller number

At 30 an agreement statistic has a chance of being informative; below it the confidence interval is
wider than any difference the study could interpret. The protocol says this explicitly — it is a
reporting guardrail, not a power guarantee — which is the honest form: it stops a number being
published, and it does not pretend the number would have been reliable at 31.

## How to re-measure

The counts above are reproducible with the AI26 corpus audit and a read-only aggregation; the
Data-Analysis repository additionally carries `tools/ai26_ready_frame_audit.py`, which reports the
ready frame against analysed results per platform. Neither writes to the store.

## What this file does not do

It does not edit `paper/PHASE_1_PAPER.md`. §4.2 is the author's text; #89 already carries the
wording, and any further change to the claim is the author's decision.
