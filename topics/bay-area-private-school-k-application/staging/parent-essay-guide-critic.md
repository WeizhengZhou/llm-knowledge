---
critic_agent: wiki-critic-agent
reviewed: '2026-04-06'
article: staging/parent-essay-guide.md
gate: NEEDS-REVISION
total_score: 6
---

# Critic Report — parent-essay-guide.md

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| D1: Reader outcome alignment | 2 | Directly serves pp11 (application authenticity / where is the line between polished and fake) and qs14 (how authentic should parent essays be) — both listed in the landscape. These are real, named pain points. |
| D2: Decision framing | 1 | The "Should You Disclose Challenges?" section makes a concrete recommendation, as does the learning-differences disclosure framing. However, the article's most important decision — how to actually structure the essay — is never addressed. The "Writing Approach" section tells parents to "use specific anecdotes" and "customize for each school" but gives no decision framework for which themes to lead with, how to handle multiple competing angles, or what to do when the child's strongest trait is not the school's stated priority. The article tells readers *what* good essays do; it does not help them *decide* what to write. |
| D3: Common mistakes quality | 1 | Three of five mistakes (wrong school name, generic content, procrastination) are obvious and appear in virtually every admissions essay guide. Only "over-editing into inauthenticity" is genuinely non-obvious. The "over-answering" mistake is underexplained: at 500-1,500 characters, choosing two themes over five is obvious to any writer; the non-obvious insight would be which theme categories schools find most compelling vs. most redundant. |
| D4: L4 synthesis presence | 1 | The article correctly cites consulting sources as L3 and explicitly notes "No Bay Area school admissions office has published its essay evaluation rubric." However, there is no epistemic note block anywhere in the article, despite pp11 being sourced primarily from community intelligence (Ruth Krishnan, L4) and consultant blogs (L3). The claim that "admissions committees look for authentic introductions and may be wary if parents do not mention any challenges" — a high-stakes claim — is presented in body prose without a formal epistemic note, which is inconsistent with the wiki's evidence discipline standard. |
| D5: Scope discipline | 1 | The "After Submission: The Thank-You Note" section is an orphaned tip that duplicates content from school-tour-guide.md (which also covers thank-you notes after open houses/interviews). It does not connect to essay writing and creates a false implied scope ("this is an essay guide plus misc. post-submission guidance"). |

**Total: 6 / 10 → GATE: NEEDS-REVISION**

## Required Revisions

The article is close to passing (6/10, one point from READY). Three targeted fixes will bring it to READY in a single revision pass.

### Fix 1: Add a decision framework for essay structure (D2)

The "Writing Approach" section must answer: given that a parent has 500-1,500 characters and multiple true things to say about their child, how do they choose? Add a 100-150 word subsection titled "Choosing What to Write" that addresses:

- **Lead with what only your family can say.** Generic strengths (curious, kind, creative) are present in every essay. Unique observations (the specific anecdote, the specific school attribute you noticed on tour) differentiate.
- **Match to school mission:** A play-based school essay should lead with exploratory learning. An academically oriented school essay should lead with intellectual curiosity. Review the school's mission statement before choosing your theme.
- **One "area of growth" per essay:** Consulting sources agree that omitting challenges signals inauthenticity. Include exactly one, framed around how the child is growing, not what is wrong.

This converts the section from "what good essays do" to "how to decide what to write."

### Fix 2: Add epistemic note block for the "committees look for challenges" claim (D4)

The following passage (lines 24-25) currently reads as body prose:

> "admissions committees look for authentic introductions in parent essays and may be wary if parents do not mention any challenges the child has faced"

Replace the surrounding paragraph with this structure:

```
Admissions consulting sources (admission.org, PrepMatters, Cardinal Education) report that
admissions committees look for authentic introductions in parent essays and may be wary if
parents do not mention any challenges the child has faced.

> **Epistemic note:** This claim is sourced from three admissions consulting firms (L3),
> not from Bay Area school admissions officers. No school has published its essay
> evaluation rubric. The consensus across consulting sources is unusually consistent,
> which increases plausibility, but the claim has not been corroborated from L1 sources.
```

### Fix 3: Remove or relocate the thank-you note section (D5)

The "After Submission: The Thank-You Note" section (lines 80-84) is out of scope for an essay guide. Either:
- **Remove it entirely** and note in the See Also that thank-you notes are covered in [[school-tour-guide#after-the-visit]], or
- **Move it to school-tour-guide.md** as part of the "After the Visit" section where it logically belongs.

The section should not appear in both articles. Choose one as the canonical location.

## Non-Blocking Issues

- **Common Mistakes — strengthen two items (D3):** Replace "wrong school name" (this is editing hygiene, not an admissions insight) with a non-obvious mistake such as: "Writing about educational philosophy in the abstract — schools want to know your *child*, not your views on progressive education." Replace "procrastination" with a more specific version: "Treating all 5-7 essays as variants of one template — each customized essay takes 2-4 hours; plan accordingly."

- **Character count framing (line 56-58):** The parenthetical "(roughly 80-250 words)" is useful but the article never explains the practical implication: at 250 words, you have room for a single anecdote and two to three observations. This would strengthen the "what fits" guidance.

## Verdict

**NEEDS-REVISION.** Score is 6/10 (boundary of NEEDS-REVISION/READY). Three targeted fixes (decision framework for structure, epistemic note for challenge-disclosure claim, removal of thank-you section) will bring the article to READY in a single revision pass. The wiki-compiler-agent should implement these changes and return to staging for re-review.
