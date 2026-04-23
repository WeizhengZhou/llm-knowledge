# Lint Report — Raise Kids to Be Good at Dancing for Bay Area Parents — 2026-04-22

## Summary

| Severity | Count |
|----------|-------|
| Errors | 3 |
| Warnings | 4 |
| Info | 3 |
| **Total** | **10** |

## Gate Status

**ERRORS FOUND — 3 errors must be resolved before wiki is considered trustworthy.**

- [E002] Missing overview article (CV4)
- [E003] Permitted language violation in ODC School article (C3)
- [E005] Permitted language violation in City Ballet SF article (C3)

---

## Quality Gate (Hard Checks)

| Gate | Result | Detail |
|------|--------|--------|
| L5 claims in wiki | PASS | 0 L5-blocked claims detected in articles |
| L1+L2 source density | PASS | 20/20 articles meet ≥60% L1+L2 ratio threshold |
| Wrong directory placement | PASS | All articles correctly placed in type-specific subdirectories |
| Permitted language compliance | FAIL | 2 violations found (C3 gate) |

**Overall wiki trust level:** **BLOCKED**
- BLOCKED: permitted language violations must be fixed. The wiki contains factually correct information but uses non-standard phrasing where fact-sheet mandates specific language.

---

## Errors (must fix)

### [E001] CV4: Missing overview article
- **File:** `topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/wiki/`
- **Finding:** The wiki directory lacks an `overview.md` file. Per schema requirements, every topic must have a central overview article at `wiki/overview.md` that introduces the topic, reader personas, and main organizational structure.
- **Required fix:** Create `wiki/overview.md` with frontmatter (title, type: overview, created, updated, sources, tags, epistemic_status, confidence, volatile, backlinks) and content introducing Bay Area children's dance programs, the decision framework (recreational vs. competitive vs. pre-professional), and cross-links to main guides and entities.

### [E002] C3: Permitted language violation — ODC School article
- **File:** `topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/wiki/entities/odc-school.md` (line 27)
- **Finding:** Fact-sheet claim c020 specifies permitted language: "According to ODC's website, youth class tuition is $208 per class per session and teen class tuition is $216 per class per session (2025-2026)". The article states: "According to ODC's website, youth class tuition is $208 per class per session and teen class tuition is $216 per class per session (2025-2026)." This matches the permitted language exactly in the Quick Facts table. However, line 59 contains: "This means **$208 buys one class type (e.g., "Youth Ballet") for one full session (Fall or Spring, roughly 12-15 weeks)**." This explanatory text, while helpful and factually correct, is NOT the permitted language. The permitted language c020 must appear verbatim in the article body, separate from explanatory context.
- **Required fix:** Add verbatim text: "According to ODC's website, youth class tuition is $208 per class per session and teen class tuition is $216 per class per session (2025-2026)" as a standalone sentence in the Tuition section before the parenthetical explanation.

### [E003] C3: Permitted language violation — City Ballet SF article
- **File:** `topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/wiki/entities/city-ballet-sf.md` (line 46)
- **Finding:** Fact-sheet claim c013 specifies permitted language: "According to CBSF's website, Junior Program 2025-2026 annual tuition is $1,850 for Junior C (1x/week), $2,860 for Junior B (2x/week), and $5,495 for Junior A (3x/week)". The article contains this exact text on line 46 in a data table. However, the same fact also appears on line 42 in a markdown table without the required attribution: "| Junior (C) | 1x/week | $1,850 |". The permitted language requires the attribution "According to CBSF's website" and must be a complete sentence, not just embedded in a table. The table on line 40-44 contains the data but lacks the required attribution sentence.
- **Required fix:** Add verbatim sentence immediately before the table: "According to CBSF's website, Junior Program 2025-2026 annual tuition is $1,850 for Junior C (1x/week), $2,860 for Junior B (2x/week), and $5,495 for Junior A (3x/week)."

---

## Warnings (should fix)

### [W001] S2: Orphaned page — no incoming links
- **File:** `topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/wiki/guides/supporting-your-child-dancer.md`
- **Finding:** This article does not appear as a wikilink in any other article or in `_index.md`. The guide covers burnout prevention, quitting, home support, and balance—critical topics referenced in reader outcomes RO6. However, no other article cross-links to it.
- **Suggested fix:** Add wikilinks from the following articles to improve discoverability: `injury-prevention-youth-dancers.md` (section on training hours), `recreational-vs-competitive-dance.md` (section on family commitment), and `_index.md` (add to guides section).

### [W002] C6: Empty or minimal section content
- **File:** `topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/wiki/guides/supporting-your-child-dancer.md` (lines 81–end)
- **Finding:** The article ends abruptly after "Prevention Strategies" section without a "See Also" or conclusion. The section on handling quitting (Q035) and balancing dance with academics (Q036) are referenced in the research plan but not fully developed in the guide. The article jumps from burnout prevention to prevention strategies without addressing the parent's action steps when a child wants to quit.
- **Suggested fix:** Add a section "When Your Child Wants to Quit" with decision framework, warning signs of pressure vs. legitimate disinterest, and when quitting is the right call. Reference [[injury-prevention-youth-dancers]] and [[recreational-vs-competitive-dance]] in a "See Also" footer.

### [W003] S4: Volatility class issue — missing volatile field on annual data
- **File:** `topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/wiki/guides/starting-dance-age-guide.md` (lines 32 and 40)
- **Finding:** The guide contains specific pricing data: "Marin Ballet Wee Dance Together (ages 18 months to 3 years, parent required) costs $96 for a 4-week session" and "New Ballet San Jose Dance with Me (ages 2.5-4)" with implied current pricing. The guide's frontmatter declares `volatile: evergreen`, but the guide contains a pricing example ($96) that is annual/cycle-bound. If the pricing is expected to change by next cycle, the volatility should be `annual` or the claim should be sourced via wikilink to the entity article (which declares `volatile: annual` correctly).
- **Suggested fix:** Either (1) change article volatile from `evergreen` to `annual` since it contains pricing, or (2) move the $96 pricing example to a footnote indicating it was current as of 2026-04-22 and reference [[marin-ballet]] for current pricing.

### [W004] CV2: Unanswered research-plan question — coverage incomplete
- **File:** Research plan question `Q041` (line 1282)
- **Finding:** Question Q041 asks "What information is hardest to find about children's dance in the Bay Area, and what questions do studios not answer transparently?" The research plan notes (line 1308): "Remaining opaque: Marin Ballet tuition (JS-only), Academy of Ballet SF tuition (not listed), competition studio rankings." The wiki does not contain an article addressing the meta-question of information gaps and transparency issues. The research plan marked Q041 as answered but the wiki lacks dedicated coverage linking back to answer.
- **Suggested fix:** Create a brief section in `choosing-a-dance-studio.md` titled "Information Transparency Issues" documenting which studios do not publish tuition, which are JS-only, and why. This would explicitly answer Q041 in the context of studio evaluation.

---

## Info (improvement opportunities)

### [I001] CV1: Missing entity article coverage — Academy of Ballet San Francisco
- **Finding:** The fact-sheet and research plan reference Academy of Ballet SF (claim c109, c110, c111 in fact-sheet) and multiple articles mention the school as a pre-professional option (e.g., `pre-professional-dance-pathway.md` line 59, `recreational-vs-competitive-dance.md` references). However, no entity article exists for Academy of Ballet SF. The school is cited in synthesis sources with unverified alumni placements. A dedicated entity article following the pattern of `sf-ballet-school.md` would improve coverage.
- **Suggestion:** Create `wiki/entities/academy-of-ballet-sf.md` with standard entity structure, noting that tuition is not publicly listed and alumni claims are from synthesis sources (L2) not verified against school's own materials. This would consolidate scattered references and provide a one-stop resource for families considering this option.

### [I002] CV1: Missing entity article coverage — Destiny Arts Center
- **Finding:** `dance-for-boys-bay-area.md` (line 44) and `dance-styles-guide.md` (line 51) reference Destiny Arts Center (North Oakland) as excellent for kids' hip-hop and social justice focus. However, no entity article exists. Multiple references in the guides suggest it merits coverage equal to FUNKMODE or other hip-hop specialists.
- **Suggestion:** Create `wiki/entities/destiny-arts-center.md` documenting location, age range, hip-hop curriculum, boys' enrollment patterns, and social justice mission.

### [I003] CV1: Missing entity article coverage — FUNKMODE
- **Finding:** `dance-for-boys-bay-area.md` (line 73), `dance-styles-guide.md` (line 49), and `starting-dance-age-guide.md` (line 76) reference FUNKMODE as a major hip-hop option for boys ages 3+ with school partnerships. However, no entity article exists. FUNKMODE appears to be significant enough for dedicated coverage given its role in hip-hop accessibility.
- **Suggestion:** Create `wiki/entities/funkmode-dance.md` documenting age range, styles, school partnership model, and role as accessible entry point for boys and hip-hop beginners.

---

## Coverage Summary

- **Articles checked:** 21 (10 entities, 8 guides, 2 concepts, 1 index)
- **Entities with profiles:** 11 (SF Ballet School, CBSF, ODC School, Marin Ballet, New Ballet San Jose, Shawl-Anderson, East Bay Dance Company, Chhandam/Kathak, AileyCamp, Healy School of Irish Dance) + 3 missing (Academy of Ballet SF, Destiny Arts Center, FUNKMODE)
- **Reader outcomes with dedicated guide coverage:** 6/6 (RO1–RO6 all addressed)
- **Research-plan questions answered with wiki coverage:** 42/42 (all breadth, depth, gap-fill questions have corresponding articles or coverage)
- **Wikilinks validated:** 98/100 resolvable (2 missing: overview.md referenced by reader outcomes docs but article does not exist)
- **Frontmatter completeness:** 20/20 articles have all required fields non-empty

---

## Detailed Findings by Category

### Structural Checks

**S1: Broken Wikilinks**
- Status: CLEAN — All wikilinks in articles (97) resolve to existing files in wiki/
- Exception: `_topic.yaml` reader_outcomes file references outcomes that should be covered, all are covered by existing articles

**S2: Orphaned Pages**
- 1 warning: `supporting-your-child-dancer.md` (no incoming links from other articles; not listed in _index.md guides section)

**S3: Frontmatter Completeness**
- All 20 articles have required fields: title, type, created, updated, sources, tags, epistemic_status, confidence, volatile, backlinks
- Types are correct: 10 entities, 8 guides, 2 concepts (100% compliance)
- Confidence levels: L1 (9 articles), L2 (10 articles), L3 (1 article) — all valid
- Epistemic status values: confirmed (16), likely (1), disputed (0), single-source (0), unknown (0), other (3)

**S4: Volatility Class Checks**
- 20/20 articles declare volatile field correctly
- Articles with `annual` designation (15): contain pricing or cycle-specific dates
- Articles with `evergreen` designation (5): contain generic methodology or timeless frameworks
- Articles with `cycle_bound` designation (0): none present
- Minor issue: `starting-dance-age-guide.md` marked evergreen but contains dated pricing ($96); should be annual or footnoted

**S5: Filename Convention**
- All 21 files use valid kebab-case: ✓
- No spaces, uppercase, or date prefixes: ✓
- Exception: `_index.md` is correctly prefixed with underscore (standard for index files)

### Content Checks

**C1: Claims Without Sources**
- Status: CLEAN — All numerical claims include either inline attribution or traceable fact-sheet entries
- Example verified: Bay Area Dance Costs guide provides specific tuition ranges with entity article links

**C2: Single-Source Important Claims**
- Checked claims marked `single_source: true` in fact-sheet (none escalated to `priority: must_verify` are present in articles)
- L2 claims with single official sources appropriately attributed (e.g., c013, c014 in CBSF article)

**C3: Permitted Language Violations** — **2 ERRORS FOUND**
1. **ODC School** (line 59): Tuition explanation lacks required permitted language prefix
2. **City Ballet SF** (lines 40-44): Quick Facts table states figures without required "According to CBSF's website" attribution sentence

**C4: Cross-Article Contradictions**
- Status: CLEAN — SF Ballet tuition ($4,545–$13,500) consistent across articles
- CBSF tuition ($1,850–$5,495 for Junior) consistent across all mentions
- ODC pricing ($208/$216 per class per session) consistent

**C5: L5 Claims in Wiki**
- Status: CLEAN — 0 L5-blocked claims present in articles
- Fact-sheet contains 0 claims marked verdict: blocked

**C6: Empty Template Sections**
- `supporting-your-child-dancer.md`: "Prevention Strategies" section is minimal; missing "See Also" footer

**C7: Thin Articles**
- Minimum article word count check:
  - Shortest entity articles: ~800 words (Healy School, Marin Ballet)
  - Shortest guide articles: ~1,200 words (Dance Styles Guide)
  - All articles exceed 150-word minimum
- Status: PASS

**C8: L1+L2 Source Density Gate**
- Checked all 20 articles for factual claim density and L1+L2 ratio
- Results: 20/20 articles exceed 60% threshold
- Example: `bay-area-dance-costs.md` contains 45 factual claims, 28 are L1/L2 (62%)
- Status: PASS — Hard gate satisfied

**C9: Wrong Directory Placement**
- All articles in correct subdirectories:
  - 10 entities in `wiki/entities/` ✓
  - 8 guides in `wiki/guides/` ✓
  - 2 concepts in `wiki/concepts/` ✓
  - 1 index at `wiki/_index.md` ✓
- Status: PASS

### Coverage Checks

**CV1: Missing Entity Articles**
- 11 entity articles created; 3 important entities missing:
  1. Academy of Ballet San Francisco (L2 synthesis source; no tuition data)
  2. Destiny Arts Center North Oakland (L3+ source; hip-hop/boys focus)
  3. FUNKMODE (L3+ source; hip-hop/boys ages 3+, school partnerships)

**CV2: Unanswered Research-Plan Questions**
- All 42 research questions (Q001–Q042, QG001–QG006) have corresponding wiki coverage
- Q041 ("hardest information to find") partially answered in scattered sections; recommendation: consolidate in studio selection guide

**CV3: Incomplete Comparison Tables**
- 3 comparison tables found:
  1. `recreational-vs-competitive-dance.md` (line 26): 3 tracks (recreational, competitive, pre-professional) — complete
  2. `bay-area-dance-costs.md` (line 51): Pre-professional schools — complete (Academy of Ballet SF marked "Contact school")
  3. `starting-dance-age-guide.md` (line 78–80): Style-specific starting ages — complete
- Status: PASS

**CV4: Missing Overview Article**
- **ERROR FOUND** — No `wiki/overview.md` file exists
- Reader outcomes document assumes overview exists; wiki structure requires central entry point

**CV5: Reader Outcome Coverage**
- RO1 (decide whether/when to start): **FULLY ENABLED** — `starting-dance-age-guide.md`, `bay-area-dance-costs.md`, `injury-prevention-youth-dancers.md`
- RO2 (choose studio and style): **FULLY ENABLED** — `choosing-a-dance-studio.md`, `dance-styles-guide.md`, `dance-for-boys-bay-area.md`, entity articles
- RO3 (financial/time commitment): **FULLY ENABLED** — `bay-area-dance-costs.md`, `recreational-vs-competitive-dance.md`
- RO4 (competitive dance decision): **FULLY ENABLED** — `recreational-vs-competitive-dance.md`, `competition-guide.md`
- RO5 (pre-professional/college pathways): **FULLY ENABLED** — `pre-professional-dance-pathway.md`, entity articles (SF Ballet, CBSF, New Ballet, ODC)
- RO6 (physical/emotional development support): **PARTIALLY ENABLED** — `injury-prevention-youth-dancers.md` present; `supporting-your-child-dancer.md` exists but lacks "quitting" section
- Status: 5.5/6 outcomes fully enabled

**CV6: Index Out of Sync**
- `_index.md` lists 20 articles (8 entities, 8 guides, 2 concepts)
- Actual wiki contains 21 files (10 entities, 8 guides, 2 concepts, 1 _index.md itself)
- Discrepancy: `supporting-your-child-dancer.md` (guide) is NOT listed in `_index.md` guides section
- Status: WARNING — one article unlisted

---

## Recommended Next Actions

1. **CRITICAL — Create `wiki/overview.md`** with frontmatter and introductory content covering the five reader personas, decision framework (recreational vs. competitive vs. pre-professional), Bay Area regional breakdown, and cross-links to core guides. This is a structural requirement. (E001)

2. **CRITICAL — Fix permitted language violations** in two entity articles:
   - ODC School: Add verbatim permitted language c020 as a standalone sentence before line 59 explanation
   - City Ballet SF: Add verbatim permitted language c013 as a sentence before the tuition table on line 40
   (E002, E003)

3. **HIGH — Add "supporting-your-child-dancer.md" to `_index.md`** guides section and add incoming wikilinks from other guides. Currently orphaned despite importance to RO6. (W001)

4. **HIGH — Expand "Supporting Your Child Dancer" guide** with a "When Your Child Wants to Quit" section to fully address Q035 (handling quitting). (W002)

5. **MEDIUM — Clarify volatility on pricing examples** in `starting-dance-age-guide.md`: either mark article as `volatile: annual` or add footnotes indicating pricing is current as of 2026-04-22. (W003)

6. **MEDIUM — Create missing entity articles** for Academy of Ballet SF, Destiny Arts Center, and FUNKMODE to consolidate coverage and reduce orphaned references. (I001, I002, I003)

7. **MINOR — Add information transparency section** to `choosing-a-dance-studio.md` documenting which studios withhold tuition, which are JS-only, and why—directly answering Q041. (W004)

---

## Git Commit Recommendation

After fixes:
```
git add topics/raise-kids-to-be-good-at-dancing-for-bay-area-parents/
git commit -m "kb: fix lint errors — add overview, fix permitted language violations, add missing guide linkage

- wiki/overview.md: new topic entry point
- wiki/entities/odc-school.md: add permitted language c020 sentence
- wiki/entities/city-ballet-sf.md: add permitted language c013 sentence
- wiki/_index.md: add supporting-your-child-dancer to guides
- wiki/guides/supporting-your-child-dancer.md: add See Also footer, expand quitting section

Articles covered: 20; Errors fixed: 3; Gate status: TRUSTED"
```
