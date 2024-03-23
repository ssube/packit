from unittest import TestCase

from packit.agent import Agent
from tests.mocks import MockLLM


class TestAgent(TestCase):
    def test_invoke(self):
        llm = MockLLM(["prompt"])
        agent = Agent("name", "backstory", {"context": "context"}, llm)
        result = agent.invoke("prompt", {"context": "context"})
        self.assertEqual(result, "prompt")

    def test_invoke_retry(self):
        llm = MockLLM(["<skip>", "prompt"])
        agent = Agent("name", "backstory", {"context": "context"}, llm)
        result = agent.invoke_retry(["prompt"], prompt_templates={"skip": ["<skip>"]})
        self.assertEqual(result.content, "prompt")
        self.assertTrue(result.response_metadata["done"])
        self.assertEqual(llm.index, 0)

    def test_format_context(self):
        llm = MockLLM(["prompt"])
        agent = Agent(
            "name", "backstory {agent_context}", {"agent_context": "agent_context"}, llm
        )
        _ = agent.invoke(
            "prompt {prompt_context}", {"prompt_context": "prompt_context"}
        )
        self.assertEqual(llm.messages[0].content, "backstory agent_context")
        self.assertEqual(llm.messages[1].content, "prompt prompt_context")
