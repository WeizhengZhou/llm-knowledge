"""Wikilink management: insertion, backlink maintenance, and link graph analysis.

Manages the network of [[wikilinks]] across wiki articles. Provides:
- Scanning all articles for outgoing and incoming links
- Inserting wikilinks when concepts are mentioned but not linked
- Updating backlink frontmatter across all articles
- Finding broken links and orphaned pages
- Generating link graph data for visualization
"""

import re
from pathlib import Path
from typing import Optional

import yaml


# Match [[wikilink]] or [[topic:wikilink]] or [[wikilink|display text]]
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]")

# Match YAML frontmatter
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_links(content: str) -> list[str]:
    """Extract all wikilink targets from markdown content."""
    return WIKILINK_PATTERN.findall(content)


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown. Returns (frontmatter_dict, body)."""
    match = FRONTMATTER_PATTERN.match(content)
    if match:
        try:
            fm = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            fm = {}
        body = content[match.end():]
        return fm, body
    return {}, content


def rebuild_with_frontmatter(frontmatter: dict, body: str) -> str:
    """Reconstruct markdown with updated frontmatter."""
    fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    return f"---\n{fm_str}\n---\n{body}"


class LinkGraph:
    """Represents the link structure of the wiki."""

    def __init__(self):
        # article_path -> list of targets it links to
        self.outgoing: dict[str, list[str]] = {}
        # article_path -> list of articles that link to it
        self.incoming: dict[str, list[str]] = {}
        # All known article paths (stem names)
        self.all_articles: set[str] = set()

    def add_article(self, article_stem: str, links_to: list[str]):
        self.all_articles.add(article_stem)
        self.outgoing[article_stem] = links_to
        for target in links_to:
            self.incoming.setdefault(target, [])
            if article_stem not in self.incoming[target]:
                self.incoming[target].append(article_stem)

    def get_broken_links(self) -> list[tuple[str, str]]:
        """Return (source, target) pairs where target doesn't exist."""
        broken = []
        for source, targets in self.outgoing.items():
            for target in targets:
                # Strip topic prefix if present
                clean_target = target.split(":")[-1] if ":" in target else target
                if clean_target not in self.all_articles:
                    broken.append((source, target))
        return broken

    def get_orphans(self) -> list[str]:
        """Return articles with no incoming links (except index/overview)."""
        skip = {"index", "_index", "overview", "log"}
        orphans = []
        for article in self.all_articles:
            if article in skip:
                continue
            if article not in self.incoming or not self.incoming[article]:
                orphans.append(article)
        return sorted(orphans)

    def get_backlinks(self, article_stem: str) -> list[str]:
        return self.incoming.get(article_stem, [])

    def stats(self) -> dict:
        total_links = sum(len(v) for v in self.outgoing.values())
        return {
            "total_articles": len(self.all_articles),
            "total_links": total_links,
            "broken_links": len(self.get_broken_links()),
            "orphaned_pages": len(self.get_orphans()),
            "avg_links_per_article": round(total_links / max(len(self.all_articles), 1), 1),
        }


def _article_stem(path: Path, wiki_dir: Path) -> str:
    """Get the stem name of an article relative to wiki dir."""
    try:
        rel = path.relative_to(wiki_dir)
        return str(rel.with_suffix(""))
    except ValueError:
        return path.stem


class CrossLinker:
    """Manages wikilinks and backlinks across wiki articles."""

    def __init__(self, wiki_dir: Path):
        self.wiki_dir = wiki_dir

    def scan_all(self) -> LinkGraph:
        """Scan all wiki articles and build the link graph."""
        graph = LinkGraph()
        for md_file in self.wiki_dir.rglob("*.md"):
            content = md_file.read_text()
            stem = _article_stem(md_file, self.wiki_dir)
            links = extract_links(content)
            graph.add_article(stem, links)
        return graph

    def find_unlinked_mentions(
        self, article_path: Path, known_concepts: list[str]
    ) -> list[str]:
        """Find concept names mentioned in text but not wikilinked."""
        content = article_path.read_text()
        _, body = parse_frontmatter(content)

        # Get already-linked concepts
        existing_links = set(extract_links(content))

        unlinked = []
        for concept in known_concepts:
            if concept in existing_links:
                continue
            # Check if the concept name appears in the body (case-insensitive)
            # but is not already inside a wikilink
            pattern = re.compile(
                r"(?<!\[\[)" + re.escape(concept.replace("-", " ")) + r"(?!\]\])",
                re.IGNORECASE,
            )
            if pattern.search(body):
                unlinked.append(concept)
        return unlinked

    def insert_links(self, article_path: Path, concepts: list[str]) -> int:
        """Insert [[wikilinks]] for mentioned concepts. Returns count inserted."""
        content = article_path.read_text()
        fm, body = parse_frontmatter(content)
        count = 0

        for concept in concepts:
            display_name = concept.replace("-", " ")
            # Replace first unlinked mention only (case-insensitive)
            pattern = re.compile(
                r"(?<!\[\[)\b(" + re.escape(display_name) + r")\b(?!\]\])",
                re.IGNORECASE,
            )
            new_body, n = pattern.subn(f"[[{concept}|\\1]]", body, count=1)
            if n > 0:
                body = new_body
                count += 1

        if count > 0:
            article_path.write_text(rebuild_with_frontmatter(fm, body))
        return count

    def update_backlinks(self) -> int:
        """Update backlinks in frontmatter for all articles. Returns count updated."""
        graph = self.scan_all()
        count = 0

        for md_file in self.wiki_dir.rglob("*.md"):
            stem = _article_stem(md_file, self.wiki_dir)
            backlinks = sorted(graph.get_backlinks(stem))

            content = md_file.read_text()
            fm, body = parse_frontmatter(content)

            current_backlinks = fm.get("backlinks", [])
            if sorted(current_backlinks) != backlinks:
                fm["backlinks"] = backlinks
                md_file.write_text(rebuild_with_frontmatter(fm, body))
                count += 1

        return count

    def get_all_concepts(self) -> list[str]:
        """Get all article stems as potential link targets."""
        concepts = []
        for md_file in self.wiki_dir.rglob("*.md"):
            stem = _article_stem(md_file, self.wiki_dir)
            if stem not in ("index", "_index", "overview", "log"):
                concepts.append(stem)
        return sorted(concepts)

    def find_broken(self) -> list[tuple[str, str]]:
        """Find broken wikilinks."""
        return self.scan_all().get_broken_links()

    def find_orphans(self) -> list[str]:
        """Find orphaned pages (no incoming links)."""
        return self.scan_all().get_orphans()
