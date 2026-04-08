# Lint Report — Bay Area Private School K Application — 2026-04-07

## Summary

| Severity | Count |
|----------|-------|
| Errors   | 8     |
| Warnings | 11    |
| Info     | 4     |
| **Total** | **23** |

## Gate Status

ERRORS FOUND — 8 errors must be resolved before wiki is considered trustworthy.

Error IDs: E001, E002, E003, E004, E005, E006, E007, E008

---

## Errors (must fix)

### [E001] S1: Broken wikilink — `[[financial-realities]]` resolves to nonexistent file
- **File:** `topics/bay-area-private-school-k-application/wiki/financial-aid.md` (lines 108, 152)
- **Finding:** The wikilink `[[financial-realities]]` is used twice in `financial-aid.md` (line 108: "see [[financial-realities]]"; line 152: "[[financial-realities]] -- True cost of ownership"). The file `wiki/financial-realities.md` does not exist. The article actually lives at `wiki/guides/financial-realities.md`, so the correct wikilink is `[[guides/financial-realities]]`.
- **Required fix:** Replace all occurrences of `[[financial-realities]]` with `[[guides/financial-realities]]` in `financial-aid.md`.

### [E002] S1: Broken wikilink — `[[financial-realities]]` in `public-vs-private.md` and `admissions-strategy-advanced.md`
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/public-vs-private.md` (line 57); `topics/bay-area-private-school-k-application/wiki/guides/admissions-strategy-advanced.md` (line 178)
- **Finding:** Both articles use the bare `[[financial-realities]]` wikilink. `wiki/financial-realities.md` does not exist; the article lives at `wiki/guides/financial-realities.md`. The same issue applies to two additional cross-links in `guides/financial-realities.md` itself (line 23), which uses `[[guides/public-vs-private]]` — that link IS correctly formed since `wiki/guides/public-vs-private.md` exists. The broken links are the bare `[[financial-realities]]` forms.
- **Required fix:** Replace `[[financial-realities]]` with `[[guides/financial-realities]]` in both files listed above.

### [E003] S1: Broken wikilink — `[[admissions-strategy-advanced]]` resolves to nonexistent file
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/parent-essay-guide.md` (line 87); `topics/bay-area-private-school-k-application/wiki/guides/school-tour-guide.md` (line 129)
- **Finding:** Both articles link `[[admissions-strategy-advanced]]`. The file `wiki/admissions-strategy-advanced.md` does not exist. The article lives at `wiki/guides/admissions-strategy-advanced.md`, requiring the wikilink `[[guides/admissions-strategy-advanced]]`.
- **Required fix:** Replace `[[admissions-strategy-advanced]]` with `[[guides/admissions-strategy-advanced]]` in both files.

### [E004] S1: Broken wikilink — `[[school-tour-guide]]` and `[[parent-essay-guide]]` resolve to nonexistent files
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/parent-essay-guide.md` (line 88 — `[[school-tour-guide]]`); `topics/bay-area-private-school-k-application/wiki/guides/school-tour-guide.md` (line 117 — `[[parent-essay-guide]]`)
- **Finding:** `[[school-tour-guide]]` would resolve to `wiki/school-tour-guide.md` (does not exist; actual path is `wiki/guides/school-tour-guide.md`). `[[parent-essay-guide]]` would resolve to `wiki/parent-essay-guide.md` (does not exist; actual path is `wiki/guides/parent-essay-guide.md`).
- **Required fix:** Replace `[[school-tour-guide]]` with `[[guides/school-tour-guide]]` in `parent-essay-guide.md`; replace `[[parent-essay-guide]]` with `[[guides/parent-essay-guide]]` in `school-tour-guide.md`.

### [E005] S4: Stale data — `cycle_bound` article past cycle close date
- **File:** `topics/bay-area-private-school-k-application/wiki/application-timeline.md` (frontmatter, line 37)
- **Finding:** `volatile: cycle_bound`. Today's date is 2026-04-07. The article's cycle close date (March 26, 2026 ISSFBA enrollment response deadline) has passed. Per S4 rules, a `cycle_bound` article must be flagged as an error once the current date is past the cycle's close date. The article already carries a banner at line 43 noting the cycle is "historical," which is correct, but the frontmatter `epistemic_status: confirmed` and `confidence: L1` are no longer accurate — these values reflected live cycle data. The wiki consumer has no automated signal that this article is now stale beyond the prose banner.
- **Required fix:** Update `epistemic_status` to `single-source` or add a `stale_since: 2026-03-27` field; or update `volatile` handling per SCHEMA.md guidance to trigger wiki-compiler re-run at cycle open (August 2026).

### [E006] C4: Contradiction — Harker K tuition figure inconsistent across articles
- **File A:** `topics/bay-area-private-school-k-application/wiki/guides/financial-realities.md` (line 46)
- **File B:** `topics/bay-area-private-school-k-application/wiki/harker-school.md` (line 27, 74); `topics/bay-area-private-school-k-application/wiki/south-bay-schools.md` (line 46); `topics/bay-area-private-school-k-application/wiki/school-profiles-peninsula-east-bay.md` (line 39)
- **Finding:** `financial-realities.md` line 46 states "Harker K $47,400" in a parenthetical noting it as a confirmed figure. All other articles in the wiki cite verified fact-sheet claim C182: "2026-27 tuition is $46,350 for TK and $51,550 for kindergarten through grade 5." The $47,400 figure does not match either the TK rate ($46,350) or the K-5 rate ($51,550). It appears to be a stale figure from raw research (the raw file referenced in C182 originally stated "$49,900 (2025)" before live verification corrected it to current rates). The $47,400 figure is present in no verified claim and contradicts C182.
  - `financial-realities.md` line 46: `"Harker K $47,400"`
  - `harker-school.md` line 27: `"Tuition, K-5 (2026-27) | $51,550"`
- **Required fix:** Replace "Harker K $47,400" in `financial-realities.md` with "Harker K-5 $51,550 (2026-27)" per verified claim C182.

### [E007] C5: Possible blocked-claim territory — `financial-realities.md` cites $520K figure flagged as unverifiable
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/financial-realities.md` (lines 31-36)
- **Finding:** The article states: "The raw research file from Redwood Grove Wealth Management references a total K-12 cost estimate of approximately $520,000 over 13 years … However, live verification of redwoodgrovewm.com (April 2026) did not return this specific figure on the page." The fact-sheet dispute d006 and overreach flag mof014 explicitly note that "$520K not on live page." The article appropriately qualifies the figure as a modeled estimate not found during live verification. This is not a full C5 violation (the article does not state it as confirmed fact and wraps it in an epistemic note). However, the figure "$520,000" appears as a live claim attribute ("approximately $520,000") in prose that does not use `permitted_language` framing. The fact-sheet has no `verdict: confirmed` for the $520K figure — only an epistemic note. This finding is elevated to error because the $520K figure is effectively unverifiable from its cited source, and the article's epistemic note does not prevent a reader from treating it as a real datum.
- **Required fix:** Remove the specific dollar figure "$520,000" from the prose or clearly label it as "not confirmed on live source." The claim should either use the $500K-$700K range from Basic Fund (which has a confirmed source) or be excised. The current phrasing ("references … approximately $520,000 … live verification did not return this specific figure") is ambiguous — a reader may anchor on $520K.

### [E008] CV5: Index out of sync — four wiki articles listed as staging in `_index.md`
- **File:** `topics/bay-area-private-school-k-application/wiki/_index.md` (lines 33-37)
- **Finding:** `_index.md` lists four articles under the heading "## Staging (Pending Wiki-Critic Review)" with staging-format slugs (`[[financial-realities|Financial Realities]]`, `[[admissions-strategy-advanced|Advanced Admissions Strategy]]`, `[[parent-essay-guide|Parent Essay Guide]]`, `[[school-tour-guide|School Tour and Open House Guide]]`). These files actually exist at `wiki/guides/financial-realities.md`, `wiki/guides/admissions-strategy-advanced.md`, `wiki/guides/parent-essay-guide.md`, and `wiki/guides/school-tour-guide.md` — they are graduated wiki articles, not staging articles. `index.md` (the topic-level index) also lists these four as "Staging (pending wiki-critic review)" (lines 32-37) pointing to `staging/` subdirectory paths that do not exist. This is a material structural error: query-agent and human users reading `_index.md` will not find these articles under the Guides section, and the broken wikilinks noted in E001-E004 are a direct consequence of this staging confusion.
- **Required fix:** Move all four article entries from the "Staging" section to the "Guides" section in `wiki/_index.md`, updating their wikilink slugs to `[[guides/financial-realities|...]]` etc. Update `index.md` similarly. Update `backlinks` frontmatter in each of the four articles.

---

## Warnings (should fix)

### [W001] S2: Orphaned pages — four new guide articles have no incoming wikilinks from wiki articles
- **Files:** `wiki/guides/financial-realities.md`, `wiki/guides/admissions-strategy-advanced.md`, `wiki/guides/parent-essay-guide.md`, `wiki/guides/school-tour-guide.md`
- **Finding:** All four articles have `backlinks: []` in their frontmatter. Incoming links from other wiki articles use the bare (broken) form `[[financial-realities]]` etc., which would not resolve. Until E001-E004 are fixed, no article correctly links to these four guides. Additionally, `overview.md` has no links to any of these four guides. Once wikilinks are corrected, the cross-linker tool should be re-run to populate `backlinks`.
- **Suggested fix:** After fixing E001-E004 wikilinks, run the cross-linker tool; add at least one valid incoming link to each guide from `overview.md`.

### [W002] S2: Orphaned page — `wiki/concepts/assessment-prep.md` not linked from `overview.md`
- **File:** `topics/bay-area-private-school-k-application/wiki/concepts/assessment-prep.md`
- **Finding:** The `_index.md` lists this article as `[[concepts/assessment-prep|K Assessment Preparation]]`. The `overview.md` "Key Concepts" section (lines 79-84) links to `[[transitional-kindergarten]]`, `[[pedagogy-philosophy]]`, `[[ravenna-hub]]`, `[[financial-aid]]`, and `[[language-immersion]]` — but not to `[[concepts/assessment-prep]]`. The article is linked from `application-timeline.md` (line 179) and `south-bay-schools.md` (line 38), so it is not fully orphaned, but `overview.md` — the root navigation — does not list it.
- **Suggested fix:** Add `[[concepts/assessment-prep]]` to the "Key Concepts" section of `overview.md`.

### [W003] S2: Orphaned page — `wiki/guides/public-vs-private.md` not linked from `overview.md`
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/public-vs-private.md`
- **Finding:** `_index.md` lists this article at `[[guides/public-vs-private|Public vs. Private K Decision Framework]]`. The `overview.md` "Navigation" sections do not include a link to it. It is linked from `guides/financial-realities.md` (correctly, using `[[guides/public-vs-private]]`) but has no path from the main navigation.
- **Suggested fix:** Add `[[guides/public-vs-private]]` to the "By Topic" navigation section of `overview.md`.

### [W004] S4: Legacy `valid_until` fields in fact-sheet claims (non-blocking but violates SCHEMA)
- **File:** `topics/bay-area-private-school-k-application/fact-sheet.yaml` (throughout)
- **Finding:** The majority of claims in the fact-sheet use `valid_until:` date fields (e.g., C001: `valid_until: "2026-08-01"`, C003: `valid_until: "2026-03-20"`) rather than the `volatile:` class system specified in SCHEMA.md. The SCHEMA.md states: "Volatile claims use `volatile:` class (annual/cycle_bound/evergreen/none) — not hard `valid_until` dates. Lint agent flags stale data by volatility class automatically." Only a subset of Harker-related claims (C176, C177, C178, C180, C181, C182) use the `volatile:` field. This means the lint agent cannot automatically flag stale fact-sheet entries by volatility class for most claims.
- **Suggested fix:** Migrate fact-sheet claims to use `volatile:` class instead of `valid_until:` in the next fact-checker-agent pass. This is a schema compliance issue, not an immediate accuracy problem.

### [W005] S4: `annual` volatile articles — `updated` date is 2026-04-06, within 12 months (no flag needed now, but note)
- **Files:** `wiki/school-profiles-sf.md`, `wiki/financial-aid.md`, `wiki/harker-school.md`, `wiki/challenger-school.md`, `wiki/stratford-school.md`, etc. (all `volatile: annual`, `updated: 2026-04-06`)
- **Finding:** All `volatile: annual` articles were updated 2026-04-06, which is 1 day ago. No staleness flag is triggered (within 12-month window). However, several of these articles contain 2025-26 cycle data (deadline dates, tuition figures) that will become stale in the 2026-27 cycle. `/kb-update` should be run in September 2026 to refresh all `volatile: annual` articles.
- **Suggested fix:** Add a calendar reminder to run `/kb-update bay-area-private-school-k-application` in September 2026. No immediate action required.

### [W006] C1: Unsourced numerical claim — `financial-realities.md` "Harker K $47,400"
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/financial-realities.md` (line 46)
- **Finding:** (Overlaps with E006.) The figure "$47,400" for Harker K has no corresponding verified claim in the fact-sheet. No `(source: ...)` attribution is present. The nearest verified claim C182 specifies $51,550 for K-5 (2026-27). This unsourced figure is also a contradiction (see E006). Flagged here separately as a sourcing failure.
- **Suggested fix:** Remove $47,400 and replace with the verified C182 figure.

### [W007] C1: Unsourced numerical claim — `financial-realities.md` "Nueva Upper School $66,960"
- **File:** `topics/bay-area-private-school-k-application/wiki/guides/financial-realities.md` (line 46)
- **Finding:** The figure "Nueva Upper School $66,960" appears in `financial-realities.md` line 46 ("consistent with confirmed school-specific tuition data: Nueva Upper School $66,960"). No verified claim in the fact-sheet contains this figure. C126 specifies "tuition ranges from $30,555 (PK) to $51,285 (high school)." The $66,960 figure is inconsistent with the fact-sheet's $51,285 upper range (which references a different year or a different subset of fees). No source attribution is present in the article text.
- **Suggested fix:** Remove or source "Nueva Upper School $66,960." If this figure is from the raw research file and was not independently verified, remove it. The verified Nueva tuition range is $30,555-$51,285 per C126.

### [W008] C2: Single-source must-verify claims — no corroboration flagging in wiki
- **Files:** Multiple articles
- **Finding:** The claims-register and fact-sheet contain a large number of claims with `sources_checked: 1`. Under C2, single-source claims with `priority: must_verify` should be flagged when they appear in wiki articles, particularly those with temporal or financial values. Representative examples include: C002 (SF Day deadline, single source), C011 (SF Day tuition $48,577, single source), C017 (SF School deadline January 23, single source), C029 (CDS deadline January 20, single source), and C155 (ISSFBA March 19 date, single source — though corroborated by pattern). The wiki articles for these schools display these values as fact without any "single source" qualifier visible to the reader.
- **Suggested fix:** This is a systemic pattern. The wiki-compiler-agent should add inline epistemic notes ("single official source") to high-stakes single-source numerical/temporal claims in entity articles, especially tuition figures and deadlines. At minimum, flag during the next `/kb-update` cycle.

### [W009] CV3: Incomplete comparison table — `language-immersion.md` has EBGIS row with all dashes
- **File:** `topics/bay-area-private-school-k-application/wiki/language-immersion.md` (line 35)
- **Finding:** The comparison table in `language-immersion.md` includes a row for "EBGIS" with all fields set to `--`. EBGIS (East Bay German International School) is listed as a stub. A comparison table row for an entity with zero data provides no value and may mislead readers into thinking the entity is being tracked. No article exists for EBGIS.
- **Suggested fix:** Either remove the EBGIS row from the comparison table and note it as an unresearched stub in a footnote, or research EBGIS to fill the data. Per `_index.md`, EBGIS is acknowledged as a stub — the table row adds no value and should be removed.

### [W010] CV5: `index.md` lists four guide articles under staging with incorrect file paths
- **File:** `topics/bay-area-private-school-k-application/index.md` (lines 33-37)
- **Finding:** `index.md` lists the four new guides as staging articles under "Staging (pending wiki-critic review)" with paths `staging/financial-realities.md`, `staging/admissions-strategy-advanced.md`, `staging/parent-essay-guide.md`, `staging/school-tour-guide.md`. These files do not exist at those paths — they are graduated wiki articles at `wiki/guides/`. This makes `index.md` wrong about both the location and the status of these four articles. (Also noted in E008, which covers `_index.md`; this warning covers the separate `index.md` file.)
- **Suggested fix:** Update `index.md` to move the four articles to the "Guides" section with their correct paths (`wiki/guides/financial-realities.md`, etc.).

### [W011] C6: Empty or stub article — `wiki/language-immersion.md` EBGIS section
- **File:** `topics/bay-area-private-school-k-application/wiki/language-immersion.md`
- **Finding:** From the comparison table row, EBGIS (East Bay German International School) has a placeholder entry with no data. While the full article section for EBGIS was not read in full (it may contain a note only), the comparison table entry creates a misleading stub presence. Combined with W009, this represents a thin coverage situation.
- **Suggested fix:** Confirm that EBGIS is excluded from the comparison table until researched, per the stub note in `_index.md`. If there is a section heading for EBGIS with no body content, mark as `[INFO]` or remove.

---

## Info (improvement opportunities)

### [I001] CV1: Missing entity article — "Lycee Francais de San Francisco" mentioned in 3 articles but has no wiki article
- **Finding:** Lycee Francais de San Francisco is mentioned in `application-timeline.md` (line 168), `language-immersion.md` (comparison table, line 33), and `overview.md` (by implication through language immersion section). It has data in the comparison table (tuition ~$35,900-$45,900, rolling deadline, early March decisions, Veracross platform) but no entity article or stub. It is not listed as a stub in `_index.md`.
- **Suggestion:** Add Lycee Francais to the stubs section in `_index.md` and add it as a gap-fill question in `research-plan.yaml`.

### [I002] CV1: Missing entity article — "SF Waldorf School" and "Terra San Francisco" mentioned in `pedagogy-philosophy.md`
- **Finding:** `pedagogy-philosophy.md` line 39-40 lists "SF Waldorf School" under the Waldorf philosophy row and "Terra San Francisco" under Reggio Emilia-Inspired, both with no article and no stub listing in `_index.md`. Terra San Francisco (trilingual immersion) was explicitly noted in `research-plan.yaml` as a stub, but is not listed in `_index.md`'s Stubs section. SF Waldorf School is not tracked anywhere.
- **Suggestion:** Add both to the stubs section of `_index.md`. Add SF Waldorf School as a gap-fill research question.

### [I003] CV2: Gap-fill questions qE022-qE035 (added 2026-04-07 to research plan) have no wiki coverage yet
- **Finding:** `research-plan.yaml` lines 46-54 note that qE022-qE035 were added in a "Third pass 2026-04-07" with `status: pending`. These cover topics including cost transparency, financial aid admission impact, working parent logistics, playdate evaluation, rejection recovery, hidden costs, and waitlist strategy. Most of these are now covered by the four new `wiki/guides/` articles (financial-realities, admissions-strategy-advanced, parent-essay-guide, school-tour-guide). However, the research-plan still shows `gap_fill` status as `status: pending` (line 50) even though articles have been compiled. This inconsistency means the evolve-agent will incorrectly identify these questions as unanswered.
- **Suggestion:** The wiki-compiler-agent should update the status of qE022-qE035 questions to `answered` (or `partial`) in `research-plan.yaml` after the new guide articles pass wiki-critic review.

### [I004] CV3: No comparison table for key guide attributes across SF schools
- **Finding:** The `school-profiles-sf.md` comparison table (line 36-49) has many `--` entries for "K Class Size," "Tuition," and other fields. Specifically: Convent & Stuart Hall tuition, La Scuola tuition, Hamlin tuition, Live Oak tuition, Presidio Hill tuition, and SF Friends tuition are all `--`. While this accurately reflects the fact that these data points were not confirmed from verified sources, 6 of 11 SF schools (55%) have missing tuition data. For a guide whose primary purpose includes helping families budget, this is a meaningful coverage gap.
- **Suggestion:** Add a research task to gap-fill tuition data for the 6 SF schools currently showing `--` in the comparison table. This should be a targeted `/kb-ingest` or `Q` priority in the next gap-fill pass.

---

## Coverage Summary

- Articles checked: 18 (wiki) + 4 new wiki/guides articles = 22 total
- Entities with profiles: 14 (SF Day, CDS, Convent & Stuart Hall, Hamlin, Live Oak, Presidio Hill, SF Friends, CAIS, La Scuola, Town School, SF School, Harker, Challenger, Stratford, + 6 in peninsula/east bay article + 7 in south bay article)
- Questions answered with wiki coverage: breadth (12/12 complete), depth (27/27 complete), gap-fill (partial — qE022-qE035 have article coverage but not marked answered in research-plan)
- Comparison tables: 5 (school-profiles-sf, school-profiles-peninsula-east-bay, south-bay-schools, pedagogy-philosophy, language-immersion)
- Cycle_bound articles past close date: 1 (`application-timeline.md`)

## Recommended Next Actions

1. **Fix broken wikilinks in 7 articles (E001-E004):** Replace all bare `[[financial-realities]]`, `[[admissions-strategy-advanced]]`, `[[parent-essay-guide]]`, and `[[school-tour-guide]]` links with their `guides/`-prefixed equivalents. This unblocks the four new guide articles from being reachable by any wiki navigation path. Affects: `financial-aid.md`, `guides/public-vs-private.md`, `guides/admissions-strategy-advanced.md`, `guides/parent-essay-guide.md`, `guides/school-tour-guide.md`.

2. **Update `_index.md` and `index.md` to reflect graduated guide articles (E008 + W010):** Move all four `wiki/guides/` articles from the "Staging" section to the "Guides" section in both files. Update their wikilink slugs to the `guides/` prefix form. This is a single-pass wiki-compiler-agent fix.

3. **Correct the Harker K tuition contradiction in `financial-realities.md` (E006 + W006):** Replace "Harker K $47,400" with "Harker K-5 $51,550 (2026-27)" per verified claim C182. Also remove or source "Nueva Upper School $66,960" per W007, replacing with the verified C126 range ($30,555-$51,285).
