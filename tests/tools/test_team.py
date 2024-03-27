from unittest import TestCase

from packit.agent import Agent
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
        self.assertEqual(
            delegate("Larry", "Do some work"),
            "I'm sorry, that coworker does not exist.",
        )

    def test_question_valid_coworker(self):
        llm = MockLLM(["Alice", "Bob"])
        agents = [
            Agent("Alice", "Alice's prompt", {}, llm),
            Agent("Bob", "Bob's prompt", {}, llm),
        ]
        _delegate, question = make_team_tools(agents)
        self.assertEqual(question("Alice", "Do some work"), "Alice")
        self.assertEqual(
            question("Larry", "Do some work"),
            "I'm sorry, that coworker does not exist.",
        )
