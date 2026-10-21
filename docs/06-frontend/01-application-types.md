---
type: Guide
title: Application Types
description: How MPAs, SPAs, SSR, static generation, and PWAs differ in where HTML is produced and what each needs.
tags: [frontend, spa, pwa, ssr, architecture]
---

Application types differ mainly in where HTML is produced: on the server for every request, once at build time, or in the browser after a JavaScript bundle loads. That one choice decides how navigation works, what a crawler sees, and how much must happen before a first-time visitor sees content.

| Type | HTML Produced · Content Without JavaScript | Navigation |
| --- | --- | --- |
| **MPA** | On the server, per request · Complete | Full page load per link |
| **SPA** | In the browser, after the bundle loads · Empty shell only | Client-side routing |
| **SSR** | On the server per request, then hydrated · Complete for the first view | Server for the first view, client-side after |
| **SSG** | At build time · Complete | Full page load, or client-side routing if added |

## Multi-Page Applications (MPA)

The server returns a complete HTML document for each URL. Every link click is a full page load that discards and rebuilds the page. Shared state lives on the server or in [browser storage](02-browser-technologies.md#browser-storage), not in memory.

## Single-Page Applications (SPA)

SPAs update the current page without full reloads, which gives app-like navigation.

| Characteristic | Description |
| --- | --- |
| **Initial Load** | Downloads the application bundle before the first view renders — see [code splitting](05-javascript-bundle-performance.md#code-splitting) for splitting it |
| **Navigation** | Client-side routing, no page reloads |
| **Data Fetching** | [API calls](../03-system-design/06-client-server-communication.md) for dynamic content |
| **SEO** | Content exists only after JavaScript runs, unless paired with [SSR](#server-side-rendering-ssr) or pre-rendering |

## Server-Side Rendering (SSR)

The server renders the requested route to HTML on each request. The browser then loads the JavaScript that attaches behavior to that markup — the step called hydration. The first view arrives as complete as an MPA's, and later navigation can stay client-side.

Hydration
:   Attaching client-side React to server-rendered HTML so it becomes interactive

    It exists because SSR alone produces markup that looks right and does nothing. It is also why server rendering does not automatically make a page faster: the HTML arrives early, but interactivity waits for the bundle to download and execute. The failure mode is a mismatch between server and client output, which React must then discard and re-render.

ISR
:   Incremental static regeneration — rendering a page statically, serving it from cache, and regenerating it in the background after a revalidation window

    The middle ground between SSG, which cannot show fresh data, and SSR, which pays rendering cost on every request. The trade: some users see content up to one window stale.

Revalidation
:   The rule that decides when cached content is refreshed — after a time window, or on demand when something changes

    - Time-based: simple, and always slightly stale.
    - On-demand: exact, but the writer must know which cached entries its write invalidates.

    The choice usually turns on whether staleness is *visible* to the user, not whether it is technically present.

Server component vs client component
:   The split between components that render only on the server and components that ship to the browser

    - A server component ships no JavaScript and may read data directly.
    - A client component may use state and effects.

    The split makes bundle size a deliberate choice, not an accident. Practical rule: keep interactivity at the leaves — one `'use client'` near the root pulls everything below it into the bundle.

Streaming SSR
:   Sending HTML in chunks as it is produced, instead of waiting for the whole page

    It improves TTFB and lets slow sections resolve behind a suspense boundary while the rest of the page is already usable. It helps only if the page is actually split into boundaries: a single boundary around everything streams one chunk, at the end.

## Static Site Generation (SSG)

Routes are rendered to HTML at build time and served as static files, so no per-request rendering happens. Anything that varies per user or changes between builds must be fetched in the browser after load.

## Progressive Web Applications (PWA)

A PWA is a capability layer, not a rendering model: any type above can add installability and offline support on top.

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
