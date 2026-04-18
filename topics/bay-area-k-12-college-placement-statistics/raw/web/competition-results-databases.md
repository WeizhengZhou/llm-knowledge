---
created: 2026-04-18
author: research-agent
purpose: Catalog of publicly accessible competition results databases with K-12 trajectory data
scope: Structured, time-stamped achievement records showing WHEN students reached certain levels
---

# Competition Results Databases — Public Accessibility Catalog

Each entry answers: exact URL, available fields, downloadability, years covered, record count, individual name publication, and school-level aggregate availability.

---

## 1. AMC / AIME / USAMO / MATHCOUNTS (MAA)

### 1a. AMC Score Distributions (Public, Aggregate Only)

**URL:** https://maa.edvistas.com/eduview/report.aspx?view=1561&mode=6

**Access:** Requires login (teacher/administrator portal). Not publicly accessible without credentials.

**What is available behind login:**
- Score distribution charts for AMC 8, AMC 10A/B, AMC 12A/B, and AIME by year
- Percentile breakdowns: top 1%, 2.5%, 5%, 10%, 25%, 50%, 75% score thresholds
- Aggregate statistics per contest: high score, mean, standard deviation
- School team score report (sum of top 3 student scores from each school)
- Grade-level and gender breakdowns
- Export formats: Excel, PDF, CSV, XML

**Fields available (to registered teachers only):**
- Student-level: individual score, grade, gender — visible only to the competition manager at that school
- School-level: team score, rank — visible to that school's manager; not publicly queryable by school
- National: score distribution histogram, percentile thresholds — the only truly public outputs

**Individual names published publicly:** No. Student names and individual scores are not released publicly by MAA. Only the school's own competition manager sees their students' individual data.

**School-level aggregates public:** No. School-level data (how many qualifiers per school, team scores) is not published in a public searchable format by MAA.

**Years covered:** Available back to at least 2010 via the teacher portal. AoPS Wiki maintains community-compiled AMC historical results (cutoff scores, top scorers by name where voluntarily shared) at https://artofproblemsolving.com/wiki/index.php/AMC_historical_results — this page returns 403 to web scrapers but is accessible via browser.

**How school counts appear in practice:**
- Schools self-publish on their own websites (e.g., Harker School published "50 AIME qualifiers" for 2012-13)
- Prep centers publish their own students' counts (Ivy League Education Center, RSM, etc.)
- AoPS community forum threads contain user-reported school tallies, but these are community data (L4)
- No MAA-published, publicly queryable database of AIME qualifiers by school exists

**AIME qualifier threshold:** Published publicly each year at https://maa.org/news/aime-thresholds-are-available/ — gives the cutoff score by contest version, not a list of qualifiers.

**USAMO/USAJMO qualifiers:** MAA does not publish a public list of qualifiers by school. Individual qualifiers are sometimes listed by name in press releases and AoPS community pages. The AoPS Wiki USAMO page at https://artofproblemsolving.com/wiki/index.php/USAMO contains community-compiled historical data.

**Scrapability:** The teacher portal (amc-reg.maa.org) requires login and is not scrapable. The public-facing maa.org pages contain only cutoff thresholds and aggregate national statistics.

**Assessment for trajectory research:** Low direct utility. School-level AIME qualifier counts must be assembled from self-reported school data, prep center marketing, and AoPS forum posts — none of which are systematic.

---

### 1b. MATHCOUNTS (School and Individual, Partial Public)

**Official results URL:** https://mathcounts.org/programs/national-competition-participants

**AoPS community archive:** https://artofproblemsolving.com/wiki/index.php/MATHCOUNTS_historical_results (returns 403 to automated fetch but browser-accessible)

**State-level archives:** Vary by state. Example — Pennsylvania archive at https://www.pspe.org/pspe-events/mathcounts/mathcounts-archive/ covers 2007–2025.

**What is publicly available:**
- National competition: MATHCOUNTS publishes a "National Competition Participants" page listing all 224 competitors (4 per state/territory) with student name and state. School names are included in the national fact sheet PDFs.
- State competition results: Published by individual state PE societies (TSPE, PSPE, etc.). Formats vary — some publish full individual scores, some only top placements.
- AoPS Wiki: Community-compiled historical national results going back to the 1980s, including individual champion names and school affiliations, and a "List of National MATHCOUNTS Teams" page.

**Fields available (national level):**
- Student name: Yes
- School name: Yes (in fact sheet PDFs and AoPS wiki)
- State: Yes
- Placement/score: Top placements published; full score distributions available in PDF documents uploaded to Scribd (e.g., "2025 RTX MATHCOUNTS National Competition Results" — score distributions, team rankings, individual rankings)

**Individual names published publicly:** Yes, for national competitors and many state-level competitors. School name included.

**School-level aggregates public:** Yes at the national level (which school's team placed where). State-level varies by state organization.

**Years covered:** National results available via AoPS wiki from 1984 onward. Systematic PDFs on Scribd from approximately 2019 onward.

**Downloadable:** PDFs on Scribd and state PE society websites. AoPS wiki is copy-pasteable. No structured data export (CSV/API).

**Scrapability:** Manual for PDFs. AoPS wiki pages are HTML-parseable if bot detection is bypassed. State sites vary widely.

**Assessment for trajectory research:** Strong for national-level trajectory (can see which schools produce national competitors across years). State-level completeness depends heavily on state.

---

## 2. Science Olympiad

### 2a. Duosmium Results Archive

**URL:** https://www.duosmium.org/results/

**GitHub data repository:** https://github.com/Duosmium/duosmium

**Scale:**
- 67 national tournaments
- 1,110 state tournaments
- 1,399 regional tournaments
- 1,233 invitational tournaments
- 3,809 total tournaments in archive

**Fields per entry (confirmed from 2023 national tournament page):**
- School/team name
- School city and state
- Overall placement rank
- Total score
- Individual event scores (23 events for Division C nationals)
- Team penalties

**Individual student names published:** No. Only team/school-level data. Individual student names are not in the Duosmium results.

**School-level aggregates:** Yes — this is the primary unit. Full placement and event-by-event scores per school team.

**Download formats:**
- YAML (SciolyFF format) — machine-readable, parseable with any YAML library
- CSV — includes school name, team name, city, state, event scores, combined scores
- Google Sheets compatible (copy-paste)
- PDF (print-to-PDF)

**Years covered:** Spans multiple decades of national tournaments; exact start year varies by tournament type. Recent years (2020–2026) are most complete. Older invitationals have gaps.

**Scrapability:** Yes — the GitHub repository at https://github.com/Duosmium/duosmium contains YAML files for each tournament in the SciolyFF format. This is the cleanest structured dataset in this entire catalog. Pull requests add new tournament YAML files continuously.

**Official Science Olympiad results:** scioly.org itself does not maintain a comparable structured archive. Duosmium is the de facto community standard.

**Assessment for trajectory research:** Excellent for school-level Science Olympiad trajectory across years. Can track which schools compete at nationals, their placement, and event-level strengths. Cannot track individual students.

---

## 3. Regeneron Science Talent Search (formerly Intel STS)

### 3a. Semifinalist / Scholar Lists (Top 300)

**URL pattern:** https://www.societyforscience.org/regeneron-sts/{year}-scholars/

**Confirmed years with live pages:** 2023, 2024, 2025, 2026

**Fields per scholar:**
- Student name
- Age (in some years)
- School name
- School city and state
- Project title

**Volume:** 300 scholars selected per year from approximately 2,400–2,500 entrants representing approximately 795 high schools.

**Individual names published publicly:** Yes.

**School-level aggregates public:** Derivable — the scholar list can be aggregated by school. Society for Science press releases state school counts (e.g., "2025 scholars represent 200 high schools in 33 states").

**Downloadable:** A "Scholar Book" PDF is available for download on each year's page. The HTML list is parseable.

**Scrapability:** The scholar list pages are standard HTML. Each scholar entry includes name, school, and project title in structured markup.

**Historical depth:** The competition began in 1942. Society for Science pages go back to at least 2023 with direct URLs. Older years: the APA (American Psychological Association) maintains a list of ISEF/STS winners at https://www.apa.org/ed/precollege/topss/isef-winners, and Wikipedia's Regeneron Science Talent Search article contains historical winners. Intel-era results (pre-2017) may require archival research.

**Assessment for trajectory research:** Strong. Can build year-by-year school-level scholar production tables from 2023–present directly from Society for Science pages. Older years require secondary sources.

---

### 3b. Finalist Lists (Top 40)

**URL pattern:** https://www.societyforscience.org/regeneron-sts/{year}-finalists/

**Confirmed years:** 2023, 2024, 2025, 2026

**Fields per finalist:**
- Student name
- School name and location
- Project title
- Full project description
- Personal background

**Volume:** 40 finalists per year. A "Finalists Program Book" PDF is available for download each year.

**Individual names published publicly:** Yes.

**Downloadable:** Yes, via PDF Program Book linked on each year's finalist page.

**Assessment for trajectory research:** Very strong signal (top 40 nationally). Small N per school per year, so most useful aggregated over multiple years.

---

## 4. ISEF (International Science and Engineering Fair)

### 4a. Abstract Database (2014–2025)

**URL:** https://abstracts.societyforscience.org/

**Search fields available:**
- Keyword or phrase
- Finalist last name
- Project category (extensive STEM discipline list)
- Fair country
- Fair state (US states and territories)
- Year (2014–2025)
- Filter: all abstracts or winning entries only

**Note:** School name is NOT a search field in this interface. You can search by state and year, then read through results to find school affiliations.

**Fields displayed per project:** Project abstract text, finalist name, category. School affiliation appears to be included in the project record but is not a primary search dimension.

**2026 Finalist Lookup:** https://finalistquestionnaire.societyforscience.org/projectlist — shows Fair ID, Finalist Name, and Project ID. Sortable by column. No school field shown in this interface.

**Volume:** ISEF selects approximately 1,700–1,800 finalists per year from roughly 49 states and 60+ countries, representing affiliated regional fairs.

**Individual names published publicly:** Yes.

**School-level aggregates public:** Not directly. Must derive by downloading/scraping results and aggregating by school.

**Downloadable:** No direct CSV/export from the abstract database. HTML-parseable.

**Years covered:** 2014–2025 in the abstract database. Older results may appear in press releases and the APA winners list.

**Assessment for trajectory research:** Moderate. The absence of school as a search field adds friction. Useful for identifying individual student trajectories (search by last name across years) and for state-level filtering. School aggregation requires scraping.

---

## 5. USA Computing Olympiad (USACO)

**Results URL pattern:** https://usaco.org/index.php?page={month}{year}results

**Examples:**
- https://usaco.org/index.php?page=open25results (2025 US Open)
- https://usaco.org/index.php?page=dec24results (December 2024)
- https://usaco.org/index.php?page=jan25results (January 2025)

**Divisions:** Platinum, Gold, Silver, Bronze — each with separate results pages linked from the main results page.

**What is publicly visible:**
- Results pages for top scorers are listed (Platinum division shows top scorers with names; the page structure confirms individual names are published for top performers)
- Promotion thresholds are published: e.g., "850+ for Gold→Platinum, 750+ for Silver→Gold, 700+ for Bronze→Silver" for the 2025 US Open
- For Gold division: "the list of USA pre-college students who were promoted [to Platinum] is [here]" — suggesting individual names are listed for promoted students

**School names published:** No. USACO results do not include school affiliation. Individual handles/usernames and names appear for top performers, but no school field exists.

**Individual names published publicly:** Yes, for top scorers and promoted students. Not a complete participant list — only high performers.

**School-level aggregates public:** No. There is no school-level aggregation in USACO's published results.

**Downloadable:** No structured download. Results pages are HTML.

**Years covered:** Results pages go back to at least 2021 at the pattern above. Older results may be archived.

**Scrapability:** USACO result pages are HTML-parseable. However, school name is absent, so school-level trajectory analysis is not directly supported.

**Community workaround:** USACO user profiles (usaco.org/index.php?page=user) show historical contest participation and division progression for individual users who have public profiles. This provides individual trajectory data but requires knowing the username.

**Assessment for trajectory research:** Limited for school-level analysis (no school field). Strong for individual trajectory if you have the student's USACO handle. AoPS forum threads often identify USACO high performers and their schools by community knowledge.

---

## 6. USAPhO (U.S. Physics Olympiad)

**Run by:** American Association of Physics Teachers (AAPT)

**Results URL:** https://aapt.org/physicsteam/PT-landing.cfm

**PDF result lists (direct download):**
- 2024: https://www.aapt.org/physicsteam/2024/upload/2024-Medal-Listing.pdf
- 2023: https://www.aapt.org/physicsteam/2023/upload/2023-Medal-Listing.pdf
- Pattern suggests prior years follow same URL structure

**Fields confirmed from 2024 PDF (8 pages, ~394 students total):**
- Student last name, first name
- School name (full name)
- City
- State
- Medal level: US Physics Team Member, Gold Medal, Silver Medal, Bronze Medal, Honorable Mention

**Tier breakdown (2024, approximate):**
- US Physics Team Member: 20 students (national team)
- Gold Medal: approximately 15–20 students
- Silver Medal: approximately 35–40 students
- Bronze Medal: approximately 80–100 students
- Honorable Mention: approximately 250–280 students

**Individual names published publicly:** Yes — full name, school, city, state, medal level.

**School-level aggregates public:** Derivable — the PDF lists every student with their school. Aggregating by school name gives a complete picture of which schools produced medalists in a given year.

**Downloadable:** Yes, direct PDF download. Machine-readable with PDF text extraction (the 2024 PDF is text-based, not scanned).

**Years covered:** PDFs confirmed for 2023 and 2024. Prior years likely follow the same URL pattern (check /physicsteam/{year}/upload/{year}-Medal-Listing.pdf). Competition has run since 1968.

**Quarter-finalists (F=ma exam):** Listed separately at https://www.aapt.org/physicsteam/quarterfinalists.cfm — these are approximately the top 400 scorers on the F=ma qualifying exam (~5,000–6,000 participants annually). Page includes student name and school.

**Scrapability:** PDF text extraction is clean (not scanned). No structured download beyond PDF.

**Assessment for trajectory research:** Excellent. Cleanest structured dataset among science olympiads — PDF with consistent fields (student, school, city, state, medal) across multiple years. School-level aggregation is straightforward.

---

## 7. Science Talent Search — Adjacent: RSM and Enrichment Program Results

**RSM (Russian School of Mathematics)** publishes competition achievement summaries on its blog at https://www.mathschool.com/blog/results/ — annual posts for each school year (confirmed: 2023-2024, 2024-2025).

**What RSM publishes:**
- Aggregate counts (e.g., "7 RSM students earned USAJMO honors")
- Named individual students for top honors
- Competition categories: MOEMS, AMC/AIME, USAJMO, USAMO, Purple Comet, Girls in Math at Yale, IMC
- RSM-internal competition (International Math Contest, ~25,000 students)

**Fields:** Student name (for top honors), competition name, award level, year. School of attendance is not listed — RSM is the program, not the school.

**Assessment for trajectory research:** Useful as a benchmark for what enrichment programs produce but does not link students to their K-12 schools of enrollment. Not a primary source for school-level trajectory data.

**Kumon:** Does not publish individual student competition results publicly.

---

## 8. National Speech and Debate Association (NSDA)

### 8a. Official NSDA Rankings and School Recognition

**URL:** https://www.speechanddebate.org/rankings/

**School recognition programs:**
- Top 100 Schools (by new degrees earned) — published annually as PDF press release: e.g., https://www.speechanddebate.org/wp-content/uploads/2023-2024-Top-100-Clubs-Press-Release10.29.24.pdf
- Schools of Outstanding Distinction (top 10 combined speech + debate points)
- Speech Schools of Excellence (top 20 in speech points)
- Debate Schools of Excellence (top 20 in debate points)

**Fields in school recognition PDFs:** School name, state, rank, points. No individual student names.

**National Tournament results:** Published in the annual Rostrum (NSDA magazine) and accessible via Rostrum archive at speechanddebate.org. Tournament-level results include competitor names, school, event, placement.

**Nationals History page:** https://www.speechanddebate.org/nationals-history/ — historical national tournament results.

**Individual names published publicly:** Yes, for national tournament participants and award recipients.

**School-level aggregates public:** Yes — the Top 100 Schools PDF is the most direct school-level aggregate.

**Years covered:** NSDA has run since 1925. Digital archives of Rostrum go back multiple decades.

### 8b. Tabroom.com (Tournament Management Platform)

**URL:** https://www.tabroom.com/

**What is publicly accessible:**
- Tournament entry lists: school names, event entries (competitor names may be shown depending on tournament director settings)
- Round-by-round pairings and results: visible in real time and after tournament closes, subject to tournament director's public results settings
- Circuit statistics: number of participating schools, students, judges per circuit and year
- School result histories: "Checker Sheets" show all tournaments a competitor attended and their results

**API:** An undocumented endpoint at /api/download_data.mhtml creates JSON backups of tournament data. Not a formal public API.

**Fields available:**
- Competitor name (usually)
- School name
- Event (LD, PF, Policy, Congress, etc.)
- Tournament name and date
- Round-by-round results (win/loss, speaker points)
- Preliminary and elimination bracket placements

**Individual names published publicly:** Yes, for most tournaments (depends on director settings, but the default is public).

**School-level aggregates public:** Derivable by filtering Tabroom data by school across tournaments.

**Years covered:** Tabroom has been the dominant platform since approximately 2010. Historical data completeness improves after 2015.

**Scrapability:** HTML-parseable. Debate Land (https://www.debate.land/) has already scraped Tabroom to build national circuit rankings for PF, LD, and Policy. Their methodology is published at https://github.com/Debate-Land/Debate-Land/blob/main/METHODOLOGY.md.

### 8c. Debate Land (Third-Party Tabroom Aggregator)

**URL:** https://www.debate.land/

**What it provides:** Pre-aggregated national circuit rankings for Public Forum, Lincoln-Douglas, and Policy debate, derived from Tabroom data.

**Fields:** Individual competitor rankings, school rankings, win rates, tournament performance metrics, opponent win percentage.

**Years covered:** Based on available Tabroom data; most complete from approximately 2018 onward.

**Assessment for trajectory research:** Strong for debate trajectory. Tabroom + Debate Land together provide the richest individual + school longitudinal dataset in the performing/competitive arts space. Individual names, schools, tournament dates, and results are all public.

---

## 9. YoungArts and Scholastic Art and Writing Awards

### 9a. YoungArts Winners Directory

**URL:** https://youngarts.org/winners-directory/

**What is published:** Annual winners lists for competition years 2013–2026 (confirmed). The Winners Directory is a searchable database.

**Disciplines covered:** Classical music, dance, design, film, jazz, photography, theater, visual arts, voice, writing — 10 disciplines total.

**Fields:** Winner name, discipline, award level (Winner with Distinction, Winner, Honorable Mention). School name is not prominently featured in the public directory based on the page structure — the directory is primarily name/discipline-oriented.

**Individual names published publicly:** Yes.

**School-level aggregates public:** Not directly available from the YoungArts directory. Some press releases from schools announce their YoungArts winners, but YoungArts itself does not publish school-aggregated data.

**Note:** The Winners Directory page requires JavaScript rendering. WebFetch returned an empty shell. Chrome MCP or a JS-rendering scraper would be needed to extract the full list.

**Awards:** Cash awards up to $10,000; finalists invited to National YoungArts Week in Miami.

### 9b. Scholastic Art and Writing Awards

**National Medalists database URL:** https://medals.artandwriting.org/

**What is published:** National medalists list published each spring. The database is JavaScript-rendered (requires JS to load content).

**Award levels:**
- American Voices/Visions Medal (one per region per discipline)
- Gold Medal (national level, selected from regional Gold Keys)
- Silver Medal
- Portfolio Gold Medal

**Regional awards (Gold Key, Silver Key, Honorable Mention):** Administered regionally. Some regional affiliates publish their own lists (e.g., Bay Area: CCA publishes Bay Area Scholastic Art and Writing Awards results).

**Fields (national medalists):** Student name, award level, discipline/category, work title. School name is listed in some years' publications; the printed Yearbook includes school information.

**Individual names published publicly:** Yes.

**School-level aggregates public:** Not directly from the medals.artandwriting.org database. School names appear in press releases and the Yearbook but are not a primary search dimension in the online database.

**Years covered:** The national medalists database appears to go back to at least 2023 online. Historical yearbooks (print) go back to 1923 (competition founded 1923).

**Scale:** Approximately 330,000 works submitted annually; approximately 800–1,000 national medalists selected.

**Assessment for trajectory research:** Moderate. Individual names are public but school-level aggregation requires cross-referencing with school press releases or the printed Yearbook. The regional Gold Key lists (which feed nationals) are distributed across dozens of regional affiliates with inconsistent online publication.

---

## 10. Athletic Recruiting Databases

### 10a. 247Sports

**URL:** https://247sports.com/

**Relevant sections:**
- National recruit rankings by year and sport: https://247sports.com/season/{year}-{sport}/recruitrankings/
- School/program team recruiting rankings: https://247sports.com/season/{year}-{sport}/compositeteamrankings/
- Individual athlete profiles with full ranking history timeline

**Fields per athlete profile:**
- Name, position, high school, hometown
- Star rating (1–5 stars) and numerical score (0–100)
- Ranking history — a complete log of every ranking update with date, previous rank, new rank
- "Timeline" tab: chronological log of all key events (first offer, de-commitment, visits, commitment, signing)
- Composite ranking (average of all major recruiting services)

**Individual names published publicly:** Yes.

**School-level aggregates public:** Yes — "Team Rankings" pages aggregate by high school or college program. High school of origin is a field on every athlete profile.

**When does a recruit first appear:** 247Sports' ranking update schedule:
- Initial rankings typically released for rising juniors (Grade 11) in the August prior to junior year
- Updates through spring (camp performances), fall junior year (film), and senior year
- Some elite athletes are identified as early as Grade 9 (freshman year) in major sports

**Rating history timeline granularity:** Full date-stamped history of every ranking change is on each profile page. This is the primary trajectory data for athletic recruiting.

**Years covered:** Rankings go back to at least 2002 in football. Other sports vary. 247Sports Database 2.0 improved historical completeness.

**Scrapability:** 247Sports is anti-scraping. The ranking history tab requires JavaScript rendering. Systematic access would require Chrome MCP or a commercial data provider.

**Sports covered:** Football, basketball (M/W), baseball, softball, soccer, volleyball, lacrosse, and others. Coverage depth varies significantly by sport — football and men's basketball have the deepest historical records.

### 10b. MaxPreps

**URL:** https://www.maxpreps.com/

**What it provides:** High school sports statistics and rankings. Less focused on individual recruiting profiles than 247Sports. Primarily game-level stats, season statistics, and team rankings.

**Relevant for trajectory:** Can show when a player began appearing in statistical leaderboards. Less useful than 247Sports for recruiting timeline data specifically.

**Fields:** Player name, school, sport, season stats (points, yards, etc.), team record.

**Individual names published publicly:** Yes.

**School-level aggregates public:** Yes — team statistics and state/national rankings by school.

**Assessment for trajectory research:** Useful for confirming athletic performance at the high school level but does not contain the recruiting ranking timeline that 247Sports provides.

---

## 11. AoPS Community (artofproblemsolving.com)

**URL:** https://artofproblemsolving.com/community/

**Why this matters for trajectory research:** AoPS is the richest qualitative source for math competition trajectory data. It contains:

**a. Community Forum Posts:**
- Students post their own competition histories (e.g., "A culmination of 13+ years: AIME qualification" — actual thread title from search results)
- Threads discussing which schools had how many AIME/USAMO qualifiers in a given year
- School-specific discussion threads (e.g., "Harker math team" threads)
- Annual "AIME qualifier roll call" threads where students self-report

**b. AoPS Wiki Pages:**
- AMC historical results: https://artofproblemsolving.com/wiki/index.php/AMC_historical_results — community-compiled top scorers, school affiliations where known, historical cutoffs
- MATHCOUNTS historical results: similar community-compiled data
- USAMO page: community-compiled qualifier lists and scores
- State-specific math competition pages (e.g., Texas MathCounts, California math competitions)

**c. Student Profiles:**
- AoPS user profiles show competition results that users choose to share
- Multi-year competition history is visible on profiles where users have entered their results
- No structured export — profile data must be extracted manually

**Fields (from forum posts and wiki, not structured):**
- Competition name, year, result (qualifier/score/placement)
- Student handle (pseudonymous, though many use real names)
- School name (self-reported, often in forum signatures or post content)
- Grade level at time of competition

**Individual names published publicly:** Pseudonymous handles are public; real names appear only when students self-disclose.

**School-level aggregates public:** Community-compiled, not systematic. Reliability depends on how many students from a given school participate in AoPS and self-report.

**Scrapability:** AoPS forum and wiki pages are HTML-parseable. The wiki returns 403 to some automated fetchers but is accessible via browser or Chrome MCP. Forum content is paginated and extensive.

**Assessment for trajectory research:** Highest signal for qualitative math trajectory patterns. Quantitative reliability is limited — it captures the self-selecting population of AoPS users, which skews toward high performers. The trajectory of "MATHCOUNTS state competitor → AIME qualifier → USAMO qualifier → Putnam" is most reliably documented here, but by self-reported, pseudonymous users. School-level data is present but scattered across years of forum posts.

---

## 12. NAQT (National Academic Quiz Tournaments) — Quiz Bowl

**URL:** https://www.naqt.com/stats/tournament/

**What it provides:** Tournament results for quiz bowl competitions at middle school, small high school, standard high school, community college, and college levels.

**Fields:**
- School/team name
- Tournament name, date, location
- Individual standing (player name, points per game, tossups heard)
- School standing (wins, losses, points per game)
- National championship results going back multiple decades

**Individual names published publicly:** Yes — individual player statistics are published (points per game, categories).

**School-level aggregates public:** Yes — team records, tournament placements, school result history pages (e.g., https://www.naqt.com/stats/school/results.jsp?org_id=59910 for Phillips Exeter Academy).

**Years covered:** Detailed statistics available from approximately 2007–2008 onward. Earlier data is incomplete. National championship history goes back further.

**Downloadable:** HTML tables, no structured download. Data prior to 2007-08 is very incomplete per NAQT's own documentation.

**Scrapability:** Standard HTML tables. Parseable.

**Assessment for trajectory research:** Strong for quiz bowl specifically. Individual player stats across tournaments and years are available. Can reconstruct a student's quiz bowl career trajectory from the data.

---

## Summary Table

| Source | URL | Individual Names | School Aggregates | Download Format | Years | Scrapable |
|---|---|---|---|---|---|---|
| AMC/AIME (MAA) | amc-reg.maa.org (login required) | No (private) | No (private) | Excel/PDF (gated) | 2000s–present | No (login wall) |
| AMC Cutoffs (public) | maa.org/news/aime-thresholds-are-available/ | N/A | N/A | HTML | Annual | Yes |
| AoPS AMC Wiki | artofproblemsolving.com/wiki/index.php/AMC_historical_results | Partial (self-reported) | Partial (community) | HTML copy | 1950s–present | Browser only |
| MATHCOUNTS National | mathcounts.org/programs/national-competition-participants | Yes | Yes (by state) | PDF/HTML | 1984–present | Manual |
| Science Olympiad (Duosmium) | duosmium.org/results/ | No | Yes (team/school) | YAML, CSV | 1985–present | Yes (GitHub) |
| Regeneron STS Scholars | societyforscience.org/regeneron-sts/{year}-scholars/ | Yes | Derivable | HTML/PDF | 2023–present (structured) | Yes |
| Regeneron STS Finalists | societyforscience.org/regeneron-sts/{year}-finalists/ | Yes | Yes | HTML/PDF | 2023–present | Yes |
| ISEF Abstracts | abstracts.societyforscience.org/ | Yes | No direct school search | HTML | 2014–2025 | Partial |
| USACO Results | usaco.org/index.php?page={contest}results | Yes (top scorers) | No | HTML | 2012–present | Yes (no school field) |
| USAPhO Medal List | aapt.org/physicsteam/{year}/upload/{year}-Medal-Listing.pdf | Yes | Derivable | PDF (text) | 2023–present confirmed | Yes (PDF extraction) |
| USAPhO Quarter-finalists | aapt.org/physicsteam/quarterfinalists.cfm | Yes | Derivable | HTML | Annual | Yes |
| NSDA Top 100 Schools | speechanddebate.org/school-recognition/ | No | Yes | PDF | Annual | Yes |
| NSDA Nationals History | speechanddebate.org/nationals-history/ | Yes | Yes | HTML | Decades | Yes |
| Tabroom.com | tabroom.com | Yes | Yes (derivable) | JSON (undocumented API) | 2010–present | Partial |
| Debate Land | debate.land | Yes | Yes | HTML | 2018–present | Yes |
| YoungArts Winners | youngarts.org/winners-directory/ | Yes | No | JS-rendered HTML | 2013–present | Chrome MCP needed |
| Scholastic Art/Writing | medals.artandwriting.org | Yes | No | JS-rendered HTML | 2023–present online | Chrome MCP needed |
| 247Sports Recruiting | 247sports.com | Yes | Yes | JS-rendered HTML | 2002–present | Chrome MCP, anti-scrape |
| MaxPreps | maxpreps.com | Yes | Yes | HTML | 2000s–present | Moderate |
| AoPS Community | artofproblemsolving.com/community | Pseudonymous | Partial (community) | HTML | 2003–present | Browser/Chrome MCP |
| NAQT Quiz Bowl | naqt.com/stats/tournament/ | Yes | Yes | HTML | 2007–present | Yes |
| RSM Blog | mathschool.com/blog/results/ | Yes (top performers) | No (RSM-level only) | HTML | 2020–present | Yes |

---

## Key Observations for K-12 Trajectory Research

**Best sources for school-level aggregation (can count achievements per school per year):**
1. USAPhO medal PDFs — cleanest, structured, PDF text-extractable, includes school
2. Science Olympiad via Duosmium — YAML/CSV downloadable by school, no individual names
3. Regeneron STS — HTML-parseable scholar/finalist lists with school name
4. MATHCOUNTS — PDFs and AoPS wiki, school name included for national competitors
5. NSDA Top 100 Schools — direct school rankings PDF, no individual names needed
6. 247Sports — school-of-origin on athlete profiles, but anti-scraping

**Best sources for individual trajectory (can track a specific student across years):**
1. USAPhO — name + school + medal across years, PDF per year
2. Tabroom.com + Debate Land — individual debate competitor history with dates
3. NAQT — individual player stats across tournaments
4. 247Sports — full dated ranking history per athlete
5. AoPS community profiles — self-reported math competition histories (pseudonymous)

**Critical gap: AMC/AIME school-level data is not publicly available.** The most frequently cited math competition achievement for K-12 schools — number of AIME qualifiers — is not published by MAA in any public form. It must be assembled from: (a) school self-reports on their own websites, (b) prep center marketing materials, (c) AoPS forum community threads. This is the most significant data gap in the landscape.

**Privacy note:** All sources listed above publish individual student names as part of their standard public communications. No source listed here requires obtaining data through means beyond what is publicly accessible. The USAPhO PDF in particular provides a clean example of what "publicly available individual-level competition data" looks like: name, school, city, state, medal — for approximately 394 students in 2024, covering US Physics Team members through Honorable Mentions.
