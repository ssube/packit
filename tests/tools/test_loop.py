from unittest import TestCase

from packit.tools.loop import make_complete_tool


class TestMakeCompleteTool(TestCase):
    def test_make_complete_tool(self):
        complete_tool, complete_condition, reset_complete = make_complete_tool()
        self.assertFalse(complete_condition())
        complete_tool("test")
        self.assertTrue(complete_condition())
        reset_complete()
        self.assertFalse(complete_condition())
