Initialize a new novel project — directory scaffolding + premise template.

## Step 1 — Parse arguments

Extract from the user's message:
- `title` — required, quoted
- `--genre <g>` — optional
- `--pov <pov>` — optional (default 3rd-limited)
- `--tense <t>` — optional (default past)
- `--target-words <n>` — optional (default 90000)
- `--audience <a>` — optional (default adult)

## Step 2 — Scaffold

Run:
```bash
python -m backend.novel_pipeline init-novel "<title>" \
  --genre "<g>" --pov "<pov>" --tense "<t>" \
  --target-words <n> --audience "<a>"
```

This creates `novels/{slug}/` with all subdirectories and seed files.

Read `novels/{slug}/_novel.yaml` to confirm slug.

## Step 3 — Prompt the human to fill in premise

Do NOT run story-architect-agent yet. `premise.md` needs the author's logline, ending, and themes before outlining can proceed.

Tell the user:

```
Initialized: novels/{slug}/

Next step: open novels/{slug}/premise.md and fill in:
  - Logline (1 sentence)
  - Ending (2-5 sentences — REQUIRED before outlining)
  - Themes (2-4 bullets)
  - Audience
  - Comp titles

When premise.md is filled in, run: /novel-outline {slug}
```

## Step 4 — Git snapshot

```bash
git add novels/{slug}/ backend/novel_pipeline.py NOVEL.md 2>/dev/null
git commit -m "novel: {slug} — scaffolded $(date +%Y-%m-%d)"
```
(Skip if nothing to commit.)
