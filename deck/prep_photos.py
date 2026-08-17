"""
Turn any portrait into a circular PNG sized for the roster cards.

Usage:
    1. Drop images into deck/photos/, named either way:
         by deck position   1.jpg  2.jpg  3.jpg ...  14.jpg
         or by slug         olivia-yace.jpg  veena-praveenar.png
       (run this script any time to see which are still missing)
    2. python prep_photos.py
    3. node build.js

Any face-up portrait works — it is centre-cropped to a square, masked to a
circle with a transparent surround, and written to photos/_circles/<slug>.png.
Slugs with no image are left as empty placeholders in the deck.
"""
import os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "photos")
OUT = os.path.join(SRC, "_circles")
SIZE = 900  # generous for print; the circle renders at ~1.4in

SLUGS = [
    "olivia-yace", "veena-praveenar", "isabella-menin", "nadia-mejia",
    "alicia-aylies", "angelique-angarni-filopon", "rebecca-biangue",
    "dorcas-dienda", "ophely-mezino", "nellie-anjaratiana",
    "sephora-kongo", "tai", "khaiza-kuyo", "bella-zabaneh",
]
EXTS = (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP")


def find(slug):
    """Accept either the slug (olivia-yace.jpg) or the deck position (1.jpg)."""
    idx = SLUGS.index(slug) + 1
    for stem in (slug, str(idx), "%02d" % idx):
        for e in EXTS:
            p = os.path.join(SRC, stem + e)
            if os.path.exists(p):
                return p
    return None


def circle(path, dest):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    s = min(w, h)
    # centre crop, biased slightly up so faces sit well in the circle
    left = (w - s) // 2
    top = max(0, int((h - s) * 0.35))
    im = im.crop((left, top, left + s, top + s)).resize((SIZE, SIZE), Image.LANCZOS)
    mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, SIZE * 4, SIZE * 4), fill=255)
    mask = mask.resize((SIZE, SIZE), Image.LANCZOS)  # supersampled = smooth edge
    im.putalpha(mask)
    im.save(dest, "PNG")


def main():
    os.makedirs(OUT, exist_ok=True)
    done, missing = [], []
    for slug in SLUGS:
        src = find(slug)
        if not src:
            missing.append(slug)
            continue
        circle(src, os.path.join(OUT, slug + ".png"))
        done.append(slug)

    if done:
        print(f"processed {len(done)}: " + ", ".join(done))
    if missing:
        print(f"\nstill needed ({len(missing)}) — name by slug or by deck position:")
        for m in missing:
            print("  %2d.jpg   or   %s.jpg" % (SLUGS.index(m) + 1, m))
    if not done and not os.path.isdir(SRC):
        print(f"\ncreated {SRC} — put images there and re-run.")
    print("\nthen: node build.js")


if __name__ == "__main__":
    os.makedirs(SRC, exist_ok=True)
    main()
