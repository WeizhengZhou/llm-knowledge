Answer a question about the novel from bible + canon + manuscript.

## Step 1 — Parse arguments

Extract:
- `slug` — required
- `question` — required, everything after slug in quotes or freeform

Set `novel_dir = novels/{slug}/`.

## Step 2 — Invoke query-agent (fiction mode)

Query-agent is reused from the KB pipeline. Tell it to operate in fiction mode:

> "Answer the question against the fiction knowledge base at `novels/{slug}/`.
>
> Question: {question}
>
> Sources to search, in order:
> 1. `canon.jsonl` — established facts (grep for subject keywords)
> 2. `bible/characters/*.md`, `bible/world/*.md`, `bible/timeline.yaml`, `bible/style-guide.md`
> 3. `outline/scene-list.yaml` — for questions about scene order, POV, chapter structure
> 4. `manuscript/**/*.md` and `staging/**/*.md` — for questions about what happens in a specific scene (grep first to find relevant scenes; do not load all)
> 5. `premise.md` — for questions about theme, ending, intent
>
> Answer using the canon tier hierarchy:
> - Prefer C1 (bible-canon) over C2 (prose-canon) only when they disagree and the bible is more recently updated
> - Prefer C2 over C3 (draft-canon) always
> - Cite the canon entry ID (e.g., c0042) OR bible file + scene id for every factual claim
> - If the question asks about the author's intent, cite premise.md or scene-list.yaml
> - If the question cannot be answered from current sources, say so — do not invent"

## Step 3 — Return the answer

Return the answer verbatim to the user with citations. If the answer reveals a gap or contradiction in canon, note it at the end.

Do NOT commit (read-only operation).
