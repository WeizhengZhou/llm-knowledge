#!/usr/bin/env python3
"""
Gemini-powered extraction for student profiles.

Uses Gemini 2.5 Flash to extract structured data from Reddit posts and
YouTube transcripts that the rule-based parser can't handle.

Usage:
    # Extract all unprocessed files from a source
    python gemini_extractor.py --source youtube --max 10

    # Extract specific files
    python gemini_extractor.py --files raw/youtube/abc123.md raw/reddit/collegeresults/xyz789.md

    # Dry run (print extracted JSON, don't save)
    python gemini_extractor.py --source youtube --max 3 --dry-run

    # Re-extract files that had 0 results with rule-based parser
    python gemini_extractor.py --reextract --max 20
"""

import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from datetime import datetime

# Load API key
ENV_PATH = Path("/Users/weizheng/projects/claude/kid_camp2/backend/.env")
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().split("\n"):
        if line.startswith("GOOGLE_API_KEY="):
            os.environ["GOOGLE_API_KEY"] = line.split("=", 1)[1].strip()
            break

import google.generativeai as genai

# Configure
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

DB_PATH = Path(__file__).parent / "profiles.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
RAW_DIR = Path(__file__).parent / "raw"

sys.path.insert(0, str(Path(__file__).parent.parent))
from ingest_athletes import normalize_college

EXTRACTION_PROMPT = """Extract structured data from this college application post/transcript. Return ONLY valid JSON.

If a field is not mentioned or unclear, use null. For results, include ALL colleges mentioned with their outcomes.
For YouTube transcripts, the data is spoken — parse carefully through the narrative.

REQUIRED JSON SCHEMA:
{
  "extraction_confidence": <float 0.0-1.0>,
  "application_year": <int or null>,
  "demographics": {
    "gender": "<male|female|nonbinary|null>",
    "ethnicity": "<asian|white|black|hispanic|multiracial|null>",
    "ethnicity_detail": "<e.g. chinese-american|null>",
    "first_gen": <true|false|null>,
    "legacy": "<undergrad|graduate|double|null>",
    "state": "<2-letter code|null>",
    "region": "<bay-area|socal|northeast|southeast|midwest|west|null>",
    "school_type": "<private|public|charter|magnet|homeschool|null>",
    "school_name_hint": "<if mentioned|null>",
    "hooks": ["<legacy|athlete|first-gen|urm|low-income|none>"]
  },
  "academics": {
    "gpa_uw": <float|null>,
    "gpa_w": <float|null>,
    "sat": <int 400-1600|null>,
    "act": <int 1-36|null>,
    "ap_count": <int|null>,
    "class_rank": "<text|null>"
  },
  "extracurriculars": [
    {"activity": "<name>", "level": "<school|state|national|international|null>"}
  ],
  "awards": [
    {"name": "<award>", "level": "<school|state|national|international>"}
  ],
  "results": [
    {"college": "<full name>", "round": "<ED|EA|REA|RD|null>", "result": "<accepted|rejected|waitlisted|deferred>", "enrolled": <true|false|null>}
  ]
}

POST/TRANSCRIPT CONTENT:
"""

MODEL_NAME = "gemini-2.5-flash"
RATE_LIMIT = 1.0  # seconds between API calls


def extract_with_gemini(text: str, retries: int = 2) -> dict | None:
    """Extract structured profile using Gemini."""
    # Truncate very long texts (YouTube transcripts can be huge)
    if len(text) > 15000:
        text = text[:15000] + "\n[TRUNCATED]"

    model = genai.GenerativeModel(MODEL_NAME)

    for attempt in range(retries + 1):
        try:
            response = model.generate_content(
                EXTRACTION_PROMPT + text,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=4096,
                    response_mime_type="application/json",
                ),
            )

            # Parse JSON from response
            result_text = response.text.strip()
            # Remove markdown code fences if present
            if result_text.startswith("```"):
                result_text = result_text.split("\n", 1)[1]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                result_text = result_text.strip()

            return json.loads(result_text)

        except json.JSONDecodeError as e:
            print(f"    JSON parse error (attempt {attempt+1}): {e}")
            if attempt < retries:
                time.sleep(RATE_LIMIT * 2)
        except Exception as e:
            print(f"    Gemini error (attempt {attempt+1}): {e}")
            if attempt < retries:
                time.sleep(RATE_LIMIT * 3)

    return None


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (metadata, body)."""
    fm = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    fm[key.strip()] = val.strip().strip('"')
            body = parts[2].strip()
    return fm, body


def store_profile(db: sqlite3.Connection, profile: dict, meta: dict):
    """Store extracted profile in SQLite."""
    source = meta.get("source", "unknown")
    source_id = meta.get("source_id", "")

    # Determine original domain
    url = meta.get("url", "")
    if "youtube.com" in url or "youtu.be" in url:
        original_domain = "youtube.com"
    elif "reddit.com" in url:
        original_domain = "reddit.com"
    else:
        original_domain = ""

    demo = profile.get("demographics", {})
    acad = profile.get("academics", {})

    # Delete old data if exists
    existing = db.execute(
        "SELECT id FROM student_profiles WHERE source=? AND source_id=?",
        (source, source_id)).fetchone()
    if existing:
        db.execute("DELETE FROM application_results WHERE profile_id=?", (existing[0],))
        db.execute("DELETE FROM student_profiles WHERE id=?", (existing[0],))

    cursor = db.execute(
        """INSERT INTO student_profiles
        (source, source_id, source_url, extraction_confidence,
         application_year, gender, ethnicity, ethnicity_detail,
         first_gen, legacy, state, region, school_type,
         school_name_hint, school_size_hint, hooks_json,
         gpa_uw, gpa_w, class_rank, sat, act, ap_count,
         ecs_json, awards_json, essay_topics,
         original_domain, original_url, post_date, extraction_method)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (source, source_id, meta.get("url", ""),
         profile.get("extraction_confidence", 0.8),
         profile.get("application_year"),
         demo.get("gender"), demo.get("ethnicity"), demo.get("ethnicity_detail"),
         demo.get("first_gen"), demo.get("legacy"),
         demo.get("state"), demo.get("region"), demo.get("school_type"),
         demo.get("school_name_hint"), demo.get("school_size_hint"),
         json.dumps(demo.get("hooks", [])),
         acad.get("gpa_uw"), acad.get("gpa_w"), acad.get("class_rank"),
         acad.get("sat"), acad.get("act"), acad.get("ap_count"),
         json.dumps(profile.get("extracurriculars", [])),
         json.dumps(profile.get("awards", [])),
         profile.get("essay_topics"),
         original_domain, meta.get("url", ""),
         meta.get("upload_date", meta.get("created_utc", "")),
         "llm"),
    )

    profile_id = cursor.lastrowid

    for result in profile.get("results", []):
        college = result.get("college", "")
        if not college:
            continue
        cn = normalize_college(college)
        try:
            db.execute(
                """INSERT OR IGNORE INTO application_results
                (profile_id, college, college_normalized, round, result, enrolled, scholarship)
                VALUES (?,?,?,?,?,?,?)""",
                (profile_id, college, cn, result.get("round"),
                 result.get("result", "accepted"),
                 result.get("enrolled", False),
                 result.get("scholarship")),
            )
        except sqlite3.Error:
            pass

    return profile_id


def process_file(filepath: Path, db: sqlite3.Connection, dry_run: bool = False) -> int:
    """Process a single raw file with Gemini extraction."""
    text = filepath.read_text()
    meta, body = parse_frontmatter(text)

    print(f"  Extracting: {filepath.name} ({len(body)} chars)...")

    profile = extract_with_gemini(body)
    time.sleep(RATE_LIMIT)

    if not profile:
        print(f"    FAILED: no extraction result")
        return 0

    results = profile.get("results", [])

    if dry_run:
        print(f"    Gender: {profile.get('demographics', {}).get('gender')}")
        print(f"    Ethnicity: {profile.get('demographics', {}).get('ethnicity')}")
        print(f"    SAT: {profile.get('academics', {}).get('sat')}")
        print(f"    GPA UW: {profile.get('academics', {}).get('gpa_uw')}")
        print(f"    Results: {len(results)} schools")
        for r in results[:5]:
            print(f"      {r.get('college', '?'):30s} → {r.get('result', '?')}")
        if len(results) > 5:
            print(f"      ... and {len(results)-5} more")
        return len(results)

    pid = store_profile(db, profile, meta)
    print(f"    Stored profile {pid}: {len(results)} results")
    return len(results)


def get_zero_result_profiles() -> list:
    """Find profiles that were extracted with rule-based but got 0 results."""
    db = sqlite3.connect(DB_PATH)
    rows = db.execute("""
        SELECT sp.source, sp.source_id
        FROM student_profiles sp
        WHERE sp.id NOT IN (SELECT DISTINCT profile_id FROM application_results)
        AND (sp.extraction_method IS NULL OR sp.extraction_method = 'rule_based')
    """).fetchall()
    db.close()

    files = []
    for source, source_id in rows:
        # Map source to file path
        if "reddit" in source:
            sid = source_id.replace("t3_", "")
            path = RAW_DIR / "reddit" / "collegeresults" / f"{sid}.md"
        elif "youtube" in source:
            path = RAW_DIR / "youtube" / f"{source_id}.md"
        else:
            continue
        if path.exists():
            files.append(path)

    return files


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, help="Source to extract: youtube, reddit/collegeresults")
    parser.add_argument("--files", nargs="+", type=Path, help="Specific files to extract")
    parser.add_argument("--reextract", action="store_true", help="Re-extract profiles that had 0 results")
    parser.add_argument("--max", type=int, default=10, help="Max files to process")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Determine files to process
    if args.files:
        files = [f for f in args.files if f.exists()]
    elif args.reextract:
        files = get_zero_result_profiles()[:args.max]
        print(f"Found {len(files)} profiles with 0 results to re-extract")
    elif args.source:
        source_dir = RAW_DIR / args.source.replace("/", "/")
        if not source_dir.exists():
            # Try common patterns
            for pattern in [args.source, f"reddit/{args.source}"]:
                candidate = RAW_DIR / pattern
                if candidate.exists():
                    source_dir = candidate
                    break
        files = sorted(source_dir.glob("*.md"))[:args.max]
    else:
        print("Provide --source, --files, or --reextract")
        sys.exit(1)

    if not files:
        print("No files to process")
        return

    print(f"Processing {len(files)} files with Gemini ({MODEL_NAME})...")

    db = None
    if not args.dry_run:
        db = sqlite3.connect(DB_PATH)
        db.executescript(SCHEMA_PATH.read_text())

    total_results = 0
    processed = 0
    for f in files:
        n = process_file(f, db, dry_run=args.dry_run)
        total_results += n
        processed += 1

    if db:
        db.commit()
        total_profiles = db.execute("SELECT COUNT(*) FROM student_profiles").fetchone()[0]
        total_ar = db.execute("SELECT COUNT(*) FROM application_results").fetchone()[0]
        print(f"\nProcessed {processed} files, extracted {total_results} results")
        print(f"DB totals: {total_profiles} profiles, {total_ar} results")
        db.close()
    else:
        print(f"\n[DRY RUN] Processed {processed} files, found {total_results} results")


if __name__ == "__main__":
    main()
