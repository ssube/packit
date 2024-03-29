from unittest import TestCase

from packit.results import str_result


class TestStrResult(TestCase):
    def test_valid(self):
        self.assertEqual(str_result("1"), "1")
        self.assertEqual(str_result("1 "), "1")
        self.assertEqual(str_result("test"), "test")
        self.assertEqual(str_result({}), "{}")
        self.assertEqual(str_result([]), "[]")
        self.assertEqual(str_result(None), "None")
