# Lint Report — Bay Area Private School K Application — 2026-04-06 (v2)

## Summary

| Severity | Count |
|----------|-------|
| Errors   | 4     |
| Warnings | 14    |
| Info     | 4     |
| **Total** | **22** |

**Gate Status:** ERRORS FOUND (E001 is historical data / cycle closed; E002 fixed in this run; E003 and E004 need action)

---

## Errors (must fix)

### [E001] stale_data: application-timeline.md valid_until has passed

- **File:** `wiki/application-timeline.md` (line 30)
- **Finding:** `valid_until: 2026-03-27` has passed. The 2025-26 cycle closed March 26, 2026. All deadlines documented are now historical.
- **Required fix:** Add cycle-closed notice at top of article. Update `valid_until` to `2026-07-01` as archive boundary, or rename to `application-timeline-2025-26.md` and create a fresh `application-timeline.md` stub for 2026-27 cycle.

### [E002] contradiction: pedagogy-philosophy.md — wrong school deadlines *(FIXED in this run)*

- **File A:** `wiki/pedagogy-philosophy.md` (line 97) — was "CDS January 23, SF Day January 23, Live Oak January 15, Presidio Hill January 30"
- **Corrected to:** CDS January 20, SF Day December 19, Live Oak January 6, Presidio Hill January 5
- **Status:** Fixed.

### [E003] missing_frontmatter: volatile class absent from 4 articles

Articles using legacy `valid_until` without `volatile:` class:
- `wiki/school-profiles-sf.md` — add `volatile: annual`
- `wiki/financial-aid.md` — add `volatile: annual`
- `wiki/issfba-bada.md` — add `volatile: annual`
- `wiki/language-immersion.md` — add `volatile: annual`
- `wiki/ravenna-hub.md` — add `volatile: annual`

### [E004] missing_frontmatter: backlinks empty across all 16 articles

- **Finding:** Every article has `backlinks: []`. Cross-linker was run but may not have written back.
- **Required fix:** Re-run `backend/tools/cross_linker.py topics/{slug}/wiki/` and verify output.

---

## Warnings (should fix)

### [W001] unsourced_claim: pedagogy-philosophy.md — deadline figures lack inline source attribution
- **Suggested fix:** Add "(source: [[school-profiles-sf]])" after deadline figures.

### [W002] orphaned_page: transitional-kindergarten.md — under-linked
- `school-profiles-sf.md` (Presidio Hill TK section) and `admissions-strategy.md` should link to `[[transitional-kindergarten]]`.

### [W003] orphaned_page: language-immersion.md — under-linked
- Comparison table entries for CAIS and La Scuola in `school-profiles-sf.md` should link to `[[language-immersion]]`.

### [W004] incomplete_comparison: school-profiles-sf.md — 11 empty cells
- CAIS decision date should be "Mar 19 (ISSFBA)" per `application-timeline.md` evidence.
- La Scuola age cutoff, decision date, and platform all `--` — needs gap-fill research.

### [W005] incomplete_comparison: school-profiles-peninsula-east-bay.md — Keys School age cutoff missing
- Flag for next gap-fill research pass.

### [W006] incomplete_comparison: school-profiles-peninsula-east-bay.md — Nueva decision date missing
- Flag for next gap-fill research pass.

### [W007] thin_article: ravenna-hub.md — ~144 words of body content
- Below 150-word minimum. Expand "How It Works" section from `raw/web/official/2026-04-06_ravennasolutions-families.md`.

### [W008] thin_article: language-immersion.md — stubs dominate
- Add immersion-specific content (language split, classroom model, progression path) for CAIS and La Scuola.

### [W009] missing_cycle_warning: application-timeline.md has no closed-cycle notice
- Add top-of-article note: "This guide covers the 2025-26 admissions cycle (now closed). Check individual school websites starting August 2026 for 2026-27 data."

### [W010] single_source: C011, C017, C029, C065 — high-stakes claims with only one source
- SF Day tuition, SF School deadline, CDS deadline, Live Oak deadline each have `sources_checked: 1`.
- Live Oak March 17 decision date (C067) is an anomaly vs. ISSFBA March 19 — flag for re-verification.

### [W011] unconfirmed_claim: transitional-kindergarten.md — CDE guaranteed-seat claim
- The "guaranteed K seat starting 2026-27" claim was not confirmed on CDE FAQ during live verification.
- Change `epistemic_status` to `likely` and add "(claim not confirmed on CDE FAQ; requires re-verification)".

### [W012] aggregator_data: south-bay-schools.md — Challenger tuition `~$12,000 (L3, undated)`
- Move confidence qualifier to a table footnote. Replace cell value with `—` and document the figure in prose with explicit L3 attribution.

### [W013] metadata_count: _index.md shows "Articles: 15" but 16 articles exist
- Change line 4 to "Articles: 16".

### [W014] missing_volatile: ravenna-hub.md uses valid_until without volatile class
- Add `volatile: annual` to frontmatter.

---

## Info (improvement opportunities)

### [I001] Nueva School — 7 mentions across wiki but no standalone entity article
- Create `wiki/nueva-school.md` extracting the profile section from `school-profiles-peninsula-east-bay.md`.

### [I002] Helios, BASIS SV, Gideon Hausner — stubs with mostly `--` in comparison table
- Add targeted gap-fill research questions or remove from comparison table to avoid misleading readers.

### [I003] Feeder preschools — research answered Q023 but wiki coverage is thin
- Add "Feeder Preschools" subsection to `admissions-strategy.md` drawing from Hamlin FAQ source.

### [I004] Open houses — Q032 answered in research but not consolidated in wiki
- Add "Open Houses" section to `application-timeline.md` with all confirmed open house dates.

---

## Coverage Summary

| Metric | Value |
|--------|-------|
| Articles checked | 16 |
| Overview articles | 1 (overview.md ✓) |
| Entity profiles | 6 (SF schools, Peninsula/EB, Harker, Challenger, Stratford, ISSFBA) |
| Guide articles | 6 |
| Concept articles | 3 |
| Broken wikilinks | 0 |
| Orphaned articles | 0 (all in _index.md) |
| L5 claims in wiki | 0 |
| Comparison tables | 4 |
| Questions with wiki coverage | ~30/38 answered |

## Recommended Next Actions

1. Re-run `backend/tools/cross_linker.py` and verify backlinks are written (E004)
2. Add `volatile: annual` to 5 articles using only `valid_until` (E003)
3. Add cycle-closed notice to `application-timeline.md` + update `valid_until` to `2026-07-01` (E001)
4. Fix `_index.md` count: 15 → 16 (W013)
5. Add TK + language-immersion wikilinks to under-linked articles (W002, W003)
