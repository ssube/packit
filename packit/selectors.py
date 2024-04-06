from random import choice
from typing import List, TypeVar

SelectorType = TypeVar("SelectorType")


def select_leader(items: List[SelectorType], iteration: int) -> SelectorType:
    return items[0]


def select_loop(items: List[SelectorType], iteration: int) -> SelectorType:
    return items[iteration % len(items)]


def select_random(items: List[SelectorType], iteration: int) -> SelectorType:
    return choice(items)
