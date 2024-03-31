from unittest import TestCase

from packit.agent import Agent
from packit.errors import ToolError
from packit.tools import make_team_tools
from tests.mocks import MockLLM


class TestTeamTools(TestCase):
    def test_delegate_valid_coworker(self):
        llm = MockLLM(["Alice", "Bob"])
        agents = [
            Agent("Alice", "Alice's prompt", {}, llm),
            Agent("Bob", "Bob's prompt", {}, llm),
        ]
        delegate, _question = make_team_tools(agents)
        self.assertEqual(delegate("Alice", "Do some work"), "Alice")
        with self.assertRaises(ToolError):
            delegate("Larry", "Do some work")

    def test_question_valid_coworker(self):
        llm = MockLLM(["Alice", "Bob"])
        agents = [
            Agent("Alice", "Alice's prompt", {}, llm),
            Agent("Bob", "Bob's prompt", {}, llm),
        ]
        _delegate, question = make_team_tools(agents)
        self.assertEqual(question("Alice", "Do some work"), "Alice")
        with self.assertRaises(ToolError):
            question("Larry", "Do some work")
