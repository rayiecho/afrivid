const CACHE = 'afrivid-v3';
const STATIC = [
  '/index.html',
  '/create.html',
  '/edit.html',
  '/aieditor.html',
  '/photo.html',
  '/design.html',
  '/studio.html',
  '/pricing.html',
  '/contact.html',
  '/chatbot.js',
  '/manifest.json',
  '/images/logo.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(STATIC)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).catch(() => caches.match('/index.html')))
  );
});
