# Data Intake Process — College Placement Statistics

Reproducible process for gathering college placement data for any school.

## Source Priority (Best → Supplementary)

| Priority | Source Type | What You Get | Automation |
|----------|-----------|-------------|------------|
| **1** | School Profile PDF | Matriculation list, test scores, class size, AP counts | Semi-auto: download PDF → LLM extract to markdown → parse into SQLite |
| **2** | School Google Doc / Web Page | College outcomes with counts | Semi-auto: WebFetch → parse into SQLite |
| **3** | UC InfoCenter | Applicants/admits/enrollees per UC campus, by ethnicity | Fully auto: CSV download → `ingest_uc.py` |
| **4** | School Athlete Commit Pages | Name, sport, college per athlete | Semi-auto: WebFetch → LLM extract table → `ingest_athletes.py` |
| **5** | Niche.com | Top enrolled colleges (NSC-verified) | Semi-auto: scrape top colleges list |
| **6** | Chicardgo School / PrepReview | ECPI index, feeder % estimates | Manual: cross-reference only |

## Adding a New School

### Step 1: Register the school

```python
# In init_db.py, add to SCHOOLS list:
("school-slug", "Full School Name", "Short", "City", "CA", "private", "6-12", "https://...", "CEEB")
```

Then re-run `python data/init_db.py`.

### Step 2: Find the school's data sources

Search for these (in order):
1. `site:{school-domain} "college counseling" OR "college profile" filetype:pdf`
2. `site:{school-domain} "where our graduates go" OR "college destinations" OR "matriculation"`
3. `site:{school-domain} "signing day" OR "committed" OR "student athletes"`
4. Check Issuu: `site:issuu.com "{school name}" "school profile"`
5. Check Niche: `https://www.niche.com/k12/{school-slug}/`

Register each found source in `init_db.py` SOURCES list.

### Step 3: Download and extract

**For PDFs:**
```bash
# Download
curl -o raw/school-profiles/{slug}/{year}_school-profile.pdf "{url}"

# Extract via LLM agent — the agent reads the PDF and produces structured markdown
# The markdown file goes to: raw/school-profiles/{slug}/{year}_school-profile.md
```

**For web pages:**
```bash
# Use WebFetch in an agent to get the page content
# Extract to: raw/school-profiles/{slug}/{description}.md
```

**For athlete commits:**
```bash
# Use WebFetch to get signing day pages
# Extract to: raw/athlete-commits/{slug}/{year}_athlete_commits.md
# Format as markdown table: | Name | Sport | College |
```

### Step 4: Ingest into SQLite

```bash
# Placements (from extracted markdown)
python data/ingest_placements.py raw/school-profiles/{slug}/{file}.md {slug} --source school_profile_pdf --source-url "{url}"

# Athletes (from extracted markdown)
python data/ingest_athletes.py raw/athlete-commits/{slug}/{year}_athlete_commits.md {slug} {year}

# UC data (from CSV download)
python data/ingest_uc.py raw/uc-infocenter/{csv_file}
```

### Step 5: Verify

```bash
python data/query.py placements {slug}
python data/query.py ivy {slug}
python data/query.py athletes {slug}
```

## Annual Refresh Process

Run each fall (September-October) when schools publish new profiles:

1. Check each school's college counseling page for updated School Profile PDFs
2. Check for new athlete commit announcements
3. Download UC InfoCenter data for the new cycle
4. Re-run ingestion for updated sources
5. Update source status in the database

## Data Quality Rules

- **Enrolled > Accepted > Applied**: Only store the most specific metric available
- **Multi-year lists**: When a school publishes "Classes of 2022-2024 combined", mark each placement with all applicable years and add a note
- **Count suppression**: Some schools don't publish per-college counts. Store count=1 for each listed college (minimum confirmed presence)
- **Athlete deduplication**: An athlete appears in both `athlete_commits` AND `placements`. The `v_non_athlete_placements` view handles the math.
- **Confidence levels**: School-published = L1-L2, Aggregators = L3, Forums = L4

## File Layout

```
data/
├── college_placement.db          # SQLite database
├── schema.sql                    # Database schema
├── init_db.py                    # Initialize DB + seed schools + register sources
├── ingest_placements.py          # Parse placement markdown → SQLite
├── ingest_athletes.py            # Parse athlete commit markdown → SQLite
├── ingest_uc.py                  # Parse UC InfoCenter CSV → SQLite
└── query.py                      # CLI query tool

raw/
├── school-profiles/
│   └── {school-slug}/
│       ├── {year}_school-profile.pdf   # Original PDF (keep)
│       ├── {year}_school-profile.md    # LLM-extracted text
│       └── college-outcomes-{years}.md # Matriculation data
├── uc-infocenter/
│   └── {year}_source-school.csv        # UC bulk data
└── athlete-commits/
    └── {school-slug}/
        └── {year}_athlete_commits.md   # Name | Sport | College table
```
