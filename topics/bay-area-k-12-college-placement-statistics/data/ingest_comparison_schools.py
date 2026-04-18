#!/usr/bin/env python3
"""Ingest college placement data for comparison schools:
Castilleja, Menlo, Nueva, Crystal Springs Uplands, Pinewood.

Sources: school profile PDFs and web pages (see raw/school-profiles/).
Most profiles list colleges with matriculant counts but NOT applied/accepted.
We store metric='enrolled' with the published count.

Crystal Springs only publishes accept/matriculate lists without counts;
we store count=1 with a note.
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ingest_athletes import normalize_college

DB_PATH = Path(__file__).parent / "college_placement.db"

# ---------------------------------------------------------------------------
# CASTILLEJA — Class of 2025 (profile 2025-26)
# List of colleges; bold = matriculated by at least one student.
# No counts published — store 1 per college.
# ---------------------------------------------------------------------------

CASTILLEJA_2025_MATRICULATED = [
    "American University", "Bates College", "Boston College", "Boston University",
    "Brown University", "Cal Poly, San Luis Obispo", "Carleton College",
    "Carnegie Mellon University", "Case Western Reserve University", "Chapman University",
    "Colgate University", "Colorado College", "Cornell University", "Dartmouth College",
    "Duke University", "Emory University", "George Washington University",
    "Georgetown University", "Georgia Institute of Technology", "Grinnell College",
    "Hamilton College", "Harvard University", "Harvey Mudd College", "Haverford College",
    "Howard University", "Kenyon College", "Lehigh University",
    "Loyola Marymount University", "McGill University", "New York University",
    "Northeastern University", "Northwestern University", "Oberlin College",
    "Occidental College", "Princeton University", "Purdue University",
    "Rice University", "San Jose State University", "Santa Clara University",
    "Scripps College", "Stanford University", "Tufts University",
    "UC Berkeley", "UC Davis", "UC Irvine", "UC Los Angeles", "UC San Diego",
    "UC Santa Barbara", "University of British Columbia", "University of Chicago",
    "University of Colorado", "University of Michigan", "University of Notre Dame",
    "University of Oregon", "University of Pennsylvania", "University of Southern California",
    "University of Virginia", "University of Washington", "University of Wisconsin",
    "Vanderbilt University", "Washington University in St Louis", "Wesleyan University",
    "Yale University",
]

# Accepted-only colleges (appeared on list but NOT bold)
CASTILLEJA_2025_ACCEPTED_ONLY = [
    "Beloit College", "Brandeis University", "Cal Poly, Humboldt", "Cal Poly, Pomona",
    "Colorado School of Mines", "CSU Chico", "CSU Fullerton", "CSU Long Beach",
    "Denison University", "DePaul University", "Embry-Riddle Aeronautical University",
    "Indiana University, Bloomington", "Macalester College", "Marymount Manhattan College",
    "Michigan State University", "Muhlenberg College", "Oregon State University",
    "Pennsylvania State University", "Rensselaer Polytechnic Institute",
    "Rose-Hulman Institute of Technology", "San Diego State University",
    "San Francisco State University", "Skidmore College", "Sonoma State University",
    "St Olaf College", "UC Merced", "UC Riverside", "UC Santa Cruz",
    "United States Air Force Academy", "United States Naval Academy",
    "University of Arizona", "University of Connecticut", "University of Edinburgh",
    "University of Georgia", "University of Glasgow", "University of Hawaii",
    "University of Illinois", "University of Maryland", "University of Miami",
    "University of North Carolina", "University of Pittsburgh",
    "University of Puget Sound", "University of Richmond", "University of Rochester",
    "University of San Diego", "University of St Andrews", "University of Toronto",
    "University of Vermont", "Vassar College",
]

CASTILLEJA_2025_URL = "https://www.castilleja.org/uploaded/College_Counseling/Documents/CastillejaProfile.pdf"

# ---------------------------------------------------------------------------
# MENLO — Classes of 2023-2025 (profile 2025-26) — matriculation counts
# ---------------------------------------------------------------------------

MENLO_2023_2025 = [
    ("Amherst College", 2), ("Babson College", 1), ("Barnard College", 3),
    ("Bates College", 1), ("Baylor University", 1), ("Boston College", 12),
    ("Boston University", 7), ("Bowdoin College", 1), ("Brandeis University", 1),
    ("Brigham Young University", 1), ("Brown University", 4), ("Bryn Mawr College", 1),
    ("Bucknell University", 1), ("California Institute of Technology", 1),
    ("California Lutheran University", 1),
    ("California Polytechnic State University, San Luis Obispo", 2),
    ("California State University, Long Beach", 1), ("Carleton College", 2),
    ("Carnegie Mellon University", 5), ("Case Western Reserve University", 1),
    ("Chapman University", 7), ("Claremont McKenna College", 2), ("Colby College", 1),
    ("Colgate University", 3), ("College of San Mateo", 1), ("Colorado College", 6),
    ("Columbia University", 2), ("Connecticut College", 1), ("Cornell University", 9),
    ("Dartmouth College", 8), ("Davidson College", 1), ("De Anza College", 2),
    ("DePaul University", 1), ("Duke University", 7), ("Emory University", 2),
    ("Fashion Institute of Technology", 1), ("Foothill College", 1),
    ("George Washington University", 1), ("Georgetown University", 5),
    ("Georgia Institute of Technology", 1), ("Grinnell College", 1),
    ("Hamilton College", 1), ("Harvard University", 7), ("Johns Hopkins University", 3),
    ("Lehigh University", 8), ("Lewis & Clark College", 1),
    ("Loyola Marymount University", 4), ("Loyola University Chicago", 2),
    ("Massachusetts Institute of Technology", 3), ("Middlebury College", 2),
    ("New York University", 6), ("Northeastern University", 6),
    ("Northwestern University", 10), ("Occidental College", 3), ("Pitzer College", 1),
    ("Princeton University", 4), ("Purdue University", 2), ("Reed College", 1),
    ("Rice University", 4), ("Rutgers University", 1),
    ("Saint Mary's College of California", 1), ("San Francisco State University", 1),
    ("San Jose State University", 1), ("Santa Clara University", 4),
    ("Scripps College", 4), ("Skidmore College", 2),
    ("Southern Methodist University", 4), ("Stanford University", 30),
    ("Syracuse University", 3), ("Texas Christian University", 2),
    ("The University of Texas at Austin", 3), ("Trinity College", 1),
    ("Tufts University", 8), ("Tulane University of Louisiana", 11),
    ("Union College", 1), ("United States Military Academy at West Point", 2),
    ("University of British Columbia", 2), ("University of California, Berkeley", 20),
    ("University of California, Davis", 3), ("University of California, Irvine", 2),
    ("University of California, Los Angeles", 8), ("University of California, Merced", 5),
    ("University of California, Riverside", 1),
    ("University of California, San Diego", 1),
    ("University of California, Santa Barbara", 4),
    ("University of California, Santa Cruz", 5), ("University of Chicago", 17),
    ("University of Colorado Boulder", 5), ("University of Denver", 3),
    ("University of Hong Kong", 1),
    ("University of Illinois at Urbana-Champaign", 1), ("University of Miami", 3),
    ("University of Michigan", 10), ("University of North Carolina at Chapel Hill", 2),
    ("University of Notre Dame", 2), ("University of Pennsylvania", 4),
    ("University of Puget Sound", 1), ("University of Redlands", 1),
    ("University of Southern California", 10), ("University of St Andrews", 1),
    ("University of Toronto", 1), ("University of Utah", 1),
    ("University of Washington, Seattle", 7), ("University of Waterloo", 1),
    ("University of Wisconsin, Madison", 7), ("Vanderbilt University", 10),
    ("Vassar College", 1), ("Villanova University", 2), ("Wake Forest University", 5),
    ("Washington University in St. Louis", 11), ("Wellesley College", 6),
    ("Whitman College", 1), ("William & Mary", 1), ("Williams College", 4),
    ("Yale University", 3),
]

MENLO_2025_26_URL = "https://www.menloschool.org/live/files/4018-menlo-school-profile-2025-2026"

# Menlo Classes of 2021-2023 (profile 2023-24)
MENLO_2021_2023 = [
    ("American University", 1), ("Amherst College", 2),
    ("ArtCenter College of Design", 1), ("Babson College", 2), ("Bates College", 3),
    ("Baylor University", 2), ("Belmont College", 1), ("Boston College", 12),
    ("Boston University", 5), ("Bowdoin College", 2), ("Brigham Young University", 2),
    ("Brown University", 6), ("Bucknell University", 1),
    ("California Polytechnic State University, San Luis Obispo", 3),
    ("Canada College", 1), ("Carleton College", 1), ("Carnegie Mellon University", 4),
    ("Case Western Reserve University", 3), ("Claremont McKenna College", 4),
    ("Colby College", 2), ("Colgate University", 1), ("College of San Mateo", 2),
    ("Colorado College", 3), ("Columbia University", 4), ("Cornell University", 13),
    ("Dartmouth College", 7), ("Denison University", 3), ("Duke University", 7),
    ("Emerson College", 1), ("Emory University", 4), ("Foothill College", 2),
    ("Fordham University", 1), ("Georgetown University", 4), ("Gonzaga University", 3),
    ("Harvard University", 5), ("Haverford College", 1),
    ("Johns Hopkins University", 5), ("Lehigh University", 4),
    ("Marquette University", 2), ("Massachusetts Institute of Technology", 2),
    ("Middlebury College", 2), ("New York University", 3),
    ("Northeastern University", 1), ("Northern Arizona University", 1),
    ("Northwestern University", 6), ("Occidental College", 2), ("Pace University", 1),
    ("Parsons School of Design", 1), ("Pomona College", 2), ("Princeton University", 5),
    ("Purdue University", 5), ("Rensselaer Polytechnic Institute", 1),
    ("Rhode Island School of Design", 1), ("Rice University", 3),
    ("Rose-Hulman Institute of Technology", 1),
    ("Saint Mary's College of California", 2), ("Santa Clara University", 8),
    ("Santa Monica College", 2), ("Sarah Lawrence College", 2), ("Scripps College", 2),
    ("Seattle University", 1), ("Skidmore College", 3),
    ("Southern Methodist University", 5), ("Stanford University", 23),
    ("Syracuse University", 2), ("Texas Christian University", 2),
    ("The University of North Carolina at Chapel Hill", 2),
    ("The University of Notre Dame", 4), ("Trinity College", 2),
    ("Tufts University", 8), ("Tulane University", 13),
    ("United States Air Force Academy", 1), ("United States Military Academy", 1),
    ("University of Arizona", 2), ("University of British Columbia", 2),
    ("University of California, Berkeley", 18), ("University of California, Davis", 1),
    ("University of California, Los Angeles", 7),
    ("University of California, Riverside", 2),
    ("University of California, San Diego", 4),
    ("University of California, Santa Barbara", 3),
    ("University of Cambridge", 1), ("University of Chicago", 14),
    ("University of Cincinnati", 1), ("University of Colorado at Boulder", 6),
    ("University of Denver", 1), ("University of Maryland", 2),
    ("University of Michigan", 8), ("University of Oregon", 1),
    ("University of Pennsylvania", 7), ("University of Redlands", 1),
    ("University of Richmond", 2), ("University of Rochester", 1),
    ("University of San Diego", 1), ("University of Southern California", 2),
    ("University of St. Andrews", 1), ("University of Tennessee", 1),
    ("University of Texas, Austin", 2), ("University of Toronto", 1),
    ("University of Utah", 3), ("University of Virginia", 1),
    ("University of Washington", 4), ("University of Wisconsin, Madison", 12),
    ("Utah Valley University", 1), ("Vanderbilt University", 5), ("Vassar College", 2),
    ("Villanova University", 4), ("Wake Forest University", 7),
    ("Washington and Lee University", 1), ("Washington University in St. Louis", 11),
    ("Wellesley College", 3), ("Whitman College", 1), ("Williams College", 3),
    ("Yale University", 4),
]

# Menlo Classes of 2020-2022 (profile 2022-23)
MENLO_2020_2022 = [
    ("Amherst College", 2), ("ArtCenter College of Design", 1), ("Babson College", 1),
    ("Bates College", 4), ("Baylor University", 1), ("Belmont College", 1),
    ("Boston College", 8), ("Boston University", 3), ("Bowdoin College", 1),
    ("Brandeis University", 1), ("Brigham Young University", 2), ("Brown University", 7),
    ("Bucknell University", 2),
    ("California Polytechnic State University, San Luis Obispo", 5),
    ("Canada College", 1), ("Carleton College", 3), ("Carnegie Mellon University", 5),
    ("Case Western Reserve University", 3), ("Claremont McKenna College", 4),
    ("Colby College", 2), ("Colgate University", 1), ("College of San Mateo", 1),
    ("Colorado College", 2), ("Columbia University", 5), ("Cornell University", 10),
    ("Dartmouth College", 9), ("Davidson College", 2), ("Denison University", 3),
    ("Duke University", 12), ("Emerson College", 1), ("Emory University", 4),
    ("Foothill College", 1), ("Fordham University", 1),
    ("Franklin and Marshall College", 1), ("Georgetown University", 5),
    ("Gonzaga University", 2), ("Harvard University", 6), ("Harvey Mudd College", 1),
    ("Haverford College", 1), ("Indiana University", 1),
    ("Johns Hopkins University", 5), ("Lafayette College", 2), ("Lehigh University", 4),
    ("Marquette University", 2), ("Massachusetts Institute of Technology", 3),
    ("Middlebury College", 3), ("New York University", 5),
    ("Northeastern University", 1), ("Northern Arizona University", 1),
    ("Northwestern University", 10), ("Occidental College", 1), ("Pace University", 1),
    ("Parsons School of Design", 1), ("Pomona College", 6), ("Princeton University", 5),
    ("Purdue University", 6), ("Reed College", 1),
    ("Rensselaer Polytechnic Institute", 1), ("Rhode Island School of Design", 1),
    ("Rice University", 1), ("Rose-Hulman Institute of Technology", 1),
    ("Saint Mary's College of California", 1), ("San Diego Christian College", 1),
    ("Santa Clara University", 7), ("Santa Monica College", 2),
    ("Sarah Lawrence College", 2), ("Scripps College", 3), ("Seattle University", 1),
    ("Skidmore College", 2), ("Sonoma State University", 1),
    ("Southern Methodist University", 4), ("Stanford University", 23),
    ("Syracuse University", 1), ("Texas Christian University", 1),
    ("The University of North Carolina at Chapel Hill", 1),
    ("The University of Notre Dame", 6), ("Trinity College", 2),
    ("Tufts University", 6), ("Tulane University", 11),
    ("United States Air Force Academy", 1), ("United States Military Academy", 2),
    ("University of Arizona", 2), ("University of British Columbia", 1),
    ("University of California, Berkeley", 15), ("University of California, Davis", 2),
    ("University of California, Irvine", 1),
    ("University of California, Los Angeles", 11),
    ("University of California, Riverside", 4),
    ("University of California, San Diego", 3),
    ("University of California, Santa Barbara", 3),
    ("University of Cambridge", 1), ("University of Chicago", 10),
    ("University of Cincinnati", 1), ("University of Colorado at Boulder", 5),
    ("University of Denver", 1), ("University of Maryland", 2),
    ("University of Michigan", 11), ("University of Oregon", 1),
    ("University of Pennsylvania", 6), ("University of Redlands", 2),
    ("University of Richmond", 2), ("University of Rochester", 1),
    ("University of San Diego", 1), ("University of Southern California", 5),
    ("University of St. Andrews", 1), ("University of Tennessee", 1),
    ("University of Texas, Austin", 3), ("University of Toronto", 1),
    ("University of Utah", 3), ("University of Virginia", 3),
    ("University of Washington", 2), ("University of Wisconsin, Madison", 12),
    ("Utah Valley University", 1), ("Vanderbilt University", 5), ("Vassar College", 1),
    ("Villanova University", 4), ("Wake Forest University", 6),
    ("Washington and Lee University", 1), ("Washington University in St. Louis", 9),
    ("Wellesley College", 2), ("Whitman College", 1), ("Williams College", 3),
    ("Yale University", 5),
]

MENLO_2023_24_URL = "https://www.menloschool.org/live/files/3729-menlo-school-profile-2023-2024"
MENLO_2022_23_URL = "https://www.menloschool.org/live/files/3625-menlo-school-profile-2022-2023"

# ---------------------------------------------------------------------------
# NUEVA — Classes of 2021-2024 (profile 2024-25)
# Tiered: "10 or more", "5 or more", "1 or more" — no exact counts.
# We store the minimum of the range (10, 5, 1).
# ---------------------------------------------------------------------------

NUEVA_2021_2024_10_PLUS = [
    "Brown University", "Carnegie Mellon University", "Columbia University",
    "Cornell University", "Harvard University", "Northeastern University",
    "Northwestern University", "Princeton University", "Stanford University",
    "University of California, Berkeley", "University of Chicago",
    "University of Pennsylvania", "University of California, Los Angeles",
    "University of Illinois at Urbana-Champaign", "University of Michigan",
    "University of Southern California", "Washington University in St. Louis",
    "Wellesley College", "Yale University",
]

NUEVA_2021_2024_5_PLUS = [
    "Amherst College", "California Institute of Technology", "Carleton College",
    "Case Western Reserve University", "Dartmouth College", "Duke University",
    "Massachusetts Institute of Technology", "New York University",
    "Pomona College", "Rice University", "Tufts University",
]

NUEVA_2021_2024_1_PLUS = [
    "Barnard College", "Boston University", "Bowdoin College", "Brandeis University",
    "Bryn Mawr College", "California Institute of the Arts",
    "California Polytechnic State University, San Luis Obispo",
    "California State University, Long Beach", "Claremont McKenna College",
    "Colorado College", "Colorado School of Mines", "Connecticut College",
    "Drexel University", "Georgetown University", "Harvey Mudd College",
    "Haverford College", "Johns Hopkins University", "Lehigh University",
    "Loyola Marymount University", "Macalester College",
    "Maryland Institute College of Art", "Middlebury College", "Oberlin College",
    "Occidental College", "Olin College of Engineering",
    "Pacific Northwest College of Art at Willamette University",
    "Pitzer College", "Pratt Institute", "Purdue University",
    "Rhode Island School of Design", "Santa Clara University",
    "Sarah Lawrence College", "School of Visual Arts", "Scripps College",
    "Skidmore College", "Smith College", "Southern Methodist University",
    "St. John's College", "Swarthmore College",
    "The University of Texas at Austin", "United States Naval Academy",
    "University of British Columbia", "University of California, Davis",
    "University of California, Irvine", "University of California, Riverside",
    "University of California, San Diego", "University of California, Santa Cruz",
    "University of Miami", "University of North Carolina at Chapel Hill",
    "University of Oregon", "University of Oxford", "University of Rochester",
    "University of St Andrews", "University of Toronto", "University of Utah",
    "University of Vermont", "University of Wisconsin, Madison",
    "Vanderbilt University", "Vassar College", "Villanova University",
    "Vrije Universiteit Amsterdam", "Wesleyan University", "Whitman College",
    "Willamette University", "William & Mary", "Williams College",
    "Worcester Polytechnic Institute",
]

NUEVA_2024_25_URL = "https://resources.finalsite.net/images/v1766430328/nuevaschoolorg/tesjhsaqpweriklu4vrr/NuevaProfile2024-25FINAL.pdf"

# Nueva Classes of 2020-2023 (profile 2023-24) — same tier structure
NUEVA_2020_2023_10_PLUS = [
    "Carnegie Mellon University", "Columbia University", "Cornell University",
    "Harvard University", "Northeastern University", "Northwestern University",
    "Princeton University", "Stanford University",
    "University of California, Berkeley", "University of Chicago",
    "University of Pennsylvania", "University of Southern California",
]

NUEVA_2020_2023_5_PLUS = [
    "Brown University", "California Institute of Technology",
    "Case Western Reserve University", "Dartmouth College", "Duke University",
    "Harvey Mudd College", "Massachusetts Institute of Technology",
    "New York University", "Reed College", "Tufts University",
    "University of California, Los Angeles",
    "University of Illinois at Urbana-Champaign", "University of Michigan",
    "Washington University in St. Louis", "Wellesley College", "Yale University",
]

NUEVA_2020_2023_1_PLUS = [
    "American University", "Amherst College", "Barnard College",
    "Boston University", "Bowdoin College", "Brandeis University",
    "Bryn Mawr College", "California Institute of the Arts",
    "California Polytechnic State University, San Luis Obispo",
    "California State University, Long Beach", "Carleton College",
    "Claremont McKenna College", "Colorado College", "Colorado School of Mines",
    "Connecticut College", "Drexel University", "Georgetown University",
    "Georgia Institute of Technology", "Haverford College",
    "Johns Hopkins University", "Lehigh University", "Loyola Marymount University",
    "Macalester College", "Maryland Institute College of Art",
    "Middlebury College", "Oberlin College", "Occidental College",
    "Olin College of Engineering",
    "Pacific Northwest College of Art at Willamette University",
    "Pitzer College", "Pomona College", "Pratt Institute", "Purdue University",
    "Rhode Island School of Design", "Rice University", "Santa Clara University",
    "Sarah Lawrence College", "School of the Art Institute of Chicago",
    "School of Visual Arts", "Scripps College", "Skidmore College",
    "Smith College", "Southern Methodist University", "St. John's College",
    "Swarthmore College", "The University of Texas at Austin",
    "United States Naval Academy", "University of British Columbia",
    "University of California, Davis", "University of California, Irvine",
    "University of California, Riverside", "University of California, San Diego",
    "University of California, Santa Cruz", "University of Miami",
    "University of North Carolina at Chapel Hill", "University of Oregon",
    "University of Oxford", "University of Rochester", "University of St Andrews",
    "University of Toronto", "University of Utah", "University of Vermont",
    "University of Wisconsin, Madison", "Vanderbilt University",
    "Vassar College", "Villanova University", "Vrije Universiteit Amsterdam",
    "Wesleyan University", "Whitman College", "Willamette University",
    "William & Mary", "Williams College", "Worcester Polytechnic Institute",
]

NUEVA_2023_24_URL = "https://resources.finalsite.net/images/v1702412698/nuevaschoolorg/xaapknab9fyt6adrrl8n/23-24CollegeProfile.pdf"

# ---------------------------------------------------------------------------
# CRYSTAL SPRINGS UPLANDS — Classes of 2022-2025
# Only matriculated list (bold); no counts. Store count=1 per college.
# ---------------------------------------------------------------------------

CRYSTAL_2022_2025_MATRICULATED = [
    "American University", "Babson College", "Barnard College", "Bates College",
    "Boston College", "Brown University", "Bryn Mawr College",
    "Brigham Young University", "California State University, Monterey Bay",
    "Carleton College", "Carnegie Mellon University",
    "Case Western Reserve University", "Chapman University",
    "Claremont McKenna College", "Colgate University", "Colorado College",
    "Colorado State University", "Columbia University", "Cornell University",
    "Dartmouth College", "Duke University", "Emory University",
    "Fordham University", "Georgetown University", "Harvard University",
    "Harvey Mudd College", "Johns Hopkins University", "Lafayette College",
    "Lehigh University", "Loyola Marymount University", "Macalester College",
    "Massachusetts Institute of Technology", "McGill University",
    "Middlebury College", "Mount Saint Mary's University", "New York University",
    "Northeastern University", "Northwestern University", "Occidental College",
    "Ohio State University", "Otterbein University", "Pitzer College",
    "Pomona College", "Princeton University", "Purdue University", "Reed College",
    "Rensselaer Polytechnic Institute", "Rice University",
    "San Francisco State University", "San Jose State University",
    "Santa Clara University", "Scripps College", "Simon Fraser University",
    "Skyline College", "Smith College", "Southern Methodist University",
    "Stanford University", "Swarthmore College", "Syracuse University",
    "The New School", "The Pennsylvania State University", "Trinity College",
    "Tufts University", "Tulane University of Louisiana", "University of Arizona",
    "University of California, Berkeley", "University of California, Davis",
    "University of California, Irvine", "University of California, Los Angeles",
    "University of California, Merced", "University of California, San Diego",
    "University of California, Santa Barbara", "University of Chicago",
    "University of Colorado Boulder", "University of Connecticut",
    "University of Hawaii at Manoa", "University of Miami",
    "University of Michigan", "University of North Carolina at Chapel Hill",
    "University of Pennsylvania", "University of Richmond",
    "University of San Francisco", "University of Southern California",
    "University of St. Andrews", "University of Virginia",
    "University of Washington", "University of Wisconsin, Madison",
    "Vanderbilt University", "Vassar College",
    "Washington University in St. Louis", "Wellesley College",
    "Wesleyan University", "Western Washington University",
    "Williams College", "Yale University",
]

CRYSTAL_URL = "https://www.crystal.org/resources/academic-support/college-counseling"

# ---------------------------------------------------------------------------
# PINEWOOD — Classes of 2022-2025 (profile 2025-26)
# Bold = Class of 2025 matriculated; * = 2+ graduates across 4 years.
# No per-college counts. Store count=1 for all, note "2+ graduates" for starred.
# ---------------------------------------------------------------------------

PINEWOOD_2022_2025_MATRICULATED = [
    # All colleges listed as matriculated (bold = Class of 2025, plus non-bold = earlier years)
    "American University", "Arizona State University", "Art Center College of Design",
    "Bates College", "Boston College", "Boston University", "Bowdoin College",
    "Brigham Young University, Provo", "Brigham Young University, Idaho",
    "University of Brighton", "Brown University", "Bucknell University",
    "California Polytechnic State University, San Luis Obispo",
    "California State University, Chico", "California State University, Long Beach",
    "San Diego State University", "San Jose State University",
    "California State University, San Marcos",
    "University of California, Berkeley", "University of California, Irvine",
    "University of California, Los Angeles", "University of California, Merced",
    "University of California, Riverside", "University of California, San Diego",
    "University of California, Santa Barbara", "University of California, Santa Cruz",
    "Carnegie Mellon University", "Case Western Reserve University",
    "Chapman University", "University of Chicago", "Colby College",
    "College of San Mateo", "University of Colorado, Boulder",
    "Columbia University", "Cornell University",
    "Culinary Institute of America", "Dartmouth College", "Davidson College",
    "University of Denver", "Drexel University", "University of Edinburgh",
    "Emory University", "Foothill College", "Franklin University Switzerland",
    "The George Washington University", "Georgetown University",
    "Harvey Mudd College", "University of Hawaii, Hilo",
    "University of Illinois at Urbana-Champaign", "Indiana University, Bloomington",
    "Johns Hopkins University", "Lehigh University",
    "List College - Jewish Theological Seminary",
    "Loyola Marymount University", "Loyola University Chicago",
    "Miami University, Oxford", "University of Miami", "Montclair State University",
    "New York University", "University of North Carolina at Chapel Hill",
    "Northeastern University", "Northwestern University", "Occidental College",
    "Ohio University", "University of Oregon", "Pacific University",
    "Pennsylvania State University", "University of Pennsylvania",
    "Pepperdine University", "Pitzer College", "Pomona College",
    "University of Portland", "University of Portsmouth",
    "Providence College", "University of Puget Sound", "Purdue University",
    "University of Redlands", "Rice University", "University of Rochester",
    "Saint Mary's College of California", "University of San Diego",
    "Santa Clara University", "Sarah Lawrence College", "Smith College",
    "University of Southern California", "Southern Methodist University",
    "Southern Utah University", "Stanford University", "Swarthmore College",
    "Syracuse University", "Texas A&M University",
    "University of British Columbia", "University of Tennessee",
    "University of Toronto", "Trinity College", "Trinity College Dublin",
    "Tufts University", "Tulane University",
    "United States Military Academy", "Utah State University",
    "Vanderbilt University", "Villanova University",
    "University of Washington, Seattle", "Wheaton College",
    "Williams College", "University of Wisconsin, Madison",
    "Worcester Polytechnic Institute",
]

# Colleges with * (2+ graduates across Classes of 2022-2025)
PINEWOOD_2_PLUS = {
    "Arizona State University", "Boston University", "Brigham Young University, Provo",
    "Brown University", "California Polytechnic State University, San Luis Obispo",
    "Carnegie Mellon University", "Chapman University", "University of Chicago",
    "Colby College", "University of Colorado, Boulder", "Columbia University",
    "Cornell University", "Dartmouth College", "Davidson College",
    "University of Denver", "Emory University", "Foothill College",
    "The George Washington University", "Lehigh University",
    "Loyola Marymount University", "New York University", "Northeastern University",
    "Northwestern University", "University of Oregon", "University of Pennsylvania",
    "Pitzer College", "University of Puget Sound", "Purdue University",
    "University of Rochester", "Santa Clara University",
    "University of Southern California", "Southern Methodist University",
    "Southern Utah University", "Stanford University", "Syracuse University",
    "Tulane University", "University of Washington, Seattle",
    "Worcester Polytechnic Institute",
    # UC campuses with *
    "University of California, Berkeley", "University of California, Los Angeles",
    "University of California, Riverside", "University of California, San Diego",
}

PINEWOOD_2025_26_URL = "https://www.pinewood.edu/uploaded/New_Website_Page_Elements/Admissions/Updated_Materials/PWSchoolProfile_25-26.pdf"
PINEWOOD_2024_25_URL = "https://www.pinewood.edu/uploaded/New_Website_Page_Elements/Admissions/Updated_Materials/PWSchoolProfile_24-25.pdf"


def insert_placements_with_count(db, school_id, data, grad_year_label, source_url,
                                  metric="enrolled", notes_base=None):
    """Insert (college, count) tuples."""
    total = 0
    for college, count in data:
        cn = normalize_college(college)
        notes = notes_base
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (school_id, grad_year_label, college, cn, metric, count,
             "school_profile_pdf", source_url, "L1", notes),
        )
        total += 1
    return total


def insert_placements_list(db, school_id, colleges, grad_year_label, source_url,
                            metric="enrolled", count=1, notes=None):
    """Insert a list of college names with a fixed count (default 1)."""
    total = 0
    for college in colleges:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (school_id, grad_year_label, college, cn, metric, count,
             "school_profile_pdf", source_url, "L1", notes),
        )
        total += 1
    return total


def main():
    db = sqlite3.connect(DB_PATH)
    total = 0

    # -----------------------------------------------------------------------
    # CASTILLEJA — Class of 2025
    # -----------------------------------------------------------------------
    print("--- Castilleja ---")
    n = insert_placements_list(
        db, "castilleja", CASTILLEJA_2025_MATRICULATED, 2025,
        CASTILLEJA_2025_URL, metric="enrolled", count=1,
        notes="count not published, minimum 1 confirmed (bold = matriculated)",
    )
    # Also store accepted-only colleges
    n += insert_placements_list(
        db, "castilleja", CASTILLEJA_2025_ACCEPTED_ONLY, 2025,
        CASTILLEJA_2025_URL, metric="accepted", count=1,
        notes="count not published, minimum 1 accepted (not bold = accepted only)",
    )
    print(f"  Class of 2025: {n} records")
    total += n

    # School profile metadata
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, mean_gpa_weighted,
         mean_gpa_unweighted, college_going_rate_4yr, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("castilleja", "2025-26", 51, 4.14, 3.96, 97.0, CASTILLEJA_2025_URL),
    )

    # -----------------------------------------------------------------------
    # MENLO — three profile windows
    # -----------------------------------------------------------------------
    print("--- Menlo ---")
    # Classes of 2023-2025 (profile 2025-26) — use grad_year=2025 as latest
    n = insert_placements_with_count(
        db, "menlo", MENLO_2023_2025, 2025, MENLO_2025_26_URL,
        notes_base="3-year aggregate (Classes 2023-2025)",
    )
    print(f"  Classes of 2023-2025: {n} records")
    total += n

    # Classes of 2021-2023 (profile 2023-24) — use grad_year=2023
    n = insert_placements_with_count(
        db, "menlo", MENLO_2021_2023, 2023, MENLO_2023_24_URL,
        notes_base="3-year aggregate (Classes 2021-2023)",
    )
    print(f"  Classes of 2021-2023: {n} records")
    total += n

    # Classes of 2020-2022 (profile 2022-23) — use grad_year=2022
    n = insert_placements_with_count(
        db, "menlo", MENLO_2020_2022, 2022, MENLO_2022_23_URL,
        notes_base="3-year aggregate (Classes 2020-2022)",
    )
    print(f"  Classes of 2020-2022: {n} records")
    total += n

    # School profiles
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, total_enrollment,
         mean_gpa_weighted, national_merit_semifinalists, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("menlo", "2025-26", 143, 602, 3.83, 5, MENLO_2025_26_URL),
    )
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, total_enrollment,
         mean_gpa_weighted, national_merit_semifinalists, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("menlo", "2023-24", 146, 584, 3.82, 12, MENLO_2023_24_URL),
    )

    # -----------------------------------------------------------------------
    # NUEVA — two profile windows
    # -----------------------------------------------------------------------
    print("--- Nueva ---")
    # Classes of 2021-2024 (profile 2024-25)
    n = 0
    for college in NUEVA_2021_2024_10_PLUS:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("nueva", 2024, college, cn, "enrolled", 10,
             "school_profile_pdf", NUEVA_2024_25_URL, "L1",
             "4-year aggregate (Classes 2021-2024); tier '10 or more', minimum count stored"),
        )
        n += 1
    for college in NUEVA_2021_2024_5_PLUS:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("nueva", 2024, college, cn, "enrolled", 5,
             "school_profile_pdf", NUEVA_2024_25_URL, "L1",
             "4-year aggregate (Classes 2021-2024); tier '5 or more', minimum count stored"),
        )
        n += 1
    for college in NUEVA_2021_2024_1_PLUS:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("nueva", 2024, college, cn, "enrolled", 1,
             "school_profile_pdf", NUEVA_2024_25_URL, "L1",
             "4-year aggregate (Classes 2021-2024); tier '1 or more', minimum count stored"),
        )
        n += 1
    print(f"  Classes of 2021-2024: {n} records")
    total += n

    # Classes of 2020-2023 (profile 2023-24)
    n = 0
    for college in NUEVA_2020_2023_10_PLUS:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("nueva", 2023, college, cn, "enrolled", 10,
             "school_profile_pdf", NUEVA_2023_24_URL, "L1",
             "4-year aggregate (Classes 2020-2023); tier '10 or more', minimum count stored"),
        )
        n += 1
    for college in NUEVA_2020_2023_5_PLUS:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("nueva", 2023, college, cn, "enrolled", 5,
             "school_profile_pdf", NUEVA_2023_24_URL, "L1",
             "4-year aggregate (Classes 2020-2023); tier '5 or more', minimum count stored"),
        )
        n += 1
    for college in NUEVA_2020_2023_1_PLUS:
        cn = normalize_college(college)
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("nueva", 2023, college, cn, "enrolled", 1,
             "school_profile_pdf", NUEVA_2023_24_URL, "L1",
             "4-year aggregate (Classes 2020-2023); tier '1 or more', minimum count stored"),
        )
        n += 1
    print(f"  Classes of 2020-2023: {n} records")
    total += n

    # School profiles
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, total_enrollment,
         national_merit_semifinalists, college_going_rate_4yr,
         mean_sat, mean_act, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("nueva", "2024-25", 108, 450, 19, 100.0, 1510, 34, NUEVA_2024_25_URL),
    )
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, total_enrollment,
         national_merit_semifinalists, college_going_rate_4yr,
         mean_sat, mean_act, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("nueva", "2023-24", 112, 450, 25, 100.0, 1510, 33, NUEVA_2023_24_URL),
    )

    # -----------------------------------------------------------------------
    # CRYSTAL SPRINGS — Classes of 2022-2025
    # -----------------------------------------------------------------------
    print("--- Crystal Springs ---")
    n = insert_placements_list(
        db, "crystal-springs", CRYSTAL_2022_2025_MATRICULATED, 2025,
        CRYSTAL_URL, metric="enrolled", count=1,
        notes="count not published, minimum 1 confirmed; 4-year aggregate (Classes 2022-2025)",
    )
    print(f"  Classes of 2022-2025: {n} records")
    total += n

    # School profile — limited data available
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size, source_url)
        VALUES (?, ?, ?, ?)""",
        ("crystal-springs", "2024-25", 90, CRYSTAL_URL),  # ~30 per counselor x 3
    )

    # -----------------------------------------------------------------------
    # PINEWOOD — Classes of 2022-2025 (profile 2025-26)
    # -----------------------------------------------------------------------
    print("--- Pinewood ---")
    n = 0
    for college in PINEWOOD_2022_2025_MATRICULATED:
        cn = normalize_college(college)
        count = 2 if college in PINEWOOD_2_PLUS else 1
        notes = "4-year aggregate (Classes 2022-2025); "
        if count >= 2:
            notes += "2+ graduates confirmed (*)"
        else:
            notes += "count not published, minimum 1 confirmed"
        db.execute(
            """INSERT OR REPLACE INTO placements
            (school_id, grad_year, college, college_normalized, metric, count,
             source, source_url, confidence, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            ("pinewood", 2025, college, cn, "enrolled", count,
             "school_profile_pdf", PINEWOOD_2025_26_URL, "L1", notes),
        )
        n += 1
    print(f"  Classes of 2022-2025: {n} records")
    total += n

    # School profiles
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size,
         national_merit_semifinalists, ap_courses_offered,
         mean_gpa_weighted, mean_gpa_unweighted, college_going_rate_4yr, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("pinewood", "2025-26", 44, 4, 17, 4.093, 3.749, 100.0,
         PINEWOOD_2025_26_URL),
    )
    db.execute(
        """INSERT OR REPLACE INTO school_profiles
        (school_id, academic_year, grad_class_size,
         national_merit_semifinalists, ap_courses_offered,
         mean_gpa_weighted, mean_gpa_unweighted, college_going_rate_4yr, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        ("pinewood", "2024-25", 54, 2, 17, 3.945, 3.684, 100.0,
         PINEWOOD_2024_25_URL),
    )

    # -----------------------------------------------------------------------
    # Register sources
    # -----------------------------------------------------------------------
    sources = [
        ("castilleja", "school_profile_pdf", CASTILLEJA_2025_URL, "2025-26"),
        ("menlo", "school_profile_pdf", MENLO_2025_26_URL, "2025-26"),
        ("menlo", "school_profile_pdf", MENLO_2023_24_URL, "2023-24"),
        ("menlo", "school_profile_pdf", MENLO_2022_23_URL, "2022-23"),
        ("nueva", "school_profile_pdf", NUEVA_2024_25_URL, "2024-25"),
        ("nueva", "school_profile_pdf", NUEVA_2023_24_URL, "2023-24"),
        ("crystal-springs", "school_website", CRYSTAL_URL, "2022-2025"),
        ("pinewood", "school_profile_pdf", PINEWOOD_2025_26_URL, "2025-26"),
        ("pinewood", "school_profile_pdf", PINEWOOD_2024_25_URL, "2024-25"),
    ]
    for school_id, stype, url, years in sources:
        db.execute(
            """INSERT OR IGNORE INTO sources
            (school_id, source_type, url, years_covered, status, ingested_date)
            VALUES (?, ?, ?, ?, 'ingested', date('now'))""",
            (school_id, stype, url, years),
        )

    db.commit()
    print(f"\n=== Total: {total} placement records inserted ===")
    db.close()


if __name__ == "__main__":
    main()
