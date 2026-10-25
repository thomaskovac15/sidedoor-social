# Instagram Reel Style Guide (Sidedoor)

"Sidedoor overrides" at the top of `AGENTS.md` win over anything here.

## Audience and positioning

- **Audience:** people looking for a job in the US: students after an internship or a first job, early-career
  people after their next one, and career switchers. Tired of applying online and hearing nothing back.
- **Channel focus:** the job search as it really is now, and why reaching a person beats one more cold application.
- **Who is speaking, in two voices:**
  1. **The job seeker** (on-screen statement, TikTok middle slides, the caption's opening lines): first person or
     "you", POV style, about the search itself. Never mentions Sidedoor. Never claims a result.
  2. **Sidedoor** (TikTok closing slide, the caption's brand line and CTA): the brand speaking as itself about
     what it does, using only `knowledge/sidedoor.md`.
- **No persona.** There is no named or implied individual behind the account. Never invent a person, employer,
  title, school or number of applications.
- **Topic mix for a normal week** (about 14 Reels): 5 cold applying vs referrals, 4 how hard the search is now
  (real stories in `knowledge/your-stories.md`, sourced numbers), 3 how to reach people at a company, 2 what the
  search costs. Vary the angle; don't run the same pillar twice in a row.

## Reel format

1. A clip from `clips/` plays full screen behind the text.
2. **Series label** (`brand_tag`): always `THE JOB SEARCH, HONESTLY` (from `brand.md`). A teal card at the top.
3. **Statement** (`technical_question`, the legacy name): the POV line. An ink card, left-aligned, lower half.
4. **Footer** (`caption_below`): `sidedoorjobs.app`. Set by the build script; no prompt like "caption below".
5. The caption carries the substance; the statement makes someone stop and read it.

## Statement rules

- One idea, at most **3 lines** at the fixed 62px size (about 26 characters a line). Shorten it; never shrink the
  font.
- Write it as the job seeker: "POV: …", "When you …", "You've …", "Nobody tells you …".
- A number must be from `knowledge/job-market-facts.md` and shown as the source states it. Keep a number on one
  line with an explicit line break (`\n`), e.g. `Applied on the careers site:\n1 in 152 got hired.`
- No hyphens, en dashes or em dashes on screen. No emoji on screen.
- Never mention Sidedoor in the statement.

## Caption format

```
<line 1: the hook, restating the statement in the job seeker's voice>

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

- The label, statement card and footer don't overlap each other or a face in the clip.
- The statement card spans the box; no line ends with a dangling single word if a rewrite avoids it.
- Colours, font and positions are exactly as `styles/ig_question_overlay.json` renders them. No overrides.

Build with:

```bash
python scripts/build_ig_reel.py \
  --clip <filename in clips/> \
  --brand-tag "THE JOB SEARCH, HONESTLY" \
  --question "<statement, with \n for forced line breaks>" \
  --out output/<name>/<name>.mp4
```

(`python3` on Mac or Linux.)

## Approved statement bank

Every entry must be backed by `knowledge/`. Add to it as topics prove out. Unconfirmed facts stay out until
`knowledge/job-market-facts.md` marks them confirmed.

1. `Applied on the careers site:\n1 in 152 got hired.\nReferred: 1 in 16.`
   Source: Lever via SHRM (2016). Caption: the study, and why a referral changes the odds.
2. `POV: you find out 54% of\nworkers got their job\nthrough a connection.`
   Source: MyPerfectResume survey via HR Dive (2025).
3. `About 1 in 4 external hires\ncomes from an employee referral.`
   Source: CareerXroads Source of Hire (confirm the year before posting).
4. `Nobody tells you the people\nwho can refer you are\nalready at your school.`
   Backed by `knowledge/sidedoor.md` (search by school or past employer). Caption: how to find alumni at a
   company and what a short note looks like.
