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
- State check: NOT PUBLIC. Postiz shows PUBLISHED with no error and emailed Thomas that it posted, but TikTok returned no video link (releaseURL is the bare profile URL; releaseId `v_pub_url~v2.7701478547940263949`), `posts:missing` returned nothing, and at 01:10Z Oct 28 the public profile showed 0 videos (account public). Thomas doesn't see it in the app either. Asked him to check the TikTok app's notifications for a review or rejection message. check_post_health.py now flags this case as NOT PUBLIC. Resolved: the same video was re-sent to his inbox (`cmvrg2awh45w7p71cgualkg96`, PUBLISHED 01:40Z Oct 28, inbox delivery) and Thomas posted it from the app.

## 2026-10-27 - TikTok switched to inbox drafts

- Cause: the first TikTok (direct post) came back PUBLISH_COMPLETE with no public post id and never appeared. TikTok's
  public profile data lists @sidedoor.jobs as a personal account (commerceUser false), and Postiz cloud posts every
  TikTok through TikTok's business API. Thomas tried to switch to a Business account and was asked for IRS/EIN
  documents, so we don't use one.
- Test: the same video sent with `content_posting_method: UPLOAD` (`cmvrg2awh45w7p71cgualkg96`, 01:40Z) reached his
  inbox (releaseURL `tiktok.com/messages#v_inbox_url~...`). He added the caption and posted it from the app; the
  public profile then showed 1 video. The inbox draft arrived without the caption.
- All 15 week-1 TikToks switched to UPLOAD with `posts:settings` and read back as UPLOAD, QUEUE. TikTok ignores
  their music settings now; Thomas picks a sound in the app.
- Captions to paste: TikTok Captions page https://claude.ai/artifact/C7TvcWWztGkA3aJkqcQKue (built by
  `scripts/tiktok_caption_page.py`). New batches default to UPLOAD (`TT_BASE` in schedule_batch.py).

## 2026-10-28 to 2026-11-01 - Week 1 batch (10 pieces, 20 posts)

- Copy approved by Thomas in chat (2026-10-27). Spec, Postiz IDs, uploads and music per post: `drafts/batches/2026-10-28.json`
- Daily: piece a = Instagram 11:30 AM then TikTok 6:30 PM; piece b = TikTok 12:30 PM then Instagram 7:30 PM (Sun Nov 1 in EST)
- Carousels: TikTok gets the 9:16 slides with autoAddMusic; Instagram gets 4:5 centre crops, no music (Postiz attaches audio to Reels only)
- QA: every frame and slide viewed; text moved off faces (wed-a y 260, thu-a y 1240, three slides y 1160-1240); bright photos swapped for dark ones
- All 20 read back from posts:list in QUEUE at the right slots; no music repeated
- State check: (pending; check_post_health.py after each day)
  - wed-a (reel): IG `cmvr2g16p37r2p71c2qtxnd6s`, TikTok `cmvr2g25637r3p71cvys3aeu0` → IG PUBLISHED https://www.instagram.com/reel/DfCwqNUivHV/ ; TikTok sent to inbox
  - wed-b (carousel): IG `cmvr2hf0037s0p71chw1b2min`, TikTok `cmvr2he1l3l2lpi1cbv5hvrq1` → IG PUBLISHED https://www.instagram.com/p/DfDnd8-jzQK/ ; TikTok sent to inbox
  - thu-a (reel): IG `cmvr2ii3a37sqp71cy4mku9d1`, TikTok `cmvr2iizs37srp71csjruhq7c` → IG PUBLISHED https://www.instagram.com/reel/DfFVbadk6-X/ ; TikTok sent to inbox
  - thu-b (reel): IG `cmvr2im593l65pi1c5xc1wbpa`, TikTok `cmvr2in4837svp71cxuubxbg9` → IG PUBLISHED https://www.instagram.com/reel/DfGMXI2DAj4/ ; TikTok sent to inbox
  - fri-a (reel): IG `cmvr2iqlq3l6ipi1cq1llx8pv`, TikTok `cmvr2irm137swp71cd42uutcl` → IG PUBLISHED https://www.instagram.com/reel/DfH6WUYgNXB/ ; TikTok sent to inbox
  - fri-b (carousel): IG `cmvr2ja3k3l88pi1cpdg6on9j`, TikTok `cmvr2j92d3l83pi1ctovu3zc5` → IG PUBLISHED https://www.instagram.com/p/DfIxFtjHROh/ ; TikTok sent to inbox
  - sat-a (reel): IG `cmvr2jcof37tcp71cvst2g7vr`, TikTok `cmvr2jdiv37tdp71cwbxatiok`
  - sat-b (reel): IG `cmvr2jgex37tgp71c5fn0wwkc`, TikTok `cmvr2jhc537thp71crdft9npl`
  - sun-a (reel): IG `cmvr2jjsv3l8vpi1c3svw70vq`, TikTok `cmvr2jkpa3l8ypi1cfg71s7c4`
  - sun-b (carousel): IG `cmvr2jz153la3pi1cnxkdbtga`, TikTok `cmvr2jxse37tup71cmwrovxc5`

## 2026-10-28 to 2026-11-01 - Week 1 extras (5 pieces, 10 posts)

- Copy approved by Thomas in chat (2026-10-27): "post more during the trial". Spec and receipts: `drafts/batches/2026-10-28-extra.json`
- Daily 9:00 PM ET: TikTok (third of the day) plus the same video as an Instagram Trial Reel (is_trial_reel, graduation SS_PERFORMANCE)
- QA: thu-x clip swapped to 83875 with text at y 1240; fri-x text at y 1240 (was over the eyes)
- All 30 posts of the week read back in QUEUE; no track repeated across both batches
- State check: (pending; check_post_health.py after each day)
  - wed-x: IG Trial Reel `cmvr3fn9038mkp71cymyed0nz`, TikTok `cmvr3fogt3nippi1c2rrir06m` → IG FAILED (ERROR "This account doesn't support Trial Reels"), not reposted, waiting on Thomas; TikTok sent to inbox
  - thu-x: IG Trial Reel `cmvr3gir638mvp71ccbqq28g9`, TikTok `cmvr3gjtn3nl6pi1csus4nhjw` → IG Trial Reel replaced (see below); TikTok sent to inbox
  - fri-x: IG Trial Reel `cmvr3gm5e38mzp71cz7bk4l98`, TikTok `cmvr3gnfm38n1p71cq1wcqilj` → IG Trial Reel replaced (see below); TikTok sent to inbox
  - sat-x: IG Trial Reel `cmvr3gviz3nlmpi1crsgalv2g`, TikTok `cmvr3gxn63nlrpi1cona17so5`
  - sun-x: IG Trial Reel `cmvr3h23638ndp71co0v81vay`, TikTok `cmvr3h3fj38nfp71c65f6qg49`
- 2026-10-29: Instagram doesn't offer Trial Reels to @sidedoorjobs yet. Approved by Thomas: all five became normal Reels
  (same video, caption and audio). The old Trial Reel posts were deleted in Postiz; receipts keep them under `replaced`.
  - wed-x: IG Reel `cmvtot34b2xgvor1cakfhpxxy`, Thu Oct 29 3:00 PM (make-up for the failed one) → IG PUBLISHED https://www.instagram.com/reel/DfFtgdmDdsq/
  - thu-x: IG Reel `cmvtotguy2aavpg1cvuxu1svd`, Thu Oct 29 9:30 PM → IG PUBLISHED https://www.instagram.com/reel/DfGZ-OaFxi7/
  - fri-x: IG Reel `cmvtotk2r2xhtor1cf6md1gsf`, Fri Oct 30 9:30 PM → IG PUBLISHED https://www.instagram.com/reel/DfI-zo7AhFx/
  - sat-x: IG Reel `cmvtotnyy2ab9pg1ch99x8xmv`, Sat Oct 31 9:30 PM
  - sun-x: IG Reel `cmvtott0v2abgpg1crbye9vuh`, Sun Nov 1 9:30 PM EST
  - Read back: no Trial Reels left; 12 Instagram audio posts, 12 different tracks
