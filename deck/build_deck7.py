# -*- coding: utf-8 -*-
"""v6. Same facts, different temperature. Colour-blocked slides alternate with
   full-bleed photography and a woven-cloth ground; the festival page becomes a
   poster instead of a table; type is much bigger and photographs are large."""
import base64, io, os, random
from PIL import Image, ImageOps, ImageDraw

SC = os.environ.get("BBB_WORK", os.path.dirname(os.path.abspath(__file__)))
PH = os.environ.get("BBB_PHOTOS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos")) + "/"
BK = SC + "/brandkit/"

ORANGE, GREEN, GOLD, COCOA = "#E2710C", "#0B7A4B", "#E8A33D", "#3E2B1D"
NAVY, IVORY, SAND, RUST = "#12303F", "#FBF6EC", "#F1E7D3", "#A83A1E"

def _uri(im, q=86, fmt="JPEG"):
    b = io.BytesIO()
    im.save(b, fmt, quality=q, optimize=True)
    return "data:image/%s;base64,%s" % ("jpeg" if fmt == "JPEG" else "png",
                                        base64.b64encode(b.getvalue()).decode())

def _crop(slug, w, h, focus):
    im = Image.open(PH + slug + ".jpg").convert("RGB")
    ow, oh = im.size; t = w / h
    if ow / oh > t:
        nw = int(oh * t); left = (ow - nw) // 2
        im = im.crop((left, 0, left + nw, oh))
    else:
        nh = int(ow / t); top = int((oh - nh) * focus)
        im = im.crop((0, top, ow, top + nh))
    return im.resize((w, h), Image.LANCZOS)

def img(slug, w, h, focus=0.06, warm=1.0):
    im = _crop(slug, w, h, focus)
    if warm != 1.0:                      # gentle warm grade, keeps skin natural
        r, g, b = im.split()
        r = r.point(lambda v: min(255, int(v * warm)))
        b = b.point(lambda v: int(v / warm))
        im = Image.merge("RGB", (r, g, b))
    return _uri(im)

def duotone(slug, w, h, dark, light, focus=0.06):
    g = ImageOps.grayscale(_crop(slug, w, h, focus))
    g = ImageOps.autocontrast(g, cutoff=1)
    return _uri(ImageOps.colorize(g, black=dark, white=light))

def cloth(tile=260, scale=1):
    """Strip-woven ground: vertical bands with simple repeated motifs."""
    im = Image.new("RGB", (tile, tile), IVORY)
    d = ImageDraw.Draw(im)
    bands = [(0, 34, ORANGE), (34, 48, IVORY), (48, 86, COCOA), (86, 100, GOLD),
             (100, 140, GREEN), (140, 154, IVORY), (154, 196, RUST), (196, 210, GOLD),
             (210, 260, ORANGE)]
    for x0, x1, col in bands:
        d.rectangle([x0, 0, x1, tile], fill=col)
    # motifs down the wide bands
    for x0, x1, col in bands:
        if x1 - x0 < 30:
            continue
        cx = (x0 + x1) // 2
        for y in range(14, tile, 46):
            d.polygon([(cx, y - 8), (cx + 8, y), (cx, y + 8), (cx - 8, y)], fill=IVORY)
            d.line([(x0 + 3, y + 23), (x1 - 3, y + 23)], fill=GOLD, width=2)
    if scale != 1:
        im = im.resize((tile * scale, tile * scale), Image.NEAREST)
    return _uri(im, fmt="PNG")

CLOTH = cloth()
logo_dark = open(BK + "01-logos/atoure/atoure-nav-lockup-on-dark.svg").read().replace(
    'width="2926" height="517"', 'width="100%" height="100%" preserveAspectRatio="xMinYMid meet"', 1)
logo_light = open(BK + "01-logos/atoure/atoure-nav-lockup-on-light.svg").read().replace(
    'width="2926" height="517"', 'width="100%" height="100%" preserveAspectRatio="xMinYMid meet"', 1)

def localimg(path, w, q=88):
    im = Image.open(path).convert("RGB")
    return _uri(im.resize((w, int(w * im.size[1] / im.size[0])), Image.LANCZOS), q)
FOY = localimg(SC + "/foy-logo-b.jpg", 620)

def flag(code, cls="fl"):
    S = '<svg class="%s" viewBox="0 0 30 20" preserveAspectRatio="none">' % cls
    if code == "CI":
        S += '<rect width="10" height="20" fill="#F77F00"/><rect x="10" width="10" height="20" fill="#fff"/><rect x="20" width="10" height="20" fill="#009E60"/>'
    elif code == "GH":
        S += ('<rect width="30" height="6.67" fill="#CE1126"/><rect y="6.67" width="30" height="6.66" fill="#FCD116"/>'
              '<rect y="13.33" width="30" height="6.67" fill="#006B3F"/>'
              '<polygon fill="#000" points="15,7.1 16.05,10.2 19.3,10.2 16.65,12.1 17.7,15.2 15,13.3 12.3,15.2 13.35,12.1 10.7,10.2 13.95,10.2"/>')
    elif code == "NG":
        S += '<rect width="10" height="20" fill="#008751"/><rect x="10" width="10" height="20" fill="#fff"/><rect x="20" width="10" height="20" fill="#008751"/>'
    elif code == "BJ":
        S += '<rect width="12" height="20" fill="#008751"/><rect x="12" width="18" height="10" fill="#FCD116"/><rect x="12" y="10" width="18" height="10" fill="#E8112D"/>'
    return S + "</svg>"

# ---------------------------------------------------------------- the ten, pinned on cloth
DELEG = [
    ("olivia-yace", "Olivia Yacé", "Côte d'Ivoire", -3.0),
    ("sheynnis-palacios", "Sheynnis Palacios", "Nicaragua", 2.4),
    ("veena-praveenar", "Veena Praveenar Singh", "Thailand", -1.6),
    ("isabella-menin", "Isabella Menin", "Brazil", 3.0),
    ("angelique-angarni-filopon", "Angélique Angarni-Filopon", "Martinique", -2.2),
    ("dorcas-dienda", "Dorcas Dienda", "DR Congo", 2.0),
    ("nadia-mejia", "Nadia Mejia", "Ecuador", -2.8),
    ("ophely-mezino", "Ophély Mézino", "Guadeloupe", 1.7),
    ("camille-thomas", "Camille Sabina Thomas", "Curaçao", -1.9),
    ("bella-zabaneh", "Bella Zabaneh", "Belize", 2.6),
]
PINS = "".join(f"""
      <figure class="pin" style="--r:{rot}deg">
        <img src="{img(slug, 330, 400, 0.04, warm=1.05)}" alt="{name}">
        <figcaption><b>{name}</b><span>{country}</span></figcaption>
      </figure>""" for slug, name, country, rot in DELEG)

# ---------------------------------------------------------------- reach
PROFILES = [
    ("Olivia Yacé", 1200, 1100, 760, True), ("Sheynnis Palacios", 2300, 2500, 1000, False),
    ("Veena Praveenar Singh", 2100, 472, 52, False), ("Isabella Menin", 1100, 205, 22, False),
    ("Angélique Angarni-Filopon", 394, 474, 0, False), ("Nadia Mejia", 434, 127, 5, False),
    ("Dorcas Dienda", 222, 263, 61, False), ("Ophély Mézino", 141, 39, 0, False),
    ("Bella Zabaneh", 23, 23, 4, False), ("Camille Sabina Thomas", 19, 4, 0, False),
]
kf = lambda k: ("%.1fM" % (k / 1000)).replace(".0M", "M") if k >= 1000 else "%dK" % round(k)
MAX = max(a + b + c for _, a, b, c, _ in PROFILES)
ROWS = ""
for name, ig, tt, fb, host in PROFILES:
    tot = ig + tt + fb
    seg = "".join('<i class="%s" style="flex:%d"></i>' % (c, v)
                  for v, c in ((ig, "ig"), (tt, "tt"), (fb, "fb")) if v)
    ROWS += ('<div class="prow"><span class="pn">%s%s</span>'
             '<span class="ptrack"><span class="pbar" style="width:%.2f%%">%s</span></span>'
             '<span class="pt">%s</span></div>') % (
        name, ' <em>host</em>' if host else '', tot / MAX * 100, seg, kf(tot))

# ---------------------------------------------------------------- the poster
POSTER = [
    ("Fally Ipupa", "CI", "24 &amp; 25 Dec", "Stade Félix-Houphouët-Boigny", "xl"),
    ("Mother Africa", "CI", "27 &amp; 28 Dec", "Marcory Zone 4, Abidjan", "xl"),
    ("AfroFuture", "GH", "28 to 30 Dec", "El-Wak Stadium, Accra", "l"),
    ("Vodun Days", "BJ", "2 to 9 Jan", "Ouidah", "l"),
    ("Flytime Fest", "NG", "22 to 25 Dec", "Eko Centre, Lagos", "m"),
    ("Rapperholic", "GH", "31 Dec", "Accra Sports Stadium", "m"),
    ("WeLovEya", "BJ", "26 &amp; 27 Dec", "Cotonou", "sm"),
    ("Detty Rave", "GH", "27 Dec", "Accra", "sm"),
    ("Rhythm Unplugged", "NG", "21 Dec", "Eko Centre, Lagos", "sm"),
]
BILL = "".join(f"""
      <div class="act {sz}">
        <span class="an">{n}</span>
        <span class="ad">{flag(c,'fl tiny')} {d} &nbsp;·&nbsp; {v}</span>
      </div>""" for n, c, d, v, sz in POSTER)

BUDGET = [("Accommodation", "53,000"), ("Air travel", "40,000"),
          ("Production and documentary crew", "60,000"), ("Per diem and hospitality", "22,000"),
          ("Ground transport and security", "20,000"), ("Insurance", "18,000"),
          ("Visas and administration", "5,000"), ("Contingency", "32,000")]
BUD = "".join(f"<tr><td>{a}</td><td class='amt'>€{b}</td></tr>" for a, b in BUDGET)


CLOTHBIG = cloth(tile=260, scale=2)
TOTALK = sum(a + b + c for _, a, b, c, _ in PROFILES)
TOTM = "%.0fM" % (TOTALK / 1000)

# ---------------------------------------------------------------- theme rhythm
# guizang rule: every page is light or dark, heroes punctuate, never 3 alike in a row.
PLAN = ["hero dark", "light", "dark", "hero light", "light", "dark", "light",
        "hero dark", "dark", "hero light", "dark", "light", "dark", "hero dark", "light"]
base = [t.split()[-1] for t in PLAN]
for i in range(len(base) - 2):
    assert len(set(base[i:i + 3])) > 1, "three %s pages in a row at %d" % (base[i], i + 1)
assert "hero dark" in PLAN and "hero light" in PLAN
heroes = [i for i, t in enumerate(PLAN) if t.startswith("hero")]
assert max(b - a for a, b in zip(heroes, heroes[1:])) <= 4, "hero gap too wide"

CSS = """
  *{box-sizing:border-box;}
  body{margin:0;background:#1b1109;color:var(--cocoa);font-family:var(--body);}
  .deck{display:flex;flex-direction:column;align-items:center;gap:18px;
     padding-block:18px;padding-inline:16px;}
  .s{width:100%;max-width:1120px;aspect-ratio:16/9;position:relative;overflow:hidden;
     container-type:inline-size;box-shadow:0 3px 20px rgba(0,0,0,.35);}
  .s.light{background:var(--ivory);color:var(--cocoa);}
  .s.dark{background:var(--navy);color:var(--ivory);}
  .pad{padding:4cqw 5cqw;height:100%;display:flex;flex-direction:column;position:relative;z-index:3;}
  .no{position:absolute;right:2.2cqw;bottom:1.5cqw;font-family:var(--disp);font-size:1.4cqw;
     color:rgba(62,43,29,.42);z-index:9;}
  .dark .no,.onphoto .no{color:rgba(251,246,236,.55);}
  h1,h2{font-family:var(--disp);font-weight:600;margin:0;line-height:1.02;letter-spacing:-.012em;}
  p{margin:0;font-size:1.72cqw;line-height:1.62;color:var(--cocoa2);}
  .dark p,.onphoto p{color:rgba(251,246,236,.88);}
  .kick{font-family:var(--hand);font-size:2.5cqw;color:var(--orange);line-height:1;}
  .dark .kick,.onphoto .kick{color:var(--gold);}
  .hand{font-family:var(--hand);line-height:1.22;}
  .fl{width:2.3cqw;height:1.53cqw;display:inline-block;vertical-align:middle;
     box-shadow:0 0 0 1px rgba(255,255,255,.35);}
  .fl.tiny{width:1.7cqw;height:1.13cqw;}
  .bleed{position:absolute;inset:0;z-index:0;}
  /* bottom-only crop: faces sit in the top of the frame and are never cut */
  .bleed img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block;}
  .clothstrip{background-image:var(--cloth);background-size:auto 100%;}
  .edgecloth.clothstrip{background-size:100% auto;background-repeat:repeat-y;}
  .presented{display:flex;align-items:center;gap:.9cqw;font-size:1.02cqw;color:var(--mid);}
  .presented .lgo{width:12.4cqw;height:2.2cqw;} .presented .lgo svg{width:100%;height:100%;display:block;}
  .onphoto .presented{color:rgba(251,246,236,.72);}

  /* ---------- hero cover ---------- */
  .cover img{object-position:62% 6%;}
  .cwash{position:absolute;inset:0;z-index:1;background:
     linear-gradient(180deg,rgba(22,10,3,.60) 0%,rgba(22,10,3,.05) 30%,rgba(22,10,3,0) 48%),
     linear-gradient(96deg,rgba(22,10,3,.86) 0%,rgba(22,10,3,.42) 38%,rgba(22,10,3,0) 66%),
     linear-gradient(0deg,rgba(22,10,3,.80) 0%,rgba(22,10,3,0) 36%);}
  .masthead{font-family:var(--disp);font-weight:700;font-size:7.4cqw;line-height:.98;
     color:var(--ivory);letter-spacing:-.02em;white-space:nowrap;text-shadow:0 2px 30px rgba(0,0,0,.45);}
  .mrule{height:3px;background:var(--orange);margin:1cqw 0 .85cqw;}
  .mline{font-size:1.4cqw;letter-spacing:.24em;text-transform:uppercase;color:rgba(251,246,236,.92);}
  .cl1{display:block;font-family:var(--disp);font-weight:600;font-size:3.8cqw;
     line-height:1.08;color:var(--ivory);}
  .cl2{display:block;font-family:var(--hand);font-size:2.35cqw;color:var(--gold);margin-top:.7cqw;}
  .seal{position:absolute;right:4.4cqw;top:4.4cqw;width:12.6cqw;height:12.6cqw;border-radius:50%;
     background:var(--orange);color:#fff;display:flex;flex-direction:column;align-items:center;
     justify-content:center;text-align:center;font-family:var(--hand);font-size:1.55cqw;
     line-height:1.16;z-index:4;box-shadow:0 4px 22px rgba(0,0,0,.35);transform:rotate(-7deg);}
  .seal b{font-family:var(--disp);font-weight:700;font-size:2.5cqw;display:block;margin-bottom:.15cqw;}

  /* ---------- big numbers ---------- */
  .nums{display:grid;grid-template-columns:repeat(4,1fr);gap:2.4cqw;align-items:end;
     margin-top:auto;}
  .footcloth{position:absolute;left:0;right:0;bottom:0;height:2.4cqw;z-index:1;}
  .nums .n{border-top:3px solid var(--orange);padding-top:1.1cqw;}
  .nums .n:nth-child(2){border-color:var(--green);} .nums .n:nth-child(3){border-color:var(--gold);}
  .nums .n:nth-child(4){border-color:var(--rust);}
  .nums .fig{font-family:var(--disp);font-weight:700;font-size:7.4cqw;line-height:.9;
     letter-spacing:-.03em;color:var(--cocoa);display:block;}
  .nums .lab{display:block;margin-top:.7cqw;font-size:1.32cqw;line-height:1.45;color:var(--cocoa2);}
  .nums .lab b{display:block;font-weight:600;color:var(--cocoa);}

  /* ---------- lead image + side text ---------- */
  .lead{display:grid;grid-template-columns:30cqw 1fr;gap:4cqw;flex:1;min-height:0;}
  .lead .shot{align-self:start;margin-top:1cqw;border-radius:0 0 14cqw 14cqw;overflow:hidden;
     box-shadow:0 10px 34px rgba(0,0,0,.4);}
  .lead .shot img{width:100%;display:block;}
  .lead .side{display:flex;flex-direction:column;justify-content:center;}
  .lead .side p + p{margin-top:1.1cqw;}

  /* ---------- act divider ---------- */
  .divider .pad{justify-content:center;}
  .divider .act-no{font-family:var(--disp);font-weight:400;font-style:italic;font-size:2.4cqw;
     letter-spacing:.3em;text-transform:uppercase;color:var(--orange);}
  .dark.divider .act-no{color:var(--gold);}
  .divider .act-t{font-family:var(--disp);font-weight:700;font-size:9.4cqw;line-height:.96;
     letter-spacing:-.03em;margin-top:.6cqw;}
  .divider .act-s{font-family:var(--hand);font-size:2.6cqw;margin-top:1.2cqw;color:var(--cocoa2);}
  .dark.divider .act-s,.onphoto.divider .act-s{color:var(--gold);}
  .edgecloth{position:absolute;left:0;top:0;bottom:0;width:6.4cqw;z-index:1;}
  .dimwash{position:absolute;inset:0;z-index:1;
     background:linear-gradient(92deg,rgba(8,20,28,.92) 0%,rgba(8,20,28,.70) 48%,rgba(8,20,28,.28) 100%);}

  /* ---------- the ten ---------- */
  .pinwrap{position:relative;flex:1;min-height:0;margin-top:1.4cqw;}
  .pinband{position:absolute;left:-5cqw;right:-5cqw;top:6.2cqw;height:2.1cqw;z-index:0;opacity:.9;}
  .pins{position:relative;z-index:2;display:grid;grid-template-columns:repeat(5,13.6cqw);
     gap:1.1cqw;height:100%;align-content:center;justify-content:space-between;}
  .pin{margin:0;background:var(--paper);padding:.55cqw .55cqw .9cqw;transform:rotate(var(--r));
     box-shadow:0 5px 14px rgba(62,43,29,.22);}
  .pin img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top center;display:block;}
  .pin figcaption{margin-top:.5cqw;text-align:center;}
  .pin b{display:block;font-family:var(--disp);font-weight:600;font-size:1.08cqw;line-height:1.15;
     color:var(--cocoa);}
  .pin span{display:block;font-size:.88cqw;color:var(--mid);margin-top:.12cqw;}

  /* ---------- reach ---------- */
  .audhead{display:flex;justify-content:space-between;align-items:flex-end;gap:2cqw;}
  .key{display:flex;gap:1.3cqw;font-size:1.12cqw;color:rgba(251,246,236,.8);}
  .key span{display:flex;align-items:center;gap:.4cqw;}
  .sw{width:1cqw;height:1cqw;border-radius:2px;display:inline-block;}
  .ig{background:var(--orange);} .tt{background:var(--gold);} .fb{background:#5FA8D3;}
  .ptable{margin-top:1.5cqw;margin-bottom:1.1cqw;display:flex;flex-direction:column;gap:.62cqw;}
  .prow{display:grid;grid-template-columns:17cqw 1fr 5.4cqw;gap:1.1cqw;align-items:center;}
  .pn{font-size:1.24cqw;color:rgba(251,246,236,.92);white-space:nowrap;overflow:hidden;
     text-overflow:ellipsis;}
  .pn em{font-style:normal;font-family:var(--hand);font-size:1.6cqw;color:var(--gold);}
  .ptrack{height:1.5cqw;background:rgba(255,255,255,.07);}
  .pbar{display:flex;height:100%;} .pbar i{display:block;height:100%;}
  .pt{font-family:var(--disp);font-weight:600;font-size:1.7cqw;color:var(--gold);text-align:right;
     font-variant-numeric:tabular-nums;}

  /* ---------- foundation ---------- */
  .foy{display:grid;grid-template-columns:24cqw 1fr;gap:3.4cqw;flex:1;min-height:0;align-items:center;}
  .foycard{background:var(--navy);padding:2.2cqw;display:flex;align-items:center;justify-content:center;
     box-shadow:0 8px 24px rgba(62,43,29,.25);}
  .foycard img{width:100%;display:block;}
  .foygrid{display:grid;grid-template-columns:1fr 1fr;gap:.8cqw 2cqw;margin-top:1.5cqw;}
  .foygrid b{display:block;font-family:var(--disp);font-weight:600;font-size:1.6cqw;color:var(--cocoa);}
  .foygrid span{font-size:1.16cqw;color:var(--mid);}
  .foynote{margin-top:1.5cqw;padding:1.05cqw 1.3cqw;border-left:3px solid var(--orange);
     font-size:1.28cqw;line-height:1.55;color:var(--cocoa2);background:var(--sand);}

  /* ---------- poster ---------- */
  .bill{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:.5cqw;
     text-align:center;}
  .act .an{font-family:var(--disp);font-weight:700;color:var(--ivory);line-height:1;display:block;
     letter-spacing:-.02em;}
  .act.xl .an{font-size:4.5cqw;} .act.l .an{font-size:3.3cqw;}
  .act.m .an{font-size:2.5cqw;} .act.sm .an{font-size:1.85cqw;}
  .act .ad{font-size:1.06cqw;color:var(--gold);letter-spacing:.06em;display:block;margin-top:.22cqw;}
  .posterrule{height:2px;background:rgba(232,163,61,.45);margin:.55cqw auto;width:34cqw;}

  /* ---------- big quote ---------- */
  .bigq .pad{justify-content:center;padding-left:11cqw;padding-right:9cqw;}
  .bigq blockquote{margin:0;font-family:var(--disp);font-weight:600;font-size:4.5cqw;
     line-height:1.14;letter-spacing:-.018em;color:var(--cocoa);max-width:28ch;}
  .bigq .mark{font-family:var(--disp);font-size:9cqw;line-height:.6;color:var(--orange);display:block;}
  .bigq .attr{margin-top:2cqw;font-size:1.28cqw;letter-spacing:.2em;text-transform:uppercase;
     color:var(--mid);}

  /* ---------- budget ---------- */
  .bud{width:100%;border-collapse:collapse;margin-top:1.6cqw;}
  .bud td{padding:.72cqw 0;border-bottom:1px solid var(--edge);font-size:1.5cqw;color:var(--cocoa2);}
  .bud .amt{text-align:right;font-family:var(--disp);font-weight:600;font-size:2.05cqw;
     color:var(--cocoa);font-variant-numeric:tabular-nums;}
  .bud tr:last-child td{border-bottom:none;border-top:3px solid var(--cocoa);padding-top:1cqw;
     font-family:var(--disp);font-weight:700;font-size:2.6cqw;color:var(--orange);}

  /* ---------- partnership ---------- */
  .ask{display:grid;grid-template-columns:1fr 1fr;gap:3.4cqw;flex:1;min-height:0;
     align-content:center;margin-top:1.4cqw;}
  .ask ul{margin:0;padding:0;list-style:none;}
  .ask li{font-size:1.58cqw;line-height:1.4;color:rgba(251,246,236,.94);padding:.62cqw 0 .62cqw 2.1cqw;
     border-bottom:1px solid rgba(255,255,255,.14);position:relative;}
  .ask li:before{content:"";position:absolute;left:0;top:1.18cqw;width:.85cqw;height:.85cqw;
     background:var(--gold);transform:rotate(45deg);}
  .tgt b{display:block;font-family:var(--disp);font-weight:600;font-size:1.85cqw;color:var(--gold);
     margin-top:1.2cqw;}
  .tgt b:first-child{margin-top:0;}
  .tgt span{display:block;font-size:1.22cqw;line-height:1.5;color:rgba(251,246,236,.82);}

  /* ---------- close ---------- */
  .close .pad{justify-content:flex-end;}
  .close h1{font-size:5.6cqw;color:var(--ivory);max-width:20ch;}
  .closebar{display:flex;justify-content:space-between;align-items:flex-end;gap:2cqw;
     margin-top:2.2cqw;padding-top:1.4cqw;border-top:2px solid rgba(232,163,61,.5);}

  /* ---------- notes ---------- */
  .notes{columns:2;column-gap:3.4cqw;margin-top:1.2cqw;}
  .notes p{font-size:1.1cqw;line-height:1.5;color:var(--cocoa2);
     break-inside:avoid;margin-bottom:.8cqw;}
  .notes p b{color:var(--cocoa);}
"""

ROOT = f"""
  :root{{
    --ivory:{IVORY}; --sand:{SAND}; --edge:#E2D4B8; --paper:#FFFDF8;
    --orange:{ORANGE}; --green:{GREEN}; --gold:{GOLD}; --rust:{RUST};
    --cocoa:{COCOA}; --cocoa2:#6B5340; --mid:#93795E; --navy:{NAVY};
    --disp:'Fraunces',Georgia,serif; --body:'Karla',Arial,sans-serif; --hand:'Caveat',cursive;
    --cloth:url("{CLOTH}");
  }}"""

# 4:5 prints, a standard ratio, cropped from the top so no face loses a chin
PINS = "".join(f"""
        <figure class="pin" style="--r:{rot}deg">
          <img src="{img(slug, 320, 400, 0.02, warm=1.05)}" alt="{name}">
          <figcaption><b>{name}</b><span>{country}</span></figcaption>
        </figure>""" for slug, name, country, rot in DELEG)

BILLP = BILL.replace('<div class="act l">', '<div class="act l">', 1)
S = []

# ---------------------------------------------------------------- 1 hero dark
S.append(f"""
  <section class="s dark cover onphoto">
    <div class="bleed"><img src="{img('olivia-yace', 1400, 788, 0.0, warm=1.06)}" alt="Olivia Yacé"></div>
    <div class="cwash"></div>
    <div class="seal"><b>10</b>women<br>four countries</div>
    <div class="pad" style="padding:3.4cqw 4.4cqw 4.4cqw;">
      <div>
        <div class="masthead">Beauty Beyond Borders</div>
        <div class="mrule"></div>
        <div class="mline">West Africa &nbsp;·&nbsp; December 2026 to January 2027</div>
      </div>
      <div style="margin-top:auto;">
        <span class="cl1">Ten women. Four countries.<br>Seventeen days of December.</span>
        <span class="cl2">and a season that never needed an introduction</span>
        <div class="presented" style="margin-top:1.7cqw;">
          <span>presented by</span><span class="lgo">{logo_dark}</span>
        </div>
      </div>
    </div>
    <div class="no">1</div>
  </section>""")

# ---------------------------------------------------------------- 2 light
S.append(f"""
  <section class="s light">
    <div class="pad">
      <div class="kick">the shape of it</div>
      <div style="display:grid;grid-template-columns:1fr 34cqw;gap:5cqw;align-items:end;margin-top:.5cqw;">
        <h2 style="font-size:3.6cqw;max-width:20ch;">Four numbers, before anything else.</h2>
        <p style="font-size:1.6cqw;">Every other page in this document is an argument. This one is just the arithmetic, and the arithmetic is the reason the tour is worth building.</p>
      </div>
      <div class="nums">
        <div class="n"><span class="fig">10</span>
          <span class="lab"><b>titleholders</b>invited by Olivia Yacé, travelling as one delegation</span></div>
        <div class="n"><span class="fig">4</span>
          <span class="lab"><b>countries</b>Côte d'Ivoire, Ghana, Nigeria, Bénin</span></div>
        <div class="n"><span class="fig">17</span>
          <span class="lab"><b>days</b>nine of them Ivorian, every one of them filmed</span></div>
        <div class="n"><span class="fig">{TOTM}</span>
          <span class="lab"><b>followers</b>across the delegation, before a single partner is added</span></div>
      </div>
      <div class="hand" style="margin-top:3cqw;font-size:2.1cqw;color:var(--green);">The season is already happening. We are bringing the audience.</div>
    </div>
    <div class="footcloth clothstrip"></div>
    <div class="no">2</div>
  </section>""")

# ---------------------------------------------------------------- 3 dark
S.append(f"""
  <section class="s dark">
    <div class="pad">
      <div class="kick">what this is</div>
      <div class="lead">
        <div class="shot"><img src="{img('sheynnis-palacios', 600, 750, 0.0, warm=1.04)}" alt=""></div>
        <div class="side">
          <h2 style="font-size:4.2cqw;color:var(--ivory);max-width:16ch;">Not a trip.<br>A moment.</h2>
          <p style="margin-top:1.6cqw;max-width:46ch;">Ten international titleholders travel West Africa together as a delegation, hosted by Olivia Yacé, through the busiest fortnight in the region's calendar.</p>
          <p style="max-width:46ch;">They attend the festivals that are already selling out, sit with the foundations doing the work, and are filmed the whole way.</p>
          <div class="hand" style="margin-top:1.8cqw;font-size:2.35cqw;color:var(--gold);">Governments get the story. Brands get the audience.</div>
        </div>
      </div>
    </div>
    <div class="no">3</div>
  </section>""")

# ---------------------------------------------------------------- 4 hero light divider
S.append("""
  <section class="s light divider">
    <div class="edgecloth clothstrip"></div>
    <div class="pad" style="padding-left:12cqw;">
      <div class="act-no">Act one</div>
      <div class="act-t">The women</div>
      <div class="act-s">ten countries of origin, one December</div>
    </div>
    <div class="no">4</div>
  </section>""")

# ---------------------------------------------------------------- 5 light
S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3.4cqw 5cqw;">
      <div class="kick">the delegation</div>
      <div class="pinwrap">
        <div class="pinband clothstrip"></div>
        <div class="pins">{PINS}</div>
      </div>
    </div>
    <div class="no">5</div>
  </section>""")

# ---------------------------------------------------------------- 6 dark
S.append(f"""
  <section class="s dark">
    <div class="pad" style="padding:3.4cqw 5cqw;">
      <div class="kick">who is watching</div>
      <div class="audhead" style="margin-top:.5cqw;">
        <h2 style="font-size:3.4cqw;color:var(--ivory);">Fifteen million, profile by profile.</h2>
        <div class="key"><span><i class="sw ig"></i>Instagram</span><span><i class="sw tt"></i>TikTok</span><span><i class="sw fb"></i>Facebook</span></div>
      </div>
      <div class="ptable">{ROWS}</div>
      <div style="font-size:1.16cqw;color:rgba(251,246,236,.58);">Summed across three platforms, not deduplicated. Host first, then by total.</div>
    </div>
    <div class="no">6</div>
  </section>""")

# ---------------------------------------------------------------- 7 light
S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3.4cqw 5cqw;">
      <div class="kick">the foundation</div>
      <div class="foy" style="margin-top:.9cqw;">
        <div class="foycard"><img src="{FOY}" alt="Fondation Olivia Yacé"></div>
        <div>
          <h2 style="font-size:3.2cqw;max-width:20ch;">The tour has a foundation behind it.</h2>
          <p style="margin-top:1cqw;max-width:48ch;">Founded in 2025 and anchored in Côte d'Ivoire, the Fondation Olivia Yacé puts vulnerable children, and girls in particular, into school and keeps them there.</p>
          <div class="foygrid">
            <div><b>School fees</b><span>paid directly</span></div>
            <div><b>Teaching kits</b><span>schools and orphanages</span></div>
            <div><b>School meals</b><span>nutrition programmes</span></div>
            <div><b>Tutoring</b><span>and mentoring</span></div>
          </div>
          <div class="foynote"><b>September 2026.</b> More than six million CFA francs raised for the École Hermann Gmeiner at the SOS Children's Village in Abobo, for the 2026 to 2027 school year.</div>
        </div>
      </div>
    </div>
    <div class="no">7</div>
  </section>""")

# ---------------------------------------------------------------- 8 hero dark divider
S.append(f"""
  <section class="s dark divider onphoto">
    <div class="bleed"><img src="{duotone('isabella-menin', 1400, 788, (8,26,38), (240,196,130), 0.0)}" alt=""></div>
    <div class="dimwash"></div>
    <div class="pad" style="padding-left:6.5cqw;">
      <div class="act-no">Act two</div>
      <div class="act-t" style="color:var(--ivory);">The season</div>
      <div class="act-s">21 December to 9 January, the coast does not sleep</div>
    </div>
    <div class="no">8</div>
  </section>""")

# ---------------------------------------------------------------- 9 dark
S.append(f"""
  <section class="s dark">
    <div class="pad" style="padding:3.2cqw 5cqw;">
      <div style="text-align:center;">
        <div class="kick">what is already booked</div>
      </div>
      <div class="bill">
        {BILL}
      </div>
      <div style="text-align:center;font-size:1.16cqw;color:rgba(251,246,236,.58);">Published dates, September 2026. Several Abidjan dates remain unconfirmed and are not listed.</div>
    </div>
    <div class="no">9</div>
  </section>""")

# ---------------------------------------------------------------- 10 hero light quote
S.append("""
  <section class="s light bigq">
    <div class="edgecloth clothstrip" style="width:4.4cqw;"></div>
    <div class="pad">
      <span class="mark">&ldquo;</span>
      <blockquote>West Africa in December is not a destination. It is a homecoming the rest of the world has not been invited to yet.</blockquote>
      <div class="attr">the case for this tour</div>
    </div>
    <div class="no">10</div>
  </section>""")

# ---------------------------------------------------------------- 11 dark
S.append(f"""
  <section class="s dark onphoto">
    <div class="bleed"><img src="{img('veena-praveenar', 1400, 788, 0.0, warm=1.05)}" alt=""></div>
    <div style="position:absolute;inset:0;z-index:1;background:linear-gradient(95deg,rgba(18,10,4,.94) 0%,rgba(18,10,4,.64) 42%,rgba(18,10,4,.04) 76%);"></div>
    <div class="pad" style="justify-content:center;">
      <div style="max-width:44cqw;">
        <div class="kick">filmed</div>
        <h2 style="margin-top:.7cqw;font-size:4.4cqw;color:var(--ivory);">Shot as a series, not covered as an event.</h2>
        <p style="margin-top:1.3cqw;">Seventeen days cut as a reality format, a short edit out every day. Broadcast rights are a second revenue line, and every partner keeps an archive that outlives the two weeks.</p>
      </div>
    </div>
    <div class="no">11</div>
  </section>""")

# ---------------------------------------------------------------- 12 light
S.append(f"""
  <section class="s light">
    <div class="edgecloth clothstrip" style="width:5.2cqw;"></div>
    <div class="pad" style="padding-left:11cqw;">
      <div class="kick">the number</div>
      <h2 style="margin-top:.5cqw;font-size:4.2cqw;">€250,000 delivers it.</h2>
      <table class="bud">{BUD}<tr><td>Total</td><td class="amt">€250,000</td></tr></table>
      <div class="hand" style="margin-top:auto;font-size:2cqw;color:var(--green);">Every confirmed partner brings this number down.</div>
    </div>
    <div class="no">12</div>
  </section>""")

# ---------------------------------------------------------------- 13 dark
S.append("""
  <section class="s dark" style="background:#0B7A4B;">
    <div class="pad">
      <div class="kick">partnership</div>
      <h2 style="margin-top:.5cqw;font-size:4.2cqw;color:var(--ivory);">What a partner takes.</h2>
      <div class="ask">
        <ul>
          <li>Category exclusivity across four markets</li>
          <li>Presence inside the series, not around it</li>
          <li>The delegation's audience and the press behind it</li>
          <li>A named role in the foundation programme</li>
          <li>A rights cleared archive to reuse</li>
        </ul>
        <div class="tgt">
          <b>Governments</b><span>Sublime Côte d'Ivoire. Lagos State Tourism. Ghana Ministry of Tourism. ANPT Bénin.</span>
          <b>Travel</b><span>Air Côte d'Ivoire. Accor. Kempinski. Eko Hotels.</span>
          <b>Consumer</b><span>Jewellery, watches, beauty, telecoms and banking, approached through the participants who have worked with them before.</span>
        </div>
      </div>
      <div class="hand" style="font-size:2cqw;color:var(--gold);">One partner per category. That is what makes it worth something.</div>
    </div>
    <div class="no">13</div>
  </section>""")

# ---------------------------------------------------------------- 14 hero dark close
S.append(f"""
  <section class="s dark close onphoto">
    <div class="bleed clothstrip" style="background-image:url('{CLOTHBIG}');background-size:auto 30cqw;"></div>
    <div class="dimwash" style="background:linear-gradient(24deg,rgba(6,16,24,.97) 34%,rgba(6,16,24,.74) 68%,rgba(6,16,24,.42) 100%);"></div>
    <div class="pad">
      <div class="kick">next</div>
      <h1 style="margin-top:.6cqw;">The season starts in twelve weeks.</h1>
      <p style="margin-top:1.2cqw;max-width:46ch;">Partners confirmed by 31 October travel with the delegation. After that we are selling coverage, not participation.</p>
      <div class="closebar">
        <div>
          <div style="font-family:var(--disp);font-weight:600;font-size:2cqw;color:var(--gold);">Baba Touré</div>
          <div style="font-size:1.24cqw;color:rgba(251,246,236,.86);">AToure Management &amp; Consulting &nbsp;·&nbsp; atoureconsulting@gmail.com</div>
        </div>
        <span class="presented"><span>presented by</span><span class="lgo">{logo_dark}</span></span>
      </div>
    </div>
    <div class="no">14</div>
  </section>""")

# ---------------------------------------------------------------- 15 light notes
S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3.2cqw 5cqw 2.6cqw;">
      <div class="kick">where the numbers come from</div>
      <div class="notes">
        <p><b>Audience.</b> Summed across Instagram, TikTok and Facebook for the ten invitees, from the client tracking sheet of September 2026. Not deduplicated between platforms.</p>
        <p><b>Delegation.</b> Ten invited, three reserves. No participation agreement is signed at the date of this document.</p>
        <p><b>Festival dates.</b> As published in September 2026. AfroFuture, Flytime Fest and Vodun Days are confirmed by their organisers. Several Abidjan dates remain unconfirmed and are not listed.</p>
        <p><b>Budget.</b> Rates researched September 2026 against published prices, not negotiated group rates. Production and insurance carry realistic lines but no quotes received. No sponsor contribution in kind deducted.</p>
        <p><b>Bénin.</b> Included on the strength of Vodun Days, 2 to 9 January 2027. Proposed, not confirmed.</p>
        <p><b>Partners.</b> Every organisation named is a target. None is contracted.</p>
        <p><b>Foundation.</b> Details and the Abobo figure come from Ivorian press including RTI, September 2026. The foundation's own site could not be reached from this machine.</p>
        <p><b>Photography.</b> Portraits supplied by the participants. Location, festival and event photography still to be commissioned.</p>
      </div>
      <div style="margin-top:auto;padding-top:1.3cqw;border-top:2px solid var(--edge);display:flex;
           justify-content:space-between;align-items:flex-end;">
        <span style="font-size:1.1cqw;color:var(--mid);">AToure Management &amp; Consulting. Company number 15129711, England and Wales.</span>
        <span class="presented"><span>presented by</span><span class="lgo">{logo_light}</span></span>
      </div>
    </div>
    <div class="no">15</div>
  </section>""")

assert len(S) == len(PLAN), "%d slides against a %d page plan" % (len(S), len(PLAN))
for i, (sec, theme) in enumerate(zip(S, PLAN), 1):
    want = theme.split()[-1]
    assert ('class="s %s' % want) in sec, "page %d is not tagged %s" % (i, want)

HTML = ("<!doctype html><meta charset=\"utf-8\"><title>Beauty Beyond Borders</title>\n"
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,'
        'wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Karla:wght@300;400;500;600'
        '&family=Caveat:wght@500;600;700&display=swap">\n<style>' + ROOT + CSS + "</style>\n"
        '<div class="deck">' + "".join(S) + "</div>\n")

out = SC + "/bbb-deck-v7.html"
open(out, "w").write(HTML)
body = HTML.split("</style>")[-1]
assert "—" not in body, "em-dash in copy"
assert body.count("<section") == 15
print("written", round(os.path.getsize(out) / 1e6, 2), "MB /", len(S), "slides")
print("rhythm:", " ".join("%d:%s" % (i, t) for i, t in enumerate(PLAN, 1)))
