# -*- coding: utf-8 -*-
"""Three design directions, same content, so the choice is made by looking."""
import base64, io, os
from PIL import Image

M = "media/"
SRC = {"skyline": M + "AFRIQUEMAGAZINE_466_20250708-(3).pdf-image-010.jpg",
       "assinie": M + "assinie.webp",
       "crowd":   M + "Photo-by-Afronation-com.jpeg",
       "stage":   M + "Au-festival-de-musique-Mother-Africa.jpg",
       "poster":  M + "Mother-Africa.jpeg",
       "olivia":  "/home/user/Detty-December/deck/photos/olivia-yace.jpg",
       "sheynnis":"/home/user/Detty-December/deck/photos/sheynnis-palacios.jpg"}

def uri(im, q=84):
    b = io.BytesIO(); im.convert("RGB").save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def pic(key, w, h, focus=0.5):
    im = Image.open(SRC[key]).convert("RGB")
    ow, oh = im.size; t = w / h
    if ow / oh > t:
        nw = int(oh * t); left = int((ow - nw) * 0.5)
        im = im.crop((left, 0, left + nw, oh))
    else:
        nh = int(ow / t); top = int((oh - nh) * focus)
        im = im.crop((0, top, ow, top + nh))
    return uri(im.resize((w, h), Image.LANCZOS))

FONTS = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,300'
         '&family=Karla:wght@200;300;400;500;600&family=Anton&family=Archivo:wght@400;600;800'
         '&display=swap">')

CSS = """
*{box-sizing:border-box;}
body{margin:0;background:#15100c;font-family:'Karla',sans-serif;}
.deck{display:flex;flex-direction:column;align-items:center;gap:26px;padding:22px;}
.tag{color:#c9b89a;font:600 13px/1 'Karla';letter-spacing:.26em;text-transform:uppercase;
  align-self:flex-start;margin-left:calc(50% - 560px);}
.s{width:1120px;aspect-ratio:16/9;position:relative;overflow:hidden;container-type:inline-size;}
.bleed{position:absolute;inset:0;} .bleed img{width:100%;height:100%;object-fit:cover;display:block;}

/* ---------------- A. editorial travel magazine ---------------- */
.A{background:#FAF6EF;color:#1E1A15;}
.A .wash{position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,14,20,.55) 0%,
  rgba(10,14,20,.05) 38%,rgba(10,14,20,.30) 72%,rgba(10,14,20,.78) 100%);}
.A .cov{position:absolute;inset:0;padding:5cqw 6cqw;display:flex;flex-direction:column;
  align-items:center;text-align:center;z-index:2;color:#fff;}
.A .lab{font:400 1.05cqw/1 'Karla';letter-spacing:.42em;text-transform:uppercase;opacity:.9;}
.A .ttl{font:300 6.4cqw/1.02 'Fraunces';letter-spacing:-.01em;margin-top:2.4cqw;max-width:17ch;}
.A .rule{width:9cqw;height:1px;background:rgba(255,255,255,.75);margin:2.2cqw 0;}
.A .sub{font:300 1.6cqw/1.6 'Karla';max-width:44ch;opacity:.94;}
.A .foot{margin-top:auto;display:flex;justify-content:space-between;width:100%;
  font:400 .95cqw/1 'Karla';letter-spacing:.2em;text-transform:uppercase;opacity:.82;}
.A2{padding:4.4cqw 5.4cqw;display:flex;flex-direction:column;}
.A2 .hd{display:flex;justify-content:space-between;align-items:baseline;
  border-bottom:1px solid #D9CDB8;padding-bottom:1.1cqw;}
.A2 .hd b{font:400 1cqw/1 'Karla';letter-spacing:.34em;text-transform:uppercase;color:#9A8B72;}
.A2 h2{font:300 3.5cqw/1.08 'Fraunces';margin:2.2cqw 0 0;max-width:24ch;}
.A2 .band{display:grid;grid-template-columns:1.62fr 1fr;gap:1.2cqw;margin-top:2cqw;}
.A2 .band img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;}
.A2 .cols{columns:3;column-gap:2.6cqw;margin-top:2cqw;}
.A2 .cols p{margin:0 0 .9cqw;font:300 1.16cqw/1.62 'Karla';color:#4A4136;break-inside:avoid;}
.A2 .cols p b{font-weight:600;color:#1E1A15;}

/* ---------------- B. festival poster ---------------- */
.B{background:#0A0A0A;color:#fff;}
.B .wash{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.34) 0%,
  rgba(0,0,0,.10) 34%,rgba(0,0,0,.72) 74%,rgba(0,0,0,.95) 100%);}
.B .cov{position:absolute;inset:0;padding:3.4cqw 4cqw;display:flex;flex-direction:column;z-index:2;}
.B .strip{display:flex;gap:.6cqw;}
.B .strip i{height:1.1cqw;flex:1;display:block;}
.B .big{margin-top:auto;font:400 10.4cqw/.86 'Anton';text-transform:uppercase;letter-spacing:-.012em;}
.B .big em{font-style:normal;color:#FF7A18;}
.B .meta{margin-top:1.6cqw;display:flex;gap:1.6cqw;align-items:center;flex-wrap:wrap;}
.B .chip{background:#FF7A18;color:#0A0A0A;font:400 1.24cqw/1 'Anton';text-transform:uppercase;
  letter-spacing:.06em;padding:.62cqw .95cqw;}
.B .chip.g{background:#12B26A;} .B .chip.w{background:#fff;}
.B2{padding:3.4cqw 4cqw;display:flex;flex-direction:column;}
.B2 .kick{font:400 1.5cqw/1 'Anton';text-transform:uppercase;letter-spacing:.2em;color:#FF7A18;}
.B2 .line{display:grid;grid-template-columns:1fr auto;gap:1.6cqw;align-items:baseline;
  border-bottom:2px solid #262626;padding:.85cqw 0;}
.B2 .line span{font:400 3.4cqw/1 'Anton';text-transform:uppercase;}
.B2 .line.sm span{font-size:2.2cqw;color:#BDBDBD;}
.B2 .line i{font-style:normal;font:600 1.06cqw/1 'Archivo';letter-spacing:.14em;
  text-transform:uppercase;color:#FF7A18;}
.B2 .rows{margin-top:1.6cqw;}
.B2 .shots{position:absolute;right:4cqw;bottom:3.4cqw;display:flex;gap:.7cqw;}
.B2 .shots img{width:13cqw;aspect-ratio:1;object-fit:cover;display:block;}

/* ---------------- C. gallery ---------------- */
.C{background:#F3EFE8;color:#17150F;}
.C1{padding:6.4cqw 7.4cqw;display:grid;grid-template-columns:1fr 1fr;gap:5cqw;align-items:center;}
.C1 .txt .lab{font:300 .95cqw/1 'Karla';letter-spacing:.46em;text-transform:uppercase;color:#8C8171;}
.C1 .txt h1{font:300 4.3cqw/1.14 'Fraunces';margin:2.6cqw 0 0;letter-spacing:-.008em;}
.C1 .txt .sub{margin-top:2.2cqw;font:300 1.28cqw/1.75 'Karla';color:#5A5346;max-width:34ch;}
.C1 .txt .sig{margin-top:3.4cqw;padding-top:1.2cqw;border-top:1px solid #D5CCBC;
  font:300 .95cqw/1.6 'Karla';letter-spacing:.2em;text-transform:uppercase;color:#8C8171;}
.C1 figure{margin:0;} .C1 figure img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;}
.C1 figcaption{margin-top:.9cqw;font:300 .88cqw/1.5 'Karla';letter-spacing:.14em;
  text-transform:uppercase;color:#8C8171;}
.C2{padding:5.4cqw 7.4cqw;display:flex;flex-direction:column;}
.C2 .lab{font:300 .95cqw/1 'Karla';letter-spacing:.46em;text-transform:uppercase;color:#8C8171;}
.C2 h2{font:300 3cqw/1.14 'Fraunces';margin:1.8cqw 0 0;max-width:26ch;}
.C2 .grid{margin-top:auto;display:grid;grid-template-columns:repeat(3,1fr);gap:2.4cqw;}
.C2 .grid img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;}
.C2 .grid b{display:block;margin-top:.8cqw;font:400 1.16cqw/1.2 'Fraunces';}
.C2 .grid span{display:block;margin-top:.25cqw;font:300 .88cqw/1.45 'Karla';
  letter-spacing:.12em;text-transform:uppercase;color:#8C8171;}
"""

SK = pic("skyline", 1400, 788, .45)
CR = pic("crowd", 1400, 788, .3)
AS = pic("assinie", 900, 600, .5)
ST = pic("stage", 640, 640, .35)
OL = pic("olivia", 620, 775, .05)
SH = pic("sheynnis", 520, 694, .05)
PO = pic("poster", 520, 694, .5)

H = f"""<!doctype html><meta charset="utf-8"><title>Three directions</title>{FONTS}
<style>{CSS}</style><div class="deck">

<div class="tag">A &nbsp;·&nbsp; editorial travel magazine</div>
<section class="s A">
  <div class="bleed"><img src="{SK}" alt=""></div><div class="wash"></div>
  <div class="cov">
    <div class="lab">Olivia Yacé International &nbsp;·&nbsp; Fondation Olivia Yacé</div>
    <div class="ttl">Beauty Beyond Borders</div>
    <div class="rule"></div>
    <div class="sub">Ten titleholders. Ten days. Three countries, through the busiest month
      in West Africa's calendar.</div>
    <div class="foot"><span>Abidjan &nbsp;·&nbsp; Assinie &nbsp;·&nbsp; Accra &nbsp;·&nbsp; Lagos</span>
      <span>21 to 30 December 2026</span></div>
  </div>
</section>
<section class="s A A2">
  <div class="hd"><b style="color:#9A8B72">Why December</b><b>02</b></div>
  <h2>The region's biggest month, and it is already measured.</h2>
  <div class="band">
    <img src="{AS}" alt=""><img src="{pic('stage',600,400,.35)}" alt="">
  </div>
  <div class="cols">
    <p><b>$71.6m</b> went into the Lagos economy from Detty December 2024 alone, on 1.2 million visitors.</p>
    <p><b>1.29m</b> international visitors came to Ghana in 2024, up 12 per cent, worth $4.82bn in receipts.</p>
    <p><b>6.7m</b> visitors came to Côte d'Ivoire in 2025, up from 6.3 million the year before.</p>
  </div>
</section>

<div class="tag">B &nbsp;·&nbsp; festival poster</div>
<section class="s B">
  <div class="bleed"><img src="{CR}" alt=""></div><div class="wash"></div>
  <div class="cov">
    <div class="strip"><i style="background:#FF7A18"></i><i style="background:#fff"></i>
      <i style="background:#12B26A"></i><i style="background:#FF7A18"></i></div>
    <div class="big">Beauty<br>Beyond<br><em>Borders</em></div>
    <div class="meta">
      <span class="chip">21&ndash;30 Dec 2026</span>
      <span class="chip g">10 titleholders</span>
      <span class="chip w">Abidjan · Accra · Lagos</span>
    </div>
  </div>
</section>
<section class="s B B2">
  <div class="kick">What is already booked</div>
  <div class="rows">
    <div class="line"><span>Fally Ipupa</span><i>24&ndash;25 Dec · Abidjan</i></div>
    <div class="line"><span>Mother Africa</span><i>27&ndash;28 Dec · Abidjan</i></div>
    <div class="line"><span>AfroFuture</span><i>28&ndash;30 Dec · Accra</i></div>
    <div class="line sm"><span>Flytime Fest</span><i>22&ndash;25 Dec · Lagos</i></div>
    <div class="line sm"><span>Rhythm Unplugged</span><i>21 Dec · Lagos</i></div>
  </div>
  <div class="shots"><img src="{ST}" alt=""><img src="{pic('crowd',640,640,.3)}" alt=""></div>
</section>

<div class="tag">C &nbsp;·&nbsp; gallery</div>
<section class="s C C1">
  <div class="txt">
    <div class="lab">West Africa &nbsp;·&nbsp; December 2026</div>
    <h1>Beauty<br>Beyond Borders</h1>
    <div class="sub">Ten titleholders travel Côte d'Ivoire, Ghana and Nigeria together for ten
      days, hosted by Olivia Yacé, and are filmed the whole way.</div>
    <div class="sig">Olivia Yacé International<br>with the Fondation Olivia Yacé</div>
  </div>
  <figure><img src="{OL}" alt=""><figcaption>Olivia Yacé &nbsp;·&nbsp; host</figcaption></figure>
</section>
<section class="s C C2">
  <div class="lab">The delegation</div>
  <h2>Ten countries of origin, one December.</h2>
  <div class="grid">
    <div><img src="{pic('olivia',480,640,.05)}" alt=""><b>Olivia Yacé</b>
      <span>Côte d'Ivoire · Miss World Africa 2021</span></div>
    <div><img src="{SH}" alt=""><b>Sheynnis Palacios</b>
      <span>Nicaragua · Miss Universe 2023</span></div>
    <div><img src="{pic('assinie',480,640,.5)}" alt=""><b>Assinie</b>
      <span>Côte d'Ivoire · 26 December</span></div>
  </div>
</section>

</div>"""
open("samples.html", "w").write(H)
print("samples.html", round(os.path.getsize("samples.html") / 1e6, 2), "MB")
