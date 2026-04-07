# LLM Knowledge Base

Personal knowledge management system using LLMs as knowledge compilers. Instead of RAG, the system incrementally builds a persistent, human-readable markdown wiki that compounds over time.

Inspired by [Karpathy's LLM Knowledge Bases](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## Quick Start

```bash
# Initialize a new research topic (scaffolds directory + generates question tree)
/kb-init "Bay Area private school K application"

# Run full research pipeline (breadth → checkpoint → depth → gap → extract → verify → compile → lint)
/kb-research private-school-k

# Ingest a single source into an existing topic
/kb-ingest --topic private-school-k --url https://sfschool.org/admissions

# Query the wiki
/kb-query --topic private-school-k "Which schools have Spanish immersion?"

# Health check
/kb-lint --topic private-school-k

# Agent-driven improvement (gap analysis, freshness, patterns)
/kb-evolve --topic private-school-k

# Real-time verify a claim before acting on it
/kb-verify --topic private-school-k "SF School deadline is January 23"

# Re-verify volatile claims for annual refresh (run each September)
/kb-update private-school-k
/kb-update private-school-k --volatile all
/kb-update private-school-k --entity hamlin-school
```

## Architecture

**Claude Code-native.** Skills orchestrate agents. Agents use their own tools (Read, Write, WebSearch, WebFetch) autonomously. No Python LLM-calling orchestrator.

- **Skills** (`.claude/skills/`) — slash commands that invoke the right agents in the right order with file-path context
- **Agents** (`.claude/agents/`) — specialized roles with system prompts; each reads its own inputs and writes its own outputs
- **`backend/pipeline.py`** — directory scaffolding only (`init` command); no LLM calls
- **`backend/tools/`** — Python data tools used by tests and optionally by agents via Bash

## Project Structure

```
llm_knowledge/
├── CLAUDE.md                    # This file
├── SCHEMA.md                    # Wiki conventions and article schema
├── .claude/
│   ├── agents/                  # 8 agent definitions (markdown system prompts)
│   └── skills/                  # 7 Claude Code slash commands
├── backend/
│   ├── pipeline.py              # Directory scaffolding only (init command)
│   ├── config.py                # Configuration constants
│   └── tools/                   # Supporting Python tools
│       ├── manifest.py          # Source tracking with content hashes
│       ├── question_tree.py     # Question CRUD, scoring, dedup
│       ├── search_log.py        # Search query recording & dedup
│       ├── claim_store.py       # Claim extraction & verification storage
│       └── cross_linker.py      # Wikilink & backlink management
├── topics/                      # Per-topic knowledge bases
│   └── {topic-slug}/
│       ├── _topic.yaml          # Topic metadata & budget
│       ├── research-plan.yaml   # Question tree
│       ├── claims-register.yaml # Extracted claims
│       ├── fact-sheet.yaml      # Verified claims with permitted language
│       ├── index.md             # Topic index
│       ├── log.md               # Operation log
│       ├── manifest.json        # Source tracking
│       ├── raw/                 # Immutable source material
│       ├── wiki/                # LLM-compiled articles
│       ├── staging/             # Draft articles pending review
│       └── output/              # Reports, slides, etc.
├── shared/                      # Cross-topic knowledge
├── docs/                        # Design documents
└── tests/                       # Test suite
```

## Agent Routing (MANDATORY)

Every task has a designated agent. Do NOT use generic agents for knowledge work.

| Task | Agent | NOT |
|------|-------|-----|
| Plan research questions | `research-planner-agent` | research-agent |
| Execute web searches | `research-agent` | wiki-compiler-agent |
| Extract claims from sources | `claim-extractor-agent` | fact-checker-agent |
| Verify facts, assign confidence | `fact-checker-agent` | research-agent |
| Write/update wiki articles | `wiki-compiler-agent` | research-agent |
| Health checks | `lint-agent` | wiki-compiler-agent |
| Answer user questions | `query-agent` | research-agent |
| Suggest improvements | `evolve-agent` | lint-agent |

## Pipeline Flow

```
research-planner → research-agent (breadth → depth → gap-fill)
  → claim-extractor → fact-checker → wiki-compiler → lint-agent
  → [optional] evolve-agent → loop back to research-agent
```

## Evidence Discipline

### Confidence Levels (L1-L5)

| Level | Definition | Permitted Language |
|-------|-----------|-------------------|
| L1 | Multi-source confirmed | State as fact: "Tuition is $38,500" |
| L2 | Single authoritative source | Attribute: "According to SFChronicle..." |
| L3 | Aggregator/review platform | Qualify: "Niche rates the school 4.2/5" |
| L4 | Community/forum signal | Anecdote only: "Some parents on forums report..." |
| L5 | Confirmed false or unverifiable | BLOCKED: cannot appear in wiki |

### Hard Rules

- **Permitted language is BINDING** — wiki text must match fact-sheet for verified claims
- **L5 claims are BLOCKED** from wiki articles
- **Community sources** (forums, Reddit) are intelligence inputs, never cited as fact
- **Overreach detection** — flag generalizations from small samples or individual cases
- **Conflicts preserved** — when sources disagree, create claims/ article documenting both positions

## Topic Lifecycle

- `active` → `dormant` (no research in 30 days) → `archived`
- Volatile claims use `volatile:` class (annual/cycle_bound/evergreen/none) — not hard `valid_until` dates
- Lint agent flags stale data by volatility class automatically
- Run `/kb-update <slug>` each September to re-verify annual claims for the new admissions cycle

## Changelog and Git Snapshots (MANDATORY)

Every agent that modifies wiki articles, fact-sheets, or design docs MUST:

### 1. Append to `topics/{slug}/CHANGELOG.md` before writing

Format:
```markdown
## 2026-04-06 — wiki-compiler-agent

**Changed:**
- `wiki/entities/sf-school.md` — updated tuition from $47,200 to $48,500 (new cycle data)
- `wiki/guides/application-timeline.md` — rewrote January deadlines section

**Added:**
- `wiki/entities/harker-school.md` — new entity article

**Reason:** gap-fill research pass + kb-update annual refresh
```

If `CHANGELOG.md` does not exist for the topic, create it with this header:
```markdown
# Changelog — {topic name}

_Append-only log of all wiki modifications. Each entry records what changed, what was added/removed, and why._
```

### 2. Git commit after every pipeline run

After a full `/kb-research` or `/kb-update` run completes (after lint), commit the changes:

```bash
git add topics/{slug}/
git commit -m "kb: {slug} — {phase} pipeline run {YYYY-MM-DD}

- Questions answered: N
- Articles created/updated: N
- Claims verified: N
- Gate status: CLEAR/BLOCKED"
```

This gives you a restore point if a future compile run corrupts or overwrites content.

### 3. Design docs and agent definitions

When modifying `.claude/agents/*.md`, `.claude/skills/**/*.md`, `SCHEMA.md`, or `CLAUDE.md`:
- Bump the version number in the file footer (e.g., `v1.0` → `v2.0`)
- Commit immediately: `git commit -m "docs: update {filename} — {brief reason}"`

## Skills Reference

| Skill | What It Does | Agents Invoked |
|-------|-------------|----------------|
| `/kb-init "<topic>"` | Scaffold directory + generate question tree | `research-planner-agent` |
| `/kb-research <slug>` | Full research pipeline | `research-planner` → `research-agent` × 3 → `claim-extractor` → `fact-checker` → `wiki-compiler` → `lint-agent` |
| `/kb-research <slug> --phase breadth\|depth\|gap` | Single research phase only | `research-agent` |
| `/kb-ingest <slug> --url <url>` | Add one web source | `research-agent` → `claim-extractor` → `fact-checker` → `wiki-compiler` |
| `/kb-ingest <slug> --file <path>` | Add one local file | `claim-extractor` → `fact-checker` → `wiki-compiler` |
| `/kb-query <slug> "<question>"` | Answer from wiki (+ optional web) | `query-agent` |
| `/kb-lint <slug>` | Health check report | `lint-agent` |
| `/kb-evolve <slug>` | Gap + freshness + pattern analysis | `evolve-agent` |
| `/kb-update <slug>` | Re-verify volatile claims; update wiki (annual refresh) | `fact-checker-agent` → `wiki-compiler-agent` |
| `/kb-verify <slug> "<claim>"` | Real-time re-verification before acting | `fact-checker-agent` (user-action mode) |

## Scaffolding CLI (init only)

```bash
# The only Python CLI command needed — everything else uses skills
python -m backend.pipeline init "topic name" [--context "user context"]
```
