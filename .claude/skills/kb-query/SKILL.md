Answer a question against the wiki knowledge base. The query-agent synthesizes answers from wiki articles, detects when the user is about to act on a claim, and files valuable answers back into the wiki.

## Parse arguments

Extract from the user's message:
- `"<question>"` — required; the question to answer
- `--topic {slug}` — required
- `--depth quick|standard|deep` — optional; default is `standard`

Set `topic_dir = topics/{slug}/`.

Verify `{topic_dir}/_topic.yaml` exists. If not, tell the user to run `/kb-init` first.

---

## Step 1 — Detect user-action signals

Before invoking the agent, scan the user's message for user-action linguistic signals:

**User-action triggers:** "I'm going to", "I'm about to", "I want to submit", "I'm applying", "I plan to", "before I", "can I now", "should I go ahead"

If a trigger is detected, set `user_action_mode = true` and note the intended action.

---

## Step 2 — Invoke query-agent

Invoke **query-agent**:

> "Answer this question: '{question}'. Topic directory: `{topic_dir}`.
>
> Depth level: **{depth}** (quick = read _index.md + top articles only; standard = full wiki search + cross-reference; deep = wiki + live web search).
>
> {IF user_action_mode}: **USER-ACTION MODE ACTIVE.** The user is about to: '{intended_action}'. Before completing your answer, re-verify any volatile claims (deadlines, tuition, enrollment numbers) against their original sources using WebFetch. Return a CONFIRMED / CHANGED / UNAVAILABLE verdict for each volatile claim.
>
> Steps:
> 1. Read `{topic_dir}/wiki/_index.md` to find relevant articles.
> 2. Read relevant wiki articles (all for standard; targeted for quick; wiki + WebSearch for deep).
> 3. Synthesize a precise answer with citations to specific wiki articles.
> 4. Include the evidence tier (L1-L4) of each key claim.
> 5. If the answer reveals a gap, add a `qQ`-prefixed question to `{topic_dir}/research-plan.yaml` under `phases.gap_fill.questions`.
> 6. If this answer adds durable knowledge not yet in the wiki, write or update the relevant article in `{topic_dir}/wiki/`.
> 7. Append a query record to `{topic_dir}/log.md`."

---

## Step 3 — Report

Show the agent's answer directly. The agent's output should include:
- The answer with inline citations (`[[wikilink]]` format)
- Evidence tier (L1-L4) for key claims
- If user-action mode: CONFIRMED / CHANGED / UNAVAILABLE verdict per volatile claim
- Any gap questions added to the research plan
- Whether any wiki article was updated or created
- If coverage was insufficient, suggest: `/kb-research {slug} --phase gap`
