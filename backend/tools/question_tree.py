"""Question tree management with scoring, deduplication, and lifecycle tracking.

The question tree is the central research planning artifact. It tracks all
questions (seed + discovered), their scores, dependencies, phases, and status.
"""

import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

import yaml


# Scoring weights (from config)
WEIGHTS = {
    "user_value": 0.35,
    "dependency_count": 0.25,
    "searchability": 0.20,
    "novelty": 0.20,
}

FACETS = ["WHO", "WHAT", "WHEN", "WHERE", "HOW", "WHY", "COMPARE", "META"]
PHASES = ["breadth", "depth", "gap_fill"]
STATUSES = ["pending", "in_progress", "answered", "skipped", "already_covered"]


class Question:
    """A single research question."""

    def __init__(
        self,
        id: str,
        text: str,
        facet: str,
        phase: str = "breadth",
        scores: Optional[dict] = None,
        dependencies: Optional[list[str]] = None,
        status: str = "pending",
        parent_id: Optional[str] = None,
        discovered_from: str = "seed",
        search_queries: Optional[list[str]] = None,
        children: Optional[list[str]] = None,
        answered_by: Optional[list[str]] = None,
    ):
        self.id = id
        self.text = text
        self.facet = facet
        self.phase = phase
        self.scores = scores or {"user_value": 5, "dependency_count": 0, "searchability": 5, "novelty": 5}
        self.dependencies = dependencies or []
        self.status = status
        self.parent_id = parent_id
        self.discovered_from = discovered_from
        self.search_queries = search_queries or []
        self.children = children or []
        self.answered_by = answered_by or []

    @property
    def composite_score(self) -> float:
        return sum(
            self.scores.get(k, 0) * w for k, w in WEIGHTS.items()
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "text": self.text,
            "facet": self.facet,
            "phase": self.phase,
            "scores": self.scores,
            "composite": round(self.composite_score, 2),
            "dependencies": self.dependencies,
            "status": self.status,
            "parent_id": self.parent_id,
            "discovered_from": self.discovered_from,
            "search_queries": self.search_queries,
            "children": self.children,
            "answered_by": self.answered_by,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        return cls(
            id=data["id"],
            text=data["text"],
            facet=data.get("facet", "WHAT"),
            phase=data.get("phase", "breadth"),
            scores=data.get("scores"),
            dependencies=data.get("dependencies", []),
            status=data.get("status", "pending"),
            parent_id=data.get("parent_id"),
            discovered_from=data.get("discovered_from", "seed"),
            search_queries=data.get("search_queries", []),
            children=data.get("children", []),
            answered_by=data.get("answered_by", []),
        )


def _normalize(text: str) -> str:
    """Normalize text for comparison: lowercase, strip punctuation, collapse whitespace."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _similarity(a: str, b: str) -> float:
    """Compute normalized text similarity (0-1)."""
    return SequenceMatcher(None, _normalize(a), _normalize(b)).ratio()


class QuestionTree:
    """Manages the research question tree with scoring and deduplication."""

    def __init__(self, plan_path: Path):
        self.path = plan_path
        self.topic: str = ""
        self.created: str = ""
        self.user_context: str = ""
        self.budget: dict = {}
        self._questions: dict[str, Question] = {}
        self._next_id: int = 1
        self._load()

    def _load(self):
        if self.path.exists():
            data = yaml.safe_load(self.path.read_text()) or {}
            self.topic = data.get("topic", "")
            self.created = data.get("created", "")
            self.user_context = data.get("user_context", "")
            self.budget = data.get("budget", {})
            for q_data in data.get("questions", []):
                q = Question.from_dict(q_data)
                self._questions[q.id] = q
            # Set next ID counter
            if self._questions:
                max_num = 0
                for qid in self._questions:
                    parts = qid.replace("q", "").split(".")
                    try:
                        num = int(parts[0])
                        max_num = max(max_num, num)
                    except ValueError:
                        pass
                self._next_id = max_num + 1

    def save(self):
        # Build phases grouping
        phases = {}
        for phase in PHASES:
            phase_qs = [q.id for q in self._questions.values() if q.phase == phase]
            phases[phase] = {"questions": phase_qs}

        data = {
            "topic": self.topic,
            "created": self.created,
            "user_context": self.user_context,
            "budget": self.budget,
            "phases": phases,
            "questions": [
                q.to_dict()
                for q in sorted(
                    self._questions.values(),
                    key=lambda x: (-x.composite_score, x.id),
                )
            ],
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        )

    def initialize(self, topic: str, user_context: str = "", budget: Optional[dict] = None):
        """Initialize a new question tree for a topic."""
        self.topic = topic
        self.created = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        self.user_context = user_context
        self.budget = budget or {
            "max_searches": 50,
            "max_fetches": 100,
        }
        self.save()

    def add_question(
        self,
        text: str,
        facet: str,
        phase: str = "breadth",
        scores: Optional[dict] = None,
        dependencies: Optional[list[str]] = None,
        parent_id: Optional[str] = None,
        discovered_from: str = "seed",
    ) -> Optional[Question]:
        """Add a question if not duplicate. Returns the question or None if duplicate."""
        is_dup, existing_id = self.deduplicate(text)
        if is_dup:
            return None

        if parent_id:
            qid = f"{parent_id}.{len(self._questions) + 1}"
        else:
            qid = f"q{self._next_id}"
            self._next_id += 1

        q = Question(
            id=qid,
            text=text,
            facet=facet,
            phase=phase,
            scores=scores or {"user_value": 5, "dependency_count": 0, "searchability": 5, "novelty": 5},
            dependencies=dependencies or [],
            parent_id=parent_id,
            discovered_from=discovered_from,
        )
        self._questions[qid] = q

        # Update parent's children list
        if parent_id and parent_id in self._questions:
            self._questions[parent_id].children.append(qid)

        self.save()
        return q

    def deduplicate(self, new_text: str, threshold: float = 0.85) -> tuple[bool, Optional[str]]:
        """Check if a question is a duplicate. Returns (is_dup, existing_id)."""
        for q in self._questions.values():
            sim = _similarity(new_text, q.text)
            if sim >= threshold:
                return True, q.id
        return False, None

    def get_question(self, question_id: str) -> Optional[Question]:
        return self._questions.get(question_id)

    def get_next(self, phase: Optional[str] = None) -> Optional[Question]:
        """Get the next pending question by composite score, optionally filtered by phase."""
        candidates = [
            q for q in self._questions.values()
            if q.status == "pending"
            and (phase is None or q.phase == phase)
            and all(
                self._questions.get(dep, Question("", "", "")).status == "answered"
                for dep in q.dependencies
            )
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda q: q.composite_score)

    def get_pending(self, phase: Optional[str] = None) -> list[Question]:
        """Get all pending questions, optionally filtered by phase."""
        return sorted(
            [
                q for q in self._questions.values()
                if q.status == "pending"
                and (phase is None or q.phase == phase)
            ],
            key=lambda q: -q.composite_score,
        )

    def mark_answered(self, question_id: str, search_ids: Optional[list[str]] = None):
        """Mark a question as answered."""
        q = self._questions.get(question_id)
        if q:
            q.status = "answered"
            q.answered_by = search_ids or []
            self.save()

    def mark_skipped(self, question_id: str, reason: str = ""):
        q = self._questions.get(question_id)
        if q:
            q.status = "skipped"
            self.save()

    def mark_already_covered(self, question_id: str, covered_by: str):
        """Mark as already covered by an existing answered question."""
        q = self._questions.get(question_id)
        if q:
            q.status = "already_covered"
            q.answered_by = [covered_by]
            self.save()

    def update_scores(self, question_id: str, scores: dict):
        q = self._questions.get(question_id)
        if q:
            q.scores.update(scores)
            self.save()

    def add_search_query(self, question_id: str, query: str):
        q = self._questions.get(question_id)
        if q:
            q.search_queries.append(query)
            self.save()

    def coverage_report(self) -> dict:
        """Return coverage statistics."""
        by_status = {}
        by_facet = {}
        by_phase = {}
        for q in self._questions.values():
            by_status[q.status] = by_status.get(q.status, 0) + 1
            by_facet.setdefault(q.facet, {"total": 0, "answered": 0})
            by_facet[q.facet]["total"] += 1
            if q.status == "answered":
                by_facet[q.facet]["answered"] += 1
            by_phase.setdefault(q.phase, {"total": 0, "answered": 0})
            by_phase[q.phase]["total"] += 1
            if q.status == "answered":
                by_phase[q.phase]["answered"] += 1

        return {
            "total": len(self._questions),
            "by_status": by_status,
            "by_facet": by_facet,
            "by_phase": by_phase,
        }

    def all_questions(self) -> list[Question]:
        return sorted(self._questions.values(), key=lambda q: (-q.composite_score, q.id))
