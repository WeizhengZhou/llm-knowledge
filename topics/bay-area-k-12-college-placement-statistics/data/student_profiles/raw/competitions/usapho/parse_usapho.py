#!/usr/bin/env python3
"""Parse USAPhO medal listing PDFs into structured JSON."""

import json
import subprocess
import re
from collections import defaultdict

BASEDIR = "/Users/weizheng/projects/claude/llm_knowledge/topics/bay-area-k-12-college-placement-statistics/data/student_profiles/raw/competitions/usapho"

# Bay Area cities for flagging
BAY_AREA_CITIES = {
    "San Jose", "Cupertino", "Palo Alto", "Mountain View", "Fremont",
    "San Ramon", "Pleasanton", "Saratoga", "San Mateo", "San Francisco",
    "Danville", "Belmont", "Los Altos", "Atherton", "Dublin", "Union City",
    "Livermore", "Castro Valley", "Piedmont", "Orinda", "Moraga",
    "Stanford", "Redwood City", "Mountain House",
}

# Tracked Bay Area schools
TRACKED_SCHOOLS = {
    "The Harker School", "Lynbrook High School", "Monta Vista High School",
    "Monta Vista", "Mission San Jose High School", "Mission San Jose High",
    "Gunn High School", "Henry M Gunn High School", "Henry M. Gunn High School",
    "Palo Alto High School", "Palo Alto Senior High School", "Palo Alto High",
    "Saratoga High School", "Dougherty Valley High School", "Dougherty Valley",
    "Amador Valley High School", "Valley Christian High School",
    "Lowell High School", "Proof School", "The Nueva School",
    "Bellarmine College Preparatory", "Archbishop Mitty High School",
    "Monte Vista High School", "Homestead High School", "Homestead high school",
    "Cupertino High School", "Leland High School", "Irvington High School",
    "American High School", "Foothill High School", "California High School",
    "Carlmont High School", "BASIS Independent Silicon Valley",
    "Basis Independent Silicon Valley", "BASIS Independent Fremont",
    "Basis Independent Fremont", "BASIS Independent Fremont Upper",
    "BASIS Independent Fremont (Upper)", "Basis Independent Fremont Upper",
    "Stanford Online High School", "Stanford OHS",
    "Piedmont Hills High School", "Evergreen Valley High School",
    "Menlo School", "Los Altos High School", "Mountain View High School",
    "Quarry Lane School", "The Quarry Lane School",
    "James Logan High School", "Granada High School",
    "Saint Francis High School", "Miramonte High School",
    "Leigh High School", "Campolindo High School",
    "Piedmont High School", "SpringLight Education Institute",
    "William Hopkins Middle School",
}

MEDAL_KEYWORDS = {
    "Gold Medal": "Gold",
    "Silver Medal": "Silver",
    "Bronze Medal": "Bronze",
    "Honorable Mention": "HM",
    "US Physics Team Member": "Team",
}

def parse_pdf(year):
    """Extract students from a single year's PDF."""
    path = f"{BASEDIR}/{year}-Medal-Listing.pdf"
    result = subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True)
    text = result.stdout

    # Split into lines and remove empty lines, page headers/footers
    lines = [l.strip() for l in text.split('\n')]
    lines = [l for l in lines if l]  # remove empty

    students = []
    i = 0

    # Skip header
    while i < len(lines):
        if lines[i] == "State":
            i += 1
            break
        i += 1

    while i < len(lines):
        line = lines[i]

        # Skip page headers/footers
        if re.match(r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)', line):
            i += 1
            continue
        if re.match(r'^Page \d+ of \d+$', line):
            i += 1
            continue
        if line in ("Student", "Medal", "School", "City", "State"):
            i += 1
            continue
        if line.startswith(f"{year} U.S. Physics"):
            i += 1
            continue
        if "Semi Finalists" in line:
            i += 1
            continue

        # Try to parse a student record: name, medal, school, city, state
        # The format alternates: name line, medal line, school line, city line, state line
        # But sometimes city+state get merged or there are edge cases

        # Check if this line could be a medal
        is_medal = any(kw in line for kw in MEDAL_KEYWORDS)

        if not is_medal:
            # This should be a name
            name = line
            # Next should be medal
            if i + 1 < len(lines):
                medal_line = lines[i + 1]
                medal = None
                for kw, short in MEDAL_KEYWORDS.items():
                    if kw in medal_line:
                        medal = short
                        break

                if medal:
                    # Get school, city, state
                    school = lines[i + 2] if i + 2 < len(lines) else ""
                    city = lines[i + 3] if i + 3 < len(lines) else ""
                    state = lines[i + 4] if i + 4 < len(lines) else ""

                    # Skip if school/city/state look like next record or page info
                    skip_patterns = [r'^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)',
                                     r'^Page \d+ of \d+$']

                    # Validate state (should be 2 chars or known)
                    # Sometimes city and state are on one line
                    if len(state) > 3 and not any(re.match(p, state) for p in skip_patterns):
                        # Might be city+state merged
                        parts = state.rsplit(None, 1)
                        if len(parts) == 2 and len(parts[1]) == 2:
                            # Actually city was merged: previous "city" is part of school
                            pass  # leave as-is for now

                    # Clean state
                    state = state.strip().upper()
                    if len(state) > 5:
                        state = ""

                    # Handle the case at end of 2019 where two students are on one line
                    # "Zhou, Amy" and "Zhu, Alexander" appear to be compressed

                    students.append({
                        "name": name.strip(),
                        "school": school.strip(),
                        "city": city.strip(),
                        "state": state.strip(),
                        "medal": medal,
                    })
                    i += 5
                    continue

        i += 1

    return students


def normalize_name(name):
    """Normalize name for matching across years."""
    # Convert to title case, strip extra whitespace
    name = name.strip()
    # Handle "LAST, FIRST" format (all caps)
    parts = name.split(',')
    if len(parts) == 2:
        last = parts[0].strip().title()
        first = parts[1].strip().title()
        # Remove middle name/initial variations and parenthetical
        first = re.sub(r'\s*\(.*?\)', '', first).strip()
        first = first.split()[0] if first else first  # just first name
        return f"{last}, {first}"
    return name.title()


def main():
    all_results = []

    for year in [2019, 2022, 2023, 2024]:
        print(f"Parsing {year}...")
        students = parse_pdf(year)
        print(f"  Found {len(students)} students")

        # Clean up data
        cleaned = []
        for s in students:
            # Skip entries that are clearly parsing errors
            if not s['name'] or not s['medal']:
                continue
            if s['name'] in ('Student', 'Medal', 'School', 'City', 'State'):
                continue
            cleaned.append(s)

        all_results.append({
            "year": year,
            "students": cleaned
        })

    # Save full results
    outpath = f"{BASEDIR}/usapho_results.json"
    with open(outpath, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nSaved {outpath}")

    # Filter California students
    ca_students = []
    for yr in all_results:
        for s in yr['students']:
            if s['state'] in ('CA',):
                ca_students.append({**s, 'year': yr['year']})

    # Flag Bay Area
    for s in ca_students:
        s['bay_area'] = s['city'] in BAY_AREA_CITIES
        s['tracked_school'] = s['school'] in TRACKED_SCHOOLS

    ca_path = f"{BASEDIR}/california_students.json"
    with open(ca_path, 'w') as f:
        json.dump(ca_students, f, indent=2)
    print(f"Saved {ca_path} ({len(ca_students)} CA students)")

    # Multi-year participants
    name_years = defaultdict(list)
    for yr in all_results:
        for s in yr['students']:
            key = normalize_name(s['name'])
            name_years[key].append({
                'year': yr['year'],
                'medal': s['medal'],
                'school': s['school'],
                'state': s['state'],
            })

    multi_year = {k: v for k, v in name_years.items() if len(v) > 1}

    # Generate summary
    summary_lines = [
        "# USAPhO Medal Listing Data Summary",
        "",
        f"Data extracted from AAPT USAPhO medal listing PDFs.",
        f"Years covered: 2019, 2022, 2023, 2024 (2020-2021 cancelled due to COVID).",
        "",
        "## Totals by Year",
        "",
    ]

    for yr in all_results:
        students = yr['students']
        by_medal = defaultdict(int)
        for s in students:
            by_medal[s['medal']] += 1
        summary_lines.append(f"### {yr['year']}")
        summary_lines.append(f"- Total semifinalists: {len(students)}")
        for medal in ['Team', 'Gold', 'Silver', 'Bronze', 'HM']:
            if by_medal[medal]:
                summary_lines.append(f"- {medal}: {by_medal[medal]}")

        ca_count = sum(1 for s in students if s['state'] == 'CA')
        ba_count = sum(1 for s in students if s['state'] == 'CA' and s['city'] in BAY_AREA_CITIES)
        summary_lines.append(f"- California total: {ca_count}")
        summary_lines.append(f"- Bay Area: {ba_count}")
        summary_lines.append("")

    # California breakdown
    summary_lines.extend([
        "## California Students (All Years)",
        "",
    ])

    for yr in all_results:
        summary_lines.append(f"### {yr['year']} California Medalists")
        summary_lines.append("")
        summary_lines.append("| Name | School | City | Medal |")
        summary_lines.append("|------|--------|------|-------|")
        for s in yr['students']:
            if s['state'] == 'CA':
                ba_flag = " *" if s['city'] in BAY_AREA_CITIES else ""
                summary_lines.append(f"| {s['name']} | {s['school']} | {s['city']}{ba_flag} | {s['medal']} |")
        summary_lines.append("")

    # Bay Area school leaderboard
    summary_lines.extend([
        "## Bay Area School Leaderboard (Tracked Schools, 2019+2022-2024)",
        "",
        "| School | Total | Team | Gold | Silver | Bronze | HM |",
        "|--------|-------|------|------|--------|--------|-----|",
    ])

    school_medals = defaultdict(lambda: defaultdict(int))
    for yr in all_results:
        for s in yr['students']:
            if s['school'] in TRACKED_SCHOOLS:
                school_medals[s['school']][s['medal']] += 1
                school_medals[s['school']]['total'] += 1

    # Normalize school names for display
    school_display = {}
    for school in school_medals:
        # Map variants to canonical
        if 'Gunn' in school:
            canonical = 'Gunn High School'
        elif 'Palo Alto' in school and 'High' in school:
            canonical = 'Palo Alto High School'
        elif 'Monta Vista' in school and school != 'Monte Vista High School':
            canonical = 'Monta Vista High School'
        elif 'Mission San Jose' in school:
            canonical = 'Mission San Jose High School'
        elif 'Homestead' in school:
            canonical = 'Homestead High School'
        elif 'Silicon Valley' in school and ('BASIS' in school or 'Basis' in school):
            canonical = 'BASIS Independent Silicon Valley'
        elif 'Fremont' in school and ('BASIS' in school or 'Basis' in school):
            canonical = 'BASIS Independent Fremont'
        elif 'Stanford' in school and ('Online' in school or 'OHS' in school):
            canonical = 'Stanford Online High School'
        elif 'Dougherty' in school:
            canonical = 'Dougherty Valley High School'
        elif 'Quarry Lane' in school:
            canonical = 'Quarry Lane School'
        else:
            canonical = school
        school_display[school] = canonical

    # Merge by canonical name
    canonical_medals = defaultdict(lambda: defaultdict(int))
    for school, medals in school_medals.items():
        canonical = school_display[school]
        for k, v in medals.items():
            canonical_medals[canonical][k] += v

    for school, medals in sorted(canonical_medals.items(), key=lambda x: -x[1]['total']):
        total = medals['total']
        team = medals.get('Team', 0)
        gold = medals.get('Gold', 0)
        silver = medals.get('Silver', 0)
        bronze = medals.get('Bronze', 0)
        hm = medals.get('HM', 0)
        summary_lines.append(f"| {school} | {total} | {team} | {gold} | {silver} | {bronze} | {hm} |")

    summary_lines.append("")

    # Multi-year participants
    summary_lines.extend([
        "## Multi-Year Participants",
        "",
        "Students appearing in 2+ years (trajectory data).",
        "",
    ])

    # Sort by number of appearances, then by whether they're from CA
    for name, appearances in sorted(multi_year.items(), key=lambda x: (-len(x[1]), x[0])):
        states = set(a['state'] for a in appearances)
        ca_flag = " [CA]" if 'CA' in states else ""
        years_str = ", ".join(f"{a['year']} ({a['medal']})" for a in sorted(appearances, key=lambda x: x['year']))
        schools = set(a['school'] for a in appearances)
        school_str = " / ".join(schools) if len(schools) > 1 else list(schools)[0]
        summary_lines.append(f"- **{name}**{ca_flag}: {years_str} — {school_str}")

    summary_lines.append("")
    summary_lines.extend([
        "## Notes",
        "",
        "- 2020 and 2021 competitions were cancelled due to COVID-19.",
        "- 2023 and 2024 include a 'US Physics Team Member' tier (top ~20, above Gold).",
        "- Bay Area cities flagged with * in California tables.",
        "- 'Tracked school' = school in our Bay Area K-12 tracking list.",
        "- Some students attend boarding/online schools (Phillips Exeter, Stanford OHS, etc.) but may be Bay Area residents.",
        "- Multi-year matching is by normalized name only. Common names (e.g. 'Wang, Daniel', 'Liu, Andrew') may conflate different students from different states/schools. Entries with multiple schools in different states are likely name collisions, not transfers.",
    ])

    summary_path = f"{BASEDIR}/summary.md"
    with open(summary_path, 'w') as f:
        f.write('\n'.join(summary_lines) + '\n')
    print(f"Saved {summary_path}")

    # Print highlights
    print(f"\n=== HIGHLIGHTS ===")
    print(f"Multi-year CA participants:")
    for name, appearances in sorted(multi_year.items(), key=lambda x: (-len(x[1]), x[0])):
        states = set(a['state'] for a in appearances)
        if 'CA' in states:
            years_str = ", ".join(f"{a['year']}({a['medal']})" for a in sorted(appearances, key=lambda x: x['year']))
            print(f"  {name}: {years_str}")


if __name__ == '__main__':
    main()
