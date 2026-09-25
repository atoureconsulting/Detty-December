# -*- coding: utf-8 -*-
"""Route map for the deck, drawn from Natural Earth 1:50m country geometry
   (world-atlas@2, pulled from the npm registry). No CDN reachable from here."""
import json, math, io, base64
from PIL import Image, ImageDraw, ImageFilter

TOPO = json.load(open("geo/package/countries-50m.json"))
SCALE, TRANS = TOPO["transform"]["scale"], TOPO["transform"]["translate"]

def arc(i):
    rev = i < 0
    if rev:
        i = ~i
    x = y = 0
    pts = []
    for dx, dy in TOPO["arcs"][i]:
        x += dx; y += dy
        pts.append((x * SCALE[0] + TRANS[0], y * SCALE[1] + TRANS[1]))
    return pts[::-1] if rev else pts

def rings(geom):
    polys = geom["arcs"] if geom["type"] == "Polygon" else [r for p in geom["arcs"] for r in p]
    out = []
    for ring in polys:
        pts = []
        for i in ring:
            seg = arc(i)
            pts.extend(seg if not pts else seg[1:])
        out.append(pts)
    return out

BY_NAME = {g["properties"]["name"]: g for g in TOPO["objects"]["countries"]["geometries"]}

TOUR = {"Côte d'Ivoire": "#E2710C", "Ghana": "#0B7A4B", "Nigeria": "#A83A1E", "Benin": "#E8A33D"}
NEIGHBOURS = ["Burkina Faso", "Mali", "Guinea", "Liberia", "Niger", "Togo", "Cameroon",
              "Sierra Leone", "Senegal", "Guinea-Bissau", "Gambia", "Chad", "Mauritania",
              "Eq. Guinea", "Gabon", "Central African Rep.", "Algeria", "Cameroon"]

W, H = 1700, 900
LON0, LON1, LAT0, LAT1 = -10.2, 15.2, 2.6, 16.0
KX = W / (LON1 - LON0)
KY = H / (LAT1 - LAT0)

def P(lon, lat):
    return ((lon - LON0) * KX, (LAT1 - lat) * KY)

SEA, LAND = "#0B2130", "#284E60"
im = Image.new("RGB", (W, H), SEA)
d = ImageDraw.Draw(im)

for n in NEIGHBOURS:
    g = BY_NAME.get(n)
    if not g:
        continue
    for r in rings(g):
        d.polygon([P(*p) for p in r], fill=LAND, outline="#0E2634")

for n, col in TOUR.items():
    g = BY_NAME.get(n)
    assert g, "missing country geometry: " + n
    for r in rings(g):
        d.polygon([P(*p) for p in r], fill=col, outline="#FBF6EC")

# the coastal corridor; the numbers and labels are set in the deck's own type
STOPS = [("Lagos", 3.38, 6.52, "r"), ("Abidjan", -4.02, 5.35, "l"),
         ("Assinie", -3.28, 5.13, "d"), ("Accra", -0.19, 5.60, "d")]
OPTIONAL = [("Ouidah", 2.09, 6.36, "u")]
pos = {n: P(lo, la) for n, lo, la, _ in STOPS + OPTIONAL}

corridor = ["Abidjan", "Assinie", "Accra", "Ouidah", "Lagos"]
for a, b in zip(corridor, corridor[1:]):
    A, B = pos[a], pos[b]
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2 - abs(B[0] - A[0]) * 0.18
    prev = A
    for t in [i / 30 for i in range(1, 31)]:
        x = (1 - t) ** 2 * A[0] + 2 * (1 - t) * t * mx + t ** 2 * B[0]
        y = (1 - t) ** 2 * A[1] + 2 * (1 - t) * t * my + t ** 2 * B[1]
        d.line([prev, (x, y)], fill="#FBF6EC", width=5)
        prev = (x, y)

for n, lo, la, _ in STOPS:
    x, y = P(lo, la)
    d.ellipse([x - 15, y - 15, x + 15, y + 15], fill="#FBF6EC")
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill="#12303F")
for n, lo, la, _ in OPTIONAL:                      # the Benin leg is an option, not a leg
    x, y = P(lo, la)
    d.ellipse([x - 15, y - 15, x + 15, y + 15], outline="#FBF6EC", width=4)

im = im.filter(ImageFilter.SMOOTH)
im.save("route-map.png")
print("route-map.png", im.size)

# label anchors as percentages, so the deck can set them in its own type
print("LABELS = " + repr([(n, round(pos[n][0] / W * 100, 2), round(pos[n][1] / H * 100, 2), sd)
                          for n, _, _, sd in STOPS + OPTIONAL]))
for n in TOUR:
    rs = rings(BY_NAME[n]); big = max(rs, key=len)
    cx = sum(x for x, _ in big) / len(big); cy = sum(y for _, y in big) / len(big)
    x, y = P(cx, cy)
    print("COUNTRY %-14s %.2f %.2f" % (n, x / W * 100, y / H * 100))
