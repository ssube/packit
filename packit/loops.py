from logging import getLogger

from packit.agent import Agent, AgentContext
from packit.conditions import Condition, condition_threshold
from packit.prompts import DEFAULT_PROMPTS, PromptTemplates, get_random_prompt

logger = getLogger(__name__)


def loop_converse(
    agents: list[Agent],
    prompt: str,
    context: AgentContext | None = None,
    max_iterations: int = 10,
    stop_condition: Condition = condition_threshold,
):
    """
    Loop through a list of agents and have them converse with each other.
    """
    context = context or {}

    agent_index = 0
    current_iteration = 0

    while not stop_condition(max_iterations, current_iteration):
        agent = agents[agent_index]
        prompt = agent(prompt, **context)

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
    stop_condition: Condition = condition_threshold,
    prompt_templates: PromptTemplates = DEFAULT_PROMPTS,
):
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
