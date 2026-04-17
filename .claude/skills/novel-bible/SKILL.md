Generate the story bible — characters, world, timeline, style-guide.

## Step 1 — Parse arguments

Extract:
- `slug` — required

Set `novel_dir = novels/{slug}/`. Verify `outline/scene-list.yaml` has scenes (empty scenes list means outline hasn't run).

## Step 2 — Invoke story-architect-agent in bible mode

> "Run in bible mode for `novels/{slug}/`. Time-boxed: ONE session.
>
> 1. Read `_novel.yaml`, `premise.md`, `outline/scene-list.yaml`, `outline/beat-sheet.yaml`.
> 2. For every named character who appears in 3+ scenes OR is POV for any scene: produce `bible/characters/{slug}.md` using the stub-first template (role, one-line, wants/needs, voice-if-POV, sparse physical, arc, relationships). Do NOT exceed 500 words per character.
> 3. Produce `bible/world/setting.md`, `bible/world/rules.md`, `bible/world/culture.md`, `bible/world/geography.md` — each ≤ 500 words. Functional, not exhaustive.
> 4. Populate `bible/timeline.yaml` with backstory beats + in-novel chronology.
> 5. Expand `bible/style-guide.md` — voice register, dialogue conventions, sentence-level rules, worldbuilding terminology. Do NOT override the POV and tense set in `_novel.yaml`.
> 6. Seed `canon.jsonl` with C1 entries for every bible fact (character physical details, world rules, timeline events). Format per canon-extractor-agent convention.
> 7. Append to `log.md` and `CHANGELOG.md`. Update `_novel.yaml` → phase_status.bible = 'complete'.
>
> Hard cap: if you find yourself writing more than 500 words on any character or world file, stop and summarize. Let canon-extraction fill in the rest during drafting."

## Step 3 — Report to user

Show:
- Character files created: N
- World files created
- C1 canon seeds: N
- Style-guide sections filled
- Suggested next: `/novel-draft {slug}` or `/novel-write {slug} --scene 001`

## Step 4 — Git snapshot

```bash
git add novels/{slug}/
git commit -m "novel: {slug} — bible generated $(date +%Y-%m-%d)

- Character files: N
- World files: N
- C1 canon seeds: N"
```
