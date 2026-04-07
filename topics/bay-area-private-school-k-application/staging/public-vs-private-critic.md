# Critic Report: public-vs-private.md

**Article:** Public vs. Private K -- The Bay Area Decision Framework
**Type:** guide
**Reviewed:** 2026-04-06
**Reviewer:** wiki-critic-agent

---

## Dimension Scores

### D1: Reader Outcome Alignment — 2/2

The public-vs-private decision is foundational to the entire knowledge base — it is the first decision a Bay Area K family makes, and it gates whether they enter the private school pipeline at all. The research plan includes Q004 (tuition ranges), Q008 (cost/value), and multiple questions about financial aid and decision-making. While not a top-scored research question on its own, it addresses the prerequisite framing that every reader needs before the more detailed application guidance becomes relevant.

The article explicitly links to downstream articles (`[[financial-aid]]`, `[[transitional-kindergarten]]`, `[[admissions-strategy]]`), positioning itself correctly as an entry-point guide. Score: **2**.

### D2: Decision Framing — 1/2

This is the article's weakest dimension. The "Key Considerations" section lists five factors, which is good, but they read more as a checklist than a decision framework. The article does not give the reader a decision rule or a structured way to reach a conclusion. For example:

- When should a family pursue private over public? The article describes the financial scale and SFUSD lottery uncertainty but does not synthesize these into "if X, then consider private" logic.
- The parochial vs. independent cost comparison is useful but not framed as a decision branch (e.g., "if budget is the primary constraint, parochial schools may be a better fit than foregoing private entirely").
- The "Common Mistakes" section is better framed — it tells readers what errors to avoid — but does not compensate for the absence of a structured decision path in the body.

The article is substantially informational, providing context for a decision without fully guiding readers through it. Score: **1**.

### D3: Common Mistakes Quality — 2/2

All three common mistakes are genuinely non-obvious:

1. **Not modeling the full K-12 cost:** Intuitive to think in yearly terms; non-obvious to compound 4-5% annual increases over 13 years to reach the $500K-$700K estimate.
2. **Treating private as all-or-nothing:** Many parents are unaware of parochial school pricing ($6,000-$10,000/year vs. $40,000-$50,000), which makes the "private school" category appear more monolithic than it is.
3. **Ignoring the SFUSD timeline:** The March timing overlap between SFUSD lottery results and private school decision letters is a genuinely non-obvious logistical fact that enables a "both tracks" strategy most first-time applicants wouldn't discover independently.

These are real, high-stakes mistakes with concrete consequences. Score: **2**.

### D4: L4 Synthesis Presence — 1/2

The article contains one epistemic note block flagging a partially-fetched source (basicfund.org). This is appropriate and correctly handled.

However, there is a problematic sentence that appears without a note block:

> "Some Bay Area education sources report that public school quality varies by district, with Palo Alto, Berkeley, and Piedmont frequently cited as having strong academic reputations. No specific test scores or rankings were cited in the source material to substantiate this claim."

This sentence is itself an admission of an unsubstantiated claim — the article flags its own weakness inline rather than removing the content or placing it in a proper epistemic note block. The content should either be (a) removed as unverifiable, (b) elevated to a cited source with specific data, or (c) placed in an epistemic note block with appropriate L4 framing. As written, it is awkward and mildly undermines the article's credibility. Score: **1**.

### D5: Scope Discipline — 2/2

The article stays within its declared scope. Financial mechanics are deferred to `[[financial-aid]]`, TK details to `[[transitional-kindergarten]]`, and strategy to `[[admissions-strategy]]`. The SFUSD lottery explanation is brief and purposeful (it explains *why* families apply to both tracks) rather than drifting into a full public school comparison.

The Basic Fund section is proportionate — it introduces an access resource relevant to the financial scale discussion without expanding into a full Basic Fund profile. Score: **2**.

---

## Summary

| Dimension | Score | Max |
|-----------|-------|-----|
| D1: Reader outcome alignment | 2 | 2 |
| D2: Decision framing | 1 | 2 |
| D3: Common mistakes quality | 2 | 2 |
| D4: L4 synthesis presence | 1 | 2 |
| D5: Scope discipline | 2 | 2 |
| **Total** | **8** | **10** |

---

## Gate Decision: READY (total = 8, threshold ≥ 7)

Total score 8/10. No D1=0. Article clears the gate but has two specific weaknesses that should be addressed in the next edit cycle. It is promotable now; revisions can be made post-promotion.

**Promote to:** `wiki/guides/public-vs-private.md`

---

## Revision Instructions (post-promotion, next edit cycle)

### R1 — Strengthen decision framing (D2)
Add a "When to Pursue Private K" subsection before or after "Key Considerations" that gives readers a structured decision path. Example structure:

> - If SFUSD lottery uncertainty is the primary driver → apply to private as a hedge while pursuing your preferred public school
> - If budget is a binding constraint → evaluate parochial schools ($6K-$10K/year) before ruling out private entirely
> - If educational philosophy is the driver → proceed to [[admissions-strategy]] and [[pedagogy-philosophy]] for school-list guidance
> - If income qualifies for aid → verify eligibility before ruling out independent schools (some cover 50-75% of tuition)

This structure transforms the article from "here is information about the decision" to "here is how to make the decision."

### R2 — Fix the unsubstantiated public school quality claim (D4)
The sentence beginning "Some Bay Area education sources report that public school quality varies by district..." should be either:
- **Removed** (weakest option; the underlying point is valid but the sourcing is inadequate)
- **Rewritten** as a proper epistemic note block: `> **Epistemic note:** Some sources cite Palo Alto, Berkeley, and Piedmont USD as strong public school districts, but no verified test score or ranking data was available in the source material. This claim is directional only (L4).`
- **Substantiated** with a specific source (e.g., CAASPP scores, Niche district rankings) if the research-agent can locate one during a future refresh.
