"""Helpers behind ./new.sh img|photo|readtime. Needs Pillow for images (pip install pillow)."""
import math
import re
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
    usage = "./new.sh img|photo <file> <assets-dir>  or  ./new.sh readtime <page.md>"
    if len(args) == 3 and args[0] in ("img", "photo"):
        convert(args[1], args[2], photo=args[0] == "photo")
    elif len(args) == 2 and args[0] == "readtime":
        readtime(args[1])
    else:
        sys.exit(usage)


if __name__ == "__main__":
    main()
