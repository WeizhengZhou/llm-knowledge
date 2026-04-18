#!/usr/bin/env python3
"""
Ingest college placement data into SQLite from extracted markdown files.

This is the main workhorse for school profile PDFs and matriculation lists.
After a PDF is extracted to markdown (by an LLM agent), this script parses
the structured data and inserts it into the placements table.

Usage:
    # Import and call programmatically:
    from ingest_placements import ingest_placement_records, normalize_college
    records = [
        {"college": "Stanford University", "count": 7, "grad_year": 2025, "metric": "enrolled"},
        {"college": "Duke University", "count": 5, "grad_year": 2025, "metric": "enrolled"},
    ]
    ingest_placement_records(db, records, "sacred-heart-atherton", source="school_profile_pdf", source_url="...")

    # Or parse a markdown file:
    python ingest_placements.py <markdown_file> <school_id> --source school_profile_pdf --source-url <url>
"""

import sqlite3
import re
import sys
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "college_placement.db"

# Import normalize_college from ingest_athletes to share the normalization logic
sys.path.insert(0, str(Path(__file__).parent))
from ingest_athletes import normalize_college


def ingest_placement_records(
    db: sqlite3.Connection,
    records: list[dict],
    school_id: str,
    source: str,
    source_url: str = None,
    confidence: str = "L2",
):
    """Insert placement records into the database.

    records: list of dicts with keys:
        - college (str, required)
        - count (int, required)
        - grad_year (int, required)
        - metric (str, default 'enrolled'): 'enrolled', 'accepted', or 'applied'
        - notes (str, optional)
    """
    inserted = 0
    for rec in records:
        college_norm = normalize_college(rec["college"])
        metric = rec.get("metric", "enrolled")
        try:
            db.execute(
                """INSERT OR REPLACE INTO placements
                (school_id, grad_year, college, college_normalized, metric, count,
                 source, source_url, confidence, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (school_id, rec["grad_year"], rec["college"], college_norm,
                 metric, rec["count"], source, source_url, confidence,
                 rec.get("notes")),
            )
            inserted += 1
        except sqlite3.Error as e:
            print(f"Error inserting {rec['college']} {rec['grad_year']}: {e}")
    db.commit()
    return inserted


def parse_placement_markdown(text: str, default_year: int = None) -> list[dict]:
    """Parse a markdown file containing college placement data.

    Handles formats:
    1. Table: | College | 2021 | 2022 | 2023 | 2024 | 2025 |
    2. Table: | College | Count | Year |
    3. List: - Stanford University (7)
    4. List: - Stanford University: 7 enrolled
    """
    records = []
    lines = text.strip().split("\n")

    # Try to detect table format
    header_line = None
    for i, line in enumerate(lines):
        if "|" in line and ("College" in line or "University" in line or "School" in line):
            header_line = i
            break

    if header_line is not None:
        # Parse table
        headers = [h.strip() for h in lines[header_line].split("|") if h.strip()]
        # Check if headers contain year columns
        year_cols = {}
        for j, h in enumerate(headers):
            try:
                year = int(h)
                if 2015 <= year <= 2030:
                    year_cols[j] = year
            except ValueError:
                pass

        # Skip separator line
        data_start = header_line + 2

        for line in lines[data_start:]:
            if not line.strip() or "---" in line:
                continue
            if "|" not in line:
                break
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if not parts:
                continue

            college = parts[0]
            if not college or college.startswith("---"):
                continue

            if year_cols:
                # Multi-year table
                for j, year in year_cols.items():
                    if j < len(parts):
                        count = _parse_count(parts[j])
                        if count and count > 0:
                            records.append({
                                "college": college,
                                "count": count,
                                "grad_year": year,
                                "metric": "enrolled",
                            })
            elif len(parts) >= 2:
                # Simple two-column table
                count = _parse_count(parts[1])
                year = default_year
                if len(parts) >= 3:
                    try:
                        year = int(parts[2])
                    except ValueError:
                        pass
                if count and count > 0 and year:
                    records.append({
                        "college": college,
                        "count": count,
                        "grad_year": year,
                        "metric": "enrolled",
                    })
    else:
        # Try list format
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # "- Stanford University (7)" or "Stanford University: 7"
            m = re.match(r'^[-*]\s*(.+?)\s*\((\d+)\)', line)
            if not m:
                m = re.match(r'^[-*]\s*(.+?):\s*(\d+)', line)
            if m and default_year:
                records.append({
                    "college": m.group(1).strip(),
                    "count": int(m.group(2)),
                    "grad_year": default_year,
                    "metric": "enrolled",
                })

    return records


def _parse_count(val: str) -> int | None:
    """Parse a count value, handling various formats."""
    val = val.strip()
    if not val or val == "-" or val == "—" or val == "n/a":
        return None
    # Remove any non-numeric prefix/suffix
    m = re.search(r'(\d+)', val)
    if m:
        return int(m.group(1))
    return None


def update_source_status(db: sqlite3.Connection, school_id: str, source_type: str, url: str, status: str = "ingested"):
    """Mark a source as ingested in the sources table."""
    db.execute(
        """UPDATE sources SET status = ?, ingested_date = date('now')
        WHERE school_id = ? AND source_type = ? AND url = ?""",
        (status, school_id, source_type, url),
    )
    db.commit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ingest_placements.py <markdown_file> <school_id> [--source TYPE] [--source-url URL] [--year YEAR]")
        sys.exit(1)

    md_file = Path(sys.argv[1])
    school_id = sys.argv[2]

    source = "school_profile_pdf"
    source_url = None
    default_year = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--source":
            source = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--source-url":
            source_url = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--year":
            default_year = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    text = md_file.read_text()
    records = parse_placement_markdown(text, default_year)

    if not records:
        print(f"No placement records found in {md_file}")
        sys.exit(1)

    db = sqlite3.connect(DB_PATH)
    n = ingest_placement_records(db, records, school_id, source, source_url)
    print(f"Inserted {n} placement records for {school_id}")

    if source_url:
        update_source_status(db, school_id, source, source_url)

    db.close()
