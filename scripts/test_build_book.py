"""Tests for the book builder's text transforms."""

import unittest

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


class Frontmatter(unittest.TestCase):
    def test_returns_the_title_and_the_body_without_the_block(self):
        source = "---\ntype: Guide\ntitle: CI/CD\ndescription: d\ntags: [a]\n---\n\n# CI/CD\n\nBody.\n"
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
                "![a](../../images/21-frontend.svg)", "06-frontend/index.md", self.anchors
            ),
            "![a](images/21-frontend.svg)",
        )

    def test_entry_page_image_path_is_rewritten_to_the_repository_root(self):
        self.assertEqual(
            build_book.rewrite_links(
                "![a](../images/welcome.svg)", "welcome.md", self.anchors
            ),
            "![a](images/welcome.svg)",
        )


class DocumentAnchors(unittest.TestCase):
    def test_two_documents_with_the_same_title_get_different_anchors(self):
        anchors = build_book.document_anchors(
            [("05-coding/index.md", "Glossary", ""), ("00-se/01-glossary.md", "Glossary", "")]
        )
        self.assertEqual(len(set(anchors.values())), 2)
        self.assertIn("glossary", anchors.values())


class StripImages(unittest.TestCase):
    """The PDF pass drops images: xelatex cannot embed SVG and this machine has
    no rasterizer, so the alternative is a build that fails."""

    def test_removes_an_image_line_and_keeps_the_prose(self):
        self.assertEqual(
            build_book.strip_images("# T\n\n![Banner](images/a.svg)\n\nText.\n"),
            "# T\n\nText.\n",
        )

    def test_keeps_an_ordinary_link(self):
        self.assertEqual(
            build_book.strip_images("see [x](#y)\n"), "see [x](#y)\n"
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
