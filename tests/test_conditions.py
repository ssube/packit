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
        self.assertTrue(combined("test"))

    def test_condition_and_one(self):
        combined = condition_and(
            lambda x: True,
            lambda x: False,
        )
        self.assertFalse(combined("test"))

    def test_condition_and_neither(self):
        combined = condition_and(
            lambda x: False,
            lambda x: False,
        )
        self.assertFalse(combined("test"))


class TestConditionOr(TestCase):
    def test_condition_or_both(self):
        combined = condition_or(
            lambda x: True,
            lambda x: True,
        )
        self.assertTrue(combined("test"))

    def test_condition_or_one(self):
        combined = condition_or(
            lambda x: True,
            lambda x: False,
        )
        self.assertTrue(combined("test"))

    def test_condition_or_neither(self):
        combined = condition_or(
            lambda x: False,
            lambda x: False,
        )
        self.assertFalse(combined("test"))


class TestConditionKeyword(TestCase):
    def test_condition_keyword_absent(self):
        self.assertFalse(condition_keyword("test", "other"))

    def test_condition_keyword_present(self):
        self.assertTrue(condition_keyword("test", "test"))


class TestConditionNot(TestCase):
    def test_condition_not_true(self):
        self.assertFalse(condition_not(lambda x: True)("test"))

    def test_condition_not_false(self):
        self.assertTrue(condition_not(lambda x: False)("test"))


class TestConditionLength(TestCase):
    def test_condition_length_true(self):
        self.assertFalse(condition_length(4, "test"))

    def test_condition_length_false(self):
        self.assertTrue(condition_length(4, "other"))


class TestConditionListOnce(TestCase):
    def test_condition_list_once_true(self):
        self.assertTrue(condition_list_once([1, 2])(2, 2))

    def test_condition_list_once_false(self):
        self.assertFalse(condition_list_once([1, 2])(2, 1))


class TestConditionThreshold(TestCase):
    def test_condition_threshold_true(self):
        self.assertTrue(condition_threshold(4, 5))

    def test_condition_threshold_false(self):
        self.assertFalse(condition_threshold(4, 3))


class TestConditionThresholdMean(TestCase):
    def test_condition_threshold_mean_true(self):
        self.assertTrue(condition_threshold_mean(4, 5, 5))

    def test_condition_threshold_mean_false(self):
        self.assertFalse(condition_threshold_mean(4, 3, 3))


class TestConditionThresholdSum(TestCase):
    def test_condition_threshold_sum_true(self):
        self.assertTrue(condition_threshold_sum(4, 3, 2))

    def test_condition_threshold_sum_false(self):
        self.assertFalse(condition_threshold_sum(4, 3, 1))


class TestConditionTimeout(TestCase):
    def test_condition_timeout_true(self):
        self.assertTrue(condition_timeout(5, 5, timer=lambda: 10))

    def test_condition_timeout_false(self):
        self.assertFalse(condition_timeout(5, 5, timer=lambda: 1))
