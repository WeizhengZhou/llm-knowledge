# Changelog

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
