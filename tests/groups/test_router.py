from unittest import TestCase

from packit.agent import Agent
from packit.groups import group_router
from tests.mocks import MockLLM


class TestGroupRouter(TestCase):
    def test_route_valid(self):
        llm_a = MockLLM(["b"])
        llm_b = MockLLM(["end"])
        agent_a = Agent("test_a", "test_a", {}, llm_a)
        agent_b = Agent("test_b", "test_b", {}, llm_b)
        agent_c = Agent("test_c", "test_c", {}, llm_a)

        routes = {
            "a": agent_a,
            "b": agent_b,
            "c": agent_c,
        }

        result = group_router(agent_a, "test", routes)
        self.assertEqual(result, "end")

    def test_route_invalid(self):
        llm = MockLLM(["e"])
        agent_a = Agent("test_a", "test_a", {}, llm)
        agent_b = Agent("test_b", "test_b", {}, llm)
        agent_c = Agent("test_c", "test_c", {}, llm)

        routes = {
            "a": agent_a,
            "b": agent_b,
            "c": agent_c,
        }

        with self.assertRaises(ValueError):
            group_router(agent_a, "test", routes)
