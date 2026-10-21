---
type: Guide
title: Performance Optimization
description: Covers Core Web Vitals, performance budgets, and measuring them with the Performance API and Lighthouse CI.
tags: [frontend, performance, web-vitals]
---

Frontend performance work splits into three places: the render path, the network, and the bundle. This guide covers what to measure in each and what to aim for. The techniques that move the number are in [Rendering and Network Performance](04-rendering-network-performance.md) and [JavaScript and Bundle Performance](05-javascript-bundle-performance.md). Together the three are this book's home for Core Web Vitals, budgets, caching headers, bundling, and profiling. The DevTools panels that produce these measurements are in [Chrome DevTools](../04-development-process/07-debugging.md#chrome-devtools).

## Core Web Vitals

Google publishes each metric with two boundaries: "good" is at or below the first, "poor" is above the second. The band between them is "needs improvement".

| Metric | Measures | Good · Poor |
| --- | --- | --- |
| **LCP** (Largest Contentful Paint) | Render time of the largest element visible in the viewport | ≤ 2.5 s · > 4.0 s |
| **INP** (Interaction to Next Paint) | Delay between an interaction and the next frame drawn | ≤ 200 ms · > 500 ms |
| **CLS** (Cumulative Layout Shift) | Visual stability — how much content moves on its own | ≤ 0.1 · > 0.25 |
| **FCP** (First Contentful Paint) | Time until the first text or image is painted | ≤ 1.8 s · > 3.0 s |
| **TTFB** (Time to First Byte) | Time until the first byte of the response arrives | ≤ 800 ms · > 1.8 s |

LCP, INP, and CLS are the three Core Web Vitals. FCP and TTFB are diagnostics: they tell you whether a bad LCP started at the server or in the browser.

- INP replaced FID (First Input Delay) as a Core Web Vital on 12 March 2024.
- Time to Interactive stopped counting toward the Lighthouse performance score in version 10 (February 2023). Its weight was redistributed, raising CLS to 25 percent. The audit itself survived for a while as a report diagnostic and was dropped later. Do not budget against it.
- INP is the field measure of responsiveness; Total Blocking Time is the lab stand-in.

## Performance Budgets

The thresholds above are published. The numbers below are not: no standard fixes them. They are common starting points. Their value comes from being chosen once and then enforced in [CI](../04-development-process/03-ci-cd.md) — a budget nobody fails is not a budget.

| Budget | Starting Target | Basis |
| --- | --- | --- |
| **JavaScript, compressed** | 200 KB | Convention; JavaScript costs more than its transfer size, because it is also parsed and executed |
| **Total page weight, compressed** | 500 KB | Convention |
| **Critical CSS, inlined** | 14 KB | Roughly what TCP sends before waiting for the first acknowledgement — the initial congestion window is 10 segments (RFC 6928) |

A request-count budget is no longer worth keeping. Under HTTP/2 one connection multiplexes many streams. The limit is `SETTINGS_MAX_CONCURRENT_STREAMS` (RFC 9113), not the six-connections-per-host convention browsers apply to HTTP/1.1. So the number of requests stopped being a good proxy for latency. See [Client-Server Communication](../03-system-design/06-client-server-communication.md) for the connection model.

---

## Performance Monitoring

### Performance API

```javascript
// Navigation timing. PerformanceNavigationTiming has startTime === 0,
// so every field is already a duration from the start of navigation;
// there is no navigationStart property to subtract.
const nav = performance.getEntriesByType('navigation')[0];
console.log('DNS:', nav.domainLookupEnd - nav.domainLookupStart);
console.log('Page load:', nav.loadEventEnd); // same as nav.duration

// LCP: the last entry before the first interaction is the final value
new PerformanceObserver((list) => {
    const last = list.getEntries().at(-1);
    console.log('LCP:', last.startTime);
}).observe({ type: 'largest-contentful-paint', buffered: true });

// CLS
let clsValue = 0;
new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) clsValue += entry.value;
    }
}).observe({ type: 'layout-shift', buffered: true });
```

- `buffered: true` replays entries recorded before the observer existed. This matters because LCP and the first layout shifts happen before your script runs.
- The CLS snippet sums every shift, but the reported metric is the largest burst within a session window. Use Google's `web-vitals` library when the number must match what field tools report.
- To read the same data interactively, use the Performance panel described in [Chrome DevTools](../04-development-process/07-debugging.md#chrome-devtools).

### Lighthouse CI

Lighthouse runs in a lab, on a simulated network and device, so its numbers are reproducible but not what real users see. It reports no INP; Total Blocking Time is its stand-in. Wire it into the [pipeline](../04-development-process/03-ci-cd.md) so a regression fails the build:

```javascript
// .lighthouserc.js
module.exports = {
    ci: {
        collect: { numberOfRuns: 3, url: ['http://localhost:3000'] },
        assert: {
            assertions: {
                'categories:performance': ['error', { minScore: 0.9 }],
                'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
                'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
                'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }]
            }
        }
    }
};
```

- The timing assertions are in milliseconds; CLS is unitless. All three are set to the published "good" thresholds.
- `numberOfRuns: 3` because a single run is noisy — Lighthouse reports the median.
