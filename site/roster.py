"""Roster data — single source of truth for the site and the pull list.

`socials` entries are (platform, handle, url, reach). reach=None means the
account exists but no figure could be found; omit the platform entirely if
no account was found at all.
"""

ROSTER = [
    dict(
        slug="olivia-yace", name="Olivia Yacé", nat="Côte d'Ivoire", kind="title",
        title="Miss Côte d'Ivoire 2021",
        role="Miss World 2021 second runner-up and Miss World Africa. Miss Universe "
             "Côte d'Ivoire 2025 — fourth runner-up, the first Ivorian to reach the Top 5.",
        socials=[
            ("Instagram", "@olivia.yace", "https://instagram.com/olivia.yace", "~1M"),
            ("TikTok", "@.oliviayace", "https://tiktok.com/@.oliviayace", "~934K"),
            ("Facebook", "OliviaYaceMissCi2021", "https://facebook.com/OliviaYaceMissCi2021", "~756K"),
            ("YouTube", "Olivia Yace", None, None),
        ],
        also="Tourism Ambassador of Côte d'Ivoire since 2022 · runs the Fondation Olivia Yacé · "
             "already publicly linked to Mother Africa Festival, the tour's opening anchor.",
        flags=["Verify affiliation"],
    ),
    dict(
        slug="veena-praveenar", name="Veena Praveenar Singh", nat="Thailand", kind="title",
        title="Miss Universe Thailand 2025",
        role="First runner-up at Miss Universe 2025, and the first winner of Indian descent "
             "for the Thai title.",
        socials=[
            ("Instagram", "@veenapraveenar", "https://instagram.com/veenapraveenar", "~2M"),
            ("TikTok", "@veenapraveenar", "https://tiktok.com/@veenapraveenar", None),
            ("Facebook", "veenapraveenarsinghthakral", None, None),
            ("YouTube", "Praveenar Singh Thakral", None, None),
        ],
        also="Cultural and tourism ambassador for Thailand · fluent in Thai, English and Russian.",
        flags=["Title corrected"],
    ),
    dict(
        slug="isabella-menin", name="Isabella Menin", nat="Brazil", kind="title",
        title="Miss Grand International 2022",
        role="The first Brazilian ever to win the title.",
        socials=[("Instagram", "@isanmenin", "https://instagram.com/isanmenin", "~1.05M")],
        also="Founder of LA Menin Beauty · MSc Finance, UCL · founded Beyond Project, "
             "supporting disability organisations in Brazil.",
        flags=[],
    ),
    dict(
        slug="nadia-mejia", name="Nadia Mejia", nat="Ecuador / USA", kind="title",
        title="Miss Universe Ecuador 2025",
        role="Previously Miss California USA 2016, Top 5 and Fan Favourite at Miss USA 2016.",
        socials=[
            ("Instagram", "@nadia_mejia", "https://instagram.com/nadia_mejia", "~435K"),
            ("TikTok", "@nadiagracemejia", "https://tiktok.com/@nadiagracemejia", "~125K"),
            ("Facebook", "TheNadiaMejia", "https://facebook.com/TheNadiaMejia", None),
        ],
        also="Singer and worship leader · daughter of musician Gerardo and Miss West Virginia USA 1989.",
        flags=["Not the Chilean singer"],
    ),
    dict(
        slug="alicia-aylies", name="Alicia Aylies", nat="French Guiana", kind="title",
        title="Miss France 2017",
        role="The first representative from French Guiana to win the national title.",
        socials=[
            ("Instagram", "@aliciaaylies", "https://instagram.com/aliciaaylies", "~423K"),
            ("TikTok", "@aliciaaylies", "https://tiktok.com/@aliciaaylies", "~148K"),
            ("Facebook", "Alicia Aylies", None, "~78K"),
            ("YouTube", "Alicia Aylies", None, None),
        ],
        also="Recording artist — \"Mojo\", \"Abuser\", \"No Wahala\" · Festina ambassador since 2017 · "
             "Hugo Boss and Lancaster Beauty campaigns.",
        flags=["Fan accounts exist"],
    ),
    dict(
        slug="angelique-angarni-filopon", name="Angélique Angarni-Filopon",
        nat="Martinique", kind="title",
        title="Miss France 2025",
        role="The first Martinican winner, and at 34 the oldest woman ever crowned Miss France.",
        socials=[
            ("Instagram", "@angeliqueaf_off", "https://instagram.com/angeliqueaf_off", "~395K"),
            ("Facebook", "Angélique Angarni-Filopon", None, None),
        ],
        also="Competing on the 2026 season of French Dancing with the Stars · appeared at Cannes 2025.",
        flags=["Year corrected — 2025, not 2019"],
    ),
    dict(
        slug="rebecca-biangue", name="Rebecca Biangue", nat="France", kind="creator",
        title="Beauty and lifestyle creator",
        role="No pageant title found in public record. Paris-based, makeup and hairstyling "
             "content with brand collaboration work.",
        socials=[
            ("Instagram", "@rebeccarih", "https://instagram.com/rebeccarih", "~220K"),
            ("TikTok", "@rebeccarihh", "https://tiktok.com/@rebeccarihh", "~43K"),
            ("YouTube", "Rebecca Biangue", None, "~20K"),
        ],
        also="Note the TikTok handle carries a double h — confirm it is hers before tagging.",
        flags=["No title found"],
    ),
    dict(
        slug="dorcas-dienda", name="Dorcas Dienda", nat="DR Congo", kind="title",
        title="Miss Africa 2019 · Miss Universe DR Congo 2025",
        role="Appointed to the national title in September 2025 after the original winner "
             "was dethroned.",
        socials=[
            ("Instagram", "@dorcas_dienda", "https://instagram.com/dorcas_dienda", "~216K"),
            ("TikTok", "@dorcasdienda1811", "https://tiktok.com/@dorcasdienda1811", None),
            ("Facebook", "dorcasdiendaofficiel", "https://facebook.com/dorcasdiendaofficiel", None),
        ],
        also="Founder of the Dorcas Dienda Foundation — child nutrition, education access, and "
             "women's empowerment through art and fashion mentorship in DRC.",
        flags=[],
    ),
    dict(
        slug="ophely-mezino", name="Ophély Mézino", nat="Guadeloupe", kind="title",
        title="Miss World 2019 first runner-up",
        role="Miss World Europe 2019. Miss Guadeloupe 2018, Miss France 2019 first runner-up, "
             "Miss Universe Guadeloupe 2025.",
        socials=[
            ("Instagram", "@ophelymezinooff", "https://instagram.com/ophelymezinooff", "~141K"),
            ("TikTok", "@ophelymezinooff", "https://tiktok.com/@ophelymezinooff", "~35K"),
            ("Facebook", "ophelymezinooff", "https://facebook.com/ophelymezinooff", "~20K"),
            ("YouTube", "@ophelymezinooff", "https://youtube.com/@ophelymezinooff", None),
        ],
        also="Hosts the \"Confidence Closet\" podcast · represented by Talent Go.",
        flags=[],
    ),
    dict(
        slug="nellie-anjaratiana", name="Nellie Anjaratiana", nat="Madagascar", kind="title",
        title="Miss Madagascar 2020",
        role="Top 40 at Miss World.",
        socials=[
            ("Instagram", "@nellie_anj", "https://instagram.com/nellie_anj", "~80K"),
            ("Facebook", "nellieofficiel", "https://facebook.com/nellieofficiel", "~105K"),
        ],
        also="Her Beauty With a Purpose project addresses the stigma faced by twins in "
             "Mananjary, Madagascar · based in New York.",
        flags=[],
    ),
    dict(
        slug="sephora-kongo", name="Sephora Kongo", nat="DR Congo", kind="creator",
        title="Fashion and lifestyle influencer",
        role="Kinshasa-based. No pageant title found in public record.",
        socials=[
            ("Instagram", "@sephorakng", "https://instagram.com/sephorakng", "~73K"),
            ("TikTok", "@sephorakng", "https://tiktok.com/@sephorakng", "~39K"),
            ("Snapchat", "@sephorakng", None, None),
        ],
        also="Featured in BellaNaija style coverage.",
        flags=["No title found"],
    ),
    dict(
        slug="tai", name="“Tai”", nat="Unknown", kind="creator",
        title="Unidentified",
        role="An Instagram handle and nothing more — no name, nationality or credentials could "
             "be found. The original note also read “Tai (+1 Angelique)”, still unresolved.",
        socials=[("Instagram", "@tai.prst", "https://instagram.com/tai.prst", "~43–63K")],
        also="Needed: a full name and bio from whoever added her to the list. Identity cannot be "
             "confirmed from the handle alone.",
        flags=["Unidentified"],
    ),
    dict(
        slug="khaiza-kuyo", name="Khaiza Kuyo", nat="Côte d'Ivoire", kind="creator",
        title="Actress",
        role="Plays Brenda in the Ivorian series Isabelle. No pageant title found in public "
             "record. Spelled Kaihza in most sources.",
        socials=[
            ("Instagram", "@kaihzakuyo", "https://instagram.com/kaihzakuyo", "~33K"),
            ("TikTok", "@kaihzakuyo", "https://tiktok.com/@kaihzakuyo", "~57K"),
            ("Facebook", "kaihza.kuyo", "https://facebook.com/kaihza.kuyo", None),
            ("YouTube", "@kaihzakuyo9430", None, None),
        ],
        also="Describes herself as an app founder and artist manager — not corroborated by press.",
        flags=["No title found"],
    ),
    dict(
        slug="bella-zabaneh", name="Bella Zabaneh", nat="Belize", kind="title",
        title="Miss Universe Belize 2025",
        role="Represented Belize at Miss Universe 2025.",
        socials=[
            ("Instagram", "@bellaezabaneh", "https://instagram.com/bellaezabaneh", "~23K"),
            ("TikTok", "@isabellazabaneh0", "https://tiktok.com/@isabellazabaneh0", "~22K"),
            ("Instagram", "@isabellazabaneh", "https://instagram.com/isabellazabaneh", "~18K"),
        ],
        also="Co-founder of Project Royalty, a nonprofit providing gowns and support to young "
             "Belizean women since 2019.",
        flags=["Two IG accounts"],
    ),
]
