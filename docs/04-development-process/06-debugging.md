---
type: Guide
title: Debugging
description: A method for finding a bug — reproduce, reduce, hypothesize, bisect, verify — and the Chrome DevTools panels and console utilities.
tags: [debugging, devtools, troubleshooting, tooling]
---

# Debugging

Debugging is a search for the one place where what a program does stops matching what you believe it does. This guide covers the method that narrows that search — reproduce, reduce, hypothesize, bisect, verify — and then the Chrome DevTools panels, breakpoints, and console utilities that carry it out in the browser.

## A Systematic Method

The steps below are ordered because each one makes the next cheaper. Skipping ahead to a fix is what turns a twenty-minute bug into an afternoon.

### Reproduce Before You Change Anything

A failure you cannot trigger on demand cannot be fixed, only guessed at, because nothing distinguishes a real fix from a coincidence. Pin down the exact input, environment, and sequence of steps that produce it, then run them twice to confirm they produce it both times. Intermittent failures still count: if it fails one run in twenty, that is the reproduction, and any fix has to survive far more than twenty runs before you believe it.

A reliable reproduction is a failing test. Once you can state the input and the wrong output, write it down as a test case and let it drive the fix — [Test-Driven Development](05-testing.md#test-driven-development-tdd) covers that loop. The test then does double duty: it tells you when the bug is gone, and it stays in the suite to tell you if it returns.

### Reduce to the Smallest Failing Case

Strip the reproduction until removing anything else makes the failure disappear. Delete records from the input, drop fields from the request body, take steps out of the sequence, and cut the page down to the single component. Everything you remove without changing the outcome is something that is not the cause, and the case that survives is often small enough that the bug is visible by reading it.

### Form One Falsifiable Hypothesis

State what you think is wrong in a form that one check can prove false: "the total is wrong because the discount is applied before tax rather than after," not "something is off in the checkout math." Then run the single experiment that settles it, and change one thing per experiment — two changes and a passing test leave you unable to say which one mattered, so put back whatever did not help before trying the next idea. Explaining the hypothesis out loud, to a colleague or to nobody in particular, tends to expose the step you have been assuming rather than checking.

### Bisect the Search Space

Every good debugging step halves what is left. If the code worked last week and fails today, the fault is in the commits between. If a request is correct at the gateway and wrong at the database, the fault is in one hop. Pick the midpoint, test it, discard the clean half, and repeat.

`git bisect` mechanizes this over history. Mark one commit bad and one good, and git checks out the midpoint for you until only one commit is left.

```bash
git bisect start
git bisect bad                  # The current commit fails
git bisect good v1.4.0          # This one did not

# Git checks out a commit in the middle; test it, then report the result
git bisect good                 # Or: git bisect bad

# Repeat until git names the first bad commit, then restore your branch
git bisect reset
```

`git bisect run ./check.sh` does the whole search unattended: any command that exits `0` for good and non-zero for bad drives it. This is where the reproduction from the first step pays off a second time, because a failing test is exactly such a command. The answer is the first commit where the behavior changed, which is a far smaller diff to read than the whole feature. Small, self-contained commits are what keep bisect useful — see [Version Control](01-version-control.md) for how branch lifetime shapes that history.

Adding logging everywhere and staring at the output is the usual alternative, and it loses on two counts. It searches linearly rather than by halves, so a range of a thousand commits costs about ten bisect steps and an unbounded amount of reading. It also prints only what you already suspected was relevant, so a wrong guess about the cause produces a wall of output that confirms nothing. Bisect needs no theory about the cause at all — only a verdict of pass or fail.

### Verify the Fix

Run the reproduction again and confirm it now passes, then revert the fix and confirm the failure comes back. A change that passes but whose removal does not restore the bug did not fix it; either something else did, or the reproduction was never reliable. Run the rest of the suite as well, and strip the temporary logging, `debugger;` statements, and hard-coded values you added along the way.

## Logging

Logging earns its place where a debugger cannot go: production, other people's machines, timing-dependent failures that vanish the moment execution stops, and anything asynchronous. Log the values the current hypothesis turns on rather than everything in scope, carry enough identifying context to tie a line back to one request or one record, and delete the lines once the bug is closed. Debug output left behind becomes the noise that hides the next failure.

## Chrome DevTools

Chrome DevTools is the debugger built into the browser, and it is where a frontend investigation runs the steps above. Key bindings below are Chrome's defaults; other browsers bind different keys for the same panels.

### Panels

| Panel | Purpose |
| --- | --- |
| **Elements** | Inspect and edit the live DOM and CSS |
| **Console** | Run JavaScript against the page and read logged output |
| **Sources** | Step through JavaScript and set breakpoints |
| **Network** | Inspect [requests](../03-system-design/06-client-server-communication.md), their headers, timing, and payloads |
| **Performance** | Record and profile runtime activity, feeding the work in [Performance Optimization](../06-frontend/03-performance-optimization.md) |
| **Application** | Inspect [browser storage](../06-frontend/02-browser-technologies.md#browser-storage), service workers, and cached resources |

### Opening a Panel

| Action | macOS | Windows, Linux |
| --- | --- | --- |
| **Open DevTools on the last used panel** | Cmd+Option+I | Ctrl+Shift+I or F12 |
| **Open the Console panel** | Cmd+Option+J | Ctrl+Shift+J |
| **Open Elements in inspect mode** | Cmd+Shift+C | Ctrl+Shift+C |
| **Open the Command Menu** | Cmd+Shift+P | Ctrl+Shift+P |

No key binding opens the other panels directly. Reach them by clicking their tab, or by opening the Command Menu and typing `Show Sources`, `Show Network`, `Show Performance`, or `Show Application`. The complete set is in the [Chrome DevTools keyboard shortcuts reference](https://developer.chrome.com/docs/devtools/shortcuts).

### Conditional Breakpoints

A bare `debugger;` halts every call, which is unusable in a function called hundreds of times. Guard it with the condition that describes the case you are hunting — the smallest failing case from the second step is usually already that condition.

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

### Console Utilities

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
