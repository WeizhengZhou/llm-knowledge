Analyze the wiki for gaps, staleness, and cross-entity patterns. The evolve-agent produces a prioritized improvement roadmap and adds new questions to the research plan.

## Parse arguments

Extract from the user's message:
- `--topic {slug}` — required

Set `topic_dir = topics/{slug}/`.

Verify `{topic_dir}/_topic.yaml` exists. If not, tell the user to run `/kb-init` first.

---

## Step 1 — Invoke evolve-agent

Invoke **evolve-agent**:

> "Run a full evolution analysis on the knowledge base at `{topic_dir}`.
>
> Read these inputs before analysis:
> - `{topic_dir}/research-plan.yaml` — question tree and coverage status
> - `{topic_dir}/wiki/_index.md` — current wiki structure
> - All `{topic_dir}/wiki/**/*.md` files
> - `{topic_dir}/fact-sheet.yaml` — confidence levels and valid_until dates
> - Most recent `{topic_dir}/output/lint-report-*.md` — avoid re-reporting lint findings
> - `{topic_dir}/log.md` — recent activity context
>
> Run all four analyses:
>
> **Analysis 1 — Gap analysis:**
> - For each answered research-plan question, verify a wiki article substantively covers it (classify: missing_article / thin_coverage / wrong_type)
> - Find pending questions that have been pending >7 days (classify: budget_blocked / dependency_unmet / no_apparent_reason)
> - Find concept-extraction questions with status: pending that were never picked up
>
> **Analysis 2 — Freshness analysis:**
> - Find articles with valid_until dates that have passed (error-level)
> - Find articles with valid_until within 30 days (warning-level)
> - Find articles containing volatile data patterns ($\d+, deadlines, enrollment \d+) but no valid_until
> - Find questions answered >6 months ago whose facet is WHEN or type is numerical
>
> **Analysis 3 — Cross-entity pattern discovery:**
> - Build a mental comparison table across all entity articles; find non-trivial attribute correlations (N≥3 to confirm; N<3 = hypothetical only)
> - Scan all articles for [[wikilinks]] targeting non-existent articles; rank by link count
> - Find article pairs with >70% content overlap as merge candidates
>
> **Analysis 4 — New question generation:**
> - Generate qE-prefixed gap_fill questions for each identified gap
> - Score each on user_value/dependency_count/searchability/novelty using the standard formula
> - Run 3-layer deduplication against all existing questions before adding
> - Add qualified questions directly to `{topic_dir}/research-plan.yaml` under phases.gap_fill.questions
>
> Write the full evolution suggestions to `{topic_dir}/output/evolution-suggestions-{YYYY-MM-DD}.md`.
>
> Update `{topic_dir}/research-plan.yaml` to include all new qE questions.
>
> Append to `{topic_dir}/log.md`:
> `{timestamp} | evolve-agent | Evolution run complete. Gaps: N, Freshness: N expired / N approaching, Patterns: N confirmed / N hypothetical. New questions: N (qE prefix). See output/evolution-suggestions-{YYYY-MM-DD}.md`"

---

## Step 2 — Report

Show:
- Gap analysis: N missing articles, N thin, N pending past-due
- Freshness: N expired, N approaching expiry, N untagged volatile
- Patterns: N confirmed (N≥3 entities), N hypothetical
- Backlink gaps: top 3 concepts linked-but-missing
- New questions added to gap_fill: N
- Path to full report: `{topic_dir}/output/evolution-suggestions-{YYYY-MM-DD}.md`
- Suggested next: `/kb-research {slug} --phase gap` to execute new questions
