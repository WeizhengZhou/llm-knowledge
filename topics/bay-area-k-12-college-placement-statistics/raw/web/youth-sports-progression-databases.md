---
fetched: 2026-04-18
question_id: supplemental-youth-progression-databases
reliability_tier: L2-authoritative (composite — each section cites direct verification of live database interfaces)
research_method: WebSearch + WebFetch + Chrome MCP live interface verification
---

# Youth Sports & Activity Progression Databases — Raw Research Notes

Researched 2026-04-18. Each section records exact URLs, verified search interface fields (via Chrome MCP a11y tree snapshots), data availability, and limitations. Purpose: assess whether these databases can generate individual development curves (performance vs. age) for children starting from elementary school.

---

## 1. Swimming — USA Swimming SWIMS / SwimCloud / SwimmingRank

### 1A. USA Swimming SWIMS 3.0 Official Database

**Primary URL:** https://www.usaswimming.org/about-usas/resources/swims-database
**Data Hub:** https://data.usaswimming.org/datahub
**Individual Times Search:** https://data.usaswimming.org/datahub/usas/individualsearch
**Individual Times Detail (with filters):** https://data.usaswimming.org/datahub/usas/individualsearch/times
**Event Rank Search:** https://data.usaswimming.org/datahub/usas/timeseventrank

**What is it:** SWIMS 3.0 is the official registration and results database of USA Swimming. Every sanctioned, approved, and observed meet time is uploaded here. Relaunched September 1, 2022 (superseding SWIMS 2.0).

**Volume:** USA Swimming had 376,320 registered members as of 2024 (down from pre-pandemic peak of 411,672 in 2019). Largest age group was 8-and-under at 41,777 members; age 11 had 33,445 members. More than 53% female. Pacific Swimming LSC (Bay Area + NorCal) is the third-largest of 59 regional LSCs with ~100 clubs and 14,000+ swimmers.

**Years covered:** Data hub dropdown confirmed: 1994 through 2026 (competition years 9/1–8/31 format), so 32 seasons of timestamped data.

**Age groups in the database (verified from live interface):**
- Individual: 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 18 & Under, 10 & Under, 11-12, 13-14, 15-16, 17-18, 19 & Over, Open
- Youngest trackable age: 7

**Data fields per swim (verified from a11y snapshot of live results):**
- Event (e.g., "50 FR SCY", "200 FR-R SCY")
- Swim Time
- Age at time of swim
- Performance Points
- Time Standard (B, BB, A, AA, AAA, AAAA, Futures, Winter Juniors, Summer Juniors, etc.)
- Meet name
- LSC (Local Swimming Committee, e.g., "Pacific Swimming")
- Team/Club name
- Swim Date (exact date, e.g., "11/07/2025")
- Splits (expandable)
- PROGRESSION button per swim (links to swimmer's progression chart)

**Individual search (name-based):**
Search fields: First or Preferred Name + Last Name only. No club search from the individual search interface. Returns all times for that swimmer across all years. A PROGRESSION button appears on each record.

**Event Rank search (LSC-filterable):**
Search fields verified: Competition Year, Gender, Age Group (individual ages 7-18), Time Standard, Display Options, Course, Event, Zone (Central/Eastern/Southern/Western), LSC (all 59 listed individually including "Pacific Swimming"). Max results: up to 500. This allows querying "all 8-year-old girls in Pacific Swimming in 2024 who swam the 50 Free."

**Bay Area club search:**
SwimCloud (third-party, see 1B) provides club-level search. The SWIMS data hub itself does not expose a club-name search on the public interface — you need the swimmer's name or must use the LSC-level event rank search.

**Can we track individuals over time?** YES. The individual times search returns all historical times for a named swimmer across all competition years back to 1994. The PROGRESSION button visualizes this. A swimmer who started at age 7 in 2010 and competed through age 18 in 2021 would have a complete 12-year timestamped record.

**Public or gated?** Fully public. No login required. The data hub is open to anyone.

**Scrapable?** Multiple open-source scrapers exist on GitHub (github.com/alexkgrimes/swimulator, github.com/maflancer/SwimScraper, pypi.org/project/SwimScraper). USA Swimming does have a 3rd-party vendor program with API agreements (usaswimming.org/about-usas/resources/swims-database/3rd-party-vendors). The public-facing search has no stated rate limits visible; scrapers report it is scrapable but SwimCloud's Terms of Service explicitly prohibit copying.

**Privacy considerations:** Data is publicly searchable by name. COPPA applies to children under 13; however the database has operated in its current public form for decades. Names, club affiliations, and times are indexed publicly. Ages appear at time of swim. Birth dates are not directly exposed (age is derived). Researchers note: "player histories dating back several years are often available online, and once a child's information is public, it is searchable and available forever."

**KEY ANSWER — Individual development curve:** YES. This is likely the most complete longitudinal youth development database in existence for any sport. A swimmer registered at age 7 generates a timestamped performance record across every sanctioned meet they enter, with age recorded at each swim. The LSC filter narrows to Pacific Swimming (Bay Area). Club-level querying requires knowing club names (e.g., Palo Alto Stanford Aquatics = PASA, ~832 competitive swimmers, SwimCloud team ID 8015).

---

### 1B. SwimCloud

**URL:** https://www.swimcloud.com/
**Pacific LSC page:** https://www.swimcloud.com/country/usa/club/lsc/Pacific/
**Pacific swimmers:** https://www.swimcloud.com/country/usa/club/lsc/Pacific/swimmers/
**Palo Alto Stanford Aquatics (PASA):** https://www.swimcloud.com/team/8015/
**PASA Roster (age group filters):** https://www.swimcloud.com/team/8015/roster/

**What is it:** Third-party platform that aggregates USA Swimming SWIMS data and presents it with richer UI — team pages, swimmer profiles, recruitment features, rankings, and performance analytics.

**Bay Area club search:** YES. SwimCloud has full club/team pages organized by LSC. Pacific Swimming LSC page lists all member clubs. PASA (Palo Alto Stanford Aquatics) confirmed public at swimcloud.com/team/8015/ with roster filters by age group (e.g., 13-14, 11-12) and gender.

**Individual swimmer profiles:** YES. Swimmer profiles show career times, progression charts, meet history, and college recruitment information. Profiles are searchable by name.

**Public access limitations:** SwimCloud displays only top 20 rankings within a team and top 100 in a region for ranking tables. However individual swimmer profiles appear fully public if you navigate directly. No login required for viewing.

**Terms of service concern:** SwimCloud's Terms of Service explicitly state that downloading, copying, or providing unauthorized access to any part of the website violates their Terms and may violate applicable laws.

**Other notable Bay Area clubs on SwimCloud:**
- South Bay Swim Team: swimcloud.com/team/10009899/
- Bay Club swimmers: search required
- Alto Swim Club: altoswimclub.com (separate platform)

---

### 1C. SwimmingRank / SwimmingRank.org

**URL (defunct .com):** https://www.swimmingrank.com/ — SHUT DOWN after ~15 years of operation. The site has been sunsetted.
**URL (active .org):** https://www.swimmingrank.org/ — Returns 403 as of 2026-04-18, possibly also defunct.

**Status:** SwimmingRank.com, a long-running independent rankings site, has been permanently shut down.

---

### 1D. Swim Standards

**URL:** https://swimstandards.com/
**Rankings:** https://swimstandards.com/rankings
**PASA club page:** https://swimstandards.com/clubs/pc/palo-alto-stanford-aquatics

**What is it:** Mobile-friendly web version of USA Swimming time standards. Provides swimmer profiles, meet results, rankings, and club pages. Confirmed public PASA club page exists.

**Individual development curve:** Yes, similar to SwimCloud — aggregates SWIMS data with swimmer-profile views.

---

### 1E. MySwimIO

**URL:** https://www.myswimio.com/

**Features (from official description):** "USA swimming swim results and swimmer profiles, graphical analytical tools like event history, season change, relay calculators, comparison tool by date or age of swimmers, visual progress for cuts along with Age Up feature, Qualifiers for LSC Age Group championships, Rankings by team, LSC, state, zone and USA."

**Public access:** Operates without mandatory login. Users can browse freely.

**Individual development curve:** YES — explicitly provides "comparison tool by date or age of swimmers" and "visual progress for cuts." This appears to be the most analysis-focused public tool for swimmer progression.

---

## 2. USTA Junior Tennis Rankings

**Primary URL:** https://www.usta.com/en/home/play/rankings.html
**Player profile search:** https://www.usta.com/en/home/play/player-search/profile.html
**Archived ranking search:** https://tennislink.usta.com/tournaments/rankings/rankinghome.aspx
**NorCal section:** https://www.ustanorcal.com/

**What is it:** USTA tracks junior tournament results and produces national standings lists updated weekly (published Wednesdays). Players accumulate ranking points from their 6 best Junior Ranking Tournaments (singles) + best 6 doubles at 15% weight.

**Age divisions tracked:**
- Boys' and Girls' 8, 10, 12, 14, 16, 18 Singles (confirmed from TennisLink interface)
- Youngest competitive ranking: 8U division
- National standings are published annually for 12U, 14U, 16U, 18U divisions specifically

**Individual player profile:**
- Accessible at usta.com/en/home/play/player-search/profile.html
- Shows match results and ranking information
- Results shown in profile are inclusive of past 52 weeks only (rolling window)
- Must be logged into TennisLink account to search for a junior rating level

**Historical data:**
- TennisLink archived ranking search confirmed years from 2001 through 2026 available
- Search fields: USTA membership number OR player name, Section/District (NorCal available), Year, Division, List Type (12-month standings, final rankings, seeding lists)

**Bay Area search:** YES — can filter by Section "Northern California" (NorCal). Cannot filter by specific club/academy directly.

**Can we track individuals over time?** PARTIALLY. Historical archived rankings (2001-2026) exist but require knowing the player's name and USTA ID. The rolling 52-week window on live profiles means you cannot see multi-year progression within the current interface — you'd need to query archived rankings for each year separately. No built-in longitudinal chart.

**Volume:** USTA does not publish granular membership statistics by age division in publicly available sources. However USTA Junior Team Tennis operates in 8U, 10U, 12U, 14U, 16U, 18U divisions nationally.

**Public or gated?** Archived ranking search appears public. Individual player rating level search requires TennisLink login.

**Development curve:** POSSIBLE but manual. You would need to query the player name across archived years (2001-2026) to reconstruct a progression from 10U through 18U. No automated progression view exists.

**Scrapable?** TennisLink uses older web infrastructure. No documented public API. Web scraping possible but interface is complex.

**Privacy:** Player names and ranking positions are fully public in published standings. Individual match results may require login.

---

## 3. Fencing — askFRED.net and FencingTracker.com

### 3A. askFRED.net

**URL:** https://www.askfred.net/
**Fencer results search:** https://www.askfred.net/results/fencer
**FAQ:** https://help.askfred.net/en/articles/8050745-frequently-asked-questions

**What is it:** FRED = "Fencing Results and Events Database." The primary national fencing tournament management and results database in the US.

**Age categories in fencing:**
- Y10 (Youth 10), Y12 (Youth 12), Y14 (Youth 14)
- Cadet (under 17)
- Junior (under 20)
- Senior
- Veteran divisions
- Age is determined by birth year, not age on day of tournament

**Individual fencer search:** Requires login. The page explicitly states: "You must be logged in to search results by fencer." Without login, you can browse tournaments and results but cannot query by individual fencer.

**Bay Area clubs:**
- Peninsula Fencing Academy (PeninsulaFA)
- Bay Area Fencing Club (BAFC)
- South Bay Fencing Academy (SBFA)
- SF Fencers Club
- Halberstadt Fencers Club
- Golden State Fencing Academy (GSFA)
- West Berkeley Fencing Club
- NorCal fencing division: norcalfence.org

**Public or gated?** Partially gated — tournament lists and results public, individual fencer search requires login (free registration).

**Development curve via askFRED:** Possible but requires account. Once logged in, you can search by fencer name and see results across age categories over years.

---

### 3B. FencingTracker.com

**URL:** https://fencingtracker.com/
**Peninsula Fencing Academy club page:** https://fencingtracker.com/club/100128001/PeninsulaFA/results
**Bay Area Fencing Club:** https://fencingtracker.com/club/100314997/BAFC/results
**South Bay Fencing Academy:** https://fencingtracker.com/club/100274397/SBFA/results

**What is it:** Third-party analytics platform for fencing. "Statistics and analytics for the sport of fencing." Distinct from askFRED — FencingTracker appears to aggregate askFRED results data and present it with club pages, individual performance trends, and opponent research.

**Data available (from Peninsula Fencing Academy club page, verified via WebFetch):**
- Tournament results for club members with placements and dates
- Competitions visible: ROCs (Regional Olympic Committees), NACs (North American Cups), nationals
- Age categories visible in results: Youth 14, Cadet, Junior, Veteran 50-59
- Individual fencer results trackable by name across multiple events
- Time span: approximately 4 years of historical results (2021 through early 2026)

**Public access:** YES — fully public, no login required. Club pages are publicly accessible.

**Can we track individuals over time?** YES — by searching a fencer's name across club results. Interface does not provide an automated developmental progression chart, but data is present. No Y10/Y12 progression visualization built in.

**Bay Area club pages confirmed on FencingTracker:**
- Peninsula Fencing Academy: fencingtracker.com/club/100128001/PeninsulaFA/results
- Bay Area Fencing Club: fencingtracker.com/club/100314997/BAFC/results
- South Bay Fencing Academy: fencingtracker.com/club/100274397/SBFA/results

**Development curve:** PARTIAL. 4 years of publicly searchable results by fencer name and club. Does not automatically chart Y10 → Y12 → Y14 → Cadet → Junior progression, but underlying data is present and researchable.

---

## 4. USA Gymnastics — MeetScoresOnline and Related Platforms

**Primary meet results source:** https://www.meetscoresonline.com/
**Athlete index:** https://www.meetscoresonline.com/Athletes.Index.aj-aja/29
**USA Gymnastics official results (elite/national):** https://usagym.org/results/2025/
**USA Competitions:** https://usacompetitions.com/results/
**MyMeetScores:** https://www.mymeetscores.com/

**Competitive levels in gymnastics:**
- Junior Olympic (JO) Levels 1-10 (compulsory levels 1-5, optional levels 6-10)
- Xcel program: Bronze, Silver, Gold, Platinum, Diamond, Sapphire (alternative pathway)
- Optional, Elite

**MeetScoresOnline:**
- A "free service for publishing live gymnastic results from ProScore, ScoreMaster, ScoreFlippers and other scoring software vendors"
- Maintains alphabetical index of all registered gymnastic athletes: Athletes.Index.{range}
- Meet results include: gymnast name, club, level, scores, date
- **Access:** "All Access Pass Required" for real-time live results. However, the alphabetical athlete index and historic results appear publicly accessible without login.
- **Individual athlete profiles:** Clickable from athlete index. Profiles aggregate results from multiple meets. Level progression visible if gymnast competed at multiple levels across years.
- **Volume:** Database covers JO levels and Xcel across all USA Gymnastics regions. No stated total athlete count found.
- **Years covered:** Not explicitly stated. Multiple years of meet results are archived.

**Key limitation:** MeetScoresOnline is a results-collection platform, not a longitudinal tracking system. Results are only present if the meet organizer uploaded to the platform. Coverage is not universal across all meets or all states. Bay Area local meets may or may not be in the database.

**USA Gymnastics official site:** Posts results for national championships and elite competitions only — not developmental JO Level 1-6 meets.

**Can we track individuals over time?** PARTIALLY. If a gymnast's meets are all uploaded to MeetScoresOnline, their career progression through levels is reconstructable. But coverage gaps exist for smaller/local meets.

**Bay Area specific:** No dedicated California or Bay Area gymnastics results portal found. ScoreCat Online (scorecatonline.com) offers "powerful data analytics platform that aggregates data from past seasons" with athlete performance comparisons — potentially useful.

**Development curve:** POSSIBLE but incomplete coverage. Unlike swimming, gymnastics does not have one national database capturing every competition. Meet-by-meet coverage is fragmentary.

---

## 5. Youth Soccer — GotSport/GotSoccer Rankings

**Rankings URL:** https://rankings.gotsport.com/
**Support page:** https://support.gotsport.com/what-are-the-gotsoccer-rankings

**What is it:** GotSport (formerly GotSoccer) is the dominant youth soccer tournament management platform. Rankings are compiled for competitive youth teams across US and Canada, age groups U10 through U19 boys and girls.

**What data exists:**
- Team rankings by age group and gender
- Teams accumulate points for winning games and competitions
- Player accounts contain: date of birth, school, jersey number, position
- Roster data maintained across years (teams must maintain same account to preserve history)

**Individual player tracking:** NOT available in public interface. GotSport is primarily a team management and tournament platform. Individual player profiles exist for college recruitment purposes ("college coaches can search for specific player profiles with multiple criteria and view results by state or specific tournament") but these are not public longitudinal records.

**Public or gated?** Team rankings are public. Individual player profiles are recruiter-facing and not publicly searchable.

**Development curve for individual children:** NO — GotSoccer does not provide a public database of individual child performance over time. It is a team management platform. Player data is siloed within team accounts.

**Alternative — SoccerWire:** soccerwire.com aggregates club rankings and tournament news but does not provide individual player data.

**Longitudinal research:** Academic research on "progression from youth to professional soccer" uses proprietary club data, not public databases (PubMed 33871087).

---

## 6. Water Polo — USA Water Polo

**Primary URL:** https://usawaterpolo.org/
**Junior Olympics page:** https://usawaterpolo.org/sports/2018/12/19/junior-olympics.aspx
**JO All-Americans 2025:** https://usawaterpolo.org/news/2025/10/7/general-2025-usa-water-polo-junior-olympics-all-americans-announced.aspx
**JO All-Americans 2024:** https://usawaterpolo.org/news/2024/9/17/general-2024-usa-water-polo-junior-olympics-all-americans-announced.aspx
**Stats platform:** https://6-8sports.com/

**Age divisions:**
- 10U, 12U, 14U, 16U, 18U (boys and girls)
- Junior Olympics covers 12U, 14U, 16U, 18U
- Club qualification through zone qualifying tournaments

**Bay Area clubs confirmed:**
- Monterey Bay United (MBU) Water Polo
- NorCal Aquatics (norcal-aquatics.com)
- California Water Polo Club (Cal Rep WPC)
- West Valley Water Polo
- SJA Water Polo Club

**What data is public:**
- Junior Olympics results (team standings, match results) posted annually on usawaterpolo.org
- All-American selections announced annually (name, club listed)
- 6-8 Sports platform used for live game stats during JO: parents can "fully stat their athletes during Junior Olympics using the 6-8 Mobile app"

**Individual player tracking:** No centralized public database of individual water polo player statistics across years or clubs. The 6-8 Sports platform provides live game statistics but these are not publicly archived in a searchable longitudinal format.

**Development curve for individuals:** NOT POSSIBLE from public data. Unlike swimming, water polo has no equivalent of SWIMS. Results are team-based (final scores, standings) not individual-stat based in public archives.

**The SHS water polo pipeline to Stanford:** Sacred Heart School (Atherton) water polo → Stanford commits. This pipeline is documented through school athlete commit lists (which we have in raw/athlete-commits/) but NOT through any public youth database. Individual water polo player development data before high school is not publicly tracked in a searchable national database.

---

## 7. Music — Certificate of Merit (CM) / MTAC / ABRSM

### 7A. Certificate of Merit (CM) — MTAC

**URL:** https://www.mtac.org/programs/cm/
**San Mateo branch (Bay Area):** https://mtacsanmateo.org/certificate-of-merit/
**FAQ:** https://www.mtac.org/programs/cm-faq/
**Online system:** new.mtac.org (members only)

**What is it:** CM is a standardized music curriculum and annual assessment program sponsored by the Music Teachers' Association of California (MTAC). Initiated in 1933. Approximately 30,000 students annually statewide.

**Levels:** Each instrument has a 10- or 11-level syllabus. Students progress level by level, evaluated annually between mid-February and March. Evaluation components: performance, technique, ear training, sight reading, written theory.

**Individual results:** All results are provided to the student and teacher in the MTAC Online System after evaluations complete. This is a private, teacher-facing portal — not a public searchable database.

**Public data:** NO public database of individual CM participants, their levels, or progression history exists. MTAC does not publish individual student results publicly.

**Development curve:** NOT POSSIBLE from public data. CM results exist only in the private MTAC Online System, accessible to participating teachers and students. There is no public equivalent of SWIMS or USCF for music.

**What IS public:** Branch-level statistics (total participants, pass rates by level) are sometimes published by local branches. The existence of CM certificates is public when students list them on resumes or applications. Level reached can be cited (e.g., "Level 10 CM certificate") but there is no database to verify or aggregate this.

---

### 7B. ABRSM (Associated Board of the Royal Schools of Music)

**URL:** https://www.abrsm.org/ (UK) / https://gb.abrsm.org/
**Portal:** https://portal.abrsm.org/

**What is it:** International music grading system (Grades 1-8 + Diploma levels) used globally. Widely used in Bay Area by piano, violin, and other instrument students as an alternative to CM.

**Grades:** Grades 1-8 practical (instruments and voice) + Grade 5-8 Theory. Diplomas (ARSM, DipABRSM, LRSM, FRSM).

**Individual results:** Available only through the ABRSM candidate portal (requires login with credentials provided at exam booking). Digital certificates downloadable from account. Results not public.

**Public database:** NO. There is no public searchable database of ABRSM candidates or their results.

**Development curve:** NOT POSSIBLE from public data. ABRSM results are strictly private, accessed only by the candidate and the booking teacher.

---

### 7C. MTAC Convention — Piano Competition Results

Some MTAC branches publish results from their annual competitions (Young Artists Guild, etc.) on branch websites. These are public but fragmentary — not a longitudinal database.

---

## 8. Chess — US Chess Federation (USCF)

**Primary ratings portal:** https://ratings.uschess.org/
**Player search (old format):** https://www.uschess.org/datapage/player-search.php
**New player search:** https://new.uschess.org/player-search
**Top 100 lists:** https://ratings.uschess.org/top100/RegularOverall
**Top players by state:** https://ratings.uschess.org/ranking
**Past event crosstables:** linked from ratings.uschess.org (Events tab)
**ChessGraphs (third-party):** https://www.chessgraphs.com/

**What is it:** The US Chess Federation maintains ratings for every member who plays in a sanctioned rated tournament. Ratings are published monthly.

**Volume:** 112,000 total USCF members as of 2024. Scholastic (K-12) players constitute a substantial portion — annual SuperNationals tournament drew 5,575 players in 2017.

**Rating types tracked per player:**
1. Regular (slow OTB)
2. Quick (OTB)
3. Blitz (OTB)
4. Online Regular
5. Online Quick
6. Online Blitz
7. Correspondence

**Youngest trackable age:** No minimum stated. USCF tracks players from first rated tournament regardless of age. A child's first rated tournament could be at age 5-6. Rating is determined by tournament results, not age.

**Search interface (verified via Chrome MCP live snapshot of ratings.uschess.org):**
- Search box: "Search name or ID..." (public, no login required)
- Tabs: All, Players, Events, Affiliates
- Advanced search: toggleable
- State filter available
- Rating range filter available
- Top 100 lists visible publicly (by state, age group, rating type)

**Player profile data (from ratings.uschess.org once player found):**
- Current ratings (all 7 types)
- Monthly supplement ratings history
- Tournament history: click any event to see rating report (before/after rating for that event)
- State/location listed
- Member since date shown
- Age/birthdate: The system uses birthdate to calculate age for Top 100 lists (age calculated as tournament end date - birth date / 365.25) — this information is in the system but display in public profiles is not fully confirmed.

**Historical data depth:** 
- Ratings data archived back to at least 2001 on the old archive (uschess.org/archive/ratings/)
- ChessGraphs.com: "data going all the way back to when international chess ratings began" for FIDE; USCF data from 2001 forward per FIDE sources, with older OlimpBase data going back further.
- Top 100 Age 7 and Under lists archived: confirmed URL pattern http://www.uschess.org/component/option,com_top_players/Itemid,371?op=list&month=2105&f=usa&l=R:Top+Age+7+and+Under shows age-7-and-under lists were published as far back as May 2021 at minimum (month=2105 = May 2021).

**Bay Area search:** YES — ratings.uschess.org has "Top Players By State" at ratings.uschess.org/ranking. Can filter by California. Cannot filter by city or club directly, but club/affiliate search exists separately (new.uschess.org/club-search-and-affiliate-directory).

**ChessGraphs.com:** Third-party tool that graphs USCF and FIDE rating history for any player over time. Free, public. Explicitly designed to show rating progression as a chart. If a child started playing at age 6 in 2012, ChessGraphs will plot their rating from first tournament to present.

**Can we track individuals over time?** YES — this is the most complete longitudinal individual development record after swimming. Every rated tournament game is permanently recorded. A player rated at age 5 who plays through age 18 has 13+ years of monthly rating snapshots and individual tournament results. ChessGraphs provides graphical visualization.

**Public or gated?** Fully public. No login required to look up any player's rating history.

**Scrapable?** Yes — the ratings system has a well-known URL pattern. No documented API but HTML is scrapable. The old archive (uschess.org/archive/ratings/) has static monthly files.

**Privacy considerations:** Player names, ratings, and tournament histories are fully public. Birthdates are used internally for age calculations but whether exact birthdate is exposed in public profiles is unclear — age group placement and "Top Age X" list inclusion implies birthdate is stored, but public display may be limited to year.

**KEY ANSWER — Individual development curve:** YES. Chess is arguably the most complete longitudinal youth development database available, second only to swimming in coverage. Unlike swimming (which requires participation in sanctioned meets), any rated USCF tournament counts. Bay Area has active scholastic chess programs, and Silicon Valley specifically produces nationally-ranked youth chess players.

---

## Cross-Database Comparison Summary

| Database | Youngest Age | Longitudinal? | Bay Area Filter | Public? | Individual Curve Possible? | Notes |
|----------|-------------|---------------|-----------------|---------|---------------------------|-------|
| USA Swimming SWIMS | 7 | YES — 1994-present | LSC = Pacific Swimming | YES (fully public) | YES — strongest | PROGRESSION button per swim; timestamps every meet |
| SwimCloud | 7 | YES | Club/team search | YES (with ToS limits) | YES | Best UI for club-level browsing |
| MySwimIO | 7 | YES | LSC/team search | YES | YES | Best analytics tools; "by age" comparison built in |
| USTA Junior Tennis | 8 | PARTIAL — 2001-present | NorCal section | PARTIAL (login for player lookup) | MANUAL only | Rolling 52-week window; no built-in career chart |
| askFRED (Fencing) | Y10 (est. age 9-10) | YES | NorCal division | PARTIAL (login for fencer search) | YES (with login) | Complete fencer result history |
| FencingTracker | Y10 | ~4 years | Club pages public | YES (fully public) | PARTIAL | 2021-2026 data; club pages for Peninsula FA, BAFC, SBFA confirmed |
| USCF Chess | Any (est. age 5+) | YES — 2001-present | By state (California) | YES (fully public) | YES — very strong | ChessGraphs provides visual rating history chart |
| USA Gymnastics / MeetScoresOnline | Level 1 (age ~6) | PARTIAL | No easy Bay Area filter | PARTIAL (paywall for live) | PARTIAL — coverage gaps | Not all meets uploaded; fragmented |
| GotSoccer / Soccer | U10 (age ~9-10) | NO | Team-level only | PARTIAL | NO | Team management platform, not individual tracking |
| USA Water Polo | 10U (age ~9-10) | NO | No national DB | NO | NO | No equivalent of SWIMS for water polo |
| CM (MTAC Music) | Level 1 (age ~5-6) | YES (private) | Bay Area branches exist | NO — private portal | NO | Private MTAC system only; ~30,000 CA students/year |
| ABRSM Music | Grade 1 (age ~6-7) | YES (private) | N/A | NO — private portal | NO | Candidate portal only; globally ~650,000 exams/year |

---

## Actionable Research Directions

**Highest-value databases for building K-8 development curves:**

1. **USA Swimming SWIMS (via data.usaswimming.org):** Name-based search returns complete career record. LSC filter = Pacific Swimming isolates Bay Area. Age-7 data available. 376,000 current members, 32 years of data. Zero barrier to public access. MySwimIO provides "by age" analytics without scraping.

2. **USCF Chess (via ratings.uschess.org + ChessGraphs.com):** 112,000 members. Every rated tournament permanently recorded. ChessGraphs plots visual rating history for any player. Top 100 by age lists published monthly (Age 7 and Under, Age 8 and Under, etc.). California filter available. Zero barrier to public access.

3. **FencingTracker (via fencingtracker.com):** Fully public club pages for Peninsula Fencing Academy, Bay Area Fencing Club, and South Bay Fencing Academy. 4 years of results (2021-2026). Individual fencer results trackable by name. Useful for the narrow population of Bay Area fencers.

**Key limitation across all sports:** These databases track children who are already competing at a club/competitive level. They systematically miss recreational participants, late starters, and children whose parents do not enroll them in competitive programs. The databases are therefore not representative samples — they are samples of children whose parents made the decision to invest in competitive participation. This selection bias is significant for any study of Bay Area private school families.

**Privacy note:** All public databases display child athletes by full name linked to performance data, club affiliation, and dates. Ages are derivable from age-group data. Exact birthdates are stored in these systems (required for age certification) but may not be directly exposed. Scrapers should be aware of COPPA implications for children under 13 and applicable terms of service.

---

## Sources

Search queries run:
1. "USA Swimming database SwimCloud individual swimmer progression times age club search"
2. "USTA junior tennis rankings database individual player progression 12U 14U 16U 18U search"
3. "askFRED fencing results database individual fencer progression age category club affiliation"
4. "USA Gymnastics meet results database individual gymnast level progression age scores public"
5. "SwimCloud Bay Area club teams search Pacific Swimming LSC swimmer profiles public"
6. "USCF chess rating database individual player progression age history uschess.org public search"
7. "Certificate of Merit MTAC music assessment California results database student progression level"
8. "USA Water Polo junior olympics results database individual player club progression public"
9. "SwimmingRank.com individual swimmer ranking age group time tracking features"
10. "Palo Alto Stanford Aquatics PAST SwimCloud team Bay Area swimmers public profile"
11. "ABRSM exam results individual student public lookup certificate music grading UK international"
12. "GotsoccerRankings youth soccer individual player tracking longitudinal age progression club"
13. "GotSoccer player profile individual history tournament results age progression public database"
14. "fencingtracker.com individual fencer results history club Bay Area Peninsula Fencing Academy"
15. "USA gymnastics JO meet results individual gymnast level 1-10 scores database MeetScoresOnline searchable"
16. "USA Water Polo 14U 12U junior development results database individual player Bay Area club"
17. "USTA junior tennis player profile search by state club section Northern California age group rankings public"
18. "USA swimming total registered members volume statistics 400000 age group breakdown 2024 2025"
19. "USCF total registered members youth chess players statistics 2024 2025 scholastic players"
20. "youth sports database privacy COPPA individual child performance data public searchable concerns scraping"
21. "SwimCloud API scraping terms of service USA swimming data access developer"

Live interface verification (Chrome MCP):
- data.usaswimming.org/datahub/usas/individualsearch — confirmed name-only search fields
- data.usaswimming.org/datahub/usas/timeseventrank — confirmed Age Group options (7, 8, 9...18), LSC dropdown with "Pacific Swimming," years 1994-2026
- data.usaswimming.org/datahub/usas/individualsearch/times — confirmed data fields: Event, Swim Time, Age, Points, Time Standard, Meet, LSC, Team, Swim Date; confirmed PROGRESSION button per swim record
- ratings.uschess.org — confirmed public search, state filter, Top 100 lists, latest rated events

Source URLs referenced:
- https://data.usaswimming.org/datahub/usas/individualsearch
- https://data.usaswimming.org/datahub/usas/timeseventrank
- https://www.usaswimming.org/about-usas/resources/swims-database
- https://www.swimcloud.com/team/8015/ (Palo Alto Stanford Aquatics)
- https://swimstandards.com/clubs/pc/palo-alto-stanford-aquatics
- https://www.myswimio.com/
- https://swimswam.com/usa-swimming-membership-stays-stable-in-2024-predicting-post-olympic-growth-for-2025/
- https://www.pacswim.org/swim-clubs
- https://www.usta.com/en/home/play/rankings.html
- https://tennislink.usta.com/tournaments/rankings/rankinghome.aspx
- https://www.ustanorcal.com/
- https://www.askfred.net/
- https://www.askfred.net/results/fencer
- https://fencingtracker.com/
- https://fencingtracker.com/club/100128001/PeninsulaFA/results
- https://fencingtracker.com/club/100314997/BAFC/results
- https://fencingtracker.com/club/100274397/SBFA/results
- https://www.norcalfence.org/clubs-division
- https://www.meetscoresonline.com/
- https://www.meetscoresonline.com/Athletes.Index.aj-aja/29
- https://usagym.org/results/2025/
- https://home.gotsport.com/rankings/
- https://rankings.gotsport.com/
- https://usawaterpolo.org/sports/2018/12/19/junior-olympics.aspx
- https://usawaterpolo.org/news/2025/8/6/general-2025-junior-olympics-complete-with-champions-crowned.aspx
- https://www.mtac.org/programs/cm/
- https://mtacsanmateo.org/certificate-of-merit/
- https://www.abrsm.org/en-gb/about-our-exams/results-and-certificates/
- https://new.uschess.org/players/search
- https://ratings.uschess.org/
- https://www.chessgraphs.com/
- https://en.wikipedia.org/wiki/United_States_Chess_Federation
- https://pypi.org/project/SwimScraper/
- https://github.com/alexkgrimes/swimulator
- https://www.usaswimming.org/about-usas/resources/swims-database/3rd-party-vendors
- https://www.swimcloud.com/terms/
