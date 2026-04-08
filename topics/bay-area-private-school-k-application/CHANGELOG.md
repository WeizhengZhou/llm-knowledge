# Changelog

## 2026-04-06 -- wiki-compiler-agent -- Wiki-Critic Revision Pass (parent-essay-guide, school-tour-guide)

**Changed:**
- `staging/parent-essay-guide.md` -- Added epistemic note block for "committees look for challenges" claim (D4 fix). Added "Choosing What to Write" decision framework with if/then structure for essay theme selection (D2 fix). Removed thank-you note section, replaced with cross-reference to school-tour-guide (D5 fix). Replaced two common mistakes (wrong school name, procrastination) with non-obvious alternatives (writing about philosophy in abstract, treating essays as template variants). Strengthened character-count practical implication.
- `staging/school-tour-guide.md` -- Added epistemic note block for thank-you note recommendation (D4 fix). Removed working-parent strategy content, replaced with one-line cross-reference to admissions-strategy-advanced (D5 fix). Added "Using Your Tour Notes to Decide" synthesis framework: forced ranking on priorities, dealbreaker vs yellow flag distinction, pattern recognition across visits, feeding observations into essays (D2 fix). Removed "Questions You Should Not Ask" section (out of scope per critic).

**Reason:** Wiki-critic revision pass. parent-essay-guide scored 6/10 (NEEDS-REVISION), school-tour-guide scored 5/10 (NEEDS-REVISION). All required fixes from critic reports implemented. Articles remain in staging for re-review.

## 2026-04-06 -- wiki-compiler-agent -- Compile Run 4 (C330-C408 Experiential/Decision Guides)

**Added:**
- `staging/financial-realities.md` -- True K-12 cost model, hidden costs (annual fund, fees, capital campaigns), need-blind vs. need-aware distinction (only Nueva confirmed L1), Nueva income brackets, Bay Area COL adjustment, private-as-bridge strategy. Serves RO4. (C330-C339, C344, C347-C358, C395, C402, C408, d006, mof012, mof014, mof015)
- `staging/admissions-strategy-advanced.md` -- Application volume (reach/match/safety), working parent logistics (20-35 events), event attendance impact (Head-Royce only corroboration), waitlist concrete actions (LOCI, ranked vs pooled, March 19-26 window), rejection recovery (enrollment management framing, reapplication paths). Serves RO2. (C340-C346, C365-C380, C397-C401, C403)
- `staging/parent-essay-guide.md` -- What schools evaluate (mission fit, honest child portrait), authenticity vs polish, disclosing challenges (recommended), learning differences disclosure, format (500-1500 characters), common mistakes. Serves RO2. (C387-C394)
- `staging/school-tour-guide.md` -- Open house components, beyond-the-brochure observations, 5 question categories (admissions, faculty, parents, K-specific, beyond brochure), K-specific observations for 4-5 year olds. Serves RO1. (C381-C386)

**Changed:**
- `wiki/guides/public-vs-private.md` -- Added explicit decision framework section (when private K makes clear sense vs. when SFUSD is better), private-as-bridge strategy, learning differences IEP/504 note, financial-realities wikilink. Addresses wiki-critic D2 flag (decision framing weak). (C325, C330, C370, C395, C401)
- `wiki/financial-aid.md` -- Added "Does applying for aid hurt my chances?" section using C351 (Nueva need-blind L1), C352 (budget constraint nuance), C354 (BPN claim NOT generalized per mof015), C269 (Almaden need-blind), C395 (no income ceiling). financial-realities wikilink added.
- `wiki/_index.md` -- Added 4 staging articles to index under new Staging section.

**Reason:** Compile run 4 -- gap-fill round 3 data (C330-C408). Focus on experiential/decision-making guides for real parent questions (RO1, RO2, RO4). All L4 claims properly attributed with epistemic notes. Mechanism overreach flags honored: mof012, mof014, mof015, mof016, mof017, mof018, mof019.

## 2026-04-06 -- fact-checker-agent -- Fact-Check Pass 4 (Depth Research: C330-C408)

### Summary
79 new claims verified (C330-C408) from 9 source files dated 2026-04-07. Topics: financial costs, working parent logistics, financial aid income thresholds, playdate evaluation, rejection recovery, waitlist strategy, open house guidance, parent essay authenticity.

### must_verify Claims (8 claims)
- C330: Total K-12 cost $520K -- DOWNGRADED to L3. Live fetch of redwoodgrovewm.com did NOT return $520K figure. This is a modeled calculation, not a surveyed statistic. Dispute d006 created (C330 $520K vs C325 $500K-$700K).
- C331: Tuition escalation 4-6% annually -- CONFIRMED L2. Duplicate of C170 (same source). Dispute d005 records the duplicate.
- C347: Nueva <$150K = 100% aid -- CONFIRMED L1. Live fetch of nuevaschool.org confirmed.
- C348: Nueva $150K-$250K = 1-10% contribution -- CONFIRMED L1. Live fetch confirmed.
- C349: Nueva 58% of aided families earn >$250K -- CONFIRMED L1. Live fetch confirmed.
- C350: Nueva grants not loans, covers beyond tuition -- CONFIRMED L1. Live fetch confirmed.
- C351: Nueva need-blind admissions -- CONFIRMED L1. Live fetch confirmed.
- C353: Nueva $8.6M aid, 20% of students (195) -- CONFIRMED L1. Live fetch confirmed + L3 corroboration.
- C373: ISSFBA waitlist movement March 19-26 -- CONFIRMED L1. Live fetch of issfba.org confirmed dates.

### Overreach Resolutions (17 claims)
- C330: $520K total cost -- downgraded to L3, labeled as modeled projection
- C332: $22K-$23K average -- qualified as blending religious and independent schools
- C333: SF/Marin averages -- noted as from search synthesis, not confirmed on live page
- C337: "Most schools" seek 100% fund participation -- changed to "Bay Area independent schools"
- C339: 88% receiving aid -- attributed to PrivateSchoolReview (L3), unnamed schools
- C340: 20-35 events -- attributed to single L4 consultant, qualified as estimate
- C341: "Most schools don't track attendance" -- qualified with only Head-Royce named
- C354: "Many schools use blind admissions" -- CRITICAL: L4 claim embedded in L1 source. Downgraded. Only Nueva confirmed need-blind from L1.
- C356: Income brackets for aid -- downgraded to L4. Author extrapolation from Nueva data.
- C359: "Looking for egregious signs" -- qualified as consultant synthesis, excluded gifted programs
- C360: Playdate assessment criteria -- added "may vary by school"
- C361: Red flag list -- attributed to consultant synthesis
- C363: "Schools can detect coached children" -- downgraded to L4 (unverifiable assertion)
- C366: Rejection = enrollment management -- framed as community observation
- C368: "Many families admitted second year" -- changed to "some families report"
- C371-C372: Waitlist acceptance rates 5-15% / 15-30% -- DOWNGRADED to L4. No Bay Area-specific data. No school publishes waitlist rates.
- C377: Waitlist composition criteria -- added "may prioritize," noted no school discloses

### New Disputes
- d005: C331 vs C170 -- duplicate extraction (same source, same figure). Resolved: no conflict.
- d006: C330 ($520K) vs C325 ($500K-$700K) -- different modeling assumptions. Both are projections.

### New Mechanism Overreach Flags
- mof014: Calculation presented as surveyed figure (C330)
- mof015: L4 claim embedded in L1 source (C354, C408)
- mof016: Consultant playdate criteria universalized (C359-C363, C405, C406)
- mof017: Waitlist rates without Bay Area data (C371, C372)
- mof018: Individual school data extrapolated to market (C356)
- mof019: Community rejection reasons presented as fact (C366, C367, C377)

### Gate Status: CLEAR (no L5 claims)

### Key Findings
1. **Nueva financial aid data is the gold standard** -- only Bay Area school publishing specific income thresholds. All other income-bracket claims are extrapolations.
2. **Playdate evaluation claims are consultant consensus, not school policy** -- LA-based sources generalized to Bay Area. Must always include "may vary by school."
3. **Waitlist acceptance rates have zero Bay Area data** -- national estimates only. Must be clearly flagged.
4. **The $520K figure is missing from the live page** -- may have been removed or was only in the search snippet. Treat as unconfirmed.

### Files
- `fact-sheet-c330-c408.yaml` -- All new verified claims, disputes, mechanism flags
- `integrate-factsheet-batch3.sh` -- Integration script to append to main fact-sheet

## 2026-04-06 -- wiki-compiler-agent -- Compile Run 3 (Gap-Fill Pass 2 Data)

**Changed:**
- `wiki/south-bay-schools.md` -- Expanded Helios, Gideon Hausner, Almaden Country Day, BASIS SV from stubs to full profiles with admissions, tuition, and financial aid data (C233-C282). Updated comparison table. Corrected "No ISSFBA coordination" generalization per mof013 (Helios, Almaden, Hausner DO follow March 19).
- `wiki/language-immersion.md` -- Added La Scuola tuition ($48,850 SF, $39,775 SV), Lycee Francais full profile (CP age quirk: requires age 6 by Sep 1), SVIS full profile (ISSFBA confirmed Mar 19, tuition $42,630). Added comparison table. Removed Lycee/SVIS/EBGIS from stub list (C283-C301).
- `wiki/application-timeline.md` -- CORRECTED Keys School decision date from Feb 19 to Mar 20 (C118 correction). Added Helios, Hausner, Almaden, BASIS SV, SVIS, Nueva to deadline and decision tables. Added second-round/late deadlines section (Hausner Round 2, Nueva Pre-K Round II, BASIS rolling, Lycee rolling). Added financial aid deadlines for Helios, SVIS, Hausner, La Scuola, Almaden.
- `wiki/_index.md` -- Updated descriptions for south-bay-schools, language-immersion. Added staging articles. Reduced stubs list (Helios, BASIS, Hausner, Lycee, SVIS promoted to full articles).

**Added:**
- `staging/assessment-prep.md` -- Concept article: IQ testing logistics (WPPSI-IV/WISC-V format, 45-60 min, no coaching), which schools require it (Nueva, Helios, Harker), IQ providers ($850-$950), FSIQ ~130 target at Nueva, playdate observation criteria, parent interview preparation (C302-C324)
- `staging/public-vs-private.md` -- Guide article: $500K decision framing (modeled estimate), parochial vs independent price spread ($6K-$10K vs $25K-$52K), SFUSD lottery as hedge driver, Basic Fund for low-income families (C325-C329)

**Changed (additional corrections):**
- `wiki/school-profiles-peninsula-east-bay.md` -- Corrected Keys School decision date from Feb 19 to Mar 20 (C118). Added Keys School admissions process details from Cardinal Education (C309-C314).
- `wiki/issfba-bada.md` -- Corrected Keys School Feb 19 reference. Added BASIS SV (Mar 18, non-ISSFBA) and Nueva (Mar 20, non-ISSFBA) to exceptions list.

**Reason:** Compile run 3 -- gap-fill pass 2 research data (C233-C329). Resolved 6 stubs (Helios, Gideon Hausner, Almaden Country Day, BASIS SV, Lycee Francais, SVIS). Corrected Keys School February 19 error (C118). Honored mof009-mof013.

## 2026-04-06 -- Fact-Check Pass 3 (Gap-Fill Pass 2: C233-C329)

### Corrections
- `fact-sheet.yaml` C118 (Keys School) -- CORRECTED: "February 19" decision date was a data extraction error. Live verification confirmed no admissions dates on keysschool.org/admission/tuition-fees/. Cardinal Education (L3) reports March 20 for 2024-25 cycle. Verdict: corrected/L3.
- `fact-sheet.yaml` mof004 -- Removed erroneous "Keys School (February 19)" reference; added Nueva (March 20) and BASIS SV (March 18).

### New Verified Claims (97 claims: C233-C329)
- Helios School: 18 claims (8 must_verify, all confirmed L1-L2; live verified)
- Gideon Hausner Jewish Day School: 13 claims (7 must_verify; decision date confirmed March 19 via live fetch)
- Almaden Country Day School: 11 claims (5 must_verify; live verified)
- BASIS Independent Silicon Valley: 8 claims (5 must_verify; live verified)
- La Scuola International School: 4 tuition updates (must_verify; L2)
- Lycee Francais de San Francisco: 8 claims (4 must_verify; L2)
- Silicon Valley International School: 7 claims (3 must_verify; L1-L2)
- Nueva School supplemental: 7 claims (must_verify; L1 with live verification)
- Keys School: 6 claims (L3 aggregator data from Cardinal Education)
- IQ Testing Logistics: 6 claims (L1-L3 mixed)
- K Application Process General: 4 claims (L2-L3)
- SF Private School Market: 5 claims (L3-L4; overreach resolved)

### New Dispute
- d004: BASIS Independent SV acceptance rate (C205 vs C282) -- L3 aggregator 56% vs official site publishing no rate

### New Mechanism Overreach Flags
- mof009: aggregator playdate criteria universalized (C323)
- mof010: partial-fetch source treated as authoritative (C325, C326, C327, C329)
- mof011: ISSFBA membership inference from decision date (C237, C268, C279, C302, C310)
- mof012: aggregate cost estimate presented as fact (C325)
- mof013: South Bay ISSFBA participation pattern more nuanced than prior assumption

### Overreach Resolutions (6 claims)
- C282/C205: BASIS acceptance rate -- dispute record created (d004)
- C310: Keys School ISSFBA membership -- added qualifier "may indicate"
- C323: Playdate criteria -- added "may vary by school" qualifier
- C325: $500K lifetime cost -- clarified as modeled estimate
- C327: Public school district quality -- downgraded to L4 (no data cited)
- C329: SFUSD lottery driving private applications -- accepted at L3

### Gate Status: CLEAR (no L5 claims)

### Files
- `fact-sheet-gap-fill-2.yaml` -- All new verified claims, disputes, mechanism flags
- `_apply_factsheet_edits.py` -- Script to integrate corrections into main fact-sheet

## 2026-04-06 -- Compile Run 2 (South Bay, Philosophy, TK, Overview)

### New Articles (7)
- `wiki/overview.md` (overview) -- Comprehensive parent guide entry point
- `wiki/harker-school.md` (entity) -- Harker School profile (San Jose, TK-12)
- `wiki/challenger-school.md` (entity) -- Challenger School profile (10 CA campuses)
- `wiki/stratford-school.md` (entity) -- Stratford School profile (15+ Bay Area campuses)
- `wiki/pedagogy-philosophy.md` (guide) -- Educational philosophy comparison guide
- `wiki/transitional-kindergarten.md` (concept) -- TK overview: public vs. private, strategic considerations
- `wiki/south-bay-schools.md` (guide) -- South Bay regional guide with comparison table

### Updated Articles (4)
- `wiki/school-profiles-peninsula-east-bay.md` -- Added Harker to comparison table; noted Challenger/Stratford rolling admissions
- `wiki/assessment-playdate.md` -- Added Harker cognitive assessment details; Challenger placement test info
- `wiki/admissions-strategy.md` -- Added South Bay vs. SF strategy section; age cutoff for Nov 30; rolling admissions
- `wiki/_index.md` -- Added all new articles; updated article count

### Sources
- Fact-sheet claims used: C155-C232 (Batch 2 verified claims)
- Disputes referenced: d003 (Harker tuition)
- Mechanism overreach flags honored: mof005, mof006, mof007

## 2026-04-06 -- Compile Run 1 (Initial)

- 8 articles created (see log.md for details)
