Add a single source to a topic's knowledge base and integrate it into the wiki.

## Parse arguments

Extract from the user's message:
- `--topic {slug}` — required
- `--url {url}` — a web page to fetch
- `--file {path}` — a local file to ingest
- Exactly one of --url or --file is required.

Set `topic_dir = topics/{slug}/`.

Verify `{topic_dir}/_topic.yaml` exists. If not, tell the user to run `/kb-init` first.

---

## Step 1 — Fetch or copy the source

**If --url:** Use **research-agent** to fetch it:

> "Fetch this URL: {url}. Save it to `{topic_dir}/raw/web/{tier}/YYYY-MM-DD_{slug}.md` with frontmatter: url, fetched timestamp, question_id 'manual-ingest', reliability_tier (assess from the domain: L1 for official sites, L2 for news, L3 for review platforms, L4 for forums), content_hash. Append a search record to `{topic_dir}/raw/search-log.jsonl` with question_id 'manual-ingest'."

**If --file:** Copy the file to `{topic_dir}/raw/manual/{filename}`. Add frontmatter noting it was human-provided with reliability_tier L1.

---

## Step 2 — Extract claims from the new source only

Invoke **claim-extractor-agent** on the single new file:

> "Read `{source_file}`. Extract all factual claims: type them, assign priority, flag overreach. Append new claims to `{topic_dir}/claims-register.yaml` (do not duplicate existing claims). Group by entity."

---

## Step 3 — Verify new claims

Invoke **fact-checker-agent** in batch mode on only the new claims:

> "Read `{topic_dir}/claims-register.yaml` and filter to claims with no verdict. Cross-reference against existing raw sources and the new source. Assign L1-L5 confidence and permitted language. Append results to `{topic_dir}/fact-sheet.yaml`."

---

## Step 4 — Update affected wiki articles

Invoke **wiki-compiler-agent** in update mode:

> "Read the new source at `{source_file}` and `{topic_dir}/fact-sheet.yaml`. Identify which existing wiki articles in `{topic_dir}/wiki/` are affected by this new information. Update those articles with new data (using permitted language). If the source introduces an entity or concept not yet in the wiki, create a new article. Update `{topic_dir}/index.md`, `{topic_dir}/wiki/_index.md`, and append to `{topic_dir}/log.md`."

---

## Step 5 — Report

Show:
- Source saved at path
- N new claims extracted (N must_verify, N should_verify)
- N claims verified (N confirmed, N disputed, N blocked)
- Wiki articles updated or created
- Suggested next: `/kb-lint {slug}` to check for new issues
