---
type: Guide
title: JavaScript and Bundle Performance
description: Covers code splitting, memory leaks, breaking up long tasks, tree shaking, and minification for frontend JavaScript.
tags: [frontend, performance, javascript, bundling]
---

This guide covers the techniques that keep the main thread free and the bundle small. The metrics and budgets they are measured against are in [Performance Optimization](03-performance-optimization.md); the render path and the network are in [Rendering and Network Performance](04-rendering-network-performance.md).

## JavaScript Performance

### Code Splitting

A dynamic `import()` returns a promise and puts its target in a separate chunk, fetched the first time the code path runs.

```jsx
import { lazy, Suspense } from 'react';
import { Route, Routes } from 'react-router-dom';

// Static import: always in the initial bundle
import Sidebar from './Sidebar';

// Dynamic import: its own chunk, fetched on first render of the route
const Dashboard = lazy(() => import('./Dashboard'));

function App() {
    return (
        <Suspense fallback={<p>Loading…</p>}>
            <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
            </Routes>
        </Suspense>
    );
}
```

Route boundaries are the natural split point, because the user has already accepted a wait there.

### Memory Leaks

```javascript
// Forgotten event listener: the listener keeps the instance reachable
class Widget {
    constructor() {
        this.handler = this.handleResize.bind(this);
        window.addEventListener('resize', this.handler);
    }
    handleResize() { /* ... */ }
    destroy() {
        window.removeEventListener('resize', this.handler); // required cleanup
    }
}

// Closure retaining large data
function createLeak() {
    const largeData = new Array(1_000_000);
    return () => console.log(largeData[0]); // holds the whole array
}
let fn = createLeak();
fn();
fn = null; // last reference dropped; the array can now be collected
```

`removeEventListener` needs the same function reference that was added. That is why the bound handler is stored on the instance, not bound inline.

### Breaking Up Long Tasks

A long task on the main thread blocks input handling, which is what INP measures. Split the work and yield between the pieces.

```javascript
// Bad - one task, main thread blocked until it finishes
function processAll(data) {
    for (const item of data) heavyProcessing(item);
}

// Good - fixed-size chunks, yielding to the event loop between them
function processInChunks(data) {
    const CHUNK_SIZE = 100;
    let index = 0;

    function processChunk() {
        const end = Math.min(index + CHUNK_SIZE, data.length);
        for (; index < end; index++) heavyProcessing(data[index]);
        if (index < data.length) setTimeout(processChunk, 0);
    }

    setTimeout(processChunk, 0);
}

// Work that can wait entirely: run it in idle time.
// requestIdleCallback ships in Chromium and Firefox, but as of 2026 Safari has it only
// behind a flag in Technology Preview - so the detection below is needed in a current
// browser, not only in older engines.
function processWhenIdle(tasks) {
    let index = 0;

    const whenIdle = typeof requestIdleCallback === 'function'
        ? (callback) => requestIdleCallback(callback)
        : (callback) => setTimeout(() => {
            const start = performance.now();
            callback({ timeRemaining: () => Math.max(0, 15 - (performance.now() - start)) });
        }, 1);

    function doWork(deadline) {
        while (index < tasks.length && deadline.timeRemaining() > 1) {
            heavyProcessing(tasks[index++]);
        }
        if (index < tasks.length) whenIdle(doWork);
    }

    whenIdle(doWork);
}
```

- The fallback gives `doWork` a real deadline, not a stub that always reports time remaining. A stub would let the loop drain the whole queue in one task — the exact problem idle scheduling is there to avoid.
- `requestIdleCallback` is wrapped in an arrow, not assigned directly, because calling it detached from `window` throws in browsers.

---

## Bundle Optimization

### Tree Shaking

Tree shaking drops exports that nothing imports. It needs static `import`/`export`; a `require()` call or a re-export computed at runtime defeats it.

```javascript
// webpack.config.js
module.exports = {
    // production mode already enables usedExports and sideEffects detection;
    // setting optimization.sideEffects to false turns that detection off
    mode: 'production',
    optimization: {
        splitChunks: {
            chunks: 'all',
            cacheGroups: {
                vendor: { test: /[\\/]node_modules[\\/]/, name: 'vendors', chunks: 'all' }
            }
        }
    }
};
```

The bigger win is the `sideEffects` flag. It lets the bundler skip a whole module instead of reasoning about individual statements:

```json
{
  "name": "your-package",
  "sideEffects": ["*.css"]
}
```

`"sideEffects": false` claims that no module in the package does anything on import. That is a claim about your own code. It is wrong the moment a file registers a polyfill or imports a stylesheet for effect — list those files instead, as above.

### Minification

- **Minifiers** strip whitespace and comments and shorten local identifiers. They run automatically in a production build and need no configuration.
- **Removing unused CSS** is the manual one. The tool scans your templates for the selectors actually used, so class names built at runtime by string concatenation are invisible to it and get deleted. Either safelist them or stop building class names by concatenation.
