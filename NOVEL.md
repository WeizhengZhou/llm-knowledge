# Fiction Writing Pipeline

A clean fork of the `/kb-*` factual knowledge-base pipeline for writing **novels and fiction**. Shares the Claude Code skills-invoke-agents harness, staging → graduation flow, and git/CHANGELOG discipline. Replaces evidence discipline with **canon discipline** and collapses the single wiki-critic pass into four distinct **revision stages** (developmental → line → copy → proof) that run in order at different points in time.

Inspired by professional novelist workflows: Save the Cat / Snowflake / Story Grid for structure, Scrivener's scene-as-unit-of-work convention, Sanderson's ending-first "Points on the Map" outlining, and the industry-standard four-stage edit progression.

## Quick Start

```bash
# Initialize a new novel (scaffolds directory + prompts for logline/ending/structure)
/novel-init "The Last Cartographer"

# Generate beat sheet + scene list from premise (requires ending defined)
/novel-outline last-cartographer

# Build character + world + style-guide bible (TIME-BOXED; one agent session)
/novel-bible last-cartographer

# Draft the whole first draft scene-by-scene (auto runs canon-extract + continuity)
/novel-draft last-cartographer

# Draft a single scene
/novel-write last-cartographer --scene 12

# Read the whole manuscript for story health (NO editing)
/novel-readthrough last-cartographer

# Run a revision stage (MUST run in order)
/novel-revise last-cartographer --stage dev      # developmental — structure/arc
/novel-revise last-cartographer --stage line     # sentence-level craft
/novel-revise last-cartographer --stage copy     # grammar + style sheet
/novel-revise last-cartographer --stage proof    # final typos

# Ask the bible/canon
/novel-query last-cartographer "What color are Mira's eyes?"

# Continuity check any time
/novel-continuity last-cartographer

# Health + retrospective
/novel-lint last-cartographer
/novel-evolve last-cartographer
```

## Architecture

**Claude Code-native.** Skills orchestrate agents. Agents use their own tools autonomously. `backend/novel_pipeline.py` handles scaffolding only — no LLM calls.

- **Skills** (`.claude/skills/novel-*`) — slash commands that invoke the right agents in the right order
- **Agents** (`.claude/agents/`) — 10 fiction-specific agents + reused `evolve-agent`
- **`backend/novel_pipeline.py`** — `init-novel` command; scaffolds `novels/{slug}/`

## Project Structure

```
novels/{novel-slug}/
├── _novel.yaml              # Metadata: title, genre, POV, tense, target length, audience
├── premise.md               # Logline + ENDING (required before outlining)
├── outline/
│   ├── beat-sheet.yaml      # Chosen structure (save-the-cat | snowflake | story-grid | 3-act)
│   └── scene-list.yaml      # One entry per scene: POV, goal, conflict, outcome, status
├── bible/
│   ├── characters/          # One file per major character (stub-first, grows via canon)
│   ├── world/               # Setting, rules, geography, culture
│   ├── timeline.yaml        # Story timeline + real-world anchors (if any)
│   └── style-guide.md       # POV, tense, voice register, profanity/dialect policy — BINDING
├── canon.jsonl              # Append-only log of facts established by graduated scenes
├── style-sheet.yaml         # Name spellings, invented-word casing, italics/caps conventions
├── manuscript/              # Graduated scenes (the book)
│   ├── ch01/
│   │   ├── s01.md
│   │   ├── s02.md
│   │   └── ...
│   └── ch02/
├── staging/                 # Draft scenes pending revision stages
├── revisions/               # Revision plans + editorial notes per stage
│   ├── readthrough-YYYY-MM-DD.md
│   ├── dev-plan-YYYY-MM-DD.md
│   └── ...
├── CHANGELOG.md             # Append-only log of all manuscript modifications
├── log.md                   # Operation log
├── output/                  # Lint + craft-eval reports
└── raw/                     # Optional: research for historical/technical fiction
```

## Agent Routing (MANDATORY)

| Task | Agent |
|------|-------|
| Logline → beats → scene list → bible | `story-architect-agent` |
| Draft / revise a scene | `scene-writer-agent` |
| Extract established facts from prose | `canon-extractor-agent` |
| Check draft against bible + canon | `continuity-checker-agent` |
| Whole-manuscript read (no editing) | `read-through-agent` |
| Big-picture revision plan | `developmental-edit-agent` |
| Sentence-level craft | `line-edit-agent` |
| Grammar + style-sheet consistency | `copy-edit-agent` |
| Final typos | `proof-agent` |
| Answer questions about the book | `query-agent` (reused) |
| Structural health check | `lint-agent` (reused, fiction mode) |
| Craft rubric eval | `craft-eval-agent` |
| Plot holes / pacing / arc retrospective | `evolve-agent` (reused) |

## Pipeline Flow

```
Phase 0: story-architect (premise → beats → scene list → time-boxed bible)
  ↓
Phase 1: DRAFT LOOP per scene
    scene-writer → canon-extractor → continuity-checker → staging/
  ↓
Phase 2: read-through-agent (whole manuscript, NO editing)
  ↓
Phase 3: developmental-edit-agent (revision plan) → HUMAN GATE → scene-writer (executes plan)
  ↓
Phase 4: line-edit-agent (per-scene, sentence-level)
  ↓
Phase 5: copy-edit-agent (grammar + style sheet)
  ↓
Phase 6: proof-agent (final typos)
  ↓
Phase 7: craft-eval-agent + evolve-agent (retrospective)
```

## Canon Discipline

### Canon Tiers (C1-C5)

| Tier | Definition | Enforcement |
|------|-----------|-------------|
| **C1 Bible-canon** | Established in bible before drafting | Binding — prose must match |
| **C2 Prose-canon** | Established by a graduated scene | Binding on all later scenes |
| **C3 Draft-canon** | In staging, not yet graduated | Provisional — may change |
| **C4 Hypothetical** | Considered, unwritten | Non-binding |
| **C5 Contradiction** | Conflict between sources | BLOCKS graduation — must resolve |

### Hard Rules

- **Style guide is BINDING** — POV and tense violations are hard errors (severity = C5)
- **C5 contradictions BLOCK graduation** to `manuscript/` until resolved
- **Canon is append-only** (`canon.jsonl`) — when a later scene needs to override, it creates an explicit retcon entry
- **No revision stage may run until the prior stage is clean for that scene** — tracked in scene frontmatter (`dev_status`, `line_status`, `copy_status`, `proof_status`)

## SOP Rules (from professional practice)

Three rules codified from the research:

1. **Ending-first.** `story-architect-agent` refuses to generate a scene list if `premise.md` lacks an ending statement. (Sanderson's rule.)
2. **Time-boxed bible.** `story-architect-agent` has a hard cap (~one agent session) for bible generation. Continue via canon-extraction during drafting, not upfront expansion. Prevents worldbuilding-forever.
3. **Revision stages run sequentially, never interleaved.** Never line-edit a scene that might be cut in developmental. Never copy-edit a sentence that might be rewritten in line edit. Stage gates are enforced by scene frontmatter status flags.

## Scene Frontmatter (BINDING)

Every scene file must have:

```yaml
---
scene_id: 012
chapter: 2
pov: Mira
tense: past
goal: "Mira must convince the cartographers' guild to fund her expedition"
conflict: "The guild master Veylan wants her discoveries for his own atlas"
outcome: "Mira gets the funding but under Veylan's name — she resents it"
word_target: 2500
status: drafted          # drafted | dev_clean | line_clean | copy_clean | proofed | GRADUATED
dev_status: pending      # pending | passed | flagged
line_status: pending
copy_status: pending
proof_status: pending
canon_facts_introduced: [mira-left-handed, guild-vault-location, veylan-limp]
---
```

## Changelog and Git Snapshots (MANDATORY)

Same as `/kb-*`:

1. Append to `novels/{slug}/CHANGELOG.md` before writing (what changed, what added, what removed, reason).
2. Git commit after every pipeline run.
3. Bump version + commit when modifying `NOVEL.md` or any `.claude/agents/*.md` / `.claude/skills/novel-*/SKILL.md`.

Example commit message:
```
novel: last-cartographer — draft phase complete 2026-04-16

- Scenes drafted: 23
- Continuity flags: 2 resolved, 0 open
- Canon facts extracted: 87
- Style-guide violations: 0
```

## Skills Reference

| Skill | What It Does | Agents Invoked |
|-------|--------------|----------------|
| `/novel-init "<title>"` | Scaffold directory + capture logline/ending/structure | — (CLI only) |
| `/novel-outline <slug>` | Generate beat sheet + scene list | `story-architect-agent` |
| `/novel-bible <slug>` | Build characters + world + style-guide (time-boxed) | `story-architect-agent` |
| `/novel-draft <slug>` | Draft all pending scenes through the scene list | `scene-writer` → `canon-extractor` → `continuity-checker` (loop) |
| `/novel-write <slug> --scene <id>` | Draft a single scene | same as above, scoped to one scene |
| `/novel-readthrough <slug>` | Whole-manuscript read → story-health report | `read-through-agent` |
| `/novel-revise <slug> --stage dev\|line\|copy\|proof` | Run the named revision stage | `developmental-edit` / `line-edit` / `copy-edit` / `proof-agent` |
| `/novel-continuity <slug>` | Standalone continuity check | `continuity-checker-agent` |
| `/novel-query <slug> "<q>"` | Answer from bible + canon + manuscript | `query-agent` (fiction mode) |
| `/novel-lint <slug>` | Structural health check | `lint-agent` (fiction mode) |
| `/novel-evolve <slug>` | Plot holes + pacing + arc retrospective | `evolve-agent` |

## Scaffolding CLI

```bash
# Only Python CLI — everything else is a skill
python -m backend.novel_pipeline init-novel "<title>" [--genre <g>] [--pov <pov>] [--tense <t>]
```

---

*Fiction Pipeline | v1.0*
