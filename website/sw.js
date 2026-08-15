const CACHE_NAME = 'gnarlypi-v1';

// Install event - bypass waiting to ensure immediate activation
self.addEventListener('install', (event) => {
    self.skipWaiting();
});

// Activate event - claim control immediately
self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

// Fetch event - Chrome strictly requires a fetch handler to pass PWA criteria.
// We allow all traffic to bypass to the network to maintain real-time performance.
self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});