from time import monotonic
from typing import Any, Callable

Condition = Callable[[int, int], bool]


def condition_keyword(keyword: str, current: str) -> bool:
    """
    Stop when a keyword is found in the current prompt.
    """
    return keyword in current


def condition_list_once(items: list[Any]) -> Callable[[int, int], bool]:
    """
    Stop when all items in the list have been iterated over once.
    """

    max_length = len(items)

    def _condition_list_once(_max_threshold: int, current: int) -> bool:
        return current >= max_length

    return _condition_list_once


def condition_length(max_length: int, current: str) -> bool:
    """
    Stop when the current prompt reaches a certain length.
    """
    return len(current) > max_length


def condition_timeout(max_time: int, _current: int, timer=monotonic) -> bool:
    """
    Stop when the time exceeds the max time.
    """
    return timer() > max_time


def condition_threshold(max_threshold: int, current: int) -> bool:
    """
    Stop when the current threshold is greater than the max threshold.
    """
    return current > max_threshold


def condition_threshold_sum(max_threshold: int, *currents: int) -> bool:
    """
    Stop when the sum of the current thresholds is greater than the max threshold.
    """
    return sum(currents) > max_threshold


def condition_threshold_mean(max_threshold: float, *currents: int) -> bool:
    """
    Stop when the mean of the current thresholds is greater than the max threshold.
    """
    return sum(currents) / len(currents) > max_threshold


def condition_and(*conditions: Condition) -> Condition:
    """
    Stop when all conditions are met.
    """

    def _condition_and(*args) -> bool:
        return all(condition(*args) for condition in conditions)

    return _condition_and


def condition_or(*conditions: Condition) -> Condition:
    """
    Stop when any condition is met.
    """

    def _condition_or(*args) -> bool:
        return any(condition(*args) for condition in conditions)

    return _condition_or


def condition_not(condition: Condition) -> Condition:
    """
    Stop when the condition is not met.
    """

    def _condition_not(*args) -> bool:
        return not condition(*args)

    return _condition_not
