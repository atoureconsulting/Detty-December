"""v14 media pass: less text on pages two and three, pictures in its place.

Runs after patch_v13_to_v14.py, against the same built HTML. The three pillar
frames and the foot ribbon are prepared from images already embedded in the
deck, so no new asset is needed on disk:

  tourism  the towers end of the cover skyline, 16:9
  enter    the festival crowd, tighter than the poster page uses it, 16:9
  impact   the Fondation emblem squared off onto its own field, 16:9
  band     a horizontal slice through the beach and the surf line, ~13:1

All four are placeholders. See the image brief in Drive for what replaces them.

    python3 deck/patch_v14_media.py bbb-deck-v14.html out.html

Changes
  p2  the four detail blocks come up under the figures instead of being pushed
      to the foot, and a coastline ribbon closes the page
  p3  the preamble goes, each pillar loses about half its copy, and each gains
      a picture above it; the number moves inline with the pillar name
"""
import base64
import io
import re
import sys

from PIL import Image

W, H = 780, 439  # 16:9 for the pillar frames


def jpeg_uri(im, quality=80):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def fit(im, box, size):
    """Crop to box, then centre-crop to the target ratio and resize."""
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


def section_images(html):
    """The data URIs already in the deck, by page number (sections do not nest)."""
    body = html.split('<div class="deck">', 1)[1].rsplit("</div>", 1)[0]
    starts = [m.start() for m in re.finditer(r"<section\b", body)]
    ends = [m.end() for m in re.finditer(r"</section>", body)]
    out = {}
    for n, (s, e) in enumerate(zip(starts, ends), 1):
        out[n] = [Image.open(io.BytesIO(base64.b64decode(b)))
                  for b in re.findall(r"data:image/[a-z+]+;base64,([A-Za-z0-9+/=]+)", body[s:e])]
    return out


def build_media(html):
    src = section_images(html)
    sky, crowd, emblem, coast = src[1][0], src[7][0], src[6][0], src[9][1]

    field = emblem.convert("RGB").getpixel((4, 4))
    canvas = Image.new("RGB", (W, H), field)
    e = emblem.copy()
    e.thumbnail((H - 36, H - 36), Image.LANCZOS)
    canvas.paste(e, ((W - e.size[0]) // 2, (H - e.size[1]) // 2))

    return {
        "tourism": jpeg_uri(fit(sky, (430, 60, 1400, 760), (W, H))),
        "enter": jpeg_uri(fit(crowd, (210, 0, 1050, 420), (W, H))),
        "impact": jpeg_uri(canvas),
        # a straight slice, not centre-cropped: the ribbon wants the full width
        "band": jpeg_uri(coast.crop((0, 300, 900, 369)).resize((1300, 100), Image.LANCZOS),
                         quality=84),
    }


PIL3_CSS = """
    .pil3{display:grid;grid-template-columns:repeat(3,1fr);gap:3.4cqw;align-items:start;}
    .pil3 .p3 img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;margin-bottom:1cqw;}
    .pil3 .p3 .ph{display:flex;align-items:baseline;gap:.75cqw;padding-top:.75cqw;
     border-top:2px solid var(--ink);font:400 1.72cqw/1.15 'Fraunces';color:var(--ink);}
    .pil3 .p3 .ph i{font:600 .86cqw/1 'Karla';font-style:normal;letter-spacing:.14em;
     color:var(--accent);}
    .pil3 .p3 span{display:block;margin-top:.6cqw;font:300 1.04cqw/1.5 'Karla';color:var(--muted);}
    .pil3 .p3 em{display:block;margin-top:.8cqw;padding-top:.5cqw;border-top:1px solid var(--rule);
     font:600 .82cqw/1.4 'Karla';font-style:normal;letter-spacing:.14em;text-transform:uppercase;
     color:var(--ink);}"""

PILLARS = """<h2 style="font-size:2.8cqw;max-width:40ch;margin-top:1.4cqw;">Put West Africa's December in
        front of an audience that has never seen it.</h2>
      <div class="pil3" style="margin-top:2.4cqw;">
        <div class="p3"><img src="%(tourism)s" alt="">
          <div class="ph"><i>01</i>Tourism</div>
          <span>Four prospective countries filmed as destinations rather than backdrops, and carried
          into ten markets by visitors rather than by advertising.</span>
          <em>Destination and travel partners</em></div>
        <div class="p3"><img src="%(enter)s" alt="">
          <div class="ph"><i>02</i>Entertainment</div>
          <span>December is when the diaspora comes home. The delegation arrives inside an audience
          that is already there, at the festivals that define the season.</span>
          <em>Consumer and lifestyle partners</em></div>
        <div class="p3"><img src="%(impact)s" alt="">
          <div class="ph"><i>03</i>Social impact</div>
          <span>The Fondation Olivia Yacé leads, and partners with an in-country foundation in each
          other territory. It is what makes this a delegation and not a holiday.</span>
          <em>Named across every pillar</em></div>
      </div>
      """

# 13:1, which is what clears page two's folio. The page has no bottom padding
# reserve of its own, so anything taller runs under the running foot.
BAND = ('<img src="%(band)s" alt="" style="display:block;width:100%%;aspect-ratio:13/1;'
        'object-fit:cover;margin-top:auto;">')


def patch(html):
    uris = build_media(html)

    old_grid = ('<div class="dgrid3" style="grid-template-columns:repeat(2,1fr);'
                'gap:1.8cqw 4cqw;margin-top:auto;">')
    assert old_grid in html
    html = html.replace(old_grid, '<div class="dgrid3" style="grid-template-columns:repeat(2,1fr);'
                                  'gap:1.6cqw 4cqw;margin-top:2cqw;">', 1)

    folio = '<div class="fol"><span>Beauty Beyond Borders</span><span>02</span></div>'
    assert html.count(folio) == 1
    i = html.index(folio)
    j = html.rindex("</div>\n    ", 0, i)          # close of .pad, before the folio
    html = html[:j] + (BAND % uris) + "\n    </div>\n    " + html[i:]

    i = html.index("\n    .pil3{display:grid")
    j = html.index("color:var(--ink);}", html.index(".pil3 .p3 em{", i)) + len("color:var(--ink);}")
    html = html[:i] + PIL3_CSS + html[j:]

    i = html.index('<div style="display:grid;grid-template-columns:auto 1fr;gap:4cqw;'
                   'align-items:baseline;margin-top:1.2cqw;">\n        '
                   '<h2 style="font-size:2.9cqw;max-width:18ch;">')
    j = html.index('<div class="obar" style="margin-top:auto;">', i)
    html = html[:i] + (PILLARS % uris) + html[j:]

    assert "Ten women who already hold that audience" not in html
    assert html.count('class="p3"') == 3 and html.count('class="ph"') == 3
    return html


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src) as f:
        out = patch(f.read())
    with open(dst, "w") as f:
        f.write(out)
    print("%s -> %s  (%.2f MB)" % (src, dst, len(out) / 1e6))
