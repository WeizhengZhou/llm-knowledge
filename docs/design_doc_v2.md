# LLM Knowledge Base: Design Document v2

**Supersedes:** `docs/design.md`
**Date:** 2026-04-06
**Basis:** Live pipeline run on topic `bay-area-private-school-k-application` (38 questions, 44 searches, 35 raw files, 9 wiki articles)

---

## What Changed from v1

v1 described the architecture in theory. v2 documents what actually broke, what worked, and the design changes those observations demand. All v1 content not mentioned here remains in effect.

---

## 1. Pipeline Issues Found in Production

### 1.1 Output Token Cap Crashes Claim Extractor

**What happened:** The claim-extractor-agent generated 171 claims and tried to write the full YAML in a single response. It crashed with:
> `Claude's response exceeded the 32000 output token maximum`

**Root cause:** `CLAUDE_CODE_MAX_OUTPUT_TOKENS` caps agent response size. A 171-claim YAML easily exceeds 32K tokens when each claim has 6-8 fields.

**Fix (two-part):**

1. Raise the cap in your shell profile:
   ```bash
   export CLAUDE_CODE_MAX_OUTPUT_TOKENS=100000
   ```

2. The agent should write incrementally — append claims entity-by-entity rather than buffering the full output:
   ```
   for each entity group:
     extract claims for that entity
     append to claims-register.yaml immediately
   ```

---

### 1.2 Lint Agent Cannot Write Its Own Report

**What happened:** The lint-agent's tool set is `Read, Glob, Grep` only (correctly read-only for safety). But it couldn't save the lint report to `output/`, so the skill had to write it manually after the agent returned.

**Fix:** Grant the lint-agent a scoped Write permission — output directory only:
```yaml
# In .claude/agents/lint-agent.md frontmatter
tools:
  - Read
  - Glob
  - Grep
  - Write  # scoped to topics/{slug}/output/ only
```

Alternatively, the skill itself writes the agent's returned content to disk — which is cleaner since the skill already knows the output path.

---

### 1.3 Pipeline Is Fully Sequential — Very Slow

**What happened:** All 8 steps ran one-at-a-time. The depth research phase alone took ~19 minutes. Total wall time exceeded 60 minutes for a single topic.

**Opportunities for parallelism:**

| Step | Can parallelize? | How |
|------|-----------------|-----|
| Breadth research | Yes | Fan out to N agents by question group (WHO/WHAT/WHEN separately) |
| Depth research | Yes | Fan out by entity (one agent per school cluster) |
| Claim extraction | Yes | Fan out by raw file |
| Fact-checking | Partially | Fan out by entity; sequential only for cross-source dispute resolution |
| Wiki compilation | No | Needs full fact-sheet before writing any article |
| Lint | No | Needs all articles complete |

Implementing parallel research requires a shared budget ledger (see §1.5).

---

### 1.4 Wiki Compiler Reads All Raw Files — Context Risk

**What happened:** The wiki compiler was instructed to read 35+ raw `.md` files (many full web pages), `fact-sheet.yaml` (171 claims), `research-plan.yaml`, and all existing wiki articles simultaneously. This worked for 35 files but will fail at scale.

**Context budget estimate:**
- Average raw file: ~2,000 tokens
- 100 raw files = 200K tokens just for sources
- Add fact-sheet (20K) + research plan (10K) + existing wiki (30K) = 260K+
- Exceeds standard 200K context windows

**Fix — tiered input strategy for wiki compiler:**

Instead of passing raw files, pass only:
1. `fact-sheet.yaml` (verified claims with permitted language) — always included
2. Per-article: only the raw files directly cited for that article's entity/theme
3. A one-line summary index of all other raw files (not full content)

The compiler reads raw files on demand per article, not all upfront.

---

### 1.5 Budget Accounting Breaks Under Parallelism

**What happened:** Each research agent reads `search-log.jsonl` to count prior searches and self-enforce the budget stop. If two agents ran in parallel they'd both read the same count and double-spend.

**Fix — centralize budget in `pipeline-state.yaml`:**

```yaml
# topics/{slug}/pipeline-state.yaml
searches_used: 40
fetches_used: 46
budget:
  max_searches: 50
  max_fetches: 100
phase_status:
  breadth: complete
  depth: complete
  gap_fill: complete
  extraction: complete
  fact_check: complete
  compilation: complete
  lint: complete
last_run: '2026-04-06T18:30:00Z'
```

Agents read and write this file with compare-and-swap semantics (read current count, add their increment, write back). Prevents double-spend. Also gives the skill a single authoritative place to check pipeline progress.

---

### 1.6 No Inter-Step Context Handoff

**What happened:** Each agent starts cold and re-reads all files from scratch. The wiki compiler doesn't know which claims were disputed. The lint agent re-parses everything the fact-checker already parsed.

**Fix — pass a pipeline context summary between steps:**

The skill builds a small `pipeline-context.yaml` that grows as each step completes:

```yaml
breadth_summary:
  questions_answered: 12
  key_entities_found: [SF Day School, Hamlin, CAIS, ...]
  platforms_found: [Ravenna, Clarity, SSS]
depth_summary:
  questions_answered: 26
  schools_with_deadlines: 17
disputes:
  - id: d001
    description: "SF Day Clarity deadline Jan 12 vs Jan 13"
  - id: d002
    description: "Live Oak March 17 vs ISSFBA March 19"
gate_status: CLEAR
```

Each agent receives this summary as context alongside its primary inputs, eliminating redundant re-parsing.

---

### 1.7 Official School Pages Are Gated

**What happened:** Many school admissions pages returned 403s or thin content (<500 chars) when fetched with `WebFetch`. This forced fallback to L3 aggregator sources for facts that should be L1.

**Root causes:**
- **Bot detection** — WebFetch sends a non-browser User-Agent; Cloudflare/Akamai block it
- **JS rendering** — Modern school sites are SPAs; `WebFetch` gets the pre-JS shell, not the rendered content
- **Cookie requirements** — Some pages require an active browser session

**Fix — Chrome DevTools MCP fallback:**

The Chrome DevTools MCP (`mcp__chrome-devtools__*`) provides a real headed Chrome session: real UA, full JS execution, cookies preserved. All three gatekeeping mechanisms are bypassed.

**Fetching strategy (ordered):**

```
1. Try WebFetch — fast, no browser overhead
2. If response is <500 chars OR contains bot-detection signals
   ("cf-ray", "captcha", "enable JavaScript", "checking your browser"):
   → Fall back to Chrome MCP:
     a. mcp__chrome-devtools__new_page(url)
     b. mcp__chrome-devtools__wait_for(selector="main", timeout=5000)
     c. mcp__chrome-devtools__take_snapshot(filePath="raw/web/{tier}/...")
        # take_snapshot uses the a11y tree — preserves heading hierarchy
        # and table structure better than evaluate_script(innerText)
     d. mcp__chrome-devtools__close_page()
3. If both fail → record as fetch_failed in search-log.jsonl, skip
```

**Prerequisite:** Chrome must be running with remote debugging enabled:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --no-first-run &
```

**Why `take_snapshot` over `evaluate_script(innerText)`:**
`take_snapshot` uses the accessibility tree, which preserves semantic structure (headings, tables, lists). Raw `innerText` is a flat dump that loses the structural cues the claim-extractor relies on to distinguish deadlines from fees from descriptions.

**Agent definition change:** Add `mcp__chrome-devtools__*` to the research-agent's allowed tools.

---

## 2. Design Improvements (Beyond Bug Fixes)

### 2.1 Human-in-the-Loop Checkpoint After Breadth

**Problem:** A bad breadth phase (wrong schools, wrong region) propagates through all 7 remaining steps with no opportunity to course-correct. Budget is wasted.

**Fix:** The skill pauses after Step 2 and presents a summary:

```
Breadth complete. Found 15 schools, 3 platforms, 2 consulting firms.
Key entities: SF Day, Hamlin, CAIS, Convent & Stuart Hall, Live Oak...

Proceed with depth research? (or type corrections)
>
```

This costs ~10 seconds of human time but can save 45 minutes of misdirected depth research.

---

### 2.2 Replace `valid_until` Dates with Volatility Classes

**Problem:** The wiki compiler set `valid_until: 2026-03-27` (the enrollment deadline) which immediately became stale. Hard-coded expiry dates are always wrong.

**Fix — encode volatility type instead:**

```yaml
volatile: annual        # re-verify each admissions cycle (Sept-Oct)
volatile: evergreen     # school mission, philosophy — rarely changes
volatile: none          # historical facts — never stale
volatile: cycle_bound   # specific to 2025-26 cycle; archive after March 26
```

Lint agent checks by volatility class, not by comparing dates:
- `annual` → flag after 12 months
- `cycle_bound` → flag after cycle close date passes
- `evergreen` → flag after 36 months
- `none` → never flag

---

### 2.3 Diff-Aware Wiki Compiler

**Problem:** On re-runs (after gap-fill or a new ingest), the compiler rewrites articles from scratch. This loses manual edits and creates noisy diffs.

**Fix:** The compiler reads each existing article first and compares its current claims against the updated fact-sheet. It only rewrites sections where:
- A verified claim changed (different permitted language)
- A new claim was added for this entity
- A claim was upgraded/downgraded in confidence

Sections with no fact-sheet changes are left untouched.

---

### 2.4 Merge Claim Extractor and Fact Checker

**Problem:** Two sequential agents both read all the same raw files. The claim-extractor classifies claims without looking at cross-source agreement. The fact-checker then re-reads everything to do the cross-reference it should have done first.

**Fix — unified extraction-and-verification pass:**

```
For each source file:
  1. Extract candidate claims (type + priority)
  2. Immediately look for corroboration in already-processed files
  3. Assign provisional confidence on the spot
  4. Flag disputes as they emerge

Output: claims-register.yaml + fact-sheet.yaml in one pass
```

This halves the file I/O, eliminates one agent invocation, and produces better confidence scores because cross-referencing happens at extraction time, not after.

---

### 2.5 Auto-Run Cross-Linker After Wiki Compilation

**Problem:** After every pipeline run, all `backlinks` arrays are empty because the cross-linker tool is never called automatically.

**Fix:** The skill calls `backend/tools/cross_linker.py` as a post-compilation step, before lint. This is a one-line addition to the skill:

```bash
# In kb-research skill, after wiki-compiler-agent completes:
python -m backend.tools.cross_linker topics/{slug}/wiki/
```

---

### 2.6 Search Query Deduplication

**Problem:** Multiple depth questions about different schools all triggered similar generic queries ("Bay Area private school K admissions process") which returned overlapping results and wasted budget.

**Fix:** Before executing a search query, the research agent checks `search-log.jsonl` for semantic near-duplicates:
- Exact match: skip entirely
- High overlap (same keywords + entity): reuse the cached result from an earlier search
- Novel: proceed

A simple keyword-overlap check (Jaccard similarity > 0.7 = duplicate) is sufficient without needing embeddings.

---

### 2.7 Add `/kb-update` Skill for Cycle Refreshes

**Problem:** Each September, ~30 temporal claims (deadlines, tuitions, class sizes) need re-verification without re-running the full pipeline.

**New skill:** `/kb-update {slug} --volatile annual`

Pipeline:
1. Read `fact-sheet.yaml` — collect all claims with `volatile: annual`
2. Re-run WebSearch/WebFetch (or Chrome MCP) for each entity's official source
3. Compare new content against existing permitted language
4. Flag diffs → human review
5. Auto-update claims where the change is unambiguous (e.g., deadline shifted by a few days)
6. Update `valid_since` field with current date

This makes annual maintenance a 5-minute operation instead of a full re-research.

---

### 2.8 Coverage Gap: `shared/` Namespace Never Used

**Problem:** The `shared/` directory exists in the schema for cross-topic knowledge but nothing writes to or reads from it. When a second topic is initialized (e.g., "East Bay private middle school"), the agents re-research ISSFBA, Ravenna, and Clarity from scratch.

**Fix:**

- After wiki compilation, the skill identifies articles that are topic-agnostic (platforms, organizations, financial mechanisms)
- These are copied/linked to `shared/wiki/`
- The research-planner-agent checks `shared/wiki/` before generating questions — if ISSFBA is already there, don't re-research it
- The wiki compiler checks `shared/wiki/` first and [[wikilinks]] to shared articles instead of duplicating content

---

## 3. Revised Pipeline Flow

```
                    ┌─────────────────────────────────────────┐
                    │  /kb-research {slug}                     │
                    └─────────────────────────────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 1  │  research-planner-agent            │  (skip if plan exists)
                    │  → research-plan.yaml              │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 2  │  research-agent (breadth)          │  parallel by facet group
                    │  WebFetch → Chrome MCP fallback    │
                    │  → raw/web/ + search-log.jsonl     │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
         CHECKPOINT │  Human review: "Found N entities,  │  ← NEW
                    │  proceed?"                         │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 3  │  research-agent (depth)            │  parallel by entity cluster
                    │  WebFetch → Chrome MCP fallback    │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 4  │  research-agent (gap-fill)         │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 5  │  claim-extractor + fact-checker    │  MERGED ← NEW
                    │  (write incrementally per entity)  │
                    │  → claims-register.yaml            │
                    │  → fact-sheet.yaml                 │
                    └─────────────────┬─────────────────┘
                                      │
                              gate_status == CLEAR?
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 6  │  wiki-compiler-agent               │  diff-aware ← NEW
                    │  (tiered input: fact-sheet first,  │
                    │   raw files on demand per article) │
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 7  │  cross_linker.py (auto)            │  ← NEW (was manual)
                    └─────────────────┬─────────────────┘
                                      │
                    ┌─────────────────▼─────────────────┐
            Step 8  │  lint-agent                        │  can now write report
                    │  → output/lint-report-YYYY-MM-DD   │
                    └─────────────────────────────────────┘
```

---

## 4. Agent Tool Matrix (Updated)

| Agent | Tools | Notes |
|-------|-------|-------|
| research-planner-agent | Read, Write, WebSearch | Unchanged |
| research-agent | Read, Write, WebSearch, WebFetch, `mcp__chrome-devtools__*` | Add Chrome MCP |
| claim-extractor-agent | Read, Write, Glob, Grep | Write incrementally (per entity) |
| fact-checker-agent | Read, Write, Glob, Grep, WebSearch, WebFetch | Unchanged |
| wiki-compiler-agent | Read, Write, Edit, Glob, Grep | Add diff-aware editing |
| lint-agent | Read, Write(output/ only), Glob, Grep | Add scoped Write |
| query-agent | Read, Write, Edit, Glob, Grep, WebSearch, WebFetch | Unchanged |
| evolve-agent | Read, Write, Glob, Grep | Unchanged |

---

## 5. Open Issues Not Yet Resolved

| Issue | Status | Notes |
|-------|--------|-------|
| Parallel research with shared budget ledger | Design only | Needs `pipeline-state.yaml` implementation |
| Merged claim-extractor + fact-checker | Design only | Single-pass extraction is a significant refactor |
| `shared/` namespace population | Design only | Need to define "topic-agnostic" heuristic |
| Chrome MCP availability | Blocked | Requires Chrome running with `--remote-debugging-port=9222` |
| `/kb-update` skill | Not built | High value for annual admissions cycle refreshes |
| Progress logging during pipeline run | Not built | `tail -f log.md` workaround exists today |

---

## 6. What Worked Well (Keep As-Is)

- **8-facet question tree** (WHO/WHAT/WHEN/WHERE/HOW/WHY/COMPARE/META) — covered the topic comprehensively with no obvious blind spots
- **Reliability tiers** (official/news/aggregator/community) — clean separation that the fact-checker used correctly to assign L1-L4 confidence
- **`permitted_language` binding** — wiki compiler consistently used verbatim fact-sheet language for verified claims; no violations found in lint
- **Budget stop conditions** — 30%/80% breadth/depth stops prevented runaway search spending
- **Dispute documentation** — both disputes (SF Day deadline conflict, Live Oak date deviation) were correctly identified, preserved, and surfaced in the wiki rather than silently resolved
- **Coordinated decision date discovery** — the ISSFBA March 19 norm emerged naturally from cross-referencing multiple school pages; not a pre-planned question
