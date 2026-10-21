---
type: Guide
title: Web Security Defenses
description: Covers security headers, TLS certificates, Content Security Policy, dependency security, and client-side storage, iframe, and JSON risks.
tags: [security, web, csp, headers]
---

This guide covers the defenses the browser and the delivery pipeline enforce: transport headers, Content Security Policy, dependency integrity, and client-side storage. The principles they implement and the attacks they counter are in [Web Application Security](07-security-web.md).

## Transport Layer Security

### Security Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'; script-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**HSTS:** after the first HTTPS visit, the browser enforces HTTPS for `max-age` seconds, which prevents downgrade attacks. Preload lists enforce it even on the first visit.

### Certificate Requirements

| Aspect | Recommendation |
| --- | --- |
| **Algorithm** | RSA 2048+ or ECDSA 256+ |
| **Validity** | Bounded by the CA/Browser Forum maximum: 200 days since March 2026, 100 days from March 2027, 47 days from March 2029 (ballot SC-081v3); automate renewal with ACME |
| **CA** | Trusted CA (Let's Encrypt, DigiCert) |

## Content Security Policy (CSP)

A CSP restricts the sources the browser may load content from.

| Directive | Purpose | Example |
| --- | --- | --- |
| **`default-src`** | Fallback | `'self'` |
| **`script-src`** | JavaScript | `'self' 'nonce-vDhTrNNbrS+dqXsjj+z1Sg=='` |
| **`style-src`** | CSS | `'self' 'unsafe-inline'` |
| **`img-src`** | Images | `'self' data: https:` |
| **`connect-src`** | Fetch/XHR targets | `'self' https://api.example.com` |
| **`frame-ancestors`** | Who can embed this page | `'none'` |

```http
Content-Security-Policy:
    default-src 'self';
    script-src 'self' 'nonce-vDhTrNNbrS+dqXsjj+z1Sg==';
    img-src 'self' data: https:;
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
    upgrade-insecure-requests;
```

**Nonce for inline scripts.** A nonce must be unpredictable and freshly generated per response. A fixed string in the source defeats it entirely.

```javascript
const nonce = crypto.randomBytes(16).toString('base64');
res.setHeader('Content-Security-Policy', `script-src 'self' 'nonce-${nonce}'`);
```

```html
<!-- The same nonce must be templated into the tag on every response.
     A hardcoded value can never match a freshly generated one. -->
<script nonce="{{nonce}}">console.log('Allowed');</script>
```

**Violation reporting:**

```javascript
document.addEventListener('securitypolicyviolation', (e) => {
    console.error('CSP Violation:', {
        blockedURI: e.blockedURI,
        violatedDirective: e.violatedDirective
    });
});
```

## Dependency Security

```bash
npm audit          # Check for vulnerabilities
npm audit fix      # Auto-fix
npm ci             # Reproducible installs
npm outdated       # Check for updates
```

| Tool | Purpose |
| --- | --- |
| **npm audit** | Built-in vulnerability scanner |
| **Snyk** | Commercial scanner with its own vulnerability database, CLI + IDE |
| **Dependabot** | GitHub automatic updates |

**Third-party scripts — use Subresource Integrity (SRI):**

```html
<!-- Generate the digest from the exact file being served:
     openssl dgst -sha384 -binary script.js | openssl base64 -A -->
<script
    src="https://cdn.example.com/script.js"
    integrity="sha384-BASE64_SHA384_DIGEST_OF_THE_SERVED_FILE"
    crossorigin="anonymous"
></script>
```

## Client-Side Security

### Storage

```javascript
// Never store sensitive data in localStorage - XSS exposes everything

// In-memory only (cleared on page unload)
const sensitiveData = new Map();

// sessionStorage (cleared on tab close) - equally readable by XSS:
// never use it for secrets or tokens, only for non-sensitive data
sessionStorage.setItem('tempData', data);
```

### Iframe Security

```html
<!-- Restrict iframe capabilities with sandbox -->
<iframe
    src="https://external-site.com"
    sandbox="allow-scripts allow-same-origin allow-forms"
    loading="lazy"
></iframe>

<!-- Prevent clickjacking -->
<!-- X-Frame-Options: DENY -->
<!-- Content-Security-Policy: frame-ancestors 'none' -->
```

### JSON Vulnerabilities

| Vulnerability | Prevention |
| --- | --- |
| **JSON Injection** | Input validation |
| **DoS via large payload** | Size limits |
| **Prototype Pollution** | Reject `__proto__`, `constructor`, and `prototype` keys on merge or parse; `Object.create(null)` for map-like objects |
| **XSS via `eval()`** | Always use `JSON.parse()` |

Prototype pollution defenses:

- **Deep cloning does not help.** A naive recursive copy assigns through `__proto__` like any other key, so it carries the polluted prototype into the copy instead of leaving it behind.
- **Freezing helps only on `Object.prototype` itself.** That is worth doing as a backstop.
- **What actually holds:** refuse the three keys wherever untrusted input is merged or parsed — a `JSON.parse` reviver that returns `undefined` for them costs almost nothing — and give map-like objects no prototype to pollute in the first place.

Use CORS, not JSONP: JSONP is vulnerable to XSS.
