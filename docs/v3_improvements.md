for research-plan, do we differtiate different rounds of invokation? e.g. in first round we have 15 questions, and after wiki generated, we ask evolve, then have another round
      of research-plan, do we append these question to the same research-plan doc, but we need to mark which are phase2 quesions right?

    Yes, exactly right — and currently the system only partially handles this. Here's how it works today vs. what it should do:

    Current behavior: Questions are appended to the same research-plan.yaml with phase labels (breadth, depth, gap_fill), but there's no round/cycle marker. Round 2 questions from
    evolve get dumped into gap_fill alongside round 1 gap-fill questions — indistinguishable.

    What you're identifying as the gap: You need to know when a question was added and why, not just what phase it belongs to. A question added by evolve-agent in round 2 is
    fundamentally different from a gap_fill question the research-agent spawned in round 1 — different provenance, different trigger, different priority context.

    The right model would be something like:

    - id: Q045
      text: "What are Harker School's K application deadlines?"
      facet: WHEN
      phase: depth
      round: 2                        # ← which research round
      cycle: evolve-2026-04-06        # ← what triggered it
      spawned_by: evolve-agent
      spawned_reason: "South Bay coverage gap identified in lint report"
      status: pending
      scores:
        user_value: 9
        ...

    This gives you:
    - Round number — so you know this is post-wiki research, not initial exploration
    - Cycle/trigger — what event caused this question to be added
    - Spawned_by — which agent added it (research-agent child question vs. evolve-agent gap vs. human request)

    Why it matters practically:
    - When re-running /kb-research, you can filter to only round 2+ questions to avoid redundant work
    - The wiki compiler can prioritize round 2 questions (they fill known gaps) over residual round 1 questions
    - The changelog can group changes by round, giving you a clear audit trail of "what did the evolve pass actually add"

    Currently none of the agent definitions enforce this — it's a real schema gap worth adding to the research-plan format.

    there are some books like "testing mom", "who get in and why", these books are extremely useful at national level for private school applicaiton, why the research step
      skipped them? and also how to extract key points from these books and not causing copy right issues?

    Great observation — two separate issues explain this.

    ---
    Why the pipeline skipped them

    The research-agent only has WebSearch and WebFetch tools. It can only access:
    - Publicly indexable web pages
    - URLs that return readable HTML/text

    Books are opaque to the pipeline by design — there's no tool to open a Kindle file, query a library database, or read a Google Books preview beyond a few sample pages. The
    agent never even "sees" these books exist as a knowledge source.

    Additionally, the research questions were framed around finding school-specific facts (deadlines, tuition, platform names), not around synthesizing strategic/experiential
    wisdom — which is exactly what those books provide.

    ---
    Why they matter

    - "Testing Mom" (Ann Hulbert / various authors) — ground-level experiential account of the SF/NYC private K application gauntlet. Rich in what actually happens in playdates,
     what schools are really evaluating, parent psychology.
    - "Who Gets In and Why" (Jeff Selingo) — focuses on college admissions but the frameworks (what admissions offices actually optimize for, yield management, institutional
    priorities) transfer directly to competitive K-12 programs.

    These fill the "HOW the school decides" dimension that no official admissions page will ever publish honestly.

    ---
    How to ingest books without copyright issues

    What's legally/ethically fine:
    - Ideas, frameworks, and conclusions are not copyrightable — only specific expression is. You can freely represent what the book argues in your own words.
    - Short direct quotes for commentary/analysis fall under fair use (especially for personal, non-commercial research).
    - Your own notes and annotations from reading are entirely yours.

    Practical workflow:

    1. You read → you summarize → /kb-ingest --file
    Write a raw/manual/testing-mom-notes.md with your own synthesis of key insights. The agent treats it as a first-party source (L1 for your notes, L2 for attributed claims).
    No copyright concern.
    2. Use freely available secondary sources — the research-agent can fetch:
      - Author interviews (YouTube transcripts, podcast episodes)
      - Long-form book reviews (NYT, Atlantic, SF Chronicle)
      - Author's own blog posts, talks, op-eds
      - Blinkist/getAbstract summaries (check TOS — Blinkist blocks scrapers but you can read and paraphrase)
    3. Structured notes format for /kb-ingest:
    ---
    source_type: book_notes
    title: "Testing Mom — Key Insights"
    book: "Testing Mom" by [author]
    notes_by: [you]
    date: 2026-04-06
    reliability_tier: L2  # your interpretation of an authoritative source
    ---

    ## Key Argument
    [In your own words]

    ## What Schools Actually Evaluate at Playdates
    [Your synthesis — not verbatim]

    ## Surprising Findings
    - "[Short direct quote, <50 words]" (p. 47)
    4. Add a /kb-ingest --file step to your workflow — the pipeline treats manual notes the same as web sources, routes them through claim-extractor and fact-checker, and the
    wiki compiler integrates them.

    ---
    Suggested addition to the system

    The research-planner-agent could be updated to always generate a SOURCES facet question: "What books, long-form journalism, or expert accounts cover this topic and where can
     secondary sources (reviews, interviews) be found?" — flagging them for manual ingestion rather than pretending they don't exist.


      Here's an honest retrospective across the full session:

  ---
  What Worked Well

  1. The 8-facet question tree was comprehensive
  WHO/WHAT/WHEN/WHERE/HOW/WHY/COMPARE/META naturally covered the topic with no obvious blind spots. The composite scoring (user_value, dependency_count, searchability, novelty)
  correctly surfaced the right questions first — deadlines and timeline questions ranked highest and were indeed the most valuable.

  2. Reliability tiers + permitted language binding
  The L1-L5 system worked exactly as designed. The fact-checker correctly downgraded aggregator acceptance rates, disputed the Harker tuition stale figure with a live fetch, and
   the wiki compiler consistently used verbatim permitted language. No violations found in lint.

  3. Dispute documentation
  Both real disputes (SF Day Jan 12 vs Jan 13, Live Oak March 17 vs March 19) were caught, documented, and surfaced — not silently resolved. This is exactly the behavior that
  makes the wiki trustworthy.

  4. Budget stops prevented runaway spending
  The 30%/80% breadth/depth stops worked correctly. The research agent self-enforced them without external intervention.

  ---
  What Still Needs Work (Observed This Round)

  1. YAML is the wrong format for incremental writes

  The claim-extractor and fact-checker both resorted to creating "splice scripts" (splice_claims.py) and staging files (fact-sheet-batch2-append.yaml) because you can't cleanly
  append to a YAML file without reading and rewriting the whole thing. I had to manually run the splice script and delete temp files twice.

  Fix: Claims register and fact-sheet should be JSONL (claims-register.jsonl, fact-sheet.jsonl) — one record per line, trivially appendable. YAML stays only for human-facing
  config files like _topic.yaml and research-plan.yaml.

  ---
  2. Lint agent Write tool didn't activate

  I updated the lint-agent frontmatter to include Write, but during the actual run it still couldn't write its own report. The tool environment at invocation time doesn't
  reflect frontmatter changes in the same session. I ended up writing the report manually twice.

  Fix: Either the skill explicitly writes the lint report after the agent returns its findings (cleaner separation), or we need to verify tool availability at the start of each
  agent run.

  ---
  3. The human checkpoint after breadth was bypassed

  I designed the checkpoint into kb-research/SKILL.md but then orchestrated the full pipeline automatically without pausing. The checkpoint only works if the skill actually
  stops and waits — not if the orchestrator (me) just proceeds.

  Fix: The skill must be written as a literal pause: output the breadth summary and stop. The user runs /kb-research {slug} --phase depth to continue. Single-step progression by
   default, full pipeline only with --auto flag.

  ---
  4. Wiki articles ended up in the wrong directory

  The schema specifies wiki/entities/, wiki/guides/, wiki/concepts/ subdirectories. The wiki compiler put everything directly in wiki/ — harker-school.md, challenger-school.md,
  etc. all landed flat. The lint agent didn't catch this because it checks filenames not paths.

  Fix: The scaffolding (pipeline.py init) already creates the subdirectories. The compiler's instructions need to be more explicit: "entity articles go to wiki/entities/, not
  wiki/ directly" — and the lint agent needs a check for files in the wrong directory.

  ---
  5. pipeline-state.yaml was created but never used

  I added it to pipeline.py and it gets initialized correctly. But none of the agents actually read or write it during the pipeline — they still count searches from
  search-log.jsonl individually. It's scaffolding with no behavior attached yet.

  Fix: The research agent needs explicit instructions to read pipeline-state.yaml for budget state and write back after each search. This is the prerequisite for
  parallelization.

  ---
  6. Budget wasn't scaled to question volume

  The original budget was 50 searches for 38 questions (~1.3 searches/question). The evolve agent added 19 more gap-fill questions. The research agent ran out of budget at
  question 6 of 19, leaving 13 unanswered. The budget didn't scale with the expanded scope.

  Fix: Budget should be calculated at pipeline start: max_searches = base_budget + (gap_fill_questions × 2). The evolve agent should either increase the budget when it adds
  questions, or flag that additional budget is needed.

  ---
  7. Cross-linker ran but backlinks stayed empty

  I ran python -m backend.tools.cross_linker topics/.../wiki/ but the lint report found all backlinks still []. Either the tool doesn't write back to files, or it writes
  somewhere other than the frontmatter. I didn't investigate before committing.

  Fix: Verify what cross_linker.py actually does — does it modify files in place or just print output? If it only prints, it needs to be updated to write backlinks into
  frontmatter.

  ---
  8. The evolve → research loop wasn't clean

  After evolve added 19 gap-fill questions, I invoked the research agent manually with a custom prompt rather than through /kb-research --phase gap. This means the gap-fill ran
  outside the skill's budget accounting and checkpoint logic. The pipeline became ad-hoc.

  Fix: Evolve agent output should feed directly back into a standard --phase gap invocation. The skill should support --reset-budget N to add more budget when evolve expands the
   question set.

  ---
  Summary Table

  ┌──────────────────────────────────────┬───────────────────────────────────┬─────────────────────────────────────────────────────┐
  │                Issue                 │              Impact               │                   Fix Complexity                    │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ YAML not appendable → splice scripts │ High — manual cleanup required    │ Medium (migrate to JSONL)                           │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ Lint Write tool didn't activate      │ Medium — manual report writing    │ Low (skill writes report instead)                   │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ Checkpoint bypassed by orchestrator  │ Medium — defeats human review     │ Low (skill must stop, not proceed)                  │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ Wrong wiki subdirectories            │ Medium — structural drift         │ Low (explicit path in compiler prompt + lint check) │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ pipeline-state.yaml unused           │ Low now, High for parallelism     │ Medium (wire agents to read/write it)               │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ Budget not scaled to question count  │ Medium — research left incomplete │ Low (formula in skill)                              │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ Cross-linker may not write files     │ Unknown — untested                │ Low (read the tool code)                            │
  ├──────────────────────────────────────┼───────────────────────────────────┼─────────────────────────────────────────────────────┤
  │ Evolve → research not via skill      │ Low — worked but fragile          │ Low (document the flow)                             │
  └──────────────────────────────────────┴───────────────────────────────────┴─────────────────────────────────────────────────────┘

  The core pipeline is solid. The gaps are mostly in the handoff points between steps — the moments where one agent's output becomes another's input. That's where brittleness
  shows up.



  Here's my honest quality assessment after reading the key wiki articles:

  ---
  Wiki Quality Assessment

  1. Comprehensiveness: 7/10

  Strong coverage:
  - SF school deadlines, fees, and platform details are specific and actionable
  - Month-by-month calendar with exact dates (September open houses → March 19 decisions) is excellent
  - Financial aid mechanics (Clarity, indexed tuition, specific school budgets) are well documented
  - Playdate vs. IQ testing distinction is clearly explained with school-specific formats
  - South Bay rolling admissions vs. ISSFBA fixed-deadline contrast is well covered
  - Age cutoff variation across schools is captured in comparison tables

  Material gaps:
  - 11 schools, but many cells are --: Hamlin tuition, La Scuola age cutoff and decision date, CAIS decision date, Town School details — a parent building their list hits dead
  ends
  - South Bay stubs: Helios, BASIS SV, Gideon Hausner have almost no data beyond "exists"
  - Nothing about what schools actually look for beyond process description — no guidance on the application essays, teacher recommendations, or what "readiness" means to each
  school
  - No feeder preschool guidance — the lint report flags this too; which preschools actually pipeline into which K schools is a critical practical question
  - No real acceptance rates — the wiki lists K class sizes (44 at SF Friends, 22 at Live Oak, 2-4 at SF School) which implies selectivity but doesn't say it explicitly
  - Language immersion is thin — CAIS and La Scuola get mentions but no details on language split, what a day looks like, or how to evaluate immersion fit

  ---
  2. Helpfulness: 8/10

  Genuinely helpful:
  - The Common Mistakes sections in every article are the best part — concrete, non-obvious, directly actionable (e.g., "SF Day has a December deadline, not January; Hamlin's
  first-choice declaration does nothing")
  - Age cutoff table in admissions-strategy.md is the kind of table a parent immediately bookmarks — July 15 vs. August 1 vs. September 1 vs. November 30 is not obvious and has
  real consequences
  - Sibling priority deadlines in October vs. general deadlines in January — most parents would miss this entirely
  - Waitlist mechanics (ISSFBA single-contract rule, when movement starts) are explained clearly
  - South Bay as safety net framing is useful strategy a parent wouldn't naturally know

  Less helpful:
  - No clear "start here" path — overview.md is a framework, not a first-day action plan. A new parent arriving in August 2026 doesn't know: go to open houses, register on
  Ravenna, get on school mailing lists. That sequence is implicit but not written
  - The financial aid numbers need context — "$48,577 tuition with average $28,800 adjustment" is meaningful, but what income level qualifies? The wiki doesn't bridge that gap
  - No geographic clustering — a parent in Noe Valley vs. the Sunset vs. the East Bay has a very different relevant school set, and the wiki doesn't acknowledge that

  ---
  3. Accuracy: 8.5/10

  Strong:
  - Epistemic hedging is applied consistently — "According to SF Day School..." vs. "According to a community source..." is done correctly throughout
  - Conflicting data is documented rather than resolved (SF Day financial aid deadline appearing as Jan 12 vs. Jan 13 on different pages)
  - Live Oak's March 17 exception vs. ISSFBA's March 19 is explicitly flagged
  - L2-L3 attribution keeps the wiki honest about source quality

  Concerns:
  - The entire cycle is now historical. All the specific dates (deadlines, playdates, decisions) are for the 2025-26 cycle that closed March 26, 2026. A parent reading in August
   2026 needs 2026-27 dates, which won't exist until schools publish them. The application-timeline.md has the closed-cycle warning, but a parent won't necessarily read that
  caveat before the deadline table
  - Challenger tuition ~$12,000 (L3, undated) appears as a hard number in the South Bay comparison table — the lint report flags this correctly as misleading
  - W011: The public TK "guaranteed K seat" claim was not confirmed during research but appears in the TK article with likely status

  ---
  Overall Verdict: 7.5/10 — Solid foundation, not yet self-sufficient

  A parent using this wiki can:
  - Understand the ISSFBA framework and why March 19 matters
  - Know which schools have December vs. January deadlines (and avoid missing them)
  - Identify age cutoff conflicts before investing time in an application
  - Understand they need Clarity for financial aid and how indexed tuition works
  - See that South Bay is a different ecosystem with different rules
  - Avoid the 4-5 most common mistakes (sibling deadlines, first-choice letters, single-contract rule)

  They still need to Google:
  - 2026-27 specific dates once schools publish them (this is unavoidable for a cycle-bound resource)
  - Which school actually fits their child's personality and family culture
  - What preschools feed into which schools
  - Specific tuition for ~5 schools still showing --
  - Language immersion specifics (CAIS, La Scuola daily experience)
  - Any acceptance rate data (almost entirely absent)

  The wiki is useful as a process and framework reference — it would save a new parent 10+ hours of reading individual school websites. It's not yet useful as a decision-making
  guide — for that, you'd still need to visit schools, read forums, and ask other parents.

  The single highest-value addition would be a "What to do each month" action checklist article, converting the timeline's passive calendar into imperative steps a parent takes.


  These are the right questions. Let me think through each.

  ---
  1. How can AI proactively think like a parent?

  The answer is: don't simulate parents — find them.

  Reddit, Niche reviews, GreatSchools discussions, local Facebook groups (SF Parents, Marin Parents) contain the actual confused questions real parents ask. A parent's first
  Google search is something like "how do I apply to private kindergarten san francisco reddit" — not "what is ISSFBA."

  The fix is structural: make UGC mining the first step of the research-planner, before generating any questions.

  Current flow:
  _topic.yaml context → AI generates facet-based question tree

  Better flow:
  UGC mining (Reddit/Niche/forums) → extract actual parent pain points
    → use those as seeds → AI fills gaps and structures the question tree

  The research-planner-agent should start by searching:
  - site:reddit.com "sf private school kindergarten"
  - site:reddit.com "bay area private school application"
  - Top Niche/GreatSchools reviews for the schools in scope
  - Cardinal Education, Aquino blog posts (they write for confused parents, not for schools)

  Then extract: what questions appear repeatedly? What confusion is common? What do parents say they wish they'd known? These become the question tree seeds. The AI isn't
  simulating a parent — it's reading what actual parents wrote.

  This would have caught: feeder preschools, acceptance rates, "what do schools actually look for," culture/fit questions — all of which show up constantly in parent forums.

  ---
  2. L4 as intelligence, not citations

  Already aligned. The implementation fix: L4 sources feed synthesis patterns, not attributable claims.

  The wiki can say "parents describe the Hamlin interview as focused on family values rather than the child's performance" without citing a Reddit thread. Or wiki-compiler
  annotates with (community pattern, multiple reports) — hedged but present. The current pipeline discards this entirely.

  ---
  3. Embedding the goal into the research process

  The core problem: agents currently optimize for information completeness ("did we cover all facets?") rather than reader outcomes ("can the parent make this decision now?").

  The fix is to define reader outcomes explicitly in _topic.yaml and make every agent downstream read them as success criteria.

  Add a reader_outcomes field to _topic.yaml:

  reader_outcomes:
    - id: RO1
      job: "Determine if my child is age-eligible before investing time in applications"
      must_answer: ["age cutoff by school", "how cutoffs vary", "what to do if borderline"]
    - id: RO2
      job: "Build a school list of 6-10 schools to actually apply to"
      must_answer: ["what differentiates schools", "geography", "philosophy fit", "K class size/selectivity"]
    - id: RO3
      job: "Never miss a deadline"
      must_answer: ["full deadline calendar", "sibling priority exceptions", "financial aid separate deadlines"]
    - id: RO4
      job: "Understand what the process will cost and whether aid is realistic"
      must_answer: ["tuition range by school", "aid participation rates", "income thresholds if any", "IQ test cost"]
    - id: RO5
      job: "Prepare my child and myself for the assessment"
      must_answer: ["what playdates evaluate", "what parents are asked in interviews", "how to prepare without coaching"]
    - id: RO6
      job: "Navigate decisions and waitlists in March"
      must_answer: ["single-contract rule", "waitlist movement timing", "how to hold multiple offers if South Bay"]

  Then each agent changes its optimization target:

  ┌──────────────────┬────────────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────┐
  │      Agent       │            Current goal            │                                        New goal                                         │
  ├──────────────────┼────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤
  │ research-planner │ Generate questions across 8 facets │ Generate questions that answer must_answer items for each RO                            │
  ├──────────────────┼────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤
  │ research-agent   │ Collect sources by question        │ Tag each source to which RO it serves; flag ROs with no coverage                        │
  ├──────────────────┼────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤
  │ wiki-compiler    │ Write articles by topic            │ Each article must fully enable ≥1 RO; incomplete = article stub, not full article       │
  ├──────────────────┼────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────┤
  │ lint-agent       │ Check structural issues            │ Add RO coverage check: which ROs have no article? Which must_answer items are still --? │
  └──────────────────┴────────────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────┘

  The lint-agent RO coverage check is the key enforcement mechanism. Right now lint flags "La Scuola age cutoff is --." With reader outcomes, it flags "RO2 partially blocked: 3
   of 11 SF schools have missing selectivity data — parent cannot confidently build school list." That's a more actionable severity signal.

  ---
  What this changes concretely

  Three changes to implement:

  1. _topic.yaml schema: add reader_outcomes field with id, job, must_answer[]
  2. research-planner-agent: step 0 = UGC mining (Reddit/forums/consultant blogs); step 1 = map parent pain points to must_answer items; step 2 = generate question tree from
  that
  3. lint-agent: add RO coverage check — report which outcomes are fully enabled, partially enabled, or blocked by missing data

  This reframes the wiki from "comprehensive reference" to "decision support tool." A parent reading it should finish each article knowing what to do, not just knowing more
  facts.


  Part 1: The real content gap map

  The gaps aren't random — they fall into three categories that the current pipeline structurally cannot produce:

  Category A: Decisions before the application decision
  These are prerequisite questions the wiki never addresses:
  - Public vs. private — what does SFUSD K actually look like? The lottery, school quality variance, the genuine tradeoffs
  - Is private school worth it — $48k × 9 years = $430k. What evidence exists for outcomes (academic, social, college)? This is the most important question for most families
  and we have zero coverage
  - Financial capacity planning — not just "aid exists" but "at $X household income, what aid is realistic?" CDS's $3,500 floor vs. $49k ceiling is meaningless without income
  context

  Category B: Experiential content that only exists in UGC
  - Parent interview questions — what do schools actually ask? ("Why this school?" "How do you handle conflict at home?" "Describe your parenting philosophy?") This is common
  knowledge in parent forums, invisible on official sites
  - Playdate preparation — what to tell your child, what not to coach, what a 4-year-old should be able to do, what "readiness" actually means day-of
  - IQ test logistics — how do you find a psychologist on Harker/Nueva's approved list, how far in advance to book, what the Wechsler WPPSI actually tests, whether you can
  prepare
  - Location/commute reality — where each school physically is, drop-off logistics, parking, whether 5-year-olds can take Muni. This is enormous for SF families and completely
  absent

  Category C: Forward-looking / lifecycle questions
  - Private → public transition — how common is it? What grade? Is there academic adjustment? This matters because families budget for 2 years but the school is K-8
  - Sibling implications — what happens to younger siblings' admissions chances once you're enrolled?
  - After-school care — most private schools end at 3pm. What do working parents do?
  - Alumni pipeline — where do kids go for middle school/high school? Does private K actually open doors?

  The root cause for A: the research plan starts at "how to apply" but should start one step earlier: "should we apply at all."

  The root cause for B: L4 community sources are discarded, but Category B content almost exclusively lives in L4.

  The root cause for C: no lifecycle framing in the research plan — the wiki treats K admission as the endpoint, not as one step in a 10-year relationship with private
  education.

  ---
  Part 2: How to evaluate helpfulness — a concrete framework

  Fact-checking is about accuracy (is X true?). Helpfulness evaluation is orthogonal — a wiki can be 100% accurate and completely unhelpful because it covers the wrong things.

  The right evaluation framework:

  Automated: Simulated parent Q&A test suite

  Build a set of 30 test questions drawn from actual Reddit posts, not AI-generated ones. Run an LLM using only the wiki as context. Score each answer:

  0 = not answerable from wiki (requires Google)
  1 = partially answerable (wiki helps but leaves open questions)
  2 = fully answerable from wiki alone

  Track the score over pipeline runs. A wiki targeting "no Google needed" should hit ≥25/30 at score 2. Right now I'd estimate this wiki scores ~14/30.

  Example test questions from real parent experience:
  - "My daughter was born September 10, 2020. Which SF schools can she apply to for fall 2026 K?"
  - "We earn $180k HHI. Is financial aid realistic at SF Day School?"
  - "What should I tell my 4-year-old before his Live Oak playdate?"
  - "Should I apply to both SFUSD and private, or just private?"
  - "Live Oak waitlisted us. What should we do now and when does movement happen?"
  - "Is Harker right for a non-gifted kid who's just bright?"

  Reader outcome coverage audit (per RO)

  For each reader outcome defined in _topic.yaml, rate:
  - Fully enabled: parent can make this decision from wiki alone
  - Partially enabled: wiki helps but leaves ≥1 must_answer item uncovered
  - Blocked: wiki doesn't address this RO meaningfully

  Run this as a lint check. Right now: RO1 (eligibility) = fully enabled. RO2 (school list) = partially enabled. RO3 (deadlines) = fully enabled. RO4 (financial) = partially
  enabled. RO5 (assessment prep) = blocked. RO6 (March navigation) = partially enabled.

  Red team task completion

  Give the wiki to an LLM with a specific parent persona and a concrete task. Persona: "First-time parent, SF Noe Valley, child born Aug 15, 2021, HHI $220k, child described as
   social/creative, no language preference, working parent who can't volunteer heavily." Task: "Using only this wiki, give me a school list of 8 schools ranked by fit."

  Can the LLM do this? If it has to say "I need more information about X" — that's a gap. If it outputs a ranked list with reasoning grounded entirely in wiki content — that RO
   is enabled.

  The meta-principle

  The current pipeline evaluates what the wiki says. Helpfulness evaluation evaluates what the reader can do after reading it. These need to be different agents with different
  prompts. A helpfulness-eval-agent that simulates a confused parent trying to complete tasks would catch gaps that the lint-agent structurally cannot see.

  The test suite itself should be built once from Reddit/forum sources and reused across pipeline runs — so you get a stable benchmark as the wiki evolves.

  if you were to design a eval rubrics, how would you evaluate the different dimensions of your wiki markdown files?

⏺ Here's how I'd design it — organized as a rubric with dimensions, scoring criteria, and explicit annotation of what's automatable vs. requires LLM judgment.

  ---
  Wiki Evaluation Rubric

  Scoring Scale

  - 3 — Fully meets the bar
  - 2 — Partially meets, meaningful gaps
  - 1 — Addressed but insufficient
  - 0 — Not addressed

  Dimension Weights

  ┌───────────────────────────────────┬────────┬─────────────────────────────────────────────────┐
  │             Dimension             │ Weight │                    Rationale                    │
  ├───────────────────────────────────┼────────┼─────────────────────────────────────────────────┤
  │ D1 Reader Outcome Enablement      │ 30%    │ The core purpose — can a parent make decisions? │
  ├───────────────────────────────────┼────────┼─────────────────────────────────────────────────┤
  │ D2 Coverage Completeness          │ 20%    │ Are the right topics present?                   │
  ├───────────────────────────────────┼────────┼─────────────────────────────────────────────────┤
  │ D3 Accuracy & Epistemic Integrity │ 20%    │ Wrong info is worse than no info                │
  ├───────────────────────────────────┼────────┼─────────────────────────────────────────────────┤
  │ D4 Actionability                  │ 15%    │ Information vs. decision-support framing        │
  ├───────────────────────────────────┼────────┼─────────────────────────────────────────────────┤
  │ D5 Perspective Balance            │ 10%    │ Official only vs. lived experience included     │
  ├───────────────────────────────────┼────────┼─────────────────────────────────────────────────┤
  │ D6 Navigability & Structure       │ 5%     │ Hygiene                                         │
  └───────────────────────────────────┴────────┴─────────────────────────────────────────────────┘

  ---
  D1: Reader Outcome Enablement (30%)

  LLM judgment required. For each defined reader_outcome in _topic.yaml, score independently.

  ┌───────┬────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                            Criteria                                            │
  ├───────┼────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ Parent can make this decision from the wiki alone. No open questions remain. No Google needed. │
  ├───────┼────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ Wiki substantially helps but ≥1 must_answer item is missing or answered only partially         │
  ├───────┼────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ Wiki mentions the topic but doesn't enable the decision                                        │
  ├───────┼────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 0     │ RO not addressed at all                                                                        │
  └───────┴────────────────────────────────────────────────────────────────────────────────────────────────┘

  Evaluation method: Simulated parent Q&A test suite. Take 5 specific questions per RO (sourced from Reddit/forums, not AI-generated). Score each 0/1/2 (not answerable /
  partial / fully answerable from wiki). Aggregate per RO.

  Current estimate for this wiki:

  ┌────────────────────────────┬───────┬──────────────────────────────────────────────────────────────┐
  │             RO             │ Score │                             Gap                              │
  ├────────────────────────────┼───────┼──────────────────────────────────────────────────────────────┤
  │ RO1 Age eligibility        │ 3     │ Fully enabled                                                │
  ├────────────────────────────┼───────┼──────────────────────────────────────────────────────────────┤
  │ RO2 Build school list      │ 1     │ Missing: selectivity/acceptance rates, culture fit, location │
  ├────────────────────────────┼───────┼──────────────────────────────────────────────────────────────┤
  │ RO3 Never miss deadline    │ 3     │ Fully enabled for 2025-26; 0 for 2026-27                     │
  ├────────────────────────────┼───────┼──────────────────────────────────────────────────────────────┤
  │ RO4 Financial planning     │ 2     │ Missing: income-to-aid mapping, total cost of attendance     │
  ├────────────────────────────┼───────┼──────────────────────────────────────────────────────────────┤
  │ RO5 Assessment preparation │ 0     │ Parent interview questions, playdate prep — absent           │
  ├────────────────────────────┼───────┼──────────────────────────────────────────────────────────────┤
  │ RO6 March navigation       │ 2     │ Single-contract rule covered; waitlist realities thin        │
  └────────────────────────────┴───────┴──────────────────────────────────────────────────────────────┘

  Weighted D1 score: ~1.8/3

  ---
  D2: Coverage Completeness (20%)

  Mix of automatable and LLM judgment.

  2a. Topic coverage (LLM judgment)

  ┌───────┬─────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                              Criteria                                               │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ All major decision categories for this topic have ≥1 article; no standalone decision left uncovered │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ 1-2 major decision categories missing (e.g., "public vs. private" absent entirely)                  │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ Core categories present but with significant gaps within each                                       │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 0     │ Major portions of the topic not addressed                                                           │
  └───────┴─────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Missing categories for this wiki: public vs. private decision, is private worth it, commute/location, interview prep, IQ test logistics, after-school care, private→public
  transition. Score: 1

  2b. Entity coverage (automatable)

  score = (schools with complete data / total schools in scope)
  complete = no more than 2 "--" cells in comparison table

  Current: 11 SF schools, ~5 have ≥2 missing cells. Peninsula: 6 schools, 3 are stubs. Score: 1

  2c. Stub ratio (automatable)

  score = 3 if stubs < 10% of articles
  score = 2 if 10-25%
  score = 1 if 25-40%
  score = 0 if >40%

  Current: 8 stubs listed in _index.md out of 16 articles = 33%. Score: 1

  Weighted D2 score: ~1.0/3

  ---
  D3: Accuracy & Epistemic Integrity (20%)

  Mix of automatable and LLM judgment.

  3a. Attribution compliance (automatable)

  score = % of factual claims with "According to X" or epistemic hedge

  Sample 20 random claim sentences. Count those with attribution. Target ≥90%.

  3b. Confidence level discipline (automatable)

  ┌───────┬───────────────────────────────────────────────────────────────────────┐
  │ Score │                               Criteria                                │
  ├───────┼───────────────────────────────────────────────────────────────────────┤
  │ 3     │ 0 L5 claims in wiki; all L4 sources flagged with epistemic note block │
  ├───────┼───────────────────────────────────────────────────────────────────────┤
  │ 2     │ 0 L5 claims; some L4 sources cited without epistemic note             │
  ├───────┼───────────────────────────────────────────────────────────────────────┤
  │ 1     │ Community sources treated as fact in ≥1 article                       │
  ├───────┼───────────────────────────────────────────────────────────────────────┤
  │ 0     │ L5 claims present                                                     │
  └───────┴───────────────────────────────────────────────────────────────────────┘

  Current: L5 = 0 (good). L4 sources (consultant content) are hedged with epistemic note blocks. Score: 3

  3c. Conflict documentation (LLM judgment)

  ┌───────┬────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                  Criteria                                  │
  ├───────┼────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ All source conflicts identified and documented                             │
  ├───────┼────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ Most conflicts documented; minor ones may be missed                        │
  ├───────┼────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ Some conflicts present but resolved by picking one source without flagging │
  ├───────┼────────────────────────────────────────────────────────────────────────────┤
  │ 0     │ Conflicts not tracked                                                      │
  └───────┴────────────────────────────────────────────────────────────────────────────┘

  Current: SF Day Jan 12 vs. Jan 13 conflict documented. Live Oak March 17 exception documented. Score: 2

  3d. Permitted language compliance (LLM judgment)

  Does wiki text match fact-sheet permitted language for verified claims?
  Current: cross-linker didn't populate backlinks; spot check needed. Estimate: 2

  Weighted D3 score: ~2.3/3

  ---
  D4: Actionability (15%)

  LLM judgment. Most important qualitative dimension.

  4a. Decision framing (per article)

  ┌───────┬───────────────────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                         Criteria                                          │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ Article tells reader what to do, not just what to know. Imperative voice in key sections. │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ Information present but framed passively — reader must translate to action themselves     │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ Pure reference material with no action guidance                                           │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 0     │ Content would confuse rather than help                                                    │
  └───────┴───────────────────────────────────────────────────────────────────────────────────────────┘

  4b. Common mistakes quality

  ┌───────┬───────────────────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                         Criteria                                          │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ Mistakes are non-obvious and specific (e.g., "SF Day has December deadline, not January") │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ Mistakes are real but generic ("start early," "apply to multiple schools")                │
  ├───────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ No common mistakes section                                                                │
  └───────┴───────────────────────────────────────────────────────────────────────────────────────────┘

  Current: Common mistakes sections exist in 6 articles and are specific. Score: 2.5

  4c. "Start here" clarity

  ┌───────┬─────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                            Criteria                                             │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ A confused parent landing on any article knows immediately what to read first and in what order │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ Overview article exists but navigation path isn't obvious from individual articles              │
  ├───────┼─────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ No clear entry point                                                                            │
  └───────┴─────────────────────────────────────────────────────────────────────────────────────────────────┘

  Current: overview.md exists but no "read in this order" explicit path. Score: 2

  Weighted D4 score: ~2.1/3

  ---
  D5: Perspective Balance (10%)

  LLM judgment.

  ┌───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │ Score │                                                           Criteria                                                           │
  ├───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3     │ Official sources + aggregator data + community patterns + expert synthesis all represented. Reader gets multiple viewpoints. │
  ├───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2     │ Official + aggregator present; community patterns absent or discarded                                                        │
  ├───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1     │ Primarily official sources only                                                                                              │
  ├───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 0     │ Single source type                                                                                                           │
  └───────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Sub-dimensions:

  ┌──────────────────────────────────────────────┬──────────────────────────────────────────────────┐
  │               Perspective type               │                     Present?                     │
  ├──────────────────────────────────────────────┼──────────────────────────────────────────────────┤
  │ Official school sources (L1-L2)              │ ✓ Heavy                                          │
  ├──────────────────────────────────────────────┼──────────────────────────────────────────────────┤
  │ Aggregator/review (L3)                       │ ✓ Light                                          │
  ├──────────────────────────────────────────────┼──────────────────────────────────────────────────┤
  │ Community/parent experience (L4)             │ Partially — consultant content but no forum data │
  ├──────────────────────────────────────────────┼──────────────────────────────────────────────────┤
  │ Expert synthesis (consultants, journalists)  │ ✓ SF Standard, Cardinal Education                │
  ├──────────────────────────────────────────────┼──────────────────────────────────────────────────┤
  │ Counterarguments ("here's why NOT to apply") │ ✗ Absent                                         │
  └──────────────────────────────────────────────┴──────────────────────────────────────────────────┘

  Weighted D5 score: ~1.5/3

  ---
  D6: Navigability & Structure (5%)

  Mostly automatable.

  ┌──────────────────────────────┬────────────────────────┬───────┐
  │            Check             │     Current status     │ Score │
  ├──────────────────────────────┼────────────────────────┼───────┤
  │ Broken wikilinks             │ 0 broken               │ 3     │
  ├──────────────────────────────┼────────────────────────┼───────┤
  │ Orphaned articles            │ 0 orphans              │ 3     │
  ├──────────────────────────────┼────────────────────────┼───────┤
  │ Backlinks populated          │ All empty              │ 0     │
  ├──────────────────────────────┼────────────────────────┼───────┤
  │ Index article count accurate │ Was 15, now 16         │ 2     │
  ├──────────────────────────────┼────────────────────────┼───────┤
  │ See Also sections present    │ All articles have them │ 3     │
  └──────────────────────────────┴────────────────────────┴───────┘

  Weighted D6 score: ~2.2/3

  ---
  Composite Score

  ┌───────────────────────────────────┬───────────┬────────┬──────────┐
  │             Dimension             │ Raw Score │ Weight │ Weighted │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ D1 Reader Outcome Enablement      │ 1.8/3     │ 30%    │ 18.0     │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ D2 Coverage Completeness          │ 1.0/3     │ 20%    │ 6.7      │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ D3 Accuracy & Epistemic Integrity │ 2.3/3     │ 20%    │ 15.3     │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ D4 Actionability                  │ 2.1/3     │ 15%    │ 10.5     │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ D5 Perspective Balance            │ 1.5/3     │ 10%    │ 5.0      │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ D6 Navigability                   │ 2.2/3     │ 5%     │ 3.7      │
  ├───────────────────────────────────┼───────────┼────────┼──────────┤
  │ Total                             │           │ 100%   │ 59/100   │
  └───────────────────────────────────┴───────────┴────────┴──────────┘

  ---
  What this rubric reveals

  59/100 is a useful baseline. The wiki is accurate and navigable but materially underserves the two highest-weight dimensions: reader outcome enablement (can't actually make
  the "school list" or "assessment prep" decisions from this wiki) and coverage completeness (wrong topics covered, right topics thin).

  The rubric also clarifies where effort yields the most return:

  - D1 and D2 together = 50% of score but current combined = ~32/50
  - Fixing D1 and D2 to ~2.5/3 each would push the wiki from 59 → 78
  - Improving D3 from 2.3 → 3.0 (already good) only adds ~5 points

  Implementation: this rubric should run as a helpfulness-eval-agent after each lint-agent pass — same pipeline position, different evaluation lens. The test question suite (30
   questions sourced from Reddit) is the single most valuable artifact to build and reuse.
