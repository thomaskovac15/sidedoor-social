# Clips

Background footage for Reels and the first slide of TikTok carousels. Media files are not stored in Git (they are
large); `sources.json` records where every stock clip came from so it can be fetched again.

## Where footage comes from

1. **Stock (Pixabay; Pexels if they reopen API keys):** `python scripts/fetch_stock.py --preset` pulls clips for
   the searches in `stock_queries.txt` (portrait first; landscape ones are cropped to 9:16) and registers them;
   add `--photos` for TikTok slide photos. Free for social media marketing, no credit needed. Both licences forbid
   misleading uses, so stock people only carry the job seeker's point of view, never Sidedoor's pitch. Keep pulls
   small (about 3 per search); Pixabay forbids systematic mass downloads, and Mixkit forbids scripted downloads
   entirely (pick Mixkit clips by hand only).
2. **Your own:** short vertical clips from your phone (5 to 15 seconds): a laptop on a kitchen table, a coffee
   shop, a walk, a screen recording of Sidedoor. Drop them here and add each filename to `clips_usage.json` at 0
   (or ask Claude to).
3. **People on camera** (you, friends with their OK, or paid creators): talking-to-camera clips. These keep their
   own sound; see `AGENTS.md`.

Never use other creators' videos.
