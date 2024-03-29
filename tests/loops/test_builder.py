from unittest import TestCase

from packit.agent import Agent
from packit.loops import loop_midfix, loop_prefix, loop_suffix
from tests.mocks import MockLLM


class TestPrefixLoop(TestCase):
    def test_prefix_loop(self):
        llm = MockLLM(["test"])
        agent = Agent("test", "Test agent", {}, llm)

        result = loop_prefix([agent], "test", "converse", prompt_filter=lambda x: x)
        self.assertEqual(result, "test")


class TestMidfixLoop(TestCase):
    def test_midfix_loop(self):
        llm = MockLLM(["test"])
        agent = Agent("test", "Test agent", {}, llm)

        result = loop_midfix(
            [agent], "test", "converse", "extend", prompt_filter=lambda x: x
        )
        self.assertEqual(result, "test")


class TestSuffixLoop(TestCase):
    def test_suffix_loop(self):
        llm = MockLLM(["test"])
        agent = Agent("test", "Test agent", {}, llm)

        result = loop_suffix([agent], "test", "converse", prompt_filter=lambda x: x)
        self.assertEqual(result, "test")
