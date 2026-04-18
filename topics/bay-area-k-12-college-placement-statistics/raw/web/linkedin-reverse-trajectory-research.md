---
title: Reverse Trajectory Research — LinkedIn, Competition Databases, and Public Records
created: 2026-04-18
research_agent: research-agent
queries_run:
  - "LinkedIn high school college students profile list activities awards public search 2025"
  - "LinkedIn scraping legality hiQ v LinkedIn 2022 2023 public profiles CFAA ruling"
  - "USAMO qualifier list public database school name student name AMC competition results archive"
  - "Regeneron STS finalists list public name school college enrollment tracking"
  - "Stanford MIT Harvard student directory searchable public 2024 2025"
  - "MATHCOUNTS national competition results public database name school state"
  - "college newspaper mentions high school competition winners USAMO Stanford Harvard enrollment profiled"
  - "USAMO qualifiers college enrollment statistics MIT Stanford Harvard Putnam competition pipeline data"
  - "LinkedIn people search Harker School education filter students alumni public profiles 2024"
  - "Google Scholar student research trajectory high school Intel STS Regeneron college lab publication continuity"
  - "IPEDS USAMO state aggregate pipeline analysis California math competition Stanford MIT enrollment data"
  - "LinkedIn Terms of Service scraping automated data collection 2024 prohibited user agreement"
  - "GDPR CCPA scraping student profiles LinkedIn privacy minors education data legal risk"
  - "AoPS Art of Problem Solving profile student competition results college destination database"
  - "Stanford class of 2027 OR class of 2028 high school listed student org members public roster"
  - "college newspaper Stanford Daily Harvard Crimson USAMO winner profile high school background article"
  - "site:thecrimson.com USAMO high school student profile math olympiad"
  - "Harker School Stanford admitted students LinkedIn profile K-12 activities competitions trajectory"
  - "Regeneron STS finalist college choice data aggregate analysis where do they enroll"
reliability_tier: L2-authoritative (legal and court documents), L3-aggregator (platform help pages, competition archives), L4-community (forums)
topic: Reverse-engineering K-12 student development trajectories from known college enrollment outcomes
---

# Reverse Trajectory Research: Working Backward from College Outcomes to K-12 Development Arcs

## Research Question

Given a known output — e.g., "34 students from Harker went to Stanford in 2023-2025" — can we identify those students on LinkedIn or other public platforms and reconstruct what their K-12 development arc looked like? This document inventories each major approach, its legal/ethical standing, data yield, and operational feasibility.

---

## Approach 1: LinkedIn as a Trajectory Source

### What LinkedIn Profiles Contain

High school students and recent college graduates are widely advised to list high school education, K-12 extracurricular activities, awards, and competitions on their LinkedIn profiles. Guidance from college counseling platforms (CollegeVine, Appily, ProResource, Transizion) confirms the following fields are commonly populated:

- **Education section**: High school name, graduation year, GPA (optional)
- **Honors & Awards**: National Merit Scholar, USAMO, Regeneron STS, Dean's List, All-State athletics, Eagle Scout, essay contest prizes
- **Activities & Societies**: Extracurricular clubs, sports, student government, math circles (500-character field)
- **Projects**: Independently built software, fundraising drives, research projects
- **Volunteer Experience**: Community service, tutoring
- **Publications**: Research papers submitted to journals (e.g., Journal of Emerging Investigators)

Advice from these platforms is consistent: "At the end of each school year, update your profile — add new awards, extracurriculars, internships, jobs, volunteer work, skills, courses, and projects." This means profiles are intended to capture the full K-12 trajectory, not just post-college activity.

### Manual Search Method (Confirmed Working)

A Google search for `LinkedIn "Harker School" "Stanford University"` returned a direct result set including named profiles. Confirmed results from this query:

- Linda Zeng — Education: Harker School → Stanford University (public profile)
- Disha Gupta — Education: Harker School → Stanford University (public profile)
- Ananya Pradhan — Education: Harker School → Stanford University School of Medicine (public profile)

LinkedIn's own Alumni tool at `linkedin.com/school/the-harker-school/people` allows filtering by:
- Where they went (college attended)
- Where they live (current location)
- What they do (industry/function)

**Standard LinkedIn search returns are capped at 1,000 profiles per query** (confirmed by LinkedIn Help documentation). For a school like Harker with ~2,040 total students and multiple graduating classes, the pool of profiles with both Harker and Stanford in their education history is likely 50-200 across all years, well within the 1,000-result cap.

### Privacy Architecture on LinkedIn

LinkedIn provides two view modes:
1. **Public view** (no login required): Name, headline, summary, education institutions listed, general location
2. **Stanford and Affiliates view** (requires SUNet ID login for StanfordWho): Full contact data, specific graduation year, department

For the reverse-trajectory purpose, the public view already yields: high school name, college attended, and often activities/awards if the user has populated them. Login-only data is not accessible without an account.

**Limitation:** LinkedIn was founded in 2003. Students who graduated from high school before ~2010 have much lower profile completion rates. Students who graduated 2015-present are increasingly likely to have populated profiles.

**Another limitation:** If a student has not selected their school from the dropdown in the Education section and instead typed a freeform entry, the school logo does not appear and the profile may not surface in school-filtered searches.

### Legal Status of LinkedIn Scraping

**Court ruling (CFAA layer):** In *hiQ Labs, Inc. v. LinkedIn Corp.* (9th Circuit, 2022), the court reaffirmed its 2019 ruling that automated scraping of **publicly accessible** LinkedIn data does not violate the Computer Fraud and Abuse Act (CFAA). The core holding: the CFAA's prohibition on accessing a computer "without authorization" applies only when a person circumvents access control mechanisms. Public profiles have no such controls. The Supreme Court remanded the case in 2021 following *Van Buren v. United States*, and the 9th Circuit reaffirmed the narrow CFAA interpretation in April 2022. The case ended with a settlement in December 2022 that did not disturb the legal principle.

**Terms of Service layer (separate from CFAA):** LinkedIn's User Agreement explicitly prohibits:
- Using "crawlers, bots, browser plugins and add-ons, or any other technology to scrape the Services or otherwise copy profiles"
- Automated crawling and indexing without LinkedIn's express permission
- Renting, leasing, or selling any data collected

Violation results in "immediate ban from all LinkedIn websites, products, and services." This is a **contractual** prohibition, not a criminal one under CFAA. LinkedIn can (and does) terminate accounts and send cease-and-desist letters.

**Privacy law layer (GDPR/CCPA/COPPA):**
- GDPR and CCPA treat scraped personal data as "processing," requiring transparency, consent, and compliance with deletion requests
- French data protection authority (CNIL) fined KASPR €240,000 for collecting LinkedIn data without consent, even though the data was publicly visible
- COPPA (Children's Online Privacy Protection Act) applies to users under 13; LinkedIn's minimum age is 16 in most jurisdictions, 13 in the US. However, high school students who created profiles at 15-16 may have been minors at time of data creation — scraped profiles of those users carry heightened legal risk
- California's CCPA grants residents the right to know what data is collected about them and to request deletion

**Summary — legal risk matrix for LinkedIn:**

| Action | CFAA | ToS | GDPR/CCPA | Risk Level |
|--------|------|-----|-----------|------------|
| Manual browsing public profiles | No violation | Allowed | Generally OK for personal use | Low |
| Manual copy/paste into spreadsheet (small scale) | No violation | Gray area | Gray area | Low-Medium |
| Automated scraping of public profiles | No violation | Clear violation | Likely violation | High |
| Scraping behind login wall | Likely violation | Clear violation | Clear violation | Very High |

**Practical conclusion:** Manual, one-by-one human review of public LinkedIn profiles is the lowest-risk method. It is slow (estimate: 5-15 minutes per profile for full extraction) but legally defensible for personal research. Automated scraping carries ToS and privacy law risk even though the CFAA no longer prohibits it for public data.

### LinkedIn Alternatives

- **Handshake** (handshake.com): College-focused career platform. Students list high school, GPA, activities. Profiles are generally visible only within a college's network, not publicly searchable by outsiders.
- **College-specific directories**: StanfordWho (Stanford's internal directory) is split into a public view (name, title, department) and a restricted view requiring a SUNet ID. Harvard has `directory.harvard.edu`. Neither lists high school backgrounds.
- **Student organization public rosters**: Some student clubs at Stanford, MIT, Harvard post public member lists on their websites (e.g., Stanford Math Club, Harvard College Mathematics Association). These list current students but rarely include high school backgrounds.

---

## Approach 2: Cross-Referencing Competition Results with College Enrollment

### USAMO Qualifier Lists

USAMO qualifier lists are published publicly by the Mathematical Association of America (MAA) as PDF documents. Confirmed data fields in these public documents:

- First initial + last name (NOT full first name in most recent lists — this is a key limitation)
- School name
- School state
- Grade (in some older lists, e.g., 2009 list)

Archived copies are available on:
- Art of Problem Solving download server (direct PDF links)
- Scribd document repositories (2022, 2021 lists confirmed)
- MAA.org (official source)
- Metroplex Math Circle (older lists, e.g., 2009)

**Scale:** Approximately 250-500 students qualify for USAMO/USAJMO combined each year. The 2022 list confirms this format.

**The identification problem:** Because recent lists show only first initial + last name, a student listed as "J. Zhang, Harker School, CA" cannot be uniquely identified from the list alone. Common surnames (Zhang, Wang, Li, Chen) at the same school may have multiple matches. However:
- If the school is small (e.g., only 1-2 students with surname Zhang at Harker), the identification may be feasible
- Cross-referencing with AoPS forum posts (where students often post under their full name alongside competition context) can resolve ambiguity
- Older lists (pre-2015) sometimes included full first names

**AIME qualifier lists:** Available from attach.seedasdan.com for 2022, showing name + school + state. The AIME list is larger (~10,000 students) and thus less useful for individual identification but excellent for aggregate school-level analysis.

**USAMO + College Enrollment Cross-Reference Feasibility:**

A student who qualifies for USAMO in year Y would typically enroll in college in year Y or Y+1. If the USAMO list says "J. Chen, Harker School, CA" and the researcher can identify "Jeremy Chen, Harker '22, Stanford '26" on LinkedIn, the USAMO qualification can be added to that student's trajectory record.

**Acceptance rate data (aggregate, not individual):** Research from multiple sources converges on:
- USAMO qualifiers: MIT acceptance rate >50% vs. ~7% overall
- MOP participants (top ~60 USAMO scorers): MIT acceptance rate >60%
- Harvard: approximately 3-7% of USAMO qualifiers matriculate there in any given year
- Single incoming class at MIT or Harvard typically includes 3-12 students with USAMO/IMO credentials

### Regeneron Science Talent Search (STS) Lists

The Society for Science publishes full finalist information publicly on societyforscience.org. Confirmed data fields for finalists (top 40):

- **Full name** (not just initial)
- Age
- City and state
- School name
- Project title and description

Scholar lists (top 300) are also published as PDFs and include name + school. Example: 2026 finalists include Colin Jie Chu, 18, Palo Alto (school identified as Gunn High School based on Palo Alto location and prior research).

**Cross-referencing STS with college enrollment:**

Because STS finalists are identified by full name (unlike USAMO which uses first initial), the identification pipeline is more tractable:

1. Pull finalist name from societyforscience.org (e.g., "Kevin Lu, Santa Clara, CA")
2. Search LinkedIn for "Kevin Lu" + Santa Clara + CS
3. Check if LinkedIn profile lists high school and college
4. If not found on LinkedIn, Google "[full name] [high school] [college]"
5. Check college newspaper archives (Crimson, Stanford Daily, The Tech at MIT) for profiles

**Publication continuity (Google Scholar approach):**

STS projects are research papers. Students who did lab-based STS research often continue publishing in college. Workflow:
1. Get student name + STS project title from societyforscience.org
2. Search Google Scholar for student name + keywords from project title
3. If found: publication record shows high school project → college lab → publications
4. This method works best for wet-lab biology/chemistry projects with publishable data

**Limitation:** Computer science and math projects (increasingly common in STS) produce algorithms and proofs that often are not published in searchable journals. The Scholar approach works better for life sciences.

### MATHCOUNTS National Competition

MATHCOUNTS Foundation publishes national competition results at mathcounts.org, with historical data on the AoPS Wiki at artofproblemsolving.com/wiki/index.php/MATHCOUNTS_historical_results.

Data fields available:
- Individual and team champions: full name + school + state
- Top scorer lists: vary by year, some include all top-25 individuals with school
- Annual competition highlights pages list winners by name

**Key characteristic:** MATHCOUNTS is a middle school competition (grades 6-8). A student winning MATHCOUNTS Nationals in 2018 would typically be entering high school in 2018-2019 and graduating college ~2026. This is the furthest back point in the K-12 trajectory.

**Cross-reference feasibility:** Because MATHCOUNTS champions are named fully and their school is listed, they can be tracked forward:
- Search "[student name] [school name]" on LinkedIn
- Search for the same name in USAMO/AIME lists 4-6 years later (cross-competition continuity)
- Search "[student name] MATHCOUNTS" on Google for any subsequent press coverage

AoPS community profiles are also valuable: many MATHCOUNTS competitors create AoPS accounts under their real names and post competition scores, high school activity, and eventually their college.

---

## Approach 3: University Directories and Public Student Lists

### Stanford

- **StanfordWho** (stanford.edu/uit/service/stanfordwho): Publicly accessible name/title/department search. Does **not** include high school attended. Restricted view (requires SUNet ID) adds contact information but still not high school.
- **Stanford Profiles** (profiles.stanford.edu): Faculty, postdocs, students, and staff. Includes publications and research interests. No high school field.
- **Alumni directory** (alumni.stanford.edu): Requires Stanford login to search.

### Harvard

- **Harvard Directory** (directory.harvard.edu): Listed as publicly accessible. Does **not** include high school. Beta version described as "richer, interactive site including user-generated content."
- **Meet Our Students** (college.harvard.edu/student-life/meet-our-students): Curated spotlights, not a searchable directory.
- **Alumni directory** (alumni.harvard.edu): Requires Harvard login.

### MIT

No public student directory equivalent to StanfordWho was found in search results.

### Assessment

University directories are not useful for the reverse-trajectory method. They do not contain high school data, and the more detailed alumni directories require institutional login credentials that external researchers do not have.

### Student Organization Rosters

Some college student clubs post public member lists on their websites. Examples to check:
- Stanford Math Club
- Harvard College Mathematics Association (HCMA)
- MIT Math Club
- Science olympiad chapters at each university

These may list current students who were competition winners in high school, but typically do not include high school affiliation. They are useful for confirming enrollment (a student listed as an HCMA officer is confirmed enrolled at Harvard) but do not add high school context.

---

## Approach 4: College Newspaper Archive Mining

### Methodology

If a student achieved a notable result in high school (USAMO winner, Regeneron STS finalist, national science fair winner), there is a non-trivial probability they were profiled in:
1. Their high school's local press at the time of achievement
2. Their college's newspaper when they enrolled (especially for award winners)
3. National STEM coverage outlets

**Confirmed examples from search:**

A 1996 Harvard Crimson article ("Breaking the Curve") profiles a student who "won first place in the United States Math Olympiad as a high school sophomore and subsequently represented the U.S. in international competition in Beijing." The article identifies the student by name, their college (Harvard), their major (math and physics), and their high school achievement trajectory — exactly the data structure sought.

The 2010 USAMO Winner Biographies page (metroplexmathcircle.wordpress.com) lists full name, high school, and biographical details for each winner. This type of content connects name → high school → achievement and (when combined with a LinkedIn search for the same name) enables full trajectory reconstruction.

**Search pattern for college newspaper mining:**

```
site:thecrimson.com "[student full name]"
site:stanforddaily.com "[student full name]"
site:thetech.mit.edu "[student full name]"
site:yaledailynews.com "[student full name]"
```

Where student names are drawn from:
- USAMO winner lists (which do provide full names for award winners, even if qualifier lists show only initials)
- Regeneron STS finalist lists (full names always)
- MATHCOUNTS national champion lists

**Evan Chen case study:** Evan Chen's personal website (web.evanchen.cc/history.html) is a self-published K-12 math trajectory document showing his competition history from 2010-2014, his Berkeley Math Circle mentorship, and his subsequent enrollment at MIT. This type of self-published record is common among high-achieving math students who maintain personal websites. It is fully public and highly informative.

**Scale estimate:** College newspaper archives are searchable but coverage is sparse. For any given USAMO qualifier, the probability of a college newspaper profile is perhaps 5-15%. For IMO team members (top 6 from USAMO), probability is higher (30-50% based on the national significance of the achievement).

---

## Approach 5: Google Scholar and Research Database Tracing

### STS Research → College Publication Pipeline

Workflow:
1. Obtain STS finalist name + project title from societyforscience.org
2. Search Google Scholar: `[author name] [3-4 keywords from project title]`
3. If student published high school project as a paper, Scholar may show it
4. Check the author's affiliation field — if they are now in college, the college affiliation appears on subsequent papers
5. The citation trail establishes: high school project (year Y) → college affiliation (year Y+1 or Y+2) → research continuity

**What this produces:** For students who continued publishing in college, this method yields:
- High school project domain (biology, chemistry, CS, physics, math)
- College enrolled at (from affiliation field on new papers)
- Whether they continued in the same research area
- Lab/mentor connections (if co-authors are college professors)

**Limitation — CS and math students:** Algorithm and proof-based STS projects often do not result in journal publications. This approach has stronger coverage for wet-lab biology and chemistry projects. For the Bay Area private school context (Harker, Nueva, Menlo, Castilleja), where CS projects are frequent, Google Scholar tracing will miss a significant fraction of STS participants.

**ORCID IDs:** Some undergraduate researchers create ORCID (Open Researcher and Contributor ID) profiles. These are publicly searchable and often list both high school and college affiliations in the employment/education fields if the researcher populated them. Less common than LinkedIn for this age cohort, but valuable when present.

---

## Approach 6: Aggregate Pipeline Analysis (No Individual Identification)

### Methodology

Without identifying any individual, it is possible to characterize the pipeline from specific high schools or specific competitions to specific colleges using:

**A. USAMO qualifier lists × school enrollment records:**
- USAMO lists by year show school name and state
- Count: how many USAMO qualifiers came from California schools each year?
- Which California schools are overrepresented?
- Use MAA's published lists (2009-2025 available) to compute school-level USAMO production

**B. IPEDS data:**
- IPEDS (nces.ed.gov/ipeds) collects institution-level enrollment data from all US postsecondary institutions
- Stanford IPEDS data (ID 243744 confirmed in search results) includes enrollment by state of origin, but NOT by high school attended
- IPEDS cannot directly link K-12 schools to colleges; it only shows geographic and demographic breakdowns

**C. College Common Data Sets:**
- Each college publishes a Common Data Set annually with detailed admissions and enrollment statistics
- Stanford's is available at irds.stanford.edu/data-findings/cds
- CDS does not include high school-level breakdowns

**D. Competition-to-competition longitudinal tracking (aggregate):**
- If a student appears on MATHCOUNTS state list in year Y and on USAMO list in year Y+4, and again on STS finalist list in year Y+5, this shows a competition progression pattern at the aggregate level
- Analysis: For California students on the 2018 MATHCOUNTS state list, what fraction appeared on a 2022 or 2023 USAMO list? This is feasible from public data without individual identification.

**What aggregate analysis cannot answer:** The specific role of high school environment (private vs. public, specific school culture) versus individual innate ability versus external enrichment (math circles, tutoring, AoPS). Aggregate data conflates all these.

**California-specific aggregate data available:**
- MATHCOUNTS California (cspeef.org) posts state competition results
- AMC/AIME qualifiers by school are available from AoPS community posts and school press releases
- Harker's own publications (Facts & Stats page) report: "In 2019, Harker had 7 Regeneron STS semifinalists — most in California"
- Crystal Springs, Castilleja, Nueva, Menlo school profiles (available in this topic's raw files) contain similar aggregate competition statistics

---

## Test Case: Harker School → Stanford, Class of 2027

**Starting data available:** Harker School college profile states approximately 9.67% of graduates go to HYPSM. With roughly 180 graduates per year, that is ~17-18 students per year to HYPSM. Stanford alone might receive 8-12 per year based on Harker's published statistics.

**Step 1 — LinkedIn search:**
Query: `site:linkedin.com "Harker School" "Stanford University" "class of 2027"` OR use LinkedIn alumni tool at linkedin.com/school/the-harker-school/people, filter by "attended Stanford."

Confirmed result: The query `LinkedIn "Harker School" "Stanford University"` returned named profiles including Linda Zeng, Disha Gupta, Ananya Pradhan (all Harker → Stanford). These are real, publicly indexed profiles.

**Step 2 — Profile extraction (manual):**
For each profile found, record:
- Activities & Societies listed under Harker entry
- Honors & Awards
- Projects listed
- Timeline (graduation year)

**Step 3 — Competition cross-reference:**
For each name extracted, search:
- USAMO/USAJMO qualifier PDFs for matching initial + surname + school
- Regeneron STS scholar/finalist lists for full name match
- MATHCOUNTS historical results on AoPS Wiki for middle school results
- Google: "[full name] [high school] competition" for press coverage

**Step 4 — College newspaper check:**
Search `site:stanforddaily.com "[student name]"` for any profile article mentioning high school background.

**Expected yield per student:** 30-60 minutes of manual work. Expected data completeness: 40-70% of profile fields (many students do not list all activities on LinkedIn; competition databases use initials only for USAMO). Expected number of recoverable profiles from one graduating class at one school: 5-15 out of perhaps 10-12 Harker→Stanford students.

---

## Summary Matrix

| Approach | Legal/Ethical | Profiles Achievable | Data Fields | Manual vs. Automated | Completeness |
|----------|--------------|--------------------|--------------|-----------------------|--------------|
| LinkedIn manual browse | Low risk (ToS allows manual) | 50-200 per school × year | High school, college, activities, awards | Manual only; ~15 min/profile | 40-70% field coverage |
| LinkedIn automated scraping | High risk (ToS + GDPR) | Theoretically 1,000/query | Same as above | Automated possible; legally risky | 40-70% field coverage |
| USAMO list cross-ref | No risk (public docs) | 250-500/year nationally | Initial, surname, school, state | Semi-automated | Low (initials only, no college destination) |
| Regeneron STS cross-ref | No risk (public docs) | 40-300/year nationally | Full name, school, project | Semi-automated | Medium (full name but college not listed) |
| MATHCOUNTS cross-ref | No risk (public docs) | Top-25 nationally/year | Full name, school, state | Semi-automated | Low (middle school only; no college) |
| Google Scholar tracing | No risk | ~30% of STS bio/chem finalists | Research trajectory, college affiliation | Semi-automated | Medium-high for life sciences; low for CS/math |
| College newspaper mining | No risk | ~5-15% of USAMO winners | Full narrative trajectory | Manual; ~30 min/student | High when found |
| University directories | No risk | Not applicable | No high school field | N/A | Zero for K-12 data |
| Aggregate IPEDS/CDS analysis | No risk | Entire cohorts | School-level, no individuals | Semi-automated | Medium for aggregate; zero for individual |

---

## Key Findings and Data Gaps

**What is feasible at small scale (individual research):**

1. Manual LinkedIn browsing of Harker → Stanford public profiles, recording listed activities and awards. Yields 5-15 profiles per graduating class. Time: 2-4 hours per school per cohort year.

2. Cross-referencing full-name competition lists (Regeneron STS, MATHCOUNTS champions, USAMO award winners — who get full names — not just qualifiers) with LinkedIn profiles. Yields trajectory data for the most distinguished achievers.

3. College newspaper archive searches for named individuals from Regeneron STS finalist lists. Yields narrative profiles but sparse coverage.

**What is infeasible without automation:**

Systematically reconstructing trajectories for all 34 Harker→Stanford students in a given year. At 30-60 minutes per student, that is 17-34 person-hours of manual work for one school-to-college pair.

**What is not available in public records:**

- SAT/ACT scores (private)
- GPA (rarely on LinkedIn; not in any public database)
- Specific course sequences (e.g., AP Calculus BC in 9th grade) — not in any public database
- Private school admissions decisions (which schools each student applied to and was rejected from)
- Financial aid data (private)
- College counselor guidance received (private)

**The critical gap:** USAMO qualifier lists use first initial + last name only (not full first name). This makes individual identification ambiguous for common surnames at large schools. The workaround is AoPS forum posts, where students often post under their full name with competition context, but this is not systematic.

**Most information-dense single source:** LinkedIn profiles of students who were Regeneron STS finalists, because (1) STS lists provide full name, enabling LinkedIn lookup, (2) STS finalists are likely to have created LinkedIn profiles (high professional self-awareness), and (3) STS finalists' LinkedIn profiles are likely to be well-populated with competition history given their research-oriented backgrounds.

---

## Sources

- [hiQ Labs v. LinkedIn — Wikipedia](https://en.wikipedia.org/wiki/HiQ_Labs_v._LinkedIn)
- [Ninth Circuit Holds Data Scraping is Legal — California Lawyers Association](https://calawyers.org/privacy-law/ninth-circuit-holds-data-scraping-is-legal-in-hiq-v-linkedin/)
- [hiQ v. LinkedIn Wrapped Up: Web Scraping Lessons Learned — ZwillGen](https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/)
- [LinkedIn's Data Scraping Battle with hiQ Labs Ends — Privacy World](https://www.privacyworld.blog/2022/12/linkedins-data-scraping-battle-with-hiq-labs-ends-with-proposed-judgment/)
- [9th Circuit Opinion — cdn.ca9.uscourts.gov](https://cdn.ca9.uscourts.gov/datastore/opinions/2022/04/18/17-16783.pdf)
- [EFF: Victory! Ruling in hiQ v. LinkedIn Protects Scraping of Public Data](https://www.eff.org/deeplinks/2019/09/victory-ruling-hiq-v-linkedin-protects-scraping-public-data)
- [LinkedIn Prohibited Software and Extensions](https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions)
- [LinkedIn Crawling Terms and Conditions](https://www.linkedin.com/legal/crawling-terms)
- [Is LinkedIn Scraping Legal? — PhantomBuster Blog](https://blogv2.phantombuster.com/blog/linkedin-automation/is-linkedin-scraping-legal/)
- [Is It Legal to Scrape LinkedIn? — MagicalAPI](https://magicalapi.com/blog/linkedin-tools-insights/is-it-legal-to-scrape-linkedin/)
- [GDPR CCPA Web Scraping Compliance — tendem.ai](https://tendem.ai/blog/is-web-scraping-legal-compliance-overview)
- [LinkedIn Profile Tips for High School Students — Judy Schramm](https://www.linkedin.com/pulse/linkedin-profile-tips-high-school-students-judy-schramm)
- [LinkedIn for High School Students — CollegeVine Blog](https://blog.collegevine.com/how-to-use-linkedin-in-high-school)
- [LinkedIn for High School Students — Appily](https://www.appily.com/guidance/articles/academics-college-readiness/linkedin-for-high-school-students)
- [Search for classmates on LinkedIn — LinkedIn Help](https://www.linkedin.com/help/linkedin/answer/a524061)
- [The Harker School: Alumni and Graduates — LinkedIn](https://www.linkedin.com/school/the-harker-school/people)
- [2022 USAMO Qualifiers List — AoPS download](https://services.artofproblemsolving.com/download.php?id=YXR0YWNobWVudHMvYy8wLzZjMjhjYTFiODUwNzBjNzY2YzIzN2E2OGJmZmI5YjlhZWNhMjA1LnBkZg%3D%3D&rn=MjAyMiBVU0FNTyBRdWFsaWZpZXJzLnBkZg%3D%3D)
- [2022 USAJMO Qualifiers List — Scribd](https://www.scribd.com/document/584888830/2022-USAJMO-Qualifiers)
- [2024 USAMO Awardees and Results — Scribd](https://www.scribd.com/document/733275791/2024-USAMO-Awardees-docx-1)
- [United States of America Mathematical Olympiad — Wikipedia](https://en.wikipedia.org/wiki/United_States_of_America_Mathematical_Olympiad)
- [MAA Introduces Official Competition Sites for 2026 USAMO and USAJMO](https://maa.org/news/maa-introduces-official-competition-sites-for-the-2026-usamo-and-usajmo/)
- [2010 USAMO Winner Biographies — Metroplex Math Circle](https://metroplexmathcircle.wordpress.com/2010/05/20/2010-usamo-winner-biographies/)
- [2024 Regeneron STS Finalists — Society for Science](https://www.societyforscience.org/regeneron-sts/2024-finalists/)
- [2023 Regeneron STS Finalists — Society for Science](https://www.societyforscience.org/regeneron-sts/2023-finalists/)
- [2026 Regeneron STS Finalists — Society for Science](https://www.societyforscience.org/regeneron-sts/2026-finalists/)
- [Regeneron STS 2023 Finalists PDF — Society for Science](https://sspcdn.blob.core.windows.net/files/Documents/SEP/STS/2023/Program-Books/Finalist.pdf)
- [Regeneron Science Talent Search — Wikipedia](https://en.wikipedia.org/wiki/Regeneron_Science_Talent_Search)
- [Regeneron STS 2026 Top Awards — Society for Science Blog](https://www.societyforscience.org/blog/regeneron-sts-2026-top-awards/)
- [MATHCOUNTS Historical Results — AoPS Wiki](https://artofproblemsolving.com/wiki/index.php/MATHCOUNTS_historical_results)
- [NATIONAL COMPETITION PARTICIPANTS — MATHCOUNTS Foundation](https://mathcounts.org/programs/national-competition-participants)
- [2024 RTX MATHCOUNTS National Competition Highlights](https://www.mathcounts.org/programs/2024-rtx-mathcounts-national-competition-highlights)
- [StanfordWho — Stanford University IT](https://uit.stanford.edu/service/stanfordwho)
- [Stanford Profiles](https://profiles.stanford.edu/)
- [Directory — Harvard University](https://www.directory.harvard.edu/)
- [Alumni Directory — Stanford Alumni Association](https://alumni.stanford.edu/help/directory/)
- [Breaking the Curve — The Harvard Crimson (1996)](https://www.thecrimson.com/article/1996/6/6/breaking-the-curve-pbibm-statistically-significant/)
- [Evan Chen Math Contest History — personal site](https://web.evanchen.cc/history.html)
- [ERIC: A Follow-up on USAMO Winners (1985)](https://eric.ed.gov/?id=EJ328725)
- [USAMO Qualification and College Admissions — Collegebase Blog](https://www.collegebase.org/blog/usamo-qualification-college-admissions)
- [Mathematical Olympiad Program (MOP) — Collegebase Blog](https://www.collegebase.org/blog/mathematical-olympiad-program-mop-college-admissions)
- [Approximately what % of USAMO qualifiers get into Harvard/MIT — Quora](https://www.quora.com/Approximately-what-percentage-of-USAMO-qualifiers-get-into-Harvard-MIT-and-other-top-schools)
- [IPEDS — National Center for Education Statistics](https://nces.ed.gov/ipeds)
- [Stanford University IPEDS reported data](https://nces.ed.gov/ipeds/reported-data/243744)
- [Stanford Common Data Set — IRDS](https://irds.stanford.edu/data-findings/cds)
- [Unfair Collection: Reclaiming Control of Publicly Available Personal Information — Michigan Law Review](https://michiganlawreview.org/journal/unfair-collection-reclaiming-control-of-publicly-available-personal-information-from-data-scrapers/)
- [Spotlight on 2025 Regeneron STS — Polygence](https://www.polygence.org/blog/regeneron-science-talent-search-key-takeaways)
- [Harker School College Acceptances — harker.org](https://www.harker.org/upper-school/support-services/college-counseling/college-acceptances)
- [Harker School — Niche](https://www.niche.com/k12/the-harker-school-san-jose-ca/)
- [LinkedIn Advanced Search Filters 2026 Guide — evaboot](https://evaboot.com/blog/linkedin-advanced-search)
