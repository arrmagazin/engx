# WCAG (Accessibility)

| Principle | Description |
| --- | --- |
| **Perceivable** | Content presentable in ways users can perceive |
| **Operable** | UI components must be operable |
| **Understandable** | Information and operation must be clear |
| **Robust** | Content works with assistive technologies |

```html
<!-- Live region for dynamic updates -->
<div aria-live="polite" aria-atomic="true">Status: {{ message }}</div>

<!-- Hidden decorative icon with label -->
<button aria-label="Close dialog">
    <span aria-hidden="true">&times;</span>
</button>

<!-- Image with extended description -->
<img src="chart.png" alt="Sales chart showing 25% growth in Q4"
     aria-describedby="chart-details">
<p id="chart-details">Detailed description...</p>

<!-- Expandable control -->
<button aria-expanded="false" aria-controls="menu">Menu</button>
<div id="menu" hidden><!-- Menu content --></div>
```
