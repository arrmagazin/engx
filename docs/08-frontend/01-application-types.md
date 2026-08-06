# Application Types

## Single-Page Applications (SPA)

SPAs update the current page without full reloads, providing app-like navigation.

| Characteristic | Description |
| --- | --- |
| Initial Load | Downloads full application bundle |
| Navigation | Client-side routing, no page reloads |
| Data Fetching | API calls for dynamic content |
| SEO | Requires SSR or pre-rendering |

## Progressive Web Applications (PWA)

PWAs are installable web apps with offline support.

| Feature | Implementation |
| --- | --- |
| Installable | Web App Manifest |
| Offline Support | Service Workers |
| Push Notifications | Push API |
| Background Sync | Background Sync API |
| Secure | Required HTTPS |

**Web App Manifest:**

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
