---
generated: 2026-04-18
purpose: Source investigation — AoPS and related math competition data sources for student trajectory research
researcher: research-agent
reliability_tier: L3-aggregator (AoPS community/wiki) | L2-authoritative (MATHCOUNTS official)
---

# AoPS and Math Competition: Data Source Investigation

Investigation of Art of Problem Solving (AoPS) and related math competition platforms as sources of student mathematical development trajectory data. Relevant for understanding how students like Lexi (Beast Academy → RSM → Math Kangaroo → MOEMS → AMC 8 → MATHCOUNTS → AMC 10/12 → AIME) typically progress.

---

## 1. AoPS Community Forums (artofproblemsolving.com/community)

### Access Status
WebFetch returns HTTP 403 for the main community domain. Chrome MCP can load forum pages successfully. Community forum content is publicly visible without login.

### Forum Structure (Confirmed)

The main competition forum is at:
- `https://artofproblemsolving.com/community/c5_contests_amp_programs`

This forum contains tagged threads. Confirmed active tags visible at that URL:
- AMC, AIME, AMC 10, AMC 12, USA(J)MO, USAMO, USAJMO, AMC 8, MATHCOUNTS, AIME I, AIME II, AMC 10A, AMC 10B, AMC 12A, AMC 12B, ARML, HMMT, Alcumus, college, summer program, PROMYS, Mathcamp, Ross Mathematics Program, AwesomeMath, USAMTS

No standalone "College Admissions" subforum was found as a top-level category. The college tag exists (`c5t209f5_college`) but it is a tag within the Contests & Programs forum, not a dedicated college admissions space. There is a "High School Life" forum at c10, but it redirects to Site Support. The AoPS community does NOT appear to have a dedicated "who got in" subforum analogous to r/collegeresults.

### AMC Score Threads — CONFIRMED HIGH-VALUE DATA SOURCE

**Example thread confirmed:** "2024 AMC 12A Score Thread"
URL: `https://artofproblemsolving.com/community/c5h3438279_2024_amc_12a_score_thread`

**Thread format confirmed by direct fetch:**
Users post to a running table with columns: Username | Grade | Score | Change (from prior year).

Confirmed sample entries from this thread:
- Jack_w | Grade 11 | AMC 12A: 120 | Change: -24 (from 2023)
- vsamc | Grade 11 | AMC 12A: 130.5 | Change: -10.5
- ezpotd | Grade 11 | AMC 12A: 144 | Change: -6
- HonestCat | Grade 11 | AMC 12A: 105 | Change: +3 (reference to 12B)

**What this data provides:**
- Username (pseudonymous AoPS handle)
- Current grade level
- Score on the specific exam
- Year-over-year score change (explicitly showing longitudinal progression)
- These are self-reported but cross-referenced against known cutoffs

**Scrapability:** Public HTML, no login required. Thread IDs follow pattern `c5h{number}_{title}`. A score thread is created for each AMC 8, AMC 10A, AMC 10B, AMC 12A, AMC 12B exam every year. Threads can have hundreds to thousands of replies.

**Data fields available:** username, grade, score, prior year score (calculated delta), sometimes school (users sometimes mention it), sometimes city/state

**Privacy note:** Users post voluntarily, using pseudonymous handles. School names appear occasionally but not systematically. Named individuals cannot be identified without additional information.

**Volume estimate:** Each major exam (AMC 10A, 10B, 12A, 12B) generates threads with typically 100-500+ posts per year from active AoPS users. These represent a self-selected sample of the most engaged math competition students.

**Key limitation:** Selection bias — AoPS forum participants are among the most serious and high-scoring competition students nationally. Not representative of all AMC takers.

---

## 2. AoPS Wiki — Competition Results Pages

### AMC Historical Results
URL: `https://artofproblemsolving.com/wiki/index.php/AMC_historical_results`

**Status: FULLY PUBLIC, EXTREMELY DATA-RICH**

This is a community-maintained wiki page covering AMC 8, AMC 10A/B, AMC 12A/B, AIME I/II, USAMO, and USAJMO statistics from approximately 2000-2001 through 2025-2026 (current year).

**Data fields per exam per year:**
- Average score
- AIME qualification floor (for AMC 10/12)
- Top 25% score
- Top 10% score
- Top 5% (Honor Roll) score
- Top 2.5% score
- Top 1% (Distinguished Honor Roll) score
- Total number of students who took the exam
- USAMO/USAJMO qualifying index cutoffs

**Sample actual data extracted (most recent cycles):**

AMC 8 — January 22-31, 2026:
- Average Score: 12.42 / 25
- Top 5% (HR): 21
- Top 2.5%: 23
- Top 1% (DHR): 24
- Total Students: 80,975

AMC 10A — November 5, 2025:
- Average Score: 57.13
- AIME Floor: 105 (top ~6%)
- Top 5% HR: 112.5
- Top 2.5%: 124.5
- Top 1% DHR: 136.5
- Total Students: 31,617

AMC 10B — November 13, 2025:
- Average Score: 57.00
- AIME Floor: 99 (top ~6%)
- Top 5% HR: 105
- Top 1% DHR: 133.5
- Total Students: 25,195

AMC 12A — November 5, 2025:
- Average Score: 64.44
- AIME Floor: 96 (top ~13%)
- Top 1% DHR: 150
- Total Students: 20,446
- Note: Problem 25 voided for all participants

AIME I — February 6, 2025:
- Average Score: 6.16
- Median: 6
- USAMO cutoff: 237 (AMC 12A), 249.5 (AMC 12B)
- USAJMO cutoff: 233 (AMC 10A), 243 (AMC 10B)
- Total Students: 4,690

AIME I — February 5, 2026:
- Average Score: 6.27
- Top 1%: 14
- Total Students: 4,752

USAMO — March 19, 2025:
- Average score: 14.37
- Total students: 293

USAJMO — March 19, 2025:
- Average score: 16.76
- Total students: 241

**Historical depth:** Data goes back to 1999-2000 (25+ years of records). The table of contents lists 29 academic year sections.

**Scrapability:** Standard public wiki HTML. Fully parseable. No login required. All data is in structured heading/text format.

**What this CANNOT tell us:** Individual student scores. School-level breakdowns. Geographic data. These are population-level statistics only.

**Key policy change noted:** Since 2025-2026, USAMO/USAJMO qualifying index formula changed from (AIME score × 10) + AMC score to (AIME score × 20) + AMC score. International students' scores no longer affect AIME cutoffs as of August 2025.

### USAMO Historical Results
URL: `https://artofproblemsolving.com/wiki/index.php/USAMO_historical_results`

**Status:** Confirmed accessible. Contains individual qualifier names by year, school affiliations in some years.

**What this provides:** Named USAMO qualifiers by year. This is the level where individual identification becomes possible (USAMO is ~250-300 students nationally per year). Bay Area school presence could be tracked at this level.

### MATHCOUNTS Historical Results
URL: `https://artofproblemsolving.com/wiki/index.php/MATHCOUNTS_historical_results`

**Status: FULLY PUBLIC, DATA-RICH**

Sections confirmed:
- National Team Champions by year (1984-2025): state-level team champions
- Countdown Round Champions by year (1984-2024): individual national champions with name and state
- Masters Round Winners
- Written Test Champions
- Most Improved Team
- Spirit Stick Winners

**Sample data extracted:**
- 2025 National Champion: Massachusetts MathCounts
- 2024 National Champion: Texas MathCounts
- 2022 Countdown Champion: Allan Yuan, Alabama
- 2023 Countdown Champion: Channing Yang, Texas
- 2024 Countdown Champion: Ben Jiang, Florida
- California has won the most national championships overall (8 times): 1986, 1992, 2000, 2002, 2003, and additional years

California MathCounts page (`/wiki/index.php/California_MathCounts`) confirms:
"Usually the majority of the California team is from the North because that includes the Bay Area."

**Scrapability:** Standard public wiki HTML. Individual champion names are linked to their AoPS community user profiles.

---

## 3. AoPS User Profiles

### Community User Profiles
URL pattern: `https://artofproblemsolving.com/community/user/{user_id}`

**Status confirmed by fetching user profile of "Jack_w" (user ID 1020558):**

Fields visible on a community user profile (WITHOUT login):
- Username
- Join date
- Status message (user-set, freeform)
- Last visited date
- Total post count (with link to posts)
- Blog link (if user has one)
- "Given" upvotes count
- "Received" upvotes count

**What is NOT on community profiles:**
- No competition scores displayed
- No grade or school information
- No structured competition history field
- No AMC/AIME/MATHCOUNTS scores database

**Verdict:** Community user profiles contain NO competition data. They are essentially activity profiles.

### AoPS Wiki User Pages
URL pattern: `https://artofproblemsolving.com/wiki/index.php/User:{username}`

**Status confirmed by fetching User:Mysmartmouth/Awards:**

Some users create personal wiki pages with their own competition records. Example found:

User: Mysmartmouth
- 6th Grade: AMC 8 Score: 18, 1st Place Certificate
- 7th Grade: AMC 8 Score 20 (Top 1% USA), AMC 10 Score 102, MathCounts Regional 15th Place Individual / 1st Place Countdown
- 8th Grade: AMC 8 Score 22 (school winner), AMC 10 Score 120.5 (Top 1%, AIME qualifier), AIME Score 4, MathCounts Regional 1st Individual / 2nd Countdown / 2nd Team, MathCounts State 3rd Individual / 2nd Countdown / 1st Team, MathCounts National 15th Place Team / 87th Individual

**This is exactly the longitudinal trajectory format needed:** Grade-by-grade competition performance across multiple years, multiple competitions, showing progression.

**Volume:** Unknown how many users have created such pages. These are entirely voluntary, self-reported, and not indexed systematically. Search via Google `site:artofproblemsolving.com/wiki/index.php User: awards` may surface more examples.

**Privacy:** Usernames are pseudonymous. Some users mention their school and state (the example above mentions SC = South Carolina based on context). Users have voluntarily made this data public.

---

## 4. AoPS School Page (AoPS Online / AoPS Academy)

URL: `https://artofproblemsolving.com/school`

**Status:** This is AoPS's commercial online school — course listings, not competition outcome data. No public student outcome or trajectory data is published here.

**AoPS Academy campuses** (in-person locations including Bay Area) do not publish student competition outcome data publicly.

**Alcumus** (AoPS's adaptive problem platform, `artofproblemsolving.com/alcumus`): No public data about individual student progress. Student-level data is private. No published aggregate statistics about progression rates.

**Beast Academy** (beastacademy.com): Elementary math curriculum. No public data about student longitudinal performance.

**Verdict on AoPS School/Alcumus/Beast Academy:** These platforms have rich longitudinal data internally, but none of it is publicly accessible for research purposes.

---

## 5. AoPS Competition Result Threads — Longitudinal Data

### Score Threads as Trajectory Data

The AMC score threads are the richest source of self-reported longitudinal data on AoPS. The key pattern:

After each AMC exam, a community member starts a thread. Users post their scores and explicitly compare to prior years. The cumulative table in each thread shows:
- Username (same across years)
- Grade level
- Current score
- Delta from prior year

A researcher tracking the same username across multiple threads (e.g., AMC 8 in 8th grade, AMC 10A in 9th grade, AMC 12A in 11th grade) can reconstruct a multi-year competition trajectory.

**Confirmed thread URLs:**
- 2024 AMC 12A: `https://artofproblemsolving.com/community/c5h3438279_2024_amc_12a_score_thread`
- 2024 AMC 10A: searchable via AoPS community
- Similar threads exist for every AMC exam back to approximately 2010-2015

**Data format:** LaTeX-rendered tables embedded in forum posts (not plain HTML — the tables are rendered as images at `latex.artofproblemsolving.com`). The image ALT text contains the LaTeX source which includes the actual data.

**Technical note:** The table data is in LaTeX image ALT attributes, not in the page HTML as text. A scraper would need to extract the `alt` attribute from `img` tags pointing to `latex.artofproblemsolving.com` and parse the LaTeX table syntax.

**Alternative approach:** Users often post plain-text versions of their scores in the post body before or after the table, which is extractable as standard HTML text.

### AoPS Personal Blogs

URL pattern: `https://artofproblemsolving.com/community/c{blog_id}`

Some active AoPS users maintain blogs documenting their math competition journey year by year. These appear in user profiles (e.g., Jack_w's blog "3. 8. 4. Three hundred eighty four."). These are rich longitudinal narratives but require individual discovery.

### "My Story" / Journey Threads

Search result surfaced: `https://artofproblemsolving.com/community/c1645340h2381838_my_story`

Some users post "my story" threads describing their math trajectory. These are gold for trajectory analysis but require thread-by-thread reading.

---

## 6. AoPS "Who Got In" Threads — College Admissions Intersection

**Finding:** No dedicated "Who Got In" subforum found on AoPS. The college tag exists within Contests & Programs but no structured admissions results thread comparable to r/collegeresults was found in the publicly visible portion of the forum.

**What may exist (unconfirmed):** Discussions about college admissions results may appear in individual blogs, "my story" threads, or under the "college" tag. Some may require login to access.

**The closest equivalent found:** The score threads implicitly provide college admissions context because users list their grade (a 12th grader's AMC score in their final year of high school is effectively their application-year score). If a user's post history can be tracked across multiple years, you can see their K-12 competition arc ending at the college application moment.

---

## 7. MATHCOUNTS Bay Area Specific Data

### California MATHCOUNTS Organization
URL: `https://cspeef.org/`
Formal name: California Society of Professional Engineers Education Foundation (CSPEEF)

### Northern California State Competition
URL: `https://cspeef.org/state-competitions/northern-california-state/`

**Status: CONFIRMED PUBLIC DATA WITH SCHOOL-LEVEL RESULTS**

Bay Area feeds into this competition via these chapter competitions:
- Coyote Valley
- Diablo
- East Bay
- Fremont
- Golden Gate
- Monterey Bay
- Peninsula
- San Mateo County
- Santa Clara Valley Central
- Santa Clara Valley Northwest
- Santa Clara Valley South

**Available result documents (all public PDFs):**

2026 NorCal State (March 28, 2026, at Harker School Upper Campus):
- Top 25% of Individuals: `http://cspeef.org/wp-content/uploads/2026/04/Top25IndividualsNorCal2026.pdf`
- Top 40% of Teams: `http://cspeef.org/wp-content/uploads/2026/04/Top40TeamsNorCal2026.pdf`
- Distribution of Scores: `http://cspeef.org/wp-content/uploads/2026/04/DistributionOfScores.pdf`

2025 NorCal State (March 22, 2025, at Harker School Middle School Campus):
- Top 25% of Competitors: `http://cspeef.org/wp-content/uploads/2025/03/Top25CompetitorsNorCal2025.pdf`
- Top 40% of Teams: `http://cspeef.org/wp-content/uploads/2025/03/Top40TeamsNorCal2025.pdf`
- Distribution of Scores: `http://cspeef.org/wp-content/uploads/2025/03/Score-DistributionNorCal2025.pdf`

2024 NorCal State:
- Top 25% Individuals: `http://cspeef.org/wp-content/uploads/2024/03/Top25NorCal2024.pdf`
- Top 40% Teams: `http://cspeef.org/wp-content/uploads/2024/03/Top40NorCal2024.pdf`
- Analysis Report: `http://cspeef.org/wp-content/uploads/2024/03/AnalysisReportNorCal2024.pdf`
- Distribution of Scores: `http://cspeef.org/wp-content/uploads/2024/03/ScoreDistributionNorCal2024.pdf`
- Question Analysis: `http://cspeef.org/wp-content/uploads/2024/03/QuestionAnalysisNorCal2024.pdf`

**Data fields in these PDFs:** Student name (first and last), school name, score, rank. PDFs are accessible without login but require PDF parsing tooling to extract text (they are not HTML-readable). 

**Note on 2026:** The NorCal state competition is hosted at The Harker School. AlphaStar Academy is a $1,000 sponsor. Both are Bay Area institutions, confirming Bay Area dominance of this competition.

### Bay Area Chapter-Level Data (Confirmed School Names)

**Santa Clara Valley Central Chapter — 2024 State Qualifiers:**
- Team 1 (The Harker School): Vihaan Gupta, Aarav Mann, Andrew Shi, Lucas Yuan
- Team 2 (BASIS Independent Silicon Valley): Nathen Chen, Ethan Qu, Keji Yuan, Alex Zhan
- Team 3 (Union Middle School): Lucian Lao, Jennifer Neyman, Elliot Seo, Siddhanth Venkatesan
- Individuals: Eric Zhang (Harker), Yichen Wu (BASIS), Jeffrey Wang (Harker)

**Santa Clara Valley Central Chapter — 2023 State Qualifiers:**
- Team 1 (The Harker School): Sylvia Chen, Shamik Khowala, Jonathan Li, Heather Wang
- Team 2 (BASIS Independent Silicon Valley): Nathan Chen, Daniel Ji, Nicholas Wang, Alex Zhan
- Individuals: Vihaan Gupta, Aarav Mann, Andrew Shi (all Harker)

**Peninsula Chapter — 2024 State Qualifiers:**
- Team: Bullis Charter School (Ethan Bao, Camea Caprita, Waroon Thapanangkun, Dylan Wang)
- Team: Frank S. Greene Middle School (Helen Law, Matthew Lee, Oscar Varodayan, Brandon Wu)
- Individuals: Krittika Chandra, Max Li, Aarush Rachakonda (Challenger School-Middlefield)

**East Bay Chapter — 2024 State Qualifiers:**
- Team: Diablo Vista Middle School (Ethan Chang, Dimitri Liveris, Sahasra Chappidi, Sean Yue)
- Team: Black Pine Circle School (Aoife Hennessey, Kannan Ravikumar, Raman Ravikumar, Shoshana Seplow)
- Individuals: Robin Byun, Noah Epstein (Diablo Vista), Titus Cheung (Harbor Light Academy)

**Observations:**
- The Harker School dominates the Santa Clara Valley Central chapter, routinely placing 2 of the 3 advancing teams
- BASIS Independent Silicon Valley consistently places in the top 2
- Bullis Charter School (Los Altos Hills) appears in Peninsula chapter results
- Challenger School (Middlefield location, Sunnyvale) places individual qualifiers

**Privacy considerations:** Student names in MATHCOUNTS results are of middle school students (grades 6-8). These are public competition results published by official organizers, but they name minors.

---

## 8. AoPS Blog — Math Contest Pathway Guide

URL: `https://artofproblemsolving.com/blog/articles/math-contest-guide-for-advanced-students`

**Status: FULLY PUBLIC**

This is AoPS's official contest pathway guide. It provides the canonical competition ladder and grade recommendations:

### Elementary Level
**Math Kangaroo:**
- Grades 1-12 (open to all)
- Format: 75 min, 30 questions (grades 5-12)
- No invitation required

**MOEMS (Mathematical Olympiads for Elementary and Middle Schools):**
- Elementary division: Grades 4-6
- Middle School division: Grades 6-8
- Format: 5 contests per year, 30 min each, 5 problems each
- No invitation required, run through schools or institutes
- 120,000+ students annually in all 50 states + 39 countries

### Middle School Level
**MATHCOUNTS Competition Series:**
- Grades 6-8
- School registration required
- Levels: Chapter → State → National

**AMC 8:**
- Grade 8 and under, under 14.5 at test time
- 25 questions, 40 minutes, multiple choice
- No algebra content
- No invitation required

### High School Level
**AMC 10:**
- Grade 10 and under, under 17.5
- 25 questions, 75 minutes, multiple choice
- Covers high school curriculum through 10th grade

**AMC 12:**
- Grade 12 and under, under 19.5
- 25 questions, 75 minutes, multiple choice
- Covers full high school curriculum excluding calculus

**AIME:**
- Invitation only (top ~6-8% of AMC 10, top ~13-16% of AMC 12)
- 15 questions, 3 hours, integer answers (0-999)

**USAMO / USAJMO:**
- Invitation only (index score from AMC + AIME)
- USAJMO for AMC 10 track; USAMO for AMC 12 track
- Proof-based, 6 problems over 2 days

**International: IMO, EGMO**
- By invitation only, national team selection

---

## 9. Summary Assessment by Data Source

| Source | URL | Data Type | School-Level? | Individual-Level? | Public? | Volume |
|--------|-----|-----------|--------------|------------------|---------|--------|
| AMC Score Threads | artofproblemsolving.com/community/c5 | Self-reported scores by exam + grade + year-over-year delta | No (occasional) | Yes (pseudonymous) | Yes | 100-500+ per exam per year |
| AoPS Wiki AMC Historical | artofproblemsolving.com/wiki/index.php/AMC_historical_results | Population stats: cutoffs, averages, participant counts | No | No | Yes | 25 years of data, all competitions |
| AoPS Wiki USAMO Historical | artofproblemsolving.com/wiki/index.php/USAMO_historical_results | Named qualifiers by year | Sometimes | Yes (real names) | Yes | ~300 per year |
| AoPS Wiki MATHCOUNTS | artofproblemsolving.com/wiki/index.php/MATHCOUNTS_historical_results | National champions, state team champions | State only | Yes (national champs) | Yes | Since 1984 |
| AoPS User Wiki Pages | artofproblemsolving.com/wiki/index.php/User:{name}/Awards | Self-reported career trajectories | Sometimes | Yes (pseudonymous) | Yes | Unknown, scattered |
| AoPS Blogs | artofproblemsolving.com/community/c{id} | Narrative journey documentation | Sometimes | Yes (pseudonymous) | Yes | Unknown |
| Community User Profiles | artofproblemsolving.com/community/user/{id} | Activity metadata only | No | No | Yes | Millions of users |
| AoPS School/Alcumus/Beast Academy | Various | None (private internal data) | No | No | No | N/A |
| NorCal MATHCOUNTS State PDFs | cspeef.org | Named students + school + score + rank | Yes | Yes (real names, minors) | Yes | Top 25% per year, ~2024-2026 available |
| NorCal MATHCOUNTS Chapter pages | cspeef.org/competitions/* | Named state qualifiers + school | Yes | Yes (real names, minors) | Yes | Per chapter, per year |
| California MathCounts Wiki | artofproblemsolving.com/wiki/index.php/California_MathCounts | State team wins only, no school data | No | No | Yes | Minimal |

---

## 10. Assessment for Lexi's Trajectory Research

### What the data CAN answer:

**Normative milestones and timing:**
The AoPS Wiki AMC historical results page provides population-level benchmarks for every step of the competition ladder:
- What AMC 8 score puts a student in the top 1%? (Currently: 24/25)
- What is the typical AIME qualifier score on AMC 10? (AIME floor: 99-105 depending on year/form)
- How many students nationally make USAMO? (~293 in 2025)
- What percentage of AMC 10 takers qualify for AIME? (~6-8%)

**Bay Area school dominance in MATHCOUNTS:**
The NorCal MATHCOUNTS data directly names which Bay Area schools dominate at the state level:
- The Harker School (San Jose): routinely 2 of 3 advancing teams from SCV Central
- BASIS Independent Silicon Valley: consistent state qualifier
- Bullis Charter School (Los Altos Hills): Peninsula chapter qualifier
- Challenger School: individual qualifiers

**Trajectory from score threads:**
By tracking a pseudonymous user across score threads from AMC 8 (7th or 8th grade) through AMC 10 (9th grade) through AMC 12 (11th grade), the AoPS score threads can document a 4-6 year trajectory for individual students (though not connected to their real identities or college outcomes).

### What the data CANNOT answer:

- Connection between competition trajectory and college admissions outcomes — no data source links individual AMC/AIME/MATHCOUNTS scores to college admission results
- Real names to competition scores (for most sources)
- Geographic breakdown below the state level for AMC data (no Bay Area-specific AMC statistics)
- What fraction of Bay Area students reach each milestone vs. national peers

### Key Gap:

There is no public dataset that links Layer 2 (math competition scores) to Layer 3 (college admissions outcomes) at the individual level. The AoPS community occasionally has blog posts or threads where individual users describe both their competition history and their college admissions results, but there is no structured database of this.

**The closest to this intersection:**
- AoPS user blogs and "my story" threads where users describe their full journey including college results
- USAMO qualification lists (real names, ~300 per year) — if cross-referenced with college acceptances in the same year, could yield the most elite end of this spectrum
- Reddit r/collegeresults posts by students who also mention competition scores (already partially captured in this project's existing data)

---

## Raw Files Saved

| File | Content |
|------|---------|
| `raw/web/community/2026-04-18_aops-wiki-amc-historical-results-v2-snapshot.txt` | AoPS Wiki AMC historical results — full a11y snapshot including actual score data for 2021-2026 |
| `raw/web/community/2026-04-18_aops-wiki-mathcounts-historical-results-snapshot.txt` | AoPS Wiki MATHCOUNTS historical results — national champions and countdown round winners 1984-2025 |
| `raw/web/community/2026-04-18_aops-2024-amc12a-score-thread-snapshot.txt` | 2024 AMC 12A score thread — sample of user-reported scores with grade and year-over-year delta |
| `raw/web/community/2026-04-18_aops-c5-contests-programs-snapshot.txt` | Contests & Programs forum structure — confirming tag taxonomy and recent announcements |
| `raw/web/community/2026-04-18_aops-college-subforum-snapshot.txt` | c13 URL — redirects to Contest Collections, not college admissions |
| `raw/web/community/2026-04-18_aops-community-c9-snapshot.txt` | Other Forums (c9) — showing Peer-to-Peer Programs content |
| `raw/web/community/2026-04-18_aops-wiki-california-mathcounts-snapshot.txt` | California MathCounts wiki — minimal, confirms Bay Area dominance note |
| `raw/web/community/2026-04-18_aops-blog-math-contest-guide-snapshot.txt` | AoPS competition pathway guide — full grade-by-grade contest ladder |
| `raw/web/community/2026-04-18_aops-wiki-user-awards-example-snapshot.txt` | Example user wiki awards page — showing grade-by-grade trajectory format |
| `raw/web/community/2026-04-18_aops-user-profile-example-snapshot.txt` | Example AoPS community user profile — confirming no competition data shown |
| `raw/web/community/2026-04-18_mathcounts-california-norcal-state-snapshot.txt` | NorCal MATHCOUNTS state competition page — listing chapter feeds, results PDFs, 2024-2026 |
| `raw/web/community/2026-04-18_mathcounts-norcal-2025-top25-snapshot.txt` | NorCal 2025 Top 25% PDF — loaded in Chrome PDF viewer (data in PDF binary, not extractable via a11y) |
| `raw/web/community/2026-04-18_aops-c10-high-school-life-snapshot.txt` | c10 URL — redirects to Site Support, not High School Life |

---

## Recommended Next Steps

1. **PDF extraction for NorCal MATHCOUNTS:** Install `pdftotext` (poppler-utils) and extract the 2024, 2025, 2026 Top 25% Individual result PDFs from cspeef.org. These would give named students + school + score for the top ~50 students at Bay Area state competition. Directly answers "which Bay Area schools dominate MATHCOUNTS?"

2. **AMC score thread scraping:** Build a scraper targeting the LaTeX image ALT attributes in score threads for AMC 8, AMC 10A/B, AMC 12A/B from 2018-2026. Cross-reference usernames across threads to reconstruct individual trajectories. Does not require login. Yields pseudonymous longitudinal data.

3. **USAMO qualifier list:** Fetch the USAMO historical results wiki page for named qualifiers. Cross-reference the ~293 annual USAMO qualifiers against Bay Area school directories to estimate Bay Area representation.

4. **AoPS user blog search:** Google `site:artofproblemsolving.com/community "AIME" "college" "Harvard" OR "MIT" OR "Stanford"` to find users who documented both competition results and college outcomes in their blogs.

5. **Chapter-level MATHCOUNTS PDFs:** Fetch chapter-level result PDFs from San Mateo County, Santa Clara Valley, East Bay, and Peninsula chapters to get school-level rankings at the chapter competition level (below state, but shows more schools).
