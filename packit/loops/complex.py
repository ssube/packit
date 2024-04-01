""" """

from logging import getLogger

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_random_prompt
from packit.results import multi_function_or_str_result
from packit.toolbox import Toolbox
from packit.types import (
    MemoryFactory,
    MemoryMaker,
    PromptFilter,
    PromptTemplate,
    ResultParser,
    StopCondition,
    ToolFilter,
)

from .base import loop_reduce

logger = getLogger(__name__)


def loop_team(
    manager: Agent,
    workers: list[Agent],
    initial_prompt: str,
    iteration_prompt: str,
    context: AgentContext | None = None,
    toolbox: Toolbox | None = None,
    max_iterations: int = 10,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = multi_function_or_str_result,
    stop_condition: StopCondition | None = condition_threshold,
    tool_filter: ToolFilter | None = None,
) -> str:
    """
    Loop through a team of agents, with a manager and workers, to refine a prompt.

    TODO: tool_filter should be bound within the result parser
    """

    context = context or {}

    if callable(memory_factory):
        memory_factory = memory_factory()

    def get_memory():
        return memory_factory

    # prep names and tools
    worker_names = [worker.name for worker in workers]

    loop_context = {
        "coworkers": worker_names,
        **context,
    }

    result = manager(
        initial_prompt + get_random_prompt("coworker"),
        memory=memory_factory,
        **loop_context,
    )

    # TODO: wrap with retry loop, with the correct agent
    result = result_parser(
        result,
        abac={
            "subject": manager.name,
        },
        toolbox=toolbox,
        tool_filter=tool_filter,
    )

    return loop_reduce(
        [manager],
        iteration_prompt + get_random_prompt("coworker"),
        context=loop_context,
        max_iterations=max_iterations,
        memory_factory=get_memory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
    )
