"""Append-only log of all search queries for audit and deduplication.

Every web search is recorded with its query, results, selections, and
skip reasons. This enables:
- Query deduplication (don't re-run the same query)
- Budget tracking (how many searches/fetches used)
- Audit trail (trace any wiki claim back to a search)
"""

import json
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional


class SearchRecord:
    """A single search operation record."""

    def __init__(
        self,
        search_id: str,
        timestamp: str,
        question_id: str,
        query: str,
        engine: str,
        results_count: int,
        results_selected: list[str],
        results_skipped: dict[str, str],
        new_concepts: list[str],
        new_questions: list[str],
    ):
        self.search_id = search_id
        self.timestamp = timestamp
        self.question_id = question_id
        self.query = query
        self.engine = engine
        self.results_count = results_count
        self.results_selected = results_selected
        self.results_skipped = results_skipped
        self.new_concepts = new_concepts
        self.new_questions = new_questions

    def to_dict(self) -> dict:
        return {
            "id": self.search_id,
            "timestamp": self.timestamp,
            "question_id": self.question_id,
            "query": self.query,
            "engine": self.engine,
            "results_count": self.results_count,
            "results_selected": self.results_selected,
            "results_skipped": self.results_skipped,
            "new_concepts_discovered": self.new_concepts,
            "new_questions_spawned": self.new_questions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SearchRecord":
        return cls(
            search_id=data["id"],
            timestamp=data["timestamp"],
            question_id=data.get("question_id", ""),
            query=data["query"],
            engine=data.get("engine", "web_search"),
            results_count=data.get("results_count", 0),
            results_selected=data.get("results_selected", []),
            results_skipped=data.get("results_skipped", {}),
            new_concepts=data.get("new_concepts_discovered", []),
            new_questions=data.get("new_questions_spawned", []),
        )


def _normalize_query(query: str) -> str:
    """Normalize a search query for comparison."""
    return " ".join(query.lower().split())


def _query_similarity(a: str, b: str) -> float:
    """Compute similarity between two search queries."""
    return SequenceMatcher(None, _normalize_query(a), _normalize_query(b)).ratio()


class SearchLog:
    """Append-only log of all search queries."""

    def __init__(self, log_path: Path):
        self.path = log_path
        self._records: list[SearchRecord] = []
        self._next_counter: int = 1
        self._load()

    def _load(self):
        if self.path.exists():
            for line in self.path.read_text().strip().split("\n"):
                if line.strip():
                    try:
                        data = json.loads(line)
                        self._records.append(SearchRecord.from_dict(data))
                    except json.JSONDecodeError:
                        continue
            self._next_counter = len(self._records) + 1

    def _generate_id(self) -> str:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        sid = f"s-{date}-{self._next_counter:03d}"
        self._next_counter += 1
        return sid

    def record(
        self,
        query: str,
        question_id: str,
        results_selected: list[str],
        results_count: int = 0,
        results_skipped: Optional[dict[str, str]] = None,
        new_concepts: Optional[list[str]] = None,
        new_questions: Optional[list[str]] = None,
        engine: str = "web_search",
    ) -> str:
        """Record a search and return the search ID."""
        search_id = self._generate_id()
        record = SearchRecord(
            search_id=search_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            question_id=question_id,
            query=query,
            engine=engine,
            results_count=results_count,
            results_selected=results_selected,
            results_skipped=results_skipped or {},
            new_concepts=new_concepts or [],
            new_questions=new_questions or [],
        )
        self._records.append(record)
        self._append(record)
        return search_id

    def _append(self, record: SearchRecord):
        """Append a single record to the log file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a") as f:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + "\n")

    def is_duplicate_query(self, query: str, threshold: float = 0.90) -> tuple[bool, Optional[str]]:
        """Check if a similar query has already been run."""
        for record in self._records:
            if _query_similarity(query, record.query) >= threshold:
                return True, record.search_id
        return False, None

    def get_queries_for_question(self, question_id: str) -> list[SearchRecord]:
        """Get all search records for a specific question."""
        return [r for r in self._records if r.question_id == question_id]

    def get_all_fetched_urls(self) -> set[str]:
        """Get all URLs that have been fetched across all searches."""
        urls = set()
        for record in self._records:
            urls.update(record.results_selected)
        return urls

    def budget_used(self) -> dict:
        """Return counts of searches and fetches performed."""
        total_fetches = sum(len(r.results_selected) for r in self._records)
        return {
            "searches": len(self._records),
            "fetches": total_fetches,
        }

    def all_records(self) -> list[SearchRecord]:
        return list(self._records)
