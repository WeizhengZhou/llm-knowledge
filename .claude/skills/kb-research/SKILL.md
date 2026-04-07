Run the research pipeline for a topic. Agents execute autonomously using their own tools.

## Parse arguments

Extract from the user's message:
- `topic_slug` — required
- `--phase breadth|depth|gap` — optional; if absent, run the full pipeline

Set `topic_dir = topics/{topic_slug}/`.

Verify `{topic_dir}/_topic.yaml` exists. If not, tell the user to run `/kb-init` first.

---

## Full pipeline (no --phase flag)

Run these steps in order. Each agent uses its own Read/Write/WebSearch/WebFetch tools — do not pass file contents manually.

### Step 1 — Research planner (if plan is empty or stale)

Check `{topic_dir}/research-plan.yaml`. If it has fewer than 5 questions or no pending questions, invoke **research-planner-agent**:

> "Read `{topic_dir}/_topic.yaml` for topic and context. Update `{topic_dir}/research-plan.yaml` with a full question tree: 8 facets (WHO/WHAT/WHEN/WHERE/HOW/WHY/COMPARE/META), scored on user_value/dependency_count/searchability/novelty, phased as breadth/depth/gap_fill, with dependencies. Save the completed plan."

### Step 2 — Research: breadth phase

Invoke **research-agent**:

> "Read `{topic_dir}/research-plan.yaml`. Execute all pending questions in the **breadth** phase. For each question: formulate 2-3 search-engine-optimized queries, check search-log.jsonl for near-duplicate queries before running (skip if 70%+ keyword overlap). Fetch pages using the two-step strategy: WebFetch first; if response is <500 chars or contains bot-detection signals, fall back to Chrome MCP (mcp__chrome-devtools__new_page → wait_for → take_snapshot → close_page). Save each page to `{topic_dir}/raw/web/{tier}/YYYY-MM-DD_{slug}.md` with full frontmatter. Extract new concepts; spawn child questions if not duplicates. Update question statuses and append all search records to `{topic_dir}/raw/search-log.jsonl`. Stop when breadth questions are exhausted or 30% of search budget is consumed."

### [CHECKPOINT] — Human review after breadth

After Step 2 completes, pause and present a summary to the user:

```
Breadth complete.
- Questions answered: N
- Key entities found: [list top 10]
- Platforms/orgs found: [list]
- Searches used: N/max

Proceed with depth research? (type 'yes' to continue, or give corrections)
```

Wait for confirmation before proceeding to Step 3. This prevents wasted depth budget if the breadth phase captured wrong entities or the wrong geographic scope.

### Step 3 — Research: depth phase

Invoke **research-agent**:

> "Read `{topic_dir}/research-plan.yaml`. Execute all pending questions in the **depth** phase. For each entity discovered in breadth: fetch its official source (L1) plus 1-2 third-party sources (L2-L3) and cross-reference. Use the two-step fetch strategy: WebFetch first; Chrome MCP fallback if gated. Save to `{topic_dir}/raw/web/`. Update research-plan.yaml and search-log.jsonl. Stop when depth questions are exhausted or 80% of total budget is consumed."

### Step 4 — Research: gap-fill phase

Invoke **research-agent**:

> "Read `{topic_dir}/research-plan.yaml`. Find pending gap_fill questions and any concepts mentioned in wiki articles that have no corresponding raw source. Run targeted searches with the two-step fetch strategy. Save to `{topic_dir}/raw/web/`. Update research-plan.yaml and search-log.jsonl."

### Step 5 — Claim extraction

Invoke **claim-extractor-agent**:

> "Read all `.md` files under `{topic_dir}/raw/`. For each file: classify sentences as factual_claim/process_description/opinion/editorial. For factual claims: type them (numerical/categorical/temporal/comparative/causal/process/definitional), assign priority (must_verify for numerical+temporal, should_verify for categorical+process, may_skip for sentiment+definitional), flag overreach. Group by entity. Write incrementally — entity by entity — to avoid output token limits: write each entity group's claims to `{topic_dir}/claims-register.yaml` immediately (create if first group, append otherwise). Write coverage_summary last."

### Step 6 — Fact-checking

Invoke **fact-checker-agent** in batch mode:

> "Read `{topic_dir}/claims-register.yaml` and all files in `{topic_dir}/raw/`. For each must_verify claim: cross-reference across sources, assign L1-L5 confidence, write PERMITTED LANGUAGE (binding on wiki compiler). Set `volatile:` class (annual/cycle_bound/evergreen/none) on every numerical and temporal claim — do NOT use hard valid_until dates. Run the Mechanism Overreach Check on all overreach-flagged claims and downgrade them. For conflicting sources: write a dispute record. Block all L5 claims with gate_status: BLOCKED. Write `{topic_dir}/fact-sheet.yaml`."

### Step 7 — Wiki compilation

Invoke **wiki-compiler-agent**:

> "Read `{topic_dir}/fact-sheet.yaml` first (gate check), then `{topic_dir}/research-plan.yaml`, then `{topic_dir}/wiki/_index.md`. For each article: load only the raw source files relevant to that entity/theme on demand — do NOT load all raw files upfront. For existing articles: use diff-aware compilation — only rewrite sections where fact-sheet claims changed; preserve unchanged sections verbatim. For new articles: write from scratch. Synthesize into thematic wiki articles. Use volatile: classes in frontmatter (not valid_until dates). Use permitted_language from fact-sheet VERBATIM. Insert [[wikilinks]]. Check shared/ namespace before writing entity articles — link to shared articles if they exist. Write articles to `{topic_dir}/wiki/`, update `{topic_dir}/wiki/_index.md` and `{topic_dir}/index.md`, append to `{topic_dir}/log.md`."

### Step 7.5 — Cross-linker (automatic)

After wiki-compiler-agent completes, run:

```bash
python -m backend.tools.cross_linker topics/{topic_slug}/wiki/
```

This populates all `backlinks: []` arrays in article frontmatter. Do not skip this step.

### Step 8 — Lint

Invoke **lint-agent**:

> "Read all files in `{topic_dir}/wiki/`, `{topic_dir}/fact-sheet.yaml`, and `{topic_dir}/research-plan.yaml`. Run structural checks (broken wikilinks, orphans, missing frontmatter, volatility class staleness), content checks (contradictions, missing sources, permitted-language violations), and coverage checks (entities without articles, unanswered questions, thin articles). Write the severity-tiered report directly to `{topic_dir}/output/lint-report-YYYY-MM-DD.md` using your Write tool."

---

## Single-phase mode (--phase flag)

If `--phase breadth`: run only Step 2 (with checkpoint after).
If `--phase depth`: run only Step 3.
If `--phase gap`: run only Step 4.

After the single phase, ask: *"Continue with extraction and compilation? Run `/kb-research {slug}` without --phase to continue."*

---

## After all steps complete

Report:
- Questions answered / total
- Raw sources collected
- Wiki articles created / updated
- Lint errors / warnings
- Suggested next: `/kb-query {slug} "..."` or `/kb-evolve {slug}`
