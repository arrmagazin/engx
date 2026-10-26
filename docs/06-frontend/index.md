---
type: Guide
title: Frontend
description: Index of the frontend chapter, with the standards, reference documentation, and roadmaps its guides draw on.
tags: [frontend, resources, reference]
---

Frontend engineering covers the runtime the code ships into and the standards it is measured against: the browser, WCAG, and the OWASP attack classes, not any one framework.

- What travels between browser and server is a system-design concern, covered in [Client-Server Communication](../03-system-design/06-client-server-communication.md) and [Data Formats](../99-appendices/07-data-formats.md).
- The guides stay framework-agnostic, with one exception: [Next.js](09-nextjs.md), distilled as the reference full-stack React framework. Other frameworks' documentation is linked below, not restated.
- The same goes for the languages: this book documents the engineering around HTML, CSS, and JavaScript, not the languages themselves. Their specifications are under Web Standards below; CSS reference material is in [Browser Technologies](02-browser-technologies.md#css-resources).

## In This Chapter

| Doc | What it covers |
| --- | --- |
| **[Application Types](01-application-types.md)** | Where each kind of application produces its HTML — MPA, SPA, SSR, static generation, and PWA |
| **[Browser Technologies](02-browser-technologies.md)** | The DOM and its event model, browser storage, and the Fetch, History, Geolocation, and Service Worker APIs |
| **[Performance Optimization](03-performance-optimization.md)** | Core Web Vitals, performance budgets, and measuring them in the lab and in the field |
| **[Rendering and Network Performance](04-rendering-network-performance.md)** | The critical rendering path, layout and paint costs, compression, HTTP caching, resource hints, and images |
| **[JavaScript and Bundle Performance](05-javascript-bundle-performance.md)** | Code splitting, memory leaks, long tasks, tree shaking, and minification |
| **[Accessibility (WCAG)](06-accessibility-wcag.md)** | The WCAG version and conformance level to build against, the POUR principles, and everyday ARIA patterns |
| **[Web Application Security](07-security-web.md)** | Core web security principles, the OWASP Top 10, common vulnerabilities, and authentication |
| **[Web Security Defenses](08-web-security-defenses.md)** | Security headers, TLS certificates, CSP, dependency security, and client-side storage, iframe, and JSON risks |
| **[Next.js](09-nextjs.md)** | The Next.js 16 App Router: routing files, Server Components, Cache Components, Server Functions, proxy, and assets |

## Core Documentation

| Resource | Link |
| --- | --- |
| **MDN Web Docs** | [developer.mozilla.org](https://developer.mozilla.org/) |
| **JavaScript.info** | [javascript.info](https://javascript.info/) |
| **TypeScript Docs** | [typescriptlang.org/docs](https://www.typescriptlang.org/docs/) |
| **React Docs** | [react.dev](https://react.dev/) |
| **React Native Docs** | [reactnative.dev](https://reactnative.dev/) |
| **Next.js Docs** | [nextjs.org/docs](https://nextjs.org/docs) |
| **GraphQL Documentation** | [graphql.org](https://graphql.org/) |
| **Web.dev PWA Guide** | [web.dev/learn/pwa](https://web.dev/learn/pwa/) |
| **DevDocs** | [devdocs.io](https://devdocs.io/) |

## Web Standards

| Resource | Link |
| --- | --- |
| **HTML Living Standard (WHATWG)** | [html.spec.whatwg.org](https://html.spec.whatwg.org/) |
| **ECMAScript Specification** | [tc39.es/ecma262](https://tc39.es/ecma262/) |
| **TC39** | [tc39.es](https://tc39.es/) |
| **W3C** | [w3.org](https://www.w3.org/) |
| **WCAG 2.2 Quick Reference** | [w3.org/WAI/WCAG22/quickref](https://www.w3.org/WAI/WCAG22/quickref/) |

## Performance

| Resource | Link |
| --- | --- |
| **Web Vitals** | [web.dev/articles/vitals](https://web.dev/articles/vitals) |
| **Critical Rendering Path** | [web.dev/articles/critical-rendering-path](https://web.dev/articles/critical-rendering-path) |
| **MDN Performance** | [developer.mozilla.org/en-US/docs/Web/Performance](https://developer.mozilla.org/en-US/docs/Web/Performance) |
| **Lighthouse Documentation** | [developer.chrome.com/docs/lighthouse](https://developer.chrome.com/docs/lighthouse/) |

## Security

| Resource | Link |
| --- | --- |
| **OWASP Top Ten** | [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/) |
| **MDN Security** | [developer.mozilla.org/en-US/docs/Web/Security](https://developer.mozilla.org/en-US/docs/Web/Security) |
| **Same-Origin Policy** | [developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy) |
| **Content Security Policy** | [content-security-policy.com](https://content-security-policy.com/) |

The attack classes themselves, beyond these reference links, are covered in [Web Application Security](07-security-web.md) and [Web Security Defenses](08-web-security-defenses.md).

## Roadmaps and Guides

| Resource | Link |
| --- | --- |
| **Frontend Roadmap** | [roadmap.sh/frontend](https://roadmap.sh/frontend) |
| **Performance Best Practices** | [roadmap.sh/frontend-performance-best-practices](https://roadmap.sh/frontend-performance-best-practices) |
| **Web Performance (Google)** | [web.dev/learn/performance](https://web.dev/learn/performance/) |
| **Front-end Guide (Grab)** | [github.com/grab/front-end-guide](https://github.com/grab/front-end-guide) |
