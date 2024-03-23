from collections import deque


def make_infinite_memory():
    return []


def make_limited_memory(limit=10):
    return deque(maxlen=limit)
