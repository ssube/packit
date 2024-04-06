from json import dumps
from unittest import TestCase

from packit.errors import ToolError
from packit.results import function_result
from packit.toolbox import Toolbox


class TestFunctionResult(TestCase):
    def test_function_list(self):
        with self.assertRaises(ValueError):
            function_result(dumps(["test-1", "test-2", "test-3"]))

    def test_function_invalid(self):
        toolbox = Toolbox([])
        with self.assertRaises(ToolError):
            function_result(
                dumps({"function": "test", "parameters": {}}), toolbox=toolbox
            )

    def test_function_missing(self):
        toolbox = Toolbox([])
        with self.assertRaises(ValueError):
            function_result(dumps({"parameters": {}}), toolbox=toolbox)