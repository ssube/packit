from unittest import TestCase

from packit.agent import Agent
from packit.loops import loop_tool
from packit.results import multi_function_or_str_result
from packit.toolbox import Toolbox
from tests.mocks import MockLLM


class TestLoopTool(TestCase):
    def test_immediate_success(self):
        def test_tool():
            return "done"

        llm = MockLLM(['{"function": "test_tool"}', "done"])
        agent = Agent("test", "Test agent", {}, llm)

        toolbox = Toolbox([test_tool])
        result = loop_tool(
            agent, "test", result_parser=multi_function_or_str_result, toolbox=toolbox
        )
        self.assertEqual(result, "done")

    def test_nested_success(self):
        counter = 0

        def test_tool():
            nonlocal counter
            if counter > 0:
                return "output"
            else:
                counter += 1
                return '{"function": "test_tool"}'

        llm = MockLLM(
            ['{"function": "test_tool"}', '{"function": "test_tool"}', "done"]
        )
        agent = Agent("test", "Test agent", {}, llm)

        toolbox = Toolbox([test_tool])
        result = loop_tool(
            agent, "test", result_parser=multi_function_or_str_result, toolbox=toolbox
        )
        self.assertEqual(result, "output")
