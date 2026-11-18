#!/usr/bin/env python3
"""Build the news-image-20261117 round-2 front page.

One dense broadsheet page for Tuesday 17 November 2026: masthead, hero
illustration of the collapsed Kerch Bridge span, lead story, a day-in-figures
strip, three columns of verified stories (ten with illustrations), a world
map with numbered markers, a markets strip and a footer ticker.

Every headline was verified against same-day reporting (Reuters, AP,
Bloomberg, Al Jazeera, PAHO, WHO, ASEAN, SEC filings, USA Today, NBC
Sports). All pictures are illustrations generated for this page and are
captioned as such.

Run:  python3 compose.py            -> writes entry.png next to this file
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024
MARGIN = 18
PAPER = (247, 243, 233)
INK = (17, 17, 17)
GREY = (105, 100, 90)
RULE = (60, 58, 52)
RED = (163, 22, 33)
OCEAN = (216, 228, 232)
LAND = (232, 224, 200)
LAND_EDGE = (168, 158, 130)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    if not os.path.exists(path):
        path = os.path.join(FONT_DIR, "DejaVuSans.ttf")
    return ImageFont.truetype(path, size)


F_NAME = font("DejaVuSerif-Bold.ttf", 50)
F_SMALL_CAPS = font("DejaVuSans-Bold.ttf", 9)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_CAPTION = font("DejaVuSerif-Italic.ttf", 11)
F_LEAD = font("DejaVuSerif-Bold.ttf", 35)
F_SUB = font("DejaVuSerif.ttf", 13)
F_FIG_NUM = font("DejaVuSerif-Bold.ttf", 20)
F_FIG_LBL = font("DejaVuSans.ttf", 9)
F_SECTION = font("DejaVuSans-Bold.ttf", 11)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_HEAD_SM = font("DejaVuSans-Bold.ttf", 10)
F_LEGEND = font("DejaVuSans.ttf", 10)
F_LEGEND_B = font("DejaVuSans-Bold.ttf", 10)
F_MARKET = font("DejaVuSans-Bold.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 9)
F_MAP_LBL = font("DejaVuSans-Bold.ttf", 8)
F_MARK_NUM = font("DejaVuSans-Bold.ttf", 9)


# ---------------------------------------------------------------- data

LEAD_HEAD = "KERCH BRIDGE SPAN FALLS"
LEAD_SUB = (
    "Ukraine\u2019s overnight strike drops the road arch into the Kerch Strait, cutting "
    "Russia\u2019s only direct road link to Crimea \u2014 the second attack in two days, "
    "and part of the largest Ukrainian drone assault of the war."
)
HERO_CAPTION = (
    "Illustration: the Kerch Bridge road span, collapsed into the strait. Rail traffic "
    "resumed on one track; the Kremlin says the bridge will be rebuilt."
)

# (big number, label) -- six distinct stories, none repeated in the columns
FIGURES = [
    ("1,441", "drones Russia said it downed overnight \u2014 a war record"),
    ("$115.8bn", "Nvidia quarterly revenue, up 103% on a year ago"),
    ("5,400+", "US measles cases in 2026, the most since 1991"),
    ("8,000+", "hoax threats that hit European schools in a month"),
    ("150+", "outcomes as ASEAN\u2019s Manila summit closes"),
    ("66\u201352", "Knesset vote installs a new speaker in Israel"),
]

# Illustrated stories: (tag, headline, asset file)
ILLUSTRATED = {
    "kyiv": ("KYIV", "Russia strikes Kyiv\u2019s two Dnipro bridges and damages the metro",
             "thumb-kyiv.jpg"),
    "gulf": ("GULF", "US jets hit an IRGC missile site on Qeshm Island after Iran\u2019s "
             "drone attacks on Bahrain and Kuwait", "thumb-gulf.jpg"),
    "manila": ("MANILA", "Trump lands for the first Quad summit in two years and signs "
               "critical-minerals deals", "thumb-manila.jpg"),
    "cop31": ("ANTALYA", "COP31 split over fossil fuels as the EU urges stronger "
              "clean-energy pledges", "thumb-cop31.jpg"),
    "gaza": ("GAZA", "UN warns Gaza needs winter shelter funding to stop children "
             "freezing", "thumb-gaza.jpg"),
    "chip": ("AI", "OpenAI ships GPT-6.2 Astra and Sol, its flagship 20% cheaper",
             "thumb-chip.jpg"),
    "paris": ("PARIS", "France\u2019s public-sector strike draws 146,000, far below the "
              "last walkout", "thumb-paris.jpg"),
    "ebola": ("CONGO", "WHO warns Congo\u2019s Ebola response still faces major "
              "obstacles", "thumb-measles.jpg"),
    "argentina": ("C\u00d3RDOBA", "Argentina rout Costa Rica 7\u20130 as Paz, \u00c1lvarez "
                  "and Mastantuono score twice each", "thumb-argentina.jpg"),
    "lakers": ("LOS ANGELES", "Lakers edge Hornets 118\u2013114 in OT for a ninth straight "
               "win; Grimes scores 47", "thumb-lakers.jpg"),
}

# Text-only stories: (tag, headline)
TEXT_STORIES = [
    ("ADEN", "Houthis advance on Aden as Saudi Arabia names a new coalition commander"),
    ("HORMUZ", "Tanker catches fire on a mine east of Hormuz; five vessels hit in the strait"),
    ("GULF", "Third US carrier reaches the Gulf, the first trio since the Iraq War"),
    ("SHENZHEN", "Trump, Xi and Putin to meet in a trilateral summit on Thursday"),
    ("ASEAN", "Summit ends without a South China Sea code; chair passes to Singapore"),
    ("MANILA", "East Asia Summit adopts a joint pact against online scams"),
    ("SKOPJE", "N. Macedonia and Greece foil an Iran-linked assassination plot; five held"),
    ("TRADE", "China and Canada expand tariff relief as US ties stay strained"),
    ("CHIPS", "US tightens AI chip curbs on China ahead of the Xi meeting"),
    ("IPO", "Anthropic files its final S-1; IPO prices Wednesday, trades as ANT"),
    ("MARKETS", "Wall Street falls a fourth straight day; Dow drops 1.6%"),
    ("MARKETS", "Europe and UK suffer their worst day since March, down 1.8%"),
    ("FED", "Musalem signals several US rate rises before spring 2027"),
    ("DOLLAR", "Dollar hits a fresh 19-month high as stocks slide"),
    ("AVIATION", "US seeks $50.1bn to rebuild air-traffic control after ground stop"),
    ("OUTAGES", "NSA internal network down as outages hit Apple and United"),
    ("WASHINGTON", "Biden releases memoir on his presidency and 2024 exit"),
    ("SENATE", "Van Hollen challenges Schumer for Senate Democratic leader"),
    ("FRAUD", "DOJ charges 15 in a VA benefits fraud crackdown"),
    ("SOCCER", "USMNT beat Haiti 2\u20130 in Pochettino\u2019s farewell; he joins Man Utd"),
    ("PERU", "Tumbes River tops red alert and floods farmland"),
    ("BRAZIL", "Senate delays vote on Lula\u2019s fiscal repair bill"),
    ("NAVY", "Navy nominee: Iran war is \u2018a strain\u2019; expired munitions used"),
    ("NUCLEAR", "Grid attacks risk a Chernobyl-level accident, regulators warn"),
    ("COURTS", "Trump appeals to erase his hush-money conviction"),
    ("FED", "Fed\u2019s Cook calls Trump panel a \u2018fa\u00e7ade\u2019 to justify her ouster"),
    ("HORMUZ", "Iran claims it shot down a US MQ-9 drone over Qeshm"),
    ("TECH", "China taps US AI models to train homegrown rivals, Reuters finds"),
]

# Column plan: (illustrated keys, slice of TEXT_STORIES)
COLUMNS = [
    (["kyiv", "gulf", "manila"], TEXT_STORIES[0:10]),
    (["cop31", "gaza", "chip"], TEXT_STORIES[10:20]),
    (["paris", "ebola", "argentina", "lakers"], TEXT_STORIES[20:28]),
]

TICKER = [
    "Togo stun Algeria 3\u20130",
    "Sensex at highest since Feb",
    "Guatemala prosecutor shot, stable",
    "ECOWAS chiefs meet in Dakar",
    "CFTC halts Kalshi Trump markets",
]

MARKETS = (
    "DOW 50,759 \u22121.64%  \u00b7  S&P 500 7,341 \u22121.03%  \u00b7  NASDAQ 24,328 "
    "\u22120.74%  \u00b7  EUROPE \u22121.8%  \u00b7  BRENT $93.14 +0.76%  \u00b7  GOLD $3,849  "
    "\u00b7  BTC $64,947  \u00b7  NVIDIA +4% after hours"
)

FOOTER = (
    "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 Al Jazeera \u00b7 PAHO \u00b7 WHO \u00b7 ASEAN \u00b7 "
    "SEC filings \u00b7 Scores: USA Today, NBC Sports.  All photographs are illustrations "
    "generated for this front page."
)

# World map: coarse continent outlines as (lon, lat) polygons.
CONTINENTS = [
    # North America
    [(-168, 66), (-158, 71), (-140, 70), (-125, 72), (-110, 73), (-95, 72),
     (-85, 70), (-80, 73), (-70, 62), (-60, 52), (-55, 52), (-65, 45),
     (-70, 42), (-75, 35), (-80, 32), (-81, 25), (-85, 30), (-90, 29),
     (-97, 26), (-105, 20), (-95, 16), (-87, 13), (-83, 9), (-79, 9),
     (-85, 15), (-95, 16), (-105, 23), (-115, 30), (-125, 40), (-124, 48),
     (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-45, 60), (-40, 64), (-30, 68), (-22, 70), (-25, 76), (-40, 80),
     (-55, 76), (-58, 70), (-52, 64)],
    # South America
    [(-79, 9), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-44, 2), (-35, -8),
     (-38, -15), (-40, -22), (-48, -28), (-52, -33), (-58, -38), (-62, -41),
     (-65, -45), (-68, -50), (-68, -54), (-72, -54), (-73, -45), (-73, -37),
     (-70, -30), (-70, -20), (-75, -15), (-77, -8), (-81, -4), (-80, 0)],
    # Africa
    [(-17, 15), (-10, 6), (-5, 5), (5, 6), (9, 4), (12, -2), (13, -12),
     (12, -18), (15, -22), (17, -29), (19, -34), (25, -34), (32, -29),
     (35, -23), (40, -15), (40, -10), (46, -2), (51, 2), (51, 11), (44, 11),
     (40, 15), (38, 18), (35, 22), (32, 31), (20, 32), (10, 37), (0, 36),
     (-6, 35), (-10, 31), (-15, 25), (-17, 20)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (10, 58),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 70), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (155, 70), (170, 67), (178, 65), (178, 62),
     (170, 60), (162, 56), (155, 52), (142, 50), (140, 40), (135, 35),
     (130, 33), (127, 35), (122, 38), (120, 32), (122, 28), (118, 25),
     (110, 20), (108, 12), (105, 9), (103, 2), (100, 7), (98, 12), (95, 16),
     (92, 21), (88, 22), (85, 20), (80, 15), (77, 8), (75, 12), (72, 20),
     (68, 23), (66, 25), (61, 25), (57, 27), (52, 26), (50, 29), (48, 30),
     (44, 29), (40, 31), (36, 36), (30, 36), (27, 37), (23, 36), (20, 40),
     (15, 44), (12, 44), (8, 44), (3, 43), (-2, 37), (-6, 36), (-9, 37)],
    # Britain
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (0, 53), (1, 51)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 36), (141, 39),
     (142, 42), (144, 44), (142, 45), (140, 42), (139, 38), (137, 35),
     (133, 34)],
    # Australia
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32), (132, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -23), (146, -19), (142, -15), (142, -11), (141, -13),
     (136, -12), (132, -12), (127, -14), (122, -17), (114, -21)],
    # New Zealand
    [(167, -45), (170, -43), (173, -39), (175, -38), (178, -38), (176, -40),
     (173, -42), (169, -46)],
    # Borneo
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3)],
    # Sumatra
    [(95, 5), (100, 0), (104, -5), (106, -6), (103, -3), (99, 2)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -10), (147, -9),
     (142, -8), (137, -7), (132, -4)],
    # Madagascar
    [(44, -12), (47, -15), (50, -17), (49, -22), (47, -25), (44, -24),
     (43, -18)],
    # Philippines
    [(120, 18), (122, 17), (122, 14), (120, 14)],
    # Iceland
    [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66), (-22, 65)],
]

MAP_LABELS = [
    ("NORTH AMERICA", -100, 58), ("SOUTH AMERICA", -60, -14),
    ("AFRICA", 19, 6), ("EUROPE", 16, 59), ("ASIA", 88, 52),
    ("AUSTRALIA", 134, -25),
]

# (lon, lat, legend text) -- a few dots are nudged a degree or two so the
# crowded Mediterranean cluster stays legible at this scale.
MARKERS = [
    (39.0, 47.0, "Kerch Bridge \u2014 span falls"),
    (30.0, 53.0, "Kyiv \u2014 bridges struck"),
    (56.3, 26.8, "Qeshm I. \u2014 US strike"),
    (45.0, 12.8, "Aden \u2014 Houthis advance"),
    (121.0, 14.6, "Manila \u2014 Quad summit"),
    (114.1, 22.5, "Shenzhen \u2014 trilateral next"),
    (26.0, 39.0, "Antalya \u2014 COP31 talks"),
    (-77.0, 38.9, "Washington \u2014 measles status lost"),
    (0.5, 50.5, "Paris \u2014 strike march"),
    (42.0, 35.0, "Jerusalem \u2014 new speaker"),
    (17.0, 45.0, "Skopje \u2014 plot foiled"),
    (32.5, 28.8, "Gaza \u2014 winter shelter plea"),
    (15.3, -4.3, "Kinshasa \u2014 Ebola obstacles"),
    (-80.5, -3.5, "Tumbes \u2014 river floods"),
    (1.2, 6.1, "Lom\u00e9 \u2014 Togo 3\u20130 Algeria"),
    (-64.2, -31.4, "C\u00f3rdoba \u2014 Argentina 7\u20130"),
]

STORY_COUNT = 1 + len(FIGURES) + sum(len(t) for _, t in COLUMNS) \
    + sum(len(i) for i, _ in COLUMNS) + len(TICKER)


# ---------------------------------------------------------------- helpers

def wrap(draw, text, fnt, width, max_lines=None):
    """Greedy word wrap; returns lines (truncated with an ellipsis if needed)."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "\u2026", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    return lines


def cover_crop(img, box_w, box_h, v_center=0.5):
    """Scale img to cover (box_w, box_h), cropping around v_center vertically."""
    scale = max(box_w / img.width, box_h / img.height)
    nw, nh = int(img.width * scale + 0.5), int(img.height * scale + 0.5)
    img = img.resize((nw, nh), Image.LANCZOS)
    cy = int(nh * v_center)
    top = min(max(cy - box_h // 2, 0), nh - box_h)
    left = (nw - box_w) // 2
    return img.crop((left, top, left + box_w, top + box_h))


def draw_headline(draw, x, y, width, tag, headline, fnt, leading, max_lines):
    """Tag in red caps + bold headline, wrapped; returns height used."""
    tag_txt = tag + " \u2014 "
    # Greedily fill: first line shares space with the tag, rest use full width.
    words = headline.split()
    lines, cur = [], ""
    limit = width - draw.textlength(tag_txt, font=F_TAG)
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur, limit = word, width
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while draw.textlength(lines[-1] + "\u2026", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    draw.text((x, y), tag_txt, font=F_TAG, fill=RED)
    tx = x + draw.textlength(tag_txt, font=F_TAG)
    draw.text((tx, y), lines[0], font=fnt, fill=INK)
    for i, line in enumerate(lines[1:], start=1):
        draw.text((x, y + i * leading), line, font=fnt, fill=INK)
    return len(lines) * leading


# ---------------------------------------------------------------- build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    inner = x1 - x0

    # --- top rules + masthead
    d.line([(x0, 4), (x1, 4)], fill=INK, width=3)
    d.line([(x0, 9), (x1, 9)], fill=INK, width=1)
    name = "THE WORLD TODAY"
    nw = d.textlength(name, font=F_NAME)
    d.text(((W - nw) / 2, 13), name, font=F_NAME, fill=INK)
    d.text((x0, 40), "Vol. I \u2014 No. 322", font=F_SMALL_CAPS, fill=GREY)
    right = "TUESDAY EDITION"
    d.text((x1 - d.textlength(right, font=F_SMALL_CAPS), 40), right,
           font=F_SMALL_CAPS, fill=GREY)

    # --- date bar
    d.rectangle([x0, 66, x1, 92], fill=INK)
    d.text((x0 + 10, 71), "TUESDAY, 17 NOVEMBER 2026", font=F_DATE,
           fill=(255, 255, 255))
    count_txt = "%d STORIES \u00b7 SIX CONTINENTS \u00b7 ONE DAY" % STORY_COUNT
    d.text((x1 - 10 - d.textlength(count_txt, font=F_DATE), 71), count_txt,
           font=F_DATE, fill=(255, 220, 120))

    # --- hero
    hero = Image.open(os.path.join(ASSETS, "hero-kerch.jpg")).convert("RGB")
    hero = cover_crop(hero, inner, 130, v_center=0.52)
    img.paste(hero, (x0, 96))
    d.rectangle([x0, 96, x1, 226], outline=INK, width=1)
    d.text((x0, 230), HERO_CAPTION, font=F_CAPTION, fill=GREY)

    # --- lead headline + subhead
    lw = d.textlength(LEAD_HEAD, font=F_LEAD)
    d.text(((W - lw) / 2, 244), LEAD_HEAD, font=F_LEAD, fill=INK)
    sub_lines = wrap(d, LEAD_SUB, F_SUB, inner - 40, max_lines=2)
    for i, line in enumerate(sub_lines):
        sw = d.textlength(line, font=F_SUB)
        d.text(((W - sw) / 2, 282 + i * 16), line, font=F_SUB, fill=(40, 40, 40))

    # --- figures strip
    fy, fh = 318, 42
    d.rectangle([x0, fy, x1, fy + fh], outline=RULE, width=1)
    cell = inner / len(FIGURES)
    for i, (num, lbl) in enumerate(FIGURES):
        cx = x0 + i * cell
        if i:
            d.line([(cx, fy + 5), (cx, fy + fh - 5)], fill=(200, 192, 172), width=1)
        d.text((cx + 8, fy + 2), num, font=F_FIG_NUM, fill=RED)
        lbl_lines = wrap(d, lbl, F_FIG_LBL, cell - 14, max_lines=2)
        for j, line in enumerate(lbl_lines):
            d.text((cx + 8, fy + 23 + j * 9), line, font=F_FIG_LBL, fill=INK)

    # --- section header
    sy = 362
    d.line([(x0, sy + 6), (x1, sy + 6)], fill=RULE, width=1)
    sec = "  THE DAY IN FULL  "
    sw = d.textlength(sec, font=F_SECTION)
    d.rectangle([(W - sw) / 2 - 2, sy - 1, (W + sw) / 2 + 2, sy + 13], fill=PAPER)
    d.text(((W - sw) / 2, sy - 1), sec, font=F_SECTION, fill=INK)

    # --- story columns
    col_y, col_h = 378, 366
    gap = 14
    col_w = (inner - 2 * gap) // 3
    for ci, (ill_keys, texts) in enumerate(COLUMNS):
        cx = x0 + ci * (col_w + gap)
        if ci:
            d.line([(cx - gap // 2, col_y), (cx - gap // 2, col_y + col_h)],
                   fill=(205, 198, 180), width=1)
        y = col_y
        # interleave: one illustrated item, then a run of text items
        queue = []
        per = len(texts) // len(ill_keys)
        for k, key in enumerate(ill_keys):
            queue.append(("ill", key))
            queue.extend(("txt", t) for t in
                         texts[k * per:(k + 1) * per if k < len(ill_keys) - 1
                               else len(texts)])
        for kind, item in queue:
            if kind == "ill":
                tag, head, asset = ILLUSTRATED[item]
                thumb = Image.open(os.path.join(ASSETS, asset)).convert("RGB")
                thumb = cover_crop(thumb, 62, 42, v_center=0.5)
                img.paste(thumb, (cx, y))
                d.rectangle([cx, y, cx + 62, y + 42], outline=RULE, width=1)
                draw_headline(d, cx + 68, y - 1, col_w - 68, tag, head,
                              F_HEAD_SM, 12, 3)
                y += 45
            else:
                tag, head = item
                draw_headline(d, cx, y, col_w, tag, head, F_HEAD, 12, 2)
                y += 23
        # thin rule under each column
        d.line([(cx, col_y + col_h + 2), (cx + col_w, col_y + col_h + 2)],
               fill=RULE, width=1)

    # --- world map panel
    my, mh = 750, 188
    d.rectangle([x0, my, x1, my + mh], outline=RULE, width=1)
    map_x, map_y, map_w, map_h = x0 + 6, my + 6, 580, mh - 12

    def project(lon, lat):
        px = map_x + (lon + 180.0) / 360.0 * map_w
        py = map_y + (75.0 - lat) / 135.0 * map_h
        return (px, py)

    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=OCEAN)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for label, lon, lat in MAP_LABELS:
        px, py = project(lon, lat)
        d.text((px - d.textlength(label, font=F_MAP_LBL) / 2, py - 4),
               label, font=F_MAP_LBL, fill=(120, 110, 90))
    for i, (lon, lat, _) in enumerate(MARKERS, start=1):
        px, py = project(lon, lat)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        num = str(i)
        d.text((px - d.textlength(num, font=F_MARK_NUM) / 2, py - 6), num,
               font=F_MARK_NUM, fill=(255, 255, 255))
    d.text((map_x + 6, map_y + 4), "WHERE IT HAPPENED", font=F_SECTION, fill=INK)

    # legend, two columns
    lx = map_x + map_w + 16
    d.text((lx, my + 8), "ON THE MAP", font=F_SECTION, fill=INK)
    leg_cols = [MARKERS[:8], MARKERS[8:]]
    for ci, col in enumerate(leg_cols):
        lcx = lx + ci * 196
        for ri, (_, _, text) in enumerate(col):
            ly = my + 28 + ri * 19
            num = str(ci * 8 + ri + 1)
            d.ellipse([lcx, ly + 1, lcx + 13, ly + 14], fill=RED)
            d.text((lcx + 6.5 - d.textlength(num, font=F_MARK_NUM) / 2, ly + 2),
                   num, font=F_MARK_NUM, fill=(255, 255, 255))
            d.text((lcx + 18, ly + 1), text, font=F_LEGEND, fill=INK)

    # --- markets strip (auto-fit: shrink until it fits the strip)
    mky = 946
    d.rectangle([x0, mky, x1, mky + 26], fill=(238, 231, 214))
    d.rectangle([x0, mky, x1, mky + 26], outline=RULE, width=1)
    mkt_font = F_MARKET
    for size in (11, 10, 9, 8):
        mkt_font = font("DejaVuSans-Bold.ttf", size)
        if d.textlength(MARKETS, font=mkt_font) <= inner - 16:
            break
    mw = d.textlength(MARKETS, font=mkt_font)
    d.text(((W - mw) / 2, mky + 7), MARKETS, font=mkt_font, fill=INK)

    # --- footer ticker + sources (auto-fit the same way)
    tick = "   \u25aa   ".join(TICKER)
    tick_font = F_FOOT
    for size in (9, 8):
        tick_font = font("DejaVuSans.ttf", size)
        if d.textlength(tick, font=tick_font) <= inner:
            break
    d.text((x0, 978), tick, font=tick_font, fill=(70, 66, 58))
    d.line([(x0, 996), (x1, 996)], fill=RULE, width=1)
    fw = d.textlength(FOOTER, font=F_FOOT)
    d.text(((W - fw) / 2, 1002), FOOTER, font=F_FOOT, fill=GREY)

    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    if size > 1048576:
        # PNG too big: JPEG is allowed under the same entry.png name.
        img.save(out, "JPEG", quality=88, optimize=True)
        size = os.path.getsize(out)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print("stories: %d" % STORY_COUNT)
    print("wrote %s  %dx%d  %d bytes  sha256 %s" % (out, img.width, img.height,
                                                    size, sha))
    if size > 1048576:
        print("ERROR: still over 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
