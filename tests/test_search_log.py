"""Tests for search_log.py — search recording and deduplication."""

import tempfile
from pathlib import Path

import pytest

from backend.tools.search_log import SearchLog


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def log(tmp_dir):
    return SearchLog(tmp_dir / "search-log.jsonl")


class TestSearchLog:
    def test_record_and_retrieve(self, log):
        sid = log.record(
            query="Bay Area private schools kindergarten 2026",
            question_id="q1",
            results_selected=["https://sfschool.org", "https://niche.com"],
            results_count=10,
        )
        assert sid.startswith("s-")
        records = log.get_queries_for_question("q1")
        assert len(records) == 1
        assert records[0].query == "Bay Area private schools kindergarten 2026"

    def test_duplicate_query_detection(self, log):
        log.record("Bay Area private schools kindergarten 2026", "q1", [])
        is_dup, existing_id = log.is_duplicate_query("Bay Area private schools kindergarten 2026")
        # Exact same query should be caught
        assert is_dup
        assert existing_id is not None

    def test_different_queries_not_duplicate(self, log):
        log.record("private schools Bay Area", "q1", [])
        is_dup, _ = log.is_duplicate_query("application timeline deadlines 2026")
        assert not is_dup

    def test_budget_tracking(self, log):
        log.record("query 1", "q1", ["url1", "url2"])
        log.record("query 2", "q2", ["url3"])
        budget = log.budget_used()
        assert budget["searches"] == 2
        assert budget["fetches"] == 3

    def test_all_fetched_urls(self, log):
        log.record("q1", "q1", ["https://a.com", "https://b.com"])
        log.record("q2", "q2", ["https://b.com", "https://c.com"])
        urls = log.get_all_fetched_urls()
        assert urls == {"https://a.com", "https://b.com", "https://c.com"}

    def test_persistence(self, tmp_dir):
        log1 = SearchLog(tmp_dir / "log.jsonl")
        log1.record("test query", "q1", ["https://test.com"])

        log2 = SearchLog(tmp_dir / "log.jsonl")
        assert len(log2.all_records()) == 1
        assert log2.all_records()[0].query == "test query"

    def test_new_concepts_and_questions(self, log):
        sid = log.record(
            query="test",
            question_id="q1",
            results_selected=[],
            new_concepts=["Ravenna Hub", "TK"],
            new_questions=["q1.1", "q1.2"],
        )
        records = log.get_queries_for_question("q1")
        assert records[0].new_concepts == ["Ravenna Hub", "TK"]
        assert records[0].new_questions == ["q1.1", "q1.2"]
