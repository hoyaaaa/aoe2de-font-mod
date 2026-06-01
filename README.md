# AoE2DE Font Mod — macOS

Replace in-game fonts in **Age of Empires II: Definitive Edition** on macOS (Steam native version).

**Translations:** [한국어](README.ko.md) · [中文](README.zh.md) · [日本語](README.ja.md)

![Before and After](assets/preview.png)

> **Left:** Original fonts (Trajan Pro) — Korean characters unsupported
> **Right:** After mod (조선100년체) — Korean fully rendered

---

## Requirements

- macOS (Apple Silicon or Intel)
- Age of Empires II: DE installed via Steam
- Python 3 (pre-installed on macOS)

---

## Usage

### Apply a font

```bash
./apply_font.sh /path/to/your/font.ttf
```

### Restore original fonts

```bash
./apply_font.sh restore
```

The first run will automatically create a virtual environment and install dependencies.

---

## How it works

AoE2DE uses a bitmap font atlas system for in-game text rendering. This tool:

1. Reads the original `combined.box` file to extract the required codepoints
2. Renders each glyph at 64px using the provided font via FreeType
3. Packs all glyphs into 2048×2048 texture pages
4. Writes new `combined.box`, `combined.txt`, and `combined_XXXX.DDS` files

Original files are backed up automatically on first run to `fonts_atlas_backup/`.

---

## Notes

- Only the in-game text atlas (`combined`) is replaced. The sans-serif atlas and UI icons are untouched.
- Game updates via Steam may overwrite the modified files. Re-run the script after updates.
- The `wpfg/fonts` folder has no effect on the macOS version of the game.

---

## License

MIT
