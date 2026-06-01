# AoE2DE 字体模组 — macOS

替换 **Age of Empires II: Definitive Edition** macOS（Steam 原生版本）中的游戏内字体。

**其他语言：** [English](README.md) · [한국어](README.ko.md) · [日本語](README.ja.md)

![修改前后对比](assets/preview.png)

> **左：** 原始字体（Trajan Pro）— 不支持韩文
> **右：** 修改后（조선100년체）— 韩文正常显示

---

## 系统要求

- macOS（Apple Silicon 或 Intel）
- 通过 Steam 安装的 Age of Empires II: DE
- Python 3（macOS 预装）

---

## 使用方法

### 应用字体

```bash
./apply_font.sh /path/to/font.ttf
```

### 还原原始字体

```bash
./apply_font.sh restore
```

首次运行时会自动创建虚拟环境并安装依赖。

---

## 工作原理

AoE2DE 使用位图字体图集系统渲染游戏内文字。本工具将：

1. 读取原始 `combined.box` 文件以提取所需字符编码点
2. 通过 FreeType 以 64px 大小渲染指定字体的每个字形
3. 将所有字形打包至 2048×2048 纹理页
4. 生成新的 `combined.box`、`combined.txt` 和 `combined_XXXX.DDS` 文件

首次运行时，原始文件会自动备份至 `fonts_atlas_backup/` 目录。

---

## 注意事项

- **游戏选项中的字体样式必须设置为衬线体**（选项 → 界面 → 字体样式）。本模组仅修改衬线体（`combined`）图集，切换为无衬线体后将不会生效。
- 仅替换游戏内文字图集（`combined`），无衬线图集和 UI 图标保持不变。
- Steam 游戏更新可能会覆盖修改后的文件，更新后请重新运行脚本。
- `wpfg/fonts` 文件夹对 macOS 版本无效。

---

## 许可证

MIT
