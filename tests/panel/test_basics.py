from unittest import TestCase

from packit.agent import Agent
from packit.panel import Panel
from tests.mocks import MockLLM


class TestPanelBasics(TestCase):
    def test_panel_weights(self):
        llm = MockLLM(["test"])
        agents = [Agent(f"test-{i}", "Test agent", {}, llm) for i in range(4)]
        weights = list(range(4))
        panel = Panel(agents, weights=weights)

        results = panel.sample("prompt", {})
        result_agents = list(results.keys())

        self.assertEqual(
            result_agents,
            [
                "test-1-0",
                "test-2-0",
                "test-2-1",
                "test-3-0",
                "test-3-1",
                "test-3-2",
            ],
        )

    def test_panel_threshold(self):
        llm = MockLLM(["yes", "no"])
        agents = [Agent(f"test-{i}", "Test agent", {}, llm) for i in range(4)]
        panel = Panel(agents)

        decision, _results = panel("prompt")
        self.assertEqual(decision, False)
