#!/usr/bin/env python3
"""Validate OKF v0.2 frontmatter on docs/**/*.md files (see CLAUDE.md)."""
import re
import sys

REQUIRED_FIELDS = ["type", "title", "description", "tags"]
BANNED_FIELDS = ["sources", "generated", "verified", "status"]
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, None
    block = match.group(1)
    fields = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields, match.end()


def find_h1(text, after):
    for line in text[after:].splitlines():
        if line.startswith("# "):
            return line[2:].strip()
        if line.strip():
            break
    return None


def check_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()

    errors = []
    fields, after = parse_frontmatter(text)
    if fields is None:
        return [f"{path}: missing OKF frontmatter block (must start with '---' ... '---')"]

    for field in REQUIRED_FIELDS:
        if field not in fields or not fields[field]:
            errors.append(f"{path}: missing required field '{field}'")

    if fields.get("type") and fields["type"] != "Guide":
        errors.append(f"{path}: 'type' must be 'Guide', got '{fields['type']}'")

    description = fields.get("description", "")
    if description and len(description) > 140:
        errors.append(f"{path}: 'description' is {len(description)} chars, keep under ~140")

    tags_raw = fields.get("tags", "")
    if tags_raw:
        if not (tags_raw.startswith("[") and tags_raw.endswith("]")):
            errors.append(f"{path}: 'tags' must be a bracketed list, got '{tags_raw}'")
        else:
            tags = [t.strip() for t in tags_raw[1:-1].split(",") if t.strip()]
            if not tags:
                errors.append(f"{path}: 'tags' list is empty")
            for tag in tags:
                if not TAG_RE.match(tag):
                    errors.append(f"{path}: tag '{tag}' must be lowercase, kebab-or-single-word")

    for field in BANNED_FIELDS:
        if field in fields:
            errors.append(f"{path}: OKF optional field '{field}' is not used in this repo")

    h1 = find_h1(text, after)
    title = fields.get("title")
    if title and h1 and title != h1:
        errors.append(f"{path}: frontmatter title '{title}' does not match H1 '{h1}'")
    elif title and h1 is None:
        errors.append(f"{path}: no H1 found after frontmatter to match against title")

    return errors


def main(paths):
    all_errors = []
    for path in paths:
        all_errors.extend(check_file(path))

    if all_errors:
        print("OKF frontmatter check failed:\n")
        for error in all_errors:
            print(f"  - {error}")
        print(f"\n{len(all_errors)} issue(s) in {len(paths)} file(s). See CLAUDE.md for the OKF convention.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
