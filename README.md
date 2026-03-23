# 🔥 옥외소화전 펌프 용량 계산서 PWA

> **Developer MANMIN** | 대성건축사사무소  
> Blueprint Engineering Theme · Ver 3.1

## 📦 파일 구성

```
pwa-project/
├── index.html          ← 메인 앱 (React 포함)
├── manifest.json       ← PWA 매니페스트
├── sw.js               ← 서비스 워커 (오프라인 지원)
├── README.md
└── icons/
    ├── favicon.ico
    ├── favicon-16.png
    ├── favicon-32.png
    ├── apple-touch-icon.png  ← iOS 홈 화면 아이콘
    ├── icon-72.png
    ├── icon-96.png
    ├── icon-128.png
    ├── icon-144.png
    ├── icon-152.png
    ├── icon-180.png
    ├── icon-192.png     ← Android 기본 아이콘
    ├── icon-384.png
    └── icon-512.png     ← Splash Screen / 마스커블
```

## 🚀 GitHub Pages 배포 방법

1. 이 폴더 전체를 GitHub 저장소에 업로드
2. `Settings` → `Pages` → `Source: main branch / root` 선택
3. 배포된 URL(예: `https://username.github.io/repo/`)로 접속
4. 브라우저 주소창 우측 **설치 아이콘(⊕)** 클릭 또는 하단 배너에서 **설치** 클릭

## 📱 PWA 설치 지원 환경

| 환경 | 설치 방법 |
|------|----------|
| Android Chrome | 하단 설치 배너 또는 메뉴 → "홈 화면에 추가" |
| iOS Safari | 공유 버튼 → "홈 화면에 추가" |
| Windows Chrome/Edge | 주소창 우측 설치 아이콘 |
| macOS Chrome | 주소창 우측 설치 아이콘 |

## ⚙️ 기술 스택

- **React 18** (UMD, CDN)
- **Service Worker** (오프라인 캐싱, 자동 업데이트)
- **Web App Manifest** (설치, 아이콘, 바로가기)
- **Hazen-Williams 공식** 기반 배관 마찰손실 계산
- **NFPC 109** (2026.3.1 시행) 기준 적용

## 📐 적용 법령

- 화재안전성능기준 NFPC 109 (소방청고시 제2025-25호)
- 시행: 2026. 3. 1.

---
*MANMIN · Blueprint Engineering Theme*
