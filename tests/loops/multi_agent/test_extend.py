from unittest import TestCase

from packit.agent import Agent
from packit.loops.multi_agent import loop_extend
from tests.mocks import MockLLM


class TestLoopConverse(TestCase):
    def test_loop_ends(self):
        llm = MockLLM(["response 1", "response 2"])
        agents = [Agent("test", "Test agent", {}, llm) for _ in range(2)]
        prompt = "Prompt"

        result = loop_extend(agents, prompt, prompt_template=lambda x: x)
        self.assertEqual(result, "response 1")
