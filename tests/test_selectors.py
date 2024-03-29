from unittest import TestCase

from packit.selectors import select_loop, select_random


class TestSelectLoop(TestCase):
    def test_select_loop(self):
        data = [1, 2, 3]

        for i in range(10):
            result = select_loop(data, i)
            self.assertIn(result, data)


class TestSelectRandom(TestCase):
    def test_select_random(self):
        data = [1, 2, 3]

        for i in range(10):
            result = select_random(data, i)
            self.assertIn(result, data)
