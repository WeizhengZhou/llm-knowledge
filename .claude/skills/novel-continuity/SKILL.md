Standalone continuity check — verify draft against bible + canon.

## Step 1 — Parse arguments

Extract:
- `slug` — required
- `--scene <id>` — optional, scope to single scene (default: all scenes)

Set `novel_dir = novels/{slug}/`.

## Step 2 — Invoke continuity-checker-agent

### Scene scope

> "Run continuity check on `novels/{slug}/staging/s{id}.md` (or manuscript path). Read canon.jsonl, bible/**, outline/scene-list.yaml. Apply all 8 checks. Write report to `revisions/continuity-report-s{id}-YYYY-MM-DD.md` with gate status."

### Whole-manuscript scope

> "Run continuity check on all scenes in `novels/{slug}/manuscript/` and `staging/`. Read canon.jsonl, bible/**, outline/scene-list.yaml. Apply all 8 checks across the manuscript. Write report to `revisions/continuity-report-all-YYYY-MM-DD.md` with per-scene gate statuses and an overall summary."

## Step 3 — Report to user

Show:
- Scope: scene {id} / whole manuscript
- C5 (blocking): N
- C4 (flag): N
- C3 (style): N
- Gate: CLEAR | FLAGGED | BLOCKED
- Report path

If BLOCKED, suggest next: run `/novel-write {slug} --scene {id} --mode revise` with the continuity report as input, or fix manually.

## Step 4 — Git snapshot (only if report adds value)

No commit for pure check runs unless the report is used. Continuity reports live in `revisions/` and get committed alongside the next real change.
