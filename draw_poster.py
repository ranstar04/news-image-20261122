"""Draw the news poster for make.fun bounty news-image-20261122.

Renders "The World in One Day - 22 November 2026" as a 1024x1024 PNG
with six verified stories from 20-22 November 2026. Run locally with
Pillow; the committed entry.png is the output. main.py only copies it.

Stories (sources in README.md):
1. Baltic: drones hit the Russian cargo ship Sparta II; 16 crew evacuated.
2. Peru: magnitude 6.7 quake near Junin, felt in Lima, no casualties.
3. COP31: climate talks in Antalya stall in overtime over fossil fuels.
4. Iran/US: Trump says Iran wants a deal, "not one I'll accept".
5. Denmark: Russian diplomat expelled over a foiled assassination plot.
6. Cyclone Akvan: landfall near Gopalpur, Odisha; 300,000+ evacuated.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
RED = (193, 39, 45)
TEAL = (14, 116, 109)
AMBER = (180, 120, 10)
SLATE = (71, 85, 105)
LIGHT = (255, 255, 255)
CARD = (255, 255, 255)
GOLD = (201, 162, 39)
SEA = (23, 58, 94)
SEA_DARK = (13, 38, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap measured in pixels; returns list of lines."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, spacing=4):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def kicker(draw, x, y, label, color):
    fnt = font(SANS_B, 17)
    w = int(draw.textlength(label, font=fnt)) + 20
    draw.rounded_rectangle([x, y, x + w, y + 28], radius=14, fill=color)
    draw.text((x + 10, y + 4), label, font=fnt, fill=LIGHT)
    return w


def card(draw, box, accent):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=10, fill=CARD,
                           outline=(203, 196, 178), width=2)
    draw.rectangle([x0, y0 + 10, x0 + 6, y1 - 10], fill=accent)


def story_card(draw, box, accent, tag, headline, deck, fact, head_size=27,
               deck_size=18):
    x0, y0, x1, y1 = box
    card(draw, box, accent)
    px = x0 + 22
    py = y0 + 16
    kicker(draw, px, py, tag, accent)
    py += 40
    py = draw_wrapped(draw, px, py, headline, font(SANS_B, head_size),
                      x1 - px - 20, INK, spacing=2)
    py += 6
    py = draw_wrapped(draw, px, py, deck, font(SANS, deck_size),
                      x1 - px - 20, SLATE, spacing=3)
    draw.text((px, y1 - 30), fact, font=font(SANS, 14), fill=(120, 113, 96))


def draw_ship_scene(draw, x0, y0, x1, y1):
    """Simple night-sea scene: sky, sea, burning cargo ship, two drones."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=SEA_DARK)
    draw.rectangle([x0, y0 + 118, x1, y1], fill=SEA)
    # moon
    draw.ellipse([x1 - 66, y0 + 18, x1 - 26, y0 + 58], fill=(238, 230, 200))
    # ship hull
    draw.polygon([(x0 + 18, y0 + 128), (x0 + 258, y0 + 128),
                  (x0 + 238, y0 + 168), (x0 + 38, y0 + 168)], fill=(38, 48, 66))
    draw.rectangle([x0 + 62, y0 + 100, x0 + 148, y0 + 128], fill=(58, 72, 96))
    draw.rectangle([x0 + 158, y0 + 112, x0 + 214, y0 + 128], fill=(58, 72, 96))
    # containers
    for i, cx in enumerate([x0 + 66, x0 + 104, x0 + 142]):
        draw.rectangle([cx, y0 + 84, cx + 34, y0 + 100],
                       fill=[(193, 39, 45), (201, 162, 39), (14, 116, 109)][i])
    # fire + smoke over the bridge
    draw.polygon([(x0 + 168, y0 + 108), (x0 + 186, y0 + 66),
                  (x0 + 204, y0 + 108)], fill=(245, 158, 11))
    draw.polygon([(x0 + 178, y0 + 108), (x0 + 188, y0 + 82),
                  (x0 + 198, y0 + 108)], fill=(239, 68, 68))
    draw.ellipse([x0 + 176, y0 + 44, x0 + 202, y0 + 70], fill=(100, 116, 139))
    draw.ellipse([x0 + 192, y0 + 28, x0 + 214, y0 + 52], fill=(148, 163, 184))
    # two drones
    for dx, dy in [(x0 + 44, y0 + 34), (x0 + 96, y0 + 22)]:
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=LIGHT)
        draw.line([dx - 12, dy, dx + 12, dy], fill=LIGHT, width=2)
        draw.line([dx, dy - 12, dx, dy + 12], fill=LIGHT, width=2)
    # waves
    for wy in (y0 + 162, y0 + 176):
        for wx in range(x0 + 8, x1 - 20, 34):
            draw.arc([wx, wy, wx + 28, wy + 14], 180, 360,
                     fill=(125, 180, 220), width=3)
    draw.text((x0 + 14, y1 - 26), "SPARTA II  •  GULF OF FINLAND",
              font=font(SANS_B, 14), fill=(191, 219, 254))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    draw.rectangle([0, 0, W, 152], fill=NAVY)
    draw.rectangle([0, 152, W, 158], fill=GOLD)
    draw.text((32, 22), "THE WORLD IN ONE DAY",
              font=font(SERIF_B, 58), fill=LIGHT)
    draw.text((34, 96), "SUNDAY, 22 NOVEMBER 2026",
              font=font(SANS_B, 24), fill=(191, 219, 254))
    draw.text((34, 126), "Six stories that defined the day",
              font=font(SANS, 19), fill=(203, 213, 225))

    # ---- Lead story: Baltic drone strike ----
    lx0, ly0, lx1, ly1 = 24, 176, 1000, 420
    card(draw, (lx0, ly0, lx1, ly1), RED)
    px = lx0 + 24
    py = ly0 + 16
    kicker(draw, px, py, "BALTIC  •  LEAD STORY", RED)
    py += 42
    py = draw_wrapped(draw, px, py, "Drones set a Russian\ncargo ship ablaze",
                      font(SANS_B, 36), 600, INK, spacing=2)
    py += 8
    py = draw_wrapped(
        draw, px, py,
        "The Sparta II, bound for Kaliningrad, was hit by two drones "
        "in the Gulf of Finland. Its 16 crew evacuated as the "
        "burning ship drifted into Finnish waters.",
        font(SANS, 18), 600, SLATE, spacing=4)
    py += 10
    draw.text((px, py), "Finland says Ukraine was likely behind the attack.",
              font=font(SANS_B, 18), fill=RED)
    draw_ship_scene(draw, 668, ly0 + 16, 976, ly1 - 16)

    # ---- Middle row: Peru + COP31 ----
    story_card(draw, (24, 436, 500, 668), AMBER, "PERU  •  EARTHQUAKE",
               "A 6.7 quake shakes Peru's Andes",
               "The tremor struck near Junin on Friday evening and was "
               "felt in Lima, sending residents into the streets. No "
               "casualties were reported.",
               "USGS  •  20 Nov 2026", head_size=26)
    story_card(draw, (516, 436, 1000, 668), TEAL, "CLIMATE  •  COP31",
               "Climate talks stall in overtime",
               "Negotiators in Antalya stretched past their Friday "
               "deadline, deadlocked over fossil fuels. The draft "
               "drops any mention of them.",
               "Reuters  •  21 Nov 2026", head_size=26)

    # ---- Bottom row: Iran, Denmark, Cyclone ----
    story_card(draw, (24, 684, 344, 940), RED, "IRAN  •  U.S.",
               "Trump: Iran wants a deal he won't accept",
               "The president demanded a “real deal” as Washington "
               "tightens its blockade on Tehran.",
               "White House  •  20 Nov 2026", head_size=20, deck_size=16)
    story_card(draw, (360, 684, 680, 940), NAVY, "DENMARK  •  EUROPE",
               "Denmark expels Russian diplomat over foiled plot",
               "Copenhagen blames Russian intelligence for a plot "
               "to kill rapper Kyivstoner. Two charged.",
               "PET / WSJ  •  20 Nov 2026", head_size=20, deck_size=16)
    story_card(draw, (696, 684, 1000, 940), TEAL, "INDIA  •  WEATHER",
               "Cyclone Akvan hits India's east coast",
               "The storm hit near Gopalpur, Odisha, gusting to "
               "90 km/h. Over 300,000 people were evacuated.",
               "IMD  •  20 Nov 2026", head_size=20, deck_size=16)

    # ---- Footer ----
    draw.text((24, 958),
              "Sources: Reuters, AP, CNN, USGS, India Meteorological Dept.  •  20–22 Nov 2026",
              font=font(SANS, 15), fill=(120, 113, 96))
    draw.text((700, 958), "make.fun  •  news-image-20261122",
              font=font(SANS_B, 15), fill=NAVY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
