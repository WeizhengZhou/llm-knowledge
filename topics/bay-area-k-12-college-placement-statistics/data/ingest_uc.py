#!/usr/bin/env python3
"""
Ingest UC InfoCenter admissions-by-source-school data into SQLite.

The UC Information Center publishes applicant/admit/enrollee counts by high school,
for each UC campus, with ethnicity breakdowns.

Data source: https://www.universityofcalifornia.edu/about-us/information-center/admissions-source-school
GitHub CSV mirror: https://github.com/metatab-packages/universityofcalifornia.edu-admissions

Usage:
    # Download the CSV first, then:
    python ingest_uc.py <csv_file>

    # Or to fetch and ingest specific schools from the UC interactive tool:
    python ingest_uc.py --fetch-schools sacred-heart-atherton harker menlo castilleja nueva crystal-springs pinewood woodside-priory
"""

import csv
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "college_placement.db"

# Map our school_ids to names as they appear in UC data
# These need to be verified against the actual UC dataset
SCHOOL_NAME_MAP = {
    "sacred-heart-atherton": ["Sacred Heart Preparatory", "Sacred Heart Prep", "Sacred Heart Schools"],
    "harker": ["The Harker School", "Harker School"],
    "menlo": ["Menlo School"],
    "castilleja": ["Castilleja School"],
    "nueva": ["Nueva School", "The Nueva School"],
    "crystal-springs": ["Crystal Springs Uplands", "Crystal Springs Uplands School"],
    "pinewood": ["Pinewood School"],
    "woodside-priory": ["Woodside Priory", "Woodside Priory School"],
}

UC_CAMPUS_NORMALIZE = {
    "Berkeley": "berkeley",
    "Davis": "davis",
    "Irvine": "irvine",
    "Los Angeles": "los-angeles",
    "Merced": "merced",
    "Riverside": "riverside",
    "San Diego": "san-diego",
    "Santa Barbara": "santa-barbara",
    "Santa Cruz": "santa-cruz",
}


def find_school_id(school_name: str) -> str | None:
    """Match a UC data school name to our school_id."""
    name_lower = school_name.lower().strip()
    for school_id, names in SCHOOL_NAME_MAP.items():
        for n in names:
            if n.lower() in name_lower or name_lower in n.lower():
                return school_id
    return None


def ingest_csv(csv_path: Path):
    """Ingest a UC admissions CSV file."""
    db = sqlite3.connect(DB_PATH)

    inserted = 0
    skipped = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            school_name = row.get("School Name", row.get("school_name", ""))
            school_id = find_school_id(school_name)
            if not school_id:
                skipped += 1
                continue

            campus = row.get("Campus", row.get("campus", ""))
            campus_norm = UC_CAMPUS_NORMALIZE.get(campus, campus.lower().replace(" ", "-"))

            year = int(row.get("Year", row.get("year", 0)))
            ethnicity = row.get("Ethnicity", row.get("ethnicity", "All"))

            applicants = _int_or_none(row.get("Applicants", row.get("applicants")))
            admits = _int_or_none(row.get("Admits", row.get("admits")))
            enrollees = _int_or_none(row.get("Enrollees", row.get("enrollees")))
            mean_gpa = _float_or_none(row.get("Mean GPA", row.get("mean_gpa")))

            try:
                db.execute(
                    """INSERT OR REPLACE INTO uc_admissions
                    (school_id, school_name_uc, year, uc_campus, ethnicity,
                     applicants, admits, enrollees, mean_gpa, source_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (school_id, school_name, year, campus_norm, ethnicity,
                     applicants, admits, enrollees, mean_gpa,
                     "https://www.universityofcalifornia.edu/about-us/information-center/admissions-source-school"),
                )
                inserted += 1
            except sqlite3.Error as e:
                print(f"Error inserting {school_name} {year} {campus}: {e}")

    db.commit()
    print(f"UC InfoCenter ingest: {inserted} rows inserted, {skipped} rows skipped (non-target schools)")
    db.close()


def ingest_manual_records(records: list[dict]):
    """Insert manually extracted UC data records.

    records: list of dicts with keys matching uc_admissions columns.
    Use this when manually extracting from the UC Tableau tool.
    """
    db = sqlite3.connect(DB_PATH)
    inserted = 0
    for rec in records:
        try:
            db.execute(
                """INSERT OR REPLACE INTO uc_admissions
                (school_id, school_name_uc, year, uc_campus, ethnicity,
                 applicants, admits, enrollees, mean_gpa, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (rec["school_id"], rec.get("school_name_uc"),
                 rec["year"], rec["uc_campus"], rec.get("ethnicity", "All"),
                 rec.get("applicants"), rec.get("admits"), rec.get("enrollees"),
                 rec.get("mean_gpa"),
                 rec.get("source_url", "https://www.universityofcalifornia.edu/about-us/information-center/admissions-source-school")),
            )
            inserted += 1
        except sqlite3.Error as e:
            print(f"Error: {e}")
    db.commit()
    print(f"Inserted {inserted} UC admissions records")
    db.close()
    return inserted


def _int_or_none(val):
    if val is None or val == "" or val == "*":
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def _float_or_none(val):
    if val is None or val == "" or val == "*":
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def ingest_collegeacceptance_json(json_path: Path):
    """Ingest UC admissions data from collegeacceptance.info JSON format.

    The JSON file (admissions_ca_private.json) contains an array of school objects:
    {
        "school_id": "53142",
        "school_name": "HARKER SCHOOL",
        "school_type": "CA Private",
        "city": "San Jose",
        "county": "Santa Clara",
        "years": {
            "2024": {
                "app": 187, "adm": 132, "enr": 29, "admit_rate": 0.7059,
                "by_ethnicity": {
                    "Asian": {"app": 120, "adm": 81, "enr": 17, ...}, ...
                },
                "by_campus": {}
            }, ...
        }
    }

    This data is Universitywide (all UC campuses combined). Per-campus breakdowns
    are not available in this JSON; they would require scraping the UC Tableau tool.

    Source: https://collegeacceptance.info/data/admissions_ca_private.json
    Original data: UC Information Center, admissions by source school
    """
    import json

    # Map school names to our school_ids
    NAME_TO_ID = {
        "SACRED HEART PREPARATORY SCH": "sacred-heart-atherton",
        "HARKER SCHOOL": "harker",
        "MENLO SCHOOL": "menlo",
        "CASTILLEJA SCHOOL": "castilleja",
        "THE NUEVA SCHOOL": "nueva",
        "CRYSTAL SPRINGS UPLANDS SCH": "crystal-springs",
        "PINEWOOD SCHOOL": "pinewood",
        "WOODSIDE PRIORY SCHOOL": "woodside-priory",
    }

    ETHNICITY_MAP = {
        "African American": "African American",
        "American Indian": "American Indian",
        "Hispanic/ Latinx": "Hispanic/Latinx",
        "Pacific Islander": "Pacific Islander",
        "Asian": "Asian",
        "White": "White",
        "Domestic Unknown": "Domestic Unknown",
        "Int'l": "International",
    }

    SOURCE_URL = "https://www.universityofcalifornia.edu/about-us/information-center/admissions-source-school"

    with open(json_path, encoding="utf-8") as f:
        schools = json.load(f)

    db = sqlite3.connect(DB_PATH)
    inserted = 0
    skipped = 0

    for school in schools:
        school_name = school["school_name"]
        school_id = NAME_TO_ID.get(school_name)
        if not school_id:
            skipped += 1
            continue

        print(f"  Processing {school_name} -> {school_id}")

        for year_str, ydata in school.get("years", {}).items():
            year = int(year_str)
            app = ydata.get("app")
            adm = ydata.get("adm")
            enr = ydata.get("enr")

            # Skip years with no data at all
            if app is None and adm is None and enr is None:
                continue

            # Insert "All" ethnicity row (universitywide)
            try:
                db.execute(
                    """INSERT OR REPLACE INTO uc_admissions
                    (school_id, school_name_uc, year, uc_campus, ethnicity,
                     applicants, admits, enrollees, mean_gpa, source_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (school_id, school_name, year, "universitywide", "All",
                     app, adm, enr, None, SOURCE_URL),
                )
                inserted += 1
            except sqlite3.Error as e:
                print(f"    Error: {e}")

            # Insert ethnicity breakdown rows
            for eth_key, eth_label in ETHNICITY_MAP.items():
                eth_data = ydata.get("by_ethnicity", {}).get(eth_key)
                if eth_data is None:
                    continue
                e_app = eth_data.get("app")
                e_adm = eth_data.get("adm")
                e_enr = eth_data.get("enr")
                if e_app is None and e_adm is None and e_enr is None:
                    continue
                try:
                    db.execute(
                        """INSERT OR REPLACE INTO uc_admissions
                        (school_id, school_name_uc, year, uc_campus, ethnicity,
                         applicants, admits, enrollees, mean_gpa, source_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (school_id, school_name, year, "universitywide", eth_label,
                         e_app, e_adm, e_enr, None, SOURCE_URL),
                    )
                    inserted += 1
                except sqlite3.Error as e:
                    print(f"    Error: {e}")

    db.commit()
    db.close()
    print(f"\nCollegeacceptance.info ingest: {inserted} rows inserted, {skipped} schools skipped (non-target)")
    return inserted


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_uc.py <csv_file_or_json_file>")
        print("  CSV: Download from https://github.com/metatab-packages/universityofcalifornia.edu-admissions")
        print("  JSON: Download from https://collegeacceptance.info/data/admissions_ca_private.json")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    if path.suffix == ".json":
        ingest_collegeacceptance_json(path)
    else:
        ingest_csv(path)
