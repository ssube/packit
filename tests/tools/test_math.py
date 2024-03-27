from unittest import TestCase

from packit.tools import multiply_tool, sum_tool


class TestMultiplyTool(TestCase):
    def test_multiply_tool(self):
        self.assertEqual(multiply_tool(2, 3), 6)
        self.assertEqual(multiply_tool(5, 5), 25)
        self.assertEqual(multiply_tool(10, 10), 100)


class TestSumTool(TestCase):
    def test_sum_tool(self):
        self.assertEqual(sum_tool(2, 3), 5)
        self.assertEqual(sum_tool(2, 3, 5), 10)
        self.assertEqual(sum_tool(2, 3, 5, 10, 50), 70)
