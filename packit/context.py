from contextlib import contextmanager
from logging import getLogger
from random import randint
from threading import local

from packit.agent import invoke_agent
from packit.conditions import condition_threshold
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

LOOP_CONTEXT_ATTR = "loop_context"

logger = getLogger(__name__)

thread_context = local()


class LoopContext:
    # context
    abac_context: ABACAttributes | None
    agent_invoker: AgentInvoker
    agent_selector: AgentSelector
    memory_factory: MemoryFactory | None
    memory_maker: MemoryMaker | None
    prompt_filter: PromptFilter | None
    prompt_template: PromptTemplate | None
    result_parser: ResultParser | None
    stop_condition: StopCondition
    toolbox: Toolbox | None
    tool_filter: ToolFilter | None

    # other
    depth: int
    tag: int

    def __init__(
        self,
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
        context_depth: int = 0,
    ):
        self.abac_context = abac_context
        self.agent_invoker = agent_invoker
        self.agent_selector = agent_selector
        self.memory_factory = memory_factory
        self.memory_maker = memory_maker
        self.prompt_filter = prompt_filter
        self.prompt_template = prompt_template
        self.result_parser = result_parser
        self.stop_condition = stop_condition
        self.toolbox = toolbox
        self.tool_filter = tool_filter

        # other
        self.depth = context_depth
        self.tag = randint(0, 1000000)


def count_loop_contexts() -> int:
    if hasattr(thread_context, LOOP_CONTEXT_ATTR):
        return len(getattr(thread_context, LOOP_CONTEXT_ATTR))

    return 0


def get_loop_context() -> LoopContext | None:
    if hasattr(thread_context, LOOP_CONTEXT_ATTR):
        contexts = getattr(thread_context, LOOP_CONTEXT_ATTR)
        if len(contexts) > 0:
            return contexts[-1]

    return None


def inherit_loop_context(
    parent_context: LoopContext | None = None,
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker | None = None,
    agent_selector: AgentSelector | None = None,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
) -> LoopContext:
    if parent_context:
        return LoopContext(
            abac_context=abac_context or parent_context.abac_context,
            agent_invoker=agent_invoker or parent_context.agent_invoker,
            agent_selector=agent_selector or parent_context.agent_selector,
            memory_factory=memory_factory or parent_context.memory_factory,
            memory_maker=memory_maker or parent_context.memory_maker,
            prompt_filter=prompt_filter or parent_context.prompt_filter,
            prompt_template=prompt_template or parent_context.prompt_template,
            result_parser=result_parser or parent_context.result_parser,
            stop_condition=stop_condition or parent_context.stop_condition,
            toolbox=toolbox or parent_context.toolbox,
            tool_filter=tool_filter or parent_context.tool_filter,
            context_depth=parent_context.depth + 1,
        )
    else:
        if agent_invoker is None:
            raise ValueError("agent_invoker is required")
        if agent_selector is None:
            raise ValueError("agent_selector is required")
        if stop_condition is None:
            raise ValueError("stop_condition is required")

        return LoopContext(
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


def push_loop_context(
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker | None = None,
    agent_selector: AgentSelector | None = None,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    save_context: bool = True,
) -> LoopContext:
    """
    Push a new loop context onto the stack. Fields that have not been set will be inherited from the current context.
    """

    current_context = get_loop_context()
    new_context = inherit_loop_context(
        parent_context=current_context,
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

    if save_context:
        loop_contexts = getattr(thread_context, LOOP_CONTEXT_ATTR, [])
        loop_contexts.append(new_context)
        setattr(thread_context, LOOP_CONTEXT_ATTR, loop_contexts)

    return new_context


def pop_loop_context() -> LoopContext | None:
    """
    Pop the current loop context off the stack.
    """

    loop_contexts = getattr(thread_context, LOOP_CONTEXT_ATTR, [])
    if loop_contexts and len(loop_contexts) > 0:
        return loop_contexts.pop()

    raise ValueError("No loop context to pop")


@contextmanager
def loopum(
    abac_context: ABACAttributes | None = None,
    agent_invoker: AgentInvoker = invoke_agent,
    agent_selector: AgentSelector = select_loop,
    memory_factory: MemoryFactory | None = None,
    memory_maker: MemoryMaker | None = None,
    prompt_filter: PromptFilter | None = None,
    prompt_template: PromptTemplate | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition | None = None,
    toolbox: Toolbox | None = None,
    tool_filter: ToolFilter | None = None,
    save_context: bool = True,
):
    """
    Context manager for setting loop context at the beginning of a loop and clearing it at the end.
    """
    context = push_loop_context(
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
    )
    if save_context:
        depth = count_loop_contexts()
        logger.debug(
            "entering loop context: depth %s/%s, tag %s",
            context.depth + 1,
            depth,
            context.tag,
        )
    try:
        yield context
    finally:
        if save_context:
            logger.debug(
                "leaving loop context: depth %s/%s, tag %s",
                context.depth + 1,
                depth,
                context.tag,
            )
            pop_loop_context()
