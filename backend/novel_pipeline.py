"""Scaffolding utilities for the fiction-writing pipeline.

Clean fork of backend/pipeline.py for novels. No LLM calls — directory
initialization only. All outlining, drafting, and revision is done by
Claude Code agents invoked through /novel-* skills.

Usage:
    python -m backend.novel_pipeline init-novel "The Last Cartographer" \
        [--genre literary-sf] [--pov 3rd-limited] [--tense past]
"""

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

from backend.config import PROJECT_ROOT


NOVELS_DIR = PROJECT_ROOT / "novels"


def slugify(text: str) -> str:
    """Convert a title to a URL-friendly slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def init_novel(
    title: str,
    genre: str = "",
    pov: str = "3rd-limited",
    tense: str = "past",
    target_words: int = 90000,
    audience: str = "adult",
) -> Path:
    """Initialize a new novel with directory structure and metadata files.

    Creates:
      novels/{slug}/
        _novel.yaml          — metadata (title, genre, POV, tense, target length)
        premise.md           — logline + ending (reader fills in; required before outline)
        outline/
          beat-sheet.yaml    — empty (structure method chosen by story-architect-agent)
          scene-list.yaml    — empty (populated by story-architect-agent)
        bible/
          characters/        — one file per major character (stub-first)
          world/             — setting, rules, geography, culture
          timeline.yaml      — empty
          style-guide.md     — seeded with POV/tense from init args
        canon.jsonl          — empty (appended by canon-extractor-agent)
        style-sheet.yaml     — empty (populated by copy-edit-agent)
        manuscript/          — empty (graduated scenes)
        staging/             — empty (drafts pending revision)
        revisions/           — empty (revision plans per stage)
        raw/                 — optional research
        output/              — lint + eval reports
        log.md               — operation log
        CHANGELOG.md         — append-only modification log

    No LLM calls. The story-architect-agent (invoked via /novel-outline and
    /novel-bible) fills in outline and bible content.
    """
    slug = slugify(title)
    novel_dir = NOVELS_DIR / slug

    if novel_dir.exists():
        print(f"Novel already exists: {slug}")
        print(f"  Directory: {novel_dir}")
        return novel_dir

    subdirs = [
        "outline",
        "bible/characters",
        "bible/world",
        "manuscript",
        "staging",
        "revisions",
        "raw",
        "output",
    ]
    for subdir in subdirs:
        (novel_dir / subdir).mkdir(parents=True, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # _novel.yaml
    (novel_dir / "_novel.yaml").write_text(
        yaml.dump(
            {
                "title": title,
                "slug": slug,
                "status": "active",
                "created": today,
                "genre": genre,
                "pov": pov,
                "tense": tense,
                "target_words": target_words,
                "audience": audience,
                "structure_method": "",  # set by story-architect: save-the-cat|snowflake|story-grid|3-act
                "phase_status": {
                    "outline": "pending",
                    "bible": "pending",
                    "draft": "pending",
                    "readthrough": "pending",
                    "dev_edit": "pending",
                    "line_edit": "pending",
                    "copy_edit": "pending",
                    "proof": "pending",
                },
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    # premise.md — the human fills this in before /novel-outline runs
    (novel_dir / "premise.md").write_text(
        f"""# {title} — Premise

## Logline
_(One sentence: protagonist + goal + obstacle + stakes. E.g.,
"A young cartographer must map an impossible continent before her
rival guild steals her discoveries and her life.")_

## Ending
_(Required before /novel-outline. Sanderson's rule: know your ending
before you start drafting. Write 2-5 sentences describing how the book
ends — what the protagonist achieves, what it costs them, how the
world has changed.)_

## Themes
_(2-4 bullets. What is this book about beneath the plot?)_

-
-

## Audience
_(Who is this book for? Genre conventions it honors or subverts?)_

## Comp Titles
_(2-3 published novels this sits alongside on the shelf.)_

-
-
"""
    )

    # outline/beat-sheet.yaml
    (novel_dir / "outline/beat-sheet.yaml").write_text(
        yaml.dump(
            {
                "structure_method": "",  # save-the-cat | snowflake | story-grid | 3-act
                "beats": [],  # populated by story-architect-agent
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    # outline/scene-list.yaml
    (novel_dir / "outline/scene-list.yaml").write_text(
        yaml.dump(
            {
                "scenes": [],  # populated by story-architect-agent
                # Each scene: {id, chapter, pov, goal, conflict, outcome,
                #              word_target, status: pending}
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    # bible/timeline.yaml
    (novel_dir / "bible/timeline.yaml").write_text(
        yaml.dump(
            {"events": []},
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    # bible/style-guide.md — seeded from init args, expanded by story-architect
    (novel_dir / "bible/style-guide.md").write_text(
        f"""# Style Guide — {title}

_BINDING reference for line-edit-agent and copy-edit-agent. POV and
tense violations are hard errors._

## POV
- **Default:** {pov}
- **Per-scene override:** allowed only if declared in scene frontmatter

## Tense
- **Default:** {tense}
- **Flashbacks:** _(specify if different — e.g., past-perfect or present)_

## Voice Register
_(Literary? Commercial? Genre-conventional? How formal is the narration?
Which registers are off-limits?)_

## Dialogue Conventions
- Dialogue tags: _(said-bookism policy; action beats preferred?)_
- Dialect / non-English words: _(italics? romanization convention?)_
- Profanity policy: _(any, limited, none — and per which characters?)_

## Sentence-Level Rules
- Paragraph length: _(short-punchy? flowing?)_
- Semicolon / em-dash usage: _(spare? liberal?)_
- Sentence-initial "And/But/So": _(allowed? sparing?)_

## Forbidden Constructions
_(Populate as line-edit surfaces patterns. Examples: "he smiled softly",
"she couldn't help but", adverb-heavy attribution, head-hopping.)_

## Worldbuilding Terminology
_(Invented words, proper nouns — canonical spellings live in style-sheet.yaml,
this section describes HOW they are used. E.g., "always italicized on first
use per chapter", "never plural", "always capitalized".)_

---

_{today} — seeded. story-architect-agent will expand during /novel-bible._
"""
    )

    # canon.jsonl (empty append-only log)
    (novel_dir / "canon.jsonl").write_text("")

    # style-sheet.yaml (character name spellings, invented words — copy-edit maintains)
    (novel_dir / "style-sheet.yaml").write_text(
        yaml.dump(
            {
                "character_names": {},  # {"Mira Vael": {"preferred": "Mira Vael", "variants": []}}
                "invented_terms": {},   # {"atlasmark": {"caps": "lower", "italics": "first-use"}}
                "place_names": {},
                "conventions": {
                    "em_dash": "no spaces",     # or "spaces"
                    "ellipsis": "three dots",
                    "quotation_marks": "double",
                    "serial_comma": True,
                },
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    # log.md
    (novel_dir / "log.md").write_text(
        f"""# Operation Log — {title}

## [{today}] init | Novel scaffolded

- Title: {title}
- Slug: {slug}
- Genre: {genre or "unset"}
- POV: {pov}
- Tense: {tense}
- Target words: {target_words}

Next: fill in `premise.md` (logline + ending), then run `/novel-outline {slug}`.
"""
    )

    # CHANGELOG.md
    (novel_dir / "CHANGELOG.md").write_text(
        f"""# Changelog — {title}

_Append-only log of all manuscript and bible modifications. Each entry
records what changed, what was added/removed, and why._

## {today} — scaffolding

**Added:**
- Directory structure
- `_novel.yaml` — metadata
- `premise.md` — empty template (user to fill)
- `bible/style-guide.md` — seeded with POV={pov}, tense={tense}
"""
    )

    print(f"Initialized novel: {slug}")
    print(f"  {novel_dir}")
    print(f"  Next step: fill in novels/{slug}/premise.md (logline + ending)")
    print(f"  Then run /novel-outline {slug}")
    return novel_dir


def main():
    parser = argparse.ArgumentParser(
        description="Fiction-writing pipeline — directory scaffolding.\n"
        "For outlining, drafting, and revision use Claude Code skills:\n"
        "  /novel-init, /novel-outline, /novel-bible, /novel-draft,\n"
        "  /novel-readthrough, /novel-revise, /novel-query, /novel-lint"
    )
    subparsers = parser.add_subparsers(dest="command")

    p_init = subparsers.add_parser("init-novel", help="Initialize novel directory")
    p_init.add_argument("title", help="Novel title (will be slugified)")
    p_init.add_argument("--genre", default="", help="Genre label")
    p_init.add_argument("--pov", default="3rd-limited", help="POV (1st, 3rd-limited, 3rd-omniscient)")
    p_init.add_argument("--tense", default="past", help="Narrative tense (past, present)")
    p_init.add_argument("--target-words", type=int, default=90000, help="Target word count")
    p_init.add_argument("--audience", default="adult", help="Audience (adult, YA, MG, children)")

    args = parser.parse_args()

    if args.command == "init-novel":
        init_novel(
            args.title,
            genre=args.genre,
            pov=args.pov,
            tense=args.tense,
            target_words=args.target_words,
            audience=args.audience,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
