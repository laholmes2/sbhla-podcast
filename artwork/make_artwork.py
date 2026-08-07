#!/usr/bin/env python3
"""Compose podcast cover art (3000x3000) from SBHLA's real logo.

SBHLA's site only hosts a 256x256 version of their logo -- too small on its
own to meet Apple Podcasts' minimum artwork size (1400x1400). Rather than
upscaling/blurring it to fill the frame, this places the logo at its native
detail in the center of a clean parchment-style canvas, matching the site's
serif/black-on-white look.

Usage:
    python3 artwork/make_artwork.py \
        --title-line1 "PASTOR'S CONFERENCE" --title-line2 "AUDIO RECORDINGS" \
        --out ../artwork.jpg
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CANVAS_SIZE = 3000
BG_COLOR = (244, 239, 227)       # warm parchment
INK_COLOR = (35, 30, 26)         # near-black ink
RULE_COLOR = (92, 26, 27)        # deep maroon accent

SRC_LOGO = Path(__file__).parent / "sbhla_logo_source.png"

FONT_BOLD = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Georgia.ttf"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title-line1", default="PASTOR'S CONFERENCE")
    parser.add_argument("--title-line2", default="AUDIO RECORDINGS")
    parser.add_argument("--out", default=str(Path(__file__).parent.parent / "artwork.jpg"))
    args = parser.parse_args()
    out_path = Path(args.out)

    canvas = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    # Thin double border for an archival-plate feel.
    margin = 90
    draw.rectangle(
        [margin, margin, CANVAS_SIZE - margin, CANVAS_SIZE - margin],
        outline=RULE_COLOR,
        width=6,
    )
    margin2 = margin + 30
    draw.rectangle(
        [margin2, margin2, CANVAS_SIZE - margin2, CANVAS_SIZE - margin2],
        outline=RULE_COLOR,
        width=2,
    )

    # Logo, upscaled modestly (not stretched to fill the frame) and centered
    # in the upper portion, leaving room for title text below.
    logo = Image.open(SRC_LOGO).convert("RGBA")
    logo_size = 1150
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    logo_x = (CANVAS_SIZE - logo_size) // 2
    logo_y = 420
    canvas.paste(logo, (logo_x, logo_y), logo)

    # Title block below the logo.
    title_font = ImageFont.truetype(FONT_BOLD, 150)
    subtitle_font = ImageFont.truetype(FONT_REG, 80)
    footer_font = ImageFont.truetype(FONT_REG, 60)

    def centered_text(y, text, font, fill):
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        draw.text(((CANVAS_SIZE - w) / 2, y), text, font=font, fill=fill)

    centered_text(1750, args.title_line1, title_font, INK_COLOR)
    centered_text(1950, args.title_line2, title_font, INK_COLOR)

    rule_y = 2160
    draw.line([(900, rule_y), (2100, rule_y)], fill=RULE_COLOR, width=4)

    centered_text(2230, "Southern Baptist Historical Library & Archives", subtitle_font, INK_COLOR)
    centered_text(2600, "personal listening archive — not an official SBHLA production", footer_font, (110, 100, 88))

    canvas.save(out_path, "JPEG", quality=92)
    print(f"Wrote {out_path} ({canvas.size[0]}x{canvas.size[1]})")


if __name__ == "__main__":
    main()
