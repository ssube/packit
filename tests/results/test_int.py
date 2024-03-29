from unittest import TestCase

from packit.results import int_result


class TestIntResult(TestCase):
    def test_valid(self):
        self.assertEqual(int_result("1"), 1)
        self.assertEqual(int_result("1 "), 1)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            int_result("test")
        with self.assertRaises(ValueError):
            int_result("1.1")
