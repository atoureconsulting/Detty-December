# -*- coding: utf-8 -*-
"""v11. Ten pages. Two registers on purpose: an editorial travel magazine that shifts into a
   festival poster for Act Two, then shifts back. Location and festival
   photography from the client Drive, September 2026."""
import base64, io, os
from PIL import Image

SC = os.environ.get("BBB_WORK", os.path.dirname(os.path.abspath(__file__)))
PH = os.environ.get("BBB_PHOTOS", os.path.join(SC, "photos")) + "/"
MD = SC + "/media/"
BK = SC + "/brandkit/"

PAPER, INK, MUTED, FAINT, RULE = "#FAF6EF", "#1E1A15", "#6A6154", "#9A8B72", "#D9CDB8"
ACCENT, GREEN = "#C2560A", "#0B7A4B"
BLACK, POP, POPG = "#0A0A0A", "#FF7A18", "#12B26A"

SRC = {"skyline": MD + "AFRIQUEMAGAZINE_466_20250708-(3).pdf-image-010.jpg",
       "assinie": MD + "assinie.webp",
       "crowd":   MD + "Photo-by-Afronation-com.jpeg",
       "stage":   MD + "Au-festival-de-musique-Mother-Africa.jpg",
       "poster":  MD + "Mother-Africa.jpeg"}

def _uri(im, q=85):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def _fit(im, w, h, fx=0.5, fy=0.5):
    ow, oh = im.size; t = w / h
    if ow / oh > t:
        nw = int(oh * t); im = im.crop((int((ow - nw) * fx), 0, int((ow - nw) * fx) + nw, oh))
    else:
        nh = int(ow / t); im = im.crop((0, int((oh - nh) * fy), ow, int((oh - nh) * fy) + nh))
    return im.resize((w, h), Image.LANCZOS)

def loc(key, w, h, fx=0.5, fy=0.5, q=85):
    return _uri(_fit(Image.open(SRC[key]).convert("RGB"), w, h, fx, fy), q)

def por(slug, w, h, fy=0.04, warm=1.05):
    im = _fit(Image.open(PH + slug + ".jpg").convert("RGB"), w, h, 0.5, fy)
    if warm != 1.0:
        r, g, b = im.split()
        r = r.point(lambda v: min(255, int(v * warm))); b = b.point(lambda v: int(v / warm))
        im = Image.merge("RGB", (r, g, b))
    return _uri(im)

def localimg(path, w, q=88):
    im = Image.open(path).convert("RGB")
    return _uri(im.resize((w, int(w * im.size[1] / im.size[0])), Image.LANCZOS), q)

MAP = localimg(SC + "/route-map-dark.png", 1240, 90)
FOY = localimg(SC + "/foy-logo-b.jpg", 560)
logo_dark = open(BK + "01-logos/atoure/atoure-nav-lockup-on-dark.svg").read().replace(
    'width="2926" height="517"', 'width="100%" height="100%" preserveAspectRatio="xMinYMid meet"', 1)
logo_light = open(BK + "01-logos/atoure/atoure-nav-lockup-on-light.svg").read().replace(
    'width="2926" height="517"', 'width="100%" height="100%" preserveAspectRatio="xMinYMid meet"', 1)

def flag(code, cls="fl"):
    S = '<svg class="%s" viewBox="0 0 30 20" preserveAspectRatio="none">' % cls
    if code == "CI":
        S += ('<rect width="10" height="20" fill="#F77F00"/><rect x="10" width="10" height="20" fill="#fff"/>'
              '<rect x="20" width="10" height="20" fill="#009E60"/>')
    elif code == "GH":
        S += ('<rect width="30" height="6.67" fill="#CE1126"/><rect y="6.67" width="30" height="6.66" fill="#FCD116"/>'
              '<rect y="13.33" width="30" height="6.67" fill="#006B3F"/>'
              '<polygon fill="#000" points="15,7.1 16.05,10.2 19.3,10.2 16.65,12.1 17.7,15.2 15,13.3 12.3,15.2 13.35,12.1 10.7,10.2 13.95,10.2"/>')
    elif code == "NG":
        S += ('<rect width="10" height="20" fill="#008751"/><rect x="10" width="10" height="20" fill="#fff"/>'
              '<rect x="20" width="10" height="20" fill="#008751"/>')
    return S + "</svg>"

# ---------------------------------------------------------------- data
DELEG = [
    ("olivia-yace", "Olivia Yacé", "Côte d'Ivoire", "Miss World Africa 2021"),
    ("sheynnis-palacios", "Sheynnis Palacios", "Nicaragua", "Miss Universe 2023"),
    ("angelique-angarni-filopon", "Angélique Angarni-Filopon", "Martinique", "Miss France 2025"),
    ("isabella-menin", "Isabella Menin", "Brazil", "Miss Grand International 2022"),
    ("ophely-mezino", "Ophély Mézino", "Guadeloupe", "1st runner-up, Miss World 2019"),
    ("veena-praveenar", "Veena Praveenar Singh", "Thailand", "Miss Universe Thailand 2025"),
    ("nadia-mejia", "Nadia Mejía", "Ecuador", "Miss Universe Ecuador 2025"),
    ("dorcas-dienda", "Dorcas Dienda", "DR Congo", "Miss Universe DR Congo 2025"),
    ("camille-thomas", "Camille Sabina Thomas", "Curaçao", "Miss Universe Curaçao 2025"),
    ("bella-zabaneh", "Bella Zabaneh", "Belize", "Miss Universe Belize 2025"),
]
CARDS = "".join(f"""
        <figure class="pcard">
          <img src="{por(s, 440, 440)}" alt="{n}">
          <figcaption><b>{n}</b><span>{c}</span><em>{a}</em></figcaption>
        </figure>""" for s, n, c, a in DELEG)
BAND = "".join(f'<img src="{por(s, 320, 320)}" alt="{n}">' for s, n, _, _ in DELEG[:5])

PROFILES = [
    ("Olivia Yacé", 1200, 1100, 760, True), ("Sheynnis Palacios", 2300, 2500, 1000, False),
    ("Veena Praveenar Singh", 2100, 472, 52, False), ("Isabella Menin", 1100, 205, 22, False),
    ("Angélique Angarni-Filopon", 394, 474, 0, False), ("Nadia Mejía", 434, 127, 5, False),
    ("Dorcas Dienda", 222, 263, 61, False), ("Ophély Mézino", 141, 39, 0, False),
    ("Bella Zabaneh", 23, 23, 4, False), ("Camille Sabina Thomas", 19, 4, 0, False),
]
kf = lambda k: ("%.1fM" % (k / 1000)).replace(".0M", "M") if k >= 1000 else "%dK" % round(k)
MAXR = max(a + b + c for _, a, b, c, _ in PROFILES)
TOTM = "%.0fM" % (sum(a + b + c for _, a, b, c, _ in PROFILES) / 1000)
ROWS = "".join(
    '<div class="prow"><span class="pn">%s%s</span><span class="ptrack"><span class="pbar" '
    'style="width:%.2f%%">%s</span></span><span class="pt">%s</span></div>' % (
        n, ' <i>host</i>' if h else '', (ig + tt + fb) / MAXR * 100,
        "".join('<i class="%s" style="flex:%d"></i>' % (c, v)
                for v, c in ((ig, "ig"), (tt, "tt"), (fb, "fb")) if v), kf(ig + tt + fb))
    for n, ig, tt, fb, h in PROFILES)

POSTER = [("Fally Ipupa", "CI", "24&ndash;25 Dec", "Stade Félix-Houphouët-Boigny, Abidjan", ""),
          ("Mother Africa", "CI", "27&ndash;28 Dec", "Marcory Zone 4, Abidjan", ""),
          ("AfroFuture", "GH", "28&ndash;30 Dec", "El-Wak Stadium, Accra", ""),
          ("Flytime Fest", "NG", "22&ndash;25 Dec", "Eko Centre, Lagos", "sm"),
          ("Rhythm Unplugged", "NG", "21 Dec", "Eko Centre, Lagos", "sm"),
          ("Detty Rave", "GH", "27 Dec", "Accra", "sm"),
          ("Rapperholic", "GH", "31 Dec", "Accra Sports Stadium", "sm")]
BILL = "".join(f"""
        <div class="line {z}"><span>{n}</span><i>{flag(c,'fl tiny')} {d} &nbsp;·&nbsp; {v}</i></div>"""
               for n, c, d, v, z in POSTER)

SEASON = [("$71.6m", "into the Lagos economy from Detty December 2024, on 1.2 million visitors",
           "Lagos State Government, January 2025"),
          ("1.29m", "international visitors to Ghana in 2024, up 12 per cent, worth $4.82bn",
           "Ghana Tourism Authority, 2024 Tourism Report"),
          ("6.7m", "visitors to Côte d'Ivoire in 2025, from 6.3 million the year before",
           "Ministère du Tourisme, Côte d'Ivoire"),
          ("40%", "of annual revenue earned in one month by many hospitality businesses",
           "Ghana Tourism Authority, December 2025")]
SEAS = "".join(f'<div class="sfig"><b>{f}</b><span>{t}</span><em>{s}</em></div>' for f, t, s in SEASON)

ITIN = [("21", "Lagos", "NG", "Rhythm Unplugged, Eko Centre"),
        ("22", "Lagos", "NG", "Flytime Fest opens"),
        ("23", "Abidjan", "CI", "Arrival, Plateau and Cocody"),
        ("24", "Abidjan", "CI", "Fally Ipupa, Stade Félix-Houphouët-Boigny"),
        ("25", "Abidjan", "CI", "Fally Ipupa, second night"),
        ("26", "Assinie", "CI", "Coast day, Grand-Bassam"),
        ("27", "Abidjan", "CI", "Mother Africa Festival"),
        ("28", "Abidjan", "CI", "Mother Africa Festival, second night"),
        ("29", "Accra", "GH", "AfroFuture, El-Wak Stadium"),
        ("30", "Accra", "GH", "AfroFuture closing night")]
DAYS = "".join(f"""
          <div class="day"><b>{n}</b><span>{flag(c,'fl tiny')} {city}</span><em>{w}</em></div>"""
               for n, city, c, w in ITIN)
MAPLBL = "".join(
    f'<span class="mp {sd}{"" if num else " opt"}" style="left:{x}%;top:{y}%">'
    f'{"<b>" + num + "</b>" if num else ""}<span>{n}</span></span>'
    for n, x, y, num, sd in [("Lagos", 53.46, 68.40, "1", "r"), ("Abidjan", 24.33, 75.62, "2", "l"),
                             ("Assinie", 27.24, 76.98, "3", "d"), ("Accra", 39.41, 74.07, "4", "d"),
                             ("Ouidah", 48.39, 69.38, "", "u")])
MAPCTY = "".join(f'<span class="mc" style="left:{x}%;top:{y}%">{n}</span>'
                 for n, x, y in [("Côte d'Ivoire", 17.22, 59.14), ("Ghana", 35.91, 57.42),
                                 ("Nigeria", 70.72, 55.35), ("Bénin", 49.39, 43.5)])

BRAND = [("Category ownership", "One partner per category for the whole tour, named in the series and in every release. The telecoms partner, the airline partner, the beauty partner."),
         ("Collaboration with the delegation", "Content shot with all ten, or with a chosen number. Scope sets the size of the group, not the other way round."),
         ("Their own channels", "An agreed number of posts from each participant, across roughly fifteen million followers the partner does not have to buy."),
         ("Image and likeness rights", "Licensed stills and footage of named participants for the partner's own campaigns, for an agreed territory and term."),
         ("Ten markets, not one", "The delegation spans ten countries across Africa, Europe, Asia, the Caribbean and Latin America. A campaign shot in Abidjan runs where a local shoot never reaches."),
         ("A stop on the itinerary", "A venue, a product or an activation written into the ten days as a filmed moment.")]
BRANDS = "".join(f'<div class="bcard"><b>{t}</b><span>{x}</span></div>' for t, x in BRAND)

BUDGET = [("Accommodation", "36,000"), ("Regional air travel", "28,000"),
          ("Production and content crew", "52,000"), ("Per diem and hospitality", "14,000"),
          ("Ground transport and security", "15,000"), ("Insurance", "12,000"),
          ("Visas and administration", "6,000"), ("Contingency", "22,000")]
assert sum(int(b.replace(",", "")) for _, b in BUDGET) == 185000
BUD = "".join(f"<tr><td>{a}</td><td>€{b}</td></tr>" for a, b in BUDGET)

CSS = """
  *{box-sizing:border-box;}
  body{margin:0;background:#141210;font-family:'Karla',Arial,sans-serif;}
  .deck{display:flex;flex-direction:column;align-items:center;gap:18px;
     padding-block:18px;padding-inline:16px;}
  .s{width:100%;max-width:1120px;aspect-ratio:16/9;position:relative;overflow:hidden;
     container-type:inline-size;box-shadow:0 3px 20px rgba(0,0,0,.4);
     background:var(--paper);color:var(--ink);}
  .bleed{position:absolute;inset:0;z-index:0;}
  .bleed img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block;}
  .pad{position:relative;z-index:3;height:100%;padding:4.2cqw 5.2cqw;display:flex;
     flex-direction:column;}
  .fl{width:1.9cqw;height:1.27cqw;display:inline-block;vertical-align:-.1cqw;
     box-shadow:0 0 0 1px rgba(255,255,255,.3);}
  .fl.tiny{width:1.5cqw;height:1cqw;}

  /* ---------- editorial register ---------- */
  .lab{font:400 1cqw/1 'Karla';letter-spacing:.34em;text-transform:uppercase;color:var(--faint);}
  .fol{position:absolute;left:5.2cqw;right:5.2cqw;bottom:2.4cqw;z-index:4;display:flex;
     justify-content:space-between;align-items:baseline;border-top:1px solid var(--rule);
     padding-top:.9cqw;font:400 .92cqw/1 'Karla';letter-spacing:.26em;text-transform:uppercase;
     color:var(--faint);}
  h1,h2{font-family:'Fraunces',Georgia,serif;font-weight:300;margin:0;letter-spacing:-.008em;}
  h2{font-size:3.3cqw;line-height:1.1;}
  p{margin:0;font:300 1.28cqw/1.66 'Karla';color:var(--muted);}
  p b,p strong{font-weight:600;color:var(--ink);}
  .hr{height:1px;background:var(--rule);}
  .cap{font:300 .86cqw/1.4 'Karla';letter-spacing:.14em;text-transform:uppercase;color:var(--faint);}
  .presented{display:flex;align-items:center;gap:.8cqw;font:400 .9cqw/1 'Karla';
     letter-spacing:.2em;text-transform:uppercase;color:var(--faint);}
  .presented .lgo{width:11cqw;height:2cqw;} .presented .lgo svg{width:100%;height:100%;display:block;}

  /* cover */
  .cover{color:#fff;}
  .cover .wash{position:absolute;inset:0;z-index:1;background:
     radial-gradient(ellipse 52% 46% at 50% 40%,rgba(6,10,16,.70) 0%,rgba(6,10,16,0) 100%),
     linear-gradient(180deg,rgba(8,12,18,.62) 0%,rgba(8,12,18,.06) 34%,
     rgba(8,12,18,.34) 68%,rgba(8,12,18,.88) 100%);}
  .cover.left .wash{background:
     linear-gradient(90deg,rgba(6,10,16,.90) 0%,rgba(6,10,16,.62) 42%,rgba(6,10,16,.05) 82%),
     linear-gradient(180deg,rgba(8,12,18,.34) 0%,rgba(8,12,18,0) 40%,rgba(8,12,18,.86) 100%);}
  .cover .pad{align-items:center;text-align:center;padding:4.6cqw 6cqw 3.4cqw;}
  .cover .lab{color:rgba(255,255,255,.92);}
  .cover h1{font-size:6.2cqw;line-height:1.02;margin-top:2.2cqw;max-width:18ch;}
  .cover .rule{width:8cqw;height:1px;background:rgba(255,255,255,.7);margin:2cqw 0;}
  .cover .sub{font:300 1.5cqw/1.62 'Karla';max-width:46ch;color:rgba(255,255,255,.94);}
  .cover .cfoot{margin-top:auto;width:100%;display:flex;justify-content:space-between;
     align-items:flex-end;border-top:1px solid rgba(255,255,255,.34);padding-top:1.2cqw;
     font:400 .95cqw/1 'Karla';letter-spacing:.26em;text-transform:uppercase;
     color:rgba(255,255,255,.88);}
  .cover .presented{color:rgba(255,255,255,.8);}

  /* running head */
  .rh{display:flex;justify-content:space-between;align-items:baseline;
     border-bottom:1px solid var(--rule);padding-bottom:1cqw;}

  /* figures */
  .figs{display:grid;grid-template-columns:repeat(4,1fr);gap:3.4cqw;margin:auto 0;}
  .figs .f b{display:block;font:300 6cqw/.92 'Fraunces';letter-spacing:-.02em;color:var(--ink);}
  .figs .f i{display:block;width:2.6cqw;height:2px;background:var(--accent);margin:1.1cqw 0 .9cqw;}
  .figs .f span{display:block;font:300 1.16cqw/1.5 'Karla';color:var(--muted);}
  .figs .f span em{display:block;font-style:normal;font-weight:600;color:var(--ink);
     letter-spacing:.16em;text-transform:uppercase;font-size:.9cqw;margin-bottom:.3cqw;}

  /* lead image + side text */
  .lead{display:grid;grid-template-columns:1fr 1fr;gap:4.4cqw;flex:1;min-height:0;
     align-items:center;margin-top:2cqw;}
  .lead img{width:100%;aspect-ratio:4/5;max-height:37cqw;object-fit:cover;
     object-position:top center;display:block;}
  .lead > div{align-self:center;}
  .lead .side p + p{margin-top:1.1cqw;}

  /* portrait band */
  .band{display:grid;grid-template-columns:repeat(5,1fr);gap:1cqw;margin-top:auto;}
  .band img{width:100%;aspect-ratio:1;object-fit:cover;object-position:top center;display:block;}

  /* the ten */
  .pgrid{display:grid;grid-template-columns:repeat(5,12.8cqw);justify-content:space-between;
     gap:1.3cqw;margin-top:1.1cqw;}
  .pcard{margin:0;} .pcard img{width:100%;aspect-ratio:1;object-fit:cover;
     object-position:top center;display:block;}
  .pcard figcaption{margin-top:.7cqw;padding-top:.55cqw;border-top:1px solid var(--rule);}
  .pcard b{display:block;font:400 .95cqw/1.2 'Fraunces';color:var(--ink);min-height:1.15cqw;}
  .pcard span{display:block;font:600 .76cqw/1 'Karla';letter-spacing:.16em;text-transform:uppercase;
     color:var(--accent);margin-top:.28cqw;}
  .pcard em{display:block;font:300 .76cqw/1.34 'Karla';font-style:normal;color:var(--faint);
     margin-top:.3cqw;min-height:1.02cqw;}

  /* reach */
  .ptable{margin:auto 0;display:flex;flex-direction:column;gap:.72cqw;}
  .prow{display:grid;grid-template-columns:18cqw 1fr 5cqw;gap:1.2cqw;align-items:center;}
  .pn{font:300 1.2cqw/1 'Karla';color:var(--ink);white-space:nowrap;overflow:hidden;
     text-overflow:ellipsis;}
  .pn i{font-style:normal;font:600 .76cqw/1 'Karla';letter-spacing:.16em;text-transform:uppercase;
     color:var(--accent);}
  .ptrack{height:.95cqw;background:#ECE4D6;}
  .pbar{display:flex;height:100%;} .pbar i{display:block;height:100%;}
  .ig{background:var(--accent);} .tt{background:#E0A94B;} .fb{background:#7FA8B8;}
  .pt{font:400 1.3cqw/1 'Fraunces';color:var(--ink);text-align:right;
     font-variant-numeric:tabular-nums;}
  .key{display:flex;gap:1.4cqw;font:300 .92cqw/1 'Karla';letter-spacing:.14em;
     text-transform:uppercase;color:var(--faint);}
  .key span{display:flex;align-items:center;gap:.4cqw;}
  .sw{width:.8cqw;height:.8cqw;display:inline-block;}

  /* foundation */
  .foy{display:grid;grid-template-columns:20cqw 1fr;gap:4cqw;flex:1;min-height:0;
     align-items:center;margin-top:2cqw;}
  .foy .stack{display:flex;flex-direction:column;gap:1.1cqw;}
  .foy .card{background:#16223A;padding:1.8cqw;} .foy .card img{width:100%;display:block;}
  .foy .stack > img{width:100%;aspect-ratio:1;object-fit:cover;object-position:top center;display:block;}
  .foygrid{display:grid;grid-template-columns:1fr 1fr;gap:1cqw 2.4cqw;margin-top:1.8cqw;
     padding-top:1.3cqw;border-top:1px solid var(--rule);}
  .foygrid b{display:block;font:400 1.4cqw/1.1 'Fraunces';color:var(--ink);}
  .foygrid span{font:300 1cqw/1.4 'Karla';color:var(--faint);}
  .foynote{margin-top:1.6cqw;font:300 1.06cqw/1.55 'Karla';color:var(--muted);
     padding-left:1.2cqw;border-left:2px solid var(--accent);}

  /* quote over photo */
  .quote{color:#fff;}
  .quote .wash{position:absolute;inset:0;z-index:1;
     background:linear-gradient(90deg,rgba(6,14,20,.86) 0%,rgba(6,14,20,.52) 52%,rgba(6,14,20,.12) 100%);}
  .quote blockquote{margin:auto 0;font:300 3.7cqw/1.2 'Fraunces';max-width:24ch;color:#fff;}
  .quote .attr{font:400 .95cqw/1 'Karla';letter-spacing:.3em;text-transform:uppercase;
     color:rgba(255,255,255,.72);margin-bottom:1cqw;}

  /* brand cards */
  .bgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:2.2cqw 2.6cqw;margin:auto 0;}
  .bcard{padding-top:.9cqw;border-top:2px solid var(--accent);}
  .bcard b{display:block;font:400 1.62cqw/1.14 'Fraunces';color:var(--ink);}
  .bcard span{display:block;margin-top:.5cqw;font:300 1.06cqw/1.5 'Karla';color:var(--muted);}

  /* partnership */
  .two{display:grid;grid-template-columns:1fr 1fr;gap:4.4cqw;margin:auto 0;}
  .two ul{margin:0;padding:0;list-style:none;}
  .two li{font:300 1.26cqw/1.35 'Karla';color:var(--ink);padding:.72cqw 0;
     border-bottom:1px solid var(--rule);}
  .two li:first-child{border-top:1px solid var(--rule);}
  .tgt b{display:block;font:400 1.4cqw/1.1 'Fraunces';color:var(--accent);margin-top:1.1cqw;}
  .tgt b:first-child{margin-top:0;}
  .tgt span{display:block;font:300 1.04cqw/1.5 'Karla';color:var(--muted);}

  /* budget */
  .bud{width:100%;border-collapse:collapse;margin:auto 0;}
  .bud td{padding:.72cqw 0;border-bottom:1px solid var(--rule);
     font:300 1.24cqw/1 'Karla';color:var(--muted);}
  .bud td:last-child{text-align:right;font:400 1.5cqw/1 'Fraunces';color:var(--ink);
     font-variant-numeric:tabular-nums;}
  .bud tr:last-child td{border-bottom:none;border-top:2px solid var(--ink);padding-top:1cqw;
     font:400 2cqw/1 'Fraunces';color:var(--ink);}
  .bud tr:last-child td:last-child{font-size:2.4cqw;color:var(--accent);}

  /* notes */
  .notes{columns:3;column-gap:2.6cqw;margin-top:1.6cqw;}
  .notes p{font:300 .92cqw/1.5 'Karla';break-inside:avoid;margin-bottom:.8cqw;}

  /* ---------- poster register ---------- */
  .P{background:var(--black);color:#fff;}
  .P .lab{color:var(--pop);font-family:'Anton';font-weight:400;letter-spacing:.22em;
     font-size:1.24cqw;}
  .P .fol{border-top-color:#2A2A2A;color:#7A7A7A;}
  .P p{color:#B9B4AC;}
  .anton{font-family:'Anton',Impact,sans-serif;font-weight:400;text-transform:uppercase;
     letter-spacing:-.008em;line-height:.9;}
  .rails{display:flex;gap:.5cqw;} .rails i{height:.9cqw;flex:1;display:block;}

  .Phero{color:#fff;}
  .Phero .wash{position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,
     rgba(0,0,0,.30) 0%,rgba(0,0,0,.06) 30%,rgba(0,0,0,.70) 72%,rgba(0,0,0,.96) 100%);}
  .Phero .big{margin-top:auto;font-size:9.6cqw;}
  .Phero .big em{font-style:normal;color:var(--pop);}
  .Phero .chips{margin-top:1.5cqw;display:flex;gap:1cqw;flex-wrap:wrap;}
  .chip{font-family:'Anton';font-size:1.2cqw;letter-spacing:.06em;text-transform:uppercase;
     padding:.6cqw .9cqw;background:var(--pop);color:#0A0A0A;}
  .chip.g{background:var(--popg);} .chip.w{background:#fff;}

  .line{display:grid;grid-template-columns:1fr auto;gap:1.6cqw;align-items:baseline;
     border-bottom:2px solid #242424;padding:.8cqw 0;}
  .line span{font-family:'Anton';text-transform:uppercase;font-size:3.5cqw;line-height:1;}
  .line i{font-style:normal;font:600 1cqw/1 'Archivo',sans-serif;letter-spacing:.12em;
     text-transform:uppercase;color:var(--pop);white-space:nowrap;}
  .line.sm span{font-size:2.1cqw;color:#9E9E9E;}
  .line.sm i{color:#6F6F6F;}

  .sgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:3cqw;margin:auto 0;}
  .sfig b{display:block;font-family:'Anton';font-size:4.6cqw;line-height:.95;color:var(--pop);}
  .sfig span{display:block;margin-top:.9cqw;padding-top:.8cqw;border-top:2px solid #262626;
     font:300 1.1cqw/1.45 'Karla';color:#D7D2C9;}
  .sfig em{display:block;margin-top:.6cqw;font:400 .85cqw/1.35 'Karla';font-style:normal;
     letter-spacing:.1em;text-transform:uppercase;color:#6F6F6F;}

  .routewrap{display:grid;grid-template-columns:1fr 20cqw;gap:2.4cqw;flex:1;min-height:0;
     margin-top:1.2cqw;}
  .mapcol{display:flex;flex-direction:column;justify-content:center;gap:1cqw;}
  .mapbox{position:relative;} .mapbox img{width:100%;display:block;}
  .mapcap{font:300 .92cqw/1.45 'Karla';color:#7A7A7A;}
  .mp{position:absolute;display:flex;align-items:center;gap:.4cqw;white-space:nowrap;}
  .mp.r{transform:translate(-.9cqw,-50%);}
  .mp.l{transform:translate(calc(-100% + .9cqw),-50%);flex-direction:row-reverse;}
  .mp.d{transform:translate(-50%,-.9cqw);flex-direction:column;gap:.25cqw;}
  .mp.u{transform:translate(-50%,calc(-100% + .9cqw));flex-direction:column-reverse;gap:.25cqw;}
  .mp b{width:1.8cqw;height:1.8cqw;border-radius:50%;background:var(--pop);color:#0A0A0A;
     font-family:'Anton';font-size:1.06cqw;display:flex;align-items:center;justify-content:center;
     flex:none;}
  .mp span{font:600 1cqw/1 'Archivo',sans-serif;color:#fff;background:rgba(0,0,0,.72);
     padding:.16cqw .42cqw;}
  .mp.opt span{color:#9E9E9E;font-weight:400;font-style:italic;}
  .mc{position:absolute;transform:translate(-50%,-50%);font-family:'Anton';font-size:1.3cqw;
     letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.72);pointer-events:none;}
  .days{display:flex;flex-direction:column;gap:.3cqw;align-self:center;}
  .day{display:grid;grid-template-columns:3.4cqw 1fr;gap:.6cqw;align-items:baseline;
     padding-bottom:.32cqw;border-bottom:1px solid #242424;}
  .day b{font-family:'Anton';font-size:1.45cqw;color:var(--pop);}
  .day span{font:600 1cqw/1.2 'Archivo',sans-serif;color:#fff;}
  .day em{grid-column:2;font:300 .88cqw/1.3 'Karla';font-style:normal;color:#8A8580;}
"""

ROOT = f"""
  :root{{
    --paper:{PAPER}; --ink:{INK}; --muted:{MUTED}; --faint:{FAINT}; --rule:{RULE};
    --accent:{ACCENT}; --green:{GREEN}; --black:{BLACK}; --pop:{POP}; --popg:{POPG};
  }}"""

# ---------------------------------------------------------------- v10 additions
COVERBAND = "".join(
    f'<figure><img src="{por(s, 340, 340)}" alt="{n}"><figcaption>{n}</figcaption></figure>'
    for s, n, _, _ in DELEG[:5])

COUNTRIES = ["Côte d'Ivoire", "Nicaragua", "Martinique", "Brazil", "Guadeloupe",
             "Thailand", "Ecuador", "DR Congo", "Curaçao", "Belize"]
assert len(COUNTRIES) == len(DELEG)
CLIST = "".join(f"<li>{c}</li>" for c in COUNTRIES)

DETAIL = [
    ("The invitation", "Olivia Yacé invites ten current and recent titleholders to travel with her "
     "as one delegation. They cover their own flights to Abidjan. Everything on the ground is covered."),
    ("The ten days", "21 to 30 December. Lagos for the opening weekend, Abidjan as the base for six "
     "days including Fally Ipupa and the Mother Africa Festival, a coast day at Assinie and "
     "Grand-Bassam, then Accra for AfroFuture."),
    ("What is filmed", "A director, a two camera crew, a stills photographer and an editor travel "
     "with the group for the full ten days. A short edit goes out daily and the whole thing cuts "
     "as a series afterwards."),
    ("The foundation", "The delegation works alongside the Fondation Olivia Yacé, and alongside "
     "partner foundations in Ghana and Nigeria, on schooling programmes already running."),
    ("How it is funded", "There is no upfront budget. The tour is delivered on sponsorship: "
     "€185,000 covers it, and every confirmed partner brings that number down."),
    ("Who delivers it", "AToure Management and Consulting, an experience and logistics agency "
     "working out of Abidjan and registered in England and Wales."),
]
DBLOCKS = "".join(f"<div class='dblk'><b>{t}</b><span>{x}</span></div>" for t, x in DETAIL)

OFFER = "".join(
    f"""<div class="oitem"><span class="onum">{i:02d}</span>
        <div><b>{t}</b><span>{x}</span></div></div>"""
    for i, (t, x) in enumerate(BRAND, 1))

CSS += """
  /* cover band of portraits */
  .cband{margin-top:auto;display:grid;grid-template-columns:repeat(5,1fr);gap:.9cqw;
     max-width:64cqw;}
  .cband figure{margin:0;}
  .cband img{width:100%;aspect-ratio:1;object-fit:cover;object-position:top center;display:block;}
  .cband figcaption{margin-top:.45cqw;font:400 .72cqw/1.25 'Karla';letter-spacing:.1em;
     text-transform:uppercase;color:rgba(255,255,255,.82);min-height:1.8cqw;}
  .cover.left .pad{align-items:flex-start;text-align:left;}
  .cover.left h1{max-width:14ch;}

  /* the project, five figures */
  .figs5{display:grid;grid-template-columns:repeat(5,1fr);gap:2.6cqw;margin:auto 0;}
  .figs5 .f b{display:block;font:300 5.4cqw/.95 'Fraunces';letter-spacing:-.02em;color:var(--ink);}
  .figs5 .f i{display:block;width:2.2cqw;height:2px;background:var(--accent);margin:1cqw 0 .8cqw;}
  .figs5 .f em{display:block;font:600 .84cqw/1 'Karla';font-style:normal;letter-spacing:.18em;
     text-transform:uppercase;color:var(--ink);}
  .figs5 .f span{display:block;margin-top:.35cqw;font:300 1.02cqw/1.45 'Karla';color:var(--muted);}

  /* detail page */
  .dgrid{display:grid;grid-template-columns:1fr 1fr;gap:1.6cqw 3cqw;margin-top:1.8cqw;}
  .dblk{padding-top:.8cqw;border-top:1px solid var(--rule);}
  .dblk b{display:block;font:400 1.34cqw/1.15 'Fraunces';color:var(--ink);}
  .dblk span{display:block;margin-top:.4cqw;font:300 1cqw/1.5 'Karla';color:var(--muted);}

  /* reach: total and the countries */
  .tot{display:grid;grid-template-columns:auto 1fr;gap:3.4cqw;align-items:center;
     padding-bottom:1.4cqw;border-bottom:1px solid var(--rule);margin-top:1.6cqw;}
  .tot .big{font:300 5.4cqw/.92 'Fraunces';letter-spacing:-.025em;color:var(--ink);}
  .tot .big em{display:block;font:600 .84cqw/1 'Karla';font-style:normal;letter-spacing:.2em;
     text-transform:uppercase;color:var(--accent);margin-top:.7cqw;}
  .tot ul{margin:0;padding:0;list-style:none;display:grid;
     grid-template-columns:repeat(5,1fr);gap:.55cqw 1.4cqw;}
  .tot li{font:400 .98cqw/1.3 'Karla';letter-spacing:.14em;text-transform:uppercase;
     color:var(--ink);padding-bottom:.35cqw;border-bottom:1px solid var(--rule);}

  /* the offer */
  .ogrid{display:grid;grid-template-columns:repeat(3,1fr);gap:2.2cqw 3cqw;margin:auto 0;}
  .oitem{display:grid;grid-template-columns:3.6cqw 1fr;gap:1cqw;padding-top:.85cqw;
     border-top:1px solid var(--rule);}
  .onum{font:300 2.6cqw/.9 'Fraunces';color:var(--accent);}
  .oitem b{display:block;font:400 1.46cqw/1.14 'Fraunces';color:var(--ink);}
  .oitem span{display:block;margin-top:.45cqw;font:300 1.02cqw/1.48 'Karla';color:var(--muted);}
  .obar{background:var(--ink);color:#F2EDE4;padding:1.3cqw 1.8cqw;display:flex;
     justify-content:space-between;align-items:center;gap:3cqw;}
  .obar b{font:400 1.24cqw/1.3 'Fraunces';color:#fff;}
  .obar span{font:300 1cqw/1.45 'Karla';color:#C8C0B2;max-width:58ch;}
"""

# ---------------------------------------------------------------- v11: ten pages
COLOPHON = [
    ("Titles", "Verified against national and international press, September 2026. Seven of the ten "
     "competed at Miss Universe 2025. Olivia Yacé placed fourth runner-up there and is an official "
     "tourism ambassador for Côte d'Ivoire; Ophély Mézino reached the Top 12."),
    ("Audience", "Instagram, TikTok and Facebook summed from the client tracking sheet, not "
     "deduplicated. Countries listed are those the participants competed for."),
    ("Status", "Ten invited, three reserves. No participation agreement is signed and no partner is "
     "contracted at the date of this document. Every organisation named is a target. Several "
     "Abidjan dates remain unconfirmed and are not listed; route stops are proposed, not booked."),
    ("Sources", "Lagos State Government, January 2025. Ghana Tourism Authority 2024 Tourism Report. "
     "Ministère du Tourisme, Côte d'Ivoire. Map from Natural Earth 1:50m geometry. Budget researched "
     "September 2026 against published prices, no quotes received."),
    ("Photography", "Portraits supplied by the participants. Location and festival images credited "
     "to Afronation.com, Afrique Magazine and the Mother Africa Festival, used here for layout. "
     "Written permission is required before this deck is circulated."),
]
COLO = "".join(f"<p><b>{t}.</b> {x}</p>" for t, x in COLOPHON)

NEXT = [("Now", "Category conversations open. One partner per category, three markets."),
        ("31 October", "Partners confirmed by this date travel with the delegation."),
        ("21 December", "The delegation lands in Lagos.")]
NEXTS = "".join(f"<div class='nx'><b>{a}</b><span>{b}</span></div>" for a, b in NEXT)

CSS += """
  /* page two: detail blocks in three columns under the figures */
  .dgrid3{display:grid;grid-template-columns:repeat(3,1fr);gap:1.3cqw 3cqw;margin-top:1.4cqw;}

  /* the season, one poster page */
  .seasonband{position:relative;height:16cqw;overflow:hidden;margin-top:1.1cqw;}
  .seasonband img{width:100%;height:100%;object-fit:cover;object-position:center 26%;display:block;}
  .seasonband .ov{position:absolute;inset:0;display:flex;align-items:flex-end;padding:1.4cqw 1.8cqw;
     background:linear-gradient(180deg,rgba(0,0,0,.28) 0%,rgba(0,0,0,.10) 44%,rgba(0,0,0,.86) 100%);}
  .seasonband .ov b{font-family:'Anton';font-size:4.6cqw;line-height:.9;text-transform:uppercase;
     color:#fff;}
  .seasonband .ov b em{font-style:normal;color:var(--pop);}
  .seasonband .rails{position:absolute;top:0;left:0;right:0;}
  .seasoncols{display:grid;grid-template-columns:1.35fr 1fr;gap:2.6cqw;flex:1;min-height:0;
     margin-top:1.4cqw;}
  .seasoncols .stats{display:grid;grid-template-columns:1fr 1fr;gap:1.2cqw 1.8cqw;
     align-content:center;border-left:2px solid #242424;padding-left:1.8cqw;}
  .seasoncols .sfig b{font-size:2.5cqw;}
  .seasoncols .sfig span{margin-top:.35cqw;padding-top:.35cqw;border-top:none;font-size:.88cqw;
     line-height:1.35;}
  .seasoncols .sfig em{margin-top:.2cqw;font-size:.72cqw;}
  .seasoncols .line{padding:.45cqw 0;}
  .seasoncols .line span{font-size:2.2cqw;} .seasoncols .line.sm span{font-size:1.5cqw;}
  .seasoncols .line i{font-size:.84cqw;}

  /* filmed, two frames */
  .twoshot{display:grid;grid-template-columns:1fr 1fr;gap:1.4cqw;}
  .twoshot img{width:100%;aspect-ratio:3/2;object-fit:cover;object-position:center;display:block;}

  /* the offer, with the categories folded in */
  .cats{display:grid;grid-template-columns:repeat(3,1fr);gap:2.6cqw;padding-top:1cqw;
     border-top:1px solid var(--rule);margin-top:1.4cqw;}
  .cats b{display:block;font:600 .82cqw/1 'Karla';letter-spacing:.2em;text-transform:uppercase;
     color:var(--accent);}
  .cats span{display:block;margin-top:.4cqw;font:300 1cqw/1.45 'Karla';color:var(--muted);}

  /* the last page */
  .nx{padding-top:.75cqw;border-top:2px solid var(--accent);margin-bottom:1.1cqw;}
  .nx b{display:block;font:400 1.34cqw/1.1 'Fraunces';color:var(--ink);}
  .nx span{display:block;margin-top:.25cqw;font:300 1cqw/1.45 'Karla';color:var(--muted);}
  .colophon{columns:3;column-gap:2.6cqw;margin-top:1.4cqw;padding-top:1.1cqw;
     border-top:1px solid var(--rule);}
  .colophon p{font:300 .78cqw/1.45 'Karla';color:var(--faint);break-inside:avoid;margin-bottom:.6cqw;}
  .colophon p b{color:var(--muted);font-weight:600;}
"""

REG = list("EEEEE" "PP" "EEE")
fol = lambda n, t: f'<div class="fol"><span>{t}</span><span>{n:02d}</span></div>'
S = []

# 01 cover
S.append(f"""
  <section class="s cover left">
    <div class="bleed"><img src="{loc('skyline', 1400, 788, .5, .45)}" alt="Abidjan"></div>
    <div class="wash"></div>
    <div class="pad">
      <div class="lab">Olivia Yacé International &nbsp;·&nbsp; Fondation Olivia Yacé</div>
      <h1 style="font-size:5.4cqw;">Beauty Beyond Borders</h1>
      <div class="rule"></div>
      <div class="sub" style="max-width:40ch;">Ten international titleholders travel Côte d'Ivoire,
        Ghana and Nigeria together for ten days, through the busiest month in the region's calendar.</div>
      <div class="cband">{COVERBAND}</div>
      <div class="cfoot">
        <span>Abidjan &nbsp;·&nbsp; Assinie &nbsp;·&nbsp; Accra &nbsp;·&nbsp; Lagos</span>
        <span>21 to 30 December 2026</span>
        <span class="presented"><span>presented by</span><span class="lgo">{logo_dark}</span></span>
      </div>
    </div>
  </section>""")

# 02 the project: the numbers and the detail on one page
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:5.2cqw;">
      <div class="rh"><div class="lab">The project</div><div class="lab">In five numbers</div></div>
      <h2 style="margin-top:1.3cqw;font-size:2.7cqw;max-width:56ch;">Ten titleholders travel West
        Africa together for ten days in December, and a production team films all of it.</h2>
      <div class="figs5" style="margin:2cqw 0 0;">
        <div class="f"><b>10</b><i></i><em>Titleholders</em>
          <span>Miss Universe, Miss World, Miss France and Miss Grand International</span></div>
        <div class="f"><b>10</b><i></i><em>Days</em>
          <span>21 to 30 December 2026, six of them Ivorian</span></div>
        <div class="f"><b>3</b><i></i><em>Countries</em>
          <span>Côte d'Ivoire, Ghana and Nigeria</span></div>
        <div class="f"><b>{TOTM}</b><i></i><em>Followers</em>
          <span>combined, across the delegation's own channels</span></div>
        <div class="f"><b>1</b><i></i><em>Season</em>
          <span>the month West Africa's diaspora comes home</span></div>
      </div>
      <div class="dgrid3">{DBLOCKS}</div>
    </div>
    {fol(2, 'Beauty Beyond Borders')}
  </section>""")

# 03 the delegation
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:6.2cqw;">
      <div class="rh"><div class="lab">The delegation</div><div class="lab">Ten invitations</div></div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:4cqw;align-items:baseline;margin-top:1.2cqw;">
        <h2 style="font-size:2.6cqw;">The women.</h2>
        <p style="max-width:78ch;">Ten countries of origin, one December. Seven of the ten
          competed at Miss Universe 2025 in Bangkok.</p>
      </div>
      <div class="pgrid">{CARDS}</div>
    </div>
    {fol(3, 'Beauty Beyond Borders')}
  </section>""")

# 04 who is watching
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:5.4cqw;">
      <div class="rh"><div class="lab">Who is watching</div>
        <div class="key"><span><i class="sw ig"></i>Instagram</span><span><i class="sw tt"></i>TikTok</span><span><i class="sw fb"></i>Facebook</span></div></div>
      <div class="tot">
        <div class="big">{TOTM}<em>Combined following</em></div>
        <div>
          <div class="cap" style="margin-bottom:.8cqw;">Ten countries represented</div>
          <ul>{CLIST}</ul>
        </div>
      </div>
      <div class="ptable">{ROWS}</div>
      <div class="cap">Summed across three platforms, not deduplicated. Host first, then by total.</div>
    </div>
    {fol(4, 'Beauty Beyond Borders')}
  </section>""")

# 05 social impact
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:5.4cqw;">
      <div class="rh"><div class="lab">Social impact</div><div class="lab">Fondation Olivia Yacé</div></div>
      <div class="foy">
        <div class="stack">
          <div class="card"><img src="{FOY}" alt="Fondation Olivia Yacé"></div>
          <img src="{por('olivia-yace', 460, 460)}" alt="Olivia Yacé">
        </div>
        <div>
          <h2 style="max-width:22ch;">The tour has a foundation behind it.</h2>
          <p style="margin-top:1.4cqw;max-width:50ch;">Founded in 2025 and anchored in Côte d'Ivoire,
            the Fondation Olivia Yacé puts vulnerable children, and girls in particular, into school
            and keeps them there. The delegation works alongside it, and alongside partner
            foundations in Ghana and Nigeria, during the ten days.</p>
          <div class="foygrid">
            <div><b>School fees</b><span>paid directly</span></div>
            <div><b>Teaching kits</b><span>schools and orphanages</span></div>
            <div><b>School meals</b><span>nutrition programmes</span></div>
            <div><b>Tutoring</b><span>and mentoring</span></div>
          </div>
          <div class="foynote"><b>September 2026.</b> More than six million CFA francs raised for the
            École Hermann Gmeiner at the SOS Children's Village in Abobo, for the 2026 to 2027 school year.</div>
        </div>
      </div>
    </div>
    {fol(5, 'Beauty Beyond Borders')}
  </section>""")

# 06 the season: hero, lineup and the December numbers on one poster page
S.append(f"""
  <section class="s P">
    <div class="pad" style="padding:3.4cqw 5.2cqw 5.4cqw;">
      <div class="rh" style="border-bottom-color:#242424;">
        <div class="lab">The season</div><div class="lab" style="color:#6F6F6F">Already booked, already measured</div></div>
      <div class="seasonband">
        <img src="{loc('crowd', 1200, 420, .5, .30)}" alt="">
        <div class="rails"><i style="background:var(--pop)"></i><i style="background:#fff"></i>
          <i style="background:var(--popg)"></i><i style="background:var(--pop)"></i></div>
        <div class="ov"><b>The<br><em>season</em></b></div>
      </div>
      <div class="seasoncols">
        <div style="display:flex;flex-direction:column;justify-content:center;">{BILL}</div>
        <div class="stats">{SEAS}</div>
      </div>
      <div class="cap" style="color:#6F6F6F;margin-top:1cqw;">Published dates, September 2026.
        Several Abidjan dates remain unconfirmed and are not listed. Vodun Days, Ouidah,
        2 to 9 January 2027, sits outside the ten days and is costed separately.</div>
    </div>
    {fol(6, 'The season')}
  </section>""")

# 07 the route
S.append(f"""
  <section class="s P">
    <div class="pad" style="padding-bottom:5.4cqw;">
      <div class="rh" style="border-bottom-color:#242424;">
        <div class="lab">The route</div><div class="lab" style="color:#6F6F6F">Ten days, one coast</div></div>
      <div class="routewrap">
        <div class="mapcol">
          <div class="mapbox"><img src="{MAP}" alt="Route map">{MAPCTY}{MAPLBL}</div>
          <div class="mapcap">Stops are proposed, not booked. Ouidah is hollow: Vodun Days runs
            2 to 9 January 2027, outside the ten days.</div>
        </div>
        <div class="days">{DAYS}</div>
      </div>
    </div>
    {fol(7, 'The season')}
  </section>""")

# 08 filmed
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:5.4cqw;">
      <div class="rh"><div class="lab">Filmed</div><div class="lab">Production and rights</div></div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:4cqw;align-items:baseline;margin-top:1.2cqw;">
        <h2 style="font-size:2.6cqw;max-width:20ch;">Shot by a production team, as a series.</h2>
        <p style="max-width:62ch;">A director, a two camera crew, a stills photographer and an editor
          travel with the delegation for the full ten days. A short edit goes out every day and the
          whole thing cuts as a series afterwards. Broadcast rights are a second revenue line, and
          every partner keeps a rights cleared archive that outlives the ten days.</p>
      </div>
      <div class="twoshot" style="margin-top:auto;">
        <img src="{loc('stage', 900, 600, .5, .3)}" alt="">
        <img src="{loc('assinie', 900, 600, .5, .5)}" alt="">
      </div>
      <div class="cap" style="margin-top:.8cqw;">Mother Africa Festival, Abidjan &nbsp;·&nbsp;
        the coast at Assinie</div>
    </div>
    {fol(8, 'Beauty Beyond Borders')}
  </section>""")

# 09 the offer
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:5.2cqw;">
      <div class="rh"><div class="lab">The offer</div><div class="lab">Six ways in</div></div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:4cqw;align-items:baseline;margin-top:1.2cqw;">
        <h2 style="font-size:2.6cqw;">The delegation is the media.</h2>
        <p style="max-width:66ch;">Not a logo on a banner. Six things a partner can hold, alone in
          its category, across three markets.</p>
      </div>
      <div class="ogrid" style="margin:1.6cqw 0 0;">{OFFER}</div>
      <div class="cats">
        <div><b>Governments</b><span>Sublime Côte d'Ivoire. Ghana Ministry of Tourism. Lagos State Tourism.</span></div>
        <div><b>Travel</b><span>Air Côte d'Ivoire. Accor. Kempinski. Eko Hotels.</span></div>
        <div><b>Consumer</b><span>Telecoms, banking, beauty, jewellery and watches, approached
          through the participants who have worked with them before.</span></div>
      </div>
      <div class="obar" style="margin-top:1.3cqw;">
        <b>Possibilities, not packages.</b>
        <span>What a partner actually receives is set by scope and by budget, and is written into
          the agreement before anything is announced.</span>
      </div>
    </div>
    {fol(9, 'The offer')}
  </section>""")

# 10 the number and next
S.append(f"""
  <section class="s">
    <div class="pad" style="padding-bottom:4.4cqw;">
      <div class="rh"><div class="lab">The number and what happens next</div>
        <div class="lab">Ten days, twenty people</div></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:4.4cqw;margin-top:1.4cqw;">
        <table class="bud" style="margin:0;">{BUD}<tr><td>Total</td><td>€185,000</td></tr></table>
        <div>
          <h2 style="font-size:2.5cqw;">€185,000 delivers it.</h2>
          <p style="margin-top:1cqw;margin-bottom:1.5cqw;">Ten days, three countries, twenty people
            on the ground. There is no upfront budget: every confirmed partner brings this number down.</p>
          {NEXTS}
          <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:2cqw;
               padding-top:1cqw;border-top:1px solid var(--rule);">
            <span style="font:300 1.06cqw/1.5 'Karla';color:var(--muted);">
              <b style="font-family:'Fraunces';font-weight:400;font-size:1.3cqw;color:var(--ink);">Baba Touré</b><br>
              AToure Management &amp; Consulting<br>atoureconsulting@gmail.com</span>
            <span class="presented"><span>presented by</span><span class="lgo">{logo_light}</span></span>
          </div>
        </div>
      </div>
      <div class="colophon">{COLO}</div>
    </div>
    {fol(10, 'The offer')}
  </section>""")

assert len(S) == len(REG) == 10, (len(S), len(REG))
for i, (sec, r) in enumerate(zip(S, REG), 1):
    if r == "P":
        assert 'class="s P' in sec, "page %d should be poster" % i
    else:
        assert 'class="s P' not in sec, "page %d should be editorial" % i

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;1,9..144,300'
         '&family=Karla:wght@200;300;400;500;600&family=Anton&family=Archivo:wght@400;600'
         '&display=swap">')
HTML = ('<!doctype html><meta charset="utf-8"><title>Beauty Beyond Borders</title>\n' + FONTS +
        "\n<style>" + ROOT + CSS + "</style>\n" + '<div class="deck">' + "".join(S) + "</div>\n")

out = SC + "/bbb-deck-v11.html"
open(out, "w").write(HTML)
body = HTML.split("</style>")[-1]
assert "—" not in body, "em-dash in copy"
assert body.count("<section") == 10
assert "€250,000" not in body and "seventeen" not in body.lower()
for must in ("185,000", "Fondation Olivia Yacé", "71.6m", "Written permission is required"):
    assert must in body, must
print("written", round(os.path.getsize(out) / 1e6, 2), "MB /", len(S), "pages /", "".join(REG))
