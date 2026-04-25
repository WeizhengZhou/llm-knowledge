# Operation Log

## [2026-04-25] init | Topic initialized

- Topic: how to raise kid to be good at Squash in Bay Area
- Context: none

## [2026-04-24] wiki-compiler-agent | Full compile run

2026-04-24T23:45:00Z | wiki-compiler-agent | Compiled 16 articles from 45 raw sources.
  Gate status: CLEAR. L5 claims: 0. Disputed claims: 1 (d001 — varsity program count).
  Articles (all in staging/):
    staging/entities/squash-zone.md (L1)
    staging/entities/hisa-squash-academy.md (L2)
    staging/entities/altius-performance-squash.md (L2)
    staging/entities/squashdrive.md (L1)
    staging/entities/norcal-squash.md (L1)
    staging/entities/bay-club-squash.md (L1)
    staging/entities/oakwood-athletic-club.md (L2)
    staging/guides/getting-started.md (L2)
    staging/guides/choosing-club-coach.md (L1)
    staging/guides/tournament-rankings.md (L1)
    staging/guides/costs-and-commitment.md (L2)
    staging/guides/development-pathway.md (L2)
    staging/guides/college-squash-recruiting.md (L2)
    staging/guides/injury-prevention.md (L1)
    staging/concepts/squash-vs-tennis.md (L2)
    staging/concepts/national-squash-academy.md (L1)
  Reader outcomes covered: RO1 (getting-started, squash-vs-tennis), RO2 (choosing-club-coach, all entities),
    RO3 (costs-and-commitment), RO4 (tournament-rankings, norcal-squash), RO5 (development-pathway, injury-prevention),
    RO6 (college-squash-recruiting).
  Next recommended: wiki-critic-agent review of staging articles, then lint-agent.

## [2026-04-24] wiki-compiler-agent | Revision + Graduation

2026-04-24T23:55:00Z | wiki-compiler-agent | Revised 9 NEEDS-REVISION articles, graduated all 16 to wiki/.
  Revisions: Common Mistakes added to all 9 articles. HISA Junior Development expanded. Oakwood junior programs clarified, EBCSL scope drift removed. Choosing-club-coach and injury-prevention Common Mistakes added.
  Graduated: 16 articles (7 entities, 7 guides, 2 concepts) from staging/ to wiki/.
  Gate status: CLEAR. L5 claims: 0.
  Articles:
    wiki/entities/squash-zone.md (L1)
    wiki/entities/hisa-squash-academy.md (L2)
    wiki/entities/altius-performance-squash.md (L2)
    wiki/entities/squashdrive.md (L1)
    wiki/entities/norcal-squash.md (L1)
    wiki/entities/bay-club-squash.md (L1)
    wiki/entities/oakwood-athletic-club.md (L2)
    wiki/guides/getting-started.md (L2)
    wiki/guides/choosing-club-coach.md (L1)
    wiki/guides/tournament-rankings.md (L1)
    wiki/guides/costs-and-commitment.md (L2)
    wiki/guides/development-pathway.md (L2)
    wiki/guides/college-squash-recruiting.md (L2)
    wiki/guides/injury-prevention.md (L1)
    wiki/concepts/squash-vs-tennis.md (L2)
    wiki/concepts/national-squash-academy.md (L1)
  Next recommended: lint-agent run to check structural integrity.
