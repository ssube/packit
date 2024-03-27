from logging import getLogger
from typing import Callable

from packit.agent import Agent, AgentContext
from packit.conditions import Condition, condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_function_example, get_random_prompt
from packit.results import multi_function_or_str_result
from packit.tools import Toolbox

logger = getLogger(__name__)


def loop_team(
    manager: Agent,
    workers: list[Agent],
    initial_prompt: str,
    iteration_prompt: str,
    context: AgentContext | None = None,
    toolbox: Toolbox | None = None,
    max_iterations: int = 10,
    memory: Callable | None = make_limited_memory,
    memory_maker: Callable | None = memory_order_width,
    result_parser: Callable[[str], str] | None = multi_function_or_str_result,
    stop_condition: Condition = condition_threshold,
    tool_filter: Callable[[dict], bool] | None = None,
) -> str:
    """
    Loop through a team of agents, with a manager and workers, to refine a prompt.
    """

    context = context or {}

    if callable(memory):
        memory = memory()

    current_iteration = 0

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

    while not stop_condition(max_iterations, current_iteration):
        result = manager(
            iteration_prompt
            + get_random_prompt("coworker")
            + get_random_prompt("function"),
            example=example,
            memory=memory,
            tools=toolbox.definitions if toolbox else None,
            workers=worker_names,
            **context,
        )
        if callable(result_parser):
            result = result_parser(result, toolbox=toolbox, tool_filter=tool_filter)

        if callable(memory_maker):
            memory_maker(memory, result)

        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return result
