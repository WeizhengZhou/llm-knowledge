Real-time verification of a specific claim before acting on it. This is the user-action gate — re-fetches the original source right now and compares it to the wiki claim.

## Parse arguments

Extract from the user's message:
- `"<claim>"` — required; the exact claim to verify (e.g., "SF School application deadline is January 23, 2026")
- `--topic {slug}` — required

Set `topic_dir = topics/{slug}/`.

Verify `{topic_dir}/_topic.yaml` exists. If not, tell the user to run `/kb-init` first.

---

## Step 1 — Invoke fact-checker-agent in user-action mode

Invoke **fact-checker-agent**:

> "**USER-ACTION MODE.** The user is about to act on this claim and needs immediate verification:
>
> **Claim:** '{claim}'
>
> Steps:
> 1. Search `{topic_dir}/wiki/**/*.md` for the article containing this claim. Note the article path.
> 2. From the article's frontmatter or body, identify the source URL(s) for this claim.
> 3. Re-fetch the source URL RIGHT NOW using WebFetch.
> 4. Compare the current live content to the claim in the wiki.
> 5. Return one of:
>    - **CONFIRMED** — source still says the same thing; claim is accurate as of today
>    - **CHANGED** — source has updated; provide the new accurate value
>    - **UNAVAILABLE** — source is gone or inaccessible; cannot confirm
> 6. If CHANGED: update the wiki article at the identified path with the corrected claim. Update the article's valid_until and sources frontmatter. Append a correction note to `{topic_dir}/log.md`.
> 7. If CONFIRMED: update the article's valid_until date to reflect re-verification today. Append to `{topic_dir}/log.md`.
>
> Always show the source URL, the date you fetched it, and the exact text you found."

---

## Step 2 — Report

Show the verdict prominently:

**If CONFIRMED:**
> ✓ CONFIRMED as of {today}: "{claim}"
> Source: {url} (fetched {timestamp})

**If CHANGED:**
> ✗ CHANGED — the wiki claim is outdated.
> Old: "{claim}"
> Current: "{new value}"
> Source: {url} (fetched {timestamp})
> Wiki has been updated automatically.

**If UNAVAILABLE:**
> ? UNAVAILABLE — source could not be re-fetched.
> Claim: "{claim}"
> Source attempted: {url}
> Treat this claim as unverified before acting.
> Suggested next: `/kb-ingest {slug} --url <alternative source>`
