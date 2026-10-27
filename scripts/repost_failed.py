"""Recover a batch post that Postiz marked ERROR. Postiz never retries a failed post, so: re-upload the same rendered
media, recreate the post with the same caption and settings at a new slot, record the failed id in the batch
receipts, then delete the failed copy.

    python scripts/repost_failed.py <post-id>                  # dry run: the piece, its error and the next free slot
    python scripts/repost_failed.py <post-id> --yes            # repost at that slot
    python scripts/repost_failed.py <post-id> --slot 2026-10-29T13:30:00Z --yes

Reposting publishes publicly: pass --yes only after Thomas says to repost (playbook.md, "Recovering a failed post").
Times use this laptop's clock, which is set to Eastern.
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule_batch import CLI, IG, PROJECT, TT, captions, create, ig_settings, postiz, tt_settings, upload  # noqa: E402

GAP = timedelta(hours=2)  # brand.md: never two posts on one app within two hours
LATE_AFTER = timedelta(hours=2)  # a QUEUE post this late is stuck, not mid-way to ERROR (check_post_health.py)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def list_posts(start: datetime, end: datetime) -> list[dict]:
    return postiz("posts:list", "--startDate", iso(start), "--endDate", iso(end))["posts"]


def find(post_id: str):
    for path in sorted((PROJECT / "drafts" / "batches").glob("*.json")):
        spec = json.loads(path.read_text(encoding="utf-8"))
        for p in spec["pieces"]:
            for app in ("ig", "tt"):
                if p.get("receipts", {}).get(app, {}).get("id") == post_id:
                    return path, spec, p, app
    raise SystemExit(f"{post_id} is not in any drafts/batches/*.json receipts; recover it by hand (playbook.md).")


def next_slot(integration: str, now: datetime) -> datetime:
    """Earliest quarter hour at least 30 minutes away, between 8 AM and 11 PM local time, two hours clear of every
    other queued or published post on the same app."""
    taken = [parse(q["publishDate"]) for q in list_posts(now - GAP, now + timedelta(days=3))
             if q["integration"]["id"] == integration and q["state"] != "ERROR"]
    t = (now + timedelta(minutes=30)).replace(second=0, microsecond=0)
    t += timedelta(minutes=-t.minute % 15)
    while not (8 <= t.astimezone().hour < 23 and all(abs(t - d) >= GAP for d in taken)):
        t += timedelta(minutes=15)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("post_id")
    ap.add_argument("--slot", help="UTC time to repost at, e.g. 2026-10-29T13:30:00Z (default: next free slot)")
    ap.add_argument("--yes", action="store_true", help="repost for real (only after Thomas approves it)")
    args = ap.parse_args()

    path, spec, p, app = find(args.post_id)
    r = p["receipts"]
    integration = IG if app == "ig" else TT
    was = parse(r[app]["slot"])
    old = next((q for q in list_posts(was - timedelta(hours=1), was + timedelta(hours=1)) if q["id"] == args.post_id), None)
    if old is None:
        raise SystemExit(f"{args.post_id} is no longer in Postiz (already deleted?). Nothing done.")
    now = datetime.now(timezone.utc)
    stuck = old["state"] == "QUEUE" and now - was > LATE_AFTER
    if old["state"] != "ERROR" and not stuck:
        raise SystemExit(f"{args.post_id} is {old['state']} (due {was:%Y-%m-%d %H:%M} UTC), not failed. Nothing done.")

    folder = PROJECT / "output" / f"batch-{path.stem}" / p["id"]
    ig_caption, tt_caption = captions(p)
    if p["format"] == "reel":
        files = [folder / f"{p['id']}.mp4"]
        settings = ig_settings(p, r["ig"]["audio"]["id"]) if app == "ig" else tt_settings(p, r["tt"]["music"])
    else:
        files = sorted(folder.glob("ig_slide_*.jpg" if app == "ig" else "slide_*.png"))
        settings = ig_settings(p) if app == "ig" else tt_settings(p)
    slot = parse(args.slot) if args.slot else next_slot(integration, now)
    retries = len(r[app].get("failed", []))

    print(f"{p['id']} ({p['format']}) on {'Instagram' if app == 'ig' else 'TikTok'}: {old['state']}, "
          f"due {was.astimezone():%a %b %d %I:%M %p}; error: {old.get('error') or 'none given'}")
    print(f"  already reposted {retries} time(s)" if retries else "  first failure of this post")
    print(f"  media: {', '.join(f.name for f in files) or 'MISSING'}")
    print(f"  repost at {slot.astimezone():%a %b %d %I:%M %p} ({iso(slot)})")
    if retries:
        print("  WARNING: this post already failed once after a repost; playbook.md says not to retry the same "
              "settings a third time. Report it to Thomas instead.")
    if not args.yes:
        print("Dry run: nothing posted. Rerun with --yes once Thomas approves.")
        return
    if retries:
        raise SystemExit("Refusing a third attempt with the same settings.")
    missing = [f for f in files if not f.exists()] if files else [folder]
    if missing:
        raise SystemExit(f"Missing render(s): {missing}. Rebuild with scripts/build_batch.py {path.stem} {p['id']}.")

    new_id = create(integration, ig_caption if app == "ig" else tt_caption, [upload(f) for f in files], iso(slot), settings)
    r[app].setdefault("failed", []).append({"id": args.post_id, "slot": r[app]["slot"], "state": old["state"],
                                             "error": old.get("error")})
    r[app]["id"], r[app]["slot"] = new_id, iso(slot)
    path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Its own Postiz group (one posts:create call per app), so this removes only the failed copy.
    subprocess.run([*CLI, "posts:delete", args.post_id], check=True, capture_output=True, cwd=PROJECT)
    print(f"Reposted as {new_id}; failed copy {args.post_id} deleted; receipts updated in {path.name}.")


if __name__ == "__main__":
    main()
