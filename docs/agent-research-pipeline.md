# Agent-Driven Research Pipeline: Design Document

**Companion to:** [design.md](./design.md)
**Running example:** *"How to apply to private school K level in the Bay Area"*

---

## 1. The Problem

A human says: *"Build me a knowledge base about applying to Bay Area private kindergartens."*

The agent needs to:
- Figure out **what questions to ask** (the human doesn't know what they don't know)
- Search the web **iteratively** (each answer reveals new questions)
- Synthesize across **dozens of sources** that may conflict
- Produce a **structured, high-quality wiki** — not a dump of raw search results
- Do this **efficiently** — minimize redundant searches, maximize signal per query

---

## 2. Pipeline Overview
<!-- should the agent record the raw search results? including the query and extract text from the web page? -->

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  1. SEED    │────>│  2. EXPAND   │────>│  3. HARVEST  │────>│  4. COMPILE  │
│  Question   │     │  Question    │     │  & Verify    │     │  Wiki        │
│  Decompose  │     │  Tree        │     │              │     │              │
└─────────────┘     └──────┬───────┘     └──────────────┘     └──────┬───────┘
                           │                                         │
                           v                                         v
                    ┌──────────────┐                          ┌──────────────┐
                    │  Loop back   │                          │  5. LINT &   │
                    │  with new    │                          │  EVOLVE      │
                    │  questions   │                          │              │
                    └──────────────┘                          └──────────────┘
```

---

## 3. Phase 1: Seed Question Decomposition

### What happens

The agent takes the user's topic and **decomposes it into a question tree** before performing any web search. This is the most critical step — the quality of the knowledge base depends entirely on asking the right questions.

### Strategy: Faceted Decomposition

The agent generates questions across **structural facets** of the topic:

```yaml
topic: "Bay Area private school K application"

facets:
  WHO:
    - What types of families apply? (demographics, priorities)
    - Who are the key decision-makers at schools? (admissions directors)

  WHAT:
    - What schools exist? (list, locations, type: secular/religious/Montessori/etc.)
    - What do applications require? (forms, essays, recommendations, assessments)
    - What are the selection criteria? (what schools look for)

  WHEN:
    - What is the application timeline? (open dates, deadlines, decision dates)
    - When should preparation start? (years ahead? months?)
    - What are the key dates for 2026-2027 cycle?

  WHERE:
    - Which geographic areas? (SF, Peninsula, South Bay, East Bay)
    - Where do families get information? (school websites, fairs, consultants)

  HOW:
    - How does the assessment/playdate work?
    - How do parents write application essays?
    - How do schools handle siblings, legacies, diversity?
    - How much does it cost? (tuition, application fees, financial aid)

  WHY:
    - Why choose private over public? (TK, language immersion, philosophy)
    - Why do families get rejected? (common mistakes)

  COMPARE:
    - How do schools differ on philosophy? (progressive vs traditional)
    - How do SF schools differ from Peninsula/South Bay?
    - What are the acceptance rates?

  META:
    - What do current parents wish they'd known?
    - What has changed recently? (post-COVID, demographic shifts)
    - What are consultants/coaches and are they worth it?
```

### Implementation

```python
# Pseudocode for seed decomposition
def decompose_topic(topic: str) -> QuestionTree:
    # Step 1: Generate faceted questions using LLM
    questions = llm.generate(
        prompt=f"""
        You are a research planner. Given the topic: "{topic}"
        Generate questions across these facets: WHO, WHAT, WHEN, WHERE, HOW, WHY, COMPARE, META.
        For each question, estimate:
        - priority: high/medium/low (how essential is this to a parent?)
        - searchability: high/medium/low (can web search answer this well?)
        - stability: stable/seasonal/volatile (how quickly does this info change?)
        """
    )

    # Step 2: Prioritize — high-priority + high-searchability first
    questions.sort(key=lambda q: (q.priority, q.searchability), reverse=True)

    # Step 3: Identify dependencies (e.g., "school list" must come before "compare schools")
    questions.add_dependencies()

    return questions
```

### Output

A prioritized question tree stored as `raw/research-plan.yaml`:

```yaml
research_plan:
  topic: "Bay Area private school K application"
  created: 2026-04-06
  questions:
    - id: q1
      question: "What are the Bay Area private schools with K entry?"
      facet: WHAT
      priority: high
      searchability: high
      stability: stable
      dependencies: []
      status: pending

    - id: q2
      question: "What is the typical application timeline and key deadlines?"
      facet: WHEN
      priority: high
      searchability: high
      stability: seasonal
      dependencies: []
      status: pending

    - id: q3
      question: "What does the application require (forms, essays, assessments)?"
      facet: WHAT
      priority: high
      searchability: high
      stability: stable
      dependencies: [q1]
      status: pending

    # ... 20-40 total questions
```

---

## 4. Phase 2: Expand — Iterative Search Loop

### Core principle: Search-Read-Reason-Refine

Each search result shapes the next query. This is **not** a batch of parallel searches — it's a directed graph exploration.

### The Loop

```
for each question in priority order:
    1. SEARCH  — run 2-3 web queries with different angles
    2. READ    — fetch top results, extract to markdown
    3. REASON  — evaluate: did we answer the question? what's new?
    4. REFINE  — generate follow-up questions discovered from results
    5. DECIDE  — enough coverage? or search deeper?
```

### Concrete Example

**Round 1 — Seed question: "What are Bay Area private K schools?"**
<!-- how to you discover new queries -->
<!-- how to score the questions, so we can prioritize high value questions? -->
<!-- how to dedup questiosn, so we don't waste effort on questions already done research? -->

```
Search queries:
  - "Bay Area private elementary schools kindergarten list 2026"
  - "San Francisco private schools K entry"
  - "Peninsula Silicon Valley private kindergarten"

Results yield: ~30 school names, locations, types

New questions discovered:
  - "What is The Bay School vs. Bay School of SF?" (disambiguation)
  - "Which schools offer TK vs K?" (didn't know TK was relevant)
  - "What is BADA/BAIA and how do fairs work?" (discovered concept)
  → These get added to the question tree as children of q1
```

**Round 2 — "Application timeline and deadlines"**

```
Search queries:
  - "SF private school application deadline 2026-2027"
  - "Ravenna admissions platform Bay Area kindergarten"
  - site:sfschool.org admissions process

Results yield: Typical timeline Aug-Mar, Ravenna platform, school-specific dates

New questions discovered:
  - "What is Ravenna Hub?" (tool all schools use — needs its own article)
  - "Do all schools use the same deadline?" (no — need per-school data)
  - "What is the parent interview vs child assessment?" (process detail)
  → Added to tree
```

**Round 3 — Depth-first on a specific school (Cathedral School for Boys)**


```
Search queries:
  - site:cathedralschool.net admissions
  - "Cathedral School for Boys kindergarten admissions experience"

Results yield: Specific dates, boys-only, interview format, financial aid

Crosscheck:
  - Compare stated deadline with Ravenna listing
  - Compare tuition with other schools already researched
```

### Search Strategy: Breadth-First then Depth-First

<!-- why do we do depth first, not breadth first?, just curious, how would a typical researcher do this? reading survey or digging very deep into a topic first? -->

```
Phase 2a: BREADTH (landscape mapping)
  - Run through all high-priority seed questions
  - Goal: 80% topic coverage with shallow depth
  - Typical: 10-15 searches, 20-30 pages fetched
  - Output: rough school list, timeline, process overview

Phase 2b: DEPTH (per-entity deep dives)
  - For each major entity (school, process, concept):
    - Fetch official source (school website)
    - Fetch 1-2 third-party sources (reviews, parent forums)
    - Cross-reference for accuracy
  - Typical: 2-4 searches per entity, 30-60 pages total
  - Output: detailed per-school profiles, process guides

Phase 2c: GAP FILL (targeted)
  - Review what's missing from question tree
  - Search specifically for gaps
  - Typical: 5-10 targeted searches
```

### Adaptive Query Formulation

The agent doesn't just ask the literal question — it formulates **search-engine-optimized queries**:

| Research question | Bad query | Good queries |
|---|---|---|
| What is the application timeline? | "application timeline" | `"private school" admissions timeline 2026 San Francisco`, `site:ravenna-hub.com kindergarten` |
| How much does it cost? | "private school cost" | `"tuition" "2026-2027" kindergarten San Francisco private`, `"financial aid" private elementary Bay Area` |
| What do parents wish they knew? | "parent advice school" | `"private school" kindergarten "wish I had known" OR "advice for parents" site:reddit.com` |

### When to Stop Searching
<!-- how to determine source quality? -->

| Signal | Action |
|--------|--------|
| Last 3 searches returned no new concepts | Stop breadth phase |
| Diminishing returns on a specific entity | Move to next entity |
| Source quality is low (forums, SEO spam) | Stop and flag as `low-confidence` |
| Budget limit reached (configurable) | Stop, document gaps |
| Question tree has no pending high-priority items | Move to compilation |

---

## 5. Phase 3: Harvest & Verify

### Raw Data Organization

Every fetched page is saved to `raw/` with metadata:

```
raw/
├── web/
│   ├── 2026-04-06_sfschool-admissions.md
│   ├── 2026-04-06_cathedral-admissions.md
│   ├── 2026-04-06_ravenna-hub-overview.md
│   └── ...
└── research-plan.yaml   # Updated with status and discovered questions
```

Each raw file has frontmatter:

```yaml
---
url: https://sfschool.org/Admissions-Process
fetched: 2026-04-06
fetched_by: agent
query_context: "SF School kindergarten admissions process"
content_hash: sha256:abc123...
reliability: official  # official | journalistic | community | unknown
---
```

### Cross-Source Verification
<!-- how to extract claims for the factuality check? -->

Before compiling into wiki articles, the agent runs verification:

```
For each factual claim extracted:
  1. Count independent sources that support it
  2. Check for contradictions across sources
  3. Assign confidence:
     - 3+ official sources agree    → L1 confirmed
     - 2 sources agree              → L2 likely
     - 1 source only                → L3 single-source
     - Sources conflict             → L4 disputed
     - No verifiable source         → L5 unknown
```

**Example — Tuition verification:**

```
Claim: "SF School tuition is $38,500 for K"
  Source 1: sfschool.org (official) — $38,500 → ✓
  Source 2: niche.com — $37,200 → ✗ (outdated?)
  Source 3: privateschoolreview.com — $38,500 → ✓

  Resolution: L1 confirmed ($38,500), note that Niche may be stale
```

**Example — Acceptance rate conflict:**

```
Claim: "Cathedral acceptance rate is 25%"
  Source 1: blog post 2024 — "around 25%"
  Source 2: parent forum 2025 — "they say it's gotten harder, maybe 20%"
  Source 3: school website — no published rate

  Resolution: L4 disputed — create claims/ article, note schools
  rarely publish official rates
```

### Handling Hard-to-Verify Information

| Category | Strategy | Example |
|----------|----------|---------|
| **Subjective** (school culture, teaching quality) | Aggregate multiple perspectives, label as opinion | "Parents describe the culture as warm but academically rigorous" |
| **Unofficial** (acceptance rates, wait-list odds) | Present ranges, cite source type, flag as unverified | "Estimated 20-30% acceptance (parent forums, unverified)" |
| **Stale** (tuition, deadlines from prior years) | Use most recent official source, tag with `valid_until` | "Tuition $38,500 (2026-27, per school website)" |
| **Experiential** (what the playdate is like) | Aggregate parent reports, note variance | "Reports vary; some describe structured activities, others free play" |

---

## 6. Phase 4: Compile Wiki

### Article Generation Strategy

The agent doesn't create one article per search — it **synthesizes across all raw sources** into thematic articles:
<!-- remember we will have many topics, school application is just one of the topics. -->
```
wiki/
├── index.md                        # Master catalog
├── log.md                          # Operation history
├── overview.md                     # Executive summary for parents
│
├── guides/
│   ├── application-timeline.md     # Month-by-month guide
│   ├── application-checklist.md    # What you need to prepare
│   ├── choosing-a-school.md        # Decision framework
│   ├── financial-aid.md            # Aid, scholarships, payment plans
│   ├── assessment-day.md           # What to expect at playdates
│   └── common-mistakes.md          # What to avoid
│
├── schools/
│   ├── _index.md                   # School comparison table
│   ├── sf-school.md                # Per-school profile
│   ├── cathedral-school.md
│   ├── la-scuola.md
│   ├── friends-school.md
│   └── ...                         # 20-40 school profiles
│
├── concepts/
│   ├── ravenna-hub.md              # Admissions platform
│   ├── transitional-kindergarten.md
│   ├── progressive-vs-traditional.md
│   ├── montessori.md
│   ├── admissions-consultants.md
│   └── sibling-legacy-policy.md
│
└── claims/
    ├── acceptance-rates.md          # Disputed/unverified data
    └── tuition-trends.md            # Time-sensitive claims
```

### Per-School Article Template

```markdown
---
title: "The San Francisco School"
type: school-profile
updated: 2026-04-06
sources:
  - raw/web/2026-04-06_sfschool-admissions.md
  - raw/web/2026-04-06_sfschool-niche.md
epistemic_status: confirmed
confidence: L2
valid_until: 2027-03-31
---

# The San Francisco School

## Quick Facts
| | |
|---|---|
| Location | San Francisco (Portola) |
| Type | Progressive, independent |
| Grades | K-8 |
| Tuition (2026-27) | $38,500 |
| Application deadline | January 23, 2026 |
| Assessment date | March 4, 2026 |
| Decision date | March 19, 2026 |
| Financial aid | Available, need-based |

## Philosophy
[Synthesized from school website + parent reviews]

## Admissions Process
1. Submit application via [[ravenna-hub|Ravenna]] by Jan 23
2. Parent tour (scheduled via Ravenna)
3. K assessment afternoon — March 4
4. Decision posted March 19; response by March 25

## What Parents Say
[Aggregated from forums, reviews — labeled as anecdotal]

## See Also
- [[application-timeline]] — where this school fits in the overall calendar
- [[progressive-vs-traditional]] — this school's pedagogical approach
- [[financial-aid]] — aid application process
```

### Compilation Rules

1. **Merge, don't duplicate** — if two sources discuss the same concept, synthesize into one article
2. **Backlink aggressively** — every mention of a school/concept should be a `[[wikilink]]`
3. **Separate facts from opinions** — use labeled sections
4. **Time-stamp volatile data** — tuition, deadlines get `valid_until` fields
5. **Cite sources inline** — `(source: sfschool.org, Jan 2026)`
6. **Create comparison tables** — parents need to compare schools side-by-side

---

## 7. Phase 5: Lint & Evolve

### Lint Checks (Automated)

```yaml
structural:
  - broken_wikilinks: links that point to nonexistent articles
  - orphaned_pages: articles with no incoming links
  - missing_frontmatter: articles missing required fields
  - stale_data: articles past their valid_until date

content:
  - contradictions: same fact stated differently in different articles
  - missing_sources: claims without source attribution
  - single_source_claims: important facts with only one source
  - empty_sections: template sections never filled in

coverage:
  - schools_without_profiles: schools mentioned but no dedicated article
  - unanswered_questions: research-plan questions still pending
  - thin_articles: articles below minimum useful length
```

### Evolve (Agent-Driven Improvement)

After initial compilation, the agent can autonomously improve the wiki:

```
1. GAP ANALYSIS
   - Which questions from the research plan are unanswered?
   - Which schools have thin profiles?
   - Which concepts are mentioned but undefined?
   → Generate new targeted search queries

2. FRESHNESS CHECK
   - Any deadlines approaching or passed?
   - Any tuition figures from prior year?
   → Search for updates

3. CONNECTION DISCOVERY
   - Are there patterns across school profiles? (e.g., "all progressive schools
     have later deadlines")
   - Can we generate a comparison matrix?
   → Create synthesis articles

4. USER-DRIVEN EVOLUTION
   - Human asks: "What about bilingual programs?"
   → Agent searches, creates new concept article, cross-links to relevant schools
   → The question and answer are filed into the wiki permanently
```

---

## 8. Efficiency Strategies

### Minimize Redundant Work

| Strategy | How | Impact |
|----------|-----|--------|
| **Manifest tracking** | Content hash per source; skip unchanged | Prevents re-ingesting same page |
| **Query deduplication** | Track all queries run; skip near-duplicates | Saves API calls |
| **Index-first reasoning** | Read `index.md` before full articles | Faster query answering |
| **Batch backlink updates** | Update links after all articles compiled, not per-article | Fewer file writes |
| **Priority ordering** | High-value questions first | If interrupted, most important knowledge exists |

### Budget Management

```yaml
research_budget:
  max_web_searches: 50        # Total search API calls
  max_page_fetches: 100       # Total pages downloaded
  max_tokens_reasoning: 500K  # LLM tokens for synthesis

  allocation:
    breadth_phase: 30%        # Landscape mapping
    depth_phase: 50%          # Per-entity deep dives
    gap_fill: 15%             # Targeted fills
    verification: 5%          # Cross-checking
```

### Parallelization Opportunities

```
CAN parallelize:
  - Fetching multiple URLs (I/O bound)
  - Independent school profile searches (no dependency)
  - Lint checks across different articles

CANNOT parallelize:
  - Question decomposition (needs prior results)
  - Cross-reference generation (needs all articles)
  - Synthesis articles (needs entity articles first)
```

---

## 9. Quality Assurance Framework

### Source Reliability Hierarchy

```
L1 (highest): School's own website, official admissions page
L2: Verified news outlets (SFChronicle, local news)
L3: Established review platforms (Niche, GreatSchools)
L4: Parent forums, blogs, Reddit (aggregated, labeled as anecdotal)
L5 (lowest): SEO content farms, undated articles, AI-generated listicles
```

### Quality Gates

```
Before an article enters wiki/:

  Gate 1: SOURCE CHECK
    - Does every factual claim have a source?
    - Is at least one source L1 or L2?
    → If no: route to staging/

  Gate 2: FRESHNESS CHECK
    - Are all sources from current admissions cycle?
    - Are dates/tuition from 2026-2027?
    → If stale: flag, search for update

  Gate 3: CONSISTENCY CHECK
    - Does this article contradict any existing wiki article?
    - Are numerical values consistent with comparison tables?
    → If conflict: create claims/ article, flag for human review

  Gate 4: COMPLETENESS CHECK
    - Are all template sections filled?
    - Does the article have at least 2 backlinks?
    → If incomplete: fill or mark as stub
```

### Handling the "I Can't Verify This" Case

Some knowledge is inherently unverifiable but still valuable:

```markdown
## What the Assessment Day is Like

> **Epistemic note:** The following is synthesized from 12 parent accounts
> on Bay Area parent forums (2024-2026). Individual experiences vary.
> Schools do not publish assessment details. Treat as directional, not
> definitive.

Parents consistently report that K assessments involve:
- Small group play activities (8-10 children)
- One-on-one interaction with a teacher
- Duration: 60-90 minutes
- Parents wait in a separate area

*Sources: Urban Baby SF (3 posts), DC Urban Mom Bay Area (5 posts),
Reddit r/SFBayArea (4 posts)*
```

---

## 10. Incremental Growth Model

The wiki doesn't need to be built in one shot. The growth follows a **maturity curve**:

```
Week 1: SCAFFOLD
  - Research plan with 30 questions
  - 10 breadth searches
  - Overview article + timeline guide
  - 5 school profiles (most popular)
  - ~10 articles, ~15K words

Week 2: FILL
  - 15 more school profiles
  - Process guides (application, assessment, financial aid)
  - Key concepts (Ravenna, TK, school philosophies)
  - ~30 articles, ~50K words

Week 3: DEEPEN
  - Remaining school profiles
  - Comparison tables
  - Parent experience synthesis
  - ~50 articles, ~80K words

Week 4+: MAINTAIN
  - Lint passes catch stale data
  - New questions from user queries get filed
  - Deadline reminders surface automatically
  - ~60+ articles, ~100K+ words, compounding
```

### User-Driven Growth

At any point, the human can:

```
/query "Which schools have Spanish immersion?"
  → Agent searches wiki, finds gap
  → Searches web for bilingual/immersion programs
  → Creates wiki/concepts/language-immersion.md
  → Updates relevant school profiles with language info
  → Files answer in wiki — future queries benefit

/ingest [URL to a school fair recap blog post]
  → Agent extracts school names, impressions, tips
  → Updates existing school profiles with new data points
  → Creates raw/web/2026-04-06_school-fair-recap.md
```

---

## 11. Architecture Decision Records

### ADR-1: Markdown over Database

**Decision:** All knowledge stored as flat markdown files.
**Rationale:** At personal scale (<500 articles), LLM context window + index.md is sufficient for retrieval. Markdown is human-readable, version-controllable, and works with Obsidian.
**Trade-off:** No structured queries (SQL). Mitigated by comparison tables in markdown and SQLite FTS5 as optional add-on.

### ADR-2: Breadth-First then Depth-First Search

**Decision:** Map the landscape first, then go deep on entities.
**Rationale:** Avoids rabbit holes. If the agent goes deep on School A before knowing School B exists, it can't cross-reference effectively. Breadth-first ensures the index is populated before detail work begins.

### ADR-3: Staging Area for Agent-Sourced Content

**Decision:** Agent web research results go to `staging/` by default; human-curated sources go directly to `wiki/`.
**Rationale:** Agent web searches can hit low-quality sources or misinterpret content. The staging area provides a human review gate without blocking compilation.
**Override:** Auto-promote when agent source is an official school website (L1 reliability).

### ADR-4: Preserve Conflicts, Don't Resolve Silently

**Decision:** When sources disagree, create a `claims/` article documenting both positions rather than choosing one.
**Rationale:** Silent resolution destroys information. A parent reading "acceptance rate is 25%" doesn't know the agent discarded a "15%" figure from another source. Surfacing the conflict lets the human decide.

### ADR-5: Question Tree as First-Class Artifact

**Decision:** The research plan (question tree) is saved as a raw artifact and maintained throughout the research process.
**Rationale:** Makes the research process transparent and auditable. Enables incremental research — stop and resume at any question. Reveals coverage gaps automatically.

---

## 12. Example End-to-End Run

```
USER: "Build me a knowledge base about applying to Bay Area private K schools"

AGENT:
  1. Generates research plan with 35 questions across 8 facets
     → Saves raw/research-plan.yaml

  2. BREADTH PHASE (10 searches, 25 pages fetched)
     → Identifies 35 schools, discovers Ravenna, TK, key dates
     → Saves 25 raw files to raw/web/

  3. DEPTH PHASE (30 searches, 60 pages fetched)
     → Builds 20 school profiles from official websites
     → Writes process guides from synthesizing across sources
     → Saves 60 raw files

  4. GAP FILL (8 searches, 15 pages fetched)
     → Financial aid details, parent experiences, consultant info
     → Saves 15 raw files

  5. COMPILE
     → Generates 45 wiki articles with 120+ backlinks
     → Creates comparison tables, timeline visualization
     → 3 articles routed to staging/ (low-confidence claims)

  6. LINT
     → Finds 2 broken links, 1 contradiction (tuition figure),
       4 schools mentioned without profiles
     → Generates lint report

  TOTAL: 48 searches, 100 pages, ~45 wiki articles, ~75K words
  TIME: ~30-45 minutes of agent work
  COST: ~$5-10 in API calls (search + LLM tokens)
```

---

## References

- [Deep Research for AI Agents (Firecrawl)](https://www.firecrawl.dev/blog/deep-research-for-ai-agents)
- [Deep Research: A Survey of Autonomous Research Agents](https://arxiv.org/html/2508.12752v1)
- [Multi-Agent Frameworks for Deep Research](https://medium.com/@karanbhutani477/multi-agent-frameworks-for-llm-powered-deep-research-systems-abf30d32fa29)
- [Karpathy's LLM Knowledge Bases gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [DAIR.AI — LLM Knowledge Bases](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)
