"""Upload and schedule an approved batch from drafts/batches/<date>.json, recording every Postiz id back into the
file as it goes, so a rerun skips what is already scheduled.

    python scripts/schedule_batch.py 2026-10-28 [piece-id ...]
"""
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
NODE_DIR = Path(shutil.which("postiz") or "postiz").parent
# Called through node directly: the postiz.cmd shim would mangle the newlines in a caption.
CLI = [str(NODE_DIR / ("node.exe" if sys.platform == "win32" else "node")),
       str(NODE_DIR / "node_modules" / "postiz" / "dist" / "index.js")]
IG, TT = "cmvq5a6fv1n4lp71ckmmi3b8t", "cmvq5d5fn1n5fp71c5izluj79"
BRAND = "Sidedoor finds people at the companies you want and gets their work email, with a draft built on what you have in common."
CTA = "Start free at sidedoorjobs.app (link in bio)."
TT_BASE = {"privacy_level": "PUBLIC_TO_EVERYONE", "duet": True, "stitch": True, "comment": True,
           "brand_content_toggle": False, "brand_organic_toggle": True, "video_made_with_ai": False,
           "content_posting_method": "DIRECT_POST"}
USED_IG_AUDIO = {"928037645307668"}
USED_TT_MUSIC = {"7542953496217978897"}


def postiz(*args):
    r = subprocess.run([*CLI, *args], capture_output=True, text=True, encoding="utf-8", cwd=PROJECT)
    if r.returncode != 0:
        raise SystemExit(f"postiz {args[0]} failed ({r.returncode}):\n{r.stderr[-800:]}\n{r.stdout[-800:]}")
    lines = r.stdout.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(("{", "[")):
            return json.loads("\n".join(lines[i:]))
    raise SystemExit(f"no JSON in postiz {args[0]} output:\n{r.stdout[-800:]}")


def upload(path: Path) -> str:
    return postiz("upload", str(path))["path"]


def create(integration, caption, media, slot, settings) -> str:
    out = postiz("posts:create", "-c", caption, "-m", ",".join(media), "-s", slot, "-t", "schedule",
                 "--shortLink", "false", "-i", integration, "--settings", json.dumps(settings, ensure_ascii=False))
    post = out[0] if isinstance(out, list) else out
    return post.get("postId") or post.get("id") or json.dumps(post)[:200]


def main():
    batch = sys.argv[1]
    only = set(sys.argv[2:])
    spec_path = PROJECT / "drafts" / "batches" / f"{batch}.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_root = PROJECT / "output" / f"batch-{batch}"

    every_piece = [q for f in (PROJECT / "drafts" / "batches").glob("*.json")
                   for q in json.loads(f.read_text(encoding="utf-8"))["pieces"]]
    for p in every_piece:
        r = p.get("receipts", {})
        USED_IG_AUDIO.update(x["audio"]["id"] for x in [r.get("ig", {})] if "audio" in x)
        USED_TT_MUSIC.update(x["music"]["id"] for x in [r.get("tt", {})] if isinstance(x.get("music"), dict))

    ig_tracks = [t for t in postiz("integrations:trigger", IG, "audioSearch", "-d", json.dumps({"q": ""}))["output"]
                 if t["id"] not in USED_IG_AUDIO]
    tt_tracks = [t for t in postiz("integrations:trigger", TT, "musicSearch", "-d", json.dumps({"genre": ""}))["output"]
                 if t.get("duration", 0) >= 30000 and t["id"] not in USED_TT_MUSIC]
    random.shuffle(ig_tracks)
    random.shuffle(tt_tracks)

    def save():
        spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for p in spec["pieces"]:
        if only and p["id"] not in only:
            continue
        r = p.setdefault("receipts", {})
        folder = out_root / p["id"]
        ig_caption = f"{p['ig_caption']}\n\n{BRAND}\n{CTA}\n\n{p['ig_tags']}"
        tt_caption = f"{p['tt_tease']}\n{CTA}\n\n{p['tt_tags']}"

        if p["format"] == "reel":
            if "media" not in r:
                r["media"] = [upload(folder / f"{p['id']}.mp4")]
                save()
            if "ig" not in r:
                track = ig_tracks.pop()
                audio = {"id": track["id"], "title": track.get("title"), "artist": track.get("artist")}
                settings = {"post_type": "post", "audio": {"id": track["id"]}}
                if p.get("ig_trial"):
                    # Trial Reel: shown to non-followers first; Instagram shares it with followers if it performs.
                    settings.update({"is_trial_reel": True, "graduation_strategy": "SS_PERFORMANCE"})
                r["ig"] = {"id": create(IG, ig_caption, r["media"], p["ig_slot"], settings),
                           "slot": p["ig_slot"], "audio": audio, "trial_reel": bool(p.get("ig_trial"))}
                save()
            if "tt" not in r:
                track = tt_tracks.pop()
                music = {"id": track["id"], "title": track["title"], "artist": track["artist"], "audio_volume": 60, "video_volume": 0}
                settings = {**TT_BASE, "autoAddMusic": "no", "music": music}
                r["tt"] = {"id": create(TT, tt_caption, r["media"], p["tt_slot"], settings), "slot": p["tt_slot"], "music": music}
                save()
        else:
            if "tt_media" not in r:
                r["tt_media"] = [upload(s) for s in sorted(folder.glob("slide_*.png"))]
                save()
            if "ig_media" not in r:
                r["ig_media"] = [upload(s) for s in sorted(folder.glob("ig_slide_*.jpg"))]
                save()
            if "tt" not in r:
                settings = {**TT_BASE, "autoAddMusic": "yes", "title": p["tt_tease"][:90]}
                r["tt"] = {"id": create(TT, tt_caption, r["tt_media"], p["tt_slot"], settings), "slot": p["tt_slot"],
                           "music": "autoAddMusic"}
                save()
            if "ig" not in r:
                r["ig"] = {"id": create(IG, ig_caption, r["ig_media"], p["ig_slot"], {"post_type": "post"}), "slot": p["ig_slot"]}
                save()
        print(p["id"], "ig", r["ig"]["id"], "tt", r["tt"]["id"])


main()
