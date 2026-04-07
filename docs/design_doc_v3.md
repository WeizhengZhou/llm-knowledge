# LLM Knowledge Base: Design Document v3

**Supersedes:** `docs/v3_improvements.md` (retrospective observations), builds on `docs/design_doc_v2.md` (pipeline fixes)
**Date:** 2026-04-06
**Focus:** Strategy, eval system, and source diversity — generalizing the system beyond a single topic

---

## Motivation

v2 addressed tactical pipeline issues (YAML appendability, token caps, budget scaling). This document addresses three strategic questions:

1. **How to research any topic comprehensively, accurately, and with high helpfulness** — not just factual reference topics but judgment-intensive ones
2. **How to evaluate wiki quality** across multiple dimensions with a reproducible eval system
3. **What source types are missing** and how to ingest them (books, UGC, video, audio, academic papers)

---

## 1. Strategy: Generalizing to Any Topic

### 1.1 The Core Strategic Gap

The system is optimized for *factual reference* topics but lacks patterns for *judgment-intensive* topics.

The private-school topic is a hybrid: it has factual data (deadlines, tuition) but the real value is judgment (which school fits my kid). The pipeline handles the factual half well. It structurally cannot produce the judgment half because of three root causes:

### 1.2 Persona-Driven Research Framing

**Problem:** The research planner generates questions from facets (WHO/WHAT/WHEN/WHERE/HOW/WHY/COMPARE/META) without considering who is reading or what decision they're making.

**Fix:** `_topic.yaml` gains two new first-class fields:

```yaml
reader_personas:
  - id: P1
    label: "First-time SF parent, high income, no network"
    needs: [school-list, timeline, assessment-prep]
    does_not_need: [financial-aid-deep-dive]
  - id: P2
    label: "Relocating family from East Coast"
    needs: [how-sf-differs, geography, timeline-compressed]
  - id: P3
    label: "Middle-income family, aid-dependent"
    needs: [financial-aid, public-vs-private, cost-of-attendance]

reader_outcomes:
  - id: RO1
    job: "Determine if my child is age-eligible before investing time"
    must_answer: ["age cutoff by school", "how cutoffs vary", "what to do if borderline"]
    personas: [P1, P2, P3]
  - id: RO2
    job: "Build a school list of 6-10 schools to actually apply to"
    must_answer: ["what differentiates schools", "geography", "philosophy fit", "selectivity"]
    personas: [P1, P2]
  - id: RO3
    job: "Never miss a deadline"
    must_answer: ["full deadline calendar", "sibling priority exceptions", "aid separate deadlines"]
    personas: [P1, P2, P3]
  - id: RO4
    job: "Understand what the process will cost and whether aid is realistic"
    must_answer: ["tuition range by school", "aid participation rates", "income thresholds", "test cost"]
    personas: [P3]
  - id: RO5
    job: "Prepare my child and myself for the assessment"
    must_answer: ["what playdates evaluate", "parent interview questions", "how to prepare without coaching"]
    personas: [P1, P2]
  - id: RO6
    job: "Navigate decisions and waitlists in March"
    must_answer: ["single-contract rule", "waitlist movement timing", "how to hold multiple offers"]
    personas: [P1, P2, P3]
```

The research planner generates questions *per persona x per outcome*, not just per facet. Different personas need different articles — a $400k HHI family doesn't need the financial aid guide; a family relocating from NYC needs the "how SF differs" guide.

### 1.3 Source Type Diversity Strategy

**Problem:** Currently: WebSearch -> WebFetch -> done. This produces a monoculture of official websites + news articles.

**Fix:** For any topic to be comprehensive, the research planner must plan which source tiers to hit for each question cluster.

| Source Tier | What It Provides | Current Coverage | Access Method |
|---|---|---|---|
| Official/primary (L1-L2) | Facts, dates, policies | Strong | WebSearch + WebFetch |
| Aggregator/review (L3) | Comparative data, ratings | Light | WebSearch (Niche, GreatSchools) |
| Expert synthesis (L2-L3) | Frameworks, strategy | Partial | Consultant blogs, journalist longform |
| Community/UGC (L4) | Pain points, lived experience | Almost absent | Reddit, forums, Facebook groups |
| Books/longform (L2) | Deep frameworks, historical context | Absent | Manual ingest + secondary sources |
| Video/audio (L2-L4) | Interviews, expert talks, vlogs | Absent | YouTube transcripts, podcast transcripts |
| Academic/research (L1-L2) | Evidence, studies, data | Absent | Google Scholar, ERIC, NBER |
| Government/regulatory (L1) | Policies, statistics, compliance | Absent | .gov sites, NCES, CDE |

The research-planner should explicitly annotate each question cluster with target source tiers, not just generate questions and hope WebSearch covers it.

### 1.4 Phase 0: Landscape Scan

**Problem:** The research planner generates questions from the LLM's training data, not from what real people actually need. The v3_improvements doc identified UGC mining as a pre-step; this formalizes it.

**Fix:** Before the question tree, run a **Landscape Scan** phase:

```
Phase 0: Landscape Scan (new)
├── 1. Search Reddit/forums for the topic → extract real human questions
├── 2. Search "best books about X" / "recommended resources for X"
├── 3. Search for YouTube channels / podcasts covering the topic
├── 4. Identify the expert ecosystem (consultants, journalists, researchers)
└── 5. Output landscape.yaml
```

Output schema:

```yaml
# landscape.yaml
entities_discovered:
  - name: "SF School"
    type: school
    mentions: 14
  - name: "Testing Mom (book)"
    type: book
    mentions: 7

source_ecosystem:
  reddit_threads:
    - url: "https://reddit.com/r/SFparents/..."
      relevance: high
      pain_points: ["deadline confusion", "playdate anxiety"]
  youtube_channels:
    - name: "Bay Area School Guide"
      subscriber_count: 12000
      relevant_videos: 8
  podcasts:
    - name: "Private School Insider"
      episodes_relevant: 3
  books:
    - title: "Testing Mom"
      author: "..."
      secondary_sources: ["NYT review", "author interview on YouTube"]
  experts:
    - name: "Cardinal Education"
      type: consultant
      blog_url: "..."

common_pain_points:
  - "Which schools can my August-birthday kid apply to?"
  - "Is private school worth $50k/year?"
  - "What do they actually evaluate at playdates?"
  - "How do I prepare without over-coaching?"

preliminary_question_seeds:
  - text: "What do schools actually evaluate during playdates?"
    source: reddit (12 threads)
    urgency: high
```

This landscape scan feeds the research planner. The question tree becomes grounded in real human needs, not LLM imagination.

---

## 2. Design: Missing Architectural Components

### 2.1 Multi-Modal Source Ingestion Pipeline

The system needs a proper ingestion layer that normalizes diverse source types into the existing `raw/` directory structure:

```
Source Types    → Extractors              → Normalized raw/     → Existing Pipeline
──────────────────────────────────────────────────────────────────────────────────
Web pages       → WebFetch                → raw/web/            ✓ exists
Books           → manual notes            → raw/manual/         ◐ described, no tooling
YouTube         → transcript API          → raw/video/          ✗ missing
Podcasts        → transcript API/Whisper  → raw/audio/          ✗ missing
Reddit/forums   → structured fetch        → raw/community/      ✗ missing
Academic papers → PDF extract             → raw/academic/       ✗ missing
Gov data        → structured fetch        → raw/government/     ✗ missing
Local files     → /kb-ingest --file       → raw/manual/         ✓ exists
```

#### YouTube Transcript Ingestion

Highest-ROI new source type. For almost any topic, there are expert interviews, conference talks, and vlogs.

**Implementation:**
- Use YouTube Data API v3 for search
- Use `youtube-transcript-api` Python package for transcript extraction
- Output timestamped markdown to `raw/video/`
- Reliability tier: L2 for expert interviews, L4 for vlogs

**What it unlocks:**
- Author interviews about books (solves the copyright problem — 70% of a book's value is in the author's 45-minute podcast appearance)
- Expert talks and panels
- Parent vlogs about their experience (L4, but rich)
- School virtual tours and recorded info sessions

#### Reddit Structured Extraction

Don't rely on `site:reddit.com` WebSearch (unreliable). Build a structured tool.

**Implementation:**
- Fetch specific threads via Reddit JSON API (`{url}.json`)
- Extract top-level comments with score > 5
- Preserve comment scores as a quality signal
- Output structured markdown to `raw/community/`
- Reliability tier: always L4 (community source)

**What it unlocks:**
- Systematic UGC mining for Phase 0 landscape scan
- Real parent pain points as question seeds
- Community patterns that can inform wiki synthesis (without citation)

#### Podcast Transcript Ingestion

**Implementation:**
- Use Listen Notes API for podcast search/discovery
- Fetch transcripts from Podscribe or similar services
- Fallback: fetch audio + Whisper for transcription
- Output to `raw/audio/`

#### Academic Paper Ingestion

**Implementation:**
- Use Semantic Scholar API (free, structured, returns abstracts + citation counts)
- For full papers: fetch PDF, extract abstract + key findings + methodology summary
- Not every topic needs this — the research planner decides
- Output to `raw/academic/`

#### Book Secondary Source Strategy

For any book identified as relevant during landscape scan, systematically fetch:

1. Goodreads/Amazon top reviews (reader summaries of key ideas)
2. Author interviews on YouTube (transcript extraction)
3. Longform book reviews (NYT, Atlantic, domain-specific publications)
4. Author blog posts, talks, op-eds
5. Blinkist/getAbstract summaries (paraphrase, don't copy)

This gets ~70% of a book's value without reading it. For the remaining 30%, the user writes `raw/manual/{book-slug}-notes.md` with their own synthesis.

**Structured notes format for manual book ingestion:**

```yaml
---
source_type: book_notes
title: "Testing Mom — Key Insights"
book: "Testing Mom"
author: "[author name]"
notes_by: "[user]"
date: 2026-04-06
reliability_tier: L2  # user's interpretation of an authoritative source
---

## Key Argument
[In user's own words — not copyrightable]

## What Schools Actually Evaluate at Playdates
[User's synthesis — not verbatim]

## Surprising Findings
- "[Short direct quote, <50 words]" (p. 47)  # fair use
```

### 2.2 Claim Lifecycle Management

**Problem:** Claims are extracted once and verified once. For a living wiki, claims need a full lifecycle.

**Current state:** The `volatile` class system (annual/cycle_bound/evergreen/none) exists but is passive — it waits for `/kb-update`.

**Target state:**

```
discovered → extracted → verified → published → monitored → re-verified | expired
```

**New fields per claim:**

```yaml
- id: C042
  text: "SF School tuition is $48,577"
  confidence: L1
  volatile: annual
  last_verified: 2026-04-06
  next_verify_by: 2026-09-01   # auto-calculated from volatile class
  source_url: "https://sfschool.org/tuition"
  monitor: true                  # flag for URL change detection
```

**New behaviors:**
- `last_verified` tracked per claim, not just per pipeline run
- Auto-flag claims approaching their volatility window (lint-agent checks `next_verify_by < today + 30d`)
- Claim subscriptions: for `monitor: true` claims, periodically re-fetch `source_url` and compare content hash

### 2.3 Helpfulness Eval Agent (New Agent)

Formalized from the idea in v3_improvements. This is a full agent, not a lint check.

```
helpfulness-eval-agent
───────────────────────
Inputs:
  - wiki/ directory (all articles)
  - reader_outcomes from _topic.yaml
  - eval/test-questions.yaml (fixed test suite)
  - reader_personas from _topic.yaml

Outputs:
  - eval/eval-report.yaml (per-RO scores, per-persona coverage, gap list)
  - eval/eval-history.jsonl (append-only, tracks scores over pipeline runs)

Position in pipeline:
  ... → lint-agent (structural) → helpfulness-eval-agent (quality) → evolve-agent (planning)

Tools: Read, Glob, Grep, Write
```

This creates the missing feedback loop. Currently: research → compile → lint → evolve, and the evolve agent guesses at helpfulness gaps. With the eval agent: research → compile → lint → **eval** → evolve, and evolve gets a scored gap list to work from.

### 2.4 L4 as Synthesis, Not Citation

**Problem:** Community sources (Reddit, forums) are either discarded entirely or improperly cited. The current L4 rules say "Anecdote only" but the wiki-compiler defaults to just dropping L4 claims.

**Fix:** L4 sources feed **synthesis patterns**, not attributable claims.

The wiki can say:
> "Parents commonly describe the Hamlin interview as focused on family values rather than the child's performance."

Without citing a Reddit thread. The wiki-compiler annotates with `(community pattern, multiple reports)` — hedged but present.

**Implementation rule for wiki-compiler-agent:**
- If 3+ independent L4 sources report the same pattern → synthesize as "parents commonly report..."
- If only 1 L4 source → do not include
- Never cite the specific forum/thread
- Always pair with whatever official source exists (even if it says nothing)

### 2.5 Cross-Topic Knowledge Graph

The `shared/` directory exists but nothing populates it. As the system accumulates topics, entities will overlap (e.g., "Bay Area geography" for schools, restaurants, housing).

**Deferred.** Not critical for single-topic quality. Becomes important when 3+ topics exist. The cross-linker tool needs to actually work first (see v2 §cross-linker issues).

---

## 3. Eval System Design

### 3.1 Three-Layer Eval Architecture

```
Layer 1: Structural (automatable, runs every pipeline)
  → lint-agent already handles most of this
  → Additions: stub ratio, entity completeness %, backlink coverage

Layer 2: Content Quality (LLM-as-judge, runs after compile)
  → helpfulness-eval-agent (new)
  → Scores D1 (reader outcomes), D4 (actionability), D5 (perspective balance)
  → Uses a fixed test question suite per topic

Layer 3: End-to-End Task Completion (LLM-as-judge, runs on demand)
  → "Red team" evaluation: LLM gets a persona + task + only the wiki
  → Can the LLM complete the task? What did it have to fabricate?
  → Gold standard but expensive — run on major milestones, not every pipeline
```

### 3.2 Test Question Suite

The single most important eval artifact. Built once per topic from real human questions (Reddit, forums), reused across pipeline runs.

**Schema: `eval/test-questions.yaml`**

```yaml
metadata:
  topic: bay-area-private-school-k-application
  version: 1
  created: 2026-04-06
  question_count: 30
  sources: [reddit, parent_forums, consultant_blogs]

questions:
  - id: TQ01
    text: "My daughter was born September 10, 2020. Which SF schools can she apply to for fall 2026 K?"
    source: reddit
    reader_outcome: RO1
    difficulty: easy        # answer is directly in one article
    expected_coverage: full # wiki should fully answer this

  - id: TQ02
    text: "We earn $180k HHI. Is financial aid realistic at SF Day School?"
    source: parent_forum
    reader_outcome: RO4
    difficulty: hard        # requires synthesis across multiple articles
    expected_coverage: full

  - id: TQ03
    text: "What should I tell my 4-year-old before his Live Oak playdate?"
    source: reddit
    reader_outcome: RO5
    difficulty: medium
    expected_coverage: full # currently: none

  - id: TQ04
    text: "Should I apply to both SFUSD and private, or just private?"
    source: reddit
    reader_outcome: RO2
    difficulty: hard
    expected_coverage: full # currently: not addressed

  - id: TQ05
    text: "Live Oak waitlisted us. What should we do now and when does movement happen?"
    source: parent_forum
    reader_outcome: RO6
    difficulty: medium
    expected_coverage: full
```

**Scoring per question:**

| Score | Definition |
|---|---|
| 0 | Not answerable from wiki — LLM must fabricate or say "I don't know" |
| 1 | Partially answerable — some info present, key details missing |
| 2 | Fully answerable from wiki alone |

**Target: 80%+ of questions score 2.** Track this metric across pipeline runs as the primary quality signal.

### 3.3 Evaluation Rubric (D1-D6)

#### Scoring Scale

- **3** — Fully meets the bar
- **2** — Partially meets, meaningful gaps
- **1** — Addressed but insufficient
- **0** — Not addressed

#### Dimension Weights

| Dimension | Weight | Rationale |
|---|---|---|
| D1 Reader Outcome Enablement | 30% | The core purpose — can the reader make decisions? |
| D2 Coverage Completeness | 20% | Are the right topics present? |
| D3 Accuracy & Epistemic Integrity | 20% | Wrong info is worse than no info |
| D4 Actionability | 15% | Information vs. decision-support framing |
| D5 Perspective Balance | 10% | Official only vs. lived experience included |
| D6 Navigability & Structure | 5% | Hygiene |

---

#### D1: Reader Outcome Enablement (30%)

**Method:** LLM judgment. For each `reader_outcome` in `_topic.yaml`, score independently using the test question suite (5 questions per RO).

| Score | Criteria |
|---|---|
| 3 | Reader can make this decision from the wiki alone. No open questions. No Google needed. |
| 2 | Wiki substantially helps but >= 1 `must_answer` item is missing or answered only partially |
| 1 | Wiki mentions the topic but doesn't enable the decision |
| 0 | RO not addressed at all |

---

#### D2: Coverage Completeness (20%)

**Mix of automatable and LLM judgment.**

**2a. Topic coverage** (LLM judgment)

| Score | Criteria |
|---|---|
| 3 | All major decision categories have >= 1 article; no standalone decision left uncovered |
| 2 | 1-2 major decision categories missing (e.g., "public vs. private" absent) |
| 1 | Core categories present but significant gaps within each |
| 0 | Major portions of the topic not addressed |

**2b. Entity coverage** (automatable)

```
score = (entities with complete data / total entities in scope)
complete = no more than 2 "--" cells in comparison table
```

**2c. Stub ratio** (automatable)

| Score | Stub % of Total Articles |
|---|---|
| 3 | < 10% |
| 2 | 10-25% |
| 1 | 25-40% |
| 0 | > 40% |

---

#### D3: Accuracy & Epistemic Integrity (20%)

**Mix of automatable and LLM judgment.**

**3a. Attribution compliance** (automatable)

Sample 20 random claim sentences. Count those with "According to X" or epistemic hedge. Target >= 90%.

**3b. Confidence level discipline** (automatable)

| Score | Criteria |
|---|---|
| 3 | 0 L5 claims in wiki; all L4 sources flagged with epistemic note block |
| 2 | 0 L5 claims; some L4 sources cited without epistemic note |
| 1 | Community sources treated as fact in >= 1 article |
| 0 | L5 claims present in wiki |

**3c. Conflict documentation** (LLM judgment)

| Score | Criteria |
|---|---|
| 3 | All source conflicts identified and documented |
| 2 | Most conflicts documented; minor ones may be missed |
| 1 | Some conflicts resolved by picking one source without flagging |
| 0 | Conflicts not tracked |

**3d. Permitted language compliance** (LLM judgment)

Does wiki text match fact-sheet permitted language for verified claims? Spot-check 10 claims.

---

#### D4: Actionability (15%)

**LLM judgment. Most important qualitative dimension.**

**4a. Decision framing** (per article)

| Score | Criteria |
|---|---|
| 3 | Article tells reader what to do, not just what to know. Imperative voice in key sections. |
| 2 | Information present but framed passively — reader must translate to action themselves |
| 1 | Pure reference material with no action guidance |
| 0 | Content would confuse rather than help |

**4b. Common mistakes quality**

| Score | Criteria |
|---|---|
| 3 | Mistakes are non-obvious and specific (e.g., "SF Day has December deadline, not January") |
| 2 | Mistakes are real but generic ("start early," "apply to multiple schools") |
| 1 | No common mistakes section |

**4c. "Start here" clarity**

| Score | Criteria |
|---|---|
| 3 | A confused reader landing on any article knows what to read first and in what order |
| 2 | Overview article exists but navigation path isn't obvious from individual articles |
| 1 | No clear entry point |

---

#### D5: Perspective Balance (10%)

**LLM judgment.**

| Score | Criteria |
|---|---|
| 3 | Official + aggregator + community patterns + expert synthesis all represented |
| 2 | Official + aggregator present; community patterns absent or discarded |
| 1 | Primarily official sources only |
| 0 | Single source type |

Sub-dimensions to check:

| Perspective Type | Present? |
|---|---|
| Official school sources (L1-L2) | Check |
| Aggregator/review (L3) | Check |
| Community/parent experience (L4) | Check |
| Expert synthesis (consultants, journalists) | Check |
| Counterarguments ("here's why NOT to do X") | Check |

---

#### D6: Navigability & Structure (5%)

**Mostly automatable.**

| Check | Scoring |
|---|---|
| Broken wikilinks | 3 = 0 broken, 2 = 1-3, 1 = 4-10, 0 = >10 |
| Orphaned articles | 3 = 0 orphans, 2 = 1-2, 1 = 3-5, 0 = >5 |
| Backlinks populated | 3 = all populated, 0 = all empty |
| Index article count accurate | 3 = matches, 2 = off by 1-2, 0 = off by >2 |
| See Also sections present | 3 = all articles, 2 = >80%, 1 = 50-80%, 0 = <50% |

---

### 3.4 Additional Eval Dimensions (Beyond D1-D6)

These are tracked as standalone metrics, not part of the weighted composite:

**Freshness score** (automatable): What % of claims have `last_verified` within their volatility window? A wiki with 60% stale claims is dangerous.

**Contradiction detection** (LLM-as-judge): Do any two articles in the same wiki make conflicting claims? The fact-checker catches source-level conflicts, but the wiki compiler might introduce cross-article contradictions.

**Information density** (automatable): Words per actionable claim. If an article is 2000 words but only contains 5 actionable facts, it's padded. Target: high density, minimal fluff.

**Comparative completeness** (automatable for entity topics): If you have N entity articles, what % of comparison table cells are filled? A table with 40% `--` cells fails its purpose.

### 3.5 Eval Pipeline Integration

```
Pipeline Position:
  ... → wiki-compiler → lint-agent → helpfulness-eval-agent → evolve-agent → ...

Eval Outputs:
  eval/test-questions.yaml     # fixed per topic, built during Phase 0
  eval/eval-report.yaml        # latest eval results
  eval/eval-history.jsonl      # append-only, one record per pipeline run

Eval Report Schema:
  run_id: "2026-04-06-full"
  composite_score: 59
  dimensions:
    D1: { score: 1.8, max: 3, gaps: ["RO5 not addressed", "RO2 missing selectivity"] }
    D2: { score: 1.0, max: 3, gaps: ["public-vs-private absent", "5/11 entities incomplete"] }
    ...
  test_question_pass_rate: 14/30
  freshness: 0.87
  contradiction_count: 0
  information_density: 12.3  # claims per 1000 words
```

The evolve-agent reads this eval report and prioritizes its gap-fill recommendations by dimension impact — fixing D1 and D2 (50% weight, currently ~32/50) yields more than polishing D3 (already 2.3/3).

---

## 4. Missing Source Types: Detailed Recommendations

### 4.1 Highest ROI (implement first)

#### YouTube Transcripts

**Why:** Covers book author interviews, expert talks, school info sessions. For almost any topic, expert knowledge exists on YouTube.

**Implementation:**
- YouTube Data API v3 for search (`search?q={topic}&type=video`)
- `youtube-transcript-api` Python package for transcript extraction
- Output timestamped markdown to `raw/video/`
- Reliability tier: L2 for expert interviews/talks, L4 for vlogs

**What it unlocks:**
- Author interviews about books (solves the copyright problem — 70% of a book's value is in the author's 45-minute podcast appearance)
- Expert talks, panels, and conference presentations
- Parent/user vlogs about their experience (L4, but experientially rich)
- School virtual tours and recorded info sessions

**Output format:**

```markdown
---
source_type: youtube_transcript
video_id: "dQw4w9WgXcQ"
title: "Testing Mom Author Interview — What Schools Really Evaluate"
channel: "Bay Area School Guide"
published: 2025-11-15
duration_minutes: 47
reliability_tier: L2
fetched: 2026-04-06
---

[00:00] Introduction and author background
[02:15] "The biggest misconception parents have is that playdates are testing the child..."
[05:30] Discussion of what admissions directors actually look for
...
```

#### Reddit Structured Extraction

**Why:** `site:reddit.com` WebSearch is unreliable. Structured extraction provides systematic UGC mining.

**Implementation:**
- Fetch specific threads via Reddit JSON API (`{url}.json`)
- Extract top-level comments with score > 5
- Preserve comment scores as quality signal
- Output structured markdown to `raw/community/`
- Reliability tier: always L4

**Output format:**

```markdown
---
source_type: reddit_thread
subreddit: SFparents
thread_url: "https://reddit.com/r/SFparents/..."
title: "Private school K application advice?"
score: 47
comment_count: 83
date: 2025-10-22
reliability_tier: L4
fetched: 2026-04-06
---

## Top Comments (score > 5)

### Comment by [deleted] (score: 34)
"We applied to 8 schools and got into 2. The playdate at Live Oak was
the most relaxed — they just let the kids play while observing..."

### Comment by user123 (score: 22)
"Don't bother with the first-choice letter at Hamlin, it doesn't affect
the decision. Focus your energy on the parent essay instead..."
```

#### Podcast Transcripts

**Why:** Many topics have dedicated podcasts with expert interviews. Especially valuable for niche/professional topics.

**Implementation:**
- Listen Notes API for podcast search/discovery
- Fetch transcripts from Podscribe or similar services
- Fallback: fetch audio + Whisper for transcription
- Output to `raw/audio/`
- Reliability tier: L2 for expert interviews, L3-L4 for casual discussion

### 4.2 Medium ROI (implement for specific topic types)

#### Academic Papers (Google Scholar / Semantic Scholar)

**When needed:** Health topics, education outcomes, policy analysis, anything with a research literature.

**Implementation:**
- Semantic Scholar API (free, structured, returns abstracts + citation counts)
- For key papers: fetch PDF, extract abstract + key findings + methodology summary
- The research planner decides per-topic whether academic sources are needed
- Output to `raw/academic/`
- Reliability tier: L1 for peer-reviewed, L2 for preprints

#### Government Data Sources

**When needed:** Topics involving policy, demographics, regulation, or public institutions.

**Key sources:**
- NCES (National Center for Education Statistics) — school-level data
- CDE (California Department of Education) — state-level school data
- Census Bureau — demographic and income data
- Local government open data portals

**Implementation:**
- Structured API calls where available
- WebFetch + table extraction for HTML-based data
- Output to `raw/government/`
- Reliability tier: L1

#### Book Secondary Source Strategy

**When needed:** For any book identified as relevant during landscape scan.

**Systematic fetch order:**

1. Goodreads/Amazon top reviews (reader summaries of key ideas)
2. Author interviews on YouTube (transcript extraction — see §4.1)
3. Longform book reviews (NYT, Atlantic, domain-specific publications)
4. Author blog posts, talks, op-eds
5. Summary services (paraphrase only, never copy)

This gets ~70% of a book's value without reading it. For the remaining 30%, the user writes `raw/manual/{book-slug}-notes.md` with their own synthesis.

### 4.3 Lower ROI (valuable for specific topics)

#### Wayback Machine / archive.org

**When needed:** Historical data, tracking policy changes over time, recovering deleted pages.

**Implementation:** Wayback Machine API (`web.archive.org/web/...`). Useful for seeing how school admissions pages changed year-over-year.

#### Social Media Beyond Reddit

**Challenge:** Facebook groups are hard to scrape (closed groups, TOS). Twitter/X threads are ephemeral. Nextdoor is hyper-local.

**Practical approach:** Manual screenshots → OCR → `raw/manual/`. Not worth automating unless the topic demands it.

#### Local News Archives

**When needed:** Topics with significant local press coverage.

**Key sources for Bay Area:** SF Chronicle, SF Standard, Palo Alto Weekly, Mercury News, The Oaklandside.

**Implementation:** WebSearch with `site:` filtering → WebFetch. Already possible with current tools, just needs explicit planning by research-planner.

---

## 5. Updated Pipeline Flow

Incorporating all changes from this document:

```
Phase 0: Landscape Scan (NEW)
  └── research-planner-agent: UGC mining + source ecosystem mapping
        → outputs: landscape.yaml

Phase 1: Research Planning
  └── research-planner-agent: persona × outcome question tree
        → inputs: _topic.yaml (with personas + outcomes), landscape.yaml
        → outputs: research-plan.yaml (with source tier annotations, round/cycle metadata)

Phase 2: Research Execution (breadth → checkpoint → depth → gap-fill)
  └── research-agent: multi-source ingestion
        → inputs: research-plan.yaml, source tier targets
        → tools: WebSearch, WebFetch, youtube-transcript, reddit-fetch, scholar-fetch
        → outputs: raw/{web,video,community,academic,manual}/

Phase 3: Claim Extraction
  └── claim-extractor-agent (unchanged, but processes new source types)
        → outputs: claims-register.jsonl (JSONL, not YAML — per v2)

Phase 4: Fact Checking
  └── fact-checker-agent (unchanged)
        → outputs: fact-sheet.jsonl

Phase 5: Wiki Compilation
  └── wiki-compiler-agent (updated: L4 synthesis rules, persona-aware articles)
        → outputs: wiki/**/*.md

Phase 6: Structural Lint
  └── lint-agent (updated: RO coverage check, directory placement check)
        → outputs: output/lint-report.md

Phase 7: Helpfulness Eval (NEW)
  └── helpfulness-eval-agent: test question suite + rubric scoring
        → inputs: wiki/, eval/test-questions.yaml, _topic.yaml
        → outputs: eval/eval-report.yaml, eval/eval-history.jsonl

Phase 8: Evolution Planning
  └── evolve-agent (updated: reads eval report for prioritized gap-filling)
        → outputs: evolution-suggestions.md, research-plan.yaml (new questions)
```

---

## 6. Implementation Priority

Ranked by impact on "research any topic comprehensively and helpfully":

| Priority | Change | Impact | Effort |
|---|---|---|---|
| 1 | Phase 0 landscape scan | Makes question tree reality-grounded, not LLM-imagined | Medium |
| 2 | Reader outcomes + personas as first-class driver | Reorients everything from "comprehensive" to "helpful" | Medium |
| 3 | Test question suite + helpfulness-eval-agent | Gives measurable quality signal; enables iteration | Medium |
| 4 | YouTube transcript ingestion | Single highest-ROI new source type | Low |
| 5 | Reddit structured extraction | Unlocks UGC as systematic input, not afterthought | Low |
| 6 | Source diversity planning in research-planner | Ensures deliberate coverage across tiers | Low |
| 7 | L4-as-synthesis pattern in wiki-compiler | Lets community knowledge inform wiki without citing forums | Low |
| 8 | Claim lifecycle management | Makes the wiki a living document, not a snapshot | Medium |
| 9 | Podcast transcript ingestion | Second-tier source type, high value for some topics | Low |
| 10 | Academic paper ingestion | Essential for research-backed topics | Medium |

**Key insight from the eval rubric:** D1 (reader outcomes) and D2 (coverage) together account for 50% of the score but currently deliver only ~32/50. Fixing these two dimensions would push the wiki from 59 → 78. Improving D3 (accuracy, already 2.3/3) only adds ~5 points. **Invest in helpfulness, not more accuracy.**

---

## 7. Resource Efficiency

### 7.1 The Cost Problem

The current pipeline is expensive. A single full `/kb-research` run on the private-school topic consumed:

- **8 sequential agent invocations** — each agent reads extensive context (raw files, YAML state, wiki articles) into its window
- **35+ raw source files** loaded by the wiki-compiler in a single context
- **171 claims** processed through extraction and verification
- **60+ minutes wall time** with no parallelism

The cost scales linearly (or worse) with topic complexity. Adding more source types (YouTube, Reddit, academic) multiplies raw files and claims. Without efficiency improvements, a comprehensive topic could cost 5-10x the current run.

### 7.2 Model Tiering: Right Model for the Right Task

Not every agent needs the most capable (and expensive) model. Tasks vary in reasoning complexity:

| Agent | Reasoning Required | Recommended Model | Current |
|---|---|---|---|
| research-planner | High — strategy, prioritization, persona modeling | Opus | Opus |
| research-agent | Low — execute searches, fetch pages, save files | Haiku | Opus |
| claim-extractor | Medium — structured extraction from text | Sonnet | Opus |
| fact-checker | High — cross-reference sources, assess reliability | Opus | Opus |
| wiki-compiler | High — synthesis, tone, structure, judgment | Opus | Opus |
| lint-agent | Low — pattern matching, structural checks | Haiku | Opus |
| helpfulness-eval | High — LLM-as-judge, nuanced scoring | Opus | N/A |
| evolve-agent | Medium — gap analysis, recommendation | Sonnet | Opus |

**Estimated cost reduction: 40-50%** by routing research-agent and lint-agent to Haiku, claim-extractor and evolve-agent to Sonnet. The quality-critical agents (planner, fact-checker, compiler, eval) stay on Opus.

**Implementation:** Agent definitions already support a `model` field. Skills pass the model override when spawning agents:

```yaml
# .claude/agents/research-agent.md frontmatter
model: haiku

# .claude/agents/lint-agent.md frontmatter
model: haiku

# .claude/agents/claim-extractor-agent.md frontmatter
model: sonnet
```

### 7.3 Context Window Management

The biggest hidden cost: agents load far more context than they need.

**Problem 1: Wiki-compiler reads all raw files.** 35 raw files at 2-5K tokens each = 70-175K tokens of context, much of it irrelevant to the specific article being written.

**Fix: Entity-scoped compilation.** Instead of one compiler invocation with all files, the skill spawns N parallel compiler invocations, each scoped to one entity or article:

```
Current (1 expensive invocation):
  wiki-compiler reads: all 35 raw files + fact-sheet + research-plan
  → writes: all wiki articles

Better (N cheap invocations):
  wiki-compiler[sf-school] reads: 3 relevant raw files + sf-school claims from fact-sheet
  wiki-compiler[live-oak] reads: 4 relevant raw files + live-oak claims from fact-sheet
  wiki-compiler[overview] reads: all entity articles (already compiled) + fact-sheet summary
  → each invocation is ~10-20K tokens instead of ~150K
```

This requires the skill to pre-filter which raw files and claims are relevant to each article. The manifest already tracks source-to-entity mappings — use it.

**Problem 2: Claim-extractor reads all raw files at once.** Same issue.

**Fix: Per-file or per-entity-cluster extraction.** Spawn parallel extractors, each processing 3-5 related raw files. Claims merge into a single JSONL (trivially appendable).

**Problem 3: Fact-checker loads entire claims register.** For 171 claims, this is manageable. At 500+ claims it won't be.

**Fix: Batch by entity.** Check all claims for entity X together (enables cross-source comparison within entity), but don't load claims for entity Y.

### 7.4 Caching and Incremental Processing

**Source-level caching.** The manifest tracks content hashes. If a source file hasn't changed, don't re-extract claims from it. Currently every pipeline run re-processes everything.

```yaml
# manifest.json enhancement
{
  "raw/web/official/sfschool-admissions.md": {
    "content_hash": "abc123",
    "last_extracted": "2026-04-06",
    "claims_extracted": ["C001", "C002", "C015"],
    "last_verified": "2026-04-06"
  }
}
```

On re-run:
- If content_hash unchanged → skip extraction, reuse existing claims
- If content_hash changed → re-extract, re-verify only changed claims
- New sources → extract + verify (no cache)

**Estimated savings: 60-70% on re-runs** (most sources don't change between runs).

**Wiki-level incremental compilation.** Don't recompile articles whose input claims haven't changed.

```
For each wiki article:
  input_claims = claims referenced by this article
  if all input_claims.last_verified == article.last_compiled:
    skip compilation
  else:
    recompile article
```

### 7.5 Parallelism

v2 identified parallelism opportunities but didn't implement them. The key constraint is the shared budget ledger.

**What can parallelize safely today (no shared state conflicts):**

| Step | Parallelism Strategy | Speedup |
|---|---|---|
| Breadth research | Fan out by facet group (WHO/WHAT/WHEN separate agents) | ~3x |
| Depth research | Fan out by entity cluster | ~3-5x |
| Claim extraction | Fan out by raw file or entity cluster | ~3-5x |
| Fact-checking | Fan out by entity (sequential only for cross-entity disputes) | ~2-3x |
| Wiki compilation | Fan out by article (overview last, after entities) | ~3-5x |

**Budget ledger for parallel research agents:**

```yaml
# pipeline-state.yaml
budget:
  max_searches: 60
  used: 0
  lock: null  # agent_id holding the lock

# Each research agent:
# 1. Read pipeline-state.yaml
# 2. Check remaining budget
# 3. Write updated count after each search
# Problem: race conditions with parallel agents
```

**Simpler approach:** Pre-allocate budget per agent at spawn time. If 3 parallel agents need to share 60 searches, give each 20. No shared state, no locks.

```
skill spawns:
  research-agent[WHO-cluster] with budget=20
  research-agent[WHAT-cluster] with budget=20
  research-agent[WHEN-cluster] with budget=20
```

Unused budget doesn't carry over. This wastes some budget but eliminates coordination complexity.

**Estimated wall time reduction: 3-4x** from parallelism alone.

### 7.6 Search Efficiency

**Problem:** The research agent sometimes runs redundant or low-value searches.

**Fix 1: Search dedup at planning time.** The research-planner should identify questions that can be answered by the same search. Group questions into search clusters:

```yaml
search_clusters:
  - search: "SF School kindergarten admissions 2026-27"
    answers_questions: [Q001, Q003, Q007]  # deadline, tuition, age cutoff
  - search: "Live Oak School kindergarten application"
    answers_questions: [Q002, Q004, Q008]
```

This reduces 38 questions from 44 searches to potentially 25-30 searches.

**Fix 2: Stop-on-saturation.** If a search returns pages already in the manifest (same URL, same content hash), don't count it against budget but also don't fetch it again. Currently the agent may re-fetch pages it already has.

**Fix 3: Prioritized search ordering.** The research-planner scores questions by `user_value × searchability`. Execute highest-scored questions first. If budget runs out, the least valuable questions are the ones dropped.

### 7.7 Eval Cost Control

The helpfulness-eval-agent is expensive (LLM-as-judge on 30 test questions). Control costs:

- **Layer 1 (structural lint):** Run every pipeline. Nearly free (no LLM calls, just file parsing).
- **Layer 2 (helpfulness eval):** Run only after wiki-compiler produces new/changed articles. Skip if no wiki changes.
- **Layer 3 (red team task completion):** Run on demand only (`/kb-eval --deep`). Never automatic.

### 7.8 Summary: Combined Efficiency Gains

| Optimization | Cost Reduction | Wall Time Reduction | Effort |
|---|---|---|---|
| Model tiering (Haiku/Sonnet for simple agents) | 40-50% | — | Low |
| Entity-scoped compilation (smaller context) | 20-30% | — | Medium |
| Source-level caching (skip unchanged) | 60-70% on re-runs | 60-70% on re-runs | Medium |
| Parallelism (fan out by entity/facet) | — | 3-4x | Medium |
| Search dedup + clustering | 15-25% fewer searches | 15-25% faster research | Low |
| Eval cost control (tiered frequency) | 30-40% eval cost | — | Low |

**Combined estimate for a re-run of an existing topic:** 70-80% cheaper, 3-4x faster than current.
**Combined estimate for a first run of a new topic:** 40-50% cheaper, 2-3x faster than current.

---

## 8. Lessons from Content Production Pipelines

*Adapted from a parallel project (trending_topics) that runs an 8-step content production pipeline with specialized agents, quality gates, and iterative revision. That system produces media content; this system produces a reusable knowledge library. The patterns below are adapted for the library context — not copied directly.*

### 8.1 Hard Gates That Can't Be Averaged Away

**What they do:** In the content pipeline, fact safety has a hard floor of 8.0. A piece scoring 9.5 on structure but 6.5 on facts is NOT publishable. The gate is absolute — no amount of excellence elsewhere compensates for factual risk.

**Adaptation for the wiki:** The current L1-L5 system blocks L5 claims from appearing in wiki, but there's no hard gate on the *overall* factual health of an article. An article could have 10 L1 claims and 8 L3 claims with thin sourcing, and it passes lint.

**New rule:** Articles must meet a **minimum L1+L2 claim density**. If more than 40% of an article's factual claims are L3 or below, the article stays in `staging/` as a draft — it doesn't graduate to `wiki/`. This prevents thinly-sourced articles from appearing authoritative.

```yaml
# Article quality gate (lint-agent check)
article_gate:
  l1_l2_claim_ratio: >= 0.60    # hard floor, can't be averaged away
  l5_count: 0                    # absolute block
  stub_cells_in_tables: <= 0.30  # comparison tables must be >= 70% filled
```

### 8.2 Self-Critic Before Eval (Separate Lenses)

**What they do:** The content pipeline runs two separate quality passes:
- **Step 4a: Self-critic** — the article critiques itself (structure, clarity, user benefit delivery)
- **Step 5a: Evaluator** — an independent agent scores against the rubric

These are different questions. The self-critic asks "does this article do what it set out to do?" The evaluator asks "does this article meet the standard?"

**Adaptation for the wiki:** Currently the lint-agent combines structural checks with some content judgment. Split into:

1. **Wiki-critic-agent** (new, runs per-article after compilation):
   - Does this article fulfill its declared reader outcome?
   - Is the structure appropriate for the article type (guide vs. entity vs. concept)?
   - Are there dead sections that add words but not value?
   - Is the "Common Mistakes" section actually non-obvious, or is it generic?
   - Output: `staging/{article}-critic.md` with must-fix items

2. **Lint-agent** (existing, runs across entire wiki):
   - Structural integrity, links, frontmatter, directory placement
   - Unchanged from current role

3. **Helpfulness-eval-agent** (new, from §3):
   - Rubric scoring, test question pass rate, RO coverage
   - The independent evaluator

This three-layer separation ensures no quality dimension gets skipped because another dimension scored well.

### 8.3 Evidence Strength Map: Claim-Type-Specific Permitted Language

**What they do:** The content pipeline maps each claim type to its maximum permitted language:

| Claim Type | Evidence Type | Max Permitted Language |
|---|---|---|
| Mechanism/policy claim | Official law/regulation | Direct statement |
| Trend claim | Government data | Direct + date anchor |
| Organization behavior | Multi-source news | "According to multiple reports..." |
| Community feeling | Forum/social signal | "Many people report..." |
| Individual case | Single source | Cannot generalize to group |

This is more granular than our L1-L5 because it binds the *type of claim* to the *type of evidence required*, not just the source quality.

**Adaptation for the wiki:** The fact-checker should output an **evidence strength map** per entity/article, not just per-claim confidence levels. The wiki-compiler receives this map and uses it as a constraint:

```yaml
# fact-sheet.jsonl enhancement — per claim
{
  "claim_id": "C042",
  "text": "SF School tuition is $48,577",
  "confidence": "L1",
  "claim_type": "factual_number",       # NEW
  "evidence_type": "official_source",    # NEW
  "max_language": "State as fact with date anchor: 'For the 2025-26 school year, tuition is $48,577.'"
}
{
  "claim_id": "C099",
  "text": "Hamlin interview focuses on family values more than child performance",
  "confidence": "L4",
  "claim_type": "behavioral_pattern",    # NEW
  "evidence_type": "community_signal",   # NEW
  "max_language": "Parents commonly describe the interview as focused on family values. (community pattern, not officially confirmed)"
}
```

This prevents the wiki-compiler from stating community patterns as if they were official facts, even if it "feels true."

### 8.4 Mechanism Overreach Detection

**What they do:** The content fact-checker explicitly flags sentences that:
- Jump from institutional design → national attitude/moral judgment
- Jump from a single event → systemic conclusion
- Jump from community feeling → universal fact
- Jump from individual example → whole population outcome

It lists the **3 most likely overreach sentences** with downgraded rewrites.

**Adaptation for the wiki:** Add an overreach detection pass to the fact-checker-agent. For a knowledge library, common overreach patterns are:

| Overreach Type | Example | Fix |
|---|---|---|
| Small sample → general claim | "Parents love SF School" (based on 3 Niche reviews) | "Several Niche reviewers rate SF School highly" |
| One cycle → permanent truth | "The deadline is January 15" (true for 2025-26 only) | "For the 2025-26 cycle, the deadline was January 15" |
| Official language → actual practice | "The school evaluates readiness" (official page says this) | "The school states it evaluates readiness; parents describe..." |
| Correlation → causation | "Families who apply to 8+ schools are more likely to get in" | "Families who receive offers tend to have applied broadly" |
| Absence → nonexistence | "There is no financial aid" (just not found in research) | "Financial aid information was not found on the school's public pages" |

The fact-checker outputs these in a `overreach_flags` section. The wiki-compiler must address each one — either downgrade the language or add hedging.

### 8.5 Pre-Compilation Planning (Don't Just Write — Decide First)

**What they do:** Before writing begins, the content pipeline runs a full pre-production step that decides:
- What is the one core insight this piece delivers?
- What is the user's primary benefit (explanation, judgment, decision support, empathy)?
- What structure type fits this topic?
- What should this piece NOT drift into?

The writer only starts after these decisions are locked.

**Adaptation for the wiki:** Currently the wiki-compiler receives raw files + fact-sheet and just... writes. There's no planning step. This leads to articles that are information-complete but structurally undirected.

**New step: Article Planning** (runs once per article, before compilation):

```markdown
# Article Plan — {article-name}

## Article Type
entity / guide / concept / claim

## Reader Outcome Served
RO2: Build a school list — this article enables comparison of SF School vs. peers

## Primary User Benefit
Decision support: after reading, the parent can decide whether SF School belongs on their list

## What This Article Must NOT Drift Into
- Do not become a marketing page for the school
- Do not list every program; focus on differentiators
- Do not include unverified acceptance rates

## Structure
1. Quick Facts table (hard data: tuition, cutoff, class size, deadline)
2. What Makes This School Different (2-3 paragraphs, differentiators only)
3. Application Process (school-specific quirks, not generic ISSFBA process)
4. What Parents Say (L4 synthesis, hedged)
5. Common Mistakes (school-specific, non-obvious)
6. See Also

## Input Claims
[filtered list of claims relevant to this article from fact-sheet]
```

This plan is generated by the wiki-compiler-agent in a planning pass, then the same agent (or a parallel instance) executes the plan. The plan can be reviewed before compilation proceeds, just like the human checkpoint after breadth research.

### 8.6 Versioned Immutability

**What they do:** `text/v1/` is never overwritten. If the chief editor requests revisions, the new draft goes to `text/v2/`. This preserves the audit trail — you can always see what v1 looked like and what changed.

**Adaptation for the wiki:** Currently wiki articles are overwritten in place. The changelog captures what changed, but the original text is lost (only recoverable via git).

**New rule:** Wiki compilation writes to `staging/` first. Only after passing the quality gate (lint + critic + eval) does the article move to `wiki/`. If a re-compilation changes an article, the old version stays in git history (already true), but the staging step provides a review point.

```
Pipeline flow:
  wiki-compiler → staging/{article}.md
  quality-gate (critic + lint + eval) → pass/fail
  if pass: mv staging/{article}.md → wiki/{type}/{article}.md
  if fail: staging/{article}.md stays as draft; gap noted in eval report
```

This is lighter than full v1/v2 versioning (the content pipeline needs it because it iterates multiple times on one piece). The wiki pipeline typically compiles once and the staging gate is sufficient.

### 8.7 Postmortem → SOP Self-Improvement Loop

**What they do:** After each piece publishes, the postmortem step asks: "What is one specific rule in this SOP that should change, based on what happened?" This is a concrete proposed edit, not a general observation. Over time, the SOP evolves based on production experience.

**Adaptation for the wiki:** After each full `/kb-research` run, the evolve-agent should include a **pipeline retrospective** section:

```markdown
## Pipeline Retrospective

### What Worked
- Entity-scoped compilation produced focused articles (confirmed by eval)

### What Didn't Work
- Budget ran out at question 25 of 38 — pre-allocated budgets were too conservative

### Proposed Agent/Skill Changes
1. research-agent.md: increase default per-cluster budget from 15 to 20 searches
   Reason: depth questions consistently need 3-4 searches each, not 2
2. wiki-compiler-agent.md: add explicit instruction to include "What Parents Say" section for entity articles
   Reason: L4 synthesis was skipped in 4/11 entity articles despite available community data
```

These proposed changes feed back to the human for approval. Over multiple runs, the pipeline improves itself — not just the wiki content.

### 8.8 Bridge Artifacts: Explicit Handoff Contracts

**What they do:** Each pipeline step produces a named file with a defined schema. Step N+1 knows exactly which files to read and what fields to expect. There's no ambiguity in handoffs — `preproduction.md` has 5 required sections; Step 3 will not start without them.

**Adaptation for the wiki:** The current pipeline has implicit handoffs — the research-agent "knows" to write to `raw/web/`, and the claim-extractor "knows" to read from there. But the contracts are in agent prompts, not in a shared schema.

**New artifact: `pipeline-contracts.yaml`** — defines what each step produces and what the next step requires:

```yaml
contracts:
  landscape_scan:
    produces: landscape.yaml
    required_fields: [entities_discovered, source_ecosystem, common_pain_points]
    consumed_by: research_planner

  research_planning:
    produces: research-plan.yaml
    required_fields: [questions, search_clusters, source_tier_targets]
    requires: [landscape.yaml, _topic.yaml]
    consumed_by: research_agent

  research_execution:
    produces: raw/**/*.md, manifest.json, search-log.jsonl
    requires: [research-plan.yaml]
    consumed_by: claim_extractor

  claim_extraction:
    produces: claims-register.jsonl
    required_fields_per_claim: [id, text, entity, source, claim_type]
    requires: [raw/**/*.md]
    consumed_by: fact_checker

  fact_checking:
    produces: fact-sheet.jsonl
    required_fields_per_claim: [id, confidence, max_language, claim_type, evidence_type]
    requires: [claims-register.jsonl]
    gate: {l5_count: 0}
    consumed_by: wiki_compiler

  article_planning:
    produces: staging/{article}-plan.md
    required_fields: [article_type, reader_outcome, primary_benefit, structure, input_claims]
    requires: [fact-sheet.jsonl, _topic.yaml]
    consumed_by: wiki_compiler

  wiki_compilation:
    produces: staging/{article}.md
    requires: [staging/{article}-plan.md, fact-sheet.jsonl, relevant raw files]
    consumed_by: [wiki_critic, lint_agent, helpfulness_eval]

  quality_gate:
    requires: [staging/{article}.md, critic output, lint report, eval report]
    gate: {l1_l2_ratio: ">=0.60", l5_count: 0, stub_ratio: "<=0.30"}
    produces: wiki/{type}/{article}.md  # only if gate passes
```

This makes the pipeline debuggable — if an article fails the quality gate, you can trace backwards through the contract chain to find where the input was insufficient.

### 8.9 What NOT to Adopt

Some patterns from the content pipeline are specific to media production and don't belong in a knowledge library:

| Content Pipeline Pattern | Why It Doesn't Apply |
|---|---|
| Anti-template checks (differ from last 3 episodes) | Wiki articles should be *consistent*, not varied. Entity articles should all follow the same structure. |
| Brand voice / persona constraints | The wiki has no persona. Neutral, clear, decision-support tone is the default. |
| Opening hooks / retention optimization | Wiki readers arrive with a specific question, not from a recommendation algorithm. |
| Packaging (titles, thumbnails) | No distribution surface. The wiki is consumed by reference, not discovery. |
| Gold sentence density | The wiki optimizes for information density, not memorability. |
| TTS/audio/video production | Not applicable — wiki is text. |
| Chief editor as human gate | The wiki pipeline should be fully automated with human oversight optional, not required per article. |

The knowledge library is the *upstream source* that a media company would consume. It optimizes for accuracy, completeness, and decision-support — not engagement, retention, or brand voice. A downstream consumer (like the trending_topics pipeline) would add voice, structure, and packaging on top of the wiki's neutral knowledge base.

---

## Appendix: Content Gap Categories

Three structural categories explain why content is missing. Each has a different fix:

**Category A: Pre-Decision Questions** — questions the reader has *before* the topic's main decision
- Example: "Is private school worth $50k/year?" comes before "how do I apply?"
- Fix: research-planner must scope one step earlier than the obvious starting point
- General rule: always include a "should I even do this?" article

**Category B: Experiential Content** — knowledge that only exists in UGC and lived experience
- Example: "What do they actually ask in the parent interview?"
- Fix: L4 synthesis patterns + Phase 0 UGC mining
- General rule: if official sources won't answer it, community sources probably will

**Category C: Lifecycle Questions** — what happens *after* the topic's main decision
- Example: "What happens if we want to switch to public in 3rd grade?"
- Fix: research-planner must scope one step beyond the obvious endpoint
- General rule: always include a "what happens next?" article

---

*v3 — 2026-04-06*
