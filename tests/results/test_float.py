from unittest import TestCase

from packit.results import float_result


class TestFloatResult(TestCase):
    def test_valid(self):
        self.assertEqual(float_result("1.5"), 1.5)
        self.assertEqual(float_result("-2.5 "), -2.5)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            float_result("test")
        with self.assertRaises(ValueError):
            float_result("true")
