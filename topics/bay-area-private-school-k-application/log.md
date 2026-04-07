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
