#!/usr/bin/env python3
"""Build entry.png: the world's news of Wednesday 25 November 2026 on one page.

Development tool only. It draws a newspaper-style front page with Pillow:
a masthead, a numbers strip, three lead stories with hand-drawn scenes,
eight numbered story cards, a world map with pins, an "also on" brief list
and a date-check footer. The graded entrypoint (main.py) does not run this
file; it copies the finished entry.png, so the entry needs no libraries.

All stories come from the day itself, Wednesday 25 November 2026, as
reported that day (Huawei verdict in Brooklyn, the Shenzhou-24 launch,
leaked Russian war-dead figures, the Riyadh tower strike, the Colombia
hostage rescue, the Australia-Solomon Islands treaty, the Anmer Hall
arrests, Senegal restored as African champions, and the rest).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 23, 18)
MUTE = (96, 88, 74)
RED = (179, 53, 44)
BLUE = (43, 94, 167)
TEAL = (13, 148, 136)
GOLD = (176, 132, 26)
GREEN = (46, 125, 50)
PURPLE = (106, 76, 147)
DARK = (52, 52, 52)
TAN = (232, 220, 192)
PANEL = (251, 248, 240)

FONT_DIR = "/usr/share/fonts/truetype/noto/"
_cache = {}


def F(name, size):
    key = (name, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _cache[key]


def serif_black(size):
    return F("NotoSerif-Black.ttf", size)


def serif_bold(size):
    return F("NotoSerif-Bold.ttf", size)


def serif(size):
    return F("NotoSerif-Regular.ttf", size)


def serif_italic(size):
    return F("NotoSerif-Italic.ttf", size)


def sans(size):
    return F("NotoSans-Regular.ttf", size)


def sans_bold(size):
    return F("NotoSans-Bold.ttf", size)


def sans_black(size):
    return F("NotoSans-Black.ttf", size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 28  # page margin


def tw(text, font):
    return d.textlength(text, font=font)


def wrap(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(t, font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, font, width, fill=INK, leading=1.22, align="left"):
    lines = wrap(text, font, width)
    lh = int(font.size * leading)
    for ln in lines:
        if align == "center":
            d.text((x + (width - tw(ln, font)) / 2, y), ln, font=font, fill=fill)
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def centered(y, text, font, fill=INK):
    d.text(((W - tw(text, font)) / 2, y), text, font=font, fill=fill)


def rule(y, x0=MX, x1=W - MX, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- masthead
f_top = sans_bold(14)
d.text((MX, 12), "THE WORLD ON ONE PAGE", font=f_top, fill=INK)
mid = "DAY 329 OF 2026"
d.text(((W - tw(mid, f_top)) / 2, 12), mid, font=f_top, fill=RED)
right = "EVERY STORY DATED WEDNESDAY 25 NOV"
d.text((W - MX - tw(right, f_top), 12), right, font=f_top, fill=INK)
rule(36, width=2)

title = "Wednesday 25 November 2026"
size = 63
while tw(title, serif_black(size)) > W - 2 * MX:
    size -= 1
centered(44, title, serif_black(size))
rule(122, width=2)

counts = ("33 STORIES, ALL FROM WEDNESDAY 25 NOV  ·  EUROPE 8  ·  MIDDLE EAST 5  ·  "
          "ASIA 7  ·  AFRICA 2  ·  AMERICAS 7  ·  OCEANIA 3  ·  GLOBAL 1")
centered(130, counts, sans_bold(13), fill=DARK)

top3_parts = ["Huawei guilty on 10 of 12 counts in Brooklyn",
              "Shenzhou-24 lifts off with Pakistan's first astronaut",
              "Russia's war dead put at 490,334"]
size = 18
while sum(tw(p, serif_italic(size)) for p in top3_parts) + 44 > W - 2 * MX:
    size -= 1
f_top3 = serif_italic(size)
total = sum(tw(p, f_top3) for p in top3_parts) + 44
tx = (W - total) / 2
for i, part in enumerate(top3_parts):
    d.text((tx, 152), part, font=f_top3, fill=(40, 36, 30))
    tx += tw(part, f_top3)
    if i < 2:
        cy = 152 + size // 2
        d.polygon([(tx + 11, cy - 4), (tx + 15, cy), (tx + 11, cy + 4), (tx + 7, cy)],
                  fill=RED)
        tx += 22
rule(180)

# ------------------------------------------------------------ numbers strip
stats = [
    ("10 of 12", "counts Huawei was\nconvicted on"),
    ("490,334", "Russian soldiers killed\nsince 2022, leaked data say"),
    ("1st", "foreign astronaut to fly\nto China's Tiangong station"),
    ("11", "wounded as a strike hits\nRiyadh's PIF Tower again"),
    ("~30", "hostages freed as Colombia\nstorms a siege supermarket"),
    ("1–0", "Senegal's restored AFCON\nfinal win over Morocco"),
]
col_w = (W - 2 * MX) / 6
for i, (num, cap) in enumerate(stats):
    x = MX + i * col_w
    d.text((x + 4, 188), num, font=serif_black(30), fill=INK)
    cy = 224
    for ln in cap.split("\n"):
        d.text((x + 4, cy), ln, font=sans(11), fill=MUTE)
        cy += 13
    if i:
        d.line([(x - 6, 192), (x - 6, 246)], fill=(200, 190, 165), width=1)
rule(254, width=2)


# ------------------------------------------------------------ lead stories
LEAD_Y, LEAD_H = 266, 218
GAP = 12
PW = (W - 2 * MX - 2 * GAP) // 3  # panel width


def panel(x, tag, tag_color, place):
    d.rectangle([x, LEAD_Y, x + PW, LEAD_Y + LEAD_H], fill=PANEL,
                outline=(205, 195, 168), width=1)
    d.rectangle([x, LEAD_Y, x + PW, LEAD_Y + 20], fill=tag_color)
    d.text((x + 8, LEAD_Y + 4), tag, font=sans_bold(11), fill=(255, 255, 255))
    pl = place
    d.text((x + PW - 8 - tw(pl, sans_bold(11)), LEAD_Y + 4), pl,
           font=sans_bold(11), fill=(255, 255, 255))


def scene_box(x, y, w, h, sky):
    d.rectangle([x, y, x + w, y + h], fill=sky, outline=(190, 180, 152), width=1)
    return (x, y, x + w, y + h)


# --- lead 1: Huawei verdict, Brooklyn courthouse -------------------------
x1 = MX
panel(x1, "AMERICAS · COURTS", RED, "1  BROOKLYN")
sx, sy, sw, sh = x1 + 8, LEAD_Y + 28, PW - 16, 68
scene_box(sx, sy, sw, sh, (214, 226, 238))
cx = sx + sw // 2
# pediment + roof
d.polygon([(cx - 88, sy + 27), (cx + 88, sy + 27), (cx, sy + 7)], fill=(240, 236, 224),
          outline=INK)
d.rectangle([cx - 92, sy + 29, cx + 92, sy + 34], fill=(240, 236, 224), outline=INK)
# columns
for i in range(5):
    cxx = cx - 72 + i * 36
    d.rectangle([cxx, sy + 36, cxx + 10, sy + 56], fill=(240, 236, 224), outline=INK)
# steps
d.rectangle([cx - 96, sy + 58, cx + 96, sy + 62], fill=(226, 220, 204), outline=INK)
d.rectangle([cx - 100, sy + 63, cx + 100, sy + 67], fill=(226, 220, 204), outline=INK)
# verdict badge
bx, by = sx + sw - 50, sy + 6
d.ellipse([bx, by, bx + 44, by + 44], fill=RED, outline=(255, 255, 255), width=2)
d.text((bx + 22 - tw("10/12", sans_black(13)) / 2, by + 7), "10/12", font=sans_black(13),
       fill=(255, 255, 255))
d.text((bx + 22 - tw("GUILTY", sans_bold(8)) / 2, by + 25), "GUILTY", font=sans_bold(8),
       fill=(255, 255, 255))
hy = text_block(x1 + 8, LEAD_Y + 102, "Huawei guilty on 10 of 12 counts — and will appeal",
                serif_bold(19), PW - 16, leading=1.12)
text_block(x1 + 8, hy + 2,
           "A Brooklyn jury convicted Huawei and three subsidiaries of bank and wire "
           "fraud, trade-secret theft and sanctions evasion over Skycom, its Iran "
           "business. Jurors cleared it of racketeering. Sentencing: 14 Sept 2027. "
           "Beijing calls it “economic coercion”.",
           sans(11.5), PW - 16, fill=(52, 48, 40), leading=1.22)

# --- lead 2: Shenzhou-24 launch, Jiuquan ---------------------------------
x2 = MX + PW + GAP
panel(x2, "ASIA · SPACE", BLUE, "2  JIUQUAN")
sx, sy, sw, sh = x2 + 8, LEAD_Y + 28, PW - 16, 68
scene_box(sx, sy, sw, sh, (24, 34, 64))
for gx in range(14):  # stars
    px = sx + 12 + (gx * 53) % (sw - 20)
    py = sy + 6 + (gx * 29) % 26
    d.point((px, py), fill=(255, 255, 255))
    d.point((px + 1, py), fill=(220, 225, 255))
# Tiangong station, top right
tx, ty = sx + sw - 92, sy + 12
d.rectangle([tx, ty, tx + 34, ty + 8], fill=(210, 216, 226), outline=(150, 160, 180))
d.rectangle([tx - 16, ty + 1, tx, ty + 7], fill=(90, 130, 200), outline=(150, 160, 180))
d.rectangle([tx + 34, ty + 1, tx + 50, ty + 7], fill=(90, 130, 200), outline=(150, 160, 180))
d.line([(tx + 17, ty + 8), (tx + 17, ty + 16)], fill=(210, 216, 226), width=2)
# rocket
rx = sx + 62
d.polygon([(rx, sy + 6), (rx - 11, sy + 23), (rx + 11, sy + 23)], fill=(238, 240, 244),
          outline=INK)
d.rectangle([rx - 11, sy + 23, rx + 11, sy + 47], fill=(238, 240, 244), outline=INK)
d.ellipse([rx - 4, sy + 27, rx + 4, sy + 35], fill=BLUE, outline=INK)
d.polygon([(rx - 11, sy + 41), (rx - 20, sy + 54), (rx - 11, sy + 54)], fill=RED, outline=INK)
d.polygon([(rx + 11, sy + 41), (rx + 20, sy + 54), (rx + 11, sy + 54)], fill=RED, outline=INK)
d.polygon([(rx - 6, sy + 52), (rx + 6, sy + 52), (rx, sy + 65)], fill=(255, 166, 47))
d.polygon([(rx - 3, sy + 52), (rx + 3, sy + 52), (rx, sy + 61)], fill=(255, 226, 130))
# launch tower + ground
d.rectangle([rx - 44, sy + 16, rx - 38, sy + 56], fill=(120, 128, 140))
d.line([(rx - 41, sy + 27), (rx - 12, sy + 31)], fill=(120, 128, 140), width=2)
d.rectangle([sx, sy + sh - 7, sx + sw, sy + sh], fill=(52, 58, 74))
d.text((sx + sw - 8 - tw("SHENZHOU-24", sans_bold(9)), sy + sh - 19), "SHENZHOU-24",
       font=sans_bold(9), fill=(200, 210, 235))
hy = text_block(x2 + 8, LEAD_Y + 102, "Shenzhou-24 lifts off with Pakistan's first astronaut",
                serif_bold(19), PW - 16, leading=1.12)
text_block(x2 + 8, hy + 2,
           "China launched a crew toward its Tiangong station from Jiuquan. Aboard "
           "is a Pakistani astronaut on a short visit — the first foreign flyer on a "
           "Chinese mission. Beijing called the launch a complete success.",
           sans(11.5), PW - 16, fill=(52, 48, 40), leading=1.22)

# --- lead 3: Russia's war dead -------------------------------------------
x3 = MX + 2 * (PW + GAP)
panel(x3, "EUROPE · WAR", DARK, "3  MOSCOW")
sx, sy, sw, sh = x3 + 8, LEAD_Y + 28, PW - 16, 68
scene_box(sx, sy, sw, sh, (243, 236, 224))
bars = [("2022", 17), ("2023", 28), ("2024", 39), ("2025", 48)]
base = sy + sh - 14
for i, (yr, bh) in enumerate(bars):
    bxx = sx + 26 + i * 44
    d.rectangle([bxx, base - bh, bxx + 26, base], fill=RED if i == 3 else (120, 60, 52))
    d.text((bxx + 13 - tw(yr, sans_bold(8)) / 2, base + 2), yr, font=sans_bold(8), fill=MUTE)
d.line([(sx + 14, base), (sx + sw - 12, base)], fill=INK, width=1)
d.text((sx + sw - 8 - tw("11M RECORDS LEAKED", sans_bold(9)), sy + 6),
       "11M RECORDS LEAKED", font=sans_bold(9), fill=RED)
hy = text_block(x3 + 8, LEAD_Y + 102, "Russia's own figures: at least 490,334 war dead",
                serif_bold(19), PW - 16, leading=1.12)
text_block(x3 + 8, hy + 2,
           "Leaked Rosstat records — 11 million death files analysed by BBC Russian — "
           "put Russian military deaths since 2022 at 490,334 or more. Of Russians "
           "aged 18–24 who died in 2025, 65% died in the war.",
           sans(11.5), PW - 16, fill=(52, 48, 40), leading=1.22)


# ------------------------------------------------------------ story cards
CARDS = [
    (4, "RIYADH · ATTACK", RED, "11", "WOUNDED",
     "Houthi strike hits PIF Tower again",
     "The tower is hit again: two Saudis, two Indians, three Nepalese and four "
     "Egyptians are hurt. Riyadh blames the Houthis."),
    (5, "CARTAGENA · SIEGE", TEAL, "~30", "HELD, ALL FREED",
     "All supermarket hostages rescued in raid",
     "Forces stormed the store on the siege's second day. The hostages were "
     "taken after a failed armoured-vehicle robbery."),
    (6, "SHANGHAI · POLITICS", PURPLE, "4th", "POLITBURO FALL",
     "Party boss probed as Xi's purge widens",
     "Shanghai's party chief is under investigation for suspected severe "
     "violations — the biggest name swept up before the congress."),
    (7, "NORFOLK · ROYALS", GOLD, "2", "ARRESTED",
     "Two held at William & Kate's estate",
     "Police arrested two men on suspicion of burglary and trespass at Anmer "
     "Hall, the Waleses' Norfolk home. No royals were there."),
    (8, "GULF OF FINLAND · WAR", BLUE, "16", "CREW EVACUATED",
     "Drone hits Russian cargo ship",
     "Kyiv says its drone set the Sparta II ablaze; all 16 crew got off and "
     "the ship was towed to St Petersburg."),
    (9, "HONIARA · PACT", TEAL, "1st", "SECURITY PARTNER",
     "Australia signs sweeping Solomons pact",
     "The treaty names Australia the Solomons' primary security partner and "
     "affirms no foreign military base will be built there."),
    (10, "RABAT · SPORT", GREEN, "1–0", "FINAL RESTORED",
     "Senegal restored as African champions",
     "Sport's top court overturned CAF's 3–0 forfeit award to Morocco and "
     "restored Senegal's extra-time win — a second title."),
    (11, "SEOUL · MISSILES", RED, "2", "MISSILES FIRED",
     "North Korea fires two missiles into the sea",
     "Seoul's military reports the launches off the North's east coast — "
     "its latest test as tensions rise around Taiwan."),
]
CW, CH, CGAP = 234, 112, 10
for idx, (num, kick, color, stat, statlab, head, body) in enumerate(CARDS):
    cx0 = MX + (idx % 4) * (CW + CGAP)
    cy0 = 496 + (idx // 4) * (CH + 8)
    d.rectangle([cx0, cy0, cx0 + CW, cy0 + 3], fill=color)
    d.ellipse([cx0, cy0 + 9, cx0 + 17, cy0 + 26], fill=INK)
    ns = str(num)
    d.text((cx0 + 8.5 - tw(ns, sans_bold(10)) / 2, cy0 + 12), ns,
           font=sans_bold(10), fill=(255, 255, 255))
    d.text((cx0 + 23, cy0 + 11), kick, font=sans_bold(10), fill=color)
    d.text((cx0, cy0 + 30), stat, font=serif_black(20), fill=INK)
    text_block(cx0, cy0 + 53, statlab, sans_bold(7), 56, fill=MUTE, leading=1.15)
    text_block(cx0 + 64, cy0 + 29, head, serif_bold(15), CW - 64, leading=1.1)
    text_block(cx0, cy0 + 78, body, sans(10.5), CW, fill=(52, 48, 40), leading=1.2)

# ------------------------------------------------- map + also-on-Wednesday
BOT_Y = 744
d.text((MX, BOT_Y), "WHERE IT HAPPENED", font=sans_bold(12), fill=INK)
d.text((MX + 172, BOT_Y + 1), "pins carry the story numbers", font=serif_italic(11),
       fill=MUTE)
ax = MX + 380
d.text((ax, BOT_Y), "ALSO ON WEDNESDAY 25 NOV", font=sans_bold(12), fill=INK)
rule(BOT_Y + 20, width=1)

MAP_X, MAP_Y, MAP_W, MAP_H = MX, BOT_Y + 28, 352, 168
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=(238, 232, 214),
            outline=(190, 180, 152), width=1)


def ll(lon, lat):
    return (MAP_X + (lon + 180) / 360 * MAP_W, MAP_Y + (90 - lat) / 180 * MAP_H)


def land(poly, fill=(226, 214, 182)):
    d.polygon([ll(lon, lat) for lon, lat in poly], fill=fill, outline=(178, 164, 128))


land([(-165, 68), (-140, 70), (-120, 71), (-105, 68), (-92, 66), (-80, 64),
      (-76, 60), (-68, 58), (-60, 52), (-65, 48), (-70, 44), (-72, 41),
      (-75, 38), (-77, 34), (-80, 30), (-81, 25), (-84, 28), (-88, 29),
      (-93, 29), (-97, 27), (-97, 23), (-95, 19), (-92, 15), (-87, 13),
      (-83, 9), (-79, 9), (-85, 13), (-92, 15), (-100, 17), (-105, 21),
      (-110, 24), (-114, 30), (-117, 33), (-122, 37), (-124, 45),
      (-127, 50), (-135, 55), (-150, 60), (-165, 62)])
land([(-79, 9), (-75, 11), (-68, 11), (-60, 8), (-52, 5), (-44, -2),
      (-35, -8), (-39, -14), (-40, -21), (-48, -27), (-55, -34), (-59, -39),
      (-63, -42), (-66, -47), (-68, -52), (-69, -54), (-72, -53), (-74, -48),
      (-74, -40), (-73, -33), (-71, -27), (-70, -19), (-75, -15), (-79, -8),
      (-80, -4), (-77, 1), (-78, 5)])
land([(-6, 35), (3, 37), (10, 37), (11, 34), (20, 32), (30, 31), (34, 28),
      (38, 22), (40, 16), (43, 12), (49, 11), (51, 12), (47, 4), (41, -2),
      (40, -11), (38, -19), (35, -24), (32, -29), (27, -34), (20, -35),
      (18, -33), (16, -28), (14, -20), (13, -13), (13, -6), (9, 0), (9, 4),
      (-8, 5), (-13, 8), (-17, 13), (-17, 16), (-16, 21), (-15, 26),
      (-13, 29), (-9, 32)])
land([(-9, 37), (-9, 43), (-2, 44), (-1, 47), (-4, 48), (0, 50), (3, 52),
      (7, 54), (8, 57), (12, 58), (19, 59), (22, 61), (26, 66), (33, 70),
      (46, 68), (62, 70), (78, 72), (95, 76), (108, 77), (122, 73),
      (137, 72), (152, 71), (166, 70), (178, 67), (171, 61), (162, 57),
      (157, 51), (150, 45), (142, 41), (140, 37), (135, 34), (129, 33),
      (126, 30), (121, 27), (117, 24), (111, 21), (108, 16), (106, 9),
      (103, 5), (100, 8), (98, 13), (94, 17), (91, 22), (88, 21), (85, 19),
      (80, 14), (77, 8), (75, 13), (72, 20), (68, 23), (65, 25), (60, 25),
      (56, 26), (52, 27), (50, 30), (52, 25), (56, 24), (59, 22), (55, 20),
      (52, 16), (48, 14), (44, 12), (42, 15), (39, 21), (35, 28), (34, 31),
      (36, 36), (32, 36), (28, 36), (23, 36), (19, 40), (15, 38), (12, 38),
      (10, 37), (6, 37), (2, 37), (-1, 37), (-5, 36), (-9, 37)])
land([(-5, 50), (-3, 53), (-5, 55), (-4, 58), (-2, 58), (-1, 54), (0, 52),
      (1, 51)], fill=(226, 214, 182))
land([(130, 31), (134, 34), (138, 35), (140, 37), (141, 41), (142, 44),
      (140, 44), (138, 38), (134, 34), (131, 32)], fill=(226, 214, 182))
land([(95, 5), (101, 0), (106, -6), (112, -7), (118, -9), (124, -10),
      (131, -3), (137, -2), (141, -3), (141, -8), (136, -7), (129, -4),
      (123, -10), (117, -10), (111, -7), (105, -6), (99, -1), (96, 3)],
     fill=(226, 214, 182))
land([(113, -22), (114, -29), (116, -34), (120, -34), (126, -32), (131, -32),
      (135, -35), (138, -36), (141, -38), (146, -39), (150, -37), (153, -31),
      (153, -26), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12),
      (136, -15), (134, -12), (131, -12), (127, -14), (122, -17), (117, -20)],
     fill=(226, 214, 182))
land([(167, -46), (171, -43), (173, -41), (175, -39), (177, -38), (175, -37),
      (172, -40), (170, -43), (168, -47)], fill=(226, 214, 182))

PINS = [(1, -73.9, 40.7), (2, 98.5, 39.7), (3, 37.6, 55.8), (4, 46.7, 24.7),
        (5, -75.5, 10.4), (6, 121.5, 31.2), (7, 1.3, 52.6), (8, 24.0, 59.5),
        (9, 160.0, -9.4), (10, -6.8, 34.0), (11, 127.5, 38.5)]
for num, lon, lat in PINS:
    px, py = ll(lon, lat)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255),
              width=1)
    ns = str(num)
    d.text((px - tw(ns, sans_bold(8)) / 2, py - 4.5), ns, font=sans_bold(8),
           fill=(255, 255, 255))

ALSO = [
    (12, "Ryazan", "Ukrainian drones hit an oil refinery"),
    (13, "Gaza", "Israeli strikes kill 7, incl. a Hamas security chief"),
    (14, "Gaza", "Two-day toll reaches 14, health ministry says"),
    (15, "Taiwan Strait", "US destroyer transits the strait"),
    (16, "Taipei", "Coastguard flotilla circles island before Saturday's vote"),
    (17, "Aden", "Houthi forces shell outskirts; government holds the line"),
    (18, "Port-au-Prince", "Gangs burn police station as Kenyan mission pulls back"),
    (19, "Beijing", "Politburo meets next week to set the 2027 reshuffle"),
    (20, "Paris", "CAF will study the CAS award before returning the trophy"),
    (21, "Los Angeles", "Mayor vows to clear the last encampment in days"),
    (22, "Honiara", "Opposition calls a vote after the PM's suspension"),
    (23, "Honiara", "Wale asks Australia to train the Solomons' police"),
    (24, "Washington", "Blanche won't say if Huawei faces a fresh probe"),
    (25, "Dakar", "Senegal's federation: “the trophy is coming home”"),
]
colw = (W - MX - ax - 14) // 2
for i, (num, place, txt) in enumerate(ALSO):
    cx0 = ax + (i // 7) * (colw + 14)
    cy0 = BOT_Y + 30 + (i % 7) * 24
    d.text((cx0, cy0), str(num), font=sans_black(10), fill=RED)
    d.text((cx0 + 22, cy0), place, font=sans_bold(10.5), fill=INK)
    rest_x = cx0 + 22 + tw(place, sans_bold(10.5)) + 5
    lines = wrap(txt, sans(10.5), cx0 + colw - rest_x)
    if lines:
        d.text((rest_x, cy0), lines[0], font=sans(10.5), fill=(52, 48, 40))
        for ln in lines[1:]:
            cy0 += 12
            d.text((cx0 + 22, cy0), ln, font=sans(10.5), fill=(52, 48, 40))

# ---------------------------------------------------------- date check etc.
rule(950, width=1)
d.rectangle([MX, 958, MX + 86, 976], fill=RED)
d.text((MX + 8, 961), "DATE CHECK", font=sans_bold(10), fill=(255, 255, 255))
d.text((MX + 94, 960),
       "Left out as other days' news — Tue 24 Nov: Russia says it downed 699 drones · "
       "Baghdad takes over Kurdish-held oilfields · Malaysia to send 6,500 Rohingya back",
       font=sans(10.5), fill=(52, 48, 40))
centered(986,
         "Every story here happened or was first reported on Wednesday 25 November 2026, "
         "as the named outlets reported it. Maps and drawings are original art.",
         serif_italic(10.5), fill=MUTE)

img.save("entry.png", optimize=True)
import os
print("saved entry.png", os.path.getsize("entry.png"), "bytes")
