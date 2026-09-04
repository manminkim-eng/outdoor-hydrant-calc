/* ═══════════════════════════════════════════════════════════════
   S9 회차 2026-09-05 — R28 JPG v5.5 소제목 동반 이관 동반 캐시명 v5.0.6
   S4 회차 2026-09-04 — R1b #mm-print-stamp 인쇄 비표시 동반 캐시명 v5.0.5
   S3-0 회차 2026-09-04 — R27 html2canvas 클론 정화 동반 캐시명 v5.0.4
   S2 회차 2026-09-04 — index 소급(R1·R21·R26 등) 동반 캐시명 v5.0.3
   R25 회차 2026-09-04 — 자기 접두어 캐시 조회 · cors 프리캐시 · opaque 가드 · 캐시명 v5.0.2 (S10)
   Service Worker — 옥외소화전 펌프 용량 계산서
   Developer MANMIN · Ver-5.0

   ▣ Ver 3.2 핵심 개선 — 재설치 문제 원천 차단
   ① INSTALL  : skipWaiting() 즉시 호출 → 대기 없이 바로 활성화
   ② ACTIVATE : 현재 버전 외 모든 캐시 전부 삭제
                clients.claim() → 열린 탭 즉시 새 SW 적용
   ③ FETCH    : Network-First (오프라인 폴백)
   ④ MESSAGE  : SKIP_WAITING / CLEAR_CACHE 모두 처리
═══════════════════════════════════════════════════════════════ */

/* §17-1 (2026-09-02) — 도구 고유 접두어. 종전 필터는 같은 origin 의 39종 캐시를 전부 지웠다 */
const PREFIX       = 'manmin-outdoor-hydrant-';
/* ═ R25 (2026-09-04) — SW 캐시 origin 오염 차단 (S10 · 지시서 §21-1 R25)
   전역 caches 의 match 는 origin 전체를 검색한다. manminkim-eng.github.io 는 34종이 한 origin 이라
   다른 도구 캐시의 opaque 응답이 <script crossorigin>(cors) 요청에 돌아가 스크립트가 폐기됐다
   (30 #root 빈 화면 · 40 html2canvas undefined). 자기 접두어 캐시만 조회하고, cross-origin
   프리캐시는 cors 로 받으며, opaque↔cors 불일치 시 캐시를 쓰지 않는다. */
const MM_EXCLUDE = [];   /* 내 접두어로 시작하지만 남의 캐시인 이름 (§17-1 충돌) */
const mmOwn   = (k) => k.indexOf(PREFIX) === 0 && !MM_EXCLUDE.some((x) => k.indexOf(x) === 0);
const mmReq   = (u) => (typeof u === 'string' && u.indexOf('http') === 0) ? new Request(u, { mode: 'cors' }) : u;
const mmMatch = (req, opt) => caches.keys()
  .then((ks) => ks.filter(mmOwn))
  .then((ks) => ks.reduce((p, k) => p.then((r) => r || caches.open(k).then((c) => c.match(req, opt))), Promise.resolve(undefined)))
  .then((r) => (r && r.type === 'opaque' && req && req.mode === 'cors') ? undefined : r);

const CACHE_VER    = 'v5.0.6';
const CACHE_NAME   = `manmin-outdoor-hydrant-${CACHE_VER}`;
const STATIC_CACHE = `manmin-outdoor-hydrant-static-${CACHE_VER}`;

const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/apple-touch-icon.png',
  './icons/favicon-32.png',
  './icons/favicon-16.png',
  './icons/favicon.ico',
  /* 로컬 폴백 폰트 — CDN 차단·오프라인 시 한글 깨짐 방지 */
  './assets/fonts/manmin-fonts.css',
  './assets/fonts/NotoSansKR-var.woff2',
];

/* ── INSTALL : 선캐싱 후 skipWaiting 즉시 호출 ── */
self.addEventListener('install', (event) => {
  console.log(`[SW ${CACHE_VER}] Installing...`);
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => Promise.allSettled(PRECACHE_URLS.map((u) => cache.add(mmReq(u)).catch((e) => console.warn('[SW] precache skip:', u, e)))).catch((e) => console.warn(`[SW ${CACHE_VER}] Pre-cache 일부 실패:`, e)))
      /* ★ 핵심: 즉시 skipWaiting → 이전 SW를 밀어내고 바로 activate */
      .then(() => self.skipWaiting())
  );
});

/* ── ACTIVATE : 이전 버전 캐시 전부 삭제 ── */
self.addEventListener('activate', (event) => {
  console.log(`[SW ${CACHE_VER}] Activating — cleaning old caches...`);
  event.waitUntil(
    caches.keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((k) => k !== CACHE_NAME && k !== STATIC_CACHE && mmOwn(k))
            .map((k) => {
              console.log(`[SW ${CACHE_VER}] 구버전 캐시 삭제:`, k);
              return caches.delete(k);
            })
        )
      )
      /* ★ 핵심: clients.claim() → 현재 열린 모든 탭에 즉시 적용 */
      .then(() => self.clients.claim())
      .then(() => console.log(`[SW ${CACHE_VER}] 활성화 완료`))
  );
});

/* ── FETCH : Network-First ── */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (url.origin !== self.location.origin) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((c) => c.put(request, copy));
          }
          return res;
        })
        .catch(() => mmMatch(request))
    );
    return;
  }

  event.respondWith(
    fetch(request)
      .then((res) => {
        if (!res || res.status !== 200 || res.type === 'opaque') return res;
        const copy = res.clone();
        caches.open(CACHE_NAME).then((c) => c.put(request, copy));
        return res;
      })
      .catch(() =>
        mmMatch(request).then((cached) => cached || mmMatch('./index.html'))
      )
  );
});

/* ── MESSAGE : SKIP_WAITING / CLEAR_CACHE ── */
self.addEventListener('message', (event) => {
  if (!event.data) return;

  if (event.data.type === 'SKIP_WAITING') {
    console.log(`[SW ${CACHE_VER}] SKIP_WAITING → 즉시 활성화`);
    self.skipWaiting();
  }

  if (event.data.type === 'CLEAR_CACHE') {
    console.log(`[SW ${CACHE_VER}] CLEAR_CACHE → 전체 캐시 삭제`);
    event.waitUntil(
      caches.keys()
        .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
        .then(() => {
          self.clients.matchAll().then((clients) =>
            clients.forEach((c) => c.postMessage({ type: 'CACHE_CLEARED' }))
          );
        })
    );
  }
});
