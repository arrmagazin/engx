---
type: Guide
title: Debugging With Chrome DevTools
description: Covers the Chrome DevTools panels, how to open them, conditional breakpoints, and the console utilities worth knowing.
tags: [debugging, devtools, frontend, tooling]
---

# Debugging With Chrome DevTools

Chrome DevTools is the debugger built into the browser, and it is where most frontend investigation starts. This guide covers what each panel is for, how to open it on macOS and on Windows or Linux, how to stop execution only on the case you care about, and the console methods that replace a wall of `console.log`. Key bindings below are Chrome's defaults; other browsers bind different keys for the same panels.

## Panels

| Panel | Purpose |
| --- | --- |
| **Elements** | Inspect and edit the live DOM and CSS |
| **Console** | Run JavaScript against the page and read logged output |
| **Sources** | Step through JavaScript and set breakpoints |
| **Network** | Inspect [requests](../06-frontend/03-client-server-communication.md), their headers, timing, and payloads |
| **Performance** | Record and profile runtime activity, feeding the work in [Performance Optimization](../06-frontend/05-performance-optimization.md) |
| **Application** | Inspect [browser storage](../06-frontend/04-browser-technologies.md#browser-storage), service workers, and cached resources |

## Opening a Panel

| Action | macOS | Windows, Linux |
| --- | --- | --- |
| **Open DevTools on the last used panel** | Cmd+Option+I | Ctrl+Shift+I or F12 |
| **Open the Console panel** | Cmd+Option+J | Ctrl+Shift+J |
| **Open Elements in inspect mode** | Cmd+Shift+C | Ctrl+Shift+C |
| **Open the Command Menu** | Cmd+Shift+P | Ctrl+Shift+P |

No key binding opens the other panels directly. Reach them by clicking their tab, or by opening the Command Menu and typing `Show Sources`, `Show Network`, `Show Performance`, or `Show Application`. The complete set is in the [Chrome DevTools keyboard shortcuts reference](https://developer.chrome.com/docs/devtools/shortcuts).

## Conditional Breakpoints

A bare `debugger;` halts every call, which is unusable in a function called hundreds of times. Guard it with the condition that describes the case you are hunting.

```javascript
function processData(data) {
    const result = data.map((item) => item.value * 2);

    if (result.length > 100) {
        debugger; // Halts only on the oversized batch
    }

    return result;
}
```

A `debugger` statement is source code, so it has to be removed before the change is committed. The Sources panel does the same thing without editing the file: right-click a line number, choose **Add conditional breakpoint**, and enter the expression.

## Console Utilities

These methods carry structure that a plain `console.log` loses.

```javascript
const orders = [{ id: 1, total: 20 }, { id: 2, total: 35 }];

console.table(orders);                            // Rows and columns instead of a nested tree
console.group('Checkout');                        // Open an indented, collapsible block
console.groupEnd();                               // Close it
console.time('checkout');                         // Start a named timer
console.timeEnd('checkout');                      // Stop it and log the elapsed time
console.trace('reached the discount branch');     // Log the current call stack
console.assert(orders.length > 0, 'no orders');   // Log only when the condition is false
```
