---
critic_agent: wiki-critic-agent
reviewed: '2026-04-06'
article: staging/school-tour-guide.md
gate: NEEDS-REVISION
total_score: 5
---

# Critic Report — school-tour-guide.md

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| D1: Reader outcome alignment | 2 | Directly serves qs11 ("what questions should parents ask at open houses to actually learn something useful") — listed in the landscape as urgency: medium. Also serves pp3 (school fit anxiety / "how do you know if a school is actually a good fit for YOUR child") which is urgency: high. The article is well-targeted. |
| D2: Decision framing | 1 | The observation checklists (student engagement signals, K-specific observations) are genuinely useful for evaluating fit. The "Before / During / After" section gives process structure. However, the article does not help a parent make the decision it implies: given what you observed, how do you use that information? There is no framework for synthesizing observations into a school ranking, no guidance on what is a dealbreaker vs. a yellow flag, and no explicit link between what you observe at a tour and what you write in your parent essay (though [[parent-essay-guide]] is cross-linked in See Also). The tour is treated as an information-gathering activity; the article does not help the reader *decide* anything with the information gathered. |
| D3: Common mistakes quality | 2 | All four mistakes are non-obvious and well-chosen: attending passively (vs. just listening), visiting only your top choice (comparison reveals preferences), bringing your child to adult events (unintended memorability), and over-indexing on facilities. The "your child is memorable for the wrong reasons" framing is practical and specific. |
| D4: L4 synthesis presence | 0 | This is the article's critical failure. The entire article is sourced from a single L3 source (Cardinal Education) with no epistemic note blocks anywhere. Several high-stakes claims are presented as body prose without qualification: "most schools do not track attendance at optional events" (line 67, sourced from Ruth Krishnan L4), "schools value diverse family structures" (line 72, L4), "attending open houses increases likelihood admissions staff will recognize a family's name" (line 73, L4). The L4 community-sourced claims from ruthkrishnan.com are interleaved with L3 Cardinal Education claims without differentiation, violating the wiki's evidence discipline standard. A reader cannot tell which claims come from a consulting firm's blog vs. from a community observer. |
| D5: Scope discipline | 0 | The article has a significant scope violation: the Working Parent Logistics subsections (lines 52-89 in admissions-strategy-advanced.md) are partially re-derived here from the same Ruth Krishnan source, covering the same material (event load, missing open houses, one parent attending) that admissions-strategy-advanced.md covers in more depth. More critically, the "Practical Guidance for Working Parents" content (lines 76-90 of admissions-strategy-advanced.md) and the tour logistics content here overlap without the articles being clearly differentiated in scope. The school-tour-guide should not contain working-parent strategy; it should cross-link to [[admissions-strategy-advanced#working-parent-logistics]] for that content. Additionally, the "Questions You Should Not Ask" section (lines 82-88) is out of scope — the article's stated purpose is helping parents extract useful information, not managing admissions optics. |

**Total: 5 / 10 → GATE: NEEDS-REVISION**

## Required Revisions

Three structural fixes are required. The article's core content (observation checklists, question categories, K-specific guidance) is solid and should be preserved; the issues are epistemic discipline and scope containment.

### Fix 1: Add epistemic note blocks and differentiate source tiers (D4 — CRITICAL)

The article conflates L3 (Cardinal Education) and L4 (Ruth Krishnan) sources throughout. Add a source-tier header at the top of each section that draws from a distinct source:

1. Add a brief inline attribution whenever Ruth Krishnan is the source, using the same pattern as admissions-strategy-advanced.md: "Admissions consultant Ruth Krishnan reports that..." followed by an epistemic note block:

   ```
   > **Epistemic note:** The following working-parent observations are sourced from one
   > admissions consultant's guide (Ruth Krishnan, L4). Individual school expectations
   > vary. Head-Royce is the only named school to corroborate the claim that optional
   > events do not count against applicants.
   ```

2. The following specific claims require inline source attribution OR removal if they cannot be attributed:
   - "most schools do not track attendance at optional events" — attribute to Ruth Krishnan (L4) with caveat
   - "attending open houses increases likelihood admissions staff will recognize a family's name" — attribute to unnamed administrator via Ruth Krishnan (L4), double-hearsay flag needed
   - "schools remember disruptive behavior more than absence" — attribute to Ruth Krishnan (L4) with caveat that no school official is named

3. The "What Open Houses Typically Include" section (sourced from Cardinal Education) should be clearly labeled: "Cardinal Education describes..." (currently it is labeled correctly; this is a model to follow for the other sections).

### Fix 2: Remove working-parent strategy content and cross-link (D5)

Lines 52-89 of admissions-strategy-advanced.md cover working-parent logistics in more depth, including the same Head-Royce corroboration and tour registration urgency material. The school-tour-guide should not re-derive this from the same source. Remove:
- The entire "Does Missing Events Hurt Your Chances?" section (currently duplicated from admissions-strategy-advanced)
- The "Tour Registration Urgency" subsection

Replace with a single sentence in the "Getting the Most from Your Visit" section: "Working parents managing the event load across 5-7 schools, including which events are required vs. optional, see [[admissions-strategy-advanced#working-parent-logistics]]."

### Fix 3: Add a synthesis framework for turning observations into decisions (D2)

After the "After the Visit" subsection, add a brief section titled "Using Your Notes" (100-150 words):

The current article collects observations but does not help a parent use them. Add guidance on:
- **What to do with your notes:** Rate each school on 3-5 dimensions that matter most to your family (e.g., teacher warmth, play vs. academics, outdoor time). A forced ranking after visiting 3+ schools often reveals preferences you did not know you had.
- **Dealbreakers vs. yellow flags:** A teacher you observed speaking dismissively to a child is a dealbreaker. A classroom that felt crowded is a yellow flag worth asking about. Distinguish these when recording notes.
- **What to feed into the essay:** Specific observations from tours ("we noticed the K teacher called three children by name when they arrived") are the raw material for the "school fit" paragraph in your parent essay (see [[parent-essay-guide]]).

## Non-Blocking Issues

- **"Questions You Should Not Ask" (lines 82-88):** This section is admissions optics management, not tour intelligence-gathering. It belongs in a general admissions etiquette article or [[admissions-strategy]], not here. Remove or relocate.
- **Duplicate thank-you note reference (line 102):** This is the second article that mentions the thank-you note (parent-essay-guide.md also mentions it). Once the parent-essay-guide revision resolves canonical ownership, align accordingly.

## Verdict

**NEEDS-REVISION.** Score is 5/10. The article has genuinely strong observation checklists and K-specific guidance, but fails on epistemic note discipline (D4 = 0) and contains out-of-scope working-parent content that duplicates admissions-strategy-advanced.md (D5 = 0). The three required fixes above are scoped and implementable in a single revision pass by the wiki-compiler-agent. Article should return to staging for re-review after revision.
