from logging import getLogger
from typing import List, Protocol

from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_threshold
from packit.context import INHERIT, OptionalInherited, RequiredInherited, loopum
from packit.selectors import select_loop
from packit.toolbox import Toolbox
from packit.tracing import SpanKind, trace
from packit.types import (
    ABACAttributes,
    AgentInvoker,
    AgentSelector,
    MemoryFactory,
    MemoryMaker,
    PromptFilter,
    PromptTemplate,
    PromptType,
    ResultParser,
    StopCondition,
    ToolFilter,
)
from packit.utils import make_list

logger = getLogger(__name__)


class BaseLoop(Protocol):
    def __call__(
        self,
        agents: Agent | list[Agent],
        prompt: PromptType,
        context: AgentContext | None = None,
        abac_context: OptionalInherited[ABACAttributes] = INHERIT,
        agent_invoker: RequiredInherited[AgentInvoker] = invoke_agent,
        agent_selector: RequiredInherited[AgentSelector] = select_loop,
        memory_factory: OptionalInherited[MemoryFactory] = INHERIT,
        memory_maker: OptionalInherited[MemoryMaker] = INHERIT,
        prompt_filter: OptionalInherited[PromptFilter] = INHERIT,
        prompt_template: OptionalInherited[PromptTemplate] = INHERIT,
        result_parser: OptionalInherited[ResultParser] = INHERIT,
        stop_condition: RequiredInherited[StopCondition] = condition_threshold,
        toolbox: OptionalInherited[Toolbox] = INHERIT,
        tool_filter: OptionalInherited[ToolFilter] = INHERIT,
        save_context: bool = True,
    ) -> PromptType:
        pass  # pragma: no cover


def loop_map(
    agents: Agent | list[Agent],
    prompt: PromptType,
    context: AgentContext | None = None,
    abac_context: OptionalInherited[ABACAttributes] = INHERIT,
    agent_invoker: OptionalInherited[AgentInvoker] = invoke_agent,
    agent_selector: OptionalInherited[AgentSelector] = select_loop,
    memory_factory: OptionalInherited[MemoryFactory] = INHERIT,
    memory_maker: OptionalInherited[MemoryMaker] = None,
    prompt_filter: OptionalInherited[PromptFilter] = INHERIT,
    prompt_template: OptionalInherited[PromptTemplate] = INHERIT,
    result_parser: OptionalInherited[ResultParser] = INHERIT,
    stop_condition: OptionalInherited[StopCondition] = condition_threshold,
    toolbox: OptionalInherited[Toolbox] = INHERIT,
    tool_filter: OptionalInherited[ToolFilter] = INHERIT,
    save_context: bool = True,
) -> List[PromptType]:
    """
    Loop through a list of agents, passing the same prompt to each agent.
    """

    agents = make_list(agents)
    context = context or {}

    with loopum(
        abac_context=abac_context,
        agent_invoker=agent_invoker,
        agent_selector=agent_selector,
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
        with trace("map", SpanKind.LOOP) as (report_args, report_output):
            report_args(agents, prompt, context)

            if callable(loop_context.memory_factory):
                history = loop_context.memory_factory()
            else:
                history = None

            current_iteration = 0
            results = []

            while not loop_context.stop_condition(current=current_iteration):
                agent = loop_context.agent_selector(agents, current_iteration)
                agent_prompt = prompt

                if callable(loop_context.prompt_filter):
                    agent_prompt = loop_context.prompt_filter(agent_prompt)

                if agent_prompt is None:
                    continue  # map continues, reduce stops

                result = agent_invoker(
                    agent,
                    agent_prompt,
                    context={
                        **context,
                        "history": history,
                    },
                    prompt_template=loop_context.prompt_template,
                    toolbox=loop_context.toolbox,
                )

                if callable(loop_context.memory_maker):
                    loop_context.memory_maker(history, result)

                if callable(loop_context.result_parser):
                    result = loop_context.result_parser(
                        result,
                        abac_context={
                            "subject": agent.name,
                        },
                        agent=agent,
                        toolbox=loop_context.toolbox,
                        tool_filter=loop_context.tool_filter,
                    )

                results.append(result)

                current_iteration += 1

            report_output(results)
            return results


def loop_reduce(
    agents: Agent | list[Agent],
    prompt: PromptType,
    context: AgentContext | None = None,
    abac_context: OptionalInherited[ABACAttributes] = INHERIT,
    agent_invoker: RequiredInherited[AgentInvoker] = invoke_agent,
    agent_selector: RequiredInherited[AgentSelector] = select_loop,
    memory_factory: OptionalInherited[MemoryFactory] = INHERIT,
    memory_maker: OptionalInherited[MemoryMaker] = INHERIT,
    prompt_filter: OptionalInherited[PromptFilter] = INHERIT,
    prompt_template: OptionalInherited[PromptTemplate] = INHERIT,
    result_parser: OptionalInherited[ResultParser] = INHERIT,
    stop_condition: RequiredInherited[StopCondition] = condition_threshold,
    toolbox: OptionalInherited[Toolbox] = INHERIT,
    tool_filter: OptionalInherited[ToolFilter] = INHERIT,
    save_context: bool = True,
) -> PromptType:
    """
    Loop through a list of agents, passing the result of each agent on to the next.
    """

    agents = make_list(agents)
    context = context or {}

    with loopum(
        abac_context=abac_context,
        agent_invoker=agent_invoker,
        agent_selector=agent_selector,
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
        with trace("reduce", SpanKind.LOOP) as (report_args, report_output):
            report_args(agents, prompt, context)

            if callable(loop_context.memory_factory):
                history = loop_context.memory_factory()
            else:
                history = None

            current_iteration = 0
            result = prompt

            while not loop_context.stop_condition(current=current_iteration):
                agent = loop_context.agent_selector(agents, current_iteration)

                if callable(loop_context.prompt_filter):
                    result = loop_context.prompt_filter(result)

                if result is None:
                    break  # map continues, reduce stops

                result = agent_invoker(
                    agent,
                    result,
                    context={
                        **context,
                        "history": history,
                    },
                    prompt_template=loop_context.prompt_template,
                    toolbox=loop_context.toolbox,
                )

                if callable(loop_context.memory_maker):
                    loop_context.memory_maker(history, result)

                if callable(loop_context.result_parser):
                    result = loop_context.result_parser(
                        result,
                        abac_context={
                            "subject": agent.name,
                        },
                        agent=agent,
                        toolbox=loop_context.toolbox,
                        tool_filter=loop_context.tool_filter,
                    )

                current_iteration += 1

            report_output(result)
            return result
