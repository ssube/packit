from logging import getLogger
from typing import Callable

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.types import MemoryFactory, MemoryMaker, ResultParser, StopCondition

logger = getLogger(__name__)


BaseLoop = Callable[[list[Agent], str], list[str] | str]


def loop_map(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a list of agents, passing the same prompt to each agent.
    """

    context = context or {}

    if callable(memory):
        memory = memory()

    current_iteration = 0

    while not stop_condition(max_iterations, current_iteration):
        agent = agents[current_iteration % len(agents)]
        result = agent(prompt, **context, memory=memory)

        if callable(result_parser):
            result = result_parser(result)

        if callable(memory_maker):
            memory_maker(memory, result)

        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    # TODO: how will this work if memory is None?
    return memory


def loop_reduce(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a list of agents, passing the result of each agent on to the next.
    """

    context = context or {}

    if callable(memory):
        memory = memory()

    current_iteration = 0
    result = prompt

    while not stop_condition(max_iterations, current_iteration):
        agent = agents[current_iteration % len(agents)]
        result = agent(result, **context, memory=memory)

        if callable(result_parser):
            result = result_parser(result)

        if callable(memory_maker):
            memory_maker(memory, result)

        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return result
