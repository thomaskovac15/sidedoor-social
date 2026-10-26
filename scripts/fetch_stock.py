#!/usr/bin/env python3
"""Pull free stock footage and photos from Pexels (https://www.pexels.com/license/) into clips/ and
photos/rotation/, record where each came from, and register them with the pickers.

The Pexels licence allows commercial use, including social media marketing, with no attribution needed. It does
not allow suggesting that an identifiable person shown endorses a product, or showing them in a bad light, so stock
people only ever carry the job seeker's point of view (AGENTS.md, Sidedoor overrides 1 and 6).

Needs PEXELS_API_KEY in the environment or in this project's .env (git-ignored). The key is never printed.

Usage:
    python scripts/fetch_stock.py --preset                       # every query in clips/stock_queries.txt
    python scripts/fetch_stock.py --query "coffee shop laptop" --per-query 4
    python scripts/fetch_stock.py --preset --photos              # photos for TikTok slides instead of clips
    python scripts/fetch_stock.py --preset --dry-run             # show what would be downloaded
"""
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLIPS = PROJECT_ROOT / "clips"
PHOTOS = PROJECT_ROOT / "photos" / "rotation"
API = "https://api.pexels.com"
USER_AGENT = "sidedoor-social/1.0"


def api_key() -> str:
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    env_file = PROJECT_ROOT / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("PEXELS_API_KEY="):
                key = line.split("=", 1)[1].strip().strip("'\"")
    if not key:
        raise SystemExit("PEXELS_API_KEY is not set. Add a line PEXELS_API_KEY=... to .env in this folder (never paste it in chat).")
    return key


def get_json(url: str, key: str) -> dict:
    request = urllib.request.Request(url, headers={"Authorization": key, "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, target: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    partial = target.with_suffix(target.suffix + ".part")
    with urllib.request.urlopen(request, timeout=120) as response, open(partial, "wb") as out:
        while chunk := response.read(1 << 16):
            out.write(chunk)
    partial.replace(target)


def load(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def best_video_file(video: dict) -> dict | None:
    """A portrait file about 1080 wide (720 to 1440), the closest to 1080 first."""
    files = [f for f in video.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("width") and f.get("height")]
    portrait = [f for f in files if f["height"] > f["width"] and 720 <= f["width"] <= 1440]
    return min(portrait, key=lambda f: abs(f["width"] - 1080)) if portrait else None


def queries_from(args) -> list[str]:
    queries = list(args.query or [])
    if args.preset:
        preset = CLIPS / "stock_queries.txt"
        queries += [line.strip() for line in preset.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
    if not queries:
        raise SystemExit("Give --query \"...\" or --preset.")
    return queries


def fetch_videos(args, key: str) -> int:
    sources_path = CLIPS / "sources.json"
    usage_path = CLIPS / "clips_usage.json"
    sources = load(sources_path, {})
    usage = load(usage_path, {"counts": {}})
    have = {entry["id"] for entry in sources.values() if entry.get("source") == "pexels"}
    added = 0
    for query in queries_from(args):
        params = urllib.parse.urlencode({"query": query, "orientation": "portrait", "per_page": 40, "size": "medium"})
        results = get_json(f"{API}/videos/search?{params}", key).get("videos", [])
        taken = 0
        for video in results:
            if taken >= args.per_query:
                break
            if video["id"] in have or not (args.min_seconds <= video.get("duration", 0) <= args.max_seconds):
                continue
            chosen = best_video_file(video)
            if chosen is None:
                continue
            name = f"pexels-{video['id']}.mp4"
            print(f"{'would get' if args.dry_run else 'getting'} {name} ({chosen['width']}x{chosen['height']}, {video['duration']}s) for \"{query}\"")
            taken += 1
            if args.dry_run:
                continue
            download(chosen["link"], CLIPS / name)
            sources[name] = {
                "source": "pexels", "id": video["id"], "page": video.get("url"), "creator": (video.get("user") or {}).get("name"),
                "creator_page": (video.get("user") or {}).get("url"), "licence": "Pexels License (https://www.pexels.com/license/)",
                "query": query, "duration_s": video.get("duration"), "size": f"{chosen['width']}x{chosen['height']}", "added": date.today().isoformat(),
            }
            usage["counts"].setdefault(name, 0)
            have.add(video["id"])
            added += 1
            save(sources_path, sources)
            save(usage_path, usage)
            time.sleep(0.3)
    return added


def fetch_photos(args, key: str) -> int:
    sources_path = PHOTOS.parent / "sources.json"
    positions_path = PHOTOS.parent / "rotation_positions.json"
    sources = load(sources_path, {})
    positions = load(positions_path, {"roles": {"fixed_slide_2": None, "cta_only": None}, "positions": {}})
    have = {entry["id"] for entry in sources.values() if entry.get("source") == "pexels"}
    PHOTOS.mkdir(parents=True, exist_ok=True)
    added = 0
    for query in queries_from(args):
        params = urllib.parse.urlencode({"query": query, "orientation": "portrait", "per_page": 40})
        results = get_json(f"{API}/v1/search?{params}", key).get("photos", [])
        taken = 0
        for photo in results:
            if taken >= args.per_query:
                break
            if photo["id"] in have:
                continue
            name = f"pexels-{photo['id']}.jpg"
            print(f"{'would get' if args.dry_run else 'getting'} {name} for \"{query}\"")
            taken += 1
            if args.dry_run:
                continue
            download(f"{photo['src']['original']}?auto=compress&cs=tinysrgb&w=1080", PHOTOS / name)
            sources[name] = {
                "source": "pexels", "id": photo["id"], "page": photo.get("url"), "creator": photo.get("photographer"),
                "creator_page": photo.get("photographer_url"), "licence": "Pexels License (https://www.pexels.com/license/)",
                "query": query, "added": date.today().isoformat(),
            }
            # The native look centres its text, so every photo joins the "middle" pool (photos/README.md).
            positions["positions"].setdefault(name, "middle")
            have.add(photo["id"])
            added += 1
            save(sources_path, sources)
            save(positions_path, positions)
            time.sleep(0.3)
    return added


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--query", action="append", help="A search, e.g. \"coffee shop laptop\" (repeatable)")
    parser.add_argument("--preset", action="store_true", help="Also use every query in clips/stock_queries.txt")
    parser.add_argument("--per-query", type=int, default=3, help="How many new items to take per query (default 3)")
    parser.add_argument("--photos", action="store_true", help="Fetch photos for TikTok slides instead of clips")
    parser.add_argument("--min-seconds", type=float, default=5)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--dry-run", action="store_true", help="List what would be downloaded; download nothing")
    args = parser.parse_args()
    key = api_key()
    added = fetch_photos(args, key) if args.photos else fetch_videos(args, key)
    print("Dry run: nothing was downloaded." if args.dry_run else f"Added {added} new item(s).")


if __name__ == "__main__":
    sys.exit(main())
