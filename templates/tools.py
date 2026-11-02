"""Helpers behind ./new.sh img|photo|notes|cs50|readtime|share. Needs Pillow for images (pip install pillow)."""
import math
import datetime
import re
import subprocess
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def convert(src, assets_dir, photo):
    """Save src as WebP under docs/assets/<assets_dir>/ and print the Markdown to paste.

    Screenshots keep their size at quality 90 (small text stays sharp); photos are capped
    at 1200px wide at quality 85.
    """
    from PIL import Image, ImageOps

    src = Path(src).expanduser()
    out_dir = ROOT / "docs" / "assets" / assets_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (src.stem.lower().replace(" ", "-") + ".webp")

    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    if photo and im.width > 1200:
        im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(out, "WEBP", quality=85 if photo else 90, method=6)

    url = "/" + out.relative_to(ROOT / "docs").as_posix()
    print(f"Saved {out.relative_to(ROOT)} ({im.width}x{im.height}, {out.stat().st_size // 1024} KB)\n")
    if photo:
        print("As a cover, in the front matter:")
        print(f"  cover: {url.lstrip('/')}")
        print('  cover_alt: "What the photo shows"\n')
    print("In the page:")
    print(f'  ![Alt text]({url}){{ width="{im.width}" height="{im.height}" loading=lazy }}')


PHOTO_TYPES = {".heic", ".jpg", ".jpeg", ".png", ".webp"}


def open_photo(src):
    """Open a photo upright. HEIC (iPhone) goes through macOS sips first, since Pillow can't read it."""
    from PIL import Image, ImageOps

    if src.suffix.lower() == ".heic":
        tmp = Path(tempfile.mkdtemp()) / (src.stem + ".jpg")
        subprocess.run(["sips", "-s", "format", "jpeg", str(src), "--out", str(tmp)], check=True, capture_output=True)
        src = tmp
    return ImageOps.exif_transpose(Image.open(src)).convert("RGB")


def notes(photos_dir, assets_dir):
    """Turn a folder of notebook photos into the files the hero notes deck expects.

    Photos are taken in name order and saved as page-1.webp, page-2.webp... (1200px wide)
    plus page-N-thumb.webp (360px) for the stack. Returns the number of pages.
    """
    from PIL import Image

    photos = sorted(p for p in Path(photos_dir).expanduser().iterdir() if p.suffix.lower() in PHOTO_TYPES)
    if not photos:
        sys.exit(f"No photos in {photos_dir}")
    out_dir = ROOT / "docs" / "assets" / assets_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, src in enumerate(photos, 1):
        im = open_photo(src)
        if im.width > 1200:
            im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        im.save(out_dir / f"page-{i}.webp", "WEBP", quality=78, method=6)
        im.thumbnail((360, 480))
        im.save(out_dir / f"page-{i}-thumb.webp", "WEBP", quality=72, method=6)
        print(f"  {src.name} -> page-{i}.webp")
    print(f"Saved {len(photos)} pages in {out_dir.relative_to(ROOT)}")
    return len(photos)


def cs50_week(week, angle, photos_dir=None):
    """Start docs/cs-fundamentals/cs50/week-N.md, convert the notebook photos and list it in the sidebar."""
    page = ROOT / "docs" / "cs-fundamentals" / "cs50" / f"week-{week}.md"
    if page.exists():
        sys.exit(f"Already exists: {page.relative_to(ROOT)}")

    notes_block = ""
    if photos_dir:
        pages = notes(photos_dir, f"cs50/week{week}")
        captions = "".join(f'    - "Page {i}"\n' for i in range(1, pages + 1))
        notes_block = f"notes:\n  path: assets/cs50/week{week}\n  pages:\n{captions}"

    text = (ROOT / "templates" / "cs50-week.md").read_text()
    text = text.replace("WEEK", str(week)).replace("ANGLE", angle).replace("NOTES", notes_block)
    text = text.replace("DATE", datetime.date.today().isoformat())
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(text)
    print(f"Created {page.relative_to(ROOT)}")

    # Sidebar: CS Fundamentals > CS50 > Week N (short label; the full title stays on the page)
    nav = ROOT / "docs" / ".nav.yml"
    lines = nav.read_text().splitlines(keepends=True)
    entry = f'      - "Week {week}": cs-fundamentals/cs50/week-{week}.md\n'
    if entry not in lines:
        last = max(i for i, l in enumerate(lines) if "cs-fundamentals/cs50/week-" in l or l.strip() == "- CS50:")
        lines.insert(last + 1, entry)
        nav.write_text("".join(lines))
        print(f"Added Week {week} to docs/.nav.yml")

    url = f"/cs-fundamentals/cs50/week-{week}/"
    print(f"""
Next:
  1. Write the page{" and give each notes page a short caption (alt text)" if photos_dir else ""}.
  2. In docs/cs-fundamentals/index.md, CS50 panel:
     - link the week's topic:   <li class="is-done"><a href="{url}">Topic</a></li>
     - point the button here:   <a class="home-btn track-panel__btn" href="{url}">Latest notes · Week {week}</a>
  3. When done writing: ./new.sh readtime {page.relative_to(ROOT)}
  4. Link preview:       ./new.sh share {page.relative_to(ROOT)}
  Preview: venv/bin/zensical serve""")


FONTS = {  # the site's fonts, from Google Fonts; downloaded once into ~/.cache/codelogium-fonts
    "SpaceGrotesk": "spacegrotesk/SpaceGrotesk%5Bwght%5D.ttf",
    "Inter": "inter/Inter%5Bopsz,wght%5D.ttf",
    "JetBrainsMono": "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}


def font(name, size, weight):
    from PIL import ImageFont
    import urllib.request

    path = Path.home() / ".cache" / "codelogium-fonts" / f"{name}.ttf"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google/fonts/main/ofl/" + FONTS[name], path)
    f = ImageFont.truetype(str(path), size)
    f.set_variation_by_name(weight)
    return f


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width pixels."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and draw.textlength(trial, font=fnt) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    return lines + [line] if line else lines


def share(page):
    """Draw the link preview (1200x630 share.jpg) for a page with a notes deck and set share_image.

    Title, category and description come from the front matter; the lead under the title is
    `share_lead` if set, else the description after its colon, cut to two lines at a comma.
    """
    from PIL import Image, ImageDraw, ImageFilter

    path = Path(page)
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"No front matter in {page}")
    front = m.group(1)

    def field(key):
        f = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', front, re.M)
        return f.group(1) if f else None

    title, notes_path = field("title"), re.search(r"^notes:\n\s+path:\s*(\S+)", front, re.M)
    if not title or not notes_path:
        sys.exit(f"{page} needs a title and a notes: path")
    assets = ROOT / "docs" / notes_path.group(1)
    category = (re.search(r"^categories:\n\s+-\s*(.+)$", front, re.M) or [None, "Codelogium"])[1].strip()

    W, H = 1200, 630
    green, grey, dim = (52, 211, 153), (160, 168, 180), (120, 128, 140)
    im = Image.new("RGB", (W, H), (17, 22, 29))
    d = ImageDraw.Draw(im)
    f_title, f_brand = font("SpaceGrotesk", 70, "Bold"), font("SpaceGrotesk", 30, "Bold")
    f_lead, f_eye = font("Inter", 26, "Regular"), font("JetBrainsMono", 21, "Bold")
    f_url, f_lab = font("JetBrainsMono", 20, "Regular"), font("JetBrainsMono", 16, "Bold")

    d.rectangle([0, 0, W, 8], fill=(14, 122, 96))
    d.text((70, 70), "Codelogium", font=f_brand, fill=(255, 255, 255))
    d.text((70, 152), category.upper(), font=f_eye, fill=green)

    # "CS50 Week 1:" on its own line, then the angle wrapped
    head, _, rest = title.partition(": ")
    title_lines = [head + ":"] + wrap(d, rest, f_title, 700) if rest else wrap(d, title, f_title, 700)
    y = 192
    for line in title_lines[:3]:
        d.text((70, y), line, font=f_title, fill=(255, 255, 255))
        y += 80

    lead = field("share_lead")
    if not lead:
        desc = field("description") or ""
        lead = desc.split(": ", 1)[-1]
        lines = wrap(d, lead, f_lead, 640)
        if len(lines) > 2:  # too long: stop at the last comma that fits in two lines
            cut = " ".join(lines[:2])
            lead = cut[: cut.rfind(",")] + "." if "," in cut else cut
        lead = lead[0].upper() + lead[1:]
    y += 16
    for line in wrap(d, lead, f_lead, 640)[:2]:
        d.text((70, y), line, font=f_lead, fill=grey)
        y += 36
    d.text((70, H - 70), "codelogium.com", font=f_url, fill=dim)

    # Three notebook pages fanned out, like the hero deck
    cx, cy, pw, ph = 960, 330, 250, 333
    for i, ang, dx, dy in [(3, 11, 55, 10), (2, -9, -55, 10), (1, 1, 0, 0)]:
        if not (assets / f"page-{i}.webp").exists():
            continue
        p = Image.open(assets / f"page-{i}.webp").convert("RGB")
        p = p.resize((pw, round(p.height * pw / p.width))).crop((0, 0, pw, ph))
        card = Image.new("RGBA", (pw + 12, ph + 12), (255, 255, 255, 255))
        card.paste(p, (6, 6))
        sh = Image.new("RGBA", (pw + 60, ph + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rectangle([30, 36, pw + 42, ph + 48], fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(14)).rotate(ang, expand=True, resample=Image.BICUBIC)
        r = card.rotate(ang, expand=True, resample=Image.BICUBIC)
        im.paste(sh, (cx + dx - sh.width // 2, cy + dy - sh.height // 2), sh)
        im.paste(r, (cx + dx - r.width // 2, cy + dy - r.height // 2), r)

    # Expand badge (two diagonal arrows) and label
    d = ImageDraw.Draw(im)
    bx, by, dk = cx + 118, cy - 178, (11, 26, 20)
    d.ellipse([bx - 28, by - 28, bx + 28, by + 28], fill=green)
    for s in (1, -1):
        d.line([bx, by, bx + 11 * s, by - 11 * s], fill=dk, width=4)
        d.line([bx + 11 * s, by - 11 * s, bx + 3 * s, by - 11 * s], fill=dk, width=4)
        d.line([bx + 11 * s, by - 11 * s, bx + 11 * s, by - 3 * s], fill=dk, width=4)
    d.text((cx, cy + 225), "MY HANDWRITTEN NOTES", font=f_lab, fill=grey, anchor="mm")

    out = assets / "share.jpg"
    im.save(out, quality=88, optimize=True)
    print(f"Saved {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")

    # Point the link preview at it (instead of the generated social card)
    if not re.search(r"^share_image:", front, re.M):
        rel = out.relative_to(ROOT / "docs").as_posix()
        block = (f"share_image: {rel}   # link preview (LinkedIn, X, WhatsApp) instead of the generated card\n"
                 f'share_image_alt: "{title}, with a stack of handwritten notebook pages"\n'
                 "social:\n  cards: false")
        front = re.sub(r"^notes:", block + "\nnotes:", front, count=1, flags=re.M)
        path.write_text(f"---\n{front}\n---\n" + text[m.end():])
        print(f"Set share_image in {page}")


def readtime(page):
    """Set reading_time in the page's front matter from its word count (200 words a minute)."""
    path = Path(page)
    text = path.read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        sys.exit(f"No front matter in {page}")
    body = text[m.end():]
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    minutes = max(1, math.ceil(len(re.findall(r"\w+", body)) / 200))

    front = m.group(1)
    if re.search(r"^reading_time:", front, re.M):
        front = re.sub(r"^reading_time:.*$", f"reading_time: {minutes}", front, flags=re.M)
    else:
        front += f"\nreading_time: {minutes}"
    path.write_text(f"---\n{front}\n---\n{body}")
    print(f"{page}: reading_time: {minutes}")


def main():
    args = sys.argv[1:]
    usage = "./new.sh img|photo <file> <assets-dir>  or  ./new.sh notes <photos-dir> <assets-dir>  or  ./new.sh readtime|share <page.md>"
    if len(args) == 3 and args[0] in ("img", "photo"):
        convert(args[1], args[2], photo=args[0] == "photo")
    elif len(args) == 3 and args[0] == "notes":
        pages = notes(args[1], args[2])
        print("\nIn the front matter (one short caption per page, used as alt text):")
        print(f"notes:\n  path: assets/{args[2]}\n  pages:")
        for i in range(1, pages + 1):
            print(f'    - "Page {i}"')
    elif len(args) in (3, 4) and args[0] == "cs50":
        cs50_week(args[1], args[2], args[3] if len(args) == 4 else None)
    elif len(args) == 2 and args[0] == "readtime":
        readtime(args[1])
    elif len(args) == 2 and args[0] == "share":
        share(args[1])
    else:
        sys.exit(usage)


if __name__ == "__main__":
    main()
