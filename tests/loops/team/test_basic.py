from unittest import TestCase

from packit.agent import Agent
from packit.loops import loop_team
from tests.mocks import MockLLM


class TestTeamLoop(TestCase):
    def test_team_loop(self):
        llm = MockLLM(["test"])
        leader = Agent(
            name="leader",
            backstory="",
            context={},
            llm=llm,
        )
        agents = [
            Agent(
                name="agent1",
                backstory="",
                context={},
                llm=llm,
            ),
            Agent(
                name="agent2",
                backstory="",
                context={},
                llm=llm,
            ),
        ]
        result = loop_team(leader, agents, "start", "loop")
        self.assertEqual(result, "test")
