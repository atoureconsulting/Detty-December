# -*- coding: utf-8 -*-
"""v8. Ten days, not seventeen. Colour-blocked slides alternate with
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

CLOTHBIG = cloth(tile=260, scale=2)
MAP = localimg(SC + "/route-map.png", 1500, q=90)

# ---------------------------------------------------------------- the ten
# Titles verified against national and international press, September 2026.
DELEG = [
    ("olivia-yace", "Olivia Yacé", "Côte d'Ivoire",
     "Miss World Africa 2021 · 4th runner-up, Miss Universe 2025", -3.0),
    ("sheynnis-palacios", "Sheynnis Palacios", "Nicaragua",
     "Miss Universe 2023", 2.4),
    ("angelique-angarni-filopon", "Angélique Angarni-Filopon", "Martinique",
     "Miss France 2025", -2.2),
    ("isabella-menin", "Isabella Menin", "Brazil",
     "Miss Grand International 2022", 3.0),
    ("ophely-mezino", "Ophély Mézino", "Guadeloupe",
     "1st runner-up, Miss World 2019 · Top 12, Miss Universe 2025", 1.7),
    ("veena-praveenar", "Veena Praveenar Singh", "Thailand",
     "Miss Universe Thailand 2025", -1.6),
    ("nadia-mejia", "Nadia Mejía", "Ecuador",
     "Miss Universe Ecuador 2025", -2.8),
    ("dorcas-dienda", "Dorcas Dienda", "DR Congo",
     "Miss Universe DR Congo 2025", 2.0),
    ("camille-thomas", "Camille Sabina Thomas", "Curaçao",
     "Miss Universe Curaçao 2025", -1.9),
    ("bella-zabaneh", "Bella Zabaneh", "Belize",
     "Miss Universe Belize 2025", 2.6),
]
PINS = "".join(f"""
        <figure class="pin" style="--r:{rot}deg">
          <img src="{img(slug, 320, 400, 0.02, warm=1.05)}" alt="{name}">
          <figcaption><b>{name}</b><span class="cy">{country}</span><span class="ac">{acc}</span></figcaption>
        </figure>""" for slug, name, country, acc, rot in DELEG)

STRIP = "".join(f'<img src="{img(slug, 200, 250, 0.02, warm=1.05)}" alt="{name}">'
                for slug, name, _, _, _ in DELEG)

# ---------------------------------------------------------------- reach
PROFILES = [
    ("Olivia Yacé", 1200, 1100, 760, True), ("Sheynnis Palacios", 2300, 2500, 1000, False),
    ("Veena Praveenar Singh", 2100, 472, 52, False), ("Isabella Menin", 1100, 205, 22, False),
    ("Angélique Angarni-Filopon", 394, 474, 0, False), ("Nadia Mejía", 434, 127, 5, False),
    ("Dorcas Dienda", 222, 263, 61, False), ("Ophély Mézino", 141, 39, 0, False),
    ("Bella Zabaneh", 23, 23, 4, False), ("Camille Sabina Thomas", 19, 4, 0, False),
]
kf = lambda k: ("%.1fM" % (k / 1000)).replace(".0M", "M") if k >= 1000 else "%dK" % round(k)
MAX = max(a + b + c for _, a, b, c, _ in PROFILES)
TOTALK = sum(a + b + c for _, a, b, c, _ in PROFILES)
TOTM = "%.0fM" % (TOTALK / 1000)
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
    ("Fally Ipupa", "CI", "24 &amp; 25 Dec", "Stade Félix-Houphouët-Boigny, Abidjan", "xl"),
    ("Mother Africa", "CI", "27 &amp; 28 Dec", "Marcory Zone 4, Abidjan", "xl"),
    ("AfroFuture", "GH", "28 to 30 Dec", "El-Wak Stadium, Accra", "l"),
    ("Flytime Fest", "NG", "22 to 25 Dec", "Eko Centre, Lagos", "l"),
    ("Rhythm Unplugged", "NG", "21 Dec", "Eko Centre, Lagos", "m"),
    ("Detty Rave", "GH", "27 Dec", "Accra", "m"),
    ("Rapperholic", "GH", "31 Dec", "Accra Sports Stadium", "sm"),
]
BILL = "".join(f"""
        <div class="act {sz}">
          <span class="an">{n}</span>
          <span class="ad">{flag(c,'fl tiny')} {d} &nbsp;·&nbsp; {v}</span>
        </div>""" for n, c, d, v, sz in POSTER)

# ---------------------------------------------------------------- the route, ten days
ITIN = [
    ("21", "Lagos", "NG", "Rhythm Unplugged, Eko Centre"),
    ("22", "Lagos", "NG", "Flytime Fest opens"),
    ("23", "Abidjan", "CI", "Arrival, Plateau and Cocody"),
    ("24", "Abidjan", "CI", "Fally Ipupa, Stade Félix-Houphouët-Boigny"),
    ("25", "Abidjan", "CI", "Fally Ipupa, second night"),
    ("26", "Assinie", "CI", "Coast day, Grand-Bassam"),
    ("27", "Abidjan", "CI", "Mother Africa Festival"),
    ("28", "Abidjan", "CI", "Mother Africa Festival, second night"),
    ("29", "Accra", "GH", "AfroFuture, El-Wak Stadium"),
    ("30", "Accra", "GH", "AfroFuture closing night"),
]
DAYS = "".join(f"""
          <div class="day">
            <span class="dn">{n}<em> Dec</em></span>
            <span class="dc">{flag(c,'fl tiny')} {city}</span>
            <span class="dx">{what}</span>
          </div>""" for n, city, c, what in ITIN)
PINSMAP = [("Lagos", 53.46, 70.75, "1", "r"), ("Abidjan", 24.33, 79.48, "2", "l"),
           ("Assinie", 27.24, 81.12, "3", "d"), ("Accra", 39.41, 77.61, "4", "d"),
           ("Ouidah", 48.39, 71.94, "", "u")]
MAPLBL = "".join(
    f'<span class="mp {sd}{"" if num else " opt"}" style="left:{x}%;top:{y}%">'
    f'{"<b>" + num + "</b>" if num else ""}<span>{n}</span></span>'
    for n, x, y, num, sd in PINSMAP)
MAPCTY = "".join(f'<span class="mc" style="left:{x}%;top:{y}%">{n}</span>'
                 for n, x, y in [("Côte d'Ivoire", 17.22, 59.55), ("Ghana", 35.91, 57.48),
                                 ("Nigeria", 70.72, 54.97), ("Bénin", 49.39, 40.0)])

# ---------------------------------------------------------------- the season, sourced
SEASON = [
    ("$71.6m", "into the Lagos economy from Detty December 2024 alone, on 1.2 million visitors",
     "Lagos State Government, January 2025"),
    ("1.29m", "international visitors to Ghana in 2024, up 12 per cent, worth $4.82bn in receipts",
     "Ghana Tourism Authority, 2024 Tourism Report"),
    ("6.7m", "visitors to Côte d'Ivoire in 2025, from 6.3 million the year before",
     "Ministère du Tourisme, Côte d'Ivoire"),
    ("40%", "of annual revenue earned in one month by many hospitality and retail businesses",
     "Ghana Tourism Authority, reported December 2025"),
]
SEAS = "".join(f"""
        <div class="sn">
          <span class="sfig">{f}</span>
          <span class="sl">{t}</span>
          <span class="ss">{src}</span>
        </div>""" for f, t, src in SEASON)

# ---------------------------------------------------------------- what a brand can get
BRAND = [
    ("Category ownership",
     "One partner per category for the whole tour, named in the series and in every release. "
     "The telecoms partner, the airline partner, the beauty partner."),
    ("Collaboration with the delegation",
     "Content shot with all ten, or with a chosen number. Scope sets the size of the group, "
     "not the other way round."),
    ("Their own channels",
     "An agreed number of posts from each participant, across roughly fifteen million followers "
     "that the partner does not have to buy."),
    ("Image and likeness rights",
     "Licensed stills and footage of named participants for the partner's own campaigns, "
     "for an agreed territory and term."),
    ("Ten markets, not one",
     "The delegation spans ten countries across Africa, Europe, Asia, the Caribbean and Latin "
     "America. A campaign shot in Abidjan runs where a local shoot never reaches."),
    ("A stop on the itinerary",
     "A venue, a product or an activation written into the ten days as a filmed moment."),
]
BRANDS = "".join(f"""
        <div class="bcard"><b>{t}</b><span>{x}</span></div>""" for t, x in BRAND)

# ---------------------------------------------------------------- the number, ten days
BUDGET = [("Accommodation", "36,000"), ("Regional air travel", "28,000"),
          ("Production and content crew", "52,000"), ("Per diem and hospitality", "14,000"),
          ("Ground transport and security", "15,000"), ("Insurance", "12,000"),
          ("Visas and administration", "6,000"), ("Contingency", "22,000")]
assert sum(int(b.replace(",", "")) for _, b in BUDGET) == 185000
BUD = "".join(f"<tr><td>{a}</td><td class='amt'>€{b}</td></tr>" for a, b in BUDGET)

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
  .nums .fig{font-family:var(--disp);font-weight:700;font-size:8.6cqw;line-height:.9;
     letter-spacing:-.03em;color:var(--cocoa);display:block;}
  .nums .lab{display:block;margin-top:.7cqw;font-size:1.38cqw;line-height:1.45;color:var(--cocoa2);}
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
  .pin b{display:block;font-family:var(--disp);font-weight:600;font-size:1.05cqw;line-height:1.15;
     color:var(--cocoa);min-height:2.42cqw;}
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
  .foystack{display:flex;flex-direction:column;gap:1.1cqw;}
  .foyshot{width:100%;aspect-ratio:4/3;object-fit:cover;object-position:top center;display:block;
     box-shadow:0 8px 24px rgba(62,43,29,.25);}
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
  .notes{columns:3;column-gap:2.8cqw;margin-top:1.2cqw;}
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



CSS += """
  /* ---------- portrait strip ---------- */
  .strip{position:absolute;left:0;right:0;bottom:0;z-index:2;display:grid;
     grid-template-columns:repeat(10,1fr);}
  .strip img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top center;display:block;}
  .strip:after{content:"";position:absolute;inset:0;
     box-shadow:inset 0 3px 0 var(--orange);pointer-events:none;}

  /* ---------- accolades on the prints ---------- */
  .pin .cy{display:block;font-size:.84cqw;color:var(--orange);margin-top:.14cqw;
     letter-spacing:.05em;text-transform:uppercase;}
  .pin .ac{display:block;font-size:.78cqw;line-height:1.3;color:var(--mid);margin-top:.2cqw;
     min-height:2.03cqw;}

  /* ---------- poster, with air ---------- */
  .bill{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;
     gap:1.5cqw;text-align:center;}
  .act .ad{margin-top:.5cqw;}

  /* ---------- the season, sourced ---------- */
  .seasongrid{display:grid;grid-template-columns:repeat(2,1fr);gap:2.2cqw 4cqw;
     margin-top:auto;margin-bottom:auto;}
  .sn{border-top:3px solid var(--orange);padding-top:.9cqw;}
  .sn:nth-child(2){border-color:var(--green);} .sn:nth-child(3){border-color:var(--gold);}
  .sn:nth-child(4){border-color:var(--rust);}
  .sfig{display:block;font-family:var(--disp);font-weight:700;font-size:4.4cqw;line-height:.95;
     letter-spacing:-.025em;color:var(--cocoa);}
  .sl{display:block;margin-top:.5cqw;font-size:1.34cqw;line-height:1.45;color:var(--cocoa2);
     max-width:30ch;}
  .ss{display:block;margin-top:.45cqw;font-size:.98cqw;color:var(--mid);font-style:italic;}

  /* ---------- the route ---------- */
  .routewrap{display:grid;grid-template-columns:1fr 22cqw;gap:2.6cqw;flex:1;min-height:0;
     margin-top:.8cqw;}
  .mapcol{display:flex;flex-direction:column;justify-content:center;gap:.9cqw;}
  .mapbox{position:relative;}
  .mapcap{font-size:1.02cqw;color:rgba(251,246,236,.6);line-height:1.45;}
  .mapbox img{width:100%;display:block;}
  .mp{position:absolute;display:flex;align-items:center;gap:.4cqw;white-space:nowrap;}
  .mp.r{transform:translate(-.95cqw,-50%);}
  .mp.l{transform:translate(calc(-100% + .95cqw),-50%);flex-direction:row-reverse;}
  .mp.d{transform:translate(-50%,-.95cqw);flex-direction:column;gap:.25cqw;}
  .mp.u{transform:translate(-50%,calc(-100% + .95cqw));flex-direction:column-reverse;gap:.25cqw;}
  .mp b{width:1.9cqw;height:1.9cqw;border-radius:50%;background:var(--orange);color:#fff;
     font-family:var(--disp);font-size:1.15cqw;display:flex;align-items:center;
     justify-content:center;flex:none;}
  .mp span{font-size:1.1cqw;color:var(--ivory);background:rgba(6,20,28,.72);
     padding:.1cqw .42cqw;border-radius:.25cqw;}
  .mp.opt span{color:rgba(251,246,236,.62);font-style:italic;}
  .mc{position:absolute;transform:translate(-50%,-50%);font-family:var(--disp);font-weight:600;
     font-size:1.35cqw;color:rgba(255,255,255,.78);letter-spacing:.08em;pointer-events:none;}
  .days{display:flex;flex-direction:column;gap:.34cqw;align-self:center;}
  .day{display:grid;grid-template-columns:4.6cqw 1fr;gap:.6cqw;align-items:baseline;
     padding-bottom:.34cqw;border-bottom:1px solid rgba(255,255,255,.13);}
  .dn{font-family:var(--disp);font-weight:700;font-size:1.5cqw;color:var(--gold);}
  .dn em{font-style:normal;font-size:.82cqw;font-weight:400;}
  .dc{font-size:1.14cqw;color:var(--ivory);}
  .dx{grid-column:2;font-size:.94cqw;color:rgba(251,246,236,.66);line-height:1.3;}

  /* ---------- what a brand can get ---------- */
  .bgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.6cqw 1.8cqw;flex:1;min-height:0;
     align-content:space-evenly;margin-top:1.2cqw;}
  .bcard{border-top:2px solid var(--orange);padding-top:.85cqw;}
  .bcard:nth-child(3n+2){border-color:var(--green);}
  .bcard:nth-child(3n){border-color:var(--gold);}
  .bcard b{display:block;font-family:var(--disp);font-weight:600;font-size:1.86cqw;
     line-height:1.12;color:var(--cocoa);}
  .bcard span{display:block;margin-top:.5cqw;font-size:1.2cqw;line-height:1.5;color:var(--cocoa2);}
"""

PLAN = ["hero dark", "light", "dark", "hero light", "light", "dark", "light",
        "hero dark", "dark", "light", "dark", "hero light", "dark", "hero light",
        "light", "dark", "light", "hero dark", "light"]
base = [t.split()[-1] for t in PLAN]
for i in range(len(base) - 2):
    assert len(set(base[i:i + 3])) > 1, "three %s pages in a row at %d" % (base[i], i + 1)
assert "hero dark" in PLAN and "hero light" in PLAN
_h = [i for i, t in enumerate(PLAN) if t.startswith("hero")]
assert max(b - a for a, b in zip(_h, _h[1:])) <= 4, "hero gap too wide"

S = []
S.append(f"""
  <section class="s dark cover onphoto">
    <div class="bleed"><img src="{img('olivia-yace', 1400, 788, 0.0, warm=1.06)}" alt="Olivia Yacé"></div>
    <div class="cwash"></div>
    <div class="seal"><b>10</b>women<br>ten days</div>
    <div class="pad" style="padding:3.4cqw 4.4cqw 4.4cqw;">
      <div>
        <div class="masthead">Beauty Beyond Borders</div>
        <div class="mrule"></div>
        <div class="mline">West Africa &nbsp;·&nbsp; 21 to 30 December 2026</div>
      </div>
      <div style="margin-top:auto;">
        <span class="cl1">Ten women. Ten days.<br>Three countries.</span>
        <span class="cl2">and a season that never needed an introduction</span>
        <div class="presented" style="margin-top:1.7cqw;">
          <span>presented by</span><span class="lgo">{logo_dark}</span>
        </div>
      </div>
    </div>
    <div class="no">1</div>
  </section>""")

S.append(f"""
  <section class="s light">
    <div class="pad" style="padding-bottom:14.5cqw;">
      <div class="kick">the shape of it</div>
      <div style="display:grid;grid-template-columns:1fr 34cqw;gap:5cqw;align-items:end;margin-top:.5cqw;">
        <h2 style="font-size:3.4cqw;max-width:20ch;">Four numbers, before anything else.</h2>
        <p style="font-size:1.54cqw;">Every other page here is an argument. This one is the arithmetic, and the arithmetic is why the tour is worth building.</p>
      </div>
      <div class="nums" style="margin-top:auto;margin-bottom:auto;">
        <div class="n"><span class="fig">10</span>
          <span class="lab"><b>titleholders</b>invited by Olivia Yacé, travelling as one delegation</span></div>
        <div class="n"><span class="fig">10</span>
          <span class="lab"><b>days</b>21 to 30 December, six of them Ivorian</span></div>
        <div class="n"><span class="fig">3</span>
          <span class="lab"><b>countries</b>Côte d'Ivoire, Ghana, Nigeria</span></div>
        <div class="n"><span class="fig">{TOTM}</span>
          <span class="lab"><b>followers</b>across the delegation, before a partner is added</span></div>
      </div>
      <div class="strip">{STRIP}</div>
    </div>
    <div class="no">2</div>
  </section>""")

S.append(f"""
  <section class="s dark">
    <div class="pad">
      <div class="kick">what this is</div>
      <div class="lead">
        <div class="shot"><img src="{img('sheynnis-palacios', 620, 830, 0.0, warm=1.04)}" alt=""></div>
        <div class="side">
          <h2 style="font-size:4cqw;color:var(--ivory);max-width:16ch;">Not a trip.<br>A moment.</h2>
          <p style="margin-top:1.4cqw;max-width:48ch;">Seven of the ten stood on the Miss Universe stage in Bangkok last November. One of them won Miss Universe outright in 2023. One is the reigning Miss France. One is Miss Grand International.</p>
          <p style="max-width:48ch;">They travel West Africa together for ten days as one delegation, hosted by Olivia Yacé, through the busiest fortnight in the region's calendar.</p>
          <div class="hand" style="margin-top:1.6cqw;font-size:2.3cqw;color:var(--gold);">They land on 21 December. The season is already running.</div>
        </div>
      </div>
    </div>
    <div class="no">3</div>
  </section>""")

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

S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3cqw 5cqw;">
      <div class="kick">the delegation</div>
      <div class="pinwrap">
        <div class="pinband clothstrip"></div>
        <div class="pins">{PINS}</div>
      </div>
    </div>
    <div class="no">5</div>
  </section>""")

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

S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3.4cqw 5cqw;">
      <div class="kick">social impact</div>
      <div class="foy" style="margin-top:.9cqw;">
        <div class="foystack">
          <div class="foycard"><img src="{FOY}" alt="Fondation Olivia Yacé"></div>
          <img class="foyshot" src="{img('olivia-yace', 520, 390, 0.0, warm=1.05)}" alt="Olivia Yacé">
        </div>
        <div>
          <h2 style="font-size:3.1cqw;max-width:22ch;">The tour has a foundation behind it.</h2>
          <p style="margin-top:1cqw;max-width:48ch;">Founded in 2025 and anchored in Côte d'Ivoire, the Fondation Olivia Yacé puts vulnerable children, and girls in particular, into school and keeps them there. The delegation works alongside it, and alongside partner foundations in Ghana and Nigeria, during the ten days.</p>
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

S.append(f"""
  <section class="s dark divider onphoto">
    <div class="bleed"><img src="{duotone('isabella-menin', 1400, 788, (8,26,38), (240,196,130), 0.0)}" alt=""></div>
    <div class="dimwash"></div>
    <div class="pad" style="padding-left:6.5cqw;">
      <div class="act-no">Act two</div>
      <div class="act-t" style="color:var(--ivory);">The season</div>
      <div class="act-s">21 to 31 December, the coast does not sleep</div>
    </div>
    <div class="no">8</div>
  </section>""")

S.append(f"""
  <section class="s dark">
    <div class="pad" style="padding:3cqw 5cqw;">
      <div style="text-align:center;"><div class="kick">what is already booked</div></div>
      <div class="bill">{BILL}</div>
      <div style="margin-top:1.6cqw;text-align:center;font-size:1.12cqw;color:rgba(251,246,236,.58);">Published dates, September 2026. Several Abidjan dates remain unconfirmed and are not listed. Vodun Days, Ouidah, 2 to 9 January 2027, sits outside the ten days and is costed separately as an extension.</div>
    </div>
    <div class="no">9</div>
  </section>""")

S.append(f"""
  <section class="s light">
    <div class="pad">
      <div class="kick">why December</div>
      <h2 style="margin-top:.4cqw;font-size:3.2cqw;max-width:34ch;">This is the region's biggest month, and it is already measured.</h2>
      <div class="seasongrid">{SEAS}</div>
      <div class="hand" style="font-size:2cqw;color:var(--green);">We are not creating an audience. We are arriving inside one.</div>
    </div>
    <div class="no">10</div>
  </section>""")

S.append(f"""
  <section class="s dark">
    <div class="pad" style="padding:3.2cqw 5cqw;">
      <div class="kick">the route</div>
      <h2 style="margin-top:.4cqw;font-size:2.9cqw;color:var(--ivory);">Ten days along one coast.</h2>
      <div class="routewrap">
        <div class="mapcol">
          <div class="mapbox">
            <img src="{MAP}" alt="Route map">
            {MAPCTY}{MAPLBL}
          </div>
          <div class="mapcap">Stops are proposed, not booked. Ouidah is shown hollow: Vodun Days runs 2 to 9 January 2027 and sits outside the ten days, costed separately as an extension.</div>
        </div>
        <div class="days">{DAYS}</div>
      </div>
    </div>
    <div class="no">11</div>
  </section>""")

S.append("""
  <section class="s light bigq">
    <div class="edgecloth clothstrip" style="width:4.4cqw;"></div>
    <div class="pad">
      <span class="mark">&ldquo;</span>
      <blockquote>West Africa in December is not a destination. It is a homecoming the rest of the world has not been invited to yet.</blockquote>
      <div class="attr">the case for this tour</div>
    </div>
    <div class="no">12</div>
  </section>""")

S.append(f"""
  <section class="s dark onphoto">
    <div class="bleed"><img src="{img('veena-praveenar', 1400, 788, 0.0, warm=1.05)}" alt=""></div>
    <div style="position:absolute;inset:0;z-index:1;background:linear-gradient(95deg,rgba(18,10,4,.94) 0%,rgba(18,10,4,.64) 42%,rgba(18,10,4,.04) 76%);"></div>
    <div class="pad" style="justify-content:center;">
      <div style="max-width:45cqw;">
        <div class="kick">filmed</div>
        <h2 style="margin-top:.7cqw;font-size:4.2cqw;color:var(--ivory);">Shot by a production team, as a series.</h2>
        <p style="margin-top:1.2cqw;">A director, a two camera crew, a stills photographer and an editor travel with the delegation for the full ten days. A short edit goes out every day and the whole thing cuts as a series afterwards.</p>
        <p style="margin-top:.9cqw;">Broadcast rights are a second revenue line, and every partner keeps a rights cleared archive that outlives the ten days.</p>
      </div>
    </div>
    <div class="no">13</div>
  </section>""")

S.append("""
  <section class="s light divider">
    <div class="edgecloth clothstrip"></div>
    <div class="pad" style="padding-left:12cqw;">
      <div class="act-no">Act three</div>
      <div class="act-t">The offer</div>
      <div class="act-s">possibilities, not packages, until scope is set</div>
    </div>
    <div class="no">14</div>
  </section>""")

S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3.2cqw 5cqw;">
      <div class="kick">what a brand can get</div>
      <div style="display:grid;grid-template-columns:1fr 32cqw;gap:4cqw;align-items:end;margin-top:.4cqw;">
        <h2 style="font-size:2.9cqw;max-width:26ch;">Six ways a partner is visible, and none of them is a logo on a banner.</h2>
        <p style="font-size:1.42cqw;">The delegation is the media. A partner buys access to ten women with their own audiences, in a month when the whole region is already looking.</p>
      </div>
      <div class="bgrid">{BRANDS}</div>
      <div style="font-size:1.12cqw;color:var(--mid);font-style:italic;">These are possibilities, not packages. What a partner actually receives is set by scope and by budget, and is written into the agreement before anything is announced.</div>
    </div>
    <div class="no">15</div>
  </section>""")

S.append("""
  <section class="s dark" style="background:#0B7A4B;">
    <div class="pad">
      <div class="kick">who we are talking to</div>
      <h2 style="margin-top:.5cqw;font-size:4cqw;color:var(--ivory);">One partner per category.</h2>
      <div class="ask">
        <ul>
          <li>Category exclusivity across three markets</li>
          <li>Presence inside the series, not around it</li>
          <li>The delegation's audience and the press behind it</li>
          <li>A named role in the foundation programme</li>
          <li>A rights cleared archive to reuse</li>
        </ul>
        <div class="tgt">
          <b>Governments</b><span>Sublime Côte d'Ivoire. Ghana Ministry of Tourism. Lagos State Tourism.</span>
          <b>Travel</b><span>Air Côte d'Ivoire. Accor. Kempinski. Eko Hotels.</span>
          <b>Consumer</b><span>Telecoms, banking, beauty, jewellery and watches, approached through the participants who have worked with them before.</span>
        </div>
      </div>
      <div class="hand" style="font-size:2cqw;color:var(--gold);">Exclusivity is what makes a category worth buying.</div>
    </div>
    <div class="no">16</div>
  </section>""")

S.append(f"""
  <section class="s light">
    <div class="edgecloth clothstrip" style="width:5.2cqw;"></div>
    <div class="pad" style="padding-left:11cqw;">
      <div class="kick">the number</div>
      <h2 style="margin-top:.4cqw;font-size:4cqw;">€185,000 delivers it.</h2>
      <table class="bud">{BUD}<tr><td>Total</td><td class="amt">€185,000</td></tr></table>
      <div class="hand" style="margin-top:auto;font-size:1.9cqw;color:var(--green);">Ten days, three countries, twenty people on the ground. Every confirmed partner brings this number down.</div>
    </div>
    <div class="no">17</div>
  </section>""")

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
    <div class="no">18</div>
  </section>""")

S.append(f"""
  <section class="s light">
    <div class="pad" style="padding:3cqw 5cqw 2.4cqw;">
      <div class="kick">where the numbers come from</div>
      <div class="notes">
        <p><b>Titles.</b> Verified September 2026 against national and international press. Seven of the ten competed at Miss Universe 2025 in Bangkok. Olivia Yacé placed fourth runner-up there and is an official tourism ambassador for Côte d'Ivoire.</p>
        <p><b>Audience.</b> Summed across Instagram, TikTok and Facebook from the client tracking sheet of September 2026. Not deduplicated between platforms.</p>
        <p><b>Delegation.</b> Ten invited, three reserves. No participation agreement is signed at the date of this document.</p>
        <p><b>Lagos.</b> $71.6m and 1.2 million visitors for December 2024, Lagos State Government, reported January 2025.</p>
        <p><b>Ghana.</b> 1,288,804 international visitors in 2024, up 12 per cent, $4.82bn in receipts. Ghana Tourism Authority 2024 Tourism Report.</p>
        <p><b>Côte d'Ivoire.</b> 6.7 million visitors in 2025 against 6.3 million in 2024, Ministère du Tourisme.</p>
        <p><b>Festival dates.</b> As published in September 2026. Several Abidjan dates remain unconfirmed and are not listed.</p>
        <p><b>Route map.</b> Drawn from Natural Earth 1:50m country geometry. Stops are proposed, not booked.</p>
        <p><b>Budget.</b> A ten day model at twenty people on the ground. Rates researched September 2026 against published prices, not negotiated group rates. No quotes received and no contribution in kind deducted.</p>
        <p><b>Bénin.</b> Vodun Days, 2 to 9 January 2027, falls outside the ten days. Costed separately as an extension.</p>
        <p><b>Partners.</b> Every organisation named is a target. None is contracted.</p>
        <p><b>Foundation.</b> Details and the Abobo figure come from Ivorian press including RTI, September 2026. The foundation's own site could not be reached from this machine.</p>
        <p><b>Photography.</b> Portraits supplied by the participants. Location, festival and event photography still to be commissioned.</p>
      </div>
      <div style="margin-top:auto;padding-top:1.2cqw;border-top:2px solid var(--edge);display:flex;
           justify-content:space-between;align-items:flex-end;">
        <span style="font-size:1.1cqw;color:var(--mid);">AToure Management &amp; Consulting. Company number 15129711, England and Wales.</span>
        <span class="presented"><span>presented by</span><span class="lgo">{logo_light}</span></span>
      </div>
    </div>
    <div class="no">19</div>
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

out = SC + "/bbb-deck-v8.html"
open(out, "w").write(HTML)
body = HTML.split("</style>")[-1]
assert "—" not in body, "em-dash in copy"
assert body.count("<section") == 19
assert "seventeen" not in body.lower() and "Seventeen" not in body
assert "€250,000" not in body and "fortnight" in body
print("written", round(os.path.getsize(out) / 1e6, 2), "MB /", len(S), "slides")
