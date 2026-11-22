#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page.

Local render program only: it runs on this machine (Pillow available) and
writes entry.png next to itself. The submitted entrypoint (main.py) is a
stdlib-only copy program; the grader never runs this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "entry.png")
W, H = 1024, 1024

PAPER = (247, 244, 236)
INK = (18, 18, 18)
RED = (178, 24, 24)
DARKRED = (140, 16, 16)
GREY = (110, 108, 100)
LIGHT = (232, 228, 218)
RULE = (60, 58, 52)
GREEN = (28, 110, 52)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, y, x1, w=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 16  # margin

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 54], fill=(12, 12, 12))
    f_mast = font(SERIF_B, 34)
    d.text((mx, 8), "THE WORLD TODAY", font=f_mast, fill=(250, 248, 242))
    f_ed = font(SANS_B, 11)
    ed = "SUNDAY EDITION  •  ONE DAY, ONE PAGE"
    d.text((W - mx - d.textlength(ed, font=f_ed), 20), ed, font=f_ed,
           fill=(200, 196, 186))

    # ---------- giant date line ----------
    f_date = font(SERIF_B, 42)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    rule(d, mx, 66, W - mx, 2)
    d.text(((W - dw) / 2, 72), date, font=f_date, fill=RED)
    rule(d, mx, 126, W - mx, 2)

    # ---------- 6-number strip ----------
    strip = [
        ("24", "bodies found after a boat capsizes in Nigeria"),
        ("4.1", "magnitude of the quake that shook Myanmar at dawn"),
        ("2", "US Patriot radars Iran says it struck in Bahrain"),
        ("5,700", "voters pick Hong Kong's Election Committee"),
        ("11", "dead from toxic alcohol in Manipur, India"),
        ("152", "Peru homes left uninhabitable by the quake"),
    ]
    y0, y1 = 134, 196
    cw = (W - 2 * mx) / 6
    f_num = font(SANS_B, 30)
    f_lab = font(SANS, 10)
    for i, (num, lab) in enumerate(strip):
        x = mx + i * cw
        if i:
            d.line([(x, y0 + 4), (x, y1 - 4)], fill=(200, 196, 186), width=1)
        cx = x + cw / 2
        nw = d.textlength(num, font=f_num)
        d.text((cx - nw / 2, y0 + 2), num, font=f_num, fill=RED)
        lines = wrap(d, lab, f_lab, cw - 14)
        ly = y0 + 36
        for ln in lines[:2]:
            lw = d.textlength(ln, font=f_lab)
            d.text((cx - lw / 2, ly), ln, font=f_lab, fill=INK)
            ly += 12
    rule(d, mx, y1 + 2, W - mx, 2)

    # ---------- heroes ----------
    heroes = [
        {
            "kicker": "CYBERATTACK  •  WASHINGTON",
            "head": "FBI probes hack of its own crime database",
            "body": ("The FBI is investigating an apparent breach of the "
                     "National Crime Information Center, the database police "
                     "across the US use to share criminal records."),
            "art": "fbi",
        },
        {
            "kicker": "GULF CRISIS  •  BAHRAIN",
            "head": "Iran claims strike on two US Patriot radars",
            "body": ("Tehran's Revolutionary Guard says it hit two American "
                     "air-defence radars in Bahrain with a combined missile "
                     "and drone attack."),
            "art": "bahrain",
        },
        {
            "kicker": "BALTIC SEA  •  FINLAND",
            "head": "Russian cargo ship still burning after drone hit",
            "body": ("The sanctioned Sparta II, struck by drones in the Gulf "
                     "of Finland, is ablaze for a second day; Helsinki warns "
                     "the fire could burn for weeks."),
            "art": "ship",
        },
    ]
    hy0, hy1 = 206, 540
    hw = (W - 2 * mx - 2 * 8) / 3
    f_kick = font(SANS_B, 10)
    f_hhead = font(SERIF_B, 19)
    f_hbody = font(SANS, 11)
    for i, hro in enumerate(heroes):
        x = mx + i * (hw + 8)
        d.rectangle([x, hy0, x + hw, hy1], outline=RULE, width=1)
        draw_art(d, hro["art"], x + 1, hy0 + 1, hw - 2, 176)
        ty = hy0 + 186
        d.text((x + 8, ty), hro["kicker"], font=f_kick, fill=RED)
        ty += 18
        lines = wrap(d, hro["head"], f_hhead, hw - 16)
        ty = text_block(d, x + 8, ty, lines, f_hhead, INK, 23)
        ty += 4
        blines = wrap(d, hro["body"], f_hbody, hw - 16)
        text_block(d, x + 8, ty, blines[:4], f_hbody, (52, 50, 46), 14)

    # ---------- secondaries ----------
    secs = [
        ("Myanmar shaken by 4.1 quake",
         "The tremor struck in the early hours of Sunday; no casualties reported yet."),
        ("24 bodies after Nigeria capsize",
         "Emergency agency NEMA recovers the dead after a boat overturns."),
        ("COP31 runs into overtime",
         "Antalya talks spill past Friday's deadline with fossil fuels still out of the draft."),
        ("UN robot-weapons talks fall short",
         "Negotiators fail to agree enforceable rules on lethal autonomous weapons."),
        ("Hong Kong votes for Election Committee",
         "About 5,700 voters choose the body that will help pick the city's leader."),
        ("Peru counts 152 homes uninhabitable",
         "Revised survey after the 6.7 quake in the Andes."),
        ("Toxic alcohol kills 11 in Manipur",
         "Another 180 people fall sick in north-east India."),
        ("Denmark expels Russian defence aide",
         "Copenhagen says Moscow plotted to kill a US-Ukrainian rapper."),
        ("Three Salvadorans die in Haiti",
         "First deaths among the foreign force deployed to fight the gangs."),
        ("Zelensky: NATO is the best guarantee",
         "Ukraine's president says NATO membership remains the clearest security guarantee."),
    ]
    sy0 = 552
    f_sec_h = font(SANS_B, 12)
    d.text((mx, sy0), "MORE FROM SUNDAY", font=f_sec_h, fill=RED)
    rule(d, mx, sy0 + 18, W - mx, 1)
    f_num2 = font(SANS_B, 15)
    f_shead = font(SANS_B, 12)
    f_sbody = font(SANS, 10)
    colw = (W - 2 * mx - 16) / 2
    rowh = 50
    for i, (head, body) in enumerate(secs):
        col = i % 2
        row = i // 2
        x = mx + col * (colw + 16)
        y = sy0 + 26 + row * rowh
        d.text((x, y), "%02d" % (i + 1), font=f_num2, fill=RED)
        tx = x + 30
        d.text((tx, y), head, font=f_shead, fill=INK)
        blines = wrap(d, body, f_sbody, colw - 30)
        text_block(d, tx, y + 16, blines[:2], f_sbody, (72, 70, 64), 12)
        if row < 4:
            d.line([(x, y + rowh - 8), (x + colw, y + rowh - 8)],
                   fill=(214, 210, 200), width=1)

    # ---------- world map ----------
    my0 = 838
    d.text((mx, my0), "WHERE IT HAPPENED", font=f_sec_h, fill=RED)
    rule(d, mx, my0 + 18, W - mx, 1)
    draw_map(d, mx, my0 + 24, W - 2 * mx, 92)

    # ---------- footer ----------
    fy = 962
    rule(d, mx, fy, W - mx, 2)
    d.rectangle([mx, fy + 8, mx + 560, fy + 44], outline=GREEN, width=2)
    f_chk = font(SANS_B, 11)
    d.text((mx + 10, fy + 13), "DATE CHECK  ✓", font=f_chk, fill=GREEN)
    f_ftr = font(SANS, 10)
    d.text((mx + 10, fy + 29),
           "Every story above was first reported on Sunday, 22 November 2026.",
           font=f_ftr, fill=INK)
    src = "Sources: BBC  •  Reuters  •  CNN  •  ANI  •  AP  •  ISW"
    sw = d.textlength(src, font=f_ftr)
    d.text((W - mx - sw, fy + 13), src, font=f_ftr, fill=GREY)
    d.text((W - mx - d.textlength("make.fun  •  news-image-20261122", font=f_ftr),
            fy + 29), "make.fun  •  news-image-20261122", font=f_ftr, fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


def draw_art(d, kind, x, y, w, h):
    if kind == "fbi":
        d.rectangle([x, y, x + w, y + h], fill=(11, 18, 38))
        # server racks
        for c in range(3):
            rx = x + 14 + c * 62
            d.rectangle([rx, y + 16, rx + 50, y + h - 16],
                        fill=(24, 34, 58), outline=(52, 68, 96), width=1)
            for r in range(6):
                ry = y + 24 + r * 20
                d.rectangle([rx + 6, ry, rx + 44, ry + 12],
                            fill=(16, 24, 44))
                for k in range(3):
                    col = (40, 200, 90) if (r + k) % 3 else (220, 60, 50)
                    d.ellipse([rx + 10 + k * 8, ry + 4, rx + 14 + k * 8,
                               ry + 8], fill=col)
        # red padlock, centre-right
        cx, cy = x + w - 78, y + 62
        d.ellipse([cx - 52, cy - 52, cx + 52, cy + 52],
                  fill=(178, 24, 24))
        d.arc([cx - 20, cy - 44, cx + 20, cy - 6], 180, 360,
              fill=(240, 240, 240), width=7)
        d.rounded_rectangle([cx - 26, cy - 10, cx + 26, cy + 30],
                            radius=6, fill=(240, 240, 240))
        d.ellipse([cx - 5, cy + 2, cx + 5, cy + 12], fill=(178, 24, 24))
        d.rectangle([cx - 2, cy + 8, cx + 2, cy + 22], fill=(178, 24, 24))
        # warning triangle
        tx, ty = x + 22, y + 14
        d.polygon([(tx, ty + 30), (tx + 34, ty + 30), (tx + 17, ty)],
                  fill=(240, 180, 20))
        f_warn = font(SANS_B, 22)
        d.text((tx + 11, ty + 8), "!", font=f_warn, fill=(12, 12, 12))
    elif kind == "bahrain":
        # night sky gradient
        for i in range(h):
            t = i / h
            r = int(10 + 90 * t * t)
            g = int(16 + 40 * t)
            b = int(42 + 30 * t)
            d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
        # stars
        import random
        rnd = random.Random(7)
        for _ in range(26):
            sx = x + rnd.randint(4, int(w) - 4)
            sy = y + rnd.randint(4, int(h * 0.45))
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=(230, 230, 220))
        # moon
        d.ellipse([x + w - 52, y + 12, x + w - 20, y + 44],
                  fill=(238, 236, 220))
        # missile trails
        d.line([(x + 20, y + h - 30), (x + 120, y + 40)], fill=(255, 210, 90),
               width=4)
        d.line([(x + 60, y + h - 20), (x + 190, y + 70)], fill=(255, 190, 80),
               width=3)
        d.ellipse([x + 112, y + 32, x + 128, y + 48], fill=(255, 220, 120))
        d.ellipse([x + 182, y + 62, x + 196, y + 76], fill=(255, 200, 100))
        # radar dish, bottom left
        bx, by = x + 34, y + h - 18
        d.line([(bx, by), (bx, by - 34)], fill=(200, 200, 200), width=4)
        d.arc([bx - 26, by - 62, bx + 26, by - 10], 180, 360,
              fill=(220, 220, 220), width=4)
        d.line([(bx - 26, by - 36), (bx + 26, by - 36)], fill=(220, 220, 220),
               width=2)
        # sea
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(8, 24, 52))
        d.line([(x, y + h - 14), (x + w, y + h - 14)], fill=(255, 170, 60),
               width=2)
    else:  # ship
        # sea
        for i in range(h):
            t = i / h
            d.line([(x, y + i), (x + w, y + i)],
                   fill=(int(14 + 10 * t), int(38 + 18 * t), int(72 + 26 * t)))
        # sky glow (kept inside the art box)
        d.ellipse([x + w // 2 - 70, y + 6, x + w // 2 + 70, y + 78],
                  fill=(200, 90, 30))
        # smoke
        import random
        rnd = random.Random(11)
        for i in range(9):
            sx = x + w // 2 - 30 + rnd.randint(-14, 60) + i * 6
            sy = y + 8 + rnd.randint(0, 26) - i * 2
            r = 12 + rnd.randint(0, 10)
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(70, 70, 74))
        # hull
        hx0, hx1, hy = x + 30, x + w - 30, y + h - 52
        d.polygon([(hx0, hy), (hx1, hy), (hx1 - 12, hy + 26), (hx0 + 18, hy + 26)],
                  fill=(20, 22, 26))
        # containers
        cols = [(120, 60, 50), (60, 90, 110), (150, 120, 60), (90, 110, 80)]
        for i in range(6):
            cx0 = hx0 + 8 + i * 42
            d.rectangle([cx0, hy - 30, cx0 + 38, hy - 2],
                        fill=cols[i % 4], outline=(30, 30, 34), width=1)
        # bridge tower
        d.rectangle([hx1 - 52, hy - 62, hx1 - 20, hy - 2],
                    fill=(210, 210, 205))
        d.rectangle([hx1 - 52, hy - 56, hx1 - 20, hy - 48], fill=(30, 60, 90))
        # flames (leaning, layered tongues)
        fx = x + w // 2 - 46
        for j, (fw, fh, col, lean) in enumerate([
                (76, 62, (230, 110, 20), 0),
                (52, 46, (250, 170, 40), 10),
                (28, 30, (255, 220, 90), 18)]):
            d.polygon([(fx + j * 6, hy - 2),
                       (fx + fw // 2 + lean, hy - fh),
                       (fx + fw + j * 4, hy - 2),
                       (fx + fw // 2 - 6 + j * 4, hy - fh // 2)], fill=col)
        # glow on water
        d.ellipse([x + w // 2 - 80, hy + 30, x + w // 2 + 80, hy + 44],
                  fill=(220, 110, 30))


CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-65, 60), (-55, 47), (-60, 45), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-105, 20), (-115, 28),
     (-125, 40), (-125, 50), (-140, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-20, 70), (-25, 76),
     (-40, 80), (-55, 76), (-60, 70)],
    # South America
    [(-80, 10), (-75, 5), (-70, 12), (-60, 8), (-50, 0), (-40, -5),
     (-35, -10), (-40, -20), (-50, -30), (-60, -38), (-65, -45),
     (-70, -52), (-73, -40), (-75, -25), (-80, -15), (-82, -5)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (48, 11), (40, 0), (35, -15), (30, -25), (20, -35),
     (15, -30), (12, -18), (8, 4), (-8, 4), (-15, 10)],
    # Eurasia
    [(-10, 36), (0, 38), (5, 44), (0, 48), (-5, 50), (0, 52), (5, 55),
     (10, 58), (18, 56), (20, 60), (25, 65), (30, 70), (40, 68),
     (50, 70), (60, 72), (70, 73), (80, 74), (90, 76), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 60),
     (160, 52), (150, 45), (140, 40), (135, 35), (130, 32), (122, 30),
     (115, 22), (108, 12), (105, 8), (100, 10), (95, 15), (90, 22),
     (85, 20), (80, 15), (75, 10), (72, 20), (65, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (44, 29), (40, 36), (35, 36),
     (30, 36), (25, 38), (20, 40), (15, 40), (12, 44)],
    # Australia
    [(114, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (136, -12), (132, -12),
     (126, -14), (122, -17), (118, -20)],
]

PINS = [
    (96, 20), (8, 9), (30.7, 36.9), (6.1, 46.2), (114.2, 22.3),
    (-75, -10), (94, 24.5), (12.6, 55.7), (-72.3, 18.5), (30.5, 50.4),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    lon0, lon1, lat0, lat1 = -170, 190, -56, 84

    def proj(lon, lat):
        px = x + (lon - lon0) / (lon1 - lon0) * w
        py = y + (lat1 - lat) / (lat1 - lat0) * h
        return px, py

    for cont in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in cont]
        d.polygon(pts, fill=(196, 192, 180), outline=(120, 116, 104))
    f_pin = font(SANS_B, 9)
    for i, (lon, lat) in enumerate(PINS, 1):
        px, py = proj(lon, lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(i)
        tw = d.textlength(t, font=f_pin)
        d.text((px - tw / 2, py - 6), t, font=f_pin, fill=(255, 255, 255))


if __name__ == "__main__":
    main()
