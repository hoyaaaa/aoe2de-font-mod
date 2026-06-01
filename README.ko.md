# AoE2DE 폰트 모드 — macOS

**Age of Empires II: Definitive Edition** macOS(Steam 네이티브)의 인게임 폰트를 교체하는 도구입니다.

**다른 언어:** [English](README.md) · [中文](README.zh.md) · [日本語](README.ja.md)

![Before and After](assets/preview.png)

> **왼쪽:** 원본 폰트 (Trajan Pro) — 한국어 미지원
> **오른쪽:** 모드 적용 후 (조선100년체) — 한국어 정상 표시

---

## 요구사항

- macOS (Apple Silicon 또는 Intel)
- Steam을 통해 설치된 Age of Empires II: DE
- Python 3 (macOS 기본 설치)

---

## 사용법

### 폰트 적용

```bash
./apply_font.sh /path/to/font.ttf
```

### 원본 복구

```bash
./apply_font.sh restore
```

첫 실행 시 가상환경을 자동으로 생성하고 의존성을 설치합니다.

---

## 작동 원리

AoE2DE는 인게임 텍스트 렌더링에 비트맵 폰트 아틀라스 시스템을 사용합니다. 이 도구는:

1. 원본 `combined.box` 파일에서 필요한 코드포인트 목록을 추출
2. FreeType을 통해 제공된 폰트로 64px 크기의 글리프를 렌더링
3. 모든 글리프를 2048×2048 텍스처 페이지에 패킹
4. 새로운 `combined.box`, `combined.txt`, `combined_XXXX.DDS` 파일 생성

첫 실행 시 원본 파일이 `fonts_atlas_backup/` 폴더에 자동 백업됩니다.

---

## 참고사항

- **게임 옵션에서 폰트 스타일을 세리프로 설정해야 합니다** (옵션 → 인터페이스 → 폰트 스타일). 이 모드는 세리프(`combined`) 아틀라스만 수정하므로, 산세리프로 설정하면 적용되지 않습니다.
- 인게임 텍스트 아틀라스(`combined`)만 교체됩니다. 산세리프 아틀라스와 UI 아이콘은 유지됩니다.
- Steam을 통한 게임 업데이트 시 수정된 파일이 덮어씌워질 수 있습니다. 업데이트 후 스크립트를 다시 실행하세요.
- `wpfg/fonts` 폴더는 macOS 버전에서 적용되지 않습니다.

---

## 라이선스

MIT
