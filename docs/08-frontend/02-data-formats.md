# Data Formats

## JSON

The dominant web data exchange format.

```json
{
    "users": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "active": true,
            "scores": [95, 87, 92]
        }
    ],
    "total": 1
}
```

## YAML

Indentation-based superset of JSON. Dominant for configuration (CI pipelines, Kubernetes, OpenAPI) because it supports comments and reads with less punctuation.

```yaml
# Same data as the JSON example above
users:
    - id: 1
      name: John Doe
      email: john@example.com
      active: true
      scores: [95, 87, 92]
total: 1
```

| Feature | Notes |
| --- | --- |
| Comments | `#` to end of line — the main advantage over JSON |
| Anchors | `&name` defines, `*name` reuses a node |
| Multi-line strings | `\|` keeps newlines, `>` folds them into spaces |
| Documents | `---` separates multiple documents in one file |

**Pitfalls:**

| Pitfall | Example | Fix |
| --- | --- | --- |
| Norway problem | `country: NO` parses as boolean `false` | Quote the value: `"NO"` |
| Version strings | `version: 1.10` becomes number `1.1` | Quote it: `"1.10"` |
| Tabs | Tab characters are invalid for indentation | Use spaces only |
| Untrusted input | Some loaders instantiate arbitrary types | Use a safe loader (`yaml.safe_load`, `js-yaml` default) |

## Markdown

Plain-text format for documents, converted to HTML for display. Used for READMEs, docs sites, and LLM output.

```markdown
# Heading

Text with **bold**, *italic*, `code`, and a [link](https://example.com).

- List item
- Another item

| Column | Column |
| --- | --- |
| Cell | Cell |
```

| Flavor | Adds |
| --- | --- |
| CommonMark | Strict, unambiguous base specification |
| GitHub Flavored Markdown (GFM) | Tables, task lists, strikethrough, autolinks |
| MDX | Embedded JSX components |
| Front matter | Leading `---` block of YAML metadata |

Rendered Markdown allows raw HTML by default, so treat user-supplied Markdown as untrusted and sanitize the HTML output (e.g. DOMPurify) before inserting it into the page.

## XML

Still relevant for enterprise systems and document formats.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<users>
    <user id="1">
        <name>John Doe</name>
        <email>john@example.com</email>
    </user>
</users>
```
