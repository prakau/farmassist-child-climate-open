const CACHE = "farmassist-v1";
const scoped = path => new URL(path, self.registration.scope).toString();
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon.svg"].map(scoped);
self.addEventListener("install", event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL))));
self.addEventListener("activate", event => event.waitUntil(self.clients.claim()));
self.addEventListener("fetch", event => {
  if (event.request.method !== "GET") return;
  event.respondWith(fetch(event.request).then(response => {
    const copy = response.clone();
    caches.open(CACHE).then(cache => cache.put(event.request, copy));
    return response;
  }).catch(() => caches.match(event.request).then(response => response || caches.match(scoped("./index.html")))));
});
