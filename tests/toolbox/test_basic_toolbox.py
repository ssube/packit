from unittest import TestCase

from packit.toolbox import Toolbox
from packit.tools import multiply_tool


class TestBasicToolboxGetDefinition(TestCase):
    def test_tool_exists(self):
        toolbox = Toolbox([multiply_tool])
        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__), toolbox.definitions[0]
        )

    def test_tool_does_not_exist(self):
        toolbox = Toolbox([])
        with self.assertRaises(KeyError):
            toolbox.get_definition("non_existent_tool")

    def test_list_definitions(self):
        toolbox = Toolbox([multiply_tool])
        self.assertEqual(toolbox.list_definitions(), toolbox.definitions)


class TestBasicToolboxGetTool(TestCase):
    def test_tool_exists(self):
        toolbox = Toolbox([multiply_tool])
        self.assertEqual(toolbox.get_tool(multiply_tool.__name__), multiply_tool)

    def test_tool_does_not_exist(self):
        toolbox = Toolbox([])
        with self.assertRaises(KeyError):
            toolbox.get_tool("non_existent_tool")

    def test_list_tools(self):
        toolbox = Toolbox([multiply_tool])
        self.assertEqual(toolbox.list_tools(), [multiply_tool.__name__])


class TestBasicToolboxListDefinitions(TestCase):
    def test_tool_exists(self):
        toolbox = Toolbox([multiply_tool])
        self.assertEqual(toolbox.list_definitions(), toolbox.definitions)

    def test_tool_does_not_exist(self):
        toolbox = Toolbox([])
        self.assertEqual(toolbox.list_definitions(), [])


class TestBasicToolboxListTools(TestCase):
    def test_tool_exists(self):
        toolbox = Toolbox([multiply_tool])
        self.assertEqual(toolbox.list_tools(), [multiply_tool.__name__])

    def test_tool_does_not_exist(self):
        toolbox = Toolbox([])
        self.assertEqual(toolbox.list_tools(), [])
