---
research_date: 2026-04-18
researcher: research-agent
purpose: Evaluate college newspaper and university-published sources for student K-12 trajectory narratives
topic_slug: bay-area-k-12-college-placement-statistics
reliability_tier_notes: |
  Sources evaluated below span L1-official (university-published), L2-authoritative (established student journalism),
  and L3-aggregator categories. Individual blog posts are L1-official when on mitadmissions.org.
  Freshman surveys are L2-authoritative (student journalism with editorial process).
---

# College Newspaper & University Profile Sources — K-12 Trajectory Research

Research question: Which college newspaper series and university-published sources contain
student profiles that describe individual K-12 trajectories (activities, competitions,
timelines, decisions) richly enough to be used as training signal or research evidence?

---

## 1. Harvard Crimson — "Fifteen Minutes" Magazine & Freshman Survey

### Fifteen Minutes (FM) Magazine
- URL: https://www.thecrimson.com/section/fm/
- Reliability tier: L2-authoritative
- Format: Long-form magazine published Thursdays; periodic glossy print editions

**What it covers:**
Fifteen Minutes primarily profiles Harvard faculty, visiting scholars, researchers, and
campus cultural phenomena. The "Fifteen Questions" interview format (e.g., Nobel laureate
Claudia Goldin, medieval historian Michael McCormick) focuses on current professional
work, not undergraduate backgrounds.

**K-12 trajectory content: None found.**
The magazine does not publish profiles of undergraduate freshmen describing their high
school journeys. Coverage focuses on accomplished professionals and campus culture.
An older feature series called "Fifteen Hottest Freshmen" was discontinued circa 2015.
The current magazine focuses on investigative journalism and faculty interviews.

**Scrapability:** HTML, well-structured. Archive searchable by issue date and tag.
Articles available at thecrimson.com/section/fm/ and thecrimson.com/topic/{date}/

**Volume:** Published weekly during academic year. Thousands of articles in archive
going back to at least the 1990s. Zero individual student K-12 trajectory profiles found.

---

### Harvard Crimson Freshman Survey (Annual)
- URL pattern: https://features.thecrimson.com/{year}/freshman-survey/
- Confirmed years: 2018 (Class of 2022) through 2025 (Class of 2029)
- Reliability tier: L2-authoritative

**What it covers:**
Annual survey of incoming Harvard freshmen covering demographics, academics, politics,
lifestyle, and extracurriculars. Published as interactive microsite plus narrative articles.
Survey participation: approximately 33–46% of each class.

**K-12 trajectory content: Aggregate statistics only.**
- High school type breakdown (public, private, religious, charter, home school)
- GPA distribution (Class of 2028: 37% reported 4.0/4.0; average 3.98)
- Student government leadership (>30% were student council president)
- Extracurricular participation rates: community service (71%), athletics (50%+), student government (50%+)
- Top 10 Popular High School Extracurriculars: identified as a data widget (Flourish chart)
  at https://www.thecrimson.com/widget/2024/12/5/top-10popular-high-school-extracurriculars/
  — full list not extractable via WebFetch (embedded in interactive chart)
- GPA by school type: public school students averaged 3.98 vs. private 3.96

**What it does NOT include:**
- Named individual students
- Specific high school names attended
- Individual competition achievements
- Activity timelines (when a student started an activity)
- Anything identifying which specific student did what

**Scrapability:** Interactive microsites (features.thecrimson.com) plus standard HTML
narrative articles. Chart data embedded in Flourish visualizations — not directly
parseable without JavaScript rendering.

**Value for K-12 trajectory research:** Moderate for aggregate benchmarks (what
fraction of Harvard admits were student council presidents, did community service,
played sports). Zero value for individual trajectories.

**Feeder schools data (separate investigation):**
- URL: https://interactives.thecrimson.com/2024/news/feeders
- Covers 15 years (2009 onward) of Harvard freshman register data
- Identifies 21 top feeder schools; school-level aggregate counts, not individual students
- Caveat: ~10% of each class does not submit to Freshman Register

---

## 2. Stanford Daily — Student Profiles

- URL: https://stanforddaily.com
- Reliability tier: L2-authoritative

**Search results:**
Three searches on site:stanforddaily.com for student profile content with K-12 trajectory
signals returned minimal relevant results:
- QuestBridge article (2020): brief mention of one student's background (first-gen, immigrant parents)
- Faculty profile (2025): Jonathan Gienapp, historian — not a student
- Community op-ed (2025): first-year student discussing identity education, no K-12 trajectory

**K-12 trajectory content: Minimal.**
Stanford Daily publishes standard student newspaper content (campus news, sports, arts,
opinion). No dedicated freshman profile series analogous to Harvard's Crimson survey
was identified. Individual student profiles that appear tend to focus on current campus
roles (elected officials, student leaders) without K-12 backstory.

**Volume of K-12 trajectory content found: Near zero.**

---

## 3. MIT — The Tech (Student Newspaper)

- URL: https://thetech.com
- Reliability tier: L2-authoritative

**What it covers:**
Standard student newspaper (MIT's oldest, published since 1881): news, opinion, arts,
sports, campus life. Publishes Thursdays during academic year, monthly in summer.

**K-12 trajectory content: Minimal.**

Two relevant series identified:

**"MIT Application Essays That Worked" series:**
- 6 articles covering admissions seasons 2013-14, 2014-15, 2016-17
- Publishes actual application essays from admitted students
- Essays are personal narratives that may contain K-12 activity descriptions
- Sample titles: "My love for people is the best part of myself," "Marching to a different beat," "Dancing after a double surgery"
- These are primary-source essay texts with the student's own words
- Volume: only 6 known published essays
- Scrapability: standard HTML at thetech.com/tags/mit-application-essays-that-worked

**"Frosh Files" personal essays:**
- Reflective first-person essays by MIT students
- Focus on college experiences, not pre-college backgrounds
- Example examined (Sept 2024): author is Class of '27, identifies background (Vietnamese-American,
  first-gen, low-income, queer) but gives no specific high school, activities, or competition data

**"First-Year Class Profile" (MIT Admissions official):**
- URL: https://mitadmissions.org/apply/process/profile/
- Class of 2029: 1,155 enrolled students
- High school type: public 68%, independent 15%, religious 8%, foreign 9%, homeschool 1%
- First-gen: 20%; Pell eligible: 27%; tuition-free: 45%
- Does NOT include: test scores, GPA, competition data, extracurriculars, individual profiles

**Value for K-12 trajectory research:** Low for The Tech overall. The "essays that worked"
series is the highest-signal content but only 6 essays exist.

---

## 4. MIT Admissions Blogs (mitadmissions.org/blogs)

- URL: https://mitadmissions.org/blogs/landing/
- URL: https://mitadmissions.org/blogs/bloggers/student-bloggers/
- Reliability tier: L1-official (MIT Admissions-sanctioned student bloggers)

**What it is:**
Active since 2004. Current cohort: 23 student bloggers (classes ranging from '25 through '29).
Bloggers are paid positions chosen competitively (63 applicants for 6 slots in one recent cycle).
Archive extends back to at least 2004 — "thousands of cumulative posts" estimated.

**K-12 trajectory content: HIGH — the richest source found in this investigation.**

The blog format is explicitly designed to give prospective students "an honest, accurate,
authentic picture of MIT" including the path to MIT. Many posts directly describe pre-college
trajectories.

**Confirmed examples with K-12 trajectory data:**

*"What I Did in High School" by Michelle G. '18 (July 20, 2015):*
- Attended a public science/engineering magnet school in New Jersey (entrance-exam required)
- GPA trajectory: freshman lowish A → junior solid A; self-studied 10 AP tests (mostly 5s)
- Sophomore: first place in tristate science fair (tomato plant / aspirin research)
- Competed in 15-20 video/science visualization contests; won approximately 11 awards
- Won NASA Aura Communications Contest, high school neuroscience video contest, U.S. Treasury video contest
- Summer: daycare job (sophomore), Rutgers University data analysis internship
- Co-founded Connect Four club; joined and quit NHS on principle
- URL: https://mitadmissions.org/blogs/entry/what-i-did-in-high-school/

*"Spring break Q&A: Part 2" by Jenny B. '25 MEng '26:*
- Grew up in Montgomery, Alabama; born in Atlanta
- Self-described as having "barely even known how to code before I came to MIT"
- Had not "won any international olympiads"
- Represents non-olympiad, non-elite-competition pathway to MIT
- URL: https://mitadmissions.org/blogs/entry/spring-break-qa-part-2/

*Additional posts with K-12 trajectory signals (from search results, not fully fetched):*
- "MIT Olympians, Part 2" by Matt McGann '00 — profiles MIT students who competed in
  international math/science olympiads; K-12 competition timelines described
- "Adventures in Math" by Matt McGann '00 — math competition background stories
- "Why I Took A Gap Year" by Vincent A. '17 — IMO participation, path to MIT
- "everyone knows each other" — describes ecosystem of competition math/physics/research kids
- "How to do everything wrong and still get into MIT" — non-traditional pathway story
- "High School Summer Research Programs" — lists research competition pathways (Intel STS, ISEF)

**Search query used:** site:mitadmissions.org "high school" "I started" "I competed" math olympiad research

**Scrapability:**
- Standard HTML pages; WebFetch works reliably on mitadmissions.org
- Each blog post has a clean URL: mitadmissions.org/blogs/entry/{slug}/
- No paywall, no login required
- Archives are browsable by blogger and date
- No structured metadata per post (must extract from narrative text)

**Volume estimate:**
- 23 current bloggers × multiple posts per semester = hundreds of active posts per year
- Archive since 2004 = estimated 2,000–5,000+ total posts
- Fraction with explicit K-12 trajectory data: unknown, but posts explicitly covering
  "what I did in high school" or "my path to MIT" appear regularly based on search results

**Time span:** 2004 to present (April 2026)

**Key limitation:**
Content is student-written and reflects individual bloggers' choices about disclosure.
Some posts have extensive K-12 detail (Michelle G.'s post is a textbook example);
others focus entirely on MIT campus life with zero pre-college content.

---

## 5. Yale Daily News — Freshman Survey & Coverage

- URL: https://yaledailynews.com
- Reliability tier: L2-authoritative

**What it covers:**
Yale Daily News publishes an annual freshman survey similar to Harvard's Crimson survey.
Class of 2028 survey: 541 respondents (from ~1,550 enrolled).

**K-12 trajectory content: Aggregate statistics only.**

From the Class of 2028 survey:
- 63% attended public high schools; 36% private schools (12% of those boarding)
- 57% graduated in top 5% of high school class
- Median SAT: 1,550 (among the 76%+ who submitted)
- Median ACT: 35
- Half of class were admitted to at least one other Ivy/Duke/MIT/Stanford
- 75% said Yale was first-choice school

**Yale Class of 2028 official profile:**
- URL: https://admissions.yale.edu/sites/default/files/classprofile2028web.pdf
- PDF format; WebFetch returned only the page framing it, not PDF content
- Likely contains aggregate statistics only (consistent with peer institutions)

**Individual student profiles: None found.**
No named individual student profiles with K-12 trajectory data were identified in Yale
Daily News search results.

---

## 6. Duke Chronicle — Freshman Survey

- URL: https://www.dukechronicle.com
- Reliability tier: L2-authoritative

**What it covers:**
The Chronicle publishes an annual first-year survey similar to Harvard's.

**K-12 trajectory content: Aggregate statistics only.**

From Class of 2027 and Class of 2028 surveys:
- 58% attended public non-charter high schools
- 25% attended private non-denominational schools
- 11% attended private religious schools; 5% public charter
- 36% hired college admissions counselors (Class of 2027)
- >17% had parents or siblings who attended Duke (legacy)
- 56% applied Early Decision
- 63% said Duke was first choice

The Class of 2028 survey (published August 2025) covers "paths to Duke, application
method, hometown, standardized testing, family income, counselor use, legacy status."
URL: https://dukechronicle.com/article/duke-chronicle-class-of-2028-first-year-survey-paths-to-duke-...
(Note: direct URL returned 403)

**Individual student profiles: None found.**

---

## 7. University "Meet Our Students" Pages — Official Admissions

**Search result:** No significant dedicated student K-12 trajectory spotlight pages
were identified through search for Stanford Engineering, MIT departmental, or similar
official pages. Most university "meet our students" content is either:
- Generic marketing copy without specific K-12 details
- Faculty/researcher spotlights, not undergraduate student profiles
- Admissions statistics pages (aggregate)

The closest found: MIT's mitadmissions.org blogs (covered above as item 4).

---

## Summary Comparison Table

| Source | Format | K-12 Trajectory Depth | Individual Profiles? | Volume of Trajectory Posts | Archive Depth | Scrapability |
|--------|--------|----------------------|---------------------|---------------------------|---------------|--------------|
| Harvard Crimson Freshman Survey | Aggregate data + charts | Low (activity categories, no names) | No | 1 survey/year, 8+ years | 2018–present | Medium (Flourish charts opaque) |
| Harvard Crimson FM Magazine | Long-form journalism | None (faculty/scholar focus) | No | 0 | 1990s–present | Good (clean HTML) |
| Harvard Crimson Feeder Schools | Aggregate by school | None (school-level counts) | No | 1 interactive (2024) | 15-year data | Medium |
| MIT Admissions Blogs | Personal blog posts | High (some posts are full K-12 narratives) | Yes (by name/class year) | Est. 2,000–5,000+ total; many with trajectory info | 2004–present | Good (clean HTML) |
| The Tech MIT Application Essays | Actual application essays | Medium (depends on essay topic) | Pseudonymous/named | 6 essays, 3 years | 2013–2017 | Good (clean HTML) |
| The Tech Frosh Files | Personal essays | Low (college-focused, not K-12) | Yes (name + class year) | Ongoing | 2024–present | Good |
| Stanford Daily | Student newspaper | Near zero | No | ~0 | 2000s–present | Good |
| Yale Daily News Freshman Survey | Aggregate data | Low (categories, no names) | No | 1 survey/year | 2020–present | Good |
| Duke Chronicle Freshman Survey | Aggregate data | Low (categories, no names) | No | 1 survey/year | 2023–present | Medium (403 on some URLs) |
| MIT official class profile | Aggregate PDF | Very low (school type only) | No | 1/year | Unknown | Medium |

---

## Findings and Recommendations

### Best source: MIT Admissions Blogs (mitadmissions.org/blogs)

The MIT Admissions blog is the single richest identified source of individual student
K-12 trajectory narratives. Key characteristics:

1. **Two-decade archive (2004–present)** with estimated 2,000–5,000+ posts
2. **Named students by class year** (e.g., Michelle G. '18, Jenny B. '25)
3. **Some posts are explicit K-12 timelines** — listing activities, competitions,
   GPA trajectories, summer programs, internships by year of high school
4. **Range of profiles** — from olympiad competitors (IMO, ISEF) to non-traditional
   students who "barely knew how to code before MIT"
5. **Clean HTML, no paywall** — directly scrapable via WebFetch
6. **MIT Admissions-sanctioned** — L1-official reliability tier

**Limitation:** Not all posts discuss K-12 background; must identify relevant posts
through search or archive browsing. No structured metadata per post.

### Second-best: Harvard Crimson Freshman Survey (aggregate benchmarks)

The annual Crimson freshman survey provides useful aggregate benchmarks on what fraction
of Harvard admits participated in various extracurricular categories. Useful for
establishing base rates, but cannot be used to construct individual trajectories.

Available at features.thecrimson.com/{year}/freshman-survey/ for classes 2022–2029.

### Third: The Tech "MIT Application Essays That Worked"

Only 6 essays published (2013–2017), but these are verbatim application essays from
admitted students — the most direct window into how admitted students narrated their
own K-12 trajectories in the admissions process itself.

URL: https://thetech.com/tags/mit-application-essays-that-worked

### Not useful for individual trajectory research:
- Harvard Crimson Fifteen Minutes: faculty/scholar focus, no student K-12 profiles
- Stanford Daily: no systematic student profile series found
- Yale Daily News: aggregate surveys only
- Duke Chronicle: aggregate surveys only
- University "meet our students" pages: generic marketing, no K-12 specificity

---

## Recommended Next Steps

1. **Crawl MIT Admissions blog archive** for posts tagged with pre-MIT or high school content.
   The mitadmissions.org/blogs/entry/ URL structure is consistent; a crawler could
   retrieve all posts and filter by those containing "high school," "competition,"
   "olympiad," "research," "intern" etc.

2. **Retrieve all 6 Tech application essays** at thetech.com/tags/mit-application-essays-that-worked
   and extract K-12 trajectory details from each.

3. **Retrieve Harvard Crimson freshman survey data** for classes 2022–2029 for aggregate
   benchmarks on extracurricular participation rates.

4. **Identify MIT Admissions blog posts** with explicit K-12 content using these confirmed
   posts as seeds:
   - https://mitadmissions.org/blogs/entry/what-i-did-in-high-school/ (Michelle G. '18)
   - https://mitadmissions.org/blogs/entry/spring-break-qa-part-2/ (Jenny B. '25)
   - https://mitadmissions.org/blogs/entry/mit_olympians_part_2/ (Matt McGann '00)
   - https://mitadmissions.org/blogs/entry/why-i-took-a-gap-year/ (Vincent A. '17)
   - https://mitadmissions.org/blogs/entry/how_to_do_everything_wrong_and/ (non-trad pathway)
   - https://mitadmissions.org/blogs/entry/everyone-knows-each-other/ (competition ecosystem)

---

## Search Queries Run (Deduplication Log)

| Query | Results | Action |
|-------|---------|--------|
| site:thecrimson.com "15 questions" "high school" student profile | 2 results | No individual student profiles found |
| thecrimson.com "fifteen minutes" freshman profile student background high school | 10 results | FM focuses on faculty/scholars, not students |
| site:thecrimson.com freshman profile "high school" "grew up" 2024 2025 | 2 results | No individual student K-12 profiles |
| site:blogs.mit.edu "high school" "how I got here" student journey K-12 | 0 results | Wrong domain; correct is mitadmissions.org |
| blogs.mit.edu student blogger "high school" admissions journey path MIT | 10 results | Found mitadmissions.org structure; 23 current bloggers |
| site:mitadmissions.org blogs "high school" "I started" "I competed" OR "math olympiad" | 10 results | Found trajectory-rich posts; key seeds identified |
| site:stanforddaily.com student profile "high school" "before Stanford" | 3 results | Near zero K-12 trajectory content |
| site:yaledailynews.com student feature profile freshman class 2024 2025 | 10 results | Aggregate stats only |
| site:dukechronicle.com student profile freshman "high school" 2024 2025 | 10 results | Aggregate surveys only |
| Harvard Crimson freshman survey 2024 2025 "class of 2028" extracurriculars | 10 results | Aggregate data; top 10 extracurriculars chart found but not parseable |
| Harvard class 2028 freshman survey top 10 extracurriculars list | 10 results | Confirmed community service #1 (71%), athletics + student govt >50% each |
| university admissions "meet our students" engineering profile "high school" | 0 relevant | No useful individual student pages found |
| MIT admissions blogs "my high school" OR "in high school I" personal narrative | 10 results | Several relevant posts identified |
| MIT admissions blogs archive 2004 2024 student trajectory "before I came to MIT" | 1 result | Jenny B. '25 post with Montgomery AL background |
| thecrimson.com "freshman survey" "class of 2028" extracurricular activities sports | 10 results | Aggregate data articles; top 10 chart found as widget URL |
| features.thecrimson.com "class of 2028" "top 10" extracurriculars high school | 10 results | Widget URL confirmed; Flourish chart not directly parseable |

---

## Raw Fetches Performed

| URL | Method | Status | Relevant Content |
|-----|--------|--------|-----------------|
| https://mitadmissions.org/blogs/bloggers/student-bloggers/ | WebFetch | OK | 23 current bloggers listed with class years and concentrations |
| https://features.thecrimson.com/2023/freshman-survey/ | WebFetch | OK | Aggregate statistics only; no individual profiles |
| https://mitadmissions.org/blogs/landing/ | WebFetch | OK | Archive back to 2004; focus on MIT campus life |
| https://mitadmissions.org/blogs/entry/what-i-did-in-high-school/ | WebFetch | OK (2x) | RICH: full K-12 trajectory, Michelle G. '18 |
| https://mitadmissions.org/blogs/entry/admissions_advice_from_someone/ | WebFetch | OK | Admissions philosophy; minimal personal K-12 detail |
| https://www.thecrimson.com/topic/04-20-2024/ | WebFetch | OK | FM magazine; faculty/scholar profiles only |
| https://www.thecrimson.com/section/fm/ | WebFetch | OK | FM section; no student K-12 profiles |
| https://www.thecrimson.com/article/2024/12/5/freshman-survey-2028-academics/ | WebFetch | OK | Aggregate: GPA, extracurriculars, athlete scores |
| https://www.thecrimson.com/tag/freshmen/ | WebFetch | OK | No individual student K-12 profiles in coverage |
| https://thetech.com/ | WebFetch | OK | Frosh Files column; Meet the Minds (faculty); no K-12 profiles |
| https://thetech.com/tags/mit-application-essays-that-worked | WebFetch | OK | 6 essays; 2013-14, 2014-15, 2016-17 seasons |
| https://thetech.com/2024/09/05/sixpence-seven | WebFetch | OK | Class of '27; no specific K-12 data |
| https://mitadmissions.org/apply/process/profile/ | WebFetch | OK | Aggregate class profile; high school type breakdown only |
| https://mitadmissions.org/blogs/entry/spring-break-qa-part-2/ | WebFetch | OK | Jenny B. '25; Montgomery AL; non-olympiad pathway |
| https://www.thecrimson.com/widget/2024/12/5/top-10popular-high-school-extracurriculars/ | WebFetch | OK (partial) | Flourish chart; full list not extractable |
| https://interactives.thecrimson.com/2024/news/feeders | WebFetch | OK | 15-year feeder school aggregate data; no individual names |
| https://harvardindependent.com/meet-the-class-of-2028/ | WebFetch | OK | Aggregate racial/ethnic stats only |
| https://mitadmissions.org/blogs/entry/high-school-summer-research-programs/ | WebFetch | OK | Resource list; informal; no individual trajectory |
| https://admissions.yale.edu/sites/default/files/classprofile2028web.pdf | WebFetch | Failed (PDF not parsed) | Yale official class profile; aggregate |
| https://dukechronicle.com/article/duke-chronicle-class-of-2028-... | WebFetch | 403 | Duke Chronicle Class of 2028 survey |
| https://borderless.so/stories/how-math-competitions-led-me-to-study-math-and-computer-science-at-mit | WebFetch | 429 (rate limited) | Could not retrieve |
| https://issuu.com/theharvardcrimson/docs/glossy_4_revised_28 | WebFetch | 404 | October 2024 FM glossy not accessible |
