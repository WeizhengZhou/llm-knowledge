"""Tests for question_tree.py — question management with scoring and dedup."""

import tempfile
from pathlib import Path

import pytest

from backend.tools.question_tree import QuestionTree, Question, _similarity


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def tree(tmp_dir):
    t = QuestionTree(tmp_dir / "research-plan.yaml")
    t.initialize("Bay Area private school K application", "Parent of 4yo in SF")
    return t


class TestQuestion:
    def test_composite_score(self):
        q = Question(
            id="q1", text="test", facet="WHAT",
            scores={"user_value": 10, "dependency_count": 8, "searchability": 6, "novelty": 4},
        )
        # 10*0.35 + 8*0.25 + 6*0.20 + 4*0.20 = 3.5 + 2.0 + 1.2 + 0.8 = 7.5
        assert q.composite_score == pytest.approx(7.5)

    def test_roundtrip(self):
        q = Question(id="q1", text="What schools exist?", facet="WHAT", phase="breadth")
        d = q.to_dict()
        q2 = Question.from_dict(d)
        assert q2.id == "q1"
        assert q2.text == "What schools exist?"
        assert q2.facet == "WHAT"


class TestQuestionTree:
    def test_initialize(self, tree):
        assert tree.topic == "Bay Area private school K application"
        assert tree.user_context == "Parent of 4yo in SF"

    def test_add_question(self, tree):
        q = tree.add_question("What schools exist?", "WHAT", "breadth")
        assert q is not None
        assert q.id == "q1"
        assert q.text == "What schools exist?"

    def test_add_duplicate_returns_none(self, tree):
        tree.add_question("What schools exist?", "WHAT")
        q2 = tree.add_question("What schools exist?", "WHAT")
        assert q2 is None

    def test_near_duplicate_detection(self, tree):
        tree.add_question("What are the Bay Area private K schools?", "WHAT")
        q2 = tree.add_question("What are the Bay Area private K schools list?", "WHAT")
        # Very close variant, should be caught
        assert q2 is None

    def test_different_questions_not_deduped(self, tree):
        tree.add_question("What schools exist?", "WHAT")
        q2 = tree.add_question("What is the application timeline?", "WHEN")
        assert q2 is not None

    def test_get_next_by_priority(self, tree):
        tree.add_question("Low priority", "META",
                         scores={"user_value": 2, "dependency_count": 0, "searchability": 2, "novelty": 2})
        tree.add_question("High priority", "WHAT",
                         scores={"user_value": 9, "dependency_count": 8, "searchability": 9, "novelty": 9})
        nxt = tree.get_next()
        assert nxt.text == "High priority"

    def test_get_next_respects_phase(self, tree):
        tree.add_question("Breadth q", "WHAT", "breadth",
                         scores={"user_value": 5, "dependency_count": 0, "searchability": 5, "novelty": 5})
        tree.add_question("Depth q", "WHAT", "depth",
                         scores={"user_value": 9, "dependency_count": 0, "searchability": 9, "novelty": 9})
        nxt = tree.get_next(phase="breadth")
        assert nxt.text == "Breadth q"

    def test_dependencies_block(self, tree):
        q1 = tree.add_question("First question", "WHAT")
        tree.add_question("Depends on first", "WHAT",
                         dependencies=[q1.id],
                         scores={"user_value": 10, "dependency_count": 10, "searchability": 10, "novelty": 10})
        # q2 has higher score but is blocked by q1
        nxt = tree.get_next()
        assert nxt.text == "First question"

    def test_mark_answered_unblocks(self, tree):
        q1 = tree.add_question("First question", "WHAT")
        q2 = tree.add_question("Depends on first", "HOW",
                              dependencies=[q1.id],
                              scores={"user_value": 10, "dependency_count": 10, "searchability": 10, "novelty": 10})
        tree.mark_answered(q1.id, ["s-001"])
        nxt = tree.get_next()
        assert nxt.id == q2.id

    def test_child_questions(self, tree):
        parent = tree.add_question("What schools exist?", "WHAT")
        child = tree.add_question("What is TK vs K?", "WHAT", parent_id=parent.id,
                                  discovered_from="concept_extraction")
        assert child is not None
        assert child.parent_id == parent.id
        parent_q = tree.get_question(parent.id)
        assert child.id in parent_q.children

    def test_coverage_report(self, tree):
        tree.add_question("Q1", "WHAT", "breadth")
        tree.add_question("Q2", "WHEN", "breadth")
        tree.add_question("Q3", "HOW", "depth")
        tree.mark_answered("q1")
        report = tree.coverage_report()
        assert report["total"] == 3
        assert report["by_status"]["answered"] == 1
        assert report["by_status"]["pending"] == 2
        assert report["by_facet"]["WHAT"]["answered"] == 1

    def test_persistence(self, tmp_dir):
        t1 = QuestionTree(tmp_dir / "plan.yaml")
        t1.initialize("Test topic")
        t1.add_question("What?", "WHAT")
        t1.add_question("When?", "WHEN")

        t2 = QuestionTree(tmp_dir / "plan.yaml")
        assert len(t2.all_questions()) == 2
        assert t2.topic == "Test topic"


class TestSimilarity:
    def test_identical(self):
        assert _similarity("hello world", "hello world") == 1.0

    def test_similar(self):
        sim = _similarity(
            "What are the Bay Area private K schools?",
            "What are Bay Area private kindergarten schools?",
        )
        assert sim > 0.8

    def test_different(self):
        sim = _similarity(
            "What schools exist?",
            "What is the application timeline?",
        )
        assert sim < 0.5
