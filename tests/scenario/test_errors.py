from unittest import TestCase

from packit.agent import Agent
from packit.conditions import condition_not
from packit.loops import loop_tool
from packit.results import multi_function_or_str_result, recursive_result
from packit.toolbox import Toolbox
from packit.tools import make_team_tools
from packit.utils import could_be_json
from tests.mocks import MockLLM


class TestToolError(TestCase):
    def test_agent_error(self):
        agent_0 = Agent(
            "agent-0",
            "prompt",
            {},
            MockLLM(
                [
                    '{"function": "delegate_tool", "parameters": {"coworker": "agent-1", "task": "prompt"}}'
                ]
            ),
        )
        agent_1 = Agent(
            "agent-1",
            "prompt",
            {},
            MockLLM(
                [
                    '{"function": "error_tool", "parameters": {}}',
                    "I'm sorry, here is a fixed response.",
                ]
            ),
        )

        def error_tool():
            raise ValueError("Error")

        delegate_tool, question_tool = make_team_tools([agent_0, agent_1])
        toolbox = Toolbox([delegate_tool, question_tool, error_tool])
        agent_0.toolbox = toolbox
        agent_1.toolbox = toolbox

        recursive_result_parser = recursive_result(
            multi_function_or_str_result, condition_not(could_be_json)
        )
        result = loop_tool(
            agent_0,
            "prompt",
            result_parser=recursive_result_parser,
            toolbox=toolbox,
        )

        self.assertEqual(result, "I'm sorry, here is a fixed response.")


if __name__ == "__main__":
    test = TestToolError()
    test.test_agent_error()
