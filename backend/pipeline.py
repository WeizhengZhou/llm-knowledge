"""Scaffolding utilities for LLM Knowledge Base.

This module handles only directory initialization — no LLM calls.
All research, compilation, and analysis is done by Claude Code agents
invoked through skills (/.claude/skills/). Agents use their own
Read/Write/WebSearch/WebFetch tools autonomously.

Usage:
    python -m backend.pipeline init "topic name" [--context "user context"]
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

from backend.config import DEFAULT_BUDGET, PROJECT_ROOT, TOPICS_DIR
from backend.tools.manifest import Manifest
from backend.tools.question_tree import QuestionTree


def slugify(text: str) -> str:
    """Convert topic name to a URL-friendly slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def init_topic(topic_name: str, user_context: str = "") -> Path:
    """Initialize a new topic with directory structure and metadata files.

    Creates:
      topics/{slug}/
        _topic.yaml         — metadata and budget
        index.md            — auto-maintained wiki catalog
        log.md              — append-only operation log
        manifest.json       — source tracking
        research-plan.yaml  — empty question tree
        raw/web/{official,journalistic,review,community}/
        raw/manual/
        wiki/{guides,entities,concepts,claims}/
        staging/
        output/

    No LLM calls. The research-planner-agent (invoked via /kb-init skill)
    generates the actual question tree.
    """
    slug = slugify(topic_name)
    topic_dir = TOPICS_DIR / slug

    if topic_dir.exists():
        print(f"Topic already exists: {slug}")
        print(f"  Directory: {topic_dir}")
        return topic_dir

    # Create directory structure
    subdirs = [
        "raw/web/official",
        "raw/web/journalistic",
        "raw/web/review",
        "raw/web/community",
        "raw/manual",
        "wiki/guides",
        "wiki/entities",
        "wiki/concepts",
        "wiki/claims",
        "staging",
        "output",
    ]
    for subdir in subdirs:
        (topic_dir / subdir).mkdir(parents=True, exist_ok=True)

    # _topic.yaml
    (topic_dir / "_topic.yaml").write_text(
        yaml.dump(
            {
                "topic": topic_name,
                "slug": slug,
                "status": "active",
                "created": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "user_context": user_context,
                "budget": DEFAULT_BUDGET.copy(),
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    # index.md
    (topic_dir / "index.md").write_text(
        f"# {topic_name}\n\n"
        "_Auto-maintained by wiki-compiler-agent. Do not edit manually._\n\n"
        "## Articles\n\n*No articles yet. Run `/kb-research` to begin.*\n"
    )

    # log.md
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (topic_dir / "log.md").write_text(
        f"# Operation Log\n\n"
        f"## [{date}] init | Topic initialized\n\n"
        f"- Topic: {topic_name}\n"
        f"- Context: {user_context or 'none'}\n"
    )

    # manifest.json
    Manifest(topic_dir / "manifest.json").save()

    # Empty question tree skeleton — research-planner-agent fills this
    tree = QuestionTree(topic_dir / "research-plan.yaml")
    tree.initialize(topic_name, user_context, DEFAULT_BUDGET.copy())

    # pipeline-state.yaml — shared budget ledger for all pipeline agents
    (topic_dir / "pipeline-state.yaml").write_text(
        yaml.dump(
            {
                "topic": topic_name,
                "slug": slug,
                "searches_used": 0,
                "fetches_used": 0,
                "budget": DEFAULT_BUDGET.copy(),
                "phase_status": {
                    "breadth": "pending",
                    "depth": "pending",
                    "gap_fill": "pending",
                    "extraction": "pending",
                    "fact_check": "pending",
                    "compilation": "pending",
                    "lint": "pending",
                },
                "last_run": None,
                "pipeline_context": {},
            },
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
    )

    print(f"Initialized: {slug}")
    print(f"  {topic_dir}")
    print(f"  Next step: open Claude Code and run /kb-init \"{topic_name}\"")
    print(f"  The research-planner-agent will generate your question tree.")
    return topic_dir


def main():
    parser = argparse.ArgumentParser(
        description="LLM Knowledge Base — directory scaffolding.\n"
        "For research, querying, and compilation use Claude Code skills:\n"
        "  /kb-init, /kb-research, /kb-query, /kb-lint, /kb-evolve, /kb-verify"
    )
    subparsers = parser.add_subparsers(dest="command")

    p_init = subparsers.add_parser("init", help="Initialize topic directory structure")
    p_init.add_argument("topic", help="Topic name (will be slugified)")
    p_init.add_argument("--context", default="", help="User context for the research planner")

    args = parser.parse_args()

    if args.command == "init":
        init_topic(args.topic, args.context)
    else:
        parser.print_help()
        print(
            "\nNote: research, compilation, and querying are done through Claude Code skills,\n"
            "not this CLI. Open Claude Code in this directory and use /kb-init <topic>."
        )


if __name__ == "__main__":
    main()
