from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_threshold
from packit.loops import loop_retry, select_loop
from packit.results import enum_result
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
    PromptType,
    ResultParser,
    StopCondition,
    ToolFilter,
)

RouteDict = dict[str, Agent]


def group_router(
    decider: Agent,
    prompt: PromptType,
    routes: RouteDict,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    """
    Route the prompt to the correct agent.
    """

    enum = list(routes.keys())

    def route_parser(value: str, **kwargs) -> str:
        choice = enum_result(value, enum=enum, **kwargs)
        if choice is None:
            raise ValueError("Please select a valid route.")
        if choice in routes:
            return choice
        raise ValueError("Invalid selection.")

    with trace("router", "packit.group") as (report_args, report_output):
        report_args(decider, prompt, context, enum=enum)

        decision = loop_retry(
            decider,
            prompt,  # TODO: add route prefix
            context=context,  # TODO: add route/expert list
            abac_context=abac_context,
            agent_invoker=agent_invoker,
            agent_selector=agent_selector,
            memory_factory=memory_factory,
            memory_maker=memory_maker,
            prompt_filter=prompt_filter,
            prompt_template=prompt_template,
            result_parser=route_parser,
            stop_condition=stop_condition,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )

        expert = routes[decision]
        result = loop_retry(
            expert,
            prompt,
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
