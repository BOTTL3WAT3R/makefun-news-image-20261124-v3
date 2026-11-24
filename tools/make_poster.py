#!/usr/bin/env python3
"""Draw the news poster for Tuesday 24 November 2026.

Renders a one-page newspaper-style poster (1024 x 1024 PNG) that sums up
the day's six biggest stories, and writes it to ../poster.png next to the
repository's entrypoint. This generator is a build-time tool only: the
submitted program (main.py) never renders anything, it copies the
committed poster.png byte for byte.

Run:  python3 tools/make_poster.py
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36

PAPER = (247, 242, 231)
INK = (24, 22, 20)
FAINT = (108, 100, 88)
RED = (143, 29, 34)
RED_DARK = (110, 20, 26)
GREEN = (22, 128, 57)
BLUE = (30, 74, 138)
ORANGE = (224, 110, 26)
PANEL = (255, 252, 245)
GREY_LINE = (196, 188, 168)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SERIF = str(FONT_DIR / "DejaVuSerif.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, xy, s, fnt, fill=INK):
    draw.text(xy, s, font=fnt, fill=fill)
    return draw.textlength(s, font=fnt)


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, s, fnt, max_w, fill=INK, leading=1.12):
    x, y = xy
    size = fnt.size
    for line in wrap(draw, s, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def hline(draw, x0, x1, y, fill=INK, width=3):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def paper_texture(img, seed=20261124):
    """Blend a whisper of grain into the page so it reads as print."""
    rng = random.Random(seed)
    noise = Image.effect_noise((W, H), 10).convert("L")
    tint = Image.merge(
        "RGB",
        (
            noise.point(lambda v: 232 + (v - 128) // 6),
            noise.point(lambda v: 226 + (v - 128) // 6),
            noise.point(lambda v: 210 + (v - 128) // 6),
        ),
    )
    return Image.blend(img, tint, 0.09)


def masthead(draw):
    y = MARGIN
    small = font(SANS_BOLD, 19)
    text_w(draw, (MARGIN, y), "ONE IMAGE  ·  ALL THE NEWS THAT MATTERS", small, FAINT)
    right = "No. 24-11"
    draw.text((W - MARGIN - draw.textlength(right, font=small), y), right, font=small, fill=FAINT)
    y += 28
    hline(draw, MARGIN, W - MARGIN, y, INK, 5)
    y += 10
    title = font(SERIF_BOLD, 66)
    s = "THE WORLD TODAY"
    draw.text(((W - draw.textlength(s, font=title)) / 2, y), s, font=title, fill=INK)
    y += 80
    hline(draw, MARGIN, W - MARGIN, y, INK, 2)
    return y + 8


def date_band(draw, y):
    band_h = 86
    for i in range(band_h):
        t = i / band_h
        col = tuple(int(RED[c] + (RED_DARK[c] - RED[c]) * t) for c in range(3))
        draw.line([(MARGIN, y + i), (W - MARGIN, y + i)], fill=col)
    f = font(SANS_BOLD, 52)
    s = "TUESDAY 24 NOVEMBER 2026"
    draw.text(((W - draw.textlength(s, font=f)) / 2, y + 15), s, font=f, fill=(255, 250, 240))
    return y + band_h + 14


def lead_story(draw, y):
    x = MARGIN
    w = 600
    text_w(draw, (x, y), "MARKETS  ·  TECHNOLOGY", font(SANS_BOLD, 20), RED)
    y += 32
    y = draw_wrapped(draw, (x, y), "NVIDIA LEAPS 31%", font(SERIF_BOLD, 60), w, INK, 1.04)
    y += 4
    y = draw_wrapped(
        draw, (x, y), "Jensen Huang reinstated as CEO", font(SERIF, 30), w, (52, 48, 44), 1.12
    )
    y += 6
    y = draw_wrapped(
        draw,
        (x, y),
        "The chip giant's shares surge as its founder returns to the "
        "top job — the day's biggest market move.",
        font(SANS, 22),
        w,
        (66, 61, 53),
        1.22,
    )
    return y


def chart_panel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(238, 244, 233), outline=GREY_LINE, width=2)
    text_w(draw, (x + 14, y + 10), "NVDA  ·  ONE DAY", font(SANS_BOLD, 17), FAINT)
    base = y + h - 26
    draw.line([(x + 16, base), (x + w - 16, base)], fill=FAINT, width=2)
    pts = [
        (x + 22, base - 14),
        (x + 70, base - 30),
        (x + 118, base - 24),
        (x + 166, base - 58),
        (x + 214, base - 52),
        (x + 262, base - 96),
        (x + w - 30, base - 128),
    ]
    draw.line(pts, fill=GREEN, width=6, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 20, ey + 2), (ex - 4, ey + 18)], fill=GREEN)
    text_w(draw, (x + w - 108, ey - 42), "+31%", font(SANS_BOLD, 30), GREEN)


def story_block(draw, x, y, w, number, kicker, headline, sub, accent):
    draw.rectangle([x, y, x + 34, y + 34], fill=accent)
    nf = font(SANS_BOLD, 22)
    ns = str(number)
    draw.text((x + (34 - draw.textlength(ns, font=nf)) / 2, y + 4), ns, font=nf, fill=(255, 250, 240))
    text_w(draw, (x + 46, y + 5), kicker, font(SANS_BOLD, 18), accent)
    y += 42
    y = draw_wrapped(draw, (x, y), headline, font(SERIF_BOLD, 27), w, INK, 1.04)
    y += 2
    y = draw_wrapped(draw, (x, y), sub, font(SANS, 20), w, (66, 61, 53), 1.14)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = masthead(draw)
    y = date_band(draw, y)

    lead_bottom = lead_story(draw, y)
    chart_panel(draw, 668, y + 4, 320, 200)
    hline(draw, MARGIN, W - MARGIN, lead_bottom + 12, GREY_LINE, 2)

    grid_y = lead_bottom + 26
    col_w = (W - 2 * MARGIN - 28) // 2
    x1, x2 = MARGIN, MARGIN + col_w + 28

    b1 = story_block(
        draw, x1, grid_y, col_w, 2, "WAR AT SEA",
        "Ukrainian sea drones sink Russian corvette Merkury",
        "Sunk off Benghazi, Libya — far from the Black Sea front.",
        BLUE,
    )
    b2 = story_block(
        draw, x2, grid_y, col_w, 3, "CLIMATE",
        "COP31 talks collapse without a deal",
        "Negotiators head home empty-handed.",
        GREEN,
    )
    row2_y = max(b1, b2) + 16
    b3 = story_block(
        draw, x1, row2_y, col_w, 4, "INDONESIA",
        "Factory fire kills 24 in Banten, Indonesia",
        "Among the country's deadliest industrial blazes in years.",
        ORANGE,
    )
    b4 = story_block(
        draw, x2, row2_y, col_w, 5, "MEXICO",
        "Mexico captures \u2018Chapo Isidro\u2019",
        "The cartel figure is taken alive in a security operation.",
        RED,
    )
    row3_y = max(b3, b4) + 14
    hline(draw, MARGIN, W - MARGIN, row3_y - 6, GREY_LINE, 2)
    end_y = story_block(
        draw, x1, row3_y, W - 2 * MARGIN, 6, "UNITED STATES",
        "US Democrats win biggest House majority since 1992",
        "A historic night in Washington redraws the balance of power in Congress.",
        BLUE,
    )

    foot_y = end_y + 16
    hline(draw, MARGIN, W - MARGIN, foot_y, INK, 3)
    ff = font(SANS_BOLD, 19)
    s = "SIX STORIES  ·  ONE DAY  ·  TUESDAY 24 NOVEMBER 2026"
    draw.text(
        ((W - draw.textlength(s, font=ff)) / 2, foot_y + 10), s, font=ff, fill=FAINT
    )

    img = paper_texture(img)
    out = Path(__file__).resolve().parent.parent / "poster.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
