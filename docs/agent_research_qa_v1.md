# Agent Research Pipeline: Q&A and Design Decisions v1

**Responds to:** inline comments in [agent-research-pipeline.md](./agent-research-pipeline.md)
**Reference system:** `trending_topics/.claude/agents/` and `trending_topics/process/`

---

## Q1: Should the agent record raw search results (query + extracted text)?

> *From Section 2: "should the agent record the raw search results? including the query and extract text from the web page?"*

**Yes, absolutely — but with structure.**

### What to record

Every search operation produces a **search record** and every page fetch produces a **raw extraction**. These are separate artifacts.

**Search record** (append to `raw/search-log.jsonl`):

```jsonl
{
  "id": "s-2026-04-06-001",
  "timestamp": "2026-04-06T10:23:00Z",
  "question_id": "q1",
  "query": "Bay Area private elementary schools kindergarten list 2026",
  "engine": "web_search",
  "results_count": 10,
  "results_selected": ["https://sfschool.org/...", "https://niche.com/..."],
  "results_skipped_reason": {"https://seosite.com/...": "SEO listicle, no original content"},
  "new_concepts_discovered": ["Ravenna Hub", "TK/transitional kindergarten"],
  "new_questions_spawned": ["q1.1", "q1.2"]
}
```

**Raw extraction** (one file per page, `raw/web/2026-04-06_sfschool-admissions.md`):

```markdown
---
url: https://sfschool.org/Admissions-Process
fetched: 2026-04-06T10:24:00Z
search_id: s-2026-04-06-001
question_id: q1
content_hash: sha256:abc123
reliability_tier: L1-official
extract_method: web_fetch_markdown
---

[Full extracted markdown content of the page]
```

### Why record both

1. **Reproducibility** — you can re-run the research pipeline and see what was searched, what was found, what was selected. Without this, the wiki is an oracle with no audit trail.

2. **Deduplication** — the search log prevents re-running the same query. When a new question is spawned, the agent checks: "has a semantically similar query already been run?"

3. **Debugging** — when a wiki claim turns out wrong, you can trace: which search → which page → which extracted text → which compiled claim. Without raw extractions, this chain breaks.

4. **Re-compilation** — if SCHEMA.md changes (new article template, different categorization), you can re-compile the wiki from raw extractions without re-fetching everything.

### Comparison with trending_topics

Trending_topics records raw data as `scraped_data.json` (per-source forum data with engagement signals) → `intelligence_brief.md` (synthesized) → `research_notes.md` (with evidence table). They separate *intelligence inputs* from *citable sources* — forum data is never cited directly.

**My take:** This is the right instinct. For the knowledge base, I'd adopt a similar two-layer approach:

```
raw/
├── search-log.jsonl         # All queries + result metadata (internal, never cited)
├── web/                     # Full page extractions (citable source material)
│   ├── official/            # L1: school websites, government sites
│   ├── journalistic/        # L2: news outlets
│   ├── review/              # L3: Niche, GreatSchools
│   └── community/           # L4: forums, Reddit (intelligence only, not citable for facts)
└── research-plan.yaml       # Question tree (internal)
```

The key rule borrowed from trending_topics: **community sources are intelligence inputs, not factual citations.** A Reddit post saying "Cathedral acceptance rate is 20%" tells you *what to verify*, not what to state as fact.

---

## Q2: How do you discover new queries?

> *From Section 4: "how do you discover new queries?"*

### Three discovery mechanisms

**Mechanism 1: Concept Extraction (during READ phase)**

After fetching a page, the agent extracts a **concept list** — proper nouns, technical terms, processes, organizations that don't yet exist in the wiki index or question tree.

```
Page: sfschool.org/Admissions-Process
Extracted concepts:
  - "Ravenna Hub" → not in question tree → spawn: "What is Ravenna Hub?"
  - "parent tour" → exists as sub-concept of q3 → no new question
  - "NAIS" → not in tree → spawn: "What is NAIS and how does it relate?"
```

Implementation: After every page extraction, run a concept diff:

```python
def discover_new_questions(page_content, existing_concepts, question_tree):
    # Extract named entities and technical terms from page
    new_concepts = extract_concepts(page_content) - existing_concepts

    new_questions = []
    for concept in new_concepts:
        # Check: is this concept important enough to research?
        relevance = score_relevance(concept, topic=question_tree.topic)
        if relevance >= THRESHOLD:
            q = Question(
                text=f"What is {concept} and how does it relate to {question_tree.topic}?",
                parent_id=current_question.id,
                source="concept_extraction",
                discovered_from=page.url
            )
            new_questions.append(q)
    return new_questions
```

**Mechanism 2: Gap Detection (during REASON phase)**

After answering a question, the agent evaluates: "what adjacent questions does this answer raise?"

```
Question: "What is the application timeline?"
Answer: "Applications due Jan, assessments Feb-Mar, decisions Mar"

Gap detection:
  - "What happens BEFORE applications open?" → prep timeline question
  - "What if you miss the deadline?" → late/rolling admissions question
  - "Are there different timelines for different school types?" → comparative question
```

This is different from concept extraction — it's about *logical adjacency*, not *named entities*.

**Mechanism 3: Cross-Reference Gaps (during COMPILE phase)**

When building wiki articles, the agent notices references to concepts without corresponding articles:

```
Article: cathedral-school.md mentions "Episcopal tradition"
  → No wiki/concepts/episcopal-schools.md exists
  → Spawn question: "What distinguishes Episcopal schools in the Bay Area?"
```

### Comparison with trending_topics

Trending_topics' source-intelligence-agent discovers new stories by scanning forums, clustering by theme, and scoring relevance. The editorial-agent then selects which to pursue using the 3-3-1 rule. Discovery is **externally driven** (what's trending) rather than **internally driven** (what's missing from our knowledge).

**Key difference:** For a knowledge base, discovery should be primarily *internal* — driven by gaps in the existing wiki. Trending content is secondary. The question tree serves as the "what we know we don't know" tracker, which trending_topics doesn't need because each episode is independent.

---

## Q3: How to score questions for prioritization?

> *From Section 4: "how to score the questions, so we can prioritize high value questions?"*

### Scoring Framework

Each question gets a composite score from four dimensions:

```yaml
question: "What is the application timeline and key deadlines?"
scores:
  user_value: 9       # How much does this matter to the end user?
  searchability: 8    # Can web search reliably answer this?
  dependency_count: 5 # How many other questions depend on this answer?
  novelty: 7          # How much new knowledge does this add vs. what we already have?
  composite: 7.5      # Weighted average
```

**Scoring criteria:**

| Dimension | 1-3 (low) | 4-6 (medium) | 7-10 (high) |
|-----------|-----------|--------------|-------------|
| **User value** | Nice to know; tangential | Useful but not blocking a decision | Directly affects what the user does next |
| **Searchability** | Subjective, experiential, hidden | Partially available, requires aggregation | Official sources exist and are accessible |
| **Dependency count** | Standalone question | 1-2 other questions reference this | Foundational — many questions can't be answered without this |
| **Novelty** | Already well-covered in existing wiki | Adds moderate new info | Opens an entirely new facet of knowledge |

**Weighting:**

```python
composite = (
    user_value * 0.35 +
    searchability * 0.20 +
    dependency_count * 0.25 +
    novelty * 0.20
)
```

User value gets the highest weight because the knowledge base exists to serve the user. Dependency count is second because foundational questions (like "what schools exist?") unblock many downstream questions.

### Dynamic Re-scoring

Scores change as research progresses:

- After answering q1 ("what schools exist?"), the novelty score of q1 drops to 0 — but the dependency_count of q3 ("what do applications require?") may increase because now we know *which specific schools* to research.
- A question that starts at medium user_value may jump to high after the user asks a related question (signal of interest).

### Comparison with trending_topics

Trending_topics uses segment-specific relevance scoring (0-10) with predefined weights per topic category: career/layoffs=10 for tech-male-bayarea, education/admissions=10 for parents. Their editorial-agent then applies the 3-3-1 rule for selection.

**Key difference:** Trending_topics scores *stories for audience segments* — a broadcast optimization problem. The knowledge base scores *questions for knowledge coverage* — a completeness optimization problem. The dimensions are fundamentally different: trending cares about engagement/timeliness; the knowledge base cares about user value/dependency structure.

**What I'd borrow:** The idea of **segment-aware scoring.** If the knowledge base user has a specific profile (e.g., "parent of 4-year-old in SF, interested in progressive schools"), questions about progressive SF schools should score higher than questions about South Bay religious schools. This is the equivalent of trending_topics' audience segments applied to research prioritization.

---

## Q4: How to deduplicate questions?

> *From Section 4: "how to dedup questions, so we don't waste effort on questions already done research?"*

### Three layers of deduplication

**Layer 1: Exact and Near-Exact Match**

Before adding a new question, check against existing questions using normalized text comparison:

```python
def is_duplicate(new_q, existing_questions):
    new_normalized = normalize(new_q.text)  # lowercase, remove stop words, stem
    for eq in existing_questions:
        if similarity(new_normalized, normalize(eq.text)) > 0.85:
            return True, eq.id
    return False, None
```

Example:
- "What is the application deadline for SF School?" ≈ "When are SF School applications due?" → **duplicate**

**Layer 2: Semantic Subsumption**

A new question may be a sub-question of one already answered, or vice versa:

```
Existing (answered): "What is the typical application timeline?"
New question:        "When does Cathedral School accept applications?"

→ NOT a duplicate — the existing answer covers the general timeline,
  but the new question asks about a specific school.
→ Mark as CHILD of the timeline question.
→ But check: does the existing answer already contain this specific info?
  If yes: mark new question as "already_covered" instead of researching.
```

**Layer 3: Query-Level Deduplication**

Even if two questions are distinct, they may produce the same search queries. The search log prevents re-running identical queries:

```python
def should_search(query, search_log):
    for past in search_log:
        if similarity(query, past.query) > 0.90:
            # Same query already run
            return False, past.id
        if past.results_selected and any(
            url in already_fetched for url in candidate_urls
        ):
            # Different query but would fetch same pages
            return "partial", past.id
    return True, None
```

### Practical example

```
Question tree after Round 1:
  q1: "What are the Bay Area private K schools?" [status: answered]
  q1.1: "What is TK vs K?" [status: pending]
  q1.2: "What is BADA/BAIA?" [status: pending]

Round 2 search discovers a new page mentioning "transitional kindergarten"
  → Agent considers spawning: "What is transitional kindergarten?"
  → Dedup Layer 1: compare with q1.1 ("What is TK vs K?")
  → "TK" = "transitional kindergarten" → semantic match
  → Result: MERGE into q1.1, don't create new question
```

### Comparison with trending_topics

Trending_topics' source-intelligence-agent clusters stories by semantic similarity at the *story level* — same event = one cluster. Their "thematic compression rule" then forces 2+ stories sharing the same frame into ONE segment.

**What I'd borrow:** The concept of **thematic clustering** above individual question dedup. If three questions are all variations of "how competitive is admission?", they should be clustered into one *research theme* and answered together, not as three independent searches. This is more efficient and produces better synthesis.

---

## Q5: Why breadth-first then depth-first? How would a typical researcher do this?

> *From Section 4: "why do we do depth first, not breadth first? just curious, how would a typical researcher do this? reading survey or digging very deep into a topic first?"*

### How researchers actually work

Research methodology literature identifies two archetypes:

**The Surveyor (breadth-first):**
- Reads 2-3 overview articles or survey papers first
- Builds a mental map of the landscape
- Then selectively deep-dives into areas of interest
- Common in: academic research, unfamiliar domains, systematic reviews

**The Driller (depth-first):**
- Picks one thread and follows it to the bottom
- Deep expertise in one area before broadening
- Common in: investigative journalism, debugging, expertise-driven work

**Most good researchers use a hybrid** — but they start with breadth. The reason is simple: **you can't know what's important to go deep on until you know the landscape.**

### Why breadth-first is correct for knowledge base building

```
Scenario A (breadth-first): Private school KB

  1. Breadth scan → discovers 35 schools, Ravenna platform, TK, financial aid
  2. Now the agent KNOWS the landscape. It can:
     - Prioritize which schools to deep-dive (most popular first)
     - Create a comparison framework that covers all schools
     - Cross-reference across schools (shared deadlines, shared platforms)
     - Detect patterns ("all progressive schools use Ravenna")

Scenario B (depth-first): Private school KB

  1. Deep dive on Cathedral School → 5 searches, detailed profile
  2. Deep dive on SF School → 5 searches, detailed profile
  3. ...after 10 schools, discovers Ravenna exists
  4. Problem: need to go BACK to all 10 school profiles and add Ravenna info
  5. Problem: no comparison framework exists yet, so profiles are inconsistently structured
  6. Problem: spent 50 searches on 10 schools but haven't discovered 25 other schools
```

Depth-first causes **rework** and **inconsistent coverage**.

### The exception: when depth-first is better

If the user has a very specific need ("tell me everything about Cathedral School"), depth-first is appropriate. The research strategy should adapt to the query scope:

| Scope | Strategy | Example |
|-------|----------|---------|
| Broad topic | Breadth → depth | "Bay Area private K schools" |
| Specific entity | Depth-first | "Tell me about Cathedral School" |
| Comparative | Breadth on compared entities, then depth on differences | "Cathedral vs SF School" |
| Process-oriented | Depth on the process, breadth on variants | "How do K assessments work?" |

### Comparison with trending_topics

Trending_topics is inherently breadth-first at the discovery stage (source-intelligence-agent scans 6+ forums) then depth-first at the production stage (research-agent deep-dives on selected stories). This is the same pattern: **survey the landscape, then drill into selected targets.**

---

## Q6: How to determine source quality?

> *From Section 4: "how to determine source quality?"*

### Source Quality Assessment Model

Source quality is not a single score — it's a multi-dimensional evaluation:

```yaml
source_assessment:
  url: https://sfschool.org/Admissions-Process

  authority:
    type: official          # official | institutional | journalistic | review-platform | community | unknown
    organization: "The San Francisco School"
    is_primary_source: true # Are they the original authority on this info?
    score: 9

  freshness:
    publication_date: 2025-09-01     # When was this content published/updated?
    retrieval_date: 2026-04-06
    staleness_risk: low              # low | medium | high
    valid_until: 2027-03-31          # When does this info likely expire?
    score: 8

  accuracy_signals:
    has_specific_dates: true         # Specific dates > vague statements
    has_verifiable_numbers: true     # Numbers that can be cross-checked
    cites_own_sources: false         # Does the page cite its sources?
    consistent_with_other_sources: true
    score: 8

  bias_signals:
    has_commercial_interest: false   # Is the source trying to sell something?
    is_promotional: false            # School's own site IS promotional but that's expected
    selection_bias: "school-favorable"  # School's own description will be positive
    score: 7

  composite: 8.0
  reliability_tier: L1
```

### Automated Quality Signals

Some quality indicators can be detected programmatically:

| Signal | Detection | Meaning |
|--------|-----------|---------|
| Domain type | `.edu`, `.gov`, `.org` vs `.com` | Institutional vs commercial |
| HTTPS + cert | TLS check | Basic legitimacy |
| Publication date | Extract from page metadata | Freshness |
| Author attribution | Byline present? | Accountability |
| Advertising density | Ad-to-content ratio | SEO farm indicator |
| Content originality | Compare with other pages on same topic | Original vs. scraped/rewritten |
| Specificity | Counts of dates, names, numbers vs. vague language | Signal-to-noise ratio |

### The Source Tier System (revised)

Building on the initial L1-L5, but with **explicit criteria** for how to classify:

| Tier | Rule | Examples | What can be cited |
|------|------|----------|------------------|
| **L1: Primary official** | The entity itself publishing about itself | sfschool.org/admissions, USCIS.gov | Facts directly |
| **L2: Authoritative third-party** | Established journalists/institutions with editorial standards | SFChronicle, EdWeek, NAIS reports | Facts with attribution |
| **L3: Aggregator/review** | Platforms that compile data with some verification | Niche.com, GreatSchools, PrivateSchoolReview | Data with "according to" |
| **L4: Community** | Forums, Reddit, parent groups — real experiences, unverified facts | r/SFBayArea, DC Urban Mom, Huaren | **As anecdote only, never as fact** |
| **L5: Low-signal** | SEO content, undated articles, AI-generated listicles | "Top 10 Best Private Schools Bay Area" | **Do not cite. Use only for discovery** |

### Comparison with trending_topics

Trending_topics has the strongest design here. Their key innovations:

1. **Permitted language per evidence level** — not just "L3 = medium confidence" but "L3 = you may only say '社区里很多人反映', never state as universal fact." This is brilliant because it **constrains the output** based on evidence quality, not just labels it.

2. **Community Signal Rule** — forum data is valid for "what people are anxious about" but invalid for "what is actually true." This distinction between *signal* and *evidence* is absent from most knowledge base designs.

3. **Mechanism Overreach Check** — detecting logical leaps from evidence to conclusion (individual example → population-wide claim). This catches a category of error that simple fact-checking misses.

**What I'd adopt for the knowledge base:**

The permitted-language concept is the most transferable. For the school application wiki:

| Evidence tier | Permitted phrasing | Prohibited phrasing |
|---------------|-------------------|---------------------|
| L1 (official site) | "SF School's tuition is $38,500" | — |
| L2 (news) | "According to SFChronicle, enrollment has declined" | "Enrollment has declined" (without attribution) |
| L3 (Niche) | "Niche rates the school 4.2/5 based on parent reviews" | "The school is rated 4.2/5" (implies universal) |
| L4 (forum) | "Some parents on Bay Area forums report long wait lists" | "The school has long wait lists" |
| L5 (SEO) | Do not cite | Anything |

This is a meaningful upgrade over the original design which only had confidence levels without constraining the *language used to express claims*.

---

## Q7: How to extract claims for factuality checking?

> *From Section 5: "how to extract claims for the factuality check?"*

### The Claim Extraction Pipeline

This is the most complex sub-problem. A wiki article contains a mix of factual claims, opinions, process descriptions, and editorial framing. Only *factual claims* need verification.

### Step 1: Sentence-Level Claim Classification

Run each sentence through a classifier:

```
Input: "SF School's tuition for 2026-27 is $38,500 and parents describe
        the community as warm and inclusive."

Output:
  - "SF School's tuition for 2026-27 is $38,500"
    → TYPE: factual_claim (verifiable number)
    → VERIFY: yes

  - "parents describe the community as warm and inclusive"
    → TYPE: sentiment_aggregation (subjective, attributed)
    → VERIFY: no (it's explicitly framed as opinion)
```

### Step 2: Claim Typing

| Claim type | Needs verification? | How to verify | Example |
|------------|-------------------|---------------|---------|
| **Numerical** (price, date, count, rate) | Yes — highest priority | Compare against L1 source | "Tuition is $38,500" |
| **Categorical** (type, status, membership) | Yes | Verify against official source | "Cathedral is an Episcopal school" |
| **Process** (steps, requirements, how-to) | Yes, but harder | Verify against official description | "Applications require two recommendations" |
| **Temporal** (timeline, sequence, deadline) | Yes — high priority | Verify against official calendar | "Decisions released March 19" |
| **Comparative** (better than, different from) | Partially — check the facts underneath | Verify underlying data points | "SF School is more progressive than Cathedral" |
| **Causal** (X causes Y, X leads to Y) | Flag for review | Often unverifiable at L1-L2 level | "Strong essays increase admission chances" |
| **Sentiment** (people feel, parents say) | No — but verify attribution | Check that the sentiment is correctly aggregated | "Parents report positive experiences" |
| **Definitional** (X is Y, X means Y) | Lower priority | Check against authoritative definitions | "TK is California's transitional kindergarten program" |

### Step 3: Claim Extraction Format

Each extracted claim becomes a structured record:

```yaml
claims:
  - id: c001
    text: "SF School tuition for 2026-27 is $38,500"
    type: numerical
    article: wiki/schools/sf-school.md
    line: 12
    sources:
      - url: https://sfschool.org/tuition
        tier: L1
        supports: true
        extracted_value: "$38,500"
      - url: https://niche.com/k12/sf-school
        tier: L3
        supports: false
        extracted_value: "$37,200"
        note: "likely prior year data"
    verdict: confirmed
    confidence: L1
    valid_until: 2027-08-01

  - id: c002
    text: "Cathedral acceptance rate is approximately 25%"
    type: numerical
    article: wiki/schools/cathedral-school.md
    line: 15
    sources:
      - url: https://parentforum.com/thread/123
        tier: L4
        supports: true
        extracted_value: "around 25%"
      - url: https://cathedralschool.net
        tier: L1
        supports: null  # no data on this
    verdict: single_source_low_tier
    confidence: L4
    note: "No official rate published. Forum-sourced estimate only."
```

### Step 4: Verification Priority

Not all claims are worth verifying with equal effort:

```
MUST verify (immediate):
  - Any claim the user might act on (deadlines, costs, requirements)
  - Any claim involving legal/regulatory information
  - Any numerical claim that appears in comparison tables

SHOULD verify (when possible):
  - Process descriptions (steps, requirements)
  - Categorical claims (school type, grade range)
  - Historical claims (founding date, changes)

MAY skip verification:
  - Clearly attributed opinions ("parents describe...")
  - Definitional claims from authoritative sources
  - Claims that are self-evident from context
```

### Comparison with trending_topics

Trending_topics has the most sophisticated claim-level pipeline I've seen in a production system:

1. **Evidence Strength Map** — every claim gets an evidence type and "max permitted language" before the content is even written. Claims are categorized as: law/official, single report, community signal, individual case.

2. **Mechanism Overreach Check** — a dedicated pass that catches *logical leaps*, not just factual errors:
   - "This layoff shows the tech industry is in systemic decline" → OVERREACH (single event → systemic conclusion)
   - Downgraded to: "This layoff is one signal of broader industry adjustment"

3. **Multi-gate verification** — claims pass through research-agent → fact-checker-agent → self-critic-agent → content-evaluator-agent → chief-editor-agent. That's 5 gates.

**What's different for a knowledge base vs. trending_topics:**

Trending_topics is optimized for *broadcast* — every claim will be heard by thousands of people, so the cost of a wrong claim is high and the pipeline justifies 5 gates. A personal knowledge base has a different trade-off:

| | Trending Topics | LLM Knowledge Base |
|---|---|---|
| Audience | Thousands | 1 person (the user) |
| Cost of error | Public trust damage | Bad personal decision |
| Correction speed | Can't un-broadcast | Edit the wiki |
| Throughput need | Daily production | Compounding over weeks |
| Verification budget | High (justifies 5 gates) | Medium (2-3 gates sufficient) |

**My design for the knowledge base: 3-gate verification**

```
Gate 1: EXTRACTION-TIME CHECK (during compile)
  - Classify claim type
  - Assign source tier
  - Set permitted language based on tier
  - Flag numerical/deadline claims for priority verification

Gate 2: CROSS-SOURCE CHECK (during compile or lint)
  - For flagged claims: search for corroborating source
  - For conflicting claims: create claims/ article
  - For single-source claims: tag and move on (don't block)

Gate 3: USER-ACTION GATE (on-demand, when user is about to act)
  - When user asks "should I submit to SF School by Jan 23?"
  - Agent re-verifies the deadline against the official source NOW
  - This is the highest-stakes check and should be real-time
```

This is fewer gates than trending_topics, but adds something trending_topics doesn't have: **the user-action gate** — a real-time verification triggered when the user is about to make a decision based on wiki content. This is more valuable for a personal knowledge base than pre-publication gates, because knowledge decays and the most important moment to verify is right before action.

**What I'd adopt from trending_topics:**

The **Mechanism Overreach Check** concept. Even in a personal wiki, the agent can make logical leaps:
- "3 out of 5 schools I researched use Ravenna" → OVERREACH → "Most Bay Area private K schools use Ravenna"
- Correct: "At least 3 Bay Area private K schools use Ravenna; it appears to be widely adopted"

This is a real risk because LLMs naturally generalize from small samples. A dedicated overreach check pass — even a lightweight one — prevents the wiki from accumulating confident-sounding but poorly-supported generalizations.

---

## Q8: Multi-topic wiki structure

> *From Section 6: "remember we will have many topics, school application is just one of the topics."*

### Topic-Namespaced Directory Structure

When the knowledge base covers multiple domains, the directory structure needs a topic layer:

```
knowledge/
├── SCHEMA.md                     # Global conventions
├── index.md                      # Cross-topic master index
├── log.md                        # Global operation log
├── manifest.json                 # Global source tracking
│
├── topics/
│   ├── private-school-k/
│   │   ├── _topic.yaml           # Topic metadata, research plan, budget
│   │   ├── index.md              # Topic-specific index
│   │   ├── overview.md
│   │   ├── raw/                  # Topic-specific raw sources
│   │   ├── wiki/                 # Topic-specific wiki articles
│   │   ├── claims/
│   │   └── output/
│   │
│   ├── bay-area-housing/
│   │   ├── _topic.yaml
│   │   ├── index.md
│   │   ├── raw/
│   │   ├── wiki/
│   │   └── ...
│   │
│   └── immigration-h1b/
│       └── ...
│
├── shared/
│   ├── concepts/                 # Cross-topic concepts
│   │   ├── bay-area-geography.md # Referenced by multiple topics
│   │   └── financial-planning.md
│   └── entities/
│       ├── people/
│       └── organizations/
│
└── .meta/
    ├── provenance/
    └── lint-reports/
```

### Cross-Topic Linking

Some entities span topics:

```markdown
<!-- In topics/private-school-k/wiki/schools/sf-school.md -->
Location: [[shared:bay-area-geography#portola|Portola, SF]]
See also: [[immigration-h1b:concepts/visa-school-choice|H-1B considerations for school choice]]
```

### Topic Lifecycle

```yaml
# topics/private-school-k/_topic.yaml
topic: "Bay Area Private School K Application"
status: active           # active | dormant | archived
created: 2026-04-06
last_research: 2026-04-06
next_lint: 2026-05-06
research_budget:
  total_searches: 50
  used_searches: 48
  remaining: 2
articles_count: 45
freshness_policy:
  volatile_claims_ttl: 90d    # Tuition, deadlines
  stable_claims_ttl: 365d     # School philosophy, location
```

---

## Summary: What's Different From Trending Topics and Why

| Aspect | Trending Topics | LLM Knowledge Base | Why Different |
|--------|----------------|--------------------|----|
| **Goal** | Daily broadcast content | Compounding personal wiki | One is consumed and forgotten; the other accumulates |
| **Verification gates** | 5 gates (research → factcheck → self-critic → evaluator → chief editor) | 3 gates (extraction → cross-source → user-action) | Lower audience = lower blast radius; user-action gate is more valuable than pre-pub gates |
| **Conflict resolution** | Hierarchy resolves (L1 beats L2) | Preserve conflict explicitly in claims/ | Broadcast must commit to one position; wiki can hold ambiguity |
| **Source treatment** | Forum = intelligence only, never cited | Same principle adopted, but with explicit tier-based permitted language | Direct adoption — this is trending_topics' best idea |
| **Scoring** | Audience segment relevance (engagement-driven) | Knowledge coverage scoring (completeness-driven) | Different optimization targets |
| **Deduplication** | Story-level semantic clustering | Question-level + query-level + concept-level (3 layers) | Knowledge base has more dedup surfaces because questions compound |
| **Permitted language** | Strict per-evidence-level language rules | Adopted from trending_topics — major upgrade over v0 design | This is the single best idea to borrow |
| **Overreach detection** | Mechanism Overreach Check (dedicated pass) | Adopted as lightweight pass during compile | Prevents confident-sounding but poorly-supported generalizations |
| **Time handling** | Episode-based (daily, disposable) | Persistent with TTL and freshness checks | Wiki content must age gracefully; broadcast doesn't |

### What trending_topics does better

1. **Permitted language per evidence tier** — the most transferable innovation. Forces the writer (human or LLM) to match claim confidence to evidence strength at the *sentence level*.
2. **Mechanism Overreach Check** — catches logical leaps that pure fact-checking misses.
3. **Compliance hard-gates** — L5 errors block publication entirely. The knowledge base should similarly block L5 claims from entering wiki/.

### What the knowledge base does better

1. **User-action gate** — verifying at the moment of decision, not at the moment of writing. More valuable when knowledge decays.
2. **Conflict preservation** — instead of resolving, hold the ambiguity. The user is a single person who can handle nuance; a broadcast audience cannot.
3. **Incremental compounding** — every query enriches the system. Trending_topics episodes are independent; the knowledge base accumulates.
4. **Question tree as research scaffold** — makes the research process itself an auditable, resumable artifact.
