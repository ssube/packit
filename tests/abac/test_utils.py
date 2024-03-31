from unittest import TestCase

from packit.abac import make_rule


class TestMakeRule(TestCase):
    def test_make_rule(self):
        rule, state = make_rule("subject", "resource", "action")
        self.assertEqual(
            rule, {"subject": "subject", "resource": "resource", "action": "action"}
        )

    def test_partial_rules(self):
        rule, state = make_rule("subject", "resource")
        self.assertEqual(rule, {"subject": "subject", "resource": "resource"})

        rule, state = make_rule("subject", action="action")
        self.assertEqual(rule, {"subject": "subject", "action": "action"})

        rule, state = make_rule(resource="resource", action="action")
        self.assertEqual(rule, {"resource": "resource", "action": "action"})

    def test_context_rule(self):
        rule, state = make_rule(
            "subject", "resource", "action", context={"key": "value"}
        )
        self.assertEqual(
            rule,
            {
                "subject": "subject",
                "resource": "resource",
                "action": "action",
                "key": "value",
            },
        )
