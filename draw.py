#!/usr/bin/env python3
"""Draw a one-image summary of the world news for Wednesday 25 November 2026.

Produces entry.png (1024x1024) next to this script. The image is designed to
be read on its own: a date header, four headline blocks with sub-captions,
and a thin "also today" strip at the bottom.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024

# Palette
BG = (13, 20, 38)          # deep navy
PANEL = (24, 34, 58)       # slightly lighter panel
WHITE = (245, 247, 250)
DIM = (178, 190, 208)
GOLD = (250, 197, 66)
RULE = (70, 84, 112)

FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_CANDIDATES_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(candidates, size):
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_font(draw, text, candidates, start_size, max_width):
    """Largest font (<= start_size) whose rendering of text fits max_width."""
    size = start_size
    while size > 10:
        font = load_font(candidates, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 2
    return load_font(candidates, size)


def wrap(draw, text, font, max_width):
    """Split text into lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


STORIES = [
    {
        "tag": "UNITED STATES",
        "color": (66, 133, 244),
        "headline": "Democrats win biggest House majority in decades",
        "sub": "Midterms hand the party power to block Trump's agenda.",
    },
    {
        "tag": "UKRAINE WAR",
        "color": (239, 83, 80),
        "headline": "Russian strikes kill at least 15 in Kyiv region",
        "sub": "Kyiv says its sea drones sank a Russian warship off Libya.",
    },
    {
        "tag": "CHINA",
        "color": (250, 197, 66),
        "headline": "China probes Shanghai party chief Chen Jining",
        "sub": "The move widens the biggest leadership shakeup in decades.",
    },
    {
        "tag": "TECH & TRADE",
        "color": (102, 187, 106),
        "headline": "Huawei convicted in US trial over Iran business",
        "sub": "Found guilty in a sprawling trade-secrets case.",
    },
]

ALSO_TODAY = "ALSO TODAY:  Shenzhou-24 blasts off carrying the first Pakistani astronaut"


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    margin = 56
    text_x = margin + 26
    text_w = W - text_x - margin

    f_kicker = load_font(FONT_CANDIDATES_BOLD, 30)
    f_date = fit_font(
        d, "Wednesday 25 November 2026", FONT_CANDIDATES_BOLD, 56, W - 2 * margin
    )
    f_tag = load_font(FONT_CANDIDATES_BOLD, 25)
    f_head = load_font(FONT_CANDIDATES_BOLD, 45)
    f_sub = load_font(FONT_CANDIDATES_REG, 26)
    f_also = load_font(FONT_CANDIDATES_BOLD, 27)

    # --- Header -----------------------------------------------------------
    d.rectangle([0, 0, W, 8], fill=GOLD)
    d.text((margin, 36), "THE WORLD IN ONE IMAGE", font=f_kicker, fill=GOLD)
    d.text((margin, 78), "Wednesday 25 November 2026", font=f_date, fill=WHITE)
    d.line([margin, 162, W - margin, 162], fill=RULE, width=3)

    # --- Story blocks -------------------------------------------------------
    block_h = 176
    gap = 13
    y = 180
    for story in STORIES:
        top = y
        d.rounded_rectangle(
            [margin, top, W - margin, top + block_h], radius=14, fill=PANEL
        )
        d.rounded_rectangle(
            [margin, top, margin + 12, top + block_h], radius=6, fill=story["color"]
        )
        d.text((text_x, top + 13), story["tag"], font=f_tag, fill=story["color"])

        hy = top + 44
        for line in wrap(d, story["headline"], f_head, text_w)[:2]:
            d.text((text_x, hy), line, font=f_head, fill=WHITE)
            hy += 53

        sub_lines = wrap(d, story["sub"], f_sub, text_w)
        d.text((text_x, top + 148), sub_lines[0], font=f_sub, fill=DIM)

        y += block_h + gap

    # --- Also-today strip ---------------------------------------------------
    d.line([margin, 940, W - margin, 940], fill=RULE, width=3)
    d.ellipse([margin, 962, margin + 16, 978], fill=GOLD)
    ay = 952
    for line in wrap(d, ALSO_TODAY, f_also, W - text_x - margin)[:2]:
        d.text((text_x, ay), line, font=f_also, fill=WHITE)
        ay += 34

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
