# Operation Log

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
