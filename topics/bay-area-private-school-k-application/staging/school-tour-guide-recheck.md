---
critic_agent: wiki-critic-agent
reviewed: '2026-04-06'
article: staging/school-tour-guide.md
prior_gate: NEEDS-REVISION
prior_score: 5
gate: READY
total_score: 8
---

# Re-Review Report — school-tour-guide.md

## Required Fixes — Implementation Status

### Fix 1: Epistemic note blocks and source-tier differentiation (D4 — CRITICAL) — IMPLEMENTED

The original article failed this dimension entirely (D4 = 0) because L3 and L4 claims were interleaved without differentiation and presented as body prose. The revised article addresses this:

- The Overview (line 20) now explicitly states: "The source material is primarily from Cardinal Education (L3 admissions consulting firm); actual event structures vary by school."
- Each major section with Cardinal Education sourcing is clearly attributed: "Cardinal Education describes...", "Cardinal Education recommends observing...", "Cardinal Education recommends asking..."
- The "After the Visit" subsection contains a proper epistemic note block (lines 98-100) for the thank-you note recommendation: "Admissions consulting source admission.org (L3). No Bay Area school has confirmed that thank-you notes influence admissions decisions."

**Partial gap:** The three specific high-stakes L4 claims the original critic flagged — (1) "most schools do not track attendance at optional events," (2) "attending open houses increases likelihood admissions staff will recognize a family's name," and (3) "schools remember disruptive behavior more than absence" — are no longer present in the revised article at all. The working-parent logistics content that contained these claims has been removed (see Fix 2). This is an acceptable resolution: the claims were removed rather than misattributed, which is the safer approach under the wiki's evidence discipline standard.

The article now has consistent source-tier labeling throughout. D4 is substantially repaired.

### Fix 2: Working-parent strategy content removed and cross-linked (D5) — IMPLEMENTED

The "Does Missing Events Hurt Your Chances?" section and "Tour Registration Urgency" subsection have been removed. The revised article replaces them with a single cross-link sentence (line 89): "Working parents managing the event load across 5-7 schools, including which events are required vs. optional, see [[admissions-strategy-advanced]]."

This is the exact text the critic requested. The scope violation that caused D5 = 0 has been resolved.

**Partial gap on the non-blocking issue:** The "Questions You Should Not Ask" section has also been removed. The critic flagged this as non-blocking but recommended removal or relocation. Its absence improves scope discipline further and is the correct call.

### Fix 3: Synthesis framework for turning observations into decisions (D2) — IMPLEMENTED

The revised article contains a new "Using Your Tour Notes to Decide" section (lines 107-117) with four concrete guidance items:

- **Rate each school on 3-5 dimensions** — implemented with the forced-ranking framework
- **Dealbreakers vs. yellow flags** — implemented with a concrete example distinguishing a dismissive teacher (dealbreaker) from a crowded classroom (yellow flag)
- **Patterns across visits** — added; not required by the critic but improves the synthesis framework
- **Feed observations into your essay** — implemented with an explicit cross-link to [[parent-essay-guide]]

This directly addresses the D2 gap: the article no longer treats the tour as information-gathering only. It now tells parents what to do with what they observed.

---

## Re-Scores

| Dimension | Prior | Revised | Notes |
|-----------|-------|---------|-------|
| D1: Reader outcome alignment | 2 | 2 | Unchanged — article still directly serves qs11 and pp3. |
| D2: Decision framing | 1 | 2 | "Using Your Tour Notes to Decide" now provides a genuine decision framework: a rating methodology, dealbreaker vs. yellow-flag distinction, pattern recognition across multiple visits, and explicit feed-forward to the essay. The article now helps parents use their observations, not just collect them. |
| D3: Common mistakes quality | 2 | 2 | Unchanged — all four mistakes remain and are still non-obvious and well-chosen. |
| D4: L4 synthesis presence | 0 | 1 | Major improvement: source-tier labeling is consistent throughout, L4 content from Ruth Krishnan has been removed rather than misattributed, and an epistemic note block is present for the thank-you note claim. The article does not achieve a 2 here because the epistemic note coverage is narrow (only the thank-you note claim gets an explicit note block; the section-level Cardinal Education attribution is adequate but there is no general epistemic note in the Overview formally explaining the evidence-tier landscape of the article as a whole). This is a minor gap and does not prevent READY. |
| D5: Scope discipline | 0 | 2 | Working-parent content fully removed and cross-linked. "Questions You Should Not Ask" removed. Thank-you note canonical ownership resolved with parent-essay-guide. The revised article's scope is tightly focused: what to observe, what to ask, how to synthesize. No orphaned sections, no duplication with admissions-strategy-advanced. |

**Total: 8 / 10 → GATE: READY**

---

## Remaining Non-Blocking Issues

One minor issue remains:

- **Epistemic note coverage in the Overview (D4 minor):** The Overview names Cardinal Education as the primary source but does not give readers a brief orientation to the evidence tier of the entire article (e.g., "All guidance is L3 consulting-source synthesis unless otherwise noted; no school admissions officers are quoted directly"). Adding one sentence of this form to the Overview would bring D4 to a clean 2. This is non-blocking for graduation to wiki/.

The two non-blocking issues from the original report are resolved:
- "Questions You Should Not Ask" removed (see Fix 2 above).
- Duplicate thank-you note reference resolved: school-tour-guide now carries the thank-you note content (with epistemic note); parent-essay-guide cross-links to it. Canonical ownership is established.

---

## Verdict

**READY.** Score is 8/10. All three required fixes have been correctly implemented. The critical D4 failure (epistemic discipline) is repaired through consistent source attribution and removal of unsourced L4 claims. The D5 scope violation is resolved through removal and cross-linking. The new synthesis section resolves D2. One minor non-blocking gap in D4 coverage remains but does not prevent graduation. Article is ready to move to `wiki/guides/school-tour-guide.md`.
