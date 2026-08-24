#!/usr/bin/env python3
"""Validate relative links and heading anchors in docs/**/*.md files."""
import os
import re
import sys
from urllib.parse import unquote

LINK_RE = re.compile(r"(?P<bang>!?)\[(?P<text>[^\[\]]*)\]\((?P<target>[^()]*)\)")
EXTERNAL_RE = re.compile(r"^(?:[a-z][a-z0-9+.\-]*:|//)", re.IGNORECASE)
HEADING_RE = re.compile(r"^(?P<level>#{1,6})\s+(?P<title>.+?)\s*$")
INLINE_LINK_RE = re.compile(r"!?\[(?P<text>[^\[\]]*)\]\([^()]*\)")
UNSLUGGABLE_RE = re.compile(r"[^\w\- ]", re.UNICODE)
FENCE_RE = re.compile(r"^ {0,3}(?P<marker>`{3,}|~{3,})\s*(?P<info>.*)$")

_anchor_cache = {}


def prose_lines(text):
    """Yield (lineno, line) for every line outside a fenced code block.

    Several docs show markdown samples containing '#' lines and bracket
    syntax; those are neither headings nor links. A fence closes only on a
    marker of the same character that is at least as long as the one that
    opened it, so a '~~~' inside a '```' block is ordinary content.
    """
    fence = None
    for lineno, line in enumerate(text.splitlines(), 1):
        match = FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = match.group("marker")
                continue
        else:
            closes = (
                match
                and match.group("marker")[0] == fence[0]
                and len(match.group("marker")) >= len(fence)
                and not match.group("info").strip()
            )
            if closes:
                fence = None
            continue
        yield lineno, line


def strip_inline_markdown(title):
    """Drop the markup a renderer would not put in the heading's text."""
    text = INLINE_LINK_RE.sub(lambda m: m.group("text"), title)
    return text.replace("*", "").replace("`", "")


def slugify(title):
    """The anchor GitHub generates for a heading.

    Lowercase the text, drop every character that is not a word character, a
    space, or a hyphen, then replace spaces with hyphens. Dropping a character
    leaves the spaces around it behind, so 'Violations & Smells' becomes
    'violations--smells'.
    """
    text = strip_inline_markdown(title).strip().lower()
    return UNSLUGGABLE_RE.sub("", text).replace(" ", "-")


def heading_anchors(path):
    """Every anchor a reader can jump to in `path`, in document order.

    Repeated headings collide, and GitHub disambiguates them by appending
    '-1', '-2' and so on to every occurrence after the first.
    """
    key = os.path.realpath(path)
    if key in _anchor_cache:
        return _anchor_cache[key]

    with open(path, encoding="utf-8") as f:
        text = f.read()

    anchors, seen = [], {}
    for _, line in prose_lines(text):
        heading = HEADING_RE.match(line)
        if not heading:
            continue
        slug = slugify(heading.group("title"))
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        anchors.append(slug if count == 0 else f"{slug}-{count}")

    _anchor_cache[key] = anchors
    return anchors


def destination(target):
    """Strip an optional link title, leaving the destination."""
    return target.strip().split(None, 1)[0] if target.strip() else ""


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    errors = []
    for lineno, line in prose_lines(text):
        for match in LINK_RE.finditer(line):
            if match.group("bang"):
                continue
            target = destination(match.group("target"))
            if not target or EXTERNAL_RE.match(target):
                continue

            relative, _, anchor = target.partition("#")
            if relative:
                resolved = os.path.normpath(
                    os.path.join(os.path.dirname(path), unquote(relative))
                )
                if not os.path.exists(resolved):
                    errors.append(f"{path}:{lineno}: link target does not exist: {target}")
                    continue
            else:
                resolved = path

            if not anchor or not resolved.endswith(".md"):
                continue
            if unquote(anchor) not in heading_anchors(resolved):
                errors.append(
                    f"{path}:{lineno}: no heading in {os.path.basename(resolved)} "
                    f"generates the anchor '#{anchor}'"
                )
    return errors


def main(paths):
    all_errors = []
    for path in paths:
        all_errors.extend(check_file(path))

    if all_errors:
        print("Link check failed:\n")
        for error in all_errors:
            print(f"  - {error}")
        files = len({e.split(":", 1)[0] for e in all_errors})
        print(f"\n{len(all_errors)} issue(s) in {files} of {len(paths)} file(s) checked.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
