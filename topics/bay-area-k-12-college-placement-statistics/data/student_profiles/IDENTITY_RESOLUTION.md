# Identity Resolution & Trajectory Matching — Design Doc

## The Problem

We have trajectory fragments across dozens of domain-specific silos:

```
Swimming DB:    "Emily Chen, age 8, PASA club, 50m free 38.2s"
Chess DB:       "Emily Chen, USCF #12345, rating 1200, age 9"
MATHCOUNTS:     "E. Chen, Harker School, San Jose, 8th grade, score 34"
AMC 8:          AoPS user "mathgirl2015", grade 7, score 22
Reddit:         "Asian female, Bay Area private school, 1560 SAT, AIME qualifier"
YouTube:        "I'm Emily, I went to Harker, and here's how I got into MIT"
School DB:      "Harker sent 12 students to MIT in 2023-2025"
```

**Question: How do we link these fragments to build complete K-12 trajectories?**

## Three Matching Strategies

### Strategy 1: Named Entity Resolution (when names are available)

**Sources with real names:**
- MATHCOUNTS state results (name + school + grade)
- USAMO/USAJMO qualifier lists (name + school + state)
- USAPhO medal lists (name + school)
- Regeneron STS scholars (name + school + project)
- Spelling Bee participants (name + school + grade + year)
- USA Swimming (name + club + age + times)
- USCF chess (name + rating + age + club)
- YouTube (self-identified in video)
- School athlete commit pages (name + sport + college)

**Matching algorithm:**

```python
def match_student(name, school=None, state=None, year=None, grade=None):
    """
    Find all records across silos that likely belong to the same student.
    
    Matching confidence levels:
    - EXACT: same name + same school + same year → 95%+ confidence
    - STRONG: same name + same city/state + compatible age → 80%+
    - PROBABLE: similar name + same school type + same region → 60%+
    - WEAK: same first name + same demographic + similar stats → <50%
    """
    
    candidates = []
    
    # Search each silo
    for silo in [mathcounts, usamo, usapho, sts, swimming, chess, athlete_commits]:
        matches = silo.search(
            name=fuzzy_match(name),  # handle "Emily Chen" vs "E. Chen" vs "Emily C."
            school=school,
            year_range=(year-2, year+2),  # allow for grade uncertainty
            state=state
        )
        candidates.extend(matches)
    
    # Score each candidate pair
    for c in candidates:
        c.confidence = compute_confidence(
            name_similarity=jaro_winkler(name, c.name),
            school_match=c.school == school,
            age_compatible=abs(c.year - year) <= 2,
            state_match=c.state == state,
        )
    
    return sorted(candidates, key=lambda c: c.confidence, reverse=True)
```

**Key challenges:**
- Name variants: "Emily Chen" vs "E. Chen" vs "Emily S. Chen"
- Common names: "Emily Chen" in Bay Area is NOT unique — need school + age to disambiguate
- School changes: student at Menlo in 8th grade, transfers to Harker for 9th
- Privacy: we're linking public records, but the composite profile is more revealing than any single source

**Verification signals:**
- **Age consistency**: if MATHCOUNTS says grade 8 in 2023 and USAMO says grade 11 in 2026, that's consistent (3 years apart)
- **School consistency**: same school across multiple competition years
- **Performance trajectory**: AMC 8 score → AMC 10 score should show reasonable progression
- **Geographic consistency**: same city/state across sources

### Strategy 2: School-Level Aggregate Matching (no individual names needed)

When we CAN'T identify individuals, we can still build powerful insights at the school level:

```sql
-- "Harker produces X MATHCOUNTS qualifiers AND sends Y to MIT"
-- No individual linkage needed — just school-level correlation

CREATE VIEW v_school_competition_to_college AS
SELECT 
    s.school_id,
    s.name,
    -- Competition strength (from competition DBs)
    mc.mathcounts_qualifiers,
    so.scioly_state_appearances,
    -- College outcomes (from placement DB)
    p.ivy_plus_enrolled,
    p.stanford_enrolled,
    p.mit_enrolled
FROM schools s
LEFT JOIN (
    SELECT school, COUNT(*) as mathcounts_qualifiers
    FROM mathcounts_results 
    WHERE level = 'state' GROUP BY school
) mc ON mc.school = s.name
LEFT JOIN (
    SELECT school, COUNT(DISTINCT year) as scioly_state_appearances
    FROM scioly_results 
    WHERE level = 'state' GROUP BY school
) so ON so.school = s.name
LEFT JOIN (
    SELECT school_id, SUM(count) as ivy_plus_enrolled, ...
    FROM placements WHERE metric='enrolled' ...
) p ON p.school_id = s.school_id;
```

This answers questions like:
- "Schools with 5+ MATHCOUNTS state qualifiers send X% to MIT" 
- "Is there a correlation between Science Olympiad strength and Ivy+ placement?"
- "Harker dominates MATHCOUNTS but barely does Sci Oly — does that matter?"

**No privacy concerns. No identity resolution needed. Just school-level joins.**

### Strategy 3: Archetype Construction (anonymous profiles)

For anonymous sources (Reddit, some YouTube), we can't link to named competition results. Instead, we build **trajectory archetypes** — composite profiles representing common development paths:

```yaml
archetype: "STEM-Strong Asian Female, Bay Area Private"
sources: 21 Reddit profiles + 3 YouTube + school aggregate data
typical_trajectory:
  K-2:
    math: "2+ years ahead, Beast Academy or RSM"
    activities: "swimming, piano, 2-3 sports"
    reading: "above grade level"
  3-5:
    math: "Math Kangaroo, possibly AMC 8 early"
    activities: "narrowing sports to 1-2, adding coding"
    competitions: "first math competition (Kangaroo or MOEMS)"
  6-8:
    math: "MATHCOUNTS, AMC 8 score 20+, AMC 10 attempt"
    activities: "1 sport, 1 instrument, 1 STEM club"
    competitions: "MATHCOUNTS state qualifier, AMC 10 qualifier for AIME"
  9-12:
    math: "AIME qualifier, possibly USAMO"
    research: "summer program (RSI/PROMYS/etc)"
    testing: "SAT 1550+, 10+ APs"
    outcomes:
      tier1: "Stanford/MIT/Caltech (if USAMO level)"
      tier2: "Duke/Dartmouth/Northwestern/Cornell (if AIME level)"
      tier3: "UC Berkeley/UCLA/CMU/Rice (if AMC distinguished honor roll)"
confidence: 0.6  # archetype, not individual
data_points: 24
```

This is what private counselors actually sell — pattern recognition across hundreds of cases. We're building it from data.

## The Matching Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Raw Data    │────▶│   Extract    │────▶│   Resolve    │────▶│   Profile    │
│  per Silo    │     │   + Normalize│     │   Identity   │     │   Store      │
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                      │
                                              ┌───────────────────────┤
                                              ▼                       ▼
                                     ┌──────────────┐     ┌──────────────┐
                                     │  Individual   │     │  Archetype   │
                                     │  Trajectories │     │  Patterns    │
                                     │  (named,high  │     │  (anonymous, │
                                     │   confidence) │     │   aggregate) │
                                     └──────────────┘     └──────────────┘
```

### Step 1: Extract + Normalize (per silo)

Each data source gets its own extractor that produces a common record format:

```json
{
  "source": "mathcounts_ca_2024",
  "record_type": "competition_result",
  "student": {
    "name": "Emily Chen",           // null if anonymous
    "name_normalized": "chen_emily", // for matching
    "school": "The Harker School",
    "school_normalized": "harker",   // maps to our school DB
    "grade": 8,
    "year": 2024,
    "state": "CA",
    "city": "San Jose"
  },
  "achievement": {
    "competition": "MATHCOUNTS",
    "level": "state",
    "score": 34,
    "rank": 12,
    "qualified_for_next": true
  }
}
```

### Step 2: Identity Resolution

```python
def resolve_identities(records: list) -> list[StudentEntity]:
    """
    Group records that likely belong to the same student.
    
    Returns a list of StudentEntity objects, each containing
    all records attributed to that student with confidence scores.
    """
    entities = []
    
    # Phase 1: Exact matches (same name + same school)
    # Group by normalized name + school
    groups = defaultdict(list)
    for r in records:
        if r.student.name:
            key = (r.student.name_normalized, r.student.school_normalized)
            groups[key].append(r)
    
    for key, group in groups.items():
        if len(group) >= 2:
            # Verify age consistency
            if age_consistent(group):
                entities.append(StudentEntity(
                    records=group,
                    confidence=0.95,
                    match_type="exact_name_school"
                ))
    
    # Phase 2: Cross-source matching
    # For each named entity, search for matching records in other silos
    for entity in entities:
        name = entity.primary_name
        school = entity.primary_school
        year_range = entity.year_range
        
        # Search swimming DB
        swim_matches = swimming_db.search(name=name, club_area="bay_area", 
                                          birth_year_range=year_range)
        for m in swim_matches:
            if jaro_winkler(name, m.name) > 0.9:
                entity.add_record(m, confidence=0.8)
        
        # Search chess DB
        chess_matches = chess_db.search(name=name, state="CA")
        # ... etc
    
    # Phase 3: Anonymous profile matching
    # For Reddit/YouTube profiles without names, try to match to entities
    for r in anonymous_records:
        if r.student.school_normalized:
            # Find entities at the same school + same year
            candidates = [e for e in entities 
                         if e.primary_school == r.student.school_normalized
                         and e.overlaps_years(r)]
            # Score based on stat similarity
            for c in candidates:
                similarity = compare_stats(c, r)  # GPA, SAT, activities
                if similarity > 0.8:
                    c.add_record(r, confidence=similarity * 0.7)
    
    return entities
```

### Step 3: Verification

Each resolved entity gets a verification score based on:

```python
def verify_trajectory(entity: StudentEntity) -> VerificationReport:
    checks = []
    
    # 1. Age/grade consistency
    # All records should be consistent with a single birth year
    grades_years = [(r.grade, r.year) for r in entity.records if r.grade]
    if grades_years:
        birth_year_estimates = [year - grade - 5 for grade, year in grades_years]
        spread = max(birth_year_estimates) - min(birth_year_estimates)
        checks.append(("age_consistency", spread <= 1))
    
    # 2. School consistency
    # Same school across records (or known transfer pattern)
    schools = set(r.school for r in entity.records if r.school)
    checks.append(("school_consistency", len(schools) <= 2))
    
    # 3. Performance trajectory plausibility
    # Scores should generally improve over time (not decrease dramatically)
    math_scores = sorted([(r.year, r.score) for r in entity.records 
                          if r.competition in ('AMC8', 'AMC10', 'AMC12')], 
                         key=lambda x: x[0])
    if len(math_scores) >= 2:
        regression_ok = not any(
            s2 < s1 * 0.5  # score shouldn't halve year-over-year
            for (y1, s1), (y2, s2) in zip(math_scores, math_scores[1:])
        )
        checks.append(("performance_plausible", regression_ok))
    
    # 4. Cross-source consistency
    # If Reddit says "1560 SAT" and YouTube says "1580 SAT", that's suspicious
    sat_values = [r.sat for r in entity.records if r.sat]
    if len(sat_values) >= 2:
        checks.append(("sat_consistent", max(sat_values) - min(sat_values) <= 40))
    
    # 5. Final verification: does this trajectory lead to a plausible outcome?
    # An AIME qualifier from Harker going to MIT is plausible
    # An AIME qualifier from Harker going to community college is suspicious (verify)
    
    return VerificationReport(
        entity_id=entity.id,
        checks=checks,
        overall_confidence=entity.confidence * (sum(1 for _, ok in checks if ok) / len(checks)),
        flags=[name for name, ok in checks if not ok]
    )
```

## The Three Output Types

### 1. Individual Verified Trajectory (highest value, smallest volume)

Named students with high-confidence cross-source matches:

```yaml
student_id: "trajectory_0042"
confidence: 0.92
name: "Emily Chen"  # or anonymized
school_trajectory:
  - school: "harker"
    grades: "K-8"
    years: "2016-2024"
  
academic_trajectory:
  - year: 2021, grade: 6, event: "Math Kangaroo, Gold"
  - year: 2022, grade: 7, event: "MATHCOUNTS Chapter, 5th place"
  - year: 2022, grade: 7, event: "AMC 8, score 22"
  - year: 2023, grade: 8, event: "MATHCOUNTS State, 12th place"
  - year: 2023, grade: 8, event: "AMC 10, score 108"
  - year: 2024, grade: 9, event: "AMC 10, score 132, AIME qualified"
  - year: 2024, grade: 9, event: "AIME I, score 7"
  - year: 2025, grade: 10, event: "AMC 12, score 138"
  - year: 2025, grade: 10, event: "AIME I, score 10"
  - year: 2026, grade: 11, event: "USAMO qualifier"

extracurricular_trajectory:
  - activity: "swimming", years: "2017-2022", level: "club (PASA)", note: "dropped after 7th grade"
  - activity: "piano", years: "2015-2026", level: "CM Level 10 by 8th grade"
  - activity: "Science Olympiad", years: "2023-2026", level: "state team"

outcome:
  college: "MIT"
  round: "RA"
  year: 2027

sources:
  - mathcounts_ca_2023 (name + school + score)
  - aops_amc_thread_2024 (username, linked by school hint)
  - usamo_2026_qualifier_list (name + school)
  - reddit_collegeresults (self-reported, matched by school + stats)
```

### 2. School-Level Trajectory Patterns (medium value, large volume)

```yaml
school: "harker"
trajectory_pattern:
  math_competition_strength:
    mathcounts_state_qualifiers_per_year: 4-6
    aime_qualifiers_per_year: 12-18 (estimated from RSM/AoPS community)
    usamo_qualifiers_5yr: 3-5
  science_competition_strength:
    scioly: "minimal (2 appearances in DB)"
    regeneron_sts_semifinalists_5yr: 2-4
  college_outcomes:
    stanford_per_year: ~11
    mit_per_year: ~4
    ivy_plus_per_year: ~46
  
  implied_trajectory:
    "A typical Harker AIME qualifier: starts RSM/AoPS by 4th grade,
     AMC 8 by 6th grade (score 20+), MATHCOUNTS state by 7th-8th,
     AMC 10 AIME qualifier by 9th-10th. ~30% of AIME qualifiers
     from Harker end up at HYPSM."
```

### 3. Archetype Trajectories (broadest applicability, lowest individual accuracy)

Built from clustering anonymous profiles + school-level patterns + competition statistics. These become the core of the guidebook's "what to expect" advice.

## Privacy Framework

| Data Type | Named? | How We Use It | Storage |
|-----------|--------|--------------|---------|
| Competition results (public PDFs) | Yes | Cross-reference, school aggregates | Raw + normalized |
| Reddit/YouTube (self-published) | Usually no | Profile extraction, archetype building | Anonymized |
| Swimming/chess times (public DBs) | Yes | Trajectory curves, school patterns | Aggregated only |
| LinkedIn (public profiles) | Yes | **DO NOT scrape** — legal/ethical risk too high | Do not store |
| School placement (official) | No | School-level aggregates | As-is |

**Rule: We never publish individual named trajectories.** All individual-level output is anonymized or aggregated. Named data is used only for identity resolution (internal matching), not for publication.

## Implementation Priority

1. **School-level competition joins** (no identity resolution needed) — connect Duosmium + MATHCOUNTS to school placement DB
2. **Named competition result extraction** — MATHCOUNTS PDFs, USAPhO PDFs, USAMO lists
3. **Cross-competition matching** — same name + same school across MATHCOUNTS → AMC → USAMO
4. **Reddit/YouTube enhanced extraction** — mine grade-level timing from existing profiles
5. **Archetype clustering** — group similar profiles into trajectory patterns
6. **Individual trajectory assembly** — high-confidence named matches only
