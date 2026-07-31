const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "Tour Management";
pres.title = "Detty December — Tour Concept Deck";

// ---------- palette ----------
const PLUM   = "2E1428"; // dark ground
const PLUM_D = "1C0C18"; // deeper
const GOLD   = "C9992B";
const GOLD_L = "E8C766";
const GOLD_D = "4A3320"; // decorative on dark
const WHITE  = "FFFFFF";
const BODY   = "3A3038";
const MUTED  = "7A6E76";
const RULE   = "E4DDE2";
const CARD   = "F6F2F5";
const CI     = "C25E2A";
const GH     = "A32C2C";
const NG     = "2E6B3E";
const CRIT   = "9C2C2C";
const OK     = "2E6B3E";
const WARN   = "8A6A12";

const HEAD = "Cambria";
const SANS = "Calibri";

const M = 0.62;            // page margin
const W = 13.33;
const CW = W - M * 2;      // content width = 12.09

// ---------- helpers ----------
function darkSlide() {
  const s = pres.addSlide();
  s.background = { color: PLUM };
  return s;
}
function lightSlide() {
  const s = pres.addSlide();
  s.background = { color: WHITE };
  return s;
}

// section header for light slides: eyebrow + title, no rules/stripes
function head(s, eyebrow, title, sub) {
  s.addText(eyebrow, {
    x: M, y: 0.42, w: CW, h: 0.26, margin: 0,
    fontFace: SANS, fontSize: 10.5, bold: true, color: GOLD, charSpacing: 2.6,
  });
  s.addText(title, {
    x: M, y: 0.72, w: CW, h: 0.62, margin: 0,
    fontFace: HEAD, fontSize: 33, bold: true, color: PLUM,
  });
  if (sub) {
    s.addText(sub, {
      x: M, y: 1.36, w: CW - 0.4, h: 0.4, margin: 0,
      fontFace: SANS, fontSize: 13, color: MUTED,
    });
  }
}

// gold circle with a number/letter — the repeating motif
function goldDot(s, x, y, d, label, labelColor) {
  s.addShape(pres.ShapeType.ellipse, {
    x, y, w: d, h: d, fill: { color: GOLD },
  });
  s.addText(label, {
    x, y, w: d, h: d, margin: 0,
    align: "center", valign: "middle",
    fontFace: SANS, fontSize: 12, bold: true, color: labelColor || PLUM,
  });
}

function chip(s, x, y, text, color) {
  const w = 0.16 + text.length * 0.072;
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: 0.24, rectRadius: 0.12,
    fill: { color: color, transparency: 88 }, line: { color: color, width: 0.75 },
  });
  s.addText(text, {
    x, y, w, h: 0.24, margin: 0, align: "center", valign: "middle",
    fontFace: SANS, fontSize: 8, bold: true, color: color, charSpacing: 0.6,
  });
  return w;
}

function card(s, x, y, w, h) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.06,
    fill: { color: CARD }, line: { color: RULE, width: 0.75 },
  });
}

// ============================================================
// 1 — TITLE
// ============================================================
{
  const s = darkSlide();
  // decorative concentric rings (circle motif), muted so they sit behind
  s.addShape(pres.ShapeType.ellipse, { x: 9.15, y: 0.55, w: 4.6, h: 4.6, fill: { type: "none" }, line: { color: GOLD_D, width: 1.25 } });
  s.addShape(pres.ShapeType.ellipse, { x: 10.05, y: 1.45, w: 4.6, h: 4.6, fill: { type: "none" }, line: { color: GOLD_D, width: 1.25 } });
  s.addShape(pres.ShapeType.ellipse, { x: 8.25, y: 1.45, w: 4.6, h: 4.6, fill: { type: "none" }, line: { color: GOLD_D, width: 1.25 } });

  s.addText("TOUR CONCEPT DECK  ·  WORKING DRAFT", {
    x: M, y: 1.95, w: 8.2, h: 0.3, margin: 0,
    fontFace: SANS, fontSize: 11, bold: true, color: GOLD, charSpacing: 3.2,
  });
  s.addText("DETTY\nDECEMBER", {
    x: M, y: 2.32, w: 8.2, h: 2.0, margin: 0, lineSpacing: 52,
    fontFace: HEAD, fontSize: 54, bold: true, color: WHITE,
  });
  s.addText("Fourteen titleholders and public figures, three countries, one December.", {
    x: M, y: 4.5, w: 7.4, h: 0.4, margin: 0,
    fontFace: SANS, fontSize: 15.5, color: "E4D6DE",
  });
  s.addText("26 DECEMBER  –  10 JANUARY   (estimative)", {
    x: M, y: 5.05, w: 7.4, h: 0.3, margin: 0,
    fontFace: SANS, fontSize: 12, bold: true, color: GOLD_L, charSpacing: 1.4,
  });

  const foot = [
    { t: "CÔTE D'IVOIRE", c: CI }, { t: "GHANA", c: GH }, { t: "NIGERIA", c: NG },
  ];
  foot.forEach((f, i) => {
    s.addShape(pres.ShapeType.ellipse, { x: M + i * 2.15, y: 6.19, w: 0.13, h: 0.13, fill: { color: f.c } });
    s.addText(f.t, {
      x: M + 0.24 + i * 2.15, y: 6.08, w: 1.9, h: 0.34, margin: 0, valign: "middle",
      fontFace: SANS, fontSize: 10.5, bold: true, color: "C9B6C2", charSpacing: 1.2,
    });
  });

  s.addNotes("Working draft. Concept is not yet signed off — see slide 2. Nothing in this deck should go to sponsors or talent until the flags on slide 8 are resolved.");
}

// ============================================================
// 2 — THE CONCEPT (established vs. open)
// ============================================================
{
  const s = lightSlide();
  head(s, "WHERE WE ACTUALLY ARE", "The concept is not yet locked",
    "Everything below the line needs answering with Olivia before this deck goes anywhere near a sponsor or a talent call.");

  const colW = (CW - 0.34) / 2;

  // LEFT — established
  s.addText("ESTABLISHED", {
    x: M, y: 2.02, w: colW, h: 0.26, margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: OK, charSpacing: 2,
  });
  card(s, M, 2.34, colW, 3.62);
  const est = [
    "Three host countries — Côte d'Ivoire, Ghana, Nigeria",
    "Arrival in Abidjan 26 Dec; Mother Africa Festival 27–28 Dec is the opening anchor",
    "Roughly 26 Dec – 10 Jan, ending in Nigeria",
    "All-female lineup of titleholders and public figures",
    "A social-impact / foundation action in each country",
    "Private jet air legs, vans and Escalades on the ground",
    "No plus-ones — talent travel solo",
    "Individual calls with each woman before anything is signed",
  ];
  s.addText(est.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i !== est.length - 1 } })), {
    x: M + 0.28, y: 2.54, w: colW - 0.56, h: 3.24, margin: 0, valign: "top",
    fontFace: SANS, fontSize: 11.5, color: BODY, paraSpaceAfter: 8, lineSpacing: 15,
  });

  // RIGHT — open
  const rx = M + colW + 0.34;
  s.addText("OPEN — DECIDE WITH OLIVIA", {
    x: rx, y: 2.02, w: colW, h: 0.26, margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: CRIT, charSpacing: 2,
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: rx, y: 2.34, w: colW, h: 3.62, rectRadius: 0.06,
    fill: { color: "FBF1F1" }, line: { color: "E8CFCF", width: 0.75 },
  });
  const open = [
    "The core purpose — celebration, tourism promotion, philanthropy, or a commercial content property?",
    "Whose trip is this — Olivia and Dorcas's initiative we execute, or our concept they host?",
    "What “Minister of Enjoyment” means in practice: curation, sign-off, public fronting?",
    "Who funds it, and is our fee flat or tied to sponsorship?",
    "Is the foundation piece core identity or a secondary activation?",
    "Ghana cities and dates — the one fully open leg",
    "Does NYE land in Abidjan or Lagos?",
    "Is this a documented trip, or a media property that travels?",
  ];
  s.addText(open.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i !== open.length - 1 } })), {
    x: rx + 0.28, y: 2.54, w: colW - 0.56, h: 3.24, margin: 0, valign: "top",
    fontFace: SANS, fontSize: 11.5, color: BODY, paraSpaceAfter: 8, lineSpacing: 15,
  });

  s.addText("Until the left column and the right column agree, the itinerary, the sponsor deck and the talent contracts are all built on an assumption.", {
    x: M, y: 6.24, w: CW, h: 0.4, margin: 0,
    fontFace: SANS, fontSize: 11.5, italic: true, color: MUTED,
  });
  s.addNotes("This is the slide to open the Olivia call with. Do not move to itinerary until the right column is answered.");
}

// ============================================================
// 3 — ROUTE
// ============================================================
{
  const s = lightSlide();
  head(s, "SHAPE OF THE TOUR", "Route and approximate dates",
    "Sixteen days, three countries, two confirmed anchors. Ghana is the open leg.");

  const stops = [
    { d: "DEC 26",     t: "Arrival — Abidjan",        n: "Everyone lands. Rest day before the festival.", c: CI, conf: "CONFIRMED" },
    { d: "DEC 27–28",  t: "Mother Africa Festival",   n: "Marcory Zone 4. 4th edition, ~40,000 attendees. Olivia is already publicly linked to it.", c: CI, conf: "CONFIRMED" },
    { d: "DEC 29–31",  t: "Assinie · Sassandra · Yamoussoukro", n: "Beach and heritage legs. Abidjan has a confirmed NYE fireworks anchor if NYE stays here.", c: CI, conf: "DRAFT" },
    { d: "EARLY JAN",  t: "Ghana",                    n: "Cities and dates not yet chosen. Season runs under the government's “December in GH” programme.", c: GH, conf: "OPEN" },
    { d: "TO JAN 10",  t: "Lagos and Abuja",          n: "New Year's and a birthday. The most event-dense leg of the three.", c: NG, conf: "DRAFT" },
  ];

  let y = 2.16;
  const rowH = 0.92;
  stops.forEach((st, i) => {
    // connector
    if (i < stops.length - 1) {
      s.addShape(pres.ShapeType.line, {
        x: M + 1.72, y: y + 0.34, w: 0, h: rowH,
        line: { color: RULE, width: 1.25 },
      });
    }
    s.addText(st.d, {
      x: M, y: y + 0.06, w: 1.5, h: 0.3, margin: 0, align: "right",
      fontFace: SANS, fontSize: 11, bold: true, color: st.c, charSpacing: 0.8,
    });
    s.addShape(pres.ShapeType.ellipse, { x: M + 1.63, y: y + 0.11, w: 0.19, h: 0.19, fill: { color: st.c } });
    s.addText(st.t, {
      x: M + 2.02, y: y, w: 4.0, h: 0.32, margin: 0,
      fontFace: HEAD, fontSize: 15, bold: true, color: PLUM,
    });
    s.addText(st.n, {
      x: M + 6.15, y: y + 0.02, w: CW - 6.15 - 1.15, h: 0.68, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10.5, color: MUTED, lineSpacing: 13,
    });
    const cc = st.conf === "CONFIRMED" ? OK : st.conf === "OPEN" ? CRIT : WARN;
    chip(s, W - M - 1.02, y + 0.04, st.conf, cc);
    y += rowH;
  });

  s.addNotes("Confirmed = date and venue are real and verified. Draft = we intend it but nothing is booked. Open = not yet decided at all.");
}

// ============================================================
// 4 — ROSTER AT A GLANCE
// ============================================================
{
  const s = darkSlide();
  s.addText("THE LINE-UP", {
    x: M, y: 0.62, w: CW, h: 0.28, margin: 0,
    fontFace: SANS, fontSize: 10.5, bold: true, color: GOLD, charSpacing: 2.6,
  });
  s.addText("Fourteen names on the list", {
    x: M, y: 0.94, w: CW, h: 0.6, margin: 0,
    fontFace: HEAD, fontSize: 33, bold: true, color: WHITE,
  });
  s.addText("On the list — not yet confirmed as attending. Reach figures are estimates from public sources, not media kits.", {
    x: M, y: 1.58, w: 9.4, h: 0.4, margin: 0,
    fontFace: SANS, fontSize: 12.5, color: "C9B6C2",
  });

  const stats = [
    { n: "14",     l: "NAMES ON THE LIST",           s2: "11 with a confirmed title" },
    { n: "~6.1M",  l: "COMBINED INSTAGRAM REACH",    s2: "estimated, unverified" },
    { n: "~1.4M",  l: "COMBINED TIKTOK REACH",       s2: "where an account was found" },
    { n: "11",     l: "NATIONALITIES & TERRITORIES", s2: "one still unidentified" },
  ];
  const sw = (CW - 0.45) / 4;
  stats.forEach((st, i) => {
    const x = M + i * (sw + 0.15);
    s.addShape(pres.ShapeType.roundRect, {
      x, y: 2.5, w: sw, h: 2.62, rectRadius: 0.06,
      fill: { color: PLUM_D }, line: { color: "45283C", width: 0.75 },
    });
    s.addText(st.n, {
      x: x + 0.24, y: 2.82, w: sw - 0.48, h: 0.94, margin: 0,
      fontFace: HEAD, fontSize: 44, bold: true, color: GOLD_L,
    });
    s.addText(st.l, {
      x: x + 0.24, y: 3.86, w: sw - 0.48, h: 0.46, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10, bold: true, color: WHITE, charSpacing: 1.1, lineSpacing: 12,
    });
    s.addText(st.s2, {
      x: x + 0.24, y: 4.62, w: sw - 0.48, h: 0.28, margin: 0,
      fontFace: SANS, fontSize: 9.5, italic: true, color: "9E8794",
    });
  });

  s.addText("Real engagement rate and audience demographics are not public on any platform. They live in each woman's private Insights dashboard — the only way to get them is to request her official media kit during the individual calls.", {
    x: M, y: 5.52, w: CW - 0.4, h: 0.8, margin: 0, valign: "top",
    fontFace: SANS, fontSize: 12, color: "C9B6C2", lineSpacing: 17,
  });
  s.addNotes("If a sponsor asks for demographic data, the honest answer is that we are collecting media kits — do not present estimated follower counts as analytics.");
}

// ============================================================
// 5–7 — ROSTER CARDS
// ============================================================
const roster = [
  { n: "Olivia Yacé",               nat: "CÔTE D'IVOIRE", t: "Miss Côte d'Ivoire 2021 · 4th RU, Miss Universe 2025", ig: "~1M",       o: "TikTok ~934K · FB ~756K", st: "warn", stl: "VERIFY TITLE" },
  { n: "Veena Praveenar Singh",     nat: "THAILAND",      t: "Miss Universe Thailand 2025 · 1st RU, Miss Universe 2025", ig: "~2M",   o: "TikTok active",           st: "warn", stl: "CORRECTED" },
  { n: "Isabella Menin",            nat: "BRAZIL",        t: "Miss Grand International 2022",                    ig: "~1.05M",   o: "No other platform found", st: "ok",   stl: "CONFIRMED" },
  { n: "Nadia Mejia",               nat: "ECUADOR / USA", t: "Miss Universe Ecuador 2025 · Miss California USA 2016", ig: "~435K", o: "TikTok ~125K",            st: "warn", stl: "CORRECTED" },
  { n: "Alicia Aylies",             nat: "FRENCH GUIANA", t: "Miss France 2017",                                 ig: "~423K",    o: "TikTok ~148K · FB ~78K",  st: "ok",   stl: "CONFIRMED" },

  { n: "Angélique Angarni-Filopon", nat: "MARTINIQUE",    t: "Miss France 2025 — first Martinican winner",        ig: "~395K",    o: "No personal TikTok",      st: "warn", stl: "CORRECTED" },
  { n: "Rebecca Biangue",           nat: "FRANCE",        t: "Beauty & lifestyle creator — no title found",       ig: "~220K",    o: "TikTok ~43K",             st: "crit", stl: "NO TITLE" },
  { n: "Dorcas Dienda",             nat: "DR CONGO",      t: "Miss Africa 2019 · Miss Universe DR Congo 2025",    ig: "~216K",    o: "TikTok active",           st: "ok",   stl: "CONFIRMED" },
  { n: "Ophély Mézino",             nat: "GUADELOUPE",    t: "Miss World 2019 1st RU · Miss Universe Guadeloupe 2025", ig: "~141K", o: "TikTok ~35K · FB ~20K", st: "ok",   stl: "CONFIRMED" },
  { n: "Nellie Anjaratiana",        nat: "MADAGASCAR",    t: "Miss Madagascar 2020 · Top 40, Miss World",         ig: "~80K",     o: "Facebook ~105K",          st: "ok",   stl: "CONFIRMED" },

  { n: "Sephora Kongo",             nat: "DR CONGO",      t: "Fashion & lifestyle influencer — no title found",   ig: "~73K",     o: "TikTok ~39K",             st: "crit", stl: "NO TITLE" },
  { n: "“Tai”",           nat: "UNKNOWN",       t: "No name, nationality or credentials found",         ig: "~43–63K",  o: "No other platform found", st: "crit", stl: "UNIDENTIFIED" },
  { n: "Khaiza Kuyo",               nat: "CÔTE D'IVOIRE", t: "Actress, Ivorian series “Isabelle” — no title found", ig: "~33K", o: "TikTok ~57K",       st: "crit", stl: "NO TITLE" },
  { n: "Bella Zabaneh",             nat: "BELIZE",        t: "Miss Universe Belize 2025",                         ig: "~23K",     o: "TikTok ~22K",             st: "ok",   stl: "CONFIRMED" },
];

function rosterSlide(items, idx, total) {
  const s = lightSlide();
  head(s, `THE LINE-UP  ·  ${idx} OF ${total}`, "Who is on the list",
    "Ordered by Instagram reach. Drop cleared photographs into the circles — do not use images we have not licensed.");

  const n = items.length;
  const gap = 0.2;
  const cw = (CW - gap * 4) / 5;
  items.forEach((p, i) => {
    const x = M + i * (cw + gap);
    const y = 2.16;
    const cardH = 4.38;
    card(s, x, y, cw, cardH);

    // circular photo frame — the motif
    const d = 1.42;
    const cx = x + (cw - d) / 2;
    s.addShape(pres.ShapeType.ellipse, {
      x: cx, y: y + 0.26, w: d, h: d,
      fill: { color: "EBE3E9" }, line: { color: GOLD, width: 1.5 },
    });
    s.addText("ADD\nPHOTO", {
      x: cx, y: y + 0.26, w: d, h: d, margin: 0, align: "center", valign: "middle",
      fontFace: SANS, fontSize: 8, bold: true, color: "A2929C", charSpacing: 1, lineSpacing: 10,
    });

    s.addText(p.n, {
      x: x + 0.16, y: y + 1.82, w: cw - 0.32, h: 0.62, margin: 0, align: "center", valign: "top",
      fontFace: HEAD, fontSize: 13, bold: true, color: PLUM, lineSpacing: 15,
    });
    s.addText(p.nat, {
      x: x + 0.14, y: y + 2.42, w: cw - 0.28, h: 0.24, margin: 0, align: "center",
      fontFace: SANS, fontSize: 8, bold: true, color: MUTED, charSpacing: 1.1,
    });
    s.addText(p.t, {
      x: x + 0.16, y: y + 2.72, w: cw - 0.32, h: 0.78, margin: 0, align: "center", valign: "top",
      fontFace: SANS, fontSize: 9.5, color: BODY, lineSpacing: 11.5,
    });
    s.addText(`IG ${p.ig}`, {
      x: x + 0.16, y: y + 3.46, w: cw - 0.32, h: 0.26, margin: 0, align: "center",
      fontFace: SANS, fontSize: 11, bold: true, color: GOLD,
    });
    s.addText(p.o, {
      x: x + 0.12, y: y + 3.7, w: cw - 0.24, h: 0.22, margin: 0, align: "center",
      fontFace: SANS, fontSize: 8, color: MUTED,
    });

    const cc = p.st === "ok" ? OK : p.st === "warn" ? WARN : CRIT;
    const chw = 0.16 + p.stl.length * 0.072;
    chip(s, x + (cw - chw) / 2, y + 3.98, p.stl, cc);
  });

  s.addText("Follower figures are approximate, from public search — verify against each media kit before any of this reaches a sponsor.", {
    x: M, y: 6.74, w: CW, h: 0.3, margin: 0,
    fontFace: SANS, fontSize: 10, italic: true, color: MUTED,
  });
  return s;
}
rosterSlide(roster.slice(0, 5), 1, 3);
rosterSlide(roster.slice(5, 10), 2, 3);
rosterSlide(roster.slice(10, 14), 3, 3);

// ============================================================
// 8 — FLAGS
// ============================================================
{
  const s = lightSlide();
  head(s, "BEFORE ANYTHING IS SENT", "Seven corrections to the original list",
    "These came out of verifying every name against public record. Resolve them with whoever wrote the original notes.");

  const flags = [
    { sev: "crit", h: "Two titles were swapped",            b: "Veena Praveenar Singh is Miss Universe Thailand 2025 and 1st Runner-Up at Miss Universe 2025. Isabella Menin is Miss Grand International 2022. The original notes attached Isabella's title to Veena." },
    { sev: "crit", h: "Three names have no pageant title",  b: "Khaiza Kuyo, Rebecca Biangue and Sephora Kongo return no title in public search — actress, content creator and influencer respectively. Not a reason to drop them; a reason to fix how they are described." },
    { sev: "crit", h: "“Tai” is unidentified",    b: "An Instagram handle and nothing else — no name, nationality or credentials. Needs a direct answer from the source of the original note." },
    { sev: "crit", h: "“+1 Angelique” is ambiguous", b: "Either a second, different Angelique, or a stray reference back to Angélique Angarni-Filopon. Unresolved by research — do not guess." },
    { sev: "warn", h: "Angélique's title year is wrong",    b: "Miss France 2025, not 2019. First Martinican winner and the oldest woman ever crowned — both worth using in promotion." },
    { sev: "warn", h: "Olivia's affiliation changed",       b: "She resigned the Miss Universe Africa & Oceania title on 24 November 2025, keeping Miss Côte d'Ivoire. Confirm her status before any Miss Universe branded material." },
    { sev: "warn", h: "Nadia Mejia is not the singer",      b: "This is Nadia Grace Eicher Mejía-Webb, Miss Universe Ecuador 2025 — not the Chilean singer of the same name, in case that was the intent." },
  ];

  const colW = (CW - 0.3) / 2;
  flags.forEach((f, i) => {
    const col = i < 4 ? 0 : 1;
    const row = i < 4 ? i : i - 4;
    const x = M + col * (colW + 0.3);
    const y = 2.06 + row * 1.16;
    const c = f.sev === "crit" ? CRIT : WARN;
    goldDot(s, x, y + 0.04, 0.3, String(i + 1), PLUM);
    s.addText(f.h, {
      x: x + 0.44, y: y, w: colW - 0.44, h: 0.28, margin: 0,
      fontFace: HEAD, fontSize: 13.5, bold: true, color: c,
    });
    s.addText(f.b, {
      x: x + 0.44, y: y + 0.3, w: colW - 0.5, h: 0.8, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10.5, color: BODY, lineSpacing: 13,
    });
  });

  s.addNotes("Items 1-4 are blocking — nothing outbound until they are answered. Items 5-7 are factual corrections we can make ourselves.");
}

// ============================================================
// 9–11 — COUNTRY LEGS
// ============================================================
function legSlide(cfg) {
  const s = lightSlide();
  head(s, cfg.eyebrow, cfg.title, cfg.sub);

  const colW = (CW - 0.6) / 3;
  cfg.cols.forEach((col, i) => {
    const x = M + i * (colW + 0.3);
    s.addShape(pres.ShapeType.ellipse, { x, y: 2.16, w: 0.14, h: 0.14, fill: { color: cfg.c } });
    s.addText(col.h, {
      x: x + 0.24, y: 2.04, w: colW - 0.24, h: 0.34, margin: 0, valign: "middle",
      fontFace: SANS, fontSize: 10, bold: true, color: cfg.c, charSpacing: 1.8,
    });
    col.items.forEach((it, j) => {
      const y = 2.52 + j * 0.72;
      s.addText(it.n, {
        x, y, w: colW, h: 0.26, margin: 0,
        fontFace: HEAD, fontSize: 12, bold: true, color: PLUM,
      });
      s.addText(it.d, {
        x, y: y + 0.25, w: colW - 0.1, h: 0.46, margin: 0, valign: "top",
        fontFace: SANS, fontSize: 9.5, color: MUTED, lineSpacing: 11.5,
      });
    });
  });

  // watch box
  s.addShape(pres.ShapeType.roundRect, {
    x: M, y: 6.06, w: CW, h: 0.78, rectRadius: 0.06,
    fill: { color: "FBF1F1" }, line: { color: "E8CFCF", width: 0.75 },
  });
  s.addText("WATCH", {
    x: M + 0.24, y: 6.24, w: 0.8, h: 0.26, margin: 0,
    fontFace: SANS, fontSize: 9, bold: true, color: CRIT, charSpacing: 1.4,
  });
  s.addText(cfg.watch, {
    x: M + 1.06, y: 6.16, w: CW - 1.34, h: 0.6, margin: 0, valign: "middle",
    fontFace: SANS, fontSize: 10.5, color: BODY, lineSpacing: 13,
  });
  return s;
}

legSlide({
  eyebrow: "LEG ONE  ·  26–31 DECEMBER", title: "Côte d'Ivoire", c: CI,
  sub: "Abidjan, Assinie, Sassandra, Yamoussoukro. The strongest leg on paper — one confirmed anchor and an existing talent relationship.",
  cols: [
    { h: "EVENTS", items: [
      { n: "Mother Africa Festival", d: "27–28 Dec, Marcory Zone 4. ~40,000 attendees, 4th edition. Founder: Kimany Tayoro." },
      { n: "NYE fireworks", d: "31 Dec, Général de Gaulle bridge over the Ebrié Lagoon. Free, city-wide, PM in attendance." },
      { n: "Sofitel Réveillon gala", d: "31 Dec, Congress Palace. Past editions featured Magic System live." },
      { n: "Nahiko, Assinie", d: "Smaller lagoon-side NYE dinner — the VIP alternative to Abidjan." },
    ]},
    { h: "SPONSOR TARGETS", items: [
      { n: "Orange Côte d'Ivoire", d: "Runs a formal sponsorship programme — sponsors events as policy." },
      { n: "Air Côte d'Ivoire", d: "AFCON 2023 official carrier; backed the Children of Africa gala via the First Lady's office." },
      { n: "Solibra", d: "Ivorian since 1955, FEMUA sponsor history, marking its 70th anniversary." },
      { n: "Brassivoire", d: "Heineken/CFAO joint venture, runs its own brand events in Abidjan." },
    ]},
    { h: "PARTNERS & LOGISTICS", items: [
      { n: "La Sunday", d: "Abidjan's signature day-party brand, 6,000+ attendees on the lagoon." },
      { n: "Ivory Jet Services", d: "New Abidjan base, European AOC, Falcon and Legacy aircraft. Matches the charter in the brief." },
      { n: "Sofitel · Radisson Blu · Hôtel Président", d: "Assinie boutique: Nahiko, Maison d'Akoula, Key 19." },
      { n: "Monbolide · WINO · Auto Ivoire", d: "Chauffeur fleets. Sedan ~55–70k FCFA/day, SUV ~80–120k." },
    ]},
  ],
  watch: "Grand-Bassam's beaches were closed on 30 December last year after an oil spill, reopening under restrictions from 1 January. If a Bassam beach day stays on the route, check live status before committing.",
});

legSlide({
  eyebrow: "LEG TWO  ·  EARLY JANUARY", title: "Ghana", c: GH,
  sub: "Cities and dates still open. The whole season runs under a government programme — that is the fastest way in.",
  cols: [
    { h: "EVENTS", items: [
      { n: "“December in GH”", d: "Government programme, 1 Dec – 3 Jan, run by the Ghana Tourism Authority. Open call for event partners." },
      { n: "AfroFuture Fest", d: "~27–29 Dec, El Wak Stadium. ~31,000 attendees. Run by Culture Management Group." },
      { n: "Detty Rave", d: "~27 Dec, Untamed Empire. Mr Eazi's event — the biggest celebrity draw on the calendar." },
      { n: "Polo Beach Club NYE", d: "31 Dec, Labadi. Tiers from ₵500 to ₵70,000 — a useful VIP pricing benchmark." },
    ]},
    { h: "SPONSOR TARGETS", items: [
      { n: "Ghana Tourism Authority", d: "Runs the season and takes partner proposals. Also the route to Miss Diaspora Ghana." },
      { n: "MTN Ghana", d: "Deep concert sponsorship history, plus a foundation — sponsor and impact partner in one." },
      { n: "AirtelTigo", d: "First operator to launch eSIM in Ghana — direct fit for a connectivity deal." },
      { n: "Guinness Ghana · Kasapreko", d: "Dominant beverage players. No confirmed festival tie-in — needs direct outreach." },
    ]},
    { h: "PARTNERS & LOGISTICS", items: [
      { n: "Culture Management Group", d: "The most internationally professionalised producer in the market." },
      { n: "McDan Aviation", d: "Ghana's dominant private-jet terminal at Kotoka. 2025 Aviation Company of the Year." },
      { n: "Kempinski · Labadi Beach · Mövenpick", d: "The standard luxury shortlist for high-end Accra groups." },
      { n: "SOS Children's Villages Ghana", d: "11 locations since 1974 — the most credible foundation partner found." },
    ]},
  ],
  watch: "No 2026 dates are published yet for AfroFuture, Detty Rave, Afro Nation or the December concerts — they typically drop in September and October. Everything above is last season's pattern. Cape Coast is confirmed weak for December nightlife: treat it as a daytime heritage stop only.",
});

legSlide({
  eyebrow: "LEG THREE  ·  NEW YEAR TO 10 JANUARY", title: "Nigeria", c: NG,
  sub: "Lagos and Abuja. The most event-dense leg, and the only one with confirmed active sponsors in the space.",
  cols: [
    { h: "EVENTS", items: [
      { n: "Flytime Fest", d: "21–25 Dec, Eko Convention Centre. 21 years running; Davido closed the 2025 edition." },
      { n: "Livespot Detty December Fest", d: "6–31 Dec. Co-produced with the Federal Ministry of Arts and Culture." },
      { n: "Abuja Groovy December", d: "15–31 Dec, Moshood Abiola Stadium. Includes a “Miss Groovy December” pageant." },
      { n: "Transcorp Hilton Abuja", d: "Runs its own NYE gala and a New Year's Day show — a turnkey Abuja venue partner." },
    ]},
    { h: "SPONSOR TARGETS", items: [
      { n: "Wema Bank (ALAT)", d: "Confirmed headline Detty December sponsor last season; also backed Davido's tour." },
      { n: "Martell · Guinness · Hennessy", d: "All three ran confirmed premium activations. Hennessy owns its own event property." },
      { n: "MTN · Airtel · Glo", d: "Heavy festive-data marketing. No confirmed festival deal — strong pitch targets." },
      { n: "Eko Hotels & Suites", d: "Runs its own December festival property; GM speaks publicly on Detty December." },
    ]},
    { h: "PARTNERS & LOGISTICS", items: [
      { n: "Livespot360", d: "The dominant producer, government-endorsed, led by Deola Art Alade. Prior Cardi B booking." },
      { n: "ExecuJet Africa", d: "Major FBO at Murtala Muhammed; hangar rated to Boeing Business Jet size." },
      { n: "Zeniks · Abuja Car Rental Express", d: "Motorcade and escort options; armoured vehicles available in Abuja." },
      { n: "Wellbeing Foundation Africa", d: "Founded by Toyin Ojora Saraki. Maternal and child health — pairs well with the birthday." },
    ]},
  ],
  watch: "Lagos State's own free New Year's flagship was cancelled hours before kickoff on 31 December last year, with no reason given, after running annually since 2012. Do not anchor the NYE plan on it until 2026 status is confirmed.",
});

// ============================================================
// 12 — CONTENT MODEL
// ============================================================
{
  const s = lightSlide();
  head(s, "THE DECISION THAT SIZES THE CREW", "What kind of content is this",
    "This changes crew, budget and timeline more than any other choice. It should be settled at concept stage, not once cameras are already on the ground.");

  const opts = [
    { k: "A", n: "Highlight reel", c: MUTED,
      d: "One videographer shooting coverage and behind-the-scenes, cut into a 3–5 minute recap with social versions after the trip.",
      crew: "Crew: 1–2 — matches the current sheet",
      pro: "Cheap, fast, low risk.",
      con: "Gives sponsors nothing sustained, and badly undersells the story." },
    { k: "B", n: "Social-first + episodic", c: OK, rec: true,
      d: "Daily short-form posted live for reach, same footage banked and cut into three long-form episodes — one per country — after the trip.",
      crew: "Crew: 1–2 videographers, photographer, on-trip editor, post editor",
      pro: "Content flows during the tour when sponsors need visibility, and still yields a polished asset.",
      con: "Needs a slightly bigger crew than currently budgeted." },
    { k: "C", n: "Full documentary series", c: CRIT,
      d: "Two episodes per country. A director, DP, sound, second camera, drone, colourist and story editor, with a narrative arc built in advance.",
      crew: "Crew: full production team + months of post",
      pro: "The most valuable long-term asset, and a genuinely strong story.",
      con: "A separate project with its own producer, budget and distribution plan. Not an add-on." },
  ];

  const cw = (CW - 0.6) / 3;
  opts.forEach((o, i) => {
    const x = M + i * (cw + 0.3);
    const y = 2.2;
    const h = 3.82;
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w: cw, h, rectRadius: 0.06,
      fill: { color: o.rec ? "F1F6F2" : CARD },
      line: { color: o.rec ? "BFD8C4" : RULE, width: o.rec ? 1.25 : 0.75 },
    });
    goldDot(s, x + 0.26, y + 0.26, 0.36, o.k, PLUM);
    s.addText(o.n, {
      x: x + 0.72, y: y + 0.26, w: cw - 0.96, h: 0.36, margin: 0, valign: "middle",
      fontFace: HEAD, fontSize: 15, bold: true, color: PLUM,
    });
    s.addText(o.d, {
      x: x + 0.26, y: y + 0.78, w: cw - 0.52, h: 0.94, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10.5, color: BODY, lineSpacing: 13,
    });
    s.addText(o.crew, {
      x: x + 0.26, y: y + 1.74, w: cw - 0.52, h: 0.4, margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: o.c, lineSpacing: 11.5,
    });
    s.addText("+   " + o.pro, {
      x: x + 0.26, y: y + 2.2, w: cw - 0.52, h: 0.62, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10, color: BODY, lineSpacing: 12.5,
    });
    s.addText("−   " + o.con, {
      x: x + 0.26, y: y + 2.86, w: cw - 0.52, h: 0.62, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10, color: MUTED, lineSpacing: 12.5,
    });
    if (o.rec) chip(s, x + 0.26, y + 3.44, "RECOMMENDED", OK);
  });

  s.addText("Recommendation: shoot at documentary quality — multi-camera on the big moments — but only commit to three episodes now. That keeps option C open later without having under-shot the first time.", {
    x: M, y: 6.22, w: CW - 0.3, h: 0.5, margin: 0,
    fontFace: SANS, fontSize: 11.5, italic: true, color: BODY, lineSpacing: 14,
  });
  s.addNotes("Running a full reality-series production inside a 16-day, three-country, festival-hopping schedule with the crew currently on the sheet is the highest-risk path.");
}

// ============================================================
// 13 — SCOPE
// ============================================================
{
  const s = lightSlide();
  head(s, "WHAT THE ROLE ACTUALLY COVERS", "Scope of work",
    "The brief named logistics, sponsorship, itinerary, negotiation and oversight. At this scale the role is closer to executive producer — here is the rest of it.");

  const groups = [
    { h: "NAMED IN THE BRIEF", c: PLUM, items: ["Tour logistics", "Sponsorship & partnership deals", "Itinerary management", "Negotiations with all parties", "General tour oversight"] },
    { h: "TALENT & DUTY OF CARE", c: CI, items: ["Talent contracts & appearance terms", "Rider management across 14 women", "Conflict resolution on the ground", "Media kit collection & distribution"] },
    { h: "LEGAL & RISK", c: GH, items: ["Waivers, insurance, medical cover", "Filming & work permits per country", "NDAs for sponsors and partners", "Force majeure & cancellation terms"] },
    { h: "IMMIGRATION", c: NG, items: ["Visa coordination, three countries", "Passport collection & tracking", "Documentation for private jet legs"] },
    { h: "SECURITY", c: CI, items: ["Advance planning & route recon", "Crisis communication protocol", "Local law enforcement liaison"] },
    { h: "FINANCE", c: GH, items: ["Master budget ownership", "Multi-currency cash flow — CFA, Cedi, Naira", "Vendor payment schedules & deposits"] },
    { h: "FOUNDATION PROGRAMME", c: NG, items: ["NGO vetting per country", "Gift & supply procurement", "Consent for filming beneficiaries", "Impact reporting for sponsors"] },
    { h: "CONTENT OPERATIONS", c: CI, items: ["Posting calendar & platform strategy", "Usage rights and ownership", "Press and media-day management"] },
    { h: "WRAP-UP", c: GH, items: ["Post-tour sponsor reporting deck", "Talent payment reconciliation", "Debrief and archive"] },
  ];

  const cw = (CW - 0.6) / 3;
  groups.forEach((g, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * (cw + 0.3);
    const y = 2.06 + row * 1.62;
    s.addShape(pres.ShapeType.ellipse, { x, y: 0.06 + y, w: 0.13, h: 0.13, fill: { color: g.c } });
    s.addText(g.h, {
      x: x + 0.22, y, w: cw - 0.22, h: 0.26, margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: g.c, charSpacing: 1.5,
    });
    s.addText(g.items.map((t, j) => ({ text: t, options: { bullet: true, breakLine: j !== g.items.length - 1 } })), {
      x: x + 0.22, y: y + 0.32, w: cw - 0.34, h: 1.18, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10, color: BODY, lineSpacing: 13, paraSpaceAfter: 3,
    });
  });
  s.addNotes("Worth confirming which of these the client assumes is ours versus theirs — particularly security hire and foundation programme management.");
}

// ============================================================
// 14 — ACTION STEPS
// ============================================================
{
  const s = lightSlide();
  head(s, "WHAT HAPPENS NEXT", "Action steps",
    "Four blocking items, then everything else can run in parallel.");

  s.addText("BLOCKING — THIS WEEK", {
    x: M, y: 2.02, w: 5.9, h: 0.26, margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: CRIT, charSpacing: 1.8,
  });
  const blocking = [
    { n: "Confirm the concept with Olivia", d: "Purpose, ownership, funding, and what “Minister of Enjoyment” means in practice." },
    { n: "Send the roster corrections", d: "Title swap, three untitled names, “Tai”, and the “+1 Angelique” ambiguity." },
    { n: "Lock Ghana cities and dates", d: "Hotels, sponsors and RSVPs there are all downstream of this." },
    { n: "Set the budget ceiling and paying client", d: "Sponsor pitches and vendor talks cannot really start without it." },
  ];
  blocking.forEach((b, i) => {
    const y = 2.4 + i * 0.94;
    goldDot(s, M, y, 0.32, String(i + 1), PLUM);
    s.addText(b.n, {
      x: M + 0.46, y: y - 0.02, w: 5.44, h: 0.3, margin: 0,
      fontFace: HEAD, fontSize: 13.5, bold: true, color: PLUM,
    });
    s.addText(b.d, {
      x: M + 0.46, y: y + 0.28, w: 5.4, h: 0.56, margin: 0, valign: "top",
      fontFace: SANS, fontSize: 10.5, color: MUTED, lineSpacing: 13,
    });
  });

  const rx = M + 6.5;
  s.addText("IN PARALLEL", {
    x: rx, y: 2.02, w: 5.6, h: 0.26, margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: OK, charSpacing: 1.8,
  });
  card(s, rx, 2.34, CW - 6.5, 3.86);
  const par = [
    "Individual calls with each woman — concept, availability, terms",
    "Collect handles, follower counts and official media kits",
    "Passport and visa documentation as confirmations land",
    "Olivia's local list: Mother Africa organiser, Bassam beach status, sponsor outreach, Côte d'Ivoire foundation partner",
    "Apply into Ghana Tourism Authority's “December in GH” partner process",
    "Confirm Lagos NYE flagship status for 2026",
    "Decide the content production model and size the crew",
    "Build sponsor decks once talent and route are locked",
    "Confirm head of security plus two, begin advance planning",
  ];
  s.addText(par.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i !== par.length - 1 } })), {
    x: rx + 0.28, y: 2.54, w: CW - 6.5 - 0.56, h: 3.48, margin: 0, valign: "top",
    fontFace: SANS, fontSize: 11, color: BODY, paraSpaceAfter: 7, lineSpacing: 14,
  });

  s.addText("Nothing outbound — no sponsor deck, no talent email — until items 1 and 2 are answered.", {
    x: M, y: 6.36, w: CW, h: 0.3, margin: 0,
    fontFace: SANS, fontSize: 11.5, bold: true, italic: true, color: CRIT,
  });
}

// ============================================================
// 15 — CLOSING
// ============================================================
{
  const s = darkSlide();
  s.addShape(pres.ShapeType.ellipse, { x: -1.5, y: 2.1, w: 5.2, h: 5.2, fill: { type: "none" }, line: { color: GOLD_D, width: 1.25 } });
  s.addShape(pres.ShapeType.ellipse, { x: 10.6, y: -1.2, w: 5.2, h: 5.2, fill: { type: "none" }, line: { color: GOLD_D, width: 1.25 } });

  s.addText("THE ONE THING TO SETTLE FIRST", {
    x: 2.3, y: 2.62, w: 8.7, h: 0.3, margin: 0, align: "center",
    fontFace: SANS, fontSize: 10.5, bold: true, color: GOLD, charSpacing: 3,
  });
  s.addText("What is this trip actually for?", {
    x: 1.9, y: 3.08, w: 9.5, h: 0.9, margin: 0, align: "center",
    fontFace: HEAD, fontSize: 38, bold: true, color: WHITE,
  });
  s.addText("Celebration, tourism promotion, philanthropy, or a commercial content property. They are not mutually exclusive — but one of them has to be the organising idea that the itinerary, the sponsors and the fourteen individual conversations are all built to serve.", {
    x: 2.5, y: 4.16, w: 8.3, h: 1.1, margin: 0, align: "center", valign: "top",
    fontFace: SANS, fontSize: 13, color: "C9B6C2", lineSpacing: 19,
  });
  s.addText("Answer it with Olivia, and everything else in this deck becomes a scheduling problem.", {
    x: 2.5, y: 5.44, w: 8.3, h: 0.4, margin: 0, align: "center",
    fontFace: SANS, fontSize: 12, italic: true, color: GOLD_L,
  });
}

pres.writeFile({ fileName: "/home/user/Detty-December/deck/Detty-December-Concept-Deck.pptx" })
  .then(f => console.log("wrote", f));
