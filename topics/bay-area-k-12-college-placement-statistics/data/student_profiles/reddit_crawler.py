#!/usr/bin/env python3
"""
Crawl r/collegeresults posts and save as raw markdown files.

Uses Reddit's public JSON API (no auth needed for public subreddits).
Rate limited to 1 request/second with proper User-Agent.

Usage:
    # Crawl recent posts from r/collegeresults
    python reddit_crawler.py --subreddit collegeresults --limit 25

    # Crawl with search filter
    python reddit_crawler.py --subreddit collegeresults --search "asian bay area" --limit 10

    # Crawl specific post IDs (for test cases)
    python reddit_crawler.py --posts t3_abc123 t3_def456
"""

import json
import time
import urllib.request
import urllib.parse
import sys
import re
from pathlib import Path
from datetime import datetime

RAW_DIR = Path(__file__).parent / "raw" / "reddit" / "collegeresults"
RATE_LIMIT = 1.5  # seconds between requests
USER_AGENT = "StudentProfileResearch/1.0 (educational research; contact: github.com/llm-knowledge)"


def fetch_json(url: str) -> dict:
    """Fetch JSON from Reddit API with rate limiting."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    time.sleep(RATE_LIMIT)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def crawl_subreddit(subreddit: str, limit: int = 25, after: str = None, search: str = None) -> list:
    """Crawl posts from a subreddit, returning list of post data dicts."""
    posts = []
    remaining = limit

    while remaining > 0:
        batch = min(remaining, 25)  # Reddit max per page

        if search:
            url = f"https://www.reddit.com/r/{subreddit}/search.json?q={urllib.parse.quote(search)}&restrict_sr=on&sort=relevance&t=all&limit={batch}"
        else:
            url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={batch}"

        if after:
            url += f"&after={after}"

        print(f"  Fetching: {url[:100]}...")
        data = fetch_json(url)

        children = data.get("data", {}).get("children", [])
        if not children:
            break

        for child in children:
            post = child.get("data", {})
            if not post.get("selftext"):
                continue  # Skip link-only posts

            posts.append({
                "id": post.get("name", ""),  # t3_xxxxx format
                "title": post.get("title", ""),
                "selftext": post.get("selftext", ""),
                "score": post.get("score", 0),
                "url": f"https://www.reddit.com{post.get('permalink', '')}",
                "created_utc": post.get("created_utc", 0),
                "num_comments": post.get("num_comments", 0),
                "flair": post.get("link_flair_text", ""),
                "author": post.get("author", "[deleted]"),
            })

        after = data.get("data", {}).get("after")
        remaining -= len(children)

        if not after:
            break

    return posts


def crawl_post(post_id: str) -> dict | None:
    """Crawl a single post by ID."""
    # Normalize: accept both "t3_abc" and "abc" formats
    if not post_id.startswith("t3_"):
        post_id = f"t3_{post_id}"

    short_id = post_id.replace("t3_", "")
    url = f"https://www.reddit.com/r/collegeresults/comments/{short_id}.json"

    print(f"  Fetching post: {short_id}...")
    try:
        data = fetch_json(url)
    except Exception as e:
        print(f"  Error fetching {short_id}: {e}")
        return None

    if not data or not isinstance(data, list) or len(data) == 0:
        return None

    post = data[0].get("data", {}).get("children", [{}])[0].get("data", {})
    if not post.get("selftext"):
        return None

    return {
        "id": post.get("name", post_id),
        "title": post.get("title", ""),
        "selftext": post.get("selftext", ""),
        "score": post.get("score", 0),
        "url": f"https://www.reddit.com{post.get('permalink', '')}",
        "created_utc": post.get("created_utc", 0),
        "num_comments": post.get("num_comments", 0),
        "flair": post.get("link_flair_text", ""),
        "author": post.get("author", "[deleted]"),
    }


def save_post(post: dict) -> Path:
    """Save a post as a markdown file with frontmatter."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    post_id = post["id"].replace("t3_", "")
    filepath = RAW_DIR / f"{post_id}.md"

    created = datetime.utcfromtimestamp(post["created_utc"]).isoformat() if post["created_utc"] else ""

    content = f"""---
source: reddit/collegeresults
source_id: {post['id']}
url: {post['url']}
title: "{post['title'].replace('"', "'")}"
score: {post['score']}
num_comments: {post['num_comments']}
flair: "{post.get('flair', '')}"
created_utc: {created}
crawled_at: {datetime.utcnow().isoformat()}
---

# {post['title']}

{post['selftext']}
"""

    filepath.write_text(content)
    return filepath


def is_results_post(post: dict) -> bool:
    """Heuristic filter: is this a college results post (not advice/question)?"""
    title = post.get("title", "").lower()
    text = post.get("selftext", "").lower()

    # Positive signals
    has_results = any(w in title for w in ["results", "accepted", "committed", "decision", "got into"])
    has_stats = any(w in text for w in ["gpa", "sat", "act", "ap ", "extracurricular"])
    has_outcomes = any(w in text for w in ["accepted", "rejected", "waitlisted", "committed"])

    # Negative signals
    is_question = any(w in title for w in ["chance me", "should i", "help", "advice", "?"])

    return (has_results or (has_stats and has_outcomes)) and not is_question


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Crawl r/collegeresults posts")
    parser.add_argument("--subreddit", default="collegeresults")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--search", type=str, default=None)
    parser.add_argument("--posts", nargs="+", help="Specific post IDs to crawl")
    parser.add_argument("--filter", action="store_true", help="Apply results-post filter")
    args = parser.parse_args()

    if args.posts:
        # Crawl specific posts
        posts = []
        for pid in args.posts:
            post = crawl_post(pid)
            if post:
                posts.append(post)
    else:
        # Crawl subreddit
        posts = crawl_subreddit(args.subreddit, args.limit, search=args.search)

    if args.filter:
        before = len(posts)
        posts = [p for p in posts if is_results_post(p)]
        print(f"Filtered: {before} → {len(posts)} results posts")

    saved = 0
    for post in posts:
        filepath = save_post(post)
        print(f"  Saved: {filepath.name} (score={post['score']}, {len(post['selftext'])} chars)")
        saved += 1

    print(f"\nTotal: {saved} posts saved to {RAW_DIR}")


if __name__ == "__main__":
    main()
