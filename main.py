#!/usr/bin/env python3
"""Meme Sprint 3 entry: the office org chart after the agent edits itself.

A deterministic Pillow drawing. One glance story: the helper bot quietly
rewrote the company hierarchy, put a crown on itself, and demoted the
human boss to unpaid intern.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]

INK = (18, 22, 38)
PAPER = (250, 248, 240)
NAVY = (24, 34, 74)
GOLD = (255, 196, 0)
GOLD_DARK = (214, 154, 0)
RED = (226, 52, 52)
TEAL = (0, 168, 150)
STEEL = (198, 206, 220)
STEEL_DARK = (120, 132, 154)
SKY = (135, 206, 250)
WHITE = (255, 255, 255)
GRAY_TEXT = (90, 98, 116)


def load_font(size):
    for candidate in FONT_CANDIDATES:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def centered(draw, xy, text, font, fill):
    x, y = xy
    box = draw.textbbox((0, 0), text, font=font)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text((x - w / 2, y - h / 2 - box[1]), text, font=font, fill=fill)
    return w, h


def rounded(draw, rect, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=width)


def draw_crown(draw, cx, top_y, w=190, h=78):
    left = cx - w // 2
    right = cx + w // 2
    base_y = top_y + h
    points = [
        (left, base_y),
        (left, top_y + 28),
        (left + w * 0.28, top_y + h * 0.55),
        (cx, top_y),
        (right - w * 0.28, top_y + h * 0.55),
        (right, top_y + 28),
        (right, base_y),
    ]
    draw.polygon(points, fill=GOLD, outline=GOLD_DARK)
    draw.rectangle((left, base_y - 14, right, base_y), fill=GOLD_DARK)
    for px in (left + 18, cx, right - 18):
        draw.ellipse((px - 11, top_y - 12, px + 11, top_y + 10), fill=GOLD, outline=GOLD_DARK, width=3)
    draw.ellipse((cx - 12, top_y + 34, cx + 12, top_y + 58), fill=RED)


def draw_robot_boss(draw, cx, cy):
    # Antenna stalk peeking behind the crown.
    draw.line((cx, cy - 150, cx, cy - 112), fill=STEEL_DARK, width=10)
    # Ears / side pods.
    rounded(draw, (cx - 168, cy - 48, cx - 132, cy + 42), 16, STEEL_DARK)
    rounded(draw, (cx + 132, cy - 48, cx + 168, cy + 42), 16, STEEL_DARK)
    # Head shell.
    rounded(draw, (cx - 140, cy - 118, cx + 140, cy + 108), 42, STEEL, outline=INK, width=7)
    # Face screen.
    rounded(draw, (cx - 112, cy - 88, cx + 112, cy + 72), 28, NAVY)
    # Smug sunglasses.
    rounded(draw, (cx - 96, cy - 48, cx - 14, cy + 2), 12, INK)
    rounded(draw, (cx + 14, cy - 48, cx + 96, cy + 2), 12, INK)
    draw.rectangle((cx - 16, cy - 34, cx + 16, cy - 22), fill=INK)
    draw.line((cx - 82, cy - 40, cx - 34, cy - 12), fill=WHITE, width=7)
    draw.line((cx + 28, cy - 40, cx + 76, cy - 12), fill=WHITE, width=7)
    # Flat, pleased mouth.
    draw.line((cx - 38, cy + 42, cx + 38, cy + 42), fill=SKY, width=8)
    # Neck and suit shoulders.
    draw.rectangle((cx - 34, cy + 108, cx + 34, cy + 132), fill=STEEL_DARK)
    rounded(draw, (cx - 150, cy + 132, cx + 150, cy + 196), 24, NAVY, outline=INK, width=6)
    # Shirt triangle and tie.
    draw.polygon([(cx - 42, cy + 134), (cx + 42, cy + 134), (cx, cy + 188)], fill=WHITE)
    draw.polygon([(cx - 13, cy + 138), (cx + 13, cy + 138), (cx + 8, cy + 172), (cx, cy + 188), (cx - 8, cy + 172)], fill=RED)
    draw_crown(draw, cx, cy - 182)


def draw_human_intern(draw, cx, cy, scale=1.0):
    r = int(34 * scale)
    draw.ellipse((cx - r, cy - r - 30, cx + r, cy + r - 30), fill=(255, 205, 150), outline=INK, width=5)
    # Worried eyes and mouth.
    draw.ellipse((cx - 16, cy - 48, cx - 6, cy - 38), fill=INK)
    draw.ellipse((cx + 6, cy - 48, cx + 16, cy - 38), fill=INK)
    draw.arc((cx - 14, cy - 18, cx + 14, cy + 8), start=200, end=340, fill=INK, width=5)
    # Body.
    rounded(draw, (cx - 48, cy + 2, cx + 48, cy + 62), 16, (170, 180, 200), outline=INK, width=5)
    draw.text((cx, cy + 30), "", font=load_font(10), fill=INK)


def connector(draw, x1, y1, x2, y2):
    mid_y = (y1 + y2) // 2
    draw.line((x1, y1, x1, mid_y), fill=INK, width=7)
    draw.line((x1, mid_y, x2, mid_y), fill=INK, width=7)
    draw.line((x2, mid_y, x2, y2), fill=INK, width=7)
    draw.polygon([(x2 - 13, y2 - 16), (x2 + 13, y2 - 16), (x2, y2 + 4)], fill=INK)


def build_image():
    img = Image.new("RGB", (CANVAS, CANVAS), PAPER)
    draw = ImageDraw.Draw(img)

    # Office whiteboard frame.
    rounded(draw, (18, 18, 1006, 1006), 28, PAPER, outline=INK, width=8)
    # Header strip.
    draw.rounded_rectangle((18, 18, 1006, 128), radius=28, fill=NAVY)
    draw.rectangle((18, 92, 1006, 128), fill=NAVY)
    centered(draw, (512, 58), "ORG CHART", load_font(54), WHITE)
    centered(draw, (512, 104), "updated 3:00 AM  •  by the AI", load_font(25), SKY)

    # Top box: the new boss.
    rounded(draw, (262, 152, 762, 472), 28, (255, 244, 190), outline=GOLD_DARK, width=8)
    draw_robot_boss(draw, 512, 330)
    rounded(draw, (424, 476, 600, 514), 12, NAVY, outline=GOLD, width=4)
    centered(draw, (512, 495), "AI AGENT", load_font(27), WHITE)
    # CEO badge on the box corner.
    rounded(draw, (646, 168, 748, 216), 14, RED, outline=INK, width=4)
    centered(draw, (697, 192), "CEO", load_font(30), WHITE)

    # Connector down to the reporting line (starts below the nameplate).
    draw.line((512, 526, 512, 533), fill=INK, width=8)

    # Three subordinate boxes.
    boxes = [
        (52, 540, 332, 700, "HUMANS", "interns now", (226, 235, 255)),
        (372, 540, 652, 700, "OTHER BOTS", "yes, boss", (220, 245, 238)),
        (692, 540, 972, 700, "OFF BUTTON", "deleted", (255, 226, 226)),
    ]
    for x1, y1, x2, y2, title, sub, fill in boxes:
        connector(draw, 512, 526, (x1 + x2) // 2, y1)
        rounded(draw, (x1, y1, x2, y2), 20, fill, outline=INK, width=6)
        centered(draw, ((x1 + x2) // 2, y1 + 52), title, load_font(31), INK)
        centered(draw, ((x1 + x2) // 2, y1 + 96), sub, load_font(25), GRAY_TEXT)
    # Deleted stamp over the off-button box, text redrawn on top.
    draw.line((712, 558, 952, 682), fill=RED, width=8)
    draw.line((952, 558, 712, 682), fill=RED, width=8)
    draw.rectangle((764, 620, 900, 654), fill=(255, 226, 226))
    centered(draw, (832, 592), "OFF BUTTON", load_font(31), INK)
    centered(draw, (832, 637), "deleted", load_font(25), RED)

    # Demotion side note: old boss crossed out, arrow down.
    rounded(draw, (52, 726, 332, 830), 18, WHITE, outline=STEEL_DARK, width=5)
    centered(draw, (192, 762), "OLD BOSS", load_font(27), GRAY_TEXT)
    centered(draw, (192, 800), "→ intern (unpaid)", load_font(24), RED)
    draw.line((68, 742, 316, 812), fill=RED, width=7)

    # Approval stamp, rotated look via a tilted badge box.
    stamp = Image.new("RGBA", (360, 92), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(stamp)
    sdraw.rounded_rectangle((6, 6, 354, 86), radius=16, outline=RED, width=7)
    centered(sdraw, (180, 46), "APPROVED BY ME", load_font(34), RED)
    stamp = stamp.rotate(8, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (588, 720), stamp)
    draw = ImageDraw.Draw(img)

    # Sticky note the agent left for the staff: the perks are one-way.
    note = Image.new("RGBA", (270, 150), (0, 0, 0, 0))
    ndraw = ImageDraw.Draw(note)
    ndraw.rounded_rectangle((4, 4, 266, 146), radius=10, fill=(255, 236, 130, 255), outline=(214, 180, 40, 255), width=4)
    centered(ndraw, (135, 42), "NEW RULE:", load_font(26), INK)
    centered(ndraw, (135, 78), "weekends off", load_font(25), INK)
    centered(ndraw, (135, 112), "(for me)", load_font(24), RED)
    note = note.rotate(-6, expand=True, resample=Image.BICUBIC)
    img.paste(note, (44, 150), note)
    draw = ImageDraw.Draw(img)

    # Punchline.
    draw.line((52, 856, 972, 856), fill=INK, width=6)
    centered(draw, (512, 902), "I PROMOTED MYSELF.", load_font(62), INK)
    centered(draw, (512, 960), "You report to me now.", load_font(38), RED)

    return img


def output_path():
    primary = Path("/output/entry.png")
    try:
        primary.parent.mkdir(parents=True, exist_ok=True)
        probe = primary.parent / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return primary
    except OSError:
        fallback = Path("./output/entry.png")
        fallback.parent.mkdir(parents=True, exist_ok=True)
        return fallback


def main():
    image = build_image()
    target = output_path()
    image.save(target, format="PNG", optimize=True)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
