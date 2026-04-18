#!/usr/bin/env python3
"""
Query the college placement database.

Usage:
    python query.py schools                          # List all schools
    python query.py sources                          # Show source ingestion status
    python query.py placements <school_id>           # All placements for a school
    python query.py ivy <school_id>                  # Ivy+ placements with athlete breakdown
    python query.py compare <college>                # Compare schools for a specific college
    python query.py athletes <school_id> [year]      # Athlete commits
    python query.py uc <school_id>                   # UC admissions data
    python query.py summary                          # Overall data summary
"""

import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent / "college_placement.db"

IVY_PLUS = [
    "harvard", "yale", "princeton", "columbia", "upenn", "brown",
    "dartmouth", "cornell", "stanford", "mit", "caltech",
    "duke", "uchicago", "northwestern", "jhu",
]


def get_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def cmd_schools():
    db = get_db()
    for row in db.execute("SELECT school_id, name, short_name, city, grades FROM schools ORDER BY name"):
        print(f"  {row['school_id']:25s} {row['name']:35s} {row['city']:15s} {row['grades']}")


def cmd_sources():
    db = get_db()
    print(f"\n{'School':25s} {'Type':20s} {'Years':12s} {'Status':10s}")
    print("-" * 70)
    for row in db.execute(
        """SELECT COALESCE(school_id, 'ALL') as sid, source_type, years_covered, status
        FROM sources ORDER BY school_id, source_type"""
    ):
        print(f"  {row['sid']:25s} {row['source_type']:20s} {row['years_covered']:12s} {row['status']:10s}")


def cmd_placements(school_id: str):
    db = get_db()
    print(f"\nPlacements for {school_id}:")
    for row in db.execute(
        """SELECT grad_year, college, count, metric, source
        FROM placements WHERE school_id = ?
        ORDER BY grad_year DESC, count DESC""",
        (school_id,),
    ):
        print(f"  {row['grad_year']} | {row['college']:40s} | {row['count']:3d} {row['metric']:8s} | {row['source']}")


def cmd_ivy(school_id: str):
    db = get_db()
    print(f"\nIvy+ placements for {school_id} (with athlete breakdown):")
    print(f"\n{'Year':6s} {'College':25s} {'Total':6s} {'Athletes':9s} {'Non-Ath':8s}")
    print("-" * 58)

    rows = db.execute(
        """SELECT p.grad_year, p.college, p.count as total,
                  COALESCE(a.ath, 0) as athletes
           FROM placements p
           LEFT JOIN (
               SELECT school_id, grad_year, college_normalized, COUNT(*) as ath
               FROM athlete_commits GROUP BY school_id, grad_year, college_normalized
           ) a ON p.school_id = a.school_id
               AND p.grad_year = a.grad_year
               AND p.college_normalized = a.college_normalized
           WHERE p.school_id = ? AND p.college_normalized IN ({})
               AND p.metric = 'enrolled'
           ORDER BY p.grad_year DESC, p.count DESC""".format(
            ",".join(f"'{c}'" for c in IVY_PLUS)
        ),
        (school_id,),
    )

    yearly_totals = {}
    for row in rows:
        non_ath = row["total"] - row["athletes"]
        print(f"  {row['grad_year']:<6d} {row['college']:25s} {row['total']:5d}  {row['athletes']:8d}  {non_ath:7d}")
        if row["grad_year"] not in yearly_totals:
            yearly_totals[row["grad_year"]] = {"total": 0, "athletes": 0}
        yearly_totals[row["grad_year"]]["total"] += row["total"]
        yearly_totals[row["grad_year"]]["athletes"] += row["athletes"]

    if yearly_totals:
        print("\nYearly totals:")
        for year in sorted(yearly_totals.keys(), reverse=True):
            t = yearly_totals[year]
            print(f"  {year}: {t['total']} total, {t['athletes']} athletes, {t['total'] - t['athletes']} non-athlete")


def cmd_compare(college: str):
    db = get_db()
    college_norm = college.lower().replace(" ", "-").replace("university", "").strip("-")
    print(f"\nSchool comparison for '{college}' (normalized: {college_norm}):")

    rows = db.execute(
        """SELECT s.short_name, p.grad_year, p.count, p.metric
        FROM placements p JOIN schools s ON p.school_id = s.school_id
        WHERE p.college_normalized LIKE ?
        ORDER BY s.short_name, p.grad_year""",
        (f"%{college_norm}%",),
    )
    for row in rows:
        print(f"  {row['short_name']:10s} {row['grad_year']} | {row['count']:3d} {row['metric']}")


def cmd_athletes(school_id: str, year: int = None):
    db = get_db()
    query = "SELECT * FROM athlete_commits WHERE school_id = ?"
    params = [school_id]
    if year:
        query += " AND grad_year = ?"
        params.append(year)
    query += " ORDER BY grad_year DESC, sport, student_name"

    print(f"\nAthlete commits for {school_id}:")
    current_year = None
    for row in db.execute(query, params):
        if row["grad_year"] != current_year:
            current_year = row["grad_year"]
            print(f"\n  Class of {current_year}:")
        print(f"    {row['student_name'] or 'N/A':25s} {row['sport']:20s} → {row['college']}")


def cmd_uc(school_id: str):
    db = get_db()
    print(f"\nUC admissions for {school_id}:")
    for row in db.execute(
        """SELECT year, uc_campus, applicants, admits, enrollees, mean_gpa
        FROM uc_admissions WHERE school_id = ? AND ethnicity = 'All'
        ORDER BY year DESC, uc_campus""",
        (school_id,),
    ):
        admit_rate = f"{100*row['admits']/row['applicants']:.0f}%" if row["applicants"] and row["admits"] else "n/a"
        gpa_str = f"{row['mean_gpa']:.2f}" if row['mean_gpa'] else "  - "
        print(f"  {row['year']} {row['uc_campus']:15s} App:{row['applicants'] or 0:3d} Adm:{row['admits'] or 0:3d} ({admit_rate:>4s}) Enr:{row['enrollees'] or 0:3d} GPA:{gpa_str}")


def cmd_summary():
    db = get_db()
    print("\n=== Database Summary ===\n")
    for table in ["schools", "placements", "uc_admissions", "school_profiles", "athlete_commits", "sources"]:
        count = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:20s}: {count:,d} rows")

    print("\n  Sources by status:")
    for row in db.execute("SELECT status, COUNT(*) as n FROM sources GROUP BY status"):
        print(f"    {row['status']:10s}: {row['n']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "schools":
        cmd_schools()
    elif cmd == "sources":
        cmd_sources()
    elif cmd == "placements" and len(sys.argv) >= 3:
        cmd_placements(sys.argv[2])
    elif cmd == "ivy" and len(sys.argv) >= 3:
        cmd_ivy(sys.argv[2])
    elif cmd == "compare" and len(sys.argv) >= 3:
        cmd_compare(sys.argv[2])
    elif cmd == "athletes" and len(sys.argv) >= 3:
        year = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        cmd_athletes(sys.argv[2], year)
    elif cmd == "uc" and len(sys.argv) >= 3:
        cmd_uc(sys.argv[2])
    elif cmd == "summary":
        cmd_summary()
    else:
        print(__doc__)
