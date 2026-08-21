const CACHE = 'afrivid-v9';
const STATIC_ASSETS = [
  '/manifest.json',
  '/images/logo.png'
];

// Install — only cache non-HTML assets
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC_ASSETS)).then(() => self.skipWaiting())
  );
});

// Activate — clear old caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

// Fetch — HTML always from network, same-origin static assets cache-first, everything else
// (any cross-origin API call — job-status polling, TTS, ai-generate, Firebase, etc.) always
// goes straight to the network. This used to cache-first EVERY non-HTML request, which meant
// the very first /job-status/{id} poll got cached and every poll after that — for the rest of
// that job — replayed the same stale response instead of ever checking again, making a job
// that finished in seconds look "stuck" for however long the user kept watching.
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Always fetch HTML fresh from network
  if (e.request.destination === 'document' || url.pathname.endsWith('.html') || url.pathname === '/') {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request))
    );
    return;
  }

  // Cross-origin requests (APIs, polling, Firebase, etc.) — never cache, always network.
  if (url.origin !== self.location.origin) {
    e.respondWith(fetch(e.request));
    return;
  }

  // Same-origin static assets — cache first, network fallback
  e.respondWith(
    caches.match(e.request).then(cached => {
      return cached || fetch(e.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return response;
      });
    })
  );
});
