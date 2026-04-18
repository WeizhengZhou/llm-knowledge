-- Student Application Profile Database
-- Stores self-reported student profiles and application outcomes
-- from public sources (Reddit, YouTube, College Confidential)

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS student_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_id TEXT NOT NULL,
    source_url TEXT,
    extraction_confidence REAL,
    application_year INTEGER,
    gender TEXT,
    ethnicity TEXT,
    ethnicity_detail TEXT,
    first_gen BOOLEAN,
    legacy TEXT,
    state TEXT,
    region TEXT,
    school_type TEXT,
    school_name_hint TEXT,
    school_id TEXT,
    school_size_hint TEXT,
    hooks_json TEXT,
    gpa_uw REAL,
    gpa_w REAL,
    class_rank TEXT,
    sat INTEGER,
    act INTEGER,
    ap_count INTEGER,
    ecs_json TEXT,
    awards_json TEXT,
    essay_topics TEXT,
    raw_text TEXT,
    original_domain TEXT,           -- 'reddit.com', 'youtube.com', 'collegeconfidential.com'
    original_url TEXT,              -- full original URL
    post_date TEXT,                 -- original post/upload date
    extraction_method TEXT,         -- 'rule_based', 'llm', 'manual'
    crawled_at TEXT,
    extracted_at TEXT DEFAULT (datetime('now')),
    UNIQUE(source, source_id)
);

CREATE TABLE IF NOT EXISTS application_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL REFERENCES student_profiles(id),
    college TEXT NOT NULL,
    college_normalized TEXT NOT NULL,
    round TEXT,
    result TEXT NOT NULL CHECK(result IN ('accepted','rejected','waitlisted','deferred')),
    enrolled BOOLEAN DEFAULT FALSE,
    scholarship TEXT,
    UNIQUE(profile_id, college_normalized, round)
);

CREATE INDEX IF NOT EXISTS idx_profiles_ethnicity ON student_profiles(ethnicity);
CREATE INDEX IF NOT EXISTS idx_profiles_state ON student_profiles(state);
CREATE INDEX IF NOT EXISTS idx_profiles_school ON student_profiles(school_type, region);
CREATE INDEX IF NOT EXISTS idx_profiles_year ON student_profiles(application_year);
CREATE INDEX IF NOT EXISTS idx_results_college ON application_results(college_normalized);
CREATE INDEX IF NOT EXISTS idx_results_result ON application_results(result);
