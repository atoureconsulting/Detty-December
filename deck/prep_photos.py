"""
Turn any portrait into a circular PNG sized for the roster cards.

Usage:
    1. Drop images into deck/photos/ named after each woman's slug, e.g.
       olivia-yace.jpg   veena-praveenar.png   isabella-menin.jpeg
       (run this script with no args to print the exact slug list)
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
    for e in EXTS:
        p = os.path.join(SRC, slug + e)
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
        print(f"\nstill needed ({len(missing)}) — drop into deck/photos/ as <slug>.jpg:")
        for m in missing:
            print("  " + m)
    if not done and not os.path.isdir(SRC):
        print(f"\ncreated {SRC} — put images there and re-run.")
    print("\nthen: node build.js")


if __name__ == "__main__":
    os.makedirs(SRC, exist_ok=True)
    main()
