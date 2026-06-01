#!/usr/bin/env python3
"""
AoE2DE Font Atlas Generator - macOS
Usage:
  python3 apply_font.py /path/to/font.ttf   # apply font
  python3 apply_font.py restore              # restore original
"""
import struct, os, sys, shutil
import freetype
from PIL import Image

# ── Config ───────────────────────────────────────────────────────────────────
ATLAS_SIZE  = 2048
PIXEL_SIZE  = 64
PADDING     = 2

# ── Auto-detect AoE2DE path ──────────────────────────────────────────────────
def find_fonts_dir():
    base = os.path.expanduser(
        "~/Library/Application Support/Steam/steamapps/common/AoE2DE"
        "/AgeOfEmpires2Data/resources/_common/fonts"
    )
    if os.path.isdir(base):
        return base
    raise FileNotFoundError(
        "AoE2DE not found. Make sure the game is installed via Steam."
    )

# ── Box format ────────────────────────────────────────────────────────────────
# Header : version(i4) numGlyphs(i4) numPages(i4) pixelSize(f4)  = 16 bytes
# Entries: W H U S V T Atlas X0 Y0 HAdv                          = 40 bytes
# Index  : [codepoint(u2) glyphIndex(u2)] * numGlyphs            = 4 bytes each
HDR   = '<iiif'
GLYPH = '<ffffffifff'
IDX   = '<HH'

def read_box(path):
    with open(path, 'rb') as f:
        data = f.read()
    ver, n, pages, pxsz = struct.unpack_from(HDR, data, 0)
    entries = [struct.unpack_from(GLYPH, data, 16 + i * 40) for i in range(n)]
    idx_off = 16 + n * 40
    index = [struct.unpack_from(IDX, data, idx_off + i * 4) for i in range(n)]
    return entries, index

def render_glyph(face, cp):
    try:
        face.load_char(cp, freetype.FT_LOAD_RENDER)
        g = face.glyph
        bm = g.bitmap
        w, h = bm.width, bm.rows
        x0 = float(g.bitmap_left)
        y0 = float(g.bitmap_top - h)
        hadv = g.advance.x / 64.0
        img = Image.frombytes('L', (w, h), bytes(bm.buffer)) if w > 0 and h > 0 else None
        return img, w, h, x0, y0, hadv
    except Exception:
        return None, 0, 0, 0.0, 0.0, 0.0

def pack(glyph_list, atlas_size, pad):
    pages = [Image.new('RGB', (atlas_size, atlas_size), (0, 0, 0))]
    place = {}
    sx, sy, sh, pg = pad, pad, 0, 0
    for idx, (img, w, h, *_) in enumerate(glyph_list):
        gw, gh = max(w, 1) + pad, max(h, 1) + pad
        if sx + gw > atlas_size:
            sy += sh + pad
            sx, sh = pad, 0
        if sy + gh > atlas_size:
            pages.append(Image.new('RGB', (atlas_size, atlas_size), (0, 0, 0)))
            pg += 1
            sx, sy, sh = pad, pad, 0
        if img and w > 0 and h > 0:
            pages[pg].paste(img.convert('RGB'), (sx, sy))
        place[idx] = (pg, sx, sy)
        sx += gw
        sh = max(sh, gh)
    return pages, place

def write_dds(img, path):
    base_w, base_h = img.size
    mips, cur = [], img.convert('RGBA')
    w, h = base_w, base_h
    while True:
        r, g, b, a = cur.split()
        mips.append(Image.merge('RGBA', (b, g, r, a)).tobytes())
        if w == 1 and h == 1:
            break
        w, h = max(1, w // 2), max(1, h // 2)
        cur = cur.resize((w, h), Image.LANCZOS)
    ddpf = struct.pack('<II4sIIIII', 32, 0x41, b'\x00\x00\x00\x00', 32,
                       0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    hdr = struct.pack('<IIIIIII', 124, 0x2100f, base_h, base_w, base_w * 4, 1, len(mips))
    hdr += b'\x00' * 44 + ddpf + struct.pack('<IIIII', 0x401008, 0, 0, 0, 0) + b'\x00' * 4
    with open(path, 'wb') as f:
        f.write(b'DDS ' + hdr)
        for m in mips:
            f.write(m)

def apply_font(font_path, fonts_dir):
    box_path = os.path.join(fonts_dir, "combined.box")
    backup   = os.path.join(fonts_dir, "..", "fonts_atlas_backup")

    print(f"Font: {os.path.basename(font_path)}")
    print("Reading codepoints …")
    _, orig_index = read_box(box_path)
    codepoints = sorted({cp for cp, _ in orig_index})

    face = freetype.Face(font_path)
    face.set_pixel_sizes(0, PIXEL_SIZE)

    print(f"Rendering {len(codepoints)} glyphs …")
    glyph_data = [render_glyph(face, cp) for cp in codepoints]

    print("Packing atlas …")
    pages, place = pack(glyph_data, ATLAS_SIZE, PADDING)
    print(f"  {len(pages)} pages")

    # Backup originals (first time only)
    if not os.path.isdir(backup):
        print("Backing up originals …")
        os.makedirs(backup)
        for f in os.listdir(fonts_dir):
            if f.startswith("combined") and not f.startswith("combined_sansserif"):
                shutil.copy2(os.path.join(fonts_dir, f), os.path.join(backup, f))

    # Write .box
    entries_out, index_out = [], []
    for gi, (cp, gd, (pg, px, py)) in enumerate(
            zip(codepoints, glyph_data, [place[i] for i in range(len(codepoints))])):
        img, w, h, x0, y0, hadv = gd
        aw, ah = max(w, 1), max(h, 1)
        entries_out.append((float(w), float(h),
                            px/ATLAS_SIZE, (px+aw)/ATLAS_SIZE,
                            py/ATLAS_SIZE, (py+ah)/ATLAS_SIZE,
                            pg, x0, y0, hadv))
        index_out.append((cp & 0xFFFF, gi))

    with open(os.path.join(fonts_dir, "combined.box"), 'wb') as f:
        f.write(struct.pack(HDR, 2, len(entries_out), len(pages), float(PIXEL_SIZE)))
        for e in entries_out:
            f.write(struct.pack(GLYPH, *e))
        for ie in index_out:
            f.write(struct.pack(IDX, *ie))

    # Write .txt
    with open(os.path.join(fonts_dir, "combined.txt"), 'w', encoding='utf-8') as f:
        f.write(f"Font File Atlas Summary\n-----------------------\n"
                f"Version : 2\nGlyphs : {len(entries_out)}\n"
                f"Texture Pages : {len(pages)}\nSource Font Pixel Size : {PIXEL_SIZE}\n"
                f"-----------------------\n\n")
        for cp, e in zip(codepoints, entries_out):
            w, h, U, S, V, T, pg, x0, y0, hadv = e
            label = f"'{chr(cp)}'" if 32 <= cp <= 126 else str(cp)
            f.write(f"Glyph - {label}    W({int(w)}), H({int(h)}), "
                    f"UV({U:.6f}, {V:.6f}), ST({S:.6f}, {T:.6f}), "
                    f"Atlas({pg}), XO({x0:.5f}), YO({y0:.5f}), HAdvance({hadv:.4f})\n")

    # Remove old combined pages, write new
    for fn in os.listdir(fonts_dir):
        if fn.startswith("combined_0") and (fn.endswith(".DDS") or fn.endswith(".png")):
            os.remove(os.path.join(fonts_dir, fn))

    for i, pg_img in enumerate(pages):
        pg_img.save(os.path.join(fonts_dir, f"combined_{i:04d}.png"))
        write_dds(pg_img, os.path.join(fonts_dir, f"combined_{i:04d}.DDS"))
        print(f"  Page {i} written")

    print("Done! Restart AoE2DE to apply.")

def restore(fonts_dir):
    backup = os.path.join(fonts_dir, "..", "fonts_atlas_backup")
    if not os.path.isdir(backup):
        print("No backup found.")
        return
    print("Restoring …")
    for fn in os.listdir(fonts_dir):
        if fn.startswith("combined_0") and (fn.endswith(".DDS") or fn.endswith(".png")):
            os.remove(os.path.join(fonts_dir, fn))
    for fn in os.listdir(backup):
        shutil.copy2(os.path.join(backup, fn), os.path.join(fonts_dir, fn))
    print("✓ Restored.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    fonts_dir = find_fonts_dir()
    if sys.argv[1] == "restore":
        restore(fonts_dir)
    else:
        if not os.path.isfile(sys.argv[1]):
            print(f"File not found: {sys.argv[1]}")
            sys.exit(1)
        apply_font(sys.argv[1], fonts_dir)
