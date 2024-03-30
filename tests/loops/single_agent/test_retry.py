from unittest import TestCase

from packit.agent import Agent
from packit.loops import loop_retry
from tests.mocks import MockLLM


class TestLoopRetry(TestCase):
    def test_immediate_success(self):
        def result_parser(value, **kwargs):
            return value

        llm = MockLLM(["test 1", "test 2", "test 3"])
        agent = Agent("test", "Test agent", {}, llm)

        result = loop_retry(agent, "test", result_parser=result_parser)
        self.assertEqual(result, "test 1")

    def test_eventual_success(self):
        counter = 0

        def result_parser(value, **kwargs):
            nonlocal counter

            if counter > 0:
                return value
            else:
                counter += 1
                raise ValueError("Test error")

        llm = MockLLM(["test 1", "test 2", "test 3"])
        agent = Agent("test", "Test agent", {}, llm)

        result = loop_retry(agent, "test", result_parser=result_parser)
        self.assertEqual(result, "test 2")

    def test_eventual_exhaustion(self):
        def result_parser(value, **kwargs):
            raise ValueError("Test error")

        llm = MockLLM(["test 1", "test 2", "test 3"])
        agent = Agent("test", "Test agent", {}, llm)

        with self.assertRaises(ValueError):
            loop_retry(agent, "test", result_parser=result_parser)

    def test_without_parser(self):
        llm = MockLLM(["test 1", "test 2", "test 3"])
        agent = Agent("test", "Test agent", {}, llm)

        result = loop_retry(agent, "test")
        self.assertEqual(result, "test 1")
