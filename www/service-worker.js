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

// CDN files: their URLs carry a version, so they never change.
const filters = [
  "https://fonts.googleapis.com/",
  "https://fonts.gstatic.com/",
  "https://unpkg.com/",
  "https://cdn.jsdelivr.net/",
];

// Site files: network first, so a deploy shows at once; the cache answers offline.
// Every route of the single-page app is index.html, kept under "/".
const fromSite = async (cache, request) => {
  const key = request.mode === "navigate" ? "/" : request;
  try {
    const response = await fetch(request);
    if (response.ok) await cache.put(key, response.clone());
    return response;
  } catch {
    return (await cache.match(key)) ?? offlineResponse(request);
  }
};

// CDN files: cache first. Stylesheets load without CORS and come back opaque (status 0): keep them too.
const fromCdn = async (cache, request) => {
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok || response.type === "opaque") await cache.put(request, response.clone());
  return response;
};

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;
  const url = request.url;
  const handle = url.startsWith(`${self.location.origin}/`)
    ? fromSite
    : filters.some((f) => url.startsWith(f))
      ? fromCdn
      : null;

  if (!handle) return;

  event.respondWith(
    caches
      .open(CACHE_NAME)
      .then((cache) => handle(cache, request))
      .catch((error) => {
        console.error("Error in fetch:", error);
        return offlineResponse(request);
      }),
  );
});
