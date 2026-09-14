/** Tests for the book builder's text transforms. Run with `bun test scripts`. */

import { describe, expect, test } from "bun:test";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";

import * as book from "./build_book";

describe("shiftHeadings", () => {
  test("demotes a heading one level", () => {
    expect(book.shiftHeadings("# Title\n")).toBe("## Title\n");
  });

  test("demotes every level", () => {
    expect(book.shiftHeadings("# One\n\n## Two\n\n### Three\n")).toBe(
      "## One\n\n### Two\n\n#### Three\n",
    );
  });

  test("leaves a hash inside a fenced block alone", () => {
    const source = "# Title\n\n```sh\n# a shell comment\n```\n\n## After\n";
    const expected = "## Title\n\n```sh\n# a shell comment\n```\n\n### After\n";
    expect(book.shiftHeadings(source)).toBe(expected);
  });

  test("handles tilde fences", () => {
    const source = "~~~\n# not a heading\n~~~\n\n# Real\n";
    const expected = "~~~\n# not a heading\n~~~\n\n## Real\n";
    expect(book.shiftHeadings(source)).toBe(expected);
  });

  test("refuses to push past level six", () => {
    expect(() => book.shiftHeadings("###### Six\n")).toThrow();
  });
});

describe("normalizeThematicBreaks", () => {
  // A bare '---' is ambiguous in pandoc's markdown: YAML metadata, a setext
  // underline, or a multiline-table delimiter. Emit '***', which is only ever a
  // horizontal rule.

  test("a bare rule becomes asterisks", () => {
    expect(book.normalizeThematicBreaks("a\n\n---\n\nb\n")).toBe("a\n\n***\n\nb\n");
  });

  test("a longer rule becomes asterisks", () => {
    expect(book.normalizeThematicBreaks("-----\n")).toBe("***\n");
  });

  test("a table delimiter row is untouched", () => {
    expect(book.normalizeThematicBreaks("| --- | --- |\n")).toBe("| --- | --- |\n");
  });

  test("a rule inside a fence is untouched", () => {
    const source = "```\n---\n```\n";
    expect(book.normalizeThematicBreaks(source)).toBe(source);
  });

  test("a list item is untouched", () => {
    expect(book.normalizeThematicBreaks("- item\n")).toBe("- item\n");
  });
});

describe("closeVoidTags", () => {
  // EPUB3 is XHTML and pandoc passes raw inline HTML through verbatim, so a bare
  // <br> in a table cell is a mismatched tag that makes a conforming reader abandon
  // the whole page at that point.

  test("a bare break is closed", () => {
    expect(book.closeVoidTags("a<br>b\n")).toBe("a<br/>b\n");
  });

  test("an already closed break is left alone", () => {
    expect(book.closeVoidTags("a<br/>b\n")).toBe("a<br/>b\n");
  });

  test("a spaced break is normalized", () => {
    expect(book.closeVoidTags("a<br />b\n")).toBe("a<br/>b\n");
  });

  test("attributes are kept", () => {
    expect(book.closeVoidTags('<img src="x.png" alt="y">\n')).toBe(
      '<img src="x.png" alt="y"/>\n',
    );
  });

  test("a break inside a fence is untouched", () => {
    // Mermaid uses <br/> for label breaks, and a fence is not HTML anyway.
    const source = '```mermaid\nA["one<br/>two"] --> B\n```\n';
    expect(book.closeVoidTags(source)).toBe(source);
  });

  test("a paired tag is untouched", () => {
    expect(book.closeVoidTags("<td>x</td>\n")).toBe("<td>x</td>\n");
  });

  test("a table cell is fixed in place", () => {
    expect(book.closeVoidTags("| **T** | one<br>two |\n")).toBe(
      "| **T** | one<br/>two |\n",
    );
  });
});

describe("splitFrontmatter", () => {
  test("returns the title and the body without the block", () => {
    const source =
      "---\ntype: Guide\ntitle: CI/CD\ndescription: d\ntags: [a]\n---\n\n# CI/CD\n\nBody.\n";
    const { title, body } = book.splitFrontmatter(source);
    expect(title).toBe("CI/CD");
    expect(body).toBe("# CI/CD\n\nBody.\n");
  });

  test("strips the quotes a YAML title may carry", () => {
    const source = '---\ntitle: "Welcome to ALMAAT"\nkeywords: [welcome]\n---\nBody.\n';
    expect(book.splitFrontmatter(source).title).toBe("Welcome to ALMAAT");
  });

  test("rejects a file with no frontmatter", () => {
    expect(() => book.splitFrontmatter("# Heading\n")).toThrow();
  });
});

describe("ensureTitleHeading", () => {
  // A knowledge base that keeps its title in the frontmatter alone has no level-1
  // heading in the body, and the builder needs one: it is the document's anchor
  // and, for a chapter opener, the \chapter itself.

  test("prepends the title when the body has no top heading", () => {
    expect(book.ensureTitleHeading("Math", "The formal core.\n\n## Sets\n")).toBe(
      "# Math\n\nThe formal core.\n\n## Sets\n",
    );
  });

  test("leaves a body that already has one alone", () => {
    const source = "# Math\n\nThe formal core.\n";
    expect(book.ensureTitleHeading("Math", source)).toBe(source);
  });

  test("a hash inside a fence is not a top heading", () => {
    const source = "```sh\n# a comment\n```\n";
    expect(book.ensureTitleHeading("Shell", source)).toBe("# Shell\n\n" + source);
  });
});

describe("addHeadingIds", () => {
  // Every heading gets a globally unique id, because 60 files become one file
  // and generic section names like 'Best Practices' repeat across chapters.

  test("the top heading takes the document anchor", () => {
    expect(book.addHeadingIds("# Clouds\n", "clouds")).toBe("# Clouds {#clouds}\n");
  });

  test("a lower heading is namespaced by the document", () => {
    expect(book.addHeadingIds("## Best Practices\n", "caching")).toBe(
      "## Best Practices {#caching--best-practices}\n",
    );
  });

  test("a repeated heading is numbered like check_links does", () => {
    expect(book.addHeadingIds("## A\n\n## A\n", "d")).toBe(
      "## A {#d--a}\n\n## A {#d--a-1}\n",
    );
  });

  test("a hash inside a fence gets no id", () => {
    const source = "```sh\n# a comment\n```\n";
    expect(book.addHeadingIds(source, "x")).toBe(source);
  });
});

describe("rewriteLinks", () => {
  const anchors = {
    "03-system-design/05-containers.md": "containers",
    "07-clouds/01-concept-map.md": "concepts-across-the-clouds",
    "07-clouds/index.md": "clouds",
    "10-humans/21-interview.md": "interviewing",
    "06-frontend/index.md": "frontend",
    "welcome.md": "welcome",
  };
  const rewrite = (text: string, source = "03-system-design/05-containers.md") =>
    book.rewriteLinks(text, source, anchors);

  test("anchored cross-doc link is namespaced to the target", () => {
    expect(rewrite("see [x](../07-clouds/01-concept-map.md#compute--containers)")).toBe(
      "see [x](#concepts-across-the-clouds--compute--containers)",
    );
  });

  test("bare cross-doc link points at the target title", () => {
    expect(rewrite("see [x](../10-humans/21-interview.md)")).toBe("see [x](#interviewing)");
  });

  test("same-file anchor is namespaced to its own document", () => {
    expect(rewrite("see [x](#design)")).toBe("see [x](#containers--design)");
  });

  test("external link is untouched", () => {
    expect(rewrite("see [x](https://example.com/a.md)")).toBe(
      "see [x](https://example.com/a.md)",
    );
  });

  test("sibling link resolves within the same chapter", () => {
    expect(rewrite("see [x](01-concept-map.md)", "07-clouds/index.md")).toBe(
      "see [x](#concepts-across-the-clouds)",
    );
  });

  test("unknown target throws rather than emitting a dead link", () => {
    expect(() => rewrite("see [x](../99-nope/01-missing.md)")).toThrow();
  });

  test("a link to a document kept out of the book keeps its words and loses the link", () => {
    expect(rewrite("read [the index](../INDEX.md) first")).toBe("read the index first");
  });

  test("chapter image path is rewritten to the repository root", () => {
    expect(rewrite("![a](../../images/diagram.png)", "06-frontend/index.md")).toBe(
      "![a](images/diagram.png)",
    );
  });

  test("entry page image path is rewritten to the repository root", () => {
    expect(rewrite("![a](../images/cover-bg.png)", "welcome.md")).toBe(
      "![a](images/cover-bg.png)",
    );
  });
});

describe("documentAnchors", () => {
  test("two documents with the same title get different anchors", () => {
    const anchors = book.documentAnchors([
      { path: "05-coding/index.md", title: "Glossary", body: "" },
      { path: "00-se/01-glossary.md", title: "Glossary", body: "" },
    ]);
    const values = Object.values(anchors);
    expect(new Set(values).size).toBe(2);
    expect(values).toContain("glossary");
  });
});

describe("extractMermaid", () => {
  test("finds a block and returns its source", () => {
    const markdown = "# T\n\n```mermaid\nflowchart LR\n  A --> B\n```\n\nText.\n";
    expect(book.extractMermaid(markdown)).toEqual(["flowchart LR\n  A --> B"]);
  });

  test("finds every block in document order", () => {
    const markdown = "```mermaid\nfirst\n```\n\n```mermaid\nsecond\n```\n";
    expect(book.extractMermaid(markdown)).toEqual(["first", "second"]);
  });

  test("ignores a fence of another language", () => {
    expect(book.extractMermaid("```sh\nmermaid\n```\n")).toEqual([]);
  });

  test("ignores the word in prose", () => {
    expect(book.extractMermaid("a mermaid diagram\n")).toEqual([]);
  });
});

describe("rasterHash", () => {
  // The file name is the hash of the source, so an unchanged source is never
  // re-rendered and a changed one cannot collide with its own earlier version.

  test("is stable for the same source", () => {
    expect(book.rasterHash("flowchart LR\n  A --> B")).toBe(
      book.rasterHash("flowchart LR\n  A --> B"),
    );
  });

  test("differs for a different source", () => {
    expect(book.rasterHash("flowchart LR\n  A --> B")).not.toBe(
      book.rasterHash("flowchart LR\n  A --> C"),
    );
  });

  test("ignores trailing whitespace", () => {
    // Re-indenting the closing lines should not invalidate a cached render.
    expect(book.rasterHash("flowchart LR  \n  A --> B\n\n")).toBe(
      book.rasterHash("flowchart LR\n  A --> B"),
    );
  });
});

describe("replaceMermaid", () => {
  test("a block becomes an image with no alt text", () => {
    // Empty alt text keeps pandoc from floating this as a captioned figure.
    const markdown = "# T\n\n```mermaid\nflowchart LR\n```\n\nText.\n";
    expect(book.replaceMermaid(markdown, ["build/diagrams/ab12.png"])).toBe(
      "# T\n\n![](build/diagrams/ab12.png)\n\nText.\n",
    );
  });

  test("each block takes its own image", () => {
    const markdown = "```mermaid\nfirst\n```\n\n```mermaid\nsecond\n```\n";
    expect(book.replaceMermaid(markdown, ["a.png", "b.png"])).toBe(
      "![](a.png)\n\n![](b.png)\n",
    );
  });

  test("a block with no image keeps its source", () => {
    // A diagram that did not render stays a code block: that is today's output
    // for it, so a renderer failure never regresses the book.
    const markdown = "```mermaid\nfirst\n```\n\n```mermaid\nsecond\n```\n";
    expect(book.replaceMermaid(markdown, [null, "b.png"])).toBe(
      "```mermaid\nfirst\n```\n\n![](b.png)\n",
    );
  });

  test("rejects a count that does not match", () => {
    expect(() => book.replaceMermaid("```mermaid\nx\n```\n", [])).toThrow();
  });
});

describe("svgSize", () => {
  // Chrome's window is the viewport it screenshots, so a wrong size crops the
  // cover or pads it with blank paper.

  test("reads the declared pixel size", () => {
    expect(book.svgSize('<svg width="1200" height="300"/>')).toEqual([1200, 300]);
  });

  test("ignores a px suffix", () => {
    expect(book.svgSize('<svg width="1200px" height="300px"/>')).toEqual([1200, 300]);
  });

  test("falls back to the viewBox", () => {
    expect(book.svgSize('<svg viewBox="0 0 800 250"/>')).toEqual([800, 250]);
  });

  test("prefers the viewBox over a relative size", () => {
    // Markup sized in percent has no intrinsic pixel size; its viewBox does.
    const markup = '<svg width="100%" height="100%" viewBox="0 0 640 480"/>';
    expect(book.svgSize(markup)).toEqual([640, 480]);
  });

  test("rejects markup that declares no size", () => {
    expect(() => book.svgSize("<svg/>")).toThrow();
  });
});

describe("coverFields", () => {
  test("reads the three fields the cover prints", () => {
    const metadata = "title: A Book\nsubtitle: And its subtitle\nauthor: Someone\nlanguage: en-GB\n";
    expect(book.coverFields(metadata)).toEqual(["A Book", "And its subtitle", "Someone"]);
  });

  test("strips quotes a YAML value may carry", () => {
    expect(book.coverFields('title: "A Book"\n')[0]).toBe("A Book");
  });

  test("ignores the folded description and the subject list", () => {
    const metadata =
      "title: A Book\n" +
      "description: >-\n" +
      "  A long line that mentions author: not really\n" +
      "subject:\n" +
      "  - Software engineering\n";
    expect(book.coverFields(metadata)).toEqual(["A Book", "", ""]);
  });

  test("a missing field is empty rather than an error", () => {
    expect(book.coverFields("language: en-GB\n")).toEqual(["", "", ""]);
  });
});

describe("pngSize", () => {
  const png = (width: number, height: number) => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), "png-"));
    const file = path.join(dir, "x.png");
    const ihdr = Buffer.alloc(8);
    ihdr.writeUInt32BE(width, 0);
    ihdr.writeUInt32BE(height, 4);
    fs.writeFileSync(
      file,
      Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "latin1"), Buffer.from("\0\0\0\rIHDR", "latin1"), ihdr]),
    );
    return file;
  };

  test("reads the dimensions from the IHDR header", () => {
    expect(book.pngSize(png(752, 478))).toEqual([752, 478]);
  });

  test("refuses a file that is not a PNG", () => {
    const file = png(1, 1);
    fs.writeFileSync(file, "not a png at all, but long enough to slice");
    expect(() => book.pngSize(file)).toThrow();
  });
});

describe("coverSvg", () => {
  // The cover is generated from the metadata, so what it prints is tested here
  // rather than eyeballed on the rendered JPEG.

  const cover = ({
    title = "A Book",
    subtitle = "A subtitle",
    author = "Someone",
    photo = "data:image/png;base64,AAAA",
    aspect = 752 / 478,
  } = {}) => book.coverSvg(title, subtitle, author, photo, aspect);

  const image = (markup: string) => {
    const match = /<image\b[^>]*\by="(\d+)"[^>]*\bheight="(\d+)"/.exec(markup);
    if (!match) throw new Error("no <image> in the cover");
    return { y: Number(match[1]), height: Number(match[2]) };
  };

  test("is an A4-sized SVG Chrome can size", () => {
    expect(book.svgSize(cover())).toEqual([book.COVER_WIDTH, book.COVER_HEIGHT]);
  });

  test("carries the photograph inline", () => {
    expect(cover()).toContain("data:image/png;base64,AAAA");
  });

  test("the photograph sits flush with the bottom edge", () => {
    const { y, height } = image(cover());
    expect(y + height).toBe(book.COVER_HEIGHT);
  });

  test("the photograph keeps its own aspect ratio", () => {
    expect(image(cover({ aspect: 2.0 })).height).toBe(book.COVER_WIDTH / 2);
  });

  test("the top of the photograph fades into the page", () => {
    const stops = [...cover().matchAll(/<stop\b[^>]*stop-opacity="([^"]+)"/g)].map((m) => m[1]);
    expect(stops).toEqual(["0", "1"]);
  });

  test("wraps a long title onto several lines", () => {
    // A made-up title, not the book's own: retitling the book in
    // book/metadata.yaml must not break a test of the wrapping.
    const markup = cover({ title: "A Rather Long Book Title" });
    const titles = [...markup.matchAll(/<text class="title"[^>]*>([^<]*)<\/text>/g)].map((m) => m[1]);
    expect(titles).toEqual(["A Rather Long", "Book Title"]);
  });

  test("escapes metadata that would otherwise break the markup", () => {
    const markup = cover({ title: "Tools & <Practices>" });
    expect(markup).toContain("Tools &amp; &lt;Practices&gt;");
    expect(markup).not.toContain("<Practices>");
  });
});

describe("startOnANewPage", () => {
  // Each document opens on a fresh page: a raw LaTeX break for the PDF, a class
  // on the opening heading for the EPUB's stylesheet to hang a break on.

  test("puts a LaTeX page break before the document", () => {
    const marked = book.startOnANewPage("## Title {#t}\n\nBody.\n");
    expect(marked.startsWith("```{=latex}\n\\clearpage\n```\n\n")).toBe(true);
  });

  test("marks the opening heading and nothing below it", () => {
    const marked = book.startOnANewPage("## Title {#t}\n\nBody.\n\n### Section {#t--section}\n");
    expect(marked).toContain("## Title {#t .document}\n");
    expect(marked).toContain("### Section {#t--section}\n");
  });

  test("leaves the body alone", () => {
    const marked = book.startOnANewPage("## Title {#t}\n\nBody.\n");
    expect(marked.endsWith("\n\nBody.\n")).toBe(true);
  });

  test("a classed heading still reports its id alone", () => {
    // The id regexes stop at the first space, or the class would become part of
    // the anchor and every check that compares anchors would fail.
    expect(book.duplicateAnchors("## A {#t .document}\n\n## B {#t}\n")).toEqual(["t"]);
  });
});

describe("inReadingOrder", () => {
  test("welcome comes first, then chapters with index ahead of siblings", () => {
    const paths = [
      "07-clouds/01-concept-map.md",
      "welcome.md",
      "07-clouds/index.md",
      "00-software-engineering/index.md",
      "07-clouds/02-service-names.md",
    ];
    expect(book.inReadingOrder(paths)).toEqual([
      "welcome.md",
      "00-software-engineering/index.md",
      "07-clouds/index.md",
      "07-clouds/01-concept-map.md",
      "07-clouds/02-service-names.md",
    ]);
  });

  test("other top-level files are back matter, after the chapters", () => {
    const paths = ["_translations.md", "01-math/index.md", "_quotes.md", "welcome.md"];
    expect(book.inReadingOrder(paths)).toEqual([
      "welcome.md",
      "01-math/index.md",
      "_quotes.md",
      "_translations.md",
    ]);
  });
});

describe("wrap", () => {
  test("breaks at the last space that fits", () => {
    expect(book.wrap("A Rather Long Book Title", 16)).toEqual(["A Rather Long", "Book Title"]);
  });

  test("an empty text has no lines", () => {
    expect(book.wrap("", 16)).toEqual([]);
  });

  test("a word longer than the width is split", () => {
    expect(book.wrap("Supercalifragilistic", 8)).toEqual(["Supercal", "ifragili", "stic"]);
  });
});
