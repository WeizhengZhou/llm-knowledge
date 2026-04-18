# College Placement Data Architecture

_How to build an AI-driven school application counselor from public data sources._

**Status:** Active development
**Created:** 2026-04-18
**Last updated:** 2026-04-18
**Related topic:** `topics/bay-area-k-12-college-placement-statistics/`

---

## The Three-Layer Model

College application advising requires three layers of data, each progressively harder to acquire:

```
Layer 3: Student Trajectory     "She started Beast Academy at 7, AMC 8 at 11,
         (K-12 development arc)  AIME qualifier at 14, published research at 16"
                                 ↕ identity resolution
Layer 2: Student Profile         "Asian female, 1560 SAT, AIME qualifier,
         (snapshot at 18)         Bay Area private school, accepted to MIT"
                                 ↕ school-level matching
Layer 1: School Placement        "Harker sends 34 to Stanford, 12 to MIT,
         (aggregate outcomes)     65% Asian applicant pool"
```

Each layer compounds the value of the layers below it. A private counselor charging $50K/year has all three — we're building them from public sources.

---

## Layer 1: School Placement Data

### What It Answers
"How many students from this school go to Stanford? What's the non-athlete rate? How does Harker compare to SHS?"

### Status: Production

| Metric | Value |
|---|---|
| Schools covered | 11 (8 private + 3 public) |
| Placement records | 1,876 |
| UC admissions records | 961 (with ethnicity, 30 years) |
| Athlete commits | 146 (SHS only, 5 years, name-level) |
| School profiles | 13 (class sizes, test scores, AP counts) |

### Data Sources (Proven)

| Source | What We Get | How to Get It | Quality | Refresh Cycle |
|---|---|---|---|---|
| School Profile PDFs | Matriculation lists, test scores, class sizes | `curl` download → `pdftotext` → parse into SQLite | L1 (official) | Annual (fall) |
| UC InfoCenter | Applicants/admits/enrollees by school, ethnicity, UC campus | JSON from collegeacceptance.info mirror | L1 (official) | Annual (spring) |
| School athlete commit pages | Name, sport, college per athlete | WebFetch → markdown table → `ingest_athletes.py` | L1 (official) | Annual (spring) |
| School Google Docs / web pages | Matriculation lists | WebFetch or Chrome CDP | L1-L2 | Annual |
| Niche.com | Top enrolled colleges (NSC-verified) | Manual check | L3 (aggregator) | Annual |

### Architecture

```
raw/school-profiles/{school-slug}/     ← downloaded PDFs + extracted markdown
raw/uc-infocenter/                     ← JSON bulk data
raw/athlete-commits/{school-slug}/     ← per-year athlete tables
data/college_placement.db              ← SQLite (schema.sql)
data/ingest_*.py                       ← 6 ingestion scripts
data/query.py                          ← CLI query tool
wiki/entities/{school-slug}.md         ← compiled articles
```

### What Proved Working at Small Scale

- **pdftotext extraction**: Reliable for all school profile PDFs tested. The "Where Do Gators Go" PDFs extracted cleanly with applied/accepted/enrolled columns.
- **UC InfoCenter JSON mirror**: collegeacceptance.info provides the same data as the UC Tableau tool in machine-readable JSON. Covers all private schools.
- **Athlete commit pages**: SHS publishes name-level data that no other school in our survey does. WebFetch extracts these cleanly.
- **Cross-validation**: SHS data matched 100% (75/75 data points) against user's manually collected spreadsheet.
- **College name normalization**: Required fixing — UC parenthesized format, Rice University, Notre Dame variants all needed explicit handling. 69 rows fixed after initial ingestion.

### What Didn't Work

- **Google Docs extraction**: Canvas rendering prevents DOM-based text extraction. Had to use Chrome CDP to access the internal `DOCS_modelChunk` JSON, which revealed the doc was a hub page linking to PDFs (not data itself).
- **Direct PDF reading via Claude's Read tool**: Required `poppler-utils` (pdftoppm), which was installed but not on Claude's PATH. Workaround: use `pdftotext` via Bash.
- **Menlo overlapping windows**: Menlo publishes 2-year rolling windows that double-count if summed naively. Requires careful handling in aggregate queries.
- **Nueva tier-based reporting**: "10 or more" stored as count=10 inflates aggregates. Must be labeled as minimums.

### What Needs More Work

- **More schools**: Only 11 schools covered. Adding Bellarmine, Presentation, Lick-Wilmerding, University High, Head-Royce would broaden coverage.
- **Public school data**: Palo Alto High, Gunn, Lynbrook data came from user's manual spreadsheet, not from official sources. Need to scrape school websites or use UC InfoCenter data.
- **Annual refresh automation**: The intake process is documented but manual. Could automate with a cron job that checks school websites for updated PDFs each September.

---

## Layer 2: Student Profile Data

### What It Answers
"What kind of student from Harker gets into Stanford? What's the acceptance rate for Asian females with 1550+ SAT?"

### Status: Prototype (working end-to-end)

| Metric | Value |
|---|---|
| Profiles | 110 |
| Application results | 1,238 |
| Extraction rate | 70% of crawled posts have results |
| Sources active | Reddit (98 posts), YouTube (14 videos) |

### Data Sources (Proven + Planned)

| Source | Volume | Format | Extraction Method | Status |
|---|---|---|---|---|
| Reddit r/collegeresults | ~5K+ posts | Semi-structured text | Rule-based parser (3 format types) | **Proven** — 98 profiles, 70% extraction |
| Reddit r/ApplyingToCollege | ~50K+ | Unstructured | Gemini LLM | Planned |
| YouTube "stats/decisions" | ~10K+ videos | Transcripts (yt-dlp) | Gemini LLM | **Proven** — 14 videos, 86% extraction |
| College Confidential | ~100K+ threads | Unstructured HTML | Gemini LLM | Planned |
| AdmitSee | ~60K profiles | Structured JSON | Paid API | Planned |
| MIT Admissions Blogs | ~5K+ posts | Clean HTML | Gemini LLM | Research complete, ready to crawl |

### Architecture

```
data/student_profiles/
├── profiles.db                    ← SQLite (schema.sql)
├── reddit_crawler.py              ← Reddit JSON API, rate-limited, filter heuristics
├── youtube_crawler.py             ← yt-dlp search + transcript download
├── llm_extractor.py               ← Rule-based extraction (3 format types)
├── gemini_extractor.py            ← Gemini 2.5 Flash LLM extraction
├── llm_extract_batch.py           ← Batch processing + import
├── cross_join.py                  ← Connect profiles to school placement DB
├── raw/reddit/collegeresults/     ← 98 crawled posts (markdown with frontmatter)
└── raw/youtube/                   ← 14 crawled videos (transcript + metadata)
```

### Crawling Approach

**Reddit:**
- Use Reddit's public JSON API (append `.json` to URLs)
- No auth needed for public subreddits, but OAuth increases rate limit (60→100 req/min)
- Pagination via `after` parameter
- Filter with `is_results_post()` heuristic: checks title for "results/accepted/committed" + body for "gpa/sat/accepted"
- Rate limit: 1.5s between requests
- User-Agent: descriptive research identifier

**YouTube:**
- `yt-dlp` for search (no API quota needed) and transcript download
- Search queries: "stats that got me into [school]", "college decision reaction stats"
- Filter: `is_relevant_video()` checks title/description for college + stats keywords, duration 3-30 min
- Auto-subtitles (`.en.vtt`) → `vtt_to_text()` strips timestamps and deduplicates
- Rate limit: 2s between downloads

**Anti-bot strategy:**
- Reddit: low risk with proper User-Agent and rate limiting
- YouTube: yt-dlp has built-in throttling; stay within reasonable volume
- College Confidential: moderate risk — needs User-Agent rotation and 2-5s delays
- General: cache aggressively (never re-fetch), respect robots.txt, store raw before processing

### Extraction Approach

**Rule-based parser** (llm_extractor.py) handles 3 Reddit format types:

1. **Section-based**: "Acceptances:" / "Rejections:" headers followed by bullet lists
2. **Inline**: "Stanford — Accepted" or "Harvard: Rejected"
3. **Round-grouped**: "ED:" / "EA:" / "RD:" headers with "College (rate%): Result"

Catches demographics (gender, ethnicity, first-gen), test scores (SAT regex, ACT regex), GPA (multiple scale formats), and school type. Works for ~70% of Reddit posts. Fails on unusual formatting, emoji-heavy posts, and YouTube transcripts.

**Gemini LLM extraction** (gemini_extractor.py) handles everything the rule-based parser misses:

- Model: `gemini-2.5-flash` via Google Generative AI SDK
- API key: loaded from `kid_camp2/backend/.env` (GOOGLE_API_KEY)
- Prompt: structured JSON schema with all fields specified
- Response format: `response_mime_type="application/json"` for clean parsing
- Retry: 3 attempts with increasing backoff
- Rate limit: 1s between calls
- Cost: effectively free at current Gemini Flash pricing for this volume
- Success rate: 80% on YouTube transcripts, 80% on Reddit re-extractions
- Main failure mode: JSON parse errors from malformed Gemini output (5-10% of calls)

### Validation Rules

```python
- GPA: 0.0-4.5 (UW), 0.0-5.5 (W), or 50-100 (percentage scale)
- SAT: 400-1600
- ACT: 1-36
- Application year: 2015-2030
- At most 1 school marked "enrolled: true"
- College names must normalize to known slugs
- extraction_confidence < 0.7 → flag for manual review
```

### What Proved Working

- **Reddit rule-based extraction**: 3 format types cover ~70% of posts. Fast, no API cost.
- **Gemini extraction for YouTube**: Transforms unstructured transcripts into structured profiles. 80% success rate.
- **Gemini re-extraction for Reddit failures**: Recovered 86 additional results from 10 posts that rule-based missed.
- **Cross-join**: Successfully matched 82 colleges across both databases. Found 21 Asian female profiles comparable to Lexi.
- **Demographic analysis**: Sample shows Asian 45% acceptance rate vs White 52% — consistent with known patterns.

### What Didn't Work

- **Gemini JSON parsing**: 10-20% of Gemini responses have malformed JSON (unterminated strings, missing commas). Need structured output enforcement or post-processing cleanup.
- **YouTube without transcript**: 2 of 14 videos had no auto-subtitles. These are unextractable without speech-to-text.
- **GPA extraction**: Many formats not caught by regex (98.178/100 scale, "top 5% of class" without numeric GPA, weighted GPA on non-standard scales).
- **Re-processing existing profiles**: SQLite FK constraint errors when re-running extraction on already-stored profiles. Fixed with delete-then-insert pattern.

### What Needs More Work

- **Scale Reddit crawl**: Paginate deeper into r/collegeresults history (only scraped ~100 of 5,000+ posts).
- **Add r/ApplyingToCollege**: Larger subreddit with more profiles but noisier (advice threads mixed in).
- **College Confidential crawler**: Different HTML structure, needs its own parser.
- **MIT Admissions Blog crawler**: Identified as richest trajectory source. Clean HTML, ready to crawl.
- **Metadata enrichment**: Add `original_domain`, `post_date`, `extraction_method` to all profiles (schema updated, migration applied).

---

## Layer 3: Student Trajectory Data

### What It Answers
"When should Lexi start AMC 8? What does a typical AIME qualifier's development look like from K through 12? What did the students who got into MIT from Harker actually do in middle school?"

### Status: Research complete, extraction beginning

This is the hardest layer. **No single public source captures the full K-12 developmental arc.** The data exists in domain-specific silos that have never been connected.

### Research Investment

11 research agents deployed across these source categories:

| Category | Agents | Key Finding |
|---|---|---|
| Competition databases | 2 | USAPhO PDFs are cleanest; AMC/AIME school-level data is NOT public (gated) |
| AoPS community | 1 | AMC score threads have longitudinal data; MATHCOUNTS CA PDFs have named students |
| Chinese parent forums | 1 | huaren.us is best public source (6,815 topics); Xiaohongshu is auth-gated |
| College newspapers | 1 | MIT Admissions Blogs is the single richest trajectory source (20yr archive) |
| LinkedIn reverse | 1 | MATHCOUNTS→USAMO→STS→college chain is traceable; LinkedIn manual OK, scraping risky |
| Essay books / retrospectives | 1 | No K-8 data in any published source; books start at 9th grade |
| Podcasts / alumni magazines | 1 | Still running |
| K-8 creative sources | 1 | Still running |
| Sports progression databases | 1 | Still running |
| Gifted program longitudinal | 1 | Still running |
| Duosmium Sci Oly download | 1 | 247 YAML files, 12,870 team records downloaded |

### The K-8 Gap

**Critical finding: No public source captures the K-8 developmental period** (ages 5-14). Every identified source starts at 9th/10th grade at earliest. The foundational years — when enrichment programs begin, when first competitions are entered, when sports are chosen — are absent from every public database surveyed.

**Best candidates for K-8 data (from ongoing research):**

| Source | Ages | Named? | Type | Status |
|---|---|---|---|---|
| **Spelling Bee (Scripps)** | 8-14 | Yes, multi-year | Competition results | **Best confirmed K-8 source** — 17-24% repeater rate, names public |
| USA Swimming times DB | 6-18 | Yes | Performance progression | Researching |
| USCF chess ratings | 5-18 | Yes | Rating progression | Researching |
| Math Kangaroo | 6-12 | TBD | Competition results | Researching |
| MOEMS | 10-13 | TBD | Competition results | Researching |
| Certificate of Merit (CA music) | 6-18 | TBD | Level progression | Researching |
| Chinese parent forums (Xiaohongshu) | K-12 | Anon | Narrative | Auth-gated |
| huaren.us | K-12 | Anon | Narrative, public | Ready to crawl |
| Davidson Young Scholars | 5-18 | Yes (internal only) | Talent ID + development | Zero published outcomes |
| **Davidson Gifted Forum** | K-8 | Anon (parent posts) | Year-by-year math progression | **Public, no login** — parents post curriculum+competition arcs |
| **Math Kangaroo winners** | 6-12 (gr 1-6) | Yes (top 20 national) | Annual winner lists | Public — 21K CA participants, grades 1-4 highest enrollment |
| **RSM competition blog** | 9-14 | Yes (named achievers) | Competition results | Public — includes 4th-grade USAJMO qualifier |
| **Scripps Spelling Bee** | 8-14 (gr 1-8) | Yes, multi-year | 243 profiles/yr, return data | Public |
| Gifted programs (CTY, Davidson, TIP) | 7-18 | Varies | Alumni outcomes |

### Data Sources for 9-18 Trajectory

| Source | What We Get | Volume | Status |
|---|---|---|---|
| **MATHCOUNTS CA PDFs** | Name + school + score + rank (gr 6-8) | ~50/yr | Extracting now |
| **USAPhO medal lists** | Name + school + medal (gr 9-12) | ~394/yr | Extracting now |
| **USAMO/USAJMO qualifier lists** | Name + school (gr 9-12) | ~500/yr | URLs identified |
| **Regeneron STS scholars** | Name + school + project (gr 12) | ~300/yr | URLs identified |
| **AoPS AMC score threads** | Username + grade + score + delta (gr 7-12) | Thousands | URLs identified |
| **MIT Admissions Blogs** | Full K-12 narrative (varies) | ~100 trajectory posts | Ready to crawl |
| **Duosmium Sci Oly** | School + placement + event scores | 12,870 records | Downloaded |
| **Tabroom.com (debate)** | Individual + school + tournament + date | 15+ yrs | URLs identified |
| **Evan Chen-style personal sites** | Full K-12 trajectory, self-published | Dozens | Manual discovery |

### Identity Resolution Approach

Three strategies for matching fragments into complete trajectories:

**Strategy 1: Named Entity Resolution**
When competition results publish real names (MATHCOUNTS: "E. Chen, Harker, 8th grade"), search for the same name across other competitions (USAMO: "Emily Chen, Harker") and athlete commits. Match on name + school + age consistency. Confidence scoring: exact name+school = 95%, same name+same state = 80%, fuzzy name+same school type = 60%.

**Strategy 2: School-Level Aggregate**
No individual matching needed. Connect school-level competition data to school-level college placement data. "Harker produces 5 MATHCOUNTS state qualifiers per year AND sends 12 to MIT per year." Answers pipeline conversion questions without privacy concerns.

**Strategy 3: Archetype Construction**
Cluster anonymous profiles (Reddit, YouTube) by demographics + school type + achievement level. Build composite trajectories: "The typical Asian female AIME qualifier from a Bay Area private school started math enrichment at age 7, MATHCOUNTS at 11, AIME at 14." Not individual, but directionally correct.

### Verification Pipeline

Every resolved trajectory gets checked for:
1. **Age/grade consistency**: All records should be consistent with a single birth year (±1 year tolerance)
2. **School consistency**: Same school across records, or known transfer pattern (max 2 schools)
3. **Performance trajectory plausibility**: Scores should generally improve (no 50% year-over-year drops)
4. **Cross-source consistency**: SAT/GPA shouldn't differ by large margins across Reddit and YouTube
5. **Outcome plausibility**: AIME qualifier from Harker → MIT is plausible; AIME qualifier → community college needs verification

### What Proved Working (Small Scale)

- **Duosmium download**: 247 YAML files with 12,870 team records ingested. Confirmed which Bay Area schools participate in Sci Oly (Monta Vista, Paly, Lynbrook dominant; Harker/SHS/Nueva absent).
- **Cross-join tool**: Connected 82 colleges across student profile and school placement databases. Found 21 comparable profiles for Lexi.
- **School-level competition→placement correlation**: Proved feasible — Harker dominates MATHCOUNTS AND sends most students to MIT.

### What Needs More Work

- **MATHCOUNTS PDF extraction**: Agent launched, results pending.
- **USAPhO PDF extraction**: Agent launched, results pending.
- **MIT Admissions Blog crawl**: Identified as highest-value trajectory source. Needs crawler + Gemini extraction.
- **Multi-year student matching**: Need to implement the named entity resolution pipeline to link the same student across MATHCOUNTS (8th grade) → AMC/AIME (10th grade) → USAMO (11th grade) → college (12th grade).
- **K-8 data sources**: Most promising leads (USA Swimming, chess, Math Kangaroo) still being researched.
- **Chinese parent forum mining**: huaren.us is public and crawlable but data is discussion-oriented, not structured trajectories. Need LLM extraction for narrative posts.
- **Build our own intake**: For the K-8 gap, the "create our own data" strategy — a structured survey for parents willing to share trajectories — may be the only scalable path.

---

## Cross-Cutting Concerns

### Storage Architecture

```
SQLite databases (structured, queryable):
  data/college_placement.db        ← Layer 1: school placement + UC admissions + athletes
  data/student_profiles/profiles.db ← Layer 2: student profiles + application results

Raw source files (immutable, for audit):
  raw/school-profiles/{slug}/      ← PDFs + extracted markdown
  raw/uc-infocenter/               ← JSON bulk data
  raw/athlete-commits/{slug}/      ← per-year athlete tables
  raw/web/                         ← research findings
  data/student_profiles/raw/       ← crawled posts, transcripts, competition results

Wiki articles (compiled, human-readable):
  wiki/entities/{slug}.md          ← per-school profiles
  wiki/guides/                     ← how-to articles

Guidebook (distribution format):
  guidebook/*.md                   ← 10 chapters + appendices
```

### College Name Normalization

Critical for cross-source joins. All systems share `normalize_college()` from `ingest_athletes.py`.

Known pitfalls (fixed):
- UC parenthesized format: "University of California (Berkeley)" → "uc-berkeley"
- Rice University → "rice" (not "rice-university")
- Notre Dame variants → "notre-dame"
- Cal Poly SLO variants → "california-polytechnic-state-university-slo"

When adding new sources, always check for normalization fragmentation with:
```sql
SELECT college_normalized, COUNT(*) FROM placements GROUP BY college_normalized 
HAVING college_normalized LIKE '%university-of-california%' OR college_normalized LIKE '%uc-%'
```

### Anti-Bot and Rate Limiting

| Source | Risk | Mitigation | Rate |
|---|---|---|---|
| Reddit JSON API | Low | Proper User-Agent, OAuth optional | 1.5s/req |
| YouTube (yt-dlp) | Medium | Built-in throttling | 2s/download |
| College Confidential | Medium | User-Agent rotation, random delays | 2-5s/req |
| AoPS | Low-Medium | Respectful crawling | 2s/req |
| cspeef.org (MATHCOUNTS) | Low | Small volume, direct PDF links | 1s/req |
| aapt.org (USAPhO) | Low | Direct PDF links | 1s/req |
| LinkedIn | **High** | Manual browsing only, NO scraping | N/A |
| Xiaohongshu | **High** | Requires auth + cookie management | N/A |

### Privacy Framework

| Data Type | How We Use It | Storage |
|---|---|---|
| Named competition results (public PDFs) | Cross-reference, school aggregates | Raw + normalized |
| Reddit/YouTube (self-published) | Profile extraction, archetype building | Anonymized |
| Swimming/chess times (public DBs) | Trajectory curves, school patterns | Aggregated only |
| LinkedIn | **DO NOT scrape** | Do not store |
| School placement (official) | School-level aggregates | As-is |

**Rule: We never publish individual named trajectories.** Named data is used for internal identity resolution and school-level aggregation only. All published output (guidebook, wiki, tools) uses anonymized archetypes or school-level statistics.

### Gemini LLM Extraction Configuration

- Model: `gemini-2.5-flash`
- API key: sourced from `kid_camp2/backend/.env` → `GOOGLE_API_KEY`
- Temperature: 0.1 (deterministic extraction)
- Max output tokens: 4,096
- Response format: `application/json`
- Retry: 3 attempts with exponential backoff
- Cost: negligible at current Flash pricing (~$0.001/extraction)
- Failure rate: ~15% (JSON parse errors), recoverable with retry

---

## Appendix: Session Artifacts

### Git Commits (2026-04-18)

1. `77859fb` — kb: Bay Area K-12 college placement statistics — initial build
2. `416354c` — kb: Duke legacy + post-SFFA admissions research
3. `4ed986c` — fix: normalize college names — fix UC/Rice/Notre Dame fragmentation
4. `b71e099` — kb: guidebook Chapter 1 + structure + public school data
5. `2ae0665` — kb: guidebook Chapter 2 — How to Read School Placement Data
6. `635c552` — kb: guidebook Chapters 3 + 5 — Athlete Hook + Asian Parent Reality
7. `48cde8c` — feat: student profile database — Reddit crawler + extractor prototype
8. `2764c2b` — feat: student profiles — scale crawl + improved extractor
9. `fafbfa8` — feat: YouTube crawler + Gemini LLM extraction + cross-join analysis
10. `b014fff` — research: Layer 3 K-12 trajectory source survey
11. `0d4db7d` — research: identity resolution design + LinkedIn reverse-trajectory findings
12. `279fc0a` — research: college newspaper trajectory sources — MIT blogs is the goldmine

### Guidebook Chapters

| Chapter | Title | Status | Words |
|---|---|---|---|
| 1 | What the Brochure Doesn't Say | Done, verified | ~3,100 |
| 2 | How to Read School Placement Data | Done, verified | ~3,200 |
| 3 | The Athlete Hook — Quantified | Done, verified | ~3,500 |
| 4 | School by School — The Real Numbers | Planned | — |
| 5 | The Asian Parent Reality | Done, verified | ~3,400 |
| 6 | Private vs Public — Is It Worth It? | Planned | — |
| 7 | Legacy, Early Decision, and Structural Advantages | Planned | — |
| 8 | The Spike, Not the Well-Rounded Kid | Planned | — |
| 9 | Grade by Grade — What to Build When | Planned | — |
| 10 | Should You Transfer Schools? | Planned | — |
