from unittest import TestCase

from packit.agent import Agent
from packit.loops import loop_converse
from tests.mocks import MockLLM


class TestLoopConverse(TestCase):
    def test_loop_ends(self):
        llm = MockLLM(["response 1", "response 2"])
        agents = [Agent("test", "Test agent", {}, llm) for _ in range(2)]
        prompt = "Prompt"

        result = loop_converse(agents, prompt)
        self.assertEqual(result, "response 1")
