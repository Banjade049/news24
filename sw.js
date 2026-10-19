const CACHE_NAME = 'news24-v3';
const STATIC_ASSETS = [
    './',
    './index.html',
    './manifest.json',
    './apple-touch-icon.png',
    './icon-192.png'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.map((k) => {
                    if (k !== CACHE_NAME) return caches.delete(k);
                })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (e) => {
    // For API calls (RSS2JSON), use Network-First, fallback to Cache
    if (e.request.url.includes('api.rss2json.com')) {
        e.respondWith(
            fetch(e.request)
                .then((res) => {
                    const resClone = res.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(e.request, resClone));
                    return res;
                })
                .catch(() => caches.match(e.request))
        );
        return;
    }

    // For static files: Cache-First, fallback to Network
    e.respondWith(
        caches.match(e.request).then((cached) => cached || fetch(e.request))
    );
});
