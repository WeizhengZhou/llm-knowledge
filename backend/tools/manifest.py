"""Source tracking with content hashes for idempotent re-runs.

Tracks every ingested source file with its content hash, ingestion timestamp,
produced wiki pages, and reliability tier. Enables:
- Delta computation (only process new/changed sources)
- Staleness detection (source changed since last compilation)
- Idempotent re-runs (skip already-ingested unchanged sources)
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class ManifestEntry:
    """A single source tracking record."""

    def __init__(
        self,
        source_path: str,
        content_hash: str,
        ingested_at: str,
        produced_pages: list[str],
        reliability_tier: str,
        search_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ):
        self.source_path = source_path
        self.content_hash = content_hash
        self.ingested_at = ingested_at
        self.produced_pages = produced_pages
        self.reliability_tier = reliability_tier
        self.search_id = search_id
        self.question_id = question_id

    def to_dict(self) -> dict:
        d = {
            "content_hash": self.content_hash,
            "ingested_at": self.ingested_at,
            "produced_pages": self.produced_pages,
            "reliability_tier": self.reliability_tier,
        }
        if self.search_id:
            d["search_id"] = self.search_id
        if self.question_id:
            d["question_id"] = self.question_id
        return d

    @classmethod
    def from_dict(cls, source_path: str, data: dict) -> "ManifestEntry":
        return cls(
            source_path=source_path,
            content_hash=data["content_hash"],
            ingested_at=data["ingested_at"],
            produced_pages=data.get("produced_pages", []),
            reliability_tier=data.get("reliability_tier", "unknown"),
            search_id=data.get("search_id"),
            question_id=data.get("question_id"),
        )


def compute_hash(file_path: Path) -> str:
    """Compute SHA-256 hash of file contents."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


class Manifest:
    """Tracks ingested sources with content hashes for idempotent re-runs."""

    def __init__(self, manifest_path: Path):
        self.path = manifest_path
        self._entries: dict[str, ManifestEntry] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            data = json.loads(self.path.read_text())
            for source_path, entry_data in data.get("sources", {}).items():
                self._entries[source_path] = ManifestEntry.from_dict(
                    source_path, entry_data
                )

    def save(self):
        data = {
            "sources": {
                path: entry.to_dict() for path, entry in sorted(self._entries.items())
            },
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    def register(
        self,
        source_path: str,
        content_hash: str,
        produced_pages: list[str],
        reliability_tier: str = "unknown",
        search_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ):
        """Register a source as ingested."""
        self._entries[source_path] = ManifestEntry(
            source_path=source_path,
            content_hash=content_hash,
            ingested_at=datetime.now(timezone.utc).isoformat(),
            produced_pages=produced_pages,
            reliability_tier=reliability_tier,
            search_id=search_id,
            question_id=question_id,
        )
        self.save()

    def is_ingested(self, source_path: str) -> bool:
        """Check if a source has been ingested."""
        return source_path in self._entries

    def is_stale(self, source_path: str, current_hash: str) -> bool:
        """Check if a source has changed since last ingestion."""
        if source_path not in self._entries:
            return True
        return self._entries[source_path].content_hash != current_hash

    def get_entry(self, source_path: str) -> Optional[ManifestEntry]:
        return self._entries.get(source_path)

    def get_uningested(self, raw_dir: Path, extensions: tuple[str, ...] = (".md", ".pdf", ".txt")) -> list[Path]:
        """Find files in raw_dir not yet ingested or stale."""
        uningested = []
        for f in raw_dir.rglob("*"):
            if f.is_file() and f.suffix in extensions:
                rel = str(f.relative_to(raw_dir.parent.parent))  # relative to topic dir
                if not self.is_ingested(rel):
                    uningested.append(f)
                else:
                    current_hash = compute_hash(f)
                    if self.is_stale(rel, current_hash):
                        uningested.append(f)
        return uningested

    def get_stale_sources(self, raw_dir: Path) -> list[tuple[str, str, str]]:
        """Return list of (source_path, old_hash, new_hash) for changed sources."""
        stale = []
        for source_path, entry in self._entries.items():
            full_path = raw_dir.parent.parent / source_path
            if full_path.exists():
                current_hash = compute_hash(full_path)
                if current_hash != entry.content_hash:
                    stale.append((source_path, entry.content_hash, current_hash))
        return stale

    def get_produced_pages(self, source_path: str) -> list[str]:
        """Get wiki pages produced from a specific source."""
        entry = self._entries.get(source_path)
        return entry.produced_pages if entry else []

    def stats(self) -> dict:
        """Return summary statistics."""
        tiers = {}
        for entry in self._entries.values():
            tier = entry.reliability_tier
            tiers[tier] = tiers.get(tier, 0) + 1
        return {
            "total_sources": len(self._entries),
            "total_produced_pages": sum(
                len(e.produced_pages) for e in self._entries.values()
            ),
            "by_tier": tiers,
        }
