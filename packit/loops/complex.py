"""
"""

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
from packit.utils import could_be_json

from .base import loop_reduce
from .single_agent import loop_retry

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

    if callable(memory):
        memory = memory()

    def get_memory():
        return memory

    # prep names and tools
    worker_names = [worker.name for worker in workers]

    loop_context = {
        "coworkers": worker_names,
        **context,
    }

    result = manager(
        initial_prompt + get_random_prompt("coworker"),
        memory=memory,
        **loop_context,
    )

    def result_parser_with_tools(value: str, **kwargs) -> str:
        if callable(result_parser):
            return result_parser(
                value, toolbox=toolbox, tool_filter=tool_filter, **kwargs
            )

        return value

    def result_parser_with_retry(value: str, **kwargs) -> str:
        retry_result = loop_retry(
            manager,  # should be the same agent over again, not necessarily the manager
            value,
            context=loop_context,
            max_iterations=3,
            prompt_filter=result_parser_with_tools,
            result_parser=result_parser_with_tools,
            stop_condition=stop_condition,
            toolbox=toolbox,
        )

        if could_be_json(retry_result):
            return result_parser_with_retry(retry_result, **kwargs)

        return retry_result

    result = result_parser_with_retry(result)

    return loop_reduce(
        [manager],
        iteration_prompt + get_random_prompt("coworker"),
        context=loop_context,
        max_iterations=max_iterations,
        memory=get_memory,
        memory_maker=memory_maker,
        prompt_filter=result_parser_with_retry,  # does the real prompt filter need to be included here?
        prompt_template=prompt_template,
        result_parser=result_parser_with_retry,
        stop_condition=stop_condition,
        toolbox=toolbox,
    )
