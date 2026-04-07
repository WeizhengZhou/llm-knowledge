Initialize a new knowledge base topic, then generate its research question tree.

## Step 1 — Scaffold the directory

Extract the topic name from the user's message. If a `--context` flag is present, extract that too.

Run:
```bash
python -m backend.pipeline init "<topic name>" --context "<context if provided>"
```

This creates `topics/{slug}/` with all subdirectories, `_topic.yaml`, `index.md`, `log.md`, `manifest.json`, and an empty `research-plan.yaml`.

Read `topics/{slug}/_topic.yaml` to confirm the slug.

## Step 2 — Generate the research question tree

Use the **research-planner-agent** to fill in `topics/{slug}/research-plan.yaml`.

Tell it:
- The topic name and user context (from `_topic.yaml`)
- The budget constraints (from `_topic.yaml`)
- To write questions across all 8 facets: WHO, WHAT, WHEN, WHERE, HOW, WHY, COMPARE, META
- To score each question on: user_value (0-10), dependency_count (0-10), searchability (0-10), novelty (0-10)
- To assign phases: breadth (landscape), depth (per-entity), gap_fill (targeted)
- To identify dependencies between questions
- To save the complete plan to `topics/{slug}/research-plan.yaml`

## Step 3 — Report to the user

Show:
- Topic slug and directory
- Number of questions generated, broken down by facet and phase
- Top 5 highest-priority questions (by composite score)
- Suggested next command: `/kb-research {slug}`
