#!/usr/bin/env python3
"""
Generate a before/after comparison image for README.
Usage:
  python3 generate_preview.py /path/to/mod_font.ttf
  python3 generate_preview.py /path/to/mod_font.ttf --output assets/preview.png
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1100, 620

BG_DARK     = (18, 12, 6)
PANEL_BG    = (32, 22, 10)
BORDER      = (90, 65, 25)
GOLD        = (210, 165, 60)
GOLD_DIM    = (140, 105, 35)
WHITE       = (235, 220, 190)
DIM_TEXT    = (120, 100, 65)
RED_LABEL   = (180, 60, 40)
GREEN_LABEL = (60, 150, 70)

SAMPLES = [
    ('CIVILIZATION',                  '문명 선택',                      28, GOLD),
    ('Holy Roman Empire',             '신성 로마 제국',                  34, WHITE),
    ('UNITS',                         '유닛',                           20, GOLD_DIM),
    ('Knight  ·  Archer  ·  Trebuchet','기사단  ·  궁수  ·  트레뷰셋',   22, WHITE),
    ('BUILDINGS',                     '건물',                           20, GOLD_DIM),
    ('Castle  ·  Town Center  ·  Monastery','성  ·  마을 회관  ·  수도원',22, WHITE),
    ('TECHNOLOGIES',                  '기술',                           20, GOLD_DIM),
    ('Bloodlines  ·  Plate Mail Armor','혈통  ·  판금 갑옷',             22, WHITE),
    ('1453 — Fall of Constantinople', '1453 — 콘스탄티노폴리스의 함락',   18, DIM_TEXT),
]

def find_original_fonts():
    wpfg = os.path.expanduser(
        "~/Library/Application Support/Steam/steamapps/common/AoE2DE"
        "/AgeOfEmpires2Data/resources/_common/wpfg/fonts"
    )
    en = os.path.join(wpfg, "TrajanPro-Regular.ttf")
    ko = os.path.join(wpfg, "MalgunGothic.ttf")
    return (en if os.path.isfile(en) else None,
            ko if os.path.isfile(ko) else None)

def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_panel(draw, x, y, w, h, title, title_color):
    draw.rectangle([x, y, x+w, y+h], fill=PANEL_BG)
    for i in range(3):
        c = tuple(max(0, BORDER[j] - i*15) for j in range(3))
        draw.rectangle([x+i, y+i, x+w-i, y+h-i], outline=c)
    draw.rectangle([x+3, y+3, x+w-3, y+36], fill=(50, 35, 12))
    draw.line([x+3, y+36, x+w-3, y+36], fill=BORDER, width=2)
    draw.text((x+14, y+10), title, fill=title_color,
              font=ImageFont.load_default())

def generate(mod_font_path, output_path):
    orig_en, orig_ko = find_original_fonts()

    img  = Image.new('RGB', (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    draw_panel(draw, 20,  20, 520, 580,
               '◀  BEFORE  —  Trajan Pro + MalgunGothic', RED_LABEL)
    draw_panel(draw, 560, 20, 520, 580,
               f'▶  AFTER  —  {os.path.splitext(os.path.basename(mod_font_path))[0]}',
               GREEN_LABEL)
    draw.line([(543, 20),(543, 600)], fill=BORDER, width=2)

    y_off = 55
    for en, ko, size, color in SAMPLES:
        # BEFORE — English: TrajanPro, Korean: MalgunGothic
        f_en = load(orig_en, size) if orig_en else ImageFont.load_default()
        f_ko = load(orig_ko, size) if orig_ko else ImageFont.load_default()
        draw.text((34, 20 + y_off), en, fill=color, font=f_en)
        draw.text((34, 20 + y_off + size + 2), ko,
                  fill=tuple(c // 2 for c in color), font=f_ko)

        # AFTER — both English and Korean
        f_mod = load(mod_font_path, size)
        draw.text((574, 20 + y_off), en, fill=color, font=f_mod)
        draw.text((574, 20 + y_off + size + 2), ko, fill=color, font=f_mod)

        y_off += size * 2 + 18

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    out  = "assets/preview.png"
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        out = sys.argv[idx + 1]

    if not args:
        print(__doc__)
        sys.exit(1)

    if not os.path.isfile(args[0]):
        print(f"File not found: {args[0]}")
        sys.exit(1)

    generate(args[0], out)
