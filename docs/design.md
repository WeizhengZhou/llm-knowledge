# LLM Knowledge Base: Design Document

## 1. Overview

A personal knowledge management system where LLMs act as **knowledge compilers** rather than stateless Q&A tools. Instead of traditional RAG (retrieve-answer-forget), the system incrementally builds a persistent, human-readable markdown wiki that compounds over time.

Inspired by Andrej Karpathy's [LLM Knowledge Bases](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern (April 2026): *"A large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge."*

### Design Principles

- **Human-readable first** — all knowledge stored as markdown, no opaque vectors
- **LLM as compiler** — the agent writes/maintains the wiki; the human curates sources and asks questions
- **Compounding returns** — every query, exploration, and ingestion enriches the system
- **Immutable sources** — raw inputs are never modified; the wiki is a derived artifact
- **Minimal tooling** — flat markdown directories suffice at personal scale; no database required

---

## 2. What is "LLM Knowledge"?

LLM Knowledge is a structured, interlinked collection of markdown documents that sits between you and your raw sources. The LLM reads raw material (papers, articles, transcripts, data) and **compiles** it into encyclopedia-style articles with cross-references, summaries, and indices.

Key distinction from RAG:
| Aspect | RAG | LLM Knowledge Base |
|--------|-----|-------------------|
| Storage | Vector embeddings | Human-readable markdown |
| Relationships | Emergent (embedding similarity) | Explicit (backlinks, indices) |
| State | Stateless per query | Persistent, compounding |
| Maintenance | Re-embed periodically | Continuous linting/updates |
| Scale sweet spot | Large heterogeneous corpora | Hundreds to low thousands of curated docs |
| Human readability | Opaque | Fully browsable |

---

## 3. Architecture

### 3.1 Directory Structure

```
knowledge/
├── SCHEMA.md              # Agent instructions: structure conventions, workflows
├── index.md               # Auto-maintained catalog by category (one-line summaries)
├── log.md                 # Append-only operation log
│                          #   Format: ## [YYYY-MM-DD] operation | Title
├── manifest.json          # Tracks ingested sources (path, hash, timestamp, produced pages)
│
├── raw/                   # IMMUTABLE — source of truth, never modified by LLM
│   ├── articles/          # Web articles (via clipper or fetch)
│   ├── papers/            # Academic papers, arXiv
│   ├── transcripts/       # YouTube, podcast, meeting transcripts
│   ├── data/              # Datasets, CSV, JSON
│   └── misc/              # Anything else
│
├── wiki/                  # LLM-OWNED — agent is primary author/editor
│   ├── concepts/          # Encyclopedia-style concept articles
│   ├── people/            # Person profiles
│   ├── tools/             # Tool/technology profiles
│   ├── claims/            # Disputed or noteworthy claims with epistemic status
│   └── _index.md          # Wiki-specific index with backlink counts
│
├── staging/               # AGENT SANDBOX — drafts before promotion to wiki/
│   └── (draft articles awaiting human review or quality gate)
│
├── output/                # Derived artifacts
│   ├── reports/           # Research reports, summaries
│   ├── slides/            # Marp slide decks
│   └── charts/            # Visualizations
│
└── .meta/                 # System metadata
    ├── provenance/        # Per-article source attribution records
    └── lint-reports/      # Historical lint results
```

### 3.2 Key Files

**SCHEMA.md** — the "constitution" for the agent. Defines:
- Directory conventions and naming rules
- Frontmatter schema for wiki articles
- Workflow definitions (ingest, compile, query, lint)
- Quality standards and verification requirements

**index.md** — entry point for both humans and LLM queries. Auto-maintained catalog organized by category with one-line descriptions. This is what the LLM reads first when answering questions.

**log.md** — append-only chronological record of all operations. Enables auditing and understanding how knowledge evolved.

**manifest.json** — tracks every ingested source with content hashes, enabling:
- Delta computation (only process new/changed sources)
- Staleness detection (source changed since last compilation)
- Idempotent re-runs

### 3.3 Article Frontmatter Schema

```yaml
---
title: "Article Title"
created: 2026-04-06
updated: 2026-04-06
sources:
  - raw/articles/source-article.md
  - raw/papers/related-paper.pdf
tags: [concept, machine-learning, attention]
epistemic_status: confirmed  # confirmed | likely | disputed | single-source | unknown
confidence: L2               # L1 (multi-source verified) to L5 (unverifiable)
backlinks:
  - concepts/transformer.md
  - people/vaswani.md
---
```

---

## 4. Core Operations

### 4.1 Ingest

**Trigger:** Human places source material in `raw/` or provides a URL.

**Process:**
1. Check manifest — skip if source already ingested and unchanged (content hash match)
2. Read raw source, extract key takeaways
3. For each concept/entity identified:
   - If wiki article exists: update with new information, add source to frontmatter
   - If new: create article in `staging/` (or `wiki/` if auto-promote enabled)
4. Generate/update backlinks across all affected articles
5. Update `index.md` and `log.md`
6. Update `manifest.json` with source hash and produced pages

**Data injection methods:**
- Obsidian Web Clipper (browser extension -> markdown)
- Direct file placement in `raw/`
- URL fetch by agent (`/ingest <url>`)
- Bulk import from directories
- Claude Code conversation history mining

### 4.2 Compile

**Trigger:** On-demand or after batch ingest.

**Process:**
1. Scan `raw/` for uncompiled sources (manifest delta)
2. For each uncompiled source, run ingest pipeline
3. After all sources processed, run cross-linker:
   - Detect mentions of existing concepts across all new/updated articles
   - Insert `[[wikilinks]]` where appropriate
   - Update backlink counts in `_index.md`
4. Generate `overview.md` — evolving synthesis of the entire knowledge base

### 4.3 Query

**Trigger:** Human asks a question.

**Depth levels:**
| Level | Method | Speed |
|-------|--------|-------|
| Quick | Read `index.md` + relevant wiki articles only | Fast |
| Standard | Full wiki search + cross-reference | Medium |
| Deep | Multi-agent: wiki search + parallel web search + synthesis | Slow |

**Critical behavior:** Query results are **filed back into the wiki** as new pages or updates to existing pages. Every exploration compounds.

### 4.4 Lint

**Trigger:** Periodic (scheduled) or on-demand.

**Checks:**
- **Structural:** Broken links, orphaned pages, missing frontmatter fields
- **Consistency:** Contradictions between articles, date mismatches
- **Freshness:** Sources changed since last compilation (hash mismatch)
- **Coverage:** Concepts mentioned but lacking dedicated articles
- **Quality:** Articles below minimum length, missing sources, low confidence claims

**Output:** Severity-tiered report saved to `.meta/lint-reports/lint-YYYY-MM-DD.md`

### 4.5 Evolve

**Trigger:** On-demand.

**Process:**
- Identify research gaps from concept graph analysis
- Suggest new article opportunities from backlink patterns
- Propose merges for overlapping articles
- Flag stale claims for re-verification via web search

---

## 5. Human vs. Agent Responsibilities

| Responsibility | Human | Agent |
|---------------|-------|-------|
| Source curation | Selects what to ingest | Processes and structures |
| Question formulation | Asks research questions | Answers and files back |
| Quality oversight | Reviews staged articles, resolves disputes | Flags issues via lint |
| Writing wiki articles | Rarely/never | Primary author |
| Cross-referencing | Never | Automatic |
| Index maintenance | Never | Automatic |
| Consistency checking | Reviews lint reports | Runs lint passes |
| Editorial direction | Chooses topics, depth, scope | Executes within guidelines |

---

## 6. Agent-Driven Research & Data Injection

When the agent performs independent research (e.g., during deep queries or evolve passes):

1. **Web search** — agent searches, evaluates relevance, downloads to `raw/`
2. **Source attribution** — every fetched resource gets a provenance record:
   ```json
   {
     "source_url": "https://...",
     "fetched_at": "2026-04-06T12:00:00Z",
     "fetched_by": "agent",
     "query_context": "What is the relationship between X and Y?",
     "content_hash": "sha256:..."
   }
   ```
3. **Staging gate** — agent-sourced articles go to `staging/` by default
4. **Confidence tagging** — agent-generated content starts at L3 (single agent source) unless corroborated

### Auto-promote vs. Stage

| Source type | Default destination | Rationale |
|------------|-------------------|-----------|
| Human-curated raw source | `wiki/` (auto-promote) | Human already vetted the source |
| Agent web search result | `staging/` | Needs human review or corroboration |
| Lint-driven gap fill | `staging/` | May contain hallucinated connections |
| Query answer filed back | `wiki/` | Derived from existing trusted wiki content |

---

## 7. Verification & Accuracy

### 7.1 Epistemic Status Framework

Every claim in the wiki carries an epistemic status:

| Status | Meaning | Action required |
|--------|---------|----------------|
| `confirmed` | Multiple independent sources agree | None |
| `likely` | Single reliable source, consistent with other knowledge | Low priority verification |
| `disputed` | Sources conflict on this claim | Surface both positions, flag for review |
| `single-source` | Only one source, not independently verified | Seek corroboration |
| `unknown` | No reliable source found | Mark clearly, deprioritize in answers |

### 7.2 Confidence Levels

| Level | Description | Examples |
|-------|-------------|---------|
| L1 | Verified by 3+ independent authoritative sources | Well-established facts |
| L2 | Verified by 2 sources or 1 authoritative source | Recent papers, official docs |
| L3 | Single source, agent-generated, or unverified | Blog posts, agent web searches |
| L4 | Conflicting evidence exists | Disputed claims |
| L5 | Unverifiable or speculative | Predictions, opinions |

### 7.3 Handling Conflicting Sources

When sources disagree:

1. **Do not silently resolve** — preserve the conflict explicitly
2. Create a `claims/` article documenting:
   - Each position with its source
   - Date of each claim
   - Any resolution criteria (e.g., "will be resolved when paper X is published")
3. Set `epistemic_status: disputed` and `confidence: L4`
4. Cross-link from all relevant concept articles
5. Flag in lint report for periodic re-evaluation

### 7.4 Provenance Tracking

Each wiki article maintains provenance in `.meta/provenance/`:

```json
{
  "article": "wiki/concepts/attention-mechanism.md",
  "propositions": [
    {
      "claim": "Attention was introduced in Bahdanau et al. 2014",
      "sources": ["raw/papers/bahdanau2014.pdf"],
      "source_hashes": ["sha256:abc..."],
      "compiled_at": "2026-04-06",
      "status": "confirmed"
    }
  ]
}
```

Content hashes enable **staleness detection**: if a source file changes, all derived propositions are flagged for re-verification.

### 7.5 Verification Strategies

| Strategy | When to use | Implementation |
|----------|------------|----------------|
| Cross-source check | Default for all claims | Compare across raw sources |
| Web verification | For agent-generated content or stale claims | Agent web search during lint |
| Human review gate | High-stakes or L4+ claims | Route to `staging/` with flag |
| Temporal decay | Time-sensitive claims (versions, prices, dates) | Auto-flag after configurable TTL |
| Authority weighting | Conflicting sources of different reliability | Prefer primary sources, peer-reviewed > blogs |

---

## 8. Scaling Considerations

### 8.1 When This Pattern Works

- Personal research (1 person, 1-N topics)
- Small team knowledge sharing
- Hundreds to low thousands of curated documents
- ~100-500 wiki articles, up to ~1M words

### 8.2 When to Augment or Switch

| Signal | Recommendation |
|--------|---------------|
| >1000 wiki articles | Add SQLite FTS5 search index |
| >5000 articles | Consider hybrid: markdown wiki + vector search for retrieval |
| Multi-team with conflicting knowledge | Add per-team namespaces + reconciliation workflow |
| Real-time data needs | Not suitable; supplement with live data feeds |
| Regulatory/compliance requirements | Add formal review workflows, access controls |

### 8.3 Performance Optimizations

- **Delta processing** via manifest — never re-ingest unchanged sources
- **Index-first queries** — read `index.md` before loading full articles
- **Lazy backlink resolution** — update backlinks in batch, not per-ingest
- **Ephemeral wikis** — spin up disposable wikis for temporary research tasks

---

## 9. Tooling

### 9.1 Core Stack

| Tool | Role |
|------|------|
| **Obsidian** | Wiki viewer, graph visualization, browsing |
| **Claude Code** | LLM agent for all wiki operations |
| **Markdown** | Universal storage format |
| **Git** | Version control for all wiki content |

### 9.2 Optional Enhancements

| Tool | Role |
|------|------|
| SQLite FTS5 | Full-text search at scale |
| Marp | Slide deck generation from wiki content |
| Dataview | Dynamic queries within Obsidian |
| Web Clipper | Browser-to-raw-directory pipeline |
| MCP tools | Agent access to external data sources |

---

## 10. Existing Implementations

| Project | Description | URL |
|---------|-------------|-----|
| Karpathy's gist | Original pattern definition | [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
| Ar9av/obsidian-wiki | Multi-agent framework with delta tracking, cross-linker, tag taxonomy | [github](https://github.com/Ar9av/obsidian-wiki) |
| rvk7895/llm-knowledge-bases | Claude Code plugin with deep research, query depth levels | [github](https://github.com/rvk7895/llm-knowledge-bases) |
| kfchou/wiki-skills | Lightweight Claude Code skills: init, ingest, query, lint, update | [github](https://github.com/kfchou/wiki-skills) |
| ussumant/llm-wiki-compiler | Markdown-to-wiki compiler plugin | [github](https://github.com/ussumant/llm-wiki-compiler) |

### Key differentiators across implementations:

- **Ar9av/obsidian-wiki** stands out for multi-agent support (Claude, Cursor, Windsurf, Codex, Gemini), manifest-based delta tracking, and conversation history ingestion
- **rvk7895/llm-knowledge-bases** adds deep research with parallel agent pipelines
- **kfchou/wiki-skills** is the simplest and most portable

---

## 11. Open Questions & Future Directions

### Unsolved Problems

1. **Verification at scale** — LLM fact-checking accuracy is not yet reliable for autonomous operation; human-in-the-loop remains necessary for high-stakes content
2. **Enterprise deployment** — conflicting tribal knowledge across teams is a known hard problem
3. **Knowledge decay** — how aggressively should stale claims be flagged or removed?
4. **Hallucination contamination** — agent-generated content can introduce subtle errors that compound through cross-references

### Future Directions

1. **Fine-tuning pathway** — use the curated wiki as training data for domain-specific models, encoding the knowledge base into model weights
2. **Multi-wiki federation** — cross-reference across separate knowledge bases with different trust levels
3. **Collaborative wikis** — multiple humans + agents with conflict resolution protocols
4. **Structured data extraction** — generate machine-readable schemas (JSON-LD, RDF) alongside markdown
5. **Temporal versioning** — track how understanding of a concept evolves over time, not just current state

---

## 12. Implementation Plan

### Phase 1: Foundation
- Set up directory structure and SCHEMA.md
- Implement `/ingest` skill (single source -> wiki articles)
- Implement `index.md` auto-maintenance
- Add manifest tracking for idempotent re-runs

### Phase 2: Core Loop
- Implement `/compile` (batch ingest + cross-linker)
- Implement `/query` with answer-filing
- Implement `/lint` with severity-tiered reports
- Add `log.md` for all operations

### Phase 3: Quality & Trust
- Add epistemic status and confidence levels to frontmatter
- Implement provenance tracking in `.meta/`
- Add staging area with promotion gates
- Implement content hash-based staleness detection

### Phase 4: Advanced
- Deep query with parallel agent web search
- Evolve pass (gap analysis, merge suggestions)
- SQLite FTS5 search for scale
- Obsidian graph view integration

---

## References

- [Karpathy's LLM Knowledge Bases gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [DAIR.AI — LLM Knowledge Bases](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy)
- [Fabian Williams — Building a Second Brain That Compounds](https://www.fabswill.com/blog/building-a-second-brain-that-compounds-karpathy-obsidian-claude)
- [TechBuddies — Markdown-First Alternative to RAG](https://www.techbuddies.io/2026/04/04/inside-karpathys-llm-knowledge-base-a-markdown-first-alternative-to-rag-for-autonomous-archives/)
- [VentureBeat — Karpathy's LLM Knowledge Base Architecture](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
- [PMC — Perils and Promises of Fact-Checking with LLMs](https://pmc.ncbi.nlm.nih.gov/articles/PMC10879553/)
