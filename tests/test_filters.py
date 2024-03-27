from unittest import TestCase

from packit.filters import repeat_prompt_filter, repeat_tool_filter


class TestRepeatPromptFilter(TestCase):
    def test_same_prompt(self):
        filter_fn, clear_memory = repeat_prompt_filter("Error")
        self.assertEqual(filter_fn("Hello"), None)
        self.assertEqual(filter_fn("Hello"), "Error")
        clear_memory()
        self.assertEqual(filter_fn("Hello"), None)


class TestRepeatToolFilter(TestCase):
    def test_same_tool(self):
        filter_fn, clear_memory = repeat_tool_filter("Error")
        self.assertEqual(filter_fn({"tool": "Hello"}), None)
        self.assertEqual(filter_fn({"tool": "Hello"}), "Error")
        clear_memory()
        self.assertEqual(filter_fn({"tool": "Hello"}), None)
