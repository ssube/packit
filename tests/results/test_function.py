from unittest import TestCase
from unittest.mock import MagicMock

from packit.results import function_result, int_result


class TestFunctionResult(TestCase):
    def test_function_result(self):
        mock_tool = MagicMock()
        mock_tool.return_value = "123"

        tools = {"test": (mock_tool, int_result)}
        result = function_result(
            """
            {
                "function": "test",
                "parameters": {
                    "value": "123"
                }
            }
            """,
            tools,
        )

        self.assertEqual(result, 123)
        self.assertEqual(mock_tool.call_count, 1)
        self.assertEqual(mock_tool.call_args.kwargs, {"value": "123"})
