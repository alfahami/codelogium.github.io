"""Helpers behind ./new.sh img|photo|notes|readtime. Needs Pillow for images (pip install pillow)."""
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
  Preview: venv/bin/zensical serve""")


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
    usage = "./new.sh img|photo <file> <assets-dir>  or  ./new.sh notes <photos-dir> <assets-dir>  or  ./new.sh readtime <page.md>"
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
    else:
        sys.exit(usage)


if __name__ == "__main__":
    main()
