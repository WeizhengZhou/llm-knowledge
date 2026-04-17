Retrospective: plot holes, pacing, arc, underused characters, thematic gaps.

## Step 1 — Parse arguments

Extract:
- `slug` — required

Set `novel_dir = novels/{slug}/`.

## Step 2 — Invoke evolve-agent (fiction mode)

Evolve-agent is reused from the KB pipeline. Tell it to operate in fiction mode:

> "Run a retrospective on `novels/{slug}/`.
>
> Inputs:
> - `premise.md`, `_novel.yaml`
> - `outline/beat-sheet.yaml`, `outline/scene-list.yaml`
> - `bible/**`
> - `canon.jsonl`
> - `manuscript/**/*.md` + `staging/**/*.md`
> - `revisions/readthrough-*.md` (most recent)
> - `output/craft-eval-report-*.yaml` (most recent, if exists)
> - `output/eval-history.jsonl` (score trend)
>
> Analyses to run:
>
> 1. **Plot holes** — grep canon.jsonl for knowledge-state entries and check every later scene where that character acts; flag any act inconsistent with their known state
> 2. **Dropped threads** — mark every promise made in the opening 20% that has not paid off by the ending
> 3. **Unseeded payoffs** — mark every major event in the final 20% that has no setup in the first 60%
> 4. **Underused characters** — characters with a bible file but appearing in <3 scenes; protagonists of subplots that don't land
> 5. **Pacing heatmap** — words per scene over manuscript order; flag long flat stretches
> 6. **Arc flatness** — protagonist scenes where the POV character does not change state; flag clusters
> 7. **Thematic drift** — themes declared in premise that are underseeded (< 3 scene-level expressions)
> 8. **Canon drift** — C3 draft-canon entries that never got promoted to C2 (scenes that never graduated)
> 9. **Eval-score trend** — if eval-history.jsonl has 3+ entries, detect dimensions that are flat or declining
>
> Write `output/evolve-suggestions-YYYY-MM-DD.md` with:
> - Top 10 suggestions ranked by impact
> - Proposed revision actions for each (cut / add / rewrite / retcon / outline-fix)
> - Which priorities would require a new dev-plan round
> - Which could be handled in the current revision round
>
> Do NOT modify any prose or outline files. Suggestions only."

## Step 3 — Report

Show:
- Plot holes flagged: N
- Dropped threads: N
- Underused characters: N
- Pacing flat spans: N
- Top 3 recommendations inline
- Report path

Suggested next: review the report, then either `/novel-revise {slug} --stage dev` (if structural) or update outline directly.

## Step 4 — Git snapshot

```bash
git add novels/{slug}/output/
git commit -m "novel: {slug} — evolve $(date +%Y-%m-%d)

- Suggestions: N
- Plot holes: N
- Dropped threads: N"
```
