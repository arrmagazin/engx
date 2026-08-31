---
type: Guide
title: Application Types
description: How MPAs, SPAs, SSR, static generation, and PWAs differ in where HTML is produced and what each needs.
tags: [frontend, spa, pwa, ssr, architecture]
---

# Application Types

Application types differ mainly in where HTML is produced: on the server for every request, once at build time, or in the browser after a JavaScript bundle loads. That single choice decides how navigation works, what a crawler sees, and how much has to happen before a first-time visitor sees content.

| Type | HTML Produced | Navigation | Content Without JavaScript |
| --- | --- | --- | --- |
| **MPA** | On the server, per request | Full page load per link | Complete |
| **SPA** | In the browser, after the bundle loads | Client-side routing | Empty shell only |
| **SSR** | On the server per request, then hydrated | Server for the first view, client-side after | Complete for the first view |
| **SSG** | At build time | Full page load, or client-side routing if added | Complete |

## Multi-Page Applications (MPA)

The server returns a complete HTML document for each URL, and every link click is a full page load that discards and rebuilds the page. Shared state lives on the server or in [browser storage](02-browser-technologies.md#browser-storage) rather than in memory.

## Single-Page Applications (SPA)

SPAs update the current page without full reloads, providing app-like navigation.

| Characteristic | Description |
| --- | --- |
| **Initial Load** | Downloads the application bundle before the first view renders — see [performance optimization](03-performance-optimization.md) for splitting it |
| **Navigation** | Client-side routing, no page reloads |
| **Data Fetching** | [API calls](../03-system-design/06-client-server-communication.md) for dynamic content |
| **SEO** | Content exists only after JavaScript runs, unless paired with [SSR](#server-side-rendering-ssr) or pre-rendering |

## Server-Side Rendering (SSR)

The server renders the requested route to HTML on each request, and the browser then loads the JavaScript that attaches behavior to that markup — the step called hydration. The first view arrives as complete as an MPA's, and navigation after it can stay client-side.

**Hydration** — Attaching client-side React to server-rendered HTML so it becomes
interactive. It exists because SSR alone produces markup that looks right and
does nothing, and it is the reason server rendering does not automatically make
a page faster: the HTML arrives early, but interactivity waits for the bundle to
download and execute. Its failure mode is a mismatch between server and client
output, which React must then discard and re-render.

**ISR** — Rendering a page statically, serving it from cache, and regenerating it
in the background after a revalidation window. It is the middle ground between
SSG, which cannot show fresh data, and SSR, which pays rendering cost on every
request. The trade is that some users see content up to one window stale.

**Revalidation** — The rule that decides when cached content is refreshed —
after a time window, or on demand when something changes. Time-based is simple
and always slightly stale; on-demand is exact and requires the writer to know
which cached entries its write invalidates. Choosing between them is usually a
question of whether staleness is *visible* to the user, not whether it is
technically present.

**Server component vs client component** — A server component renders only on
the server, ships no JavaScript, and may read data directly; a client component
ships to the browser and may use state and effects. The division exists to make
bundle size a deliberate choice rather than an accident, and the practical rule
is to keep interactivity at the leaves — one `'use client'` near the root pulls
everything below it into the bundle.

**Streaming SSR** — Sending HTML in chunks as it is produced rather than waiting
for the whole page. It improves TTFB and lets slow sections resolve behind a
suspense boundary while the rest of the page is already usable. It only helps if
the page is actually decomposed into boundaries; a single boundary around
everything streams one chunk, at the end.


## Static Site Generation (SSG)

Routes are rendered to HTML at build time and served as static files, so no per-request rendering happens at all. Anything that varies per user or changes between builds has to be fetched in the browser after load.

## Progressive Web Applications (PWA)

A PWA is a capability layer rather than a rendering model: any of the types above can add installability and offline support on top of what it already does.

| Feature | Implementation |
| --- | --- |
| **Installable** | Web App Manifest |
| **Offline Support** | [Service worker](02-browser-technologies.md#service-workers) intercepting requests |
| **Push Notifications** | Push API, delivered to the [service worker](02-browser-technologies.md#service-workers) |
| **Background Sync** | Background Sync API, deferred to the [service worker](02-browser-technologies.md#service-workers) |
| **Secure Context** | HTTPS, required before a service worker can register |

### Web App Manifest

```json
{
    "name": "My PWA App",
    "short_name": "PWA App",
    "start_url": "/",
    "display": "standalone",
    "theme_color": "#4a90d9",
    "icons": [
        { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
        { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
    ]
}
```

---

## Related Guides

- [Client-Server Communication](../03-system-design/06-client-server-communication.md) — the HTTP, REST, and GraphQL calls every type above uses to fetch data
- [Browser Technologies](02-browser-technologies.md) — service workers, browser storage, and the other APIs a PWA builds on
- [Performance Optimization](03-performance-optimization.md) — bundle splitting, caching, and the metrics that separate these types in practice
