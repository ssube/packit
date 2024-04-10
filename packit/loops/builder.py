from logging import getLogger

from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_threshold
from packit.prompts import get_random_prompt
from packit.selectors import select_loop
from packit.toolbox import Toolbox
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

from .base import BaseLoop, loop_reduce

logger = getLogger(__name__)


def loop_prefix(
    agents: Agent | list[Agent],
    prompt: PromptType,
    prefix_prompt: PromptType = "",
    context: AgentContext | None = None,
    base_loop: BaseLoop = loop_reduce,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str | list[str]:
    """
    Run a map or reduce loop, adding a prefix to the prompt each iteration.
    """

    agents = make_list(agents)

    def prefix_filter(value) -> str:
        if callable(prompt_filter):
            value = prompt_filter(value)

        return prompt_template(prefix_prompt) + " " + value

    return base_loop(
        agents,
        prompt,
        context=context,
        abac_context=abac_context,
        agent_invoker=agent_invoker,
        agent_selector=agent_selector,
        memory_factory=memory_factory,
        memory_maker=memory_maker,
        prompt_filter=prefix_filter,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
    )


def loop_suffix(
    agents: Agent | list[Agent],
    prompt: PromptType,
    suffix_prompt: PromptType = "",
    context: AgentContext | None = None,
    base_loop: BaseLoop = loop_reduce,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str | list[str]:
    """
    Run a map or reduce loop, adding a suffix to the prompt each iteration.
    """

    agents = make_list(agents)

    def suffix_filter(value) -> str:
        if callable(prompt_filter):
            value = prompt_filter(value)

        return value + " " + prompt_template(suffix_prompt)

    return base_loop(
        agents,
        prompt,
        context=context,
        abac_context=abac_context,
        agent_invoker=agent_invoker,
        agent_selector=agent_selector,
        memory_factory=memory_factory,
        memory_maker=memory_maker,
        prompt_filter=suffix_filter,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
    )


def loop_midfix(
    agents: Agent | list[Agent],
    prompt: PromptType,
    prefix_prompt: PromptType = "",
    suffix_prompt: PromptType = "",
    context: AgentContext | None = None,
    base_loop: BaseLoop = loop_reduce,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str | list[str]:
    """
    Run a map or reduce loop, adding a prefix and suffix to the prompt each iteration.
    """

    agents = make_list(agents)

    def midfix_filter(value) -> str:
        if callable(prompt_filter):
            value = prompt_filter(value)

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
        abac_context=abac_context,
        agent_invoker=agent_invoker,
        agent_selector=agent_selector,
        memory_factory=memory_factory,
        memory_maker=memory_maker,
        prompt_filter=midfix_filter,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
    )
