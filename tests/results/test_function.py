from json import dumps
from unittest import TestCase

from packit.agent import Agent
from packit.errors import ToolError
from packit.results import function_result, normalize_function_json
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

    def test_missing_agent(self):
        toolbox = Toolbox([])
        with self.assertRaises(ValueError):
            function_result(
                dumps({"function": "test", "parameters": {}}), toolbox=toolbox
            )

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

    def test_function_name_type(self):
        llm = MockLLM([])
        agent = Agent("test", "test", {}, llm)
        toolbox = Toolbox([])
        with self.assertRaises(ValueError):
            function_result(
                dumps({"function": 1, "parameters": {}}), agent=agent, toolbox=toolbox
            )


class TestNormalizeFunctionJson(TestCase):
    def test_normalize_valid(self):
        input = {"function": "test", "parameters": {}}
        result = normalize_function_json(input)
        self.assertEqual(result, input)

    def test_normalize_invalid(self):
        for input in [
            {"parameters": {}},
        ]:
            self.assertEqual(normalize_function_json(input), input)

    def test_normalize_nested_function(self):
        result = normalize_function_json(
            {"function": {"name": "test", "parameters": {}}}
        )
        self.assertEqual(result, {"function": "test", "parameters": {}})

    def test_normalize_nested_function_missing_parameters(self):
        result = normalize_function_json({"function": {"name": "test"}})
        self.assertEqual(result, {"function": "test", "parameters": {}})
