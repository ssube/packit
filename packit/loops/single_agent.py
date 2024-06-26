from logging import getLogger

from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_or, condition_threshold
from packit.context import INHERIT, loopum
from packit.memory import make_limited_memory, memory_order_width
from packit.results import multi_function_or_str_result
from packit.selectors import select_leader
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
from packit.utils import could_be_json, make_list

from .base import loop_reduce

logger = getLogger(__name__)


def loop_retry(
    agents: Agent | list[Agent],
    prompt: PromptType,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = INHERIT,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_leader,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = INHERIT,
    prompt_template: PromptTemplate | None = INHERIT,
    result_parser: ResultParser | None = INHERIT,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = INHERIT,
    tool_filter: ToolFilter | None = INHERIT,
) -> PromptType:
    """
    Loop through a single agent, retrying until the result parser succeeds. If the result cannot be parsed, the prompt
    will be repeated with the error message.
    """

    agent = select_leader(make_list(agents), 0)

    last_error: Exception | None = None
    success: bool = False

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
    ) as loop_context:
        with trace("retry", SpanKind.LOOP) as (report_args, report_output):
            report_args(agent, prompt, context)

            def parse_or_error(
                value: PromptType,
                **kwargs,
            ) -> str:
                nonlocal last_error
                nonlocal success

                try:
                    if callable(loop_context.result_parser):
                        parsed = loop_context.result_parser(
                            value,
                            **kwargs,
                        )
                    else:
                        parsed = value

                    success = True
                    return parsed
                except Exception as e:
                    logger.exception("Error parsing result: %s", value)
                    last_error = e
                    # TODO: check this conversion
                    return f"There was an error with your last response, please try again: {e}"

            stop_condition_or_success = condition_or(
                loop_context.stop_condition, lambda *args, **kwargs: success
            )

            # loop until the prompt succeeds
            result = loop_reduce(
                agents=agent,
                prompt=prompt,
                context=context,
                abac_context=loop_context.abac_context,
                agent_invoker=loop_context.agent_invoker,
                agent_selector=loop_context.agent_selector,
                memory_factory=loop_context.memory_factory,
                memory_maker=loop_context.memory_maker,
                prompt_filter=loop_context.prompt_filter,
                prompt_template=loop_context.prompt_template,
                result_parser=parse_or_error,
                stop_condition=stop_condition_or_success,
                toolbox=loop_context.toolbox,
                tool_filter=loop_context.tool_filter,
                save_context=False,
            )

            if success:
                report_output(result)
                return result

            if last_error:
                raise last_error

            # this is very difficult to reach, but here for completeness
            raise ValueError(
                "No error was raised, but the result could not be parsed."
            )  # pragma: no cover


def loop_tool(
    agents: Agent | list[Agent],
    prompt: PromptType,
    context: AgentContext | None = None,
    abac_context: ABACAttributes | None = INHERIT,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_leader,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = INHERIT,
    result_parser: ResultParser = multi_function_or_str_result,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = INHERIT,
    tool_filter: ToolFilter | None = INHERIT,
) -> PromptType:
    """
    Loop using a single agent, parsing the result as a function call until it is no longer JSON.
    """

    agent = agent_selector(make_list(agents), 0)

    with trace("tool", SpanKind.LOOP) as (report_args, report_output):
        report_args(agent, prompt, context)

        outer_result_parser = result_parser
        outer_toolbox = toolbox

        def result_parser_with_tools(
            value: str,
            result_parser=None,
            toolbox=None,
            **kwargs,
        ) -> str:
            inner_result_parser = result_parser or outer_result_parser
            inner_toolbox = toolbox or outer_toolbox

            if callable(inner_result_parser):
                value = inner_result_parser(
                    value,
                    result_parser=inner_result_parser,
                    toolbox=inner_toolbox,
                    **kwargs,
                )

            return value

        result = loop_retry(
            agent,
            prompt,
            context=context,
            abac_context=abac_context,
            agent_invoker=agent_invoker,
            agent_selector=agent_selector,
            memory_factory=memory_factory,
            memory_maker=memory_maker,
            prompt_filter=prompt_filter,
            result_parser=result_parser_with_tools,
            stop_condition=stop_condition,
            toolbox=toolbox,
            tool_filter=tool_filter,
        )

        while could_be_json(result):
            result = loop_retry(
                agent,
                result,
                context=context,
                abac_context=abac_context,
                agent_invoker=agent_invoker,
                agent_selector=agent_selector,
                memory_factory=memory_factory,
                memory_maker=memory_maker,
                prompt_filter=prompt_filter,
                result_parser=result_parser_with_tools,
                stop_condition=stop_condition,
                toolbox=toolbox,
                tool_filter=tool_filter,
            )

        report_output(result)
        return result
