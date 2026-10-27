# Your settings

**This is the only file you need to edit to make this agent yours.** The rules that make it Sidedoor's are in
"Sidedoor overrides" at the top of `AGENTS.md`. Content lives in `knowledge/`, `clips/`, `photos/rotation/` and
the style guides.

---

## Autopilot

```
autopilot: off
```

**`off`**: the agent writes the on-screen text and captions and shows them to you in the chat first. You approve
or edit the wording; then it renders and publishes real public posts without asking again.

**`on`**: it skips the copy approval and publishes on its own. Only turn this on after a few weeks of output you
would have posted yourself.

## Brand

| Field | Value |
|---|---|
| Brand name | `Sidedoor` |
| Website | `sidedoorjobs.app` |
| Instagram | `@sidedoorjobs` (https://www.instagram.com/sidedoorjobs/) |
| TikTok | `@sidedoor.jobs` (https://www.tiktok.com/@sidedoor.jobs) |

## Connected Postiz integrations

From `postiz integrations:list` (2026-10-27). Never post to an integration ID that is not in this table. The X
account Postiz also shows (@sidedoor_jobs) is not used by this agent.

| Platform | Integration ID | Profile |
|---|---|---|
| Instagram (Facebook Business connection: Reel music works) | `cmvq5a6fv1n4lp71ckmmi3b8t` | `sidedoorjobs` |
| TikTok (TikTok Business account) | `cmvq5d5fn1n5fp71c5izluj79` | `sidedoor.jobs` |
| LinkedIn | Not used | Not used |
| X | Not used | Not used |

## Posting schedule

Thomas, 2026-10-25: 2 to 3 posts a day at the times people are most active. No time makes a post go viral on
its own; the first hour's watch time and shares decide reach. After two weeks, move the slots to the hours each
app's analytics show the followers are online. Never two TikToks within two hours of each other.

| Field | Value |
|---|---|
| Timezone | `America/New_York` |
| Instagram slots per day | `11:30 AM, 7:30 PM` |
| TikTok slots per day | `12:30 PM, 6:30 PM, 9:00 PM` |
| Instagram Trial Reel (extra, non-followers only) | `9:00 PM` (the 9:00 PM TikTok's video; graduates to followers if it performs) |

## Topic scope

**In bounds**:

- How hard the job search is now: cold applying, silence, rejections, how many people apply for each job.
- Referrals and connections versus cold applications, with sourced numbers.
- What the search costs, LinkedIn Premium included (wording from knowledge/job-market-facts.md section 5).
- How to reach people at a company: alumni, former colleagues, a short note built on common ground.
- What Sidedoor does, in Sidedoor's own voice, from `knowledge/sidedoor.md`.

**Out of bounds** (never, even if `knowledge/` mentions them):

- Anyone saying Sidedoor helped them, got them hired, or got them replies, unless it is a real, named user who
  agreed in writing (kept in `knowledge/`).
- Promises or odds of getting a job, interviews or replies through Sidedoor.
- Naming or criticising a specific company's hiring, or any person. LinkedIn only by its published price and
  features, stated as fact, without its logo.
- Competitors by name, politics, layoffs news.
- AI-generated people, faces or voices.

**Standing topic list** (topics already covered, so you don't repeat yourself). Add a line per published topic:

- (none yet)

## Fixed copy

Written once, reused verbatim on every post. Proposed; confirm before the first batch.

| Where | Your wording |
|---|---|
| Caption brand line (second to last line of every caption) | `Sidedoor finds people at the companies you want and gets their work email, with a draft built on what you have in common.` |
| Caption CTA (final line of every caption) | `Start free at sidedoorjobs.app (link in bio).` |
| TikTok closing slide text | `Sidedoor finds people at the companies you want, gets their work email and drafts the note. You press send.` |

No on-screen label, watermark or swipe prompt: the native look (2026-10-25, v2) is text the way people type it
in the app. The handle already shows in the app around every post.
