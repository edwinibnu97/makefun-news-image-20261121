# generate.py — renders entry.png (1024x1024) for make.fun news-image-20261121.
# Deterministic: no randomness, no network, no timestamps. Pure Pillow drawing.
# The shipped entry.png is the output of this script; main.ts only copies it.
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
MUTED = (90, 90, 90)
RED = (180, 35, 24)
NAVY = (11, 42, 74)
GOLD = (232, 193, 90)
CARD = (255, 255, 255)
BORDER = (200, 192, 175)

FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)
F_SERIF = lambda s: font("DejaVuSerif.ttf", s)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_spaced(draw, xy, text, fnt, fill, spacing=2):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x

def text_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- outer border ----
d.rectangle([12, 12, W - 13, H - 13], outline=NAVY, width=3)

# ---- masthead ----
d.rectangle([24, 24, W - 25, 118], fill=NAVY)
d.text((44, 38), "THE WORLD TODAY", font=F_SERIF_B(52), fill=(255, 255, 255))
d.text(((W - 44 - d.textlength("SATURDAY", font=F_SANS_B(24))), 34), "SATURDAY",
       font=F_SANS_B(24), fill=GOLD)
d.text(((W - 44 - d.textlength("21 NOVEMBER 2026", font=F_SANS_B(26))), 62),
       "21 NOVEMBER 2026", font=F_SANS_B(26), fill=(255, 255, 255))
d.rectangle([24, 118, W - 25, 124], fill=RED)

# ---- hero card ----
d.rectangle([24, 140, W - 25, 448], fill=CARD, outline=BORDER, width=2)
d.rectangle([24, 140, 34, 448], fill=RED)
draw_spaced(d, (56, 158), "LEAD STORY  ·  WAR IN EUROPE", F_SANS_B(19), RED, 2)
d.text((56, 186), "RUSSIAN MISSILES", font=F_SANS_B(54), fill=INK)
d.text((56, 246), "HIT POLAND", font=F_SANS_B(54), fill=INK)
body = ("Two Russian missiles and a drone came down in Poland "
        "during a massive attack on Ukraine. Warsaw calls it a "
        "deliberate provocation.")
blines = wrap(d, body, F_SANS(22), 616)
text_block(d, (56, 312), blines, F_SANS(22), (40, 40, 40), 29)
d.text((56, 404), "WARSAW — No injuries reported.", font=F_SANS(18), fill=MUTED)
d.text((56, 426), "NATO calls it a grave violation of its airspace.",
       font=F_SANS(18), fill=MUTED)

# hero graphic: night sky, missile arcs, impact burst
gx0, gy0, gx1, gy1 = 700, 156, 984, 432
d.rectangle([gx0, gy0, gx1, gy1], fill=NAVY)
# ground + skyline
d.rectangle([gx0, gy1 - 46, gx1, gy1], fill=(7, 28, 52))
for i, (bx, bw, bh) in enumerate([(0, 34, 26), (44, 26, 38), (80, 40, 20), (130, 30, 32),
                                  (170, 36, 24), (216, 28, 36), (254, 28, 22)]):
    d.rectangle([gx0 + bx, gy1 - 46 - bh, gx0 + bx + bw, gy1 - 46], fill=(16, 54, 96))
# missile arcs (quadratic curves via sampled points)
import math
def arc_pts(p0, p1, p2, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    return pts
for (p0, p1, p2) in [((gx0 + 18, gy1 - 52), (gx0 + 120, gy0 + 60), (gx0 + 238, gy1 - 60)),
                     ((gx0 + 60, gy1 - 52), (gx0 + 170, gy0 + 90), (gx0 + 252, gy1 - 66))]:
    pts = arc_pts(p0, p1, p2)
    d.line(pts, fill=(232, 193, 90, 90), width=7)
    d.line(pts, fill=GOLD, width=3)
    d.ellipse([p2[0] - 5, p2[1] - 5, p2[0] + 5, p2[1] + 5], fill=(255, 255, 255))
# impact starburst
cx, cy = gx0 + 238, gy1 - 60
for ang in range(0, 360, 30):
    r = math.radians(ang)
    d.line([(cx, cy), (cx + 26 * math.cos(r), cy + 26 * math.sin(r))],
           fill=(255, 220, 120), width=3)
d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 240, 180))
d.text((gx0 + 14, gy0 + 10), "POLAND", font=F_SANS_B(22), fill=(255, 255, 255))
d.text((gx0 + 14, gy0 + 38), "NATO AIRSPACE", font=F_SANS_B(15), fill=(190, 205, 225))

# ---- story grid 2x2 ----
def icon_scales(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.line([(cx, cy - r + 12), (cx, cy + r - 12)], fill=NAVY, width=3)
    d.line([(cx - 22, cy - 8), (cx + 22, cy - 8)], fill=NAVY, width=3)
    for sx in (-22, 22):
        d.line([(sx + cx, cy - 8), (sx + cx, cy + 8)], fill=NAVY, width=2)
        d.arc([sx + cx - 11, cy + 4, sx + cx + 11, cy + 26], 0, 180, fill=NAVY, width=2)
    d.ellipse([cx - 4, cy - r + 8, cx + 4, cy - r + 16], fill=RED)

def icon_check(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.line([(cx - 14, cy + 1), (cx - 3, cy + 12), (cx + 16, cy - 12)],
           fill=RED, width=5, joint="curve")

def icon_chart(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    d.line([(cx - 20, cy + 18), (cx - 20, cy - 18)], fill=NAVY, width=2)
    d.line([(cx - 20, cy + 18), (cx + 20, cy + 18)], fill=NAVY, width=2)
    d.line([(cx - 16, cy - 8), (cx - 4, cy + 2), (cx + 8, cy - 2), (cx + 18, cy + 12)],
           fill=RED, width=4, joint="curve")

def icon_quake(cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=3)
    for rr in (8, 15, 22):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 200, 340, fill=NAVY, width=2)
    d.line([(cx - 20, cy + 14), (cx - 10, cy + 6), (cx - 2, cy + 18), (cx + 8, cy + 4),
            (cx + 16, cy + 16)], fill=RED, width=3, joint="curve")

cards = [
    ("JUSTICE  ·  THE HAGUE", "WORLD COURT: MYANMAR",
     "COMMITTED GENOCIDE",
     "The ICJ rules Myanmar's forces carried out state-sponsored "
     "genocide against the Rohingya.", icon_scales),
    ("POLITICS  ·  BRUSSELS", "UK AND EU STRIKE",
     "LANDMARK DEAL",
     "Biggest post-Brexit pact: food checks scrapped, carbon markets "
     "linked, 100,000 youth visas each way.", icon_check),
    ("MARKETS  ·  NEW YORK", "WALL STREET SLUMPS",
     "INTO CORRECTION",
     "S&P 500 and Dow fall into correction as AI and chip shares sell "
     "off; stocks down about 3.7%.", icon_chart),
    ("DISASTER  ·  LIMA", "6.8 QUAKE SHAKES",
     "PERU",
     "Strong tremor in the central Andes near Junín is felt in Lima; "
     "no casualties are reported.", icon_quake),
]
cw, ch, gx, gy = 472, 172, 24, 468
for i, (tag, h1, h2, summ, icon) in enumerate(cards):
    x0 = gx + (i % 2) * (cw + 16)
    y0 = gy + (i // 2) * (ch + 16)
    d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=BORDER, width=2)
    icon(x0 + 52, y0 + 52, 34)
    draw_spaced(d, (x0 + 100, y0 + 14), tag, F_SANS_B(14), RED, 1)
    d.text((x0 + 100, y0 + 34), h1, font=F_SANS_B(25), fill=INK)
    d.text((x0 + 100, y0 + 64), h2, font=F_SANS_B(25), fill=INK)
    slines = wrap(d, summ, F_SANS(18), cw - 116)
    text_block(d, (x0 + 100, y0 + 98), slines[:3], F_SANS(18), (40, 40, 40), 24)

# ---- also today band ----
d.rectangle([24, 848, W - 25, 958], fill=NAVY)
d.text((44, 860), "ALSO TODAY", font=F_SANS_B(21), fill=GOLD)
also = ("Shenzhen: Trump, Xi and Putin end their first trilateral summit with few "
        "concrete results  ·  COP31 climate talks run into overtime as a fossil-fuel "
        "deal stalls  ·  Riyadh: Saudi-led coalition intercepts Houthi missiles  ·  "
        "Pill hailed as a breakthrough for pancreatic cancer")
alines = wrap(d, also, F_SANS(17), W - 90)
text_block(d, (44, 886), alines[:3], F_SANS(17), (235, 235, 235), 23)

# ---- footer ----
foot = "World news of Saturday 21 November 2026  ·  As reported by Reuters, AP, BBC, NYT and Al Jazeera"
d.text(((W - d.textlength(foot, font=F_SANS(16))) / 2, 970), foot,
       font=F_SANS(16), fill=MUTED)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True, compress_level=9)
print("saved", out, os.path.getsize(out), "bytes", img.size)
