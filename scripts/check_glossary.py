#!/usr/bin/env python3
"""Validate glossary term tables in docs/**/*.md files (see CLAUDE.md).

A "glossary table" is a markdown table introduced by the header

    | Concept | Definition |

(or `| Component | Definition |`), whose rows look like `| **Term** | definition |`.
Other tables in the repo use bold first columns for things that are not term
definitions, so the header is what makes a table in scope. Files with no
glossary table are skipped, making this safe to run over every doc.

Errors (exit 1) cover the mechanically decidable rules: broken table rows,
duplicate terms, self-restating definitions, trailing periods, and pairs of
terms that define each other. Indirect loops and oversized tables print as
notes and do not fail the run. The remaining rules in CLAUDE.md — casing of
cross-references, grounding, whether a term earns its row — need human
judgement and are deliberately not checked here.
"""
import re
import sys

ROW_RE = re.compile(r"^\|\s*\*\*(?P<term>[^*|]+?)\*\*\s*\|(?P<definition>.*)$")
HEADER_RE = re.compile(r"^\|\s*(Concept|Component)\s*\|\s*Definition\s*\|\s*$")
HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*$")
MAX_ROWS_PER_TABLE = 12


def aliases(term):
    """Singular and plural spellings a definition might use to refer to `term`."""
    forms = {term}
    if term.endswith("ies"):
        forms.add(term[:-3] + "y")
    elif term.endswith("s"):
        forms.add(term[:-1])
    else:
        forms.add(term + "s")
        if term.endswith("y"):
            forms.add(term[:-1] + "ies")
    return forms


def strip_markup(definition):
    """Drop the trailing cell pipe and inline markup that is not prose."""
    text = definition.strip()
    if text.endswith("|"):
        text = text[:-1]
    text = text.replace("<br>", " ")
    return re.sub(r"[*`_]", "", text).strip()


def parse(text):
    """Return (rows, structure_errors). Each row is (term, definition, line, section)."""
    rows, errors = [], []
    section, in_table, in_glossary, table_rows = None, False, False, 0

    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        heading = HEADING_RE.match(line)

        if line.startswith("|"):
            if not in_table:
                in_glossary = bool(HEADER_RE.match(line))
            in_table, table_rows = True, table_rows + 1
            if not in_glossary:
                continue
            if not line.endswith("|"):
                errors.append((lineno, "table row does not end with '|' (a raw newline inside a cell breaks the table)"))
            match = ROW_RE.match(line)
            if match:
                rows.append((match.group("term").strip(), match.group("definition"), lineno, section))
            continue

        if in_table and in_glossary and line.strip() and not heading:
            errors.append((lineno, f"line inside a table does not start with '|': {line.strip()[:48]!r}"))
            continue

        if not line.strip() or heading:
            if in_glossary and table_rows - 2 > MAX_ROWS_PER_TABLE:
                errors.append((lineno, f"__note__table has {table_rows - 2} terms, over the {MAX_ROWS_PER_TABLE}-row guideline; consider splitting it"))
            in_table, in_glossary, table_rows = False, False, 0
        if heading and len(heading.group("level")) == 2:
            section = heading.group("title")

    return rows, errors


def find_cycles(graph):
    """Return each distinct reference cycle as a list of terms."""
    cycles, state, stack = [], {}, []

    def visit(node):
        state[node] = "open"
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            if state.get(nxt) == "open":
                cycles.append(stack[stack.index(nxt):] + [nxt])
            elif nxt not in state:
                visit(nxt)
        stack.pop()
        state[node] = "done"

    for node in sorted(graph):
        if node not in state:
            visit(node)

    seen, unique = set(), []
    for cycle in cycles:
        key = frozenset(cycle)
        if key not in seen:
            seen.add(key)
            unique.append(cycle)
    return unique


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    rows, structure = parse(text)
    if not rows:
        return [], []

    errors = [f"{path}:{n}: {m}" for n, m in structure if not m.startswith("__note__")]
    notes = [f"{path}:{n}: {m[len('__note__'):]}" for n, m in structure if m.startswith("__note__")]

    seen = {}
    for term, _, lineno, _ in rows:
        if term in seen:
            errors.append(f"{path}:{lineno}: '{term}' is already defined on line {seen[term]}")
        else:
            seen[term] = lineno

    # Map every spelling of every defined term back to its canonical term.
    lookup = {}
    for term in seen:
        for form in aliases(term):
            lookup.setdefault(form, term)

    graph = {}
    for term, definition, lineno, _ in rows:
        prose = strip_markup(definition)
        if prose.endswith("."):
            errors.append(f"{path}:{lineno}: definition of '{term}' ends with a period")

        targets = set()
        for form, canonical in lookup.items():
            if not re.search(r"(?<![\w-])" + re.escape(form) + r"(?![\w-])", prose):
                continue
            if canonical == term:
                errors.append(f"{path}:{lineno}: definition of '{term}' restates the term")
            else:
                targets.add(canonical)
        graph[term] = targets

    for cycle in find_cycles(graph):
        trail = " -> ".join(cycle)
        if len(cycle) == 3:  # A -> B -> A: the two terms define each other
            errors.append(f"{path}:{seen[cycle[0]]}: '{cycle[0]}' and '{cycle[1]}' define each other ({trail}); state the relationship once, in one direction")
        else:
            notes.append(f"{path}:{seen[cycle[0]]}: indirect reference loop {trail}")


    return errors, notes


def main(paths):
    all_errors, all_notes = [], []
    for path in paths:
        errors, notes = check_file(path)
        all_errors.extend(errors)
        all_notes.extend(notes)

    if all_notes:
        print("Glossary notes (not failures):\n")
        for note in all_notes:
            print(f"  - {note}")
        print()

    if all_errors:
        print("Glossary check failed:\n")
        for error in all_errors:
            print(f"  - {error}")
        print(f"\n{len(all_errors)} issue(s) in {len(paths)} file(s). See CLAUDE.md ('Glossary conventions').")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
