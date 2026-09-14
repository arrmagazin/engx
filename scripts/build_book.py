#!/usr/bin/env python3
"""Assemble docs/ into one document and render it as an EPUB and a PDF.

Stdlib only, like the three checkers. Pandoc does the rendering. This module does
the part pandoc cannot: put the files in reading order, demote their headings so a
folder reads as a chapter, turn cross-document links into intra-document anchors so
navigation still works when 57 files become one, and rasterize the mermaid diagrams,
which neither output format can render.

    python3 scripts/build_book.py            # both formats into build/
    python3 scripts/build_book.py --epub      # one format
    python3 scripts/build_book.py --markdown  # assemble only, render nothing
"""

import argparse
import base64
import hashlib
import pathlib
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import textwrap
import time
import xml.etree.ElementTree as ElementTree
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
BUILD = ROOT / "build"
DIAGRAMS = BUILD / "diagrams"
METADATA = ROOT / "book" / "metadata.yaml"
TABLE_RULES = ROOT / "book" / "table-rules.lua"
EPUB_CSS = ROOT / "book" / "epub.css"
COVERS = BUILD / "cover"
COVER_PHOTO = ROOT / "images" / "cover-bg.png"

FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^(#{1,6})(\s+\S.*)$")
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]*)\)")
MERMAID_FENCE_RE = re.compile(
    r"^```[ \t]*mermaid[ \t]*\n(.*?)\n[ \t]*```[ \t]*$", re.M | re.S
)
VOID_TAG_RE = re.compile(r"<(br|hr|wbr|img)((?:\s[^>]*?)?)\s*/?>", re.I)
UNSLUGGABLE_RE = re.compile(r"[^\w\- ]")
THEMATIC_BREAK_RE = re.compile(r"^ {0,3}-{3,}[ \t]*$")
TITLE_RE = re.compile(r"^title:[ \t]*(.+?)[ \t]*$", re.M)
METADATA_FIELD_RE = re.compile(r"^(title|subtitle|author):[ \t]*(.+?)[ \t]*$", re.M)
EXPLICIT_ID_RE = re.compile(r"\{#([^}\s]+)[^}]*\}\s*$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "ftp://")
# A raw block rather than a bare \clearpage line: the explicit syntax needs no
# markdown extension to be read as LaTeX, and every other writer drops it.
PAGE_BREAK = "```{=latex}\n\\clearpage\n```"
DOCUMENT_HEADING_RE = re.compile(r"^(#{1,6} .*\{#[^}\s]+)\}")

# Neither EPUB nor PDF can render a mermaid fence; pandoc prints it as a verbatim
# code block. So the diagrams are rasterized before pandoc sees them, by mermaid-cli
# under npx — an external renderer invoked the same way as pandoc and xelatex, which
# keeps this module stdlib-only. The version is pinned so a rebuild cannot silently
# change the diagrams' appearance. Scale 3 is legible in print without being heavy.
MERMAID_CLI = "@mermaid-js/mermaid-cli@11.17.0"
DIAGRAM_SCALE = 3

# The cover is the one image this module rasterizes itself, and it uses headless
# Chrome rather than a standalone rasterizer: Chrome is already on the machine, so
# this costs no install, and it is the engine the cover was drawn against, with the
# gradient mask and the system fonts it names already in hand. If it is missing the
# book is built without a cover.
#
# Scale 2 where the diagrams get 3: the cover is A4 at 620x877 CSS pixels, so 2 gives
# 1240x1754, which is 150dpi on A4 — as much as a 752px photograph can carry.
#
# And JPEG where the diagrams are PNG. The cover is mostly photograph, which is close
# to incompressible, so lossless is the wrong bargain: it multiplies the size for no
# visible gain, and xelatex embeds JPEG without re-encoding it. A diagram is flat line
# art and stays PNG, where lossless is cheap. Chrome picks the format from the
# extension and accepts only '.jpg' — '.jpeg' is refused outright.
CHROME = pathlib.Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
RASTER_SCALE = 2
RASTER_FORMAT = "jpg"

# Two measured facts shape how Chrome is called. It takes a singleton lock on its
# user-data directory, so pointing it at the default profile while the browser is
# open blocks until the browser quits — a build that hangs rather than fails; hence a
# throwaway profile. And given its own profile it writes the screenshot in about two
# and a half seconds and then keeps running rather than exiting, so what is waited on
# is the file settling, not the process. The timeout is only a backstop.
RASTER_TIMEOUT = 60
RASTER_POLL = 0.2

# The cover is generated, not drawn: an SVG built from book/metadata.yaml with the
# photograph across the bottom, rasterized by headless Chrome. Built
# rather than committed so the title, subtitle and author printed on it cannot drift
# from the metadata pandoc sets inside the book.
#
# A4 proportions in CSS pixels, doubled to 1240x1754 by RASTER_SCALE, which is 150dpi
# on A4. Not larger: the photograph is 752px wide, and a wider cover would only
# upscale it further. It sits flush with the bottom edge at its own aspect ratio, and
# the top of it fades into the page over COVER_FADE of its height.
COVER_WIDTH = 620
COVER_HEIGHT = 877
COVER_FADE = 0.45
COVER_MARGIN = 70
COVER_PAPER = "#0A1017"
COVER_INK = "#F4F7FA"
COVER_MUTED = "#8FA3B3"
COVER_ACCENT = "#4FD8E4"

# The book uses box-drawing characters for diagrams and a few maths symbols in
# prose. TeX's default Latin Modern has none of them, so the PDF needs fonts that
# do. These two are present on macOS and verified to cover every character the
# book uses; if either is missing the PDF still builds, with glyphs dropped.
# A bare '---' in the book is a horizontal rule, never metadata. normalize_thematic_breaks
# removes the other readings; this removes the one it cannot.
PANDOC_READER = "markdown-yaml_metadata_block"

TABLE_PADDING = (
    r"\renewcommand{\arraystretch}{1.3}"
    r"\setlength{\extrarowheight}{2pt}"
)

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
#
# Those same four-column tables wrap one row to three or four lines, so rows need
# separating or they run together. Each gets a little vertical padding and a hairline
# above it, drawn at a quarter black so a long table reads as banded rather than as a
# grid. The rules themselves come from book/table-rules.lua, which is the only place
# they can come from — see that file. Padding is deliberately modest: at the 1.45
# arraystretch that reads best on its own, the book grows by twenty-two pages.
# Blockquotes in this book are asides: a rule of thumb, a caution, a line worth
# stopping on. Pandoc sets them as an indented paragraph, which at 11pt on a 15.4cm
# measure reads as body text that has drifted right. Each becomes a callout instead —
# warm paper, with an amber bar down the left edge, so it is
# visibly not the argument it interrupts.
#
# mdframed rather than framed's snugshade, on two counts: snugshade takes its colour
# from `shadecolor`, which pandoc's highlighting already owns for code blocks, and it
# draws no rule. mdframed's default style breaks across a page, which a long quote
# needs.
PDF_CALLOUT = (
    r"\usepackage{mdframed}"
    r"\definecolor{engxcalloutback}{HTML}{FAF4E8}"
    r"\definecolor{engxcalloutrule}{HTML}{EFAE16}"
    r"\newmdenv[backgroundcolor=engxcalloutback,linecolor=engxcalloutrule,"
    r"linewidth=3pt,topline=false,bottomline=false,rightline=false,"
    r"innerleftmargin=12pt,innerrightmargin=12pt,innertopmargin=9pt,"
    r"innerbottommargin=9pt,skipabove=0.9\baselineskip,skipbelow=0.9\baselineskip,"
    r"leftmargin=0pt,rightmargin=0pt]{engxcallout}"
    r"\renewenvironment{quote}{\begin{engxcallout}}{\end{engxcallout}}"
)

# Glossaries are definition lists, which LaTeX sets run-in: the term in bold at the
# left margin, its definition alongside, the rest of it hung underneath. That is how a
# printed glossary reads and it needs no help. What does need help is a definition
# holding a bulleted list — LaTeX gives a nested itemize a left margin of its own on
# top of the description's, so the bullets land a long way right of the definition they
# belong to and read as a separate block. The margin is narrowed for that nesting only,
# inside the description environment, so every other list in the book is untouched.
PDF_DEFINITION_LIST = (
    r"\usepackage{enumitem}"
    r"\AtBeginEnvironment{description}{\setlist[itemize]{leftmargin=1.2em}}"
)

PDF_HEADER_INCLUDES = (
    r"header-includes="
    r"\usepackage{etoolbox}"
    r"\usepackage{seqsplit}"
    r"\usepackage{colortbl}"
    r"\let\oldtexttt\texttt"
    r"\renewcommand{\texttt}[1]{\oldtexttt{\seqsplit{#1}}}"
    r"\newcommand{\engxrowrule}{\arrayrulecolor{black!25}\hline\arrayrulecolor{black}}"
    r"\AtBeginEnvironment{longtable}{\small\let\texttt\oldtexttt" + TABLE_PADDING + "}"
    r"\AtBeginEnvironment{tabular}{\small\let\texttt\oldtexttt" + TABLE_PADDING + "}"
    + PDF_CALLOUT
    + PDF_DEFINITION_LIST
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
    """Return (title, body): the frontmatter block dropped, and the body opened
    with `# <title>`. A document carries no H1 of its own — its frontmatter title
    is the heading — so the assembler writes the one the book needs."""
    if not text.startswith("---\n"):
        raise ValueError("file does not start with frontmatter")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError("unterminated frontmatter")
    title = TITLE_RE.search(text[4:end + 1])
    if not title:
        raise ValueError("frontmatter has no title")
    body = text[end + len("\n---\n"):].lstrip("\n")
    return title.group(1), f"# {title.group(1)}\n\n{body}"


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


def extract_mermaid(markdown):
    """The source of every mermaid block, in document order."""
    return MERMAID_FENCE_RE.findall(markdown)


def raster_hash(source):
    """The name of a rasterized PNG: a digest of the source it was rendered from.

    Content-addressing gives the cache for free — an unchanged source is already on
    disk and is never re-rendered, and an edited one cannot be confused with its own
    earlier version. Callers fold the render scale into what they hash, because
    otherwise retuning a scale would serve every old PNG as a hit forever. Trailing
    whitespace is normalized away so a cosmetic edit does not cost a render.
    """
    normalized = "\n".join(line.rstrip() for line in source.strip().splitlines())
    return hashlib.sha256(normalized.encode()).hexdigest()[:12]


def diagram_path(source):
    """Where a diagram's PNG lives. Under build/, so it is a build artifact."""
    return DIAGRAMS / f"{raster_hash(f'{DIAGRAM_SCALE}\n{source}')}.png"


def replace_mermaid(markdown, images):
    """Swap each mermaid block for its rendered image, positionally.

    A `None` image leaves that block as it was: a diagram that would not render stays
    a code block, which is what the book prints today, so a renderer that is missing
    or broken degrades the output instead of failing the build.
    """
    sources = extract_mermaid(markdown)
    if len(images) != len(sources):
        raise ValueError(f"{len(sources)} mermaid blocks but {len(images)} images")
    pending = iter(images)

    def substitute(match):
        image = next(pending)
        # Empty alt text: pandoc turns an image *with* alt text into a captioned,
        # floating figure, which would reorder 32 diagrams away from their prose.
        return match.group(0) if image is None else f"![]({image})"

    return MERMAID_FENCE_RE.sub(substitute, markdown)


def run_mermaid_cli(jobs):
    """Render `jobs`, a list of (destination, source), in one mermaid-cli run.

    Given a markdown input, mermaid-cli renders every block it finds in a single
    browser launch and numbers the output files by each block's *position in the
    input* — not by the order the concurrent renders finish. That is what makes the
    rename to <hash>.png safe, and it is why the diagrams are batched through a
    scratch document rather than invoked one at a time.
    """
    scratch = BUILD / "diagrams-pending.md"
    rendered = BUILD / "diagrams-rendered.md"
    # An interrupted earlier run can leave numbered PNGs behind, and this run's
    # numbering means something different. Clear them or one could be renamed to a
    # hash it is not a render of.
    for stale in BUILD.glob(f"{rendered.stem}-*.png"):
        stale.unlink()
    scratch.write_text(
        "\n\n".join(f"```mermaid\n{source}\n```" for _, source in jobs) + "\n"
    )
    command = [
        "npx", "-y", "-p", MERMAID_CLI, "mmdc",
        "-i", str(scratch), "-o", str(rendered),
        "-e", "png", "--scale", str(DIAGRAM_SCALE), "--backgroundColor", "white",
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, cwd=ROOT)
    except FileNotFoundError:
        print("  warning: npx is not installed, so diagrams stay as code blocks",
              file=sys.stderr)
        return
    except subprocess.CalledProcessError as error:
        print(f"  warning: mermaid-cli failed, so diagrams stay as code blocks\n"
              f"{error.stderr.strip()}", file=sys.stderr)
        return
    finally:
        scratch.unlink(missing_ok=True)
        rendered.unlink(missing_ok=True)
    for index, (destination, _) in enumerate(jobs, start=1):
        produced = BUILD / f"{rendered.stem}-{index}.png"
        if produced.exists():
            produced.replace(destination)


def render_diagrams(sources):
    """The PNG path of each source, or None where no PNG was produced.

    Only uncached diagrams are rendered, and identical diagrams share one render.
    Paths come back relative to the repository root, which is where pandoc is pointed,
    alongside the number of PNGs this run actually produced.
    """
    DIAGRAMS.mkdir(parents=True, exist_ok=True)
    pending = {}
    for source in sources:
        destination = diagram_path(source)
        if not destination.exists():
            pending.setdefault(destination, source)
    if pending:
        run_mermaid_cli(list(pending.items()))
    paths = [
        path.relative_to(ROOT).as_posix() if path.exists() else None
        for path in (diagram_path(source) for source in sources)
    ]
    return paths, sum(1 for path in pending if path.exists())


def resolve_mermaid(markdown):
    """Replace every mermaid block with a rendered PNG.

    Returns (markdown, resolved, rendered): how many blocks became images, and how
    many of those cost a render rather than a cache hit.
    """
    sources = extract_mermaid(markdown)
    if not sources:
        return markdown, 0, 0
    images, rendered = render_diagrams(sources)
    unresolved = images.count(None)
    if unresolved:
        print(f"  warning: {unresolved} of {len(sources)} diagrams did not render "
              "and stay as code blocks", file=sys.stderr)
    return replace_mermaid(markdown, images), len(sources) - unresolved, rendered


def svg_size(markup):
    """The pixel size an SVG should be screenshotted at.

    Chrome's window is the viewport it captures, so a wrong size crops the cover or
    pads it with blank paper. A declared pixel width and height win; a relative one
    says nothing about intrinsic size, so the viewBox answers instead.
    """
    root = ElementTree.fromstring(markup)
    width, height = root.get("width", ""), root.get("height", "")
    if width.removesuffix("px").isdigit() and height.removesuffix("px").isdigit():
        return int(width.removesuffix("px")), int(height.removesuffix("px"))
    box = (root.get("viewBox") or "").split()
    if len(box) == 4:
        return round(float(box[2])), round(float(box[3]))
    raise ValueError("svg declares neither a pixel size nor a viewBox")


def settled(path, process):
    """Wait until `path` has been written and has stopped growing. True if it was.

    Chrome does not exit after taking its screenshot, so there is no exit code to
    wait for: the file appearing, and then holding its size across two polls, is the
    signal that it is complete rather than half-written.
    """
    deadline = time.monotonic() + RASTER_TIMEOUT
    previous = -1
    while time.monotonic() < deadline:
        time.sleep(RASTER_POLL)
        if not path.exists():
            if process.poll() is not None:
                return False  # chrome gave up before writing anything
            continue
        size = path.stat().st_size
        if size and size == previous:
            return True
        previous = size
    return False


def rasterize_svg(svg, destination, profile):
    """Screenshot one SVG with headless Chrome. True if the image was written.

    `profile` is a throwaway user-data directory, and the screenshot lands on a
    partial path that is renamed into place only once complete — see RASTER_TIMEOUT
    for why, and note that a half-written file left in the cache would otherwise be
    served as a hit forever.
    """
    if not CHROME.exists():
        return False
    try:
        width, height = svg_size(svg.read_text())
    except (ElementTree.ParseError, ValueError) as error:
        print(f"  warning: cannot size {svg.name}: {error}", file=sys.stderr)
        return False
    # Chrome picks the format from the extension and refuses anything it does not
    # know, so the in-progress name keeps the real extension last rather than
    # appending .part to it.
    partial = destination.with_name(f"{destination.stem}.part{destination.suffix}")
    partial.unlink(missing_ok=True)
    process = subprocess.Popen(
        [
            str(CHROME), "--headless", "--disable-gpu", "--hide-scrollbars",
            "--no-first-run", "--no-default-browser-check",
            f"--user-data-dir={profile}",
            f"--window-size={width},{height}",
            f"--force-device-scale-factor={RASTER_SCALE}",
            f"--screenshot={partial}",
            svg.as_uri(),
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ROOT,
    )
    try:
        written = settled(partial, process)
    finally:
        process.kill()
        process.wait()
    if not written:
        print(f"  warning: rasterizing {svg.name} did not finish within "
              f"{RASTER_TIMEOUT}s", file=sys.stderr)
        partial.unlink(missing_ok=True)
        return False
    partial.replace(destination)
    return True


def png_size(path):
    """(width, height) from a PNG's IHDR, which is always the first chunk."""
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path.name} is not a PNG")
    return struct.unpack(">II", header[16:24])


def cover_fields(metadata):
    """The three fields the cover prints, read from book/metadata.yaml.

    A deliberately small reader rather than a YAML parser: these are plain scalars on
    one line each, and the file's only other shapes — a folded description and a list
    of subjects — are not wanted here.
    """
    fields = {
        key: value.strip("\"'")
        for key, value in METADATA_FIELD_RE.findall(metadata)
    }
    return fields.get("title", ""), fields.get("subtitle", ""), fields.get("author", "")


def data_uri(path, media_type):
    """A file as a data: URI, so the generated SVG is self-contained.

    Self-contained is what makes the cache correct: the digest that names the
    rasterized cover is taken over the SVG's text, so with the photograph inside it a
    replaced photograph changes the digest and the cover is re-rendered.
    """
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def text_lines(markup, lines, x, y, leading, css_class):
    """One <text> element per line. SVG does no line breaking of its own."""
    for index, line in enumerate(lines):
        markup.append(
            f'  <text class="{css_class}" x="{x}" y="{y + index * leading}">'
            f"{escape(line)}</text>"
        )
    return y + max(len(lines) - 1, 0) * leading


def cover_svg(title, subtitle, author, photo, photo_aspect):
    """The cover as SVG markup: type block above, the photograph along the bottom.

    The photograph keeps its own aspect ratio at full cover width, so how much of the
    page it covers follows from the image rather than from a number chosen here. Its
    top fades to nothing against the page, which is why the page is dark: the
    photograph is, and fading it into a light page would only muddy it.
    """
    photo_height = round(COVER_WIDTH / photo_aspect)
    photo_top = COVER_HEIGHT - photo_height
    title_lines = textwrap.wrap(title, 16) or [""]
    subtitle_lines = textwrap.wrap(subtitle, 44)
    markup = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {COVER_WIDTH} '
        f'{COVER_HEIGHT}" width="{COVER_WIDTH}" height="{COVER_HEIGHT}" role="img" '
        f'aria-label="{escape(title)}">',
        "  <defs>",
        f'    <linearGradient id="fade" x1="0" y1="{photo_top}" x2="0" '
        f'y2="{photo_top + round(photo_height * COVER_FADE)}" '
        'gradientUnits="userSpaceOnUse">',
        '      <stop offset="0" stop-color="#fff" stop-opacity="0"/>',
        '      <stop offset="1" stop-color="#fff" stop-opacity="1"/>',
        "    </linearGradient>",
        f'    <mask id="fadeMask"><rect x="0" y="{photo_top}" width="{COVER_WIDTH}" '
        f'height="{photo_height}" fill="url(#fade)"/></mask>',
        "    <style>",
        "      text { font-family: \"Times New Roman\", Georgia, serif; }",
        f"      .title {{ font-size: 58px; fill: {COVER_INK}; }}",
        f"      .subtitle {{ font-size: 19px; fill: {COVER_MUTED}; }}",
        f"      .author {{ font-size: 16px; fill: {COVER_INK}; "
        "letter-spacing: 3px; text-transform: uppercase; }",
        "    </style>",
        "  </defs>",
        f'  <rect width="{COVER_WIDTH}" height="{COVER_HEIGHT}" fill="{COVER_PAPER}"/>',
        f'  <image href="{photo}" x="0" y="{photo_top}" width="{COVER_WIDTH}" '
        f'height="{photo_height}" mask="url(#fadeMask)" '
        'preserveAspectRatio="xMidYMid slice"/>',
        f'  <rect x="{COVER_MARGIN}" y="168" width="84" height="3" '
        f'fill="{COVER_ACCENT}"/>',
    ]
    last = text_lines(markup, title_lines, COVER_MARGIN, 226, 66, "title")
    last = text_lines(markup, subtitle_lines, COVER_MARGIN, last + 74, 28, "subtitle")
    text_lines(markup, [author.upper()], COVER_MARGIN, last + 66, 0, "author")
    markup.append("</svg>")
    return "\n".join(markup) + "\n"


def build_cover():
    """Render the cover and return its path relative to ROOT, or None if it was not.

    Content-addressed, so the cover costs a render only when the
    metadata or the photograph changes. The directory holds exactly one cover: unlike
    a diagram, there is never a second one to serve, so a superseded file is removed
    rather than left in the cache.
    """
    if not COVER_PHOTO.exists():
        print(f"  warning: {COVER_PHOTO.name} is missing; the book has no cover",
              file=sys.stderr)
        return None
    if not CHROME.exists():
        print("  warning: Chrome is missing; the book has no cover", file=sys.stderr)
        return None
    width, height = png_size(COVER_PHOTO)
    title, subtitle, author = cover_fields(METADATA.read_text())
    markup = cover_svg(title, subtitle, author,
                       data_uri(COVER_PHOTO, "image/png"), width / height)
    COVERS.mkdir(parents=True, exist_ok=True)
    destination = COVERS / f"{raster_hash(str(RASTER_SCALE) + chr(10) + markup)}.{RASTER_FORMAT}"
    if not destination.exists():
        source = COVERS / "cover.svg"
        source.write_text(markup)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
            written = rasterize_svg(source, destination, profile)
        source.unlink(missing_ok=True)
        if not written:
            return None
        for stale in COVERS.glob(f"*.{RASTER_FORMAT}"):
            if stale != destination:
                stale.unlink()
        print(f"  cover rendered -> {destination}")
    return destination.relative_to(ROOT).as_posix()


def pdf_cover_include(cover):
    """LaTeX that opens the PDF on a full-bleed cover page.

    AtBeginDocument rather than an --include-before-body file, because pandoc's
    template puts \\maketitle before the includes and the cover has to come first.
    Margins are dropped for that one page so the photograph reaches the paper's edge,
    and restored immediately after; the cover is A4-proportioned, so asking for both
    the paper's width and its height does not stretch it.

    \\maketitle is then emptied: the cover already carries the title, the subtitle and
    the author, and pandoc's title page would otherwise repeat all three overleaf.
    """
    return (
        r"header-includes="
        r"\renewcommand{\maketitle}{}"
        r"\AtBeginDocument{"
        r"\newgeometry{margin=0pt}"
        r"\thispagestyle{empty}"
        rf"\noindent\includegraphics[width=\paperwidth,height=\paperheight]{{{cover}}}"
        r"\clearpage"
        r"\restoregeometry}"
    )


def close_void_tags(text):
    """Close void HTML elements, so `<br>` becomes `<br/>`, outside fenced blocks.

    EPUB3 is XHTML, and pandoc passes raw inline HTML through verbatim rather than
    parsing it. A bare `<br>` in a table cell therefore reaches the EPUB as a
    mismatched tag, and a conforming reader abandons the rest of that page — which is
    what happened to three chapters. The glossary convention asks authors for `<br>`
    in a multi-line cell, so the builder is the right place to make it well-formed.
    Fences are skipped: mermaid uses `<br/>` in labels, and a fence is not HTML.
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
        # rstrip: the attribute group absorbs the space in `<br />`, which would
        # otherwise come back out as `<br />` rather than a uniform `<br/>`.
        closed = VOID_TAG_RE.sub(
            lambda match: f"<{match.group(1)}{match.group(2).rstrip()}/>", line
        )
        out.append(closed if fence is None else line)
    return "".join(out)


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


def start_on_a_new_page(body):
    """Open a document on a fresh page, in both formats.

    A folder's index.md is a \\chapter and already breaks; its siblings are
    \\section, which does not, so the PDF needs an explicit \\clearpage. The EPUB has
    no pages of its own, but a paginated reader honours a CSS break, and pandoc puts
    a heading's classes on the <section> it wraps — so the opening heading is marked
    `.document` and book/epub.css hangs the break on that.
    """
    marked = DOCUMENT_HEADING_RE.sub(r"\1 .document}", body, count=1)
    return f"{PAGE_BREAK}\n\n{marked}"


def assemble(documents):
    """One markdown document. A folder's index.md keeps its level, so it reads as
    the chapter opener; its siblings are demoted under it."""
    anchors = document_anchors(documents)
    chunks = []
    for path, _, body in documents:
        is_chapter_opener = path == "welcome.md" or path.endswith("/index.md")
        body = close_void_tags(normalize_thematic_breaks(body))
        body = add_heading_ids(rewrite_links(body, path, anchors), anchors[path])
        chunks.append(body if is_chapter_opener
                      else start_on_a_new_page(shift_headings(body)))
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
    declared = set(re.findall(r"^#{1,6}\s.*\{#([^}\s]+)[^}]*\}\s*$", markdown, re.M))
    rendered = set(re.findall(r'id="([^"]+)"', html))
    linked = set(re.findall(r'href="#([^"]+)"', html))
    problems = []
    for anchor in sorted(declared - rendered):
        problems.append(f"heading id '{anchor}' was declared but did not render")
    for anchor in sorted(linked - rendered):
        problems.append(f"link target '#{anchor}' matches no heading")
    return problems


def render(markdown_path, target, out_path, cover=None):
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
            # table-rules.lua hands each table back as a raw block, so pandoc stops
            # seeing a table in the document and its template stops loading
            # longtable and booktabs. This says to load them anyway.
            "--lua-filter", str(TABLE_RULES),
            "-V", "tables=true",
        ]
        if cover:
            # A second -V of the same name: pandoc collects them, so this joins
            # PDF_HEADER_INCLUDES in the preamble rather than replacing it.
            command += ["-V", pdf_cover_include(cover)]
        fonts = ["-V", f"mainfont={PDF_MAIN_FONT}", "-V", f"monofont={PDF_MONO_FONT}"]
        if subprocess.run(command + fonts, cwd=ROOT).returncode == 0:
            return
        print(f"  warning: {PDF_MAIN_FONT}/{PDF_MONO_FONT} unavailable, falling back "
              "to the TeX default; diagram characters will be missing", file=sys.stderr)
    else:
        # --css REPLACES pandoc's default EPUB stylesheet rather than adding to
        # it, which would drop the book's baseline typography. So ask pandoc for
        # its own default and layer ours on top: two --css arguments are embedded
        # and linked in order, and this keeps the default in step with whatever
        # pandoc is installed rather than vendoring a copy that goes stale.
        default_css = BUILD / "epub-default.css"
        default_css.write_text(subprocess.run(
            ["pandoc", "--print-default-data-file", "epub.css"],
            check=True, capture_output=True, text=True,
        ).stdout)
        command += ["--to", "epub3", "--split-level=1",
                    "--css", str(default_css), "--css", str(EPUB_CSS)]
        if cover:
            command += ["--epub-cover-image", cover]
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

    # Before the assembled file is written, so that what verify_anchors checks and
    # what pandoc reads are the same document. --markdown renders diagrams too: they
    # are the markdown's own content, and a cache hit costs nothing.
    markdown, diagrams, rendered = resolve_mermaid(markdown)

    source = BUILD / "engx.md"
    source.write_text(markdown)
    words = len(markdown.split())
    print(f"assembled {len(documents)} documents, {words:,} words -> {source}")
    if diagrams:
        print(f"  {diagrams} mermaid diagram(s): {rendered} rendered, "
              f"{diagrams - rendered} cached -> {DIAGRAMS}")

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

    # Both formats take the same cover, so it is rendered once, before either.
    cover = build_cover()

    both = not (args.epub or args.pdf)
    if args.epub or both:
        render(source, "epub", BUILD / "engx.epub", cover)
        print(f"wrote {BUILD / 'engx.epub'}")
    if args.pdf or both:
        render(source, "pdf", BUILD / "engx.pdf", cover)
        print(f"wrote {BUILD / 'engx.pdf'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
