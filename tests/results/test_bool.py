from unittest import TestCase

from packit.results import bool_result


class TestBoolResult(TestCase):
    def test_bool_true(self):
        self.assertTrue(bool_result("yes"))
        self.assertTrue(bool_result("yes."))
        self.assertTrue(bool_result("yes,"))
        self.assertTrue(bool_result("yes, and"))
        self.assertTrue(bool_result("yes and"))

    def test_bool_false(self):
        self.assertFalse(bool_result("no"))
        self.assertFalse(bool_result("no."))
        self.assertFalse(bool_result("no,"))
        self.assertFalse(bool_result("no, but"))
        self.assertFalse(bool_result("no but"))
