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
        self.assertEqual(
            result, [f"test-{i}" for i in range(11)]
        )  # TODO: is this off by one?

    def test_map_loop_no_memory(self):
        llms = [MockLLM([f"test-{i}"]) for i in range(100)]
        agents = [Agent(f"test-{i}", "Test agent", {}, llms[i]) for i in range(100)]

        result = loop_map(agents, "test")
        self.assertEqual(result, [f"test-{i}" for i in range(11)])

    def test_map_loop_with_prompt_filter(self):
        llms = [MockLLM([f"test-{i}"]) for i in range(100)]
        agents = [Agent(f"test-{i}", "Test agent", {}, llms[i]) for i in range(100)]

        def prompt_filter(prompt):
            return prompt if prompt != "test-10" else None

        result = loop_map(agents, "test", prompt_filter=prompt_filter)
        self.assertEqual(result, [f"test-{i}" for i in range(11)])

    def test_map_loop_with_result_parser(self):
        llms = [MockLLM([f"test-{i}"]) for i in range(100)]
        agents = [Agent(f"test-{i}", "Test agent", {}, llms[i]) for i in range(100)]

        def result_parser(value, **kwargs):
            return value if value != "test-10" else None

        result = loop_map(agents, "test", result_parser=result_parser)
        self.assertEqual(
            result, [*(f"test-{i}" for i in range(10)), None]
        )  # TODO: why is there a None at the end?


class TestReduceLoop(TestCase):
    def test_reduce_loop(self):
        llms = [MockLLM([f"test-{i}"]) for i in range(100)]
        agents = [Agent(f"test-{i}", "Test agent", {}, llms[i]) for i in range(100)]

        result = loop_reduce(agents, "test")
        self.assertEqual(result, "test-10")
