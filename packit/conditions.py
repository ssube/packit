from time import monotonic
from typing import Any, Callable, Tuple

from packit.types import StopCondition

DEFAULT_MAX = 10


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

    def _condition_list_once(max: int, current: int) -> bool:
        return current >= max_length

    return _condition_list_once


def condition_length(max: int = DEFAULT_MAX, current: str = "") -> bool:
    """
    Stop when the current prompt reaches a certain length.
    """
    return len(current) > max


def condition_timeout(
    max: int = DEFAULT_MAX, current: int = 0, timer=monotonic
) -> bool:
    """
    Stop when the time exceeds the max time.
    """
    return timer() > max


def condition_threshold(max: int = DEFAULT_MAX, current: int = 0) -> bool:
    """
    Stop when the current threshold is greater than the max threshold.
    """
    return current > max


def condition_threshold_sum(max: int = DEFAULT_MAX, *currents: int) -> bool:
    """
    Stop when the sum of the current thresholds is greater than the max threshold.
    """
    return sum(currents) > max


def condition_threshold_mean(max: float = DEFAULT_MAX, *currents: int) -> bool:
    """
    Stop when the mean of the current thresholds is greater than the max threshold.
    """
    return sum(currents) / len(currents) > max


def condition_and(*conditions: StopCondition) -> StopCondition:
    """
    Stop when all conditions are met.
    """

    def _condition_and(*args, **kwargs) -> bool:
        return all(condition(*args, **kwargs) for condition in conditions)

    return _condition_and


def condition_or(*conditions: StopCondition) -> StopCondition:
    """
    Stop when any condition is met.
    """

    def _condition_or(*args, **kwargs) -> bool:
        return any(condition(*args, **kwargs) for condition in conditions)

    return _condition_or


def condition_not(condition: StopCondition) -> StopCondition:
    """
    Stop when the condition is not met.
    """

    def _condition_not(*args, **kwargs) -> bool:
        return not condition(*args, **kwargs)

    return _condition_not


def make_flag_condition() -> Tuple[Callable[[bool], bool], StopCondition]:
    """
    Make a flag condition that stops when the flag is set.
    """

    flag = False

    def _condition_flag(*args, **kwargs) -> bool:
        return flag

    def _set_flag() -> None:
        nonlocal flag
        flag = True

    return _set_flag, _condition_flag
