"""Write output/tiktok-captions.html: one card per TikTok inbox draft with its arrival time, the video's first
on-screen line (to recognise it) and a one-tap copy of its caption and hashtags. Thomas keeps it open on his phone
and posts each draft from the TikTok app. Republish it to the same Artifact URL after each batch (playbook.md).

    python scripts/tiktok_caption_page.py 2026-10-28 2026-10-28-extra
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schedule_batch import PROJECT, captions  # noqa: E402

TEMPLATE = r"""<title>TikTok Captions</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Figtree:wght@400;500;600&display=swap">
<style>
/* One column of drafts in arrival order, grouped by day; the caption block and its copy button are the point. */
:root {
  --bg: #f3f5f4; --surface: #ffffff; --ink: #141917; --muted: #5a6560; --line: #dbe1de;
  --accent: #0b7a62; --on-accent: #ffffff;
  --due-bg: #fff1d6; --due-ink: #8a5300; --done-ink: #4e6b61;
  --display: "Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --body: "Figtree", "Segoe UI", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0e1211; --surface: #161b1a; --ink: #e9eeec; --muted: #9aa8a2; --line: #29312e;
  --accent: #3fc7a3; --on-accent: #06221b; --due-bg: #3a2908; --due-ink: #ffc46b; --done-ink: #86a59a; color-scheme: dark;
} }
:root[data-theme="dark"] {
  --bg: #0e1211; --surface: #161b1a; --ink: #e9eeec; --muted: #9aa8a2; --line: #29312e;
  --accent: #3fc7a3; --on-accent: #06221b; --due-bg: #3a2908; --due-ink: #ffc46b; --done-ink: #86a59a; color-scheme: dark;
}
body { background: var(--bg); color: var(--ink); font: 400 16px/1.5 var(--body); }
main { max-width: 34rem; margin: 0 auto; padding-block: 24px 48px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 28px; }
h1 { font: 700 1.75rem/1.15 var(--display); margin: 0; text-wrap: balance; }
h2 { font: 600 0.8rem/1 var(--body); text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin: 0; }
.lede { margin: 6px 0 0; color: var(--muted); }
ol.steps { margin: 0; padding: 14px 16px 14px 34px; background: var(--surface); border: 1px solid var(--line);
  border-radius: 12px; display: grid; gap: 4px; }
ol.steps li::marker { color: var(--accent); font-weight: 600; }
.day { display: grid; gap: 12px; }
.card { background: var(--surface); border: 1px solid var(--line); border-radius: 14px; padding: 16px;
  display: grid; gap: 12px; min-width: 0; }
.card.posted { opacity: 0.6; }
.card.posted .caption, .card.posted .copy { display: none; }
.meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
.time { font: 600 1.05rem/1 var(--display); font-variant-numeric: tabular-nums; }
.kind { font-size: 0.85rem; color: var(--muted); }
.chip { margin-left: auto; font-size: 0.78rem; font-weight: 600; padding: 4px 10px; border-radius: 999px;
  border: 1px solid var(--line); color: var(--muted); }
.chip.due { background: var(--due-bg); color: var(--due-ink); border-color: transparent; }
.chip.done { color: var(--done-ink); }
.cue { margin: 0; font-weight: 600; text-wrap: balance; }
.cue::before { content: "On screen: "; font-weight: 400; color: var(--muted); }
.caption { margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; padding: 12px; border-radius: 10px;
  background: var(--bg); border: 1px dashed var(--line); font-size: 0.95rem; }
.actions { display: flex; gap: 8px; flex-wrap: wrap; }
button { font: 600 0.95rem/1 var(--body); border-radius: 10px; padding: 12px 16px; cursor: pointer;
  border: 1px solid var(--line); background: var(--surface); color: var(--ink); }
button.copy { flex: 1 1 12rem; background: var(--accent); color: var(--on-accent); border-color: transparent; }
button:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
.note { font-size: 0.85rem; color: var(--muted); margin: 0; }
</style>

<main>
  <header>
    <h1>TikTok captions</h1>
    <p class="lede" id="summary">Each video arrives in your TikTok inbox at the time shown.</p>
  </header>
  <ol class="steps">
    <li>Open the new draft from your TikTok inbox.</li>
    <li>Tap <b>Copy caption</b> on its card below.</li>
    <li>Paste it into the description.</li>
    <li>Optional: tap <b>Add sound</b> and pick a trending one.</li>
    <li>Post, then tap <b>Mark posted</b> here.</li>
  </ol>
  <div id="days"></div>
  <p class="note">Post each draft the same day it arrives; TikTok may clear inbox drafts after about a day. Times are Eastern.</p>
</main>

<script>
const POSTS = __DATA__;
const tz = "America/New_York";
const dayFmt = new Intl.DateTimeFormat("en-US", { timeZone: tz, weekday: "long", month: "short", day: "numeric" });
const timeFmt = new Intl.DateTimeFormat("en-US", { timeZone: tz, hour: "numeric", minute: "2-digit" });
const store = {
  get(k) { try { return localStorage.getItem(k); } catch { return null; } },
  set(k, v) { try { v === null ? localStorage.removeItem(k) : localStorage.setItem(k, v); } catch {} },
};

function render() {
  const now = Date.now();
  const days = document.getElementById("days");
  days.replaceChildren();
  let waiting = 0, firstOpen = null;
  const groups = new Map();
  for (const p of [...POSTS].sort((a, b) => a.slot.localeCompare(b.slot))) {
    const key = dayFmt.format(new Date(p.slot));
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(p);
  }
  for (const [day, posts] of groups) {
    const section = document.createElement("section");
    section.className = "day";
    const h = document.createElement("h2");
    h.textContent = day;
    section.append(h);
    for (const p of posts) {
      const t = new Date(p.slot).getTime();
      const posted = store.get("posted:" + p.id) === "1";
      const arrived = t <= now;
      if (arrived && !posted) waiting++;
      const card = document.createElement("article");
      card.className = "card" + (posted ? " posted" : "");
      const chip = posted ? ["done", "Posted"] : arrived ? ["due", "In your inbox"] : ["", "Arrives later"];
      card.innerHTML = `
        <div class="meta"><span class="time"></span><span class="kind"></span><span class="chip ${chip[0]}"></span></div>
        <p class="cue"></p>
        <p class="caption"></p>
        <div class="actions"><button class="copy" type="button">Copy caption</button><button class="mark" type="button"></button></div>`;
      card.querySelector(".time").textContent = timeFmt.format(new Date(p.slot));
      card.querySelector(".kind").textContent = p.kind;
      card.querySelector(".chip").textContent = chip[1];
      card.querySelector(".cue").textContent = p.cue;
      const cap = card.querySelector(".caption");
      cap.textContent = p.caption;
      const copy = card.querySelector(".copy");
      copy.addEventListener("click", () => {
        const done = () => { copy.textContent = "Copied"; setTimeout(() => (copy.textContent = "Copy caption"), 1600); };
        const fallback = () => {
          const r = document.createRange(); r.selectNodeContents(cap);
          const s = getSelection(); s.removeAllRanges(); s.addRange(r);
          copy.textContent = "Selected: tap Copy";
        };
        navigator.clipboard?.writeText(p.caption).then(done, fallback) ?? fallback();
      });
      const mark = card.querySelector(".mark");
      mark.textContent = posted ? "Undo" : "Mark posted";
      mark.addEventListener("click", () => { store.set("posted:" + p.id, posted ? null : "1"); render(); });
      if (!posted && !firstOpen && (arrived || t - now < 18 * 3600e3)) firstOpen = card;
      section.append(card);
    }
    days.append(section);
  }
  document.getElementById("summary").textContent = waiting
    ? `${waiting} draft${waiting > 1 ? "s" : ""} waiting in your TikTok inbox.`
    : "Nothing waiting right now. Each video arrives in your TikTok inbox at the time shown.";
  return firstOpen;
}
const first = render();
first?.scrollIntoView({ block: "center" });
</script>
"""


def main():
    posts = []
    for batch in sys.argv[1:]:
        spec = json.loads((PROJECT / "drafts" / "batches" / f"{batch}.json").read_text(encoding="utf-8"))
        for p in spec["pieces"]:
            cue = (p.get("lines") or [p.get("hook")])[0]
            posts.append({"id": p["id"], "slot": p["receipts"]["tt"]["slot"],
                          "kind": "Video" if p["format"] == "reel" else "Photo carousel",
                          "cue": " ".join(cue.split()), "caption": captions(p)[1]})
    out = PROJECT / "output" / "tiktok-captions.html"
    data = json.dumps(posts, ensure_ascii=False).replace("</", "<\\/")
    out.write_text(TEMPLATE.replace("__DATA__", data), encoding="utf-8")
    print(out, len(posts), "posts")


if __name__ == "__main__":
    main()
