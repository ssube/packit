from logging import getLogger

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.prompts import get_random_prompt
from packit.types import (
    MemoryFactory,
    MemoryMaker,
    PromptTemplate,
    ResultParser,
    StopCondition,
)

from .base import BaseLoop, loop_reduce

logger = getLogger(__name__)


def loop_prefix(
    agents: list[Agent],
    prompt: str,
    prefix_prompt: str,
    context: AgentContext | None = None,
    base_loop: BaseLoop = loop_reduce,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_template: PromptTemplate | None = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
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
    base_loop: BaseLoop = loop_reduce,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_template: PromptTemplate | None = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
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
    base_loop: BaseLoop = loop_reduce,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_template: PromptTemplate | None = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
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
