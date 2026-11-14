---
type: Guide
title: Accessibility (WCAG)
description: The WCAG version and conformance level to build against, the four POUR principles, and ARIA patterns for common markup.
tags: [frontend, accessibility, wcag, aria]
---

Accessibility is a [quality attribute](../02-architecture/01-quality-attributes.md) with a published standard behind it: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), a W3C Recommendation since 5 October 2023. This page gives frontend developers the version and level to build against, the four principles the success criteria are grouped under, and the ARIA patterns that recur in everyday markup.

## Version and Conformance Level

WCAG 2.2 is the current W3C Recommendation and the version to cite. Conformance is claimed at one of three levels — A, AA, or AAA — in increasing strictness, each including the level below it.

Target **AA**. Most legal and procurement policies that name a level name AA, so an audit, a public-sector tender, or a customer questionnaire will ask about it. Each law names its own WCAG version:

| Law or standard | WCAG version |
| --- | --- |
| **US Section 508 standards** | 2.0 AA |
| **US ADA Title II rule (2024)** | 2.1 AA |
| **EU EN 301 549 v3.2.1** | 2.1 AA for web content ([W3C WAI summary](https://www.w3.org/WAI/policies/european-union/)) |

- EN 301 549 is the harmonised standard under the Web Accessibility Directive for the public sector. As of October 2026 no version of it has been formally cited under the European Accessibility Act, but it is the usual working reference for that law; check the EU Official Journal for later citations.
- WCAG 2.2 is designed to be backward compatible, so building to 2.2 AA meets the WCAG part of each law above. The laws also cover documents, software, and hardware.
- Rules differ by country and change over time; this is not legal advice.

State the version and the level together. "WCAG 2.2 AA" is a claim someone can check; "WCAG compliant" on its own says nothing.

## The Four Principles (POUR)

WCAG groups every success criterion under one of four principles, abbreviated POUR.

Perceivable
: Content reaching the user through more than one sense — text alternatives, captions, and enough contrast that nothing is carried by sight or sound alone

Operable
: Every control reachable without a mouse — keyboard access, a visible focus indicator, and no time limit or motion the user cannot pause or extend

Understandable
: Predictable behavior and plain language — readable text, consistent navigation, and error messages that name what went wrong and how to fix it

Robust
: Markup that assistive technology can parse reliably — valid HTML, accurate names and roles, and state exposed through attributes rather than visual styling alone

## ARIA Patterns

ARIA attributes annotate the [DOM](02-browser-technologies.md) the browser already exposes. They add names, roles, and states — nothing else. They add no behavior, so keyboard handling and focus management remain your code's job.

- Use a native HTML element whenever one carries the semantics you need. Use ARIA only when none does.
- The [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) documents the full keyboard and state contract for each widget pattern.

| Pattern | Key Attributes | Use When |
| --- | --- | --- |
| **Live Region** | `aria-live`, `aria-atomic` | Content changes without a page load and the change must be announced |
| **Icon-Only Button** | `aria-label`, `aria-hidden` | The control's only visible content is a glyph |
| **Image With Extended Description** | `alt`, `aria-describedby` | A short alternative cannot carry the whole meaning |
| **Expandable Control** | `aria-expanded`, `aria-controls`, `hidden` | One control shows and hides another region |

### Live Region

- `aria-live="polite"` queues the announcement until the user is idle.
- `aria-atomic="true"` makes the region read as a whole, not only the changed part.
- The element must exist in the DOM before the update, or there is nothing for the screen reader to watch.

```html
<div aria-live="polite" aria-atomic="true">Status: order saved</div>
```

### Icon-Only Button

The label lives on the control and the glyph is hidden from the accessibility tree, so the button is announced once, by name.

```html
<button aria-label="Close dialog">
  <span aria-hidden="true">&times;</span>
</button>
```

### Image With Extended Description

`alt` carries the short equivalent. `aria-describedby` points at visible prose for the detail that does not fit in it. Write the description for someone who cannot see the image at all.

```html
<img src="sales-by-quarter.png"
     alt="Bar chart of sales by quarter, rising in every quarter"
     aria-describedby="chart-details">
<p id="chart-details">Sales rise in each quarter of the year, with the
  largest single increase between the third and the fourth quarter.</p>
```

### Expandable Control

- `aria-expanded` reports the current state.
- `aria-controls` names the region the control governs.
- `hidden` keeps the collapsed region out of both the page and the accessibility tree.

Your script updates `aria-expanded` and `hidden` together on every toggle.

```html
<button aria-expanded="false" aria-controls="menu">Menu</button>
<div id="menu" hidden><!-- Menu content --></div>
```
