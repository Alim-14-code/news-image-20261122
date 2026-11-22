#!/usr/bin/env python3
"""Render 'THE WORLD TODAY' - news-image-20261122 round 4.

Draws the whole front page procedurally with Pillow (stdlib-free render
program; the entry program main.py only copies entry.png).
Every story on the page was verified from live wires on 22 Nov 2026:
first reported, or with a genuine development, on Sunday 22 Nov 2026.
See BUILD-NOTES.md for the verified story list with outlets.
Deterministic: no randomness, no timestamps, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 232)
INK = (22, 22, 22)
RED = (139, 26, 26)
RED2 = (178, 34, 34)
NAVY = (27, 42, 74)
CREAM = (250, 244, 224)
GOLD = (176, 141, 44)
TEAL = (13, 105, 104)
BROWN = (122, 84, 52)
PURPLE = (94, 64, 128)
GREY = (64, 64, 66)
BLUE = (31, 68, 120)
GREEN = (34, 102, 58)
OLIVE = (106, 106, 40)
MAROON = (122, 32, 48)
SEA = (214, 228, 232)
LAND = (232, 219, 190)
LAND_EDGE = (168, 148, 118)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, s, font):
    return draw.textlength(s, font=font)


def fit_font(draw, s, path, size, max_w, min_size=7):
    while size > min_size and tw(draw, s, F(path, size)) > max_w:
        size -= 1
    return F(path, size)


def wrap(s, font, max_w, draw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(draw, t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading=None):
    if leading is None:
        leading = font.size + 2
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, bg, fg=(255, 255, 255), size=10, pad=5):
    f = F(SANS_B, size)
    w = int(tw(draw, text, f)) + pad * 2
    h = size + 7
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad, y + 3), text, font=f, fill=fg)
    return w


TAG_COLORS = {
    "ONGOING": (176, 96, 16),
    "REPORTED": (34, 102, 58),
    "CLAIM": (178, 34, 34),
    "FORECAST": (94, 64, 128),
}


def tag_chip(draw, x, y, tag, size=10):
    return chip(draw, x, y, tag, TAG_COLORS[tag], size=size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 8], fill=RED)
f_title = F(SERIF_B, 58)
t = "THE WORLD TODAY"
d.text(((W - tw(d, t, f_title)) / 2, 12), t, font=f_title, fill=RED)
f_date = F(SANS_B, 17)
t = "SUNDAY, 22 NOVEMBER 2026"
d.text(((W - tw(d, t, f_date)) / 2, 72), t, font=f_date, fill=INK)
d.line([12, 96, W - 12, 96], fill=RED, width=2)
f_claim = F(SANS_B, 11)
t = "EVERY ONE DATED SUNDAY 22 NOVEMBER 2026  ·  34 STORIES  ·  ALL VERIFIED TODAY"
d.text(((W - tw(d, t, f_claim)) / 2, 100), t, font=f_claim, fill=RED)

# ------------------------------------------------------------ sub-headline
d.rectangle([0, 118, W, 142], fill=NAVY)
f_sub = F(SANS_B, 14)
t = "COP31's final text lands at dawn  •  Iran claims strikes on US bases in Bahrain  •  186 drones over Ukraine overnight"
f_sub = fit_font(d, t, SANS_B, 14, W - 24, 11)
d.text(((W - tw(d, t, f_sub)) / 2, 124), t, font=f_sub, fill=CREAM)

# -------------------------------------------------------------- number strip
STRIP = [
    ("0", "COP31 DEALS AGREED"),
    ("186", "DRONES FIRED AT UKRAINE"),
    ("2", "US RADARS 'HIT' BY IRAN"),
    ("16", "DEAD IN MANIPUR"),
    ("129", "BODIES FOUND IN GAZA"),
    ("5,700", "HONG KONG VOTERS"),
]
sx, sy, sw, sh = 12, 148, (W - 24) // 6, 52
d.rectangle([0, sy, W, sy + sh], fill=RED)
for i, (num, lab) in enumerate(STRIP):
    cx = sx + i * sw
    if i:
        d.line([cx, sy + 6, cx, sy + sh - 6], fill=(200, 120, 120), width=1)
    fn = fit_font(d, num, SANS_B, 30, sw - 10, 18)
    d.text((cx + (sw - tw(d, num, fn)) / 2, sy + 2), num, font=fn, fill=CREAM)
    fl = fit_font(d, lab, SANS_B, 10, sw - 8, 8)
    d.text((cx + (sw - tw(d, lab, fl)) / 2, sy + 36), lab, font=fl, fill=(255, 220, 200))

# --------------------------------------------------------------- region bar
REGIONS = [
    ("EUROPE", 9, (31, 68, 120)),
    ("MIDDLE EAST", 5, (178, 34, 34)),
    ("ASIA", 5, (13, 105, 104)),
    ("AMERICAS", 8, (176, 141, 44)),
    ("AFRICA", 2, (34, 102, 58)),
    ("WORLD", 5, (94, 64, 128)),
]
rx, ry, rw = 12, 206, W - 24
x = rx
for name, n, col in REGIONS:
    wseg = rw * n // 34
    d.rectangle([x, ry, x + wseg - 1, ry + 15], fill=col)
    lab = "%s %d" % (name, n)
    fl = fit_font(d, lab, SANS_B, 9, wseg - 4, 7)
    d.text((x + (wseg - tw(d, lab, fl)) / 2, ry + 3), lab, font=fl,
           fill=(255, 255, 255))
    x += wseg

# ---------------------------------------------------------------- hero art
def hero_cop31(g, x0, y0, w, h):
    """COP31 hall: warm sunset, dense delegates, globe, thermometer, clock."""
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 176, 96))
    # tall windows with sunset sky
    for i in range(4):
        wx = x0 + 14 + i * (w - 28) // 4
        ww = (w - 28) // 4 - 8
        g.rectangle([wx, y0 + 8, wx + ww, y0 + 62], fill=(246, 196, 110))
        g.rectangle([wx, y0 + 8, wx + ww, y0 + 62], outline=(150, 90, 30), width=2)
        g.ellipse([wx + ww // 2 - 9, y0 + 34, wx + ww // 2 + 9, y0 + 52],
                  fill=(240, 120, 40))
        g.line([wx + 4, y0 + 46, wx + ww - 4, y0 + 46], fill=(200, 120, 50), width=2)
    # back wall band with flags
    g.rectangle([x0, y0 + 64, x0 + w, y0 + 78], fill=(120, 60, 30))
    flag_cols = [(178, 34, 34), (31, 68, 120), (34, 102, 58), (240, 200, 60),
                 (94, 64, 128), (220, 120, 40), (13, 105, 104), (200, 60, 90)]
    for i in range(12):
        fx = x0 + 10 + i * ((w - 20) // 12)
        g.rectangle([fx, y0 + 66, fx + 12, y0 + 76],
                    fill=flag_cols[i % len(flag_cols)])
    # big globe, left (fully above the desk)
    gx, gy, gr = x0 + 52, y0 + 70, 20
    g.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 110, 170))
    g.ellipse([gx - 12, gy - 9, gx - 1, gy + 2], fill=(74, 150, 90))
    g.ellipse([gx + 3, gy + 5, gx + 14, gy + 14], fill=(74, 150, 90))
    g.ellipse([gx - 6, gy - 17, gx + 6, gy - 8], fill=(74, 150, 90))
    g.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(40, 60, 90), width=2)
    g.rectangle([gx - 3, gy + gr, gx + 3, gy + gr + 6], fill=(90, 60, 30))
    g.rectangle([gx - 13, gy + gr + 6, gx + 13, gy + gr + 8], fill=(90, 60, 30))
    # thermometer screen, right
    tx = x0 + w - 78
    g.rectangle([tx, y0 + 62, tx + 64, y0 + 92], fill=(30, 30, 34))
    g.rectangle([tx + 4, y0 + 66, tx + 60, y0 + 88], outline=(240, 200, 60), width=1)
    for j in range(5):
        bh = 3 + j * 3
        g.rectangle([tx + 8 + j * 10, y0 + 84 - bh, tx + 15 + j * 10, y0 + 84],
                    fill=(240, 90, 40) if j > 2 else (240, 200, 60))
    g.text((tx + 6, y0 + 64), "35%", font=F(SANS_B, 10), fill=(255, 220, 120))
    # wall clock above globe
    cx, cy, cr = x0 + w // 2, y0 + 72, 11
    g.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(250, 244, 224),
              outline=(60, 40, 20), width=2)
    g.line([cx, cy, cx, cy - 7], fill=INK, width=2)
    g.line([cx, cy, cx + 5, cy + 2], fill=INK, width=2)
    # long desk arc with delegates (dark silhouettes, heads on shoulders)
    g.ellipse([x0 + 8, y0 + h - 22, x0 + w - 8, y0 + h + 30], fill=(96, 52, 26))
    g.ellipse([x0 + 16, y0 + h - 16, x0 + w - 16, y0 + h + 22], fill=(150, 96, 52))
    for i in range(11):
        px = x0 + 22 + i * ((w - 44) // 10)
        py = y0 + h - 14 + (0 if i % 2 == 0 else 3)
        g.ellipse([px - 4, py - 5, px + 4, py + 3], fill=(40, 32, 28))
        g.rounded_rectangle([px - 9, py + 1, px + 9, py + 13], radius=4,
                            fill=(38, 44, 66) if i % 3 else (66, 38, 44))
        g.rectangle([px - 7, py + 11, px + 7, py + 13], fill=(250, 244, 224))
    # papers on desks
    for i in range(6):
        px = x0 + 30 + i * ((w - 60) // 5)
        g.rectangle([px, y0 + h - 6, px + 12, y0 + h - 2], fill=(250, 244, 224))
    # clip the desk arc to the art box (panel fill below y0+h)
    g.rectangle([x0, y0 + h, x0 + w, y0 + h + 30], fill=(255, 253, 247))


def hero_ukraine(g, x0, y0, w, h):
    """Ukraine night: dense skyline, drone trails, fires, searchlights."""
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(16, 24, 52))
    # stars
    for sx, sy in [(18, 12), (52, 26), (96, 10), (140, 22), (188, 8), (230, 28),
                   (272, 14), (306, 30), (70, 40), (160, 38), (250, 44), (30, 52)]:
        g.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=(220, 220, 200))
    # moon
    g.ellipse([x0 + w - 44, y0 + 10, x0 + w - 20, y0 + 34], fill=(240, 236, 210))
    # drone trails (dotted arcs)
    for k, (ty, tcol) in enumerate([(26, (255, 220, 120)), (44, (255, 190, 90)),
                                    (62, (255, 220, 120))]):
        for i in range(0, w - 20, 8):
            g.ellipse([x0 + 10 + i, y0 + ty + (i // 24) % 2 * 3,
                       x0 + 13 + i, y0 + ty + 3 + (i // 24) % 2 * 3], fill=tcol)
    # skyline: dense buildings with lit windows
    import math as _m
    bx = x0
    heights = [58, 74, 66, 88, 60, 96, 70, 82, 56, 92, 64, 78, 60, 86, 68]
    bi = 0
    while bx < x0 + w - 8:
        bw = 20 + (bi * 7) % 14
        bh = heights[bi % len(heights)]
        g.rectangle([bx, y0 + h - bh, bx + bw, y0 + h], fill=(10, 14, 34))
        for wy in range(y0 + h - bh + 6, y0 + h - 6, 10):
            for wx in range(bx + 3, bx + bw - 3, 7):
                if (wx * 7 + wy * 3 + bi) % 5 < 3:
                    g.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 210, 110))
        bx += bw + 2
        bi += 1
    # fires with smoke
    for fx, fy, fs in [(x0 + 52, y0 + h - 8, 12), (x0 + 168, y0 + h - 8, 15),
                       (x0 + 268, y0 + h - 8, 11)]:
        g.ellipse([fx - fs, fy - fs // 2, fx + fs, fy + 4], fill=(240, 110, 30))
        g.ellipse([fx - fs // 2, fy - fs, fx + fs // 2, fy], fill=(255, 190, 60))
        g.ellipse([fx - 8, fy - fs - 14, fx + 8, fy - fs + 2], fill=(70, 70, 80))
        g.ellipse([fx - 5, fy - fs - 26, fx + 9, fy - fs - 10], fill=(90, 90, 100))
    # searchlight beams
    g.polygon([(x0 + 120, y0 + h), (x0 + 96, y0 + 18), (x0 + 108, y0 + 18)],
              fill=(200, 200, 150))
    g.polygon([(x0 + 250, y0 + h), (x0 + 282, y0 + 30), (x0 + 292, y0 + 30)],
              fill=(200, 200, 150))


def hero_sparta(g, x0, y0, w, h):
    """Sparta II: tanker ablaze at dawn, smoke, waves, rescue boat."""
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(58, 84, 110))
    # dawn sky band
    g.rectangle([x0, y0, x0 + w, y0 + 34], fill=(232, 160, 90))
    g.ellipse([x0 + w - 52, y0 + 6, x0 + w - 28, y0 + 30], fill=(250, 210, 130))
    # distant coast
    g.polygon([(x0, y0 + 52), (x0 + 60, y0 + 38), (x0 + 130, y0 + 50),
               (x0 + 200, y0 + 40), (x0 + w, y0 + 52), (x0 + w, y0 + 58),
               (x0, y0 + 58)], fill=(44, 66, 52))
    # sea
    g.rectangle([x0, y0 + 58, x0 + w, y0 + h], fill=(32, 56, 84))
    for wy in range(y0 + 66, y0 + h - 4, 12):
        for wx in range(x0 + 6, x0 + w - 10, 26):
            g.line([wx, wy, wx + 14, wy], fill=(90, 130, 160), width=2)
    # tanker hull
    hy = y0 + h - 52
    g.polygon([(x0 + 18, hy), (x0 + w - 18, hy), (x0 + w - 34, hy + 22),
               (x0 + 34, hy + 22)], fill=(24, 24, 28))
    g.rectangle([x0 + 30, hy - 6, x0 + w - 30, hy], fill=(120, 30, 30))
    # superstructure
    g.rectangle([x0 + w - 96, hy - 34, x0 + w - 52, hy - 6], fill=(220, 220, 210))
    for wy in range(hy - 30, hy - 8, 8):
        g.rectangle([x0 + w - 90, wy, x0 + w - 58, wy + 4], fill=(40, 60, 90))
    # funnel with smoke
    g.rectangle([x0 + 60, hy - 26, x0 + 76, hy - 6], fill=(200, 60, 40))
    # big flames midship
    for fx, fs in [(x0 + 130, 22), (x0 + 160, 30), (x0 + 190, 20)]:
        g.ellipse([fx - fs, hy - fs - 8, fx + fs, hy + 2], fill=(240, 110, 30))
        g.ellipse([fx - fs // 2, hy - fs - 20, fx + fs // 2, hy - 4],
                  fill=(255, 190, 60))
    # smoke columns (kept inside the art box: top >= y0)
    for sx in [x0 + 140, x0 + 175]:
        g.ellipse([sx - 12, hy - 38, sx + 12, hy - 14], fill=(60, 60, 66))
        g.ellipse([sx - 8, hy - 56, sx + 10, hy - 34], fill=(80, 80, 88))
    g.ellipse([x0 + 60, hy - 34, x0 + 76, hy - 18], fill=(70, 70, 78))
    # listing: waterline tilt marks
    g.line([x0 + 18, hy + 22, x0 + w - 18, hy + 22], fill=(200, 220, 230), width=1)
    # rescue boat with searchlight
    bx, by = x0 + w - 150, y0 + h - 18
    g.polygon([(bx, by), (bx + 44, by), (bx + 38, by + 8), (bx + 6, by + 8)],
              fill=(220, 120, 30))
    g.rectangle([bx + 12, by - 8, bx + 28, by], fill=(240, 240, 230))
    g.polygon([(bx + 40, by - 4), (bx + 70, by - 16), (bx + 70, by - 12)],
              fill=(240, 240, 180))

# ---------------------------------------------------------------- hero panels
HEROES = [
    dict(art=hero_cop31, loc="1 · ANTALYA, TURKEY", tag="ONGOING",
         head="COP31 REACHES DEAL AT DAWN",
         summ="Final 10-page text out at 02:00; vote due 06:00 GMT, now 11:00. "
              "No fossil-fuel mention. 35% clean power by 2035.",
         src="Reuters · Guardian · The Curtain"),
    dict(art=hero_ukraine, loc="2 · KYIV, UKRAINE", tag="REPORTED",
         head="186 DRONES OVER UKRAINE OVERNIGHT",
         summ="Russia launches 186 drones from 18:00; Kyiv downs 161 by 08:00. "
              "18 places hit; fires burn into the morning.",
         src="Ukrainian Air Force"),
    dict(art=hero_sparta, loc="3 · GULF OF FINLAND", tag="ONGOING",
         head="TANKER SPARTA II STILL BURNING",
         summ="Struck Sat 09:00, fire burns through the night off Loviisa. "
              "16 crew evacuated; ship anchored, listing.",
         src="Reuters"),
]
hx, hy, hw, hh, hg = 12, 226, 326, 204, 8
for i, hh_ in enumerate(HEROES):
    x0 = hx + i * (hw + hg)
    d.rectangle([x0, hy, x0 + hw, hy + hh], fill=(255, 253, 247),
                outline=(150, 130, 110), width=1)
    d.rectangle([x0, hy, x0 + hw, hy + 20], fill=INK)
    fl = F(SANS_B, 10)
    d.text((x0 + 6, hy + 4), hh_["loc"], font=fl, fill=CREAM)
    tw_ = tag_chip(d, x0 + hw - 74, hy + 3, hh_["tag"], size=9)
    hh_["art"](d, x0 + 4, hy + 24, hw - 8, 108)
    fh = fit_font(d, hh_["head"], SANS_B, 15, hw - 12, 12)
    y = hy + 136
    d.text((x0 + 6, y), hh_["head"], font=fh, fill=INK)
    fs = F(SANS, 11)
    slines = wrap(hh_["summ"], fs, hw - 12, d)[:2]
    y = draw_lines(d, x0 + 6, y + 19, slines, fs, (60, 60, 60), leading=12)
    d.line([x0 + 6, hy + hh - 16, x0 + hw - 6, hy + hh - 16],
           fill=(200, 180, 150), width=1)
    fc = F(SANS, 9)
    d.text((x0 + 6, hy + hh - 13), "SOURCE: " + hh_["src"], font=fc,
           fill=(110, 90, 70))

# -------------------------------------------------------------- by the clock
CLOCK = [
    ("04:05", "Myanmar quake"),
    ("08:30", "Gaza: 129 bodies"),
    ("11:00", "Verstappen wins GP"),
    ("13:00", "COP31 vote slips"),
    ("14:34", "Bayelsa toll 24"),
    ("16:29", "Hamas seeks talks"),
]
cy0, chh = 438, 26
d.rectangle([0, cy0, W, cy0 + chh], fill=(40, 40, 44))
d.text((12, cy0 + 6), "BY THE CLOCK · WIB", font=F(SANS_B, 11), fill=GOLD)
cx = 150
cw = (W - 150 - 12) // 6
for tm, tx in CLOCK:
    ft = F(SANS_B, 9)
    tw_tm = tw(d, tm + "  ", ft)
    f2 = fit_font(d, tx, SANS, 9, cw - tw_tm - 6, 8)
    d.text((cx, cy0 + 7), tm, font=ft, fill=(255, 220, 120))
    d.text((cx + tw_tm, cy0 + 7), tx, font=f2, fill=CREAM)
    cx += cw

# ---------------------------------------------------------- secondary art
def sec_iran(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(24, 20, 44))
    for sx, sy in [(12, 8), (44, 16), (90, 6), (130, 14), (168, 8)]:
        g.ellipse([x0 + sx, y0 + sy, x0 + sx + 2, y0 + sy + 2], fill=(220, 220, 200))
    # radar dish
    g.pieslice([x0 + 18, y0 + 18, x0 + 58, y0 + 58], 200, 340, fill=(180, 180, 190))
    g.line([x0 + 38, y0 + 48, x0 + 38, y0 + h - 8], fill=(150, 150, 160), width=3)
    g.line([x0 + 28, y0 + h - 8, x0 + 48, y0 + h - 8], fill=(150, 150, 160), width=3)
    # missile trails
    for mx in [80, 110, 140]:
        for i in range(0, 34, 6):
            g.ellipse([x0 + mx + i // 3, y0 + 44 - i, x0 + mx + 3 + i // 3,
                       y0 + 47 - i], fill=(255, 200, 90))
    # base buildings
    for bx, bw, bh in [(x0 + 96, 26, 18), (x0 + 126, 30, 26), (x0 + 158, 28, 14)]:
        g.rectangle([bx, y0 + h - bh, bx + bw, y0 + h], fill=(12, 12, 26))
        g.rectangle([bx + 4, y0 + h - bh + 4, bx + bw - 4, y0 + h - bh + 8],
                    fill=(255, 210, 110))
    g.ellipse([x0 + 132, y0 + 52, x0 + 152, y0 + 72], fill=(240, 110, 30))


def sec_manipur(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 232, 226))
    g.rectangle([x0, y0, x0 + w, y0 + 16], fill=(13, 105, 104))
    g.text((x0 + 6, y0 + 3), "WARD", font=F(SANS_B, 10), fill=(255, 255, 255))
    # hospital beds row
    for i in range(3):
        bx = x0 + 12 + i * 58
        by = y0 + 34
        g.rectangle([bx, by + 18, bx + 48, by + 24], fill=(90, 110, 130))
        g.rectangle([bx, by + 24, bx + 4, by + 40], fill=(60, 80, 100))
        g.rectangle([bx + 44, by + 24, bx + 48, by + 40], fill=(60, 80, 100))
        g.ellipse([bx + 4, by + 6, bx + 14, by + 16], fill=(240, 200, 170))
        g.rounded_rectangle([bx + 12, by + 12, bx + 46, by + 20], radius=3,
                            fill=(240, 240, 235))
        g.line([bx + 40, by - 6, bx + 40, by + 12], fill=(120, 120, 120), width=1)
        g.rectangle([bx + 36, by - 6, bx + 44, by + 4], fill=(220, 240, 255))
    g.rectangle([x0 + w - 24, y0 + 22, x0 + w - 8, y0 + 38], fill=(255, 255, 255))
    g.rectangle([x0 + w - 20, y0 + 25, x0 + w - 12, y0 + 35], fill=(178, 34, 34))
    g.rectangle([x0 + w - 17, y0 + 22, x0 + w - 15, y0 + 38], fill=(178, 34, 34))
    g.line([x0, y0 + h - 10, x0 + w, y0 + h - 10], fill=(150, 170, 160), width=1)


def sec_myanmar(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 232, 214))
    # seismograph paper
    g.rectangle([x0 + 8, y0 + 10, x0 + w - 8, y0 + 52], fill=(255, 255, 255),
                outline=(120, 100, 80), width=1)
    pts = []
    import math as _m
    for i in range(0, w - 16):
        amp = 2 if i < 60 else (14 if 60 <= i < 110 else 3)
        yy = y0 + 31 + int(amp * _m.sin(i * 0.55) * (1 if i % 3 else -1))
        pts.append((x0 + 8 + i, yy))
    g.line(pts, fill=(178, 34, 34), width=2)
    g.text((x0 + 12, y0 + 13), "M4.1  02:35 IST", font=F(SANS_B, 9), fill=(120, 60, 30))
    # cracked ground + tilted buildings
    g.rectangle([x0, y0 + 56, x0 + w, y0 + h], fill=(188, 164, 132))
    for bx, tilt in [(x0 + 16, -4), (x0 + 70, 5), (x0 + 128, -3)]:
        g.polygon([(bx, y0 + h), (bx + 6 + tilt, y0 + 62), (bx + 34 + tilt, y0 + 62),
                   (bx + 40, y0 + h)], fill=(140, 110, 80))
        for wy in range(y0 + 68, y0 + h - 4, 8):
            g.rectangle([bx + 8, wy, bx + 14, wy + 4], fill=(60, 50, 40))
    g.line([(x0 + 60, y0 + 58), (x0 + 76, y0 + 68), (x0 + 70, y0 + 76),
            (x0 + 88, y0 + h)], fill=(60, 40, 20), width=2)


def sec_hk(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 222, 240))
    # ballot box
    g.rectangle([x0 + 70, y0 + 26, x0 + 120, y0 + h - 12], fill=(94, 64, 128))
    g.rectangle([x0 + 64, y0 + 20, x0 + 126, y0 + 28], fill=(70, 44, 100))
    g.rectangle([x0 + 88, y0 + 22, x0 + 102, y0 + 26], fill=(20, 20, 30))
    g.text((x0 + 76, y0 + 40), "VOTE", font=F(SANS_B, 12), fill=(255, 255, 255))
    # ballot paper going in
    g.polygon([(x0 + 84, y0 + 22), (x0 + 104, y0 + 22), (x0 + 100, y0 + 6),
               (x0 + 88, y0 + 6)], fill=(255, 255, 255))
    # queue of voters
    for i in range(4):
        px = x0 + 12 + i * 14
        g.ellipse([px, y0 + 44, px + 9, y0 + 53], fill=(240, 200, 170))
        g.rounded_rectangle([px - 2, y0 + 53, px + 11, y0 + h - 12], radius=4,
                            fill=((38, 44, 66), (66, 38, 44), (34, 102, 58),
                                  (120, 90, 30))[i])
    for i in range(3):
        px = x0 + 140 + i * 14
        g.ellipse([px, y0 + 44, px + 9, y0 + 53], fill=(220, 180, 150))
        g.rounded_rectangle([px - 2, y0 + 53, px + 11, y0 + h - 12], radius=4,
                            fill=((94, 64, 128), (13, 105, 104), (178, 34, 34))[i])


def sec_gaza(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 182, 160))
    # rubble piles
    for rx, rw, rh in [(x0 + 6, 52, 30), (x0 + 120, 60, 36), (x0 + 66, 44, 22)]:
        g.polygon([(rx, y0 + h), (rx + rw // 2, y0 + h - rh), (rx + rw, y0 + h)],
                  fill=(140, 128, 108))
        g.line([(rx + 8, y0 + h - 10), (rx + rw - 10, y0 + h - 18)],
               fill=(110, 98, 80), width=2)
    # aid van
    g.rectangle([x0 + 62, y0 + 34, x0 + 122, y0 + 62], fill=(240, 240, 235))
    g.rectangle([x0 + 62, y0 + 34, x0 + 122, y0 + 42], fill=(178, 34, 34))
    g.rectangle([x0 + 122, y0 + 44, x0 + 138, y0 + 62], fill=(220, 220, 210))
    g.ellipse([x0 + 72, y0 + 60, x0 + 82, y0 + 70], fill=(30, 30, 30))
    g.ellipse([x0 + 122, y0 + 60, x0 + 132, y0 + 70], fill=(30, 30, 30))
    # stretcher team
    g.rectangle([x0 + 140, y0 + 58, x0 + 178, y0 + 63], fill=(240, 220, 180))
    for px in [142, 172]:
        g.ellipse([px, y0 + 46, px + 8, y0 + 54], fill=(240, 200, 170))
        g.rounded_rectangle([px - 2, y0 + 54, px + 10, y0 + 70], radius=3,
                            fill=(200, 120, 40))


def sec_finland(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(178, 200, 214))
    # pine forest
    for tx in range(x0 + 4, x0 + w - 8, 18):
        th = 26 + (tx * 7) % 14
        g.polygon([(tx, y0 + h), (tx + 7, y0 + h - th), (tx + 14, y0 + h)],
                  fill=(30, 80, 50))
    g.rectangle([x0, y0 + h - 12, x0 + w, y0 + h], fill=(60, 90, 60))
    # border line
    g.line([(x0 + w // 2, y0 + 8), (x0 + w // 2, y0 + h - 12)],
           fill=(178, 34, 34), width=2)
    for by in range(y0 + 10, y0 + h - 12, 12):
        g.line([(x0 + w // 2 - 5, by), (x0 + w // 2 + 5, by)],
               fill=(178, 34, 34), width=2)
    # helicopter
    hx, hy = x0 + 58, y0 + 18
    g.ellipse([hx - 4, hy - 4, hx + 26, hy + 8], fill=(60, 60, 66))
    g.rectangle([hx + 22, hy - 1, hx + 52, hy + 3], fill=(60, 60, 66))
    g.line([hx + 8, hy - 8, hx + 14, hy - 8], fill=(60, 60, 66), width=3)
    g.line([hx - 2, hy - 12, hx + 24, hy - 12], fill=(40, 40, 44), width=2)
    g.rectangle([hx + 46, hy - 6, hx + 50, hy + 8], fill=(60, 60, 66))
    # magnifier
    mx, my = x0 + w - 44, y0 + 14
    g.ellipse([mx, my, mx + 20, my + 20], outline=(20, 20, 30), width=3)
    g.line([mx + 16, my + 16, mx + 26, my + 26], fill=(20, 20, 30), width=3)


def sec_bayelsa(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(52, 110, 140))
    # sky
    g.rectangle([x0, y0, x0 + w, y0 + 26], fill=(214, 228, 232))
    # capsized hull
    g.pieslice([x0 + 52, y0 + 8, x0 + 132, y0 + 52], 180, 360, fill=(120, 60, 30))
    g.rectangle([x0 + 52, y0 + 30, x0 + 132, y0 + 36], fill=(90, 40, 20))
    # water lines
    for wy in range(y0 + 44, y0 + h - 4, 10):
        for wx in range(x0 + 6, x0 + w - 12, 30):
            g.line([wx, wy, wx + 18, wy], fill=(180, 215, 230), width=2)
    # life rings
    for rx, ry in [(x0 + 22, y0 + 48), (x0 + 150, y0 + 56)]:
        g.ellipse([rx, ry, rx + 16, ry + 16], outline=(240, 120, 40), width=4)
    # rescue boat
    bx, by = x0 + 128, y0 + h - 22
    g.polygon([(bx, by), (bx + 48, by), (bx + 42, by + 10), (bx + 6, by + 10)],
              fill=(240, 120, 30))
    g.rectangle([bx + 14, by - 10, bx + 30, by], fill=(250, 250, 245))


def sec_hamas(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 222, 196))
    # flags behind table
    for i, col in enumerate([(34, 102, 58), (178, 34, 34), (31, 68, 120),
                             (176, 141, 44), (94, 64, 128)]):
        fx = x0 + 14 + i * 34
        g.rectangle([fx, y0 + 10, fx + 22, y0 + 30], fill=col)
        g.line([fx + 2, y0 + 10, fx + 2, y0 + 40], fill=(120, 100, 70), width=2)
    # table
    g.rectangle([x0 + 8, y0 + 48, x0 + w - 8, y0 + 56], fill=(96, 52, 26))
    g.rectangle([x0 + 8, y0 + 56, x0 + w - 8, y0 + h - 6], fill=(120, 70, 36))
    # microphones + papers
    for mx in [x0 + 30, x0 + 90, x0 + 150]:
        g.line([mx, y0 + 48, mx + 6, y0 + 38], fill=(40, 40, 40), width=2)
        g.ellipse([mx + 3, y0 + 33, mx + 11, y0 + 41], fill=(40, 40, 40))
        g.rectangle([mx - 8, y0 + 50, mx + 8, y0 + 55], fill=(255, 255, 255))
    # seated figures
    for i in range(3):
        px = x0 + 34 + i * 56
        g.ellipse([px, y0 + 60, px + 12, y0 + 72], fill=(240, 200, 170))
        g.rounded_rectangle([px - 4, y0 + 72, px + 16, y0 + h - 8], radius=4,
                            fill=(38, 44, 66))


def sec_bolsonaro(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 232, 236))
    g.rectangle([x0, y0, x0 + w, y0 + 16], fill=(122, 32, 48))
    g.text((x0 + 6, y0 + 3), "ICU", font=F(SANS_B, 10), fill=(255, 255, 255))
    # monitor with heartbeat
    g.rectangle([x0 + w - 62, y0 + 22, x0 + w - 10, y0 + 52], fill=(20, 30, 30))
    pts = [(x0 + w - 58, y0 + 40), (x0 + w - 46, y0 + 40), (x0 + w - 42, y0 + 30),
           (x0 + w - 38, y0 + 48), (x0 + w - 34, y0 + 36), (x0 + w - 28, y0 + 40),
           (x0 + w - 14, y0 + 40)]
    g.line(pts, fill=(80, 220, 120), width=2)
    # bed + patient
    bx, by = x0 + 12, y0 + 44
    g.rectangle([bx, by + 14, bx + 96, by + 20], fill=(90, 110, 130))
    g.rectangle([bx, by + 20, bx + 4, by + 40], fill=(60, 80, 100))
    g.rectangle([bx + 92, by + 20, bx + 96, by + 40], fill=(60, 80, 100))
    g.ellipse([bx + 6, by, bx + 18, by + 12], fill=(240, 200, 170))
    g.rounded_rectangle([bx + 16, by + 8, bx + 92, by + 16], radius=3,
                        fill=(240, 240, 235))
    # IV drip
    g.line([bx + 104, y0 + 24, bx + 104, by + 8], fill=(120, 120, 120), width=1)
    g.rectangle([bx + 100, y0 + 24, bx + 108, y0 + 36], fill=(220, 240, 255))
    g.line([bx + 104, by + 8, bx + 92, by + 10], fill=(120, 120, 120), width=1)


def sec_gp(g, x0, y0, w, h):
    g.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 20, 44))
    # skyline
    for bx, bw, bh in [(x0 + 6, 22, 26), (x0 + 32, 18, 36), (x0 + 54, 26, 22),
                       (x0 + 150, 20, 30), (x0 + 174, 16, 40)]:
        g.rectangle([bx, y0 + 44 - bh, bx + bw, y0 + 44], fill=(40, 44, 80))
        for wy in range(y0 + 48 - bh, y0 + 42, 7):
            g.rectangle([bx + 3, wy, bx + 6, wy + 3], fill=(255, 210, 110))
    # track
    g.rectangle([x0, y0 + 44, x0 + w, y0 + h], fill=(50, 50, 56))
    g.line([x0, y0 + 52, x0 + w, y0 + 52], fill=(240, 240, 240), width=1)
    g.line([x0, y0 + h - 8, x0 + w, y0 + h - 8], fill=(240, 240, 240), width=1)
    for lx in range(x0 + 4, x0 + w - 4, 20):
        g.line([lx, y0 + 66, lx + 10, y0 + 66], fill=(255, 220, 90), width=2)
    # race cars
    for cx, col in [(x0 + 30, (220, 40, 40)), (x0 + 92, (40, 110, 220)),
                    (x0 + 148, (240, 200, 60))]:
        cy = y0 + 56
        g.rounded_rectangle([cx, cy, cx + 34, cy + 10], radius=4, fill=col)
        g.rectangle([cx + 8, cy - 5, cx + 22, cy], fill=col)
        g.ellipse([cx + 5, cy + 8, cx + 11, cy + 14], fill=(10, 10, 10))
        g.ellipse([cx + 23, cy + 8, cx + 29, cy + 14], fill=(10, 10, 10))
    # checkered flag
    fx, fy = x0 + w - 34, y0 + 6
    for r in range(3):
        for c in range(4):
            g.rectangle([fx + c * 6, fy + r * 6, fx + c * 6 + 6, fy + r * 6 + 6],
                        fill=(20, 20, 20) if (r + c) % 2 else (255, 255, 255))
    g.line([fx, fy, fx, fy + 26], fill=(150, 150, 150), width=2)

# ----------------------------------------------------------- secondary grid
SECS = [
    dict(art=sec_iran, n=4, tag="CLAIM", col=RED2,
         head="IRAN CLAIMS STRIKES ON US RADARS",
         summ="Bahrain: civilian site hit."),
    dict(art=sec_manipur, n=5, tag="REPORTED", col=TEAL,
         head="FAKE LIQUOR KILLS 16 IN MANIPUR",
         summ="About 600 in hospital."),
    dict(art=sec_myanmar, n=6, tag="REPORTED", col=BROWN,
         head="M4.1 QUAKE SHAKES MYANMAR",
         summ="95 km deep near Tamu."),
    dict(art=sec_hk, n=7, tag="REPORTED", col=PURPLE,
         head="5,700 VOTE IN HONG KONG POLLS",
         summ="856 vie for 723 seats."),
    dict(art=sec_gaza, n=8, tag="REPORTED", col=GREY,
         head="129 BODIES PULLED FROM RUBBLE",
         summ="Civil Defence recovers the dead."),
    dict(art=sec_finland, n=9, tag="ONGOING", col=BLUE,
         head="FINLAND PROBES HELICOPTER BREACH",
         summ="Suspected 4.1 km breach, Sat."),
    dict(art=sec_bayelsa, n=10, tag="ONGOING", col=GREEN,
         head="BAYELSA BOAT TOLL RISES TO 24",
         summ="Capsized Fri; search continues."),
    dict(art=sec_hamas, n=11, tag="REPORTED", col=OLIVE,
         head="HAMAS SEEKS URGENT MEDIATOR TALKS",
         summ="After strike kills 3 aid workers."),
    dict(art=sec_bolsonaro, n=12, tag="ONGOING", col=MAROON,
         head="BOLSONARO IN ICU, DAY TWO",
         summ="Difficult night; surgery weighed."),
    dict(art=sec_gp, n=13, tag="REPORTED", col=NAVY,
         head="VERSTAPPEN WINS LAS VEGAS GP",
         summ="35 lead changes; Norris 2nd."),
]
sy0, srh = 470, 139
sxs = [12, 213, 414, 615, 816]
sws = [197, 197, 197, 197, 196]
for i, s in enumerate(SECS):
    r, c = divmod(i, 5)
    x0 = sxs[c]
    y0 = sy0 + r * srh
    w = sws[c]
    d.rectangle([x0, y0, x0 + w, y0 + srh], fill=(255, 253, 247),
                outline=(150, 130, 110), width=1)
    d.rectangle([x0, y0, x0 + w, y0 + 17], fill=s["col"])
    # number chip: white circle, dark number
    d.ellipse([x0 + 4, y0 + 2, x0 + 18, y0 + 16], fill=(255, 255, 255))
    fn = F(SANS_B, 10)
    ns = str(s["n"])
    d.text((x0 + 11 - tw(d, ns, fn) / 2, y0 + 3), ns, font=fn, fill=INK)
    # tag chip: white pill with coloured text (readable on any banner)
    ft = F(SANS_B, 8)
    tw_tag = int(tw(d, s["tag"], ft)) + 10
    d.rounded_rectangle([x0 + w - tw_tag - 4, y0 + 3, x0 + w - 4, y0 + 14],
                        radius=3, fill=(255, 255, 255))
    d.text((x0 + w - tw_tag + 1, y0 + 4), s["tag"], font=ft,
           fill=TAG_COLORS[s["tag"]])
    s["art"](d, x0 + 3, y0 + 20, w - 6, 80)
    fh = F(SANS_B, 12)
    hlines = wrap(s["head"], fh, w - 10, d)[:2]
    draw_lines(d, x0 + 5, y0 + 102, hlines, fh, INK, leading=12)
    fs = fit_font(d, s["summ"], SANS, 10, w - 10, 9)
    d.text((x0 + 5, y0 + 126), s["summ"], font=fs, fill=(60, 60, 60))

# ------------------------------------------------------------ map + also on
my0, mh = 754, 144
d.rectangle([12, my0, 342, my0 + mh], fill=SEA, outline=(150, 130, 110), width=1)
d.text((20, my0 + 4), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=NAVY)
MAP_X, MAP_Y, MAP_W, MAP_H = 16, my0 + 20, 322, 120


def proj(lon, lat):
    return (MAP_X + (lon + 180) / 360 * MAP_W,
            MAP_Y + (85 - lat) / 140 * MAP_H)


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21),
     (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-124, 48), (-140, 60),
     (-155, 58), (-165, 60)],
    [(-80, 10), (-77, 4), (-80, -3), (-81, -6), (-70, -18), (-70, -30),
     (-72, -40), (-73, -50), (-68, -55), (-65, -45), (-58, -34), (-48, -28),
     (-40, -20), (-35, -8), (-44, 0), (-52, 5), (-60, 8), (-70, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 71), (40, 68), (44, 66), (40, 60),
     (30, 60), (28, 55), (23, 54), (19, 54), (12, 54), (8, 53), (5, 50),
     (0, 46), (-2, 43), (-6, 36)],
    [(-17, 15), (-16, 20), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
     (32, 31), (35, 28), (37, 22), (40, 15), (43, 11), (48, 10), (51, 12),
     (44, 0), (40, -10), (35, -18), (32, -26), (28, -33), (20, -35),
     (16, -28), (12, -18), (9, -2), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(40, 68), (50, 70), (60, 70), (70, 73), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 66),
     (162, 60), (158, 52), (150, 45), (142, 40), (140, 35), (135, 33),
     (130, 31), (127, 35), (122, 38), (120, 30), (115, 23), (110, 20),
     (108, 12), (105, 9), (100, 8), (98, 12), (94, 17), (92, 21), (88, 22),
     (86, 20), (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (62, 25),
     (58, 25), (54, 26), (52, 28), (50, 29), (48, 30), (44, 29), (40, 28),
     (38, 22), (36, 20), (35, 28), (34, 31), (36, 36), (40, 41), (44, 46),
     (40, 50), (38, 55), (35, 60), (32, 66), (30, 68)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (136, -12), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
     (114, -22)],
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-30, 76),
     (-45, 78), (-58, 76), (-55, 70), (-52, 64), (-48, 60)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (142, 44), (144, 44), (142, 42), (140, 38), (138, 36),
     (136, 34), (133, 34), (131, 32)],
    [(95, 5), (98, 3), (100, 0), (102, -3), (105, -5), (110, -7), (114, -8),
     (119, -8), (120, -10), (124, -10), (128, -8), (131, -3), (136, -2),
     (141, -3), (141, -8), (136, -8), (130, -7), (125, -9), (120, -10),
     (115, -8), (110, -7), (105, -5), (100, 0), (96, 4)],
    [(43, -12), (47, -15), (50, -16), (50, -20), (47, -24), (44, -25),
     (43, -20), (43, -15)],
    [(167, -45), (170, -42), (174, -41), (177, -38), (178, -37), (175, -40),
     (172, -43), (168, -46)],
]
for poly in CONTINENTS:
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
              outline=LAND_EDGE)
PINS = [
    (1, 30.7, 36.9, 10, 6), (2, 30.5, 50.4, -12, -6), (3, 24.5, 59.7, -12, -10),
    (4, 50.6, 26.2, 0, 0), (5, 93.9, 24.8, -12, 10), (6, 94.3, 24.2, 12, 10),
    (7, 114.2, 22.3, 0, 0), (8, 34.5, 31.4, -14, 8), (9, 26.2, 60.5, 12, -12),
    (10, 6.2, 4.8, 0, 0), (11, 34.45, 31.5, 14, -10), (12, -47.9, -15.8, 0, 0),
    (13, -115.1, 36.2, 0, 0),
]
for n, lon, lat, dx, dy in PINS:
    px, py = proj(lon, lat)
    cx, cy = px + dx, py + dy
    if dx or dy:
        d.line([px, py, cx, cy], fill=RED, width=1)
    d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
              outline=(255, 255, 255), width=1)
    fn = F(SANS_B, 8)
    ns = str(n)
    d.text((cx - tw(d, ns, fn) / 2, cy - 5), ns, font=fn, fill=(255, 255, 255))

# ALSO ON 14-25
ALSO_ON = [
    ("Saudi forces stop Houthi missile near Mecca", "Al Jazeera"),
    ("Denmark expels Russian attaché over 'plot'", "BBC"),
    ("Candy-factory fire in Serang: 3 dead, dozens missing", "BBC"),
    ("South Korea's education minister resigns", "Presidential Office"),
    ("UN: 1 in 4 women can't refuse sex in marriage", "Guardian"),
    ("US may sanction judge behind Myanmar ruling", "Guardian"),
    ("California braces for biggest waves in years", "Guardian"),
    ("Palisades fire arsonist convicted", "BBC"),
    ("Amazon nears $7.5bn deal for Decart", "Crypto Briefing"),
    ("WHO warns antibiotic resistance is rising", "WHO"),
    ("UN states agree tentative weapons rules", "UN"),
    ("Pope shares lunch with 1,300 poor", "Vatican News"),
    ("Paolo Bulgari dies aged 89", "BBC"),
    ("Wembanyama scores 50 in Spurs win", "BBC"),
    ("Theresa May 'aghast' at Burnham EU plans", "BBC"),
    ("Wales coach rues Australia defeat", "BBC"),
    ("BBC sorry over Strictly noise glitch", "BBC"),
    ("Pugh swims Hormuz for wildlife", "AP"),
    ("US officers arrest travellers at Seattle airport", "AP"),
    ("Senate Democrats face leadership test", "AP"),
    ("Nigeria's youth 'shut out of politics'", "BBC"),
]
ax0, ay0 = 350, my0
d.text((ax0, ay0 + 4), "ALSO ON · 14–34", font=F(SANS_B, 11), fill=INK)
d.line([ax0, ay0 + 20, 1012, ay0 + 20], fill=RED, width=1)
acol_w = (1012 - ax0 - 8) // 3
for i, (lead, outlet) in enumerate(ALSO_ON):
    col, row = divmod(i, 7)
    ix = ax0 + col * (acol_w + 8)
    iy = ay0 + 24 + row * 17
    fl = fit_font(d, lead, SANS_B, 9, acol_w, 7)
    d.text((ix, iy), lead, font=fl, fill=INK)
    d.text((ix, iy + 9), outlet, font=F(SANS, 8), fill=(110, 90, 70))

# --------------------------------------------------------------- date check
dy0, dh = 900, 98
d.rectangle([12, dy0, 1012, dy0 + dh], outline=RED, width=2)
d.rectangle([12, dy0, 1012, dy0 + 18], fill=RED)
d.text((20, dy0 + 3), "DATE CHECK — WHAT WE LEFT OUT, AND WHY",
       font=F(SANS_B, 11), fill=(255, 255, 255))
EXCL_L = [
    ("400-drone barrage — Thu–Fri 19–20 Nov. Tonight's was 186, not 400.", True),
    ("Peru M6.7 quake — Fri 20 Nov. 1 dead, 16 hurt.", False),
    ("Russian missiles land in Poland — Fri 20 Nov. No casualties.", False),
    ("Kerch Bridge road span down — 16–17 Nov.", False),
    ("GTA VI launch — Thu 19 Nov. $3.79bn day one.", False),
    ("Anthropic IPO — Thu 19 Nov. $81.3bn, ANT +17%.", False),
]
EXCL_R = [
    ("Shenzhen summit: Trump–Xi–Putin — Thu 19 Nov.", False),
    ("EU–Indonesia trade deal signed — Sat 21 Nov.", False),
    ("BepiColombo enters Mercury orbit — Sat 21 Nov.", False),
    ("El Chapo captured Fri 20 Nov; Kryvyi Rih Sat 21 Nov.", False),
    ("FBI database breach — first reported Fri 20 Nov.", False),
    ("UK–EU reset deal — Fri 20 Nov.", False),
]
for i, (txt, lead) in enumerate(EXCL_L):
    f = F(SANS_B, 10) if lead else F(SANS, 10)
    d.text((24, dy0 + 21 + i * 10), txt, font=f,
           fill=RED if lead else INK)
for i, (txt, lead) in enumerate(EXCL_R):
    f = F(SANS_B, 10) if lead else F(SANS, 10)
    d.text((512, dy0 + 21 + i * 10), txt, font=f,
           fill=RED if lead else INK)
d.text((24, dy0 + 21 + 6 * 10 + 3),
       "NOT YET TODAY: COP31 approval vote (due 06:00 GMT, slipped to 11:00)  ·  "
       "ATP final: Alcaraz v Zverev, Turin  ·  Liverpool v Man Utd 23:30 WIB",
       font=F(SANS_B, 10), fill=NAVY)

# ------------------------------------------------------------------- footer
d.text((12, 1000),
       "SOURCES: REUTERS · GUARDIAN · UKRAINIAN AIR FORCE · XINHUA · NCS/ANI · "
       "HK GOVT · GAZA CIVIL DEFENCE · ANADOLU · BBC · AL JAZEERA · VATICAN NEWS · WHO · UN",
       font=F(SANS, 9), fill=(110, 90, 70))
d.text((12, 1012),
       "TAGS: ONGOING still developing  ·  REPORTED confirmed today  ·  "
       "CLAIM one side says it, not confirmed  ·  FORECAST not yet happened",
       font=F(SANS, 9), fill=(110, 90, 70))

# --------------------------------------------------------------------- save
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    print("wrote", out)
