from unittest import TestCase

from packit.agent import Agent
from packit.loops import loop_map, loop_reduce
from packit.memory import make_limited_memory, memory_order_width
from tests.mocks import MockLLM


class TestMapLoop(TestCase):
    def test_map_loop(self):
        llms = [MockLLM([f"test-{i}"]) for i in range(100)]
        agents = [Agent(f"test-{i}", "Test agent", {}, llms[i]) for i in range(100)]

        result = loop_map(
            agents,
            "test",
            memory_factory=make_limited_memory,
            memory_maker=memory_order_width,
        )
        self.assertEqual(result, [f"test-{i}" for i in range(1, 11)])


class TestReduceLoop(TestCase):
    def test_reduce_loop(self):
        llms = [MockLLM([f"test-{i}"]) for i in range(100)]
        agents = [Agent(f"test-{i}", "Test agent", {}, llms[i]) for i in range(100)]

        result = loop_reduce(agents, "test")
        self.assertEqual(result, "test-10")
