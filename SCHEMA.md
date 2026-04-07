# Wiki Schema

Conventions and standards for all wiki articles in this knowledge base.

## Article Frontmatter (Required Fields)

```yaml
---
title: "Article Title"
type: guide | entity | concept | claim | overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/web/official/2026-04-06_sfschool-admissions.md
tags: [tag1, tag2]
epistemic_status: confirmed | likely | disputed | single-source | unknown
confidence: L1 | L2 | L3 | L4 | L5
valid_until: YYYY-MM-DD          # Required for volatile data (dates, prices)
backlinks:
  - wiki/concepts/related.md
---
```

## Directory Conventions

```
topics/{slug}/wiki/
├── _index.md          # Topic wiki index with backlink counts
├── overview.md        # Executive summary
├── guides/            # How-to articles, process descriptions
├── entities/          # Profiles: schools, people, tools, organizations
├── concepts/          # Explanatory articles for ideas, terms, frameworks
└── claims/            # Disputed or noteworthy claims with evidence

shared/
├── concepts/          # Cross-topic concepts (e.g., bay-area-geography)
└── entities/          # Cross-topic entities (e.g., organizations)
```

## Naming Rules

- **Filenames:** kebab-case, no dates in filename (dates go in frontmatter)
  - Good: `sf-school.md`, `application-timeline.md`
  - Bad: `2026-04-06-sf-school.md`, `SF_School.md`
- **Wikilinks:** `[[article-name]]` within same topic, `[[topic-slug:article-name]]` cross-topic
- **Tags:** lowercase, hyphenated, singular: `private-school`, `financial-aid`

## Article Types

### Guide
How-to articles with steps, checklists, timelines.
Template sections: Overview, Prerequisites, Steps, Common Mistakes, See Also.

### Entity
Profiles for schools, people, tools, organizations.
Template sections: Quick Facts (table), Description, Details, What Others Say (labeled anecdotal), See Also.

### Concept
Explanatory articles for ideas, terms, frameworks.
Template sections: Definition, How It Works, Examples, Relevance, See Also.

### Claim
Disputed or noteworthy claims requiring evidence tracking.
Template sections: Claim Statement, Positions (with sources), Resolution Status, Last Checked.

### Overview
Executive summary for the entire topic. One per topic. Auto-generated from index.

## Permitted Language Rules

The fact-sheet assigns permitted language per claim. Wiki articles MUST use the permitted phrasing.

| Evidence Tier | Permitted Phrasing | Prohibited Phrasing |
|---------------|-------------------|---------------------|
| L1 (official source) | State directly: "Tuition is $38,500" | — |
| L2 (authoritative third-party) | Attribute: "According to [source], ..." | Stating without attribution |
| L3 (aggregator/review) | Qualify: "[Platform] rates/lists ..." | Implying universal agreement |
| L4 (community/forum) | Anecdote: "Some parents report ..." | "The school has ..." (as if fact) |
| L5 (false/unverifiable) | DO NOT USE | Anything |

## Epistemic Notes

For unverifiable but valuable information (experiential, subjective), use an epistemic note block:

```markdown
> **Epistemic note:** The following is synthesized from N parent accounts
> on Bay Area forums (date range). Individual experiences vary.
> Treat as directional, not definitive.
```

## Cross-Reference Rules

- Every mention of an entity or concept that has its own article SHOULD be a `[[wikilink]]`
- Backlinks in frontmatter are auto-maintained by the cross-linker tool
- Comparison tables should link to individual entity articles
- Claims articles should be cross-linked from all relevant entity/concept articles

## Source Attribution

- Inline citations: `(source: domain.com, Month YYYY)`
- For L1-L2 claims: source attribution is recommended but phrasing takes priority
- For L3-L4 claims: source attribution is REQUIRED
- Raw source files are referenced in frontmatter `sources:` field

## Volatile Data — Volatility Classes

Any data that changes with time (tuition, deadlines, enrollment numbers) MUST have a `volatile:` class in frontmatter. Do NOT use hard `valid_until: YYYY-MM-DD` dates — they are always wrong and become stale immediately.

| Class | Meaning | Re-verify cadence | Example |
|-------|---------|------------------|---------|
| `annual` | Changes each admissions cycle | Every September | Tuition, deadlines, class sizes |
| `cycle_bound` | Specific to one named cycle; archive after cycle closes | After cycle close date | "2025-26 deadline is Jan 23" |
| `evergreen` | Stable over years | Every 3 years | School mission, founding year, philosophy |
| `none` | Historical fact, never changes | Never | "Founded in 1928" |

Additionally, include year qualifiers in body text for all numerical volatile data:
- Correct: "Tuition is $38,500 (2026-27)"
- Incorrect: "Tuition is $38,500"

The lint agent checks `volatile:` classes against article `updated:` dates and flags accordingly.
