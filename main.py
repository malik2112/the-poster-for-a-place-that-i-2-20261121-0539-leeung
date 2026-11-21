#!/usr/bin/env python3
"""The Poster for a Place That Isn't There — THISTLEDOWN.

Deterministic PIL travel poster (1024x1024 PNG) for an invented alpine
village above a sea of clouds: snow peaks, a green knoll of chalets, a
suspension bridge to a rocky lookout, and a thistle meadow in the
foreground. The only text in the picture is the place name, set in the
deep-green band at the foot.
No network; fixed-seed pseudo-random detail only.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "/output/entry.png"
rng = random.Random(77410221)

FONT_DIRS = ["/usr/share/fonts/truetype/liberation", "/usr/share/fonts/truetype/dejavu"]

def load_font(names, size):
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()

SERIF_B = lambda s: load_font(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"], s)

PAPER = (246, 239, 222)
INK = (33, 38, 48)
CREAM = (252, 247, 230)
PINE_D = (27, 64, 48)
PINE = (44, 96, 66)
MEADOW = (110, 168, 92)
MEADOW_L = (150, 198, 118)
ROCK = (96, 102, 124)
ROCK_D = (66, 72, 96)
SNOW = (250, 251, 252)
WOOD = (122, 82, 52)
ROOF = (168, 72, 54)
THISTLE = (150, 96, 178)
THISTLE_D = (110, 62, 140)
GOLD = (238, 186, 92)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

X0, Y0, X1, Y1 = 34, 34, W - 34, H - 34
BAND = 868

def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

# ---------- morning sky ----------
sky_top = (86, 144, 194)
sky_mid = (160, 200, 222)
sky_low = (250, 214, 160)
for y in range(Y0, 700):
    t = (y - Y0) / (700 - Y0)
    c = mix(sky_top, sky_mid, t / 0.55) if t < 0.55 else mix(sky_mid, sky_low, (t - 0.55) / 0.45)
    d.line([(X0, y), (X1, y)], fill=c)

# small sky clouds + birds
for ccx, ccy, cw in [(200, 150, 120), (470, 110, 90), (610, 300, 80)]:
    d.ellipse([ccx - cw // 2, ccy - 14, ccx + cw // 2, ccy + 14], fill=(244, 248, 250))
    d.ellipse([ccx - cw // 4, ccy - 24, ccx + cw // 4, ccy + 8], fill=(250, 252, 253))
for bx, by, bs in [(300, 260, 13), (348, 282, 10), (560, 210, 11)]:
    d.arc([bx - bs, by - bs // 2, bx, by + bs // 2], start=200, end=330, fill=INK, width=2)
    d.arc([bx, by - bs // 2, bx + bs, by + bs // 2], start=210, end=340, fill=INK, width=2)

# ---------- sun with halo ----------
sx, sy, sr = 768, 190, 62
halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
hd.ellipse([sx - sr - 26, sy - sr - 26, sx + sr + 26, sy + sr + 26], fill=(254, 230, 170, 42))
img.paste(Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img)
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(252, 224, 148))
d.ellipse([sx - sr + 12, sy - sr + 12, sx + sr - 12, sy + sr - 12], fill=(250, 206, 110))

# ---------- distant snow peaks ----------
def peak(cx, base_y, half_w, apex_y, body, snow_h):
    d.polygon([(cx - half_w, base_y), (cx, apex_y), (cx + half_w, base_y)], fill=body)
    t = snow_h / max(1, (base_y - apex_y))
    sx1 = cx - half_w * t
    sx2 = cx + half_w * t
    sy2 = apex_y + snow_h
    d.polygon([(sx1, sy2), (cx, apex_y), (sx2, sy2),
               (cx + half_w * t * 0.4, sy2 - snow_h * 0.35),
               (cx, sy2 + snow_h * 0.25),
               (cx - half_w * t * 0.45, sy2 - snow_h * 0.3)], fill=SNOW)

peak(190, 560, 230, 250, ROCK, 95)
peak(430, 560, 200, 310, ROCK_D, 70)
peak(660, 560, 250, 230, ROCK, 105)
peak(890, 560, 190, 320, ROCK_D, 62)

# ---------- sea of clouds ----------
d.rectangle([X0, 520, X1, 706], fill=(238, 244, 248))
for _ in range(26):
    cx = rng.randint(X0 + 10, X1 - 10)
    cy = rng.randint(606, 690)
    rw = rng.randint(52, 140)
    rh = rng.randint(14, 28)
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(232, 240, 246))
for _ in range(46):
    cx = rng.randint(X0 + 10, X1 - 10)
    cy = rng.randint(512, 612)
    rw = rng.randint(46, 130)
    rh = rng.randint(16, 34)
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(250, 252, 253))
for _ in range(22):
    cx = rng.randint(X0 + 10, X1 - 10)
    cy = rng.randint(560, 632)
    rw = rng.randint(40, 100)
    rh = rng.randint(12, 24)
    d.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(224, 234, 242))

# ---------- village knoll ----------
d.polygon([(X0, BAND), (X0, 690), (180, 630), (420, 606), (650, 638), (780, BAND)], fill=PINE)
d.polygon([(X0, BAND), (X0, 736), (240, 670), (480, 650), (710, 698), (780, BAND)], fill=PINE_D)

# pine trees on the knoll
def pine(px, py, s):
    d.rectangle([px - 2, py - 6 * s, px + 2, py], fill=WOOD)
    for i, (ww, yy) in enumerate([(16, -8), (12, -22), (8, -34)]):
        d.polygon([(px - ww * s // 2, py + yy * s // 4), (px + ww * s // 2, py + yy * s // 4), (px, py + (yy - 16) * s // 4)], fill=(58, 122, 82))

pine(110, 700, 3)
pine(392, 668, 3)
pine(528, 682, 2)
pine(84, 748, 4)

def chalet(hx, hy, hw, hh):
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=CREAM)
    d.polygon([(hx - 6, hy), (hx + hw + 6, hy), (hx + hw // 2, hy - 22)], fill=ROOF)
    d.rectangle([hx + 8, hy + 10, hx + 16, hy + 20], fill=GOLD)
    d.rectangle([hx + hw - 16, hy + 10, hx + hw - 8, hy + 20], fill=GOLD)
    d.rectangle([hx + hw // 2 - 4, hy + hh - 15, hx + hw // 2 + 4, hy + hh], fill=INK)

chalet(150, 668, 56, 36)
chalet(224, 656, 62, 40)
chalet(304, 664, 54, 34)
chalet(190, 716, 60, 38)
chalet(268, 724, 52, 34)
chalet(336, 712, 58, 36)

# chapel with spire
cx0, cy0 = 428, 676
d.rectangle([cx0, cy0, cx0 + 46, cy0 + 52], fill=CREAM)
d.polygon([(cx0 - 5, cy0), (cx0 + 51, cy0), (cx0 + 23, cy0 - 20)], fill=ROOF)
d.rectangle([cx0 + 15, cy0 - 52, cx0 + 31, cy0 - 18], fill=CREAM)
d.polygon([(cx0 + 12, cy0 - 52), (cx0 + 34, cy0 - 52), (cx0 + 23, cy0 - 78)], fill=INK)
d.rectangle([cx0 + 19, cy0 + 16, cx0 + 27, cy0 + 30], fill=GOLD)

# ---------- rocky lookout (right) ----------
d.polygon([(690, BAND), (736, 612), (820, 572), (912, 614), (X1, 706), (X1, BAND)], fill=ROCK_D)
d.polygon([(736, 612), (820, 572), (882, 604), (798, 646)], fill=ROCK)
d.rectangle([794, 530, 846, 576], fill=WOOD)
d.polygon([(788, 530), (852, 530), (820, 504)], fill=ROOF)
d.rectangle([812, 544, 828, 560], fill=GOLD)

# ---------- suspension bridge: knoll -> lookout ----------
bx1, by1, bx2, by2 = 492, 640, 796, 556
sag = 46
deck = []
for i in range(41):
    t = i / 40
    x = bx1 + (bx2 - bx1) * t
    y = by1 + (by2 - by1) * t + sag * 4 * t * (1 - t)
    deck.append((x, y))
d.line(deck, fill=WOOD, width=8)
d.line([(x, y - 18) for x, y in deck], fill=INK, width=2)
for i in range(0, 41, 4):
    x, y = deck[i]
    d.line([(x, y), (x, y - 18)], fill=INK, width=2)
d.line([(bx1, by1), (bx1, by1 - 56)], fill=INK, width=5)
d.line([(bx2, by2), (bx2, by2 - 56)], fill=INK, width=5)
d.line([(bx1, by1 - 56), ((bx1 + bx2) // 2, min(by1, by2) - 8), (bx2, by2 - 56)], fill=INK, width=2)
# cable car hanging from the main cable
gx, gy = 636, 584
d.line([(gx, gy - 34), (gx, gy)], fill=INK, width=3)
d.rectangle([gx - 20, gy, gx + 20, gy + 26], fill=ROOF)
d.rectangle([gx - 14, gy + 5, gx - 3, gy + 16], fill=(210, 232, 240))
d.rectangle([gx + 3, gy + 5, gx + 14, gy + 16], fill=(210, 232, 240))

# ---------- foreground meadow ----------
d.polygon([(X0, BAND), (X0, 800), (360, 770), (760, 806), (X1, 790), (X1, BAND)], fill=MEADOW)
d.polygon([(X0, BAND), (X0, 830), (420, 806), (X1, 824), (X1, BAND)], fill=MEADOW_L)
for _ in range(70):
    x = rng.randint(X0 + 14, X1 - 14)
    y = rng.randint(788, BAND - 12)
    c = rng.choice([THISTLE, (250, 214, 90), (250, 250, 244), (244, 150, 130)])
    r = rng.choice([3, 4, 5])
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)
# tall thistles in the near foreground
for tx, ty, th in [(120, BAND, 64), (196, BAND, 48), (856, BAND, 58), (930, BAND, 44)]:
    d.line([(tx, ty), (tx, ty - th)], fill=PINE_D, width=3)
    d.line([(tx, ty - th // 2), (tx - 12, ty - th // 2 - 8)], fill=PINE_D, width=2)
    d.ellipse([tx - 9, ty - th - 16, tx + 9, ty - th + 4], fill=THISTLE_D)
    d.ellipse([tx - 6, ty - th - 22, tx + 6, ty - th - 8], fill=THISTLE)

# ---------- name band: the only text ----------
d.rectangle([X0, BAND, X1, Y1], fill=PINE_D)
d.line([(X0 + 44, BAND + 24), (X1 - 44, BAND + 24)], fill=GOLD, width=2)
name = "THISTLEDOWN"
size = 72
spacing = 12
while size > 30:
    f = SERIF_B(size)
    widths = [d.textlength(ch, font=f) for ch in name]
    total = sum(widths) + spacing * (len(name) - 1)
    if total <= (X1 - X0 - 90):
        break
    size -= 4
x = (W - total) / 2
for ch, wch in zip(name, widths):
    d.text((x, BAND + 36), ch, font=f, fill=CREAM)
    x += wch + spacing

# ---------- print grain (deterministic) ----------
grain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grain)
for _ in range(2200):
    gx = rng.randint(0, W - 1)
    gy = rng.randint(0, H - 1)
    ga = rng.randint(4, 12)
    gd.point((gx, gy), fill=(28, 30, 24, ga) if rng.random() < 0.5 else (255, 252, 240, ga))
img = Image.alpha_composite(img.convert("RGBA"), grain).convert("RGB")
d = ImageDraw.Draw(img)

# ---------- frame ----------
d.rectangle([X0, Y0, X1, Y1], outline=INK, width=3)
d.rectangle([16, 16, W - 16, H - 16], outline=INK, width=1)

os.makedirs("/output", exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes, {img.size}")
