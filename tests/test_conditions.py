from unittest import TestCase

from packit.conditions import (
    condition_and,
    condition_keyword,
    condition_length,
    condition_list_once,
    condition_not,
    condition_or,
    condition_threshold,
    condition_threshold_mean,
    condition_threshold_sum,
    condition_timeout,
)


class TestConditionAnd(TestCase):
    def test_condition_and_both(self):
        combined = condition_and(
            lambda x: True,
            lambda x: True,
        )
        self.assertEqual(combined("test"), True)

    def test_condition_and_one(self):
        combined = condition_and(
            lambda x: True,
            lambda x: False,
        )
        self.assertEqual(combined("test"), False)

    def test_condition_and_neither(self):
        combined = condition_and(
            lambda x: False,
            lambda x: False,
        )
        self.assertEqual(combined("test"), False)


class TestConditionOr(TestCase):
    def test_condition_or_both(self):
        combined = condition_or(
            lambda x: True,
            lambda x: True,
        )
        self.assertEqual(combined("test"), True)

    def test_condition_or_one(self):
        combined = condition_or(
            lambda x: True,
            lambda x: False,
        )
        self.assertEqual(combined("test"), True)

    def test_condition_or_neither(self):
        combined = condition_or(
            lambda x: False,
            lambda x: False,
        )
        self.assertEqual(combined("test"), False)


class TestConditionKeyword(TestCase):
    def test_condition_keyword_absent(self):
        self.assertEqual(condition_keyword("test", "other"), False)

    def test_condition_keyword_present(self):
        self.assertEqual(condition_keyword("test", "test"), True)


class TestConditionNot(TestCase):
    def test_condition_not_true(self):
        self.assertEqual(condition_not(lambda x: True)("test"), False)

    def test_condition_not_false(self):
        self.assertEqual(condition_not(lambda x: False)("test"), True)


class TestConditionLength(TestCase):
    def test_condition_length_true(self):
        self.assertEqual(condition_length(4, "test"), False)

    def test_condition_length_false(self):
        self.assertEqual(condition_length(4, "other"), True)


class TestConditionListOnce(TestCase):
    def test_condition_list_once_true(self):
        self.assertEqual(condition_list_once([1, 2])(2, 2), True)

    def test_condition_list_once_false(self):
        self.assertEqual(condition_list_once([1, 2])(2, 1), False)


class TestConditionThreshold(TestCase):
    def test_condition_threshold_true(self):
        self.assertEqual(condition_threshold(4, 5), True)

    def test_condition_threshold_false(self):
        self.assertEqual(condition_threshold(4, 3), False)


class TestConditionThresholdMean(TestCase):
    def test_condition_threshold_mean_true(self):
        self.assertEqual(condition_threshold_mean(4, 5, 5), True)

    def test_condition_threshold_mean_false(self):
        self.assertEqual(condition_threshold_mean(4, 3, 3), False)


class TestConditionThresholdSum(TestCase):
    def test_condition_threshold_sum_true(self):
        self.assertEqual(condition_threshold_sum(4, 3, 2), True)

    def test_condition_threshold_sum_false(self):
        self.assertEqual(condition_threshold_sum(4, 3, 1), False)


class TestConditionTimeout(TestCase):
    def test_condition_timeout_true(self):
        self.assertEqual(condition_timeout(5, 5, timer=lambda: 10), True)

    def test_condition_timeout_false(self):
        self.assertEqual(condition_timeout(5, 5, timer=lambda: 1), False)
