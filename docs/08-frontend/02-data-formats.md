---
type: Guide
title: Data Formats
description: Compares data exchange and configuration formats such as JSON and YAML with examples.
tags: [frontend, data-formats, json, yaml]
---

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

## CSV

Flat, row-based text format for tabular data. No nested structures or types — every value is a string until the reader parses it.

```csv
id,name,email,active
1,John Doe,john@example.com,true
```

| Pitfall | Example | Fix |
| --- | --- | --- |
| Delimiter in value | `John "Doe", Jr.` splits into extra columns | Quote fields containing the delimiter: `"Doe, Jr."` |
| Embedded quotes | `She said "hi"` breaks quoting | Escape by doubling: `"She said ""hi"""` |
| No types | `"true"`, `"1"`, `"1.10"` are all strings | Cast explicitly after parsing; don't infer |
| No standard encoding | Excel exports often use Latin-1, not UTF-8 | Detect or specify encoding when reading |
| Line endings | CRLF vs LF differs by OS/tool | Use a CSV parser, not manual `split("\n")` |

Always parse and generate with a library (e.g. Papa Parse, `csv-parse`) rather than splitting on commas — quoting and escaping rules make naive parsing unsafe.

## Parquet

Columnar binary format for large datasets, built for analytics rather than transport. Not human-readable; used with data tools (Spark, Pandas, DuckDB) rather than in application code.

```
row group
├── column: id       [1, 2, 3, ...]
├── column: name     ["John Doe", "Jane Roe", ...]
└── column: active   [true, false, ...]
```

| Feature | Notes |
| --- | --- |
| Columnar layout | Reading one column doesn't require reading the rest — fast for analytical queries |
| Compression | Per-column encoding (dictionary, run-length) — much smaller than CSV/JSON |
| Schema | Embedded in the file, with types — no inference needed |
| Splittable | Row groups can be read independently for parallel/distributed processing |

Expect it on the backend/data-pipeline side (data lakes, exports, warehouse tables), not in frontend request/response bodies.
