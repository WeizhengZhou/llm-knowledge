#!/usr/bin/env python3
"""
Entity Resolution Pipeline — Link students across competition databases.

Matches named student records from MATHCOUNTS (grades 6-8), USAPhO (grades 9-12),
and athlete commits (grade 12), then cross-references with college placement data.

Usage:
    python entity_resolver.py                    # run full pipeline
    python entity_resolver.py --summary-only     # skip file output, print summary
    python entity_resolver.py --min-confidence 0.8  # filter low-confidence matches
"""

import json
import sqlite3
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
import argparse

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(__file__).resolve().parent
TOPIC = BASE.parent
DATA = TOPIC
MATHCOUNTS_PATH = BASE / "raw/competitions/mathcounts/mathcounts_ca_results.json"
USAPHO_PATH = BASE / "raw/competitions/usapho/california_students.json"
DB_PATH = DATA / "college_placement.db"
OUTPUT_PATH = BASE / "resolved_trajectories.json"

# ---------------------------------------------------------------------------
# School name normalization map — maps competition school names to DB school_ids
# ---------------------------------------------------------------------------
SCHOOL_NORM: dict[str, str] = {
    # Private schools
    "the harker school": "harker",
    "harker school": "harker",
    "harker": "harker",
    "menlo school": "menlo",
    "menlo": "menlo",
    "castilleja school": "castilleja",
    "castilleja": "castilleja",
    "the nueva school": "nueva",
    "nueva school": "nueva",
    "nueva": "nueva",
    "crystal springs uplands school": "crystal-springs",
    "crystal springs uplands": "crystal-springs",
    "pinewood school": "pinewood",
    "pinewood": "pinewood",
    "woodside priory school": "woodside-priory",
    "woodside priory": "woodside-priory",
    "sacred heart preparatory": "sacred-heart-atherton",
    "sacred heart prep": "sacred-heart-atherton",
    "basis independent silicon valley": "basis-sv",
    "basis independent fremont": "basis-fremont",
    "proof school": "proof-school",
    # Public schools
    "palo alto high school": "palo-alto-high",
    "palo alto high": "palo-alto-high",
    "palo alto senior high school": "palo-alto-high",
    "henry m. gunn high school": "gunn",
    "gunn high school": "gunn",
    "gunn high": "gunn",
    "lynbrook high school": "lynbrook",
    "lynbrook high": "lynbrook",
    "monta vista high school": "monta-vista",
    "monta vista": "monta-vista",
    "mission san jose high school": "mission-san-jose",
    "mission san jose high": "mission-san-jose",
    "saratoga high school": "saratoga",
    "saratoga high": "saratoga",
    "homestead high school": "homestead",
    "homestead high": "homestead",
    "cupertino high school": "cupertino-high",
    "cupertino high": "cupertino-high",
    "amador valley high school": "amador-valley",
    "amador valley high": "amador-valley",
    "dougherty valley high school": "dougherty-valley",
    "dougherty valley high": "dougherty-valley",
    "mountain view high school": "mountain-view-high",
    "mountain view high": "mountain-view-high",
    "lowell high school": "lowell",
    "lowell high": "lowell",
    "valley christian high school": "valley-christian",
    "valley christian high": "valley-christian",
    # Middle schools that feed into tracked high schools
    "bullis charter school": "bullis",
    "joaquin miller middle school": "joaquin-miller",
    "hopkins middle school": "hopkins",
    "ellen fletcher middle school": "fletcher",
    "challenger school berryessa": "challenger-berryessa",
    "rancho milpitas middle school": "rancho-milpitas",
    "sierra vista middle school": "sierra-vista",
    "kennedy middle school": "kennedy-cupertino",
    "redwood middle school": "redwood-middle",
    "gale ranch middle school": "gale-ranch",
    "thornton middle school": "thornton",
    "bret harte middle school": "bret-harte",
    "peterson middle school": "peterson",
    "union middle school": "union-middle",
    "stratford preparatory blackford middle": "stratford-blackford",
}

# Middle school -> likely high school feeder mapping (Bay Area)
FEEDER_MAP: dict[str, list[str]] = {
    "bullis": ["palo-alto-high", "gunn"],
    "joaquin-miller": ["cupertino-high", "monta-vista", "lynbrook", "homestead"],
    "hopkins": ["palo-alto-high", "gunn"],
    "fletcher": ["palo-alto-high", "gunn"],
    "challenger-berryessa": ["harker", "lynbrook", "monta-vista"],
    "rancho-milpitas": ["milpitas-high", "monta-vista"],
    # sierra-vista: excluded — SoCal, not Bay Area feeder
    "kennedy-cupertino": ["cupertino-high", "monta-vista", "homestead", "lynbrook"],
    "thornton": ["saratoga", "lynbrook", "monta-vista"],
    "bret-harte": ["palo-alto-high", "gunn"],
    "peterson": ["palo-alto-high", "gunn"],
    "redwood-middle": ["saratoga"],
    "gale-ranch": ["dougherty-valley"],
    "union-middle": ["palo-alto-high", "gunn"],
    "stratford-blackford": ["harker", "lynbrook", "monta-vista"],
    "basis-sv": ["basis-sv"],  # K-12
    "harker": ["harker"],  # K-12
    "nueva": ["nueva"],  # K-12
    "castilleja": ["castilleja"],  # 6-12
    "crystal-springs": ["crystal-springs"],  # 6-12
    "proof-school": ["proof-school"],  # 6-12
}

# Bay Area cities for geographic matching
BAY_AREA_CITIES = {
    "san jose", "palo alto", "cupertino", "mountain view", "sunnyvale",
    "santa clara", "milpitas", "fremont", "pleasanton", "san ramon",
    "dublin", "livermore", "san mateo", "hillsborough", "atherton",
    "menlo park", "redwood city", "san francisco", "berkeley", "oakland",
    "saratoga", "los gatos", "campbell", "portola valley", "woodside",
    "los altos", "los altos hills", "stanford",
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class StudentRecord:
    """A single record from one data source."""
    source: str  # "mathcounts", "usapho", "athlete_commits"
    name_raw: str
    name_first: str
    name_last: str
    name_normalized: str  # "last_first" lowercase
    school_raw: str
    school_normalized: Optional[str]  # mapped to DB school_id or slug
    year: int
    grade: Optional[int] = None
    city: Optional[str] = None
    state: str = "CA"
    bay_area: Optional[bool] = None
    # Competition-specific
    competition: Optional[str] = None
    result: Optional[str] = None  # rank, medal, sport
    detail: Optional[str] = None  # college for athletes, level for mathcounts


@dataclass
class Trajectory:
    """A resolved student entity with linked records."""
    entity_id: str
    name: str
    confidence: float
    match_type: str
    school_trajectory: list[str] = field(default_factory=list)
    achievements: list[dict] = field(default_factory=list)
    school_context: Optional[dict] = None  # placement data from DB
    records: list[StudentRecord] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = {
            "entity_id": self.entity_id,
            "name": self.name,
            "confidence": self.confidence,
            "match_type": self.match_type,
            "school_trajectory": self.school_trajectory,
            "achievements": self.achievements,
        }
        if self.school_context:
            d["school_context"] = self.school_context
        return d


# ---------------------------------------------------------------------------
# Name normalization
# ---------------------------------------------------------------------------
def normalize_unicode(text: str) -> str:
    """Remove ligatures, combining chars, normalize whitespace."""
    # Normalize unicode (handle fi ligatures etc.)
    text = unicodedata.normalize("NFKD", text)
    # Remove combining characters
    text = "".join(c for c in text if not unicodedata.combining(c))
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_name(name_raw: str, source: str) -> tuple[str, str, str]:
    """
    Parse a name into (first, last, normalized_key).

    USAPhO format: "Last, First"
    MATHCOUNTS format: "First Last" (sometimes "First(Nickname) Last")
    Athlete commits: "First Last"
    """
    name = normalize_unicode(name_raw.strip())

    if source == "usapho" and "," in name:
        parts = name.split(",", 1)
        last = parts[0].strip()
        first = parts[1].strip()
    else:
        # Handle parenthetical nicknames: "Arthur(Yuxin) Chang" -> first="Arthur", last="Chang"
        name_clean = re.sub(r"\([^)]*\)", "", name).strip()
        name_clean = re.sub(r"\s+", " ", name_clean)
        parts = name_clean.split()
        if len(parts) >= 2:
            first = parts[0]
            last = parts[-1]  # take last word as surname
        elif len(parts) == 1:
            first = parts[0]
            last = ""
        else:
            first = name
            last = ""

    first = first.strip().title()
    last = last.strip().title()
    # Handle ALL CAPS names like "Maxwell LIU" or "Aditya ASHOK"
    if last.isupper() and len(last) > 1:
        last = last.title()
    if first.isupper() and len(first) > 1:
        first = first.title()

    normalized = f"{last.lower()}_{first.lower()}"
    return first, last, normalized


def normalize_school(school_raw: str) -> Optional[str]:
    """Map school name to normalized school_id."""
    if not school_raw:
        return None
    key = normalize_unicode(school_raw.strip().lower())
    return SCHOOL_NORM.get(key)


# ---------------------------------------------------------------------------
# Jaro-Winkler similarity (pure Python implementation)
# ---------------------------------------------------------------------------
def jaro_similarity(s1: str, s2: str) -> float:
    """Compute Jaro similarity between two strings."""
    if s1 == s2:
        return 1.0
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0.0

    match_distance = max(len1, len2) // 2 - 1
    if match_distance < 0:
        match_distance = 0

    s1_matches = [False] * len1
    s2_matches = [False] * len2
    matches = 0
    transpositions = 0

    for i in range(len1):
        start = max(0, i - match_distance)
        end = min(i + match_distance + 1, len2)
        for j in range(start, end):
            if s2_matches[j] or s1[i] != s2[j]:
                continue
            s1_matches[i] = True
            s2_matches[j] = True
            matches += 1
            break

    if matches == 0:
        return 0.0

    k = 0
    for i in range(len1):
        if not s1_matches[i]:
            continue
        while not s2_matches[k]:
            k += 1
        if s1[i] != s2[k]:
            transpositions += 1
        k += 1

    return (matches / len1 + matches / len2 +
            (matches - transpositions / 2) / matches) / 3


def jaro_winkler(s1: str, s2: str, p: float = 0.1) -> float:
    """Compute Jaro-Winkler similarity."""
    jaro = jaro_similarity(s1, s2)
    # Find common prefix length (up to 4)
    prefix = 0
    for i in range(min(len(s1), len(s2), 4)):
        if s1[i] == s2[i]:
            prefix += 1
        else:
            break
    return jaro + prefix * p * (1 - jaro)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------
def load_mathcounts() -> list[StudentRecord]:
    """Load MATHCOUNTS CA results."""
    with open(MATHCOUNTS_PATH) as f:
        data = json.load(f)

    records = []
    for entry in data:
        year = entry["year"]
        level = entry["level"]
        region = entry.get("region", "")
        students = entry.get("students", [])

        for s in students:
            name_raw = s["name"]
            first, last, norm = parse_name(name_raw, "mathcounts")
            school_raw = s.get("school", "")
            school_norm = normalize_school(school_raw)

            rank = s.get("rank")
            result_str = f"Rank {rank}" if rank else f"{level} qualifier"
            ind_rank = s.get("individual_rank")
            if ind_rank:
                result_str = f"Individual Rank {ind_rank}"

            records.append(StudentRecord(
                source="mathcounts",
                name_raw=name_raw,
                name_first=first,
                name_last=last,
                name_normalized=norm,
                school_raw=school_raw,
                school_normalized=school_norm,
                year=year,
                grade=None,  # MATHCOUNTS is grades 6-8; we don't know exact grade
                state="CA",
                bay_area=(False if region == "socal"
                         else (True if region in ("norcal",) or school_norm
                               else None)),
                competition="MATHCOUNTS",
                result=result_str,
                detail=f"{level}/{region}",
            ))
    return records


def load_usapho() -> list[StudentRecord]:
    """Load USAPhO California students."""
    with open(USAPHO_PATH) as f:
        data = json.load(f)

    records = []
    for r in data:
        name_raw = r["name"]
        first, last, norm = parse_name(name_raw, "usapho")
        school_raw = r.get("school", "")
        school_norm = normalize_school(school_raw)

        records.append(StudentRecord(
            source="usapho",
            name_raw=name_raw,
            name_first=first,
            name_last=last,
            name_normalized=norm,
            school_raw=school_raw,
            school_normalized=school_norm,
            year=r["year"],
            grade=None,  # USAPhO is grades 9-12
            city=r.get("city"),
            state=r.get("state", "CA"),
            bay_area=r.get("bay_area"),
            competition="USAPhO",
            result=r["medal"],
            detail=None,
        ))
    return records


def load_athlete_commits() -> list[StudentRecord]:
    """Load athlete commits from the college placement DB."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM athlete_commits"
    ).fetchall()
    conn.close()

    records = []
    for r in rows:
        name_raw = r["student_name"] or ""
        if not name_raw.strip():
            continue
        first, last, norm = parse_name(name_raw, "athlete_commits")
        school_id = r["school_id"]

        records.append(StudentRecord(
            source="athlete_commits",
            name_raw=name_raw,
            name_first=first,
            name_last=last,
            name_normalized=norm,
            school_raw=school_id,
            school_normalized=school_id,  # already a school_id
            year=r["grad_year"],
            grade=12,  # athlete commits are always senior year
            state="CA",
            bay_area=True,
            competition="Athlete Commit",
            result=r["sport"],
            detail=r["college"],
        ))
    return records


# ---------------------------------------------------------------------------
# School context from placement DB
# ---------------------------------------------------------------------------
def get_school_context(school_ids: list[str]) -> dict[str, dict]:
    """Pull Ivy+ placement stats for schools from the DB."""
    if not school_ids:
        return {}
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    context = {}
    for sid in set(school_ids):
        # Get total Ivy+ enrolled
        row = conn.execute("""
            SELECT school_id,
                   SUM(count) as ivy_plus_total
            FROM placements
            WHERE school_id = ?
              AND metric = 'enrolled'
              AND college_normalized IN (
                  'harvard', 'yale', 'princeton', 'columbia', 'upenn', 'brown',
                  'dartmouth', 'cornell', 'stanford', 'mit', 'caltech',
                  'duke', 'uchicago', 'northwestern', 'jhu'
              )
            GROUP BY school_id
        """, (sid,)).fetchone()

        if row:
            context[sid] = {
                "school_id": sid,
                "ivy_plus_enrolled_total": row["ivy_plus_total"],
            }

        # Get school name
        name_row = conn.execute(
            "SELECT name, city FROM schools WHERE school_id = ?", (sid,)
        ).fetchone()
        if name_row:
            if sid not in context:
                context[sid] = {"school_id": sid}
            context[sid]["school_name"] = name_row["name"]
            context[sid]["city"] = name_row["city"]

    conn.close()
    return context


# ---------------------------------------------------------------------------
# Matching logic
# ---------------------------------------------------------------------------
def estimate_grade_range(record: StudentRecord) -> tuple[int, int]:
    """
    Estimate the grade a student was in when the record was created.
    Returns (min_grade, max_grade).
    """
    if record.grade:
        return (record.grade, record.grade)
    if record.source == "mathcounts":
        return (6, 8)
    if record.source == "usapho":
        return (9, 12)
    if record.source == "athlete_commits":
        return (12, 12)
    return (6, 12)


def age_compatible(r1: StudentRecord, r2: StudentRecord) -> bool:
    """
    Check if two records could plausibly be the same student based on year/grade.

    A MATHCOUNTS student (grades 6-8) in year X could be in USAPhO (grades 9-12)
    roughly 1-6 years later.
    """
    year_diff = r2.year - r1.year
    g1_min, g1_max = estimate_grade_range(r1)
    g2_min, g2_max = estimate_grade_range(r2)

    # The student ages 1 grade per year
    # If in grade g1 in year y1, they'd be in grade g1 + (y2 - y1) in year y2
    projected_min = g1_min + year_diff
    projected_max = g1_max + year_diff

    # Check overlap with r2's grade range
    return projected_min <= g2_max and projected_max >= g2_min


def schools_compatible(r1: StudentRecord, r2: StudentRecord) -> bool:
    """Check if two school assignments are compatible (same school or feeder)."""
    s1 = r1.school_normalized
    s2 = r2.school_normalized
    if not s1 or not s2:
        return False
    if s1 == s2:
        return True
    # Check feeder pattern: MATHCOUNTS middle school -> USAPhO high school
    if r1.source == "mathcounts" and r2.source in ("usapho", "athlete_commits"):
        feeders = FEEDER_MAP.get(s1, [])
        if s2 in feeders:
            return True
    if r2.source == "mathcounts" and r1.source in ("usapho", "athlete_commits"):
        feeders = FEEDER_MAP.get(s2, [])
        if s1 in feeders:
            return True
    return False


def resolve_entities(
    all_records: list[StudentRecord],
    min_confidence: float = 0.0,
) -> list[Trajectory]:
    """
    Main entity resolution: group records belonging to the same student.

    Phase 1: Exact name + same school (95%)
    Phase 2: Fuzzy name (Jaro-Winkler > 0.9) + same school (85%)
    Phase 3: Same name + compatible age + same city/state (75%)
    Phase 4: Cross-competition matching (MATHCOUNTS -> USAPhO via feeder schools)
    """

    # Index records by normalized name for fast lookup
    by_norm_name: dict[str, list[StudentRecord]] = defaultdict(list)
    for r in all_records:
        by_norm_name[r.name_normalized].append(r)

    # Track which records have been assigned to an entity
    assigned: set[int] = set()  # indices into all_records
    record_idx = {id(r): i for i, r in enumerate(all_records)}
    entities: list[Trajectory] = []
    entity_counter = 0

    def make_entity(records: list[StudentRecord], confidence: float,
                    match_type: str) -> Trajectory:
        nonlocal entity_counter
        entity_counter += 1
        # Use the most complete name
        best_name = max(records, key=lambda r: len(r.name_raw))
        # Normalize the display name to "First Last"
        display_name = f"{best_name.name_first} {best_name.name_last}".strip()

        schools = []
        seen_schools_lower = set()
        for r in sorted(records, key=lambda r: r.year):
            school = r.school_raw
            if school and school.lower() not in seen_schools_lower:
                schools.append(school)
                seen_schools_lower.add(school.lower())

        achievements = []
        for r in sorted(records, key=lambda r: r.year):
            ach = {
                "year": r.year,
                "competition": r.competition,
                "result": r.result,
                "source": r.source,
            }
            if r.detail:
                ach["detail"] = r.detail
            achievements.append(ach)

        return Trajectory(
            entity_id=f"traj_{entity_counter:04d}",
            name=display_name,
            confidence=confidence,
            match_type=match_type,
            school_trajectory=schools,
            achievements=achievements,
            records=records,
        )

    # ------- Phase 1: Exact name + same school = 95% -------
    for norm_name, group in by_norm_name.items():
        if len(group) < 2:
            continue
        # Sub-group by school_normalized
        by_school: dict[str, list[StudentRecord]] = defaultdict(list)
        for r in group:
            if r.school_normalized:
                by_school[r.school_normalized].append(r)

        for school, school_group in by_school.items():
            if len(school_group) >= 2:
                indices = [record_idx[id(r)] for r in school_group]
                if any(i in assigned for i in indices):
                    continue
                if age_compatible(school_group[0], school_group[-1]):
                    ent = make_entity(school_group, 0.95, "exact_name_school")
                    if ent.confidence >= min_confidence:
                        entities.append(ent)
                    for i in indices:
                        assigned.add(i)

    # ------- Phase 2: Fuzzy name + same school = 85% -------
    # Compare unassigned records with each other
    unassigned_records = [
        r for r in all_records if record_idx[id(r)] not in assigned
    ]
    # Index unassigned by school
    by_school_unassigned: dict[str, list[StudentRecord]] = defaultdict(list)
    for r in unassigned_records:
        if r.school_normalized:
            by_school_unassigned[r.school_normalized].append(r)

    for school, school_group in by_school_unassigned.items():
        if len(school_group) < 2:
            continue
        # Pairwise comparison within same school
        used_in_phase2: set[int] = set()
        for i in range(len(school_group)):
            if i in used_in_phase2:
                continue
            cluster = [school_group[i]]
            for j in range(i + 1, len(school_group)):
                if j in used_in_phase2:
                    continue
                # Compare last names first (must be very similar)
                last_sim = jaro_winkler(
                    school_group[i].name_last.lower(),
                    school_group[j].name_last.lower()
                )
                if last_sim < 0.85:
                    continue
                # Then compare full normalized names
                full_sim = jaro_winkler(
                    school_group[i].name_normalized,
                    school_group[j].name_normalized
                )
                if full_sim > 0.9 and age_compatible(school_group[i], school_group[j]):
                    cluster.append(school_group[j])
                    used_in_phase2.add(j)

            if len(cluster) >= 2:
                indices = [record_idx[id(r)] for r in cluster]
                if any(idx in assigned for idx in indices):
                    continue
                ent = make_entity(cluster, 0.85, "fuzzy_name_school")
                if ent.confidence >= min_confidence:
                    entities.append(ent)
                for idx in indices:
                    assigned.add(idx)

    # ------- Phase 3: Same name + compatible age + city/state = 75% -------
    # Try to match remaining records across sources by name + geography
    unassigned_records = [
        r for r in all_records if record_idx[id(r)] not in assigned
    ]
    by_norm_unassigned: dict[str, list[StudentRecord]] = defaultdict(list)
    for r in unassigned_records:
        by_norm_unassigned[r.name_normalized].append(r)

    for norm_name, group in by_norm_unassigned.items():
        if len(group) < 2:
            continue
        # Check if they share city or state and are age-compatible
        sources = set(r.source for r in group)
        if len(sources) < 2:
            continue  # same source, not interesting for cross-source matching
        if all(age_compatible(group[0], r) for r in group[1:]):
            # Check geographic compatibility
            cities = set(
                r.city.lower() for r in group if r.city
            )
            all_bay_area = all(r.bay_area for r in group if r.bay_area is not None)
            if cities and len(cities) <= 2 or all_bay_area:
                indices = [record_idx[id(r)] for r in group]
                if any(i in assigned for i in indices):
                    continue
                ent = make_entity(group, 0.75, "name_geo_age")
                if ent.confidence >= min_confidence:
                    entities.append(ent)
                for i in indices:
                    assigned.add(i)

    # ------- Phase 4: Cross-competition MATHCOUNTS -> USAPhO via feeder -------
    # A student in MATHCOUNTS 8th grade in year X could be in USAPhO in year X+1 to X+6
    # Key insight: match by exact last+first name across sources, since these are
    # real public competition results with real names. School won't match because
    # middle school != high school, so we rely on name + Bay Area geography.

    mc_unassigned = [
        r for r in all_records
        if record_idx[id(r)] not in assigned and r.source == "mathcounts"
    ]
    usapho_unassigned = [
        r for r in all_records
        if record_idx[id(r)] not in assigned and r.source == "usapho"
    ]

    # Also try matching MATHCOUNTS students to already-resolved USAPhO entities
    usapho_entities = [e for e in entities if any(
        r.source == "usapho" for r in e.records
    )]

    for mc in mc_unassigned:
        # Try matching against unassigned USAPhO records
        best_match = None
        best_score = 0.0

        for up in usapho_unassigned:
            if record_idx[id(up)] in assigned:
                continue
            year_diff = up.year - mc.year
            if year_diff < 0 or year_diff > 6:
                continue

            # Name matching — compare last and first separately for higher precision
            last_sim = jaro_winkler(mc.name_last.lower(), up.name_last.lower())
            first_sim = jaro_winkler(mc.name_first.lower(), up.name_first.lower())
            full_sim = jaro_winkler(mc.name_normalized, up.name_normalized)

            # Require very strong name match (exact last name + close first name)
            if last_sim < 0.95 or first_sim < 0.85:
                continue

            # School compatibility (feeder or same K-12 school)
            school_ok = schools_compatible(mc, up)

            # Both Bay Area
            geo_ok = (mc.bay_area and up.bay_area)

            if last_sim == 1.0 and first_sim == 1.0 and school_ok:
                score = 0.95  # exact name + feeder school
            elif last_sim == 1.0 and first_sim == 1.0 and geo_ok:
                score = 0.85  # exact name + both Bay Area
            elif full_sim > 0.9 and school_ok:
                score = 0.85
            elif full_sim > 0.9 and geo_ok:
                score = 0.75
            elif last_sim == 1.0 and first_sim == 1.0:
                score = 0.70  # exact name, no geo confirmation
            else:
                continue

            if score > best_score:
                best_score = score
                best_match = up

        if best_match and best_score >= min_confidence:
            idx_mc = record_idx[id(mc)]
            idx_up = record_idx[id(best_match)]
            if idx_mc not in assigned and idx_up not in assigned:
                ent = make_entity(
                    [mc, best_match], best_score, "cross_competition"
                )
                entities.append(ent)
                assigned.add(idx_mc)
                assigned.add(idx_up)

    # Also try adding unassigned MATHCOUNTS records to existing USAPhO entities
    mc_still_unassigned = [
        r for r in all_records
        if record_idx[id(r)] not in assigned and r.source == "mathcounts"
    ]
    for mc in mc_still_unassigned:
        for ent in usapho_entities:
            # Compare against all records in entity, use best match
            best_name_sim = 0.0
            for er in ent.records:
                last_sim = jaro_winkler(mc.name_last.lower(), er.name_last.lower())
                first_sim = jaro_winkler(mc.name_first.lower(), er.name_first.lower())
                if last_sim >= 0.95 and first_sim >= 0.85:
                    best_name_sim = max(best_name_sim,
                                        (last_sim + first_sim) / 2)
            if best_name_sim < 0.9:
                continue
            # Check age compatibility
            if not any(age_compatible(mc, r) for r in ent.records):
                continue
            # Check school or geo compatibility
            school_ok = any(schools_compatible(mc, r) for r in ent.records)
            geo_ok = mc.bay_area and any(r.bay_area for r in ent.records)
            if school_ok or geo_ok:
                # Add to existing entity
                ent.records.append(mc)
                ent.achievements.append({
                    "year": mc.year,
                    "competition": mc.competition,
                    "result": mc.result,
                    "source": mc.source,
                    "detail": mc.detail,
                })
                ent.achievements.sort(key=lambda a: a["year"])
                if mc.school_raw not in ent.school_trajectory:
                    ent.school_trajectory.insert(0, mc.school_raw)
                ent.match_type += "+cross_competition"
                # Confidence based on match quality
                if school_ok:
                    ent.confidence = min(ent.confidence, 0.85)
                else:
                    ent.confidence = min(ent.confidence, 0.75)
                assigned.add(record_idx[id(mc)])
                break

    # Build single-record "trajectories" for remaining unassigned
    for r in all_records:
        idx = record_idx[id(r)]
        if idx not in assigned:
            ent = make_entity([r], 1.0, "single_record")
            ent.confidence = 1.0  # single record, no matching needed
            entities.append(ent)
            assigned.add(idx)

    return entities


# ---------------------------------------------------------------------------
# Cross-reference with placement DB
# ---------------------------------------------------------------------------
def enrich_with_school_context(entities: list[Trajectory]) -> None:
    """Add school-level placement context to each trajectory."""
    all_school_ids = set()
    for ent in entities:
        for r in ent.records:
            if r.school_normalized:
                all_school_ids.add(r.school_normalized)

    context = get_school_context(list(all_school_ids))

    for ent in entities:
        school_ids = [r.school_normalized for r in ent.records if r.school_normalized]
        if school_ids:
            # Use the most recent school
            latest = max(ent.records, key=lambda r: r.year)
            sid = latest.school_normalized
            if sid and sid in context:
                ent.school_context = context[sid]


# ---------------------------------------------------------------------------
# Output and summary
# ---------------------------------------------------------------------------
def print_summary(entities: list[Trajectory], all_records: list[StudentRecord]) -> None:
    """Print a summary of the entity resolution results."""
    multi = [e for e in entities if len(e.records) > 1]
    single = [e for e in entities if len(e.records) == 1]

    print("=" * 70)
    print("ENTITY RESOLUTION SUMMARY")
    print("=" * 70)
    print(f"\nInput records:  {len(all_records)}")
    print(f"  - MATHCOUNTS:      {sum(1 for r in all_records if r.source == 'mathcounts')}")
    print(f"  - USAPhO:          {sum(1 for r in all_records if r.source == 'usapho')}")
    print(f"  - Athlete commits: {sum(1 for r in all_records if r.source == 'athlete_commits')}")
    print(f"\nResolved entities: {len(entities)}")
    print(f"  - Multi-record matches: {len(multi)}")
    print(f"  - Single-record only:   {len(single)}")

    # Confidence distribution
    print("\nConfidence distribution (multi-record only):")
    conf_buckets = defaultdict(int)
    for e in multi:
        bucket = f"{int(e.confidence * 100)}%"
        conf_buckets[bucket] += 1
    for bucket in sorted(conf_buckets.keys(), reverse=True):
        print(f"  {bucket}: {conf_buckets[bucket]}")

    # Match types
    print("\nMatch types:")
    type_counts = defaultdict(int)
    for e in multi:
        type_counts[e.match_type] += 1
    for mt, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {mt}: {cnt}")

    # Schools represented
    print("\nSchools represented in multi-record matches:")
    school_counts = defaultdict(int)
    for e in multi:
        for school in set(r.school_normalized for r in e.records if r.school_normalized):
            school_counts[school] += 1
    for school, cnt in sorted(school_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {school}: {cnt} students")

    # Cross-competition matches
    cross = [e for e in multi if len(set(r.source for r in e.records)) > 1]
    print(f"\nCross-source matches: {cross_count(entities)}")

    # Most interesting trajectories
    print("\n" + "=" * 70)
    print("MOST INTERESTING TRAJECTORIES")
    print("=" * 70)

    # Sort by: number of records, then number of sources, then number of years spanned
    interesting = sorted(
        multi,
        key=lambda e: (
            len(set(r.source for r in e.records)),
            len(e.records),
            max(r.year for r in e.records) - min(r.year for r in e.records),
        ),
        reverse=True,
    )

    for ent in interesting[:20]:
        sources = set(r.source for r in ent.records)
        year_span = max(r.year for r in ent.records) - min(r.year for r in ent.records)
        print(f"\n  {ent.entity_id}: {ent.name} "
              f"(conf={ent.confidence:.0%}, type={ent.match_type})")
        print(f"    Schools: {' -> '.join(ent.school_trajectory)}")
        print(f"    Sources: {', '.join(sorted(sources))}, Span: {year_span} years")
        for ach in ent.achievements:
            detail = f" ({ach['detail']})" if ach.get('detail') else ""
            print(f"    {ach['year']} {ach['competition']}: {ach['result']}{detail}")
        if ent.school_context:
            ctx = ent.school_context
            ivy = ctx.get("ivy_plus_enrolled_total", "?")
            print(f"    School context: {ctx.get('school_name', '?')} — "
                  f"Ivy+ enrolled total: {ivy}")


def cross_count(entities: list[Trajectory]) -> int:
    return sum(
        1 for e in entities
        if len(e.records) > 1 and len(set(r.source for r in e.records)) > 1
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Entity resolution pipeline")
    parser.add_argument("--summary-only", action="store_true",
                        help="Print summary only, skip file output")
    parser.add_argument("--min-confidence", type=float, default=0.0,
                        help="Minimum confidence threshold for matches")
    args = parser.parse_args()

    print("Loading data sources...")
    mc_records = load_mathcounts()
    print(f"  MATHCOUNTS: {len(mc_records)} records")

    usapho_records = load_usapho()
    print(f"  USAPhO: {len(usapho_records)} records")

    athlete_records = load_athlete_commits()
    print(f"  Athlete commits: {len(athlete_records)} records")

    all_records = mc_records + usapho_records + athlete_records
    print(f"  Total: {len(all_records)} records")

    print("\nResolving entities...")
    entities = resolve_entities(all_records, min_confidence=args.min_confidence)

    print("Enriching with school context...")
    enrich_with_school_context(entities)

    print_summary(entities, all_records)

    if not args.summary_only:
        # Save multi-record trajectories (the interesting ones)
        multi = [e for e in entities if len(e.records) > 1]
        output = {
            "metadata": {
                "generated": "2026-04-18",
                "sources": ["mathcounts_ca_results.json", "california_students.json",
                            "college_placement.db (athlete_commits)"],
                "total_input_records": len(all_records),
                "total_entities": len(entities),
                "multi_record_entities": len(multi),
                "cross_source_matches": cross_count(entities),
            },
            "trajectories": [e.to_dict() for e in sorted(
                multi, key=lambda e: (-e.confidence, -len(e.records))
            )],
        }

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump(output, f, indent=2)
        print(f"\nSaved {len(multi)} trajectories to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
