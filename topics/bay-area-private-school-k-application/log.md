# Operation Log

## [2026-04-06] wiki-compiler-agent | Wiki-critic revision pass

2026-04-06T23:30:00Z | wiki-compiler-agent | Revised 2 staging articles per wiki-critic feedback.
  Articles revised: staging/parent-essay-guide.md (6/10 -> re-review), staging/school-tour-guide.md (5/10 -> re-review).
  Fixes applied: 3 per article (D2 decision framework, D4 epistemic notes, D5 scope discipline).
  parent-essay-guide: added essay theme decision framework, epistemic note for challenge-disclosure claim, removed thank-you section.
  school-tour-guide: added tour-to-decision synthesis framework, epistemic note for thank-you claim, removed working-parent content.
  No new claims added. All permitted language verified against fact-sheet.
  Next recommended: wiki-critic-agent re-review of both articles.

## [2026-04-06] init | Topic initialized

- Topic: Bay Area private school K application
- Context: none

## [2026-04-06] wiki-compiler-agent | Compiled 8 articles from 39 raw sources

2026-04-06T16:30:00Z | wiki-compiler-agent | Compiled 8 articles from 39 raw sources.
  Gate status: CLEAR. L5 claims: 0. Disputed claims: 2 (d001, d002).
  Articles:
    - wiki/application-timeline.md (guide, L1)
    - wiki/school-profiles-sf.md (entity, L2)
    - wiki/school-profiles-peninsula-east-bay.md (entity, L2)
    - wiki/financial-aid.md (guide, L2)
    - wiki/assessment-playdate.md (guide, L2)
    - wiki/issfba-bada.md (entity, L2)
    - wiki/admissions-strategy.md (guide, L2)
    - wiki/language-immersion.md (concept, L2)
    - wiki/ravenna-hub.md (concept, L1)
    - wiki/_index.md (index)
  Verified claims used: 87 must_verify + 84 should_verify = 171 total
  Disputes documented in articles: d001 (SF Day Clarity deadline), d002 (Live Oak decision date)
  Mechanism overreach flags honored: mof001 (aggregator averages), mof002 (school-wide acceptance rates), mof003 (single-practitioner data), mof004 (coordinated date exceptions)
  Stubs identified: 8 schools/programs for future research
  Next recommended: lint-agent run to check structural integrity.

## [2026-04-06] evolve-agent | Evolution run complete

2026-04-06T00:00:00Z | evolve-agent | Evolution run complete.
  Gaps: 3 missing articles (wiki/overview.md, wiki/school-profiles-south-bay.md, wiki/pedagogy-philosophy.md), 4 thin articles. Q001c budget-blocked (South Bay research never executed against official sources).
  Freshness: 1 expired (application-timeline.md valid_until 2026-03-27, 10 days past — already in lint E001), 0 approaching, 2 articles with untagged volatile data.
  Patterns: 3 confirmed (progressive schools cluster Jan deadlines; indexed-tuition schools cluster Jan deadlines; ISSFBA membership predicts Mar 19 decision date), 2 hypothetical (IQ testing South Bay only; non-ISSFBA/non-Ravenna correlation).
  Concept backlink gaps: 4 missing articles (pedagogy-philosophy, transitional-kindergarten, feeder-preschools, accreditation-nais-cais).
  Merge candidate: 1 (language-immersion.md into school-profiles-immersion.md after stub research completes).
  New questions added: 19 (qE001-qE019). South Bay school profiles: qE001-qE010. Concept gaps: qE011-qE016. Pattern verification: qE017-qE019.
  gap_fill phase reopened (status: complete -> pending).
  Suggestions: output/evolution-suggestions.md
  Recommended next: research-agent gap-fill (prioritize qE001 Harker, qE003 Challenger, qE002 Helios, qE009 South Bay decision dates), then wiki-compiler-agent for school-profiles-south-bay.md and pedagogy-philosophy.md.

## [2026-04-06] wiki-compiler-agent | Compiled 7 new articles, updated 4 existing articles

2026-04-06T19:00:00Z | wiki-compiler-agent | Compile run 2: 7 new + 4 updated articles from 52 cumulative raw sources.
  Gate status: CLEAR. L5 claims: 0. Disputed claims: 3 (d001, d002, d003).
  New articles:
    - wiki/overview.md (overview, L2)
    - wiki/harker-school.md (entity, L2)
    - wiki/challenger-school.md (entity, L2)
    - wiki/stratford-school.md (entity, L2)
    - wiki/pedagogy-philosophy.md (guide, L2)
    - wiki/transitional-kindergarten.md (concept, L2)
    - wiki/south-bay-schools.md (guide, L2)
  Updated articles:
    - wiki/school-profiles-peninsula-east-bay.md (added Harker to comparison table, updated stubs)
    - wiki/assessment-playdate.md (added Harker cognitive details, Challenger/Stratford placement tests)
    - wiki/admissions-strategy.md (added South Bay vs. SF strategy section, expanded age cutoffs)
    - wiki/_index.md (added 7 new articles, updated count to 15)
  Verified claims used: C155-C232 (Batch 2), plus cross-references to Batch 1
  Disputes referenced: d003 (Harker tuition resolved -- live-verified 2026-27 rates)
  Mechanism overreach flags honored: mof005 (South Bay not ISSFBA), mof006 (philosophy-deadline confound), mof007 (TK priority unstated)
  Stubs remaining: 5 (Helios, BASIS SV, Gideon Hausner, Redwood Day, immersion schools)
  CHANGELOG.md created.
  Next recommended: lint-agent run to check structural integrity of all 15 articles.

## [2026-04-06] research-agent | Gap-fill phase second pass (evolve-agent priority list)

2026-04-06T18:00:00Z-19:00:00Z | research-agent | Gap-fill second pass: 11 new searches (s-052 through s-062), 14 new raw files saved.

### Searches Run (s-052 through s-062)

| Search ID | Question | Query |
|-----------|----------|-------|
| s-052 | qE002 (Helios) | Helios School Sunnyvale kindergarten admissions requirements tuition 2025 2026 gifted IQ |
| s-053 | qE004 (Gideon Hausner) | Gideon Hausner Jewish Day School Palo Alto kindergarten admissions tuition deadline 2025 2026 |
| s-054 | qE006 (Almaden Country) | Almaden Country School kindergarten admissions tuition San Jose 2025 2026 |
| s-055 | qE015 (La Scuola tuition) | La Scuola International School San Francisco tuition 2025 2026 Italian immersion kindergarten |
| s-056 | qE015 (Lycee Francais) | Lycee Francais San Francisco kindergarten admissions tuition immersion percentage 2025 2026 |
| s-057 | qE015 (SVIS) | Silicon Valley International School SVIS kindergarten admissions tuition French immersion 2025 2026 formerly ISTP |
| s-058 | qE007 (BASIS + Nueva dates) | BASIS Independent Silicon Valley kindergarten admissions deadline decision date assessment 2026-27 |
| s-059 | qE019 (Keys School) | Keys School Palo Alto kindergarten admissions process age cutoff application deadline 2025 2026 |
| s-060 | qE020 (IQ test logistics) | Nueva School Helios private school kindergarten IQ test psychologist Bay Area licensed providers cost how to schedule 2025 |
| s-061 | qE020 (parent interview prep) | Bay Area private school kindergarten parent interview questions what to expect preparation tips 2025 |
| s-062 | qE021 (public vs private) | private school kindergarten public vs private decision framework Bay Area considerations cost benefit factors 2025 |

### Raw Files Saved (14 new files)

| File | Tier | Question |
|------|------|----------|
| raw/web/official/2026-04-06_helios-admissions-steps.md | L1-official | qE002 |
| raw/web/official/2026-04-06_helios-assessments.md | L1-official | qE002 |
| raw/web/official/2026-04-06_helios-tuition-financial-aid.md | L1-official | qE002 |
| raw/web/official/2026-04-06_hausner-applying-to-kindergarten.md | L1-official | qE004 |
| raw/web/official/2026-04-06_hausner-tuition-fees.md | L1-official | qE004 |
| raw/web/official/2026-04-06_almaden-country-day-how-to-apply.md | L1-official | qE006 |
| raw/web/official/2026-04-06_almaden-country-day-tuition.md | L1-official | qE006 |
| raw/web/official/2026-04-06_basis-independent-sv-admissions.md | L1-official | qE007 |
| raw/web/official/2026-04-06_lascuola-tuition-affordability.md | L1-official | qE015 |
| raw/web/official/2026-04-06_lycee-francais-early-learning-apply.md | L1-official | qE015 |
| raw/web/official/2026-04-06_svis-admissions-process.md | L1-official | qE015 |
| raw/web/official/2026-04-06_nueva-faq-decision-dates.md | L1-official | qE007/qE009 |
| raw/web/official/2026-04-06_nueva-iq-assessment-requirements.md | L1-official | qE007 |
| raw/web/official/2026-04-06_keys-school-admissions-cardinal-guide.md | L3-aggregator | qE019 |
| raw/web/official/2026-04-06_assessment-prep-iq-testing-logistics.md | L3-aggregator | qE020 |
| raw/web/community/2026-04-06_parent-interview-assessment-prep-guide.md | L3-aggregator | qE020 |
| raw/web/news/2026-04-06_public-vs-private-bay-area-decision-framework.md | L2-authoritative | qE021 |

### Question Status Updates

| Question | Old Status | New Status | Key Findings |
|----------|-----------|-----------|--------------|
| qE002 (Helios) | partially_answered | answered | Tuition $46,360 (2026-27 K-5); deadline Jan 8 2026; decision Mar 19 (ISSFBA); WPPSI-IV required; no published FSIQ minimum (holistic review); Clarity FA |
| qE004 (Gideon Hausner) | partially_answered | answered | TK tuition $38,340; K-4 tuition $42,480; deadline Jan 29 2026; decision Mar 19 2026 (ISSFBA, not Feb 19 as previously noted — prior cycle data corrected); max FA 75%; non-Jewish families accepted |
| qE006 (Almaden Country) | skipped | answered | K-5 tuition $39,340 (2026-27); deadline Feb 1; decision Mar 19 (ISSFBA confirmed); need-blind; Clarity FA; K process: application + family conversation only (no shadow visit) |
| qE007 (BASIS SV) | partially_answered | answered | Submission deadline Jan 28 2026; completion Feb 13; notification Mar 18 (independent, one day before ISSFBA); $3,000 deposit; rolling admissions from Jan 29 |
| qE015 (immersion schools) | skipped | answered | La Scuola K-5 $48,850 (SF campus 2026-27); 30% sliding scale; Lycee CP (K) age cutoff 6 by Sept 1; Lycee $150 fee; Veracross (not Ravenna); SVIS K $42,630; SVIS Mar 19 decision (ISSFBA); SVIS Jan 13 deadline |
| qE019 (Keys/non-ISSFBA dates) | partially_answered | answered | Keys: Jan 9 deadline (prior cycle), Mar 20 decision (one day after ISSFBA — possibly not ISSFBA member); $44,600 K-4 tuition; campus playdate + parent conversation |
| qE009 (South Bay decision dates) | partially_answered | answered (extended) | Hausner Mar 19 (ISSFBA); Almaden Mar 19 (ISSFBA); SVIS Mar 19 (ISSFBA); BASIS Mar 18 (independent); Nueva Mar 20 (independent); Keys Mar 20 (independent); Harker Mar 20 (independent) |
| qE020 (assessment prep — new) | new | answered | IQ test providers: Shelley Sinclair LEP $950 (Los Altos); Dr. Ginny Estupinian $850 (Los Gatos); book Sept-Oct for Nov guarantee deadline; parent interview questions documented; child playdate prep documented |
| qE021 (public vs private — new) | new | answered | Total K-12 private cost $500K-$700K; SFUSD lottery uncertainty drives private applications; ISSFBA: complete financial analysis BEFORE applying; public schools more diverse; private schools smaller classes + more resources |

### Key Corrections from This Pass

- **Gideon Hausner decision date correction**: Prior data from s-022 showed February 19, 2026. Official Ravenna fetch (s-053) shows March 19, 2026 for first-round decisions. Prior cycle data was likely for 2024-25 cycle or a different grade level. The authoritative 2026-27 first-round decision date is March 19 (ISSFBA coordinated). The research-plan.yaml note on qE004 and qE019 should be updated to reflect this correction.

- **Gideon Hausner ISSFBA status**: School IS an ISSFBA member (March 19 decision date confirmed). Previously marked as "independent" based on erroneous Feb 19 data.

- **Helios ISSFBA status**: Helios IS using March 19 2026 decision date (ISSFBA coordinated). A South Bay school (Sunnyvale) aligned with ISSFBA timing. Noteworthy.

- **SVIS ISSFBA status confirmed**: March 19 decision date; January 13 deadline.

### New Questions Discovered

- **qE020** (Assessment prep / RO5 focus): IQ test logistics, parent interview questions, child playdate preparation. New question spawned from s-060 and s-061. Filed as answered.
- **qE021** (Public vs. private decision framework): New concept article question. Spawned from s-062. Filed as answered.

## [2026-04-06] wiki-compiler-agent | Compile run 3: 2 new staging + 4 updated wiki articles

2026-04-06T22:45:00Z | wiki-compiler-agent | Compile run 3: 2 new staging articles + 4 updated wiki articles from 66 cumulative raw sources.
  Gate status: CLEAR. L5 claims: 0. Disputed claims: 4 (d001, d002, d003, d004).
  New staging articles:
    - staging/assessment-prep.md (concept, L1) -- IQ testing logistics, providers, playdate criteria, parent interview prep
    - staging/public-vs-private.md (guide, L3) -- $500K decision framework, parochial vs independent, Basic Fund
  Updated articles:
    - wiki/south-bay-schools.md (guide, L2) -- Expanded Helios, Hausner, Almaden, BASIS SV from stubs to full profiles
    - wiki/language-immersion.md (concept, L2) -- Added La Scuola tuition, Lycee Francais, SVIS full profiles
    - wiki/application-timeline.md (guide, L1) -- Corrected Keys School Feb 19 -> Mar 20; added 7 new school deadlines; second-round section
    - wiki/_index.md (index) -- Updated descriptions, added staging articles, reduced stubs
  Verified claims used: C233-C329 (gap-fill pass 2), C118 correction
  Disputes referenced: d004 (BASIS SV acceptance rate)
  Mechanism overreach flags honored: mof009 (playdate criteria L3), mof010 (partial fetch L3), mof011 (ISSFBA inference), mof012 ($500K modeled), mof013 (South Bay ISSFBA nuanced)
  Corrections applied: Keys School decision date Feb 19 -> Mar 20 (C118); South Bay ISSFBA generalization removed (mof013)
  Stubs remaining: 3 (Redwood Day, Terra SF, EBGIS)
  CHANGELOG.md updated.
  Next recommended: wiki-critic-agent for staging/assessment-prep.md and staging/public-vs-private.md, then lint-agent.

### Chrome MCP Availability

Chrome MCP was not available during this session (connection refused at 127.0.0.1:9222). Berkeley Parents Network (403), Parents Press article (JS-rendered), and Basic Fund article (JS-rendered) could not be fetched. These gaps are noted in raw files. Data from these sources was captured via search result summaries.

### Budget Status Post-Run

- Searches used: 62 (12 over original 50-search budget; this is an extended authorized run)
- Fetches used: approximately 66 (14 new fetches + 52 prior)
- Gap-fill phase: substantively complete for high-priority questions
- Remaining skipped questions: qE010 (South Bay FA), qE014 (NAIS/CAIS detail), qE016 (Redwood Day detail), qE017-qE018 (pattern verification)

## [2026-04-07] research-agent | Gap-fill phase round 3 (landscape seed questions qE022-qE035)

2026-04-07T00:00:00Z | research-agent | Gap-fill round 3: 8 new searches (s-063 through s-070), 8 new raw files saved. 10 of 14 new questions answered. 4 questions remain pending (lower urgency).

### Searches Run (s-063 through s-070)

| Search ID | Questions | Query |
|-----------|-----------|-------|
| s-063 | qE022, qE029 | Bay Area private school total cost K-12 tuition escalation annual fund capital campaign true cost 2025 |
| s-064 | qE023, qE027 | Bay Area private school kindergarten need-blind need-aware financial aid admissions impact does applying for aid hurt chances 2025 |
| s-065 | qE024, qE029 | Bay Area private school kindergarten admissions working parents both work open houses tours scheduling tips 2025 |
| s-066 | qE025 | private school kindergarten playdate red flags what schools evaluate social emotional readiness child behavior 2025 |
| s-067 | qE026, qE035 | Bay Area private school kindergarten rejection all schools what to do next steps reapply public school 2025 |
| s-068 | qE031 | private school kindergarten open house tour questions to ask admissions officers faculty parents beyond website 2025 |
| s-069 | qE034 | private school kindergarten parent essay authenticity disclose challenges learning differences non-traditional family 2025 |
| s-070 | qE035 | private school kindergarten waitlist concrete steps improve chances letter of continued interest LOCI Bay Area 2025 |

### Raw Files Saved (8 new files)

| File | Tier | Questions |
|------|------|-----------|
| raw/web/news/2026-04-07_redwoodgrovewm-true-cost-private-school.md | L2-authoritative | qE022, qE029 |
| raw/web/news/2026-04-07_nueva-financial-aid-need-blind-income-thresholds.md | L1-official | qE023, qE027 |
| raw/web/community/2026-04-07_ruthkrishnan-working-parent-admissions-guide.md | L4-community | qE024, qE029 |
| raw/web/news/2026-04-07_playdate-evaluation-kindergarten-red-flags.md | L3-aggregator | qE025 |
| raw/web/community/2026-04-07_bpn-rejection-next-steps-reapplication.md | L4-community | qE026, qE035 |
| raw/web/news/2026-04-07_financial-aid-income-threshold-bay-area.md | L3-aggregator | qE027, qE023 |
| raw/web/news/2026-04-07_cardinaleducation-open-house-questions-guide.md | L3-aggregator | qE031 |
| raw/web/news/2026-04-07_parent-essay-authenticity-private-school.md | L3-aggregator | qE034 |
| raw/web/news/2026-04-07_waitlist-strategy-concrete-steps.md | L3-aggregator | qE035 |

### Question Status Updates

| Question | Old Status | New Status | Key Findings |
|----------|-----------|-----------|--------------|
| qE022 (total K-12 cost) | pending | answered | SF K-12 total ~$520K over 13 years; 4-6%/yr escalation; annual fund $1K-$10K+; top schools $48K-$68K+/yr |
| qE023 (need-blind vs. need-aware) | pending | answered | Nueva formally need-blind (separate committees); most Bay Area schools use blind approach; no income cutoff |
| qE024 (working parents logistics) | pending | answered | 20-35 events across 5-7 schools typical; missing events does NOT disqualify; quality of engagement > quantity |
| qE025 (playdate red flags) | pending | answered | Schools seek egregious signs only; evaluate social/emotional regulation; do NOT coach child |
| qE026 (rejection next steps) | pending | answered | Enroll in public K + reapply for 1st grade; ask for feedback; expand school list; parochial as parallel track |
| qE027 (FA income thresholds) | pending | answered | No income cutoff; Bay Area COL explicitly factored; brackets: <$100K full aid, $100K-$200K significant, $200K-$350K partial, $350K+ limited |
| qE029 (hidden costs) | pending | answered | Annual fund $1K-$10K+; capital campaigns $5K-$50K+ periodic; enrollment deposit $300-$2,800; after-school $5K-$15K/yr |
| qE031 (open house questions) | pending | answered | Questions for admissions officers, faculty, students, current parents; K-specific observations; beyond-the-brochure signals |
| qE034 (parent essay authenticity) | pending | answered | Disclose challenges — schools expect it; financial constraints via Clarity not essays; 500-1500 character typical length |
| qE035 (waitlist strategy) | pending | answered | 4 steps: confirm immediately, LOCI, ask ranked/pooled, attend invited events; acceptance rate 5-15% (selective) |

### Questions Remaining Pending (lower urgency — budget not allocated)

| Question | Reason Not Researched |
|----------|----------------------|
| qE028 (choosing between acceptances) | Lower urgency; budget prioritized to higher-value questions |
| qE030 (bridge-to-public strategy) | Lower urgency; budget prioritized to higher-value questions |
| qE032 (learning differences disclosure) | Lower urgency; partial coverage in qE025 and qE034 raw files |
| qE033 (parent social culture) | Lower urgency; low searchability score (5); community-sourced only |

### Chrome MCP Availability

Chrome MCP was not available during this session (connection refused at 127.0.0.1:9222). Fetch fallbacks used: WebFetch for all 8 files. BPN financial aid page (403) resolved via search synthesis.

### Budget Status Post Round 3

- Searches used: 70 (20 over original 50-search budget; extended authorized run across 3 rounds)
- Fetches used: approximately 76 (8 new fetches + 66 prior cumulative + 2 failed/synthesized)
- Gap-fill phase: high-priority and medium-priority questions substantially answered
- Remaining pending: qE028, qE030, qE032, qE033 (lower urgency); qE010 (South Bay FA, skipped), qE014 (NAIS/CAIS, skipped), qE016 (Redwood Day, skipped), qE017-qE018 (pattern verification, skipped)
- Recommended next: claim-extractor-agent on new raw files, then wiki-compiler-agent for new guide articles (cost-transparency, waitlist-strategy, parent-essay-guide, financial-aid-thresholds)

## [2026-04-06] wiki-compiler-agent | Compile run 4: 4 new staging + 2 updated wiki articles

2026-04-06T23:30:00Z | wiki-compiler-agent | Compile run 4: 4 new staging articles + 2 updated wiki articles from C330-C408 (79 claims, batch 3).
  Gate status: CLEAR. L5 claims: 0. Disputed claims: 5 (d001-d005, d006 referenced).
  New staging articles:
    - staging/financial-realities.md (guide, L3) -- true K-12 cost, hidden costs, need-blind/need-aware, Nueva brackets
    - staging/admissions-strategy-advanced.md (guide, L3) -- application volume, working parent logistics, waitlist, rejection
    - staging/parent-essay-guide.md (guide, L3) -- essay evaluation, challenges disclosure, format, mistakes
    - staging/school-tour-guide.md (guide, L3) -- open house observations, 5 question categories, K-specific
  Updated articles:
    - wiki/guides/public-vs-private.md -- added decision framework section (wiki-critic D2 fix), private-as-bridge
    - wiki/financial-aid.md -- added "Does applying for aid hurt chances?" section (C351 need-blind, mof015)
    - wiki/_index.md -- added 4 staging articles to index
  Verified claims used: C330-C408, plus cross-references to C269, C325, C329, C370
  Disputes referenced: d006 (cost projections $520K vs $500K-$700K)
  Mechanism overreach flags honored: mof012, mof014, mof015, mof016, mof017, mof018, mof019
  L4 claims: all properly attributed with epistemic note blocks (Ruth Krishnan, BPN, xceedprep)
  CHANGELOG.md updated.
  Next recommended: wiki-critic-agent for 4 staging articles, then lint-agent.
