""" """

from logging import getLogger

from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_random_prompt
from packit.results import multi_function_or_str_result
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
    ResultParser,
    StopCondition,
    ToolFilter,
)

from .base import loop_reduce
from .single_agent import loop_retry

logger = getLogger(__name__)


def loop_team(
    manager: Agent,
    workers: list[Agent],
    prompt: str,
    loop_prompt: str,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = multi_function_or_str_result,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    """
    Loop through a team of agents, with a manager and workers, to refine a prompt.
    """

    context = context or {}

    if callable(memory_factory):
        memory = memory_factory()
    else:
        memory = None

    def get_memory():
        return memory

    # prep names and tools
    worker_names = [worker.name for worker in workers]

    loop_context = {
        "coworkers": worker_names,
        **context,
    }

    result = loop_retry(
        manager,
        prompt + get_random_prompt("coworker"),
        context=loop_context,
        abac_context=abac_context,
        agent_invoker=agent_invoker,
        agent_selector=agent_selector,
        memory_factory=get_memory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
    )

    return loop_reduce(
        [manager],
        result + loop_prompt + get_random_prompt("coworker"),
        context=loop_context,
        abac_context=abac_context,
        agent_invoker=loop_retry,
        agent_selector=agent_selector,
        memory_factory=get_memory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        prompt_template=prompt_template,
        result_parser=result_parser,
        stop_condition=stop_condition,
        toolbox=toolbox,
        tool_filter=tool_filter,
    )
