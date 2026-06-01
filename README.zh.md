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

- 仅替换游戏内文字图集（`combined`），无衬线图集和 UI 图标保持不变。
- Steam 游戏更新可能会覆盖修改后的文件，更新后请重新运行脚本。
- `wpfg/fonts` 文件夹对 macOS 版本无效。

---

## 推荐字体

支持所有 TTF/OTF 格式字体。

| 字体 | 风格 | 下载 |
|---|---|---|
| 조선100년체 (朝鲜百年体) | 经典韩式衬线 | [chosun.com](https://fontdown.chosun.com/100/ChosunCentennial_ttf.zip) |
| 덕온공주체 (德温公主体) | 朝鲜宫廷书法 | [hangeul.go.kr](https://hanfont.hangeul.go.kr/fonts/DeogonPrincess_TTF.zip) |
| EBS 훈민정음체 | 木版活字风格 | [ebs.co.kr](https://about.ebs.co.kr/kor/organization/font?tabVal=hunmin) |
| Sam3KRFont (三国志3) | 复古像素 | [GitHub](https://github.com/hurss/fonts) |

---

## 许可证

MIT
