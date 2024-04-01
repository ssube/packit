from logging import getLogger
from typing import Protocol

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.context import DEFAULT_MAX_ITERATIONS, LoopContext, loopum
from packit.selectors import select_loop
from packit.toolbox import Toolbox
from packit.types import (
    AgentSelector,
    MemoryFactory,
    MemoryMaker,
    PromptFilter,
    PromptTemplate,
    ResultParser,
    StopCondition,
    ToolFilter,
)

logger = getLogger(__name__)


class BaseLoop(Protocol):
    def __call__(
        self,
        agents: list[Agent],
        prompt: str,
        context: AgentContext | None = None,
        agent_selector: AgentSelector = select_loop,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        loop_context: LoopContext | None = None,
        memory_factory: MemoryFactory | None = None,
        memory_maker: MemoryMaker | None = None,
        prompt_template: PromptTemplate | None = None,
        result_filter: PromptFilter | None = None,
        result_parser: ResultParser | None = None,
        stop_condition: StopCondition = condition_threshold,
        toolbox: Toolbox | None = None,
        tool_filter: ToolFilter | None = None,
    ) -> str | list[str]:
        pass  # pragma: no cover


def loop_map(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    agent_selector: AgentSelector = select_loop,
    loop_context: LoopContext | None = None,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    save_context: bool = True,
) -> list[str]:
    """
    Loop through a list of agents, passing the same prompt to each agent.
    """

    context = context or {}
    with loopum(
        agent_selector=agent_selector,
        max_iterations=max_iterations,
        memory_factory=memory_factory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
        save_context=save_context,
    ) as loop_context:
        if callable(loop_context.memory_factory):
            memory = loop_context.memory_factory()

        current_iteration = 0

        while not loop_context.stop_condition(
            loop_context.max_iterations, current_iteration
        ):
            agent = loop_context.agent_selector(agents, current_iteration)
            agent_prompt = prompt

            if callable(loop_context.prompt_filter):
                agent_prompt = loop_context.prompt_filter(agent_prompt)

            if agent_prompt is None:
                continue  # map continues, reduce stops

            result = agent(
                agent_prompt,
                **context,
                memory=memory,
                prompt_template=loop_context.prompt_template,
                toolbox=loop_context.toolbox,
            )

            if callable(loop_context.memory_maker):
                loop_context.memory_maker(memory, result)

            if callable(loop_context.result_parser):
                result = loop_context.result_parser(
                    result,
                    abac={
                        "subject": agent.name,
                    },
                    toolbox=loop_context.toolbox,
                    tool_filter=loop_context.tool_filter,
                )

            current_iteration += 1

        if current_iteration == loop_context.max_iterations:
            logger.warning("Max iterations reached")

        return memory or []


def loop_reduce(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    agent_selector: AgentSelector = select_loop,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
    memory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    save_context: bool = True,
) -> str:
    """
    Loop through a list of agents, passing the result of each agent on to the next.
    """

    context = context or {}
    with loopum(
        agent_selector=agent_selector,
        max_iterations=max_iterations,
        memory_factory=memory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
        save_context=save_context,
    ) as loop_context:
        if callable(loop_context.memory_factory):
            memory = loop_context.memory_factory()

        current_iteration = 0
        result = prompt

        while not loop_context.stop_condition(
            loop_context.max_iterations, current_iteration
        ):
            agent = loop_context.agent_selector(agents, current_iteration)

            if callable(loop_context.prompt_filter):
                result = loop_context.prompt_filter(result)

            if result is None:
                break  # map continues, reduce stops

            result = agent(
                result,
                **context,
                memory=memory,
                prompt_template=loop_context.prompt_template,
                toolbox=loop_context.toolbox,
            )

            if callable(loop_context.memory_maker):
                loop_context.memory_maker(memory, result)

            if callable(loop_context.result_parser):
                result = loop_context.result_parser(
                    result,
                    abac={
                        "subject": agent.name,
                    },
                    toolbox=loop_context.toolbox,
                    tool_filter=loop_context.tool_filter,
                )

            current_iteration += 1

        if current_iteration == loop_context.max_iterations:
            logger.warning("Max iterations reached")

        return result
