/* ═══════════════════════════════════════════════════════════════
   Service Worker — 옥외소화전 펌프 용량 계산서
   Developer MANMIN · Ver-3.1
═══════════════════════════════════════════════════════════════ */

const CACHE_NAME = 'manmin-hydrant-v3.1';
const STATIC_CACHE = 'manmin-static-v3.1';

/* 캐싱할 핵심 파일 목록 */
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
];

/* ── INSTALL : 핵심 파일 선 캐싱 ── */
self.addEventListener('install', (event) => {
  console.log('[SW] Installing v3.1...');
  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch((err) => {
        console.warn('[SW] Pre-cache 일부 실패:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

/* ── ACTIVATE : 구버전 캐시 삭제 ── */
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating...');
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_NAME && k !== STATIC_CACHE)
          .map((k) => {
            console.log('[SW] 구버전 캐시 삭제:', k);
            return caches.delete(k);
          })
      )
    ).then(() => self.clients.claim())
  );
});

/* ── FETCH : 네트워크 우선, 캐시 폴백 ── */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  /* 외부 CDN(Google Fonts, unpkg 등)은 네트워크 우선, 실패 시 캐시 */
  if (url.origin !== location.origin) {
    event.respondWith(
      fetch(request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE_NAME).then((c) => c.put(request, copy));
          return res;
        })
        .catch(() => caches.match(request))
    );
    return;
  }

  /* 로컬 파일 : 네트워크 우선, 오프라인 시 캐시 사용 */
  event.respondWith(
    fetch(request)
      .then((res) => {
        if (!res || res.status !== 200 || res.type === 'opaque') return res;
        const copy = res.clone();
        caches.open(CACHE_NAME).then((c) => c.put(request, copy));
        return res;
      })
      .catch(() =>
        caches.match(request).then(
          (cached) => cached || caches.match('./index.html')
        )
      )
  );
});

/* ── MESSAGE : SKIP_WAITING (업데이트 적용) ── */
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[SW] SKIP_WAITING 수신 → 즉시 활성화');
    self.skipWaiting();
  }
});
