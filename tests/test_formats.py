from unittest import TestCase

from packit.formats import (
    format_bullet_list,
    format_number_list,
    format_str_or_json,
    join_lines,
    join_list,
    join_paragraphs,
    join_sentences,
)


class TestFormatStrOrJson(TestCase):
    def test_format_str_or_json(self):
        self.assertEqual(format_str_or_json("string"), "string")
        self.assertEqual(format_str_or_json({"key": "value"}), '{"key": "value"}')


class TestFormatBulletList(TestCase):
    def test_format_bullet_list(self):
        self.assertEqual(format_bullet_list(["item1", "item2"]), "- item1\n- item2")


class TestFormatNumberList(TestCase):
    def test_format_number_list(self):
        self.assertEqual(format_number_list([1, 2]), "1. 1\n2. 2")

    def test_format_number_list_start(self):
        self.assertEqual(format_number_list([1, 2], start=0), "0. 1\n1. 2")
        self.assertEqual(format_number_list([1, 2], start=2), "2. 1\n3. 2")


class TestJoinLines(TestCase):
    def test_join_lines(self):
        self.assertEqual(join_lines(["line1", "line2"]), "line1\nline2")


class TestJoinList(TestCase):
    def test_join_list(self):
        self.assertEqual(join_list(["item1", "item2"]), "item1, item2")


class TestJoinParagraphs(TestCase):
    def test_join_paragraphs(self):
        self.assertEqual(
            join_paragraphs(["paragraph1", "paragraph2"]), "paragraph1\n\nparagraph2"
        )


class TestJoinSentences(TestCase):
    def test_join_sentences(self):
        self.assertEqual(
            join_sentences(["sentence1", "sentence2"]), "sentence1. sentence2."
        )
