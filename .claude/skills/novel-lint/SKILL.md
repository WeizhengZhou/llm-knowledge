Structural health check on a novel + craft eval.

## Step 1 — Parse arguments

Extract:
- `slug` — required

Set `novel_dir = novels/{slug}/`.

## Step 2 — Invoke lint-agent (fiction mode)

Lint-agent is reused from the KB pipeline. Tell it to operate in fiction mode:

> "Run a structural health check on `novels/{slug}/`.
>
> Checks to run:
> 1. **Scene frontmatter completeness** — every scene file has required fields (scene_id, chapter, pov, tense, goal, conflict, outcome, word_target, word_count, all four *_status fields)
> 2. **Status consistency** — no scene has `line_status: passed` with `dev_status: pending` (stage ordering violated)
> 3. **Scene-list vs. file alignment** — every scene in scene-list.yaml has a file in staging/ or manuscript/; orphaned files in staging/ flagged; missing scenes flagged
> 4. **POV consistency** — scene frontmatter POV matches scene-list entry and matches prose usage (spot-checks)
> 5. **Word count tracking** — total manuscript words vs. target in _novel.yaml; flag if >20% off
> 6. **Canon integrity** — canon.jsonl lines are valid JSON; all IDs unique; no append-order violations
> 7. **Style-sheet coverage** — every character in bible/characters/ has a style-sheet entry; every invented term used 3+ times has an entry
> 8. **Revision artifact health** — unresolved continuity flags; pending dev-plans; stale readthrough reports (>60 days old)
> 9. **Bible-canon sync** — every bible fact has a corresponding C1 entry in canon.jsonl
> 10. **Graduation eligibility** — scenes with all four *_status: passed should be in manuscript/ not staging/
>
> Write `output/lint-report-YYYY-MM-DD.md` with severity tiers: ERROR | WARN | INFO. Overall status: TRUSTED | DEGRADED | BLOCKED."

## Step 3 — Invoke craft-eval-agent (optional, only if manuscript is substantially complete)

Check: if ≥80% of scenes have graduated (status: GRADUATED), also run craft-eval:

> "Run craft eval on `novels/{slug}/`. Read _novel.yaml, premise.md, all manuscript scenes, and the most recent readthrough. Score CE1-CE8. Answer the 7 test-reader questions. Produce `output/craft-eval-report-YYYY-MM-DD.yaml` and append to `output/eval-history.jsonl`."

Otherwise skip craft-eval and note in the report that the manuscript is too early for craft scoring.

## Step 4 — Report

Show:
- Lint status: TRUSTED / DEGRADED / BLOCKED
- Errors: N, warnings: N, info: N
- Craft composite: N/10 (if run)
- Top 3 lint errors or top 3 craft recommendations
- Report paths

## Step 5 — Git snapshot

```bash
git add novels/{slug}/output/
git commit -m "novel: {slug} — lint $(date +%Y-%m-%d)

- Lint status: {status}
- Errors: N / Warnings: N
- Craft composite: N/10 (if run)"
```
