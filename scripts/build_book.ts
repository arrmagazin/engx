#!/usr/bin/env bun
/**
 * Assemble docs/ into one document and render it as an EPUB and a PDF.
 *
 * Node built-ins only. Pandoc does the rendering. This module does the part pandoc
 * cannot: put the files in reading order, demote their headings so a folder reads as
 * a chapter, turn cross-document links into intra-document anchors so navigation
 * still works when many files become one, and rasterize the mermaid diagrams, which
 * neither output format can render.
 *
 *     bun scripts/build_book.ts             # both formats into build/
 *     bun scripts/build_book.ts --epub      # one format
 *     bun scripts/build_book.ts --markdown  # assemble only, render nothing
 *
 * The book takes its file name from the package: build/<name>.md, .epub and .pdf.
 */

import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { createHash } from "node:crypto";
import * as fs from "node:fs";
import * as os from "node:os";
import * as path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const DOCS = path.join(ROOT, "docs");
export const BUILD = path.join(ROOT, "build");
const DIAGRAMS = path.join(BUILD, "diagrams");
const METADATA = path.join(ROOT, "book", "metadata.yaml");
const TABLE_RULES = path.join(ROOT, "book", "table-rules.lua");
const EPUB_CSS = path.join(ROOT, "book", "epub.css");
const COVERS = path.join(BUILD, "cover");
const COVER_PHOTO = path.join(ROOT, "images", "cover-bg.png");
export const BOOK: string = JSON.parse(fs.readFileSync(path.join(ROOT, "package.json"), "utf8")).name;

// Files at the root of docs/ that are about the repository rather than in the book:
// the content rulebook, and a hand-written index the rendered table of contents
// replaces. Every other root file is back matter — see inReadingOrder.
const NOT_CONTENT = new Set(["CLAUDE.md", "INDEX.md"]);

const FENCE_RE = /^\s*(`{3,}|~{3,})/;
const HEADING_RE = /^(#{1,6})(\s+\S.*)$/;
const LINK_RE = /(!?)\[([^\]]*)\]\(([^)\s]*)\)/g;
const MERMAID_FENCE_RE = /^```[ \t]*mermaid[ \t]*\n([\s\S]*?)\n[ \t]*```[ \t]*$/gm;
const VOID_TAG_RE = /<(br|hr|wbr|img)((?:\s[^>]*?)?)\s*\/?>/gi;
const UNSLUGGABLE_RE = /[^\p{L}\p{N}_\- ]/gu;
const THEMATIC_BREAK_RE = /^ {0,3}-{3,}[ \t]*$/;
const TITLE_RE = /^title:[ \t]*(.+?)[ \t]*$/m;
const METADATA_FIELD_RE = /^(title|subtitle|author):[ \t]*(.+?)[ \t]*$/gm;
const EXPLICIT_ID_RE = /\{#([^}\s]+)[^}]*\}\s*$/;
const DECLARED_ID_RE = /^#{1,6}\s.*\{#([^}\s]+)[^}]*\}\s*$/gm;
const EXTERNAL_PREFIXES = ["http://", "https://", "mailto:", "ftp://"];
// A raw block rather than a bare \clearpage line: the explicit syntax needs no
// markdown extension to be read as LaTeX, and every other writer drops it.
const PAGE_BREAK = "```{=latex}\n\\clearpage\n```";
const DOCUMENT_HEADING_RE = /^(#{1,6} .*\{#[^}\s]+)\}/;

// Neither EPUB nor PDF can render a mermaid fence; pandoc prints it as a verbatim
// code block. So the diagrams are rasterized before pandoc sees them, by mermaid-cli
// under npx — an external renderer invoked the same way as pandoc and xelatex. The
// version is pinned so a rebuild cannot silently change the diagrams' appearance.
// Scale 3 is legible in print without being heavy.
const MERMAID_CLI = "@mermaid-js/mermaid-cli@11.17.0";
const DIAGRAM_SCALE = 3;

// The cover is the one image this module rasterizes itself, and it uses headless
// Chrome rather than a standalone rasterizer: Chrome is already on the machine, so
// this costs no install, and it is the engine the cover was drawn against, with the
// gradient mask and the system fonts it names already in hand. If it is missing the
// book is built without a cover.
//
// Scale 2 where the diagrams get 3: the cover is A4 at 620x877 CSS pixels, so 2 gives
// 1240x1754, which is 150dpi on A4 — as much as a 752px photograph can carry.
//
// And JPEG where the diagrams are PNG. The cover is mostly photograph, which is close
// to incompressible, so lossless is the wrong bargain: it multiplies the size for no
// visible gain, and xelatex embeds JPEG without re-encoding it. A diagram is flat line
// art and stays PNG, where lossless is cheap. Chrome picks the format from the
// extension and accepts only '.jpg' — '.jpeg' is refused outright.
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const RASTER_SCALE = 2;
const RASTER_FORMAT = "jpg";

// Two measured facts shape how Chrome is called. It takes a singleton lock on its
// user-data directory, so pointing it at the default profile while the browser is
// open blocks until the browser quits — a build that hangs rather than fails; hence a
// throwaway profile. And given its own profile it writes the screenshot in about two
// and a half seconds and then keeps running rather than exiting, so what is waited on
// is the file settling, not the process. The timeout is only a backstop.
const RASTER_TIMEOUT_MS = 60_000;
const RASTER_POLL_MS = 200;

// The cover is generated, not drawn: an SVG built from book/metadata.yaml with the
// photograph across the bottom, rasterized by headless Chrome. Built rather than
// committed so the title, subtitle and author printed on it cannot drift from the
// metadata pandoc sets inside the book.
//
// A4 proportions in CSS pixels, doubled to 1240x1754 by RASTER_SCALE, which is 150dpi
// on A4. Not larger: the photograph is 752px wide, and a wider cover would only
// upscale it further. It sits flush with the bottom edge at its own aspect ratio, and
// the top of it fades into the page over COVER_FADE of its height.
export const COVER_WIDTH = 620;
export const COVER_HEIGHT = 877;
const COVER_FADE = 0.45;
const COVER_MARGIN = 70;
const COVER_PAPER = "#0A1017";
const COVER_INK = "#F4F7FA";
const COVER_MUTED = "#8FA3B3";
const COVER_ACCENT = "#4FD8E4";

// A bare '---' in the book is a horizontal rule, never metadata.
// normalizeThematicBreaks removes the other readings; this removes the one it cannot.
const PANDOC_READER = "markdown-yaml_metadata_block";

const TABLE_PADDING = "\\renewcommand{\\arraystretch}{1.3}" + "\\setlength{\\extrarowheight}{2pt}";

// Two typesetting problems the book creates for itself.
//
// Identifiers like iam.disableServiceAccountKeyCreation are unbreakable in a
// monospace font and run into the margin; seqsplit adds breakpoints TeX uses only
// when it must, and breaks without a hyphen, which is right for code.
//
// Comparison tables carry prose in four columns, so a step down inside a table keeps
// them on the measure without shrinking the body text. Inside a table the plain
// \texttt is restored: columns are narrow enough that seqsplit would break short
// tokens like split("\n") mid-word, which reads as two tokens. A table cell may then
// run a few points wide, which is the better of the two faults.
//
// Those same four-column tables wrap one row to three or four lines, so rows need
// separating or they run together. Each gets a little vertical padding and a hairline
// above it, drawn at a quarter black so a long table reads as banded rather than as a
// grid. The rules themselves come from book/table-rules.lua, which is the only place
// they can come from — see that file. Padding is deliberately modest: at the 1.45
// arraystretch that reads best on its own, the book grows by twenty-two pages.
//
// Blockquotes in this book are asides: a rule of thumb, a caution, a line worth
// stopping on. Pandoc sets them as an indented paragraph, which at 11pt on a 15.4cm
// measure reads as body text that has drifted right. Each becomes a callout instead —
// warm paper, with an amber bar down the left edge, so it is visibly not the argument
// it interrupts.
//
// mdframed rather than framed's snugshade, on two counts: snugshade takes its colour
// from `shadecolor`, which pandoc's highlighting already owns for code blocks, and it
// draws no rule. mdframed's default style breaks across a page, which a long quote
// needs.
const PDF_CALLOUT =
  "\\usepackage{mdframed}" +
  "\\definecolor{bookcalloutback}{HTML}{FAF4E8}" +
  "\\definecolor{bookcalloutrule}{HTML}{EFAE16}" +
  "\\newmdenv[backgroundcolor=bookcalloutback,linecolor=bookcalloutrule," +
  "linewidth=3pt,topline=false,bottomline=false,rightline=false," +
  "innerleftmargin=12pt,innerrightmargin=12pt,innertopmargin=9pt," +
  "innerbottommargin=9pt,skipabove=0.9\\baselineskip,skipbelow=0.9\\baselineskip," +
  "leftmargin=0pt,rightmargin=0pt]{bookcallout}" +
  "\\renewenvironment{quote}{\\begin{bookcallout}}{\\end{bookcallout}}";

// Glossaries are definition lists, which LaTeX sets run-in: the term in bold at the
// left margin, its definition alongside, the rest of it hung underneath. That is how a
// printed glossary reads and it needs no help. What does need help is a definition
// holding a bulleted list — LaTeX gives a nested itemize a left margin of its own on
// top of the description's, so the bullets land a long way right of the definition they
// belong to and read as a separate block. The margin is narrowed for that nesting only,
// inside the description environment, so every other list in the book is untouched.
const PDF_DEFINITION_LIST =
  "\\usepackage{enumitem}" + "\\AtBeginEnvironment{description}{\\setlist[itemize]{leftmargin=1.2em}}";

const PDF_HEADER_INCLUDES =
  "header-includes=" +
  "\\usepackage{etoolbox}" +
  "\\usepackage{seqsplit}" +
  "\\usepackage{colortbl}" +
  "\\let\\oldtexttt\\texttt" +
  "\\renewcommand{\\texttt}[1]{\\oldtexttt{\\seqsplit{#1}}}" +
  "\\newcommand{\\bookrowrule}{\\arrayrulecolor{black!25}\\hline\\arrayrulecolor{black}}" +
  "\\AtBeginEnvironment{longtable}{\\small\\let\\texttt\\oldtexttt" + TABLE_PADDING + "}" +
  "\\AtBeginEnvironment{tabular}{\\small\\let\\texttt\\oldtexttt" + TABLE_PADDING + "}" +
  PDF_CALLOUT +
  PDF_DEFINITION_LIST;

// The book uses box-drawing characters for diagrams and a few maths symbols in
// prose. TeX's default Latin Modern has none of them, so the PDF needs fonts that
// do. These two are present on macOS; if either is missing the PDF still builds,
// with glyphs dropped.
const PDF_MAIN_FONT = "Times New Roman";
const PDF_MONO_FONT = "Menlo";

export interface Document {
  path: string; // relative to docs/, posix
  title: string;
  body: string;
}

type Fence = string | null;

const warn = (message: string) => console.error(message);

/** Walk the fence state one line forward. Returns whether the line was a fence. */
function fenceStep(fence: Fence, bare: string): [boolean, Fence] {
  const match = FENCE_RE.exec(bare);
  if (!match) return [false, fence];
  const marker = match[1][0];
  return [true, fence === null ? marker : fence === marker ? null : fence];
}

/** The anchor a renderer generates for a heading. Mirrors check_links.slugify. */
export function slugify(title: string): string {
  const text = title.replaceAll("*", "").replaceAll("`", "").trim().toLowerCase();
  return text.replace(UNSLUGGABLE_RE, "").replaceAll(" ", "-");
}

/** Demote every ATX heading by `by` levels, ignoring fenced code blocks. */
export function shiftHeadings(text: string, by = 1): string {
  let fence: Fence = null;
  return text
    .split("\n")
    .map((bare) => {
      let isFence: boolean;
      [isFence, fence] = fenceStep(fence, bare);
      if (isFence) return bare;
      const heading = fence === null ? HEADING_RE.exec(bare) : null;
      if (!heading) return bare;
      const level = heading[1].length + by;
      if (level > 6) throw new Error(`heading would exceed level 6: ${JSON.stringify(bare)}`);
      return "#".repeat(level) + heading[2];
    })
    .join("\n");
}

/** Return the title and the body, dropping the frontmatter block. */
export function splitFrontmatter(text: string): { title: string; body: string } {
  if (!text.startsWith("---\n")) throw new Error("file does not start with frontmatter");
  const end = text.indexOf("\n---\n", 3);
  if (end === -1) throw new Error("unterminated frontmatter");
  const title = TITLE_RE.exec(text.slice(4, end + 1));
  if (!title) throw new Error("frontmatter has no title");
  return {
    title: title[1].replace(/^(["'])(.*)\1$/, "$2"),
    body: text.slice(end + "\n---\n".length).replace(/^\n+/, ""),
  };
}

/** True if the body has a level-1 heading outside fenced code. */
function hasTopHeading(body: string): boolean {
  let fence: Fence = null;
  for (const bare of body.split("\n")) {
    let isFence: boolean;
    [isFence, fence] = fenceStep(fence, bare);
    if (isFence || fence !== null) continue;
    const heading = HEADING_RE.exec(bare);
    if (heading && heading[1].length === 1) return true;
  }
  return false;
}

/**
 * Open the body with `# title` unless it already has a level-1 heading.
 *
 * A knowledge base may keep the title in the frontmatter alone. The builder needs it
 * in the body: the level-1 heading is the document's anchor, and for a chapter opener
 * it is the \chapter itself.
 */
export function ensureTitleHeading(title: string, body: string): string {
  return hasTopHeading(body) ? body : `# ${title}\n\n${body}`;
}

/**
 * Rewrite one document's links for life inside a single assembled document.
 *
 * `source` is the document's path relative to docs/. A link to another document
 * becomes an anchor — its own if the link carried one, otherwise the target
 * document's title. A link to a file outside docs/ (an image) becomes a path
 * relative to the repository root, which is where pandoc is pointed.
 */
export function rewriteLinks(text: string, source: string, anchors: Record<string, string>): string {
  const sourceDir = path.dirname(path.join(DOCS, source));
  const own = () => {
    const anchor = anchors[source];
    if (anchor === undefined) throw new Error(`no anchor for ${source}`);
    return anchor;
  };
  return text.replace(LINK_RE, (whole, bang: string, label: string, target: string) => {
    if (!target || EXTERNAL_PREFIXES.some((prefix) => target.startsWith(prefix))) return whole;
    if (target.startsWith("#")) return `${bang}[${label}](#${own()}--${target.slice(1)})`;
    const hash = target.indexOf("#");
    const file = hash === -1 ? target : target.slice(0, hash);
    const anchor = hash === -1 ? "" : target.slice(hash + 1);
    const resolved = path.resolve(sourceDir, file);
    if (resolved.endsWith(".md") && resolved.startsWith(DOCS + path.sep)) {
      const key = path.relative(DOCS, resolved).split(path.sep).join("/");
      const targetAnchor = anchors[key];
      if (targetAnchor === undefined) throw new Error(`${source} links to unknown document ${key}`);
      return anchor ? `${bang}[${label}](#${targetAnchor}--${anchor})` : `${bang}[${label}](#${targetAnchor})`;
    }
    const relative = path.relative(ROOT, resolved);
    if (relative.startsWith("..")) return whole;
    return `${bang}[${label}](${relative.split(path.sep).join("/")})`;
  });
}

/** The source of every mermaid block, in document order. */
export function extractMermaid(markdown: string): string[] {
  return [...markdown.matchAll(MERMAID_FENCE_RE)].map((match) => match[1]);
}

/**
 * The name of a rasterized PNG: a digest of the source it was rendered from.
 *
 * Content-addressing gives the cache for free — an unchanged source is already on
 * disk and is never re-rendered, and an edited one cannot be confused with its own
 * earlier version. Callers fold the render scale into what they hash, because
 * otherwise retuning a scale would serve every old PNG as a hit forever. Trailing
 * whitespace is normalized away so a cosmetic edit does not cost a render.
 */
export function rasterHash(source: string): string {
  const normalized = source
    .trim()
    .split("\n")
    .map((line) => line.replace(/\s+$/, ""))
    .join("\n");
  return createHash("sha256").update(normalized).digest("hex").slice(0, 12);
}

/** Where a diagram's PNG lives. Under build/, so it is a build artifact. */
function diagramPath(source: string): string {
  return path.join(DIAGRAMS, `${rasterHash(`${DIAGRAM_SCALE}\n${source}`)}.png`);
}

/**
 * Swap each mermaid block for its rendered image, positionally.
 *
 * A `null` image leaves that block as it was: a diagram that would not render stays
 * a code block, which is what the book prints today, so a renderer that is missing
 * or broken degrades the output instead of failing the build.
 */
export function replaceMermaid(markdown: string, images: (string | null)[]): string {
  const sources = extractMermaid(markdown);
  if (images.length !== sources.length) {
    throw new Error(`${sources.length} mermaid blocks but ${images.length} images`);
  }
  let index = 0;
  // Empty alt text: pandoc turns an image *with* alt text into a captioned,
  // floating figure, which would reorder the diagrams away from their prose.
  return markdown.replace(MERMAID_FENCE_RE, (whole) => {
    const image = images[index++];
    return image === null ? whole : `![](${image})`;
  });
}

/**
 * Render `jobs`, a list of [destination, source], in one mermaid-cli run.
 *
 * Given a markdown input, mermaid-cli renders every block it finds in a single
 * browser launch and numbers the output files by each block's *position in the
 * input* — not by the order the concurrent renders finish. That is what makes the
 * rename to <hash>.png safe, and it is why the diagrams are batched through a
 * scratch document rather than invoked one at a time.
 */
function runMermaidCli(jobs: [string, string][]): void {
  const scratch = path.join(BUILD, "diagrams-pending.md");
  const rendered = path.join(BUILD, "diagrams-rendered.md");
  const stem = "diagrams-rendered";
  // An interrupted earlier run can leave numbered PNGs behind, and this run's
  // numbering means something different. Clear them or one could be renamed to a
  // hash it is not a render of.
  for (const stale of fs.readdirSync(BUILD)) {
    if (stale.startsWith(`${stem}-`) && stale.endsWith(".png")) fs.unlinkSync(path.join(BUILD, stale));
  }
  fs.writeFileSync(scratch, jobs.map(([, source]) => `\`\`\`mermaid\n${source}\n\`\`\``).join("\n\n") + "\n");
  const args = [
    "-y", "-p", MERMAID_CLI, "mmdc",
    "-i", scratch, "-o", rendered,
    "-e", "png", "--scale", String(DIAGRAM_SCALE), "--backgroundColor", "white",
  ];
  try {
    const result = spawnSync("npx", args, { cwd: ROOT, encoding: "utf8" });
    if (result.error) {
      warn("  warning: npx is not installed, so diagrams stay as code blocks");
      return;
    }
    if (result.status !== 0) {
      warn(`  warning: mermaid-cli failed, so diagrams stay as code blocks\n${result.stderr.trim()}`);
      return;
    }
  } finally {
    fs.rmSync(scratch, { force: true });
    fs.rmSync(rendered, { force: true });
  }
  jobs.forEach(([destination], index) => {
    const produced = path.join(BUILD, `${stem}-${index + 1}.png`);
    if (fs.existsSync(produced)) fs.renameSync(produced, destination);
  });
}

/**
 * The PNG path of each source, or null where no PNG was produced.
 *
 * Only uncached diagrams are rendered, and identical diagrams share one render.
 * Paths come back relative to the repository root, which is where pandoc is pointed,
 * alongside the number of PNGs this run actually produced.
 */
function renderDiagrams(sources: string[]): { paths: (string | null)[]; rendered: number } {
  fs.mkdirSync(DIAGRAMS, { recursive: true });
  const pending = new Map<string, string>();
  for (const source of sources) {
    const destination = diagramPath(source);
    if (!fs.existsSync(destination) && !pending.has(destination)) pending.set(destination, source);
  }
  if (pending.size) runMermaidCli([...pending.entries()]);
  const paths = sources.map((source) => {
    const file = diagramPath(source);
    return fs.existsSync(file) ? path.relative(ROOT, file).split(path.sep).join("/") : null;
  });
  const rendered = [...pending.keys()].filter((file) => fs.existsSync(file)).length;
  return { paths, rendered };
}

/**
 * Replace every mermaid block with a rendered PNG.
 *
 * Returns the markdown, how many blocks became images, and how many of those cost a
 * render rather than a cache hit.
 */
function resolveMermaid(markdown: string): { markdown: string; diagrams: number; rendered: number } {
  const sources = extractMermaid(markdown);
  if (!sources.length) return { markdown, diagrams: 0, rendered: 0 };
  const { paths, rendered } = renderDiagrams(sources);
  const unresolved = paths.filter((image) => image === null).length;
  if (unresolved) {
    warn(`  warning: ${unresolved} of ${sources.length} diagrams did not render and stay as code blocks`);
  }
  return { markdown: replaceMermaid(markdown, paths), diagrams: sources.length - unresolved, rendered };
}

/**
 * The pixel size an SVG should be screenshotted at.
 *
 * Chrome's window is the viewport it captures, so a wrong size crops the cover or
 * pads it with blank paper. A declared pixel width and height win; a relative one
 * says nothing about intrinsic size, so the viewBox answers instead.
 */
export function svgSize(markup: string): [number, number] {
  const root = /<svg\b([^>]*)>/i.exec(markup);
  if (!root) throw new Error("markup has no <svg> element");
  const attribute = (name: string) => new RegExp(`\\b${name}="([^"]*)"`).exec(root[1])?.[1] ?? "";
  const width = attribute("width").replace(/px$/, "");
  const height = attribute("height").replace(/px$/, "");
  if (/^\d+$/.test(width) && /^\d+$/.test(height)) return [Number(width), Number(height)];
  const box = attribute("viewBox").trim().split(/\s+/);
  if (box.length === 4) return [Math.round(Number(box[2])), Math.round(Number(box[3]))];
  throw new Error("svg declares neither a pixel size nor a viewBox");
}

const sleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));

/**
 * Wait until `file` has been written and has stopped growing. True if it was.
 *
 * Chrome does not exit after taking its screenshot, so there is no exit code to
 * wait for: the file appearing, and then holding its size across two polls, is the
 * signal that it is complete rather than half-written.
 */
async function settled(file: string, child: ChildProcess): Promise<boolean> {
  const deadline = Date.now() + RASTER_TIMEOUT_MS;
  let previous = -1;
  while (Date.now() < deadline) {
    await sleep(RASTER_POLL_MS);
    if (!fs.existsSync(file)) {
      if (child.exitCode !== null) return false; // chrome gave up before writing anything
      continue;
    }
    const { size } = fs.statSync(file);
    if (size && size === previous) return true;
    previous = size;
  }
  return false;
}

/**
 * Screenshot one SVG with headless Chrome. True if the image was written.
 *
 * `profile` is a throwaway user-data directory, and the screenshot lands on a
 * partial path that is renamed into place only once complete — see RASTER_TIMEOUT_MS
 * for why, and note that a half-written file left in the cache would otherwise be
 * served as a hit forever.
 */
async function rasterizeSvg(svg: string, destination: string, profile: string): Promise<boolean> {
  if (!fs.existsSync(CHROME)) return false;
  let width: number;
  let height: number;
  try {
    [width, height] = svgSize(fs.readFileSync(svg, "utf8"));
  } catch (error) {
    warn(`  warning: cannot size ${path.basename(svg)}: ${(error as Error).message}`);
    return false;
  }
  // Chrome picks the format from the extension and refuses anything it does not
  // know, so the in-progress name keeps the real extension last rather than
  // appending .part to it.
  const extension = path.extname(destination);
  const partial = path.join(path.dirname(destination), `${path.basename(destination, extension)}.part${extension}`);
  fs.rmSync(partial, { force: true });
  const child = spawn(
    CHROME,
    [
      "--headless", "--disable-gpu", "--hide-scrollbars",
      "--no-first-run", "--no-default-browser-check",
      `--user-data-dir=${profile}`,
      `--window-size=${width},${height}`,
      `--force-device-scale-factor=${RASTER_SCALE}`,
      `--screenshot=${partial}`,
      pathToFileURL(svg).href,
    ],
    { stdio: "ignore", cwd: ROOT },
  );
  let written: boolean;
  try {
    written = await settled(partial, child);
  } finally {
    child.kill();
  }
  if (!written) {
    warn(`  warning: rasterizing ${path.basename(svg)} did not finish within ${RASTER_TIMEOUT_MS / 1000}s`);
    fs.rmSync(partial, { force: true });
    return false;
  }
  fs.renameSync(partial, destination);
  return true;
}

/** [width, height] from a PNG's IHDR, which is always the first chunk. */
export function pngSize(file: string): [number, number] {
  const header = fs.readFileSync(file).subarray(0, 24);
  if (header.subarray(0, 8).toString("latin1") !== "\x89PNG\r\n\x1a\n") {
    throw new Error(`${path.basename(file)} is not a PNG`);
  }
  return [header.readUInt32BE(16), header.readUInt32BE(20)];
}

/**
 * The three fields the cover prints, read from book/metadata.yaml.
 *
 * A deliberately small reader rather than a YAML parser: these are plain scalars on
 * one line each, and the file's only other shapes — a folded description and a list
 * of subjects — are not wanted here.
 */
export function coverFields(metadata: string): [string, string, string] {
  const fields: Record<string, string> = {};
  for (const [, key, value] of metadata.matchAll(METADATA_FIELD_RE)) {
    fields[key] = value.replace(/^["']+|["']+$/g, "");
  }
  return [fields.title ?? "", fields.subtitle ?? "", fields.author ?? ""];
}

/**
 * A file as a data: URI, so the generated SVG is self-contained.
 *
 * Self-contained is what makes the cache correct: the digest that names the
 * rasterized cover is taken over the SVG's text, so with the photograph inside it a
 * replaced photograph changes the digest and the cover is re-rendered.
 */
function dataUri(file: string, mediaType: string): string {
  return `data:${mediaType};base64,${fs.readFileSync(file).toString("base64")}`;
}

/** Greedy word wrap, like Python's textwrap.wrap: a word longer than the width is split. */
export function wrap(text: string, width: number): string[] {
  const lines: string[] = [];
  let current = "";
  for (let word of text.split(/\s+/).filter(Boolean)) {
    while (word.length > width) {
      const room = current ? width - current.length - 1 : width;
      if (room > 0) {
        lines.push(current ? `${current} ${word.slice(0, room)}` : word.slice(0, room));
        word = word.slice(room);
      } else {
        lines.push(current);
      }
      current = "";
    }
    if (!current) current = word;
    else if (current.length + 1 + word.length <= width) current += ` ${word}`;
    else {
      lines.push(current);
      current = word;
    }
  }
  if (current) lines.push(current);
  return lines;
}

/** The three characters XML markup cannot carry as text. */
const escapeXml = (text: string) => text.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");

/** One <text> element per line. SVG does no line breaking of its own. */
function textLines(markup: string[], lines: string[], x: number, y: number, leading: number, cssClass: string): number {
  lines.forEach((line, index) => {
    markup.push(`  <text class="${cssClass}" x="${x}" y="${y + index * leading}">${escapeXml(line)}</text>`);
  });
  return y + Math.max(lines.length - 1, 0) * leading;
}

/**
 * The cover as SVG markup: type block above, the photograph along the bottom.
 *
 * The photograph keeps its own aspect ratio at full cover width, so how much of the
 * page it covers follows from the image rather than from a number chosen here. Its
 * top fades to nothing against the page, which is why the page is dark: the
 * photograph is, and fading it into a light page would only muddy it.
 */
export function coverSvg(title: string, subtitle: string, author: string, photo: string, photoAspect: number): string {
  const photoHeight = Math.round(COVER_WIDTH / photoAspect);
  const photoTop = COVER_HEIGHT - photoHeight;
  const titleLines = wrap(title, 16);
  if (!titleLines.length) titleLines.push("");
  const subtitleLines = wrap(subtitle, 44);
  const markup = [
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${COVER_WIDTH} ${COVER_HEIGHT}" ` +
      `width="${COVER_WIDTH}" height="${COVER_HEIGHT}" role="img" aria-label="${escapeXml(title)}">`,
    "  <defs>",
    `    <linearGradient id="fade" x1="0" y1="${photoTop}" x2="0" ` +
      `y2="${photoTop + Math.round(photoHeight * COVER_FADE)}" gradientUnits="userSpaceOnUse">`,
    '      <stop offset="0" stop-color="#fff" stop-opacity="0"/>',
    '      <stop offset="1" stop-color="#fff" stop-opacity="1"/>',
    "    </linearGradient>",
    `    <mask id="fadeMask"><rect x="0" y="${photoTop}" width="${COVER_WIDTH}" ` +
      `height="${photoHeight}" fill="url(#fade)"/></mask>`,
    "    <style>",
    '      text { font-family: "Times New Roman", Georgia, serif; }',
    `      .title { font-size: 58px; fill: ${COVER_INK}; }`,
    `      .subtitle { font-size: 19px; fill: ${COVER_MUTED}; }`,
    `      .author { font-size: 16px; fill: ${COVER_INK}; letter-spacing: 3px; text-transform: uppercase; }`,
    "    </style>",
    "  </defs>",
    `  <rect width="${COVER_WIDTH}" height="${COVER_HEIGHT}" fill="${COVER_PAPER}"/>`,
    `  <image href="${photo}" x="0" y="${photoTop}" width="${COVER_WIDTH}" ` +
      `height="${photoHeight}" mask="url(#fadeMask)" preserveAspectRatio="xMidYMid slice"/>`,
    `  <rect x="${COVER_MARGIN}" y="168" width="84" height="3" fill="${COVER_ACCENT}"/>`,
  ];
  let last = textLines(markup, titleLines, COVER_MARGIN, 226, 66, "title");
  last = textLines(markup, subtitleLines, COVER_MARGIN, last + 74, 28, "subtitle");
  textLines(markup, [author.toUpperCase()], COVER_MARGIN, last + 66, 0, "author");
  markup.push("</svg>");
  return markup.join("\n") + "\n";
}

/**
 * Render the cover and return its path relative to ROOT, or null if it was not.
 *
 * Content-addressed, so the cover costs a render only when the metadata or the
 * photograph changes. The directory holds exactly one cover: unlike a diagram, there
 * is never a second one to serve, so a superseded file is removed rather than left in
 * the cache.
 */
async function buildCover(): Promise<string | null> {
  if (!fs.existsSync(COVER_PHOTO)) {
    warn(`  warning: ${path.basename(COVER_PHOTO)} is missing; the book has no cover`);
    return null;
  }
  if (!fs.existsSync(CHROME)) {
    warn("  warning: Chrome is missing; the book has no cover");
    return null;
  }
  const [width, height] = pngSize(COVER_PHOTO);
  const [title, subtitle, author] = coverFields(fs.readFileSync(METADATA, "utf8"));
  const markup = coverSvg(title, subtitle, author, dataUri(COVER_PHOTO, "image/png"), width / height);
  fs.mkdirSync(COVERS, { recursive: true });
  const destination = path.join(COVERS, `${rasterHash(`${RASTER_SCALE}\n${markup}`)}.${RASTER_FORMAT}`);
  if (!fs.existsSync(destination)) {
    const source = path.join(COVERS, "cover.svg");
    fs.writeFileSync(source, markup);
    const profile = fs.mkdtempSync(path.join(os.tmpdir(), "book-cover-"));
    let written: boolean;
    try {
      written = await rasterizeSvg(source, destination, profile);
    } finally {
      fs.rmSync(profile, { recursive: true, force: true });
      fs.rmSync(source, { force: true });
    }
    if (!written) return null;
    for (const stale of fs.readdirSync(COVERS)) {
      const file = path.join(COVERS, stale);
      if (stale.endsWith(`.${RASTER_FORMAT}`) && file !== destination) fs.unlinkSync(file);
    }
    console.log(`  cover rendered -> ${destination}`);
  }
  return path.relative(ROOT, destination).split(path.sep).join("/");
}

/**
 * LaTeX that opens the PDF on a full-bleed cover page.
 *
 * AtBeginDocument rather than an --include-before-body file, because pandoc's
 * template puts \maketitle before the includes and the cover has to come first.
 * Margins are dropped for that one page so the photograph reaches the paper's edge,
 * and restored immediately after; the cover is A4-proportioned, so asking for both
 * the paper's width and its height does not stretch it.
 *
 * \maketitle is then emptied: the cover already carries the title, the subtitle and
 * the author, and pandoc's title page would otherwise repeat all three overleaf.
 */
function pdfCoverInclude(cover: string): string {
  return (
    "header-includes=" +
    "\\renewcommand{\\maketitle}{}" +
    "\\AtBeginDocument{" +
    "\\newgeometry{margin=0pt}" +
    "\\thispagestyle{empty}" +
    `\\noindent\\includegraphics[width=\\paperwidth,height=\\paperheight]{${cover}}` +
    "\\clearpage" +
    "\\restoregeometry}"
  );
}

/**
 * Close void HTML elements, so `<br>` becomes `<br/>`, outside fenced blocks.
 *
 * EPUB3 is XHTML, and pandoc passes raw inline HTML through verbatim rather than
 * parsing it. A bare `<br>` in a table cell therefore reaches the EPUB as a
 * mismatched tag, and a conforming reader abandons the rest of that page. The
 * glossary convention asks authors for `<br>` in a multi-line cell, so the builder is
 * the right place to make it well-formed. Fences are skipped: mermaid uses `<br/>` in
 * labels, and a fence is not HTML.
 */
export function closeVoidTags(text: string): string {
  let fence: Fence = null;
  return text
    .split("\n")
    .map((bare) => {
      let isFence: boolean;
      [isFence, fence] = fenceStep(fence, bare);
      if (isFence || fence !== null) return bare;
      // trimEnd: the attribute group absorbs the space in `<br />`, which would
      // otherwise come back out as `<br />` rather than a uniform `<br/>`.
      return bare.replace(VOID_TAG_RE, (_, tag: string, attributes: string) => `<${tag}${attributes.trimEnd()}/>`);
    })
    .join("\n");
}

/**
 * Rewrite '---' rules as '***'.
 *
 * A bare dashed line is ambiguous in pandoc's markdown: a YAML metadata block, a
 * setext heading underline, or a multiline-table delimiter. Read as the last of
 * those it swallows every following heading into table cells, silently and with a
 * zero exit code. '***' is only ever a horizontal rule.
 */
export function normalizeThematicBreaks(text: string): string {
  let fence: Fence = null;
  return text
    .split("\n")
    .map((bare) => {
      let isFence: boolean;
      [isFence, fence] = fenceStep(fence, bare);
      if (isFence) return bare;
      return fence === null && THEMATIC_BREAK_RE.test(bare) ? "***" : bare;
    })
    .join("\n");
}

/**
 * Give every heading an explicit, globally unique id.
 *
 * A level-1 heading is the document itself, so it takes the document's anchor.
 * Everything below is namespaced under it, because section names like 'Best
 * Practices' repeat across chapters and a renderer would silently renumber them.
 */
export function addHeadingIds(text: string, documentAnchor: string): string {
  let fence: Fence = null;
  const seen = new Map<string, number>();
  return text
    .split("\n")
    .map((bare) => {
      let isFence: boolean;
      [isFence, fence] = fenceStep(fence, bare);
      if (isFence) return bare;
      const heading = fence === null ? HEADING_RE.exec(bare) : null;
      if (!heading) return bare;
      const [, hashes, textPart] = heading;
      let anchor = hashes.length === 1 ? documentAnchor : `${documentAnchor}--${slugify(textPart)}`;
      const repeats = seen.get(anchor) ?? 0;
      seen.set(anchor, repeats + 1);
      if (repeats) anchor = `${anchor}-${repeats}`;
      return `${hashes}${textPart.trimEnd()} {#${anchor}}`;
    })
    .join("\n");
}

/** One unique anchor per document, keyed by its path relative to docs/. */
export function documentAnchors(documents: Document[]): Record<string, string> {
  const anchors: Record<string, string> = {};
  const taken = new Set<string>();
  for (const { path: docPath, title } of documents) {
    let candidate = slugify(title);
    if (taken.has(candidate)) candidate = `${slugify(docPath.split("/")[0])}--${candidate}`;
    for (let suffix = 2; taken.has(candidate); suffix++) candidate = `${candidate}-${suffix}`;
    anchors[docPath] = candidate;
    taken.add(candidate);
  }
  return anchors;
}

/**
 * welcome.md, then chapters in folder order, each led by its index.md, then any
 * other root file as back matter (quotations, a translations table).
 */
export function inReadingOrder(paths: string[]): string[] {
  const key = (docPath: string): [number, string, string] => {
    const parts = docPath.split("/");
    if (docPath === "welcome.md") return [0, "", ""];
    if (parts.length === 1) return [2, parts[0], ""];
    return [1, parts[0], parts[1] === "index.md" ? "" : parts[1]];
  };
  const compare = (a: [number, string, string], b: [number, string, string]) => {
    for (let i = 0; i < 3; i++) {
      if (a[i] < b[i]) return -1;
      if (a[i] > b[i]) return 1;
    }
    return 0;
  };
  return [...paths].sort((a, b) => compare(key(a), key(b)));
}

/** Every *.md under `dir`, as posix paths relative to it. */
function markdownFiles(dir: string, prefix = ""): string[] {
  const files: string[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name;
    if (entry.isDirectory()) files.push(...markdownFiles(path.join(dir, entry.name), relative));
    else if (entry.name.endsWith(".md")) files.push(relative);
  }
  return files;
}

/** Every document under docs/, in reading order. */
function collectDocuments(): Document[] {
  const paths = inReadingOrder(markdownFiles(DOCS).filter((docPath) => !NOT_CONTENT.has(docPath)));
  return paths.map((docPath) => {
    const { title, body } = splitFrontmatter(fs.readFileSync(path.join(DOCS, docPath), "utf8"));
    return { path: docPath, title, body: ensureTitleHeading(title, body) };
  });
}

/**
 * Open a document on a fresh page, in both formats.
 *
 * A folder's index.md is a \chapter and already breaks; its siblings are \section,
 * which does not, so the PDF needs an explicit \clearpage. The EPUB has no pages of
 * its own, but a paginated reader honours a CSS break, and pandoc puts a heading's
 * classes on the <section> it wraps — so the opening heading is marked `.document`
 * and book/epub.css hangs the break on that.
 */
export function startOnANewPage(body: string): string {
  const marked = body.replace(DOCUMENT_HEADING_RE, "$1 .document}");
  return `${PAGE_BREAK}\n\n${marked}`;
}

/**
 * One markdown document. A folder's index.md keeps its level, so it reads as the
 * chapter opener; its siblings are demoted under it.
 */
export function assemble(documents: Document[]): string {
  const anchors = documentAnchors(documents);
  const chunks = documents.map(({ path: docPath, body }) => {
    const isChapterOpener = docPath === "welcome.md" || docPath.endsWith("/index.md");
    let text = closeVoidTags(normalizeThematicBreaks(body));
    text = addHeadingIds(rewriteLinks(text, docPath, anchors), anchors[docPath]);
    return isChapterOpener ? text : startOnANewPage(shiftHeadings(text));
  });
  return chunks.map((chunk) => chunk.replace(/\n+$/, "")).join("\n\n") + "\n";
}

/** Heading slugs that occur more than once, which a renderer will rename. */
export function duplicateAnchors(markdown: string): string[] {
  const seen = new Map<string, number>();
  const duplicates: string[] = [];
  let fence: Fence = null;
  for (const line of markdown.split("\n")) {
    let isFence: boolean;
    [isFence, fence] = fenceStep(fence, line);
    if (isFence) continue;
    const heading = fence === null ? HEADING_RE.exec(line) : null;
    if (!heading) continue;
    const explicit = EXPLICIT_ID_RE.exec(heading[2]);
    const slug = explicit ? explicit[1] : slugify(heading[2]);
    const count = (seen.get(slug) ?? 0) + 1;
    seen.set(slug, count);
    if (count === 2) duplicates.push(slug);
  }
  return duplicates;
}

/** Run a command to completion, inheriting the terminal. Throws on a nonzero exit. */
function run(command: string, args: string[]): void {
  const result = spawnSync(command, args, { cwd: ROOT, stdio: "inherit" });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${command} exited with status ${result.status}`);
}

/** Run a command and return its stdout. Throws on a nonzero exit. */
function capture(command: string, args: string[]): string {
  const result = spawnSync(command, args, { cwd: ROOT, encoding: "utf8" });
  if (result.error) throw result.error;
  if (result.status !== 0) throw new Error(`${command} exited with status ${result.status}\n${result.stderr}`);
  return result.stdout;
}

/**
 * Check that pandoc sees every heading and link the assembled file declares.
 *
 * Markdown is ambiguous enough that a document can render with a zero exit code and
 * a quietly mangled structure — headings absorbed into a table, say. This renders to
 * HTML and compares what arrived against what was written.
 */
function verifyAnchors(markdownPath: string): string[] {
  const html = capture("pandoc", [markdownPath, "--from", PANDOC_READER, "--to", "html5", "--section-divs"]);
  const markdown = fs.readFileSync(markdownPath, "utf8");
  const declared = new Set([...markdown.matchAll(DECLARED_ID_RE)].map((match) => match[1]));
  const rendered = new Set([...html.matchAll(/id="([^"]+)"/g)].map((match) => match[1]));
  const linked = new Set([...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]));
  const problems: string[] = [];
  for (const anchor of [...declared].filter((id) => !rendered.has(id)).sort()) {
    problems.push(`heading id '${anchor}' was declared but did not render`);
  }
  for (const anchor of [...linked].filter((id) => !rendered.has(id)).sort()) {
    problems.push(`link target '#${anchor}' matches no heading`);
  }
  return problems;
}

/** Run pandoc for one output format. */
function render(markdownPath: string, target: "epub" | "pdf", outPath: string, cover: string | null): void {
  const args = [
    markdownPath,
    "--from", PANDOC_READER,
    "--toc", "--toc-depth=2",
    "--resource-path", ROOT,
    "--metadata-file", METADATA,
    "--output", outPath,
  ];
  if (target === "pdf") {
    args.push(
      "--pdf-engine", "xelatex",
      // A reading book, not a paper: chapters open on a fresh page, the folder is
      // the chapter, and the measure is wide enough for four-column tables.
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
      // table-rules.lua hands each table back as a raw block, so pandoc stops seeing
      // a table in the document and its template stops loading longtable and
      // booktabs. This says to load them anyway.
      "--lua-filter", TABLE_RULES,
      "-V", "tables=true",
    );
    // A second -V of the same name: pandoc collects them, so this joins
    // PDF_HEADER_INCLUDES in the preamble rather than replacing it.
    if (cover) args.push("-V", pdfCoverInclude(cover));
    const fonts = ["-V", `mainfont=${PDF_MAIN_FONT}`, "-V", `monofont=${PDF_MONO_FONT}`];
    if (spawnSync("pandoc", [...args, ...fonts], { cwd: ROOT, stdio: "inherit" }).status === 0) return;
    warn(
      `  warning: ${PDF_MAIN_FONT}/${PDF_MONO_FONT} unavailable, falling back to the TeX default; ` +
        "diagram characters will be missing",
    );
  } else {
    // --css REPLACES pandoc's default EPUB stylesheet rather than adding to it, which
    // would drop the book's baseline typography. So ask pandoc for its own default
    // and layer ours on top: two --css arguments are embedded and linked in order,
    // and this keeps the default in step with whatever pandoc is installed rather
    // than vendoring a copy that goes stale.
    const defaultCss = path.join(BUILD, "epub-default.css");
    fs.writeFileSync(defaultCss, capture("pandoc", ["--print-default-data-file", "epub.css"]));
    args.push("--to", "epub3", "--split-level=1", "--css", defaultCss, "--css", EPUB_CSS);
    if (cover) args.push("--epub-cover-image", cover);
  }
  run("pandoc", args);
}

const USAGE = `usage: bun scripts/build_book.ts [--epub] [--pdf] [--markdown]

  --epub      build the EPUB only
  --pdf       build the PDF only
  --markdown  assemble build/${BOOK}.md and stop`;

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

export async function main(argv: string[] = process.argv.slice(2)): Promise<number> {
  const flags = new Set(argv);
  for (const flag of flags) {
    if (!["--epub", "--pdf", "--markdown", "--help", "-h"].includes(flag)) fail(`unknown option ${flag}\n\n${USAGE}`);
  }
  if (flags.has("--help") || flags.has("-h")) {
    console.log(USAGE);
    return 0;
  }
  const markdownOnly = flags.has("--markdown");

  if (!markdownOnly && spawnSync("pandoc", ["--version"]).error) fail("pandoc is not installed: brew install pandoc");

  const documents = collectDocuments();
  fs.mkdirSync(BUILD, { recursive: true });

  // Before the assembled file is written, so that what verifyAnchors checks and what
  // pandoc reads are the same document. --markdown renders diagrams too: they are
  // the markdown's own content, and a cache hit costs nothing.
  const { markdown, diagrams, rendered } = resolveMermaid(assemble(documents));

  const source = path.join(BUILD, `${BOOK}.md`);
  fs.writeFileSync(source, markdown);
  const words = markdown.split(/\s+/).filter(Boolean).length;
  console.log(`assembled ${documents.length} documents, ${words.toLocaleString("en-US")} words -> ${source}`);
  if (diagrams) {
    console.log(`  ${diagrams} mermaid diagram(s): ${rendered} rendered, ${diagrams - rendered} cached -> ${DIAGRAMS}`);
  }

  for (const slug of duplicateAnchors(markdown)) warn(`  warning: heading slug '${slug}' occurs more than once`);

  const problems = verifyAnchors(source);
  for (const problem of problems) warn(`  error: ${problem}`);
  if (problems.length) fail(`${problems.length} structural problem(s); not rendering`);
  console.log("  structure verified: every heading and link target resolves");

  if (markdownOnly) return 0;

  // Both formats take the same cover, so it is rendered once, before either.
  const cover = await buildCover();

  const both = !(flags.has("--epub") || flags.has("--pdf"));
  if (flags.has("--epub") || both) {
    const out = path.join(BUILD, `${BOOK}.epub`);
    render(source, "epub", out, cover);
    console.log(`wrote ${out}`);
  }
  if (flags.has("--pdf") || both) {
    const out = path.join(BUILD, `${BOOK}.pdf`);
    render(source, "pdf", out, cover);
    console.log(`wrote ${out}`);
  }
  return 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().then((code) => process.exit(code));
}
