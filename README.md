# Sidedoor social

The content agent for Sidedoor's Instagram (@sidedoorjobs) and TikTok (@sidedoor.jobs). You talk to Claude Code
in this folder ("make 3 vids"); it writes the on-screen text and captions from `knowledge/`, shows you the copy,
renders Reels and TikTok carousels in Sidedoor's style over your footage, publishes through Postiz, and checks
that each post went live.

**Start here:** `AGENTS.md` (the rules, with "Sidedoor overrides" at the top), then `brand.md` (settings).

## Setting it up on your computer

1. Install [Claude Code](https://claude.com/claude-code), Python 3.10+, Node.js (for the Postiz CLI) and Git.
2. Get this folder onto the computer (clone your private GitHub copy).
3. Open Claude Code in the folder and say: **"read AGENTS.md and set me up"**. It installs what's missing
   (Pillow, ffmpeg, jq, the Postiz CLI), runs `python scripts/check_setup.py`, and walks you through the rest
   one item at a time.
4. Start the Postiz trial at **postiz.com** when you are ready to connect the accounts (the trial is 7 days, so
   have footage ready first). Connect Instagram (it must be a Business account) and TikTok in Postiz, then
   Claude runs `postiz auth:login` and fills in the IDs in `brand.md`.
5. Put footage in `clips/` and photos in `photos/rotation/` (see `photos/README.md`).
6. Ask for **one** video first. Nothing is posted during setup.

## What's yours

`brand.md`, `knowledge/`, `clips/`, `photos/rotation/`, the style guides, and the logs. The rendering scripts,
styles and playbook are the pipeline.

## Credits

The pipeline began as an MIT-licensed template; its licence is kept in `LICENSE` as that licence requires. The
look (styles, Geist font, colours) and all content are Sidedoor's. Geist is under the SIL Open Font License
(`fonts/Geist-OFL.txt`).
