// One cache for the site. Entries never expire; there is no per-deploy cache.
const CACHE_NAME = "cache";

// Answer instead of rejecting: a rejected respondWith() is logged as an uncaught error and
// shows the browser's network-error page.
const OFFLINE_PAGE = `<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Offline</title>
<body style="font-family:system-ui,sans-serif;display:grid;place-items:center;min-height:100vh;margin:0;color:#1f2937">
<main style="text-align:center;padding:24px"><h1 style="margin:0 0 8px">You're offline</h1>
<p style="margin:0 0 20px;color:#6b7280">This page can't load right now. Check your connection.</p>
<button onclick="location.reload()" style="font:inherit;font-weight:600;padding:12px 24px;border:0;border-radius:999px;background:#1f2937;color:#fff;cursor:pointer">Try again</button>
</main></body></html>`;

const offlineResponse = (request) =>
  request.mode === "navigate"
    ? new Response(OFFLINE_PAGE, { status: 503, headers: { "Content-Type": "text/html; charset=utf-8" } })
    : new Response("", { status: 504, statusText: "Offline" });

const filters = [
  "https://fonts.googleapis.com/",
  "https://fonts.gstatic.com/",
  "https://unpkg.com/",
  "https://data.jsdelivr.com/v1/",
  "https://cdn.jsdelivr.net/gh/",
];

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((cacheNames) =>
        Promise.all(cacheNames.filter((name) => name.startsWith("cache-")).map((name) => caches.delete(name))),
      ),
  );
});

self.addEventListener("fetch", (event) => {
  const url = event.request.url;
  event.respondWith(
    caches
      .open(CACHE_NAME)
      .then(async (cache) => {
        const cached = await cache.match(event.request);
        if (cached) return cached;

        const response = await fetch(event.request.clone());

        if (response.status === 200 && filters.some((f) => url.startsWith(f))) {
          await cache.put(event.request, response.clone());
        }

        return response;
      })
      .catch((error) => {
        console.error("Error in fetch:", error);
        return offlineResponse(event.request);
      }),
  );
});
