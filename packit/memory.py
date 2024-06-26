from collections import deque
from typing import MutableSequence

from packit.types import MemoryType


def make_infinite_memory():
    return []


def make_limited_memory(limit=10):
    return deque(maxlen=limit)


def memory_order_width(memory: MutableSequence[MemoryType], prompt: MemoryType):
    """
    Width-first memory order.
    """
    memory.append(prompt)


def memory_order_depth(memory: MutableSequence[MemoryType], prompt: MemoryType):
    """
    Depth-first memory order.
    """
    memory.insert(0, prompt)
