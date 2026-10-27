# Content Agent — Drafts Log

Running log of what's been drafted/posted and its Postiz post ID. One dated
entry per batch/change, newest at the bottom — see `playbook.md` for the
full workflow this log documents.

Empty out of the box. Start logging from your first batch.

## Entry format

Copy this block for each batch:

```
## YYYY-MM-DD - <short batch description>

- Platform: Instagram (`@<your-handle>`, `<integration name>`)
- Postiz post IDs: `<id>`, `<id>`, `<id>`
- Clip / photo used, highlight color, audio track per post
- QA notes: what you visually verified before upload
- State check: confirm each post left `QUEUE` and reached `PUBLISHED`
- Receipts: `drafts/batches/YYYY-MM-DD.json`
```

## 2026-10-27 - First post (Instagram Reel, one-line POV)

- Platform: Instagram (`@sidedoorjobs`, Postiz `cmvq5a6fv1n4lp71ckmmi3b8t`)
- Postiz post ID: `cmvqqst8q2kh7p71cqse8qo0y`, scheduled 2026-10-27 11:30 AM ET (15:30Z), state QUEUE at creation
- Clip: `pixabay-42305.mp4` (man at a monitor, from behind); audio: Friend Forever (Instrumental), Charlie Peacock (`928037645307668`, random from audioSearch)
- On screen: "applied on the careers site: / 1 in 152 got hired. / referred: 1 in 16" (Lever via SHRM, 2016); caption approved by Thomas in chat
- QA notes: frame at 3 s checked: text over the back of the head, no face covered, clear of the app UI
- State check: PUBLISHED 15:34Z (4 min after the slot): https://www.instagram.com/reel/DfALt_mnJfr/ . Public embed shows the portrait video, the "Charlie Peacock · Friend Forever (Instrumental)" credit and the full caption.

## 2026-10-27 - First post, TikTok cross-post (same video)

- Platform: TikTok (`@sidedoor.jobs`, Postiz `cmvq5d5fn1n5fp71c5izluj79`, TikTok Business)
- Postiz post ID: `cmvqursyw306upi1crra00pfw`, scheduled 2026-10-27 6:30 PM ET (22:30Z), state QUEUE at creation
- Media: `output/first-post/reel_42305.mp4`, uploaded fresh (`https://uploads.postiz.com/lYF8a1yUDS.mp4`)
- Music: O Peso do Amor Calado, Alexandro Bezerra de Araujo (`7542953496217978897`, random from musicSearch among tracks of 30 s or more), audio_volume 60, video_volume 0
- Settings: DIRECT_POST, PUBLIC_TO_EVERYONE, brand_organic_toggle true ("Your brand"), video_made_with_ai false; stored settings confirmed with posts:list
- Caption: `output/first-post/caption_tiktok.txt`, approved by Thomas in chat
- State check: (pending; verify it reaches PUBLISHED after the slot)
