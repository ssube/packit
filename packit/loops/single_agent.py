from logging import getLogger

from packit.agent import Agent, AgentContext
from packit.conditions import condition_or, condition_threshold
from packit.memory import make_limited_memory, memory_order_width
from packit.types import MemoryFactory, MemoryMaker, ResultParser, StopCondition

from .base import loop_reduce

logger = getLogger(__name__)


def loop_retry(
    agent: Agent,
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    memory: MemoryFactory | None = make_limited_memory,
    memory_maker: MemoryMaker | None = memory_order_width,
    result_parser: ResultParser | None = None,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a single agent, retrying until the result parser succeeds. If the result cannot be parsed, the prompt
    will be repeated with the error message.
    """

    success = False

    def parse_or_error(value) -> str:
        nonlocal success

        try:
            parsed = result_parser(value)
            success = True
            return parsed
        except Exception as e:
            logger.error(e)
            return e

    stop_condition_or_success = condition_or(stop_condition, lambda *args: success)

    # loop until the prompt succeeds
    return loop_reduce(
        agents=[agent],
        prompt=prompt,
        context=context,
        max_iterations=max_iterations,
        memory=memory,
        memory_maker=memory_maker,
        result_parser=parse_or_error,
        stop_condition=stop_condition_or_success,
    )
