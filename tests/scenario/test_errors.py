from unittest import TestCase
from unittest.mock import Mock

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

        mock_0 = Mock(agent_0)
        mock_0.name = agent_0.name
        mock_0.side_effect = agent_0
        mock_1 = Mock(agent_1)
        mock_1.name = agent_1.name
        mock_1.side_effect = agent_1

        def error_tool():
            raise ValueError("Error")

        delegate_tool, question_tool = make_team_tools([mock_0, mock_1])
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
