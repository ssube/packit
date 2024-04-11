from unittest import TestCase

from packit.context import (
    count_loop_contexts,
    inherit_loop_context,
    pop_loop_context,
    push_loop_context,
)


class TestCountLoopContexts(TestCase):
    def test_count_loop_contexts(self):
        necessary_params = {
            "agent_invoker": lambda x: x,
            "agent_selector": lambda x: x,
            "stop_condition": lambda x: x,
        }

        self.assertEqual(count_loop_contexts(), 0)

        push_loop_context(**necessary_params)
        self.assertEqual(count_loop_contexts(), 1)

        push_loop_context(**necessary_params)
        self.assertEqual(count_loop_contexts(), 2)

        pop_loop_context()
        self.assertEqual(count_loop_contexts(), 1)

        pop_loop_context()
        self.assertEqual(count_loop_contexts(), 0)

    def test_count_empty(self):
        self.assertEqual(count_loop_contexts(), 0)

    def test_pop_empty(self):
        with self.assertRaises(ValueError):
            pop_loop_context()

    def test_inherit_missing_agent_invoker(self):
        with self.assertRaises(ValueError):
            inherit_loop_context(agent_selector=lambda x: x, stop_condition=lambda x: x)

    def test_inherit_missing_agent_selector(self):
        with self.assertRaises(ValueError):
            inherit_loop_context(agent_invoker=lambda x: x, stop_condition=lambda x: x)

    def test_inherit_missing_stop_condition(self):
        with self.assertRaises(ValueError):
            inherit_loop_context(agent_invoker=lambda x: x, agent_selector=lambda x: x)
