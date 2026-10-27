#!/usr/bin/env python3
"""Pull free stock footage and photos into clips/ and photos/rotation/, record where each came from, and register
them with the pickers. Sources:

- Pixabay (default): https://pixabay.com/service/license-summary/ . Key: PIXABAY_API_KEY (free; shown on
  https://pixabay.com/api/docs/ when signed in). Searches are cached for 24 hours, as Pixabay's API rules require,
  and pulls stay small and hand-chosen by query (no systematic mass downloads).
- Pexels: https://www.pexels.com/license/ . Key: PEXELS_API_KEY (Pexels paused new keys in Oct 2026).

Both licences allow commercial use with no attribution, and both forbid misleading uses, so a stock person only
ever carries the job seeker's point of view, never Sidedoor's pitch (AGENTS.md, Sidedoor overrides 1 and 6).
Keys come from the environment or this project's .env (git-ignored) and are never printed.

Usage:
    python scripts/fetch_stock.py --preset                       # every query in clips/stock_queries.txt
    python scripts/fetch_stock.py --query "coffee shop laptop" --per-query 4
    python scripts/fetch_stock.py --preset --photos              # photos for TikTok slides instead of clips
    python scripts/fetch_stock.py --preset --dry-run             # show what would be downloaded
    python scripts/fetch_stock.py --source pexels --preset       # Pexels instead of Pixabay
"""
import argparse
import hashlib
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
CACHE = PROJECT_ROOT / ".cache" / "stock"
USER_AGENT = "sidedoor-social/1.0"
LICENCES = {
    "pixabay": "Pixabay Content License (https://pixabay.com/service/license-summary/)",
    "pexels": "Pexels License (https://www.pexels.com/license/)",
}


def api_key(name: str) -> str:
    key = os.environ.get(name, "").strip()
    env_file = PROJECT_ROOT / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith(f"{name}="):
                key = line.split("=", 1)[1].strip().strip("'\"")
    if not key:
        raise SystemExit(f"{name} is not set. Add a line {name}=... to .env in this folder (never paste it in chat).")
    return key


def get_json(url: str, headers: dict) -> dict:
    """GET with a 24-hour on-disk cache (Pixabay requires caching; it also spares the rate limits)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / (hashlib.sha256(url.encode("utf-8")).hexdigest()[:24] + ".json")
    if cached.exists() and time.time() - cached.stat().st_mtime < 24 * 3600:
        return json.loads(cached.read_text(encoding="utf-8"))
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **headers})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    cached.write_text(json.dumps(data), encoding="utf-8")
    return data


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


def closest_to_1080(files: list[dict], allow_landscape: bool) -> dict | None:
    """A portrait file about 1080 wide (720 to 1440) if there is one; otherwise, if allowed, a landscape file about
    1080 high (it is cropped to 9:16 when rendered)."""
    portrait = [f for f in files if f["height"] > f["width"] and 720 <= f["width"] <= 1440]
    if portrait:
        return min(portrait, key=lambda f: abs(f["width"] - 1080))
    if allow_landscape:
        landscape = [f for f in files if f["width"] >= f["height"] and 720 <= f["height"] <= 1440]
        if landscape:
            return min(landscape, key=lambda f: abs(f["height"] - 1080))
    return None


# --- Sources: each returns candidates as {id, page, creator, creator_page, duration, url, width, height} ----------

def pixabay_videos(query: str, key: str, allow_landscape: bool) -> list[dict]:
    params = urllib.parse.urlencode({"key": key, "q": query, "video_type": "film", "safesearch": "true", "per_page": 50})
    out = []
    for hit in get_json(f"https://pixabay.com/api/videos/?{params}", {}).get("hits", []):
        files = [v for v in (hit.get("videos") or {}).values() if v.get("url") and v.get("width") and v.get("height")]
        chosen = closest_to_1080(files, allow_landscape)
        if chosen:
            out.append({"id": hit["id"], "page": hit.get("pageURL"), "creator": hit.get("user"), "creator_page": None,
                        "duration": hit.get("duration", 0), "url": chosen["url"], "width": chosen["width"], "height": chosen["height"]})
    return out


def pexels_videos(query: str, key: str, allow_landscape: bool) -> list[dict]:
    params = urllib.parse.urlencode({"query": query, "orientation": "portrait", "per_page": 40, "size": "medium"})
    out = []
    for video in get_json(f"https://api.pexels.com/videos/search?{params}", {"Authorization": key}).get("videos", []):
        files = [f for f in video.get("video_files", []) if f.get("file_type") == "video/mp4" and f.get("width") and f.get("height")]
        chosen = closest_to_1080(files, allow_landscape)
        if chosen:
            user = video.get("user") or {}
            out.append({"id": video["id"], "page": video.get("url"), "creator": user.get("name"), "creator_page": user.get("url"),
                        "duration": video.get("duration", 0), "url": chosen["link"], "width": chosen["width"], "height": chosen["height"]})
    return out


def pixabay_photos(query: str, key: str) -> list[dict]:
    params = urllib.parse.urlencode({"key": key, "q": query, "image_type": "photo", "orientation": "vertical", "safesearch": "true", "per_page": 50})
    return [{"id": hit["id"], "page": hit.get("pageURL"), "creator": hit.get("user"), "creator_page": None, "url": hit["largeImageURL"]}
            for hit in get_json(f"https://pixabay.com/api/?{params}", {}).get("hits", []) if hit.get("largeImageURL")]


def pexels_photos(query: str, key: str) -> list[dict]:
    params = urllib.parse.urlencode({"query": query, "orientation": "portrait", "per_page": 40})
    return [{"id": photo["id"], "page": photo.get("url"), "creator": photo.get("photographer"), "creator_page": photo.get("photographer_url"),
             "url": f"{photo['src']['original']}?auto=compress&cs=tinysrgb&w=1080"}
            for photo in get_json(f"https://api.pexels.com/v1/search?{params}", {"Authorization": key}).get("photos", [])]


SOURCES = {
    "pixabay": {"key": "PIXABAY_API_KEY", "videos": pixabay_videos, "photos": pixabay_photos},
    "pexels": {"key": "PEXELS_API_KEY", "videos": pexels_videos, "photos": pexels_photos},
}


def queries_from(args) -> list[str]:
    queries = list(args.query or [])
    if args.preset:
        preset = CLIPS / "stock_queries.txt"
        queries += [line.strip() for line in preset.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
    if not queries:
        raise SystemExit("Give --query \"...\" or --preset.")
    return queries


def fetch(args, key: str) -> int:
    photos = args.photos
    folder = PHOTOS if photos else CLIPS
    sources_path = (PHOTOS.parent if photos else CLIPS) / "sources.json"
    register_path = PHOTOS.parent / "rotation_positions.json" if photos else CLIPS / "clips_usage.json"
    sources = load(sources_path, {})
    register = load(register_path, {"roles": {"fixed_slide_2": None, "cta_only": None}, "positions": {}} if photos else {"counts": {}})
    have = {(entry.get("source"), entry.get("id")) for entry in sources.values()}
    search = SOURCES[args.source]["photos" if photos else "videos"]
    folder.mkdir(parents=True, exist_ok=True)
    added = 0
    for query in queries_from(args):
        candidates = search(query, key) if photos else search(query, key, args.allow_landscape)
        # Portrait first: it needs no cropping.
        candidates.sort(key=lambda c: 0 if c.get("height", 1) > c.get("width", 0) else 1)
        taken = 0
        for item in candidates:
            if taken >= args.per_query:
                break
            if (args.source, item["id"]) in have:
                continue
            if not photos and not (args.min_seconds <= item["duration"] <= args.max_seconds):
                continue
            name = f"{args.source}-{item['id']}.{'jpg' if photos else 'mp4'}"
            size = "" if photos else f" ({item['width']}x{item['height']}{', cropped to 9:16' if item['width'] >= item['height'] else ''}, {item['duration']}s)"
            print(f"{'would get' if args.dry_run else 'getting'} {name}{size} for \"{query}\"")
            taken += 1
            if args.dry_run:
                continue
            download(item["url"], folder / name)
            entry = {"source": args.source, "id": item["id"], "page": item["page"], "creator": item["creator"], "creator_page": item["creator_page"],
                     "licence": LICENCES[args.source], "query": query, "added": date.today().isoformat()}
            if not photos:
                entry.update({"duration_s": item["duration"], "size": f"{item['width']}x{item['height']}"})
                register["counts"].setdefault(name, 0)
            else:
                # The native look centres its text, so every photo joins the "middle" pool (photos/README.md).
                register["positions"].setdefault(name, "middle")
            sources[name] = entry
            have.add((args.source, item["id"]))
            added += 1
            save(sources_path, sources)
            save(register_path, register)
            time.sleep(0.5)
    return added


def reject(names: list[str]) -> None:
    """Takes items out of rotation for good: deletes the file, drops it from the picker, and keeps its source entry
    marked rejected so a later fetch never downloads it again."""
    for name in names:
        photo = name.lower().endswith((".jpg", ".jpeg", ".png"))
        folder = PHOTOS if photo else CLIPS
        sources_path = (PHOTOS.parent if photo else CLIPS) / "sources.json"
        register_path = PHOTOS.parent / "rotation_positions.json" if photo else CLIPS / "clips_usage.json"
        sources, register = load(sources_path, {}), load(register_path, {})
        (folder / name).unlink(missing_ok=True)
        if name in sources:
            sources[name]["rejected"] = date.today().isoformat()
        (register.get("positions") if photo else register.get("counts", {})).pop(name, None)
        save(sources_path, sources)
        save(register_path, register)
        print(f"rejected {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--reject", nargs="+", metavar="FILE", help="Take these files (names in clips/ or photos/rotation/) out of rotation for good")
    parser.add_argument("--source", choices=sorted(SOURCES), default="pixabay")
    parser.add_argument("--query", action="append", help="A search, e.g. \"coffee shop laptop\" (repeatable)")
    parser.add_argument("--preset", action="store_true", help="Also use every query in clips/stock_queries.txt")
    parser.add_argument("--per-query", type=int, default=3, help="How many new items to take per query (default 3)")
    parser.add_argument("--photos", action="store_true", help="Fetch photos for TikTok slides instead of clips")
    parser.add_argument("--allow-landscape", action=argparse.BooleanOptionalAction, default=True,
                        help="Also take landscape clips (cropped to 9:16) when a search has too few portrait ones")
    parser.add_argument("--min-seconds", type=float, default=5)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--dry-run", action="store_true", help="List what would be downloaded; download nothing")
    args = parser.parse_args()
    if args.reject:
        reject(args.reject)
        return
    key = api_key(SOURCES[args.source]["key"])
    added = fetch(args, key)
    print("Dry run: nothing was downloaded." if args.dry_run else f"Added {added} new item(s).")


if __name__ == "__main__":
    sys.exit(main())
