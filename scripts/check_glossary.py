#!/usr/bin/env python3
"""Validate glossary definition lists in docs/**/*.md files (see CLAUDE.md).

A glossary entry is a markdown definition list entry (the extended syntax at
markdownguide.org/extended-syntax): a term alone on its line, the definition on
the next line behind a colon, and a blank line before the next term.

    Solution
    : an artificial phenomenon a Team designs for someone outside it

Definition lists are used in this book for exactly one thing, so every one of
them is in scope and no header row is needed to mark them. Comparisons, ladders
and nav tables stay tables and are not read here. Files with no definition list
are skipped, making this safe to run over every doc.

Errors (exit 1) cover the mechanically decidable rules: entries a renderer would
silently fold together, duplicate terms, self-restating definitions, trailing
periods, and pairs of terms that define each other. Indirect loops and oversized
lists print as notes and do not fail the run. The remaining rules in CLAUDE.md —
casing of cross-references, grounding, whether a term earns its row — need human
judgement and are deliberately not checked here.
"""
import re
import sys

DEFINITION_RE = re.compile(r"^:\s+(?P<definition>.*)$")
HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# A term is a bare line of prose. Anything opening a block of its own — a list
# item, a quote, a table row, a heading, an indented code line — is not one.
NOT_A_TERM_RE = re.compile(r"^(\s|[-*+>|#]|\d+\.)")
# The block shapes that read as a continuation of the definition above them, and so
# have to be indented into it. A heading or a table is a structure of its own and
# separates two entries legitimately, so neither is listed here.
DETACHABLE_RE = re.compile(r"^([-*+>]\s|\d+\.\s)")
MAX_TERMS_PER_LIST = 12


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
    """Drop the inline markup that is not prose."""
    text = definition.strip().replace("<br>", " ").replace("<br/>", " ")
    return re.sub(r"[*`_]", "", text).strip()


def parse(text):
    """Return (rows, structure_errors). Each row is (term, definition, line, section).

    Reads the file line by line rather than with one regex, because an entry is
    defined by its neighbours: a line is a term only because the next line is a
    definition, and an entry belongs to the run of entries around it.
    """
    lines = text.splitlines()
    rows, errors = [], []
    section, fence, run = None, None, 0
    index = 0

    def is_term(pos):
        """A bare line whose successor is a definition — that is what makes a term."""
        return (
            pos + 1 < len(lines)
            and lines[pos].strip()
            and not NOT_A_TERM_RE.match(lines[pos])
            and not DEFINITION_RE.match(lines[pos])
            and DEFINITION_RE.match(lines[pos + 1].rstrip())
        )

    def detached_block(pos, _lines=lines):
        """An unindented block sitting between one entry and the next."""
        start = pos
        while start < len(_lines) and not _lines[start].strip():
            start += 1
        if start == pos or start >= len(_lines) or not DETACHABLE_RE.match(_lines[start]):
            return False
        end = start
        while end < len(_lines) and _lines[end].strip():
            end += 1
        while end < len(_lines) and not _lines[end].strip():
            end += 1
        return is_term(end)

    while index < len(lines):
        line = lines[index].rstrip()

        if FENCE_RE.match(line):
            marker = FENCE_RE.match(line).group(1)
            fence = None if fence == marker else (fence or marker)
            index += 1
            continue
        if fence:
            index += 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            if len(heading.group("level")) == 2:
                section = heading.group("title")
            run = 0
            index += 1
            continue

        if DEFINITION_RE.match(line):
            errors.append((index + 1, "definition has no term above it"))
            index += 1
            continue

        if not is_term(index):
            if line.strip():
                run = 0
            index += 1
            continue

        term, index = line.strip(), index + 1
        while index < len(lines) and DEFINITION_RE.match(lines[index].rstrip()):
            definition = DEFINITION_RE.match(lines[index].rstrip()).group("definition")
            start = index
            index += 1
            # A line the author broke on purpose, with a trailing backslash, carries on
            # the same definition. Collect it, so a term named after the break still
            # counts as a reference.
            while index < len(lines) and definition.endswith("\\") and lines[index].strip():
                definition = definition[:-1] + " " + lines[index].strip()
                index += 1
            rows.append((term, definition, start + 1, section))
            # Two ways a definition loses content silently, both of which render
            # without an error and so cannot be caught by reading the output.
            #
            # A non-blank line here is folded into the definition above it, so the
            # break the author wrote disappears — and if that line was the next term,
            # the whole entry disappears with it. This is the definition-list version
            # of a raw newline breaking a table row.
            while index < len(lines) and lines[index].strip() and not DEFINITION_RE.match(lines[index].rstrip()):
                errors.append((index + 1, f"line after the definition of '{term}' is folded into it, losing the break; end the line above with a backslash, or indent this line by four spaces to make it a block of the definition"))
                index += 1
            # An unindented block between two entries detaches from the definition
            # above it: the renderer closes the list, emits the block on its own, and
            # opens a second list. Only flagged between entries, where it cannot be
            # the prose that follows the glossary.
            if detached_block(index):
                errors.append((index + 2, f"block after the definition of '{term}' is not indented, so it detaches from the definition and splits the list in two; indent it by four spaces"))

        run += 1
        if run == MAX_TERMS_PER_LIST + 1:  # once per run, not once per term past the line
            errors.append((index, f"__note__more than {MAX_TERMS_PER_LIST} terms run together here; consider splitting them under a new heading"))

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
