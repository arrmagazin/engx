#!/usr/bin/env python3
"""Assemble docs/ into one document and render it as an EPUB and a PDF.

Stdlib only, like the three checkers. Pandoc does the rendering. This module does
the part pandoc cannot: put the files in reading order, demote their headings so a
folder reads as a chapter, and turn cross-document links into intra-document
anchors so navigation still works when 57 files become one.

    python3 scripts/build_book.py            # both formats into build/
    python3 scripts/build_book.py --epub      # one format
    python3 scripts/build_book.py --markdown  # assemble only, render nothing
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BUILD = ROOT / "build"
METADATA = ROOT / "book" / "metadata.yaml"

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})(\s+\S.*)$")
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]*)\)")
IMAGE_BLOCK_RE = re.compile(r"^!\[[^\]]*\]\([^)]*\)[ \t]*\n\n?", re.M)
UNSLUGGABLE_RE = re.compile(r"[^\w\- ]")
THEMATIC_BREAK_RE = re.compile(r"^ {0,3}-{3,}[ \t]*$")
TITLE_RE = re.compile(r"^title:[ \t]*(.+?)[ \t]*$", re.M)
EXPLICIT_ID_RE = re.compile(r"\{#([^}]+)\}\s*$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://")

# The book uses box-drawing characters for diagrams and a few maths symbols in
# prose. TeX's default Latin Modern has none of them, so the PDF needs fonts that
# do. These two are present on macOS and verified to cover every character the
# book uses; if either is missing the PDF still builds, with glyphs dropped.
# A bare '---' in the book is a horizontal rule, never metadata. normalize_thematic_breaks
# removes the other readings; this removes the one it cannot.
PANDOC_READER = "markdown-yaml_metadata_block"

# Two typesetting problems the book creates for itself.
#
# Identifiers like iam.disableServiceAccountKeyCreation are unbreakable in a
# monospace font and run into the margin; seqsplit adds breakpoints TeX uses only
# when it must, and breaks without a hyphen, which is right for code.
#
# Comparison tables carry prose in four columns, so a step down inside a table keeps
# them on the measure without shrinking the body text. Inside a table the plain
# \\texttt is restored: columns are narrow enough that seqsplit would break short
# tokens like split("\\n") mid-word, which reads as two tokens. A table cell may then
# run a few points wide, which is the better of the two faults.
PDF_HEADER_INCLUDES = (
    r"header-includes="
    r"\usepackage{etoolbox}"
    r"\usepackage{seqsplit}"
    r"\let\oldtexttt\texttt"
    r"\renewcommand{\texttt}[1]{\oldtexttt{\seqsplit{#1}}}"
    r"\AtBeginEnvironment{longtable}{\small\let\texttt\oldtexttt}"
    r"\AtBeginEnvironment{tabular}{\small\let\texttt\oldtexttt}"
)

PDF_MAIN_FONT = "Times New Roman"
PDF_MONO_FONT = "Menlo"


def slugify(title):
    """The anchor a renderer generates for a heading. Mirrors check_links.slugify."""
    text = title.replace("*", "").replace("`", "").strip().lower()
    return UNSLUGGABLE_RE.sub("", text).replace(" ", "-")


def shift_headings(text, by=1):
    """Demote every ATX heading by `by` levels, ignoring fenced code blocks."""
    out, fence = [], None
    for line in text.splitlines(keepends=True):
        bare = line.rstrip("\n")
        fence_match = FENCE_RE.match(bare)
        if fence_match:
            marker = fence_match.group(1)[0]
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            out.append(line)
            continue
        heading = HEADING_RE.match(bare) if fence is None else None
        if heading:
            level = len(heading.group(1)) + by
            if level > 6:
                raise ValueError(f"heading would exceed level 6: {bare!r}")
            out.append("#" * level + heading.group(2) + line[len(bare):])
            continue
        out.append(line)
    return "".join(out)


def split_frontmatter(text):
    """Return (title, body) and drop the frontmatter block."""
    if not text.startswith("---\n"):
        raise ValueError("file does not start with frontmatter")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    title = TITLE_RE.search(text[4:end + 1])
    if not title:
        raise ValueError("frontmatter has no title")
    return title.group(1), text[end + len("\n---\n"):].lstrip("\n")


def rewrite_links(text, source, anchors):
    """Rewrite one document's links for life inside a single assembled document.

    `source` is the document's path relative to docs/. A link to another document
    becomes an anchor — its own if the link carried one, otherwise the target
    document's title. A link to a file outside docs/ (an image) becomes a path
    relative to the repository root, which is where pandoc is pointed.
    """
    source_dir = (DOCS / source).parent

    def replace(match):
        bang, label, target = match.groups()
        if not target or target.startswith(EXTERNAL_PREFIXES):
            return match.group(0)
        if target.startswith("#"):
            return f"{bang}[{label}](#{anchors[source]}--{target[1:]})"
        path, _, anchor = target.partition("#")
        resolved = (source_dir / path).resolve()
        if resolved.suffix == ".md" and DOCS in resolved.parents:
            key = resolved.relative_to(DOCS).as_posix()
            target_anchor = anchors[key]
            return f"{bang}[{label}](#{target_anchor}--{anchor})" if anchor \
                else f"{bang}[{label}](#{target_anchor})"
        try:
            return f"{bang}[{label}]({resolved.relative_to(ROOT).as_posix()})"
        except ValueError:
            return match.group(0)

    return LINK_RE.sub(replace, text)


def strip_images(text):
    """Drop image blocks. The PDF pass needs this: xelatex cannot embed SVG."""
    return IMAGE_BLOCK_RE.sub("", text)


def normalize_thematic_breaks(text):
    """Rewrite '---' rules as '***'.

    A bare dashed line is ambiguous in pandoc's markdown: a YAML metadata block,
    a setext heading underline, or a multiline-table delimiter. Read as the last
    of those it swallows every following heading into table cells, silently and
    with a zero exit code. '***' is only ever a horizontal rule.
    """
    out, fence = [], None
    for line in text.splitlines(keepends=True):
        bare = line.rstrip("\n")
        fence_match = FENCE_RE.match(bare)
        if fence_match:
            marker = fence_match.group(1)[0]
            fence = marker if fence is None else (None if fence == marker else fence)
            out.append(line)
            continue
        if fence is None and THEMATIC_BREAK_RE.match(bare):
            out.append("***" + line[len(bare):])
            continue
        out.append(line)
    return "".join(out)


def add_heading_ids(text, document_anchor):
    """Give every heading an explicit, globally unique id.

    A level-1 heading is the document itself, so it takes the document's anchor.
    Everything below is namespaced under it, because section names like 'Best
    Practices' repeat across chapters and a renderer would silently renumber them.
    """
    out, fence, seen = [], None, {}
    for line in text.splitlines(keepends=True):
        bare = line.rstrip("\n")
        fence_match = FENCE_RE.match(bare)
        if fence_match:
            marker = fence_match.group(1)[0]
            fence = marker if fence is None else (None if fence == marker else fence)
            out.append(line)
            continue
        heading = HEADING_RE.match(bare) if fence is None else None
        if not heading:
            out.append(line)
            continue
        hashes, text_part = heading.groups()
        slug = slugify(text_part)
        anchor = document_anchor if len(hashes) == 1 else f"{document_anchor}--{slug}"
        repeats = seen.get(anchor, 0)
        seen[anchor] = repeats + 1
        if repeats:
            anchor = f"{anchor}-{repeats}"
        out.append(f"{hashes}{text_part.rstrip()} {{#{anchor}}}{line[len(bare):]}")
    return "".join(out)


def document_anchors(documents):
    """One unique anchor per document, keyed by its path relative to docs/."""
    anchors, taken = {}, set()
    for path, title, _ in documents:
        candidate = slugify(title)
        if candidate in taken:
            candidate = f"{slugify(path.split('/')[0])}--{candidate}"
        suffix = 2
        while candidate in taken:
            candidate, suffix = f"{candidate}-{suffix}", suffix + 1
        anchors[path] = candidate
        taken.add(candidate)
    return anchors


def in_reading_order(paths):
    """welcome.md, then chapters in folder order, each led by its index.md."""
    def key(path):
        parts = path.split("/")
        if path == "welcome.md":
            return (0, "", "")
        if len(parts) == 1:
            return (1, parts[0], "")
        return (2, parts[0], "" if parts[1] == "index.md" else parts[1])

    return sorted(paths, key=key)


def collect_documents():
    """Every document under docs/, in reading order, as (path, title, body)."""
    paths = in_reading_order(
        [p.relative_to(DOCS).as_posix() for p in DOCS.rglob("*.md")]
    )
    documents = []
    for path in paths:
        title, body = split_frontmatter((DOCS / path).read_text())
        documents.append((path, title, body))
    return documents


def assemble(documents):
    """One markdown document. A folder's index.md keeps its level, so it reads as
    the chapter opener; its siblings are demoted under it."""
    anchors = document_anchors(documents)
    chunks = []
    for path, _, body in documents:
        is_chapter_opener = path == "welcome.md" or path.endswith("/index.md")
        body = normalize_thematic_breaks(body)
        body = add_heading_ids(rewrite_links(body, path, anchors), anchors[path])
        chunks.append(body if is_chapter_opener else shift_headings(body))
    return "\n\n".join(chunk.rstrip("\n") for chunk in chunks) + "\n"


def duplicate_anchors(markdown):
    """Heading slugs that occur more than once, which a renderer will rename."""
    seen, duplicates = {}, []
    fence = None
    for line in markdown.splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)[0]
            fence = marker if fence is None else (None if fence == marker else fence)
            continue
        heading = HEADING_RE.match(line) if fence is None else None
        if not heading:
            continue
        explicit = EXPLICIT_ID_RE.search(heading.group(2))
        slug = explicit.group(1) if explicit else slugify(heading.group(2))
        seen[slug] = seen.get(slug, 0) + 1
        if seen[slug] == 2:
            duplicates.append(slug)
    return duplicates


def verify_anchors(markdown_path):
    """Check that pandoc sees every heading and link the assembled file declares.

    Markdown is ambiguous enough that a document can render with a zero exit code
    and a quietly mangled structure — headings absorbed into a table, say. This
    renders to HTML and compares what arrived against what was written.
    """
    html = subprocess.run(
        ["pandoc", str(markdown_path), "--from", PANDOC_READER,
         "--to", "html5", "--section-divs"],
        check=True, capture_output=True, text=True, cwd=ROOT,
    ).stdout
    markdown = markdown_path.read_text()
    declared = set(re.findall(r"^#{1,6}\s.*\{#([^}]+)\}\s*$", markdown, re.M))
    rendered = set(re.findall(r'id="([^"]+)"', html))
    linked = set(re.findall(r'href="#([^"]+)"', html))
    problems = []
    for anchor in sorted(declared - rendered):
        problems.append(f"heading id '{anchor}' was declared but did not render")
    for anchor in sorted(linked - rendered):
        problems.append(f"link target '#{anchor}' matches no heading")
    return problems


def render(markdown_path, target, out_path):
    """Run pandoc for one output format."""
    command = [
        "pandoc", str(markdown_path),
        "--from", PANDOC_READER,
        "--toc", "--toc-depth=2",
        "--resource-path", str(ROOT),
        "--metadata-file", str(METADATA),
        "--output", str(out_path),
    ]
    if target == "pdf":
        command += [
            "--pdf-engine", "xelatex",
            # A reading book, not a paper: chapters open on a fresh page, the folder
            # is the chapter, and the measure is wide enough for four-column tables.
            "--top-level-division=chapter",
            "-V", "documentclass=book",
            "-V", "classoption=oneside",
            "-V", "papersize=a4",
            "-V", "geometry=top=2.5cm",
            "-V", "geometry=bottom=2.5cm",
            "-V", "geometry=left=2.8cm",
            "-V", "geometry=right=2.8cm",
            "-V", "fontsize=11pt",
            "-V", "linestretch=1.15",
            "-V", "colorlinks=true",
            "-V", "linkcolor=RoyalBlue",
            "-V", PDF_HEADER_INCLUDES,
        ]
        fonts = ["-V", f"mainfont={PDF_MAIN_FONT}", "-V", f"monofont={PDF_MONO_FONT}"]
        if subprocess.run(command + fonts, cwd=ROOT).returncode == 0:
            return
        print(f"  warning: {PDF_MAIN_FONT}/{PDF_MONO_FONT} unavailable, falling back "
              "to the TeX default; diagram characters will be missing", file=sys.stderr)
    else:
        command += ["--to", "epub3", "--split-level=1"]
    subprocess.run(command, check=True, cwd=ROOT)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epub", action="store_true", help="build the EPUB only")
    parser.add_argument("--pdf", action="store_true", help="build the PDF only")
    parser.add_argument("--markdown", action="store_true",
                        help="assemble build/engx.md and stop")
    args = parser.parse_args(argv)

    if not args.markdown and not shutil.which("pandoc"):
        sys.exit("pandoc is not installed: brew install pandoc")

    documents = collect_documents()
    markdown = assemble(documents)
    BUILD.mkdir(exist_ok=True)
    source = BUILD / "engx.md"
    source.write_text(markdown)
    words = len(markdown.split())
    print(f"assembled {len(documents)} documents, {words:,} words -> {source}")

    for slug in duplicate_anchors(markdown):
        print(f"  warning: heading slug '{slug}' occurs more than once", file=sys.stderr)

    problems = verify_anchors(source)
    for problem in problems:
        print(f"  error: {problem}", file=sys.stderr)
    if problems:
        sys.exit(f"{len(problems)} structural problem(s); not rendering")
    print("  structure verified: every heading and link target resolves")

    if args.markdown:
        return 0

    both = not (args.epub or args.pdf)
    if args.epub or both:
        render(source, "epub", BUILD / "engx.epub")
        print(f"wrote {BUILD / 'engx.epub'}")
    if args.pdf or both:
        pdf_source = BUILD / "engx-print.md"
        pdf_source.write_text(strip_images(markdown))
        render(pdf_source, "pdf", BUILD / "engx.pdf")
        print(f"wrote {BUILD / 'engx.pdf'} (images omitted: no SVG rasterizer)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
