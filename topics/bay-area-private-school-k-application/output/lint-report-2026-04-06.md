# Lint Report — bay-area-private-school-k-application
**Date:** 2026-04-06
**Gate:** BLOCKED (2 errors must be resolved before publishing)

## Summary

| Severity | Count |
|----------|-------|
| Errors   | 2     |
| Warnings | 11    |
| Info     | 5     |
| **Total** | **18** |

---

## Errors (must fix before publishing)

### [E001] stale_data: application-timeline.md valid_until has expired

- **File:** `wiki/application-timeline.md` (line 30)
- **Finding:** `valid_until: 2026-03-27` is 10 days past today (2026-04-06). All time-sensitive data in this article is now stale for the active cycle.
- **Required fix:** Update `valid_until` to `2026-10-01` and add a notice that dates reflect the completed 2025-26 cycle.

### [E002] missing_overview: wiki/overview.md does not exist

- **File:** `wiki/overview.md` (missing)
- **Finding:** No synthesizing entry point exists. A query-agent asked a broad question has no root article. The `_index.md` lists 9 sub-articles but no overview.
- **Required fix:** wiki-compiler-agent must create `wiki/overview.md` covering: topic scope, ISSFBA framework, general timeline, two assessment models (playdate vs. IQ), financial aid overview, and navigation links.

---

## Warnings (should fix)

### [W001] backlinks_empty: Cross-linker never run — all 9 articles have empty backlinks arrays

- **Files:** All 9 wiki articles
- **Finding:** Every article has `backlinks: []`. Wikilinks exist throughout the articles but reciprocal backlinks are not recorded. Blocks orphan detection and degrades query-agent traversal.
- **Suggested fix:** Run `backend/tools/cross_linker.py` against the wiki directory.

### [W002] metadata_count_error: _index.md header says "Articles: 8" but 9 articles are listed

- **File:** `wiki/_index.md` (line 4)
- **Finding:** 3 entity + 4 guide + 2 concept articles = 9 total. Header shows 8.
- **Suggested fix:** Change line 4 to `Articles: 9`.

### [W003] duplicate_row_confusion: The San Francisco School appears twice in the January Application Deadlines table

- **File:** `wiki/application-timeline.md` (lines 64 and 69)
- **Finding:** Line 64 shows a Clarity financial aid deadline (Jan 9) mixed into the Application Deadlines table alongside the actual application deadline (Jan 23) in line 69. Both rows show the same $100 fee, creating confusion.
- **Suggested fix:** Remove line 64 (Clarity row) from this table; it already appears correctly in the Financial Aid Deadlines table. Add a cross-reference footnote to the Jan 23 row.

### [W004] incomplete_comparison: CAIS Decision Date is blank in SF comparison table

- **File:** `wiki/school-profiles-sf.md` (line 45)
- **Finding:** CAIS decision date shows `--` in the comparison table and in the CAIS profile section. Likely follows ISSFBA March 19 date but unverified.
- **Suggested fix:** Verify via official CAIS admissions page. Update table and add verified claim to fact-sheet.yaml.

### [W005] incomplete_comparison: La Scuola row missing Age Cutoff, Decision Date, and Platform

- **File:** `wiki/school-profiles-sf.md` (line 46)
- **Finding:** Three of eight comparison columns are `--` for La Scuola. All three fields are publicly available on `lascuolasf.org`.
- **Suggested fix:** Research and fill from official admissions page.

### [W006] incomplete_comparison: Keys School (Age Cutoff) and Nueva School (Decision Date) missing in Peninsula table

- **File:** `wiki/school-profiles-peninsula-east-bay.md` (lines 29-30)
- **Finding:** Keys School age cutoff and Nueva School decision date both show `--`. Both fields should be on their respective official admissions pages.
- **Suggested fix:** Fill from official sources.

### [W007] unsourced_claim: Tuition inflation rate (4-6% annually) not in fact-sheet

- **File:** `wiki/financial-aid.md` (line 95)
- **Finding:** Claim attributed to Redwood Grove Wealth Management (a financial advisory/marketing source) bypassed the claim-extractor and fact-checker pipelines. No confidence level or permitted-language constraint exists.
- **Suggested fix:** Submit to fact-checker-agent. If rated L3 or below, add epistemic qualifier or remove.

### [W008] unsourced_claim: Two KQED statistics in financial-aid.md not in fact-sheet

- **File:** `wiki/financial-aid.md` (lines 111 and 113)
- **Finding:** "KQED: SF private school tuition ranges $10K-$65K" and "KQED: 30% of SF K-12 students attend private schools (2023-24)" have no fact-sheet entries. Both claims bypassed the fact-checker pipeline entirely.
- **Suggested fix:** Add both claims to fact-sheet.yaml via fact-checker-agent with confidence levels and permitted_language.

### [W009] stubs_unresearched: 8 stub schools in _index.md have zero wiki content

- **Files:** `wiki/_index.md` (lines 22-29)
- **Finding:** No articles exist for: Harker School, Helios School, Redwood Day School, Gideon Hausner, Lycee Francais, Terra SF, Silicon Valley International School, East Bay German International School.
- **Suggested fix:** Prioritize Harker (fact-sheet claim C163 already verified) and Helios, then the four immersion schools. Add all 8 to gap_fill phase in research-plan.yaml.

### [W010] sort_order_error: January deadline table is not chronologically sorted

- **File:** `wiki/application-timeline.md` (lines 57-70)
- **Finding:** First row is Keys School (Jan 9), but Presidio Hill (Jan 5) and Live Oak (Jan 6) appear later. A parent scanning for earliest deadlines will miss them.
- **Suggested fix:** Re-sort ascending: Presidio Hill (Jan 5) → Live Oak (Jan 6) → Nueva/Town (Jan 8) → Keys/Head-Royce (Jan 9) → La Scuola (Jan 15) → CAIS/Park Day (Jan 16) → Children's Day (Jan 20) → The San Francisco School (Jan 23) → Marin Horizon (Jan 30).

### [W011] coverage_gap: Educational philosophies answered in research but absent from wiki

- **Finding:** Research plan Q007 (composite 7.9) and Q007a (composite 6.7) are both `status: answered` with raw sources collected. No wiki article covers Quaker (SF Friends), progressive (Park Day, CDS), traditional (Town School, Hamlin), Montessori, or Waldorf philosophies.
- **Suggested fix:** Add a "Pedagogical Philosophy" section to `admissions-strategy.md`, or create a standalone `pedagogy-philosophy.md` article.

---

## Info (improvement opportunities)

### [I001] Harker School has verified fact-sheet data (C163) but no article

- **Finding:** Fact-sheet entry C163 (L2, confirmed) covers Harker's IQ test deadline (Jan 23, 2026). It is the most research-ready stub in the wiki.
- **Suggestion:** Create a minimal Harker stub article using existing fact-sheet data.

### [I002] South Bay school coverage absent despite Q001c marked answered

- **Finding:** Q001c answered in research but no South Bay wiki content exists beyond Harker/Helios mentions.
- **Suggestion:** Add explicit "Not Yet Researched" section to `school-profiles-peninsula-east-bay.md` acknowledging the South Bay gap, or create a `school-profiles-south-bay.md` stub.

### [I003] CAIS decision date unresearched across all sources

- **Finding:** CAIS decision date is `--` in both the comparison table and profile. March 19 likely applies but is unverified.
- **Suggestion:** Add to next fact-checker pass.

### [I004] language-immersion.md is thin and largely duplicates school-profiles-sf.md

- **File:** `wiki/language-immersion.md`
- **Finding:** Only CAIS and La Scuola have substantive content (~180 words unique to this article). Four stub programs (Lycee Francais, Terra SF, SVIS, EBGIS) have no data. The article adds little value over the SF school profiles.
- **Suggestion:** Research the four stub immersion programs. Add immersion model details (full vs. partial ratios) and outcomes data.

### [I005] school-profiles-peninsula-east-bay.md title overstates coverage

- **File:** `wiki/school-profiles-peninsula-east-bay.md`
- **Finding:** East Bay coverage is limited to Head-Royce and Park Day (both Oakland). No Berkeley, Piedmont, Alameda, or South Bay schools are covered. Title implies comprehensive Bay Area coverage outside SF.
- **Suggestion:** Add introductory note listing which sub-regions are fully vs. partially researched, or rename to reflect partial coverage.

---

## Coverage Summary

| Metric | Value |
|--------|-------|
| Articles checked | 9 |
| Overview article | Missing (E002) |
| Schools with full profiles | 17 (11 SF, 6 Peninsula/East Bay/Marin) |
| Schools as stubs only | 8 |
| Broken wikilinks | 0 |
| Orphaned articles | 0 |
| Backlinks populated | 0 of 9 (cross-linker not run) |
| Wiki claims without fact-sheet entries | 3 (W007, W008) |
| Fact-sheet claims without wiki coverage | 0 |

---

## Recommended Next Actions (priority order)

1. **Run cross-linker** (`backend/tools/cross_linker.py`) — zero-research fix, resolves W001
2. **Fix `valid_until`** in `application-timeline.md` line 30: `2026-03-27` → `2026-10-01` — resolves E001
3. **Create `wiki/overview.md`** via wiki-compiler-agent — resolves E002 (only remaining hard blocker)
4. **Remove duplicate SF School row** from January deadlines table (`application-timeline.md` line 64) — resolves W003
5. **Fix `_index.md` article count**: `Articles: 8` → `Articles: 9` — resolves W002
6. **Submit 3 unsourced wiki claims to fact-checker-agent** (`financial-aid.md` lines 95, 111, 113) — resolves W007, W008
7. **Add 8 stub schools to gap_fill phase** in `research-plan.yaml` — enables W009 resolution via `/kb-research --phase gap`
