from logging import getLogger
from random import randint

from packit.agent import Agent, AgentContext, invoke_agent
from packit.conditions import condition_or, condition_threshold
from packit.context import loopum
from packit.memory import make_limited_memory, memory_order_width
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
    PromptType,
    ResultParser,
    StopCondition,
    ToolFilter,
)
from packit.utils import could_be_json

from .base import loop_reduce

logger = getLogger(__name__)


def loop_retry(
    agent: Agent,
    prompt: PromptType,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    memory: list[str] | None = None,  # TODO: remove
) -> str:
    """
    Loop through a single agent, retrying until the result parser succeeds. If the result cannot be parsed, the prompt
    will be repeated with the error message.
    """

    last_error: Exception | None = None
    success: bool = False

    with loopum(
        max_iterations=max_iterations,
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
        closure_tag = randint(0, 1000000)

        def parse_or_error(value, **kwargs) -> str:
            nonlocal last_error
            nonlocal success

            logger.debug("closure_tag: %s", closure_tag)

            try:
                if callable(loop_context.result_parser):
                    parsed = loop_context.result_parser(value, **kwargs)
                else:
                    parsed = value

                success = True
                return parsed
            except Exception as e:
                logger.exception("Error parsing result: %s", value)
                last_error = e
                # TODO: check this conversion
                return (
                    f"There was an error with your last response, please try again: {e}"
                )

        stop_condition_or_success = condition_or(
            loop_context.stop_condition, lambda *args: success
        )

        # loop until the prompt succeeds
        result = loop_reduce(
            agents=[agent],
            prompt=prompt,
            context=context,
            max_iterations=loop_context.max_iterations,
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
            return result

        raise last_error


def loop_tool(
    agent: Agent,
    prompt: PromptType,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    result_parser: ResultParser | None = multi_function_or_str_result,
    stop_condition: StopCondition = condition_threshold,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> str:
    """
    Loop using a single agent, parsing the result as a function call until it is no longer JSON.
    """

    outer_toolbox = toolbox

    def result_parser_with_tools(
        value: str, abac=None, toolbox=None, tool_filter=None
    ) -> str:
        if callable(result_parser):
            return result_parser(
                value,
                abac=abac,
                toolbox=toolbox or outer_toolbox,
                tool_filter=tool_filter,
            )

        return value

    result = loop_retry(
        agent,
        prompt,
        context=context,
        max_iterations=max_iterations,
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
            max_iterations=max_iterations,
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

    return result
