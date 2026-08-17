#!/usr/bin/env python3
"""Build site/index.html.

Roster photos are read from deck/photos/ (the same folder the PowerPoint
uses), centre-cropped, masked to a circle and inlined as data URIs — the
published page blocks external image requests, so everything must be
embedded. Women with no photo yet fall back to a gold monogram.

    python site/build_site.py
"""
import base64, io, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from roster import ROSTER  # noqa: E402

PHOTOS = os.path.join(ROOT, "deck", "photos")
OUT = os.path.join(HERE, "index.html")
PX = 420
EXTS = (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP")

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None


def find_photo(slug, idx):
    for stem in (slug, str(idx), "%02d" % idx):
        for e in EXTS:
            p = os.path.join(PHOTOS, stem + e)
            if os.path.exists(p):
                return p
    return None


def circle_data_uri(path):
    """Centre-crop square (biased up for faces), mask to a circle, return a data URI."""
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    s = min(w, h)
    im = im.crop((
        (w - s) // 2, max(0, int((h - s) * 0.35)),
        (w - s) // 2 + s, max(0, int((h - s) * 0.35)) + s,
    )).resize((PX, PX), Image.LANCZOS)
    mask = Image.new("L", (PX * 4, PX * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, PX * 4, PX * 4), fill=255)
    im.putalpha(mask.resize((PX, PX), Image.LANCZOS))
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode(), len(buf.getvalue())


def initials(name):
    bits = [b for b in name.replace("“", "").replace("”", "").split() if b[:1].isalpha()]
    if not bits:
        return "?"
    return (bits[0][0] + (bits[-1][0] if len(bits) > 1 else "")).upper()


E = html.escape


def social_html(socials):
    out = []
    for plat, handle, url, reach in socials:
        inner = '<span class="p">%s</span> <span class="h">%s</span>' % (E(plat), E(handle))
        inner += ' <b>%s</b>' % E(reach) if reach else ' <i>—</i>'
        if url:
            out.append('<a class="soc" href="%s" target="_blank" rel="noopener">%s</a>' % (E(url), inner))
        else:
            out.append('<span class="soc nolink">%s</span>' % inner)
    return "".join(out)


def card_html(p, idx):
    photo = find_photo(p["slug"], idx) if Image else None
    if photo:
        uri, nbytes = circle_data_uri(photo)
        disc = '<img class="disc" src="%s" alt="%s" width="72" height="72">' % (uri, E(p["name"]))
        got = nbytes
    else:
        disc = '<div class="disc mono" aria-hidden="true">%s</div>' % E(initials(p["name"]))
        got = 0
    tags = '<span class="tag pend">Pending</span>'
    if p["kind"] == "title":
        tags += '<span class="tag title">Titleholder</span>'
    for f in p["flags"]:
        tags += '<span class="tag flag">%s</span>' % E(f)
    kinds = p["kind"] + (" flag" if p["flags"] else "")
    return got, """
      <article class="who" data-k="%s">
        <div class="who-top">%s
          <div><h3>%s</h3><span class="nat">%s</span></div></div>
        <p class="role"><b>%s.</b> %s</p>
        <div class="socials">%s</div>
        <p class="acc">%s</p>
        <div class="tags">%s</div>
      </article>""" % (kinds, disc, E(p["name"]), E(p["nat"]),
                       E(p["title"]), E(p["role"]), social_html(p["socials"]),
                       E(p["also"]), tags)


# ---------------------------------------------------------------- legs
LEGS = [
    dict(c="ci", name="Côte d'Ivoire", when="26 – 31 December", st="Anchor confirmed", stc="ok",
         intro="Where the tour opens, and the leg with the most already in place.",
         cols=[
             ("Events", [
                 ("Mother Africa Festival", "27–28 Dec, Marcory Zone 4. Fourth edition, ~40,000 attendees. Founded by Kimany Tayoro."),
                 ("New Year's Eve fireworks", "31 Dec, Général de Gaulle bridge over the Ebrié Lagoon. Free, city-wide."),
                 ("Sofitel Réveillon gala", "Congress Palace. Past editions featured Magic System live."),
                 ("Nahiko, Assinie", "Lagoon-side NYE dinner — the intimate alternative."),
             ]),
             ("Sponsor targets", [
                 ("Orange Côte d'Ivoire", "Runs a formal sponsorship programme as policy."),
                 ("Air Côte d'Ivoire", "AFCON 2023 official carrier; backed the Children of Africa gala."),
                 ("Solibra", "Ivorian since 1955, FEMUA sponsor, marking its 70th year."),
                 ("Brassivoire", "Heineken and CFAO joint venture, runs its own Abidjan events."),
             ]),
             ("Partners &amp; logistics", [
                 ("Ivory Jet Services", "New Abidjan base, European AOC, Falcon and Legacy aircraft."),
                 ("La Sunday", "Abidjan's signature day-party brand, 6,000+ on the lagoon."),
                 ("Sofitel · Radisson Blu · Hôtel Président", "Assinie boutique: Nahiko, Maison d'Akoula, Key 19."),
                 ("Monbolide · WINO · Auto Ivoire", "Chauffeur fleets, ~55–120k FCFA per day."),
             ]),
         ],
         impact="No local foundation partner identified yet — this is the one country where the "
                "social-impact day still needs a partner sourced.",
         watch="Grand-Bassam's beaches were closed on 30 December last year after an oil spill, "
               "reopening under restrictions from 1 January. Check live status before committing a Bassam day."),
    dict(c="gh", name="Ghana", when="Early January", st="Cities open", stc="stop",
         intro="The one leg with nothing fixed — and a government programme that offers a way in.",
         cols=[
             ("Events", [
                 ("“December in GH”", "Government programme, 1 Dec – 3 Jan, run by the Ghana Tourism Authority with an open call for partners."),
                 ("AfroFuture Fest", "~27–29 Dec, El Wak Stadium, ~31,000 attendees."),
                 ("Detty Rave", "Mr Eazi's event — the biggest celebrity draw on the calendar."),
                 ("Polo Beach Club NYE", "Labadi. Tiers from ₵500 to ₵70,000 — a useful VIP benchmark."),
             ]),
             ("Sponsor targets", [
                 ("Ghana Tourism Authority", "Runs the season and takes partner proposals; also the route to Miss Diaspora Ghana."),
                 ("MTN Ghana", "Concert sponsorship history plus a foundation — sponsor and impact partner in one."),
                 ("AirtelTigo", "First operator to launch eSIM in Ghana."),
                 ("Guinness Ghana · Kasapreko", "Dominant beverage players, no confirmed tie-in yet."),
             ]),
             ("Partners &amp; logistics", [
                 ("Culture Management Group", "The most internationally professionalised producer in the market."),
                 ("McDan Aviation", "Ghana's dominant private-jet terminal at Kotoka."),
                 ("Kempinski · Labadi Beach · Mövenpick", "The standard luxury shortlist for Accra groups."),
                 ("Cape Coast &amp; Elmina", "Heritage day-trip — castles and Kakum. Daytime only, no nightlife infrastructure."),
             ]),
         ],
         impact="SOS Children's Villages Ghana — eleven locations since 1974, the most credible partner "
                "found. MTN Ghana Foundation could serve as sponsor and impact partner in one relationship.",
         watch="No 2026 dates are published yet — festival line-ups typically drop in September and "
               "October, so everything here follows last season's pattern."),
    dict(c="ng", name="Nigeria", when="New Year – 10 January", st="Draft", stc="wait",
         intro="The closing leg, the densest calendar, and the only market with confirmed active sponsors.",
         cols=[
             ("Events", [
                 ("Flytime Fest", "21–25 Dec, Eko Convention Centre. Twenty-one years running."),
                 ("Livespot Detty December Fest", "Co-produced with the Federal Ministry of Arts and Culture."),
                 ("Abuja Groovy December", "Moshood Abiola Stadium. Includes a “Miss Groovy December” pageant."),
                 ("Transcorp Hilton Abuja", "Runs its own NYE gala and New Year's Day show."),
             ]),
             ("Sponsor targets", [
                 ("Wema Bank (ALAT)", "Confirmed headline Detty December sponsor last season."),
                 ("Martell · Guinness · Hennessy", "All three ran confirmed premium activations."),
                 ("MTN · Airtel · Glo", "Heavy festive-data marketing; strong pitch targets."),
                 ("Eko Hotels &amp; Suites", "Runs its own December festival property."),
             ]),
             ("Partners &amp; logistics", [
                 ("Livespot360", "The dominant producer, government-endorsed. Prior Cardi B booking."),
                 ("ExecuJet Africa", "Major FBO at Murtala Muhammed, hangar rated to BBJ size."),
                 ("Zeniks · Abuja Car Rental Express", "Motorcade and escort options; armoured vehicles in Abuja."),
                 ("Bristow Helicopters", "Fixed-wing and helicopter shuttle for Lagos–Abuja hops."),
             ]),
         ],
         impact="Wellbeing Foundation Africa — maternal and child health, founded by Toyin Ojora Saraki, "
                "which pairs naturally with the birthday celebration. Slum2School Africa is the "
                "education-focused alternative in Lagos.",
         watch="Lagos State's own free New Year's flagship was cancelled hours before kickoff last year "
               "with no reason given, after running annually since 2012. Do not anchor the NYE plan on it."),
]


def legs_html():
    out = []
    for lg in LEGS:
        cols = ""
        for h4, items in lg["cols"]:
            its = "".join(
                '<div class="it"><strong>%s</strong><span>%s</span></div>' % (n, d)
                for n, d in items)
            cols += '<div class="lc"><h4>%s</h4>%s</div>' % (h4, its)
        out.append("""
      <div class="leg" data-c="%s">
        <div class="leg-head">
          <h3>%s</h3><span class="when">%s</span>
          <span class="st" style="color:var(--%s);">%s</span>
        </div>
        <p class="leg-intro">%s</p>
        <div class="leg-body">%s</div>
        <div class="impact"><b>Social impact</b>%s</div>
        <div class="watch"><b>Watch</b>%s</div>
      </div>""" % (lg["c"], lg["name"], lg["when"], lg["stc"], lg["st"],
                   lg["intro"], cols, lg["impact"], lg["watch"]))
    return "".join(out)


def bill_html():
    parts = []
    for p in ROSTER:
        cls = ' class="q"' if p["slug"] == "tai" else ""
        parts.append("<span%s>%s</span>" % (cls, E(p["name"])))
    return "\n        <i>·</i>\n        ".join(parts)


def main():
    if Image is None:
        print("Pillow not installed — photos will be skipped. pip install Pillow")
    cards, total, withpic = "", 0, 0
    for i, p in enumerate(ROSTER, 1):
        n, h = card_html(p, i)
        cards += h
        total += n
        withpic += 1 if n else 0

    page = TEMPLATE.replace("{{BILL}}", bill_html()) \
                   .replace("{{CARDS}}", cards) \
                   .replace("{{LEGS}}", legs_html()) \
                   .replace("{{NPHOTO}}", str(withpic))
    with open(OUT, "w") as f:
        f.write(page)

    size = os.path.getsize(OUT)
    print("wrote %s — %.2f MB" % (OUT, size / 1e6))
    print("photos embedded: %d of %d (%.2f MB of image data)" % (withpic, len(ROSTER), total / 1e6))
    if withpic < len(ROSTER):
        missing = [p["slug"] for i, p in enumerate(ROSTER, 1) if not find_photo(p["slug"], i)]
        print("missing:", ", ".join(missing))
    if size > 15_000_000:
        print("WARNING: approaching the 16 MB publish limit — lower PX in this script.")


TEMPLATE = r"""<title>Detty December</title>
<style>
  :root{
    --night:#150B13; --night-2:#1F1019; --raise:#271520;
    --line:#3C2431; --line-2:#4E2F3E;
    --gold:#D9A940; --gold-dim:#8E6C29;
    --ivory:#F3E9EE; --soft:#B29AA7; --faint:#8A7280;
    --ci:#E08A58; --gh:#D96A66; --ng:#77BE8D;
    --ok:#77BE8D; --wait:#E0B856; --stop:#E2807E;
    --display:"Didot","Bodoni MT","Hoefler Text","Playfair Display",Georgia,serif;
    --sans:"Helvetica Neue",Helvetica,Arial,system-ui,sans-serif;
    --mono:ui-monospace,"SF Mono","Cascadia Code",Menlo,Consolas,monospace;
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  body{margin:0;background:var(--night);color:var(--ivory);
    font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased;}
  @media (prefers-reduced-motion:reduce){html{scroll-behavior:auto;}}
  .wrap{max-width:1080px;margin:0 auto;padding:0 28px;}
  h1,h2,h3,h4{font-family:var(--display);font-weight:400;margin:0;text-wrap:balance;}
  a{color:inherit;}
  .eyebrow{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--gold);}

  nav{position:sticky;top:0;z-index:20;background:rgba(21,11,19,.94);
    backdrop-filter:blur(10px);border-bottom:1px solid var(--line);}
  nav .wrap{display:flex;align-items:center;gap:20px;height:52px;overflow-x:auto;}
  nav .mark{font-family:var(--display);font-size:16px;white-space:nowrap;}
  nav .mark b{color:var(--gold);font-weight:400;}
  nav a{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
    text-decoration:none;color:var(--soft);white-space:nowrap;padding:4px 0;
    border-bottom:1px solid transparent;}
  nav a:hover,nav a:focus-visible{color:var(--gold);border-bottom-color:var(--gold);outline:none;}
  nav .sp{margin-left:auto;}

  header.hero{position:relative;padding:84px 0 60px;overflow:hidden;
    border-bottom:1px solid var(--line);}
  .rings{position:absolute;inset:0;pointer-events:none;opacity:.5;}
  .rings i{position:absolute;border:1px solid var(--gold-dim);border-radius:50%;display:block;}
  .hero h1{font-size:clamp(52px,10.5vw,124px);line-height:.9;letter-spacing:-.015em;margin-top:16px;}
  .hero h1 em{font-style:italic;color:var(--gold);}
  .hero .lede{margin-top:26px;max-width:44ch;font-size:16.5px;color:var(--soft);}
  .hero .meta{margin-top:30px;display:flex;flex-wrap:wrap;gap:10px 26px;
    font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;}
  .hero .meta span{color:var(--faint);}
  .hero .meta b{color:var(--ivory);font-weight:400;}
  .bill{margin-top:50px;padding-top:26px;border-top:1px solid var(--line);
    font-family:var(--display);font-size:clamp(17px,2.5vw,27px);line-height:1.45;}
  .bill span{white-space:nowrap;}
  .bill i{color:var(--gold-dim);font-style:normal;padding:0 .3em;}
  .bill .q{color:var(--faint);font-style:italic;}

  section{padding:74px 0;border-bottom:1px solid var(--line);}
  .sec-head{margin-bottom:36px;}
  .sec-head h2{font-size:clamp(28px,4.2vw,42px);margin-top:10px;line-height:1.08;}
  .sec-head p{color:var(--soft);max-width:62ch;margin:14px 0 0;font-size:15px;}

  /* what this is */
  .thesis{font-family:var(--display);font-size:clamp(21px,2.9vw,31px);line-height:1.38;
    max-width:24ch;margin:0 0 34px;}
  .thesis em{font-style:italic;color:var(--gold);}
  .prose{columns:2;column-gap:44px;font-size:15px;color:var(--soft);max-width:none;}
  .prose p{margin:0 0 15px;break-inside:avoid;}
  .prose b{color:var(--ivory);font-weight:600;}

  .pillars{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:44px;}
  .pillar{background:var(--night-2);border:1px solid var(--line);border-radius:3px;padding:28px 26px;}
  .pillar .n{font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--gold);}
  .pillar h3{font-size:25px;margin:12px 0 12px;}
  .pillar p{font-size:14.5px;color:var(--soft);margin:0 0 14px;}
  .pillar ul{margin:0;padding-left:17px;font-size:13.5px;color:var(--faint);}
  .pillar li{margin-bottom:7px;}
  .pillar li::marker{color:var(--gold-dim);}

  .countries{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:44px;}
  .country{border-top:1px solid var(--line-2);padding-top:18px;}
  .country h4{font-size:21px;}
  .country .w{font-family:var(--mono);font-size:10px;letter-spacing:.13em;
    text-transform:uppercase;color:var(--faint);margin-top:6px;display:block;}
  .country p{font-size:13.5px;color:var(--soft);margin:12px 0 0;}
  .countries [data-c="ci"] h4{color:var(--ci);}
  .countries [data-c="gh"] h4{color:var(--gh);}
  .countries [data-c="ng"] h4{color:var(--ng);}

  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1px;
    background:var(--line);border:1px solid var(--line);border-radius:3px;overflow:hidden;}
  .stat{background:var(--night-2);padding:24px 22px;}
  .stat .n{font-family:var(--display);font-size:40px;color:var(--gold);line-height:1;
    font-variant-numeric:tabular-nums;}
  .stat .l{font-family:var(--mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
    margin-top:12px;color:var(--ivory);}
  .stat .s{font-size:12.5px;color:var(--faint);margin-top:5px;font-style:italic;}

  .note{margin-top:26px;padding:16px 20px;border:1px solid var(--line-2);border-radius:3px;
    background:var(--night-2);font-size:14px;color:var(--soft);}
  .note b{color:var(--ivory);font-weight:600;}

  .cols{display:grid;grid-template-columns:1fr 1fr;gap:26px;}
  .panel{background:var(--night-2);border:1px solid var(--line);border-radius:3px;padding:24px;}
  .panel h4{font-size:11px;font-family:var(--mono);letter-spacing:.14em;text-transform:uppercase;
    margin-bottom:16px;}
  .panel.ok h4{color:var(--ok);}
  .panel.open h4{color:var(--stop);}
  .panel ul{margin:0;padding-left:17px;font-size:14px;color:var(--soft);}
  .panel li{margin-bottom:9px;}
  .panel li::marker{color:var(--gold-dim);}

  .filters{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px;}
  .filters button{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;
    text-transform:uppercase;background:transparent;color:var(--soft);
    border:1px solid var(--line-2);border-radius:100px;padding:7px 15px;cursor:pointer;}
  .filters button:hover{color:var(--gold);border-color:var(--gold-dim);}
  .filters button[aria-pressed="true"]{background:var(--gold);color:var(--night);border-color:var(--gold);}
  .filters button:focus-visible{outline:2px solid var(--gold);outline-offset:2px;}

  .roster{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:20px;}
  .who{background:var(--night-2);border:1px solid var(--line);border-radius:3px;
    padding:24px 22px;display:flex;flex-direction:column;gap:14px;}
  .who.hide{display:none;}
  .who-top{display:flex;gap:16px;align-items:flex-start;}
  .disc{flex:0 0 72px;width:72px;height:72px;border-radius:50%;
    border:1px solid var(--gold);background:var(--raise);object-fit:cover;display:block;}
  .disc.mono{display:flex;align-items:center;justify-content:center;
    font-family:var(--display);font-size:23px;color:var(--gold);}
  .who h3{font-size:20px;line-height:1.15;}
  .who .nat{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;
    text-transform:uppercase;color:var(--faint);margin-top:6px;display:block;}
  .role{font-size:13.5px;color:var(--soft);margin:0;}
  .role b{color:var(--ivory);font-weight:600;}

  .socials{display:flex;flex-direction:column;gap:5px;}
  .soc{display:flex;align-items:baseline;gap:7px;text-decoration:none;
    font-family:var(--mono);font-size:11px;padding:5px 9px;border-radius:2px;
    border:1px solid var(--line-2);color:var(--soft);font-variant-numeric:tabular-nums;}
  .soc .p{color:var(--faint);flex:0 0 62px;}
  .soc .h{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .soc b{margin-left:auto;color:var(--gold);font-weight:400;white-space:nowrap;}
  .soc i{margin-left:auto;color:var(--faint);}
  a.soc:hover,a.soc:focus-visible{border-color:var(--gold-dim);color:var(--ivory);outline:none;}
  .soc.nolink{border-style:dashed;}

  .acc{font-size:13px;color:var(--faint);border-top:1px solid var(--line);
    padding-top:13px;margin:0;}
  .tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:auto;padding-top:4px;}
  .tag{font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;
    padding:3px 8px;border-radius:100px;border:1px solid currentColor;}
  .tag.pend{color:var(--wait);}
  .tag.flag{color:var(--stop);}
  .tag.title{color:var(--ok);}

  .legs{display:flex;flex-direction:column;gap:22px;}
  .leg{background:var(--night-2);border:1px solid var(--line);border-radius:3px;overflow:hidden;}
  .leg-head{padding:22px 24px 0;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;}
  .leg-head h3{font-size:27px;}
  .leg-head .when{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;}
  .leg-head .st{margin-left:auto;font-family:var(--mono);font-size:9px;letter-spacing:.11em;
    text-transform:uppercase;padding:3px 9px;border-radius:100px;border:1px solid currentColor;}
  .leg-intro{padding:10px 24px 20px;margin:0;font-size:14px;color:var(--soft);
    border-bottom:1px solid var(--line);}
  .leg[data-c="ci"] h3,.leg[data-c="ci"] .when{color:var(--ci);}
  .leg[data-c="gh"] h3,.leg[data-c="gh"] .when{color:var(--gh);}
  .leg[data-c="ng"] h3,.leg[data-c="ng"] .when{color:var(--ng);}
  .leg-body{display:grid;grid-template-columns:repeat(3,1fr);}
  .lc{padding:22px 24px;border-right:1px solid var(--line);}
  .lc:last-child{border-right:none;}
  .lc h4{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;
    color:var(--faint);margin-bottom:14px;}
  .lc .it{margin-bottom:14px;}
  .lc .it strong{display:block;font-size:14px;font-weight:600;color:var(--ivory);}
  .lc .it span{font-size:12.5px;color:var(--faint);}
  .impact,.watch{padding:15px 24px;border-top:1px solid var(--line);font-size:13px;color:var(--soft);}
  .impact{background:rgba(119,190,141,.06);}
  .watch{background:var(--raise);}
  .impact b,.watch b{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;
    text-transform:uppercase;margin-right:12px;}
  .impact b{color:var(--ok);}
  .watch b{color:var(--stop);}

  .steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;}
  .step{border-top:1px solid var(--gold-dim);padding-top:16px;}
  .step .k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--gold);}
  .step h4{font-size:18px;margin:8px 0 7px;}
  .step p{font-size:13.5px;color:var(--faint);margin:0;}

  .closer{padding:86px 0;text-align:center;}
  .closer h2{font-size:clamp(26px,4.6vw,44px);line-height:1.14;max-width:17ch;margin:18px auto 0;}
  .closer p{color:var(--soft);max-width:52ch;margin:22px auto 0;font-size:15px;}
  footer{padding:32px 0 60px;color:var(--faint);font-size:12px;}
  footer p{margin:0 0 6px;}

  @media (max-width:900px){
    .prose{columns:1;}
    .countries{grid-template-columns:1fr;}
  }
  @media (max-width:820px){
    .cols,.pillars{grid-template-columns:1fr;}
    .leg-body{grid-template-columns:1fr;}
    .lc{border-right:none;border-bottom:1px solid var(--line);}
    .lc:last-child{border-bottom:none;}
  }
  @media (max-width:760px){
    .rings{opacity:.22;}
    .bill{font-size:16px;}
  }
</style>

<nav>
  <div class="wrap">
    <span class="mark">Detty <b>December</b></span>
    <a href="#project" class="sp">The Project</a>
    <a href="#pillars">Pillars</a>
    <a href="#lineup">Line-up</a>
    <a href="#route">Route</a>
    <a href="#status">Status</a>
  </div>
</nav>

<header class="hero">
  <div class="rings" aria-hidden="true">
    <i style="width:520px;height:520px;right:-130px;top:-120px;"></i>
    <i style="width:520px;height:520px;right:40px;top:60px;"></i>
    <i style="width:520px;height:520px;right:-45px;top:240px;"></i>
  </div>
  <div class="wrap">
    <div class="eyebrow">Project Hub · Pending Confirmation</div>
    <h1>Detty<br><em>December</em></h1>
    <p class="lede">A sixteen-day tour of Côte d'Ivoire, Ghana and Nigeria with fourteen of the
      world's most recognisable women — built on two pillars: showing West Africa to the world,
      and leaving something behind in every country we enter.</p>
    <div class="meta">
      <span>Dates <b>26 Dec – 10 Jan</b></span>
      <span>Countries <b>Three</b></span>
      <span>Line-up <b>14 invited</b></span>
      <span>Confirmed <b>None yet</b></span>
    </div>
    <div class="bill">
        {{BILL}}
    </div>
  </div>
</header>

<section id="project">
  <div class="wrap">
    <div class="eyebrow">The Project</div>
    <p class="thesis">West Africa in December is already the party. We are bringing the
      <em>women the world watches</em> — and making the trip count for something.</p>

    <div class="prose">
      <p><b>What this is.</b> Between 26 December and 10 January, fourteen titleholders and public
        figures — Miss Universe and Miss World titleholders, Miss France winners, and creators with
        genuine reach — travel together through Côte d'Ivoire, Ghana and Nigeria. They arrive in
        Abidjan on the 26th and open at Mother Africa Festival on the 27th.</p>
      <p><b>Why now.</b> "Detty December" has become one of the largest annual movements of people
        and money into West Africa, drawing the diaspora home for a month of festivals. Ghana and
        Nigeria both run government-backed December programmes. The season already exists — what it
        has not had is a single travelling group of this profile moving across three countries at once.</p>
      <p><b>What we aim to achieve.</b> Three things. Put West Africa in front of a combined audience
        of several million as a destination rather than a headline. Deliver a real, documented social
        impact action in each of the three countries, not a photo opportunity. And produce content
        with a life beyond the trip — footage that carries the destinations and the foundation work
        long after everyone flies home.</p>
      <p><b>Who it serves.</b> The countries get visibility and tourism attention in their peak
        season. The sponsors get reach and a genuine impact story. The women get a platform that
        connects them to the continent. And the communities we work with in each country get the
        actual point of the exercise.</p>
    </div>

    <div class="countries">
      <div class="country" data-c="ci">
        <h4>Côte d'Ivoire</h4><span class="w">26 – 31 December · Christmas</span>
        <p>Abidjan, Assinie, Sassandra and Yamoussoukro. Opens with Mother Africa Festival, a
          two-day pan-African culture festival drawing around forty thousand people.</p>
      </div>
      <div class="country" data-c="gh">
        <h4>Ghana</h4><span class="w">Early January · Cities open</span>
        <p>The heart of the diaspora return. Cities and dates are still to be set, and the whole
          season runs under a government programme that formally invites partners.</p>
      </div>
      <div class="country" data-c="ng">
        <h4>Nigeria</h4><span class="w">New Year – 10 January</span>
        <p>Lagos and Abuja. The densest events calendar of the three countries, and where the tour
          closes — New Year's and a birthday celebration.</p>
      </div>
    </div>
  </div>
</section>

<section id="pillars">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Two Pillars</div>
      <h2>Not only events</h2>
      <p>Every day of this tour should answer to one of these two things. Where a day serves
        neither, it does not belong on the itinerary.</p>
    </div>

    <div class="pillars">
      <div class="pillar">
        <div class="n">PILLAR ONE</div>
        <h3>Promoting West&nbsp;Africa</h3>
        <p>Showing three countries as places to come to — their festivals, coastlines, hotels and
          cities — through women whose audiences have never been shown them this way.</p>
        <ul>
          <li>Festival and cultural appearances in each country</li>
          <li>Destination content across Instagram, TikTok, YouTube and Snapchat</li>
          <li>Tourism board and ministry partnerships where they exist — Ghana's programme takes
            partner proposals directly</li>
          <li>Coastal, heritage and city coverage, not just nightlife</li>
        </ul>
      </div>
      <div class="pillar">
        <div class="n">PILLAR TWO</div>
        <h3>Social Impact</h3>
        <p>One substantive action in every country, planned with a local partner rather than
          arranged around a camera. Several of the women already run their own foundations.</p>
        <ul>
          <li>A vetted local NGO or foundation partner per country</li>
          <li>Holiday gift-giving, food and supply distribution, school and community visits</li>
          <li>Consent and dignity protocols before any filming of beneficiaries</li>
          <li>Impact reporting back to sponsors after the tour — measured, not implied</li>
        </ul>
      </div>
    </div>

    <div class="note">
      <b>Existing foundation work in the line-up.</b> Olivia Yacé runs the Fondation Olivia Yacé ·
      Dorcas Dienda's foundation works on child nutrition and education access in DRC ·
      Isabella Menin founded Beyond Project for disability organisations in Brazil ·
      Bella Zabaneh co-founded Project Royalty in Belize ·
      Nellie Anjaratiana's Beauty With a Purpose project addresses the stigma faced by twins in
      Madagascar. The second pillar is not something we are imposing on this group.
    </div>
  </div>
</section>

<section id="lineup">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">The Line-up</div>
      <h2>Fourteen women, none yet confirmed</h2>
      <p>Ordered by Instagram reach, with every account we could verify. Each profile was checked
        against public record — where the original list was wrong, the correction is on the card.</p>
    </div>

    <div class="filters" role="group" aria-label="Filter the line-up">
      <button type="button" data-f="all" aria-pressed="true">All 14</button>
      <button type="button" data-f="title" aria-pressed="false">Titleholders</button>
      <button type="button" data-f="creator" aria-pressed="false">Creators</button>
      <button type="button" data-f="flag" aria-pressed="false">Needs resolving</button>
    </div>

    <div class="roster" id="roster">{{CARDS}}
    </div>

    <div class="stats" style="margin-top:34px;">
      <div class="stat"><div class="n">14</div><div class="l">Invited</div><div class="s">none confirmed yet</div></div>
      <div class="stat"><div class="n">~6.1M</div><div class="l">Instagram reach</div><div class="s">estimated, unverified</div></div>
      <div class="stat"><div class="n">~1.4M</div><div class="l">TikTok reach</div><div class="s">where an account was found</div></div>
      <div class="stat"><div class="n">11</div><div class="l">Nationalities</div><div class="s">one still unidentified</div></div>
    </div>

    <div class="note">
      <b>On the numbers.</b> Every follower figure here is an estimate compiled from public sources —
      not a live platform reading, and not analytics. Engagement rate and audience demographics are
      private to each woman's own dashboard and cannot be obtained any other way than by requesting
      her official media kit. That request is part of the individual calls.
    </div>
  </div>
</section>

<section id="route">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">The Route</div>
      <h2>Three legs, sixteen days</h2>
      <p>Events, sponsor targets, ground partners and the social-impact position for each country.
        Nothing below is booked — these are verified options and leads, not commitments.</p>
    </div>
    <div class="legs">{{LEGS}}
    </div>
  </div>
</section>

<section id="status">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Where We Are</div>
      <h2>Settled, and still open</h2>
      <p>The shape of the trip is real. Several decisions underneath it are not — and they need
        answering before the itinerary, the sponsor pitch or the fourteen calls can be finalised.</p>
    </div>

    <div class="cols">
      <div class="panel ok">
        <h4>Established</h4>
        <ul>
          <li>Three host countries — Côte d'Ivoire, Ghana, Nigeria</li>
          <li>Arrival in Abidjan 26 December; Mother Africa Festival on the 27th–28th is the opening anchor</li>
          <li>Roughly 26 December to 10 January, closing in Nigeria</li>
          <li>An all-female line-up of titleholders and public figures</li>
          <li>Two pillars — promoting West Africa, and a social-impact action in each country</li>
          <li>Private jet between legs, vans and Escalades on the ground</li>
          <li>No plus-ones — talent travel solo</li>
          <li>An individual call with each woman before anything is signed</li>
        </ul>
      </div>
      <div class="panel open">
        <h4>Open — to decide with Olivia</h4>
        <ul>
          <li>Which pillar leads when the two compete for the same day</li>
          <li>Whose project this is — Olivia and Dorcas's initiative, or the agency's concept they host</li>
          <li>What "Minister of Enjoyment" means in practice</li>
          <li>Who funds it, and how the agency is paid</li>
          <li>Ghana cities and dates — the one fully open leg</li>
          <li>Whether New Year's Eve lands in Abidjan or Lagos</li>
          <li>Whether this is a documented trip or a media property that travels</li>
          <li>A foundation partner for Côte d'Ivoire — the only country without one identified</li>
        </ul>
      </div>
    </div>

    <div class="sec-head" style="margin-top:56px;">
      <div class="eyebrow">What's Next</div>
      <h2>Four things block everything else</h2>
    </div>
    <div class="steps">
      <div class="step"><div class="k">01</div><h4>Confirm the concept with Olivia</h4><p>Purpose, ownership, funding, and what "Minister of Enjoyment" means in practice.</p></div>
      <div class="step"><div class="k">02</div><h4>Send the roster corrections</h4><p>The title swap, the three names with no title, "Tai", and the "+1 Angelique" ambiguity.</p></div>
      <div class="step"><div class="k">03</div><h4>Lock Ghana cities and dates</h4><p>Hotels, sponsors and event RSVPs there are all downstream of this one decision.</p></div>
      <div class="step"><div class="k">04</div><h4>Set the budget and the paying client</h4><p>Sponsor pitches and vendor negotiations cannot meaningfully start without it.</p></div>
    </div>

    <div class="note">
      <b>Running in parallel:</b> individual calls with each woman covering concept, availability and
      terms · collecting official media kits · passports and visas as confirmations land ·
      Olivia's local list — the Mother Africa organiser, Bassam beach status, sponsor outreach, and a
      Côte d'Ivoire foundation partner · applying into the Ghana Tourism Authority partner process ·
      confirming the Lagos NYE flagship for 2026 · deciding the content production model and sizing the crew.
    </div>
  </div>
</section>

<div class="closer">
  <div class="wrap">
    <div class="eyebrow">The one thing to settle first</div>
    <h2>What is this trip actually for?</h2>
    <p>Promotion and impact are the two pillars. Which of them leads — when a festival slot and a
      foundation day fall on the same afternoon — is the decision everything else is built on.</p>
  </div>
</div>

<footer>
  <div class="wrap">
    <p>Internal project hub — working draft, compiled from public sources. {{NPHOTO}} of 14 photographs in place.</p>
    <p>Follower figures are estimates and should be replaced with official media-kit data before
      anything reaches a sponsor. Line-up is invited, not confirmed.</p>
  </div>
</footer>

<script>
  (function () {
    var btns = document.querySelectorAll(".filters button");
    var cards = document.querySelectorAll("#roster .who");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.dataset.f;
        btns.forEach(function (o) { o.setAttribute("aria-pressed", String(o === b)); });
        cards.forEach(function (c) {
          var k = c.dataset.k || "";
          c.classList.toggle("hide", !(f === "all" || k.indexOf(f) !== -1));
        });
      });
    });
  })();
</script>
"""

if __name__ == "__main__":
    main()
