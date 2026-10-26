# Instagram Reel Style Guide (Sidedoor)

"Sidedoor overrides" at the top of `AGENTS.md` win over anything here.

## Audience and positioning

- **Audience:** people looking for a job in the US: students after an internship or a first job, early-career
  people after their next one, and career switchers. Tired of applying online and hearing nothing back.
- **Channel focus:** the job search as it really is now, and why reaching a person beats one more cold application.
- **Who is speaking, in two voices:**
  1. **The job seeker** (the on-screen text, TikTok middle slides, the caption's opening lines): first person or
     "you", POV style, about the search itself. Never mentions Sidedoor. Never claims a result.
  2. **Sidedoor** (TikTok closing slide, the caption's brand line and CTA): the brand speaking as itself about
     what it does, using only `knowledge/sidedoor.md`.
- **No persona.** There is no named or implied individual behind the account. Never invent a person, employer,
  title, school or number of applications.
- **Topic mix for a normal week** (about 14 Reels): 5 cold applying vs referrals, 4 how hard the search is now
  (`knowledge/your-stories.md` and sourced numbers), 3 how to reach people at a company, 2 what the search costs.
  Vary the angle; don't run the same pillar twice in a row.

## Formats and the weekly mix

Rotate formats so the feed never looks like one template. Per week, across both apps (about 35 posts):

| Format | Where | How | Share |
|---|---|---|---|
| **One-line POV Reel** | Instagram, then the same video on TikTok | `build_ig_reel.py --question` | about 35% |
| **Multi-beat Reel**: the line changes 2 to 4 times (setup, turn, payoff) | Instagram, then TikTok | `build_ig_reel.py --beat … --beat …` (2.5 s a beat at least) | about 25% |
| **Carousel**: hook, 2 to 4 points, Sidedoor's closing slide | TikTok photo post, and the same slides as an Instagram carousel | `generate_slides.py` (see `tiktok/style_guide.md`) | about 30% |
| **Talking to camera** (a real person; their own sound) | both | when such clips exist in `clips/` (see `clips/README.md`) | the rest, growing |

A video made for Instagram also goes to TikTok (a different day or slot), and a TikTok carousel also goes to
Instagram as a carousel. Different clip and hook each time; never the same clip twice in one day.

## Reel format: POV over real footage

1. A clip from `clips/` plays full screen: a real person somewhere ordinary (home, coffee shop, a walk, a desk).
2. One line of on-screen text, typed-in-the-app style (TikTok Sans, white, dark outline, centred, upper middle).
   Nothing else on screen: no label, card, logo or web address.
3. Music is attached at posting time (see `AGENTS.md`).
4. The caption carries the substance; the on-screen line makes someone stop and read it.

## On-screen line rules

- One idea, at most **4 lines** at the fixed 56px size (about 24 characters a line). Shorten it; never shrink the
  font.
- Sentence case, the way people type: "POV: …", "when you …", "nobody tells you …", "me after …". Lowercase
  starts are fine. No full stop at the end of a one-liner.
- A number must be from `knowledge/job-market-facts.md` with status `confirmed`. Keep a number on one line with an
  explicit line break (`\n`), e.g. `applied on the careers site:\n1 in 152 got hired`.
- No hyphens, en dashes or em dashes. At most one emoji, and only if it reads naturally.
- Never mention Sidedoor on screen in a POV Reel.

## Caption format

```
<line 1: the hook, in the job seeker's voice>

<2 to 4 short lines: the substance, from knowledge/ only. When a number is used, name the source and year in
plain words, e.g. "(Lever data on 4M+ candidates, via SHRM, 2016)".>

<brand line from brand.md, verbatim>
<CTA from brand.md, verbatim>

#jobsearch #jobhunting #networking #referrals #careeradvice
```

- 3 to 5 hashtags, from: #jobsearch #jobhunting #networking #referrals #careeradvice #newgrad #internship
  #careerchange #hiring #jobtips. Vary them.
- No @-mentions, no links other than the CTA's site name.

## Visual QA (every Reel)

- The text doesn't cover a face, and stays clear of the top bar, the right-hand buttons and the bottom caption area.
  If a face sits where the text goes, move the text with `--text-y` (top edge in pixels: about 260 to sit above
  a face, about 1240 to sit below it; never below 1300, where the app's caption covers it). On TikTok slides do
  the same with `"style_overrides": {"technical_question": {"y": 1240}}` in that slide's spec.
- It reads easily on that clip (bright backgrounds need the outline; pick another clip if it still doesn't).
- Font, size and position exactly as `styles/ig_question_overlay.json` renders them. No overrides.

Build with:

```bash
python scripts/build_ig_reel.py \
  --clip <filename in clips/> \
  --question "<on-screen line, with \n for forced line breaks>" \
  --out output/<name>/<name>.mp4
```

(`python3` on Mac or Linux; on this Windows laptop use `.venv\Scripts\python`.)

## Approved pairing bank

Every entry must be backed by `knowledge/`. Add to it as topics prove out.

1. `applied on the careers site:\n1 in 152 got hired.\nreferred: 1 in 16`
   Source: Lever via SHRM (2016). Caption: the study, and why a referral changes the odds.
2. `POV: you realise 54% of people\ngot their job through\nsomeone they know`
   Source: MyPerfectResume survey via HR Dive (2025).
3. `cold applying in 2026 feels like\nsending your resume into the void`
   Source: Thomas's view in `knowledge/your-stories.md`. Caption: the Lever numbers.
4. `nobody tells you the people\nwho can refer you\nwent to your school`
   Backed by `knowledge/sidedoor.md` (search by school or past employer). Caption: how to find alumni at a
   company and what a short note looks like.
5. `POV: you're paying $50+ a month\nfor LinkedIn Premium\nand still hearing nothing`
   Source: `knowledge/job-market-facts.md` section 5 (use its wording; add "prices vary by plan" in the caption).
