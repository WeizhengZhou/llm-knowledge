#!/usr/bin/env python3
"""
Extract structured student profile data from raw crawled posts using LLM.

This uses Claude via the Anthropic SDK to parse unstructured text into
structured JSON profiles. Falls back to rule-based extraction for simple cases.

Usage:
    # Extract a single raw file
    python llm_extractor.py raw/reddit/collegeresults/abc123.md

    # Extract all unprocessed files in a directory
    python llm_extractor.py raw/reddit/collegeresults/

    # Dry run (show extracted JSON without saving to DB)
    python llm_extractor.py raw/reddit/collegeresults/abc123.md --dry-run
"""

import json
import re
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "profiles.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

# Add parent dir for normalize_college
sys.path.insert(0, str(Path(__file__).parent.parent))
from ingest_athletes import normalize_college


EXTRACTION_PROMPT = """Extract structured data from this college application results post. Return ONLY valid JSON matching the schema below. If a field is not mentioned, use null.

SCHEMA:
{
  "extraction_confidence": <float 0-1>,
  "demographics": {
    "gender": "<male|female|nonbinary|null>",
    "ethnicity": "<asian|white|black|hispanic|native|multiracial|other|null>",
    "ethnicity_detail": "<e.g. chinese-american, korean, indian|null>",
    "first_gen": <true|false|null>,
    "legacy": "<undergrad|graduate|double|null>",
    "state": "<2-letter state code|null>",
    "region": "<bay-area|northeast|southeast|midwest|west|southwest|pacific-nw|null>",
    "school_type": "<private|public|charter|magnet|homeschool|null>",
    "school_name_hint": "<if mentioned|null>",
    "school_size_hint": "<e.g. '~200 per class'|null>",
    "hooks": ["<legacy|athlete|first-gen|urm|rural|low-income|none>"]
  },
  "academics": {
    "gpa_uw": <float|null>,
    "gpa_w": <float|null>,
    "class_rank": "<text|null>",
    "sat": <int 400-1600|null>,
    "act": <int 1-36|null>,
    "ap_count": <int|null>,
    "ap_scores": "<summary|null>",
    "notable_courses": ["<course names>"]
  },
  "extracurriculars": [
    {"activity": "<name>", "years": <int|null>, "level": "<school|regional|state|national|international|null>", "detail": "<brief>"}
  ],
  "awards": [
    {"name": "<award>", "level": "<school|regional|state|national|international>", "detail": "<brief|null>"}
  ],
  "application_year": <int|null>,
  "results": [
    {"college": "<full name>", "round": "<ED|ED2|EA|REA|RD|null>", "result": "<accepted|rejected|waitlisted|deferred>", "enrolled": <true|false|null>}
  ]
}

POST CONTENT:
{post_content}

Return ONLY the JSON object. No markdown, no explanation."""


def rule_based_extract(text: str) -> dict:
    """Simple rule-based extraction for common patterns. Fallback if no LLM available."""
    profile = {
        "extraction_confidence": 0.5,
        "demographics": {},
        "academics": {},
        "extracurriculars": [],
        "awards": [],
        "application_year": None,
        "results": [],
    }

    text_lower = text.lower()

    # Gender
    if "female" in text_lower or "girl" in text_lower or "woman" in text_lower:
        profile["demographics"]["gender"] = "female"
    elif "male" in text_lower or "boy" in text_lower or "guy" in text_lower:
        profile["demographics"]["gender"] = "male"

    # Ethnicity
    for eth, label in [("asian", "asian"), ("chinese", "asian"), ("indian", "asian"),
                        ("korean", "asian"), ("vietnamese", "asian"), ("japanese", "asian"),
                        ("black", "black"), ("african american", "black"),
                        ("hispanic", "hispanic"), ("latino", "hispanic"), ("latina", "hispanic"),
                        ("white", "white"), ("caucasian", "white")]:
        if eth in text_lower:
            profile["demographics"]["ethnicity"] = label
            break

    # GPA
    gpa_uw = re.search(r'(?:uw|unweighted)\s*(?:gpa)?[:\s]*(\d+\.\d+)', text_lower)
    gpa_w = re.search(r'(?:w|weighted)\s*(?:gpa)?[:\s]*(\d+\.\d+)', text_lower)
    if not gpa_uw:
        gpa_uw = re.search(r'gpa[:\s]*(\d+\.\d+)\s*/\s*4\.0', text_lower)
    if not gpa_w:
        gpa_w = re.search(r'gpa[:\s]*(\d+\.\d+)\s*/\s*(?:5\.0|100)', text_lower)

    if gpa_uw:
        profile["academics"]["gpa_uw"] = float(gpa_uw.group(1))
    if gpa_w:
        profile["academics"]["gpa_w"] = float(gpa_w.group(1))

    # SAT
    sat = re.search(r'sat[:\s]*(\d{3,4})', text_lower)
    if sat:
        score = int(sat.group(1))
        if 400 <= score <= 1600:
            profile["academics"]["sat"] = score

    # ACT
    act = re.search(r'act[:\s]*(\d{1,2})', text_lower)
    if act:
        score = int(act.group(1))
        if 1 <= score <= 36:
            profile["academics"]["act"] = score

    # AP count
    ap = re.search(r'(\d+)\s*aps?\b', text_lower)
    if ap:
        profile["academics"]["ap_count"] = int(ap.group(1))

    # Results — multiple format strategies
    # Strategy 1: Section-based ("Acceptances:", "Rejections:", "Waitlists:" followed by bullet lists)
    current_result_type = None
    for line in text.split('\n'):
        line_stripped = line.strip().lower()

        # Detect section headers
        if re.match(r'^#{0,3}\s*\**\s*accept', line_stripped):
            current_result_type = "accepted"
            continue
        elif re.match(r'^#{0,3}\s*\**\s*reject', line_stripped):
            current_result_type = "rejected"
            continue
        elif re.match(r'^#{0,3}\s*\**\s*waitlist', line_stripped):
            current_result_type = "waitlisted"
            continue
        elif re.match(r'^#{0,3}\s*\**\s*defer', line_stripped):
            current_result_type = "deferred"
            continue
        elif re.match(r'^#{0,3}\s*\**\s*(demographics|stats|extracurricular|award|honor|letter|interview|essay|additional|final)', line_stripped):
            current_result_type = None
            continue

        # If we're in a results section, extract college names from bullets
        if current_result_type and re.match(r'^[\-\*\\•]\s*', line.strip()):
            college_text = re.sub(r'^[\-\*\\•]+\s*', '', line.strip())
            # Clean up markdown formatting
            college_text = re.sub(r'\*+', '', college_text)
            college_text = re.sub(r'\\-\s*', '', college_text)
            # Remove round info in parens but capture it
            round_match = re.search(r'\((ED|ED2|EA|REA|RD)\)', college_text, re.IGNORECASE)
            app_round = round_match.group(1).upper() if round_match else None
            college_text = re.sub(r'\(.*?\)', '', college_text)
            # Remove trailing punctuation and emoji
            college_text = re.sub(r'[!🎉🥳✅❌💀😭]+', '', college_text).strip()
            # Remove "— enrolled" type suffixes but detect enrollment
            enrolled = "commit" in college_text.lower() or "enrolled" in college_text.lower() or "attending" in college_text.lower()
            college_text = re.sub(r'\s*[-—–]\s*(enrolled|committed|attending).*', '', college_text, flags=re.IGNORECASE).strip()

            if college_text and len(college_text) > 2 and not college_text.startswith('#'):
                profile["results"].append({
                    "college": college_text,
                    "round": app_round,
                    "result": current_result_type,
                    "enrolled": enrolled if enrolled else None,
                })

    # Strategy 2: "College (rate%): Result" format (common in r/collegeresults)
    # Also handles: "College: **Accepted**", "College — Rejected"
    if not profile["results"]:
        current_round = None
        for line in text.split('\n'):
            line_stripped = line.strip()
            line_lower = line_stripped.lower()

            # Detect round headers: "ED:", "EA:", "RD:", "REA:"
            round_match = re.match(r'^(ED2?|EA|REA|SCEA|RD)\s*:', line_stripped, re.IGNORECASE)
            if round_match:
                current_round = round_match.group(1).upper()
                continue

            # Pattern: "College (optional%): **Result**" or "College (rate): Result"
            m = re.match(
                r'[*\-•\\]?\s*\*?\*?([A-Za-z][A-Za-z\s&\'\.\-,()]+?)\s*'
                r'(?:\([^)]*\))?\s*'  # optional (rate%) or (description)
                r'[\-:–—]\s*'
                r'(?:>?\s*)?'
                r'\*?\*?(Accepted|Rejected|Waitlisted|Admitted|Denied|Deferred)\*?\*?',
                line_stripped, re.IGNORECASE)
            if m:
                college = m.group(1).strip().rstrip('*').rstrip(',').strip()
                # Clean up escaped characters
                college = college.replace('\\-', '-').replace('\\', '')
                result = m.group(2).lower()
                if result in ("admitted", "accepted"):
                    result = "accepted"
                elif result == "denied":
                    result = "rejected"
                enrolled = "commit" in line_lower or "enrolled" in line_lower or "attending" in line_lower
                profile["results"].append({
                    "college": college,
                    "round": current_round,
                    "result": result,
                    "enrolled": enrolled if enrolled else None,
                })
                continue

            # Pattern: emoji-based: "✅ College" or "❌ College"
            emoji_match = re.match(r'([✅✓☑🟢])\s*(.+?)(?:\n|$)', line_stripped)
            if emoji_match:
                profile["results"].append({
                    "college": emoji_match.group(2).strip(),
                    "round": current_round,
                    "result": "accepted",
                    "enrolled": None,
                })
                continue
            emoji_match = re.match(r'([❌✗☒🔴])\s*(.+?)(?:\n|$)', line_stripped)
            if emoji_match:
                profile["results"].append({
                    "college": emoji_match.group(2).strip(),
                    "round": current_round,
                    "result": "rejected",
                    "enrolled": None,
                })

    # School type
    for indicator, stype in [("private school", "private"), ("public school", "public"),
                              ("charter", "charter"), ("magnet", "magnet")]:
        if indicator in text_lower:
            profile["demographics"]["school_type"] = stype
            break

    # State
    state_match = re.search(r'\b(CA|NY|TX|MA|IL|PA|FL|NJ|VA|WA|CT|MD|GA|NC|OH)\b', text)
    if state_match:
        profile["demographics"]["state"] = state_match.group(1)

    # First gen
    if "first gen" in text_lower or "first-gen" in text_lower or "fgli" in text_lower:
        profile["demographics"]["first_gen"] = True

    return profile


def validate_profile(profile: dict) -> list:
    """Validate extracted profile, return list of issues."""
    issues = []

    academics = profile.get("academics", {})
    if academics.get("gpa_uw") and not (0.0 <= academics["gpa_uw"] <= 4.5):
        issues.append(f"GPA UW out of range: {academics['gpa_uw']}")
    if academics.get("gpa_w") and not (0.0 <= academics["gpa_w"] <= 5.5):
        # Some schools use 100-point scale
        if not (50 <= academics["gpa_w"] <= 100):
            issues.append(f"GPA W out of range: {academics['gpa_w']}")
    if academics.get("sat") and not (400 <= academics["sat"] <= 1600):
        issues.append(f"SAT out of range: {academics['sat']}")
    if academics.get("act") and not (1 <= academics["act"] <= 36):
        issues.append(f"ACT out of range: {academics['act']}")

    results = profile.get("results", [])
    enrolled_count = sum(1 for r in results if r.get("enrolled"))
    if enrolled_count > 1:
        issues.append(f"Multiple enrolled schools: {enrolled_count}")

    year = profile.get("application_year")
    if year and not (2015 <= year <= 2030):
        issues.append(f"Application year out of range: {year}")

    return issues


def store_profile(db: sqlite3.Connection, profile: dict, source: str, source_id: str, source_url: str, raw_text: str):
    """Store extracted profile in SQLite."""
    demo = profile.get("demographics", {})
    acad = profile.get("academics", {})

    # Delete old results if re-processing
    existing = db.execute(
        "SELECT id FROM student_profiles WHERE source=? AND source_id=?",
        (source, source_id)).fetchone()
    if existing:
        db.execute("DELETE FROM application_results WHERE profile_id=?", (existing[0],))
        db.execute("DELETE FROM student_profiles WHERE id=?", (existing[0],))

    cursor = db.execute(
        """INSERT INTO student_profiles
        (source, source_id, source_url, extraction_confidence,
         application_year, gender, ethnicity, ethnicity_detail,
         first_gen, legacy, state, region, school_type,
         school_name_hint, school_size_hint, hooks_json,
         gpa_uw, gpa_w, class_rank, sat, act, ap_count,
         ecs_json, awards_json, essay_topics, raw_text)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (source, source_id, source_url, profile.get("extraction_confidence"),
         profile.get("application_year"), demo.get("gender"), demo.get("ethnicity"),
         demo.get("ethnicity_detail"), demo.get("first_gen"), demo.get("legacy"),
         demo.get("state"), demo.get("region"), demo.get("school_type"),
         demo.get("school_name_hint"), demo.get("school_size_hint"),
         json.dumps(demo.get("hooks", [])),
         acad.get("gpa_uw"), acad.get("gpa_w"), acad.get("class_rank"),
         acad.get("sat"), acad.get("act"), acad.get("ap_count"),
         json.dumps(profile.get("extracurriculars", [])),
         json.dumps(profile.get("awards", [])),
         profile.get("essay_topics"), raw_text),
    )

    profile_id = cursor.lastrowid

    for result in profile.get("results", []):
        college = result.get("college", "")
        if not college:
            continue
        cn = normalize_college(college)
        try:
            db.execute(
                """INSERT OR IGNORE INTO application_results
                (profile_id, college, college_normalized, round, result, enrolled, scholarship)
                VALUES (?,?,?,?,?,?,?)""",
                (profile_id, college, cn, result.get("round"),
                 result["result"], result.get("enrolled", False), result.get("scholarship")),
            )
        except sqlite3.Error:
            pass

    db.commit()
    return profile_id


def extract_file(filepath: Path, dry_run: bool = False) -> dict:
    """Extract a single raw file using rule-based extraction."""
    text = filepath.read_text()

    # Parse frontmatter
    fm = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    fm[key.strip()] = val.strip().strip('"')
            text_body = parts[2].strip()
        else:
            text_body = text
    else:
        text_body = text

    # Extract using rules (LLM extraction would go here)
    profile = rule_based_extract(text_body)

    # Validate
    issues = validate_profile(profile)

    source = fm.get("source", "reddit/collegeresults")
    source_id = fm.get("source_id", filepath.stem)
    source_url = fm.get("url", "")

    if dry_run:
        print(f"\n{'='*60}")
        print(f"File: {filepath.name}")
        print(f"Source: {source_id}")
        print(f"Confidence: {profile.get('extraction_confidence', 'N/A')}")
        print(f"Gender: {profile.get('demographics', {}).get('gender')}")
        print(f"Ethnicity: {profile.get('demographics', {}).get('ethnicity')}")
        print(f"SAT: {profile.get('academics', {}).get('sat')}")
        print(f"GPA UW: {profile.get('academics', {}).get('gpa_uw')}")
        print(f"Results: {len(profile.get('results', []))} schools")
        for r in profile.get("results", [])[:10]:
            print(f"  {r.get('college', '?'):30s} → {r.get('result', '?')}")
        if issues:
            print(f"VALIDATION ISSUES: {issues}")
        return profile

    # Store in DB
    db = sqlite3.connect(DB_PATH)
    db.executescript(SCHEMA_PATH.read_text())
    pid = store_profile(db, profile, source, source_id, source_url, text_body)
    db.close()
    print(f"  Stored profile {pid} from {filepath.name} ({len(profile.get('results', []))} results)")
    return profile


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Raw file or directory to extract")
    parser.add_argument("--dry-run", action="store_true", help="Print extraction without saving to DB")
    args = parser.parse_args()

    if args.path.is_dir():
        files = sorted(args.path.glob("*.md"))
    else:
        files = [args.path]

    # Init DB
    if not args.dry_run:
        db = sqlite3.connect(DB_PATH)
        db.executescript(SCHEMA_PATH.read_text())
        db.close()

    for f in files:
        extract_file(f, dry_run=args.dry_run)

    if not args.dry_run:
        db = sqlite3.connect(DB_PATH)
        total = db.execute("SELECT COUNT(*) FROM student_profiles").fetchone()[0]
        results = db.execute("SELECT COUNT(*) FROM application_results").fetchone()[0]
        print(f"\nDB totals: {total} profiles, {results} application results")
        db.close()


if __name__ == "__main__":
    main()
