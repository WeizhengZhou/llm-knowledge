Generate beat sheet + scene list for a novel.

## Step 1 — Parse arguments

Extract:
- `slug` — required, positional

Set `novel_dir = novels/{slug}/`. Verify `_novel.yaml` exists. If not, tell the user to run `/novel-init` first.

## Step 2 — Gate check: ending in premise

Read `novel_dir/premise.md`. Check that the **Ending** section contains content beyond the placeholder. If empty or placeholder, STOP and tell the user:

> `premise.md` has no ending. Fiction requires ending-first outlining (Sanderson's rule). Open `novels/{slug}/premise.md` and fill in the Ending section, then re-run `/novel-outline {slug}`.

Do NOT proceed to invoking story-architect-agent without an ending.

## Step 3 — Invoke story-architect-agent in outline mode

> "Run in outline mode for `novels/{slug}/`.
>
> 1. Read `_novel.yaml`, `premise.md` (confirm ending is present), and any existing bible files.
> 2. Choose a structure method: save-the-cat | snowflake | story-grid | 3-act — based on genre, length, audience, and comps. Write choice to `_novel.yaml` → structure_method AND `outline/beat-sheet.yaml` → structure_method. Explain the choice in one sentence to the log.
> 3. Produce `outline/beat-sheet.yaml` with novel-specific (non-generic) beats tied to themes.
> 4. Produce `outline/scene-list.yaml` with goal/conflict/outcome per scene, POV, beat linkage, word targets, and canon_seeds.
> 5. Self-check: every beat has at least one scene; the final scene realizes the ending; stakes rise; POV distribution is intentional.
> 6. Append to `log.md` and `CHANGELOG.md`."

## Step 4 — Report to user

Show:
- Structure method chosen + 1-sentence rationale
- Number of beats
- Number of scenes + rough target word count
- Top-level arc (opening → midpoint → climax → resolution, one sentence each)
- Suggested next: `/novel-bible {slug}`

## Step 5 — Git snapshot

```bash
git add novels/{slug}/
git commit -m "novel: {slug} — outline generated $(date +%Y-%m-%d)

- Structure: {method}
- Beats: N
- Scenes: N
- Target words: N"
```
