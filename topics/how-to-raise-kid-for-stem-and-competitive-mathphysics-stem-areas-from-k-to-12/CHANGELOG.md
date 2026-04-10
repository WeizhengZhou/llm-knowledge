# Changelog — How to Raise a Kid for STEM and Competitive Math/Physics, from K to 12

_Append-only log of all wiki modifications. Each entry records what changed, what was added/removed, and why._

## 2026-04-10 — wiki-compiler-agent

**Added:**
- `staging/concepts/is-this-right-for-my-child.md` — Decision framework for whether to pursue competitive STEM (RO1)
- `staging/concepts/competition-math-vs-school-math.md` — Why school math and competition math diverge (RO2)
- `staging/guides/k12-stem-roadmap.md` — Full K-12 timeline by grade band (RO2, RO3)
- `staging/guides/competition-math-pipeline.md` — AMC 8 through IMO pipeline with 2025-2026 dates (RO3)
- `staging/guides/physics-competitions-pathway.md` — F=ma through IPhO pipeline (RO3)
- `staging/guides/summer-programs-guide.md` — 10-program comparison table: Ross, PROMYS, Mathcamp, HCSSiM, RSI, MOP, MathPath, MathILy, SUMaC, AwesomeMath (RO4)
- `staging/guides/enrichment-programs-guide.md` — AoPS, Beast Academy, Singapore Math, RSM, OTIS, Expii comparison (RO4)
- `staging/guides/book-resources-by-level.md` — Math and physics book recommendations by stage (RO4)
- `staging/guides/acceleration-decisions.md` — Research-backed guide to grade skipping, dual enrollment, magnet schools (RO5)
- `staging/guides/college-admissions-strategy.md` — How competitions/programs factor into admissions (RO6)
- `staging/guides/burnout-prevention.md` — Warning signs, recovery, parent behaviors (RO7)
- `staging/guides/cost-and-financial-aid.md` — 4-tier cost breakdown, financial aid sources, free resources (RO8)
- `staging/entities/aops-art-of-problem-solving.md` — AoPS ecosystem: books, courses, Beast Academy, Alcumus
- `staging/entities/mathcounts.md` — MATHCOUNTS + MOEMS competition profiles
- `staging/entities/amc-competitions.md` — AMC 8/10/12 + ARML + USAMTS + Math Kangaroo
- `staging/entities/ross-program.md` — Ross Mathematics Program profile
- `staging/entities/promys.md` — PROMYS profile
- `staging/entities/canada-usa-mathcamp.md` — Canada/USA Mathcamp profile
- `staging/entities/research-science-institute.md` — RSI profile
- `staging/entities/science-competitions.md` — ISEF, Regeneron STS, Science Olympiad, JSHS

**Changed:**
- `wiki/_index.md` — Created wiki index with all 20 articles
- `index.md` — Updated with research run summary

**Reason:** First full pipeline compile run. All 126 fact-sheet claims processed; 4 disputes resolved; c058 (L5 BLOCKED) handled via replacement_permitted_language.

## 2026-04-10 — wiki-compiler-agent (critic revision pass)

**Changed:**
- `staging/concepts/is-this-right-for-my-child.md` — Added Common Mistakes section (3 mistakes: conflating school performance with competition readiness, early-start pressure, mistaking compliance for motivation)
- `staging/concepts/competition-math-vs-school-math.md` — Added Common Mistakes section (3 mistakes: school grades as predictor, adding vs. replacing school math, interpreting AMC 8 disappointment)
- `staging/guides/k12-stem-roadmap.md` — Added "Fostering Mathematical Thinking Without Drilling" subsection to K-2 grade band (RO2 must_answer); improved Common Mistakes to be more specific (replaced generic entries)
- `staging/guides/physics-competitions-pathway.md` — Removed duplicate "Book Progression for Physics Competitions" section (scope violation); replaced with one-sentence wikilink to book-resources-by-level
- `staging/guides/summer-programs-guide.md` — Added "Private Coach vs. Self-Study vs. Group Classes" section (RO4 must_answer item)
- `staging/guides/book-resources-by-level.md` — Added "Start with" recommendations within each of 4 stages; added Olympiad-level per-topic entry points
- `staging/guides/acceleration-decisions.md` — Added "Acceleration vs. Enrichment: What Research Shows" section comparing SMPY outcomes; added is-this-right-for-my-child cross-link
- `staging/guides/college-admissions-strategy.md` — Added "How to Present Competition Achievements on College Applications" section with Activities/Honors/Additional Info/Essays guidance (RO6 must_answer)
- `staging/guides/cost-and-financial-aid.md` — Added "Opportunity Cost: What Heavy Competition Focus Displaces" section with time-commitment-to-lifestyle-impact mapping (RO8 must_answer)
- `staging/guides/enrichment-programs-guide.md` — Removed inline program pricing figures (Beast Academy, Singapore Math, Kumon, AoPS courses, AwesomeMath); replaced with wikilinks to cost-and-financial-aid
- `staging/entities/aops-art-of-problem-solving.md` — Added "Which AoPS Product Should You Use?" decision table; added Common Mistakes section (3 mistakes); added accreditation context
- `staging/entities/mathcounts.md` — Added "Is MATHCOUNTS Right for My Child?" decision framing with L4 synthesis; added Common Mistakes section (3 mistakes)
- `staging/entities/amc-competitions.md` — Added "What Participants Observe" L4 synthesis section (c124, c123); added Common Mistakes section (3 mistakes)
- `staging/entities/ross-program.md` — Added Common Mistakes section (3 mistakes); added L4 synthesis on student experience
- `staging/entities/promys.md` — Added "How PROMYS Differs from Ross" section with 4 concrete differentiators; added Common Mistakes section (3 mistakes)
- `staging/entities/canada-usa-mathcamp.md` — Added Application section (Qualifying Quiz); added Common Mistakes section (3 mistakes); added L4 synthesis on breadth experience
- `staging/entities/research-science-institute.md` — Added Common Mistakes section (3 mistakes); added L4 synthesis on research experience
- `staging/entities/science-competitions.md` — Added "ISEF Qualification Pathway" 4-step explanation with timeline implications; added Common Mistakes section (3 mistakes)

**Reason:** Critic revision pass addressing all NEEDS-REVISION must-fix items across 18 articles. Cross-cutting fixes: Common Mistakes added to all entity articles; L4 synthesis blocks added where community data exists; pricing removed from enrichment guide (deferred to cost guide).

## 2026-04-10 — wiki-compiler-agent (gap-fill: broken wikilinks)

**Added:**
- `wiki/entities/usamts.md` — Standalone USAMTS entity article (L1, evergreen). Fixes broken `[[entities/usamts|USAMTS]]` wikilinks in competition-math-pipeline, k12-stem-roadmap, competition-math-vs-school-math, cost-and-financial-aid. Uses claims c051, c052, c053, c118.
- `wiki/entities/mathpath.md` — Standalone MathPath entity article (L3, annual). Fixes broken `[[entities/mathpath|MathPath]]` wikilinks in k12-stem-roadmap. Uses claim c081.

**Changed:**
- `wiki/_index.md` — Added usamts and mathpath to Entities section; updated article count from 20 to 22

**Reason:** Gap-fill pass to resolve broken wikilinks to entities referenced across 6+ existing wiki articles.
