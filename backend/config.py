"""Pipeline configuration for LLM Knowledge Base."""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Directory structure
TOPICS_DIR = PROJECT_ROOT / "topics"
SHARED_DIR = PROJECT_ROOT / "shared"
AGENTS_DIR = PROJECT_ROOT / ".claude" / "agents"

# Default research budget
DEFAULT_BUDGET = {
    "max_searches": 50,
    "max_fetches": 100,
    "max_tokens_reasoning": 500_000,
    "allocation": {
        "breadth": 0.30,
        "depth": 0.50,
        "gap_fill": 0.15,
        "verification": 0.05,
    },
}

# Question scoring weights
QUESTION_WEIGHTS = {
    "user_value": 0.35,
    "dependency_count": 0.25,
    "searchability": 0.20,
    "novelty": 0.20,
}

# Source reliability tiers
SOURCE_TIERS = {
    "L1": "Primary official source (school website, government site)",
    "L2": "Authoritative third-party (news outlets, institutional reports)",
    "L3": "Aggregator/review platform (Niche, GreatSchools)",
    "L4": "Community signal (forums, Reddit — intelligence only, not citable)",
    "L5": "Low-signal (SEO farms, undated, AI-generated — do not cite)",
}

# Claim verification priorities
VERIFICATION_PRIORITIES = {
    "must_verify": ["numerical", "temporal"],  # prices, dates, deadlines
    "should_verify": ["categorical", "process"],  # types, steps, requirements
    "may_skip": ["sentiment", "definitional"],  # opinions, standard definitions
}

# Deduplication thresholds
DEDUP_TEXT_SIMILARITY = 0.85
DEDUP_QUERY_SIMILARITY = 0.90

# Lint severity levels
LINT_SEVERITY = {
    "error": "Must fix — blocks quality gate",
    "warning": "Should fix — degrades quality",
    "info": "Nice to fix — improvement opportunity",
}

# Topic statuses
TOPIC_STATUSES = ["active", "dormant", "archived"]

# Default TTLs for volatile data
DEFAULT_TTL_VOLATILE = 90  # days for prices, deadlines
DEFAULT_TTL_STABLE = 365  # days for descriptions, philosophy
