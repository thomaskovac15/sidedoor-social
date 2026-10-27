"""Render a weekly batch from drafts/batches/<date>.json: Reels with build_ig_reel.py, carousels with
generate_slides.py (plus 4:5 crops for Instagram), QA frames, and one preview sheet per piece.

    python scripts/build_batch.py 2026-10-28 [piece-id ...]
"""
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

PROJECT = Path(__file__).resolve().parent.parent
PY = sys.executable
sys.path.insert(0, str(PROJECT / "scripts"))
from build_ig_reel import ffmpeg_executable, get_duration  # noqa: E402

FFMPEG = ffmpeg_executable()
FONT = PROJECT / "fonts" / "TikTokSans[opsz,slnt,wdth,wght].ttf"
STYLES = {
    "hook": "styles/tiktok_question_overlay.json",
    "mistake": "styles/tiktok_mistake_boxed.json",
    "teaching": "styles/tiktok_teaching_boxed.json",
    "cta": "styles/tiktok_cta_boxed.json",
}
CTA_TEXT = "Sidedoor finds people at the companies you want, gets their work email and drafts the note. You press send."
IG_CROP = (0, 285, 1080, 1635)  # centre 4:5 of the 9:16 slide; every text box sits between y 600 and 1300


def line_report(text: str, size: int = 56) -> list[str]:
    font = ImageFont.truetype(str(FONT), size)
    font.set_variation_by_name("SemiBold")
    draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    return [f"{draw.textlength(line, font=font):.0f}px {line!r}" for line in text.split("\n")]


def frame(video: Path, at: float, dest: Path) -> Image.Image:
    subprocess.run([FFMPEG, "-y", "-ss", f"{at:.2f}", "-i", str(video), "-frames:v", "1",
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", str(dest),
                    "-loglevel", "error"], check=True)
    return Image.open(dest).convert("RGB")


def strip(images: list[Image.Image], dest: Path, h: int = 640) -> Path:
    thumbs = [ImageOps.contain(im, (10_000, h)) for im in images]
    gap = 12
    canvas = Image.new("RGB", (sum(t.width for t in thumbs) + gap * (len(thumbs) + 1), h + 2 * gap), (246, 245, 241))
    x = gap
    for t in thumbs:
        canvas.paste(t, (x, gap))
        x += t.width + gap
    canvas.save(dest, quality=88)
    return dest


def build_reel(piece: dict, out: Path) -> list[Image.Image]:
    video = out / f"{piece['id']}.mp4"
    cmd = [PY, str(PROJECT / "scripts" / "build_ig_reel.py"), "--clip", piece["clip"], "--out", str(video)]
    if len(piece["lines"]) == 1:
        cmd += ["--question", piece["lines"][0]]
    else:
        for line in piece["lines"]:
            cmd += ["--beat", line]
    if piece.get("text_y") is not None:
        cmd += ["--text-y", str(piece["text_y"])]
    subprocess.run(cmd, check=True, cwd=PROJECT, capture_output=True)
    duration = get_duration(video, FFMPEG)
    step = duration / len(piece["lines"])
    return [frame(video, step * i + step * 0.5, out / f"qa_beat{i + 1}.jpg") for i in range(len(piece["lines"]))]


def build_carousel(piece: dict, out: Path) -> list[Image.Image]:
    clip = PROJECT / "clips" / piece["hook_clip"]
    still = out / "hook_still.jpg"
    frame(clip, max(0.5, get_duration(clip, FFMPEG) * piece.get("hook_at", 0.35)), still)
    rel = lambda p: str(p.relative_to(PROJECT)).replace("\\", "/")  # noqa: E731
    slides = [{"style": STYLES["hook"], "image": rel(still), "text": {"technical_question": piece["hook"]},
               **({"style_overrides": piece["hook_overrides"]} if piece.get("hook_overrides") else {})}]
    for s in piece["slides"]:
        slide = {"style": STYLES[s["style"]], "image": f"photos/rotation/{s['image']}",
                 "text": {"heading": s["heading"], "body": s["body"]}}
        if s.get("overrides"):
            slide["style_overrides"] = s["overrides"]
        slides.append(slide)
    slides.append({"style": STYLES["cta"], "image": f"photos/rotation/{piece['cta_image']}", "text": {"cta": CTA_TEXT},
                   **({"style_overrides": piece["cta_overrides"]} if piece.get("cta_overrides") else {})})
    spec = out / "spec.json"
    spec.write_text(json.dumps({"slides": slides}, indent=1, ensure_ascii=False), encoding="utf-8")
    for old in out.glob("slide_*.png"):
        old.unlink()
    subprocess.run([PY, str(PROJECT / "scripts" / "generate_slides.py"), "--content", str(spec), "--out", str(out)],
                   check=True, cwd=PROJECT, capture_output=True)
    images = []
    for path in sorted(out.glob("slide_*.png")):
        img = Image.open(path).convert("RGB")
        img.crop(IG_CROP).save(out / f"ig_{path.stem}.jpg", quality=95)
        images.append(img)
    return images


def main():
    batch = sys.argv[1]
    only = set(sys.argv[2:])
    spec = json.loads((PROJECT / "drafts" / "batches" / f"{batch}.json").read_text(encoding="utf-8"))
    for piece in spec["pieces"]:
        if only and piece["id"] not in only:
            continue
        out = PROJECT / "output" / f"batch-{batch}" / piece["id"]
        out.mkdir(parents=True, exist_ok=True)
        texts = piece.get("lines") or [piece["hook"]] + [s["heading"] for s in piece["slides"]]
        for t in texts:
            for row in line_report(t):
                flag = "  <-- may wrap" if int(row.split("px")[0]) > 800 else ""
                print(f"{piece['id']}: {row}{flag}")
        images = build_reel(piece, out) if piece["format"] == "reel" else build_carousel(piece, out)
        print(strip(images, out / "preview.jpg"))


main()
