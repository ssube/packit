from unittest import TestCase

from packit.toolbox import RestrictedToolbox, RuleState
from packit.tools import multiply_tool


class TestRestrictedToolboxGetDefinition(TestCase):
    def test_rule_allow_all(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                ({}, RuleState.ALLOW),
            ],
        )

        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__, agent="test"),
            toolbox.definitions[0],
        )

    def test_rule_allow_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__, agent="test"),
            toolbox.definitions[0],
        )

    def test_rule_deny_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        with self.assertRaises(ValueError):
            toolbox.get_definition(multiply_tool.__name__, agent="test")

    def test_rule_allow_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.ALLOW)
        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__, agent="test"),
            toolbox.definitions[0],
        )

    def test_rule_deny_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.DENY)
        with self.assertRaises(ValueError):
            toolbox.get_definition(multiply_tool.__name__, agent="test")

    def test_rule_skip_extra(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                        "extra": "extra",
                    },
                    RuleState.ALLOW,
                ),
            ],
            default_state=RuleState.DENY,
        )

        with self.assertRaises(ValueError):
            toolbox.get_definition(multiply_tool.__name__, agent="test")


class TestRestrictedToolboxGetTool(TestCase):
    def test_rule_allow_all(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                ({}, RuleState.ALLOW),
            ],
        )

        self.assertEqual(
            toolbox.get_tool(multiply_tool.__name__, agent="test"), multiply_tool
        )

    def test_rule_allow_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        self.assertEqual(
            toolbox.get_tool(multiply_tool.__name__, agent="test"), multiply_tool
        )

    def test_rule_deny_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        with self.assertRaises(ValueError):
            toolbox.get_tool(multiply_tool.__name__, agent="test")

    def test_rule_allow_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.ALLOW)
        self.assertEqual(
            toolbox.get_tool(multiply_tool.__name__, agent="test"), multiply_tool
        )

    def test_rule_deny_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.DENY)
        with self.assertRaises(ValueError):
            toolbox.get_tool(multiply_tool.__name__, agent="test")


class TestRestrictedToolboxListDefinitions(TestCase):
    def test_rule_allow_all(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                ({}, RuleState.ALLOW),
            ],
        )

        self.assertEqual(toolbox.list_definitions(agent="test"), toolbox.definitions)

    def test_rule_allow_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        self.assertEqual(toolbox.list_definitions(agent="test"), toolbox.definitions)

    def test_rule_deny_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        self.assertEqual(toolbox.list_definitions(agent="test"), [])

    def test_rule_allow_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.ALLOW)
        self.assertEqual(toolbox.list_definitions(agent="test"), toolbox.definitions)

    def test_rule_deny_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.DENY)
        self.assertEqual(toolbox.list_definitions(agent="test"), [])


class TestRestrictedToolboxListTools(TestCase):
    def test_rule_allow_all(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                ({}, RuleState.ALLOW),
            ],
        )

        self.assertEqual(toolbox.list_tools(agent="test"), [multiply_tool.__name__])

    def test_rule_allow_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        self.assertEqual(toolbox.list_tools(agent="test"), [multiply_tool.__name__])

    def test_rule_deny_named(self):
        toolbox = RestrictedToolbox(
            [multiply_tool],
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        self.assertEqual(toolbox.list_tools(agent="test"), [])

    def test_rule_allow_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.ALLOW)
        self.assertEqual(toolbox.list_tools(agent="test"), [multiply_tool.__name__])

    def test_rule_deny_default(self):
        toolbox = RestrictedToolbox([multiply_tool], [], default_state=RuleState.DENY)
        self.assertEqual(toolbox.list_tools(agent="test"), [])
