---
type: Guide
title: Data Formats
description: Compares JSON, YAML, Markdown, XML, CSV, and Parquet, and lists the parsing traps each one carries.
tags: [frontend, data-formats, json, yaml]
---

Data formats trade readability, size, and type fidelity against each other. This is a working reference for picking one and for the parsing traps each carries.

| Format | Use it for | Watch out for |
| --- | --- | --- |
| **JSON** | API payloads ([Client-Server Communication](06-client-server-communication.md)) | No comments, no trailing commas, no date type — dates travel as ISO 8601 strings |
| **YAML** | Configuration (CI, Kubernetes, OpenAPI) | Implicit typing; tabs are invalid indentation |
| **Markdown** | Documents rendered to HTML | Raw HTML passes through, so sanitize user-supplied Markdown after rendering |
| **XML** | Existing ecosystems: SOAP, RSS/Atom, SVG, Office files | Verbosity; rarely chosen for a new API |
| **CSV** | Flat tabular exchange | No types, no standard encoding |
| **Parquet** | Large analytical datasets (Spark, Pandas, DuckDB) | Not human-readable |

## YAML

YAML 1.2 is a superset of JSON; YAML 1.1 is not. It dominates configuration because it allows `#` comments and needs less punctuation, and it adds anchors (`&name` defines, `*name` reuses a node) and multi-line strings (`|` keeps newlines, `>` folds them).

| Pitfall | Example | Fix |
| --- | --- | --- |
| **Norway problem** | `country: NO` parses as boolean `false` under YAML 1.1, which also resolves `yes`, `no`, `on`, and `off` | Quote the value: `"NO"`. YAML 1.2 resolves only `true` and `false`, but the loader decides which schema applies, so quote anyway |
| **Version strings** | `version: 1.10` parses as the float `1.1` | Quote it: `"1.10"` |
| **Untrusted input** | Some loaders instantiate arbitrary types | Use a safe loader (`yaml.safe_load`, `js-yaml` default) |

## CSV

Every value is a string until the reader parses it, and there is no nesting.

| Pitfall | Example | Fix |
| --- | --- | --- |
| **Delimiter in value** | `Doe, Jr.` splits into two columns | Quote the field: `"Doe, Jr."` |
| **Embedded quotes** | `She said "hi"` breaks quoting | Double them: `"She said ""hi"""` |
| **No types** | `"true"`, `"1"`, `"1.10"` are all strings | Cast explicitly after parsing |
| **No standard encoding** | Excel's plain CSV export uses the system code page, not UTF-8 | Specify or detect the encoding when reading |

Parse and generate CSV with a library, never by splitting on commas and newlines: the quoting rules make naive parsing unsafe.

## Parquet

A columnar binary format built for analytics, not transport. Reading one column does not read the rest, per-column encoding makes files much smaller than CSV or JSON, the typed schema is embedded so nothing is inferred, and row groups can be read in parallel.
