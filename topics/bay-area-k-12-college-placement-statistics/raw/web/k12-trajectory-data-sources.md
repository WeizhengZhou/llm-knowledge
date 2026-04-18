---
created: 2026-04-18
purpose: Source inventory for K-12 student trajectory data — decisions, timing, activity arcs from elementary through college admission
researcher: research-agent
---

# K-12 Student Trajectory Data Sources: Inventory and Access Guide

This document maps all investigated sources for student trajectory data showing WHEN students made decisions — when they entered competitions, added/dropped activities, built projects — not just final college placement stats.

---

## 1. Math Competition Results by School

### 1A. AMC/AIME School-Level Results — MAA

**Primary URL:** https://amc-reg.maa.org/reports/generalreports.aspx

**What is available:**
- School-level team scores (sum of top 3 student scores per school)
- School Honor Roll (team score ≥ 400 on AMC 10 or AMC 12 top 3 students)
- School Merit Roll (team score 300-399)
- Score distribution charts and summary statistics
- Individual student qualification notifications (sent to schools)

**What is NOT publicly available:**
- A downloadable list of school names on the honor/merit roll is not published as a public-facing document. The reporting portal (EduVistas system) is accessible to competition managers and registered schools, not the general public.
- No publicly searchable database of "which schools produced how many AIME qualifiers" in a given year exists on the MAA site.
- AIME qualifier names are not published by MAA on a per-school public list.

**Time span:** Current year + some historical. No confirmed multi-year archive of school-level data.

**Scrapable/downloadable:** No. Portal requires school-level login.

**Data points:** Aggregate school team scores only; no individual student names in public view.

**Key finding:** The MAA does NOT publish a public list of school names with AIME qualifier counts. Individual tutoring centers (Ivy League Education Center, Think Academy) self-publish their own student results, but there is no authoritative public aggregation.

**Reliability tier:** L1-official (for what they do publish); data completeness is low for the trajectory research use case.

---

### 1B. USAMO / USAJMO Qualifier Lists — MAA via AoPS

**Primary URLs:**
- 2022 USAMO Qualifiers PDF: https://services.artofproblemsolving.com/download.php?id=YXR0YWNobWVudHMvYy8wLzZjMjhjYTFiODUwNzBjNzY2YzIzN2E2OGJmZmI5YjlhZWNhMjA1LnBkZg%3D%3D&rn=MjAyMiBVU0FNTyBRdWFsaWZpZXJzLnBkZg%3D%3D
- 2022 USAJMO Qualifiers on Scribd: https://www.scribd.com/document/584888830/2022-USAJMO-Qualifiers
- 2024 USAMO Awardees PDF: https://maa.org/wp-content/uploads/2024/11/2024-USAMO-Awardees-FINAL.pdf
- 2021 USAMO Qualifiers (College Sidekick): https://www.collegesidekick.com/study-docs/14711573
- USAMO Wikipedia with school mentions: https://en.wikipedia.org/wiki/United_States_of_America_Mathematical_Olympiad

**What is available:**
- Annual qualifier lists in PDF format: first initial, last name, school name, school state
- These lists exist and are linkable/downloadable for at least 2021, 2022; 2024 awardees list confirmed at maa.org
- AoPS forum threads host links to these PDFs when MAA releases them
- Scribd hosts several years' qualifier lists as searchable documents

**What is NOT available:**
- The 2024 full qualifier list (as opposed to awardees-only) was not confirmed as a public direct download link
- No single archive page consolidates all years' qualifier PDFs
- Lists show first initial + last name only (not full first name), limiting individual identification

**Time span:** Confirmed availability: 2021, 2022 qualifier lists; 2024 awardees list. Earlier years likely exist but require hunting AoPS forum threads year-by-year.

**Scrapable/downloadable:** Yes, PDFs are directly downloadable when URL is known. The format is image-encoded PDF (not text-layer), meaning OCR would be needed for bulk extraction.

**Data points per entry:** First initial, last name, school name, school state. Approximately 250-500 qualifiers per year (USAMO ~250-300; USAJMO ~200-250).

**Trajectory value:** MEDIUM. Tells you which schools produced USAMO/USAJMO qualifiers in a given year, but does not tell you WHEN the student started their math journey or their developmental arc.

**Reliability tier:** L1-official

---

### 1C. AMC Historical Results — AoPS Wiki

**URL:** https://artofproblemsolving.com/wiki/index.php/AMC_historical_results

**What is available:**
- Historical cutoff scores, participation numbers, and competition statistics by year
- Not school-level data — aggregate national statistics only
- Wiki page links to individual year pages with problem sets

**What is NOT available:**
- No school-by-school breakdown of qualifiers
- No individual student records

**Reliability tier:** L3-aggregator (community-maintained wiki)

---

### 1D. AoPS Community Forum — Indirect School-Level Intelligence

**URL:** https://artofproblemsolving.com/community/

**What is available:**
- Forum threads where students and parents self-report scores, competition results, school affiliations
- Threads about which prep schools/programs produced AIME qualifiers
- Individual student "journey" posts (e.g., "A Culmination of 13+ Years: AIME Qualification" thread at artofproblemsolving.com/community/c2409693h2979272)
- These posts often describe WHEN a student started competing (grade level), which competitions they entered each year, how their trajectory evolved

**Trajectory value:** HIGH for individual case studies. AoPS users frequently narrate their multi-year competition journey in detail — "I started AMC 8 in 5th grade, moved to AMC 10 in 7th..." These are self-reported but detailed.

**Scrapable:** Yes, forum is publicly readable without login. Requires keyword search within forum.

**Data points:** Highly variable; qualitative narratives, not structured data.

**Reliability tier:** L4-community

---

### 1E. MATHCOUNTS Historical Results — AoPS Wiki + State Organizations

**URL:** https://artofproblemsolving.com/wiki/index.php/MATHCOUNTS_historical_results

**State-level archives (examples):**
- Pennsylvania: https://www.pspe.org/pspe-events/mathcounts/mathcounts-archive/
- Minnesota: https://mathcountsmn.org/state-competition-history/
- California: https://cspeef.org/

**What is available:**
- State championship results going back to ~2007 for states that maintain archives
- Team results include school names
- Individual winner names included at state and national level
- AoPS wiki page aggregates national-level results historically

**Time span:** 2007-2025 for well-maintained state archives; national results back to 1980s on AoPS wiki.

**Trajectory value:** MEDIUM-HIGH. MATHCOUNTS is a middle school competition (grades 6-8), so results tell you which schools had strong 6th-8th grade math students. Combined with later AIME/USAMO data, this begins to reconstruct developmental arcs across the middle-to-high school transition.

**Scrapable/downloadable:** Varies by state. Some states publish PDFs, some HTML tables. No unified national school-level download.

**Reliability tier:** L1-official (official state organization sites); L3-aggregator (AoPS wiki)

---

## 2. Science Olympiad Results

### 2A. Duosmium — Science Olympiad Results Archive

**Primary URL:** https://www.duosmium.org/results/

**By School:** https://www.duosmium.org/results/schools/y/

**By Season:** https://www.duosmium.org/results/all/

**GitHub source:** https://github.com/Duosmium/duosmium

**What is available:**
- 3,809 total tournaments indexed (as of 2026): 67 national, 1,110 state, 1,399 regional, 1,233 invitational
- Results organized by school — can search a specific school and see all their tournament placements across all years
- Results organized by season (year)
- Tournament-level CSV downloads confirmed (includes school name, team name, school city, school state, placement)
- School search bar for browsing individual school history
- Time span confirmed: 1986 through 2026 (40+ years for some schools)

**What is NOT available:**
- Individual student names are generally not listed (teams compete, not named individuals)
- No cross-tournament "career arc" view for a single student

**Trajectory value:** HIGH for school-level trajectories. Can see how a school's Science Olympiad program built from regional competitor to national finalist over a decade. Combined with school roster data, provides strong school-level developmental signal. LOW for individual student arcs.

**Scrapable/downloadable:** YES. CSV download available per tournament. GitHub repository contains underlying data in SciolyFF format (open source). This is the most machine-readable science competition dataset found in this research.

**Data points:** School name, city, state, tournament placement (rank), event-level scores, year. Thousands of schools represented.

**Reliability tier:** L2-authoritative (open-source community project with verified tournament data)

---

### 2B. Scilympiad Archive

**URL:** https://scilympiad.com/public/Archive/Results

**What is available:**
- Archive of past tournament results hosted on the Scilympiad scoring platform
- Complement to Duosmium; some tournaments use Scilympiad that are not in Duosmium

**Reliability tier:** L2-authoritative

---

## 3. Regeneron / Intel Science Talent Search

### 3A. Regeneron STS — Society for Science

**Primary URL:** https://www.societyforscience.org/regeneron-sts/

**2025 Scholars page:** https://www.societyforscience.org/regeneron-sts/2025-scholars/

**2024 Finalists:** https://www.societyforscience.org/regeneron-sts/2024-student-finalists/

**2025 Finalists PDF:** https://sspcdn.blob.core.windows.net/files/Documents/SEP/STS/2025/Program-Books/Finalists.pdf

**What is available:**
- Annual list of Top 300 Scholars (semifinalists) with student name, age, school name, state, research project title
- Annual list of Top 40 Finalists with same fields
- Coverage: 2025 confirmed; 2024, 2023, 2022 linked from main page; older years require navigation
- 2026 Scholars list confirmed accessible (300 scholars from 206 American and international high schools in 35 states)
- PDF program books available for finalist class each year

**What is NOT available:**
- No CSV download — only web pages and PDF program books
- Full first name + last name available (unlike USAMO which uses first initial only)
- No K-12 backstory or timeline of research development in the scholars list itself
- No indication of what grade the student began their research project

**Time span:** 2022-2026 confirmed accessible from main page; Wikipedia page covers history back to 1942 (formerly Westinghouse STS 1942-1997, then Intel STS 1998-2016, then Regeneron STS 2017-present)

**Scrapable:** Yes, the scholars list page is readable HTML. 300 entries per year with school names. Approximately 5 years of recent data easily accessible = ~1,500 scholar profiles with school affiliation.

**Trajectory value:** MEDIUM. Identifies which high schools produce top science research students. Does NOT show developmental arc (when student started research, what grade). Finalist program books have brief bios but not systematic timeline data.

**Reliability tier:** L1-official

---

### 3B. Regeneron ISEF — International Science and Engineering Fair

**Primary URL:** https://www.societyforscience.org/isef/

**Project database:** https://partner.projectboard.world/isef (redirect from projectboard.world/isef)

**What is available:**
- Searchable database of abstracts from 2014 to 2025
- Project title, student name, school name, school city, school state, award information
- Approximately thousands of finalists per year (ISEF selects ~1,800 students annually from regional competitions)
- Sortable finalist list by column headers

**What is NOT available:**
- No CSV download confirmed
- No developmental backstory for individual students
- Regional fair results that feed into ISEF are maintained separately by each regional fair

**Time span:** 2014-2025 confirmed in project database; 2026 finalists listed at https://finalistquestionnaire.societyforscience.org/projectlist

**Trajectory value:** LOW-MEDIUM for individual trajectory (no timeline), HIGH for identifying which schools consistently send students to ISEF.

**Scrapable:** Partially — web interface is readable but may require pagination.

**Reliability tier:** L1-official

---

## 4. College Newspaper Freshman Surveys

### 4A. Harvard Crimson Freshman Survey

**URL pattern:** https://features.thecrimson.com/{YYYY}/freshman-survey/

**Available years:**
- Class of 2018 (2014 survey): https://features.thecrimson.com/2014/freshman-survey/
- Class of 2019 (2015): https://features.thecrimson.com/2015/freshman-survey/
- Class of 2020 (2016): https://features.thecrimson.com/2016/freshman-survey/
- Class of 2021 (2017): https://features.thecrimson.com/2017/freshman-survey/
- Class of 2022 (2018): https://features.thecrimson.com/2018/freshman-survey/
- Class of 2023 (2019): https://features.thecrimson.com/2019/freshman-survey/
- Class of 2024 (2020): https://features.thecrimson.com/2020/freshman-survey/
- Class of 2025 (2021): https://features.thecrimson.com/2021/freshman-survey/
- Class of 2027 (2023): https://features.thecrimson.com/2023/freshman-survey/ [Class of 2026 survey was NOT published]
- Class of 2025 senior survey (2025): https://features.thecrimson.com/2025/senior-survey/

**What is available:**
- Extracurricular participation rates (% who participated in athletics, math clubs, science clubs, community service, music, student government)
- Leadership rates (% who held leadership positions)
- Demographic breakdown
- Academic data

**What is NOT available:**
- Data on WHEN students started activities (no "what grade did you begin X" question surfaced in any year's published results)
- Individual student profiles
- No per-school breakdown
- Aggregate data only; approximately 45-65% survey response rate among incoming freshmen

**Key data found:** Class of 2025: athletics 44.2%, math clubs 21.5%, science clubs 26.3%, music 23.2%; Class of 2023: athletics 57%, math clubs 32%, science clubs 32%, community service 74%.

**Trajectory value:** LOW for individual trajectory; useful for aggregate "what Harvard freshmen did in high school" benchmarking. Does NOT capture when activities began in K-12.

**Scrapable:** Yes, pages are standard HTML with interactive charts.

**Data points:** Aggregate percentages across ~700-1,000 respondents per year. Individual-level data not published.

**Language:** English

**Reliability tier:** L2-authoritative

---

### 4B. Yale Daily News Class Profile

**URL:** https://yaledailynews.com/blog/2024/08/30/data-the-class-of-2028-in-numbers/

**What is available:**
- Demographic composition (race, school type attended, class rank)
- Class of 2028: 63% public high school, 36% private, 12% boarding school
- 57% graduated in top 5% of high school class

**What is NOT available (confirmed via search):**
- No detailed extracurricular timing data
- Less comprehensive than Harvard Crimson survey; more demographic focus

**Trajectory value:** LOW for activity timing data.

**Reliability tier:** L2-authoritative

---

### 4C. Stanford Daily

**URL:** https://stanforddaily.com/

**Status:** No equivalent structured freshman/class survey data series found comparable to the Harvard Crimson annual survey. Stanford Daily publishes individual articles about admissions data but not a systematic multi-section annual survey. Stanford students do publish YouTube channels (e.g., The Kath Path, Arpi Park's channel) with admissions advice content, but these are individual, not systematic.

---

## 5. Chinese Parent Forums and Communities

### 5A. 文学城 (Wenxuecity) — 子女教育 and 名校|爬藤 Forums

**URL:** https://bbs.wenxuecity.com/znjy/ and https://bbs.wenxuecity.com/eliteuniversity/

**What is available:**
- Long-form narrative posts by Chinese-American parents documenting their children's K-12-to-college journey
- Some posts span multiple years of observation; parents return to update threads
- Topics include: college application outcome shares, EC strategy debates, school selection, competition prep
- Representative threads found:
  - "分享一下去年我儿子申请大学的经历" (Sharing my son's college application experience): https://bbs.wenxuecity.com/znjy/7689488.html
  - "子女上名校，父母谈心得" (Parents of top college students share insights): https://bbs.wenxuecity.com/eliteuniversity/5533466.html
  - "升学结束了，谈谈感想" (Application season over, reflections): https://bbs.wenxuecity.com/znjy/7374752.html

**What is NOT available:**
- Content quality is highly variable. Direct review of the 分享我儿子 thread showed the parent narrated the application process with minimal specific activity timeline — "besides sailing, there's not much else" without grade-level detail.
- Most posts are outcome-focused (college result + general impressions), not development-arc focused (when did child start X in 4th grade).
- No structured data — all qualitative narrative, reader must extract timeline manually.

**Language:** Chinese (Simplified)

**Trajectory value:** LOW-MEDIUM. Better threads do exist (parents who systematically planned and now document 8-10 year arcs), but these are rare and require search within the forum. Most posts discuss the senior year application experience.

**Scrapable:** Pages are publicly accessible HTML without login.

**Reliability tier:** L4-community

---

### 5B. 一亩三分地 (1point3acres) — 为人父母 Section

**URL:** https://www.1point3acres.com/bbs/

**Relevant section:** 为人父母 (parenting)

**What is available:**
- Discussions on K-12 education in the US, competition preparation, school selection
- Primary audience is Chinese graduate students and professionals in the US; parenting section is secondary to the graduate admissions focus
- Thread found: "美国K12教育这么不堪吗？" (Is American K-12 education really this bad?)

**What is NOT available:**
- 一亩三分地's core strength is graduate school admissions data, not K-12 trajectory documentation
- The parenting section is smaller and less active than Wenxuecity's 子女教育 forum
- No structured K-12 timeline data

**Language:** Chinese (Simplified)

**Trajectory value:** LOW for detailed K-12 trajectory data specifically.

**Reliability tier:** L4-community

---

### 5C. 未名空间 MITBBS — 湾区家长俱乐部 (SF Parents Club) + afterschool_k12

**URLs:**
- 湾区家长俱乐部: http://www.mitbbs.com/club_bbsdoc/SFparents.html
- afterschool_k12 club: http://www.mitbbs.com/clubarticle_t/afterschool_k12/

**What is available:**
- Bay Area-specific Chinese parent community
- Topics include: preschool selection, piano/instrument learning, reading programs (RAZ-Kids), self-control development
- Geographically relevant to Bay Area specifically

**What is NOT available:**
- Content is dated; MITBBS activity has declined significantly compared to peak years (2010-2018)
- No systematic competition trajectory threads found in search results
- More focused on early childhood (K-5) than high school competition trajectory

**Language:** Chinese (Simplified)

**Trajectory value:** LOW. Active era has passed; better Bay Area Chinese parent discussion has moved to WeChat groups (not publicly indexed) and 文学城.

**Reliability tier:** L4-community

---

### 5D. 小红书 (Xiaohongshu / RedNote) — 爬藤 Content

**URL:** https://www.xiaohongshu.com/explore

**What is available:**
- Active platform with "爬藤" (ivy league) content from Chinese parents and students
- Mix of authentic experience shares and commercially motivated educational consulting content
- Video and image format posts make systematic extraction difficult

**Critical caveat identified:** Multiple sources flag Xiaohongshu's 爬藤 content as heavily polluted with fabricated credentials (documented case of fake Harvard SEAS graduate running paid consulting). Thepaper.cn documented a case of a parent paying 10,000+ RMB to a "Harvard 学姐" who fabricated credentials.

**What is NOT available:**
- No public API or scraping without account
- Content is not indexable by standard web search in most cases
- Authenticity verification is difficult

**Language:** Chinese (Simplified)

**Trajectory value:** LOW-MEDIUM. Authentic posts from actual families can contain rich developmental narrative. Commercial/fake posts are indistinguishable without manual vetting.

**Reliability tier:** L4-community (with significant L5-low-signal contamination)

---

### 5E. FindingSchool (findingschool.com) — Chinese College Counseling Platform

**URL:** https://www.findingschool.com/cn/

**Relevant content found:** https://www.findingschool.com/cn/columnist/3998

"ED录取哥伦比亚大学，梦想照进现实，我女儿的爬藤之路！" (ED admitted to Columbia — my daughter's ivy journey)

**Access issue:** The URL returned HTTP 403. Content not retrievable.

**What would be available if accessible:**
- Narrative accounts of K-12 journey written by parents for a Chinese-American audience
- Platform features structured content from experienced parents/counselors
- More editorial vetting than MITBBS or free forum posts

**Reliability tier:** L3-aggregator if editorially reviewed; L4-community if user-submitted

---

## 6. Published Essay and Profile Books

### 6A. "50 Successful Harvard Application Essays" — Harvard Crimson Staff

**Amazon listings:**
- 6th Edition (most recent): https://www.amazon.com/Successful-Harvard-Application-Essays-6th/dp/1250889723
- 5th Edition: https://www.amazon.com/50-Successful-Harvard-Application-Essays/dp/1250127556

**What is available:**
- 50 student essays per edition with brief student profiles
- Profiles include: GPA, test scores, extracurricular activities, awards
- Essays reveal what activities the student cared about and often reference when they started
- Multiple editions cover different years (1st edition ~2000; 6th edition ~2023)

**What is NOT available:**
- Profiles are brief — typically 3-5 lines of stats, not a full K-12 timeline
- No structured "what grade did you start X" field
- No way to determine which activities were started in elementary vs. middle school without reading individual essay content carefully

**Companion book:** "How They Got into Harvard" (same publisher) — 50 applicants share 8 key strategies; each includes test scores, GPA, ECs, awards, family background. https://www.amazon.com/How-They-Got-into-Harvard/dp/0312343752

**Trajectory value:** MEDIUM. Essays often contain narrative evidence of when activities started ("I first picked up a violin at age 7...") but this must be extracted manually from 50 essays per edition. 6 editions exist = potentially 300 essay profiles, though overlap between editions is possible.

**Language:** English

**Reliability tier:** L2-authoritative (published, edited, attributed to real students)

---

## 7. Video / Podcast / Multi-Year Documentary Sources

### 7A. "Try Harder!" — Documentary Film (PBS/Sundance 2021)

**URL:** https://www.pbs.org/video/dream-school-a-journey-to-higher-ed-uw8zuz/ (related PBS doc)

**Try Harder! specific:**
- Premiered Sundance 2021; broadcast on PBS Independent Lens spring 2022
- Director Debbie Lum follows 5 seniors at San Francisco's Lowell High School through senior year application process
- Reference: https://calhum.org/try-harder-director-interview/

**What is available:**
- Qualitative narrative following real students through college admissions process
- Bay Area–specific (Lowell High, San Francisco — a selective public high school)
- Documents activities, pressures, decisions in real time over ~1 year

**What is NOT available:**
- Covers only senior year, not elementary/middle school origins of activities
- 5 students only — not a statistical dataset
- Film is not downloadable as structured data

**Trajectory value:** LOW for systematic data, HIGH for qualitative context about Asian-American student pressure dynamics in Bay Area specifically.

**Language:** English

---

### 7B. YouTube "College Application Journey" / "How I Got In" Channels

**Representative example found:** https://m.youtube.com/watch?v=HXLmRp1w3DA ("How I Got Into Harvard, Stanford, UPenn + More!")

**What is available:**
- Individual students narrate their application journey, often including what they did in high school and sometimes middle school
- Decision reaction compilations exist
- Stanford students have created named channels (The Kath Path, Arpi Park's channel) per Stanford Daily

**What is NOT available:**
- No systematic collection; highly fragmented
- Videos typically cover junior/senior year, not full K-12 arc
- Quality and detail vary enormously; most are highlight reels not developmental histories
- No machine-readable structured data

**Trajectory value:** LOW for systematic research; LOW-MEDIUM for qualitative examples of "what a Harvard-admitted student did."

---

### 7C. "Dream School: A Journey to Higher Ed" — WGCU/PBS Documentary

**URL:** https://www.pbs.org/video/dream-school-a-journey-to-higher-ed-uw8zuz/

**What is available:**
- Follows 6 high school students working toward top college admission
- Richer than individual YouTube videos; documentary production quality

**Trajectory value:** LOW for systematic data; qualitative only.

---

## 8. Parent Blogs Documenting K-12 Journeys

**What was found:**

Dedicated parent blogs on Medium or Substack documenting a child's multi-year competitive academic journey (AMC → AIME, Science Olympiad progression, project development year by year) do exist but are fragmented and hard to find via web search. Search results for "parent blog raising gifted child K-12 AMC AIME" returned predominantly tutoring center marketing content (Think Academy, AlphaStar, Random Math) rather than authentic parent narratives.

**Known examples of this genre (not individually retrieved but search-confirmed):**
- "Her STEM Journey" blog (herstemjourney.com): AMC/AIME problem explanation videos — appears to be a parent-run educational resource
- Random Math blog (randommath.com/blogs) — written by competitive math center, not a parent documenting one child's journey, but discusses the "applying sideways" phenomenon and HYPSM dynamics with data
- AoPS forum individual posts documenting personal journeys (mentioned above in 1D)

**Key structural problem:** True multi-year parent blogs documenting a child's development from elementary school through college admission are rare and typically:
1. Written by parents who realized retrospectively they had interesting data, not prospectively tracking
2. Often in Chinese (WeChat accounts, Weibo) and not publicly indexed
3. Short-lived — blogs abandoned when the child's process concludes

**Trajectory value:** HIGH when found; LOW probability of systematic coverage.

---

## 9. Reddit r/ApplyingToCollege and r/ChanceMe

**URL:** https://www.reddit.com/r/ApplyingToCollege/ and https://www.reddit.com/r/chanceme/

**What is available:**
- r/ChanceMe posts include student self-reported profiles: GPA, test scores, activities list with years of participation, awards, intended major
- Common App activities section requires students to list grades of participation — these are often transcribed into chance-me posts
- Posts include statements like "Science Olympiad (9, 10, 11, 12), AMC (9, 10, 11)" indicating grade-level start
- The subreddit grew exponentially from the 2017-2018 cycle; large post volume since 2018
- Individual student posts in r/collegeresults subreddit (already partially collected in this project at `/data/student_profiles/raw/reddit/collegeresults/`) sometimes include full activity lists with grade ranges

**What is available from existing project data:**
- This project already has ~30 Reddit r/collegeresults posts collected under `/data/student_profiles/raw/reddit/collegeresults/`
- These posts often include activity lists but the grade-of-start data depends on how much detail each poster shares

**Trajectory value:** MEDIUM-HIGH. Grade ranges on activities (e.g., "started Science Olympiad in 9th grade") are frequently included in chance-me and results posts. This is the closest thing to machine-readable K-12 trajectory data from individual students at scale. Hundreds of thousands of posts since 2018.

**Scrapable:** Reddit's Pushshift archive (now access-restricted) formerly allowed bulk download. Reddit API (paid tier) allows current access. Manual browsing is free.

**Language:** English

**Reliability tier:** L4-community

---

## Summary Comparison Table

| Source | Type | School-Level? | Individual-Level? | Timing/Arc Data? | Time Span | Downloadable? | Language |
|--------|------|--------------|------------------|-----------------|-----------|--------------|----------|
| MAA AMC School Honor Roll | Competition | Yes (gated) | No | No | Current year | No (login required) | EN |
| USAMO/USAJMO Qualifier Lists | Competition | Yes (school name) | First initial + last name | No | 2021-2024 (PDFs) | Yes (PDF, image-encoded) | EN |
| MATHCOUNTS State Results | Competition | Yes | Yes (individual names) | No | 2007-2025 (by state) | Varies | EN |
| AoPS Forum (individual posts) | Community | Indirect | Self-reported | YES (narrative) | 2005-present | Manual scrape | EN |
| Duosmium (Science Olympiad) | Competition | Yes | No (team only) | No (but multi-year) | 1986-2026 | YES (CSV) | EN |
| Regeneron STS Scholars | Competition | Yes | Full name | No | 2022-2026 | No (HTML/PDF) | EN |
| Regeneron ISEF Database | Competition | Yes | Full name | No | 2014-2026 | Partial | EN |
| Harvard Crimson Survey | Survey | No (aggregate) | No | No (aggregate %) | 2014-2025 | No | EN |
| Yale Daily News Profile | Survey | No (aggregate) | No | No | 2024+ | No | EN |
| 文学城子女教育 Forum | Community | No | Self-reported | Partial (variable) | 2005-present | Manual scrape | ZH |
| Reddit r/ChanceMe | Community | No | Self-reported | YES (grade ranges) | 2017-present | API (paid) | EN |
| "50 Successful Harvard Essays" | Book | No | Individual essays | Partial (narrative) | 2000-2023 (6 editions) | Purchase | EN |
| Try Harder! Documentary | Film | No | 5 students | Senior year only | 2021 | Purchase/stream | EN |
| MITBBS SFparents | Community | No | Self-reported | Low | 2005-2018 (declining) | Manual | ZH |
| 1point3acres 为人父母 | Community | No | Self-reported | Low | 2010-present | Manual | ZH |
| Xiaohongshu 爬藤 | Community | No | Self-reported | Low (+ high noise) | 2018-present | No (requires account) | ZH |

---

## Recommendations for Trajectory Data Acquisition

**Highest-yield sources for WHEN decisions were made:**

1. **AoPS Forum** — Search for "journey" + "AIME" + "years" within forum. Individual posts documenting multi-year competition trajectories are common and detailed. Publicly accessible. Free. English.

2. **Reddit r/ChanceMe and r/collegeresults** — Activity lists in chance-me posts frequently include grade ranges (9-12, 10-12, etc.). The project already has ~30 such posts. Expanding this to hundreds would give statistically useful timing data. English.

3. **USAMO/USAJMO qualifier PDFs** — Download 5 years' worth (2020-2024). Combined with MATHCOUNTS state data for same schools, begin to reconstruct school-level pipeline: which schools produce both middle school math champions AND high school Olympiad qualifiers. Requires cross-referencing two datasets. English.

4. **Duosmium CSV exports** — For Science Olympiad trajectory by school. Machine-readable. Download and join to school profile data already in this project. English.

5. **文学城 名校|爬藤 forum** (https://bbs.wenxuecity.com/eliteuniversity/) — Search for long threads where parents narrate multi-year journeys. "子女上名校，父母谈心得" thread is an example. Higher-quality than 子女教育 for trajectory specifics. Chinese.

**Sources to deprioritize:**

- Harvard Crimson survey: aggregate only, no timing data
- Xiaohongshu: too noisy, access difficult, commercial contamination high
- MITBBS: low activity, Bay Area parenting discussion has moved elsewhere
- YouTube "how I got in" videos: low signal-to-effort ratio for systematic research
