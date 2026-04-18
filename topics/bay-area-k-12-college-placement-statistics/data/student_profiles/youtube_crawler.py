#!/usr/bin/env python3
"""
Crawl YouTube "college decision/stats" videos and extract transcripts.

Uses yt-dlp for transcript download (no API quota needed).
Searches via YouTube's public search (or accepts video IDs directly).

Usage:
    # Search and download transcripts
    python youtube_crawler.py --search "stats that got me into stanford asian" --limit 5

    # Download specific video transcripts
    python youtube_crawler.py --videos dQw4w9WgXcQ abc123xyz

    # Search with multiple queries
    python youtube_crawler.py --search "college decisions stats got into ivy" --limit 10
"""

import json
import subprocess
import sys
import re
import time
from pathlib import Path
from datetime import datetime

RAW_DIR = Path(__file__).parent / "raw" / "youtube"
RATE_LIMIT = 2.0  # seconds between downloads


def search_youtube(query: str, limit: int = 10) -> list:
    """Search YouTube and return video metadata using yt-dlp search."""
    cmd = [
        "yt-dlp",
        f"ytsearch{limit}:{query}",
        "--flat-playlist",
        "--dump-json",
        "--no-download",
        "--no-warnings",
    ]

    print(f"  Searching YouTube: '{query}' (limit {limit})...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        print("  Search timed out")
        return []
    except FileNotFoundError:
        print("  ERROR: yt-dlp not installed. Run: brew install yt-dlp")
        return []

    videos = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        try:
            data = json.loads(line)
            videos.append({
                "id": data.get("id", ""),
                "title": data.get("title", ""),
                "url": data.get("url", f"https://www.youtube.com/watch?v={data.get('id', '')}"),
                "duration": data.get("duration", 0),
                "view_count": data.get("view_count", 0),
                "upload_date": data.get("upload_date", ""),
                "channel": data.get("channel", data.get("uploader", "")),
                "description": (data.get("description", "") or "")[:500],
            })
        except json.JSONDecodeError:
            continue

    return videos


def download_transcript(video_id: str) -> str | None:
    """Download auto-generated or manual subtitles for a video."""
    cmd = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={video_id}",
        "--write-auto-sub",
        "--write-sub",
        "--sub-lang", "en",
        "--sub-format", "vtt",
        "--skip-download",
        "--no-warnings",
        "-o", "/tmp/yt_sub_%(id)s",
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None

    # Look for the subtitle file
    for suffix in [".en.vtt", ".en.auto.vtt"]:
        sub_path = Path(f"/tmp/yt_sub_{video_id}{suffix}")
        if sub_path.exists():
            content = sub_path.read_text()
            sub_path.unlink()  # cleanup
            return vtt_to_text(content)

    return None


def vtt_to_text(vtt_content: str) -> str:
    """Convert VTT subtitle format to plain text, removing timestamps and duplicates."""
    lines = []
    seen = set()

    for line in vtt_content.split("\n"):
        # Skip timestamps, headers, style blocks
        if "-->" in line or line.startswith("WEBVTT") or line.startswith("Kind:") or \
           line.startswith("Language:") or line.startswith("NOTE") or not line.strip():
            continue
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', line).strip()
        if clean and clean not in seen:
            seen.add(clean)
            lines.append(clean)

    return " ".join(lines)


def is_relevant_video(video: dict) -> bool:
    """Filter for college decision/stats videos."""
    title = (video.get("title", "") or "").lower()
    desc = (video.get("description", "") or "").lower()
    text = title + " " + desc

    # Positive signals
    has_college = any(w in text for w in ["college", "university", "ivy", "stanford", "mit", "harvard"])
    has_stats = any(w in text for w in ["stats", "gpa", "sat", "act", "accepted", "decision", "results", "got into", "how i got"])
    has_reaction = any(w in text for w in ["reaction", "decision day", "where i'm going", "committed"])

    # Negative signals
    is_unrelated = any(w in text for w in ["football highlights", "basketball highlights", "gameplay", "music video", "tutorial"])

    # Duration filter: 3-30 min (too short = clickbait, too long = vlog)
    duration = video.get("duration", 0) or 0
    good_duration = 180 <= duration <= 1800

    return (has_college and (has_stats or has_reaction)) and not is_unrelated and good_duration


def save_video(video: dict, transcript: str) -> Path:
    """Save video metadata + transcript as markdown."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    video_id = video["id"]
    filepath = RAW_DIR / f"{video_id}.md"

    upload_date = video.get("upload_date", "")
    if upload_date and len(upload_date) == 8:
        upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    content = f"""---
source: youtube
source_id: {video_id}
url: https://www.youtube.com/watch?v={video_id}
title: "{(video.get('title', '') or '').replace('"', "'")}"
channel: "{(video.get('channel', '') or '').replace('"', "'")}"
view_count: {video.get('view_count', 0) or 0}
duration: {video.get('duration', 0) or 0}
upload_date: {upload_date}
crawled_at: {datetime.utcnow().isoformat()}
has_transcript: {bool(transcript)}
---

# {video.get('title', 'Untitled')}

## Description
{(video.get('description', '') or '')[:1000]}

## Transcript
{transcript or '[No transcript available]'}
"""

    filepath.write_text(content)
    return filepath


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Crawl YouTube college decision videos")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max videos per search")
    parser.add_argument("--videos", nargs="+", help="Specific video IDs")
    parser.add_argument("--no-transcript", action="store_true", help="Save metadata only, skip transcript download")
    parser.add_argument("--filter", action="store_true", help="Apply relevance filter")
    args = parser.parse_args()

    videos = []

    if args.videos:
        for vid in args.videos:
            videos.append({
                "id": vid,
                "title": "",
                "url": f"https://www.youtube.com/watch?v={vid}",
                "duration": 0,
                "view_count": 0,
                "upload_date": "",
                "channel": "",
                "description": "",
            })
    elif args.search:
        videos = search_youtube(args.search, args.limit)
    else:
        print("Provide --search or --videos")
        sys.exit(1)

    if args.filter:
        before = len(videos)
        videos = [v for v in videos if is_relevant_video(v)]
        print(f"  Filtered: {before} → {len(videos)} relevant videos")

    saved = 0
    for video in videos:
        # Skip if already crawled
        filepath = RAW_DIR / f"{video['id']}.md"
        if filepath.exists():
            print(f"  Skip (exists): {video['id']}")
            continue

        transcript = None
        if not args.no_transcript:
            print(f"  Downloading transcript: {video['id']} — {video.get('title', '')[:60]}...")
            transcript = download_transcript(video["id"])
            time.sleep(RATE_LIMIT)

        filepath = save_video(video, transcript)
        t_len = len(transcript) if transcript else 0
        print(f"  Saved: {filepath.name} (transcript: {t_len} chars, views: {video.get('view_count', 0)})")
        saved += 1

    print(f"\nTotal: {saved} videos saved to {RAW_DIR}")


if __name__ == "__main__":
    main()
