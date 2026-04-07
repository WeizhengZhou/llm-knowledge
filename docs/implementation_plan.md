# LLM Knowledge Base: Implementation Plan

**Based on:** [design.md](./design.md), [agent-research-pipeline.md](./agent-research-pipeline.md), [agent_research_qa_v1.md](./agent_research_qa_v1.md)
**Architecture pattern:** Follows `trending_topics/` — agent definitions as markdown, Python orchestrator, file-based handoffs

---

## 1. What Needs to Be Built

Three layers:

```
Layer 1: Agent Definitions      (.claude/agents/*.md)
         — LLM system prompts with role boundaries, standards, output formats

Layer 2: Pipeline Orchestrator   (backend/pipeline.py)
         — Python CLI that sequences agents, manages state, handles retries

Layer 3: Supporting Tools        (backend/tools/*.py)
         — Question tree, manifest, search log, claim store, cross-linker
```

Plus: `CLAUDE.md`, `SCHEMA.md`, config files, and Claude Code skills for interactive use.

---

## 2. Agent Definitions

### 2.1 Agent Inventory (8 agents)

| # | Agent | Role | Input | Output | Model |
|---|-------|------|-------|--------|-------|
| 1 | `research-planner-agent` | Decompose topic → question tree | Topic string + user context | `research-plan.yaml` | opus |
| 2 | `research-agent` | Execute searches, fetch pages, record raw data | `research-plan.yaml` | `raw/web/*.md` + `search-log.jsonl` | sonnet |
| 3 | `claim-extractor-agent` | Extract verifiable claims from raw sources | `raw/web/*.md` | `claims-register.yaml` | sonnet |
| 4 | `fact-checker-agent` | Verify claims, assign L1-L5, set permitted language | `claims-register.yaml` + raw sources | `fact-sheet.yaml` | opus |
| 5 | `wiki-compiler-agent` | Synthesize raw sources → wiki articles | raw sources + fact-sheet + research-plan | `wiki/**/*.md` | opus |
| 6 | `lint-agent` | Structural/content/coverage checks | `wiki/` tree | `lint-report.md` | sonnet |
| 7 | `query-agent` | Answer questions, file answers back into wiki | User question + `wiki/` | Answer + optional new wiki page | opus |
| 8 | `evolve-agent` | Gap analysis, freshness checks, improvement suggestions | `wiki/` + `research-plan.yaml` | Updated research-plan + new questions | sonnet |

### 2.2 Agent Definition Details

Each agent follows the trending_topics format: YAML frontmatter (`name`, `description`, `tools`, `model`) + detailed markdown system prompt.

---

#### Agent 1: `research-planner-agent`

**Purpose:** Takes a topic and produces a structured, scored, prioritized question tree.

**Key behaviors:**
- Generates questions across 8 facets (WHO/WHAT/WHEN/WHERE/HOW/WHY/COMPARE/META)
- Scores each question on 4 dimensions: user_value (0.35), dependency_count (0.25), searchability (0.20), novelty (0.20)
- Identifies dependencies between questions (e.g., "school list" before "compare schools")
- Groups questions into research phases: breadth → depth → gap-fill
- Estimates total search budget

**Output format:** `research-plan.yaml`
```yaml
topic: "Bay Area private school K application"
created: 2026-04-06
user_context: "Parent of 4yo in SF, interested in progressive schools"
budget:
  max_searches: 50
  max_fetches: 100
phases:
  breadth:
    questions: [q1, q2, q5, q8]
  depth:
    questions: [q3, q4, q6, q7]
    depends_on: breadth
  gap_fill:
    questions: []  # populated after breadth+depth
    depends_on: depth
questions:
  - id: q1
    text: "What Bay Area private schools have K entry?"
    facet: WHAT
    scores: {user_value: 9, dependency: 8, searchability: 9, novelty: 10}
    composite: 9.0
    phase: breadth
    dependencies: []
    status: pending
    search_queries: []     # populated by research-agent
    discovered_from: seed  # seed | concept_extraction | gap_detection | user_query
    children: []           # populated as new sub-questions discovered
```

**Tools:** Read, Write, WebSearch (for initial landscape check only)

**Not responsible for:** Executing searches, fetching pages, writing wiki articles.

---

#### Agent 2: `research-agent`

**Purpose:** Executes the research plan — runs web searches, fetches pages, records everything, discovers new questions.

**Key behaviors:**
- Reads `research-plan.yaml`, processes questions in phase/priority order
- For each question: formulates 2-3 search-engine-optimized queries
- Fetches top results, converts to markdown, saves to `raw/web/`
- Runs concept extraction on each page → discovers new questions
- Deduplicates new questions against existing tree (3-layer: text, semantic, query)
- Updates `research-plan.yaml` with status, discovered children, search queries run
- Appends to `search-log.jsonl` for every search
- Classifies each source's reliability tier (L1-L5) based on domain, content signals
- Implements stop conditions: diminishing returns, budget exhaustion, coverage saturation

**Output:**
- `raw/web/*.md` — one file per fetched page with frontmatter (url, date, search_id, question_id, reliability_tier, content_hash)
- `search-log.jsonl` — every query with results, selections, skip reasons
- Updated `research-plan.yaml` — question statuses, new children, queries run

**Three sub-modes:**
1. **Breadth mode** — landscape mapping, run through high-priority seed questions
2. **Depth mode** — per-entity deep dives, fetch official + third-party sources
3. **Gap-fill mode** — targeted searches for specific missing information

**Tools:** Read, Write, Glob, Grep, WebSearch, WebFetch

**Not responsible for:** Deciding which questions to ask (planner does that), verifying claims (fact-checker does that), writing wiki articles.

---

#### Agent 3: `claim-extractor-agent`

**Purpose:** Reads raw source files and extracts structured, verifiable claims.

**Key behaviors:**
- Reads all raw source files for a topic
- Classifies each sentence: factual_claim | process_description | opinion | editorial
- For factual claims, further classifies: numerical | categorical | temporal | comparative | causal | definitional
- Assigns verification priority: must_verify (actionable) | should_verify | may_skip
- Groups claims by entity/concept (all claims about "SF School" together)
- Detects potential overreach: individual case → population generalization, single event → systemic conclusion

**Output:** `claims-register.yaml`
```yaml
claims:
  - id: c001
    text: "SF School tuition for 2026-27 is $38,500"
    type: numerical
    priority: must_verify
    sources:
      - file: raw/web/2026-04-06_sfschool-admissions.md
        tier: L1
        value: "$38,500"
    entity: sf-school
    question_id: q7

  - id: c002
    text: "Most Bay Area private schools use Ravenna Hub"
    type: categorical
    priority: should_verify
    overreach_flag: true
    overreach_reason: "Generalization from 5 observed schools"
    sources:
      - file: raw/web/2026-04-06_ravenna-overview.md
        tier: L2
        value: "widely used"
    entity: ravenna-hub
    question_id: q1
```

**Tools:** Read, Write, Glob, Grep

**Not responsible for:** Verifying claims (fact-checker), searching the web, writing wiki articles.

---

#### Agent 4: `fact-checker-agent`

**Purpose:** Verifies extracted claims, assigns confidence levels, sets permitted language.

**Two modes:**

**Mode A: Batch verification (during compile pipeline)**
- Reads `claims-register.yaml`
- For `must_verify` claims: cross-references across raw sources, optionally runs web search for corroboration
- For `overreach_flag` claims: downgrades language
- Assigns L1-L5 confidence and permitted language per claim
- Groups conflicts into dispute records

**Mode B: User-action verification (on-demand)**
- User is about to act on a specific claim (e.g., "submit by Jan 23")
- Agent re-verifies against the official source RIGHT NOW
- Returns: confirmed / changed / source unavailable

**Output:** `fact-sheet.yaml`
```yaml
verified_claims:
  - id: c001
    verdict: confirmed
    confidence: L1
    permitted_language: "SF School tuition is $38,500"  # can state directly
    sources_checked: 3
    last_verified: 2026-04-06

  - id: c002
    verdict: downgraded
    confidence: L3
    original: "Most Bay Area private schools use Ravenna Hub"
    permitted_language: "Several Bay Area private schools, including SF School and Cathedral, use Ravenna Hub"
    overreach_resolution: "Changed 'most' to named examples"

disputes:
  - id: d001
    claim: "Cathedral acceptance rate"
    positions:
      - value: "~25%"
        source: forum post 2024
        tier: L4
      - value: "~20%"
        source: forum post 2025
        tier: L4
      - value: null
        source: cathedralschool.net
        tier: L1 (no data published)
    resolution: "No official rate published. Forum estimates range 20-25%."
    permitted_language: "Acceptance rate is not officially published; parent forums estimate 20-25%"
```

**Hard rules (borrowed from trending_topics):**
- L5 (confirmed false) claims → BLOCK: cannot appear in any wiki article
- Claims about legal/immigration/medical topics require L1 or L2 source
- Overreach claims must be downgraded, never promoted
- Permitted language is BINDING — wiki-compiler must use it verbatim for verified claims

**Tools:** Read, Write, Glob, Grep, WebSearch, WebFetch

---

#### Agent 5: `wiki-compiler-agent`

**Purpose:** Synthesizes raw sources + fact sheet into structured wiki articles.

**Key behaviors:**
- Reads raw sources, fact-sheet, research-plan, and existing wiki articles
- Creates/updates wiki articles organized by type: guides, entities (schools/people/tools), concepts, claims
- For verified claims: uses permitted_language from fact-sheet verbatim
- For unverified claims: uses epistemic hedging ("reportedly", "according to [source]")
- Generates frontmatter with all required fields (title, sources, epistemic_status, confidence, valid_until, backlinks)
- Builds comparison tables where applicable
- Generates/updates `index.md` and `wiki/_index.md`
- Appends to `log.md`

**Multi-topic awareness:**
- Articles go under `topics/{topic-slug}/wiki/`
- Cross-topic concepts go under `shared/concepts/`
- Uses `[[topic:article]]` syntax for cross-topic links

**Output:** `wiki/**/*.md` articles, updated `index.md`, updated `log.md`

**Quality gates (self-enforced before writing):**
1. Every factual claim has a source attribution
2. No L5 claims present
3. Permitted language from fact-sheet used for L1-L3 claims
4. `valid_until` set for all volatile data (dates, prices)
5. At least 2 backlinks per article (or mark as stub)

**Tools:** Read, Write, Edit, Glob, Grep

---

#### Agent 6: `lint-agent`

**Purpose:** Automated health checks across the entire wiki.

**Three check categories:**

```yaml
structural:
  - broken_wikilinks
  - orphaned_pages (no incoming links)
  - missing_frontmatter_fields
  - stale_data (past valid_until)

content:
  - cross_article_contradictions
  - claims_without_sources
  - single_source_important_claims
  - empty_template_sections
  - permitted_language_violations (claim text ≠ fact-sheet permitted text)

coverage:
  - entities_mentioned_without_articles
  - unanswered_research_plan_questions
  - thin_articles (below minimum length)
  - comparison_tables_missing_entries
```

**Output:** `lint-report-YYYY-MM-DD.md` with severity tiers (error/warning/info) and actionable suggestions.

**Tools:** Read, Glob, Grep

---

#### Agent 7: `query-agent`

**Purpose:** Answers user questions against the wiki. Files valuable answers back.

**Three depth levels:**
1. **Quick** — reads `index.md` + relevant articles. Fast, no web search.
2. **Standard** — full wiki search + cross-reference. Medium.
3. **Deep** — wiki + web search + synthesis. Spawns research-agent for new data.

**Key behavior:** After answering, evaluates: "Is this answer valuable enough to persist?" If yes, creates or updates a wiki article with the new knowledge. Every exploration compounds.

**User-action gate:** If the user is about to act on a claim (deadline, price, requirement), triggers fact-checker-agent Mode B for real-time verification before answering.

**Tools:** Read, Write, Edit, Glob, Grep, WebSearch, WebFetch

---

#### Agent 8: `evolve-agent`

**Purpose:** Autonomous improvement of the wiki — finds gaps, suggests new research, identifies patterns.

**Behaviors:**
- Reviews `research-plan.yaml` for unanswered questions
- Analyzes wiki article coverage vs. question tree
- Identifies cross-entity patterns ("all progressive schools have later deadlines")
- Suggests new questions based on backlink analysis
- Flags articles needing freshness updates
- Proposes article merges for overlapping content
- Generates `evolution-suggestions.md`

**Tools:** Read, Write, Glob, Grep

---

## 3. Pipeline Orchestrator

### 3.1 Architecture

Following trending_topics pattern: **Python CLI that sequences agents, passes files between them.**

Agents do NOT invoke each other. The orchestrator:
1. Reads agent `.md` files as system prompts
2. Calls Claude API with context (input files)
3. Writes agent output to disk
4. Passes output to next agent

```
backend/
├── pipeline.py              # Main orchestrator CLI
├── config.py                # Pipeline configuration
└── tools/
    ├── manifest.py          # Source tracking with content hashes
    ├── question_tree.py     # Question CRUD, scoring, dedup
    ├── search_log.py        # Search query recording and dedup
    ├── claim_store.py       # Claim extraction storage and lookup
    └── cross_linker.py      # Wikilink insertion and backlink maintenance
```

### 3.2 Pipeline Commands

```bash
# Initialize a new topic
python -m kb.pipeline init "Bay Area private school K application" \
  --context "Parent of 4yo in SF, interested in progressive schools"

# Run full research pipeline (planner → researcher → claims → factcheck → compile → lint)
python -m kb.pipeline research --topic private-school-k

# Run individual phases
python -m kb.pipeline plan --topic private-school-k
python -m kb.pipeline search --topic private-school-k --phase breadth
python -m kb.pipeline search --topic private-school-k --phase depth
python -m kb.pipeline verify --topic private-school-k
python -m kb.pipeline compile --topic private-school-k
python -m kb.pipeline lint --topic private-school-k
python -m kb.pipeline evolve --topic private-school-k

# Ingest a single source
python -m kb.pipeline ingest --topic private-school-k --url "https://sfschool.org/admissions"
python -m kb.pipeline ingest --topic private-school-k --file ./some-article.pdf

# Query the wiki
python -m kb.pipeline query --topic private-school-k "Which schools have Spanish immersion?" --depth standard
```

### 3.3 Pipeline State Machine

```python
@dataclass
class PipelineState:
    topic_slug: str
    topic_dir: Path          # topics/{slug}/
    date: str
    phase: str               # init | plan | search | extract | verify | compile | lint | evolve
    research_plan: Path      # topics/{slug}/research-plan.yaml
    search_log: Path         # topics/{slug}/raw/search-log.jsonl
    claims_register: Path    # topics/{slug}/claims-register.yaml
    fact_sheet: Path         # topics/{slug}/fact-sheet.yaml
    budget_remaining: dict   # {searches: N, fetches: N}
    errors: list
```

### 3.4 Full Research Pipeline Flow

```
Step 1: research-planner-agent
  Input:  topic string + user context
  Output: research-plan.yaml (30-40 questions, scored, phased)

Step 2a: research-agent (breadth phase)
  Input:  research-plan.yaml (breadth questions only)
  Output: raw/web/*.md, search-log.jsonl, updated research-plan.yaml
  Loop:   Until breadth questions exhausted or budget 30% consumed

Step 2b: research-agent (depth phase)
  Input:  research-plan.yaml (depth questions, informed by breadth results)
  Output: raw/web/*.md, search-log.jsonl, updated research-plan.yaml
  Loop:   Until depth questions exhausted or budget 80% consumed

Step 2c: research-agent (gap-fill phase)
  Input:  research-plan.yaml (remaining gaps)
  Output: raw/web/*.md, search-log.jsonl, updated research-plan.yaml
  Loop:   Until gap-fill done or budget exhausted

Step 3: claim-extractor-agent
  Input:  All raw/web/*.md files
  Output: claims-register.yaml

Step 4: fact-checker-agent (batch mode)
  Input:  claims-register.yaml + raw sources
  Output: fact-sheet.yaml
  Gate:   If L5 claims found → flag, block from compilation

Step 5: wiki-compiler-agent
  Input:  raw sources + fact-sheet + research-plan
  Output: wiki/**/*.md, index.md, log.md
  Gate:   Self-enforced quality checks before writing each article

Step 6: lint-agent
  Input:  wiki/ tree
  Output: lint-report.md
  Decision: If errors found → log for human review or auto-fix pass

[Optional] Step 7: evolve-agent
  Input:  wiki/ + research-plan
  Output: evolution-suggestions.md, updated research-plan with new questions
  → Can loop back to Step 2 for additional research
```

### 3.5 Revision Loop

Following trending_topics pattern: if lint finds errors, loop back:

```
lint finds errors → categorize:
  - structural (broken links, missing frontmatter) → auto-fix by cross-linker tool
  - content (contradictions, missing sources) → re-run wiki-compiler for affected articles
  - coverage (missing articles, thin content) → add to research-plan → re-run research-agent

Max 2 revision loops before escalating to human review.
```

---

## 4. Supporting Tools (Python)

### 4.1 `manifest.py` — Source Tracking

```python
class Manifest:
    """Tracks ingested sources with content hashes for idempotent re-runs."""

    def register(self, source_path: Path, content_hash: str, produced_pages: list[str])
    def is_ingested(self, source_path: Path) -> bool
    def is_stale(self, source_path: Path) -> bool  # content changed since last ingest
    def get_uningesteed(self, raw_dir: Path) -> list[Path]
    def get_stale(self) -> list[Path]

# Storage: topics/{slug}/manifest.json
{
  "sources": {
    "raw/web/2026-04-06_sfschool-admissions.md": {
      "content_hash": "sha256:abc...",
      "ingested_at": "2026-04-06T10:24:00Z",
      "produced_pages": ["wiki/schools/sf-school.md"],
      "reliability_tier": "L1"
    }
  }
}
```

### 4.2 `question_tree.py` — Question Management

```python
class QuestionTree:
    """Manages the research question tree with scoring and dedup."""

    def add_question(self, text: str, facet: str, parent_id: str = None) -> Question
    def score(self, question: Question) -> float  # composite score
    def deduplicate(self, new_q: str) -> tuple[bool, str | None]  # (is_dup, existing_id)
    def get_next(self, phase: str) -> Question | None  # next pending question by priority
    def mark_answered(self, question_id: str, search_ids: list[str])
    def get_coverage_report(self) -> dict  # {answered: N, pending: N, by_facet: {...}}
    def add_discovered(self, text: str, discovered_from: str, parent_id: str)

# Deduplication layers:
#   1. Normalized text similarity > 0.85
#   2. Semantic subsumption check (is new_q a sub-question of an answered one?)
#   3. Query-level: would this produce the same search as an existing question?
```

### 4.3 `search_log.py` — Search Recording & Dedup

```python
class SearchLog:
    """Append-only log of all search queries for audit and deduplication."""

    def record(self, query: str, question_id: str, results: list[dict]) -> str  # returns search_id
    def is_duplicate_query(self, query: str) -> tuple[bool, str | None]  # (is_dup, past_search_id)
    def get_queries_for_question(self, question_id: str) -> list[dict]
    def get_budget_used(self) -> dict  # {searches: N, fetches: N}

# Storage: topics/{slug}/raw/search-log.jsonl (one JSON object per line)
```

### 4.4 `claim_store.py` — Claim Management

```python
class ClaimStore:
    """Stores extracted claims and their verification status."""

    def add_claim(self, text: str, type: str, sources: list, entity: str) -> str
    def get_unverified(self, priority: str = None) -> list[Claim]
    def update_verdict(self, claim_id: str, verdict: str, confidence: str, permitted_language: str)
    def get_disputes(self) -> list[Dispute]
    def get_claims_for_entity(self, entity: str) -> list[Claim]
    def get_claims_for_article(self, article_path: str) -> list[Claim]

# Storage: topics/{slug}/claims-register.yaml + topics/{slug}/fact-sheet.yaml
```

### 4.5 `cross_linker.py` — Wikilink Management

```python
class CrossLinker:
    """Manages wikilinks and backlinks across wiki articles."""

    def scan_all(self, wiki_dir: Path) -> LinkGraph
    def insert_links(self, article_path: Path, concepts: list[str])  # add [[wikilinks]]
    def update_backlinks(self, wiki_dir: Path)  # batch update all backlink frontmatter
    def find_broken(self, wiki_dir: Path) -> list[str]
    def find_orphans(self, wiki_dir: Path) -> list[str]
    def get_link_graph(self, wiki_dir: Path) -> dict  # for visualization
```

---

## 5. Claude Code Skills (Interactive Use)

These wrap the pipeline commands for interactive use within Claude Code sessions:

```
.claude/skills/
├── kb-init/SKILL.md          # /kb-init <topic>
├── kb-research/SKILL.md      # /kb-research <topic> [--phase breadth|depth|gap]
├── kb-ingest/SKILL.md        # /kb-ingest <url-or-file>
├── kb-query/SKILL.md         # /kb-query <question> [--depth quick|standard|deep]
├── kb-lint/SKILL.md          # /kb-lint [--fix]
├── kb-evolve/SKILL.md        # /kb-evolve
└── kb-verify/SKILL.md        # /kb-verify <claim> (user-action gate)
```

Each skill invokes the corresponding pipeline command and formats output for the Claude Code conversation.

---

## 6. Configuration Files

### 6.1 `CLAUDE.md` — Master Project Document

```markdown
# LLM Knowledge Base

Personal knowledge management system using LLMs as knowledge compilers.

## Quick Start
- `/kb-init "topic name"` — start a new research topic
- `/kb-research topic-slug` — run full research pipeline
- `/kb-query "your question"` — ask the wiki
- `/kb-lint` — health check

## Project Structure
[directory layout diagram]

## Agent Routing (MANDATORY)
- Plan research questions → `research-planner-agent` (NOT research-agent)
- Execute web searches → `research-agent`
- Extract claims → `claim-extractor-agent`
- Verify facts → `fact-checker-agent`
- Write wiki articles → `wiki-compiler-agent` (NOT research-agent)
- Answer questions → `query-agent`
- Health checks → `lint-agent`

## Evidence Discipline
- L1-L5 confidence levels (see SCHEMA.md for definitions)
- Permitted language is BINDING — wiki text must match fact-sheet
- L5 claims are BLOCKED from wiki
- Community sources (forums, Reddit) are intelligence only, never cited as fact

## Topic Lifecycle
- active → dormant (no research in 30d) → archived
- Volatile claims (dates, prices) expire per valid_until field
- Lint runs flag stale data automatically
```

### 6.2 `SCHEMA.md` — Wiki Conventions

```markdown
# Wiki Schema

## Article Frontmatter (required fields)
- title, created, updated, sources, tags
- epistemic_status: confirmed | likely | disputed | single-source | unknown
- confidence: L1 | L2 | L3 | L4 | L5
- valid_until: date (for volatile data)
- backlinks: list of linking articles

## Directory Conventions
- topics/{slug}/wiki/guides/ — how-to articles
- topics/{slug}/wiki/entities/ — school/person/tool profiles
- topics/{slug}/wiki/concepts/ — explanatory articles
- topics/{slug}/wiki/claims/ — disputed or noteworthy claims
- shared/concepts/ — cross-topic concepts

## Naming Rules
- Filenames: kebab-case, no dates (dates go in frontmatter)
- Wikilinks: [[article-name]] or [[topic:article-name]] for cross-topic

## Permitted Language Rules
[L1-L5 table with examples]
```

---

## 7. Directory Structure (Final)

```
llm_knowledge/
├── CLAUDE.md                          # Master project doc
├── SCHEMA.md                          # Wiki conventions
│
├── .claude/
│   ├── agents/                        # Agent definitions
│   │   ├── research-planner-agent.md
│   │   ├── research-agent.md
│   │   ├── claim-extractor-agent.md
│   │   ├── fact-checker-agent.md
│   │   ├── wiki-compiler-agent.md
│   │   ├── lint-agent.md
│   │   ├── query-agent.md
│   │   └── evolve-agent.md
│   │
│   ├── skills/                        # Claude Code slash commands
│   │   ├── kb-init/SKILL.md
│   │   ├── kb-research/SKILL.md
│   │   ├── kb-ingest/SKILL.md
│   │   ├── kb-query/SKILL.md
│   │   ├── kb-lint/SKILL.md
│   │   ├── kb-evolve/SKILL.md
│   │   └── kb-verify/SKILL.md
│   │
│   └── settings.local.json
│
├── backend/
│   ├── __init__.py
│   ├── pipeline.py                    # Main orchestrator CLI
│   ├── config.py                      # Pipeline configuration
│   └── tools/
│       ├── __init__.py
│       ├── manifest.py                # Source tracking
│       ├── question_tree.py           # Question CRUD, scoring, dedup
│       ├── search_log.py              # Search recording & dedup
│       ├── claim_store.py             # Claim extraction storage
│       └── cross_linker.py            # Wikilink management
│
├── topics/                            # Per-topic knowledge bases
│   └── private-school-k/             # Example topic
│       ├── _topic.yaml                # Topic metadata & budget
│       ├── research-plan.yaml         # Question tree
│       ├── claims-register.yaml       # Extracted claims
│       ├── fact-sheet.yaml            # Verified claims
│       ├── index.md                   # Topic index
│       ├── log.md                     # Operation log
│       ├── manifest.json              # Source tracking
│       ├── raw/
│       │   ├── search-log.jsonl       # All search queries
│       │   ├── web/                   # Fetched pages (by tier)
│       │   │   ├── official/
│       │   │   ├── journalistic/
│       │   │   ├── review/
│       │   │   └── community/
│       │   └── manual/                # Human-placed sources
│       ├── wiki/
│       │   ├── _index.md
│       │   ├── overview.md
│       │   ├── guides/
│       │   ├── entities/
│       │   ├── concepts/
│       │   └── claims/
│       ├── staging/                   # Draft articles pending review
│       └── output/                    # Reports, slides, etc.
│
├── shared/                            # Cross-topic knowledge
│   ├── concepts/
│   └── entities/
│
├── docs/                              # Design documents (existing)
│   ├── design.md
│   ├── agent-research-pipeline.md
│   ├── agent_research_qa_v1.md
│   └── implementation_plan.md
│
└── tests/                             # Test suite
    ├── test_manifest.py
    ├── test_question_tree.py
    ├── test_search_log.py
    ├── test_claim_store.py
    └── test_cross_linker.py
```

---

## 8. Implementation Phases

### Phase 1: Foundation (Week 1)
**Goal:** Skeleton that can initialize a topic and run a basic research pass.

Build:
- [ ] Directory scaffolding script
- [ ] `CLAUDE.md` and `SCHEMA.md`
- [ ] `research-planner-agent.md` — full agent definition
- [ ] `research-agent.md` — full agent definition
- [ ] `backend/tools/question_tree.py` — question CRUD, scoring
- [ ] `backend/tools/search_log.py` — append-only log
- [ ] `backend/tools/manifest.py` — source tracking
- [ ] `backend/pipeline.py` — init + plan + search commands
- [ ] `/kb-init` and `/kb-research` skills

**Milestone:** Can run `/kb-init "Bay Area private school K"` → get a research plan → run breadth search → see raw files appear in `raw/web/`.

### Phase 2: Verification (Week 2)
**Goal:** Claims extraction and fact-checking pipeline.

Build:
- [ ] `claim-extractor-agent.md` — full agent definition
- [ ] `fact-checker-agent.md` — full agent definition
- [ ] `backend/tools/claim_store.py` — claim CRUD
- [ ] Pipeline: extract + verify commands
- [ ] Permitted language enforcement
- [ ] L5 blocking gate

**Milestone:** Can extract claims from raw sources → verify → produce fact-sheet with permitted language.

### Phase 3: Compilation (Week 3)
**Goal:** Wiki article generation from verified sources.

Build:
- [ ] `wiki-compiler-agent.md` — full agent definition
- [ ] `lint-agent.md` — full agent definition
- [ ] `backend/tools/cross_linker.py` — wikilink management
- [ ] Pipeline: compile + lint commands
- [ ] Index and log auto-maintenance
- [ ] Multi-topic directory structure

**Milestone:** Full pipeline: init → plan → search → extract → verify → compile → lint. Wiki articles appear in `topics/{slug}/wiki/`.

### Phase 4: Interactive Use (Week 4)
**Goal:** Query, evolve, and incremental growth.

Build:
- [ ] `query-agent.md` — full agent definition
- [ ] `evolve-agent.md` — full agent definition
- [ ] `/kb-query`, `/kb-lint`, `/kb-evolve`, `/kb-verify`, `/kb-ingest` skills
- [ ] User-action verification gate
- [ ] Answer-filing (query results → wiki)
- [ ] Revision loops (lint → fix → re-lint)

**Milestone:** Can query the wiki, get answers, see them filed back. Can ingest new sources incrementally. Evolve agent suggests improvements.

---

## 9. Key Differences from Trending Topics Architecture

| Aspect | Trending Topics | LLM Knowledge Base | Rationale |
|--------|----------------|--------------------|----|
| **Agent count** | 22 | 8 | Knowledge base is simpler; no visual/audio/distribution pipeline |
| **Orchestrator** | Python CLI calling Claude API directly | Same pattern | Proven, auditable, file-based handoffs |
| **Pipeline shape** | Linear per episode (7 steps) | Phased with loops (plan → search cycles → verify → compile → lint → evolve) | Research is iterative; content production is linear |
| **Output versioning** | `v1/`, `v2/` directories | Git versioning + manifest hashes | Wiki is continuously edited, not versioned per-pass |
| **Skills** | None (all agents) | Skills for interactive use, agents for pipeline | Knowledge base needs both batch and interactive modes |
| **Revision trigger** | Evaluator score < threshold | Lint report errors | Different quality signals for different output types |
| **State persistence** | Per-episode output directory | Per-topic directory with long-lived YAML state files | Episodes are ephemeral; knowledge compounds |
