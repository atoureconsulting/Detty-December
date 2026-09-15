"""Roster data — single source of truth for the site and the pull list.

`socials` entries are (platform, handle, url, reach). reach=None means the
account exists but no figure could be found; omit the platform entirely if
no account was found at all.

Follower figures below marked in the `also`/source come from the client's
own September 2026 tracking sheet for the reworked 18-name "West Africa
Queens Tour" concept, replacing the earlier public-search estimates for
anyone who appears on both lists.
"""

ROSTER = [
    dict(
        slug="olivia-yace", name="Olivia Yacé", nat="Côte d'Ivoire", kind="title", status="core",
        title="Miss Côte d'Ivoire 2021",
        role="Miss World 2021 second runner-up and Miss World Africa. Miss Universe "
             "Côte d'Ivoire 2025 — fourth runner-up, the first Ivorian to reach the Top 5. "
             "Host and convener of the tour through Olivia Yacé International.",
        socials=[
            ("Instagram", "@olivia.yace", "https://instagram.com/olivia.yace", "1.2M"),
            ("TikTok", "@.oliviayace", "https://tiktok.com/@.oliviayace", "1.1M"),
            ("Facebook", "OliviaYaceMissCi2021", "https://facebook.com/OliviaYaceMissCi2021", "760K"),
        ],
        also="Tourism Ambassador of Côte d'Ivoire since 2022 · runs the Fondation Olivia Yacé · "
             "already publicly linked to Mother Africa Festival.",
        flags=["Verify affiliation"],
        brands=[("Raymond Weil", "Watches", "global", "low"), ("ZINO / ADOHA", "Jewelry / real estate", "local", "med")],
    ),
    dict(
        slug="berenice-dickinson", name="Bereniece Dickenson", nat="Turks & Caicos", kind="title", status="dropped",
        title="Miss Universe Turks & Caicos 2025",
        role="Competed at Miss Universe 2025 in Thailand, did not advance to the Top 30. "
             "Trained in architecture and building technologies; worked as a junior accountant "
             "before pageantry.",
        socials=[
            ("Instagram", "—", None, "21.3K"),
            ("TikTok", "—", None, "2K"),
        ],
        also="Name corrected from the client's brief spelling. Sponsors: COMO Hotels & Resorts "
             "(genuine international luxury group), bēchë swimwear and HAB Group (both local).",
        flags=["Name spelling corrected", "Not selected"],
        brands=[("COMO Hotels & Resorts", "Hospitality", "global", "med"), ("bēchë / HAB Group", "Swimwear / local sponsor", "local", "med")],
    ),
    dict(
        slug="camille-thomas", name="Camille Sabina Thomas", nat="Curaçao", kind="title", status="core",
        title="Miss Universe Curaçao 2025",
        role="Her first-ever pageant. Former officer at a military academy; holds a fine arts "
             "degree; studied Japanese and Korean. Drafted and presented an \"Emotional "
             "Well-Being and Protection Act\" proposal to Curaçao's Minister of Justice.",
        socials=[
            ("Instagram", "—", None, "18.5K"),
            ("TikTok", "—", None, "3.8K"),
        ],
        also="No brand deals found, local or global.",
        flags=["Namesake collision — see note"],
        brands=[],
    ),
    dict(
        slug="nadia-mejia", name="Nadia Mejia", nat="Ecuador / USA", kind="title", status="core",
        title="Miss Universe Ecuador 2025",
        role="Previously Miss California USA 2016, Top 5 and Fan Favourite at Miss USA 2016.",
        socials=[
            ("Instagram", "@nadia_mejia", "https://instagram.com/nadia_mejia", "434K"),
            ("TikTok", "@nadiagracemejia", "https://tiktok.com/@nadiagracemejia", "127K"),
            ("Facebook", "TheNadiaMejia", "https://facebook.com/TheNadiaMejia", "5K"),
        ],
        also="Singer and worship leader · daughter of musician Gerardo and Miss West Virginia USA 1989.",
        flags=["Not the Chilean singer"],
        brands=[("Guess", "Fashion", "global", "med"), ("Kitchen Crafted", "Food", "global", "high")],
    ),
    dict(
        slug="sheynnis-palacios", name="Sheynnis Palacios", nat="Nicaragua", kind="title", status="core",
        title="Miss Universe 2023",
        role="Won Nov 18, 2023 — the first Nicaraguan ever to win. Miss World Nicaragua 2020, "
             "Miss World 2021 Top 40. Bachelor's in mass communication, UCA Managua. Hosts a "
             "mental-health podcast, \"Entiende tu Mente.\"",
        socials=[
            ("Instagram", "—", None, "2.3M"),
            ("TikTok", "—", None, "2.5M"),
            ("Facebook", "—", None, "1M"),
        ],
        also="Advocacy ties to UNICEF, Smile Train and the AIDS Healthcare Foundation (advocate-level, "
             "not confirmed as formal contracted ambassadorships).",
        flags=[],
        brands=[("Pandora", "Jewelry", "global", "high")],
    ),
    dict(
        slug="angelique-angarni-filopon", name="Angélique Angarni-Filopon",
        nat="Martinique", kind="title", status="core",
        title="Miss France 2025",
        role="The first Martinican winner, and at 34 the oldest woman ever crowned Miss France.",
        socials=[
            ("Instagram", "@angeliqueaf_off", "https://instagram.com/angeliqueaf_off", "394K"),
            ("TikTok", "—", None, "474K"),
        ],
        also="Competing on the 2026 season of French Dancing with the Stars · appeared at Cannes 2025.",
        flags=["Year corrected — 2025, not 2019"],
        brands=[("Festina", "Watches", "global", "high")],
    ),
    dict(
        slug="alicia-aylies", name="Alicia Aylies", nat="French Guiana", kind="title", status="reserve",
        title="Miss France 2017",
        role="The first representative from French Guiana to win the national title.",
        socials=[
            ("Instagram", "@aliciaaylies", "https://instagram.com/aliciaaylies", "423K"),
            ("TikTok", "@aliciaaylies", "https://tiktok.com/@aliciaaylies", "147K"),
            ("Facebook", "Alicia Aylies", None, "76K"),
        ],
        also="Recording artist — \"Mojo\", \"Abuser\", \"No Wahala\" · Festina ambassador since 2017 · "
             "Hugo Boss and Lancaster Beauty campaigns.",
        flags=["Fan accounts exist"],
        brands=[("Festina", "Watches", "global", "high"), ("Mauboussin", "Jewelry", "global", "high"), ("Palmer's", "Beauty", "global", "med")],
    ),
    dict(
        slug="ophely-mezino", name="Ophély Mézino", nat="Guadeloupe", kind="title", status="core",
        title="Miss World 2019 first runner-up",
        role="Miss World Europe 2019. Miss Guadeloupe 2018, Miss France 2019 first runner-up, "
             "Miss Universe Guadeloupe 2025.",
        socials=[
            ("Instagram", "@ophelymezinooff", "https://instagram.com/ophelymezinooff", "141K"),
            ("TikTok", "@ophelymezinooff", "https://tiktok.com/@ophelymezinooff", "39K"),
        ],
        also="Hosts the \"Confidence Closet\" podcast · represented by Talent Go.",
        flags=[],
        brands=[("Local Guadeloupe soda brand", "Beverage", "local", "med")],
    ),
    dict(
        slug="veena-praveenar", name="Veena Praveenar Singh", nat="Thailand", kind="title", status="core",
        title="Miss Universe Thailand 2025",
        role="First runner-up at Miss Universe 2025, and the first winner of Indian descent "
             "for the Thai title.",
        socials=[
            ("Instagram", "@veenapraveenar", "https://instagram.com/veenapraveenar", "2.1M"),
            ("TikTok", "@veenapraveenar", "https://tiktok.com/@veenapraveenar", "472K"),
            ("Facebook", "veenapraveenarsinghthakral", None, "52K"),
        ],
        also="Cultural and tourism ambassador for Thailand · fluent in Thai, English and Russian.",
        flags=["Title corrected"],
        brands=[],
    ),
    dict(
        slug="dorcas-dienda", name="Dorcas Dienda", nat="DR Congo", kind="title", status="core",
        title="Miss Africa 2019 · Miss Universe DR Congo 2025",
        role="Appointed to the national title in September 2025 after the original winner "
             "was dethroned.",
        socials=[
            ("Instagram", "@dorcas_dienda", "https://instagram.com/dorcas_dienda", "222K"),
            ("TikTok", "@dorcasdienda1811", "https://tiktok.com/@dorcasdienda1811", "263K"),
            ("Facebook", "dorcasdiendaofficiel", "https://facebook.com/dorcasdiendaofficiel", "61K"),
        ],
        also="Founder of the Dorcas Dienda Foundation — child nutrition, education access, and "
             "women's empowerment through art and fashion mentorship in DRC.",
        flags=[],
        brands=[],
    ),
    dict(
        slug="camila-vitorino", name="Camila Vitorino", nat="Portugal", kind="title", status="dropped",
        title="Miss Universo Portugal 2025",
        role="First married woman and first mother to hold the title. Earlier titles: Miss "
             "Planet 2017 (Georgia), Miss Queen Portugal 2019. Volunteers with CASA, a homeless "
             "support centre in Setúbal, since 2019.",
        socials=[
            ("Instagram", "—", None, "50.4K"),
            ("TikTok", "—", None, "16.7K"),
        ],
        also="João Sousa Brand supplied looks for her Miss Universe run — a local fashion sponsor, "
             "not a global deal.",
        flags=["Not selected"],
        brands=[],
    ),
    dict(
        slug="camilla-diagne", name="Camilla Diagne", nat="Senegal", kind="title", status="dropped",
        title="Miss Universe Senegal 2025",
        role="Karateka and model; founder of Milla's Wax, a label modernising traditional "
             "African wax-print fabric. Her selection drew public controversy in Senegal over "
             "marital-status eligibility, which the national committee publicly defended.",
        socials=[
            ("Instagram", "—", None, "18.5K"),
            ("TikTok", "—", None, "62.3K"),
            ("Facebook", "—", None, "5.6K"),
        ],
        also="No brand deals found beyond her own label.",
        flags=["Not selected"],
        brands=[],
    ),
    dict(
        slug="bella-zabaneh", name="Bella Zabaneh", nat="Belize", kind="title", status="core",
        title="Miss Universe Belize 2025",
        role="Represented Belize at Miss Universe 2025.",
        socials=[
            ("Instagram", "@bellaezabaneh", "https://instagram.com/bellaezabaneh", "23.3K"),
            ("TikTok", "@isabellazabaneh0", "https://tiktok.com/@isabellazabaneh0", "22.6K"),
            ("Facebook", "—", None, "3.5K"),
        ],
        also="Co-founder of Project Royalty, a nonprofit providing gowns and support to young "
             "Belizean women since 2019. Two active Instagram accounts — confirm which is official.",
        flags=["Two IG accounts"],
        brands=[("Belize Bank", "Banking", "local", "high"), ("ID Seven Apparel", "Fashion", "local", "med")],
    ),
    dict(
        slug="gabrielle-henry", name="Dr. Gabrielle Henry", nat="Jamaica", kind="title", status="dropped",
        title="Miss Universe Jamaica 2025",
        role="Ophthalmology trainee, University Hospital of the West Indies. Founder of the See "
             "Me Foundation, supporting people who are blind or visually impaired.",
        socials=[("Instagram", "—", None, "21.1K")],
        also="Sustained serious injuries in a stage fall at the Miss Universe 2025 preliminary "
             "round (Nov 2025); made her first public reappearance in May 2026. Handle with care "
             "in any outreach. Sponsor tie is a local dealership prize package, not a global deal.",
        flags=["Not selected"],
        brands=[],
    ),
    dict(
        slug="isabella-menin", name="Isabella Menin", nat="Brazil", kind="title", status="core",
        title="Miss Grand International 2022",
        role="The first Brazilian ever to win the title.",
        socials=[
            ("Instagram", "@isanmenin", "https://instagram.com/isanmenin", "1.1M"),
            ("TikTok", "—", None, "205.4K"),
            ("Facebook", "—", None, "22K"),
        ],
        also="Founder of LA Menin Beauty · MSc Finance, UCL · founded Beyond Project, "
             "supporting disability organisations in Brazil.",
        flags=[],
        brands=[],
    ),
    dict(
        slug="chloe-lim", name="Chloe Lim", nat="Malaysia", kind="title", status="dropped",
        title="Miss Universe Malaysia 2025",
        role="Management consultant; two master's degrees including a Master's in Law. "
             "Long-time volunteer with Lighthouse Children's Welfare Home; advocacy focus on "
             "education equity and animal rights.",
        socials=[
            ("Instagram", "—", None, "18.6K"),
            ("TikTok", "—", None, "1K"),
        ],
        also="No confirmed brand deals, local or global.",
        flags=["Common name — verify by photo", "Not selected"],
        brands=[],
    ),
    dict(
        slug="sanly-liuu", name="Sanly Liu (Hendrawati)", nat="Indonesia", kind="title", status="reserve",
        title="Miss Universe Indonesia 2025",
        role="Entrepreneur and 10-year beauty content creator before adding the pageant title. "
             "Owns several Bali businesses: Spring Summer Style, Spring Summer Studio Bali, "
             "Salvus Villa, The Pause Bali.",
        socials=[
            ("Instagram", "—", None, "258K"),
            ("TikTok", "—", None, "46.2K"),
        ],
        also="Indonesian press describes past \"collaborations with international brands\" from her "
             "creator career, but no specific names were verifiable — treat as unconfirmed.",
        flags=["Handle reads Sanly Liuu; name is Sanly Liu"],
        brands=[],
    ),
    dict(
        slug="huong-giang", name="Hương Giang", nat="Vietnam", kind="title", status="reserve",
        title="Miss International Queen 2018",
        role="Major Vietnamese entertainment figure — singer, actress, TV host/judge (The Face "
             "Vietnam, Rap Việt), first transgender contestant on Vietnam Idol (2012). Reportedly "
             "the first Asian transgender woman to compete in Miss Universe, as Miss Universe "
             "Vietnam 2025. Widely credited with mainstreaming transgender visibility in Vietnam.",
        socials=[
            ("Instagram", "—", None, "4.2M"),
            ("TikTok", "—", None, "4.5M"),
            ("Facebook", "—", None, "3.9M"),
        ],
        also="Brand tie found (Dezus fashion) is a domestic Vietnamese label, not a global deal.",
        flags=[],
        brands=[("Dezus", "Fashion", "local", "high")],
    ),
]
