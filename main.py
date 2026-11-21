"""Passport spread for the fictional Republic of Meridia.

Draws an open passport (data page + stamps page) at 1024x1024 and writes
it to /output/entry.png. Deterministic: no clock, no randomness, no network.
"""
import base64
import io
import os
from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
F_SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
F_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
F_MONO = os.path.join(FONT_DIR, "DejaVuSansMono.ttf")
F_OBLIQUE = os.path.join(FONT_DIR, "DejaVuSerif.ttf")

NAVY = (31, 58, 95)
INK = (28, 32, 40)
GREY = (110, 112, 116)
PAGE = (246, 241, 227)
CREAM = (250, 246, 236)
BG = (118, 123, 130)

PORTRAIT_B64 = """/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBAUEBAYFBQUGBgYHCQ4JCQgICRINDQoOFRIWFhUS
FBQXGiEcFxgfGRQUHScdHyIjJSUlFhwpLCgkKyEkJST/2wBDAQYGBgkICREJCREkGBQYJCQkJCQk
JCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCQkJCT/wAARCAHCAWgDASIA
AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA
AAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3
ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm
p6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA
AwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx
BhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK
U1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3
uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD2nNGa
KKACijNIaACjrS9qSgAoopaAEooooAdQRSZooAMUlFBoAUGjJpN3FJmgB2aSl60YoASkqC81C10+
Iy3E8caZxuY4FRR6xZzKjxTLIr/dKjg/SgC7mioWuoEfbJKqE9ATiqk+s2kd08BvIEaL7ylxuPHp
QBpcik6157qPxu8M6dcPbtNJK6HaQiE4P1rZ0D4kaF4hCrZTmR2/hKlSKVwOpzilznrUAuI5AZAw
IAHQ9zStcorbSy5x0BzimBLS4qJJg5ICnI7cZ/KpiMdaADNIaM0UAFKKTNANADqaRRmjNABijFFG
aADFFGaQUAKaSlNJQAUtGeKBQAUlLRigBM0UtFABmikooAWkpQaKADNFJ2pRQAnSlzSUYoAKKDS5
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
UUUABpKKKACl9KKKAHUUUUAf/9k="""


def font(path, size):
    return ImageFont.truetype(path, size)


def mrz_check(text):
    """ICAO MRZ check digit: weights 7,3,1; A=10..Z=35, '<'=0."""
    weights = (7, 3, 1)
    total = 0
    for i, ch in enumerate(text):
        if ch == "<":
            val = 0
        elif ch.isdigit():
            val = int(ch)
        else:
            val = ord(ch) - 55
        total += val * weights[i % 3]
    return str(total % 10)


def mrz_lines():
    line1 = "P<MDVOSS<<ELARA"
    line1 = line1 + "<" * (44 - len(line1))
    doc = "MD4829137"
    dob = "940312"
    exp = "340214"
    part = doc + mrz_check(doc) + "MER" + dob + mrz_check(dob) + "F" + exp + mrz_check(exp)
    optional = "<" * 14
    line2 = part + optional
    line2 = line2 + mrz_check(part + optional)
    line2 = line2 + "<" * (44 - len(line2))
    assert len(line1) == 44 and len(line2) == 44
    return line1, line2


def compass(draw, cx, cy, r, color, width=3):
    """Eight-point compass rose in a circle."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=width)
    draw.ellipse([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8],
                 outline=color, width=1)
    for k in range(8):
        import math
        ang = math.radians(k * 45)
        long = r - 4 if k % 2 == 0 else r - 14
        x2 = cx + long * math.sin(ang)
        y2 = cy - long * math.cos(ang)
        draw.line([cx, cy, x2, y2], fill=color, width=width if k % 2 == 0 else 2)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=color)


def stamp(base, cx, cy, w, h, lines, color, angle, size=20):
    """A rotated rubber-stamp box with centred lines of text."""
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=8,
                        outline=color + (230,), width=3)
    d.rounded_rectangle([26, 26, 14 + w, 14 + h], radius=6,
                        outline=color + (200,), width=1)
    f = font(F_BOLD, size)
    total = len(lines) * (size + 6)
    y = 20 + (h - total) // 2 + 3
    for line in lines:
        tw = d.textlength(line, font=f)
        d.text((20 + (w - tw) / 2, y), line, font=f, fill=color + (235,))
        y += size + 6
    layer = layer.rotate(angle, resample=Image.BICUBIC, expand=False)
    base.alpha_composite(layer, (int(cx - (w + 40) / 2), int(cy - (h + 40) / 2)))


def draw_spread():
    img = Image.new("RGB", (1024, 1024), BG)
    # soft radial lightening behind the passport
    glow = Image.new("RGB", (1024, 1024), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([80, 40, 944, 984], fill=(28, 28, 28))
    img = Image.blend(img, Image.new("RGB", (1024, 1024), (138, 142, 148)),
                      0.35)
    img = img.convert("RGBA")
    # drop shadows for the two pages
    shadow = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([70, 194, 512, 854], radius=6, fill=(0, 0, 0, 110))
    sd.rounded_rectangle([512, 194, 966, 854], radius=6, fill=(0, 0, 0, 110))
    from PIL import ImageFilter
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img.alpha_composite(shadow)

    d = ImageDraw.Draw(img)
    # pages
    d.rounded_rectangle([58, 182, 500, 842], radius=6, fill=PAGE + (255,))
    d.rounded_rectangle([524, 182, 966, 842], radius=6, fill=PAGE + (255,))
    d.line([512, 182, 512, 842], fill=(120, 110, 90, 255), width=3)

    # ---------- left page: data page ----------
    compass(d, 279, 252, 34, NAVY)
    f_title = font(F_BOLD, 26)
    t = "REPUBLIC OF MERIDIA"
    d.text((279 - d.textlength(t, font=f_title) / 2, 296), t, font=f_title,
           fill=NAVY)
    f_sub = font(F_BOLD, 20)
    t = "P A S S P O R T"
    d.text((279 - d.textlength(t, font=f_sub) / 2, 330), t, font=f_sub,
           fill=NAVY)
    d.line([88, 362, 470, 362], fill=NAVY, width=2)

    # portrait
    portrait = Image.open(io.BytesIO(base64.b64decode(PORTRAIT_B64)))
    portrait = portrait.resize((170, 213), Image.LANCZOS)
    img.paste(portrait, (88, 380))
    d.rectangle([88, 380, 258, 593], outline=INK, width=2)

    # data fields right of the portrait
    f_label = font(F_SANS, 12)
    f_val = font(F_BOLD, 17)
    fields = [
        ("SURNAME", "VOSS"),
        ("GIVEN NAMES", "ELARA"),
        ("DATE OF BIRTH", "12 MAR 1994"),
        ("PLACE OF BIRTH", "MERIDIA CITY"),
        ("SEX", "F"),
        ("NATIONALITY", "MERIDIAN"),
    ]
    y = 384
    for label, value in fields:
        d.text((276, y), label, font=f_label, fill=GREY)
        d.text((276, y + 15), value, font=f_val, fill=INK)
        y += 36

    # document details, two columns under the photo
    y = 606
    left_col = [
        ("PASSPORT No.", "MD-4829137"),
        ("DATE OF ISSUE", "14 FEB 2024"),
    ]
    right_col = [
        ("DATE OF EXPIRY", "14 FEB 2034"),
        ("AUTHORITY", "PASSPORT OFFICE"),
    ]
    for (l1, v1), (l2, v2) in zip(left_col, right_col):
        d.text((88, y), l1, font=f_label, fill=GREY)
        d.text((88, y + 15), v1, font=f_val, fill=INK)
        d.text((290, y), l2, font=f_label, fill=GREY)
        d.text((290, y + 15), v2, font=f_val, fill=INK)
        y += 36

    # signature
    d.line([88, 700, 258, 700], fill=INK, width=1)
    d.text((88, 708), "SIGNATURE OF HOLDER", font=f_label, fill=GREY)
    f_sig = font(F_OBLIQUE, 20)
    d.text((88, 678), "Elara Voss", font=f_sig, fill=(40, 48, 90))

    # machine-readable zone
    line1, line2 = mrz_lines()
    f_mrz = font(F_MONO, 15)
    d.text((88, 742), line1, font=f_mrz, fill=INK)
    d.text((88, 764), line2, font=f_mrz, fill=INK)
    d.text((88, 812), "PAGE 1", font=f_label, fill=GREY)

    # ---------- right page: stamps ----------
    f_head = font(F_BOLD, 19)
    t = "VISAS AND ENDORSEMENTS"
    d.text((745 - d.textlength(t, font=f_head) / 2, 206), t, font=f_head,
           fill=NAVY)
    d.line([554, 236, 936, 236], fill=NAVY, width=2)
    # faint compass watermark
    wm = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wm)
    compass(wd, 745, 512, 150, NAVY + (26,), width=4)
    img.alpha_composite(wm)

    stamp(img, 745, 330, 300, 104,
          ["PORT OF CALLAIS", "ARRIVED", "03 JUN 2024"],
          (37, 64, 143), -7)
    stamp(img, 745, 472, 300, 104,
          ["THALASSA", "DEPARTED", "18 SEP 2025"],
          (156, 47, 38), 5)
    stamp(img, 745, 614, 300, 104,
          ["MERIDIA HARBOUR", "ARRIVED", "02 MAR 2026"],
          (90, 58, 125), -4)
    stamp(img, 745, 742, 300, 62,
          ["SEAFARER'S LEVY — PAID", "MERIDIA HARBOUR AUTHORITY"],
          (46, 107, 56), 3, size=16)

    d = ImageDraw.Draw(img)
    f_note = font(F_SANS, 14)
    t = "HOLDER MUST GREET THE HARBOURMASTER ON ARRIVAL"
    d.text((745 - d.textlength(t, font=f_note) / 2, 800), t, font=f_note,
           fill=INK)
    d.text((906, 822), "PAGE 2", font=f_label, fill=GREY)

    return img.convert("RGB")


def main():
    out = draw_spread()
    os.makedirs("/output", exist_ok=True)
    out.save("/output/entry.png", optimize=True)


if __name__ == "__main__":
    main()
