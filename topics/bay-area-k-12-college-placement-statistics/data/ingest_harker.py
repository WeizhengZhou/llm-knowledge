#!/usr/bin/env python3
"""One-off script to ingest Harker 2023-2025 combined matriculation data."""

import sqlite3
import re
from pathlib import Path

DB_PATH = Path(__file__).parent / "college_placement.db"

sys_path = str(Path(__file__).parent)
import sys
sys.path.insert(0, sys_path)
from ingest_athletes import normalize_college

def main():
    md = (Path(__file__).parent.parent / "raw/school-profiles/harker/college-acceptances-2023-2025.md").read_text()

    db = sqlite3.connect(DB_PATH)
    inserted = 0

    in_table = False
    for line in md.split("\n"):
        if line.startswith("| College"):
            in_table = True
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|") and in_table:
            break
        if not in_table:
            continue

        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 2:
            continue

        college = parts[0]
        try:
            count = int(parts[1])
        except ValueError:
            continue

        college_norm = normalize_college(college)

        # Store as 3-year combined. We'll use grad_year=0 as a convention
        # for multi-year combined data, with a note.
        # Actually, better to distribute: store once per year as count/3 would lose info.
        # Best approach: store as-is with a note about the 3-year window.
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("harker", 2025, college, college_norm, "enrolled", count,
             "school_website",
             "https://www.harker.org/upper-school/support-services/college-counseling/college-acceptances",
             "L1",
             "Combined Classes of 2023-2025 (3 years). Per-year breakdown not available."),
        )
        inserted += 1

    db.commit()
    print(f"Inserted {inserted} Harker placement records (3-year combined, tagged as 2025)")

    # Also update source status
    db.execute(
        """UPDATE sources SET status = 'ingested', ingested_date = date('now')
        WHERE school_id = 'harker' AND source_type = 'school_website'"""
    )
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
