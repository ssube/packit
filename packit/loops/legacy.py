from logging import getLogger
from typing import Callable

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold
from packit.prompts import get_function_example, get_random_prompt
from packit.results import ToolFilter, multi_function_or_str_result
from packit.types import StopCondition

logger = getLogger(__name__)

ToolDict = dict[str, Callable | tuple[Callable, Callable | None]]


def loop_converse(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a list of agents and have them converse with each other.
    """
    context = context or {}

    agent_index = 0
    current_iteration = 0

    while not stop_condition(max_iterations, current_iteration):
        agent = agents[agent_index]
        intro = get_random_prompt("converse")
        prompt = agent(intro + " " + prompt, **context)

        agent_index = (agent_index + 1) % len(agents)
        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return prompt


def loop_extend(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a list of agents to extend a prompt.
    """
    context = context or {}

    agent_index = 0
    current_iteration = 0

    while not stop_condition(max_iterations, current_iteration):
        agent = agents[agent_index]
        intro = get_random_prompt("extend")
        prompt = agent(intro + " " + prompt, **context)

        agent_index = (agent_index + 1) % len(agents)
        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return prompt


def loop_refine(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    stop_condition: StopCondition = condition_threshold,
) -> str:
    """
    Loop through a list of agents to refine a prompt.
    """
    context = context or {}

    agent_index = 0
    current_iteration = 0

    while not stop_condition(max_iterations, current_iteration):
        agent = agents[agent_index]
        intro = get_random_prompt("refine")
        prompt = agent(intro + " " + prompt, **context)

        agent_index = (agent_index + 1) % len(agents)
        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return prompt


def loop_team(
    manager: Agent,
    coworkers: list[Agent],
    tools: list[dict],
    tool_dict: dict[str, Callable],
    initial_prompt: str,
    loop_prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    result_parser: Callable[
        [str, ToolDict, ToolFilter], list[str]
    ] = multi_function_or_str_result,
    stop_condition: StopCondition = condition_threshold,
    tool_filter: Callable[[str], str] | None = None,
) -> str:
    """
    Loop through a team of agents to complete a task.
    """
    context = context or {}
    coworker_names = [coworker.name for coworker in coworkers]
    example = get_function_example()

    answers = []
    current_iteration = 0

    result = manager(
        initial_prompt + get_random_prompt("coworker") + get_random_prompt("function"),
        example=example,
        names=coworker_names,
        tools=tools,
        **context,
    )

    while not stop_condition(max_iterations, current_iteration):
        logger.info("Manager: %s", result)
        new_answers = result_parser(result, tool_dict, tool_filter=tool_filter)
        logger.debug("New answers: %s", new_answers)
        answers.extend(new_answers)

        result = manager(
            loop_prompt
            + get_random_prompt("coworker")
            + get_random_prompt("function")
            + get_random_prompt("answers"),
            answers=answers,
            example=example,
            names=coworker_names,
            tools=tools,
            **context,
        )
        current_iteration += 1

    if current_iteration == max_iterations:
        logger.warning("Max iterations reached")

    return result
