"""Tests for the book builder's text transforms."""

import pathlib
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree

import build_book


class ShiftHeadings(unittest.TestCase):
    def test_demotes_a_heading_one_level(self):
        self.assertEqual(build_book.shift_headings("# Title\n"), "## Title\n")

    def test_demotes_every_level(self):
        self.assertEqual(
            build_book.shift_headings("# One\n\n## Two\n\n### Three\n"),
            "## One\n\n### Two\n\n#### Three\n",
        )

    def test_leaves_a_hash_inside_a_fenced_block_alone(self):
        source = "# Title\n\n```sh\n# a shell comment\n```\n\n## After\n"
        expected = "## Title\n\n```sh\n# a shell comment\n```\n\n### After\n"
        self.assertEqual(build_book.shift_headings(source), expected)

    def test_handles_tilde_fences(self):
        source = "~~~\n# not a heading\n~~~\n\n# Real\n"
        expected = "~~~\n# not a heading\n~~~\n\n## Real\n"
        self.assertEqual(build_book.shift_headings(source), expected)

    def test_refuses_to_push_past_level_six(self):
        with self.assertRaises(ValueError):
            build_book.shift_headings("###### Six\n")


class NormalizeThematicBreaks(unittest.TestCase):
    """A bare '---' is ambiguous in pandoc's markdown: YAML metadata, a setext
    underline, or a multiline-table delimiter. Emit '***', which is only ever a
    horizontal rule."""

    def test_a_bare_rule_becomes_asterisks(self):
        self.assertEqual(
            build_book.normalize_thematic_breaks("a\n\n---\n\nb\n"),
            "a\n\n***\n\nb\n",
        )

    def test_a_longer_rule_becomes_asterisks(self):
        self.assertEqual(
            build_book.normalize_thematic_breaks("-----\n"), "***\n"
        )

    def test_a_table_delimiter_row_is_untouched(self):
        self.assertEqual(
            build_book.normalize_thematic_breaks("| --- | --- |\n"), "| --- | --- |\n"
        )

    def test_a_rule_inside_a_fence_is_untouched(self):
        source = "```\n---\n```\n"
        self.assertEqual(build_book.normalize_thematic_breaks(source), source)

    def test_a_list_item_is_untouched(self):
        self.assertEqual(
            build_book.normalize_thematic_breaks("- item\n"), "- item\n"
        )


class CloseVoidTags(unittest.TestCase):
    """EPUB3 is XHTML and pandoc passes raw inline HTML through verbatim, so a bare
    <br> in a table cell is a mismatched tag that makes a conforming reader abandon
    the whole page at that point."""

    def test_a_bare_break_is_closed(self):
        self.assertEqual(build_book.close_void_tags("a<br>b\n"), "a<br/>b\n")

    def test_an_already_closed_break_is_left_alone(self):
        self.assertEqual(build_book.close_void_tags("a<br/>b\n"), "a<br/>b\n")

    def test_a_spaced_break_is_normalized(self):
        self.assertEqual(build_book.close_void_tags("a<br />b\n"), "a<br/>b\n")

    def test_attributes_are_kept(self):
        self.assertEqual(
            build_book.close_void_tags('<img src="x.png" alt="y">\n'),
            '<img src="x.png" alt="y"/>\n',
        )

    def test_a_break_inside_a_fence_is_untouched(self):
        """Mermaid uses <br/> for label breaks, and a fence is not HTML anyway."""
        source = '```mermaid\nA["one<br/>two"] --> B\n```\n'
        self.assertEqual(build_book.close_void_tags(source), source)

    def test_a_paired_tag_is_untouched(self):
        self.assertEqual(build_book.close_void_tags("<td>x</td>\n"), "<td>x</td>\n")

    def test_a_table_cell_is_fixed_in_place(self):
        self.assertEqual(
            build_book.close_void_tags("| **T** | one<br>two |\n"),
            "| **T** | one<br/>two |\n",
        )


class Frontmatter(unittest.TestCase):
    def test_returns_the_title_and_opens_the_body_with_it_as_the_heading(self):
        """A document has no H1 of its own; the book needs one for the chapter."""
        source = "---\ntype: Guide\ntitle: CI/CD\ndescription: d\ntags: [a]\n---\n\nBody.\n"
        title, body = build_book.split_frontmatter(source)
        self.assertEqual(title, "CI/CD")
        self.assertEqual(body, "# CI/CD\n\nBody.\n")

    def test_rejects_a_file_with_no_frontmatter(self):
        with self.assertRaises(ValueError):
            build_book.split_frontmatter("# Heading\n")


class AddHeadingIds(unittest.TestCase):
    """Every heading gets a globally unique id, because 60 files become one file
    and generic section names like 'Best Practices' repeat across chapters."""

    def test_the_top_heading_takes_the_document_anchor(self):
        self.assertEqual(
            build_book.add_heading_ids("# Clouds\n", "clouds"),
            "# Clouds {#clouds}\n",
        )

    def test_a_lower_heading_is_namespaced_by_the_document(self):
        self.assertEqual(
            build_book.add_heading_ids("## Best Practices\n", "caching"),
            "## Best Practices {#caching--best-practices}\n",
        )

    def test_a_repeated_heading_is_numbered_like_check_links_does(self):
        self.assertEqual(
            build_book.add_heading_ids("## A\n\n## A\n", "d"),
            "## A {#d--a}\n\n## A {#d--a-1}\n",
        )

    def test_a_hash_inside_a_fence_gets_no_id(self):
        source = "```sh\n# a comment\n```\n"
        self.assertEqual(build_book.add_heading_ids(source, "x"), source)


class RewriteLinks(unittest.TestCase):
    def setUp(self):
        self.anchors = {
            "03-system-design/05-containers.md": "containers",
            "07-clouds/01-concept-map.md": "concepts-across-the-clouds",
            "07-clouds/index.md": "clouds",
            "10-humans/21-interview.md": "interviewing",
            "06-frontend/index.md": "frontend",
            "welcome.md": "welcome",
        }

    def rewrite(self, text, source="03-system-design/05-containers.md"):
        return build_book.rewrite_links(text, source, self.anchors)

    def test_anchored_cross_doc_link_is_namespaced_to_the_target(self):
        self.assertEqual(
            self.rewrite("see [x](../07-clouds/01-concept-map.md#compute--containers)"),
            "see [x](#concepts-across-the-clouds--compute--containers)",
        )

    def test_bare_cross_doc_link_points_at_the_target_title(self):
        self.assertEqual(
            self.rewrite("see [x](../10-humans/21-interview.md)"),
            "see [x](#interviewing)",
        )

    def test_same_file_anchor_is_namespaced_to_its_own_document(self):
        self.assertEqual(self.rewrite("see [x](#design)"), "see [x](#containers--design)")

    def test_external_link_is_untouched(self):
        self.assertEqual(
            self.rewrite("see [x](https://example.com/a.md)"),
            "see [x](https://example.com/a.md)",
        )

    def test_sibling_link_resolves_within_the_same_chapter(self):
        self.assertEqual(
            build_book.rewrite_links(
                "see [x](01-concept-map.md)", "07-clouds/index.md", self.anchors
            ),
            "see [x](#concepts-across-the-clouds)",
        )

    def test_unknown_target_raises_rather_than_emitting_a_dead_link(self):
        with self.assertRaises(KeyError):
            self.rewrite("see [x](../99-nope/01-missing.md)")

    def test_chapter_image_path_is_rewritten_to_the_repository_root(self):
        self.assertEqual(
            build_book.rewrite_links(
                "![a](../../images/diagram.png)", "06-frontend/index.md", self.anchors
            ),
            "![a](images/diagram.png)",
        )

    def test_entry_page_image_path_is_rewritten_to_the_repository_root(self):
        self.assertEqual(
            build_book.rewrite_links(
                "![a](../images/cover-bg.png)", "welcome.md", self.anchors
            ),
            "![a](images/cover-bg.png)",
        )


class DocumentAnchors(unittest.TestCase):
    def test_two_documents_with_the_same_title_get_different_anchors(self):
        anchors = build_book.document_anchors(
            [("05-coding/index.md", "Glossary", ""), ("00-se/01-glossary.md", "Glossary", "")]
        )
        self.assertEqual(len(set(anchors.values())), 2)
        self.assertIn("glossary", anchors.values())


class ExtractMermaid(unittest.TestCase):
    def test_finds_a_block_and_returns_its_source(self):
        markdown = "# T\n\n```mermaid\nflowchart LR\n  A --> B\n```\n\nText.\n"
        self.assertEqual(
            build_book.extract_mermaid(markdown), ["flowchart LR\n  A --> B"]
        )

    def test_finds_every_block_in_document_order(self):
        markdown = "```mermaid\nfirst\n```\n\n```mermaid\nsecond\n```\n"
        self.assertEqual(build_book.extract_mermaid(markdown), ["first", "second"])

    def test_ignores_a_fence_of_another_language(self):
        self.assertEqual(build_book.extract_mermaid("```sh\nmermaid\n```\n"), [])

    def test_ignores_the_word_in_prose(self):
        self.assertEqual(build_book.extract_mermaid("a mermaid diagram\n"), [])


class RasterHash(unittest.TestCase):
    """The file name is the hash of the source, so an unchanged source is never
    re-rendered and a changed one cannot collide with its own earlier version."""

    def test_is_stable_for_the_same_source(self):
        self.assertEqual(
            build_book.raster_hash("flowchart LR\n  A --> B"),
            build_book.raster_hash("flowchart LR\n  A --> B"),
        )

    def test_differs_for_a_different_source(self):
        self.assertNotEqual(
            build_book.raster_hash("flowchart LR\n  A --> B"),
            build_book.raster_hash("flowchart LR\n  A --> C"),
        )

    def test_ignores_trailing_whitespace(self):
        """Re-indenting the closing lines should not invalidate a cached render."""
        self.assertEqual(
            build_book.raster_hash("flowchart LR  \n  A --> B\n\n"),
            build_book.raster_hash("flowchart LR\n  A --> B"),
        )


class ReplaceMermaid(unittest.TestCase):
    def test_a_block_becomes_an_image_with_no_alt_text(self):
        """Empty alt text keeps pandoc from floating this as a captioned figure."""
        markdown = "# T\n\n```mermaid\nflowchart LR\n```\n\nText.\n"
        self.assertEqual(
            build_book.replace_mermaid(markdown, ["build/diagrams/ab12.png"]),
            "# T\n\n![](build/diagrams/ab12.png)\n\nText.\n",
        )

    def test_each_block_takes_its_own_image(self):
        markdown = "```mermaid\nfirst\n```\n\n```mermaid\nsecond\n```\n"
        self.assertEqual(
            build_book.replace_mermaid(markdown, ["a.png", "b.png"]),
            "![](a.png)\n\n![](b.png)\n",
        )

    def test_a_block_with_no_image_keeps_its_source(self):
        """A diagram that did not render stays a code block: that is today's output
        for it, so a renderer failure never regresses the book."""
        markdown = "```mermaid\nfirst\n```\n\n```mermaid\nsecond\n```\n"
        self.assertEqual(
            build_book.replace_mermaid(markdown, [None, "b.png"]),
            "```mermaid\nfirst\n```\n\n![](b.png)\n",
        )

    def test_rejects_a_count_that_does_not_match(self):
        with self.assertRaises(ValueError):
            build_book.replace_mermaid("```mermaid\nx\n```\n", [])


class SvgSize(unittest.TestCase):
    """Chrome's window is the viewport it screenshots, so a wrong size crops the
    cover or pads it with blank paper."""

    def test_reads_the_declared_pixel_size(self):
        self.assertEqual(
            build_book.svg_size('<svg width="1200" height="300"/>'), (1200, 300)
        )

    def test_ignores_a_px_suffix(self):
        self.assertEqual(
            build_book.svg_size('<svg width="1200px" height="300px"/>'), (1200, 300)
        )

    def test_falls_back_to_the_viewbox(self):
        self.assertEqual(
            build_book.svg_size('<svg viewBox="0 0 800 250"/>'), (800, 250)
        )

    def test_prefers_the_viewbox_over_a_relative_size(self):
        """Markup sized in percent has no intrinsic pixel size; its viewBox does."""
        markup = '<svg width="100%" height="100%" viewBox="0 0 640 480"/>'
        self.assertEqual(build_book.svg_size(markup), (640, 480))

    def test_rejects_markup_that_declares_no_size(self):
        with self.assertRaises(ValueError):
            build_book.svg_size("<svg/>")


class CoverFields(unittest.TestCase):
    def test_reads_the_three_fields_the_cover_prints(self):
        metadata = (
            "title: A Book\n"
            "subtitle: And its subtitle\n"
            "author: Someone\n"
            "language: en-GB\n"
        )
        self.assertEqual(
            build_book.cover_fields(metadata), ("A Book", "And its subtitle", "Someone")
        )

    def test_strips_quotes_a_yaml_value_may_carry(self):
        self.assertEqual(build_book.cover_fields('title: "A Book"\n')[0], "A Book")

    def test_ignores_the_folded_description_and_the_subject_list(self):
        metadata = (
            "title: A Book\n"
            "description: >-\n"
            "  A long line that mentions author: not really\n"
            "subject:\n"
            "  - Software engineering\n"
        )
        self.assertEqual(build_book.cover_fields(metadata), ("A Book", "", ""))

    def test_a_missing_field_is_empty_rather_than_an_error(self):
        self.assertEqual(build_book.cover_fields("language: en-GB\n"), ("", "", ""))


class PngSize(unittest.TestCase):
    def png(self, width, height):
        path = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory())) / "x.png"
        path.write_bytes(
            b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\rIHDR"
            + width.to_bytes(4, "big") + height.to_bytes(4, "big")
        )
        return path

    def test_reads_the_dimensions_from_the_ihdr_header(self):
        self.assertEqual(build_book.png_size(self.png(752, 478)), (752, 478))

    def test_refuses_a_file_that_is_not_a_png(self):
        path = self.png(1, 1)
        path.write_bytes(b"not a png at all, but long enough to slice")
        with self.assertRaises(ValueError):
            build_book.png_size(path)


class CoverSvg(unittest.TestCase):
    """The cover is generated from the metadata, so what it prints is tested here
    rather than eyeballed on the rendered JPEG."""

    def cover(self, title="A Book", subtitle="A subtitle", author="Someone",
              photo="data:image/png;base64,AAAA", aspect=752 / 478):
        return build_book.cover_svg(title, subtitle, author, photo, aspect)

    def test_is_an_a4_sized_svg_chrome_can_size(self):
        self.assertEqual(
            build_book.svg_size(self.cover()),
            (build_book.COVER_WIDTH, build_book.COVER_HEIGHT),
        )

    def test_carries_the_photograph_inline(self):
        self.assertIn("data:image/png;base64,AAAA", self.cover())

    def test_the_photograph_sits_flush_with_the_bottom_edge(self):
        root = ElementTree.fromstring(self.cover())
        image = root.find("{http://www.w3.org/2000/svg}image")
        bottom = float(image.get("y")) + float(image.get("height"))
        self.assertEqual(bottom, build_book.COVER_HEIGHT)

    def test_the_photograph_keeps_its_own_aspect_ratio(self):
        root = ElementTree.fromstring(self.cover(aspect=2.0))
        image = root.find("{http://www.w3.org/2000/svg}image")
        self.assertEqual(float(image.get("height")), build_book.COVER_WIDTH / 2)

    def test_the_top_of_the_photograph_fades_into_the_page(self):
        root = ElementTree.fromstring(self.cover())
        stops = root.iter("{http://www.w3.org/2000/svg}stop")
        self.assertEqual(
            [stop.get("stop-opacity") for stop in stops], ["0", "1"]
        )

    def test_wraps_a_long_title_onto_several_lines(self):
        """A made-up title, not the book's own: retitling the book in
        book/metadata.yaml must not break a test of the wrapping."""
        root = ElementTree.fromstring(self.cover(title="A Rather Long Book Title"))
        titles = [
            element.text for element in root.iter("{http://www.w3.org/2000/svg}text")
            if element.get("class") == "title"
        ]
        self.assertEqual(titles, ["A Rather Long", "Book Title"])

    def test_escapes_metadata_that_would_otherwise_break_the_markup(self):
        markup = self.cover(title="Tools & <Practices>")
        self.assertIn("Tools &amp; &lt;Practices&gt;", markup)
        ElementTree.fromstring(markup)  # still well-formed


class StartOnANewPage(unittest.TestCase):
    """Each document opens on a fresh page: a raw LaTeX break for the PDF, a class on
    the opening heading for the EPUB's stylesheet to hang a break on."""

    def test_puts_a_latex_page_break_before_the_document(self):
        marked = build_book.start_on_a_new_page("## Title {#t}\n\nBody.\n")
        self.assertTrue(marked.startswith("```{=latex}\n\\clearpage\n```\n\n"))

    def test_marks_the_opening_heading_and_nothing_below_it(self):
        marked = build_book.start_on_a_new_page(
            "## Title {#t}\n\nBody.\n\n### Section {#t--section}\n"
        )
        self.assertIn("## Title {#t .document}\n", marked)
        self.assertIn("### Section {#t--section}\n", marked)

    def test_leaves_the_body_alone(self):
        marked = build_book.start_on_a_new_page("## Title {#t}\n\nBody.\n")
        self.assertTrue(marked.endswith("\n\nBody.\n"))

    def test_a_classed_heading_still_reports_its_id_alone(self):
        """The id regexes stop at the first space, or the class would become part of
        the anchor and every check that compares anchors would fail."""
        self.assertEqual(
            build_book.duplicate_anchors("## A {#t .document}\n\n## B {#t}\n"), ["t"]
        )


class DocumentOrder(unittest.TestCase):
    def test_welcome_comes_first_then_chapters_with_index_ahead_of_siblings(self):
        paths = [
            "07-clouds/01-concept-map.md",
            "welcome.md",
            "07-clouds/index.md",
            "00-software-engineering/index.md",
            "07-clouds/02-service-names.md",
        ]
        self.assertEqual(
            build_book.in_reading_order(paths),
            [
                "welcome.md",
                "00-software-engineering/index.md",
                "07-clouds/index.md",
                "07-clouds/01-concept-map.md",
                "07-clouds/02-service-names.md",
            ],
        )


if __name__ == "__main__":
    unittest.main()
