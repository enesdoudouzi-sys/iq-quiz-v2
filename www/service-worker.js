const CACHE = 'iq-quiz-v1';
const FILES = [
  '/',
  '/index.html',
  '/app.js',
  '/style.css',
  '/assets/icon-192.png',
];

self.addEventListener('install', function(e){
  e.waitUntil(
    caches.open(CACHE).then(function(c){
      return c.addAll(FILES);
    })
  );
});

self.addEventListener('fetch', function(e){
  e.respondWith(
    caches.match(e.request).then(function(r){
      return r || fetch(e.request);
    })
  );
});
