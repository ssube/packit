from collections import deque
from typing import List


def make_infinite_memory():
    return []


def make_limited_memory(limit=10):
    return deque(maxlen=limit)


def memory_order_width(memory: List[str], prompt: str):
    """
    Width-first memory order.
    """
    memory.append(prompt)


def memory_order_depth(memory: List[str], prompt: str):
    """
    Depth-first memory order.
    """
    memory.insert(0, prompt)
