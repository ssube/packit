from unittest import TestCase

from packit.tools import lowercase_tool, titlecase_tool, uppercase_tool


class TestLowercaseTool(TestCase):
    def test_lowercase_tool(self):
        self.assertEqual(lowercase_tool("Hello"), "hello")
        self.assertEqual(lowercase_tool("HELLO"), "hello")
        self.assertEqual(lowercase_tool("hElLo"), "hello")


class TestUppercaseTool(TestCase):
    def test_uppercase_tool(self):
        self.assertEqual(uppercase_tool("Hello"), "HELLO")
        self.assertEqual(uppercase_tool("HELLO"), "HELLO")
        self.assertEqual(uppercase_tool("hElLo"), "HELLO")


class TestTitlecaseTool(TestCase):
    def test_titlecase_tool(self):
        self.assertEqual(titlecase_tool("hello"), "Hello")
        self.assertEqual(titlecase_tool("HELLO"), "Hello")
        self.assertEqual(titlecase_tool("hElLo"), "Hello")
