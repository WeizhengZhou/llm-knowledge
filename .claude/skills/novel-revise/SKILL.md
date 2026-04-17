Run a revision stage: developmental, line, copy, or proof.

Stages MUST run in order. You cannot run `line` until `dev` is clean for the affected scenes. Cannot run `copy` until `line` is clean. Cannot run `proof` until `copy` is clean.

## Step 1 — Parse arguments

Extract:
- `slug` — required
- `--stage dev|line|copy|proof` — required
- `--scene <id>` — optional, scope to a single scene (for line/copy/proof)

Set `novel_dir = novels/{slug}/`.

## Step 2 — Branch on stage

### Stage: dev

Pre-flight: verify `revisions/readthrough-*.md` exists (most recent within 30 days ideally). If not, STOP:

> Developmental edit requires a recent read-through. Run `/novel-readthrough {slug}` first.

Invoke **developmental-edit-agent**:

> "Read the most recent readthrough report in `revisions/`, plus `premise.md`, `outline/beat-sheet.yaml`, `outline/scene-list.yaml`, `_novel.yaml`, `bible/**`, and all manuscript + staging scenes.
>
> Produce `revisions/dev-plan-YYYY-MM-DD.md` with: diagnosis, structural priorities (ranked P1-P3+), scene-by-scene actions table, outline modifications, canon implications, revision budget estimate, human approval gate, and preserve-explicitly list.
>
> Do NOT write prose. Do NOT modify scenes. This is a plan for human review."

**HUMAN GATE.** After the plan is written, present its summary to the user and stop:

> Dev plan written to `revisions/dev-plan-YYYY-MM-DD.md`.
>
> Summary: {diagnosis first paragraph}
> P1 items: {count}
> P2 items: {count}
> P3 items: {count}
>
> Review the plan. When ready to execute, run: /novel-revise {slug} --stage dev --execute
>
> Or: /novel-revise {slug} --stage dev --execute P1 (only priority 1 items)

If `--execute` flag is present: invoke **scene-writer-agent** in revise mode for each scene-level action in the plan, in priority order. After all scenes rewrite, run continuity-check across the affected scenes. Then update scene frontmatter to `dev_status: passed` for all scenes that executed cleanly.

If any `outline-fix` actions exist in the plan, invoke **story-architect-agent** FIRST to apply scene-list/beat-sheet changes before scene rewrites.

### Stage: line

Pre-flight: identify target scenes. If `--scene <id>` given, scope to one. Otherwise, target all scenes with `dev_status: passed` AND `line_status: pending`.

If any target scene has `dev_status: pending|flagged`, STOP that scene and report. Do not silently skip.

For each target scene, invoke **line-edit-agent**:

> "Line-edit `novels/{slug}/staging/s{id}.md` (or manuscript path). Gate check: dev_status must be `passed`. Apply L1-L8 dimensions in passes (L1 POV/tense is binding). Edit in place. Update frontmatter: line_status: passed, status: line_clean. Append to log + CHANGELOG."

After each scene: re-invoke **continuity-checker-agent** scoped to that scene (edits can introduce drift).

### Stage: copy

Pre-flight: target scenes with `line_status: passed` AND `copy_status: pending`. Gate: line_status must be passed.

For each target scene, invoke **copy-edit-agent**:

> "Copy-edit `novels/{slug}/staging/s{id}.md`. Apply CP1-CP7. Maintain `style-sheet.yaml` — add new canonical entries as you normalize. Edit in place. Update frontmatter: copy_status: passed, status: copy_clean. Append to log + CHANGELOG."

### Stage: proof

Pre-flight: target scenes with `copy_status: passed` AND `proof_status: pending`. Gate: copy_status must be passed.

For each target scene, invoke **proof-agent**:

> "Proof `novels/{slug}/staging/s{id}.md`. Fix typos and mechanical glitches only. Flag anything requiring judgment to `revisions/proof-flags-YYYY-MM-DD.md`. Update frontmatter: proof_status: passed, status: proofed."

After proof passes for a scene, if all four `*_status` are `passed`:
- Move the scene file from `staging/` to `manuscript/chXX/s{id}.md`
- Update `status: GRADUATED`
- Promote relevant canon entries from C3 → C2 in `canon.jsonl` (append new entries noting promotion; do not overwrite)

## Step 3 — Report

Show:
- Stage: dev | line | copy | proof
- Scenes processed: N
- Scenes graduated (proof only): N
- Flags raised: N → path to flag file
- Next suggested stage

## Step 4 — Git snapshot

```bash
git add novels/{slug}/
git commit -m "novel: {slug} — revise {stage} $(date +%Y-%m-%d)

- Scenes processed: N
- Graduated: N
- Flags: N"
```
