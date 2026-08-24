#!/usr/bin/env python3
"""Tests for scripts/check_links.py.

Run with:

    python3 -m unittest discover -s scripts -p 'test_*.py'

Standard library only — there is no pytest in this repo. Every fixture is
built inside a `tempfile.TemporaryDirectory`, so the suite never writes into
the working tree.
"""
import io
import os
import contextlib
import tempfile
import unittest

import check_links


class LinkCheckerTestCase(unittest.TestCase):
    """Builds a throwaway docs tree and runs the checker over it."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def write(self, relpath, text):
        path = os.path.join(self.root, relpath)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)
        return path

    def run_checker(self, *relpaths):
        """Return (exit_code, stdout) from a full `main()` run."""
        paths = [os.path.join(self.root, rel) for rel in relpaths]
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = check_links.main(paths)
        return code, buffer.getvalue()


class TestRelativePaths(LinkCheckerTestCase):
    def test_link_to_existing_sibling_passes(self):
        self.write("a.md", "# A\n\nSee [B](b.md).\n")
        self.write("b.md", "# B\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)
        self.assertEqual(out, "")

    def test_link_to_missing_file_fails_with_path_and_line(self):
        self.write("a.md", "# A\n\nintro\n\nSee [B](b.md).\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("a.md:5", out)
        self.assertIn("b.md", out)

    def test_link_resolves_relative_to_the_linking_file(self):
        self.write("nested/deep/a.md", "# A\n\n[Up](../b.md) and [Down](sub/c.md)\n")
        self.write("nested/b.md", "# B\n")
        self.write("nested/deep/sub/c.md", "# C\n")
        code, out = self.run_checker("nested/deep/a.md")
        self.assertEqual(code, 0, out)

    def test_parent_traversal_to_missing_file_fails(self):
        self.write("nested/a.md", "# A\n\n[Gone](../nowhere/x.md)\n")
        code, out = self.run_checker("nested/a.md")
        self.assertEqual(code, 1)
        self.assertIn("../nowhere/x.md", out)

    def test_link_to_a_non_markdown_file_is_checked_as_a_path(self):
        self.write("a.md", "# A\n\n[Script](../run.sh)\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("run.sh", out)

    def test_percent_encoded_target_is_decoded_before_resolving(self):
        self.write("a.md", "# A\n\n[Spaced](my%20file.md)\n")
        self.write("my file.md", "# My File\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_several_files_are_all_reported(self):
        self.write("a.md", "# A\n\n[X](x.md)\n")
        self.write("b.md", "# B\n\n[Y](y.md)\n")
        code, out = self.run_checker("a.md", "b.md")
        self.assertEqual(code, 1)
        self.assertIn("a.md:3", out)
        self.assertIn("b.md:3", out)


class TestWhatIsNotFlagged(LinkCheckerTestCase):
    def test_external_urls_are_ignored(self):
        self.write(
            "a.md",
            "# A\n\n[Spec](https://example.com/x.md) and [Old](http://example.com/y)\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_mailto_is_ignored(self):
        self.write("a.md", "# A\n\n[Mail](mailto:someone@example.com)\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_image_embeds_are_ignored(self):
        self.write("a.md", "# A\n\n![Alt](../../images/missing.svg)\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_reference_style_definitions_are_ignored(self):
        self.write(
            "a.md",
            "# A\n\nSee [the spec][spec].\n\n[spec]: https://example.com/spec\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_empty_target_is_ignored(self):
        self.write("a.md", "# A\n\nAn empty [target]() is not a path\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)


class TestAnchors(LinkCheckerTestCase):
    def test_bare_fragment_matching_a_local_heading_passes(self):
        self.write("a.md", "# A\n\n[Jump](#other-paradigms)\n\n## Other Paradigms\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_bare_fragment_with_no_matching_heading_fails(self):
        self.write("a.md", "# A\n\n[Jump](#other-paradigms)\n\n## Some Paradigms\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("a.md:3", out)
        self.assertIn("other-paradigms", out)

    def test_cross_file_anchor_that_exists_passes(self):
        self.write("a.md", "# A\n\n[Storage](b.md#browser-storage)\n")
        self.write("b.md", "# B\n\n## Browser Storage\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_renamed_heading_leaves_a_broken_anchor(self):
        """The defect this checker exists for: path fine, anchor dead."""
        self.write("a.md", "# A\n\n[Storage](b.md#browser-storage)\n")
        self.write("b.md", "# B\n\n## Client-Side Storage\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("a.md:3", out)
        self.assertIn("browser-storage", out)
        self.assertIn("b.md", out)

    def test_missing_target_file_reports_the_path_not_the_anchor(self):
        self.write("a.md", "# A\n\n[Storage](b.md#browser-storage)\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertEqual(out.count(" - "), 1, out)
        self.assertIn("b.md", out)

    def test_anchor_on_a_non_markdown_target_is_not_checked(self):
        self.write("a.md", "# A\n\n[Chart](diagram.svg#layer1)\n")
        self.write("diagram.svg", "<svg></svg>")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_h1_and_h3_headings_both_yield_anchors(self):
        self.write("a.md", "# Top Level\n\n[One](#top-level) [Three](#deep-dive-search)\n\n### Deep Dive: Search\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)


class TestAnchorGeneration(LinkCheckerTestCase):
    def slug(self, heading):
        return check_links.slugify(heading)

    def test_lowercases_and_hyphenates(self):
        self.assertEqual(self.slug("Browser Storage"), "browser-storage")

    def test_strips_punctuation_but_keeps_hyphens_and_underscores(self):
        self.assertEqual(self.slug("Pub/Sub vs. Streams"), "pubsub-vs-streams")
        self.assertEqual(self.slug("Multi-Page Applications (MPA)"), "multi-page-applications-mpa")
        self.assertEqual(self.slug("Test-Driven Development (TDD)"), "test-driven-development-tdd")
        self.assertEqual(self.slug("N+1 Queries"), "n1-queries")
        self.assertEqual(self.slug("snake_case_name"), "snake_case_name")

    def test_each_stripped_character_leaves_its_space_behind(self):
        self.assertEqual(self.slug("Violations & Smells"), "violations--smells")
        self.assertEqual(
            self.slug("GRASP — General Responsibility"),
            "grasp--general-responsibility",
        )

    def test_strips_inline_markdown_from_heading_text(self):
        self.assertEqual(self.slug("**Bold** Heading"), "bold-heading")
        self.assertEqual(self.slug("The `code` Heading"), "the-code-heading")
        self.assertEqual(self.slug("A [Linked](x.md) Heading"), "a-linked-heading")
        self.assertEqual(self.slug("*Italic* Heading"), "italic-heading")

    def test_duplicate_headings_get_numeric_suffixes_in_document_order(self):
        path = self.write(
            "a.md",
            "# A\n\n## Best Practices\n\ntext\n\n## Best Practices\n\ntext\n\n## Best Practices\n",
        )
        self.assertEqual(
            check_links.heading_anchors(path),
            ["a", "best-practices", "best-practices-1", "best-practices-2"],
        )

    def test_duplicate_suffix_anchors_resolve(self):
        self.write(
            "a.md",
            "# A\n\n[Second](#best-practices-1)\n\n## Best Practices\n\n## Best Practices\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)


class TestFencedCodeBlocks(LinkCheckerTestCase):
    def test_headings_inside_a_fence_are_not_anchors(self):
        self.write(
            "a.md",
            "# A\n\n[Sample](#heading)\n\n```markdown\n# Heading\n```\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("#heading", out)

    def test_links_inside_a_fence_are_not_checked(self):
        self.write(
            "a.md",
            "# A\n\n```markdown\nText with a [link](nowhere.md).\n```\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_comment_lines_inside_a_fence_are_not_headings(self):
        self.write(
            "a.md",
            "# A\n\n```dockerfile\n# Build Stage\nFROM node\n```\n\n[Bad](#build-stage)\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("build-stage", out)

    def test_tilde_fences_are_tracked(self):
        self.write(
            "a.md",
            "# A\n\n~~~markdown\n# Heading\n[link](nowhere.md)\n~~~\n\n[Sample](#heading)\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("#heading", out)
        self.assertNotIn("nowhere.md", out)

    def test_a_fence_only_closes_on_a_matching_marker(self):
        self.write(
            "a.md",
            "# A\n\n```\n~~~\n# Not A Heading\n```\n\n[Sample](#not-a-heading)\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("not-a-heading", out)

    def test_a_longer_closing_fence_still_closes_the_block(self):
        self.write(
            "a.md",
            "# A\n\n```\ncode\n````\n\n## Real Heading\n\n[Sample](#real-heading)\n",
        )
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 0, out)

    def test_fences_in_the_target_file_are_skipped_too(self):
        self.write("a.md", "# A\n\n[Sample](b.md#heading)\n")
        self.write("b.md", "# B\n\n```markdown\n# Heading\n```\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("heading", out)


class TestOutputShape(LinkCheckerTestCase):
    def test_clean_run_prints_nothing_and_exits_zero(self):
        self.write("a.md", "# A\n\n[B](b.md)\n")
        self.write("b.md", "# B\n")
        code, out = self.run_checker("a.md", "b.md")
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

    def test_failures_are_listed_one_per_line_with_path_and_line(self):
        self.write("a.md", "# A\n\n[X](x.md)\n[Y](y.md)\n")
        code, out = self.run_checker("a.md")
        self.assertEqual(code, 1)
        self.assertIn("Link check failed", out)
        lines = [line for line in out.splitlines() if line.strip().startswith("- ")]
        self.assertEqual(len(lines), 2, out)
        self.assertTrue(all(":" in line for line in lines))

    def test_no_paths_is_a_clean_run(self):
        code, out = self.run_checker()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
