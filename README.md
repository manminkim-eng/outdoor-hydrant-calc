# 🟢 옥외소화전 펌프 용량 계산서 PWA — Ver 3.2

> **Developer MANMIN** | 대성건축사사무소  
> Blueprint Engineering Theme · **재설치 문제 원천 차단 버전**

---

## 🆕 Ver 3.2 — 재설치 문제 완전 해결

### Ver 3.2 개선 목록

| 위치 | 개선 내용 |
|------|----------|
| **sw.js** | `CACHE_VER = 'v3.2'` — 캐시 버전 명시적 구분 |
| **sw.js INSTALL** | `skipWaiting()` 즉시 호출 → 대기 SW 없이 바로 활성화 |
| **sw.js ACTIVATE** | 현재 버전 외 **모든 이전 캐시 전부 삭제** |
| **sw.js ACTIVATE** | `clients.claim()` → 열린 탭 즉시 새 SW 적용 |
| **sw.js MESSAGE** | `CLEAR_CACHE` 명령 추가 — 긴급 초기화 가능 |
| **index.html SW** | 등록 시 `reg.waiting` 감지 → 즉시 `SKIP_WAITING` 전송 |
| **index.html SW** | `appinstalled` 이벤트 → `sessionStorage` 설치 플래그 기록 |
| **index.html SW** | `CACHE_CLEARED` 수신 시 자동 새로고침 |
| **index.html SW** | `window.clearPwaCache()` 긴급 함수 노출 |
| **index.html React** | `beforeinstallprompt` 시 세션플래그 초기화 |
| **index.html React** | 설치 완료 시 `sessionStorage` 기록 |

---

## 📦 파일 구성

```
outdoor-hydrant-v32/
├── index.html          ← 메인 앱 (React 포함, Ver 3.2)
├── manifest.json       ← PWA 매니페스트
├── sw.js               ← 서비스 워커 (Ver 3.2 — 재설치 문제 해결)
├── README.md
└── icons/              ← 아이콘 13종
```

## 🚀 GitHub Pages 배포

1. 저장소 루트에 전체 업로드
2. `Settings → Pages → main / (root)`
3. **HTTPS URL** 접속 → **📲 앱 설치** FAB 클릭

## 🛠️ 재설치 문제 발생 시 긴급 해결

브라우저 콘솔(`F12`)에서:
```javascript
clearPwaCache()
```

## 다음 버전 배포 시
```javascript
const CACHE_VER = 'v3.3';  // sw.js 한 줄만 변경
```

---
*MANMIN · Ver 3.2 · NFPC 109 (소방청고시 제2025-25호, 시행 2026.3.1.)*
