Draft all pending scenes through the scene list — first-draft pipeline.

## Step 1 — Parse arguments

Extract:
- `slug` — required
- `--from <scene-id>` — optional, resume from specific scene
- `--to <scene-id>` — optional, stop at specific scene
- `--max <n>` — optional cap on scenes per run (default: all pending)

Set `novel_dir = novels/{slug}/`.

## Step 2 — Pre-flight

- Verify `outline/scene-list.yaml` has pending scenes
- Verify `bible/style-guide.md` exists and is filled in (not placeholders)
- Verify `canon.jsonl` has at least some C1 seeds (confirms bible was run)

If any check fails, direct user to the missing step and stop.

## Step 3 — Drafting loop

For each pending scene in `scene-list.yaml` (in order), within the scope of `--from` / `--to` / `--max`:

### Step 3a — Invoke scene-writer-agent

> "Draft scene `{scene_id}` for `novels/{slug}/`. Mode: draft (new scene).
>
> Read `_novel.yaml`, `bible/style-guide.md`, `bible/characters/{pov-char}.md`, the scene-list entry, canon.jsonl (grep for subjects relevant to this scene), beat-sheet.yaml, and the immediately preceding drafted scene for continuity.
>
> Execute the scene's goal/conflict/outcome. Honor POV and tense. Follow style-guide bindings. Write to `staging/s{scene_id}.md` with full frontmatter. Fill in `word_count` and list `canon_facts_introduced` after writing. Append to log.md and CHANGELOG.md."

### Step 3b — Invoke canon-extractor-agent

> "Extract canon from `staging/s{scene_id}.md`. Append new C3 entries to `canon.jsonl`. Flag any conflicts with existing C1/C2 canon to `revisions/continuity-flags-YYYY-MM-DD.md`. Do not modify existing entries. Append to log.md."

### Step 3c — Invoke continuity-checker-agent (scoped to this scene)

> "Run continuity check on `staging/s{scene_id}.md`. Write report to `revisions/continuity-report-{scene_id}-YYYY-MM-DD.md`. Set gate status: CLEAR | FLAGGED | BLOCKED."

### Step 3d — Handle gate

- **CLEAR**: mark scene's frontmatter `status: drafted`, continue to next scene
- **FLAGGED**: log the flags but continue (non-blocking)
- **BLOCKED**: stop drafting. Re-invoke scene-writer-agent with the continuity report as input and the instruction to fix the C5 items. Retry the check. If still blocked after 2 retries, report to user and stop.

## Step 4 — Report after loop

Show:
- Scenes drafted: N
- Total new words: N
- Continuity gates: CLEAR N / FLAGGED N / BLOCKED N
- Canon facts extracted: N
- Remaining pending scenes: N
- Suggested next: `/novel-readthrough {slug}` once ALL scenes are drafted, or `/novel-draft {slug}` to continue

## Step 5 — Git snapshot

```bash
git add novels/{slug}/
git commit -m "novel: {slug} — draft progress $(date +%Y-%m-%d)

- Scenes drafted this run: N
- Total scenes drafted: N / {total}
- Continuity blocks: N
- Canon facts added: N"
```
