#!/usr/bin/env python3
"""
LLM-powered batch extraction for student profiles.

This script prepares raw posts for LLM extraction and processes the results.
It's designed to work with Claude Code agents — the agent reads the raw files,
extracts structured JSON using its own LLM capabilities, and this script
validates and stores the results.

Usage:
    # Prepare extraction tasks (outputs JSON files for LLM processing)
    python llm_extract_batch.py prepare --source youtube --max 10

    # Import LLM-extracted JSON results
    python llm_extract_batch.py import extracted/youtube_batch_001.json

    # Show extraction stats
    python llm_extract_batch.py stats
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from ingest_athletes import normalize_college

DB_PATH = Path(__file__).parent / "profiles.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
RAW_DIR = Path(__file__).parent / "raw"
EXTRACTED_DIR = Path(__file__).parent / "extracted"


def get_unextracted_files(source: str, max_files: int = 10) -> list:
    """Find raw files that haven't been successfully extracted yet."""
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA_PATH.read_text())

    # Get all source_ids already in DB with results
    existing = set()
    for row in db.execute(
        "SELECT source_id FROM student_profiles WHERE source=? AND id IN (SELECT DISTINCT profile_id FROM application_results)",
        (source,)
    ):
        existing.add(row[0])

    # Find raw files not yet extracted
    source_dir = RAW_DIR / source.replace("/", "/")
    if not source_dir.exists():
        # Try subdirectory patterns
        for pattern in [f"{source}", f"reddit/{source}", f"youtube"]:
            candidate = RAW_DIR / pattern
            if candidate.exists():
                source_dir = candidate
                break

    if not source_dir.exists():
        print(f"Source directory not found: {source_dir}")
        return []

    unextracted = []
    for f in sorted(source_dir.glob("*.md")):
        # Read frontmatter to get source_id
        text = f.read_text()
        source_id = None
        if text.startswith("---"):
            for line in text.split("---", 2)[1].split("\n"):
                if line.startswith("source_id:"):
                    source_id = line.split(":", 1)[1].strip()
                    break

        if source_id and source_id not in existing:
            unextracted.append(f)

        if len(unextracted) >= max_files:
            break

    db.close()
    return unextracted


def import_extracted(json_path: Path):
    """Import LLM-extracted profiles from a JSON file."""
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA_PATH.read_text())

    with open(json_path) as f:
        profiles = json.load(f)

    if not isinstance(profiles, list):
        profiles = [profiles]

    imported = 0
    for entry in profiles:
        source = entry.get("_source", "youtube")
        source_id = entry.get("_source_id", "")
        source_url = entry.get("_source_url", "")
        post_date = entry.get("_post_date", "")
        original_domain = entry.get("_original_domain", "")

        profile = entry.get("profile", entry)
        demo = profile.get("demographics", {})
        acad = profile.get("academics", {})
        results = profile.get("results", [])

        if not results:
            continue

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
            (source, source_id, source_url,
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
             original_domain, source_url, post_date, "llm"),
        )

        profile_id = cursor.lastrowid

        for result in results:
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
                     result.get("result", "accepted"), result.get("enrolled", False),
                     result.get("scholarship")),
                )
            except sqlite3.Error:
                pass

        imported += 1

    db.commit()
    total = db.execute("SELECT COUNT(*) FROM student_profiles").fetchone()[0]
    results_total = db.execute("SELECT COUNT(*) FROM application_results").fetchone()[0]
    print(f"Imported {imported} profiles from {json_path.name}")
    print(f"DB totals: {total} profiles, {results_total} results")
    db.close()


def show_stats():
    """Show extraction statistics."""
    db = sqlite3.connect(DB_PATH)

    total = db.execute("SELECT COUNT(*) FROM student_profiles").fetchone()[0]
    with_results = db.execute(
        "SELECT COUNT(*) FROM student_profiles WHERE id IN (SELECT DISTINCT profile_id FROM application_results)"
    ).fetchone()[0]
    results = db.execute("SELECT COUNT(*) FROM application_results").fetchone()[0]

    print(f"\n=== Extraction Stats ===")
    print(f"Total profiles: {total}")
    print(f"With results: {with_results} ({100*with_results/total:.0f}%)" if total else "")
    print(f"Total results: {results}")

    print(f"\nBy source:")
    for r in db.execute("SELECT source, COUNT(*) FROM student_profiles GROUP BY source ORDER BY COUNT(*) DESC"):
        print(f"  {r[0]:30s} {r[1]:4d}")

    print(f"\nBy extraction method:")
    for r in db.execute("SELECT COALESCE(extraction_method,'rule_based'), COUNT(*) FROM student_profiles GROUP BY extraction_method ORDER BY COUNT(*) DESC"):
        print(f"  {r[0]:20s} {r[1]:4d}")

    print(f"\nExtraction rate (with results) by source:")
    for r in db.execute("""
        SELECT sp.source, COUNT(*) as total,
               SUM(CASE WHEN sp.id IN (SELECT profile_id FROM application_results) THEN 1 ELSE 0 END) as extracted
        FROM student_profiles sp GROUP BY sp.source
    """):
        rate = f"{100*r[2]/r[1]:.0f}%" if r[1] else "n/a"
        print(f"  {r[0]:30s} {r[2]}/{r[1]} ({rate})")

    db.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "prepare":
        source = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--source" else "youtube"
        max_files = 10
        for i, arg in enumerate(sys.argv):
            if arg == "--max" and i + 1 < len(sys.argv):
                max_files = int(sys.argv[i + 1])
        files = get_unextracted_files(source, max_files)
        print(f"Found {len(files)} unextracted files from {source}:")
        for f in files:
            print(f"  {f}")
    elif cmd == "import":
        import_extracted(Path(sys.argv[2]))
    elif cmd == "stats":
        show_stats()
    else:
        print(f"Unknown command: {cmd}")
