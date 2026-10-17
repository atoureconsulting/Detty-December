"""Cut the three generated frames into the deck, and drop two unlicensed ones.

The three came back from the prompts in the image brief and live in the Photo
folder in Drive, not in this repository. Download them next to this script as:

    gen/ribbon.png     the aerial coastline  (1344x768, Craiyon mark bottom right)
    gen/tourism.png    the colonnade         (1376x768)
    gen/enter.png      the night crowd       (1376x768)

    python3 deck/patch_v14_generated.py bbb-deck-v14.html out.html

Five frames change:

  p2  the foot ribbon            <- a 103px band of gen/ribbon, taken from y=360
                                    so it clears the watermark in the corner
  p3  pillar 01, Tourism         <- gen/tourism
  p3  pillar 02, Entertainment   <- gen/enter
  p7  the poster band            <- gen/enter, replacing the Afronation crowd
  p9  the right hand frame       <- gen/ribbon, replacing the Assinie aerial

That clears two of the three unlicensed photographs. The Abidjan skyline on the
cover is the third and still needs a commercial route.

Two captions move with them. Page nine can no longer name Assinie for a frame
that is generated, and page ten no longer credits Afronation, which has left
the deck; it says instead that some location imagery is illustrative.
"""
import base64
import io
import re
import sys

from PIL import Image


def jpeg_uri(im, quality=82):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def fit(path, size, box=None):
    """Crop to box if given, then centre-crop to the target ratio and resize."""
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    w, h = im.size
    target = size[0] / size[1]
    if w / h > target:
        nw = int(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    return im.resize(size, Image.LANCZOS)


def sections(html):
    """Start and end offsets of each section. They never nest, so these pair off."""
    off = html.index('<div class="deck">') + len('<div class="deck">')
    body = html[off:html.rindex("</div>")]
    starts = [m.start() for m in re.finditer(r"<section\b", body)]
    ends = [m.end() for m in re.finditer(r"</section>", body)]
    return [(off + s, off + e) for s, e in zip(starts, ends)]


def swap(html, page, nth, uri):
    """Replace the nth img src inside the given page, 1-indexed page, 0-indexed img."""
    start, end = sections(html)[page - 1]
    pos = start
    for _ in range(nth + 1):
        pos = html.index('<img src="', pos) + len('<img src="')
    stop = html.index('"', pos)
    assert stop < end, "img %d is not inside page %d" % (nth, page)
    return html[:pos] + uri + html[stop:]


def patch(html):
    rib = Image.open("gen/ribbon.png").convert("RGB")
    # the band sits above the watermark, and reads lagoon / palms / sand / surf
    band = rib.crop((0, 360, rib.size[0], 463)).resize((1300, 100), Image.LANCZOS)

    html = swap(html, 2, 0, jpeg_uri(band))
    html = swap(html, 3, 0, jpeg_uri(fit("gen/tourism.png", (780, 439))))
    html = swap(html, 3, 1, jpeg_uri(fit("gen/enter.png", (780, 439))))
    html = swap(html, 7, 0, jpeg_uri(fit("gen/enter.png", (1200, 420))))
    # above y=600 to clear the watermark
    html = swap(html, 9, 1, jpeg_uri(fit("gen/ribbon.png", (900, 600), box=(0, 0, 1344, 600))))

    old = ('<div class="cap" style="margin-top:.7cqw;">Mother Africa Festival, Abidjan &nbsp;·&nbsp;\n'
           '        the coast at Assinie</div>')
    assert old in html
    html = html.replace(
        old, '<div class="cap" style="margin-top:.7cqw;">Mother Africa Festival, Abidjan</div>', 1)

    old = ('<div class="cap" style="margin-top:.7cqw;">Location and festival photography credited to\n'
           '        Afronation.com, Afrique Magazine and the Mother Africa Festival.</div>')
    assert old in html
    html = html.replace(old, '<div class="cap" style="margin-top:.7cqw;">Festival photography '
                             'courtesy of the\n        Mother Africa Festival. Abidjan skyline, '
                             'Afrique Magazine. Some location imagery is\n        illustrative '
                             'rather than documentary.</div>', 1)

    assert "Afronation" not in html and "the coast at Assinie" not in html
    assert html.count("Assinie") == 2, "the route map pin and the country list should remain"
    return html


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src) as f:
        out = patch(f.read())
    with open(dst, "w") as f:
        f.write(out)
    print("%s -> %s  (%.2f MB)" % (src, dst, len(out) / 1e6))
