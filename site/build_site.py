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
    status = p.get("status", "core")
    tags = {"core": '<span class="tag pend">Pending confirm</span>',
            "reserve": '<span class="tag reserve">Reserve</span>',
            "dropped": '<span class="tag dropped">Not selected</span>'}[status]
    if p["kind"] == "title":
        tags += '<span class="tag title">Titleholder</span>'
    for f in p["flags"]:
        tags += '<span class="tag flag">%s</span>' % E(f)
    kinds = p["kind"] + " " + status + (" flag" if p["flags"] else "")
    return got, """
      <article class="who st-%s" data-k="%s">
        <div class="who-top">%s
          <div><h3>%s</h3><span class="nat">%s</span></div></div>
        <p class="role"><b>%s.</b> %s</p>
        <div class="socials">%s</div>
        <p class="acc">%s</p>
        <div class="tags">%s</div>
      </article>""" % (status, kinds, disc, E(p["name"]), E(p["nat"]),
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
                 ("Sublime Côte d'Ivoire", "The tourism ministry's own promotion campaign — has an active pattern of paying for international sponsorship placements (Olympique de Marseille since 2023, Stade Français Paris since 2025). Strong precedent for exactly this kind of partnership."),
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
    dict(c="ng", name="Nigeria", when="New Year – 9 January", st="Draft", stc="wait",
         intro="The closing leg, the densest calendar, and the only market with confirmed active sponsors.",
         cols=[
             ("Events", [
                 ("Flytime Fest", "21–25 Dec, Eko Convention Centre. Twenty-one years running."),
                 ("Livespot Detty December Fest", "Co-produced with the Federal Ministry of Arts and Culture."),
                 ("Abuja Groovy December", "Moshood Abiola Stadium. Includes a “Miss Groovy December” pageant."),
                 ("Transcorp Hilton Abuja", "Runs its own NYE gala and New Year's Day show."),
             ]),
             ("Sponsor targets", [
                 ("Lagos State Ministry of Tourism, Arts and Culture", "Actively co-brands Detty December with corporate sponsors — Access Bank, MTN, Zenith Bank, Giwa Gardens. Reports $71.6M generated from Detty December 2024/25. The single strongest institutional precedent found anywhere on this tour."),
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
    dict(c="bj", name="Benin", when="Proposed — dates open", st="Unconfirmed", stc="stop",
         intro="Newly added to the brief. Real and researchable, but nothing here is booked, and the "
               "signature cultural event falls just after a Jan 9 close.",
         cols=[
             ("Events", [
                 ("We Love Eya Festival", "~27–28 Dec, Place de l'Amazone, Cotonou. Africa-focused Afro-urban/Afrobeat festival funding local youth \"EYA Centers\" — a real event with existing sponsor partners (Digital Virgo, Trace Urban)."),
                 ("Vodun Days", "8–10 Jan, Ouidah — the rebranded national Vodun/Voodoo festival, ceremonies and a beach concert stage. Falls just after a Jan 9 finish; extending one day would catch it."),
                 ("PFL Africa Finals", "20 Dec 2025, Sofitel Cotonou Dome — shows Cotonou now hosts large international productions, not itself repeatable on these dates."),
             ]),
             ("Sponsor targets", [
                 ("ANPT / Bénin Révélé", "The national tourism-development agency and its flagship campaign, targeting 2M visitors by 2030 with World Bank/AFD backing. Partnerships found so far are B2B (travel-trade agencies), not an ambassador programme — would need direct outreach."),
                 ("We Love Eya", "Independent festival brand with its own sponsor pattern — a natural co-activation partner given the overlapping date."),
             ]),
             ("Partners &amp; logistics", [
                 ("Sofitel Cotonou Marina Hotel &amp; Spa", "5-star, opened Nov 2023, private beach, largest convention space in the city."),
                 ("Golden Tulip Le Diplomate · Azalaï Hôtel Cotonou", "4-star alternatives, both near the airport/Marina district."),
                 ("Ouidah &amp; Ganvié", "Door of No Return, Python Temple, Sacred Forest, the stilt village — visitable year-round, no December-specific programming found."),
             ]),
         ],
         impact="Women's cooperatives and Vodun cultural-heritage preservation were named in the client's "
                "own itinerary sketch — no specific partner organisation identified yet.",
         watch="No confirmed December-specific festival tied to Ouidah or Ganvié themselves — their "
               "signature event is Vodun Days in January. DMC options (1 DMC World, TransAfrica, Denin "
               "Travel) are real but unvetted; confirm service quality directly before booking."),
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


def parse_reach(s):
    if not s or s == "—":
        return 0
    s = s.replace(",", "").strip()
    mult = 1
    if s.endswith("M"):
        mult, s = 1_000_000, s[:-1]
    elif s.endswith("K"):
        mult, s = 1_000, s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return 0


def fmt_reach(n):
    if n >= 1_000_000:
        return "%.1fM" % (n / 1_000_000)
    return "%.0fK" % (n / 1_000)


def roster_stats():
    active = [p for p in ROSTER if p.get("status") != "dropped"]
    ig = sum(parse_reach(r) for p in active for plat, h, u, r in p["socials"] if plat == "Instagram")
    tt = sum(parse_reach(r) for p in active for plat, h, u, r in p["socials"] if plat == "TikTok")
    nations = len(set(p["nat"] for p in active))
    return dict(ig=fmt_reach(ig), tt=fmt_reach(tt), nations=nations, active=len(active))


def bill_html():
    parts = []
    for p in ROSTER:
        if p.get("status") == "dropped":
            continue
        cls = ' class="rsv"' if p.get("status") == "reserve" else ""
        parts.append("<span%s>%s</span>" % (cls, E(p["name"])))
    return "\n        <i>·</i>\n        ".join(parts)


SCOPE_LABEL = {"global": "Global", "local": "Local only"}
SCOPE_COLOR = {"global": "ok", "local": "wait"}
CONF_LABEL = {"high": "Confirmed", "med": "Reported", "low": "Unconfirmed"}


def brands_html():
    rows = []
    for p in ROSTER:
        if p.get("status") == "dropped":
            continue
        b = p.get("brands", [])
        if not b:
            rows.append(
                '<div class="brow empty"><div class="bname">%s</div>'
                '<div class="bdeals"><span class="none">No verifiable brand history found</span></div></div>'
                % E(p["name"]))
            continue
        deals = "".join(
            '<span class="deal"><b>%s</b><i>%s</i>'
            '<span class="sc %s">%s</span>'
            '<span class="cf">%s</span></span>'
            % (E(brand), E(cat), SCOPE_COLOR[scope], SCOPE_LABEL[scope], CONF_LABEL[conf])
            for brand, cat, scope, conf in b
        )
        rows.append('<div class="brow"><div class="bname">%s</div><div class="bdeals">%s</div></div>' % (E(p["name"]), deals))
    return "".join(rows)


STATUS_ORDER = {"core": 0, "reserve": 1, "dropped": 2}


def main():
    if Image is None:
        print("Pillow not installed — photos will be skipped. pip install Pillow")
    cards, total, withpic = "", 0, 0
    ordered = sorted(enumerate(ROSTER, 1), key=lambda t: STATUS_ORDER.get(t[1].get("status", "core"), 0))
    for i, p in ordered:
        n, h = card_html(p, i)
        cards += h
        total += n
        withpic += 1 if n else 0

    rs = roster_stats()
    page = TEMPLATE.replace("{{BILL}}", bill_html()) \
                   .replace("{{CARDS}}", cards) \
                   .replace("{{LEGS}}", legs_html()) \
                   .replace("{{BRANDS}}", brands_html()) \
                   .replace("{{IG_SUM}}", rs["ig"]) \
                   .replace("{{TT_SUM}}", rs["tt"]) \
                   .replace("{{N_NATIONS}}", str(rs["nations"])) \
                   .replace("{{N_ACTIVE}}", str(rs["active"])) \
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
    --gold:#CFAA5C; --gold-dim:#8E6C29;
    --ivory:#F3E9EE; --soft:#B29AA7; --faint:#8A7280;
    --ci:#E08A58; --gh:#D96A66; --ng:#77BE8D; --bj:#B08FD9;
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

  .letterhead{background:var(--night);border-bottom:1px solid var(--line);}
  .lh-inner{display:flex;align-items:center;gap:9px;height:30px;font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;color:var(--faint);}
  .lh-badge{font-family:var(--display);font-size:13px;color:var(--gold);border:1px solid var(--gold-dim);border-radius:50%;width:19px;height:19px;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0;}
  .ftr-badge{width:26px;height:26px;font-size:16px;}
  .lh-sep{color:var(--line-2);}
  nav{position:sticky;top:30px;z-index:20;background:rgba(21,11,19,.94);
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
  .bill .rsv{color:var(--faint);font-style:italic;}
  .name-tbd{margin-top:20px;font-family:var(--mono);font-size:11px;color:var(--faint);
    letter-spacing:.04em;}
  .name-tbd b{color:var(--soft);font-weight:600;}

  .timeline{margin-top:38px;display:flex;flex-direction:column;}
  .tl-row{display:flex;align-items:baseline;gap:22px;padding:14px 0;
    border-top:1px solid var(--line);}
  .tl-row:last-child{border-bottom:1px solid var(--line);}
  .tl-y{font-family:var(--display);font-size:22px;color:var(--gold);width:64px;flex-shrink:0;}
  .tl-r{font-size:15px;color:var(--ivory);}
  .tl-c{margin-left:auto;font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;
    text-transform:uppercase;padding:3px 9px;border-radius:100px;border:1px solid currentColor;}
  .tl-c.ci{color:var(--ci);}
  .tl-note{margin-top:24px;font-size:14px;color:var(--soft);max-width:66ch;}

  section{padding:74px 0;border-bottom:1px solid var(--line);}
  .sec-head{margin-bottom:36px;}
  .sec-head h2{font-size:clamp(28px,4.2vw,42px);margin-top:10px;line-height:1.08;}
  .sec-head p{color:var(--soft);max-width:62ch;margin:14px 0 0;font-size:15px;}

  /* what this is */
  .thesis{font-family:var(--display);font-size:clamp(21px,2.9vw,31px);line-height:1.38;
    max-width:24ch;margin:0 0 34px;}
  .thesis em{font-style:italic;color:var(--gold);}
  .prose{columns:2;column-gap:44px;font-size:15px;color:var(--soft);max-width:none;}
  .prose.narrow{columns:1;max-width:62ch;}
  .prose p{margin:0 0 15px;break-inside:avoid;}
  .prose b{color:var(--ivory);font-weight:600;}

  .pillars{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:44px;}
  .pillars.obj-grid{grid-template-columns:repeat(auto-fit,minmax(230px,1fr));}
  .pillar{background:var(--night-2);border:1px solid var(--line);border-radius:3px;padding:28px 26px;}
  .pillar .n{font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--gold);}
  .pillar h3{font-size:25px;margin:12px 0 12px;}
  .pillar p{font-size:14.5px;color:var(--soft);margin:0 0 14px;}
  .pillar ul{margin:0;padding-left:17px;font-size:13.5px;color:var(--faint);}
  .pillar li{margin-bottom:7px;}
  .pillar li::marker{color:var(--gold-dim);}

  .countries{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:44px;}
  .country h4 .qmark{color:var(--stop);}
  .country{border-top:1px solid var(--line-2);padding-top:18px;}
  .country h4{font-size:21px;}
  .country .w{font-family:var(--mono);font-size:10px;letter-spacing:.13em;
    text-transform:uppercase;color:var(--faint);margin-top:6px;display:block;}
  .country p{font-size:13.5px;color:var(--soft);margin:12px 0 0;}
  .countries [data-c="ci"] h4{color:var(--ci);}
  .countries [data-c="gh"] h4{color:var(--gh);}
  .countries [data-c="ng"] h4{color:var(--ng);}
  .countries [data-c="bj"] h4{color:var(--bj);}

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
  .tag.reserve{color:var(--bj);}
  .tag.dropped{color:var(--faint);}
  .who.st-dropped{opacity:.55;}
  .who.st-dropped:hover{opacity:.85;}

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
  .leg[data-c="bj"] h3,.leg[data-c="bj"] .when{color:var(--bj);}
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

  .brands-table{display:flex;flex-direction:column;gap:1px;background:var(--line);
    border:1px solid var(--line);border-radius:3px;overflow:hidden;}
  .brow{background:var(--night-2);padding:16px 22px;display:grid;
    grid-template-columns:200px 1fr;gap:18px;align-items:flex-start;}
  .brow.empty{opacity:.72;}
  .bname{font-family:var(--display);font-size:16px;color:var(--ivory);padding-top:2px;}
  .bdeals{display:flex;flex-direction:column;gap:10px;}
  .deal{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-size:13px;}
  .deal b{color:var(--ivory);font-weight:600;}
  .deal i{color:var(--faint);font-style:normal;}
  .deal .sc{font-family:var(--mono);font-size:9px;letter-spacing:.09em;text-transform:uppercase;
    padding:2px 7px;border-radius:100px;border:1px solid currentColor;}
  .deal .sc.ok{color:var(--ok);}
  .deal .sc.wait{color:var(--wait);}
  .deal .cf{font-family:var(--mono);font-size:9px;letter-spacing:.09em;text-transform:uppercase;
    color:var(--faint);}
  .bdeals .none{font-size:13px;color:var(--faint);font-style:italic;}
  @media (max-width:640px){.brow{grid-template-columns:1fr;}}

  .steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;}
  .step{border-top:1px solid var(--gold-dim);padding-top:16px;}
  .step .k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;color:var(--gold);}
  .step h4{font-size:18px;margin:8px 0 7px;}
  .step p{font-size:13.5px;color:var(--faint);margin:0;}

  .closer{padding:86px 0;text-align:center;}
  .closer h2{font-size:clamp(26px,4.6vw,44px);line-height:1.14;max-width:17ch;margin:18px auto 0;}
  .closer p{color:var(--soft);max-width:52ch;margin:22px auto 0;font-size:15px;}
  footer{padding:40px 0 60px;color:var(--faint);font-size:12px;}
  footer p{margin:0 0 6px;}
  .ftr-brand{display:flex;align-items:center;gap:12px;margin-bottom:22px;padding-bottom:20px;border-bottom:1px solid var(--line);}
  .ftr-name{font-family:var(--mono);font-size:11px;letter-spacing:.1em;color:var(--ivory);}
  .ftr-line{font-size:11.5px;color:var(--faint);margin-top:4px;}

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

<div class="letterhead">
  <div class="wrap lh-inner">
    <span class="lh-badge">A</span>
    <span>ATOURE MANAGEMENT &amp; CONSULTING</span>
    <span class="lh-sep">·</span>
    <span>PROJECT HUB</span>
  </div>
</div>
<nav>
  <div class="wrap">
    <span class="mark">Detty <b>December</b></span>
    <a href="#project" class="sp">The Project</a>
    <a href="#objectives">Objectives</a>
    <a href="#vision">Vision</a>
    <a href="#lineup">Line-up</a>
    <a href="#route">Route</a>
    <a href="#brands">Brand History</a>
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
    <p class="lede">A tourism-diplomacy and cultural-exchange initiative — presented by Olivia Yacé
      International with the Fondation Olivia Yacé and national tourism boards. International
      titleholders, entrepreneurs, philanthropists and global digital creators showcase West
      Africa through tourism, philanthropy, entrepreneurship and culture.</p>
    <div class="meta">
      <span>Dates <b>26 Dec – 9 Jan</b></span>
      <span>Countries <b>Four</b></span>
      <span>Core line-up <b>10 + 3 reserve</b></span>
      <span>Confirmed <b>None yet</b></span>
    </div>
    <div class="bill">
        {{BILL}}
    </div>
    <p class="name-tbd">Working name: <b>West Africa Queens Tour</b> — not settled.</p>
  </div>
</header>

<section id="project">
  <div class="wrap">
    <div class="eyebrow">The Project</div>
    <p class="thesis">West Africa in December is already the party. We are bringing
      <em>women the world watches</em> — as cultural ambassadors, not vacationers.</p>

    <div class="prose narrow">
      <p>Between 26 December and 9 January, ten core titleholders, entrepreneurs and philanthropists
        — plus three reserves — travel together through Côte d'Ivoire, Ghana, Nigeria and, if
        confirmed, Benin. Framed correctly this is not an influencer trip: it is a diplomatic tourism
        initiative that tourism boards, airlines, hotel groups and luxury brands can support, with a
        combined audience the brief estimates at 30–70M+ followers discovering West Africa together.</p>
      <p>Every day should answer to one of five objectives — tourism promotion, economic impact,
        social impact, cultural exchange, international media — set out below. Where a day serves
        none of them, it does not belong on the itinerary.</p>
    </div>

    <div class="countries">
      <div class="country" data-c="ci">
        <h4>Côte d'Ivoire</h4><span class="w">Opens the tour · Christmas</span>
        <p>Abidjan, Assinie, Grand-Bassam, Banco National Park, Yamoussoukro. Opening ceremony,
          designer fashion shows, a children's hospital visit, and a tourism conference.</p>
      </div>
      <div class="country" data-c="gh">
        <h4>Ghana</h4><span class="w">Cities open</span>
        <p>Accra, Cape Coast Castle, Kakum National Park, artisan markets. A social project and
          entrepreneur meetings alongside the heritage sites.</p>
      </div>
      <div class="country" data-c="ng">
        <h4>Nigeria</h4><span class="w">Closes the tour</span>
        <p>Lagos — art galleries, Nigerian fashion, the Afrobeats industry, entrepreneur networking
          and a community action.</p>
      </div>
      <div class="country" data-c="bj">
        <h4>Benin <span class="qmark">?</span></h4><span class="w">Proposed, unconfirmed</span>
        <p>Ouidah, Ganvié, Vodun cultural heritage, women's cooperatives. Newly added — see the
          Route section for what's actually verifiable.</p>
      </div>
    </div>
  </div>
</section>

<section id="objectives">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Five Objectives</div>
      <h2>Not only events</h2>
      <p>The brief's own framing, kept intact — this is what every partner conversation should be
        pitched against, government or corporate.</p>
    </div>

    <div class="pillars obj-grid">
      <div class="pillar">
        <div class="n">01 — TOURISM PROMOTION</div>
        <h3>A modern West&nbsp;Africa</h3>
        <p>Show the region as modern, safe, luxurious, authentic, welcoming and rich in heritage —
          not only safaris or beaches.</p>
      </div>
      <div class="pillar">
        <div class="n">02 — ECONOMIC IMPACT</div>
        <h3>Real spend, not just reach</h3>
        <p>Spotlight hotels, airlines, restaurants, artisans, designers, museums and local
          businesses to stimulate the tourism economy of each participating country.</p>
      </div>
      <div class="pillar">
        <div class="n">03 — SOCIAL IMPACT</div>
        <h3>A legacy in every country</h3>
        <p>Through the Fondation Olivia Yacé — hospital visits, orphanage visits, girls' education,
          women's empowerment, environmental initiatives, school and medical donations.</p>
      </div>
      <div class="pillar">
        <div class="n">04 — CULTURAL EXCHANGE</div>
        <h3>Ambassadors, not tourists</h3>
        <p>Traditions, local culture, art, music, fashion and gastronomy — every guest leaves as a
          genuine ambassador for West Africa.</p>
      </div>
      <div class="pillar">
        <div class="n">05 — INTERNATIONAL MEDIA</div>
        <h3>Global and African press together</h3>
        <p>Built to draw international media alongside major African outlets, generating worldwide
          visibility for the region.</p>
      </div>
    </div>

    <div class="note">
      <b>Existing foundation work in the core group.</b> Olivia Yacé runs the Fondation Olivia Yacé ·
      Dorcas Dienda's foundation works on child nutrition and education access in DRC ·
      Isabella Menin founded Beyond Project for disability organisations in Brazil ·
      Bella Zabaneh co-founded Project Royalty in Belize · Sheynnis Palacios hosts a mental-health
      podcast and has advocacy ties to UNICEF, Smile Train and the AIDS Healthcare Foundation.
      Objective three is not something being imposed on this group.
    </div>
  </div>
</section>

<section id="vision">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Long-Term Vision</div>
      <h2>One continent, five years</h2>
      <p>The brief's own stated ambition — worth stating plainly, since it changes how this year's
        edition should be built. A first edition that can't repeat isn't the start of a franchise.</p>
    </div>
    <div class="timeline">
      <div class="tl-row"><span class="tl-y">2026</span><span class="tl-r">West Africa</span><span class="tl-c ci">this edition</span></div>
      <div class="tl-row"><span class="tl-y">2027</span><span class="tl-r">East Africa</span></div>
      <div class="tl-row"><span class="tl-y">2028</span><span class="tl-r">Southern Africa</span></div>
      <div class="tl-row"><span class="tl-y">2029</span><span class="tl-r">North Africa</span></div>
      <div class="tl-row"><span class="tl-y">2030</span><span class="tl-r">Central Africa</span></div>
    </div>
    <p class="tl-note">The stated goal is to become the largest women-led tourism and cultural
      promotion initiative on the continent. Whatever gets built for governance, budget and
      production this year is the template the next four editions inherit.</p>
  </div>
</section>

<section id="model">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Business Model</div>
      <h2>Where the money comes from</h2>
      <p>Ten proposed revenue streams from the brief. None are contracted yet — this is the target
        list, not a funding commitment.</p>
    </div>
    <div class="cols">
      <div class="panel">
        <h4>Institutional</h4>
        <ul>
          <li>National tourism board partnerships</li>
          <li>Airline partnerships</li>
          <li>Hotel group partnerships</li>
        </ul>
      </div>
      <div class="panel">
        <h4>Commercial</h4>
        <ul>
          <li>Private sponsorship</li>
          <li>Brand activations</li>
          <li>Official merchandise</li>
        </ul>
      </div>
      <div class="panel">
        <h4>Content &amp; events</h4>
        <ul>
          <li>Audiovisual broadcast rights</li>
          <li>International documentary</li>
          <li>Digital content production</li>
          <li>Charity gala</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="lineup">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">The Line-up</div>
      <h2>Eighteen candidates, ten core</h2>
      <p>Ten core plus three reserves is the working group — "the group can't be too big." The
        other five stay on record but are not being pursued. Every profile was checked against
        public record; where a name or title didn't match, the correction is on the card.</p>
    </div>

    <div class="filters" role="group" aria-label="Filter the line-up">
      <button type="button" data-f="all" aria-pressed="true">All 18</button>
      <button type="button" data-f="core" aria-pressed="false">Core Ten</button>
      <button type="button" data-f="reserve" aria-pressed="false">Reserves</button>
      <button type="button" data-f="dropped" aria-pressed="false">Not Selected</button>
      <button type="button" data-f="flag" aria-pressed="false">Needs resolving</button>
    </div>

    <div class="roster" id="roster">{{CARDS}}
    </div>

    <div class="stats" style="margin-top:34px;">
      <div class="stat"><div class="n">{{N_ACTIVE}}</div><div class="l">Core + reserve</div><div class="s">of 18 candidates</div></div>
      <div class="stat"><div class="n">{{IG_SUM}}</div><div class="l">Instagram reach</div><div class="s">core + reserve, per client tracking</div></div>
      <div class="stat"><div class="n">{{TT_SUM}}</div><div class="l">TikTok reach</div><div class="s">core + reserve, per client tracking</div></div>
      <div class="stat"><div class="n">{{N_NATIONS}}</div><div class="l">Nationalities/territories</div><div class="s">core + reserve</div></div>
    </div>

    <div class="note">
      <b>Pattern worth flagging.</b> Once identities were verified, the great majority of both the
      core group and the reserves turned out to be current Miss Universe 2025 national delegates
      (Thailand cycle, Nov 2025) rather than the broader mix of "entrepreneurs, philanthropists and
      digital creators" the positioning calls for. Worth deciding whether that concentration is fine
      or whether the profile mix needs deliberate broadening.
    </div>
    <div class="note">
      <b>On the numbers.</b> Follower figures for the reworked list are from the client's own
      September 2026 tracking, not public-search estimates — more current than the numbers on the
      original 14-name roster. Engagement rate and audience demographics still aren't public
      anywhere; that only comes from each woman's official media kit.
    </div>
  </div>
</section>

<section id="route">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">The Route</div>
      <h2>Four legs, one unconfirmed</h2>
      <p>Events, sponsor targets, ground partners and the social-impact position for each country.
        Nothing below is booked — these are verified options and leads, not commitments.</p>
    </div>
    <div class="legs">{{LEGS}}
    </div>
  </div>
</section>

<section id="brands">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Sponsor Precedent</div>
      <h2>What brand history actually exists</h2>
      <p>Researched to find international/global deals specifically — the point was to lean on each
        woman's own network rather than pitch African brands exclusively. Scoped to the 13 people
        actually in play (core + reserve); the five not selected are excluded here.</p>
    </div>

    <div class="stats" style="margin-bottom:34px;">
      <div class="stat"><div class="n">4</div><div class="l">With a global deal</div><div class="s">of 13 in the working group</div></div>
      <div class="stat"><div class="n">4</div><div class="l">Local deals only</div><div class="s">Olivia Yacé, Ophély Mézino, Bella Zabaneh, Hương Giang</div></div>
      <div class="stat"><div class="n">5</div><div class="l">No history found</div><div class="s">a real finding, not a gap in search</div></div>
    </div>

    <div class="brands-table">{{BRANDS}}
    </div>

    <div class="note">
      <b>Reading this.</b> Sheynnis Palacios (Pandora) is the strongest global tie found in this whole
      project — a confirmed, named jewelry-brand ambassadorship for Miss Universe 2023 herself. Alicia
      Aylies (Festina, Mauboussin, Palmer's, reserve) and Nadia Mejia (Guess, Kitchen Crafted) back it
      up. Angélique Angarni-Filopon's Festina deal is real but structural to the Miss France title, not
      personally negotiated. For everyone else, a sponsor pitch has to rest on reach and story, not an
      existing relationship to extend.
    </div>
  </div>
</section>

<section id="status">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Where We Are</div>
      <h2>Settled, and still open</h2>
      <p>The repositioning answered several questions that were open before — but it opened new ones.
        These need answering before the itinerary, the sponsor pitch or the calls to the core ten can
        be finalised.</p>
    </div>

    <div class="cols">
      <div class="panel ok">
        <h4>Established</h4>
        <ul>
          <li>Presented by Olivia Yacé International with the Fondation Olivia Yacé and national tourism boards</li>
          <li>Positioning: tourism diplomacy and cultural exchange, not an influencer trip</li>
          <li>Core group of ten, plus three reserves — Côte d'Ivoire, Ghana, Nigeria confirmed; Benin proposed</li>
          <li>Roughly 26 December to 9 January</li>
          <li>Five objectives — tourism, economic impact, social impact, cultural exchange, international media</li>
          <li>Camille Thomas shares her name with a well-known international cellist — disambiguate in every public-facing material</li>
          <li>No plus-ones — talent travel solo</li>
          <li>An individual call with each woman before anything is signed</li>
        </ul>
      </div>
      <div class="panel open">
        <h4>Open — to decide with Olivia</h4>
        <ul>
          <li>The tour name — "West Africa Queens Tour" is a working title only</li>
          <li>Whether the Miss Universe 2025-delegate concentration in the roster is intentional</li>
          <li>Whether Benin is confirmed as a fourth leg, given its signature event (Vodun Days) falls just after the Jan 9 close</li>
          <li>Ghana cities and dates — the one fully open leg among the confirmed three</li>
          <li>Who funds it, and which of the ten revenue streams are actually being pursued</li>
          <li>Government outreach sequencing — Sublime Côte d'Ivoire and Lagos Tourism both have strong precedent and are worth approaching first</li>
          <li>A foundation partner for Côte d'Ivoire — the only confirmed country without one identified</li>
          <li>Whether this is a documented trip or a media property that travels</li>
        </ul>
      </div>
    </div>

    <div class="sec-head" style="margin-top:56px;">
      <div class="eyebrow">What's Next</div>
      <h2>Four things block everything else</h2>
    </div>
    <div class="steps">
      <div class="step"><div class="k">01</div><h4>Settle the tour name</h4><p>"West Africa Queens Tour" is a placeholder — needed before any external pitch document goes out.</p></div>
      <div class="step"><div class="k">02</div><h4>Confirm Camille Thomas's disambiguation line</h4><p>Every bio, deck and press note needs "Miss Universe Curaçao" attached to her name to avoid the cellist mix-up.</p></div>
      <div class="step"><div class="k">03</div><h4>Decide Benin, one way or the other</h4><p>Real country, real hotels, but no December-specific event and no confirmed ambassador programme with ANPT.</p></div>
      <div class="step"><div class="k">04</div><h4>Set the budget and revenue mix</h4><p>Ten proposed streams; sponsor pitches can't start until which ones are live is decided.</p></div>
    </div>

    <div class="note">
      <b>Running in parallel:</b> individual calls with each of the core ten covering concept,
      availability and terms · collecting official media kits · passports and visas as confirmations
      land · outreach to Sublime Côte d'Ivoire and Lagos State Tourism, Arts and Culture — both have
      real, current sponsorship precedent · Ghana cities and dates · vetting the Benin DMC options
      directly before committing to anything there · deciding the content production model.
    </div>
  </div>
</section>

<div class="closer">
  <div class="wrap">
    <div class="eyebrow">The one thing to settle first</div>
    <h2>What is this trip actually for?</h2>
    <p>Five objectives are named. Which one leads — when a festival slot, a government meeting and a
      foundation visit compete for the same afternoon — is the decision everything else is built on.</p>
  </div>
</div>

<footer>
  <div class="wrap">
    <div class="ftr-brand">
      <span class="lh-badge ftr-badge">A</span>
      <div>
        <div class="ftr-name">ATOURE MANAGEMENT &amp; CONSULTING</div>
        <div class="ftr-line">30 Chichele Road, London, England &nbsp;·&nbsp; General@atoureconsulting.com &nbsp;·&nbsp; www.atoureconsulting.com</div>
      </div>
    </div>
    <p>Working draft, compiled from public sources and the client's own tracking. {{NPHOTO}} of 18
      photographs in place. Core and reserve line-up is proposed, not confirmed.</p>
    <p>Follower figures for the core group come from the client's own September 2026 tracking sheet.
      Engagement rate and audience demographics remain private — media kits only.</p>
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
