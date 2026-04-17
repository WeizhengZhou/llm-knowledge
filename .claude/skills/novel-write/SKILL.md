Draft or revise a single scene.

## Step 1 — Parse arguments

Extract:
- `slug` — required positional
- `--scene <id>` — required, scene ID from scene-list.yaml
- `--mode draft|revise` — optional, default `draft`. `revise` mode requires a dev-plan that references this scene.

Set `novel_dir = novels/{slug}/`.

## Step 2 — Invoke scene-writer-agent

### Draft mode

> "Draft scene `{scene_id}` for `novels/{slug}/`. Mode: draft (new scene).
>
> Read `_novel.yaml`, `bible/style-guide.md`, `bible/characters/{pov-char}.md`, the scene-list entry, canon.jsonl, beat-sheet, and the immediately preceding drafted scene. Honor POV, tense, and style-guide. Write to `staging/s{scene_id}.md` with full frontmatter. Fill in `word_count` and `canon_facts_introduced` after writing. Append to log + CHANGELOG."

### Revise mode

> "Revise scene `{scene_id}` for `novels/{slug}/`. Mode: revise.
>
> Read the most recent `revisions/dev-plan-*.md` and find the directive for this scene. If no directive exists, STOP — the scene is not in the approved revision plan. Execute the directive: may be goal/conflict/outcome change, prose rewrite, partial edit. Keep POV and tense locked unless the dev plan overrides. Update the scene in place (staging/ if not yet graduated, manuscript/ if previously graduated). Update frontmatter: reset `line_status` and `copy_status` and `proof_status` to `pending`. Append to log + CHANGELOG."

## Step 3 — Canon + continuity follow-up

Invoke canon-extractor-agent, then continuity-checker-agent (scoped to this scene) — same sub-steps as `/novel-draft`.

## Step 4 — Report

Show scene-level summary:
- Scene ID, POV, word count
- Canon facts extracted
- Continuity gate (CLEAR / FLAGGED / BLOCKED)
- Next suggested: continue drafting, run revision stage, or `/novel-continuity {slug}`

## Step 5 — Git snapshot

Same pattern as `/novel-draft`.
