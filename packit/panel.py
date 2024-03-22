from typing import Any

from packit.agent import Agent, AgentContext
from packit.conditions import condition_threshold_mean
from packit.results import bool_result


class Panel:
    agents: list[Agent]
    weights: list[int]

    def __init__(self, agents: dict[Agent, int]):
        self.agents = list(agents.keys())
        self.weights = list(agents.values())

    def invoke(self, prompt: str, context: AgentContext) -> dict[str, str]:
        results = {}

        for agent, weight in zip(self.agents, self.weights):
            for i in range(weight):
                result = agent.invoke(prompt, context)
                results[f"{agent.name}-{i}"] = result

        return results

    def decide(
        self,
        prompt: str,
        context: AgentContext,
        parse_result=bool_result,
        decision_condition=condition_threshold_mean,
        min_threshold: float = 0.5,
    ) -> tuple[bool, dict[str, str]]:
        results = self.invoke(prompt, context)
        values = [parse_result(result) for result in results.values()]

        return decision_condition(min_threshold, *values), results

    def __call__(self, prompt, **kwargs: Any) -> Any:
        return self.decide(prompt, kwargs)
