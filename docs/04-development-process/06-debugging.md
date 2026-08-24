---
type: Guide
title: Debugging
description: Summarizes Chrome DevTools panels, shortcuts, and JavaScript console debugging techniques.
tags: [debugging, tooling, frontend]
---

# Debugging

## Chrome DevTools

| Panel | Purpose | Shortcut |
| --- | --- | --- |
| Elements | DOM inspection | Ctrl+Shift+C |
| Console | JavaScript execution | Ctrl+Shift+J |
| Sources | JS debugging, breakpoints | Ctrl+Shift+P → Sources |
| Network | Request analysis | Ctrl+Shift+E |
| Performance | Profiling | Ctrl+Shift+P → Performance |
| Application | Storage and resources | Ctrl+Shift+P → Application |

**Debugging techniques:**

```javascript
function processData(data) {
    const result = data.map(item => item.value * 2);

    // Conditional breakpoint: result.length > 100
    debugger;

    return result;
}

// Console utilities
console.table(array);                          // Tabular view
console.group('Group'); console.groupEnd();    // Grouped logs
console.time('op'); console.timeEnd('op');     // Timing
console.trace('Here');                         // Stack trace
console.assert(condition, 'msg');              // Assertions
```
