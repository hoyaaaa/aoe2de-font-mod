#!/bin/bash
# AoE2DE 인게임 폰트 교체 스크립트
# 사용법: ./apply_font.sh /path/to/font.ttf
# 원복:   ./apply_font.sh restore

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/.venv"

# venv 없으면 생성
if [ ! -d "$VENV" ]; then
    echo "Setting up Python environment..."
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install --quiet Pillow freetype-py
    echo "Done."
fi

"$VENV/bin/python3" "$SCRIPT_DIR/apply_font.py" "$1"
