from unittest import TestCase

from packit.filters import repeat_prompt_filter, repeat_tool_filter


class TestRepeatPromptFilter(TestCase):
    def test_same_prompt(self):
        filter_fn, clear_memory = repeat_prompt_filter("Error")
        self.assertIsNone(filter_fn("Hello"))
        self.assertEqual(filter_fn("Hello"), "Error")
        clear_memory()
        self.assertIsNone(filter_fn("Hello"))


class TestRepeatToolFilter(TestCase):
    def test_same_tool(self):
        filter_fn, clear_memory = repeat_tool_filter("Error")
        self.assertIsNone(filter_fn({"tool": "Hello"}))
        self.assertEqual(filter_fn({"tool": "Hello"}), "Error")
        clear_memory()
        self.assertIsNone(filter_fn({"tool": "Hello"}))
