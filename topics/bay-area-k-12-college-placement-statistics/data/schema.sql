-- Bay Area K-12 College Placement Database
-- Created: 2026-04-18
-- Purpose: Structured storage for college placement stats across Bay Area private schools

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Schools we track
CREATE TABLE IF NOT EXISTS schools (
    school_id TEXT PRIMARY KEY,           -- slug: 'sacred-heart-atherton'
    name TEXT NOT NULL,
    short_name TEXT,                      -- 'SHS', 'Harker', etc.
    city TEXT,
    state TEXT DEFAULT 'CA',
    type TEXT CHECK(type IN ('private','public')),
    grades TEXT,                          -- 'K-12', '9-12', '6-12'
    website TEXT,
    ceeb_code TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Annual college placement: one row per school-year-college
CREATE TABLE IF NOT EXISTS placements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id TEXT NOT NULL REFERENCES schools(school_id),
    grad_year INTEGER NOT NULL,
    college TEXT NOT NULL,
    college_normalized TEXT NOT NULL,     -- lowercase slug for joins
    metric TEXT NOT NULL CHECK(metric IN ('enrolled','accepted','applied')),
    count INTEGER NOT NULL,
    source TEXT NOT NULL,                 -- 'school_profile_pdf', 'school_google_doc', 'uc_infocenter', 'niche', 'school_website'
    source_url TEXT,
    confidence TEXT DEFAULT 'L2' CHECK(confidence IN ('L1','L2','L3','L4','L5')),
    extracted_date TEXT DEFAULT (date('now')),
    notes TEXT,
    UNIQUE(school_id, grad_year, college_normalized, metric, source)
);

-- UC-specific admissions data (from UC InfoCenter)
CREATE TABLE IF NOT EXISTS uc_admissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id TEXT NOT NULL REFERENCES schools(school_id),
    school_name_uc TEXT,                 -- name as it appears in UC data
    year INTEGER NOT NULL,               -- admission cycle year
    uc_campus TEXT NOT NULL,             -- 'berkeley', 'ucla', 'davis', etc.
    ethnicity TEXT DEFAULT 'All',        -- 'All', 'Asian', 'White', 'Hispanic', etc.
    applicants INTEGER,
    admits INTEGER,
    enrollees INTEGER,
    mean_gpa REAL,
    source_url TEXT,
    extracted_date TEXT DEFAULT (date('now')),
    UNIQUE(school_id, year, uc_campus, ethnicity)
);

-- School profile metadata (one row per school per year)
CREATE TABLE IF NOT EXISTS school_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id TEXT NOT NULL REFERENCES schools(school_id),
    academic_year TEXT NOT NULL,          -- '2024-25'
    grad_class_size INTEGER,
    total_enrollment INTEGER,
    ap_courses_offered INTEGER,
    mean_sat INTEGER,
    median_sat INTEGER,
    mean_act REAL,
    median_act REAL,
    national_merit_semifinalists INTEGER,
    national_merit_finalists INTEGER,
    college_going_rate_4yr REAL,         -- percentage
    mean_gpa_weighted REAL,
    mean_gpa_unweighted REAL,
    source_url TEXT,
    raw_file_path TEXT,                  -- path to extracted markdown
    extracted_date TEXT DEFAULT (date('now')),
    UNIQUE(school_id, academic_year)
);

-- Athlete commits (name-level, from school signing day announcements)
CREATE TABLE IF NOT EXISTS athlete_commits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id TEXT NOT NULL REFERENCES schools(school_id),
    grad_year INTEGER NOT NULL,
    student_name TEXT,
    sport TEXT NOT NULL,
    college TEXT NOT NULL,
    college_normalized TEXT NOT NULL,
    division TEXT,                        -- 'D1', 'D2', 'D3', 'NAIA'
    source_url TEXT,
    extracted_date TEXT DEFAULT (date('now')),
    UNIQUE(school_id, grad_year, student_name, sport, college_normalized)
);

-- Data source registry (what we've ingested)
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_id TEXT REFERENCES schools(school_id),
    source_type TEXT NOT NULL,           -- 'school_profile_pdf', 'uc_infocenter', 'athlete_page', 'google_doc', 'niche', 'aggregator'
    url TEXT,
    file_path TEXT,                      -- local path if downloaded
    years_covered TEXT,                  -- '2021-2025' or '2024-25'
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending','ingested','failed','needs_update')),
    ingested_date TEXT,
    notes TEXT,
    UNIQUE(school_id, source_type, url)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_placements_school_year ON placements(school_id, grad_year);
CREATE INDEX IF NOT EXISTS idx_placements_college ON placements(college_normalized);
CREATE INDEX IF NOT EXISTS idx_uc_school_year ON uc_admissions(school_id, year);
CREATE INDEX IF NOT EXISTS idx_athlete_school_year ON athlete_commits(school_id, grad_year);

-- Views for common analyses

-- Non-athlete placements (total enrolled minus known athlete commits)
CREATE VIEW IF NOT EXISTS v_non_athlete_placements AS
SELECT
    p.school_id,
    p.grad_year,
    p.college,
    p.college_normalized,
    p.count AS total_enrolled,
    COALESCE(a.athlete_count, 0) AS athlete_count,
    p.count - COALESCE(a.athlete_count, 0) AS non_athlete_count
FROM placements p
LEFT JOIN (
    SELECT school_id, grad_year, college_normalized, COUNT(*) AS athlete_count
    FROM athlete_commits
    GROUP BY school_id, grad_year, college_normalized
) a ON p.school_id = a.school_id
    AND p.grad_year = a.grad_year
    AND p.college_normalized = a.college_normalized
WHERE p.metric = 'enrolled';

-- School comparison: Ivy+ placement rates
CREATE VIEW IF NOT EXISTS v_ivy_plus_rates AS
SELECT
    p.school_id,
    p.grad_year,
    SUM(p.count) AS ivy_plus_enrolled,
    sp.grad_class_size,
    ROUND(100.0 * SUM(p.count) / sp.grad_class_size, 1) AS ivy_plus_pct
FROM placements p
JOIN school_profiles sp ON p.school_id = sp.school_id
    AND sp.academic_year = (p.grad_year - 1) || '-' || substr(p.grad_year, 3, 2)
WHERE p.metric = 'enrolled'
    AND p.college_normalized IN (
        'harvard', 'yale', 'princeton', 'columbia', 'upenn', 'brown',
        'dartmouth', 'cornell', 'stanford', 'mit', 'caltech',
        'duke', 'uchicago', 'northwestern', 'jhu'
    )
GROUP BY p.school_id, p.grad_year;
