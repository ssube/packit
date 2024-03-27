from logging import getLogger

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_function_example, get_random_prompt
from packit.results import multi_function_or_str_result
from packit.tools import Toolbox
from packit.types import (
    MemoryFactory,
    MemoryMaker,
    PromptFilter,
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
    memory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    result_parser: ResultParser | None = multi_function_or_str_result,
    stop_condition: StopCondition | None = condition_threshold,
    tool_filter: ToolFilter | None = None,
) -> str:
    """
    Loop through a team of agents, with a manager and workers, to refine a prompt.

    TODO: tool_filter should be bound within the result parser
    """

    context = context or {}

    if callable(memory):
        memory = memory()

    def get_memory():
        return memory

    # prep names and tools
    worker_names = [worker.name for worker in workers]
    example = get_function_example()

    result = manager(
        initial_prompt + get_random_prompt("coworker") + get_random_prompt("function"),
        example=example,
        memory=memory,
        tools=toolbox.definitions if toolbox else None,
        workers=worker_names,
        **context,
    )

    if callable(result_parser):
        result = result_parser(result)

    return loop_reduce(
        [manager],
        iteration_prompt
        + get_random_prompt("coworker")
        + get_random_prompt("function"),
        context={
            "example": example,
            "memory": memory,
            "tools": toolbox.definitions if toolbox else None,
            "workers": worker_names,
            **context,
        },
        max_iterations=max_iterations,
        memory=get_memory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        result_parser=result_parser,
        stop_condition=stop_condition,
    )
