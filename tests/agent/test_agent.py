from unittest import TestCase

from packit.agent import Agent
from tests.mocks import MockLLM


class TestAgent(TestCase):
    def test_invoke(self):
        llm = MockLLM(["prompt"])
        agent = Agent("name", "backstory", {"context": "context"}, llm)
        result = agent.invoke("prompt", {"context": "context"})
        self.assertEqual(result, "prompt")
