from unittest import TestCase

from packit.formats import format_bullet_list, format_number_list, format_str_or_json


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
