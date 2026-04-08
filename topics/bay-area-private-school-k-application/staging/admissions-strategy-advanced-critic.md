---
critic_agent: wiki-critic-agent
reviewed: '2026-04-06'
article: staging/admissions-strategy-advanced.md
gate: READY
total_score: 8
---

# Critic Report — admissions-strategy-advanced.md

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| D1: Reader outcome alignment | 2 | Directly serves pp2 (emotional toll on working parents), pp6 (waitlist helplessness), pp8 (portfolio strategy), and qs5 (rejection recovery) — all rated urgency: high in the landscape. |
| D2: Decision framing | 2 | Every major section closes with a concrete action: the waitlist section gives four numbered steps; the rejection section has three numbered next steps; working parents section distills to one-sentence heuristic ("strategic participation over attendance volume") with a prioritized list. |
| D3: Common mistakes quality | 2 | Four mistakes, all non-obvious: applying only to reach schools, waitlist panic during the wrong window, treating rejection as a child referendum, and burning bridges before reapplication. None are generic. The panicking-during-the-wrong-window mistake is especially well-grounded in the ISSFBA March 19-26 mechanic. |
| D4: L4 synthesis presence | 1 | Epistemic notes are present for the three highest-risk sections (application volume, working-parent logistics, rejection recovery). However, the Waitlist Strategy section draws from "admissions prep sources" (xceedprep.org, an L3 aggregator) that are cited without a formal epistemic note block. The 5-15% and 15-30% waitlist acceptance rates are given in body text only, with the disclaimer buried in a separate blockquote. Given these are the most anxiety-driving statistics in the article, they deserve a formal epistemic note block. |
| D5: Scope discipline | 1 | The application-cost budget paragraph (lines 49-51) duplicates financial-realities.md verbatim. The "public-to-private path" subsection (lines 157-163) partially duplicates the same content in financial-realities.md. These are cross-wiki duplicates, not scope drift within the article itself — but they reflect that the compiler did not resolve overlap between these two articles. |

**Total: 8 / 10 → GATE: READY**

## Strengths

- The ISSFBA March 19-26 window is used as a concrete anchor throughout the waitlist section, which is exactly the right approach for Bay Area-specific guidance.
- "Ranked vs. pooled waitlist" distinction is non-obvious and practically important; the article explains its implications (position vs. class-composition need) without overstating what is known about individual school practices.
- Working parent section correctly names the single school (Head-Royce) that corroborates the consultant claim, rather than treating Ruth Krishnan's observation as broadly verified.
- Rejection framing ("class composition, sibling seats, financial aid budgets are factors families cannot see") is psychologically sound and consistent with L4 community intelligence without overclaiming causation.

## Issues (Non-blocking)

1. **Waitlist acceptance rates need an epistemic note block (lines 118-123):** The 5-15% / 15-30% figures are the most memorable numbers a reader will take away from this article. The source (xceedprep.org) is an admissions prep aggregator — an L3 source at best — and the figures are national estimates, not Bay Area data. The current prose disclaimer ("This is a general private school estimate with no Bay Area-specific data cited") is present but is inline text rather than a formatted epistemic block. Add a formal `> **Epistemic note:**` block matching the style used elsewhere in the article. This is the minimum fix needed before promotion.

2. **Application-cost paragraph (lines 49-51):** Duplicates financial-realities.md. Replace with a one-sentence cross-reference: "For application-phase cost budgeting (fees, consultants, testing), see [[financial-realities#application-phase-costs]]."

3. **Public-to-private path subsection (lines 157-163):** This information is also in financial-realities.md. One article should be primary; cross-link from the other. Given that financial-realities.md frames it as a financial risk-management strategy (its natural home), trim this subsection to a one-sentence pointer: "For families considering private K as a 1-2 year bridge before public school entry, see [[financial-realities#private-as-bridge-strategy]]."

## Verdict

**READY for promotion to `wiki/guides/admissions-strategy-advanced.md`.**

Issue 1 (epistemic note block for waitlist rates) should be fixed before promotion by the wiki-compiler-agent in a minimal revision pass. Issues 2 and 3 are cleanup items that should be resolved when financial-realities.md lands in wiki/ and the duplicate content can be replaced with cross-references.
