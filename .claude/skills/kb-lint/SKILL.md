Run automated health checks on the wiki. The lint-agent checks structural integrity, content quality, and coverage gaps, then writes a severity-tiered report.

## Parse arguments

Extract from the user's message:
- `--topic {slug}` — required

Set `topic_dir = topics/{slug}/`.

Verify `{topic_dir}/_topic.yaml` exists. If not, tell the user to run `/kb-init` first.

---

## Step 1 — Invoke lint-agent

Invoke **lint-agent**:

> "Run a full health check on the knowledge base at `{topic_dir}`.
>
> Read these inputs:
> - All `{topic_dir}/wiki/**/*.md` files
> - `{topic_dir}/wiki/_index.md`
> - `{topic_dir}/fact-sheet.yaml`
> - `{topic_dir}/research-plan.yaml`
> - `{topic_dir}/claims-register.yaml`
>
> Run all three check categories:
>
> **Structural checks (error severity):**
> - Broken `[[wikilinks]]` — links to articles that don't exist
> - Orphaned articles — articles with no incoming links and not in _index.md
> - Missing required frontmatter fields (title, type, created, sources, confidence)
> - Stale valid_until dates that have passed
>
> **Content checks (warning severity):**
> - Cross-article contradictions — claims in two articles that cannot both be true
> - Missing source attribution — claims stated as fact with no source link
> - Permitted-language violations — wiki language stronger than what fact-sheet allows for that claim
> - Overreach language — individual data point stated as population-level fact
>
> **Coverage checks (info severity):**
> - Research-plan questions with status: answered but no wiki article covers the answer
> - Named entities mentioned across multiple articles but no dedicated entity article exists
> - Thin articles — substantive articles under 150 words
> - Unanswered breadth-phase questions (may indicate incomplete research)
>
> Write the full report to `{topic_dir}/output/lint-report-{YYYY-MM-DD}.md` with:
> - Executive summary: counts by severity
> - Errors section (must fix before next research cycle)
> - Warnings section
> - Info section
> - Suggested commands for next steps
>
> Append to `{topic_dir}/log.md`:
> `{timestamp} | lint-agent | Lint complete. Errors: N, Warnings: N, Info: N.`"

---

## Step 2 — Report

Show:
- Error count / Warning count / Info count
- Top 3 highest-severity findings
- Path to full report: `{topic_dir}/output/lint-report-{YYYY-MM-DD}.md`
- Suggested next: `/kb-evolve {slug}` if errors > 0, or `/kb-research {slug}` if coverage gaps found
