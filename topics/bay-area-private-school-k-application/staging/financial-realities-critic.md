---
critic_agent: wiki-critic-agent
reviewed: '2026-04-06'
article: staging/financial-realities.md
gate: READY
total_score: 9
---

# Critic Report — financial-realities.md

## Scores

| Dimension | Score | Notes |
|-----------|-------|-------|
| D1: Reader outcome alignment | 2 | Directly serves pp1 (financial shock / true total cost), pp4 (financial aid opacity), and qs1/qs6 from the landscape pain-point inventory. These are rated "urgency: high". |
| D2: Decision framing | 2 | Closes with a concrete decision heuristic ("apply for aid if you need it"), the reach/match/safety cost budgeting model, the private-as-bridge strategy framing, and the explicit Common Mistakes list that reframes decisions parents get wrong. |
| D3: Common mistakes quality | 2 | All four mistakes are non-obvious: planning on sticker price only, assuming you earn too much for aid, not applying for aid due to admission fear, and using market averages that blend parochial with selective independents. None are generic. |
| D4: L4 synthesis presence | 2 | BPN community claims are clearly separated from L1/L2 data. Three distinct epistemic note blocks are present, each locating the specific source tier and its limitation. The need-blind claim escalation (L4 BPN → Nueva L1 only) is especially well-handled. |
| D5: Scope discipline | 1 | Minor drift: the article duplicates the application-cost budget paragraph from admissions-strategy-advanced.md verbatim (consultant fees, application fees). Also, the "private-as-bridge strategy" section belongs more naturally in guides/public-vs-private; here it is tacked on without clear financial framing. Neither drift is disqualifying. |

**Total: 9 / 10 → GATE: READY**

## Strengths

- The Nueva School income brackets section is the strongest fact-dense passage in any guide in the wiki: it is specific, cites confidence level and data vintage, and explicitly flags what has not been independently verified.
- Epistemic note blocks are used three times at precisely the right moments (aggregate cost projections, need-blind prevalence, income bracket extrapolations).
- The "Should You Apply for Aid?" section converts uncertainty into a concrete recommendation with a risk-reasoning structure, rather than hedging both ways.

## Issues (Non-blocking)

1. **Duplicate cost-budget paragraph (lines 56-57):** The application cost ranges (consultant fees $3K-$15K, testing $500-$1,500, fees $100-$200, annual fund $1K-$10K+) appear verbatim in `admissions-strategy-advanced.md` lines 49-51. When both articles land in wiki/, this will create redundancy and confuse readers about which article owns this information. Before promotion, add a `[[financial-realities#application-phase-costs]]` cross-reference in admissions-strategy-advanced and trim the duplication there.

2. **Private-as-bridge section (lines 140-144):** This strategy is framed as a financial risk-management tool, which is relevant here. However, the section concludes with a BPN community signal about public-to-private middle school paths that is also repeated in `admissions-strategy-advanced.md` lines 158-159. Consider whether this content belongs in [[guides/public-vs-private]] as primary and cross-linked from here, or vice versa.

3. **Confidence header says L3 but content includes L1 material:** The front-matter `confidence: L3` reflects the floor. Consider using `confidence: mixed (L1-L3)` or splitting by section, so readers understand that the Nueva data is L1 while the income bracket extrapolations are L3.

## Verdict

**READY for promotion to `wiki/guides/financial-realities.md`.**

The duplicate paragraph (issue 1) is the only item worth fixing pre-promotion; it should be resolved in admissions-strategy-advanced, not here. Issues 2 and 3 are low-priority cleanup items that can be addressed in a subsequent compiler pass.
