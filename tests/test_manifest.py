"""Tests for manifest.py — source tracking with content hashes."""

import json
import tempfile
from pathlib import Path

import pytest

from backend.tools.manifest import Manifest, compute_hash


@pytest.fixture
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def manifest(tmp_dir):
    return Manifest(tmp_dir / "manifest.json")


class TestManifest:
    def test_init_creates_empty(self, manifest, tmp_dir):
        manifest.save()
        data = json.loads((tmp_dir / "manifest.json").read_text())
        assert data["sources"] == {}

    def test_register_and_check(self, manifest):
        manifest.register(
            source_path="raw/web/test.md",
            content_hash="sha256:abc123",
            produced_pages=["wiki/concepts/test.md"],
            reliability_tier="L1",
        )
        assert manifest.is_ingested("raw/web/test.md")
        assert not manifest.is_ingested("raw/web/other.md")

    def test_stale_detection(self, manifest):
        manifest.register(
            source_path="raw/web/test.md",
            content_hash="sha256:abc123",
            produced_pages=[],
            reliability_tier="L2",
        )
        assert not manifest.is_stale("raw/web/test.md", "sha256:abc123")
        assert manifest.is_stale("raw/web/test.md", "sha256:changed")
        assert manifest.is_stale("raw/web/new.md", "sha256:anything")

    def test_get_produced_pages(self, manifest):
        manifest.register(
            source_path="raw/web/test.md",
            content_hash="sha256:abc",
            produced_pages=["wiki/a.md", "wiki/b.md"],
        )
        assert manifest.get_produced_pages("raw/web/test.md") == ["wiki/a.md", "wiki/b.md"]
        assert manifest.get_produced_pages("raw/web/nonexist.md") == []

    def test_persistence(self, tmp_dir):
        m1 = Manifest(tmp_dir / "manifest.json")
        m1.register("raw/test.md", "sha256:abc", ["wiki/test.md"], "L1")

        m2 = Manifest(tmp_dir / "manifest.json")
        assert m2.is_ingested("raw/test.md")
        entry = m2.get_entry("raw/test.md")
        assert entry.content_hash == "sha256:abc"
        assert entry.reliability_tier == "L1"

    def test_stats(self, manifest):
        manifest.register("raw/a.md", "sha256:a", ["wiki/a.md"], "L1")
        manifest.register("raw/b.md", "sha256:b", ["wiki/b.md", "wiki/c.md"], "L2")
        manifest.register("raw/c.md", "sha256:c", [], "L1")
        stats = manifest.stats()
        assert stats["total_sources"] == 3
        assert stats["total_produced_pages"] == 3
        assert stats["by_tier"]["L1"] == 2
        assert stats["by_tier"]["L2"] == 1

    def test_search_id_and_question_id(self, manifest):
        manifest.register(
            source_path="raw/web/test.md",
            content_hash="sha256:abc",
            produced_pages=[],
            search_id="s-2026-04-06-001",
            question_id="q1",
        )
        entry = manifest.get_entry("raw/web/test.md")
        assert entry.search_id == "s-2026-04-06-001"
        assert entry.question_id == "q1"


class TestComputeHash:
    def test_hash_consistency(self, tmp_dir):
        f = tmp_dir / "test.txt"
        f.write_text("hello world")
        h1 = compute_hash(f)
        h2 = compute_hash(f)
        assert h1 == h2
        assert h1.startswith("sha256:")

    def test_hash_changes_with_content(self, tmp_dir):
        f = tmp_dir / "test.txt"
        f.write_text("version 1")
        h1 = compute_hash(f)
        f.write_text("version 2")
        h2 = compute_hash(f)
        assert h1 != h2
