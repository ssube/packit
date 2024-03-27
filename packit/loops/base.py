from logging import getLogger
from typing import Protocol

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.selectors import select_loop
from packit.types import (
    AgentSelector,
    MemoryFactory,
    MemoryMaker,
    PromptFilter,
    ResultParser,
    StopCondition,
)

logger = getLogger(__name__)


class BaseLoop(Protocol):
    def __call__(
        self,
        agents: list[Agent],
        prompt: str,
        agent_selector: AgentSelector | None = select_loop,
        context: AgentContext | None = None,
        max_iterations: int = 10,
        memory: MemoryFactory | None = None,
        memory_maker: MemoryMaker | None = None,
        result_filter: PromptFilter | None = None,
        result_parser: ResultParser | None = None,
        stop_condition: StopCondition = condition_threshold,
    ) -> str | list[str]:
        pass


def loop_map(
    agents: list[Agent],
    prompt: str,
    agent_selector: AgentSelector | None = select_loop,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
) -> list[str]:
    """
    Loop through a list of agents, passing the same prompt to each agent.
    """

    context = context or {}

    if callable(memory):
        memory = memory()

    current_iteration = 0

    while not stop_condition(max_iterations, current_iteration):
        agent = agent_selector(agents, current_iteration)
        agent_prompt = prompt

        if callable(prompt_filter):
            agent_prompt = prompt_filter(agent_prompt)

        if agent_prompt is None:
            continue  # map continues, reduce stops

        result = agent(agent_prompt, **context, memory=memory)

        if callable(result_parser):
            result = result_parser(result)

        if callable(memory_maker):
            memory_maker(memory, result)

        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return memory or []


def loop_reduce(
    agents: list[Agent],
    prompt: str,
    agent_selector: AgentSelector | None = select_loop,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
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
        agent = agent_selector(agents, current_iteration)

        if callable(prompt_filter):
            result = prompt_filter(result)

        if result is None:
            break  # map continues, reduce stops

        result = agent(result, **context, memory=memory)

        if callable(result_parser):
            result = result_parser(result)

        if callable(memory_maker):
            memory_maker(memory, result)

        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return result
