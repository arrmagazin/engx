---
type: Guide
title: Browser Technologies
description: Covers the DOM, the event model, browser storage, and the Fetch, History, Geolocation, and Service Worker APIs.
tags: [frontend, browser, dom, css, web-apis]
---

# Browser Technologies

The browser is the runtime every frontend application ships into. This guide covers the DOM and its event model, the browser APIs for fetching, navigation, storage, and location, and the service worker that runs behind them all.

## DOM

The DOM represents the page as a tree of nodes that JavaScript can read and change. Reading a geometric property (`offsetHeight`, `getBoundingClientRect`) forces the browser to settle any pending layout, so interleaving reads and writes makes it recompute layout on every iteration — layout thrashing.

| Pattern | Effect |
| --- | --- |
| **Batch reads, then writes** | One layout pass instead of one per element |
| **Read and write in the same loop** | Layout thrashing — layout is recomputed each iteration |
| **`DocumentFragment` for bulk inserts** | One insertion into the live tree instead of many |
| **`textContent` over `innerHTML`** | No HTML parsing, and no markup injection surface |

```javascript
// Bad - multiple reflows
elements.forEach(el => { const h = el.offsetHeight; el.style.height = (h + 10) + 'px'; });

// Good - batch reads then writes
const heights = Array.from(elements).map(el => el.offsetHeight);
elements.forEach((el, i) => { el.style.height = (heights[i] + 10) + 'px'; });

// Use fragment for bulk inserts
const fragment = document.createDocumentFragment();
for (let i = 0; i < 100; i++) {
    const div = document.createElement('div');
    div.textContent = `Item ${i}`;
    fragment.appendChild(div);
}
document.body.appendChild(fragment);
```

Measuring which of these actually costs you anything belongs to [Performance Optimization](05-performance-optimization.md); the [Performance panel](../04-development-process/06-debugging.md#chrome-devtools) records the layout passes.

## Events

Events bubble from target up to Window (capture phase goes the other direction).

**Event delegation** — attach one listener to the parent instead of many to children:

```javascript
document.getElementById('list').addEventListener('click', (event) => {
    if (event.target.classList.contains('item')) {
        handleItemClick(event);
    }
});
```

A `click` handler on a non-interactive element such as a `div` gets no keyboard or screen reader behavior for free. Use a real `button` or `a`, or supply the role, tab order, and key handling yourself — see [Accessibility (WCAG)](06-accessibility-wcag.md).

## Browser APIs

### Fetch API

`fetch` returns a promise that rejects only on network failure. An HTTP error status resolves normally, so check `response.ok` yourself. Methods, status codes, and the rest of the protocol are in [Client-Server Communication](03-client-server-communication.md).

```javascript
async function getUsers() {
    try {
        const response = await fetch('https://api.example.com/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ name: 'New User' })
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}
```

### Location and History API

`window.location` describes the current URL and triggers full page loads. `window.history` manipulates the session stack without reloading — the basis of client-side routing in a [single-page application](01-application-types.md).

| Part | `https://site.com:8080/docs/page?tab=api#top` |
| --- | --- |
| **`protocol`** | `https:` |
| **`host` / `hostname` / `port`** | `site.com:8080` / `site.com` / `8080` |
| **`pathname`** | `/docs/page` |
| **`search`** | `?tab=api` |
| **`hash`** | `#top` |
| **`origin`** | `https://site.com:8080` |

```javascript
// Navigation — reloads the page
location.href = '/next';      // adds a history entry
location.assign('/next');     // same as above
location.replace('/next');    // no history entry (back button skips it)
location.reload();

// Read and edit query params
const params = new URLSearchParams(location.search);
params.get('tab');            // 'api'
params.set('tab', 'guide');

// Parse or build any URL
const url = new URL('/docs?tab=api', location.origin);
```

| History method | Effect |
| --- | --- |
| **`pushState(state, '', url)`** | Adds an entry, no reload |
| **`replaceState(state, '', url)`** | Rewrites current entry, no reload |
| **`back()` / `forward()` / `go(n)`** | Moves along the stack |
| **`history.length`** | Entries in this tab's session |

```javascript
// Client-side routing
function navigate(path) {
    history.pushState({ path }, '', path);
    render(path);
}

// Fires on back/forward, NOT on pushState/replaceState
window.addEventListener('popstate', (event) => {
    render(event.state?.path ?? location.pathname);
});
```

Notes:

- `pushState` never fires `popstate` — call the renderer yourself.
- State must be structured-cloneable and is capped — Firefox rejects a state object over 16 MiB. Keep it small and treat the URL as the source of truth.
- The URL must be same-origin; cross-origin throws a `SecurityError`.
- Changing only `location.hash` adds a history entry and fires `hashchange`, not a reload — the pre-`pushState` routing technique.

### Browser Storage

| Storage | Capacity | Lifetime | Scope |
| --- | --- | --- | --- |
| **Cookie** | About 4 KB per cookie | `Expires` or `Max-Age`; cleared when the session ends if neither is set | Domain and path it was set for; sent from a third-party frame only with `SameSite=None; Secure`, which browsers increasingly block |
| **`localStorage`** | Typically around 5 MB per origin; no specification fixes the number | Persists until cleared, except in Safari, where Intelligent Tracking Prevention deletes it after seven days without user interaction with the site | Same origin |
| **`sessionStorage`** | Typically around 5 MB per origin | Until the tab or window closes | Same origin, one tab |
| **IndexedDB** | Browser-managed quota against available disk space, reaching gigabytes | Persists until cleared or evicted; Safari's Intelligent Tracking Prevention deletes it on the same seven-day rule | Same origin |

Safari's seven-day rule also removes service worker registrations, so treat script-writable storage as a cache you can lose, not a database of record. The DevTools **Application** panel shows what is stored — see [Chrome DevTools](../04-development-process/06-debugging.md#chrome-devtools).

```javascript
// localStorage
localStorage.setItem('user', JSON.stringify({ name: 'John' }));
const user = JSON.parse(localStorage.getItem('user'));
localStorage.removeItem('user');

// IndexedDB
const request = indexedDB.open('MyDatabase', 1);
request.onupgradeneeded = (event) => {
    const db = event.target.result;
    const store = db.createObjectStore('users', { keyPath: 'id' });
    store.createIndex('email', 'email', { unique: true });
};
```

### Geolocation API

Geolocation needs a secure context and explicit user permission; the first call raises the browser's permission prompt, and a refusal arrives as an error, not a rejection you can retry around.

```javascript
navigator.geolocation.getCurrentPosition(
    (position) => {
        console.log('Lat:', position.coords.latitude);
        console.log('Lng:', position.coords.longitude);
    },
    (error) => console.error('Error:', error),
    { enableHighAccuracy: true, timeout: 5000 }
);

// Watch position
const watchId = navigator.geolocation.watchPosition(
    pos => console.log(pos),
    err => console.error(err)
);
navigator.geolocation.clearWatch(watchId);
```

## Service Workers

A service worker is a script that runs separately from any page and can intercept requests from the pages it controls, which is what makes offline behavior and [progressive web apps](01-application-types.md) possible. It needs a secure context, is registered from the page, and keeps its own cache storage independent of the HTTP cache.

```javascript
const CACHE_NAME = 'my-pwa-cache-v1';
const STATIC_ASSETS = ['/', '/index.html', '/styles/main.css', '/scripts/app.js'];

self.addEventListener('install', (event) => {
    event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS)));
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then(names =>
            Promise.all(names.filter(n => n !== CACHE_NAME).map(n => caches.delete(n)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then(response => response || fetch(event.request))
    );
});
```

Versioning the cache name, as above, is what lets `activate` delete the previous version. Which assets belong in it is a [performance](05-performance-optimization.md) decision.

## CSS Resources

| Resource | Link |
| --- | --- |
| **MDN CSS Reference** | [developer.mozilla.org/en-US/docs/Web/CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) |
| **MDN Learn CSS** | [developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics) |
| **CSS Specifications (W3C)** | [w3.org/Style/CSS/specs](https://www.w3.org/Style/CSS/specs) |
| **A Complete Guide to Flexbox** | [css-tricks.com/snippets/css/a-guide-to-flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) |
| **A Complete Guide to Grid** | [css-tricks.com/complete-guide-css-grid-layout](https://css-tricks.com/complete-guide-css-grid-layout/) |
| **Tailwind CSS Docs** | [tailwindcss.com/docs](https://tailwindcss.com/docs) |
| **DaisyUI** | [daisyui.com](https://daisyui.com/) |
