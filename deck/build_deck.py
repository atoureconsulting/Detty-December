import base64, io, os
from PIL import Image

SC = "/tmp/claude-0/-home-user-Detty-December/dc1ddaf8-c346-5c37-8c29-e3e176f0c094/scratchpad"
PH = "/home/user/Detty-December/deck/photos/"
BK = SC + "/brandkit/"

def portrait(slug, w=620):
    im = Image.open(PH + slug + ".jpg").convert("RGB")
    ow, oh = im.size
    s = min(ow, oh)
    left = (ow - s) // 2
    top = max(0, int((oh - s) * 0.18))
    im = im.crop((left, top, left + s, top + s)).resize((w, w), Image.LANCZOS)
    b = io.BytesIO()
    im.save(b, "JPEG", quality=84, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

LADIES = [
    ("olivia-yace", "Olivia Yacé", "Côte d'Ivoire", "Miss Côte d'Ivoire 2021 · Miss World Africa", "Host &amp; convener"),
    ("sheynnis-palacios", "Sheynnis Palacios", "Nicaragua", "Miss Universe 2023", ""),
    ("veena-praveenar", "Veena Praveenar Singh", "Thailand", "Miss Universe Thailand 2025", ""),
    ("isabella-menin", "Isabella Menin", "Brazil", "Miss Grand International 2022", ""),
    ("angelique-angarni-filopon", "Angélique Angarni-Filopon", "Martinique", "Miss France 2025", ""),
    ("nadia-mejia", "Nadia Mejia", "Ecuador", "Miss Universe Ecuador 2025", ""),
    ("dorcas-dienda", "Dorcas Dienda", "DR Congo", "Miss Africa 2019 · Miss Universe DRC 2025", ""),
    ("ophely-mezino", "Ophély Mézino", "Guadeloupe", "Miss World 2019, 1st runner-up", ""),
    ("camille-thomas", "Camille Sabina Thomas", "Curaçao", "Miss Universe Curaçao 2025", ""),
    ("bella-zabaneh", "Bella Zabaneh", "Belize", "Miss Universe Belize 2025", ""),
]

logo = open(BK + "01-logos/atoure/atoure-nav-lockup-on-dark.svg").read()
# strip the xml width/height so it scales to its container
logo = logo.replace('width="2926" height="517"', 'width="100%" height="100%" preserveAspectRatio="xMinYMid meet"', 1)

cards = []
for slug, name, country, title, role in LADIES:
    extra = f'<span class="role">{role}</span>' if role else ""
    cards.append(f"""
      <figure class="q">
        <div class="q-img"><img src="{portrait(slug)}" alt="{name}"></div>
        <figcaption>
          <span class="q-country">{country}</span>
          <span class="q-name">{name}</span>
          <span class="q-title">{title}</span>{extra}
        </figcaption>
      </figure>""")
CARDS = "".join(cards)

OBJECTIVES = [
    ("01", "Tourism promotion", "Show the region as modern, safe, luxurious, authentic and rich in heritage — not only safaris and beaches."),
    ("02", "Economic impact", "Spotlight hotels, airlines, restaurants, artisans, designers, museums and local business in every host country."),
    ("03", "Social impact", "Hospital and orphanage visits, girls' education, women's empowerment, environmental and school initiatives, through the Fondation Olivia Yacé."),
    ("04", "Cultural exchange", "Traditions, art, music, fashion and gastronomy. Every guest leaves as a genuine ambassador for West Africa."),
    ("05", "International media", "Global press alongside major African outlets, generating worldwide visibility for the region."),
]
OBJ = "".join(f"""
    <div class="obj">
      <span class="obj-n">{n}</span>
      <h3>{t}</h3>
      <p>{d}</p>
    </div>""" for n, t, d in OBJECTIVES)

COUNTRIES = [
    ("Côte d'Ivoire", "Opens the tour", "Abidjan · Assinie · Grand-Bassam · Yamoussoukro",
     "Opening ceremony, designer fashion showcases, a children's hospital visit and a tourism conference."),
    ("Ghana", "Heritage leg", "Accra · Cape Coast Castle · Kakum National Park",
     "Artisan markets, a social project, and entrepreneur meetings alongside the heritage sites."),
    ("Nigeria", "Industry leg", "Lagos",
     "Art galleries, Nigerian fashion, the Afrobeats industry, entrepreneur networking and a community action."),
    ("Benin", "Proposed", "Ouidah · Ganvié · Cotonou",
     "Vodun cultural heritage, lake-village tourism and women's cooperatives."),
]
CTRY = "".join(f"""
      <div class="ctry">
        <div class="ctry-head">
          <h3>{n}</h3><span class="tag">{tag}</span>
        </div>
        <span class="ctry-cities">{cities}</span>
        <p>{d}</p>
      </div>""" for n, tag, cities, d in COUNTRIES)

EVENTS = [
    ("18–30 Dec", "Detty December Fest", "Ilubirin, Lagos", "13 days, two stages. Wizkid headlines the opener."),
    ("24–25 Dec", "Fally Ipupa — 20 Years", "Stade Félix-Houphouët-Boigny, Abidjan", "Two nights, ~60,000 across both."),
    ("26–27 Dec", "WeLovEya Festival", "Esplanade des Amazones, Cotonou", "3rd edition. Past bills: Davido, Rema, Asake."),
    ("27–28 Dec", "Mother Africa Festival", "Marcory Zone 4, Abidjan", "5th anniversary edition."),
    ("28–29 Dec", "AfroFuture Festival", "El-Wak Stadium, Accra", "Formerly Afrochella. Music, art, fashion village."),
    ("31 Dec", "Rapperholic", "Accra Sports Stadium", "Sarkodie's 15th edition, New Year's Eve."),
]
EVT = "".join(f"""
        <tr><td class="e-date">{dt}</td><td class="e-name">{n}</td><td class="e-place">{p}</td><td class="e-note">{d}</td></tr>"""
    for dt, n, p, d in EVENTS)

ACTS = [
    ("Festival main stage", "Mother Africa · AfroFuture · WeLovEya — the delegation on stage and in the crowd."),
    ("Opening ceremony", "Abidjan. Red carpet, national press, tourism board presence."),
    ("Designer showcase", "Ivorian and Nigerian designers dressing the delegation."),
    ("Foundation visit", "Hospital, school and orphanage programme with the Fondation Olivia Yacé."),
    ("Heritage &amp; landscape", "Cape Coast Castle · Ganvié · Assinie · Grand-Bassam."),
    ("Markets &amp; gastronomy", "Artisan markets, local makers, and the food of each country."),
]
ACT = "".join(f"""
      <div class="act">
        <div class="frame"><span>Photography to supply</span></div>
        <b>{t}</b><i>{d}</i>
      </div>""" for t, d in ACTS)

BUDGET = [
    ("Accommodation", "Four countries, fifteen nights", "53,000"),
    ("Air travel", "International arrivals and regional legs", "40,000"),
    ("Production &amp; documentary crew", "Full-time team across all legs", "47,000"),
    ("Per diem &amp; hospitality", "Delegation and staff", "20,000"),
    ("Ground transport &amp; security", "Vehicles, drivers, protection detail", "16,000"),
    ("Visas, insurance &amp; admin", "Delegation of seventeen", "3,000"),
    ("Contingency", "Approximately 12%", "21,000"),
]
BUD = "".join(f"""
        <tr><td class="b-item">{i}</td><td class="b-note">{n}</td><td class="b-amt">€{a}</td></tr>"""
    for i, n, a in BUDGET)

HTML = f"""<title>Beauty Beyond Borders</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Jost:wght@300;400;500;600&display=swap">
<style>
  :root{{
    --black:#0D0C0A; --black-soft:#1A1814; --black-mid:#2C2820;
    --gold:#C8A951; --gold-light:#E0C47A; --gold-dark:#A08830; --gold-pale:#F5EDD6;
    --cream:#FAF6EE; --cream-mid:#F0E8D4; --warm-white:#FEFCF8;
    --text-mid:#5C5040; --text-light:#9A8870;
    --serif:'Cormorant Garamond', Georgia, 'Times New Roman', serif;
    --sans:'Jost', 'Helvetica Neue', Arial, sans-serif;
  }}
  *{{box-sizing:border-box;}}
  body{{
    margin:0; background:var(--black); color:var(--cream);
    font-family:var(--sans); font-weight:300;
    -webkit-font-smoothing:antialiased;
  }}
  .deck{{ display:flex; flex-direction:column; align-items:center; gap:22px; padding-block:22px; padding-inline:16px; }}

  .slide{{
    width:100%; max-width:1120px; aspect-ratio:16/9;
    background:var(--black); border:1px solid rgba(200,169,81,.22);
    position:relative; overflow:hidden;
    display:flex; flex-direction:column;
    padding:44px 52px 40px;
    container-type:inline-size;
  }}
  /* everything inside scales with the slide so 16:9 holds at any width */
  .slide > *{{ position:relative; z-index:2; }}
  .s-num{{
    position:absolute; right:22px; bottom:16px; z-index:3;
    font-size:2.1cqw; letter-spacing:.14em; color:var(--gold-dark); font-weight:400;
  }}
  .rule-top{{ position:absolute; left:0; right:0; top:0; height:2px; background:linear-gradient(90deg,var(--gold) 0%, rgba(200,169,81,0) 62%); z-index:3; }}

  .eyebrow{{
    font-size:1.55cqw; letter-spacing:.34em; text-transform:uppercase;
    color:var(--gold); font-weight:400; margin-bottom:2.2cqw;
  }}
  h1{{ font-family:var(--serif); font-weight:400; font-size:8.6cqw; line-height:.98; margin:0; letter-spacing:-.01em; }}
  h1 em{{ font-style:italic; color:var(--gold-light); font-weight:300; }}
  h2{{ font-family:var(--serif); font-weight:400; font-size:5.4cqw; line-height:1.06; margin:0 0 2cqw; letter-spacing:-.005em; text-wrap:balance; }}
  h2 em{{ font-style:italic; color:var(--gold-light); }}
  h3{{ font-family:var(--serif); font-weight:500; font-size:2.9cqw; margin:0; line-height:1.15; }}
  p{{ font-size:1.72cqw; line-height:1.62; color:var(--cream); opacity:.88; margin:0; font-weight:300; }}
  .lead{{ font-size:2.15cqw; line-height:1.55; max-width:60ch; }}
  .muted{{ color:var(--text-light); }}

  /* ---------- cover ---------- */
  .cover{{ justify-content:space-between; }}
  .cover .logo{{ width:26cqw; height:4.6cqw; }}
  .cover .logo svg{{ width:100%; height:100%; display:block; }}
  .cover-mid h1{{ font-size:11cqw; }}
  .cover-line{{ width:100%; height:1px; background:linear-gradient(90deg,var(--gold),rgba(200,169,81,.05)); margin:2.6cqw 0; }}
  .cover-meta{{ display:flex; justify-content:space-between; align-items:flex-end; gap:3cqw; }}
  .cover-meta .m{{ font-size:1.5cqw; letter-spacing:.2em; text-transform:uppercase; color:var(--text-light); }}
  .cover-meta .m b{{ display:block; color:var(--gold-pale); font-weight:400; letter-spacing:.12em; margin-top:.5cqw; font-size:1.62cqw; }}
  .cover-glow{{ position:absolute; z-index:1; right:-18%; top:-30%; width:70%; height:150%;
    background:radial-gradient(ellipse at center, rgba(200,169,81,.15) 0%, rgba(200,169,81,0) 62%); }}

  /* ---------- generic layout helpers ---------- */
  .body-grid{{ display:grid; grid-template-columns:1.15fr 1fr; gap:4cqw; align-items:start; flex:1; }}
  .stats{{ display:flex; gap:3.4cqw; margin-top:auto; padding-top:2.4cqw; border-top:1px solid rgba(200,169,81,.24); }}
  .stat .n{{ font-family:var(--serif); font-size:5.2cqw; color:var(--gold-light); line-height:1; display:block; }}
  .stat .l{{ font-size:1.32cqw; letter-spacing:.2em; text-transform:uppercase; color:var(--text-light); margin-top:.7cqw; display:block; }}

  /* ---------- objectives ---------- */
  .objs{{ display:grid; grid-template-columns:repeat(5,1fr); gap:1.9cqw; flex:1; align-content:center; }}
  .obj{{ border-top:1px solid rgba(200,169,81,.32); padding-top:1.5cqw; display:flex; flex-direction:column; gap:.9cqw; }}
  .obj-n{{ font-family:var(--serif); font-size:2.6cqw; color:var(--gold); line-height:1; }}
  .obj h3{{ font-size:2.15cqw; }}
  .obj p{{ font-size:1.36cqw; line-height:1.55; opacity:.8; }}

  /* ---------- delegation ---------- */
  .slide.people{{ padding:30px 42px 30px; }}
  .people .eyebrow{{ margin-bottom:1.3cqw; }}
  .queens{{ display:grid; grid-template-columns:repeat(5,1fr); gap:1.05cqw 1.2cqw; flex:1; align-content:start; }}
  .q{{ margin:0; display:flex; flex-direction:column; gap:.55cqw; }}
  .q-img{{ aspect-ratio:1/.9; overflow:hidden; border:1px solid rgba(200,169,81,.3); background:var(--black-soft); }}
  .q-img img{{ width:100%; height:100%; object-fit:cover; object-position:50% 22%; display:block; filter:saturate(.97); }}
  .q figcaption{{ display:flex; flex-direction:column; gap:.15cqw; }}
  .q-country{{ font-size:.94cqw; letter-spacing:.2em; text-transform:uppercase; color:var(--gold); }}
  .q-name{{ font-family:var(--serif); font-size:1.56cqw; color:var(--cream); line-height:1.12; }}
  .q-title{{ font-size:.94cqw; line-height:1.32; color:var(--text-light); }}
  .q .role{{ font-size:.94cqw; color:var(--gold-light); font-style:italic; }}

  /* ---------- activities / shot list ---------- */
  .slide.acts-slide h2{{ font-size:3.6cqw; margin-bottom:1.2cqw; }}
  .acts{{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.2cqw; flex:1; align-content:start; }}
  .act{{ display:flex; flex-direction:column; gap:.6cqw; }}
  .act .frame{{ aspect-ratio:16/5.5; border:1px dashed rgba(200,169,81,.42); background:
      repeating-linear-gradient(135deg, rgba(200,169,81,.045) 0 8px, rgba(200,169,81,0) 8px 16px);
    display:flex; align-items:center; justify-content:center; }}
  .act .frame span{{ font-size:1.02cqw; letter-spacing:.2em; text-transform:uppercase; color:var(--gold-dark); }}
  .act b{{ font-family:var(--serif); font-weight:500; font-size:1.95cqw; color:var(--gold-light); line-height:1.15; }}
  .act i{{ font-style:normal; font-size:1.2cqw; color:var(--text-light); line-height:1.45; }}

  /* ---------- reach ---------- */
  .reach{{ display:grid; grid-template-columns:repeat(4,1fr); gap:2.4cqw; align-items:end; margin:1cqw 0 2cqw; }}
  .reach .r{{ border-left:1px solid rgba(200,169,81,.3); padding-left:1.6cqw; }}
  .reach .rn{{ font-family:var(--serif); font-size:6.4cqw; line-height:.95; color:var(--gold-light); display:block; }}
  .reach .rl{{ font-size:1.3cqw; letter-spacing:.2em; text-transform:uppercase; color:var(--text-light); margin-top:.8cqw; display:block; }}
  .regions{{ display:flex; flex-wrap:wrap; gap:.7cqw; margin-top:.6cqw; }}
  .pill{{ border:1px solid rgba(200,169,81,.34); color:var(--gold-pale); font-size:1.24cqw;
    letter-spacing:.11em; text-transform:uppercase; padding:.55cqw 1.1cqw; border-radius:99px; }}
  .caveat{{ font-size:1.22cqw; color:var(--text-light); margin-top:auto; padding-top:1.6cqw; border-top:1px solid rgba(200,169,81,.18); line-height:1.5; }}

  /* ---------- countries ---------- */
  .ctrys{{ display:grid; grid-template-columns:repeat(4,1fr); gap:1.8cqw; flex:1; align-content:center; }}
  .ctry{{ border-top:1px solid rgba(200,169,81,.32); padding-top:1.4cqw; }}
  .ctry-head{{ display:flex; align-items:baseline; justify-content:space-between; gap:.6cqw; }}
  .ctry h3{{ font-size:2.1cqw; }}
  .tag{{ font-size:1.02cqw; letter-spacing:.16em; text-transform:uppercase; color:var(--gold); white-space:nowrap; }}
  .ctry-cities{{ display:block; font-size:1.22cqw; color:var(--gold-light); margin:.8cqw 0 .9cqw; line-height:1.45; }}
  .ctry p{{ font-size:1.32cqw; line-height:1.55; opacity:.8; }}
  .slot{{ margin-top:1.2cqw; aspect-ratio:16/10; border:1px dashed rgba(200,169,81,.35);
    display:flex; align-items:center; justify-content:center; text-align:center; padding:.8cqw;
    font-size:1.05cqw; letter-spacing:.12em; text-transform:uppercase; color:var(--gold-dark); background:rgba(200,169,81,.04); }}

  /* ---------- tables ---------- */
  table{{ width:100%; border-collapse:collapse; }}
  td{{ padding:1.05cqw .6cqw; border-bottom:1px solid rgba(200,169,81,.16); vertical-align:baseline; }}
  tr:last-child td{{ border-bottom:none; }}
  .e-date{{ font-size:1.36cqw; letter-spacing:.1em; text-transform:uppercase; color:var(--gold); white-space:nowrap; width:14%; }}
  .e-name{{ font-family:var(--serif); font-size:2.25cqw; color:var(--cream); width:28%; }}
  .e-place{{ font-size:1.32cqw; color:var(--gold-light); width:28%; }}
  .e-note{{ font-size:1.28cqw; color:var(--text-light); }}
  .b-item{{ font-family:var(--serif); font-size:2.25cqw; color:var(--cream); width:36%; }}
  .b-note{{ font-size:1.32cqw; color:var(--text-light); }}
  .b-amt{{ font-family:var(--serif); font-size:2.45cqw; color:var(--gold-light); text-align:right; white-space:nowrap;
    font-variant-numeric:tabular-nums; }}
  .b-total td{{ border-top:1px solid var(--gold); border-bottom:none; padding-top:1.5cqw; }}
  .slide.budget td{{ padding:.78cqw .6cqw; }}
  .slide.budget h2{{ margin-bottom:1.2cqw; }}
  .slide.budget .caveat{{ padding-top:1.1cqw; margin-top:1.2cqw; padding-right:6cqw; }}
  .b-total .b-item{{ font-size:2.6cqw; color:var(--gold); }}
  .b-total .b-amt{{ font-size:3.6cqw; color:var(--gold); }}

  /* ---------- list ---------- */
  ul.ticks{{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:1.15cqw; }}
  ul.ticks li{{ display:flex; gap:1.1cqw; align-items:baseline; font-size:1.62cqw; line-height:1.5; }}
  ul.ticks li::before{{ content:"—"; color:var(--gold); flex:none; }}
  .fdns{{ display:grid; grid-template-columns:repeat(2,1fr); gap:1.5cqw 2.6cqw; }}
  .fdn{{ border-left:1px solid rgba(200,169,81,.3); padding-left:1.4cqw; }}
  .fdn b{{ font-family:var(--serif); font-weight:500; font-size:2cqw; color:var(--gold-light); display:block; line-height:1.2; }}
  .fdn span{{ font-size:1.32cqw; color:var(--cream); opacity:.82; line-height:1.5; display:block; margin-top:.4cqw; }}

  /* ---------- closing ---------- */
  .closing{{ align-items:center; justify-content:center; text-align:center; }}
  .closing .logo{{ width:30cqw; height:5.2cqw; margin-top:3cqw; }}
  .closing .logo svg{{ width:100%; height:100%; display:block; }}

  @media (max-width:700px){{
    .slide{{ padding:26px 22px 24px; }}
  }}
</style>

<div class="deck">

  <!-- 1 COVER -->
  <section class="slide cover">
    <div class="cover-glow"></div>
    <div class="logo">{logo}</div>
    <div class="cover-mid">
      <div class="eyebrow">Olivia Yacé International × Fondation Olivia Yacé</div>
      <h1>Beauty Beyond<br><em>Borders</em></h1>
      <div class="cover-line"></div>
    </div>
    <div class="cover-meta">
      <div class="m">Host countries<b>Côte d'Ivoire · Ghana · Nigeria · Benin</b></div>
      <div class="m">Dates<b>24 Dec 2026 — 9 Jan 2027</b></div>
      <div class="m">Delegation<b>Ten international titleholders</b></div>
    </div>
    <div class="s-num">01</div>
  </section>

  <!-- 2 THE PROJECT -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">The project</div>
    <div class="body-grid">
      <div>
        <h2>West Africa in December is already the party. We are bringing <em>the women the world watches</em>.</h2>
      </div>
      <div style="display:flex;flex-direction:column;gap:1.6cqw;">
        <p class="lead">Ten international titleholders, entrepreneurs, philanthropists and global digital creators travel West Africa together for fifteen days — hosted by Olivia Yacé, delivered with the Fondation Olivia Yacé, and presented alongside national tourism boards.</p>
        <p>Framed correctly this is not an influencer trip. It is a tourism-diplomacy and cultural-exchange initiative that tourism boards, airlines, hotel groups and luxury brands can support — and that leaves something behind in every country it visits.</p>
      </div>
    </div>
    <div class="stats">
      <div class="stat"><span class="n">10</span><span class="l">Countries of origin</span></div>
      <div class="stat"><span class="n">4</span><span class="l">Host countries</span></div>
      <div class="stat"><span class="n">15</span><span class="l">Days</span></div>
      <div class="stat"><span class="n">≈15M</span><span class="l">Combined following</span></div>
    </div>
    <div class="s-num">02</div>
  </section>

  <!-- 3 OBJECTIVES -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Goals &amp; aims</div>
    <h2>Every day answers to one of <em>five objectives</em>.</h2>
    <div class="objs">{OBJ}</div>
    <div class="s-num">03</div>
  </section>

  <!-- 4 DELEGATION -->
  <section class="slide people">
    <div class="rule-top"></div>
    <div class="eyebrow">The delegation · ten core</div>
    <div class="queens">{CARDS}</div>
    <div class="s-num">04</div>
  </section>

  <!-- 5 REACH -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Visibility</div>
    <h2>Ten women. Ten territories. <em>One audience</em>.</h2>
    <div class="reach">
      <div class="r"><span class="rn">7.9M</span><span class="rl">Instagram</span></div>
      <div class="r"><span class="rn">5.2M</span><span class="rl">TikTok</span></div>
      <div class="r"><span class="rn">1.9M</span><span class="rl">Facebook</span></div>
      <div class="r"><span class="rn">15M</span><span class="rl">Combined</span></div>
    </div>
    <p class="lead" style="margin-bottom:1.4cqw;">The delegation carries its own audiences into markets that rarely see West Africa presented this way — and brings the international press that follows them.</p>
    <div class="regions">
      <span class="pill">West Africa</span><span class="pill">Central Africa</span><span class="pill">Caribbean</span>
      <span class="pill">Latin America</span><span class="pill">South-East Asia</span><span class="pill">Europe</span>
    </div>
    <div class="caveat">Combined platform totals for the core ten, from the September 2026 tracking sheet. Followings are summed across Instagram, TikTok and Facebook and are not deduplicated between platforms.</div>
    <div class="s-num">05</div>
  </section>

  <!-- 6 TOURISM -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Tourism</div>
    <h2>Four countries, <em>one route</em>.</h2>
    <div class="ctrys">{CTRY}</div>
    <div class="s-num">06</div>
  </section>

  <!-- 7 ENTERTAINMENT -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Entertainment</div>
    <h2>The tour doesn't build the audience. <em>It joins it.</em></h2>
    <table>{EVT}</table>
    <div class="caveat">Festival dates as published at September 2026. The itinerary is being built around these, not alongside them.</div>
    <div class="s-num">07</div>
  </section>

  <!-- 8 ACTIVITIES -->
  <section class="slide acts-slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Activities · shot list</div>
    <h2>What the fifteen days <em>actually look like</em>.</h2>
    <div class="acts">{ACT}</div>
    <div class="caveat">Photography to be supplied or commissioned. Festival imagery requires clearance from each rights holder before it appears in a document sent externally.</div>
    <div class="s-num">08</div>
  </section>

  <!-- 9 SOCIAL IMPACT -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Social impact</div>
    <div class="body-grid" style="grid-template-columns:.85fr 1.15fr;">
      <div>
        <h2>Not a programme bolted onto a trip.</h2>
        <p>Four of the ten already run or co-found their own foundations. The Fondation Olivia Yacé leads the programme in each country — hospital and orphanage visits, girls' education, women's empowerment, school and environmental initiatives — with the delegation's own organisations joining where their work overlaps.</p>
      </div>
      <div class="fdns">
        <div class="fdn"><b>Fondation Olivia Yacé</b><span>Leads the social programme across all four countries.</span></div>
        <div class="fdn"><b>Dorcas Dienda Foundation</b><span>Child nutrition, education access, and women's empowerment through art and fashion mentorship in the DRC.</span></div>
        <div class="fdn"><b>Beyond Project — Isabella Menin</b><span>Supports disability organisations in Brazil.</span></div>
        <div class="fdn"><b>Project Royalty — Bella Zabaneh</b><span>Co-founded in 2019, supporting young Belizean women.</span></div>
      </div>
    </div>
    <div class="caveat">Sheynnis Palacios brings mental-health advocacy and ties to UNICEF, Smile Train and the AIDS Healthcare Foundation at advocate level.</div>
    <div class="s-num">09</div>
  </section>

  <!-- 10 PRODUCTION -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Documentation</div>
    <div class="body-grid">
      <div>
        <h2>Filmed as a series, not <em>covered as an event</em>.</h2>
        <p class="lead">A professional production team documents all fifteen days as a reality format — the arrivals, the foundation work, the festivals, the friendships and the friction.</p>
      </div>
      <div>
        <ul class="ticks">
          <li>Full-time production crew across every leg</li>
          <li>Reality series format, built broadcast-ready</li>
          <li>Short-form cut daily for the delegation's own channels</li>
          <li>Broadcast and documentary rights as a revenue stream</li>
          <li>Archive footage licensed back to tourism boards and sponsors</li>
        </ul>
      </div>
    </div>
    <div class="caveat">Production partner to be appointed. Broadcast and streaming distribution is a named revenue stream in the business model, not an assumed commitment.</div>
    <div class="s-num">10</div>
  </section>

  <!-- 11 BUDGET -->
  <section class="slide budget">
    <div class="rule-top"></div>
    <div class="eyebrow">Budget</div>
    <h2>A tour of this size runs at <em>€200,000</em>.</h2>
    <table>
      {BUD}
      <tr class="b-total"><td class="b-item">Total</td><td class="b-note">Delegation of seventeen, fifteen days, four countries</td><td class="b-amt">€200,000</td></tr>
    </table>
    <div class="caveat">Working estimate. Hotel, flight and ground-transport rates researched September 2026; production and hospitality lines pending vendor quotes. No sponsor in-kind contribution has been deducted — every confirmed partnership reduces this figure.</div>
    <div class="s-num">11</div>
  </section>

  <!-- 12 PARTNERSHIP -->
  <section class="slide">
    <div class="rule-top"></div>
    <div class="eyebrow">Partnership</div>
    <div class="body-grid">
      <div>
        <h2>What a partner takes home.</h2>
        <ul class="ticks" style="margin-top:1.6cqw;">
          <li>Named association across four West African markets</li>
          <li>Presence inside the series, not around it</li>
          <li>The delegation's combined reach and the press that follows it</li>
          <li>A social-impact programme with the Fondation Olivia Yacé</li>
          <li>A rights-cleared content archive to reuse after the tour</li>
        </ul>
      </div>
      <div>
        <div class="eyebrow" style="margin-bottom:1.4cqw;">Partners in discussion</div>
        <div class="fdns" style="grid-template-columns:1fr;">
          <div class="fdn"><b>National tourism bodies</b><span>Sublime Côte d'Ivoire · Ghana Ministry of Tourism · Lagos State Ministry of Tourism, Arts &amp; Culture · ANPT Benin</span></div>
          <div class="fdn"><b>Festival partners</b><span>Mother Africa Festival · WeLovEya Festival</span></div>
          <div class="fdn"><b>Travel &amp; hospitality</b><span>Air Côte d'Ivoire · Sofitel / Accor · Kempinski · Eko Hotels</span></div>
        </div>
      </div>
    </div>
    <div class="caveat">Target list. No partnership named here is contracted at the date of this document.</div>
    <div class="s-num">12</div>
  </section>

  <!-- 13 CLOSE -->
  <section class="slide closing">
    <div class="cover-glow"></div>
    <div class="eyebrow">Côte d'Ivoire · Ghana · Nigeria · Benin</div>
    <h1 style="font-size:9cqw;">Beauty Beyond<br><em>Borders</em></h1>
    <div class="logo">{logo}</div>
    <div class="s-num">13</div>
  </section>

</div>
"""

out = SC + "/bbb-deck.html"
with open(out, "w") as f:
    f.write(HTML)
print("written", out, os.path.getsize(out) / 1e6, "MB")
