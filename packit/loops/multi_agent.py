from logging import getLogger

from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.prompts import get_random_prompt
from packit.selectors import select_loop
from packit.toolbox import Toolbox
from packit.tracing import trace
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

from .builder import loop_prefix

logger = getLogger(__name__)


def loop_converse(
    agents: Agent | list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    with trace("converse", "packit.loop") as (report_args, report_output):
        report_args(agents, prompt, context)
        result = loop_prefix(
            agents,
            prompt,
            "converse",
            context=context,
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
        )
        report_output(result)
        return result


def loop_extend(
    agents: Agent | list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    with trace("extend", "packit.loop") as (report_args, report_output):
        report_args(agents, prompt, context)
        result = loop_prefix(
            agents,
            prompt,
            "extend",
            context=context,
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
        )
        report_output(result)
        return result


def loop_refine(
    agents: Agent | list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate = get_random_prompt,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    with trace("refine", "packit.loop") as (report_args, report_output):
        report_args(agents, prompt, context)
        result = loop_prefix(
            agents,
            prompt,
            "refine",
            context=context,
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
        )
        report_output(result)
        return result
