#!/usr/bin/env python3
"""Ingest SHS Where Do Gators Go data into SQLite."""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ingest_athletes import normalize_college

DB_PATH = Path(__file__).parent / "college_placement.db"

# SHS Class of 2025 — from Where Do Gators Go PDF
SHS_2025 = [
    # Colleges with 10+ applications: (college, applied, accepted, enrolled)
    ("Santa Clara University", 53, 31, 7),
    ("UCLA", 50, 6, 2),
    ("UC Berkeley", 47, 9, 2),
    ("UC Santa Barbara", 45, 13, 3),
    ("California Polytechnic State University (SLO)", 43, 18, 3),
    ("UC San Diego", 39, 9, 1),
    ("University of Southern California", 33, 7, 5),
    ("San Diego State University", 33, 12, 1),
    ("University of Colorado-Boulder", 32, 26, 5),
    ("Loyola Marymount University", 30, 19, 1),
    ("UC Davis", 27, 6, 1),
    ("University of Michigan", 27, 4, 1),
    ("University of Washington-Seattle", 27, 18, 2),
    ("Chapman University", 26, 24, 4),
    ("Stanford University", 26, 7, 7),
    ("Boston College", 24, 6, 3),
    ("University of Wisconsin-Madison", 24, 11, 1),
    ("Indiana University-Bloomington", 23, 22, 2),
    ("University of Arizona", 23, 23, 0),
    ("Southern Methodist University", 22, 20, 4),
    ("University of San Diego", 22, 16, 1),
    ("Texas Christian University", 21, 19, 3),
    ("UC Irvine", 21, 2, 0),
    ("UC Santa Cruz", 20, 18, 1),
    ("University of Oregon", 20, 19, 1),
    ("University of Virginia", 20, 6, 5),
    ("San Jose State University", 19, 17, 1),
    ("Duke University", 18, 0, 0),
    ("Northeastern University", 18, 16, 2),
    ("UC Riverside", 17, 16, 2),
    ("Tulane University", 15, 6, 3),
    ("Wake Forest University", 15, 4, 2),
    ("Boston University", 14, 7, 2),
    ("Brown University", 14, 1, 1),
    ("Harvard University", 14, 2, 1),
    ("Northwestern University", 14, 2, 2),
    ("Princeton University", 14, 2, 2),
    ("University of Miami", 14, 7, 4),
    ("University of Pennsylvania", 14, 1, 1),
    ("California State University-Long Beach", 13, 4, 0),
    ("San Francisco State University", 13, 13, 0),
    ("University of Denver", 13, 13, 1),
    ("University of Notre Dame", 13, 5, 5),
    ("Clemson University", 12, 6, 0),
    ("Gonzaga University", 12, 12, 0),
    ("Claremont McKenna College", 11, 6, 6),
    ("Cornell University", 11, 4, 2),
    ("Georgetown University", 11, 0, 0),
    ("University of Chicago", 11, 3, 3),
    ("Carnegie Mellon University", 10, 3, 2),
    ("Dartmouth College", 10, 1, 1),
    ("Vanderbilt University", 10, 3, 3),
]

# Fewer than 10 applications — enrolled count in parens, default 1
SHS_2025_SMALL = [
    ("American University", 1), ("Brandeis University", 1), ("Canada College", 1),
    ("California State University-San Marcos", 1), ("Case Western Reserve University", 2),
    ("Colorado State University", 2), ("Colgate University", 2), ("Consumnes River College", 1),
    ("Denison University", 1), ("Elon University", 1), ("Emory University", 1),
    ("Grinnell College", 1), ("Haverford College", 1), ("Lehigh University", 3),
    ("Massachusetts Institute of Technology", 1), ("New York University", 2),
    ("Oxford College of Emory University", 1), ("Parsons School of Design", 1),
    ("Pitzer College", 1), ("Pomona College", 2), ("Purdue University", 1),
    ("Rhode Island School of Design", 1), ("San Joaquin Delta College", 1),
    ("Scripps College", 1), ("Solano Community College", 1),
    ("US Air Force Academy", 1), ("US Naval Academy", 1),
    ("University of Georgia", 1), ("University of Kansas", 1),
    ("University of North Carolina-Chapel Hill", 1), ("University of Oxford", 1),
    ("University of Redlands", 1), ("University of San Francisco", 2),
    ("University of St. Andrews", 1), ("University of St. Thomas", 1),
    ("University of Utah", 1), ("Villanova University", 1),
    ("Washington University in St. Louis", 1), ("William & Mary", 1),
    ("Yale University", 1),
]

# SHS Class of 2023 — from Where Do Gators Go PDF
SHS_2023 = [
    ("UCLA", 78, 13, 7),
    ("UC Santa Barbara", 70, 16, 2),
    ("UC Berkeley", 68, 17, 6),
    ("California Polytechnic State University (SLO)", 65, 31, 5),
    ("UC San Diego", 59, 11, 1),
    ("Santa Clara University", 56, 34, 9),
    ("University of Southern California", 50, 5, 4),
    ("University of San Diego", 47, 22, 2),
    ("University of Washington-Seattle", 44, 12, 1),
    ("Loyola Marymount University", 42, 19, 3),
    ("San Diego State University", 40, 11, 2),
    ("University of Michigan", 38, 7, 4),
    ("Northeastern University", 36, 18, 5),
    ("Boston College", 35, 13, 7),
    ("UC Santa Cruz", 34, 19, 1),
    ("University of Colorado-Boulder", 28, 20, 1),
    ("University of Wisconsin-Madison", 27, 11, 3),
    ("University of Virginia", 26, 2, 1),
    ("Boston University", 24, 10, 3),
    ("New York University", 24, 7, 3),
    ("Stanford University", 24, 7, 5),
    ("Texas Christian University", 24, 11, 2),
    ("Northwestern University", 23, 3, 3),
    ("San Jose State University", 23, 21, 2),
    ("Villanova University", 23, 6, 2),
    ("Wake Forest University", 21, 4, 1),
    ("Princeton University", 20, 5, 5),
    ("Tulane University", 19, 9, 1),
    ("UC Riverside", 18, 14, 2),
    ("California State University-Long Beach", 17, 5, 1),
    ("Chapman University", 17, 15, 4),
    ("Georgetown University", 17, 2, 2),
    ("Harvard University", 17, 4, 3),
    ("Pomona College", 17, 3, 2),
    ("Brown University", 16, 2, 1),
    ("University of Miami", 16, 2, 2),
    ("Tufts University", 15, 4, 3),
    ("University of Notre Dame", 15, 3, 2),
    ("Southern Methodist University", 14, 14, 1),
    ("University of Arizona", 14, 13, 2),
    ("Dartmouth College", 13, 3, 3),
    ("Syracuse University", 12, 9, 1),
    ("Columbia University", 11, 1, 1),
    ("Duke University", 11, 3, 3),
    ("Pepperdine University", 10, 5, 1),
    ("San Francisco State University", 10, 10, 1),
    ("Sonoma State University", 10, 9, 1),
]

SHS_2023_SMALL = [
    ("American University", 1), ("Babson College", 1), ("Brandeis University", 1),
    ("Canada College", 1), ("Carnegie Mellon University", 1),
    ("Claremont McKenna College", 2), ("Clemson University", 1),
    ("Colby College", 1), ("Colgate University", 1), ("College of San Mateo", 3),
    ("Elon University", 1), ("Emerson College", 1), ("Foothill College", 2),
    ("Iona College", 1), ("Lewis & Clark College", 1),
    ("Manhattan College of Music", 1), ("Occidental College", 1),
    ("Parsons School of Design", 1), ("Pitzer College", 1),
    ("Purdue University", 1), ("Rice University", 1),
    ("Santa Monica College", 1), ("Sarah Lawrence College", 1),
    ("School of the Art Institute of Chicago", 1), ("Skidmore College", 1),
    ("Swarthmore College", 1), ("The University of Tennessee", 1),
    ("The University of Texas at Austin", 1), ("US Naval Academy", 1),
    ("University of Cambridge", 1), ("University of Chicago", 1),
    ("University of Denver", 1), ("University of Florida", 1),
    ("University of Puget Sound", 1), ("University of Redlands", 1),
    ("University of San Francisco", 1), ("University of Utah", 1),
    ("Williams College", 2), ("Yale University", 1),
]


def main():
    db = sqlite3.connect(DB_PATH)
    total = 0

    # Class of 2025
    for college, applied, accepted, enrolled in SHS_2025:
        cn = normalize_college(college)
        for metric, count in [("applied", applied), ("accepted", accepted), ("enrolled", enrolled)]:
            if count > 0:
                db.execute(
                    """INSERT OR REPLACE INTO placements
                    (school_id, grad_year, college, college_normalized, metric, count,
                     source, source_url, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("sacred-heart-atherton", 2025, college, cn, metric, count,
                     "school_profile_pdf",
                     "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_228662.pdf",
                     "L1"),
                )
                total += 1

    for college, enrolled in SHS_2025_SMALL:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("sacred-heart-atherton", 2025, college, cn, "enrolled", enrolled,
             "school_profile_pdf",
             "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_228662.pdf",
             "L1", "Fewer than 10 applications"),
        )
        total += 1

    # Class of 2023
    for college, applied, accepted, enrolled in SHS_2023:
        cn = normalize_college(college)
        for metric, count in [("applied", applied), ("accepted", accepted), ("enrolled", enrolled)]:
            if count > 0:
                db.execute(
                    """INSERT OR REPLACE INTO placements
                    (school_id, grad_year, college, college_normalized, metric, count,
                     source, source_url, confidence)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("sacred-heart-atherton", 2023, college, cn, metric, count,
                     "school_profile_pdf",
                     "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_216012.pdf",
                     "L1"),
                )
                total += 1

    for college, enrolled in SHS_2023_SMALL:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("sacred-heart-atherton", 2023, college, cn, "enrolled", enrolled,
             "school_profile_pdf",
             "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_216012.pdf",
             "L1", "Fewer than 10 applications"),
        )
        total += 1

    # Update school profile metadata
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, source_url)
        VALUES (?, ?, ?, ?)""",
        ("sacred-heart-atherton", "2024-25", 160,
         "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_228662.pdf"),
    )
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, source_url)
        VALUES (?, ?, ?, ?)""",
        ("sacred-heart-atherton", "2022-23", 171,
         "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_216012.pdf"),
    )

    # Mark sources as ingested
    db.execute(
        """UPDATE sources SET status = 'ingested', ingested_date = date('now')
        WHERE school_id = 'sacred-heart-atherton' AND source_type = 'school_profile_pdf'"""
    )
    db.execute(
        """UPDATE sources SET status = 'ingested', ingested_date = date('now')
        WHERE school_id = 'sacred-heart-atherton' AND source_type = 'google_doc'"""
    )

    db.commit()
    print(f"Inserted {total} SHS placement records (2023 + 2025)")
    print(f"School profiles: 2 years")

    db.close()


if __name__ == "__main__":
    main()
