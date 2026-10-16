"""v13 -> v14: turn the partner deck into a sponsorship deck.

This one patches the built HTML rather than regenerating it. The source assets
(portraits, brand marks, the Drive photography, the route map) are gitignored
and no longer on disk, so build_deck13.py cannot be re-run. Everything below is
expressed against the markup build_deck13.py emits, and every substitution is
asserted before anything is written.

    python3 deck/patch_v13_to_v14.py bbb-deck-v13.html bbb-deck-v14.html

Changes
  p2   the line about participants paying their own flights to Abidjan is cut;
       "Countries" becomes "Prospective countries"; the "Who delivers it" block
       is removed, leaving four detail blocks laid out two by two
  p3   NEW - the three pillars: tourism, entertainment, social impact, each
       carrying the kind of partner it speaks to
  p9   "Filmed" becomes "The visibility": owned, made and earned, led by their
       numbers, keeping both photographs
  p10  contact and the photography credit fold into the offer page
  --   the budget and next-steps page is removed; no euro figure survives
"""
import re
import sys

PIL3_CSS = """
    .pil3{display:grid;grid-template-columns:repeat(3,1fr);gap:3.4cqw;align-items:start;}
    .pil3 .p3{padding-top:.9cqw;border-top:2px solid var(--ink);}
    .pil3 .p3 i{display:block;font:300 2.9cqw/1 'Fraunces';font-style:normal;color:var(--accent);
     letter-spacing:-.02em;}
    .pil3 .p3 b{display:block;margin-top:.45cqw;font:400 1.9cqw/1.12 'Fraunces';color:var(--ink);}
    .pil3 .p3 span{display:block;margin-top:.7cqw;font:300 1.02cqw/1.5 'Karla';color:var(--muted);}
    .pil3 .p3 em{display:block;margin-top:.8cqw;padding-top:.55cqw;border-top:1px solid var(--rule);
     font:600 .82cqw/1.4 'Karla';font-style:normal;letter-spacing:.14em;text-transform:uppercase;
     color:var(--ink);}"""

PILLARS = """<section class="s">
    <div class="pad" style="padding-bottom:5.4cqw;">
      <div class="rh"><div class="lab">The goal</div><div class="lab">Three pillars</div></div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:4cqw;align-items:baseline;margin-top:1.2cqw;">
        <h2 style="font-size:2.9cqw;max-width:18ch;">Put West Africa's December in front of an
          audience that has never seen it.</h2>
        <p style="max-width:64ch;">Ten women who already hold that audience spend the busiest month
          of the regional calendar inside it. Everything the tour does sits under one of three
          pillars, and a partner can take one of them or stand across all three.</p>
      </div>
      <div class="pil3" style="margin-top:2.4cqw;">
        <div class="p3"><i>01</i><b>Tourism</b>
          <span>Four prospective countries filmed and posted as destinations rather than as
          backdrops. The cities, the coast, the heritage quarters and the people who run them,
          carried into ten markets by visitors rather than by advertising, and kept afterwards as
          a rights cleared archive.</span>
          <em>Destination and travel partners</em></div>
        <div class="p3"><i>02</i><b>Entertainment</b>
          <span>December is the month the diaspora comes home and the regional calendar is at its
          fullest. The delegation arrives inside an audience that is already there, at the concerts,
          the festivals and the nights that define the season, rather than building one from
          nothing.</span>
          <em>Consumer and lifestyle partners</em></div>
        <div class="p3"><i>03</i><b>Social impact</b>
          <span>The Fondation Olivia Yacé leads the programme in Côte d'Ivoire and partners with an
          in-country foundation in each other territory, on initiatives that may differ from its own
          but align with its principles. It is what makes this a delegation and not a
          holiday.</span>
          <em>Named across every pillar</em></div>
      </div>
      <div class="obar" style="margin-top:auto;">
        <b>One audience, three reasons to be in front of it.</b>
        <span>A destination partner buys the first and a consumer brand the second. The third is
          what makes either of them worth announcing.</span>
      </div>
    </div>
    <div class="fol"><span>Three pillars</span><span>03</span></div>
  </section>"""

VISIBILITY = """<section class="s">
    <div class="pad" style="padding-bottom:5.4cqw;">
      <div class="rh"><div class="lab">The visibility</div><div class="lab">Where a partner appears</div></div>
      <div style="display:grid;grid-template-columns:auto 1fr;gap:4cqw;align-items:baseline;margin-top:1.2cqw;">
        <h2 style="font-size:2.6cqw;max-width:17ch;">Three places a partner is seen.</h2>
        <p style="max-width:62ch;">Channels the delegation already owns, content made on the ground
          every day of the tour, and the press that follows it. A partner appears in all three and
          holds its category alone.</p>
      </div>
      <div class="figs4" style="grid-template-columns:repeat(3,1fr);gap:4cqw;margin-top:2cqw;">
        <div class="f"><b style="font-size:4.6cqw;">15M</b><i></i><em>Owned</em>
          <span>The delegation's own channels across Instagram, TikTok and Facebook, in ten
          countries of origin. A minimum number of posts from each participant is written into her
          agreement.</span></div>
        <div class="f"><b style="font-size:4.6cqw;">11</b><i></i><em>Made</em>
          <span>A short edit out every day of the tour, and one long-form series afterwards, plus a
          stills library, partner cut-downs and a rights cleared archive each partner keeps.</span></div>
        <div class="f"><b style="font-size:4.6cqw;">18</b><i></i><em>Earned</em>
          <span>Outlets briefed across the four countries and the diaspora press, alongside the
          festivals' own channels and their coverage of the delegation.</span></div>
      </div>
      <div class="twoshot" style="margin-top:auto;">
        <img src="%s" alt="" style="aspect-ratio:21/9;">
        <img src="%s" alt="" style="aspect-ratio:21/9;">
      </div>
      <div class="cap" style="margin-top:.7cqw;">Mother Africa Festival, Abidjan &nbsp;·&nbsp;
        the coast at Assinie</div>
    </div>
    <div class="fol"><span>The visibility</span><span>09</span></div>
  </section>"""

OLD_OBAR = """      <div class="obar" style="margin-top:1.3cqw;">
        <b>Possibilities, not packages.</b>
        <span>What a partner actually receives is set by scope and by budget, and is written into
          the agreement before anything is announced.</span>
      </div>"""

NEW_OBAR = """      <div class="obar" style="margin-top:1.2cqw;">
        <b>Baba Touré &nbsp;·&nbsp; AToure Management &amp; Consulting<br>
          <span style="font-family:'Karla',sans-serif;font-weight:400;font-size:1.02cqw;opacity:.85;">atoureconsulting@gmail.com</span></b>
        <span>What a partner receives is set by scope and by budget and is written into the
          agreement before anything is announced. No partner is contracted at the date of this
          document.</span>
      </div>
      <div class="cap" style="margin-top:.7cqw;">Location and festival photography credited to
        Afronation.com, Afrique Magazine and the Mother Africa Festival.</div>"""


def split_sections(body):
    """Sections never nest in this deck, so starts and ends pair off in order."""
    starts = [m.start() for m in re.finditer(r"<section\b", body)]
    ends = [m.end() for m in re.finditer(r"</section>", body)]
    assert len(starts) == len(ends)
    return [body[s:e] for s, e in zip(starts, ends)]


def patch(html):
    head, rest = html.split('<div class="deck">', 1)
    body = rest.rsplit("</div>", 1)[0]
    secs = split_sections(body)
    assert len(secs) == 10, "expected the v13 ten-page deck, got %d" % len(secs)

    # keep the two photographs before Filmed is rebuilt
    imgs = re.findall(r'<img src="(data:image/[^"]+)" alt="">', secs[7])
    assert len(imgs) == 2, "expected two photographs on the Filmed page"

    s2 = secs[1]
    flights = "They cover their own flights to Abidjan. Everything on the ground is covered."
    assert flights in s2
    s2 = s2.replace(flights, "Everything on the ground is covered.", 1)
    assert "<em>Countries</em>" in s2
    s2 = s2.replace("<em>Countries</em>", "<em>Prospective countries</em>", 1)
    i = s2.index("<div class='dblk'><b>Who delivers it</b>")
    j = s2.index("</div>", s2.index("</span>", i)) + len("</div>")
    blk = s2[i:j]
    assert blk.count("<div") == blk.count("</div>") and len(blk) < 400
    s2 = s2[:i] + s2[j:]
    # four blocks read better two by two than three with an orphan
    assert s2.count('<div class="dgrid3">') == 1
    s2 = s2.replace(
        '<div class="dgrid3">',
        '<div class="dgrid3" style="grid-template-columns:repeat(2,1fr);'
        'gap:1.8cqw 4cqw;margin-top:auto;">', 1)
    secs[1] = s2

    s9 = secs[8]
    assert OLD_OBAR in s9
    secs[8] = s9.replace(OLD_OBAR, NEW_OBAR, 1)

    # drop the budget page, insert the pillars at three, swap Filmed for visibility
    out = [secs[0], secs[1], PILLARS, secs[2], secs[3], secs[4], secs[5], secs[6],
           VISIBILITY % (imgs[0], imgs[1]), secs[8]]

    renumbered = []
    for n, sec in enumerate(out, 1):
        renumbered.append(re.sub(
            r'(<div class="fol"><span>[^<]*</span><span>)\d{2}(</span>)',
            lambda m: "%s%02d%s" % (m.group(1), n, m.group(2)), sec))

    anchor = ".onum{font:300 2.6cqw/.9 'Fraunces';color:var(--accent);}"
    assert anchor in head
    head = head.replace(anchor, anchor + PIL3_CSS, 1)

    return head + '<div class="deck">' + "".join(renumbered) + "</div>\n"


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    with open(src) as f:
        out = patch(f.read())
    for gone in ("Who delivers", "own flights", "€185,000"):
        assert gone not in out, gone
    with open(dst, "w") as f:
        f.write(out)
    print("%s -> %s  (%d sections, %.1f MB)"
          % (src, dst, out.count("<section"), len(out) / 1e6))
