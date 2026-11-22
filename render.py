#!/usr/bin/env python3
"""Render the news-image-20261122 R2 front page.

Draws a 1024x1024 newspaper front page summing up Sunday 22 November
2026: masthead with story/region counts, giant date line, 6-number strip,
coloured region bar, 3 illustrated heroes, 10 illustrated secondaries in
a 5-column grid, a recognisable dotted world map with numbered pins,
an ALSO ON list to 32 stories, a DATE CHECK box written as proof, and a
sources footer. All art is procedural, drawn in code with Pillow.

Run: python3 render.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024

# ---- palette -----------------------------------------------------------
INK = (20, 20, 20)
PAPER = (250, 246, 236)
CREAM = (244, 238, 226)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
BLACK = (15, 15, 15)
GREY = (110, 110, 108)
LGREY = (200, 196, 188)
SEA = (196, 220, 232)
LAND = (232, 220, 188)
LAND_EDGE = (180, 164, 128)
WHITE = (255, 255, 255)
NAVY = (24, 44, 84)
TEAL = (18, 110, 110)
ORANGE = (214, 110, 30)
GREEN = (46, 110, 60)
GOLD = (198, 158, 40)
PURPLE = (96, 60, 120)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, width, fill, spacing=3, max_lines=None):
    lines = wrap(d, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def chip(d, x, y, text, bg=RED, fg=WHITE, size=10):
    f = font(SANS_B, size)
    tw = d.textlength(text, font=f)
    pad = 5
    d.rounded_rectangle([x, y, x + tw + pad * 2, y + size + 7],
                        radius=3, fill=bg)
    d.text((x + pad, y + 2), text, font=f, fill=fg)
    return tw + pad * 2


# ---- story data --------------------------------------------------------
# region codes: EU europe, AF africa, AP asia-pacific, AM americas,
# ME middle east, WO world
HEROES = [
    dict(num=1, region="AM", tag="CYBERATTACK",
         head="FBI probes hack of its national crime database",
         summ="NCIC system hit in the second FBI breach in months; who did it is still unconfirmed.",
         cap="National Crime Information Center  •  Washington  •  CNN / AP",
         scene="fbi"),
    dict(num=2, region="ME", tag="MIDDLE EAST",
         head="Iran says it hit two US Patriot radars in Bahrain",
         summ="IRGC claims a missile-and-drone strike on US air defences; Washington has not confirmed it.",
         cap="Bahrain  •  IRGC claim  •  ANI",
         scene="iran"),
    dict(num=3, region="EU", tag="BALTIC SEA",
         head="Russian cargo ship burns after drone strike",
         summ="Sparta II ablaze in the Gulf of Finland; 16 crew evacuated as Finland leads the rescue.",
         cap="Gulf of Finland  •  Finnish Border Guard  •  Reuters / Yle",
         scene="sparta"),
]

SECONDARIES = [
    dict(num=4, region="WO", tag="COP31",
         summ="COP31 gets a new text, still no deal: revised draft tabled early Sunday; fossil fuels still out. (Reuters)",
         scene="cop"),
    dict(num=5, region="AM", tag="MEXICO",
         summ="Cartel kingpin 'El Chapo Isidro' arrested in a shoot-out; he was on the FBI's 10 most wanted. (BBC)",
         scene="isidro"),
    dict(num=6, region="EU", tag="UKRAINE",
         summ="Ukrainian drones strike a Russian National Guard HQ in Krasnodar overnight. (Kyiv Independent)",
         scene="krasnodar"),
    dict(num=7, region="EU", tag="UKRAINE",
         summ="Glide bombs rain on Zaporizhzhia City: 12 KAB bombs and a jet drone hit overnight. (AMK)",
         scene="zaporizhzhia"),
    dict(num=8, region="ME", tag="GAZA",
         summ="Israeli tanks roll into central Gaza, first ground incursion since the ceasefire; 129 bodies recovered. (Reuters)",
         scene="gaza"),
    dict(num=9, region="AP", tag="MYANMAR",
         summ="4.1 quake shakes Myanmar at dawn; India's seismology centre reports no casualties yet. (ANI)",
         scene="myanmar"),
    dict(num=10, region="AP", tag="HONG KONG",
         summ="Hong Kong votes for its 1,500-seat Election Committee: 5,700 voters, turnout 69.6% by 11am. (China Daily)",
         scene="hongkong"),
    dict(num=11, region="AP", tag="INDIA",
         summ="Toxic liquor toll in Manipur rises to 16; some 600 in hospital, six arrested. (Xinhua)",
         scene="manipur"),
    dict(num=12, region="EU", tag="UKRAINE",
         summ="Russian drones hit Dnipropetrovsk cities overnight: rail yards and substations in flames. (AMK)",
         scene="dnipro"),
    dict(num=13, region="ME", tag="HORMUZ",
         summ="Iran cuts its Hormuz reopening plan to two days after the week's tanker strikes. (WaitWhatNews)",
         scene="hormuz"),
]

ALSO = [
    (14, "AF", "Al-Shabaab claims hundreds dead in Somalia ambush", "C54"),
    (15, "AF", "Kenya discharges last Ebola patient; DRC toll passes 5,300", "C54"),
    (16, "AF", "Ghana unveils Heritage banknotes honouring Nkrumah, Annan", "C54"),
    (17, "EU", "Norway court voids climate-disputed oil licences", "C54"),
    (18, "AF", "Sahel states restart dialogue with West Africa bloc", "C54"),
    (19, "AF", "DRC president enacts constitutional reform law", "C54"),
    (20, "EU", "EU hunts for new ECB chief as Lagarde resigns", "C54"),
    (21, "AP", "Japan and India agree to deepen military cooperation", "AP"),
    (22, "WO", "TikTok launches global deepfake-detection tool", "AP"),
    (23, "EU", "Zelenskyy: NATO entry is Ukraine's clearest guarantee", "ANI"),
    (24, "AM", "Teen gamer and his mother help FBI rescue missing girl", "BBC"),
    (25, "AM", "US declassifies more UFO footage from the Middle East", "BBC"),
    (26, "AF", "ANC fights to hold South Africa's big cities", "BBC"),
    (27, "EU", "Denmark accuses Russia of plot to kill US-Ukrainian rapper", "BBC"),
    (28, "WO", "UN talks end with no clear curb on AI 'killer robots'", "Japako"),
    (29, "AP", "Australia bowls first as Smith misses South Africa decider", "C54"),
    (30, "AF", "Nigeria starts building naval ships at home", "C54"),
    (31, "ME", "Eisenkot's Yashar party opens coalition talks in Israel", "ANI"),
    (32, "EU", "Trafalgar Square Christmas tree felled in Norway", "BBC"),
]

NUMBERS = [
    ("0", "COP31 deals agreed in Antalya"),
    ("2", "US Patriot radars Iran says it hit"),
    ("16", "dead in Manipur toxic liquor tragedy"),
    ("80", "drones shot down over Leningrad overnight"),
    ("129", "bodies recovered from Gaza rubble"),
    ("5,700", "Hong Kong Election Committee voters"),
]

REGIONS = [
    ("EUROPE", 9, NAVY),
    ("AFRICA", 7, ORANGE),
    ("ASIA-PACIFIC", 5, TEAL),
    ("AMERICAS", 4, GREEN),
    ("MIDDLE EAST", 4, (150, 60, 60)),
    ("WORLD", 3, GREY),
]

DATE_CHECK = (
    "Wires read up to 04:00 UTC, Sunday 22 November 2026.  "
    "Left out as other days' news: the Peru earthquake (20 Nov), Russian "
    "missiles landing in Poland (19 Nov), the Kerch Bridge strikes (earlier "
    "this week), the Shenzhen summit (19 Nov), Bolsonaro taken to ICU "
    "(21 Nov).  Not yet happened, so not shown: the final COP31 text; the "
    "Las Vegas GP result.  Still unconfirmed at draw time: who hacked the "
    "FBI's NCIC database."
)

# ---- hero scenes -------------------------------------------------------
def scene_fbi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 28, 56))
    # server racks filling the panel
    for r in range(3):
        rx = x + 12 + r * (w // 3)
        d.rectangle([rx, y + 10, rx + w // 3 - 16, y + h - 12],
                    fill=(30, 52, 96), outline=(90, 120, 170))
        for s in range(5):
            sy = y + 18 + s * 17
            d.rectangle([rx + 6, sy, rx + w // 3 - 22, sy + 9],
                        fill=(52, 84, 138))
            for li in range(3):
                col = (90, 220, 120) if (s + li) % 3 else (255, 200, 60)
                d.ellipse([rx + 9 + li * 9, sy + 2, rx + 15 + li * 9, sy + 8],
                          fill=col)
    # red warning triangle
    cx, cy = x + w - 52, y + 30
    d.polygon([(cx, cy - 18), (cx + 20, cy + 14), (cx - 20, cy + 14)],
              fill=(220, 40, 40), outline=(255, 220, 60), width=2)
    d.text((cx - 3, cy - 8), "!", font=font(SANS_B, 18), fill=WHITE)
    # small padlock
    px, py = x + w - 62, y + h - 44
    d.rectangle([px, py, px + 26, py + 20], fill=(255, 210, 60),
                outline=(120, 80, 0))
    d.arc([px + 5, py - 12, px + 21, py + 4], 180, 360,
          fill=(255, 210, 60), width=4)
    d.ellipse([px + 10, py + 6, px + 16, py + 12], fill=(120, 40, 0))
    d.rectangle([px + 12, py + 11, px + 14, py + 16], fill=(120, 40, 0))
    d.text((x + 12, y + h - 26), "ACCESS DENIED", font=font(SANS_B, 11),
           fill=(255, 120, 120))


def scene_iran(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 16, 40))
    for sx, sy in [(30, 14), (90, 26), (160, 10), (230, 22), (290, 12)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    d.ellipse([x + w - 46, y + 10, x + w - 16, y + 40], fill=(240, 230, 190))
    # desert ground
    d.polygon([(x, y + h - 34), (x + w // 3, y + h - 52), (x + 2 * w // 3, y + h - 30),
               (x + w, y + h - 44), (x + w, y + h), (x, y + h)], fill=(120, 84, 48))
    # two radar dishes
    for rx in (x + 34, x + 210):
        d.line([rx, y + h - 34, rx, y + h - 78], fill=(200, 200, 200), width=4)
        d.pieslice([rx - 26, y + h - 104, rx + 26, y + h - 52], 200, 340,
                   fill=(220, 220, 220), outline=(150, 150, 150))
    # missile trails arcing down
    for mx, my, ex in [(x + 70, y + 8, x + 60), (x + 170, y + 4, x + 190),
                       (x + 250, y + 12, x + 260)]:
        d.arc([mx - 40, my, mx + 60, my + 90], 200, 330, fill=(255, 170, 60),
              width=3)
        d.ellipse([ex - 4, my + 74, ex + 4, my + 82], fill=(255, 220, 80))
    # explosion blooms on the dishes
    for ex, ey in [(x + 60, y + h - 80), (x + 236, y + h - 80)]:
        for r, col in [(16, (255, 120, 20)), (9, (255, 200, 60)),
                       (4, (255, 240, 160))]:
            d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)


def scene_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 22, 44))
    for sx, sy in [(20, 12), (70, 22), (150, 10), (220, 18), (290, 14)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=WHITE)
    # sea
    d.rectangle([x, y + h - 44, x + w, y + h], fill=(18, 52, 84))
    for wx in range(0, w, 46):
        d.arc([x + wx, y + h - 30, x + wx + 34, y + h - 16], 0, 180,
              fill=(90, 140, 180), width=2)
    # ship hull and deckhouse
    d.polygon([(x + 30, y + h - 46), (x + w - 30, y + h - 46),
               (x + w - 52, y + h - 22), (x + 52, y + h - 22)],
              fill=(60, 60, 66), outline=(150, 150, 150))
    d.rectangle([x + 120, y + h - 84, x + 210, y + h - 46],
                fill=(90, 90, 96), outline=(160, 160, 160))
    d.line([x + 165, y + h - 110, x + 165, y + h - 84], fill=(200, 200, 200),
           width=4)
    # fire on the deckhouse
    for fx in (150, 175, 196):
        for r, col in [(17, (255, 110, 20)), (10, (255, 190, 60)),
                       (5, (255, 240, 150))]:
            d.ellipse([x + fx - r, y + h - 96 - r, x + fx + r, y + h - 96 + r],
                      fill=col)
    # smoke (kept inside the panel: centres low, small radii)
    for sx, sy, sr in [(150, y + h - 96, 10), (170, y + h - 104, 11),
                       (192, y + h - 94, 9), (205, y + h - 100, 10)]:
        d.ellipse([x + sx - sr, sy - sr, x + sx + sr, sy + sr],
                  fill=(70, 70, 78))
    # lifeboat
    d.polygon([(x + 250, y + h - 18), (x + 292, y + h - 18),
               (x + 284, y + h - 8), (x + 258, y + h - 8)], fill=(255, 150, 40))
    d.text((x + 256, y + h - 34), "16 CREW", font=font(SANS_B, 9), fill=(255, 200, 120))


# ---- secondary icons ---------------------------------------------------
def icon_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 80, 96))
    d.ellipse([x + w - 46, y + 6, x + w - 8, y + 44], fill=(255, 210, 90))
    d.ellipse([x + w - 40, y + 12, x + w - 14, y + 38], fill=(24, 80, 96))
    d.rectangle([x + 14, y + h - 26, x + w - 14, y + h - 14], fill=(150, 100, 50))
    for px in (30, 80, 130):
        d.ellipse([x + px, y + h - 44, x + px + 14, y + h - 26],
                  fill=(240, 220, 190))


def icon_isidro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 110, 60))
    d.polygon([(x, y + h), (x + w // 2, y + 18), (x + w, y + h)], fill=(190, 150, 80))
    d.rectangle([x + 18, y + h - 34, x + w - 18, y + h - 12], fill=(30, 30, 34))
    d.rectangle([x + 30, y + h - 48, x + w - 30, y + h - 34], fill=(50, 90, 160))
    d.ellipse([x + 44, y + h - 10, x + 62, y + h + 8], fill=BLACK)
    d.ellipse([x + w - 62, y + h - 10, x + w - 44, y + h + 8], fill=BLACK)
    d.text((x + w // 2 - 14, y + h - 30), "POLICE", font=font(SANS_B, 8),
           fill=WHITE)
    for cx in (x + 150, x + 168):
        d.ellipse([cx - 8, y + 8, cx + 8, y + 24], outline=(255, 220, 120),
                  width=3)


def icon_krasnodar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 44, 66))
    d.rectangle([x + 30, y + 18, x + w - 30, y + h - 10], fill=(90, 92, 110))
    for wy in range(24, h - 14, 14):
        for wx in range(40, w - 40, 20):
            d.rectangle([x + wx, y + wy, x + wx + 10, y + wy + 8],
                        fill=(255, 220, 100))
    d.ellipse([x + w // 2 - 12, y + 2, x + w // 2 + 12, y + 26],
              fill=(255, 140, 30))
    for dx in (-46, 46):
        d.line([x + w // 2 + dx, y + 14, x + w // 2, y + 14], fill=GREY, width=2)
        d.rectangle([x + w // 2 + dx - 8, y + 10, x + w // 2 + dx + 8, y + 18],
                    fill=(200, 200, 200))


def icon_zaporizhzhia(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 40, 70))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(20, 60, 100))
    for bx in range(10, w - 10, 34):
        d.line([x + bx, y + h - 22, x + bx + 14, y + h - 40], fill=(180, 180, 180),
               width=3)
        d.line([x + bx + 14, y + h - 40, x + bx + 28, y + h - 22],
               fill=(180, 180, 180), width=3)
    d.polygon([(x + 60, y + 8), (x + 110, y + 8), (x + 130, y + 18),
               (x + 60, y + 18)], fill=(220, 220, 220))
    d.ellipse([x + 130, y + 12, x + 138, y + 20], fill=(255, 150, 40))
    for ex, ey in [(x + 40, y + h - 34), (x + 150, y + h - 30)]:
        d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=(255, 120, 30))


def icon_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 150, 110))
    d.rectangle([x + 20, y + h - 40, x + 130, y + h - 16], fill=(60, 70, 50))
    d.rectangle([x + 40, y + h - 58, x + 110, y + h - 40], fill=(80, 90, 66))
    d.line([x + 110, y + h - 52, x + 150, y + h - 58], fill=(40, 44, 36), width=5)
    for rx, ry in [(150, h - 18), (168, h - 26), (140, h - 30)]:
        d.polygon([(x + rx, y + ry), (x + rx + 12, y + ry - 10),
                   (x + rx + 22, y + ry)], fill=(120, 110, 96))
    d.text((x + 8, y + 6), "129", font=font(SANS_B, 20), fill=(120, 20, 20))


def icon_myanmar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 210))
    d.line([x + 10, y + h // 2, x + 40, y + h // 2 - 16, x + 60, y + h // 2 + 14,
            x + 85, y + h // 2 - 20, x + 105, y + h // 2 + 8, x + 130, y + h // 2 - 6,
            x + 160, y + h // 2 + 12, x + w - 10, y + h // 2],
           fill=RED, width=3)
    d.polygon([(x, y + h), (x + 60, y + h - 16), (x + 120, y + h - 6),
               (x + w, y + h - 18), (x + w, y + h)], fill=(140, 110, 70))
    d.text((x + 10, y + 8), "M 4.1", font=font(SANS_B, 18), fill=INK)


def icon_hongkong(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 90, 140))
    d.rectangle([x + 60, y + 26, x + 130, y + h - 8], fill=(200, 40, 40))
    d.rectangle([x + 70, y + 14, x + 120, y + 26], fill=WHITE)
    d.line([x + 95, y + 14, x + 95, y + 4], fill=WHITE, width=3)
    for px in (16, 34, 52, 140, 158, 176):
        d.ellipse([x + px, y + h - 22, x + px + 10, y + h - 12], fill=(240, 220, 180))
    d.line([x + 95, y + 14, x + 95, y + 4], fill=WHITE, width=3)
    d.polygon([(x + 95, y + 4), (x + 112, y + 8), (x + 95, y + 12)],
              fill=(255, 210, 90))


def icon_manipur(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    d.rectangle([x + 76, y + 10, x + 116, y + h - 10], fill=(40, 120, 60))
    d.rectangle([x + 86, y + 2, x + 106, y + 10], fill=(40, 120, 60))
    d.ellipse([x + 86, y + 22, x + 106, y + 42], fill=WHITE)
    d.ellipse([x + 90, y + 26, x + 96, y + 32], fill=BLACK)
    d.ellipse([x + 100, y + 26, x + 106, y + 32], fill=BLACK)
    d.line([x + 92, y + 36, x + 104, y + 44], fill=BLACK, width=2)
    d.line([x + 104, y + 36, x + 92, y + 44], fill=BLACK, width=2)
    d.text((x + 8, y + 6), "16", font=font(SANS_B, 20), fill=RED)
    d.text((x + 128, y + h - 20), "600 IN HOSPITAL", font=font(SANS_B, 8),
           fill=INK)


def icon_dnipro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(50, 40, 60))
    for tx in range(0, w, 26):
        d.line([x + tx, y + h - 12, x + tx + 18, y + h - 12], fill=(200, 180, 120),
               width=3)
    d.rectangle([x + 40, y + h - 34, x + 90, y + h - 18], fill=(120, 60, 40))
    d.rectangle([x + 100, y + h - 30, x + 140, y + h - 18], fill=(90, 50, 30))
    for ex, ey in [(x + 60, y + h - 40), (x + 120, y + h - 36), (x + 160, y + h - 42)]:
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 140, 30))
    d.polygon([(x + 150, y + 10), (x + 180, y + 10), (x + 172, y + 20),
               (x + 158, y + 20)], fill=(220, 220, 220))


def icon_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 70, 100))
    for i in range(6):
        d.ellipse([x + 14 + i * 30, y + 14, x + 22 + i * 30, y + 22],
                  fill=(255, 220, 120))
    d.polygon([(x + 20, y + h - 30), (x + w - 20, y + h - 30),
               (x + w - 40, y + h - 14), (x + 40, y + h - 14)],
              fill=(120, 40, 40))
    d.rectangle([x + 70, y + h - 52, x + 120, y + h - 30], fill=(160, 60, 50))
    d.text((x + 8, y + h - 26), "2 DAYS", font=font(SANS_B, 12), fill=WHITE)


ICONS = {
    "cop": icon_cop, "isidro": icon_isidro, "krasnodar": icon_krasnodar,
    "zaporizhzhia": icon_zaporizhzhia, "gaza": icon_gaza,
    "myanmar": icon_myanmar, "hongkong": icon_hongkong,
    "manipur": icon_manipur, "dnipro": icon_dnipro, "hormuz": icon_hormuz,
}

HERO_SCENES = {"fbi": scene_fbi, "iran": scene_iran, "sparta": scene_sparta}

# ---- map -----------------------------------------------------------------
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
           (-75, 72), (-60, 62), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
           (-80, 25), (-85, 20), (-90, 15), (-95, 18), (-100, 20), (-105, 22),
           (-115, 30), (-125, 40), (-125, 50), (-140, 60), (-160, 58)],
    "SA": [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10),
           (-35, -15), (-40, -25), (-48, -28), (-55, -35), (-65, -45),
           (-70, -55), (-73, -50), (-73, -40), (-72, -30), (-70, -20),
           (-75, -15), (-80, -5)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31),
           (35, 28), (43, 12), (51, 10), (48, 0), (40, -10), (35, -20),
           (32, -28), (20, -35), (15, -30), (12, -18), (9, -5), (9, 4),
           (-8, 5), (-13, 8)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
           (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (28, 66),
           (25, 70), (18, 69), (12, 65), (5, 60), (0, 55), (-5, 50),
           (-10, 43)],
    "AS": [(30, 62), (40, 68), (55, 70), (70, 72), (90, 75), (110, 76),
           (130, 72), (150, 70), (170, 67), (178, 65), (170, 60), (160, 55),
           (158, 50), (142, 45), (140, 40), (130, 35), (127, 35), (122, 30),
           (120, 25), (110, 20), (108, 10), (105, 5), (100, 8), (95, 15),
           (90, 22), (85, 20), (80, 15), (75, 10), (72, 20), (66, 25),
           (60, 25), (55, 26), (50, 29), (48, 30), (43, 28), (40, 32),
           (35, 36), (30, 36), (28, 40), (30, 45), (28, 50), (30, 55)],
    "OC": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
           (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
           (153, -32), (153, -27), (150, -22), (146, -19), (142, -15),
           (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
           (126, -14), (122, -17), (118, -20)],
    "UK": [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (-1, 51)],
    "JP": [(130, 31), (133, 34), (137, 35), (140, 38), (141, 42), (143, 44),
           (141, 41), (139, 37), (135, 34), (131, 33)],
}

# story number -> (lon, lat, dx, dy) pin offset in px
PINS = {
    1: (-77, 39, -6, -12), 2: (50.5, 26.2, 10, -12), 3: (27, 60, -4, -14),
    4: (30.7, 36.9, 12, 12), 5: (-107, 25, -10, 12), 6: (39, 45, 14, 14),
    7: (35.2, 47.8, 16, -12), 8: (34.5, 31.5, -16, 10), 9: (96, 21, 10, -10),
    10: (114.2, 22.3, 10, 10), 11: (94, 24.5, -14, -10), 12: (35, 48.5, -18, 12),
    13: (56.5, 26.5, 12, 12),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # graticule
    for gx in range(0, w + 1, 128):
        d.line([x + gx, y, x + gx, y + h], fill=(170, 200, 214), width=1)
    for gy in range(0, h + 1, 42):
        d.line([x, y + gy, x + w, y + gy], fill=(170, 200, 214), width=1)

    def px(lon, lat):
        return x + (lon + 180.0) / 360.0 * w, y + (75.0 - lat) / 130.0 * h

    for poly in CONTINENTS.values():
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # dashed equator for orientation
    ex0, ey0 = px(-180, 0)
    ex1, _ = px(180, 0)
    for gx in range(int(ex0), int(ex1), 10):
        d.line([gx, ey0, gx + 5, ey0], fill=(150, 170, 180), width=1)
    # continent labels
    lab = font(SANS_B, 10)
    for text, lon, lat in [("NORTH AMERICA", -100, 52), ("SOUTH AMERICA", -60, -14),
                           ("EUROPE", 12, 56), ("AFRICA", 16, 4),
                           ("ASIA", 92, 56), ("AUSTRALIA", 134, -26)]:
        lx, ly = px(lon, lat)
        d.text((lx - d.textlength(text, font=lab) / 2, ly - 6), text,
               font=lab, fill=(120, 104, 70))
    # numbered pins
    pin_f = font(SANS_B, 10)
    for num, (lon, lat, dx, dy) in PINS.items():
        tx, ty = px(lon, lat)
        cx, cy = tx + dx, ty + dy
        if (cx, cy) != (tx, ty):
            d.line([tx, ty, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=WHITE, width=2)
        t = str(num)
        tw = d.textlength(t, font=pin_f)
        d.text((cx - tw / 2, cy - 7), t, font=pin_f, fill=WHITE)


# ---- page ----------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # masthead bar
    d.rectangle([0, 0, W, 26], fill=BLACK)
    d.text((10, 5), "THE WORLD TODAY", font=font(SERIF_B, 15), fill=WHITE)
    right = "32 STORIES  •  6 REGIONS  •  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    rf = font(SANS_B, 10)
    d.text((W - 10 - d.textlength(right, font=rf), 6), right, font=rf,
           fill=(230, 200, 120))
    y = 26

    # giant red date line
    df = font(SERIF_B, 44)
    date = "SUNDAY, 22 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=df)) / 2, y + 4), date, font=df,
           fill=RED)
    y += 56

    # sub-headline: the three hero headlines in one line
    sf = font(SANS, 12)
    sub = ("FBI probes crime-database hack  •  Iran says it hit two US radars  •  "
           "Russian ship burns in the Baltic")
    d.text(((W - d.textlength(sub, font=sf)) / 2, y + 2), sub, font=sf, fill=INK)
    y += 22
    d.line([10, y, W - 10, y], fill=INK, width=2)
    y += 6

    # 6-number strip
    cell = W // 6
    nf = font(SERIF_B, 30)
    lf = font(SANS, 10)
    for i, (num, label) in enumerate(NUMBERS):
        cx = i * cell
        if i:
            d.line([cx, y + 4, cx, y + 52], fill=LGREY, width=1)
        nw = d.textlength(num, font=nf)
        d.text((cx + (cell - nw) / 2, y + 2), num, font=nf, fill=RED)
        ly = y + 36
        for ln in wrap(d, label, lf, cell - 16):
            tw = d.textlength(ln, font=lf)
            d.text((cx + (cell - tw) / 2, ly), ln, font=lf, fill=INK)
            ly += 12
    y += 58
    d.line([10, y, W - 10, y], fill=INK, width=1)
    y += 4

    # coloured region bar with true counts
    total = sum(c for _, c, _ in REGIONS)
    rx = 0
    rbf = font(SANS_B, 10)
    for name, count, col in REGIONS:
        seg = int(round(count / total * W))
        d.rectangle([rx, y, rx + seg - 1, y + 20], fill=col)
        label = "%s %d" % (name, count)
        tw = d.textlength(label, font=rbf)
        if tw < seg - 8:
            d.text((rx + (seg - tw) / 2, y + 4), label, font=rbf, fill=WHITE)
        rx += seg
    y += 26

    # heroes: 3 columns
    hw, gap = 328, 10
    hx = 10
    hero_y, hero_h = y, 198
    for hero in HEROES:
        d.rectangle([hx, hero_y, hx + hw, hero_y + hero_h], fill=WHITE,
                    outline=LGREY, width=1)
        pic_h = 118
        HERO_SCENES[hero["scene"]](d, hx + 1, hero_y + 1, hw - 2, pic_h)
        chip(d, hx + 8, hero_y + 8, hero["tag"])
        num = str(hero["num"])
        d.ellipse([hx + hw - 30, hero_y + 8, hx + hw - 8, hero_y + 30],
                  fill=RED, outline=WHITE, width=2)
        d.text((hx + hw - 22, hero_y + 12), num, font=font(SANS_B, 12),
               fill=WHITE)
        ty = hero_y + pic_h + 8
        ty = draw_wrapped(d, hx + 8, ty, hero["head"], font(SERIF_B, 14),
                          hw - 16, INK, spacing=1, max_lines=2)
        ty = draw_wrapped(d, hx + 8, ty + 2, hero["summ"], font(SANS, 10),
                          hw - 16, (60, 60, 60), spacing=1, max_lines=2)
        cap_h = 18
        d.rectangle([hx + 1, hero_y + hero_h - cap_h - 1, hx + hw - 1,
                     hero_y + hero_h - 1], fill=(40, 40, 40))
        d.text((hx + 8, hero_y + hero_h - cap_h + 3), hero["cap"],
               font=font(SANS, 9), fill=(220, 220, 220))
        hx += hw + gap
    y = hero_y + hero_h + 6

    # secondaries: 5 columns x 2 rows, illustrated
    cols, rows = 5, 2
    sw = (W - 20 - (cols - 1) * 8) // cols
    sh = 100
    sx0, sy0 = 10, y
    for i, sec in enumerate(SECONDARIES):
        r, c = divmod(i, cols)
        sx = sx0 + c * (sw + 8)
        sy = sy0 + r * (sh + 8)
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=WHITE, outline=LGREY,
                    width=1)
        pic_h = 56
        ICONS[sec["scene"]](d, sx + 1, sy + 1, sw - 2, pic_h)
        chip(d, sx + 5, sy + 5, str(sec["num"]), size=9)
        d.text((sx + 5, sy + pic_h + 5), sec["tag"], font=font(SANS_B, 9),
               fill=RED)
        draw_wrapped(d, sx + 5, sy + pic_h + 19, sec["summ"], font(SANS, 9),
                     sw - 10, INK, spacing=1, max_lines=3)
    y = sy0 + rows * sh + (rows - 1) * 8 + 6

    # map band
    map_y, map_h = y, 158
    d.text((10, map_y), "WHERE IT HAPPENED — PINS MATCH STORY NUMBERS 1–13",
           font=font(SANS_B, 11), fill=INK)
    map_y += 16
    draw_map(d, 10, map_y, W - 20, map_h - 16)
    y = map_y + map_h - 16 + 6

    # ALSO ON list: 19 more stories, two columns
    d.text((10, y), "ALSO ON SUNDAY 22 NOVEMBER — 19 MORE STORIES",
           font=font(SANS_B, 12), fill=RED)
    y += 16
    af = font(SANS, 10)
    nbf = font(SANS_B, 10)
    col_w = (W - 20) // 2
    for i, (num, region, text, outlet) in enumerate(ALSO):
        col = 0 if i < 10 else 1
        row = i if i < 10 else i - 10
        ax = 10 + col * col_w
        ay = y + row * 12
        d.text((ax, ay), "%d" % num, font=nbf, fill=RED)
        line = "%s  (%s)" % (text, outlet)
        # shrink the line to fit the column
        f = af
        while d.textlength(line, font=f) > col_w - 30 and f.size > 8:
            f = font(SANS, f.size - 1)
        d.text((ax + 24, ay), line, font=f, fill=INK)
    y += 10 * 12 + 6

    # DATE CHECK box, written as proof
    box_y = y
    d.rectangle([10, box_y, W - 10, box_y + 56], outline=RED, width=2,
                fill=(255, 244, 244))
    d.text((18, box_y + 5), "DATE CHECK", font=font(SANS_B, 11), fill=RED)
    draw_wrapped(d, 18, box_y + 21, DATE_CHECK, font(SANS, 10), W - 36,
                 INK, spacing=2, max_lines=3)
    y = box_y + 56 + 6

    # sources footer
    ff = font(SANS, 9)
    foot = ("Sources: Reuters  •  AP  •  BBC  •  CNN  •  ANI  •  Xinhua  •  "
            "Al Jazeera  •  China Daily  •  info.gov.hk  •  Yle  •  Kyiv "
            "Independent  •  C54 News.   Every story names its outlet.   "
            "Pictures and map: original, drawn in code.")
    draw_wrapped(d, 10, y, foot, ff, W - 20, GREY, spacing=2, max_lines=2)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
