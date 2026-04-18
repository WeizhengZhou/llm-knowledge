#!/usr/bin/env python3
"""Ingest SHS Where Do Gators Go data for 2021, 2022, 2024 into SQLite."""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ingest_athletes import normalize_college

DB_PATH = Path(__file__).parent / "college_placement.db"

# SHS Class of 2021 — from Where Do Gators Go PDF (misc_199926.pdf)
# Class size: 155
SHS_2021 = [
    # (college, applied, accepted, enrolled)
    ("University of California, Santa Barbara", 57, 12, 1),
    ("UCLA", 54, 10, 5),
    ("UC Berkeley", 52, 4, 1),
    ("Santa Clara University", 50, 37, 5),
    ("University of Southern California", 47, 6, 1),
    ("Boston College", 40, 14, 2),
    ("UC Davis", 37, 15, 1),
    ("University of Colorado-Boulder", 36, 26, 2),
    ("UC Santa Cruz", 32, 20, 1),
    ("Villanova University", 32, 8, 2),
    ("University of Washington-Seattle", 31, 23, 6),
    ("Stanford University", 29, 5, 5),
    ("California Polytechnic State University (SLO)", 28, 14, 4),
    ("University of Michigan", 28, 11, 7),
    ("Duke University", 27, 7, 5),
    ("Loyola Marymount University", 27, 19, 3),
    ("Tulane University", 25, 9, 4),
    ("Tufts University", 24, 8, 5),
    ("University of San Diego", 24, 15, 3),
    ("University of Wisconsin-Madison", 24, 12, 2),
    ("San Diego State University", 21, 15, 3),
    ("Northeastern University", 20, 5, 1),
    ("Georgetown University", 19, 5, 4),
    ("Southern Methodist University", 19, 19, 4),
    ("Northwestern University", 18, 4, 2),
    ("Vanderbilt University", 18, 2, 1),
    ("New York University", 17, 7, 1),
    ("University of Notre Dame", 17, 6, 6),
    ("Gonzaga University", 16, 15, 1),
    ("Princeton University", 16, 4, 4),
    ("Boston University", 15, 6, 3),
    ("University of Pennsylvania", 15, 2, 1),
    ("University of Virginia", 15, 5, 2),
    ("Texas Christian University", 14, 12, 3),
    ("UC Riverside", 13, 9, 1),
    ("University of North Carolina-Chapel Hill", 13, 2, 2),
    ("Indiana University-Bloomington", 12, 11, 2),
    ("San Jose State University", 12, 12, 1),
    ("Columbia University", 10, 2, 1),
    ("Fordham University", 10, 7, 1),
    ("Yale University", 10, 1, 1),
]

SHS_2021_SMALL = [
    ("Amherst College", 1),
    ("Azusa Pacific University", 1),
    ("Barnard College", 2),
    ("California State University-Chico", 1),
    ("Canada College", 1),
    ("Carnegie Mellon University", 3),
    ("Claremont McKenna College", 3),
    ("Colby College", 2),
    ("Cornell University", 2),
    ("Emerson College", 1),
    ("Foothill College", 1),
    ("Hamilton College", 1),
    ("Harvard University", 1),
    ("Holy Cross College", 1),
    ("Johns Hopkins University", 1),
    ("Lehigh University", 1),
    ("McGill University", 1),
    ("Michigan State University", 1),
    ("Middlebury College", 1),
    ("NYU Shanghai", 1),
    ("Pepperdine University", 1),
    ("Pitzer College", 1),
    ("Pomona College", 2),
    ("Purdue University", 1),
    ("Swarthmore College", 1),
    ("Syracuse University", 1),
    ("The New School", 2),
    ("United States Naval Academy", 1),
    ("University of Chicago", 1),
    ("University of Illinois-Urbana-Champaign", 1),
    ("University of San Francisco", 2),
    ("University of South Carolina", 1),
    ("University of St. Andrews", 1),
]

# SHS Class of 2022 — from Where Do Gators Go PDF (misc_208682.pdf)
# Class size: 155
SHS_2022 = [
    # (college, applied, accepted, enrolled)
    ("UC Santa Barbara", 54, 8, 1),
    ("UCLA", 49, 5, 2),
    ("UC Berkeley", 46, 11, 6),
    ("UC Santa Cruz", 39, 17, 1),
    ("University of Southern California", 36, 4, 3),
    ("Santa Clara University", 34, 27, 7),
    ("Boston College", 31, 4, 1),
    ("California Polytechnic State University (SLO)", 31, 17, 9),
    ("University of Washington-Seattle", 31, 19, 1),
    ("University of Michigan", 30, 3, 1),
    ("Villanova University", 29, 12, 2),
    ("University of Colorado-Boulder", 26, 23, 1),
    ("Loyola Marymount University", 25, 15, 2),
    ("San Diego State University", 25, 12, 2),
    ("Boston University", 24, 9, 2),
    ("Northeastern University", 24, 13, 4),
    ("UC Riverside", 24, 13, 1),
    ("Stanford University", 23, 8, 8),
    ("University of San Diego", 23, 16, 3),
    ("Texas Christian University", 20, 14, 5),
    ("UC Merced", 20, 18, 1),
    ("New York University", 19, 5, 2),
    ("Tulane University", 17, 7, 6),
    ("University of Notre Dame", 17, 4, 4),
    ("Brown University", 16, 2, 2),
    ("Duke University", 16, 4, 3),
    ("Southern Methodist University", 16, 16, 3),
    ("Wake Forest University", 16, 3, 2),
    ("Gonzaga University", 15, 12, 1),
    ("Indiana University-Bloomington", 15, 14, 2),
    ("Georgetown University", 14, 3, 2),
    ("University of Virginia", 13, 5, 1),
    ("Cornell University", 12, 3, 2),
    ("University of Pennsylvania", 12, 1, 1),
    ("San Jose State University", 10, 9, 4),
    ("Syracuse University", 10, 5, 1),
]

SHS_2022_SMALL = [
    ("Middlebury College", 2),
    ("San Francisco State University", 1),
    ("Sonoma State University", 2),
    ("University of Chicago", 2),
    ("University of Illinois-Urbana-Champaign", 2),
    ("University of Vermont", 1),
    ("Washington University in St. Louis", 1),
    ("Case Western Reserve University", 1),
    ("Chapman University", 2),
    ("Dartmouth College", 2),
    ("Harvard University", 1),
    ("Princeton University", 2),
    ("University of St. Andrews", 2),
    ("Amherst College", 1),
    ("Arizona State University", 1),
    ("California State University-Fullerton", 1),
    ("Hamilton College", 2),
    ("Lewis & Clark College", 1),
    ("Pomona College", 1),
    ("Rensselaer Polytechnic Institute", 2),
    ("University of Richmond", 1),
    ("Bucknell University", 1),
    ("Claremont McKenna College", 1),
    ("Clemson University", 1),
    ("Colby College", 1),
    ("Bates College", 1),
    ("Brandeis University", 1),
    ("Georgia Institute of Technology", 1),
    ("Trinity University", 2),
    ("Auburn University", 1),
    ("Barnard College", 1),
    ("Belmont University", 1),
    ("Canada College", 2),
    ("Carleton College", 1),
    ("Lafayette College", 1),
    ("Pitzer College", 1),
    ("Rhode Island School of Design", 1),
    ("University of Alabama", 1),
    ("University of Minnesota", 1),
    ("College of the Holy Cross", 1),
    ("Foothill College", 1),
    ("Queen Mary University of London", 1),
    ("University of Puget Sound", 1),
]

# SHS Class of 2024 — from Where Do Gators Go PDF (Google Drive)
# Class size: 149
# Note: 2024 PDF has dual application figures (total/after-withdrawals).
# We use the after-withdrawals figure as the application count for consistency.
SHS_2024 = [
    # (college, applied, accepted, enrolled)
    ("UCLA", 55, 8, 4),
    ("UC Santa Barbara", 49, 22, 6),
    ("UC Berkeley", 45, 17, 7),
    ("California Polytechnic State University (SLO)", 43, 19, 1),
    ("UC San Diego", 38, 12, 0),
    ("University of Southern California", 41, 12, 6),
    ("Santa Clara University", 37, 25, 7),
    ("UC Davis", 30, 8, 0),
    ("Loyola Marymount University", 30, 18, 4),
    ("University of Colorado-Boulder", 26, 18, 1),
    ("University of San Diego", 23, 14, 2),
    ("Boston College", 29, 5, 3),
    ("San Diego State University", 26, 14, 0),
    ("UC Santa Cruz", 22, 13, 0),
    ("University of Michigan", 23, 1, 0),
    ("UC Irvine", 23, 5, 1),
    ("Texas Christian University", 23, 16, 4),
    ("University of Washington-Seattle", 19, 11, 1),
    ("Villanova University", 18, 5, 4),
    ("Northeastern University", 20, 9, 3),
    ("Chapman University", 19, 17, 4),
    ("Boston University", 17, 3, 1),
    ("Stanford University", 20, 3, 3),
    ("University of Miami", 13, 6, 0),
    ("Duke University", 17, 5, 5),
    ("Tulane University", 12, 6, 2),
    ("University of Notre Dame", 18, 1, 1),
    ("UC Riverside", 13, 10, 0),
    ("Georgetown University", 16, 3, 1),
    ("Southern Methodist University", 14, 14, 5),
    ("University of Oregon", 17, 16, 0),
    ("University of Virginia", 11, 3, 2),
    ("University of Wisconsin-Madison", 14, 7, 2),
    ("San Jose State University", 15, 14, 3),
    ("Wake Forest University", 13, 3, 1),
    ("Harvard University", 14, 3, 3),
    ("Indiana University-Bloomington", 12, 10, 0),
    ("Dartmouth College", 13, 4, 4),
    ("University of Arizona", 12, 12, 0),
    ("University of Denver", 11, 11, 0),
    ("UC Merced", 9, 9, 0),
    ("Brown University", 11, 3, 3),
    ("New York University", 9, 2, 1),
    ("Princeton University", 10, 2, 2),
    ("California State University-Long Beach", 8, 3, 0),
    ("Carnegie Mellon University", 9, 2, 1),
    ("University of Pennsylvania", 10, 1, 1),
    ("Vanderbilt University", 8, 2, 2),
]

SHS_2024_SMALL = [
    ("American University", 2),
    ("Bucknell University", 1),
    ("California Institute of Technology", 1),
    ("California Polytechnic State University (Pomona)", 1),
    ("California State University-East Bay", 1),
    ("California State University-Sacramento", 1),
    ("California State University-San Marcos", 1),
    ("Case Western Reserve University", 1),
    ("Colorado College", 3),
    ("Colorado School of Mines", 1),
    ("Columbia University", 1),
    ("Cornell University", 1),
    ("Denison University", 1),
    ("Duquesne University", 1),
    ("Emory University", 2),
    ("Haverford College", 1),
    ("Holy Cross College", 1),
    ("Johns Hopkins University", 1),
    ("Louisiana State University", 1),
    ("Macalester College", 4),
    ("Massachusetts Institute of Technology", 2),
    ("Northwestern University", 1),
    ("Parsons School of Design", 1),
    ("Pitzer College", 1),
    ("Pomona College", 1),
    ("Purdue University", 2),
    ("Rice University", 1),
    ("Sarah Lawrence College", 1),
    ("Scripps College", 1),
    ("Syracuse University", 1),
    ("Tufts University", 1),
    ("University of Illinois-Urbana-Champaign", 1),
    ("University of Oxford", 1),
    ("University of St. Andrews", 1),
    ("University of Texas at Austin", 1),
    ("University of Utah", 1),
    ("William & Mary", 1),
    ("Yale University", 1),
]


def main():
    db = sqlite3.connect(DB_PATH)
    total = 0

    years_data = [
        (2021, SHS_2021, SHS_2021_SMALL,
         "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_199926.pdf"),
        (2022, SHS_2022, SHS_2022_SMALL,
         "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_208682.pdf"),
        (2024, SHS_2024, SHS_2024_SMALL,
         "https://drive.google.com/file/d/1TVtxiNGaZsTVF7nYuJPXhP7clrc_6n-j/view"),
    ]

    for grad_year, main_data, small_data, source_url in years_data:
        year_count = 0

        for college, applied, accepted, enrolled in main_data:
            cn = normalize_college(college)
            for metric, count in [("applied", applied), ("accepted", accepted), ("enrolled", enrolled)]:
                if count > 0:
                    db.execute(
                        """INSERT OR REPLACE INTO placements
                        (school_id, grad_year, college, college_normalized, metric, count,
                         source, source_url, confidence)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        ("sacred-heart-atherton", grad_year, college, cn, metric, count,
                         "school_profile_pdf", source_url, "L1"),
                    )
                    year_count += 1

        for college, enrolled in small_data:
            cn = normalize_college(college)
            db.execute(
                """INSERT OR REPLACE INTO placements
                (school_id, grad_year, college, college_normalized, metric, count,
                 source, source_url, confidence, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                ("sacred-heart-atherton", grad_year, college, cn, "enrolled", enrolled,
                 "school_profile_pdf", source_url, "L1", "Fewer than 10 applications"),
            )
            year_count += 1

        total += year_count
        print(f"  Class of {grad_year}: {year_count} records")

    # Update school profile metadata
    profiles = [
        ("2020-21", 155,
         "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_199926.pdf"),
        ("2021-22", 155,
         "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_208682.pdf"),
        ("2023-24", 149,
         "https://drive.google.com/file/d/1TVtxiNGaZsTVF7nYuJPXhP7clrc_6n-j/view"),
    ]

    for academic_year, class_size, source_url in profiles:
        db.execute(
            """INSERT OR REPLACE INTO school_profiles
            (school_id, academic_year, grad_class_size, source_url)
            VALUES (?, ?, ?, ?)""",
            ("sacred-heart-atherton", academic_year, class_size, source_url),
        )

    db.commit()
    print(f"\nInserted {total} SHS placement records (2021 + 2022 + 2024)")
    print(f"School profiles: 3 years added")

    db.close()


if __name__ == "__main__":
    main()
