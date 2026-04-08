---
critic_agent: wiki-critic-agent
reviewed: '2026-04-06'
article: staging/parent-essay-guide.md
prior_gate: NEEDS-REVISION
prior_score: 6
gate: READY
total_score: 9
---

# Re-Review Report — parent-essay-guide.md

## Required Fixes — Implementation Status

### Fix 1: Decision framework for essay structure (D2) — IMPLEMENTED

The original article had a "Writing Approach" section that described what good essays do but gave no framework for deciding what to write. The revised article replaces this with a dedicated "Choosing What to Write" section (lines 41-51) that provides exactly the required decision framework:

- **Lead with what only your family can say** — implemented as the anecdote-vs-adjectives contrast ("Instead of 'Our daughter is curious, creative, and kind,' write about the specific moment...")
- **Match to school mission** — implemented as conditional bullets: play-based school leads with exploratory learning, academically oriented leads with intellectual curiosity, trait-mismatch case also handled
- **One "area of growth" per essay** — implemented explicitly: "include exactly one 'area of growth' framed around how the child is developing, not what is wrong"
- **Planning implication** — implemented: "each essay takes 2-4 hours of focused writing; plan your calendar accordingly"

The framework also covers the case the critic specifically called out: "what to do when the child's strongest trait is not the school's stated priority." This is a genuine improvement over the original.

### Fix 2: Epistemic note block for the "committees look for challenges" claim (D4) — IMPLEMENTED

The revised article (lines 24-29) contains the required epistemic note block in the specified format, attributed to three admissions consulting firms (L3), explicitly noting that no Bay Area school has published its essay evaluation rubric and that the claim has not been corroborated from L1 sources. The surrounding paragraph is correctly attributed: "Admissions consulting sources (admission.org, PrepMatters, Cardinal Education) report that..."

This is an exact implementation of the critic's required revision.

### Fix 3: Removal of thank-you note section (D5) — IMPLEMENTED

The "After Submission: The Thank-You Note" section has been removed entirely from the essay guide. The See Also section now correctly redirects: `[[school-tour-guide]] -- What to observe at open houses and tours; thank-you notes after visits`. This establishes school-tour-guide as the canonical location for thank-you note guidance, resolving the duplication.

---

## Re-Scores

| Dimension | Prior | Revised | Notes |
|-----------|-------|---------|-------|
| D1: Reader outcome alignment | 2 | 2 | Unchanged — article still directly serves pp11 and qs14. |
| D2: Decision framing | 1 | 2 | "Choosing What to Write" now provides a genuine decision framework with conditional branches for each scenario a parent faces: mission-match, challenge-disclosure, trait-mismatch, and multi-school volume. This is actionable, not descriptive. |
| D3: Common mistakes quality | 1 | 2 | Two of the weaker items from the original have been replaced. "Wrong school name" (editing hygiene) is gone; in its place is "Writing about educational philosophy in the abstract" — a non-obvious mistake specific to this context. "Procrastination" is gone; in its place is "Treating all 5-7 essays as variants of one template" with the specific planning cost (2-4 hours per essay) that makes it actionable. All five mistakes are now genuinely non-obvious for this audience. |
| D4: L4 synthesis presence | 1 | 2 | Epistemic note block is present (lines 26-29), correctly formatted, and attached to the high-stakes claim it qualifies. Source-tier labeling is consistent throughout the article ("admissions consulting sources," "admission.org states," "Cardinal Education reports"). No L4 claims are presented as body prose without qualification. |
| D5: Scope discipline | 1 | 2 | Thank-you note section removed. See Also cross-links are clean and non-redundant. Article scope is now tightly limited to essay writing and disclosure decisions. No orphaned sections. |

**Total: 9 / 10 → GATE: READY**

---

## Remaining Non-Blocking Issues

The two non-blocking issues from the original report were optional. Both have been addressed:

- **"Wrong school name" and "procrastination" replaced** — done as noted in D3 above.
- **Character count practical implication** — implemented: line 43 now reads "At 500-1,500 characters, you have roughly 80-250 words -- room for a single anecdote and two to three observations. Every sentence must earn its place." And line 82 reinforces: "At 250 words, you have room for a single anecdote and two to three supporting observations."

No non-blocking issues remain.

---

## Verdict

**READY.** Score is 9/10. All three required fixes have been correctly implemented. The article now provides the decision framework the original lacked, applies epistemic discipline to its highest-stakes claim, and has resolved the scope duplication with school-tour-guide. The article is ready to graduate from staging to `wiki/guides/parent-essay-guide.md`.
