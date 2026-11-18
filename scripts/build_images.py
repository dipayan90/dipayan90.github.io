#!/usr/bin/env python3
"""Dev-time image build. Needs Pillow installed locally; Pillow is not a Pipfile dependency.

Writes responsive portrait derivatives to docs/assets/img/ and the static OG card.
Run: python scripts/build_images.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets-src" / "profile.JPG"
OUT_DIR = ROOT / "docs" / "assets" / "img"
OG_CARD = ROOT / "docs" / "assets" / "og-card.png"
WIDTHS = (320, 560, 800)
WEBP_BUDGET = {560: 80 * 1024}
OG_SIZE = (1200, 630)

PAPER = "#f6efe2"
INK = "#191411"
ACCENT = "#a43d1c"
NAME = "Dipayan Chattopadhyay"
ROLE = "Software Development Manager at AWS"
SITE = "dipayan90.github.io"
FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
)
BOLD_FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
)


def load_font(size, bold=False):
    for path in BOLD_FONT_CANDIDATES if bold else FONT_CANDIDATES:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def fit_font(draw, text, max_width, start, bold=False):
    size = start
    while size > 10:
        face = load_font(size, bold)
        if draw.textlength(text, font=face) <= max_width:
            return face
        size -= 2
    return load_font(size, bold)


def save_webp(image, path, budget=None):
    for quality in range(96, 29, -2):
        image.save(path, "WEBP", quality=quality, method=6)
        if budget is None or path.stat().st_size <= budget:
            return quality
    raise SystemExit("%s exceeds its %d byte budget" % (path, budget))


def build_portraits():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCE) as source:
        source = source.convert("RGB")
        for width in WIDTHS:
            height = round(source.height * width / source.width)
            resized = source.resize((width, height), Image.LANCZOS)
            quality = save_webp(resized, OUT_DIR / ("portrait-%d.webp" % width),
                                WEBP_BUDGET.get(width))
            resized.save(OUT_DIR / ("portrait-%d.jpg" % width), "JPEG",
                         quality=82, optimize=True, progressive=True)
            print("portrait-%d: %dx%d webp q%d, jpg q82" % (width, width, height, quality))


def build_og_card():
    def wrap(draw, text, face, max_width):
        words, lines, line = text.split(), [], ""
        for word in words:
            candidate = (line + " " + word).strip()
            if draw.textlength(candidate, font=face) <= max_width or not line:
                line = candidate
            else:
                lines.append(line)
                line = word
        return lines + [line]

    card = Image.new("RGB", OG_SIZE, PAPER)
    draw = ImageDraw.Draw(card)
    margin = 96
    inner = OG_SIZE[0] - 2 * margin

    draw.rectangle((margin, 150, margin + 96, 156), fill=ACCENT)
    name_face = fit_font(draw, NAME, inner, 96, bold=True)
    draw.text((margin, 190), NAME, font=name_face, fill=INK)
    role_face = load_font(42)
    y = 190 + int(name_face.size * 1.15)
    for line in wrap(draw, ROLE, role_face, inner):
        draw.text((margin, y), line, font=role_face, fill=ACCENT)
        y += int(role_face.size * 1.35)
    site_face = load_font(26)
    draw.text((margin, OG_SIZE[1] - margin - site_face.size), SITE, font=site_face, fill=INK)
    card.save(OG_CARD, "PNG", optimize=True)
    print("og-card: %dx%d, %d bytes" % (OG_SIZE[0], OG_SIZE[1], OG_CARD.stat().st_size))


def main():
    build_portraits()
    build_og_card()


if __name__ == "__main__":
    main()
