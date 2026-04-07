Re-verify and update volatile claims in an existing wiki topic without re-running the full research pipeline. Designed for annual admissions cycle refreshes (run each September when new cycle data becomes available).

## Parse arguments

Extract from the user's message:
- `topic_slug` — required
- `--volatile annual|cycle_bound|evergreen|all` — which volatility class to re-verify (default: `annual`)
- `--entity {entity-slug}` — optional; limit to a single entity

Set `topic_dir = topics/{topic_slug}/`.

Verify `{topic_dir}/_topic.yaml` and `{topic_dir}/fact-sheet.yaml` exist. If not, tell the user to run `/kb-research` first.

---

## Step 1 — Collect target claims

Read `{topic_dir}/fact-sheet.yaml`. Collect all `verified_claims` where `volatile` matches the requested class (or all classes if `--volatile all`).

If `--entity` is specified, filter to only that entity's claims.

Report to the user:
```
Found N claims to re-verify (volatile: annual)
Entities affected: [list]
Proceed? This will use web searches.
```

Wait for confirmation.

---

## Step 2 — Re-verify each claim

For each target claim, invoke **fact-checker-agent** in User-Action mode:

> "Re-verify this specific claim before the user acts on it. Claim: '{permitted_language}'. Go directly to the primary official source — do not rely on cached raw files. Fetch the current page live. Compare the claimed value to what the official source currently states. Return: confirmed / changed / source_unavailable / not_found. If changed, provide the new value and new permitted_language."

Group claims by entity to minimize redundant fetches (one fetch per school page covers all that school's claims).

---

## Step 3 — Process results

For each claim result:

**If `confirmed`:** Update `last_verified` to today in `fact-sheet.yaml`. No wiki changes needed.

**If `changed`:**
1. Update `permitted_language` in `fact-sheet.yaml` with the new value
2. Update `last_verified` to today
3. Flag the wiki article for update (add to a `pending_wiki_updates` list)
4. Note the old vs. new value in `log.md`

**If `source_unavailable` or `not_found`:**
1. Flag the claim as `needs_research` in `fact-sheet.yaml`
2. Add to `log.md` with URL and timestamp
3. Optionally: add a targeted gap_fill question to `research-plan.yaml`

---

## Step 4 — Update wiki articles (changed claims only)

If any claims changed, invoke **wiki-compiler-agent** in diff-aware mode:

> "Update wiki articles for entities with changed claims. Read `{topic_dir}/fact-sheet.yaml` for new permitted_language. For each affected article: use diff-aware compilation — only rewrite the specific sections containing changed claims. Leave all other sections untouched. Update `updated:` in frontmatter to today. Append to `log.md`."

---

## Step 5 — Run cross-linker

```bash
python -m backend.tools.cross_linker topics/{topic_slug}/wiki/
```

---

## Step 6 — Report

```
kb-update complete for {slug}

Claims re-verified:  N
  Confirmed:         N (no change)
  Changed:           N (wiki updated)
  Source unavailable: N (flagged for research)

Wiki articles updated: [list]

Recommended next: /kb-lint {slug} to check for any new structural issues.
```

Append a summary to `{topic_dir}/log.md`.

---

## Usage examples

```bash
# Re-verify all annual claims (typical September refresh)
/kb-update bay-area-private-school-k-application

# Re-verify only one school
/kb-update bay-area-private-school-k-application --entity hamlin-school

# Re-verify everything
/kb-update bay-area-private-school-k-application --volatile all
```
