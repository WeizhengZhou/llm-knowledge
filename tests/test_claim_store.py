"""Tests for claim_store.py — claim extraction and verification tracking."""

import tempfile
from pathlib import Path

import pytest

from backend.tools.claim_store import ClaimStore, Source


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def store(tmp_dir):
    return ClaimStore(
        claims_path=tmp_dir / "claims-register.yaml",
        factsheet_path=tmp_dir / "fact-sheet.yaml",
    )


class TestClaimStore:
    def test_add_claim(self, store):
        claim = store.add_claim(
            text="SF School tuition is $38,500",
            claim_type="numerical",
            sources=[Source(file="raw/web/sfschool.md", tier="L1", value="$38,500")],
            entity="sf-school",
        )
        assert claim.id == "c001"
        assert claim.priority == "must_verify"  # numerical → must_verify

    def test_auto_priority(self, store):
        c1 = store.add_claim("Tuition is $38K", "numerical", [])
        assert c1.priority == "must_verify"

        c2 = store.add_claim("Deadline is Jan 23", "temporal", [])
        assert c2.priority == "must_verify"

        c3 = store.add_claim("It's an Episcopal school", "categorical", [])
        assert c3.priority == "should_verify"

        c4 = store.add_claim("Parents describe it as warm", "sentiment", [])
        assert c4.priority == "may_skip"

    def test_update_verdict(self, store):
        claim = store.add_claim("Test claim", "numerical",
                               [Source("raw/test.md", "L1", "$100")])
        store.update_verdict(
            claim.id,
            verdict="confirmed",
            confidence="L1",
            permitted_language="Test claim is confirmed at $100",
        )
        updated = store.get_permitted_language(claim.id)
        assert updated == "Test claim is confirmed at $100"

    def test_overreach_flag(self, store):
        claim = store.add_claim(
            text="Most schools use Ravenna",
            claim_type="categorical",
            sources=[],
            overreach_flag=True,
            overreach_reason="Generalization from 3 schools",
        )
        overreach_claims = store.get_overreach_claims()
        assert len(overreach_claims) == 1
        assert overreach_claims[0].overreach_reason == "Generalization from 3 schools"

    def test_add_dispute(self, store):
        dispute = store.add_dispute(
            claim_text="Cathedral acceptance rate",
            positions=[
                {"value": "25%", "source": "forum 2024", "tier": "L4"},
                {"value": "20%", "source": "forum 2025", "tier": "L4"},
            ],
            resolution="No official rate published",
            permitted_language="Acceptance rate not officially published; estimated 20-25%",
        )
        assert dispute.id == "d001"
        disputes = store.get_disputed()
        assert len(disputes) == 1

    def test_get_unverified(self, store):
        store.add_claim("Claim 1", "numerical", [])
        store.add_claim("Claim 2", "temporal", [])
        store.add_claim("Claim 3", "sentiment", [])

        must = store.get_unverified(priority="must_verify")
        assert len(must) == 2  # numerical + temporal

    def test_claims_by_entity(self, store):
        store.add_claim("Tuition $38K", "numerical", [], entity="sf-school")
        store.add_claim("Founded 1966", "temporal", [], entity="sf-school")
        store.add_claim("Tuition $40K", "numerical", [], entity="cathedral")

        sf_claims = store.get_claims_for_entity("sf-school")
        assert len(sf_claims) == 2

    def test_stats(self, store):
        store.add_claim("C1", "numerical", [])
        store.add_claim("C2", "temporal", [])
        store.add_claim("C3", "categorical", [])
        store.update_verdict("c001", "confirmed", "L1", "C1 confirmed")

        stats = store.stats()
        assert stats["total_claims"] == 3
        assert stats["verified"] == 1
        assert stats["unverified"] == 2
        assert stats["by_type"]["numerical"] == 1

    def test_persistence(self, tmp_dir):
        s1 = ClaimStore(tmp_dir / "claims.yaml", tmp_dir / "facts.yaml")
        s1.add_claim("Test", "numerical", [Source("raw/t.md", "L1")])
        s1.update_verdict("c001", "confirmed", "L1", "Test confirmed")

        s2 = ClaimStore(tmp_dir / "claims.yaml", tmp_dir / "facts.yaml")
        assert len(s2.get_unverified()) == 0  # c001 is now verified
        assert s2.get_permitted_language("c001") == "Test confirmed"

    def test_blocked_claims(self, store):
        c = store.add_claim("False claim", "categorical", [])
        store.update_verdict(c.id, "blocked", "L5", "")
        blocked = store.get_blocked()
        assert len(blocked) == 1
