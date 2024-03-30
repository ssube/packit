from unittest import TestCase

from packit.abac import SubsetABAC
from packit.toolbox import RestrictedToolbox, RuleState
from packit.tools import multiply_tool

TEST_ATTRIBUTES = {
    "agent": "test",
}


class TestRestrictedToolboxGetDefinition(TestCase):
    def test_rule_allow_all(self):
        abac = SubsetABAC(
            [
                ({}, RuleState.ALLOW),
            ],
        )

        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )

        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__, abac=TEST_ATTRIBUTES),
            toolbox.definitions[0],
        )

    def test_rule_allow_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__, abac=TEST_ATTRIBUTES),
            toolbox.definitions[0],
        )

    def test_rule_deny_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        with self.assertRaises(ValueError):
            toolbox.get_definition(multiply_tool.__name__, abac=TEST_ATTRIBUTES)

    def test_rule_allow_default(self):
        abac = SubsetABAC([], default_state=RuleState.ALLOW)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        self.assertEqual(
            toolbox.get_definition(multiply_tool.__name__, abac=TEST_ATTRIBUTES),
            toolbox.definitions[0],
        )

    def test_rule_deny_default(self):
        abac = SubsetABAC([], default_state=RuleState.DENY)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        with self.assertRaises(ValueError):
            toolbox.get_definition(multiply_tool.__name__, abac=TEST_ATTRIBUTES)

    def test_rule_skip_extra(self):
        abac = SubsetABAC(
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
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )

        with self.assertRaises(ValueError):
            toolbox.get_definition(multiply_tool.__name__, abac=TEST_ATTRIBUTES)


class TestRestrictedToolboxGetTool(TestCase):
    def test_rule_allow_all(self):
        abac = SubsetABAC(
            [
                ({}, RuleState.ALLOW),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )

        self.assertEqual(
            toolbox.get_tool(multiply_tool.__name__, abac=TEST_ATTRIBUTES),
            multiply_tool,
        )

    def test_rule_allow_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        self.assertEqual(
            toolbox.get_tool(multiply_tool.__name__, abac=TEST_ATTRIBUTES),
            multiply_tool,
        )

    def test_rule_deny_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        with self.assertRaises(ValueError):
            toolbox.get_tool(multiply_tool.__name__, abac=TEST_ATTRIBUTES)

    def test_rule_allow_default(self):
        abac = SubsetABAC([], default_state=RuleState.ALLOW)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        self.assertEqual(
            toolbox.get_tool(multiply_tool.__name__, abac=TEST_ATTRIBUTES),
            multiply_tool,
        )

    def test_rule_deny_default(self):
        abac = SubsetABAC([], default_state=RuleState.DENY)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        with self.assertRaises(ValueError):
            toolbox.get_tool(multiply_tool.__name__, abac=TEST_ATTRIBUTES)


class TestRestrictedToolboxListDefinitions(TestCase):
    def test_rule_allow_all(self):
        abac = SubsetABAC(
            [
                ({}, RuleState.ALLOW),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )

        self.assertEqual(
            toolbox.list_definitions(abac=TEST_ATTRIBUTES), toolbox.definitions
        )

    def test_rule_allow_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        self.assertEqual(
            toolbox.list_definitions(abac=TEST_ATTRIBUTES), toolbox.definitions
        )

    def test_rule_deny_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        self.assertEqual(toolbox.list_definitions(abac=TEST_ATTRIBUTES), [])

    def test_rule_allow_default(self):
        abac = SubsetABAC([], default_state=RuleState.ALLOW)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        self.assertEqual(
            toolbox.list_definitions(abac=TEST_ATTRIBUTES), toolbox.definitions
        )

    def test_rule_deny_default(self):
        abac = SubsetABAC([], default_state=RuleState.DENY)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        self.assertEqual(toolbox.list_definitions(abac=TEST_ATTRIBUTES), [])


class TestRestrictedToolboxListTools(TestCase):
    def test_rule_allow_all(self):
        abac = SubsetABAC(
            [
                ({}, RuleState.ALLOW),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )

        self.assertEqual(
            toolbox.list_tools(abac=TEST_ATTRIBUTES), [multiply_tool.__name__]
        )

    def test_rule_allow_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.ALLOW,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        self.assertEqual(
            toolbox.list_tools(abac=TEST_ATTRIBUTES), [multiply_tool.__name__]
        )

    def test_rule_deny_named(self):
        abac = SubsetABAC(
            [
                (
                    {
                        "agent": "test",
                    },
                    RuleState.DENY,
                ),
            ],
        )
        toolbox = RestrictedToolbox(
            [multiply_tool],
            abac,
        )
        self.assertEqual(toolbox.list_tools(abac=TEST_ATTRIBUTES), [])

    def test_rule_allow_default(self):
        abac = SubsetABAC([], default_state=RuleState.ALLOW)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        self.assertEqual(
            toolbox.list_tools(abac=TEST_ATTRIBUTES), [multiply_tool.__name__]
        )

    def test_rule_deny_default(self):
        abac = SubsetABAC([], default_state=RuleState.DENY)
        toolbox = RestrictedToolbox([multiply_tool], abac)
        self.assertEqual(toolbox.list_tools(abac=TEST_ATTRIBUTES), [])
