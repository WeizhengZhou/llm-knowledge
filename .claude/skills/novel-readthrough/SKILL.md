Read the whole manuscript cover-to-cover and produce a story-health report.

## Step 1 — Parse arguments

Extract:
- `slug` — required

Set `novel_dir = novels/{slug}/`.

## Step 2 — Pre-flight

Verify at least 80% of scenes in `outline/scene-list.yaml` have been drafted (i.e., corresponding files exist in `staging/` or `manuscript/`). If fewer, warn the user:

> Only N of M scenes drafted. Read-through is designed for full first drafts. Continue anyway? (y/n)

## Step 3 — Invoke read-through-agent

> "Run a whole-manuscript read-through on `novels/{slug}/`.
>
> Read `_novel.yaml`, `premise.md`, `outline/beat-sheet.yaml`, `outline/scene-list.yaml`, and all scene files — IN SCENE-LIST ORDER (not file order).
>
> Produce `revisions/readthrough-YYYY-MM-DD.md` with dimensions D1 (narrative arc), D2 (character arc), D3 (promises/payoffs), D4 (pacing), D5 (POV/voice), D6 (theme), D7 (opening/ending), D8 (genre fit). End with Top 5 issues for developmental edit and a What's Already Working list.
>
> NO sentence-level feedback. NO continuity flagging (that's continuity-checker's domain). Observations, not prescriptions.
>
> Update `_novel.yaml` → phase_status.readthrough = 'complete'. Append to log.md."

## Step 4 — Report

Show the Overall Impression paragraph + the Top 5 list to the user inline. Indicate where the full report lives.

Suggested next: `/novel-revise {slug} --stage dev`

## Step 5 — Git snapshot

```bash
git add novels/{slug}/
git commit -m "novel: {slug} — readthrough $(date +%Y-%m-%d)

- Manuscript word count: N
- Top issues: N
- Readthrough report: revisions/readthrough-YYYY-MM-DD.md"
```
