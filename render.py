#!/usr/bin/env python3
"""THE WORLD TODAY — Sunday 22 November 2026. Renders entry.png (1024x1024).
Fresh R3 build from the R3 evaluation spec. Procedural illustration, Pillow only.
Run: python3 render.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 236)
INK = (18, 18, 18)
RED = (200, 16, 46)
DARKRED = (150, 10, 32)
NAVY = (20, 33, 61)
GREY = (110, 108, 100)
LIGHT = (238, 232, 218)
CARD = (255, 255, 255)
BLUE = (31, 93, 168)
TEAL = (0, 128, 128)
GREEN = (34, 120, 66)
ORANGE = (214, 96, 20)
PURPLE = (96, 60, 150)

FD = "/usr/share/fonts/truetype/dejavu"


def F(size, bold=False, serif=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FD, name), size)


def tw(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, width, lh=None, max_lines=None):
    lh = lh or int(font.size * 1.25)
    lines = wrap(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def chip(d, cx, cy, r, num, fill=RED):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill, outline=(255, 255, 255), width=2)
    f = F(13 if r >= 11 else 11, bold=True)
    t = str(num)
    d.text((cx - d.textlength(t, font=f) / 2, cy - f.size / 2 - 1), t, font=f, fill=(255, 255, 255))


def tag(d, x, y, text, fill=RED):
    f = F(11, bold=True)
    w = int(d.textlength(text, font=f)) + 14
    d.rectangle((x, y, x + w, y + 18), fill=fill)
    d.text((x + 7, y + 2), text, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories
# regions: EU Europe, ME Middle East, WO World, AM Americas, AP Asia-Pacific
HEROES = [
    dict(n=1, tag="CLIMATE", loc="ANTALYA, TURKIYE",
         head="COP31 PUTS FINAL DEAL TO VOTE — NO WORD ON FOSSIL FUELS",
         summ="10-page text tabled; vote at 06:00 GMT. (Reuters)",
         cap="Summit presidency — Reuters",
         region="WO", art="cop31"),
    dict(n=2, tag="WAR", loc="KYIV, UKRAINE",
         head="400+ DRONES IN THE WAR'S BIGGEST BARRAGE",
         summ="400+ drones, 110+ missiles; 8 killed. (CNN)",
         cap="Ukraine Air Force — CNN",
         region="EU", art="barrage"),
    dict(n=3, tag="BALTIC", loc="GULF OF FINLAND",
         head="SANCTIONED RUSSIAN SHIP ABLAZE AFTER DRONE STRIKE",
         summ="16 crew evacuated; fire still burning. (CNN)",
         cap="Finnish Border Guard — CNN",
         region="EU", art="sparta"),
]

SECONDARIES = [
    dict(n=4, tag="CLAIM", loc="BAHRAIN",
         head="IRAN SAYS IT HIT 2 US PATRIOT RADARS",
         summ="IRGC claims strikes; US has not confirmed.",
         region="ME", art="iran"),
    dict(n=5, tag="MEXICO", loc="SINALOA",
         head="MEXICO CAPTURES 'EL CHAPO ISIDRO'",
         summ="11 dead in Guasave raid; kingpin flown out.",
         region="AM", art="chapo"),
    dict(n=6, tag="UKRAINE", loc="KRYVYI RIH",
         head="TRIPLE-TAP STRIKE KILLS BOY, 7, AND PARAMEDIC",
         summ="Missiles, then drones hit rescuers; 60 hurt.",
         region="EU", art="kryvyi"),
    dict(n=7, tag="UKRAINE", loc="KYIV",
         head="186 DRONES OVERNIGHT, 161 DOWNED",
         summ="Air Force: 18 locations hit in new wave.",
         region="EU", art="drones186"),
    dict(n=8, tag="QUAKE", loc="SAGAING, MYANMAR",
         head="4.1 QUAKE SHAKES MYANMAR AT DAWN",
         summ="NCS: 02:35 IST, 95 km deep, near Tamu.",
         region="AP", art="myanmar"),
    dict(n=9, tag="INDIA", loc="MANIPUR",
         head="TOXIC LIQUOR TOLL REACHES 16",
         summ="600 in hospital in Chandel; 6 arrested.",
         region="AP", art="manipur"),
    dict(n=10, tag="HONG KONG", loc="HONG KONG",
         head="5,700 VOTERS PICK 723 ELECTION SEATS",
         summ="Turnout 93.5% by 2pm in Committee poll.",
         region="AP", art="hk"),
    dict(n=11, tag="FINLAND", loc="GULF OF FINLAND",
         head="RUSSIAN HELICOPTER IN AIRSPACE BREACH",
         summ="Suspected incursion at 12:34 in rescue.",
         region="EU", art="finland"),
    dict(n=12, tag="UKRAINE", loc="DNIPROPETROVSK",
         head="POWER GRID IN FLAMES AFTER STRIKES",
         summ="Rail yard, substations hit in barrage.",
         region="EU", art="dnipro"),
    dict(n=13, tag="SPORT", loc="LAS VEGAS",
         head="VERSTAPPEN WINS LAS VEGAS GP",
         summ="Antonelli fastest; penalty hands him pole.",
         region="AM", art="vegas"),
]

ALSO_ON = [
    (14, "Gaza: 129 bodies pulled from rubble in central Gaza", "Al Jazeera"),
    (15, "COP31: 130 nations demand fossil-fuel text back", "Reuters"),
    (16, "COP31: EU's Hoekstra — 'good deal or no deal'", "Reuters"),
    (17, "Ukraine: Zelensky calls barrage 'biggest this year'", "CNN"),
    (18, "Bahrain: Iranian strike sets industrial site ablaze", "Al Jazeera"),
    (19, "US denies Iran damaged an F-16", "US officials"),
    (20, "Iran tankers move to break US blockade", "Geneva Times"),
    (21, "Washington halts gun-check system over NCIC breach", "Wash. State Patrol"),
    (22, "Finland imposes air, sea limits around wreck", "NY Post"),
    (23, "Sparta II anchored off Loviisa; firefighting goes on", "Border Guard"),
    (24, "Sinaloa: 4 soldiers among 11 dead in raid", "Defence Ministry"),
    (25, "October was 1.8C hotter than the 1800s", "Berkeley Earth"),
    (26, "COP31 text: 35% of energy from electricity by 2035", "draft"),
    (27, "COP31 text admits 1.5C will be overshot", "draft"),
    (28, "Gaza: 9 killed, 55 hurt in past 48 hours", "Health Ministry"),
    (29, "Gaza City drone strike kills 3, fourth shot in Jabalia", "Al Jazeera"),
    (30, "NATO condemns Russian missiles over Poland", "NATO"),
    (31, "France calls UN Security Council over Poland", "Reuters"),
    (32, "COP31: Saudi Arabia, oil states block fossil-fuel text", "Guardian"),
    (33, "COP31 text: 1bn-tonne carbon capture goal", "draft"),
    (34, "Lviv: missile hits flats, 2 killed, 10 hurt", "ANI"),
    (35, "Manipur: 6 held, 2,400 litres of liquor seized", "police"),
    (36, "Gaza: 350,000 families homeless, 80% of homes destroyed", "Housing Ministry"),
]

REGIONS = [("EUROPE", 13, BLUE), ("MIDDLE EAST", 8, ORANGE),
           ("WORLD", 6, TEAL), ("AMERICAS", 5, GREEN), ("ASIA-PACIFIC", 4, PURPLE)]

STRIP = [
    ("0", "COP31 DEALS AGREED"),
    ("400+", "DRONES FIRED AT UKRAINE"),
    ("2", "US RADARS IRAN SAYS IT HIT"),
    ("16", "MANIPUR LIQUOR DEAD"),
    ("129", "GAZA BODIES RECOVERED"),
    ("5,700", "HONG KONG VOTERS"),
]

CLOCK = [
    ("02:35 IST", "Myanmar quake"),
    ("03:00 GMT", "COP31 text put to vote"),
    ("08:00 Kyiv", "186 drones downed"),
    ("12:34 Loviisa", "airspace breach"),
]

# ---------------------------------------------------------------- art scenes
# Every scene draws densely into box (x0, y0, x1, y1): no more than ~25% empty.

def _sky(d, x0, y0, x1, y1, bands):
    h = (y1 - y0) / len(bands)
    for i, c in enumerate(bands):
        d.rectangle((x0, y0 + i * h, x1, y0 + (i + 1) * h), fill=c)


def _windows(d, x0, y0, x1, y1, cols, rows, lit=(255, 214, 90), dark=(38, 48, 70)):
    import random
    rnd = random.Random(7)
    cw = (x1 - x0) / cols
    rh = (y1 - y0) / rows
    for c in range(cols):
        for r in range(rows):
            col = lit if rnd.random() < 0.55 else dark
            d.rectangle((x0 + c * cw + 2, y0 + r * rh + 2,
                         x0 + (c + 1) * cw - 2, y0 + (r + 1) * rh - 2), fill=col)


def _flames(d, x0, y0, x1, y1, n=7, seed=3):
    import random
    rnd = random.Random(seed)
    w = (x1 - x0) / n
    for i in range(n):
        fx = x0 + i * w + w / 2
        fh = rnd.randint(int((y1 - y0) * 0.5), int((y1 - y0) * 0.95))
        d.polygon([(fx - w * 0.42, y1), (fx, y1 - fh), (fx + w * 0.42, y1)],
                  fill=(230, 90, 20))
        d.polygon([(fx - w * 0.22, y1), (fx, y1 - fh * 0.55), (fx + w * 0.22, y1)],
                  fill=(250, 200, 40))


def _smoke(d, x0, y0, x1, y1, n=5, seed=5):
    import random
    rnd = random.Random(seed)
    for i in range(n):
        sx = x0 + (x1 - x0) * (i + 0.5) / n + rnd.randint(-6, 6)
        sy = y0 + rnd.randint(0, int((y1 - y0) * 0.5))
        r = rnd.randint(8, 16)
        d.ellipse((sx - r, sy - r, sx + r, sy + r), fill=(120, 118, 112))


def art_cop31(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(232, 226, 205), (214, 206, 182), (196, 188, 162)])
    # flags row
    for i in range(9):
        fx = x0 + 8 + i * ((x1 - x0 - 16) / 9)
        d.rectangle((fx, y0 + 6, fx + 14, y0 + 22), fill=[BLUE, RED, GREEN, TEAL, ORANGE, PURPLE, (180, 30, 30), (30, 120, 90), (90, 60, 140)][i])
    # wall clock
    cx, cy = x1 - 26, y0 + 30
    d.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill=(255, 255, 255), outline=INK, width=2)
    d.line((cx, cy, cx, cy - 9), fill=INK, width=2)
    d.line((cx, cy, cx + 7, cy + 2), fill=INK, width=2)
    # long table
    d.rectangle((x0 + 6, y1 - 58, x1 - 6, y1 - 8), fill=(122, 74, 40))
    d.rectangle((x0 + 6, y1 - 58, x1 - 6, y1 - 50), fill=(150, 96, 54))
    # thermometer
    tx = x0 + 22
    d.rectangle((tx, y0 + 34, tx + 8, y1 - 66), fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle((tx + 1, y1 - 78, tx + 7, y1 - 66), fill=RED)
    d.ellipse((tx - 3, y1 - 66, tx + 11, y1 - 52), fill=RED)
    # delegates: heads + shoulders along the table
    import random
    rnd = random.Random(11)
    for i in range(7):
        px = x0 + 24 + i * ((x1 - x0 - 48) / 7)
        py = y1 - 58
        d.ellipse((px - 8, py - 22, px + 8, py - 6), fill=(232, 190, 150), outline=INK, width=1)
        d.polygon([(px - 13, py - 6), (px + 13, py - 6), (px + 10, py + 14), (px - 10, py + 14)],
                  fill=[NAVY, (90, 30, 30), (30, 90, 50), (60, 60, 90), (120, 80, 20), (40, 80, 80), (100, 40, 90)][i])
    # globe on the table, right end, drawn after the delegates so it sits in front
    gx, gy = x1 - 34, y1 - 78
    d.ellipse((gx - 16, gy - 16, gx + 16, gy + 16), fill=BLUE, outline=INK, width=1)
    d.ellipse((gx - 9, gy - 12, gx + 2, gy - 2), fill=GREEN)
    d.ellipse((gx - 2, gy + 4, gx + 12, gy + 12), fill=GREEN)
    d.rectangle((gx - 2, gy + 16, gx + 2, gy + 22), fill=INK)
    # documents on the table
    for i in range(4):
        px = x0 + 30 + i * 62
        d.rectangle((px, y1 - 48, px + 26, y1 - 34), fill=(255, 255, 255), outline=GREY, width=1)
        d.line((px + 3, y1 - 44, px + 23, y1 - 44), fill=GREY, width=1)
        d.line((px + 3, y1 - 40, px + 23, y1 - 40), fill=GREY, width=1)


def art_barrage(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(14, 20, 40), (20, 30, 58), (30, 42, 76)])
    # stars
    import random
    rnd = random.Random(4)
    for _ in range(26):
        sx = rnd.randint(x0 + 3, x1 - 3)
        sy = rnd.randint(y0 + 3, y0 + int((y1 - y0) * 0.35))
        d.ellipse((sx, sy, sx + 2, sy + 2), fill=(220, 220, 200))
    # drone trails (dotted diagonals)
    for i in range(9):
        sx = x0 + rnd.randint(0, int((x1 - x0) * 0.7))
        sy = y0 + rnd.randint(4, int((y1 - y0) * 0.4))
        ex, ey = sx + rnd.randint(40, 90), sy + rnd.randint(18, 42)
        for t in range(0, 11):
            px = sx + (ex - sx) * t / 10
            py = sy + (ey - sy) * t / 10
            d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=(255, 170, 60))
    # skyline
    base = y1 - 8
    bx = x0
    while bx < x1 - 20:
        bw = rnd.randint(22, 44)
        bh = rnd.randint(28, 78)
        d.rectangle((bx, base - bh, bx + bw, base), fill=(16, 22, 40))
        _windows(d, bx + 2, base - bh + 3, bx + bw - 2, base - 3,
                 max(2, bw // 9), max(2, bh // 12))
        bx += bw + 3
    # fires at building bases
    _flames(d, x0 + 12, base - 26, x0 + 70, base, n=4, seed=9)
    _flames(d, x1 - 84, base - 30, x1 - 20, base, n=4, seed=12)
    _smoke(d, x0 + 20, y0 + int((y1 - y0) * 0.45), x0 + 90, y0 + int((y1 - y0) * 0.6), n=3, seed=6)


def art_sparta(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(70, 90, 110), (110, 125, 140), (150, 160, 165)])
    # sea
    sy = y0 + int((y1 - y0) * 0.62)
    d.rectangle((x0, sy, x1, y1), fill=(28, 68, 110))
    for i in range(6):
        wy = sy + 6 + i * 6
        d.line((x0 + 4, wy, x1 - 4, wy), fill=(90, 140, 190), width=1)
    # ship hull + superstructure
    hx0, hx1 = x0 + 14, x1 - 14
    hy = sy - 6
    d.polygon([(hx0, hy), (hx1, hy), (hx1 - 12, sy + 14), (hx0 + 12, sy + 14)], fill=(60, 30, 26))
    d.rectangle((hx0 + 26, hy - 26, hx0 + 90, hy), fill=(210, 200, 180))
    d.rectangle((hx0 + 96, hy - 40, hx0 + 150, hy), fill=(180, 60, 40))
    d.rectangle((hx0 + 96, hy - 52, hx0 + 118, hy - 40), fill=(120, 40, 30))
    # containers
    for i in range(5):
        d.rectangle((hx0 + 160 + i * 20, hy - 22, hx0 + 178 + i * 20, hy), fill=[(40, 90, 140), (180, 120, 30), (60, 120, 70), (140, 60, 60), (90, 90, 160)][i])
    # big flames on deck
    _flames(d, hx0 + 60, hy - 66, hx0 + 170, hy, n=8, seed=2)
    _smoke(d, hx0 + 70, y0 + 8, hx0 + 190, y0 + 34, n=5, seed=8)
    # lifeboat
    lx, ly = x1 - 62, sy + 22
    d.ellipse((lx, ly, lx + 34, ly + 12), fill=(255, 140, 0), outline=INK, width=1)
    d.ellipse((lx + 8, ly - 6, lx + 14, ly), fill=(232, 190, 150))
    d.ellipse((lx + 20, ly - 6, lx + 26, ly), fill=(232, 190, 150))
    # helicopter
    hx, hy2 = x0 + 34, y0 + 16
    d.ellipse((hx, hy2, hx + 34, hy2 + 12), fill=(200, 60, 40), outline=INK, width=1)
    d.line((hx + 34, hy2 + 6, hx + 52, hy2 + 6), fill=INK, width=2)
    d.line((hx + 4, hy2 - 6, hx + 30, hy2 - 6), fill=INK, width=2)


def art_iran(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(60, 40, 60), (90, 60, 70), (130, 90, 80)])
    # Bahrain skyline
    base = y1 - 6
    bx = x0
    import random
    rnd = random.Random(21)
    while bx < x1 - 16:
        bw = rnd.randint(18, 34)
        bh = rnd.randint(24, 64)
        d.rectangle((bx, base - bh, bx + bw, base), fill=(40, 30, 46))
        _windows(d, bx + 2, base - bh + 3, bx + bw - 2, base - 3, max(2, bw // 8), max(2, bh // 11),
                 lit=(255, 200, 110), dark=(52, 42, 58))
        bx += bw + 3
    # radar domes
    for dx, dh in ((x0 + 52, 46), (x1 - 78, 58)):
        d.rectangle((dx - 22, base - 12, dx + 22, base), fill=(120, 118, 110))
        d.pieslice((dx - 24, base - 12 - 26, dx + 24, base - 12 + 22), 180, 360, fill=(235, 232, 225), outline=INK, width=1)
        d.line((dx, base - 38, dx + 26, base - 52), fill=(255, 220, 100), width=2)
    # missile arcs
    for i in range(3):
        sx = x0 + 20 + i * 60
        d.arc((sx, y0 + 8, sx + 90, y0 + 70), 200, 330, fill=(255, 150, 50), width=2)
    # fire at industrial site
    _flames(d, x1 - 70, base - 24, x1 - 16, base, n=4, seed=14)


def art_chapo(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(120, 70, 50), (150, 95, 60), (180, 130, 80)])
    # street buildings
    base = y1 - 6
    for bx, bw, bh in ((x0 + 6, 34, 52), (x0 + 46, 28, 40), (x1 - 76, 30, 58), (x1 - 42, 34, 44)):
        d.rectangle((bx, base - bh, bx + bw, base), fill=(90, 60, 44))
        _windows(d, bx + 3, base - bh + 4, bx + bw - 3, base - 4, 3, max(2, bh // 12),
                 lit=(255, 210, 90), dark=(70, 48, 36))
    # street
    d.rectangle((x0, base - 4, x1, y1), fill=(60, 58, 56))
    d.line((x0, y1 - 2, x1, y1 - 2), fill=(240, 220, 80), width=1)
    # helicopter with beam
    hx, hy = x0 + 60, y0 + 12
    d.ellipse((hx, hy, hx + 36, hy + 12), fill=(40, 60, 40), outline=INK, width=1)
    d.line((hx + 36, hy + 6, hx + 54, hy + 6), fill=INK, width=2)
    d.line((hx + 6, hy - 6, hx + 32, hy - 6), fill=INK, width=2)
    d.polygon([(hx + 8, hy + 12), (hx + 30, hy + 12), (hx + 52, base - 6), (hx + 16, base - 6)],
              fill=(255, 240, 160))
    # roadblock fire
    _flames(d, x0 + 96, base - 22, x0 + 150, base - 4, n=5, seed=17)
    # soldiers
    for sx in (x0 + 20, x0 + 170, x1 - 30):
        d.ellipse((sx, base - 18, sx + 8, base - 10), fill=(232, 190, 150))
        d.rectangle((sx - 2, base - 10, sx + 10, base - 4), fill=(50, 70, 50))


def art_kryvyi(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(40, 44, 66), (70, 66, 84), (110, 96, 92)])
    base = y1 - 6
    # restaurant building, damaged
    d.rectangle((x0 + 10, base - 52, x0 + 120, base), fill=(150, 120, 90))
    d.polygon([(x0 + 10, base - 52), (x0 + 60, base - 70), (x0 + 120, base - 52)], fill=(120, 80, 60))
    _windows(d, x0 + 16, base - 48, x0 + 114, base - 6, 6, 3, lit=(255, 200, 90), dark=(60, 50, 44))
    d.rectangle((x0 + 52, base - 22, x0 + 76, base), fill=(70, 50, 36))
    # fires + smoke
    _flames(d, x0 + 20, base - 34, x0 + 70, base, n=4, seed=19)
    _smoke(d, x0 + 30, y0 + 10, x0 + 110, y0 + 30, n=4, seed=21)
    # ambulance
    ax, ay = x1 - 74, base - 26
    d.rectangle((ax, ay, ax + 62, ay + 20), fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle((ax + 22, ay + 5, ax + 30, ay + 15), fill=RED)
    d.rectangle((ax + 17, ay + 8, ax + 35, ay + 12), fill=RED)
    d.ellipse((ax + 10, ay + 18, ax + 20, ay + 26), fill=INK)
    d.ellipse((ax + 44, ay + 18, ax + 54, ay + 26), fill=INK)
    # rubble
    for i in range(6):
        rx = x0 + 130 + i * 10
        d.polygon([(rx, base), (rx + 6, base - 8), (rx + 12, base)], fill=(100, 90, 80))


def art_drones186(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(12, 18, 38), (18, 28, 56), (28, 40, 72)])
    import random
    rnd = random.Random(23)
    for _ in range(20):
        sx = rnd.randint(x0 + 3, x1 - 3)
        sy = rnd.randint(y0 + 3, y0 + int((y1 - y0) * 0.3))
        d.ellipse((sx, sy, sx + 2, sy + 2), fill=(220, 220, 200))
    # interception flashes
    for fx, fy in ((x0 + 40, y0 + 26), (x1 - 60, y0 + 34), ((x0 + x1) // 2, y0 + 18)):
        for a in range(8):
            import math
            ang = a * math.pi / 4
            d.line((fx, fy, fx + 14 * math.cos(ang), fy + 14 * math.sin(ang)), fill=(255, 220, 90), width=2)
    # drone dots with short trails
    for i in range(12):
        sx = x0 + rnd.randint(6, int((x1 - x0) * 0.8))
        sy = y0 + rnd.randint(6, int((y1 - y0) * 0.45))
        d.line((sx, sy, sx + 16, sy + 8), fill=(255, 170, 60), width=2)
        d.ellipse((sx + 14, sy + 6, sx + 18, sy + 10), fill=(255, 200, 80))
    # skyline
    base = y1 - 6
    bx = x0
    while bx < x1 - 18:
        bw = rnd.randint(20, 38)
        bh = rnd.randint(24, 62)
        d.rectangle((bx, base - bh, bx + bw, base), fill=(14, 20, 38))
        _windows(d, bx + 2, base - bh + 3, bx + bw - 2, base - 3, max(2, bw // 9), max(2, bh // 11))
        bx += bw + 3
    # searchlights
    d.polygon([(x0 + 30, base), (x0 + 44, base), (x0 + 90, y0 + 10), (x0 + 70, y0 + 10)], fill=(240, 240, 200))
    d.polygon([(x1 - 50, base), (x1 - 36, base), (x1 - 90, y0 + 14), (x1 - 110, y0 + 14)], fill=(240, 240, 200))

def art_myanmar(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(200, 190, 170), (214, 204, 184), (228, 218, 198)])
    base = y1 - 6
    # collapsed building: tilted slabs
    d.polygon([(x0 + 8, base), (x0 + 30, base - 44), (x0 + 62, base - 40), (x0 + 70, base)],
              fill=(150, 130, 110))
    d.polygon([(x0 + 34, base - 30), (x0 + 66, base - 46), (x0 + 96, base - 20), (x0 + 88, base)],
              fill=(120, 104, 88))
    d.line((x0 + 30, base - 44, x0 + 62, base - 40), fill=(90, 76, 62), width=2)
    d.line((x0 + 40, base - 20, x0 + 58, base - 34), fill=(90, 76, 62), width=2)
    # cracks on ground
    d.line((x0 + 8, base, x0 + 60, base - 6), fill=(80, 68, 56), width=2)
    d.line((x0 + 70, base, x0 + 110, base - 4), fill=(80, 68, 56), width=2)
    # seismograph chart card (right side)
    cx0, cy0, cx1, cy1 = x1 - 92, y0 + 8, x1 - 8, y0 + 46
    d.rectangle((cx0, cy0, cx1, cy1), fill=(255, 255, 255), outline=INK, width=1)
    for gx in range(cx0 + 8, cx1 - 4, 8):
        d.line((gx, cy0 + 4, gx, cy1 - 4), fill=(220, 220, 220), width=1)
    pts = []
    import random
    rnd = random.Random(31)
    for i in range(18):
        px = cx0 + 4 + i * ((cx1 - cx0 - 8) / 17)
        # keep the trace below the "M4.1" label so it never crosses the text
        py = cy0 + 14 + rnd.randint(0, (cy1 - cy0) - 18) if i % 3 else cy0 + (cy1 - cy0) // 2 + rnd.randint(-2, 2)
        pts.append((px, py))
    d.line(pts, fill=RED, width=2)
    f = F(10, bold=True)
    d.text((cx0 + 4, cy0 + 2), "M4.1", font=f, fill=RED)
    # rescue figure
    rx = x0 + 100
    d.ellipse((rx, base - 20, rx + 8, base - 12), fill=(232, 190, 150))
    d.rectangle((rx - 2, base - 12, rx + 10, base - 4), fill=(200, 60, 40))


def art_manipur(d, x0, y0, x1, y1):
    # hospital ward — everything sized inside the box (y0..y1)
    d.rectangle((x0, y0, x1, y1), fill=(226, 238, 232))
    d.rectangle((x0, y0, x1, y0 + 6), fill=(180, 210, 195))
    # green cross sign (top right)
    cx, cy = x1 - 14, y0 + 12
    d.rectangle((cx - 8, cy - 3, cx + 8, cy + 3), fill=GREEN)
    d.rectangle((cx - 3, cy - 8, cx + 3, cy + 8), fill=GREEN)
    # nurse figure (left, inside the box)
    nx = x0 + 10
    d.ellipse((nx, y0 + 8, nx + 8, y0 + 16), fill=(232, 190, 150))
    d.polygon([(nx - 1, y0 + 16), (nx + 9, y0 + 16), (nx + 8, y0 + 26), (nx, y0 + 26)],
              fill=(255, 255, 255))
    # beds with patients along the bottom of the box
    for i, bx in enumerate((x0 + 26, x0 + 78, x0 + 130)):
        by = y1 - 10
        d.rectangle((bx, by, bx + 44, by + 6), fill=(255, 255, 255), outline=INK, width=1)
        d.rectangle((bx, by - 4, bx + 9, by), fill=(255, 255, 255), outline=INK, width=1)
        d.ellipse((bx + 1, by - 9, bx + 8, by - 2), fill=(232, 190, 150))
        d.rectangle((bx + 9, by - 6, bx + 42, by - 2), fill=[(120, 170, 220), (220, 170, 120), (170, 200, 130)][i])
        # IV pole + bag + line, all inside the box
        d.line((bx + 40, by - 18, bx + 40, by - 4), fill=INK, width=1)
        d.rectangle((bx + 36, by - 24, bx + 44, by - 18), fill=(220, 240, 255), outline=INK, width=1)
        d.line((bx + 40, by - 18, bx + 28, by - 6), fill=(120, 120, 120), width=1)


def art_hk(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(210, 222, 235), (226, 234, 242), (240, 244, 248)])
    base = y1 - 6
    # polling station backdrop
    d.rectangle((x0 + 6, y0 + 8, x1 - 6, base), fill=(245, 242, 235), outline=GREY, width=1)
    # ballot box (centre)
    bx0, by0 = (x0 + x1) // 2 - 26, base - 34
    d.rectangle((bx0, by0, bx0 + 52, base), fill=RED, outline=DARKRED, width=2)
    d.rectangle((bx0 - 4, by0 - 6, bx0 + 56, by0), fill=DARKRED)
    d.rectangle((bx0 + 18, by0 - 4, bx0 + 34, by0 - 1), fill=(20, 20, 20))
    d.text((bx0 + 8, by0 + 8), "VOTE", font=F(12, bold=True), fill=(255, 255, 255))
    # ballot paper going in
    d.polygon([(bx0 + 22, by0 - 22), (bx0 + 38, by0 - 22), (bx0 + 34, by0 - 4), (bx0 + 26, by0 - 4)],
              fill=(255, 255, 255), outline=INK, width=1)
    # queue of voters (heads + shoulders)
    for i, px in enumerate((x0 + 16, x0 + 44, x1 - 52, x1 - 24)):
        py = base - 6
        d.ellipse((px, py - 22, px + 12, py - 10), fill=(232, 190, 150), outline=INK, width=1)
        d.polygon([(px - 3, py - 10), (px + 15, py - 10), (px + 13, py), (px - 1, py)],
                  fill=[NAVY, (90, 30, 30), (30, 90, 50), (60, 60, 90)][i])
    # check mark
    d.text((x0 + 8, y0 + 12), "✓", font=F(16, bold=True), fill=GREEN)


def art_finland(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(150, 170, 185), (175, 190, 200), (195, 205, 210)])
    # sea
    sy = y0 + int((y1 - y0) * 0.55)
    d.rectangle((x0, sy, x1, y1), fill=(40, 90, 130))
    for i in range(4):
        wy = sy + 5 + i * 6
        d.line((x0 + 4, wy, x1 - 4, wy), fill=(110, 160, 200), width=1)
    # coastline (top-left land)
    d.polygon([(x0, y0), (x0 + 70, y0), (x0 + 96, sy), (x0, sy)], fill=(90, 120, 80))
    # patrol boat
    bx, by = x0 + 96, sy + 8
    d.polygon([(bx, by), (bx + 52, by), (bx + 44, by + 10), (bx + 8, by + 10)], fill=(220, 220, 220), outline=INK, width=1)
    d.rectangle((bx + 14, by - 10, bx + 34, by), fill=(200, 60, 40))
    # helicopter
    hx, hy = x1 - 66, y0 + 14
    d.ellipse((hx, hy, hx + 34, hy + 12), fill=(60, 90, 60), outline=INK, width=1)
    d.line((hx + 34, hy + 6, hx + 52, hy + 6), fill=INK, width=2)
    d.line((hx + 4, hy - 6, hx + 30, hy - 6), fill=INK, width=2)
    # restricted-area buoys
    for bx2 in (x0 + 60, x0 + 110, x1 - 30):
        d.ellipse((bx2, sy + 20, bx2 + 8, sy + 26), fill=(255, 140, 0), outline=INK, width=1)


def art_dnipro(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(50, 40, 44), (80, 58, 52), (120, 84, 66)])
    base = y1 - 6
    # substation towers
    for tx in (x0 + 18, x0 + 60, x1 - 46):
        d.line((tx, base - 44, tx, base), fill=INK, width=2)
        d.line((tx - 10, base - 44, tx + 10, base - 44), fill=INK, width=2)
        d.line((tx - 8, base - 30, tx + 8, base - 30), fill=INK, width=2)
        d.rectangle((tx - 6, base - 14, tx + 6, base - 6), fill=(90, 90, 96))
    # power lines
    d.line((x0 + 18, base - 44, x1 - 46, base - 44), fill=(60, 60, 60), width=1)
    # rail tracks
    for ry in (base - 4, base - 1):
        d.line((x0, ry, x1, ry), fill=(40, 40, 40), width=2)
    for rx in range(x0 + 4, x1 - 4, 10):
        d.line((rx, base - 6, rx, base), fill=(40, 40, 40), width=1)
    # rail cars
    for i, cx in enumerate((x0 + 96, x0 + 130)):
        d.rectangle((cx, base - 24, cx + 30, base - 6), fill=[(120, 60, 40), (60, 90, 120)][i], outline=INK, width=1)
    # flames + smoke
    _flames(d, x0 + 96, base - 40, x0 + 170, base - 6, n=6, seed=33)
    _smoke(d, x0 + 100, y0 + 8, x0 + 170, y0 + 26, n=4, seed=35)


def art_vegas(d, x0, y0, x1, y1):
    _sky(d, x0, y0, x1, y1, [(16, 16, 40), (30, 22, 60), (52, 32, 78)])
    # strip skyline with neon
    base = y1 - 22
    import random
    rnd = random.Random(41)
    bx = x0
    while bx < x1 - 16:
        bw = rnd.randint(18, 32)
        bh = rnd.randint(22, 52)
        d.rectangle((bx, base - bh, bx + bw, base), fill=(24, 24, 48))
        _windows(d, bx + 2, base - bh + 3, bx + bw - 2, base - 3, max(2, bw // 8), max(2, bh // 10),
                 lit=[(255, 80, 160), (80, 220, 255), (255, 210, 60), (160, 255, 120)][rnd.randint(0, 3)],
                 dark=(34, 34, 58))
        bx += bw + 3
    # neon signs
    d.text((x0 + 8, y0 + 6), "★ LAS VEGAS ★", font=F(11, bold=True), fill=(255, 80, 160))
    # track
    d.rectangle((x0, base, x1, y1), fill=(40, 40, 44))
    d.line((x0, y1 - 8, x1, y1 - 8), fill=(255, 255, 255), width=1)
    for cx in range(x0 + 10, x1 - 10, 22):
        d.rectangle((cx, y1 - 12, cx + 10, y1 - 4), fill=(255, 255, 255))
    # race car
    cx0, cy0 = (x0 + x1) // 2 - 52, base + 2
    d.polygon([(cx0, cy0 + 10), (cx0 + 12, cy0 + 2), (cx0 + 70, cy0 + 2), (cx0 + 96, cy0 + 8),
               (cx0 + 104, cy0 + 12), (cx0, cy0 + 14)], fill=(200, 20, 40), outline=INK, width=1)
    d.polygon([(cx0 + 26, cy0 + 2), (cx0 + 36, cy0 - 6), (cx0 + 62, cy0 - 6), (cx0 + 68, cy0 + 2)],
              fill=(220, 220, 230), outline=INK, width=1)
    d.ellipse((cx0 + 14, cy0 + 10, cx0 + 28, cy0 + 20), fill=INK)
    d.ellipse((cx0 + 76, cy0 + 10, cx0 + 90, cy0 + 20), fill=INK)
    # checkered flag
    fx, fy = x1 - 30, y0 + 22
    d.line((fx, fy, fx, fy + 18), fill=INK, width=2)
    for r in range(2):
        for c in range(3):
            col = (20, 20, 20) if (r + c) % 2 == 0 else (255, 255, 255)
            d.rectangle((fx + 1 + c * 6, fy + r * 7, fx + 7 + c * 6, fy + 7 + r * 7), fill=col, outline=INK, width=1)


ART = {"cop31": art_cop31, "barrage": art_barrage, "sparta": art_sparta,
       "iran": art_iran, "chapo": art_chapo, "kryvyi": art_kryvyi,
       "drones186": art_drones186, "myanmar": art_myanmar, "manipur": art_manipur,
       "hk": art_hk, "finland": art_finland, "dnipro": art_dnipro, "vegas": art_vegas}


# Clip wrapper: every scene is drawn on a temp image of exactly the box size, so
# anything taller than the box (skylines, flames, IV poles) is clipped at the box
# edge instead of bleeding into the panel above or below.
def draw_art(name, img, x0, y0, x1, y1):
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (w, h), PAPER)
    td = ImageDraw.Draw(tmp)
    ART[name](td, 0, 0, w, h)
    img.paste(tmp, (x0, y0))

# ---------------------------------------------------------------- page layout
def draw_hero(img, d, h, x, y, w, hh):
    d.rectangle((x, y, x + w, y + hh), fill=CARD, outline=(200, 194, 178), width=1)
    tag(d, x + 8, y + 8, h["tag"])
    # art panel (clipped to the box)
    ax0, ay0, ax1, ay1 = x + 8, y + 32, x + w - 8, y + 186
    d.rectangle((ax0 - 1, ay0 - 1, ax1 + 1, ay1 + 1), fill=INK)
    draw_art(h["art"], img, ax0, ay0, ax1, ay1)
    # location line
    f_loc = F(11, bold=True)
    d.text((x + 8, ay1 + 8), f"{h['n']} — {h['loc']}", font=f_loc, fill=RED)
    # headline (2 lines max)
    f_head = F(15, bold=True, serif=True)
    yy = para(d, x + 8, ay1 + 26, h["head"], f_head, INK, w - 16, lh=18, max_lines=2)
    # summary (1 line)
    f_sum = F(11)
    yy = para(d, x + 8, yy + 3, h["summ"], f_sum, (60, 58, 52), w - 16, lh=14, max_lines=1)
    # caption strip at the bottom
    f_cap = F(10)
    d.text((x + 8, y + hh - 18), h["cap"], font=f_cap, fill=GREY)


def draw_secondary(img, d, s, x, y, w, hh):
    d.rectangle((x, y, x + w, y + hh), fill=CARD, outline=(200, 194, 178), width=1)
    # HARD RULE: the number chip lives in its own top strip, clear of art and text.
    chip(d, x + 13, y + 11, 9, s["n"])
    f_tag = F(9, bold=True)
    d.text((x + 27, y + 5), s["tag"], font=f_tag, fill=RED)
    # art band below the chip strip (clipped to the box)
    ax0, ay0, ax1, ay1 = x + 5, y + 21, x + w - 5, y + 60
    draw_art(s["art"], img, ax0, ay0, ax1, ay1)
    # headline below the art (2 lines max)
    f_head = F(10, bold=True)
    para(d, x + 6, ay1 + 3, s["head"], f_head, INK, w - 12, lh=11, max_lines=2)
    # one-line summary, truncated to fit the card width
    f_sum = F(8)
    txt = s["summ"]
    while d.textlength(txt, font=f_sum) > w - 12 and len(txt) > 4:
        txt = txt[:-1]
    if txt != s["summ"]:
        txt = txt[:-1] + "…"
    d.text((x + 6, y + hh - 12), txt, font=f_sum, fill=(70, 68, 62))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 20  # margin

    # ---- masthead
    f_title = F(30, bold=True, serif=True)
    d.text((M, 6), "THE WORLD TODAY", font=f_title, fill=INK)
    f_meta = F(12, bold=True)
    meta = "36 STORIES  •  5 REGIONS"
    d.text((W - M - d.textlength(meta, font=f_meta), 16), meta, font=f_meta, fill=RED)
    d.line((M, 44, W - M, 44), fill=INK, width=2)

    # ---- giant date line
    f_date = F(40, bold=True, serif=True)
    date_txt = "SUNDAY, 22 NOVEMBER 2026"
    d.text(((W - d.textlength(date_txt, font=f_date)) / 2, 50), date_txt, font=f_date, fill=RED)
    d.line((M, 96, W - M, 96), fill=INK, width=1)

    # ---- 3-story sub-headline
    f_sub = F(13, bold=True)
    sub = "COP31 VOTE WITHOUT FOSSIL FUELS  •  400+ DRONES OVER UKRAINE  •  RUSSIAN SHIP ABLAZE IN THE BALTIC"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 102), sub, font=f_sub, fill=INK)
    d.line((M, 122, W - M, 122), fill=INK, width=1)

    # ---- number strip
    y0, y1 = 128, 176
    cw = (W - 2 * M) / 6
    f_num = F(34, bold=True, serif=True)
    f_lab = F(9, bold=True)
    for i, (num, lab) in enumerate(STRIP):
        cx = M + i * cw
        if i:
            d.line((cx, y0 + 4, cx, y1 - 4), fill=(200, 194, 178), width=1)
        nw = d.textlength(num, font=f_num)
        d.text((cx + (cw - nw) / 2, y0), num, font=f_num, fill=RED if i == 1 else INK)
        lw = d.textlength(lab, font=f_lab)
        d.text((cx + (cw - lw) / 2, y0 + 38), lab, font=f_lab, fill=GREY)
    d.line((M, y1, W - M, y1), fill=INK, width=1)

    # ---- region bar
    y0, y1 = 182, 204
    total = sum(c for _, c, _ in REGIONS)
    x = M
    f_reg = F(11, bold=True)
    for name, cnt, col in REGIONS:
        wseg = (W - 2 * M) * cnt / total
        d.rectangle((x, y0, x + wseg - 1, y1), fill=col)
        lab = f"{name} {cnt}"
        lw = d.textlength(lab, font=f_reg)
        d.text((x + (wseg - lw) / 2, y0 + 4), lab, font=f_reg, fill=(255, 255, 255))
        x += wseg

    # ---- heroes
    hy, hh = 212, 288
    hw = 320
    for i, h in enumerate(HEROES):
        draw_hero(img, d, h, M + i * (hw + 12), hy, hw, hh)

    # ---- secondaries: 5 columns x 2 rows
    sy, sh = 508, 100
    sw = 190
    gap = 8
    for i, s in enumerate(SECONDARIES):
        col, row = i % 5, i // 5
        draw_secondary(img, d, s, M + col * (sw + gap), sy + row * (sh + 4), sw, sh)

    # ---- BY THE CLOCK strip
    y0, y1 = 718, 748
    d.rectangle((M, y0, W - M, y1), fill=NAVY)
    f_clk = F(11, bold=True)
    d.text((M + 10, y0 + 9), "BY THE CLOCK", font=f_clk, fill=(255, 210, 60))
    f_ci = F(11)
    cx = M + 132
    for t, what in CLOCK:
        d.text((cx, y0 + 9), t, font=F(11, bold=True), fill=(255, 255, 255))
        cx += d.textlength(t, font=F(11, bold=True)) + 6
        d.text((cx, y0 + 9), what, font=f_ci, fill=(210, 215, 230))
        cx += d.textlength(what, font=f_ci) + 18
        if (t, what) != CLOCK[-1]:
            d.text((cx - 10, y0 + 9), "•", font=f_ci, fill=(255, 210, 60))

    return img, d

# ---------------------------------------------------------------- map + also on + date check
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73), (-70, 62),
           (-60, 55), (-55, 47), (-70, 44), (-75, 38), (-80, 32), (-85, 30), (-90, 21),
           (-95, 18), (-105, 20), (-110, 24), (-120, 34), (-125, 40), (-125, 48),
           (-140, 60), (-155, 58), (-165, 60)],
    "GL": [(-45, 60), (-30, 68), (-20, 70), (-25, 76), (-55, 76), (-58, 70)],
    "SA": [(-80, 10), (-70, 12), (-60, 8), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
           (-48, -28), (-55, -35), (-65, -45), (-70, -55), (-75, -50), (-73, -40),
           (-72, -30), (-70, -18), (-77, -12), (-80, -3)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
           (43, 12), (48, 11), (51, 10), (40, -2), (40, -12), (35, -25), (28, -33),
           (18, -35), (15, -27), (12, -18), (9, 4), (-8, 5), (-13, 8)],
    "EUAS": [(-10, 36), (-9, 43), (0, 48), (5, 58), (10, 57), (18, 56), (21, 55), (28, 60),
             (30, 62), (30, 70), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76),
             (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55), (150, 45),
             (140, 40), (130, 35), (122, 30), (114, 22), (108, 12), (104, 8), (100, 6),
             (95, 10), (90, 22), (85, 20), (80, 13), (75, 8), (70, 20), (65, 25),
             (58, 25), (52, 26), (48, 30), (44, 29), (40, 36), (36, 36), (30, 36),
             (26, 38), (22, 40), (18, 40), (12, 44), (8, 44), (2, 44), (-2, 48), (-5, 48)],
    "AU": [(113, -22), (114, -30), (115, -35), (125, -32), (130, -32), (135, -35),
           (140, -38), (145, -38), (150, -37), (153, -27), (150, -22), (146, -19),
           (142, -11), (136, -12), (130, -13), (122, -17), (118, -20)],
}

# (story number, lon, lat, chip dx, chip dy) — offsets spread the Ukraine / Finland /
# Myanmar clusters so chips never overlap; a leader line joins chip to true location.
PINS = [(1, 30.7, 36.9, 0, -12), (2, 30.5, 50.5, -2, -18), (3, 27.0, 60.0, 16, -14),
        (4, 50.6, 26.2, 0, -12), (5, -108.5, 25.6, 12, 10), (6, 33.4, 47.9, -22, 14),
        (7, 33.0, 49.5, 18, -4), (8, 94.6, 24.2, -16, -14), (9, 93.0, 23.5, 14, 12),
        (10, 114.2, 22.3, 0, -14), (11, 25.0, 61.0, -18, -14), (12, 35.0, 48.5, 20, 16),
        (13, -115.1, 36.2, -14, -12)]

ALSO_SHORT = [
    (14, "Gaza: 129 bodies from rubble", "AJ"),
    (15, "COP31: 130 nations want fossil text back", "Reuters"),
    (16, "COP31: EU — 'good deal or no deal'", "Reuters"),
    (17, "Zelensky: barrage 'biggest this year'", "CNN"),
    (18, "Bahrain: Iranian strike sets site ablaze", "AJ"),
    (19, "US denies Iran damaged an F-16", "US"),
    (20, "Iran tankers move to break US blockade", "GT"),
    (21, "Washington halts gun checks over breach", "WSP"),
    (22, "Finland: air, sea limits around wreck", "NY Post"),
    (23, "Sparta II anchored off Loviisa", "BG"),
    (24, "Sinaloa: 4 soldiers among 11 dead", "Def. Min."),
    (25, "October 1.8C hotter than the 1800s", "Berkeley"),
    (26, "COP31: 35% of energy from power by 2035", "draft"),
    (27, "COP31 admits 1.5C will be overshot", "draft"),
    (28, "Gaza: 9 killed, 55 hurt in 48 hours", "Health Min."),
    (29, "Gaza City drone strike kills 3", "AJ"),
    (30, "NATO condemns missiles over Poland", "NATO"),
    (31, "France calls UN council over Poland", "Reuters"),
    (32, "COP31: Saudis block fossil-fuel text", "Guardian"),
    (33, "COP31: 1bn-tonne carbon capture goal", "draft"),
    (34, "Lviv: missile hits flats, 2 killed", "ANI"),
    (35, "Manipur: 6 held, 2,400 litres seized", "police"),
    (36, "Gaza: 350,000 families homeless", "Housing Min."),
]


def draw_map(d, x0, y0, x1, y1):
    d.rectangle((x0, y0, x1, y1), fill=(196, 214, 226), outline=(160, 160, 150), width=1)
    f_t = F(10, bold=True)
    d.text((x0 + 6, y0 + 4), "WHERE IT HAPPENED — PINS MATCH STORY NUMBERS", font=f_t, fill=NAVY)
    mx0, my0, mx1, my1 = x0 + 4, y0 + 20, x1 - 4, y1 - 4
    mw, mh = mx1 - mx0, my1 - my0

    def proj(lon, lat):
        return (mx0 + (lon + 180) / 360 * mw, my0 + (75 - lat) / 135 * mh)

    for pts in CONTINENTS.values():
        d.polygon([proj(lon, lat) for lon, lat in pts], fill=(214, 206, 182),
                  outline=(120, 112, 96), width=1)
    # equator + tropics (faint)
    for lat in (0, 23.4, -23.4):
        _, ey = proj(0, lat)
        d.line((mx0, ey, mx1, ey), fill=(170, 190, 205), width=1)
    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        cx, cy = int(px) + dx, int(py) + dy
        if dx or dy:
            d.line((px, py, cx, cy), fill=(60, 60, 60), width=1)
            d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=INK)
        chip(d, cx, cy, 8, n)


def draw_also_on(d, x0, y0, x1, y1):
    f_t = F(11, bold=True)
    d.text((x0, y0), "ALSO ON — 14 TO 36", font=f_t, fill=INK)
    d.line((x0, y0 + 16, x1, y0 + 16), fill=INK, width=1)
    f_i = F(9)
    f_n = F(9, bold=True)
    col_w = (x1 - x0 - 12) / 2
    yy = y0 + 22
    for i, (n, txt, src) in enumerate(ALSO_SHORT):
        col = i // 12
        row = i % 12
        xx = x0 + col * (col_w + 12)
        yline = yy + row * 12
        d.text((xx, yline), f"{n}.", font=f_n, fill=RED)
        line = f"{txt} ({src})"
        if d.textlength(line, font=f_i) > col_w - 18:
            line = txt  # drop the outlet first; keep the story text whole
        while d.textlength(line, font=f_i) > col_w - 18 and len(line) > 4:
            line = line[:-1]
        if line != f"{txt} ({src})" and line != txt:
            line = line[:-1] + "…"
        d.text((xx + 18, yline), line, font=f_i, fill=INK)


def finish(img, d):
    M = 20
    # ---- map + ALSO ON
    draw_map(d, M, 756, 500, 924)
    draw_also_on(d, 512, 756, W - M, 924)

    # ---- DATE CHECK
    y0, y1 = 932, 992
    d.rectangle((M, y0, W - M, y1), outline=RED, width=2)
    f_t = F(11, bold=True)
    d.text((M + 8, y0 + 5), "DATE CHECK — WIRES READ TO 08:00 UTC, SUNDAY 22 NOVEMBER 2026",
           font=f_t, fill=RED)
    f_b = F(10)
    lines = [
        "LEFT OUT ON PURPOSE: FBI NCIC hack (first reported 20 Nov)  •  Peru 6.9 quake (20 Nov)  •  Nigeria boat (21 Nov)  •  Bolsonaro in ICU (21 Nov)  •  Poland airspace breach (20 Nov)  •  Kerch Bridge (18 Nov)  •  Shenzhen APEC (19 Nov)  •  GTA VI launch (19 Nov)  •  Anthropic IPO (19 Nov)",
        "NOT YET: COP31 final vote result  •  Liverpool v Man Utd result (16:30 GMT)  •  ATP Finals result     CLAIM, NOT CONFIRMED: Iran's radar strikes  •  scope of the FBI breach",
    ]
    yy = y0 + 22
    for ln in lines:
        yy = para(d, M + 8, yy, ln, f_b, INK, W - 2 * M - 16, lh=13)

    # ---- footer
    f_f = F(9)
    foot = "SOURCES: BBC  •  REUTERS  •  CNN  •  AP  •  ANI  •  AL JAZEERA  •  XINHUA  •  HK GOVT  •  FINLAND MOD  •  UKRAINE AIR FORCE  —  EVERY STORY NUMBERED, EVERY STORY SOURCED"
    d.text(((W - d.textlength(foot, font=f_f)) / 2, 998), foot, font=f_f, fill=GREY)


def main():
    img, d = build()
    finish(img, d)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
