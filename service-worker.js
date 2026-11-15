/* Service Worker – IQ Quiz (Website)
   Seiten zuerst frisch aus dem Netz, gespeicherte Version nur offline.
   Anfragen an den Server (Render) und fremde Seiten werden nie gespeichert. */
const CACHE = 'iq-quiz-v3';
const FILES = ['./', './index.html', './i18n.js', './app.js', './style.css', './assets/icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => Promise.all(FILES.map(f => c.add(f).catch(() => {})))).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  if (req.url.endsWith('.apk')) return; // Downloads nicht cachen
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req))
  );
});
