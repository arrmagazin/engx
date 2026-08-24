---
type: Guide
title: Data Formats
description: Compares data exchange and configuration formats such as JSON and YAML with examples.
tags: [frontend, data-formats, json, yaml]
---

# Data Formats

JSON, YAML, Markdown, XML, CSV, and Parquet trade readability, size, and type fidelity against each other. This is a working reference for picking one and for the parsing traps each carries; shared vocabulary is defined in the [glossary](../00-software-engineering/01-glossary.md).

## JSON

The default payload format of web APIs — [Client-Server Communication](03-client-server-communication.md) covers how REST and GraphQL carry it. Values are limited to string, number, boolean, null, object, and array: no comments, no trailing commas, no date type.

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

Indentation-based configuration format, and a superset of JSON as of YAML 1.2 (2009) — YAML 1.1 is not. Dominant for CI pipelines, Kubernetes, and OpenAPI because it supports comments and reads with less punctuation.

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
| **Comments** | `#` to end of line — the main advantage over JSON |
| **Anchors** | `&name` defines, `*name` reuses a node |
| **Multi-line strings** | `\|` keeps newlines, `>` folds them into spaces |
| **Documents** | `---` separates multiple documents in one file |

**Pitfalls:**

| Pitfall | Example | Fix |
| --- | --- | --- |
| **Norway problem** | `country: NO` parses as boolean `false` under YAML 1.1, which also resolves `yes`, `no`, `on`, and `off` | Quote the value: `"NO"`. The YAML 1.2 core schema resolves only `true` and `false`, but the loader decides which schema applies, so quote regardless |
| **Version strings** | `version: 1.10` parses as the float `1.1`, losing the trailing zero | Quote it: `"1.10"` |
| **Tabs** | Tab characters are invalid for indentation | Use spaces only |
| **Untrusted input** | Some loaders instantiate arbitrary types | Use a safe loader (`yaml.safe_load`, `js-yaml` default) |

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
| **CommonMark** | Strict, unambiguous base specification |
| **GitHub Flavored Markdown (GFM)** | Tables, task lists, strikethrough, autolinks |
| **MDX** | Embedded JSX components |
| **Front matter** | Leading `---` block of YAML metadata |

Markdown source may contain raw HTML, and most renderers pass it through, so treat user-supplied Markdown as untrusted and sanitize the rendered HTML (e.g. with DOMPurify) before inserting it into the page.

## XML

Verbose, schema-oriented format met through existing ecosystems rather than new API design: SOAP services, RSS and Atom feeds, and document formats such as SVG and Office Open XML. It carries attributes alongside elements, namespaces, and external schema validation (XSD).

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
| **Delimiter in value** | `John "Doe", Jr.` splits into extra columns | Quote fields containing the delimiter: `"Doe, Jr."` |
| **Embedded quotes** | `She said "hi"` breaks quoting | Escape by doubling: `"She said ""hi"""` |
| **No types** | `"true"`, `"1"`, `"1.10"` are all strings | Cast explicitly after parsing; don't infer |
| **No standard encoding** | Excel on Windows exports Windows-1252, not UTF-8 | Specify or detect the encoding when reading |
| **Line endings** | CRLF vs. LF differs by OS and tool | Use a CSV parser, not manual `split("\n")` |

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
| **Columnar layout** | Reading one column doesn't require reading the rest — fast for analytical queries |
| **Compression** | Per-column encoding (dictionary, run-length) — much smaller than CSV/JSON |
| **Schema** | Embedded in the file, with types — no inference needed |
| **Splittable** | Row groups can be read independently for parallel or distributed processing |

Expect it on the backend and data-pipeline side (data lakes, exports, warehouse tables), not in frontend request or response bodies.
