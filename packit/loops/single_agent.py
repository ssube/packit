from logging import getLogger

from packit.agent import Agent, AgentContext
from packit.conditions import condition_or, condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.types import (
    MemoryFactory,
    MemoryMaker,
    PromptFilter,
    ResultParser,
    StopCondition,
)

from .base import loop_reduce

logger = getLogger(__name__)


def loop_retry(
    agent: Agent,
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    prompt_filter: PromptFilter | None = None,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a single agent, retrying until the result parser succeeds. If the result cannot be parsed, the prompt
    will be repeated with the error message.
    """

    last_error = None
    success = False

    def parse_or_error(value) -> str:
        nonlocal last_error
        nonlocal success

        try:
            if callable(result_parser):
                parsed = result_parser(value)
            else:
                parsed = value

            success = True
            return parsed
        except Exception as e:
            logger.warning(e)
            last_error = e
            return str(e)

    stop_condition_or_success = condition_or(stop_condition, lambda *args: success)

    # loop until the prompt succeeds
    result = loop_reduce(
        agents=[agent],
        prompt=prompt,
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        prompt_filter=prompt_filter,
        result_parser=parse_or_error,
        stop_condition=stop_condition_or_success,
    )

    if success:
        return result

    if last_error is None:
        raise ValueError("Failed to parse result")

    raise last_error
