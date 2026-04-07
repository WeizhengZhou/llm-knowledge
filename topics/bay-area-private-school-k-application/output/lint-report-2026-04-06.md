# Lint Report — Bay Area Private School K Application — 2026-04-06

## Summary

| Severity | Count |
|----------|-------|
| Errors | 9 |
| Warnings | 18 |
| Info | 5 |
| **Total** | **32** |

## Gate Status

ERRORS FOUND — 9 errors must be resolved before wiki is considered trustworthy.

Error IDs: E001, E002, E003, E004, E005, E006, E007, E008, E009

---

## Quality Gate: L1+L2 Density

All 16 graduated wiki articles carry `confidence: L1` or `confidence: L2`. No graduated article carries L3. The two articles in `wiki/` subdirectories (`wiki/concepts/assessment-prep.md` and `wiki/guides/public-vs-private.md`) are staging-tier; `public-vs-private.md` carries `confidence: L3` and `epistemic_status: single-source`. Both are flagged under E008 and E009 for wrong-directory placement.

The L1+L2 density requirement is met for articles that legitimately belong in `wiki/`.

---

## Errors (must fix)

### [E001] S4 stale_data + legacy_valid_until: application-timeline.md — cycle_bound article past cycle close date

- **File:** `topics/bay-area-private-school-k-application/wiki/application-timeline.md` (lines 37–39)
- **Finding:** The article carries both `valid_until: 2026-07-01` (a legacy field) and `volatile: cycle_bound`. Today is 2026-04-06, which is past the 2025-26 cycle's enrollment response deadline of March 26, 2026. Per S4, `cycle_bound` articles must be flagged `error` when the current date is past the cycle's close date. The article's opening block correctly notes all deadlines are "historical" but the frontmatter `valid_until: 2026-07-01` implies the article is valid until July — a misleading signal that conflicts with the article's own disclaimer. The `valid_until` field is also a legacy field per SCHEMA.md.
- **Required fix:** Remove the legacy `valid_until` field. Retain `volatile: cycle_bound`. Update `_index.md` to label this article as an archived 2025-26 cycle document. When 2026-27 school data becomes available (expected August 2026), run `/kb-update` to create a fresh cycle article.

### [E002] S3 legacy_valid_until: school-profiles-sf.md has both valid_until and volatile

- **File:** `topics/bay-area-private-school-k-application/wiki/school-profiles-sf.md` (lines 28–29)
- **Finding:** Frontmatter contains both `valid_until: 2027-07-01` and `volatile: annual`. Per SCHEMA.md, `valid_until` is a legacy field; articles must use only `volatile:` class. The coexistence of both fields is a legacy_valid_until violation. Additionally, the tuition comparison table mixes year references (`$48,577 (2025-26)` for SF Day, `$3,500-$48,895 (2026-27)` for CDS, `$46,300 (2026-27)` for CAIS), producing an apples-to-oranges tuition comparison without consistent year labeling.
- **Required fix:** Remove `valid_until: 2027-07-01` from frontmatter. Retain `volatile: annual`. Audit all tuition figures in the article to normalize year labels.

### [E003] S3 legacy_valid_until: financial-aid.md has both valid_until and volatile

- **File:** `topics/bay-area-private-school-k-application/wiki/financial-aid.md` (line 19)
- **Finding:** Frontmatter contains `valid_until: 2027-07-01` alongside `volatile: annual`. Same legacy-field-coexistence violation as E002.
- **Required fix:** Remove `valid_until: 2027-07-01` from frontmatter. Retain `volatile: annual`.

### [E004] S3 legacy_valid_until: ravenna-hub.md has both valid_until and volatile

- **File:** `topics/bay-area-private-school-k-application/wiki/ravenna-hub.md` (line 12)
- **Finding:** Frontmatter contains `valid_until: 2027-07-01` alongside `volatile: annual`. Same legacy-field violation.
- **Required fix:** Remove `valid_until: 2027-07-01` from frontmatter. Retain `volatile: annual`.

### [E005] S3 legacy_valid_until: issfba-bada.md has both valid_until and volatile

- **File:** `topics/bay-area-private-school-k-application/wiki/issfba-bada.md` (lines 14–15)
- **Finding:** Frontmatter contains `valid_until: 2027-07-01` alongside `volatile: annual`. Same legacy-field violation.
- **Required fix:** Remove `valid_until: 2027-07-01` from frontmatter. Retain `volatile: annual`.

### [E006] C4 contradiction: Keys School decision date — "Feb 19, 2026" in comparison table vs. "March 20" everywhere else

- **File A:** `topics/bay-area-private-school-k-application/wiki/school-profiles-peninsula-east-bay.md` (line 33)
- **File B:** `topics/bay-area-private-school-k-application/wiki/application-timeline.md` (lines 62, 138, 158); `wiki/issfba-bada.md` (line 46); `wiki/school-profiles-peninsula-east-bay.md` (line 60, same file)
- **Finding:** The comparison table on line 33 of `school-profiles-peninsula-east-bay.md` shows Keys School decision date as `Feb 19, 2026`. Every other reference to Keys School's decision date in the wiki — including the Keys School detail section on line 60 of the same article, `application-timeline.md` lines 62, 138, and 158, and `issfba-bada.md` — states `March 20`. The Keys School detail section (line 60) explicitly states: "The February 19 date previously cited was a data extraction error." The comparison table was not corrected to match this acknowledged correction. A reader consulting only the comparison table will receive a definitively wrong date.
- **Required fix:** Update the comparison table at `school-profiles-peninsula-east-bay.md` line 33 to show `Mar 20, 2026 (L3)`. Remove the "data extraction error" acknowledgment note from the detail section (the correction has been made; the note no longer needs to document a discrepancy that no longer exists once the table is fixed).

### [E007] S1 broken_wikilink: [[assessment-prep]] — target file not found at wiki/assessment-prep.md

- **File:** `topics/bay-area-private-school-k-application/wiki/application-timeline.md` (line 180); `topics/bay-area-private-school-k-application/wiki/south-bay-schools.md` (lines 38, 76, 186, 203)
- **Finding:** Five occurrences of `[[assessment-prep]]` across two articles link to a target slug `assessment-prep`. There is no file at `wiki/assessment-prep.md`. A file named `assessment-prep.md` exists at `wiki/concepts/assessment-prep.md`, a subdirectory path. Wikilink resolution requires a flat slug match; `[[assessment-prep]]` does not resolve to a subdirectory file under standard wikilink conventions.
- **Required fix:** Either (a) move `wiki/concepts/assessment-prep.md` to `wiki/assessment-prep.md` (requires resolving E008 first to confirm graduation status), or (b) update all five `[[assessment-prep]]` occurrences to use the correct path syntax for subdirectory files. The choice depends on the resolution of E008.

### [E008] wrong_directory_placement: wiki/concepts/assessment-prep.md is in wiki/ but listed as staging

- **File:** `topics/bay-area-private-school-k-application/wiki/concepts/assessment-prep.md`
- **Finding:** `_index.md` line 31 lists `staging/assessment-prep.md` as pending wiki-critic review. However, the file physically exists at `wiki/concepts/assessment-prep.md`, not under `staging/`. No wiki-critic READY status is documented in the file or any pipeline log. The article has bypassed the staging → critic → graduation pipeline. Its frontmatter carries `confidence: L1` and `epistemic_status: confirmed`, which are appropriate quality levels, but graduation requires explicit critic sign-off per the pipeline rules.
- **Required fix:** Run wiki-critic review on this article. If it passes, move to `wiki/assessment-prep.md` (recommended: flat wiki root, not subdirectory), update `_index.md` to list it under Concepts, and update the frontmatter backlinks. If it does not pass, move back to `staging/assessment-prep.md` and remove from `wiki/`.

### [E009] wrong_directory_placement: wiki/guides/public-vs-private.md is in wiki/ but listed as staging; carries sub-standard confidence

- **File:** `topics/bay-area-private-school-k-application/wiki/guides/public-vs-private.md`
- **Finding:** `_index.md` line 32 lists `staging/public-vs-private.md` as pending wiki-critic review. The file physically exists at `wiki/guides/public-vs-private.md`. No wiki-critic approval is documented. Critically, this article carries `confidence: L3` and `epistemic_status: single-source` — below the L1+L2 quality bar required for graduated wiki articles. It also has only one source (`raw/web/news/2026-04-06_public-vs-private-bay-area-decision-framework.md`). A single-source L3 article in the wiki/ directory is a trust failure: the quality gate should have blocked this graduation.
- **Required fix:** Move `wiki/guides/public-vs-private.md` back to `staging/public-vs-private.md` immediately. Run wiki-critic review. The article needs additional sources to pass L2 confidence before graduation. Update `_index.md` to remove it from the wiki section (it should remain listed under Staging only).

---

## Warnings (should fix)

### [W001] S2 orphaned_page: wiki/concepts/assessment-prep.md — no working incoming links

- **File:** `topics/bay-area-private-school-k-application/wiki/concepts/assessment-prep.md`
- **Finding:** The only incoming links to this article use the broken `[[assessment-prep]]` slug (see E007). Because those links are broken, this article is effectively unreachable. It also does not appear in any `_index.md` wiki section listing.
- **Suggested fix:** Resolve E007 and E008 first. Once the article is properly placed and the wikilinks corrected, add an entry to `_index.md` under Concepts.

### [W002] S2 orphaned_page: wiki/guides/public-vs-private.md — no incoming links, not in index

- **File:** `topics/bay-area-private-school-k-application/wiki/guides/public-vs-private.md`
- **Finding:** No wiki article links to `[[public-vs-private]]`. The article does not appear under any wiki section in `_index.md`. It is entirely unreachable from within the wiki.
- **Suggested fix:** Resolve E009 first (return to staging). If graduated in a future run, add incoming links from `overview.md` and `financial-aid.md`, and list in `_index.md` under Guides.

### [W003] CV5 unlisted_article: wiki/concepts/assessment-prep.md not listed in _index.md wiki sections

- **File:** `topics/bay-area-private-school-k-application/wiki/concepts/assessment-prep.md`
- **Finding:** The article exists in `wiki/` but is listed only in the "Staging" note of `_index.md`, not under any Concepts, Guides, or Entities section. Any article in `wiki/` must be listed in `_index.md` under a proper wiki section to be discoverable.
- **Suggested fix:** Resolve E008 first. After graduation, add to `_index.md` under Concepts.

### [W004] CV5 unlisted_article: wiki/guides/public-vs-private.md not listed in _index.md wiki sections

- **File:** `topics/bay-area-private-school-k-application/wiki/guides/public-vs-private.md`
- **Finding:** Same issue as W003. The article exists in `wiki/guides/` but is not listed under any `_index.md` wiki section.
- **Suggested fix:** Resolve E009 first. After proper graduation, add to `_index.md` under Guides.

### [W005] S4 annual volatility: Stratford tuition data is labeled 2025-26 while peer data is 2026-27

- **File:** `topics/bay-area-private-school-k-application/wiki/stratford-school.md` (line 25); `wiki/south-bay-schools.md` (lines 40, 52, 168); `wiki/guides/public-vs-private.md` (line 32); `wiki/transitional-kindergarten.md` (lines 63, 94)
- **Finding:** Stratford's TK/K tuition of `$25,170 (2025-26, Almaden)` is from the prior academic year. All other selective school tuition data in the wiki uses 2026-27 figures (Harker: $46,350/$51,550 2026-27; CAIS: $46,300 2026-27; Town School: ~$46,935 2026-27; Children's Day: $48,895 2026-27). The comparison table in `south-bay-schools.md` line 52 places Stratford's 2025-26 figure directly alongside Harker's 2026-27 figure, creating a misleading apples-to-oranges cost comparison. The `volatile: annual` class and `updated: 2026-04-06` date indicate this should have been refreshed in the current pipeline run.
- **Suggested fix:** Retrieve 2026-27 Stratford tuition from the official admissions page and update all six locations where the 2025-26 figure appears. Until then, add a parenthetical "(2025-26; 2026-27 not yet available)" to every instance to signal the data-year difference.

### [W006] C1 unsourced_claim: transitional-kindergarten.md line 46 — district TK expansion figures

- **File:** `topics/bay-area-private-school-k-application/wiki/transitional-kindergarten.md` (line 46)
- **Finding:** "SFUSD added 15 TK programs in 2025-26, Oakland USD added 7, and San Jose USD added 3" is attributed only to "the raw research file citing district sources." No specific source URL is in the frontmatter for this claim, and no `According to [source]...` attribution is in the prose. The claim contains specific numerical data (15, 7, 3) with no verifiable source chain.
- **Suggested fix:** Add the specific district source URLs to the frontmatter `sources` list and rewrite with explicit attribution (e.g., "According to [district source]..."), or remove the specific numbers and replace with a general statement about TK expansion.

### [W007] C1 unsourced_claim: transitional-kindergarten.md lines 50–51 — CDE "guaranteed K seat" claim self-described as unverified

- **File:** `topics/bay-area-private-school-k-application/wiki/transitional-kindergarten.md` (lines 50–51)
- **Finding:** The article states: "According to the raw research file citing CDE sources, starting 2026-27 all public TK students receive a guaranteed kindergarten seat at their feeder school. This specific claim was not independently confirmed on the CDE FAQ page during live verification." A claim documented within the article itself as unconfirmed should not appear in the article body. It is presented as a factual statement with only a trailing caveat, which is insufficient — the first half of the sentence reads as fact before the caveat appears.
- **Suggested fix:** Remove this claim from the article body. If the pipeline team wishes to preserve it for future investigation, move it to a `claims/` dispute article noting the unresolved status. Do not present an independently-unconfirmed claim as a stated fact even with an embedded disclaimer.

### [W008] C1 unsourced_claim: assessment-playdate.md line 99 — WPPSI duration "1-2 hours" uses non-standard citation format

- **File:** `topics/bay-area-private-school-k-application/wiki/assessment-playdate.md` (line 99)
- **Finding:** The line reads `Duration: 1-2 hours (source: SF Standard, December 2025)`. This is the only place in any wiki article where a parenthetical `(source: ...)` format is used instead of the standard `According to [source]...` attribution pattern. The SF Standard is listed in frontmatter sources and the citation is present, but the formatting inconsistency may cause automated citation-checking tools to miss it.
- **Suggested fix:** Reformat to: "According to the SF Standard (December 2025), the WPPSI assessment takes 1-2 hours."

### [W009] C1 unsourced_claim: pedagogy-philosophy.md lines 93–94 — Terra San Francisco description from L3 aggregator without prose attribution

- **File:** `topics/bay-area-private-school-k-application/wiki/pedagogy-philosophy.md` (lines 93–94)
- **Finding:** "TestingForKindergarten.com describes Terra San Francisco as a PreK-8 Reggio Emilia-inspired school in the Richmond District with Mandarin and Spanish language learning." The source (testingforkindergarten.com) is an L3 aggregator listed in frontmatter, but in the prose the attribution is implicit: the prior paragraph names the source, but the sentence itself does not include the `According to [source]...` marker. The source attribution is one sentence away.
- **Suggested fix:** Rewrite as: "TestingForKindergarten.com describes Terra San Francisco as a PreK-8 Reggio Emilia-inspired school in the Richmond District with Mandarin and Spanish language learning." (The fix is to make the attribution explicit in the same sentence, which it almost is — the current prose says "TestingForKindergarten.com lists" in the prior paragraph about SF Waldorf, then the Terra description follows without re-attributing.)

### [W010] C2 single_source_claim: high density of must_verify claims with sources_checked: 1

- **Files:** Multiple articles (all SF school profiles, ISSFBA article, Harker, Challenger, Stratford)
- **Finding:** Review of `fact-sheet.yaml` shows that the large majority of verified claims carry `sources_checked: 1`. Examples: C001 (SF Day age cutoff), C002 (SF Day deadline), C011 (SF Day $48,577 tuition), C017 (SF School deadline), C029 (CDS deadline), C035 (CDS sliding scale tuition). All are designated `must_verify` in `claims-register.yaml` and all are single-source. This is an acceptable outcome of budget-constrained research but represents systemic single-source risk for all deadline and tuition claims throughout the wiki.
- **Suggested fix:** During the next `/kb-update` cycle, prioritize cross-verifying tuition figures and application deadlines via secondary sources (local press, admissions consultant published guides, school marketing materials). Specifically target claims where the single source is the school's own website, as these are subject to removal or change without notice.

### [W011] CV3 incomplete_comparison: school-profiles-sf.md comparison table — 7 of 11 schools have tuition as "--"

- **File:** `topics/bay-area-private-school-k-application/wiki/school-profiles-sf.md` (lines 37–50)
- **Finding:** The main SF school comparison table has 11 school rows. Tuition is populated for only 4 (SF Day: $48,577, CDS: $3,500-$48,895, CAIS: $46,300, Town School: ~$46,935). The remaining 7 schools — Convent & Stuart Hall, The Hamlin School, Live Oak School, Presidio Hill School, SF Friends School, La Scuola International, and The San Francisco School — all show "--" for tuition. The most common reader question is "how much does this school cost?" and the table fails to answer it for 64% of the schools listed.
- **Suggested fix:** Research and add 2026-27 tuition for the 7 missing schools. For schools with indexed/sliding scale tuition (Live Oak, Presidio Hill, SF Friends), note the tuition model and link to the financial-aid article. The Hamlin School tuition is notable by its absence given the school's detailed financial aid budget ($3.14M) is known.

### [W012] CV3 incomplete_comparison: school-profiles-peninsula-east-bay.md — Nueva School decision date "--" despite being confirmed elsewhere

- **File:** `topics/bay-area-private-school-k-application/wiki/school-profiles-peninsula-east-bay.md` (line 34)
- **Finding:** Nueva School's decision date shows "--" in the comparison table. However, `application-timeline.md` line 136, `issfba-bada.md` line 46, and the Keys School detail section of the same article (line 60) all state explicitly that "Nueva School K-8 admissions decisions are released March 20, 2026 at approximately 4 p.m. via Ravenna." This confirmed fact exists in the wiki but was not propagated to the comparison table.
- **Suggested fix:** Update the Nueva School row in the comparison table to show `Mar 20, 2026` for decision date.

### [W013] CV3 incomplete_comparison: language-immersion.md comparison table — EBGIS row is entirely "--"

- **File:** `topics/bay-area-private-school-k-application/wiki/language-immersion.md` (line 35)
- **Finding:** East Bay German International School (EBGIS) appears as a comparison table row with all data fields as "--" except Language (German) and Location (East Bay). The article itself acknowledges EBGIS is a stub at line 113. A table row with zero data except category labels provides no useful information and may mislead readers into thinking the school is viable for comparison when no data exists.
- **Suggested fix:** Remove EBGIS from the comparison table until it is individually researched. Retain the mention in the "Not Yet Individually Researched" section.

### [W014] CV3 incomplete_comparison: south-bay-schools.md "How South Bay Differs from SF" table — Almaden platform potentially misidentified

- **File:** `topics/bay-area-private-school-k-application/wiki/south-bay-schools.md` (line 178)
- **Finding:** The "How South Bay Differs" comparison table groups Almaden Country Day with Challenger and Stratford as "school-specific (Challenger, Stratford, Almaden)" for the admissions platform column. However, the Almaden Country Day profile section (line 118) describes an "online application" with no platform name. The `south-bay-schools.md` article also states at line 122 that "The March 19 decision date is consistent with ISSFBA coordinated timing" and that the school "uses the ISSFBA standard Confidential Student Evaluation form" — both suggesting possible Ravenna use, which is not reflected in the comparison table.
- **Suggested fix:** Verify whether Almaden Country Day uses Ravenna or a proprietary system. Update both the comparison table and the entity profile section. If Ravenna, the table should reflect that (and the school could be listed in the `ravenna-hub.md` article).

### [W015] CV2 unanswered_question: gap_fill phase budget-exhausted with no per-question status tracking

- **File:** `topics/bay-area-private-school-k-application/research-plan.yaml` (lines 36–47)
- **Finding:** The gap_fill phase is marked `budget_exhausted` as of 2026-04-06. It contains 23 questions (QG001–QG004, qE001–qE019). None of these questions have `status: answered` or `answered_at` dates recorded in the research plan. It is impossible to determine from the research plan which gap_fill questions were answered before budget exhaustion and which were skipped. This breaks CV2 checks for the entire gap_fill phase.
- **Suggested fix:** Update `research-plan.yaml` to record individual question status for all gap_fill questions: mark each as `status: answered`, `status: skipped`, or `status: budget_exhausted` with notes. This will enable precise coverage gap tracking in future lint runs.

### [W016] S3 missing_frontmatter (functional): all 16 articles have backlinks: [] — cross-linker not run

- **File:** All 16 graduated wiki articles
- **Finding:** Every article in `wiki/` has `backlinks: []` (empty array) in frontmatter. The backlinks field is structurally present (satisfying S3 technically), but the cross-linker tool was not run to populate it. Empty backlinks prevent orphan detection accuracy and break the query-agent's ability to traverse the wiki graph.
- **Suggested fix:** Run `backend/tools/cross_linker.py` against the `wiki/` directory immediately after resolving E007 (so that broken links do not generate false backlinks). This is a zero-research mechanical fix.

### [W017] C6 empty_section: multiple articles have section headings with thin content

- **File:** `topics/bay-area-private-school-k-application/wiki/challenger-school.md` (line 59: "Feeder/Pipeline" section); `wiki/stratford-school.md` (line 55: "Feeder/Pipeline" section)
- **Finding:** Both Challenger School and Stratford School have a "Feeder/Pipeline" section that contains only one sentence stating no feeder pipeline was documented: "No preschool-to-kindergarten priority structure was documented for Challenger School in available community or official sources." / "No preschool-to-kindergarten priority structure was documented for Stratford School in available community or official sources." A section heading with a single negative-finding sentence conveys little value and may create false expectations for readers.
- **Suggested fix:** Either fold the negative finding into the Application Process section as a parenthetical note, or remove the section heading and incorporate the information into the Overview paragraph.

### [W018] CV3 incomplete_comparison: school-profiles-sf.md — La Scuola comparison table row missing Age Cutoff, Decision Date, and Platform

- **File:** `topics/bay-area-private-school-k-application/wiki/school-profiles-sf.md` (line 47)
- **Finding:** The La Scuola International row in the SF comparison table shows "--" for Age Cutoff, Decision Date, and Platform. Yet the La Scuola profile section in the same article (lines 282–298) and the `language-immersion.md` article have substantive La Scuola data. The La Scuola profile section notes the general deadline is January 15, 2026 and sibling deadline is December 1, 2025. No decision date is confirmed in any article for La Scuola, but the missing age cutoff and platform should be researchable.
- **Suggested fix:** Research La Scuola age cutoff and admissions platform from official source. Populate the comparison table. Add La Scuola decision date to the fact-checker backlog.

---

## Info (improvement opportunities)

### [I001] CV1 missing_entity_article: Nueva School mentioned in 5 articles, no dedicated entity profile

- **Finding:** Nueva School is referenced substantively in `school-profiles-peninsula-east-bay.md` (full profile section), `assessment-playdate.md`, `admissions-strategy.md`, `concepts/assessment-prep.md`, and `financial-aid.md`. It is the most selective school in the research set (IQ minimum 130, ~20-22 K openings) and has significantly more verified fact-sheet claims than either Challenger or Stratford, both of which have standalone entity articles. The school profile in `school-profiles-peninsula-east-bay.md` is comprehensive but not independently navigable.
- **Suggestion:** Create `wiki/nueva-school.md` as a standalone entity article using the existing profile section as a base. This would be the highest-value new article for query-agent accuracy on gifted-program admissions questions.

### [I002] CV1 missing_entity_article: Helios School mentioned in 4 articles, no dedicated entity profile

- **Finding:** Helios School has detailed admissions, assessment, and tuition data in `south-bay-schools.md` (the most detailed South Bay subsection after Harker) and is referenced in `assessment-playdate.md`, `pedagogy-philosophy.md`, and `application-timeline.md`. It is a gifted-focused school with WPPSI-IV/WISC-V requirements, a January 8 deadline, and confirmed ISSFBA-coordinated March 19 decisions. No standalone `[[helios-school]]` entity article exists.
- **Suggestion:** Create `wiki/helios-school.md` as a standalone entity article using the Helios subsection in `south-bay-schools.md` as the source. This would enable direct wikilinks and improve query-agent precision on IQ-test school comparisons.

### [I003] CV1 missing_entity_article: Lycee Francais de San Francisco mentioned in 3 articles, no dedicated profile

- **Finding:** Lycee Francais appears in `language-immersion.md` (full profile section), `application-timeline.md`, and `pedagogy-philosophy.md`. The school has a critical structural difference from other K programs (CP grade requires age 6 by September 1, one year older than standard US kindergarten cutoff) that warrants prominent standalone documentation.
- **Suggestion:** Create `wiki/lycee-francais.md`. The CP age-offset finding is the most important distinguishing fact in the immersion category and is currently buried in the language-immersion article rather than surfaced at the entity level.

### [I004] CV1 missing_entity_article: Gideon Hausner Jewish Day School mentioned in 3 articles, no dedicated profile

- **Finding:** Gideon Hausner has detailed data in `south-bay-schools.md` (two-round admissions system, April 16 Round 2, $42,480 K-4 tuition 2026-27, 40% professional partner discount, Sibling Savings Program) and is referenced in `application-timeline.md` and `admissions-strategy.md`. The two-round admissions structure is unique among the schools researched and merits a standalone entity article.
- **Suggestion:** Create `wiki/gideon-hausner.md` as a standalone entity profile.

### [I005] fact_checker note: verified_claims in fact-sheet.yaml use claim-level valid_until dates (not volatile classes)

- **Finding:** In `fact-sheet.yaml`, each verified claim carries its own `valid_until` date (e.g., C001 `valid_until: 2026-08-01`, C003 `valid_until: 2026-03-20`). This is the expected format for claim-level tracking and is distinct from the article-level `volatile:` class. These claim-level `valid_until` dates are not legacy violations — they are the correct mechanism at the claim level. However, many claim-level `valid_until` dates are in the past as of 2026-04-06 (e.g., C003 `valid_until: 2026-03-20`, C004 `valid_until: 2026-03-24`, C005 `valid_until: 2026-01-12`). These represent claims about cycle-specific dates that have now passed and should be re-verified when the 2026-27 cycle data becomes available.
- **Suggestion:** When running `/kb-update` for the 2026-27 cycle, use the claim-level `valid_until` dates to prioritize which claims need re-verification. Claims where `valid_until` is past should be the first targets for fact-checker-agent review.

---

## Structural Findings Detail

### S1 Wikilink Audit

All wikilinks in all 18 articles (16 graduated + 2 wrong-directory) were scanned for `[[...]]` patterns and checked against files present in `wiki/`:

**Broken wikilinks (1 slug, 5 occurrences):**
- `[[assessment-prep]]` — `wiki/application-timeline.md` line 180; `wiki/south-bay-schools.md` lines 38, 76, 186, 203. No file at `wiki/assessment-prep.md`. (E007)

**All other internal wikilinks verified intact:**
`[[overview]]`, `[[school-profiles-sf]]`, `[[school-profiles-peninsula-east-bay]]`, `[[harker-school]]`, `[[challenger-school]]`, `[[stratford-school]]`, `[[issfba-bada]]`, `[[application-timeline]]`, `[[financial-aid]]`, `[[assessment-playdate]]`, `[[admissions-strategy]]`, `[[south-bay-schools]]`, `[[pedagogy-philosophy]]`, `[[language-immersion]]`, `[[ravenna-hub]]`, `[[transitional-kindergarten]]` — all resolve to existing `wiki/[slug].md` files. Note: `[[public-vs-private]]` is not linked from any article, so generates no broken-link error, but the article is unreachable (W002).

### S5 Filename Convention Audit

All 18 filenames in `wiki/` (excluding `_index.md`): kebab-case, no uppercase letters, no spaces, no date prefixes. No violations found.

### S3 Frontmatter Completeness Audit

All 16 graduated articles have all required fields present and non-empty: `title`, `type`, `created`, `updated`, `sources` (non-empty), `tags`, `epistemic_status`, `confidence`, `backlinks`. All `type` values are from the permitted set (`entity`, `guide`, `concept`, `overview`). All `epistemic_status` values are from the permitted set. Confidence: all graduated articles carry L1 or L2. The only structural violations are the legacy `valid_until` fields present alongside `volatile:` in 5 articles (covered by E001–E005).

---

## Coverage Summary

- Articles in wiki/ directory: 18 total (16 graduated; 2 wrong-directory staging articles)
- Articles properly graduated: 16 (should be 14 once E008/E009 are resolved)
- `wiki/overview.md`: EXISTS — no CV4 error
- Entities with dedicated profiles: 4 (Harker School, Challenger School, Stratford School, ISSFBA/BADA)
- Major entities with profile sections only (no standalone article): Nueva School, Helios School, Gideon Hausner, Lycee Francais
- Broken wikilinks: 1 slug (`assessment-prep`), 5 occurrences
- Orphaned articles: 2 (`wiki/concepts/assessment-prep.md`, `wiki/guides/public-vs-private.md`)
- Articles with empty backlinks arrays: 16 of 16 (cross-linker not run)
- Legacy `valid_until` fields: 5 articles
- Comparison tables: 7 found; 4 have incomplete rows (W011, W012, W013, W018)
- Research-plan gap_fill phase: budget_exhausted; 23 questions with no individual status records (W015)

---

## Recommended Next Actions

1. **Fix the Keys School date contradiction in school-profiles-peninsula-east-bay.md line 33 (E006).** This is the most immediately harmful error: a reader consulting the comparison table will get the wrong decision date (Feb 19 vs. the correct Mar 20). The fix is a one-line table edit plus removing the now-redundant "data extraction error" note from the detail section.

2. **Move wiki/guides/public-vs-private.md back to staging/ (E009).** This L3, single-source article bypassed the wiki-critic review and quality gate. It should not be in `wiki/`. Moving it back to staging is the priority because it actively degrades the wiki's trustworthiness profile if a reader or query-agent encounters it.

3. **Strip all five legacy `valid_until` fields (E002–E005, part of E001).** These are mechanical one-field deletions in `school-profiles-sf.md`, `financial-aid.md`, `ravenna-hub.md`, and `issfba-bada.md`. For `application-timeline.md` (E001), also update the `_index.md` description to reflect the article's archived status.

4. **Resolve the assessment-prep staging/placement issue (E008) and fix all five broken [[assessment-prep]] wikilinks (E007).** The correct resolution path: run wiki-critic on `wiki/concepts/assessment-prep.md`; if approved, relocate to `wiki/assessment-prep.md` (flat root, not subdirectory), update `_index.md`, and update all five `[[assessment-prep]]` links. This resolves E007, E008, W001, and W003 together.

5. **Run backend/tools/cross_linker.py to populate backlinks (W016).** All 16 articles have empty `backlinks: []`. This is a zero-research mechanical fix that should run after E007 is resolved (to avoid logging broken links as real backlinks). Resolves W016 and enables accurate S2 orphan detection in future lint runs.
