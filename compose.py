#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Tuesday 17 November 2026.

Reads photo.jpg (the collapsed Kerch bridge photograph), lays out the
masthead, the lead story and 28 further stories in three columns, and
writes the finished 1024x1024 page as entry.png (JPEG bytes).

Geometry was set by measuring the finished page itself: masthead cap
40 px, photo strip 26..998 by 121..373, lead headline cap 23 px, story
columns starting at y 464 with a 39 px pitch per one-deck-line story.

Run from anywhere:  python3 compose.py
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(HERE, "photo.jpg")
OUT = os.path.join(HERE, "entry.png")

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 26            # outer side margin: rules, photo and ticker span 26..998
COL_W = 313            # width of one story column
COL_X = [26, 355, 684]  # column left edges
COL_TOP = 464          # first section header / first headline

INK = (12, 12, 12)
GREY = (88, 88, 88)
RED = (178, 24, 24)
RULE = (60, 60, 60)
PAPER = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "liberation", "LiberationSans-Regular.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "liberation", "LiberationSans-Bold.ttf")

# Photo strip: a wide slice of the photograph holding the arch, the smoke
# and the water, with the misty hills along the top. In photo pixels.
PHOTO_TOP = 230
PHOTO_BOTTOM = 728
BANNER_H = 252


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns the lines that fit in width."""
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
    return lines


def centred(draw, y, text, fnt, fill):
    draw.text((PAGE_W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def hline(draw, y, weight=1, fill=INK):
    draw.rectangle([MARGIN, y, PAGE_W - MARGIN, y + weight - 1], fill=fill)


# ---------------------------------------------------------------- stories
# Each column is a list of blocks: ("section", TITLE) or
# ("story", headline, deck). The lead story sits above the columns.

LEAD_HEAD = "UKRAINE BRINGS DOWN KERCH BRIDGE SPAN"
LEAD_DECK = ("Second night of strikes collapses a road span of Russia's link "
             "to Crimea; Moscow hits two Kyiv bridges in reply.")

COLUMNS = [
    [
        ("section", "NORTH AMERICA"),
        ("story", "No blackout: FEMA tests alert system",
         "Nationwide EAS test at 2:20 p.m. ET; agency rebuts viral blackout rumour."),
        ("story", "Microsoft explains global outage",
         "Latent defect plus load knocked out 80% of servers last week."),
        ("story", "Trump lands in Manila for ASEAN",
         "Asia trip ahead of Thursday's Xi-Trump-Putin talks in Shenzhen."),
        ("story", "Mamdani disbands NYPD unit",
         "New York mayor ends the Strategic Response Group."),
        ("story", "US banks hit by software glitches",
         "Major banks report disruptions; JPMorgan denies cyberattack."),
        ("story", "Petrol falls to $3.78 a gallon",
         "US fuel prices down about 20 cents in a week."),
        ("section", "EUROPE"),
        ("story", "Russia strikes Kyiv bridges",
         "Two river crossings hit; engineers assess the damage."),
        ("story", "Estonia to shut Russian border",
         "Crossings close Dec. 1 after a foiled drone-plant bomb plot."),
        ("story", "Five EU states plan Rwanda hub",
         "Return hub for failed asylum seekers, led by Germany."),
    ],
    [
        ("story", "UK sanctions settlement builders",
         "Eight Israeli construction firms hit over West Bank building."),
        ("story", "Depardieu admits assault charge",
         "French actor drops his appeal in a Paris court."),
        ("story", "Xi and Carney agree tariff cuts",
         "Canada and China pledge deeper ties."),
        ("story", "UN meets on killer robots",
         "128 states in Geneva debate a ban on lethal autonomous weapons."),
        ("section", "ASIA"),
        ("story", "Xi-Trump-Putin summit set",
         "China confirms first three-way meeting, Thursday in Shenzhen."),
        ("story", "Japan scrambles fighter jets",
         "Suspected Russian planes violate airspace; Tokyo protests."),
        ("story", "Third US carrier reaches Gulf",
         "Build-up grows as tankers are hit near Hormuz."),
        ("story", "Rocket failure destroys satellites",
         "Boeing-Lockheed launch fails; Amazon payload lost."),
        ("section", "MIDDLE EAST"),
        ("story", "Iran drones at Bahrain base downed",
         "IRGC targeted US radar at Sheikh Isa; no casualties."),
    ],
    [
        ("story", "US intel: Iran plots dirty bomb",
         "CNN: Tehran weighing attack on Trump officials in Washington."),
        ("story", "Tankers hit by mines near Hormuz",
         "Several vessels struck; crew abandons gas tanker off Oman."),
        ("story", "West urges Israel to open Gaza aid",
         "UK, Australia, Canada, Italy call the situation catastrophic."),
        ("story", "Houthis advance on Aden",
         "Saudi-backed forces pull back from the Red Sea coast."),
        ("section", "AFRICA"),
        ("story", "Ebola still out of control",
         "DR Congo: 11,200 cases, 5,500 dead after six months."),
        ("story", "17 dead in South Africa shootings",
         "Two mass shootings in KwaZulu-Natal and Gauteng."),
        ("story", "Guinea arrests 1,263 miners",
         "Illegal gold-mining ban; 10 killed in clashes."),
        ("story", "Eritrea eliminates trachoma",
         "WHO validates elimination of the eye disease."),
        ("section", "SOUTH AMERICA"),
        ("story", "Pope urges justice for Amazon defenders",
         "Leo XIV in Peru; struck by object thrown from crowd."),
        ("section", "OCEANIA"),
        ("story", "RBA split over sharper downturn",
         "Dissenters warn on Australia's economy."),
    ],
]

TICKER = ("COP31 DRAFT EXPOSES DIVISIONS  \u2022  GRAMMYS: AFRICAN ARTISTS TAKE 4 OF 5 "
          "GLOBAL ALBUM SPOTS  \u2022  RIO TINTO PAYS $250M FOR PANGUNA")


def build_banner():
    """Crop the photograph to the banner strip and scale it to page width."""
    photo = Image.open(PHOTO).convert("RGB")
    strip = photo.crop((0, PHOTO_TOP, photo.width, PHOTO_BOTTOM))
    return strip.resize((PAGE_W - 2 * MARGIN, BANNER_H), Image.LANCZOS)


def draw_columns(draw):
    sect_f = font(SANS_BOLD, 14)
    head_f = font(SANS_BOLD, 14)
    deck_f = font(SANS, 10)
    for x, blocks in zip(COL_X, COLUMNS):
        y = COL_TOP
        for block in blocks:
            if block[0] == "section":
                draw.text((x, y), block[1], font=sect_f, fill=RED)
                y += 16
                draw.rectangle([x, y, x + COL_W, y], fill=RULE)
                y += 11
                continue
            _, headline, deck = block
            draw.text((x, y), headline, font=head_f, fill=INK)
            y += 15
            for line in wrap(draw, deck, deck_f, COL_W):
                draw.text((x, y), line, font=deck_f, fill=GREY)
                y += 15
            y += 9


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead and dateline.
    centred(draw, 27, "THE WORLD TODAY", font(SERIF_BOLD, 58), INK)
    hline(draw, 81, 3)
    date_f = font(SANS_BOLD, 16)
    draw.text((MARGIN, 92), "TUESDAY, NOVEMBER 17, 2026", font=date_f, fill=INK)
    centred(draw, 92, "29 STORIES  \u2022  6 CONTINENTS", date_f, RED)
    draw.text((PAGE_W - MARGIN, 92), "LATE FINAL", font=date_f, fill=INK, anchor="ra")
    hline(draw, 112, 1)

    # Photograph banner.
    page.paste(build_banner(), (MARGIN, 121))

    # Lead story.
    centred(draw, 390, LEAD_HEAD, font(SANS_BOLD, 33), INK)
    centred(draw, 428, LEAD_DECK, font(SANS, 14), GREY)
    hline(draw, 450, 1)

    # Story columns.
    draw_columns(draw)

    # Footer ticker.
    hline(draw, 994, 1)
    centred(draw, 1003, TICKER, font(SANS_BOLD, 12), GREY)

    page.save(OUT, "JPEG", quality=90, optimize=True)
    print(f"wrote {OUT} {PAGE_W}x{PAGE_H} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
