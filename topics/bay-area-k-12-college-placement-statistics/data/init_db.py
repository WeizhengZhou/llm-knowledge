#!/usr/bin/env python3
"""Initialize the college placement SQLite database and seed school records."""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "college_placement.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

SCHOOLS = [
    ("sacred-heart-atherton", "Sacred Heart Preparatory", "SHP", "Atherton", "CA", "private", "K-12", "https://www.shschools.org", "053578"),
    ("harker", "The Harker School", "Harker", "San Jose", "CA", "private", "K-12", "https://www.harker.org", "053516"),
    ("menlo", "Menlo School", "Menlo", "Atherton", "CA", "private", "6-12", "https://www.menloschool.org", "052306"),
    ("castilleja", "Castilleja School", "Castilleja", "Palo Alto", "CA", "private", "6-12", "https://www.castilleja.org", "050490"),
    ("nueva", "The Nueva School", "Nueva", "San Mateo", "CA", "private", "PK-12", "https://www.nuevaschool.org", "054857"),
    ("crystal-springs", "Crystal Springs Uplands School", "Crystal", "Hillsborough", "CA", "private", "6-12", "https://www.crystal.org", "050690"),
    ("pinewood", "Pinewood School", "Pinewood", "Los Altos Hills", "CA", "private", "K-12", "https://www.pinewood.edu", "051512"),
    ("woodside-priory", "Woodside Priory School", "Priory", "Portola Valley", "CA", "private", "6-12", "https://www.prioryca.org", "053350"),
]

# Known data sources to register for tracking
SOURCES = [
    # SHS sources
    ("sacred-heart-atherton", "google_doc", "https://docs.google.com/document/d/1XLvwQAaRL0W3tf8r9hn8wxZ01Rj_xExTaIrwNjf9qMk/edit", "2022-2024"),
    ("sacred-heart-atherton", "school_profile_pdf", "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_224258.pdf", "2024-25"),
    ("sacred-heart-atherton", "school_profile_pdf", "https://bbk12e1-cdn.myschoolcdn.com/ftpimages/783/misc/misc_230695.pdf", "2025-26"),
    ("sacred-heart-atherton", "athlete_page", "https://www.shschools.org/z-2021-hpr-news-detail?pk=1401618", "2025"),
    ("sacred-heart-atherton", "athlete_page", "https://www.shschools.org/z-2021-hpr-news-detail?pk=1337581", "2024"),
    ("sacred-heart-atherton", "athlete_page", "https://www.shschools.org/z-2021-hpr-news-detail?pk=1287308", "2023"),
    ("sacred-heart-atherton", "athlete_page", "https://www.shschools.org/z-2021-hpr-news-detail?pk=1237527", "2022"),
    ("sacred-heart-atherton", "athlete_page", "https://www.shschools.org/copy-of-news-detail?pk=1177379&fromId=203251", "2021"),
    # Harker
    ("harker", "school_website", "https://www.harker.org/upper-school/support-services/college-counseling/college-acceptances", "2023-2025"),
    ("harker", "school_profile_pdf", "https://www.harker.org/uploaded/assets/documents/pdfs/counseling/ADM_US_Harker_Profile_F_2425.pdf", "2024-25"),
    # Menlo
    ("menlo", "school_profile_pdf", "https://www.menloschool.org/live/files/4018-menlo-school-profile-2025-2026", "2025-26"),
    ("menlo", "school_profile_pdf", "https://www.menloschool.org/live/files/3729-menlo-school-profile-2023-2024", "2023-24"),
    ("menlo", "school_profile_pdf", "https://www.menloschool.org/live/files/3625-menlo-school-profile-2022-2023", "2022-23"),
    # Castilleja
    ("castilleja", "school_profile_pdf", "https://www.castilleja.org/uploaded/College_Counseling/Documents/CastillejaProfile.pdf", "2025-26"),
    # Nueva
    ("nueva", "school_profile_pdf", "https://resources.finalsite.net/images/v1766430328/nuevaschoolorg/tesjhsaqpweriklu4vrr/NuevaProfile2024-25FINAL.pdf", "2024-25"),
    ("nueva", "school_profile_pdf", "https://resources.finalsite.net/images/v1702412698/nuevaschoolorg/xaapknab9fyt6adrrl8n/23-24CollegeProfile.pdf", "2023-24"),
    # Crystal Springs
    ("crystal-springs", "school_website", "https://www.crystal.org/resources/academic-support/college-counseling", "2022-2025"),
    # Pinewood
    ("pinewood", "school_profile_pdf", "https://www.pinewood.edu/uploaded/New_Website_Page_Elements/Admissions/Updated_Materials/PWSchoolProfile_24-25.pdf", "2024-25"),
    ("pinewood", "school_profile_pdf", "https://www.pinewood.edu/uploaded/New_Website_Page_Elements/Admissions/Updated_Materials/PWSchoolProfile_25-26.pdf", "2025-26"),
    # UC InfoCenter (covers all schools)
    (None, "uc_infocenter", "https://www.universityofcalifornia.edu/about-us/information-center/admissions-source-school", "1994-2025"),
]


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA_PATH.read_text())

    # Seed schools
    db.executemany(
        """INSERT OR IGNORE INTO schools
        (school_id, name, short_name, city, state, type, grades, website, ceeb_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        SCHOOLS,
    )

    # Register known sources
    for school_id, source_type, url, years in SOURCES:
        db.execute(
            """INSERT OR IGNORE INTO sources
            (school_id, source_type, url, years_covered)
            VALUES (?, ?, ?, ?)""",
            (school_id, source_type, url, years),
        )

    db.commit()

    # Print summary
    print(f"Database: {DB_PATH}")
    print(f"Schools: {db.execute('SELECT COUNT(*) FROM schools').fetchone()[0]}")
    print(f"Sources registered: {db.execute('SELECT COUNT(*) FROM sources').fetchone()[0]}")
    print(f"\nPending sources:")
    for row in db.execute(
        "SELECT s.school_id, s.source_type, s.years_covered FROM sources s WHERE s.status = 'pending' ORDER BY s.school_id"
    ):
        print(f"  {row[0] or 'ALL'} | {row[1]} | {row[2]}")

    db.close()


if __name__ == "__main__":
    init_db()
