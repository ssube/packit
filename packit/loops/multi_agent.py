from logging import getLogger
from typing import Callable

from packit.agent import Agent, AgentContext
from packit.conditions import Condition, condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_random_prompt

from .builder import loop_prefix

logger = getLogger(__name__)


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
