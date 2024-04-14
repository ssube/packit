from unittest import TestCase

from packit.utils import could_be_json, hash_dict, logger_with_colors, monotonic_delta


class TestLoggerWithColors(TestCase):
    def test_logger_with_colors(self):
        self.assertTrue(logger_with_colors("test"))


class TestHashDict(TestCase):
    def test_hash_dict(self):
        self.assertTrue(hash_dict({"test": "test"}))


class TestMonotonicDelta(TestCase):
    def test_monotonic_delta(self):
        def timer():
            return 100

        delta, last = monotonic_delta(0, timer=timer)
        self.assertEqual(delta, 100)
        self.assertEqual(last, 100)


class TestCouldBeJSON(TestCase):
    def test_maybe_json(self):
        self.assertTrue(could_be_json('{"test": "test"}'))
        self.assertTrue(could_be_json('[{"test": "test"}]'))

    def test_definitely_not_json(self):
        self.assertFalse(could_be_json("test"))
        self.assertFalse(could_be_json(None))
