# Social share images (1200x630) for link previews on Facebook, Pinterest, X, etc.
# build.py calls make_card() for every live article and the site default.
# Fonts are vendored in _src/fonts so every run renders identical images.
import os, html, re

W, H = 1200, 630
INK, GOLD, SOFT, MUTED = (42, 27, 45), (201, 164, 106), (251, 247, 241), (190, 176, 192)
HERE = os.path.dirname(os.path.abspath(__file__))
SERIF = os.path.join(HERE, "fonts", "cormorant-garamond-latin-700-normal.woff")
SERIF_LOGO = os.path.join(HERE, "fonts", "cormorant-garamond-latin-600-normal.woff")
SANS = os.path.join(HERE, "fonts", "Inter-SemiBold.otf")


def _wrap(draw, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _crown(d, x, y, s, color):
    # small crown mark, s = width in px
    k = s / 36.0
    pts = [(0, 28), (3, 6), (11, 16), (18, 0), (25, 16), (33, 6), (36, 28)]
    d.line([(x + px * k, y + py * k) for px, py in pts] + [(x, y + 28 * k)], fill=color, width=max(2, int(3 * k)), joint="curve")
    d.line([(x, y + 34 * k), (x + 36 * k, y + 34 * k)], fill=color, width=max(2, int(3 * k)))


def make_card(out, title, eyebrow="", footer="parvaregina.com  ·  Longevity science for women 35+"):
    """Render one card to `out` (PNG). Returns True if written, False if Pillow is missing."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    title = html.unescape(re.sub(r"<[^>]+>", "", title))
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    d.rectangle([24, 24, W - 25, H - 25], outline=(84, 62, 88), width=2)   # fine inner frame
    x, maxw = 90, W - 180
    _crown(d, x, 66, 40, GOLD)
    logo = ImageFont.truetype(SERIF_LOGO, 44)
    d.text((x + 56, 62), "Parva Regina", font=logo, fill=SOFT)
    sans = ImageFont.truetype(SANS, 24)
    if eyebrow:
        d.text((x + 56 + d.textlength("Parva Regina", font=logo) + 24, 78), "/  " + eyebrow.upper(), font=sans, fill=GOLD)
    for size in (84, 76, 68, 60, 54, 48):
        f = ImageFont.truetype(SERIF, size)
        lines = _wrap(d, title, f, maxw)
        lh = int(size * 1.12)
        if len(lines) <= 4 and lh * len(lines) <= 320:
            break
    block = lh * len(lines)
    y = 160 + (320 - block) // 2
    for ln in lines:
        d.text((x, y), ln, font=f, fill=(255, 255, 255))
        y += lh
    d.line([x, H - 118, x + 120, H - 118], fill=GOLD, width=3)
    d.text((x, H - 96), footer, font=ImageFont.truetype(SANS, 26), fill=MUTED)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out, "PNG", optimize=True)
    return True
