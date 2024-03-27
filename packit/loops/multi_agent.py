from logging import getLogger
from typing import Callable

from packit.agent import Agent, AgentContext
from packit.conditions import Condition, condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_random_prompt

from .base import loop_reduce

logger = getLogger(__name__)


def loop_prefix(
    agents: list[Agent],
    prompt: str,
    prefix_prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: Callable | None = None,
    memory_maker: Callable | None = None,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    """
    Loop through a list of agents and have them converse with each other.
    """

    def prefix_parser(value) -> str:
        if callable(result_parser):
            value = result_parser(value)

        return prompt_template(prefix_prompt) + " " + value

    return loop_reduce(
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
    max_iterations: int = 10,
    memory: Callable | None = None,
    memory_maker: Callable | None = None,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    """
    Loop through a list of agents and have them converse with each other.
    """

    def suffix_parser(value) -> str:
        if callable(result_parser):
            value = result_parser(value)

        return value + " " + prompt_template(suffix_prompt)

    return loop_reduce(
        agents,
        prompt,
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        result_parser=suffix_parser,
        stop_condition=stop_condition,
    )


def loop_converse(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: Callable | None = make_limited_memory,
    memory_maker: Callable | None = memory_order_width,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    return loop_prefix(
        agents,
        prompt,
        "converse",
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
    )


def loop_extend(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: Callable | None = make_limited_memory,
    memory_maker: Callable | None = memory_order_width,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    return loop_prefix(
        agents,
        prompt,
        "extend",
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
    )


def loop_refine(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: Callable | None = make_limited_memory,
    memory_maker: Callable | None = memory_order_width,
    prompt_template: Callable | None = get_random_prompt,
    result_parser: Callable[[str], str] | None = None,
    stop_condition: Condition = condition_threshold,
) -> str:
    return loop_prefix(
        agents,
        prompt,
        "refine",
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
    )
