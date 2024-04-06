from logging import getLogger
from typing import Any

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold_mean
from packit.loops import loop_retry
from packit.results import bool_result

logger = getLogger(__name__)


class Panel:
    agents: list[Agent]
    weights: list[int]

    def __init__(self, agents: dict[Agent, int]):
        self.agents = list(agents.keys())
        self.weights = list(agents.values())

    def sample(
        self, prompt: str, context: AgentContext, max_retry=3, parse_result=bool_result
    ) -> dict[str, str]:
        results = {}

        for agent, weight in zip(self.agents, self.weights):
            for i in range(weight):
                result = loop_retry(
                    agent,
                    prompt,
                    context=context,
                    result_parser=parse_result,
                    max_iterations=max_retry,
                )
                results[f"{agent.name}-{i}"] = result

        return results

    def invoke(
        self,
        prompt: str,
        context: AgentContext,
        parse_result=bool_result,
        decision_condition=condition_threshold_mean,
        min_threshold: float = 0.5,
    ) -> tuple[bool, dict[str, str]]:
        results = self.sample(prompt, context, parse_result=parse_result)
        values = list(results.values())

        return decision_condition(min_threshold, *values), results

    def __call__(self, prompt, **kwargs: Any) -> Any:
        return self.invoke(prompt, kwargs)
