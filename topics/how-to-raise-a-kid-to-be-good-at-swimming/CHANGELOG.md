# Changelog -- How to Raise a Kid to Be Good at Swimming

_Append-only log of all wiki modifications. Each entry records what changed, what was added/removed, and why._

## 2026-04-09 -- wiki-compiler-agent

**Added:**
- `staging/getting-started.md` -- Guide: when/how to start swim lessons; program types; readiness checklist
- `staging/choosing-a-club-and-coach.md` -- Guide: credentials, questions, red flags, trial period
- `staging/developmental-pathway.md` -- Guide: LTAD stages; age benchmarks; training volume
- `staging/recreational-to-competitive.md` -- Guide: decision framework for rec-to-club switch
- `staging/swim-meets-explained.md` -- Guide: Pacific Swimming meets; time standards; first meet
- `staging/parent-playbook.md` -- Guide: evidence-based parent behaviors; "I love watching you swim"
- `staging/costs-and-commitment.md` -- Guide: cost breakdown $200-$15K+; Bay Area estimates
- `staging/preventing-burnout.md` -- Guide: dropout causes; burnout risk; prevention strategies
- `staging/ltad-model.md` -- Concept: Long-Term Athlete Development 7-stage framework
- `staging/early-specialization.md` -- Concept: AAP guidance; specialization timing research
- `staging/swimming-and-other-sports.md` -- Concept: cross-training; complementary sports; water polo
- `staging/body-type-and-swimming.md` -- Concept: anthropometry research with mof-001 caveat
- `staging/cognitive-benefits.md` -- Concept: IQ research with mof-004 caveat; blocked c137
- `staging/alto-swim-club.md` -- Entity: Alto Swim Club profile
- `staging/pasa.md` -- Entity: Palo Alto Stanford Aquatics profile
- `staging/daca.md` -- Entity: De Anza Cupertino Aquatics profile
- `staging/santa-clara-swim-club.md` -- Entity: Santa Clara Swim Club profile
- `staging/bay-area-swim-camps.md` -- Entity: summer camps comparison (Cal, Stanford, Alto, DACA)
- `wiki/_index.md` -- Wiki index with all 16 articles

**Reason:** Initial wiki compilation from full pipeline run (breadth + depth + gap-fill + extraction + verification). 156 claims processed, 2 L5 blocked, 4 disputes resolved, 6 mechanism overreach flags respected.

## 2026-04-09 -- wiki-compiler-agent (BLOCKED article resolution)

**Changed:**
- `staging/pasa.md` -- Complete rewrite with verified status (previously BLOCKED by wiki-critic). PASA confirmed as active independent club, not merged into Alto. Added: multi-site structure, Rinconada training groups with fees, PASA/Alto clarification, Common Mistakes, who it suits best.
- `staging/santa-clara-swim-club.md` -- Complete rewrite with training group research (previously BLOCKED by wiki-critic). Added: full program pathway (Learn to Swim through Senior), competitive division structure table, facility info, historical context, Common Mistakes, who it suits best.

**Reason:** Targeted research resolved two wiki-critic BLOCKED verdicts. PASA status verified via Pacific Swimming Zone 1 North directory and pasa-rinconada.org. SCSC training groups documented from santaclaraswimclub.org public pages and Wikipedia.

## 2026-04-09 -- wiki-compiler-agent (revision pass)

**Changed:**
- `staging/getting-started.md` -- Added "How to Choose a Good Beginner Swim School or Instructor" checklist (RO1 must-answer gap); added Common Mistakes section
- `staging/developmental-pathway.md` -- Added pre-team/bridge program as explicit Stage 1 in developmental stages (RO5 must-answer gap); deduplicated Late Developer Effect data to summary + wikilink to body-type-and-swimming
- `staging/recreational-to-competitive.md` -- Added full cost trajectory table (rec through elite/travel) in family readiness section (RO5 must-answer gap)
- `staging/parent-playbook.md` -- Replaced abstract Common Mistakes with 6 specific behavior-level mistakes (e.g., "Asking 'What was your time?' as first question"); deduplicated PMC7174680 Late Developer data to summary + wikilink
- `staging/preventing-burnout.md` -- Added training volume by age summary table in overtraining section (RO7 must-answer gap); added immediate response guidance for overtraining signs
- `staging/ltad-model.md` -- Added Common Mistakes section (4 LTAD-specific misapplication errors)
- `staging/early-specialization.md` -- Added Common Mistakes section (4 specialization-specific errors)
- `staging/swimming-and-other-sports.md` -- Added Common Mistakes section (5 multi-sport errors)
- `staging/body-type-and-swimming.md` -- Added Common Mistakes section (4 body-type-interpretation errors); this article is now the canonical location for PMC7174680 Late Developer Effect data
- `staging/cognitive-benefits.md` -- Added Common Mistakes section with "15% math" misinformation risk as lead item
- `staging/alto-swim-club.md` -- Added "Who Alto Suits Best" paragraph (competitive-track swimmers; not ideal for absolute beginners); added Common Mistakes section
- `staging/daca.md` -- Added Training Groups section with typical group structure (Junior Dolphins, Age Group, Senior); expanded beginner-to-elite pathway description; added Common Mistakes section
- `staging/bay-area-swim-camps.md` -- Added Common Mistakes section (camp selection errors including prerequisite checking)
- `staging/costs-and-commitment.md` -- Added hidden costs detail (away meet travel, long-course suits, parking/food at meets)

**Reason:** Revision pass based on wiki-critic-agent feedback. Cross-cutting fixes: (1) added Common Mistakes sections to 10 articles that lacked them, (2) deduplicated PMC7174680 Late Developer Effect data across 3 articles (canonical in body-type-and-swimming, summary + wikilink in developmental-pathway and parent-playbook). Per-article fixes addressed RO must-answer gaps, decision-framing improvements, and missing content identified by critic reports.

## 2026-04-09 -- wiki-compiler-agent

**Added:**
- `wiki/overview.md` -- Topic overview: core principles (LTAD, delayed specialization, parent behavior), key decisions roadmap, reading guide by reader goal, common mistakes section

**Changed:**
- `wiki/_index.md` -- Added Overview section with link to overview.md; article count 16 to 17

**Reason:** Overview article required as topic entry point. Maps all 4 reader personas (P1-P4) and 7 reader outcomes (RO1-RO7) to specific wiki articles.
