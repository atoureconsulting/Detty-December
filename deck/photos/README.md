# Roster photos

Drop one image per woman here. Named either way:

    by position   1.jpg  2.jpg  ...  14.jpg      (deck/site order)
    or by slug    olivia-yace.jpg  dorcas-dienda.png

Any size, any crop, any of .jpg/.jpeg/.png/.webp. Both the deck and the
site centre-crop and mask them to circles automatically.

    python deck/prep_photos.py     # crops + masks, reports what's missing
    node   deck/build.js           # rebuilds the PowerPoint
    python site/build_site.py      # rebuilds the website

Position order:

     1 Olivia Yacé              8 Dorcas Dienda
     2 Veena Praveenar Singh    9 Ophély Mézino
     3 Isabella Menin          10 Nellie Anjaratiana
     4 Nadia Mejia             11 Sephora Kongo
     5 Alicia Aylies           12 "Tai"
     6 Angélique Angarni-Filopon  13 Khaiza Kuyo
     7 Rebecca Biangue         14 Bella Zabaneh

These are committed so the site build can embed them. Only add images you
have the rights to use.
