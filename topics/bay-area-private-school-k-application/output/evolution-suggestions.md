# Evolution Suggestions — Bay Area Private School K Application — 2026-04-06

## Summary

| Category | Findings | New Questions Added to gap_fill |
|----------|----------|---------------------------------|
| Gap analysis | 3 missing articles, 4 thin, 1 pending past due (Q001c) | 2 |
| Freshness | 1 expired (E001, already in lint), 0 approaching, 2 untagged volatile | 0 (E001 in lint) |
| Pattern discovery | 3 confirmed patterns, 2 hypothetical | 3 |
| Concept gaps (backlinks) | 4 missing concept articles | 4 |
| Merge candidates | 1 pair | 0 (no new research needed) |
| South Bay targeted questions | 0 existing, user-requested | 10 |
| **Total new questions** | | **qE001–qE019 (19)** |

---

## Priority Actions (do these first)

1. [HIGH] Fix expired `valid_until` in `wiki/application-timeline.md` line 30: change `2026-03-27` to `2026-10-01` and add a header note that all dates reflect the completed 2025-26 cycle — resolves lint E001.
2. [HIGH] Create `wiki/overview.md` via wiki-compiler-agent covering topic scope, ISSFBA framework, two assessment models, financial aid overview, regional map, and navigation links — resolves lint E002.
3. [HIGH] Run `/kb-research bay-area-private-school-k-application --phase gap` to execute qE001–qE010 (South Bay school profiles) and qE011–qE015 (concept gaps) — these are the highest-value unresearched entities.
4. [HIGH] Create `wiki/school-profiles-south-bay.md` after research completes — dedicated article rather than appending to the Peninsula/East Bay article, which already overstates its coverage (lint I005).
5. [MEDIUM] Create `wiki/pedagogy-philosophy.md` covering educational philosophy clusters across Bay Area schools — fills lint W011 (Q007 and Q007a answered but no wiki article).
6. [MEDIUM] Expand `wiki/language-immersion.md` to fill the four stub immersion programs (Lycee Francais, Terra SF, SVIS, EBGIS) after research executes qE016.
7. [MEDIUM] Fill missing comparison table values: CAIS decision date (W004), La Scuola age cutoff/decision date/platform (W005), Keys School age cutoff and Nueva decision date (W006) — these are targeted fact lookups, not new research questions.
8. [LOW] Add article merge: absorb `wiki/language-immersion.md` into a new `wiki/school-profiles-immersion.md` that covers all immersion schools as an entity file rather than a concept stub, once the four stubs are researched.

---

## 1. Gap Analysis Findings

### Missing Articles (create these)

| Question ID | Question Text | Suggested Article | Type |
|-------------|---------------|-------------------|------|
| Q001c | "Major private elementary schools in the South Bay (San Jose, Saratoga, Los Altos) with K programs" | `wiki/school-profiles-south-bay.md` — full entity article covering Harker, Helios, Challenger, Stratford, Gideon Hausner, Almaden Country School, and others identified by qE001–qE010 | entity |
| Q007 / Q007a | "Educational philosophies among Bay Area private K schools (Montessori, Waldorf, Reggio, progressive, traditional, religious)" — status: answered; no wiki article exists | `wiki/pedagogy-philosophy.md` — philosophy clusters with named school examples per philosophy | guide/concept |
| (new) | Overview article explicitly called for in lint E002 | `wiki/overview.md` — root entry point for the wiki, ~600 words | guide |

Note: lint W011 confirms Q007 and Q007a are answered but have no wiki representation. This is the most significant answered-but-not-compiled gap.

### Thin Coverage (expand these)

| Article | Current Coverage | What's Missing |
|---------|-----------------|----------------|
| `wiki/school-profiles-peninsula-east-bay.md` | 6 schools (Keys, Nueva, Head-Royce, Park Day, MCDS, Marin Horizon) + 4 stubs | South Bay is entirely absent (lint I002); East Bay beyond Oakland is absent (no Berkeley, Piedmont, Alameda schools). Title implies comprehensive coverage it doesn't have. Add intro note disclosing coverage gaps immediately. |
| `wiki/language-immersion.md` | 2 verified programs (CAIS, La Scuola); 4 stubs | Full immersion model ratios (percentage of instruction in target language vs. English), outcomes data, sibling policies, language placement at enrollment. Four stub programs have zero data. |
| `wiki/admissions-strategy.md` | Covers SF-centric strategy, sibling policy, consultants, waitlist | Missing: South Bay-specific strategy (IQ testing scheduling lead time of 3-6 months required), gifted-school track advice, public TK as alternative / bridging strategy, ISSFBA vs. non-ISSFBA school differences in waitlist mechanics. |
| `wiki/assessment-playdate.md` | Covers SF playdates well; IQ testing section has Harker, Helios, Nueva but only SF Standard single-source data | IQ test logistics: which psychologists administer WPPSI in South Bay, timeline for scheduling (books out fast September-January), what to do if child tests below threshold, whether multiple attempts are accepted. |

### Pending Question Not Yet Compiled

| Question ID | Question Text | Status | Notes |
|-------------|---------------|--------|-------|
| Q001c | "Major private elementary schools in the South Bay with K programs" | answered | Raw file linked is `nuevaschool-kindergarten-apply.md` — a Peninsula school, not South Bay. The actual South Bay research was captured only in a single search query (`s-2026-04-06-032`: "BASIS Independent Silicon Valley Harker School Stratford School South Bay kindergarten admissions tuition 2026"). No raw file with South Bay official source data was produced. The question is marked `answered` but the wiki has zero South Bay content beyond Harker/Helios stubs. This is `budget_blocked` — research stopped at Q001c without fetching official sources. |

---

## 2. Freshness Findings

### Expired Content

| Article | Volatile Field | valid_until | Days Past | Re-verification Source |
|---------|---------------|-------------|-----------|----------------------|
| `wiki/application-timeline.md` | All deadline and date data (March 19 decision date, Jan 5-30 application deadlines, March 24-26 enrollment deadlines, September open house dates) | 2026-03-27 | 10 days | Individual school admissions pages listed in article's `sources` frontmatter; ISSFBA coordinated dates page at issfba.org |

Note: This is already flagged as E001 in lint-report-2026-04-06.md. Not re-reporting here; referencing for prioritization.

### Approaching Expiry (within 30 days)

None. All other articles have `valid_until: 2027-07-01`.

### Untagged Volatile Data

| Article | Detected Content | Fix |
|---------|-----------------|-----|
| `wiki/admissions-strategy.md` | Consultant fee range "$3,000-$15,000" and application fees "$100-200 per school" — sourced from community-tier (ruthkrishnan.com blog) with no `valid_until` qualifier | Add year qualifier "(as of 2026, unverified)" inline and note in frontmatter that consultant pricing data was not confirmed against consultant websites |
| `wiki/financial-aid.md` | Tuition inflation rate "4-6% annually" (line 95, W007) and two KQED statistics ("$10K-$65K range" and "30% of SF K-12 students in private schools") — no fact-sheet entries | These are flagged as W007 and W008 in lint. Add `valid_until: 2027-07-01` to article frontmatter and submit three claims to fact-checker-agent. |

### Annual Re-Research Candidates

| Question | answered_at | Facet | Notes |
|----------|-------------|-------|-------|
| Q014 "Specific 2026-2027 application deadlines" | 2026-04-06 | WHEN | The article was compiled for the 2025-26 cycle (applications submitted fall 2025, enrollment fall 2026). At 6 months (October 2026), this content will need full replacement for the 2026-27 cycle. Flag for re-research at `valid_until: 2026-10-01`. |
| Q002 "Annual admissions timeline" | 2026-04-06 | WHEN | Core deadline structure shifts annually with ISSFBA coordinated dates. Re-verify in September 2026 when schools post 2026-27 cycle dates. |
| Q004 / Q017 "Tuition ranges" | 2026-04-06 | WHAT/numerical | Bay Area private school tuition historically increases 4-6% annually. Most tuition figures in the wiki are 2025-26 or 2026-27 figures. Re-verify August 2026 when schools post new tuition for 2026-27 cycle. |

---

## 3. Cross-Entity Patterns

### Confirmed Patterns (N >= 3 entities)

**Pattern A: Progressive schools cluster at the late end of the January deadline window**
- Evidence: Live Oak School (Jan 6, progressive), Park Day School (Jan 16, progressive), The San Francisco School (Jan 23, progressive), Marin Horizon School (Jan 30, progressive)
- Contrast: Traditional schools with earlier deadlines: Convent & Stuart Hall (Dec 12), SF Day School (Dec 19), SF Friends School (Dec 19), Town School for Boys (Jan 8), The Hamlin School (December)
- Pattern: Progressive-philosophy schools in the research dataset have deadlines Jan 6 or later; traditional/structured schools have deadlines Dec 12 through Jan 8.
- Evidence strength: 4 progressive schools at Jan 6–30 vs. 5 traditional schools at Dec 12–Jan 8. Confirmed (N=4). Not causal — but actionable for parents: if applying to a progressive-philosophy list, the deadline pressure wave falls in the second half of January.
- Suggested article section: Add to `wiki/admissions-strategy.md` under "Building a School List" — "Philosophy and Deadline Alignment" subsection.
- Added question: qE017

**Pattern B: Schools with indexed/sliding-scale tuition also have later application deadlines**
- Evidence: CDS (Jan 20, indexed tuition), Park Day (Jan 16, indexed), The San Francisco School (Jan 23, indexed), La Scuola (Jan 15, sliding scale)
- Contrast: Fixed-tuition schools: SF Day (Dec 19, fixed $48,577), Convent & Stuart Hall (Dec 12, fixed)
- Pattern: 4 of 4 indexed-tuition schools have January deadlines; 2 of the earliest-deadline schools have fixed tuition. The correlation may reflect school culture/mission (progressive + need-blind financial access together), not a direct causal mechanism.
- Evidence strength: 4 data points — moderate. Confirmed for wiki mention with epistemic qualifier.
- Suggested article update: Add to `wiki/financial-aid.md` under a new "Admissions Context" note.
- Added question: qE018 (verify whether this correlation holds in South Bay data once collected)

**Pattern C: ISSFBA membership predicts March 19 coordinated decision date with near-certainty**
- Evidence: SF Day (Mar 19), CDS (Mar 19), Convent & Stuart Hall (Mar 19), Hamlin (Mar 19), Presidio Hill (Mar 19), SF Friends (Mar 19), Head-Royce (Mar 19), Park Day (Mar 19), MCDS (Mar 19), Marin Horizon (Mar 19) — 10 confirmed schools
- Exceptions: Live Oak (Mar 17 — confirmed ISSFBA member but early); Keys School (Feb 19 — likely not ISSFBA)
- Pattern: All confirmed ISSFBA member schools in this dataset use March 19 except Live Oak. Keys School (non-ISSFBA likely) uses February 19 — a full month earlier.
- Actionable insight: Non-ISSFBA schools (Harker, Helios, Challenger, Stratford) may have decision timelines entirely detached from March 19. This is important for South Bay applicants who may get decisions in January-February.
- Added question: qE019 (confirm South Bay school decision date timelines)

### Hypothetical Patterns (N < 3 — verify before publishing)

**Hypothesis A: IQ-testing schools are clustered in the South Bay / Peninsula and absent from SF proper**
- Evidence: Nueva (Peninsula, IQ required), Harker (South Bay, IQ required), Helios (South Bay, IQ required) — 3 data points but concentrated in 2 sub-regions
- SF schools (Hamlin, CDS, SF Day, Live Oak, SF Friends, Town School, Convent, Presidio Hill, CAIS, La Scuola, The SF School): 0 IQ tests required
- This is looking confirmed (N=3 IQ schools; N=11 non-IQ SF schools) but the South Bay is under-researched. Challenger School and BASIS Independent Silicon Valley need verification.
- Added verification question: qE006 (embedded in South Bay research)

**Hypothesis B: Schools that are not ISSFBA members do not use Ravenna**
- Evidence: Keys School (likely not ISSFBA, not confirmed Ravenna user). Nueva School confirmed Ravenna user but has non-standard decision date.
- Nuance: Nueva uses Ravenna but departs from coordinated decision dates — suggesting Ravenna membership and ISSFBA membership are not perfectly correlated.
- N=1 for the non-Ravenna/non-ISSFBA link. Need data from Harker, Challenger, Stratford.
- Added verification question: qE007 (embedded in South Bay research)

### Concept Gaps (ranked by backlink count)

| Concept | Linked from | Status | Suggestion |
|---------|------------|--------|------------|
| Educational philosophy / progressive vs. traditional | Referenced in `admissions-strategy.md` (3x), `assessment-playdate.md` (1x), `school-profiles-sf.md` (4x, implicitly), `school-profiles-peninsula-east-bay.md` (1x) — 5+ articles | No article | CREATE `wiki/pedagogy-philosophy.md` — covers Montessori, Waldorf, Reggio Emilia, progressive, traditional, religious philosophies with named Bay Area school examples per category. Q007 and Q007a are answered; this is a compilation gap. |
| TK (Transitional Kindergarten) | Referenced in `school-profiles-sf.md` (Presidio Hill "TK-8"), `school-profiles-peninsula-east-bay.md` (Park Day "TK Age Cutoff"), `application-timeline.md` (PreK/TK/JK notification date), `issfba-bada.md` (PreK/TK/JK coordinated date) — 4 articles | No article | CREATE `wiki/transitional-kindergarten.md` — covers what TK is, California public TK expansion context, which private schools offer TK, age eligibility (4 by Sep 1), how private TK differs from public TK. |
| Feeder preschools | Referenced in `admissions-strategy.md` (implicitly — "Hamlin K class draws from 28 different preschools"), `school-profiles-sf.md` (1x mention), not explicitly wikilinked | No article | CREATE `wiki/feeder-preschools.md` — covers whether preschool choice affects K admissions, the "28 preschools" Hamlin data point, consultant advice on preschool selection, and epistemic limits (schools don't disclose preschool preference). |
| NAIS / CAIS accreditation | Referenced in `issfba-bada.md` ("Q008" covers NAIS/CAIS/ISSFBA) but no wiki article covers what NAIS/CAIS accreditation means for quality signaling | No article | CREATE `wiki/accreditation-nais-cais.md` — covers what NAIS membership signals, CAIS (California Association of Independent Schools) accreditation, and how families should use accreditation status in school evaluation. |

### Article Merge Candidates

| Article A | Article B | Overlap | Recommendation |
|-----------|-----------|---------|----------------|
| `wiki/language-immersion.md` (concept, ~400 words, 2 verified + 4 stubs) | Sections in `wiki/school-profiles-sf.md` (CAIS and La Scuola profiles) | ~70% — the language-immersion article duplicates the CAIS and La Scuola sections from school-profiles-sf.md and adds only 3 sentences of unique content | After qE016 research fills the 4 stub immersion programs, convert `wiki/language-immersion.md` from a concept stub into a full entity-style article `wiki/school-profiles-immersion.md` covering all 6 immersion schools. This gives CAIS and La Scuola richer profiles in the immersion article (immersion model ratios, outcomes, language placement) without duplicating the admissions-focused data already in school-profiles-sf.md. |

---

## 4. Regional Coverage Map

| Region | Schools with Full Profiles | Schools as Stubs | Coverage Level |
|--------|---------------------------|-----------------|----------------|
| San Francisco (city) | 11 (SF Day, CDS, Convent & Stuart Hall, Hamlin, Live Oak, Presidio Hill, SF Friends, CAIS, La Scuola, Town School, The SF School) | Lycee Francais SF, Terra SF | STRONG — the most complete region |
| Peninsula (north — Hillsborough, Palo Alto, Menlo Park) | 2 (Keys, Nueva) | Gideon Hausner (Palo Alto), Peninsula School (Menlo Park) | PARTIAL — 2 profiles, 2 stubs, other schools not identified |
| East Bay (Oakland) | 2 (Head-Royce, Park Day) | Redwood Day School | PARTIAL — Oakland only; Berkeley, Piedmont, Alameda absent |
| Marin County | 2 (MCDS, Marin Horizon) | Ring Mountain Day, Branson (K program?), Reed Union | PARTIAL — 2 profiles; other Marin schools not confirmed |
| South Bay (San Jose, Saratoga, Los Altos, Cupertino, Campbell, Palo Alto) | 0 | Harker, Helios, Challenger, Stratford, Gideon Hausner, Almaden Country School, BASIS Independent Silicon Valley | ABSENT — highest priority gap for user's stated goal |

**For a comprehensive parent guide, the South Bay gap is the largest single structural deficit.** A parent in Saratoga or San Jose cannot use this wiki to answer their most basic question: which schools serve my area?

---

## 5. Parent Guide Article Outline

The user's goal is a standalone comprehensive Bay Area K private school application reference. The current wiki covers the SF-centric journey well but is missing the following articles and sections to be a true Bay Area guide:

### Missing Articles Needed for a Comprehensive Parent Guide

| Article | Content | Priority |
|---------|---------|----------|
| `wiki/overview.md` | Topic scope, ISSFBA framework, two assessment tracks (playdate vs. IQ), Bay Area regional map, financial aid overview, how to use the wiki, 600-800 words | BLOCKER (lint E002) |
| `wiki/school-profiles-south-bay.md` | Full profiles for Harker, Helios, Challenger School, Stratford School, Gideon Hausner, Almaden Country School; comparison table with Age Cutoff, App Deadline, Tuition, Assessment Type, IQ min (if applicable), Decision Date, Platform | HIGH |
| `wiki/pedagogy-philosophy.md` | Philosophy map: which schools are progressive / traditional / Montessori / Waldorf / Reggio / religious / gifted; what each philosophy means for daily school life and admissions culture | HIGH |
| `wiki/transitional-kindergarten.md` | Private TK vs. public TK, age eligibility, which private schools offer TK, how TK differs from K in admissions | MEDIUM |
| `wiki/feeder-preschools.md` | Does preschool choice matter? Hamlin's "28 preschools" data point; consultant perspective; epistemic limits | MEDIUM |
| `wiki/accreditation-nais-cais.md` | What NAIS and CAIS membership signals about school quality and oversight | LOW |
| `wiki/school-profiles-east-bay-expanded.md` | Berkeley, Piedmont, Alameda K programs currently absent | MEDIUM |

### Sections Missing from Existing Articles

| Article | Missing Section |
|---------|----------------|
| `wiki/admissions-strategy.md` | "If You're in the South Bay" — how the process differs: IQ testing required at several schools, non-ISSFBA decision timelines, different application platforms, Harker/Helios IQ scheduling (must book September); "Philosophy and Deadline Alignment" — progressive vs. traditional schools have different deadline windows |
| `wiki/assessment-playdate.md` | "Scheduling IQ Testing: Logistics" — which licensed psychologists administer WPPSI in the South Bay, typical booking lead time (2-4 months), cost ($850+), whether multiple tests are permitted, what to do if score falls below threshold |
| `wiki/financial-aid.md` | South Bay financial aid data — Harker, Stratford, Challenger tuition and aid programs (currently $0 data); table comparing South Bay vs. SF vs. Peninsula full tuition |
| `wiki/application-timeline.md` | South Bay timeline column — South Bay schools (Harker, Helios, Challenger) have different cycle structures not synchronized with ISSFBA March 19 |

---

## 6. New Questions Added to Research Plan

The following questions have been added to `research-plan.yaml` under `phases.gap_fill.questions`. The composite formula used is: `user_value * 0.35 + dependency_count * 0.25 + searchability * 0.20 + novelty * 0.20`.

### South Bay School Profile Questions (qE001–qE010)

```yaml
- id: qE001
  text: "What are Harker School's kindergarten/TK admissions requirements, application deadline, IQ test details, tuition, class size, and philosophy for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 9
    dependency_count: 4
    searchability: 9
    novelty: 7
  composite: 7.60
  dependencies: [Q001c, Q031]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE002
  text: "What are Helios School's kindergarten admissions requirements, application deadline, IQ test policy, tuition, and philosophy for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 8
    dependency_count: 3
    searchability: 8
    novelty: 7
  composite: 6.80
  dependencies: [Q001c, Q031]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE003
  text: "What are Challenger School's kindergarten admissions process, tuition, philosophy (structured/direct instruction), and locations in the South Bay for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 8
    dependency_count: 3
    searchability: 8
    novelty: 8
  composite: 6.95
  dependencies: [Q001c]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE004
  text: "What are Gideon Hausner Jewish Day School's kindergarten admissions requirements, application deadline, tuition, Jewish identity policy, and philosophy for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 2
    searchability: 8
    novelty: 7
  composite: 6.35
  dependencies: [Q001c, Q034]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE005
  text: "What are Stratford School's kindergarten admissions process, tuition, South Bay campus locations, and academic philosophy for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 2
    searchability: 8
    novelty: 7
  composite: 6.35
  dependencies: [Q001c]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE006
  text: "What are Almaden Country School's kindergarten admissions process, tuition, and philosophy for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 6
    dependency_count: 2
    searchability: 7
    novelty: 7
  composite: 5.75
  dependencies: [Q001c]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE007
  text: "What are BASIS Independent Silicon Valley's kindergarten admissions requirements, assessment process, tuition, and philosophy for the 2026-27 cycle?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 2
    searchability: 8
    novelty: 7
  composite: 6.35
  dependencies: [Q001c, Q031]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06

- id: qE008
  text: "What application platforms (Ravenna or school-specific) do South Bay private schools (Harker, Helios, Challenger, Stratford, Gideon Hausner, BASIS) use, and are they ISSFBA members?"
  facet: HOW
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 3
    searchability: 8
    novelty: 6
  composite: 6.45
  dependencies: [Q001c, Q011, QG001]
  status: pending
  discovered_from: evolution_pattern_discovery
  evolution_run: 2026-04-06

- id: qE009
  text: "What are the kindergarten decision notification dates and enrollment response deadlines for major South Bay private schools (Harker, Helios, Challenger, Stratford) — do they follow the ISSFBA March 19 date or have independent timelines?"
  facet: WHEN
  phase: gap_fill
  scores:
    user_value: 8
    dependency_count: 3
    searchability: 8
    novelty: 7
  composite: 6.95
  dependencies: [Q001c, Q014, QG001]
  status: pending
  discovered_from: evolution_pattern_discovery
  evolution_run: 2026-04-06

- id: qE010
  text: "What financial aid and tuition assistance programs are available at South Bay private K schools (Harker, Challenger, Stratford, Gideon Hausner), and what percentage of families receive aid?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 8
    dependency_count: 2
    searchability: 7
    novelty: 6
  composite: 6.45
  dependencies: [Q001c, Q012, Q018]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06
```

### Concept Gap Questions (qE011–qE016)

```yaml
- id: qE011
  text: "What are the major educational philosophy types (Montessori, Waldorf, Reggio Emilia, progressive, traditional, gifted) represented among Bay Area private K schools, and which specific named schools fall into each category?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 8
    dependency_count: 4
    searchability: 7
    novelty: 5
  composite: 6.55
  dependencies: [Q007, Q007a]
  status: pending
  discovered_from: evolution_gap_analysis
  notes: "Q007 and Q007a are both answered but no wiki article was compiled from the research. This question directs research-agent to fetch official school philosophy pages for the compilation pass."
  evolution_run: 2026-04-06

- id: qE012
  text: "What is California's Transitional Kindergarten program, how do private school TK offerings compare to public TK, and which Bay Area private schools offer TK entry (distinct from K)?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 3
    searchability: 8
    novelty: 6
  composite: 6.50
  dependencies: [Q001, Q010]
  status: pending
  discovered_from: evolution_backlink_analysis
  evolution_run: 2026-04-06

- id: qE013
  text: "Does preschool choice meaningfully affect Bay Area private K admissions outcomes, and which preschools are known feeders to competitive SF, Peninsula, and South Bay private elementaries?"
  facet: WHO
  phase: gap_fill
  scores:
    user_value: 8
    dependency_count: 2
    searchability: 5
    novelty: 8
  composite: 6.35
  dependencies: [Q023, Q019]
  status: pending
  discovered_from: evolution_backlink_analysis
  evolution_run: 2026-04-06

- id: qE014
  text: "What does NAIS (National Association of Independent Schools) and CAIS (California Association of Independent Schools) membership or accreditation signify, and which Bay Area K schools hold these memberships?"
  facet: WHO
  phase: gap_fill
  scores:
    user_value: 6
    dependency_count: 2
    searchability: 8
    novelty: 6
  composite: 5.90
  dependencies: [Q008]
  status: pending
  discovered_from: evolution_backlink_analysis
  evolution_run: 2026-04-06

- id: qE015
  text: "What are the specific admissions processes, immersion model structures (percentage of instruction in target language), and K application details for Lycee Francais de San Francisco, Terra School SF, Silicon Valley International School, and East Bay German International School?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 3
    searchability: 8
    novelty: 6
  composite: 6.45
  dependencies: [Q020, Q001]
  status: pending
  discovered_from: evolution_gap_analysis
  notes: "Fills the 4 immersion school stubs in wiki/language-immersion.md. Silicon Valley International School was formerly ISTP."
  evolution_run: 2026-04-06

- id: qE016
  text: "What are the admissions processes, tuition, and K program details for Redwood Day School (Oakland) and other East Bay private K schools not yet profiled (Berkeley, Piedmont, Alameda)?"
  facet: WHAT
  phase: gap_fill
  scores:
    user_value: 6
    dependency_count: 2
    searchability: 7
    novelty: 6
  composite: 5.75
  dependencies: [Q001a, Q027]
  status: pending
  discovered_from: evolution_gap_analysis
  evolution_run: 2026-04-06
```

### Pattern Verification Questions (qE017–qE019)

```yaml
- id: qE017
  text: "Do progressive-philosophy Bay Area private K schools consistently set later application deadlines (January 15 or later) compared to traditional and structured schools — and does this pattern hold across South Bay schools once researched?"
  facet: COMPARE
  phase: gap_fill
  scores:
    user_value: 6
    dependency_count: 3
    searchability: 5
    novelty: 9
  composite: 5.80
  dependencies: [Q022, Q007a, qE001, qE003, qE005]
  status: pending
  discovered_from: evolution_pattern_discovery
  notes: "Pattern A confirmed for SF (N=4) but not yet tested against South Bay schools. Resolve after South Bay research completes."
  evolution_run: 2026-04-06

- id: qE018
  text: "Do Bay Area private K schools with indexed/sliding-scale tuition models also tend to use the Clarity financial aid platform, and do they cluster at later application deadlines compared to fixed-tuition schools?"
  facet: COMPARE
  phase: gap_fill
  scores:
    user_value: 6
    dependency_count: 2
    searchability: 5
    novelty: 8
  composite: 5.55
  dependencies: [Q017, Q018, qE010]
  status: pending
  discovered_from: evolution_pattern_discovery
  notes: "Pattern B confirmed for SF (N=4) but needs South Bay data to hold or refute."
  evolution_run: 2026-04-06

- id: qE019
  text: "What are the actual kindergarten decision notification dates for South Bay and non-ISSFBA Peninsula private schools — do they use March 19 (ISSFBA coordinated) or independent dates, and what is the typical timeline?"
  facet: WHEN
  phase: gap_fill
  scores:
    user_value: 7
    dependency_count: 3
    searchability: 7
    novelty: 7
  composite: 6.30
  dependencies: [qE001, qE003, qE005, QG001]
  status: pending
  discovered_from: evolution_pattern_discovery
  notes: "Pattern C — extends ISSFBA/non-ISSFBA decision date analysis to South Bay. Keys School (Feb 19) is the only confirmed non-ISSFBA data point currently."
  evolution_run: 2026-04-06
```

---

## 7. Recommended Pipeline Commands

```bash
# Re-open gap_fill phase and execute South Bay + concept gap research
# (research-agent will execute qE001–qE019 in composite score order)
python -m backend.pipeline search --topic bay-area-private-school-k-application --phase gap-fill

# After research: compile new South Bay article, philosophy article, TK article, and overview
python -m backend.pipeline compile --topic bay-area-private-school-k-application

# Health check after compile
python -m backend.pipeline lint --topic bay-area-private-school-k-application
```

**Manual fixes that do not require research (do before next pipeline run):**
1. `wiki/application-timeline.md` line 30: `valid_until: 2026-03-27` → `valid_until: 2026-10-01`
2. `wiki/_index.md` line 4: `Articles: 8` → `Articles: 9` (resolves lint W002)
3. `wiki/application-timeline.md` lines 57–70: remove line 64 (Clarity row duplicate) and re-sort Jan table ascending (resolves lint W003, W010)
4. Run `backend/tools/cross_linker.py` against wiki directory (resolves lint W001)
