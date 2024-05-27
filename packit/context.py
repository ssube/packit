from contextlib import contextmanager
from logging import getLogger
from random import randint
from threading import local
from typing import Optional, TypeVar, Union

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


class InheritedValue:
    pass


INHERIT = InheritedValue()
CLEAR = None


InheritedType = TypeVar("InheritedType")

RequiredInherited = Union[InheritedType, InheritedValue]
OptionalInherited = Union[InheritedType, InheritedValue, None]


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


def inherit_required_value(
    value: RequiredInherited[InheritedType], parent_value: InheritedType
) -> InheritedType:
    if value is INHERIT:
        return parent_value

    return value


def inherit_optional_value(
    value: OptionalInherited[InheritedType], parent_value: InheritedType | None
) -> InheritedType | None:
    if value is INHERIT:
        return parent_value

    return value


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
    parent_context: Optional[LoopContext] = None,
    abac_context: OptionalInherited[ABACAttributes] = INHERIT,
    agent_invoker: RequiredInherited[AgentInvoker] = INHERIT,
    agent_selector: RequiredInherited[AgentSelector] = INHERIT,
    memory_factory: OptionalInherited[MemoryFactory] = INHERIT,
    memory_maker: OptionalInherited[MemoryMaker] = INHERIT,
    prompt_filter: OptionalInherited[PromptFilter] = INHERIT,
    prompt_template: OptionalInherited[PromptTemplate] = INHERIT,
    result_parser: OptionalInherited[ResultParser] = INHERIT,
    stop_condition: RequiredInherited[StopCondition] = INHERIT,
    toolbox: OptionalInherited[Toolbox] = INHERIT,
    tool_filter: OptionalInherited[ToolFilter] = INHERIT,
) -> LoopContext:
    if parent_context:
        return LoopContext(
            abac_context=inherit_optional_value(
                abac_context, parent_context.abac_context
            ),
            agent_invoker=inherit_optional_value(
                agent_invoker, parent_context.agent_invoker
            ),
            agent_selector=inherit_optional_value(
                agent_selector, parent_context.agent_selector
            ),
            memory_factory=inherit_optional_value(
                memory_factory, parent_context.memory_factory
            ),
            memory_maker=inherit_optional_value(
                memory_maker, parent_context.memory_maker
            ),
            prompt_filter=inherit_optional_value(
                prompt_filter, parent_context.prompt_filter
            ),
            prompt_template=inherit_optional_value(
                prompt_template, parent_context.prompt_template
            ),
            result_parser=inherit_optional_value(
                result_parser, parent_context.result_parser
            ),
            stop_condition=inherit_optional_value(
                stop_condition, parent_context.stop_condition
            ),
            toolbox=inherit_optional_value(toolbox, parent_context.toolbox),
            tool_filter=inherit_optional_value(tool_filter, parent_context.tool_filter),
            context_depth=parent_context.depth + 1,
        )
    else:
        # TODO: replace these with inherit_required, but that will need to throw?
        agent_invoker = inherit_optional_value(agent_invoker, None)
        if agent_invoker is None:
            raise ValueError("agent_invoker is required")

        agent_selector = inherit_optional_value(agent_selector, None)
        if agent_selector is None:
            raise ValueError("agent_selector is required")

        stop_condition = inherit_optional_value(stop_condition, None)
        if stop_condition is None:
            raise ValueError("stop_condition is required")

        return LoopContext(
            abac_context=inherit_optional_value(abac_context, None),
            agent_invoker=agent_invoker,
            agent_selector=agent_selector,
            memory_factory=inherit_optional_value(memory_factory, None),
            memory_maker=inherit_optional_value(memory_maker, None),
            prompt_filter=inherit_optional_value(prompt_filter, None),
            prompt_template=inherit_optional_value(prompt_template, None),
            result_parser=inherit_optional_value(result_parser, None),
            stop_condition=stop_condition,
            toolbox=inherit_optional_value(toolbox, None),
            tool_filter=inherit_optional_value(tool_filter, None),
        )


def push_loop_context(
    abac_context: OptionalInherited[ABACAttributes] = INHERIT,
    agent_invoker: RequiredInherited[AgentInvoker] = INHERIT,
    agent_selector: RequiredInherited[AgentSelector] = INHERIT,
    memory_factory: OptionalInherited[MemoryFactory] = INHERIT,
    memory_maker: OptionalInherited[MemoryMaker] = INHERIT,
    prompt_filter: OptionalInherited[PromptFilter] = INHERIT,
    prompt_template: OptionalInherited[PromptTemplate] = INHERIT,
    result_parser: OptionalInherited[ResultParser] = INHERIT,
    stop_condition: OptionalInherited[StopCondition] = INHERIT,
    toolbox: OptionalInherited[Toolbox] = INHERIT,
    tool_filter: OptionalInherited[ToolFilter] = INHERIT,
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
    abac_context: OptionalInherited[ABACAttributes] = INHERIT,
    agent_invoker: RequiredInherited[AgentInvoker] = invoke_agent,
    agent_selector: RequiredInherited[AgentSelector] = select_loop,
    memory_factory: OptionalInherited[MemoryFactory] = INHERIT,
    memory_maker: OptionalInherited[MemoryMaker] = INHERIT,
    prompt_filter: OptionalInherited[PromptFilter] = INHERIT,
    prompt_template: OptionalInherited[PromptTemplate] = INHERIT,
    result_parser: OptionalInherited[ResultParser] = INHERIT,
    stop_condition: OptionalInherited[StopCondition] = INHERIT,
    toolbox: OptionalInherited[Toolbox] = INHERIT,
    tool_filter: OptionalInherited[ToolFilter] = INHERIT,
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
