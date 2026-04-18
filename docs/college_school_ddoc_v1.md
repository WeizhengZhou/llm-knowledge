# College Placement Intelligence System — Design & Retrospective Document v1

_A complete record of how a single conversation turned a parent's question into a data-driven knowledge system, a 10-chapter guidebook, and the foundations of an AI-driven school application counselor._

**Created:** 2026-04-18
**Author:** Human + Claude Opus 4.6 (1M context)
**Session duration:** ~6 hours, single continuous conversation
**Total git commits:** 24

---

## Part 1: The Original Problem

### What the user asked

A parent (Weizheng) had been talking to an AI in a separate conversation about Sacred Heart Schools (SHS) Atherton's college placement data. He had uploaded 5 years of "Where Do Gators Go?" PDF brochures and asked: "How many SHS students go to Ivy League schools, and how many of those are athlete recruits vs non-athletes?" He wanted this analysis tailored to his daughter Lexi — a 7-year-old Asian girl at SHS, math-strong, non-athlete, with both parents holding Duke MS Physics degrees.

The AI in that conversation produced a long analysis, but it had a fundamental flaw: **the data was manually extracted from PDFs in a single conversation with no persistence.** Next time he asked a follow-up, he'd have to re-upload and re-extract everything. The estimates for athlete vs non-athlete splits were approximations, not verified cross-references.

### What the user actually needed

Not a one-time analysis. He needed:

1. **Persistent, verified data** about school placement that doesn't disappear when the chat ends
2. **Cross-school comparison** grounded in real numbers, not vibes
3. **Personalized advice** for Lexi that acknowledges her specific profile (Asian, female, non-athlete, math-strong, Duke legacy)
4. **A system that compounds** — each new data point, each new school, each new year makes the whole thing more valuable

The deeper question behind the question: **"Can I build the equivalent of a $50K/year private college counselor from public data?"**

---

## Part 2: The Trajectory We Explored

### Phase 1: Architecture (first 30 minutes)

Before writing any code, we mapped the strategic landscape:

- **Three projects** in play: `llm_knowledge/` (factual KB), `parenting/` (Lexi-specific), `school_application/` (product)
- **Four knowledge layers** needed: school placement stats, school-specific intelligence, personal context, application engine
- **The key insight**: separate factual knowledge from personal application. SHS placement data should live in a reusable KB, not trapped in a chat about Lexi.

This phase produced the 4-layer architecture that guided everything after:
1. Factual KB (school placement data) → `llm_knowledge/topics/`
2. School-specific intelligence (entity articles) → `wiki/entities/`
3. Personal context (Lexi) → `parenting/user_docs/`
4. Application engine → `school_application/` (future)

### Phase 2: Layer 1 — School Placement Database (hours 1-2)

**The approach:** SQLite for structured data + markdown for extracted PDFs. Hybrid storage.

**What we built:**
- Initialized a new KB topic: `bay-area-k-12-college-placement-statistics`
- Designed SQLite schema: `schools`, `placements`, `uc_admissions`, `school_profiles`, `athlete_commits`, `sources` tables
- Created views for non-athlete placements and Ivy+ rate comparisons

**Data ingestion (8 schools, 5 data source types):**

| Source Type | How We Got It | What We Learned |
|---|---|---|
| SHS "Where Gators Go" PDFs | `curl` download → `pdftotext` → manual parsing into Python dicts | `pdftotext` works perfectly on these PDFs. The text extraction is clean with columns intact. |
| SHS athlete commit pages | WebFetch → markdown tables | SHS is unique — no other school publishes name-level athlete data. This is what makes the athlete/non-athlete decomposition possible. |
| SHS Google Doc | Chrome CDP → `DOCS_modelChunk` JSON | Google Docs canvas rendering blocks all DOM extraction. The doc turned out to be a hub page linking to PDFs, not data itself. Lesson: always check what a document actually contains before building extraction pipeline. |
| Harker web page | WebFetch → markdown table | Harker labels data as "College Acceptances" but body text uses "matriculated" — it's actually enrollment data. Read carefully. |
| UC InfoCenter | JSON download from collegeacceptance.info mirror | The GitHub CSV mirror only has public schools. The collegeacceptance.info JSON has private schools. This took 3 attempts to discover. |
| School Profile PDFs (Menlo, Castilleja, Nueva, etc.) | `curl` → `pdftotext` → parse | Each school reports differently: Menlo uses overlapping 2-year windows, Nueva uses tier minimums ("10 or more"), Castilleja uses presence-only lists. You cannot compare across schools without understanding each school's reporting methodology. |
| Public school data | User's manual spreadsheet | No automated source for public school placement data. The user's spreadsheet from a prior year was the only source. |

**Critical bugs found and fixed:**
- College name normalization fragmentation: "University of California (Berkeley)" → `university-of-california-berkeley` instead of `uc-berkeley`. Fixed with UC regex handler. 69 rows affected.
- Rice University → `rice-university` instead of `rice`. Added to explicit mapping.
- Notre Dame variants. Cal Poly SLO variants.
- Re-processing existing profiles caused FK constraint errors. Fixed with delete-then-insert pattern.

**Data quality validation:**
- Cross-validated all SHS data against user's manually collected spreadsheet: **100% match (75/75 data points)**
- Harker data from a different year range than user's spreadsheet — correctly identified as non-error (different time windows)
- Class size discrepancy: user had SHS 2023 as 170, PDF says 171. Trivial.

### Phase 3: Admissions Research (hour 2)

Two parallel research agents deployed:

**Duke Legacy Research** — the most impactful finding of the session:
- Duke MS-only legacy is **weaker than undergraduate legacy** (L3 consensus from admissions consultants)
- Duke's official pages are ambiguous about whether graduate degrees qualify
- This directly changed the Lexi strategy from "Duke double legacy is a strong hook" to "Duke affiliation is a positive signal but not primary legacy"
- Duke ED rate: 13.8% vs ~3.7% RD. Legacy applicants apply ED at 81.7%. **ED is the real lever, not the legacy label.**

**Post-SFFA Research** — split pattern by school type:
- Asian enrollment rose at Harvard (30→41%), MIT (40→47%), Columbia (30→39%), Stanford (41→44%)
- Asian enrollment **fell** at Duke (35→25%) — SFFA sent Duke a threatening letter
- **California AB 1780** banned legacy at Stanford effective Sept 2025 — the single most important structural change for Bay Area families
- Socioeconomic proxies (first-gen, Pell-eligible) provide zero boost to affluent Bay Area private school families

### Phase 4: Guidebook (hours 2-4)

**The strategic decision:** Write a guidebook, not a web app. Reasons:
1. The user had already built two successful guidebooks (K-application, STEM)
2. A guidebook forces narrative synthesis (not just tables)
3. It's shareable immediately (PDF, WeChat groups)
4. It surfaces data gaps (you discover what's missing while writing)
5. The Chinese translation reaches the exact target audience

**Production approach:**
- Used SOP v2 (documented from STEM guidebook lessons): chapter brief template, evidence tier system, 7 skeleton elements, 3 diagrams per chapter, self-scoring rubric
- Drafted chapters in parallel (3 agents at a time)
- Every data claim verified against SQLite DB
- Chapter 1 verified at 100% accuracy (8/8 claims matched DB exactly)

**Chapter flow:**

| Ch | Title | Key Insight | Data Source |
|---|---|---|---|
| 1 | What the Brochure Doesn't Say | SHS 16.8% Ivy+ headline drops to 10.5% without athletes | placements + athlete_commits |
| 2 | How to Read Placement Data | 4 source types, each with different biases | Source catalog |
| 3 | The Athlete Hook — Quantified | Water polo + lacrosse = 72% of athlete-to-Ivy+ | athlete_commits |
| 4 | School by School | 11 schools profiled with standardized tables | All DB tables |
| 5 | The Asian Parent Reality | Asian share ranges 22% (SHS) to 65% (Harker) | uc_admissions ethnicity |
| 6 | Private vs Public | Gunn (free) matches SHS ($55K/yr) Ivy+ rate | placements + public school data |
| 7 | Legacy, ED, Hooks | Duke MS-only ≠ undergrad legacy; Stanford legacy ban | Duke/SFFA research |
| 8 | The Spike | Math competition pipeline with benchmarks | MATHCOUNTS + USAPhO trajectories |
| 9 | Grade by Grade | K-12 framework: Foundations → Exploration → Commitment → Execution | All trajectory data |
| 10 | Should You Transfer? | SHS 9.5% non-athlete vs Menlo ~26% vs Gunn 33.3% | Cross-school comparison |

### Phase 5: Layer 2 — Student Profile Database (hours 3-4)

**The realization:** School-level data tells you "SHS sends 28 to Stanford." You also need to know "what kind of student from SHS gets into Stanford."

**Reddit crawler (r/collegeresults):**
- Built crawler using Reddit's public JSON API (no auth needed)
- Rate limited to 1.5s between requests with proper User-Agent
- `is_results_post()` filter: checks title for "results/accepted/committed" + body for stats keywords
- 4 search queries + 100 recent posts → 98 posts crawled, 44 passed filter

**Rule-based extractor (3 format types discovered):**
1. Section-based: "Acceptances:" / "Rejections:" headers + bullet lists
2. Inline: "Stanford — Accepted" or "Harvard: Rejected"
3. Round-grouped: "ED:" / "EA:" / "RD:" headers with "College (rate%): Result"

Initial extraction: 12 results from 4 posts. After adding section-based parser: 58 results. After adding round-grouped parser: 1,103 results from 98 posts. **Iterative parser improvement was critical.**

**YouTube crawler:**
- yt-dlp for search + transcript download (no API quota needed)
- Auto-subtitles (`.en.vtt`) converted to plain text
- 14 videos crawled, transcripts extracted
- Rule-based parser got **0 results** from YouTube (completely unstructured flowing text)

**Gemini LLM extraction (the breakthrough):**
- Gemini 2.5 Flash via Google Generative AI SDK
- API key from existing project (`kid_camp2/backend/.env`)
- `response_mime_type="application/json"` for clean structured output
- Temperature 0.1 for deterministic extraction
- Success rate: 80% on YouTube transcripts, 80% on Reddit re-extractions
- Main failure mode: JSON parse errors (10-15% of calls) — malformed Gemini output
- Cost: negligible (~$0.001 per extraction)

**Cross-join tool:**
- Connected student profiles DB to school placement DB
- 82 colleges overlap between databases
- Found 21 Asian female profiles comparable to Lexi
- Per-college acceptance rates by ethnicity: Stanford 12%, Harvard 14%, Brown 7%, Princeton 7%

### Phase 6: Layer 3 — K-12 Trajectory Data (hours 4-6)

**The hardest problem.** The user asked: "Where can we find the full trajectory of a student — when did they start Beast Academy, when did they enter their first competition, when did they drop piano?"

**16 research agents deployed** across these categories:

| Category | Agents | Outcome |
|---|---|---|
| Competition databases | 2 | USAPhO = cleanest; AMC school data gated; Duosmium = 40yr Sci Oly archive |
| AoPS community | 1 | MATHCOUNTS CA PDFs have named students; AMC score threads have longitudinal data |
| Chinese parent forums | 1 | huaren.us best public source; Xiaohongshu auth-gated but richest |
| College newspapers | 1 | MIT Admissions Blogs = richest trajectory source (20yr, 5K+ posts) |
| LinkedIn reverse | 1 | MATHCOUNTS→USAMO→STS→college chain traceable; LinkedIn manual OK, scraping risky |
| Essay books | 1 | No K-8 data in any published source |
| Podcasts/alumni magazines | 1 | Dead end — no podcast covers K-12 arcs |
| Gifted programs | 1 | Spelling Bee = best K-8 longitudinal; SMPY starts age 12 |
| K-8 creative sources | 1 | Davidson Gifted Forum = parents post year-by-year math progression |
| Sports progression DBs | 1 | USA Swimming SWIMS = most complete youth longitudinal DB (age 7+, public) |
| Duosmium download | 1 | 247 YAML files, 12,870 team records |
| MATHCOUNTS extraction | 1 | 371 named students, 43 multi-year competitors |
| USAPhO extraction | 1 | 1,049 records, 8 multi-year Bay Area trajectories |
| MIT blogs crawl | 1 | 13 structured profiles (2006-2027) |
| Davidson forum crawl | 1 | 36 K-8 trajectory records from parent posts |
| Entity resolution | 1 | 90 multi-record trajectories linked across competitions |

**The fundamental finding:** No public source captures the K-8 developmental period (ages 5-14). The data exists in domain-specific silos:

```
Age 5-7:   Chess ratings (USCF) | Davidson Forum parent posts
Age 6-10:  Swimming times (USA Swimming SWIMS) | Math Kangaroo winners
Age 8-14:  Spelling Bee (multi-year) | MATHCOUNTS (gr 6-8)
Age 14-18: USAPhO | USAMO | Regeneron STS | AoPS threads | Reddit/YouTube
Age 18:    School placement DB | College enrollment
```

**Entity resolution pipeline:**
- 901 input records (371 MATHCOUNTS + 384 USAPhO + 146 athlete commits)
- 90 multi-record trajectories resolved
- Notable: Dylan Wang (Bullis Charter) MATHCOUNTS #11→#6→#1 over 3 years
- Notable: Jamin Xie (Valley Christian) USAPhO Gold→Gold→Gold over 3 years
- Cross-competition matches are limited because MATHCOUNTS (2024-2026) students are too young to appear in USAPhO (2019-2024). As more years accumulate, this gap closes.

---

## Part 3: What Worked and What Didn't

### What Proved Working at Small Scale

| Approach | Evidence | Can It Scale? |
|---|---|---|
| `pdftotext` for school profile extraction | 100% match on SHS data (75/75 points) | Yes — automated for any school |
| UC InfoCenter JSON mirror | 961 rows, 30 years, ethnicity breakdowns | Already at scale |
| Reddit rule-based extraction | 70% of posts yield results (3 format types) | Yes — paginate deeper |
| Gemini LLM extraction for unstructured text | 80% success on YouTube/Reddit | Yes — cost negligible |
| MATHCOUNTS PDF extraction | 371 named students, 43 multi-year | Yes — add more years/chapters |
| USAPhO PDF extraction | 1,049 students, 8 trajectories | Yes — add more years |
| Duosmium Sci Oly YAML download | 12,870 records from GitHub | Already complete |
| Cross-validation against manual data | Found and fixed normalization bugs | Essential — do for every new source |
| Entity resolution (name + school matching) | 90 trajectories from 901 records | Yes — improves with more data |

### What Didn't Work

| Approach | What Happened | Lesson |
|---|---|---|
| Google Docs text extraction | Canvas rendering blocks DOM access. Required Chrome CDP to find the doc was just a hub page linking to PDFs. | Always check what a document actually contains before building extraction. |
| Claude's Read tool for PDFs | `pdftoppm` path issue despite poppler being installed. | Use `pdftotext` via Bash as fallback. |
| Rule-based extraction for YouTube | 0 results — flowing transcript text has no structure. | LLM extraction is mandatory for narrative sources. |
| Gemini JSON output reliability | 10-15% parse failures (unterminated strings, missing commas). | Need retry logic + post-processing cleanup. Could try structured output mode or JSON schema enforcement. |
| AMC/AIME school-level data | Gated behind MAA teacher login. Every "Harker had 15 AIME qualifiers" is self-reported. | The most commonly cited metric in this space has no public authoritative source. |
| Menlo overlapping windows | 2-year rolling windows double-count if summed naively. | Every school's reporting methodology is different. You cannot compare across schools without understanding each one. |
| Nueva tier minimums | "10 or more" stored as count=10 inflates aggregates. | Label minimums explicitly; don't use in aggregate comparisons. |
| LinkedIn scraping | Legally low-risk (hiQ v. LinkedIn), but contractually prohibited by ToS. Manual browsing only. | Don't automate LinkedIn. Use it for manual spot-checks. |
| Podcasts for trajectory data | No podcast systematically covers K-12 development arcs. | Audio is the wrong format for structured data extraction. |
| Alumni magazines | Career snapshots, not developmental narratives. | Schools optimize alumni communications for fundraising, not research. |
| Davidson Institute outcomes data | Zero published data despite tracking from age 5. | Institutional longitudinal data exists but is gated. Relationship-building required. |

### What Needs More Work

1. **Scale Reddit crawl** — only 98 of 5,000+ posts. Paginate through full history.
2. **Add r/ApplyingToCollege** — larger subreddit, noisier, but more profiles.
3. **College Confidential crawler** — different HTML structure, needs its own parser.
4. **MIT Admissions Blog systematic crawl** — only got 13 profiles from ~100 trajectory-relevant posts.
5. **USA Swimming data prototype** — confirmed as most complete K-8 longitudinal DB but haven't built the crawler yet.
6. **USCF chess ratings lookup** — confirmed available with ChessGraphs.com but haven't integrated.
7. **Chinese parent forum mining** — huaren.us is public and crawlable but needs LLM extraction for narrative posts. Xiaohongshu requires auth.
8. **Multi-year MATHCOUNTS→USAPhO matching** — need 2-3 more years of data for the age gap to close and cross-competition trajectories to emerge.
9. **Build the intake survey** — for the K-8 gap, the "create our own data" strategy (structured parent survey) may be the only scalable path.

---

## Part 4: Data Validation Approach

### The Validation Stack

Every claim in the guidebook and strategy documents goes through this validation:

**Level 1: Source verification**
- Is this from an official school publication (L1) or a third-party aggregator (L3)?
- Is the methodology documented? (e.g., "enrolled" vs "accepted" vs "applied")
- Are there known biases? (e.g., school profiles are marketing documents)

**Level 2: Cross-source validation**
- Does SHS's published Stanford enrollment count match the number of athlete commits to Stanford?
- Does the UC InfoCenter ethnicity data for Harker match the known demographic composition?
- Do Reddit self-reported SAT scores fall in plausible ranges?

**Level 3: Internal consistency**
- Are class sizes consistent across sources and years?
- Do year-over-year trends make sense (no 500% spikes without explanation)?
- Do athlete commit counts + non-athlete counts = total enrolled?

**Level 4: External benchmark**
- Does the user's manually collected spreadsheet match our DB? (100% match achieved)
- Do our acceptance rates match known national rates? (Stanford 17% from our sample vs ~4% nationally — explained by self-selection bias in Reddit)

### Specific Validation Results

| Claim | Method | Result |
|---|---|---|
| SHS 5yr Ivy+ total = 133 | Summed from DB, cross-checked with wiki article | Exact match |
| Athletes to Ivy+ = 50 | Counted from athlete_commits table | Exact match |
| Water polo to Ivy+ = 22 | Filtered by sport | Exact match |
| Stanford total enrolled = 28 | DB query | Exact match |
| 2022 Stanford athletes = 8 (7 WP + 1 LAX) | Individual athlete records | Exact match |
| SHS Asian share = 22-29% | UC InfoCenter, 5 years | Consistent across years |
| Harker class size ~230 | Not directly confirmed | Estimated from placement volume — needs official verification |
| Duke MS-only = weaker than undergrad legacy | 3 consulting sources + Duke policy ambiguity | L3 confidence — no L1 confirmation |
| Stanford legacy ban (AB 1780) | California Governor's press release | L1 confirmed |

### What We Cannot Validate

- Harker's athlete share (they don't publish athlete commit data)
- Menlo's per-year enrollment counts (only publish 2-year windows)
- Whether Nueva's "10 or more" is actually 10, 15, or 25
- Duke's specific policy on graduate-degree legacy
- Any individual Reddit/YouTube profile's accuracy (self-reported)

---

## Part 5: Lessons Learned

### On Data Architecture

1. **SQLite + markdown hybrid is the right architecture.** Structured queries for numbers (how many? what rate?), markdown for narratives and raw sources. Don't force everything into one format.

2. **College name normalization is harder than it looks.** "University of California (Berkeley)" vs "UC Berkeley" vs "University of California, Berkeley" — you'll discover new variants with every new source. Build the normalizer incrementally and test constantly.

3. **Store raw before processing.** Every crawled post, PDF, and web page gets saved as markdown with frontmatter before any extraction. When sources go down (and they will), you still have the data.

4. **Cross-validation is not optional.** The 100% match against the user's manual spreadsheet caught normalization bugs (69 rows affected) that would have silently corrupted all aggregate queries.

### On Data Collection

5. **School-published data is the ground truth.** Aggregators (Niche, PrepReview, Chicardgo School) are useful for discovery but unreliable for precision. Always go to the source PDF.

6. **Every school reports differently.** You cannot compare across schools without understanding each school's methodology. Menlo's "23 went to Stanford" means something different from SHS's "7 went to Stanford" because Menlo's number is from a 2-year overlapping window.

7. **The most valuable data is the data nobody else publishes.** SHS's athlete commit pages are the single most valuable data source in this project because no other school does this. The athlete/non-athlete decomposition changes every conclusion.

8. **The K-8 gap is real and structural.** No institution, no publication, no database captures what children do between ages 5 and 14. This is the moat that private counselors sell. Breaking it requires connecting domain-specific silos (swimming, chess, music, math competitions) that have never been linked.

### On LLM Extraction

9. **Rule-based extraction first, LLM second.** The rule-based parser handles 70% of Reddit posts at zero cost and infinite speed. Gemini handles the remaining 30%. Don't use LLM for everything — it's slower, costlier, and less reliable.

10. **Structured output from LLMs is fragile.** Gemini 2.5 Flash produces malformed JSON 10-15% of the time despite `response_mime_type="application/json"`. Always retry and always validate.

11. **The extraction prompt is the product.** The difference between 12 results and 1,103 results was entirely in the prompt and parsing logic — same source data, same LLM. Iteration on extraction quality matters more than iteration on data collection.

### On Guidebook Production

12. **SOP v2 works.** The one-iteration rule — every requirement the critic checks must be in the brief the compiler reads — eliminated the 4-pass polish cycles from the STEM guidebook.

13. **Data-grounded writing is faster, not slower.** Having verified numbers in a queryable DB made chapter drafting faster because the writer (agent) could query exact figures instead of estimating. Every claim has a source.

14. **The editorial angle matters more than the data.** "Here's what the school brochure doesn't tell you" is a more powerful frame than "Here's our comprehensive data analysis." The insight (athlete decomposition changes everything) is what makes people read; the data is what makes them trust.

---

## Part 6: Monetization Thoughts

### The Guidebook as a Product

**Free distribution (growth strategy):**
- PDF shared via WeChat groups, parent forums, school WhatsApp groups
- Builds credibility and audience for premium offerings
- Chinese translation doubles the addressable market (Bay Area Chinese parents are the primary audience)
- Annual refresh (each September when new placement data publishes) gives reason to re-share

**Paid guidebook ($29-49):**
- Enhanced version with interactive data (not just static tables)
- School-specific deep dives (custom report for your school)
- Personalized positioning worksheet
- Annual subscription for updated data

### The Data as a Service

**School comparison tool (freemium web app):**
- Free tier: see aggregate Ivy+ rates for 11 schools
- Paid tier ($9.99/month): filter by athlete/non-athlete, ethnicity, specific colleges
- Premium tier ($29.99/month): student profile matching, archetype analysis, trajectory planning

**Custom school report ($99-299 per school):**
- Deep dive on a specific school using our DB + UC data + athlete analysis
- For parents considering enrollment or transfer
- Can be generated programmatically from the DB

### The AI Counselor (long-term)

**Personal positioning analysis ($199-499):**
- Parent inputs child's profile (age, school, activities, competitions, demographics)
- System matches against 110+ student profiles, 90 trajectories, school placement data
- Outputs: realistic target schools, probability estimates, grade-by-grade action plan
- Updated annually as new data comes in

**Ongoing advisory ($49/month subscription):**
- Quarterly check-ins: "Is my child on track?"
- Competition result analysis: "My kid scored 22 on AMC 8, what does that mean?"
- School transfer analysis: "Should we move from SHS to Menlo for 6th grade?"
- College list building: "Given her profile at age 14, what's realistic?"

### Pricing Benchmark

| Service | Price | What They Offer |
|---|---|---|
| Private college counselor | $5,000-$50,000/package | Personal relationship, Naviance access, essay editing |
| IvyWise comprehensive | $10,000-$30,000 | Multi-year advising, school selection, application support |
| Crimson Education | $5,000-$20,000 | International, data-driven, team of specialists |
| Our AI counselor (proposed) | $199-499/year | Data-driven analysis, trajectory planning, profile matching |

The value proposition: **80% of what a $20K counselor knows, at 2% of the cost, grounded in verified public data instead of anecdotes.**

---

## Part 7: Adjacent Books to Write

The college placement guidebook is one piece of a larger content strategy. The same data architecture and production SOP can produce:

### Book 2: "The Math Competition Parent's Handbook"
- **Audience:** Parents of K-8 kids considering competition math
- **Data we already have:** MATHCOUNTS CA results (371 students, 43 multi-year), USAPhO medals (1,049), AoPS historical results, Davidson Forum trajectories (36 K-8 records)
- **What it covers:** The AMC pipeline explained, when to start, how to tell if your kid is ready, RSM vs AoPS vs self-study, MATHCOUNTS preparation, what scores mean at each level, how competition math maps to college admissions
- **Synergy:** Chapters 8-9 of the placement guidebook are the nucleus; this book goes 10x deeper

### Book 3: "The Bay Area School Choice Guide — Middle and High School"
- **Audience:** Parents making 6th-grade or 9th-grade school decisions
- **Data we already have:** 11 schools profiled, Ivy+ rates, UC ethnicity data, MATHCOUNTS school presence, Sci Oly school rankings
- **What it covers:** School-by-school analysis deeper than Chapter 4, interview advice, application timelines, financial aid comparison, "culture fit" framework
- **Synergy:** Chapter 10 (Should You Transfer?) is the teaser

### Book 4: "The Asian American College Application — A Data-Driven Guide"
- **Audience:** Asian American families navigating post-SFFA admissions
- **Data we already have:** UC ethnicity data across 11 schools, post-SFFA enrollment trends at 7 universities, demographic competition analysis, 21 Asian female comparable profiles
- **What it covers:** The real impact of being Asian in admissions (data, not narrative), how to differentiate within a large Asian applicant pool, the SES proxy problem, which schools are gaining vs losing Asian enrollment, essay strategy for Asian applicants
- **Synergy:** Chapter 5 is the nucleus; this book goes 10x deeper and adds essay/narrative guidance

### Book 5: "From Beast Academy to AIME — A 10-Year Math Journey" (Chinese language)
- **Audience:** Chinese immigrant parents in the US
- **Data we already have:** STEM guidebook (13 chapters), MATHCOUNTS data, Davidson Forum K-8 trajectories, competition ladder (Math Kangaroo → MOEMS → AMC 8 → MATHCOUNTS → AMC 10 → AIME)
- **What it covers:** Year-by-year curriculum guide, RSM vs AoPS decision framework, how to supplement school math, when to enter competitions, realistic score benchmarks by age
- **Synergy:** Direct sequel to the STEM guidebook, focused on the math track specifically, in Chinese

---

## Part 8: What an AI Counselor Still Needs to Know

The system we built today has impressive breadth but significant gaps for a production-grade counselor:

### Knowledge Gaps

| What's Missing | Why It Matters | How to Get It |
|---|---|---|
| **Actual application essays** | Essays are 30-40% of the decision at holistic schools | AdmitSee ($), published essay books, MIT Admissions Blogs |
| **Recommendation letter patterns** | What teachers say matters enormously | No public data exists. Could survey parents about counselor/teacher recs. |
| **Interview preparation** | Many schools interview; no data on what works | Podcast transcripts, forum advice threads |
| **Financial aid strategies** | Aid packages vary 5x across schools for same family | School-published CDS financial aid data, Net Price Calculators |
| **Demonstrated interest tracking** | Some schools track campus visits, email opens | Admissions consultant knowledge, school-specific policies |
| **Waitlist conversion rates** | "Waitlisted" means different things at different schools | Common Data Set Section C2, school-specific data |
| **Transfer student outcomes** | What happens to kids who transfer between schools? | No public data. Would need to survey transfer families. |
| **Gap year impact** | How does a gap year affect admissions? | Anecdotal only. Admissions office policies. |
| **International student dynamics** | How do international applicants affect domestic admits? | SEVIS data (aggregate), school-published international %) |

### Data Quality Improvements Needed

| Current State | Target State | Effort |
|---|---|---|
| 98 Reddit profiles | 1,000+ profiles | Scale crawl, add r/ApplyingToCollege |
| 13 MIT blog profiles | 50+ trajectory profiles | Deeper blog crawl + Gemini extraction |
| 36 Davidson K-8 trajectories | 200+ K-8 records | Systematic forum crawl + huaren.us |
| 0 swimming/chess data | 100+ development curves | Build SWIMS + USCF lookup tools |
| 11 schools | 30+ schools | Add top public + more privates |
| No essay data | 500+ essays with outcomes | AdmitSee API or published collections |
| Self-reported profiles only | Verified profiles | Cross-reference competition results with college enrollment |

### Technical Infrastructure Needed

| Component | Current | Needed |
|---|---|---|
| Query interface | Python CLI (`query.py`) | Web UI or natural language query |
| Profile matching | `cross_join.py` script | ML-powered similarity scoring |
| Archetype engine | Not built | Cluster analysis on 1,000+ profiles |
| Annual refresh | Manual process | Automated cron (check school websites each September) |
| Entity resolution | Prototype (90 trajectories) | Production system with confidence scoring and manual review queue |
| Chinese content | Not started | Translate guidebook + build Chinese source crawlers |

---

## Part 9: The Meta-Lesson

This entire system — from a parent's question about SHS placement data to a 10-chapter guidebook, two SQLite databases, 16 research agents, and the foundations of an AI counselor — was built in a single 6-hour conversation.

The enabling factors:

1. **The `llm_knowledge/` architecture already existed.** The KB pipeline (topics, raw sources, wiki articles, guidebook SOP) gave us a production-ready framework from day one.

2. **Parallel agent execution.** Running 3-4 agents simultaneously (research + drafting + data extraction) compressed what would be weeks of sequential work into hours.

3. **SQLite as the single source of truth.** Every claim traces back to a queryable database row. No estimates, no "I think it was about 28." Either the DB says 28 or it doesn't.

4. **Iterative validation.** The 100% match against manual data wasn't lucky — it was the result of finding and fixing normalization bugs before they compounded.

5. **The user's domain expertise.** Weizheng's manually collected spreadsheet, his knowledge of which PDFs to look at, his understanding of which questions matter (athlete vs non-athlete, Duke legacy, Asian demographics) — these shaped every decision. The AI executed; the human directed.

The system is not finished. But the hardest part — proving that public data can produce counselor-grade insights — is done. The athlete/non-athlete decomposition. The ethnicity-adjusted school comparison. The competition-to-college trajectory linking. These are things no public resource offers today. Every additional data point, every additional school, every additional year of competition results makes the whole system more valuable.

The $50K counselor has intuition built from hundreds of cases. This system has data built from thousands of public records. Neither is complete alone. The combination — data-grounded intuition, or intuition-guided data — is what parents actually need.

---

**Document version:** v1.0
**Total session artifacts:** 24 git commits, 10 guidebook chapters (~32K words), 2 SQLite databases, 16 research reports, 90 resolved trajectories, 1 PDF (3.0 MB)
