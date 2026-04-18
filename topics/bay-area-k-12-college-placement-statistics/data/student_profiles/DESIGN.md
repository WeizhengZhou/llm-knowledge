# Student Application Profile Database — Design Doc

## Problem

School-level placement data tells us "SHS sends 28 students to Stanford over 5 years."
Student-level profile data tells us "what kind of student from a school like SHS gets into Stanford."
Combining both creates a calibrated probability model: given THIS profile at THIS school, what are realistic outcomes?

## Data Sources (ranked by signal quality)

| Source | Format | Volume | Structure | Signal | Access |
|--------|--------|--------|-----------|--------|--------|
| r/collegeresults | Reddit posts | ~5K posts | Semi-structured (template) | High — full profiles + outcomes | Public API / scrape |
| r/ApplyingToCollege | Reddit posts | ~50K+ relevant | Unstructured | Medium — mixed with advice posts | Public API / scrape |
| YouTube "stats" videos | Video transcripts | ~10K relevant | Unstructured | High — detailed narratives | yt-dlp + API |
| College Confidential | Forum threads | ~100K+ | Unstructured | Medium — self-reported, older | Scrape |
| AdmitSee | Structured profiles | ~60K | Structured | High — includes essays | Paid API ($) |
| Naviance scattergrams | Screenshots | Scattered | Semi-structured | High — GPA/score vs outcome | Not systematically accessible |

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Crawlers       │────▶│  Raw Store    │────▶│  LLM Extract │────▶│  Validated   │
│ (per-source)     │     │  (markdown)   │     │  (structured) │     │  SQLite DB   │
└─────────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                         │
                                                                         ▼
                                                                  ┌──────────────┐
                                                                  │  Cross-Join   │
                                                                  │  with School  │
                                                                  │  Placement DB │
                                                                  └──────────────┘
```

### Layer 1: Crawlers

Each source needs its own crawler because the access patterns differ:

**Reddit (r/collegeresults, r/ApplyingToCollege)**
- Use Reddit's JSON API: append `.json` to any subreddit/post URL
- No auth needed for public subreddits
- Rate limit: 60 req/min without auth, 100 req/min with OAuth
- Pagination: use `after` parameter
- Filter: flair "Results" or title containing "results", "accepted", "stats"
- Anti-bot: Reddit is lenient with JSON API; use proper User-Agent header
- Volume: ~50-100 posts per batch, paginate through history

**YouTube**
- Search API (quota: 10K units/day, search costs 100 units = 100 searches/day)
- yt-dlp for transcript download (no API quota, uses scraping)
- Search queries: "college decision reaction stats", "how I got into Stanford", "college results stats"
- Filter by: view count > 1K, upload date within 3 years, English language
- Anti-bot: YouTube API is rate-limited but not hostile; yt-dlp has built-in throttling

**College Confidential**
- HTML scrape (no API)
- Target: "College Admissions Results" subforum
- Structure: thread per student, first post has profile + results
- Anti-bot: moderate — need rotation of User-Agent, delays between requests
- Volume: massive archive but quality varies

### Layer 2: Raw Store

Save every crawled item as a markdown file before any processing:

```
data/student_profiles/raw/
├── reddit/
│   ├── collegeresults/
│   │   ├── t3_abc123.md    # one file per post
│   │   ├── t3_def456.md
│   │   └── ...
│   └── a2c/
│       └── ...
├── youtube/
│   ├── dQw4w9WgXcQ.md     # one file per video (transcript)
│   └── ...
└── cc/
    └── ...
```

Each raw file has frontmatter:
```yaml
---
source: reddit/collegeresults
source_id: t3_abc123
url: https://reddit.com/r/collegeresults/comments/abc123/
crawled_at: 2026-04-18T12:00:00Z
title: "Asian Female | 1560 SAT | STEM | Results"
score: 234
---
{raw post content}
```

### Layer 3: LLM Extraction

Run each raw file through an LLM extraction prompt that outputs structured JSON:

```json
{
  "extraction_confidence": 0.92,
  "demographics": {
    "gender": "female",
    "ethnicity": "asian",
    "ethnicity_detail": "chinese-american",
    "first_gen": false,
    "legacy": null,
    "state": "CA",
    "region": "bay-area",
    "school_type": "private",
    "school_name_hint": null,
    "school_size_hint": "~200 per class",
    "hooks": ["none"]
  },
  "academics": {
    "gpa_uw": 3.97,
    "gpa_w": 4.45,
    "class_rank": "top 5%",
    "sat": 1560,
    "act": null,
    "sat_subject_tests": null,
    "ap_count": 12,
    "ap_scores": "all 5s",
    "notable_courses": ["Multivariable Calculus", "Linear Algebra"]
  },
  "extracurriculars": [
    {"activity": "Math Team Captain", "years": 4, "level": "national", "detail": "AIME qualifier"},
    {"activity": "Research", "years": 2, "level": "published", "detail": "Stanford math REU"},
    {"activity": "Violin", "years": 8, "level": "regional", "detail": "youth orchestra"}
  ],
  "awards": [
    {"name": "AIME qualifier", "level": "national"},
    {"name": "Science Olympiad", "level": "state", "detail": "3rd place"}
  ],
  "application_year": 2024,
  "results": [
    {"college": "Stanford", "college_normalized": "stanford", "round": "REA", "result": "accepted", "enrolled": true},
    {"college": "MIT", "round": "RA", "result": "accepted", "enrolled": false},
    {"college": "Harvard", "round": "RD", "result": "rejected", "enrolled": false},
    {"college": "Duke", "round": "RD", "result": "accepted", "enrolled": false}
  ]
}
```

**Validation rules (automated):**
- GPA: 0.0-4.0 (UW), 0.0-5.0 (W)
- SAT: 400-1600, ACT: 1-36
- Application year: 2018-2026
- At most 1 school marked "enrolled": true
- College names normalize to known slugs
- If extraction_confidence < 0.7, flag for manual review

### Layer 4: SQLite Storage

```sql
CREATE TABLE student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,           -- 'reddit', 'youtube', 'cc'
    source_id TEXT NOT NULL,        -- post ID / video ID
    source_url TEXT,
    extraction_confidence REAL,
    application_year INTEGER,
    gender TEXT,
    ethnicity TEXT,
    ethnicity_detail TEXT,
    first_gen BOOLEAN,
    legacy TEXT,                    -- null, 'undergrad', 'graduate', 'double'
    state TEXT,
    region TEXT,                    -- 'bay-area', 'northeast', etc.
    school_type TEXT,               -- 'private', 'public', 'charter', 'magnet'
    school_name_hint TEXT,          -- if disclosed (many don't)
    school_id TEXT,                 -- FK to schools table if we can match
    school_size_hint TEXT,
    hooks TEXT,                     -- JSON array: ['legacy', 'athlete', 'first-gen']
    gpa_uw REAL,
    gpa_w REAL,
    class_rank TEXT,
    sat INTEGER,
    act INTEGER,
    ap_count INTEGER,
    ecs_json TEXT,                  -- JSON array of EC objects
    awards_json TEXT,               -- JSON array of award objects
    essay_topics TEXT,              -- brief description if shared
    crawled_at TEXT,
    extracted_at TEXT,
    UNIQUE(source, source_id)
);

CREATE TABLE application_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER REFERENCES student_profiles(id),
    college TEXT NOT NULL,
    college_normalized TEXT NOT NULL,
    round TEXT,                     -- 'ED', 'ED2', 'EA', 'REA', 'RD'
    result TEXT NOT NULL,           -- 'accepted', 'rejected', 'waitlisted', 'deferred'
    enrolled BOOLEAN DEFAULT FALSE,
    scholarship TEXT,               -- if mentioned
    UNIQUE(profile_id, college_normalized, round)
);

-- Cross-join view: match student profiles to school placement data
CREATE VIEW v_profile_school_match AS
SELECT 
    sp.*,
    s.name as matched_school,
    s.school_id as matched_school_id
FROM student_profiles sp
LEFT JOIN schools s ON sp.school_id = s.school_id
WHERE sp.school_id IS NOT NULL;
```

### Layer 5: Cross-Join and Insights

**Match 1: Profile → School**
If a student says "Bay Area private school, ~200 per class, 65% Asian" → likely Harker.
Use heuristics + school_profiles table to match.

**Match 2: Profile + School → Calibrated Probability**
"Asian female, 1560 SAT, AIME qualifier, from Harker, applied Stanford REA → accepted"
Cross-reference with: "Harker sends 34 to Stanford over 3 years"
→ Build conditional probabilities by profile segment

**Match 3: Similar Profiles → Outcome Distribution**
Find all profiles with similar demographics + stats + school type
→ Show the distribution of outcomes (not just one person's story)

## Anti-Bot Strategy

| Source | Risk Level | Mitigation |
|--------|-----------|------------|
| Reddit JSON API | Low | Use OAuth app credentials, proper User-Agent, 1 req/sec |
| YouTube Data API | Low | Stay within quota (100 searches/day), use yt-dlp for transcripts |
| YouTube yt-dlp | Medium | Built-in throttling, rotate IPs if needed |
| College Confidential | Medium | Random delays (2-5s), rotate User-Agent, session cookies |
| AdmitSee | N/A | Paid API, no scraping needed |

**General rules:**
- Never parallel-crawl the same source
- Cache aggressively — never re-fetch a URL
- Respect robots.txt
- Store raw before processing (if source goes down, you still have data)
- Rate limit: 1 request/second default, 0.5 req/sec for CC

## Test Case Strategy (Phase 1)

Start small, validate the pipeline, then scale:

1. **Reddit test (10 posts):** Manually pick 10 high-quality r/collegeresults posts
   - 3 Asian Bay Area private school students
   - 3 Asian Bay Area public school students  
   - 2 non-Asian Bay Area students
   - 2 non-Bay Area students (control)
   → Crawl, extract, validate, store. Verify LLM extraction accuracy.

2. **YouTube test (5 videos):** Pick 5 "stats that got me into" videos
   → Download transcripts, extract, compare quality to Reddit

3. **Cross-validation test:** For the Reddit profiles where school is identifiable,
   match against our school placement DB and check consistency

4. **Scale decision:** Based on extraction accuracy and cross-validation results,
   decide whether to scale to full subreddit crawl

## File Layout

```
data/student_profiles/
├── DESIGN.md                  # This file
├── profiles.db                # SQLite database
├── schema.sql                 # Database schema
├── crawlers/
│   ├── reddit_crawler.py      # Reddit JSON API crawler
│   ├── youtube_crawler.py     # YouTube search + yt-dlp transcripts
│   └── cc_crawler.py          # College Confidential scraper
├── extract/
│   ├── llm_extractor.py       # LLM-based structured extraction
│   └── validator.py           # Automated validation rules
├── raw/                       # Raw crawled content (markdown)
│   ├── reddit/
│   ├── youtube/
│   └── cc/
└── analysis/
    ├── cross_join.py           # Match profiles to school DB
    └── insights.py             # Statistical analysis
```
