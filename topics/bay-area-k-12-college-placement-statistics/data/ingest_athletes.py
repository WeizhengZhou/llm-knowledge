#!/usr/bin/env python3
"""
Ingest athlete commit data into SQLite.

Usage:
    # After extracting athlete data to markdown, run:
    python ingest_athletes.py <markdown_file> <school_id> <grad_year>

    # Or import and call from another script:
    from ingest_athletes import ingest_athlete_records
    ingest_athlete_records(db, records, school_id, grad_year, source_url)

The markdown file should have rows like:
    | Student Name | Sport | College |
    or plain text lines: "Name - Sport - College"
"""

import sqlite3
import re
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "college_placement.db"


def normalize_college(name: str) -> str:
    """Normalize college name to a consistent slug."""
    name = name.strip().lower()
    # Common normalizations
    replacements = {
        "university of california, berkeley": "uc-berkeley",
        "university of california, los angeles": "uc-los-angeles",
        "university of california at berkeley": "uc-berkeley",
        "uc berkeley": "uc-berkeley",
        "ucla": "uc-los-angeles",
        "usc": "usc",
        "university of southern california": "usc",
        "stanford university": "stanford",
        "stanford": "stanford",
        "harvard university": "harvard",
        "harvard college": "harvard",
        "yale university": "yale",
        "princeton university": "princeton",
        "columbia university": "columbia",
        "university of pennsylvania": "upenn",
        "penn": "upenn",
        "brown university": "brown",
        "dartmouth college": "dartmouth",
        "cornell university": "cornell",
        "duke university": "duke",
        "massachusetts institute of technology": "mit",
        "mit": "mit",
        "california institute of technology": "caltech",
        "caltech": "caltech",
        "university of chicago": "uchicago",
        "northwestern university": "northwestern",
        "johns hopkins university": "jhu",
        "georgetown university": "georgetown",
        "notre dame": "notre-dame",
        "university of notre dame": "notre-dame",
    }
    for full, slug in replacements.items():
        if name == full:
            return slug
    # Generic: lowercase, replace spaces/special chars with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', name).strip('-')
    return slug


def ingest_athlete_records(db: sqlite3.Connection, records: list, school_id: str, grad_year: int, source_url: str):
    """Insert athlete commit records into the database.

    records: list of dicts with keys: name, sport, college, division (optional)
    """
    inserted = 0
    for rec in records:
        college_norm = normalize_college(rec["college"])
        try:
            db.execute(
                """INSERT OR IGNORE INTO athlete_commits
                (school_id, grad_year, student_name, sport, college, college_normalized, division, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (school_id, grad_year, rec.get("name"), rec["sport"],
                 rec["college"], college_norm, rec.get("division"), source_url),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            pass
    db.commit()
    return inserted


def parse_markdown_table(text: str) -> list:
    """Parse a markdown table of athlete commits."""
    records = []
    lines = text.strip().split("\n")
    for line in lines:
        # Skip header and separator lines
        if not line.strip() or line.strip().startswith("---") or "Student" in line or "Name" in line and "Sport" in line:
            continue
        # Parse pipe-delimited rows
        if "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 3:
                records.append({
                    "name": parts[0],
                    "sport": parts[1],
                    "college": parts[2],
                    "division": parts[3] if len(parts) > 3 else None,
                })
    return records


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python ingest_athletes.py <markdown_file> <school_id> <grad_year>")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    school_id = sys.argv[2]
    grad_year = int(sys.argv[3])

    text = md_file.read_text()
    records = parse_markdown_table(text)

    db = sqlite3.connect(DB_PATH)
    n = ingest_athlete_records(db, records, school_id, grad_year, f"file://{md_file}")
    print(f"Inserted {n} athlete commit records for {school_id} class of {grad_year}")
    db.close()
