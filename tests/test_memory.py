from unittest import TestCase

from packit.memory import (
    make_infinite_memory,
    make_limited_memory,
    memory_order_depth,
    memory_order_width,
)


class TestInfiniteMemory(TestCase):
    def test_infinite_memory(self):
        memory = make_infinite_memory()
        self.assertEqual(len(memory), 0)


class TestLimitedMemory(TestCase):
    def test_limited_memory(self):
        memory = make_limited_memory(1)
        self.assertEqual(len(memory), 0)

        for i in range(10):
            memory.append(i)
            self.assertEqual(len(memory), 1)


class TestMemoryOrderDepth(TestCase):
    def test_memory_order_depth(self):
        memory = make_infinite_memory()
        memory_order_depth(memory, "1")
        memory_order_depth(memory, "2")
        memory_order_depth(memory, "3")
        self.assertEqual(memory, ["3", "2", "1"])


class TestMemoryOrderWidth(TestCase):
    def test_memory_order_width(self):
        memory = make_infinite_memory()
        memory_order_width(memory, "1")
        memory_order_width(memory, "2")
        memory_order_width(memory, "3")
        self.assertEqual(memory, ["1", "2", "3"])
