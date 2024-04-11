from json import dumps
from unittest import TestCase

from packit.agent import Agent
from packit.errors import ToolError
from packit.results import function_result
from packit.toolbox import Toolbox
from tests.mocks import MockLLM


class TestFunctionResult(TestCase):
    def test_function_list(self):
        llm = MockLLM([])
        agent = Agent("test", "test", {}, llm)
        toolbox = Toolbox([])
        with self.assertRaises(ValueError):
            function_result(
                dumps(["test-1", "test-2", "test-3"]), agent=agent, toolbox=toolbox
            )

    def test_function_invalid(self):
        llm = MockLLM([])
        agent = Agent("test", "test", {}, llm)
        toolbox = Toolbox([])
        with self.assertRaises(ToolError):
            function_result(
                dumps({"function": "test", "parameters": {}}),
                agent=agent,
                toolbox=toolbox,
            )

    def test_function_missing(self):
        llm = MockLLM([])
        agent = Agent("test", "test", {}, llm)
        toolbox = Toolbox([])
        with self.assertRaises(ValueError):
            function_result(dumps({"parameters": {}}), agent=agent, toolbox=toolbox)

    def test_missing_toolbox(self):
        llm = MockLLM([])
        agent = Agent("test", "test", {}, llm)
        with self.assertRaises(ValueError):
            function_result(dumps({"function": "test", "parameters": {}}), agent=agent)

    def test_tool_filter(self):
        llm = MockLLM([])
        agent = Agent("test", "test", {}, llm)
        toolbox = Toolbox([])
        result = function_result(
            dumps({"function": "test", "parameters": {}}),
            agent=agent,
            toolbox=toolbox,
            tool_filter=lambda x: "nope",
        )
        self.assertEqual(result, "nope")
