#!/usr/bin/env python3
"""Draw the 24 Nov 2026 news front page, v3, 1024x1024 PNG.
Changes vs v2 (per 2026-11-25 top-3 review of 7 failed news-image days):
- 12 fine vector scenes: one per headline panel + 8 small panels.
- Per-story source + confidence tag on EVERY story, ALSO list included.
- "THE DAY IN NUMBERS" sidebar (5 Tuesday numbers).
- Headline #2 reframed to the Tuesday rally itself (Huang's return was
  Monday; it stays in the DATE CHECK box as excluded).
- Fonts stay serif masthead/headlines + clean sans body (no pixel/mono).
All facts verified by web search on 24-25 Nov 2026. Deterministic:
same bytes on every run. No network at run time.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (17, 17, 17)
RED = (158, 27, 27)
MUT = (90, 83, 72)
RULE = (120, 110, 95)
PANEL = (255, 253, 246)
GOLD = (176, 141, 43)
GOLDD = (141, 110, 20)
BLUE = (38, 84, 124)
GREEN = (46, 110, 62)
SKY = (198, 214, 224)
SAND = (233, 227, 211)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

OUT_WORK = "/home/hatch/workspace/makefun-news-image/news-image-20261124/work/entry.png"
OUT_REPO = "/home/hatch/workspace/makefun-news-image/news-image-20261124/repo/entry.png"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, font, width):
    if draw.textlength(text, font=font) <= width:
        return text
    while text and draw.textlength(text + "…", font=font) > width:
        text = text[:-1]
    return text + "…" if text else ""


def star(cx, cy, r_out, r_in, n=8):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 16  # margin


# ---------- vector scenes (each draws inside its box) ----------
def scene_gaza(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SAND)
    base = y1 - 6
    for bx, bh in [(0, 52), (18, 68), (38, 44), (58, 74), (78, 58)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 16, base], fill=INK)
        for wy in range(base - bh + 6, base - 4, 10):
            d.rectangle([x0 + bx + 4, wy, x0 + bx + 7, wy + 3], fill=SAND)
    cx, cy = x1 - 26, y0 + 24
    d.polygon(star(cx, cy, 16, 7), fill=(214, 120, 30))
    d.polygon(star(cx, cy, 8, 3.5), fill=RED)
    for sx, sy, r in [(x0 + 30, y0 + 16, 4), (x0 + 44, y0 + 10, 3), (x0 + 58, y0 + 18, 3)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 110, 95))
    d.line([(x0, base), (x1, base)], fill=INK, width=1)


def scene_shares(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 238, 228))
    base = y1 - 12
    for bx, bh, col in [(12, 30, RED), (34, 48, GOLD), (56, 66, BLUE), (78, 86, GREEN)]:
        d.rectangle([x0 + bx, base - bh, x0 + bx + 16, base], fill=col)
    d.line([(x0 + 8, base - 24), (x0 + 34, base - 44), (x0 + 58, base - 58),
            (x0 + 96, base - 82)], fill=RED, width=3)
    d.polygon([(x0 + 96, base - 82), (x0 + 84, base - 80), (x0 + 94, base - 70)], fill=RED)
    d.line([(x0, base), (x1, base)], fill=INK, width=1)


def scene_jets(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.ellipse([x0 + 8, y1 - 26, x0 + 52, y1 - 6], fill=GREEN)
    d.polygon([(x0 + 14, y1 - 14), (x0 + 26, y1 - 30), (x0 + 38, y1 - 14)], fill=(38, 90, 50))
    d.line([(x0, y1 - 16), (x1, y1 - 16)], fill=BLUE, width=1)
    jx, jy = x0 + 62, y0 + 26
    d.polygon([(jx, jy + 6), (jx + 30, jy), (jx + 36, jy + 6), (jx + 30, jy + 12)], fill=INK)
    d.polygon([(jx + 12, jy + 6), (jx + 22, jy - 8), (jx + 26, jy + 6)], fill=INK)
    d.line([(jx - 2, jy + 4), (x0 + 8, jy + 14)], fill=(255, 255, 255), width=2)
    d.line([(jx - 2, jy + 10), (x0 + 14, jy + 18)], fill=(255, 255, 255), width=1)
    tx, ty = x0 + 10, y0 + 8
    d.polygon([(tx + 8, ty), (tx + 18, ty + 16), (tx - 2, ty + 16)], outline=RED, width=2)
    d.text((tx + 5, ty + 4), "!", font=F(SANSB, 10), fill=RED)


def scene_gold(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(240, 236, 220))
    d.polygon([(x0 + 14, y1 - 34), (x0 + 20, y1 - 46), (x0 + 62, y1 - 46), (x0 + 68, y1 - 34)],
              fill=(201, 162, 39))
    d.polygon([(x0 + 24, y1 - 46), (x0 + 30, y1 - 58), (x0 + 56, y1 - 58), (x0 + 62, y1 - 46)],
              fill=(226, 186, 64))
    d.polygon([(x0 + 32, y1 - 58), (x0 + 36, y1 - 68), (x0 + 50, y1 - 68), (x0 + 54, y1 - 58)],
              fill=(201, 162, 39))
    f_dollar = F(SERIF, 34)
    d.text((x0 + 38, y0 + 8), "$", font=f_dollar, fill=GOLDD)
    d.line([(x0 + 88, y0 + 34), (x0 + 88, y0 + 14)], fill=RED, width=3)
    d.polygon([(x0 + 88, y0 + 10), (x0 + 82, y0 + 20), (x0 + 94, y0 + 20)], fill=RED)


def scene_car(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 230, 222))
    d.polygon([(x0 + 6, y1 - 26), (x0 + 12, y1 - 36), (x0 + 22, y1 - 40),
               (x0 + 40, y1 - 40), (x0 + 48, y1 - 26)], fill=RED)
    d.rectangle([x0 + 4, y1 - 28, x0 + 54, y1 - 18], fill=RED)
    d.polygon([(x0 + 16, y1 - 37), (x0 + 24, y1 - 38), (x0 + 34, y1 - 38), (x0 + 40, y1 - 29)],
              fill=SKY)
    for wx in (x0 + 14, x0 + 42):
        d.ellipse([wx - 6, y1 - 20, wx + 6, y1 - 8], fill=INK)
        d.ellipse([wx - 2, y1 - 16, wx + 2, y1 - 12], fill=(240, 240, 240))
    d.line([(x0, y1 - 8), (x1, y1 - 8)], fill=RULE, width=1)


def scene_football(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 205))
    d.line([(x0 + 8, y0 + 10), (x0 + 8, y1 - 24)], fill=(255, 255, 255), width=3)
    d.line([(x0 + 8, y0 + 10), (x0 + 34, y0 + 10)], fill=(255, 255, 255), width=3)
    d.line([(x0 + 34, y0 + 10), (x0 + 34, y1 - 24)], fill=(255, 255, 255), width=3)
    for ny in range(y0 + 16, y1 - 24, 8):
        d.line([(x0 + 8, ny), (x0 + 34, ny)], fill=(255, 255, 255), width=1)
    cx, cy = x0 + 38, y1 - 22
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(cx, cy - 5), (cx + 5, cy - 1), (cx + 3, cy + 5), (cx - 3, cy + 5), (cx - 5, cy - 1)],
              fill=INK)


def scene_rocket(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(200, 212, 226))
    for sx, sy in [(x0 + 8, y0 + 10), (x0 + 48, y0 + 8), (x0 + 44, y0 + 26)]:
        d.line([(sx - 2, sy), (sx + 2, sy)], fill=(255, 255, 255), width=1)
        d.line([(sx, sy - 2), (sx, sy + 2)], fill=(255, 255, 255), width=1)
    cx = x0 + 29
    d.polygon([(cx - 6, y1 - 18), (cx + 6, y1 - 18), (cx, y1 - 6)], fill=(214, 120, 30))
    d.polygon([(cx - 3, y1 - 18), (cx + 3, y1 - 18), (cx, y1 - 10)], fill=(232, 190, 60))
    d.rectangle([cx - 8, y0 + 22, cx + 8, y1 - 18], fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(cx - 8, y0 + 22), (cx, y0 + 8), (cx + 8, y0 + 22)], fill=RED)
    d.ellipse([cx - 4, y0 + 30, cx + 4, y0 + 38], fill=BLUE, outline=INK, width=1)
    d.polygon([(cx - 8, y1 - 30), (cx - 16, y1 - 16), (cx - 8, y1 - 18)], fill=RED)
    d.polygon([(cx + 8, y1 - 30), (cx + 16, y1 - 16), (cx + 8, y1 - 18)], fill=RED)


def scene_tower(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 230, 222))
    cx = x0 + 29
    d.polygon([(cx, y0 + 10), (cx + 8, y1 - 14), (cx - 8, y1 - 14)], fill=INK)
    for by in (y0 + 24, y0 + 36, y0 + 48):
        d.line([(cx - 7, by), (cx + 7, by)], fill=(232, 230, 222), width=2)
    for r in (10, 16, 22):
        d.arc([cx - r, y0 + 10 - r, cx + r, y0 + 10 + r], start=-60, end=60, fill=RED, width=2)
    d.ellipse([cx - 2, y0 + 8, cx + 2, y0 + 12], fill=RED)
    d.line([(x0 + 6, y1 - 12), (x0 + 52, y1 - 12)], fill=INK, width=1)


def scene_tennis(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 205))
    d.ellipse([x0 + 6, y0 + 8, x0 + 30, y0 + 34], outline=INK, width=2)
    d.line([(x0 + 14, y0 + 16), (x0 + 26, y0 + 28)], fill=INK, width=1)
    d.line([(x0 + 28, y0 + 32), (x0 + 40, y0 + 52)], fill=INK, width=3)
    cx, cy = x0 + 38, y1 - 20
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(190, 205, 60), outline=INK, width=1)
    d.arc([cx - 11, cy - 11, cx + 11, cy + 11], start=200, end=340, fill=(255, 255, 255), width=2)
    d.arc([cx - 11, cy - 11, cx + 11, cy + 11], start=20, end=160, fill=(255, 255, 255), width=2)


def scene_chess(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 230, 222))
    bx0, by0, cs = x0 + 8, y0 + 10, 14
    for r in range(2):
        for c in range(2):
            col = (235, 225, 205) if (r + c) % 2 == 0 else INK
            d.rectangle([bx0 + c * cs, by0 + r * cs, bx0 + (c + 1) * cs, by0 + (r + 1) * cs],
                        fill=col, outline=INK, width=1)
    px, py = x0 + 38, y0 + 22
    d.ellipse([px - 5, py - 8, px + 5, py + 2], fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(px - 3, py + 2), (px + 3, py + 2), (px + 7, py + 16), (px - 7, py + 16)],
              fill=(255, 255, 255), outline=INK)
    d.rectangle([px - 8, py + 16, px + 8, py + 19], fill=(255, 255, 255), outline=INK)
    px2, py2 = x0 + 20, y1 - 22
    d.ellipse([px2 - 4, py2 - 6, px2 + 4, py2 + 2], fill=INK)
    d.polygon([(px2 - 3, py2 + 2), (px2 + 3, py2 + 2), (px2 + 6, py2 + 12), (px2 - 6, py2 + 12)],
              fill=INK)


def scene_bitcoin(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 230, 222))
    cx, cy = x0 + 29, y0 + 37
    d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=(226, 186, 64), outline=GOLDD, width=2)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], outline=GOLDD, width=1)
    f_b = F(SANSB, 20)
    t = "B"
    tw = d.textlength(t, font=f_b)
    d.text((cx - tw / 2, cy - 12), t, font=f_b, fill=GOLDD)
    d.line([(cx - 8, cy - 14), (cx - 8, cy + 14)], fill=GOLDD, width=2)
    d.line([(cx + 8, cy - 14), (cx + 8, cy + 14)], fill=GOLDD, width=2)


def scene_phone(x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 230, 222))
    d.rectangle([x0 + 14, y0 + 8, x0 + 44, y1 - 8], fill=INK)
    d.rectangle([x0 + 17, y0 + 12, x0 + 41, y1 - 14], fill=SKY)
    d.line([(x0 + 24, y0 + 13), (x0 + 34, y0 + 13)], fill=INK, width=2)
    d.line([(x0 + 20, y1 - 22), (x0 + 26, y1 - 30), (x0 + 32, y1 - 26), (x0 + 38, y1 - 34)],
           fill=RED, width=2)
    d.line([(x0 + 20, y1 - 16), (x0 + 38, y1 - 16)], fill=(255, 255, 255), width=1)


# ---- top strip ----
f_top = F(SANSB, 11)
d.text((MX, 8), "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f_top, fill=INK)
r = "46 STORIES  ·  12 VECTOR SCENES  ·  6 REGIONS"
d.text((W - MX - d.textlength(r, font=f_top), 8), r, font=f_top, fill=RED)
d.line([(MX, 26), (W - MX, 26)], fill=RULE, width=1)

# ---- masthead ----
f_mast = F(SERIF, 46)
t = "THE WORLD IN ONE DAY"
d.text(((W - d.textlength(t, font=f_mast)) / 2, 30), t, font=f_mast, fill=INK)
f_date = F(SANSB, 21)
t2 = "TUESDAY  24  NOVEMBER  2026"
d.text(((W - d.textlength(t2, font=f_date)) / 2, 80), t2, font=f_date, fill=RED)
d.line([(MX, 106), (W - MX, 106)], fill=INK, width=2)
d.line([(MX, 109), (W - MX, 109)], fill=RULE, width=1)

# ---- UTC timeline ----
f_tl_lab = F(SANSB, 11)
f_tl_time = F(SANSB, 11)
f_tl_txt = F(SANS, 10)
d.text((MX, 116), "THE DAY IN UTC", font=f_tl_lab, fill=RED)
tl = [
    ("00:23", "Gold up to $3,645; Fed hike bet at 95%"),
    ("00:35", "Japan factory PMI 53.7, output and export orders up"),
    ("09:00", "Germany Ifo business climate, Nov, released"),
    ("13:15", "US ADP weekly jobs data, out"),
    ("14:00", "US Case-Shiller home prices, Sep"),
    ("15:00", "US consumer confidence, Nov, released"),
]
cw = (W - 2 * MX - 130) / 6
x = MX + 132
for tm, txt in tl:
    d.text((x, 116), tm, font=f_tl_time, fill=RED)
    lines = wrap(d, txt, f_tl_txt, cw - 4)
    yy = 131
    for ln in lines[:3]:
        d.text((x, yy), ln, font=f_tl_txt, fill=INK)
        yy += 12
    x += cw
d.line([(MX, 168), (W - MX, 168)], fill=RULE, width=1)

# ---- headline panels: 2 x 2, each with a scene strip on the right ----
HEAD = [
    ("1  MIDDLE EAST  ·  WAR", "ISRAELI STRIKE KILLS THREE IN GAZA",
     "An Israeli airstrike near a police outpost in Khan Younis killed at least three "
     "Palestinians on Tuesday and wounded five, health officials said.",
     "CONFIRMED  ·  REUTERS", scene_gaza),
    ("2  MARKETS  ·  ASIA", "ASIAN SHARES SURGE AS AI TRADE ROARS BACK",
     "Asian stocks leapt on Tuesday, tracking a Wall Street rebound as the AI trade "
     "revived. MSCI Asia-Pacific +4.6%; Nikkei +4.5%, Kospi +7.5%, Taiwan +9.1%.",
     "CONFIRMED  ·  REUTERS", scene_shares),
    ("3  ASIA  ·  SECURITY", "SEOUL WARNS ISLAND AS RUSSIAN JETS ENTER ZONE",
     "South Korea told Ulleung islanders to take shelter on Tuesday after Russian jets "
     "entered its air defence zone; the warning was lifted three minutes later.",
     "CONFIRMED  ·  REUTERS / AP", scene_jets),
    ("4  MARKETS  ·  ECONOMY", "GOLD REBOUNDS; FED HIKE BET AT 95%",
     "Gold edged up to $3,645 an ounce on Tuesday, extending a rebound from a 14-month "
     "low. Markets price a 95% chance of a 25-point Fed rate rise in December.",
     "CONFIRMED  ·  REUTERS", scene_gold),
]
hy, hh, hw, gap = 176, 118, 488, 16
SCENE_W = 116
f_kick = F(SANSB, 10)
f_ht = F(SERIF, 17)
f_hs = F(SANS, 11)
f_src = F(SANSB, 9)
for i, (kick, title, summ, src, scene) in enumerate(HEAD):
    px = MX + (i % 2) * (hw + gap)
    py = hy + (i // 2) * (hh + 8)
    d.rectangle([px, py, px + hw, py + hh], fill=PANEL, outline=RULE, width=1)
    d.rectangle([px, py, px + hw, py + 20], fill=RED)
    d.text((px + 8, py + 4), kick, font=f_kick, fill=(255, 255, 255))
    sx0 = px + hw - SCENE_W
    scene(sx0, py + 20, px + hw, py + hh)
    d.line([(sx0, py + 20), (sx0, py + hh)], fill=RULE, width=1)
    tw = hw - SCENE_W - 16
    ty = py + 24
    for ln in wrap(d, title, f_ht, tw)[:2]:
        d.text((px + 8, ty), ln, font=f_ht, fill=INK)
        ty += 20
    sy = ty + 2
    for ln in wrap(d, summ, f_hs, tw)[:3]:
        d.text((px + 8, sy), ln, font=f_hs, fill=INK)
        sy += 13
    d.text((px + 8, py + hh - 14), src, font=f_src, fill=MUT)
d.line([(MX, 428), (W - MX, 428)], fill=RULE, width=1)

# ---- small panels: 4 cols x 3 rows; 8 of them carry a scene strip ----
SMALL = [
    ("EUROPE · AUTOS", "VW opens pay talks; seeks two-year wage freeze",
     "REPORTED · REUTERS", scene_car),
    ("SPORT · FOOTBALL", "Champions League: Arsenal host Dortmund",
     "REPORTED · UEFA", scene_football),
    ("NORTH AMERICA · TECH", "Dell reports after the close; AI servers in focus",
     "REPORTED · REUTERS", None),
    ("NORTH AMERICA · SPACE", "SpaceX Falcon 9 launches classified USSF-266",
     "REPORTED · REUTERS", scene_rocket),
    ("ASIA · DEALS", "StarHub to buy M1 in $3.8bn all-share telecom deal",
     "CONFIRMED · REUTERS", scene_tower),
    ("ASIA · ECONOMY", "Japan factory activity expands in Nov; services soften",
     "OFFICIAL · S&P GLOBAL", None),
    ("SPORT · TENNIS", "Davis Cup opens in Bologna; Czechia face Canada",
     "REPORTED · ITF", scene_tennis),
    ("SPORT · CHESS", "Gukesh-Sindarov title match opens in Geneva",
     "REPORTED · FIDE", scene_chess),
    ("NORTH AMERICA · POLITICS", "Trump pardons turkeys Freedom and Feathers",
     "REPORTED · WHITE HOUSE", None),
    ("OCEANIA · HEALTH", "Ramsay members vote on Santé demerger",
     "REPORTED · REUTERS", None),
    ("MARKETS · CRYPTO", "Bitcoin steadies near $61,500 after weekend slide",
     "REPORTED · REUTERS", scene_bitcoin),
    ("ASIA · TECH", "Xiaomi reports after HK close",
     "REPORTED · REUTERS", scene_phone),
]
sy0, sh, sw, sgap = 436, 74, 242, 8
SSW = 58
f_sk = F(SANSB, 8)
f_st = F(SANSB, 11)
f_ss = F(SANS, 8)
for i, (kick, title, src, scene) in enumerate(SMALL):
    px = MX + (i % 4) * (sw + sgap)
    py = sy0 + (i // 4) * (sh + 6)
    d.rectangle([px, py, px + sw, py + sh], fill=PANEL, outline=RULE, width=1)
    if scene is not None:
        scene(px, py, px + SSW, py + sh)
        d.line([(px + SSW, py), (px + SSW, py + sh)], fill=RULE, width=1)
        tx0, tw = px + SSW + 6, sw - SSW - 12
    else:
        tx0, tw = px + 6, sw - 12
    d.text((tx0, py + 4), kick, font=f_sk, fill=RED)
    ty = py + 17
    for ln in wrap(d, title, f_st, tw)[:3]:
        d.text((tx0, ty), ln, font=f_st, fill=INK)
        ty += 13
    d.text((tx0, py + sh - 12), src, font=f_ss, fill=MUT)
d.line([(MX, 672), (W - MX, 672)], fill=RULE, width=1)

# ---- map + numbers + date check row ----
my0 = 680
f_sec = F(SANSB, 11)
d.text((MX, my0), "WHERE IT HAPPENED", font=f_sec, fill=RED)
d.text((MX + 452, my0), "THE DAY IN NUMBERS", font=f_sec, fill=RED)
d.text((MX + 640, my0), "DATE CHECK  —  LEFT OUT ON PURPOSE", font=f_sec, fill=RED)

# dotted world map: coarse land mask, 64 x 18 grid
LAND = [
"        ####  ##########                       ##################   ",
"   ######## #############  ###           #########################  ",
"  ########## ##############              ########################   ",
"   #########  ##########   ##            ###  ########  #########   ",
"    ######     ########     #             ##   ######    ####  ##    ",
"     ####       ######                   ###    ####      ##         ",
"      ##        ####    #               ####    ###                 ",
"                ###    ##             ######   ##    ##            ",
"                ##      #             #####         ####           ",
"                #       ##           ######        ######          ",
"                       ###          #######        #######          ",
"                       ##           ######          #####           ",
"                      ###            ####            ###            ",
"                       #             ###               #            ",
"                                     ##                              ",
"                                    ###                              ",
"                                     #                               ",
"                                                                    ",
]
map_x, map_y, map_w, map_h = MX, my0 + 18, 440, 92
cell_w = map_w / 64.0
cell_h = map_h / 18.0
for r, row in enumerate(LAND):
    for c, ch in enumerate(row):
        if ch == "#":
            cx = map_x + c * cell_w + cell_w / 2
            cy = map_y + r * cell_h + cell_h / 2
            d.ellipse([cx - 2.0, cy - 2.0, cx + 2.0, cy + 2.0], fill=(95, 85, 65))

def pin(n, lon, lat):
    # lon -180..180 -> x; lat 75..-60 -> y
    px = map_x + (lon + 180) / 360.0 * map_w
    py = map_y + (75 - lat) / 135.0 * map_h
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    f_pin = F(SANSB, 10)
    tw = d.textlength(str(n), font=f_pin)
    d.text((px - tw / 2, py - 7), str(n), font=f_pin, fill=(255, 255, 255))

pin(1, 34.5, 31.4)    # Gaza
pin(2, 127.0, 37.5)   # Seoul
pin(3, 103.8, 1.35)   # Singapore
pin(4, 139.7, 35.7)   # Tokyo
pin(5, 151.2, -33.9)  # Sydney
pin(6, -77.0, 38.9)   # Washington
pin(7, -120.6, 34.7)  # Vandenberg
pin(8, -52.8, 5.2)    # Kourou
f_mapleg = F(SANS, 8)
d.text((MX, my0 + 112),
       "Pins: 1 Gaza  2 Seoul  3 Singapore  4 Tokyo  5 Sydney  6 Washington  7 Vandenberg  8 Kourou",
       font=f_mapleg, fill=MUT)

# numbers sidebar
NUMBERS = [
    ("+4.6%", "MSCI Asia-Pacific, best day since Jul 31"),
    ("9.1%", "Taiwan shares jump; TSMC at daily limit"),
    ("$3,645", "Gold an ounce, up 0.4% off 14-month low"),
    ("95%", "Chance of Dec Fed hike, CME FedWatch"),
    ("81.5m", "Americans travelling for Thanksgiving"),
]
nx, nw = MX + 452, 176
f_num = F(SANSB, 15)
f_numlab = F(SANS, 9)
ny = my0 + 18
for num, lab in NUMBERS:
    d.text((nx, ny), num, font=f_num, fill=RED)
    ly = ny + 2
    for ln in wrap(d, lab, f_numlab, nw - 60)[:2]:
        d.text((nx + 58, ly), ln, font=f_numlab, fill=INK)
        ly += 11
    ny += 21

# date check box
bx, by, bw, bh = MX + 640, my0 + 18, W - MX - (MX + 640), 112
d.rectangle([bx, by, bx + bw, by + bh], fill=(255, 252, 240), outline=RED, width=2)
f_dc = F(SANS, 10)
f_dcb = F(SANSB, 10)
dc = [
    ("COP31 climate talks collapse, Antalya — Sun 22 Nov, not Tue.",),
    ("Vanuatu M6.5 quake, 02:40 UTC — Mon 23 Nov, not Tue.",),
    ("Nvidia's Huang reinstated as CEO; shares +31% — Mon 23 Nov.",),
    ("NATO AWACS aircraft for Poland announced — Mon 23 Nov.",),
    ("Ukraine sank Russian corvette off Libya — Sun 22 Nov.",),
    ("FIFA names 2031 Women's WC hosts — Mon 23 Nov.",),
    ("Charles 'reached out' to Meghan — Sat 21 Nov.",),
    ("NOT YET: US PCE inflation Wed 25 Nov; Korea rate call Thu.",),
]
yy = by + 6
for (line,) in dc:
    for ln in wrap(d, line, f_dc, bw - 12)[:2]:
        d.text((bx + 6, yy), ln, font=f_dc, fill=INK)
        yy += 12
    yy += 1

# ---- ALSO list, every item with source + confidence ----
ay0 = 806
d.text((MX, ay0), "ALSO ON TUESDAY 24 NOVEMBER 2026", font=f_sec, fill=RED)
d.line([(MX, ay0 + 16), (W - MX, ay0 + 16)], fill=INK, width=1)
ALSO = [
    ("Hong Kong lags Asia rally; Hang Seng flat", "RTRS", "REPORTED"),
    ("Analog Devices reports before the open", "RTRS", "REPORTED"),
    ("Medtronic reports before the open", "RTRS", "REPORTED"),
    ("Korea central bank seen hiking rates to 3.25%", "RTRS", "REPORTED"),
    ("US consumer confidence for Nov. out at 15:00 UTC", "RTRS", "OFFICIAL"),
    ("Thanksgiving travel peaks; 81.5m on the move", "AAA", "REPORTED"),
    ("Celtics, on four straight losses, face Wizards", "ESPN", "REPORTED"),
    ("Oilers host Golden Knights in Pacific clash", "NHL", "REPORTED"),
    ("Mavericks visit Nuggets; Flagg faces Jokic", "ESPN", "REPORTED"),
    ("Pistons visit Magic in NBA Cup play", "NBA", "REPORTED"),
    ("Treasury sells $70bn of 5-year notes", "RTRS", "OFFICIAL"),
    ("Bank of Canada's Macklem speaks", "RTRS", "OFFICIAL"),
    ("AustralianSuper backs Brookfield Reliance bid", "RTRS", "REPORTED"),
    ("Indian markets shut for Guru Nanak Jayanti", "RTRS", "REPORTED"),
    ("India may import 2m tonnes of sugar", "RTRS", "REPORTED"),
    ("Workday, Autodesk report after the close", "RTRS", "REPORTED"),
    ("Seoul subway talks; strike looms Wednesday", "YONHAP", "REPORTED"),
    ("Seoul court issues warrant for election official", "YONHAP", "REPORTED"),
    ("Amazon Leo satellites ride Ariane 6 from Kourou", "AFP", "REPORTED"),
    ("Russian Progress freighter lifts off for station", "TASS", "REPORTED"),
    ("CFP rankings out tonight; Georgia No. 1", "ESPN", "REPORTED"),
    ("Australia, England in 2nd T20I on Gold Coast", "ESPN", "REPORTED"),
    ("Nor'easter forms Tuesday; rain reaches Florida", "AP", "REPORTED"),
    ("Al-Nassr host Al Sadd in Asian Champions League", "AFC", "REPORTED"),
    ("Compass Group reports full-year results", "RTRS", "REPORTED"),
    ("Abercrombie & Fitch reports before the open", "RTRS", "REPORTED"),
    ("Couche-Tard reports after the Toronto close", "RTRS", "REPORTED"),
    ("Best Buy, Dollar Tree, Dick's test shoppers", "RTRS", "REPORTED"),
    ("Nutanix reports after the close", "RTRS", "REPORTED"),
    ("HP reports after the close; PC demand in focus", "RTRS", "REPORTED"),
]
f_al = F(SANS, 10)
f_alb = F(SANSB, 10)
f_tag = F(SANSB, 8)
col_w = (W - 2 * MX) / 3
for i, (item, src, conf) in enumerate(ALSO):
    col = i // 10
    row = i % 10
    ax = MX + col * col_w
    ay = ay0 + 22 + row * 15
    num = f"{17 + i}"
    d.text((ax, ay), num, font=f_alb, fill=RED)
    tag = f"{src} · {conf}"
    tag_w = d.textlength(tag, font=f_tag)
    d.text((ax + col_w - 4 - tag_w, ay + 1), tag, font=f_tag, fill=RED)
    text_w = col_w - 22 - tag_w - 10
    d.text((ax + 22, ay), trunc(d, item, f_al, text_w), font=f_al, fill=INK)

# ---- footer ----
fy = 992
d.line([(MX, fy - 6), (W - MX, fy - 6)], fill=RULE, width=1)
f_ft = F(SANS, 9)
foot = ("Every story here happened or was first reported on Tuesday 24 November 2026. "
        "Tags: CONFIRMED = confirmed by the source; REPORTED = reported, not independently "
        "confirmed; OFFICIAL = announced by the institution. Sources: Reuters, AP, AFP, Yonhap, "
        "TASS, UEFA, FIDE, ITF, White House, S&P Global, CME FedWatch, AAA, ESPN, NBA, NHL, AFC, "
        "company calendars, market data.")
for ln in wrap(d, foot, f_ft, W - 2 * MX):
    d.text((MX, fy), ln, font=f_ft, fill=MUT)
    fy += 11

img.save(OUT_WORK, optimize=True)
img.save(OUT_REPO, optimize=True)
print("saved")
