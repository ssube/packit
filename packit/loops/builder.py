from logging import getLogger
from typing import Callable

from packit.agent import Agent, AgentContext
from packit.conditions import Condition, condition_threshold
from packit.prompts import get_random_prompt

from .base import loop_reduce

logger = getLogger(__name__)


def loop_prefix(
    agents: list[Agent],
    prompt: str,
    prefix_prompt: str,
    context: AgentContext | None = None,
    base_loop: Callable = loop_reduce,
    max_iterations: int = 10,
    memory: Callable | None = None,
    memory_maker: Callable | None = None,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    """
    Run a map or reduce loop, adding a prefix to the prompt each iteration.
    """

    def prefix_parser(value) -> str:
        if callable(result_parser):
            value = result_parser(value)

        return prompt_template(prefix_prompt) + " " + value

    return base_loop(
        agents,
        prompt,
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        result_parser=prefix_parser,
        stop_condition=stop_condition,
    )


def loop_suffix(
    agents: list[Agent],
    prompt: str,
    suffix_prompt: str,
    context: AgentContext | None = None,
    base_loop: Callable = loop_reduce,
    max_iterations: int = 10,
    memory: Callable | None = None,
    memory_maker: Callable | None = None,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    """
    Run a map or reduce loop, adding a suffix to the prompt each iteration.
    """

    def suffix_parser(value) -> str:
        if callable(result_parser):
            value = result_parser(value)

        return value + " " + prompt_template(suffix_prompt)

    return base_loop(
        agents,
        prompt,
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        result_parser=suffix_parser,
        stop_condition=stop_condition,
    )


def loop_midfix(
    agents: list[Agent],
    prompt: str,
    prefix_prompt: str,
    suffix_prompt: str,
    context: AgentContext | None = None,
    base_loop: Callable = loop_reduce,
    max_iterations: int = 10,
    memory: Callable | None = None,
    memory_maker: Callable | None = None,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    """
    Run a map or reduce loop, adding a prefix and suffix to the prompt each iteration.
    """

    def midfix_parser(value) -> str:
        if callable(result_parser):
            value = result_parser(value)

        return (
            prompt_template(prefix_prompt)
            + " "
            + value
            + " "
            + prompt_template(suffix_prompt)
        )

    return base_loop(
        agents,
        prompt,
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        result_parser=midfix_parser,
        stop_condition=stop_condition,
    )
