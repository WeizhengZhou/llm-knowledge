#!/usr/bin/env python3
"""
Cross-join student profiles with school placement data.

Connects individual student outcomes with school-level statistics to enable:
1. Profile → School matching (identify which school a student likely attended)
2. Outcome calibration (compare individual results against school baselines)
3. Segment analysis (acceptance rates by profile type within school context)

Usage:
    python cross_join.py summary         # Overall cross-database statistics
    python cross_join.py match-schools   # Attempt to match profiles to schools
    python cross_join.py college-rates   # Per-college acceptance rates by demographics
    python cross_join.py lexi-comps      # Find comparable profiles for Lexi
"""

import json
import sqlite3
import sys
from pathlib import Path

PROFILE_DB = Path(__file__).parent / "profiles.db"
SCHOOL_DB = Path(__file__).parent.parent / "college_placement.db"


def get_dbs():
    pdb = sqlite3.connect(PROFILE_DB)
    pdb.row_factory = sqlite3.Row
    sdb = sqlite3.connect(SCHOOL_DB)
    sdb.row_factory = sqlite3.Row
    return pdb, sdb


def cmd_summary():
    pdb, sdb = get_dbs()

    print("=" * 70)
    print("CROSS-DATABASE SUMMARY")
    print("=" * 70)

    # Profile DB stats
    p_total = pdb.execute("SELECT COUNT(*) FROM student_profiles").fetchone()[0]
    p_results = pdb.execute("SELECT COUNT(*) FROM application_results").fetchone()[0]
    p_with = pdb.execute("SELECT COUNT(*) FROM student_profiles WHERE id IN (SELECT DISTINCT profile_id FROM application_results)").fetchone()[0]

    # School DB stats
    s_schools = sdb.execute("SELECT COUNT(*) FROM schools").fetchone()[0]
    s_placements = sdb.execute("SELECT COUNT(*) FROM placements").fetchone()[0]
    s_athletes = sdb.execute("SELECT COUNT(*) FROM athlete_commits").fetchone()[0]

    print(f"\nProfile DB: {p_total} profiles, {p_with} with results, {p_results} total application results")
    print(f"School DB: {s_schools} schools, {s_placements} placements, {s_athletes} athlete commits")

    # Overlap: colleges that appear in both databases
    profile_colleges = set(r[0] for r in pdb.execute("SELECT DISTINCT college_normalized FROM application_results"))
    school_colleges = set(r[0] for r in sdb.execute("SELECT DISTINCT college_normalized FROM placements"))
    overlap = profile_colleges & school_colleges

    print(f"\nCollege overlap: {len(overlap)} colleges in both DBs (out of {len(profile_colleges)} in profiles, {len(school_colleges)} in schools)")

    # Most common overlapping colleges
    print(f"\nTop overlapping colleges (profile apps → school placements):")
    for college in sorted(overlap):
        p_count = pdb.execute("SELECT COUNT(*) FROM application_results WHERE college_normalized=?", (college,)).fetchone()[0]
        s_count = sdb.execute("SELECT SUM(count) FROM placements WHERE college_normalized=? AND metric='enrolled'", (college,)).fetchone()[0] or 0
        if p_count >= 3:
            print(f"  {college:30s}  profiles: {p_count:3d} apps  |  schools: {s_count:4d} enrolled")


def cmd_college_rates():
    pdb, _ = get_dbs()

    print("=" * 70)
    print("ACCEPTANCE RATES BY COLLEGE AND DEMOGRAPHICS")
    print("=" * 70)

    # Top 15 colleges by application volume
    colleges = pdb.execute("""
        SELECT college_normalized, COUNT(*) as n
        FROM application_results
        GROUP BY college_normalized
        HAVING n >= 3
        ORDER BY n DESC LIMIT 20
    """).fetchall()

    for row in colleges:
        college = row["college_normalized"]
        print(f"\n{college}")
        print("-" * 50)

        # Overall
        overall = pdb.execute("""
            SELECT COUNT(*) as apps,
                   SUM(CASE WHEN result='accepted' THEN 1 ELSE 0 END) as acc,
                   SUM(CASE WHEN result='rejected' THEN 1 ELSE 0 END) as rej
            FROM application_results WHERE college_normalized=?
        """, (college,)).fetchone()
        rate = f"{100*overall['acc']/overall['apps']:.0f}%" if overall["apps"] else "n/a"
        print(f"  Overall: {overall['acc']}/{overall['apps']} ({rate})")

        # By ethnicity
        for eth in ["asian", "white", "black", "hispanic"]:
            eth_row = pdb.execute("""
                SELECT COUNT(*) as apps,
                       SUM(CASE WHEN ar.result='accepted' THEN 1 ELSE 0 END) as acc
                FROM application_results ar
                JOIN student_profiles sp ON ar.profile_id = sp.id
                WHERE ar.college_normalized=? AND sp.ethnicity=?
            """, (college, eth)).fetchone()
            if eth_row["apps"] > 0:
                e_rate = f"{100*eth_row['acc']/eth_row['apps']:.0f}%"
                print(f"  {eth:12s}: {eth_row['acc']}/{eth_row['apps']} ({e_rate})")

        # By SAT range
        for sat_min, sat_max, label in [(1550, 1600, "1550+"), (1500, 1549, "1500-1549"), (1400, 1499, "1400-1499")]:
            sat_row = pdb.execute("""
                SELECT COUNT(*) as apps,
                       SUM(CASE WHEN ar.result='accepted' THEN 1 ELSE 0 END) as acc
                FROM application_results ar
                JOIN student_profiles sp ON ar.profile_id = sp.id
                WHERE ar.college_normalized=? AND sp.sat BETWEEN ? AND ?
            """, (college, sat_min, sat_max)).fetchone()
            if sat_row["apps"] > 0:
                s_rate = f"{100*sat_row['acc']/sat_row['apps']:.0f}%"
                print(f"  SAT {label:10s}: {sat_row['acc']}/{sat_row['apps']} ({s_rate})")


def cmd_lexi_comps():
    """Find profiles comparable to Lexi's projected profile."""
    pdb, sdb = get_dbs()

    print("=" * 70)
    print("COMPARABLE PROFILES FOR LEXI")
    print("=" * 70)
    print()
    print("Lexi's projected profile (age 7, extrapolated to 18):")
    print("  Asian female, Bay Area private school, non-athlete")
    print("  Math-strong (projected AIME qualifier), strong writer")
    print("  SAT projected: 1550+, GPA: 3.9+ UW")
    print("  Duke MS-only legacy (not undergrad)")
    print()

    # Find Asian females with 1500+ SAT
    comps = pdb.execute("""
        SELECT sp.id, sp.source_id, sp.gender, sp.ethnicity, sp.sat, sp.gpa_uw, sp.gpa_w,
               sp.school_type, sp.state, sp.awards_json, sp.ecs_json,
               sp.source_url
        FROM student_profiles sp
        WHERE sp.ethnicity = 'asian'
        AND sp.gender = 'female'
        AND sp.id IN (SELECT DISTINCT profile_id FROM application_results)
        ORDER BY sp.sat DESC NULLS LAST
    """).fetchall()

    print(f"Found {len(comps)} Asian female profiles with results:")
    print()

    for comp in comps:
        print(f"  Profile {comp['source_id']} (SAT: {comp['sat'] or 'N/A'}, GPA: {comp['gpa_uw'] or 'N/A'} UW)")
        print(f"  School: {comp['school_type'] or 'unknown'}, State: {comp['state'] or 'N/A'}")

        # Show their awards (look for math competition signals)
        awards = json.loads(comp["awards_json"]) if comp["awards_json"] else []
        math_awards = [a for a in awards if any(w in str(a).lower() for w in ["aime", "amc", "math", "olympiad", "putnam"])]
        if math_awards:
            print(f"  Math awards: {[a.get('name', a) if isinstance(a, dict) else a for a in math_awards[:3]]}")

        # Show results
        results = pdb.execute("""
            SELECT college, result, round FROM application_results
            WHERE profile_id = ? ORDER BY
            CASE result WHEN 'accepted' THEN 0 WHEN 'waitlisted' THEN 1 ELSE 2 END
        """, (comp["id"],)).fetchall()

        accepted = [r for r in results if r["result"] == "accepted"]
        rejected = [r for r in results if r["result"] == "rejected"]
        print(f"  Accepted ({len(accepted)}): {', '.join(r['college'][:20] for r in accepted[:5])}")
        print(f"  Rejected ({len(rejected)}): {', '.join(r['college'][:20] for r in rejected[:5])}")
        print(f"  URL: {comp['source_url'] or 'N/A'}")
        print()

    # Acceptance rates for Asian females at target schools
    print("\nAcceptance rates for Asian females at Lexi's target schools:")
    print(f"{'College':25s} {'Apps':>5} {'Acc':>5} {'Rate':>7}")
    print("-" * 45)
    targets = ["stanford", "duke", "mit", "harvard", "princeton", "dartmouth", "brown", "cornell", "uchicago", "northwestern"]
    for college in targets:
        row = pdb.execute("""
            SELECT COUNT(*) as apps,
                   SUM(CASE WHEN ar.result='accepted' THEN 1 ELSE 0 END) as acc
            FROM application_results ar
            JOIN student_profiles sp ON ar.profile_id = sp.id
            WHERE ar.college_normalized=? AND sp.ethnicity='asian' AND sp.gender='female'
        """, (college,)).fetchone()
        if row["apps"] > 0:
            rate = f"{100*row['acc']/row['apps']:.0f}%"
            print(f"  {college:23s} {row['apps']:5d} {row['acc']:5d} {rate:>7}")
        else:
            print(f"  {college:23s}     0     -      -")


def cmd_match_schools():
    """Attempt to match profiles to known schools based on hints."""
    pdb, sdb = get_dbs()

    print("=" * 70)
    print("SCHOOL MATCHING ATTEMPTS")
    print("=" * 70)

    # Profiles with school hints
    hints = pdb.execute("""
        SELECT id, source_id, school_name_hint, school_type, state, region
        FROM student_profiles
        WHERE school_name_hint IS NOT NULL AND school_name_hint != ''
    """).fetchall()

    print(f"\nProfiles with school name hints: {len(hints)}")
    for h in hints:
        print(f"  {h['source_id']:15s} → {h['school_name_hint']} ({h['school_type'] or '?'}, {h['state'] or '?'})")

    # Profiles identifiable as Bay Area
    ba = pdb.execute("""
        SELECT id, source_id, school_type, state, region, sat
        FROM student_profiles
        WHERE (state = 'CA' AND (school_type = 'private' OR region = 'bay-area'))
        OR region = 'bay-area'
    """).fetchall()

    print(f"\nBay Area private school profiles: {len(ba)}")
    for b in ba:
        print(f"  {b['source_id']:15s} SAT:{b['sat'] or 'N/A'} type:{b['school_type'] or '?'}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "summary":
        cmd_summary()
    elif cmd == "college-rates":
        cmd_college_rates()
    elif cmd == "lexi-comps":
        cmd_lexi_comps()
    elif cmd == "match-schools":
        cmd_match_schools()
    else:
        print(f"Unknown command: {cmd}")
