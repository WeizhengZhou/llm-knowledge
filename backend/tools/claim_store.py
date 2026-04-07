"""Claim extraction, storage, and verification tracking.

Manages the lifecycle of factual claims from extraction through verification.
Each claim carries a type, source attribution, verification status, confidence
level, and permitted language (binding on wiki compiler).
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml


CLAIM_TYPES = [
    "numerical",    # prices, dates, counts, rates
    "categorical",  # types, status, membership
    "temporal",     # timelines, sequences, deadlines
    "comparative",  # better than, different from
    "causal",       # X causes Y, X leads to Y
    "process",      # steps, requirements, how-to
    "sentiment",    # people feel, parents say
    "definitional", # X is Y, X means Y
]

VERIFICATION_PRIORITY = {
    "must_verify": ["numerical", "temporal"],
    "should_verify": ["categorical", "process", "comparative"],
    "may_skip": ["sentiment", "definitional", "causal"],
}

VERDICTS = ["confirmed", "likely", "single_source", "disputed", "downgraded", "blocked"]
CONFIDENCE_LEVELS = ["L1", "L2", "L3", "L4", "L5"]


class Source:
    """A source reference for a claim."""

    def __init__(self, file: str, tier: str, value: Optional[str] = None,
                 supports: Optional[bool] = None, note: str = ""):
        self.file = file
        self.tier = tier
        self.value = value
        self.supports = supports
        self.note = note

    def to_dict(self) -> dict:
        d = {"file": self.file, "tier": self.tier}
        if self.value is not None:
            d["value"] = self.value
        if self.supports is not None:
            d["supports"] = self.supports
        if self.note:
            d["note"] = self.note
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Source":
        return cls(
            file=data["file"],
            tier=data["tier"],
            value=data.get("value"),
            supports=data.get("supports"),
            note=data.get("note", ""),
        )


class Claim:
    """A single factual claim extracted from sources."""

    def __init__(
        self,
        id: str,
        text: str,
        claim_type: str,
        priority: str,
        sources: list[Source],
        entity: str = "",
        question_id: str = "",
        article_path: str = "",
        line_number: Optional[int] = None,
        overreach_flag: bool = False,
        overreach_reason: str = "",
        # Verification fields (set by fact-checker)
        verdict: str = "",
        confidence: str = "",
        permitted_language: str = "",
        last_verified: str = "",
    ):
        self.id = id
        self.text = text
        self.claim_type = claim_type
        self.priority = priority
        self.sources = sources
        self.entity = entity
        self.question_id = question_id
        self.article_path = article_path
        self.line_number = line_number
        self.overreach_flag = overreach_flag
        self.overreach_reason = overreach_reason
        self.verdict = verdict
        self.confidence = confidence
        self.permitted_language = permitted_language
        self.last_verified = last_verified

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "text": self.text,
            "type": self.claim_type,
            "priority": self.priority,
            "sources": [s.to_dict() for s in self.sources],
        }
        if self.entity:
            d["entity"] = self.entity
        if self.question_id:
            d["question_id"] = self.question_id
        if self.article_path:
            d["article_path"] = self.article_path
        if self.line_number is not None:
            d["line_number"] = self.line_number
        if self.overreach_flag:
            d["overreach_flag"] = True
            d["overreach_reason"] = self.overreach_reason
        if self.verdict:
            d["verdict"] = self.verdict
            d["confidence"] = self.confidence
            d["permitted_language"] = self.permitted_language
            d["last_verified"] = self.last_verified
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Claim":
        return cls(
            id=data["id"],
            text=data["text"],
            claim_type=data.get("type", "categorical"),
            priority=data.get("priority", "should_verify"),
            sources=[Source.from_dict(s) for s in data.get("sources", [])],
            entity=data.get("entity", ""),
            question_id=data.get("question_id", ""),
            article_path=data.get("article_path", ""),
            line_number=data.get("line_number"),
            overreach_flag=data.get("overreach_flag", False),
            overreach_reason=data.get("overreach_reason", ""),
            verdict=data.get("verdict", ""),
            confidence=data.get("confidence", ""),
            permitted_language=data.get("permitted_language", ""),
            last_verified=data.get("last_verified", ""),
        )


class Dispute:
    """A conflict between sources on a claim."""

    def __init__(self, id: str, claim_text: str, positions: list[dict],
                 resolution: str = "", permitted_language: str = ""):
        self.id = id
        self.claim_text = claim_text
        self.positions = positions
        self.resolution = resolution
        self.permitted_language = permitted_language

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "claim": self.claim_text,
            "positions": self.positions,
            "resolution": self.resolution,
            "permitted_language": self.permitted_language,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Dispute":
        return cls(
            id=data["id"],
            claim_text=data["claim"],
            positions=data.get("positions", []),
            resolution=data.get("resolution", ""),
            permitted_language=data.get("permitted_language", ""),
        )


def _priority_for_type(claim_type: str) -> str:
    """Determine verification priority from claim type."""
    for priority, types in VERIFICATION_PRIORITY.items():
        if claim_type in types:
            return priority
    return "should_verify"


class ClaimStore:
    """Stores extracted claims and their verification status."""

    def __init__(self, claims_path: Path, factsheet_path: Optional[Path] = None):
        self.claims_path = claims_path
        self.factsheet_path = factsheet_path
        self._claims: dict[str, Claim] = {}
        self._disputes: dict[str, Dispute] = {}
        self._next_claim_id: int = 1
        self._next_dispute_id: int = 1
        self._load()

    def _load(self):
        if self.claims_path.exists():
            data = yaml.safe_load(self.claims_path.read_text()) or {}
            for c_data in data.get("claims", []):
                c = Claim.from_dict(c_data)
                self._claims[c.id] = c
            if self._claims:
                max_num = max(int(cid.lstrip("c")) for cid in self._claims if cid.startswith("c"))
                self._next_claim_id = max_num + 1

        if self.factsheet_path and self.factsheet_path.exists():
            data = yaml.safe_load(self.factsheet_path.read_text()) or {}
            # Merge verified claims
            for vc in data.get("verified_claims", []):
                cid = vc.get("id")
                if cid and cid in self._claims:
                    self._claims[cid].verdict = vc.get("verdict", "")
                    self._claims[cid].confidence = vc.get("confidence", "")
                    self._claims[cid].permitted_language = vc.get("permitted_language", "")
                    self._claims[cid].last_verified = vc.get("last_verified", "")
            for d_data in data.get("disputes", []):
                d = Dispute.from_dict(d_data)
                self._disputes[d.id] = d

    def save_claims(self):
        data = {
            "claims": [c.to_dict() for c in sorted(self._claims.values(), key=lambda c: c.id)],
        }
        self.claims_path.parent.mkdir(parents=True, exist_ok=True)
        self.claims_path.write_text(
            yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        )

    def save_factsheet(self):
        if not self.factsheet_path:
            return
        verified = [
            c.to_dict() for c in self._claims.values() if c.verdict
        ]
        data = {
            "verified_claims": verified,
            "disputes": [d.to_dict() for d in self._disputes.values()],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
        self.factsheet_path.parent.mkdir(parents=True, exist_ok=True)
        self.factsheet_path.write_text(
            yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        )

    def add_claim(
        self,
        text: str,
        claim_type: str,
        sources: list[Source],
        entity: str = "",
        question_id: str = "",
        overreach_flag: bool = False,
        overreach_reason: str = "",
    ) -> Claim:
        """Add a new claim."""
        cid = f"c{self._next_claim_id:03d}"
        self._next_claim_id += 1
        claim = Claim(
            id=cid,
            text=text,
            claim_type=claim_type,
            priority=_priority_for_type(claim_type),
            sources=sources,
            entity=entity,
            question_id=question_id,
            overreach_flag=overreach_flag,
            overreach_reason=overreach_reason,
        )
        self._claims[cid] = claim
        self.save_claims()
        return claim

    def update_verdict(
        self,
        claim_id: str,
        verdict: str,
        confidence: str,
        permitted_language: str,
    ):
        """Update verification result for a claim."""
        c = self._claims.get(claim_id)
        if c:
            c.verdict = verdict
            c.confidence = confidence
            c.permitted_language = permitted_language
            c.last_verified = datetime.now(timezone.utc).isoformat()
            self.save_claims()
            self.save_factsheet()

    def add_dispute(
        self,
        claim_text: str,
        positions: list[dict],
        resolution: str = "",
        permitted_language: str = "",
    ) -> Dispute:
        """Create a dispute record for conflicting sources."""
        did = f"d{self._next_dispute_id:03d}"
        self._next_dispute_id += 1
        dispute = Dispute(
            id=did,
            claim_text=claim_text,
            positions=positions,
            resolution=resolution,
            permitted_language=permitted_language,
        )
        self._disputes[did] = dispute
        self.save_factsheet()
        return dispute

    def get_unverified(self, priority: Optional[str] = None) -> list[Claim]:
        """Get claims that haven't been verified yet."""
        return [
            c for c in self._claims.values()
            if not c.verdict
            and (priority is None or c.priority == priority)
        ]

    def get_blocked(self) -> list[Claim]:
        """Get claims that are L5/blocked."""
        return [c for c in self._claims.values() if c.confidence == "L5"]

    def get_disputed(self) -> list[Dispute]:
        return list(self._disputes.values())

    def get_claims_for_entity(self, entity: str) -> list[Claim]:
        return [c for c in self._claims.values() if c.entity == entity]

    def get_overreach_claims(self) -> list[Claim]:
        return [c for c in self._claims.values() if c.overreach_flag]

    def get_permitted_language(self, claim_id: str) -> Optional[str]:
        """Get the permitted language for a verified claim (binding on wiki compiler)."""
        c = self._claims.get(claim_id)
        if c and c.permitted_language:
            return c.permitted_language
        return None

    def stats(self) -> dict:
        by_type = {}
        by_priority = {}
        by_verdict = {}
        by_confidence = {}
        for c in self._claims.values():
            by_type[c.claim_type] = by_type.get(c.claim_type, 0) + 1
            by_priority[c.priority] = by_priority.get(c.priority, 0) + 1
            if c.verdict:
                by_verdict[c.verdict] = by_verdict.get(c.verdict, 0) + 1
            if c.confidence:
                by_confidence[c.confidence] = by_confidence.get(c.confidence, 0) + 1

        return {
            "total_claims": len(self._claims),
            "verified": sum(1 for c in self._claims.values() if c.verdict),
            "unverified": sum(1 for c in self._claims.values() if not c.verdict),
            "disputes": len(self._disputes),
            "overreach_flags": sum(1 for c in self._claims.values() if c.overreach_flag),
            "by_type": by_type,
            "by_priority": by_priority,
            "by_verdict": by_verdict,
            "by_confidence": by_confidence,
        }
