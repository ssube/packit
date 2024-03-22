from typing import Callable

Condition = Callable[[], bool]


def condition_counter(max: int, current: int) -> bool:
    """
    Stop when the current count is equal to the max count.
    """
    return current < max


def condition_counter_mean(max: int, *currents: int) -> bool:
    """
    Stop when the mean of the current counts is equal to the max count.
    """
    return sum(currents) / len(currents) < max


def condition_counter_sum(max_sum: int, *currents: int) -> bool:
    """
    Stop when the sum of the current counts is equal to the max sum.
    """
    return sum(currents) < max_sum


def condition_keyword(keyword: str, current: str) -> bool:
    """
    Stop when a keyword is found in the current prompt.
    """
    return keyword in current


def condition_length(max_length: int, current: str) -> bool:
    """
    Stop when the current prompt reaches a certain length.
    """
    return len(current) < max_length


def condition_timeout(max_time: int, current: int) -> bool:
    raise NotImplementedError("Timeout condition not implemented")


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


def condition_and(*conditions: Condition) -> Condition:
    """
    Stop when all conditions are met.
    """

    def _condition_and() -> bool:
        return all(condition() for condition in conditions)

    return _condition_and


def condition_or(*conditions: Condition) -> Condition:
    """
    Stop when any condition is met.
    """

    def _condition_or() -> bool:
        return any(condition() for condition in conditions)

    return _condition_or


def condition_not(condition: Condition) -> Condition:
    """
    Stop when the condition is not met.
    """

    def _condition_not() -> bool:
        return not condition()

    return _condition_not
